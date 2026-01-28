---
name: trader-analysis
description: Analyze Polymarket traders, identify profitable traders to follow, and track their performance. Use when building copy trading features or trader discovery.
---

# Trader Analysis Skill

## Tracking Trader Activity

### On-Chain Data
```python
from web3 import Web3
import httpx
from typing import AsyncIterator

CTF_EXCHANGE = "0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E"

class TraderTracker:
    def __init__(self, polygon_rpc: str):
        self.w3 = Web3(Web3.HTTPProvider(polygon_rpc))
        self.exchange = self.w3.eth.contract(
            address=CTF_EXCHANGE,
            abi=CTF_EXCHANGE_ABI
        )
    
    async def get_trader_trades(
        self,
        address: str,
        from_block: int = None
    ) -> list[dict]:
        """Fetch all trades for an address."""
        events = self.exchange.events.OrderFilled.get_logs(
            fromBlock=from_block or "earliest",
            argument_filters={"maker": address}
        )
        
        return [self._parse_trade_event(e) for e in events]
    
    def _parse_trade_event(self, event: dict) -> dict:
        """Parse OrderFilled event into trade dict."""
        return {
            "tx_hash": event.transactionHash.hex(),
            "block_number": event.blockNumber,
            "maker": event.args.maker,
            "taker": event.args.taker,
            "token_id": str(event.args.tokenId),
            "amount": event.args.amount / 1e6,  # Assuming 6 decimals
            "price": event.args.price / 1e18,
            "side": "BUY" if event.args.side == 0 else "SELL",
            "timestamp": self._get_block_timestamp(event.blockNumber)
        }
```

### Polymarket Data API
```python
class PolymarketDataClient:
    BASE_URL = "https://data-api.polymarket.com"
    
    def __init__(self):
        self.client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            timeout=30.0
        )
    
    async def get_trader_profile(self, address: str) -> dict:
        """Fetch trader profile and stats."""
        response = await self.client.get(f"/users/{address}")
        response.raise_for_status()
        return response.json()
    
    async def get_trader_positions(self, address: str) -> list[dict]:
        """Get all positions for a trader."""
        response = await self.client.get(
            "/positions",
            params={"user": address}
        )
        response.raise_for_status()
        return response.json()
    
    async def get_trader_activity(
        self,
        address: str,
        limit: int = 100,
        offset: int = 0
    ) -> list[dict]:
        """Get recent trading activity."""
        response = await self.client.get(
            "/activity",
            params={
                "user": address,
                "limit": limit,
                "offset": offset
            }
        )
        response.raise_for_status()
        return response.json()
    
    async def get_leaderboard(
        self,
        period: str = "all",
        limit: int = 100
    ) -> list[dict]:
        """Get top traders by P&L."""
        response = await self.client.get(
            "/leaderboard",
            params={"period": period, "limit": limit}
        )
        response.raise_for_status()
        return response.json()
```

## Trader Scoring System

```python
from dataclasses import dataclass
from datetime import datetime, timedelta
import numpy as np
from typing import Optional

@dataclass
class TraderMetrics:
    address: str
    total_pnl: float
    realized_pnl: float
    unrealized_pnl: float
    win_rate: float
    avg_return_per_trade: float
    sharpe_ratio: float
    total_trades: int
    unique_markets: int
    avg_position_size: float
    avg_hold_time: timedelta
    consistency_score: float
    recency_score: float
    largest_win: float
    largest_loss: float
    profit_factor: float  # gross profit / gross loss

class TraderAnalyzer:
    def __init__(self, data_client: PolymarketDataClient):
        self.client = data_client
    
    async def analyze_trader(
        self,
        address: str,
        days: int = 90
    ) -> TraderMetrics:
        """Comprehensive trader analysis."""
        activity = await self.client.get_trader_activity(
            address, limit=1000
        )
        positions = await self.client.get_trader_positions(address)
        
        # Filter to time period
        cutoff = datetime.utcnow() - timedelta(days=days)
        recent_trades = [
            t for t in activity
            if datetime.fromisoformat(t["timestamp"]) > cutoff
        ]
        
        return TraderMetrics(
            address=address,
            total_pnl=self._calculate_total_pnl(positions, recent_trades),
            realized_pnl=self._calculate_realized_pnl(recent_trades),
            unrealized_pnl=self._calculate_unrealized_pnl(positions),
            win_rate=self._calculate_win_rate(recent_trades),
            avg_return_per_trade=self._calculate_avg_return(recent_trades),
            sharpe_ratio=self._calculate_sharpe(recent_trades),
            total_trades=len(recent_trades),
            unique_markets=len(set(t["market_id"] for t in recent_trades)),
            avg_position_size=self._calculate_avg_size(recent_trades),
            avg_hold_time=self._calculate_avg_hold_time(recent_trades),
            consistency_score=self._calculate_consistency(recent_trades),
            recency_score=self._calculate_recency_score(recent_trades),
            largest_win=max((t.get("pnl", 0) for t in recent_trades), default=0),
            largest_loss=min((t.get("pnl", 0) for t in recent_trades), default=0),
            profit_factor=self._calculate_profit_factor(recent_trades)
        )
    
    def _calculate_win_rate(self, trades: list[dict]) -> float:
        """Calculate percentage of profitable trades."""
        if not trades:
            return 0
        
        winning = sum(1 for t in trades if t.get("pnl", 0) > 0)
        return winning / len(trades)
    
    def _calculate_sharpe(self, trades: list[dict]) -> float:
        """Calculate Sharpe ratio of returns."""
        returns = [t.get("return_pct", 0) for t in trades if "return_pct" in t]
        
        if len(returns) < 2:
            return 0
        
        mean_return = np.mean(returns)
        std_return = np.std(returns)
        
        if std_return == 0:
            return 0
        
        # Annualize assuming daily trades
        return (mean_return * 365**0.5) / std_return
    
    def _calculate_consistency(self, trades: list[dict]) -> float:
        """Score how consistent the trader's performance is."""
        if len(trades) < 10:
            return 0
        
        # Group by week
        weekly_pnl = {}
        for trade in trades:
            week = datetime.fromisoformat(trade["timestamp"]).isocalendar()[:2]
            weekly_pnl[week] = weekly_pnl.get(week, 0) + trade.get("pnl", 0)
        
        if len(weekly_pnl) < 4:
            return 0
        
        # Calculate consistency as % of profitable weeks
        profitable_weeks = sum(1 for pnl in weekly_pnl.values() if pnl > 0)
        return profitable_weeks / len(weekly_pnl)
    
    def _calculate_recency_score(self, trades: list[dict]) -> float:
        """Score based on recent activity (more recent = higher)."""
        if not trades:
            return 0
        
        latest = max(
            datetime.fromisoformat(t["timestamp"]) for t in trades
        )
        days_since = (datetime.utcnow() - latest).days
        
        # Decay score over 30 days
        return max(0, 1 - (days_since / 30))
    
    def _calculate_profit_factor(self, trades: list[dict]) -> float:
        """Gross profit / gross loss."""
        gross_profit = sum(t.get("pnl", 0) for t in trades if t.get("pnl", 0) > 0)
        gross_loss = abs(sum(t.get("pnl", 0) for t in trades if t.get("pnl", 0) < 0))
        
        if gross_loss == 0:
            return float('inf') if gross_profit > 0 else 0
        
        return gross_profit / gross_loss


class TraderScorer:
    def __init__(self, weights: dict = None):
        self.weights = weights or {
            "pnl": 0.20,
            "win_rate": 0.15,
            "sharpe": 0.15,
            "consistency": 0.15,
            "recency": 0.10,
            "profit_factor": 0.10,
            "experience": 0.10,
            "diversity": 0.05
        }
    
    def calculate_score(self, metrics: TraderMetrics) -> float:
        """Calculate overall trader score (0-100)."""
        scores = {
            "pnl": self._normalize_pnl(metrics.total_pnl),
            "win_rate": metrics.win_rate * 100,
            "sharpe": self._normalize_sharpe(metrics.sharpe_ratio),
            "consistency": metrics.consistency_score * 100,
            "recency": metrics.recency_score * 100,
            "profit_factor": self._normalize_profit_factor(metrics.profit_factor),
            "experience": self._normalize_trades(metrics.total_trades),
            "diversity": self._normalize_markets(metrics.unique_markets)
        }
        
        return sum(scores[k] * self.weights[k] for k in self.weights)
    
    def _normalize_pnl(self, pnl: float) -> float:
        """Normalize P&L to 0-100 scale."""
        if pnl <= 0:
            return max(0, 50 + pnl / 1000)
        return min(100, 50 + np.log1p(pnl) * 8)
    
    def _normalize_sharpe(self, sharpe: float) -> float:
        """Normalize Sharpe ratio to 0-100."""
        # Sharpe of 2+ is excellent
        return min(100, max(0, sharpe * 33))
    
    def _normalize_profit_factor(self, pf: float) -> float:
        """Normalize profit factor to 0-100."""
        if pf == float('inf'):
            return 100
        # PF of 2+ is good
        return min(100, pf * 40)
    
    def _normalize_trades(self, trades: int) -> float:
        """Normalize trade count to 0-100."""
        # 100+ trades shows experience
        return min(100, trades)
    
    def _normalize_markets(self, markets: int) -> float:
        """Normalize unique markets to 0-100."""
        # Trading 10+ markets shows diversity
        return min(100, markets * 10)
```

## Finding Traders to Follow

```python
class TraderDiscovery:
    def __init__(
        self,
        data_client: PolymarketDataClient,
        analyzer: TraderAnalyzer
    ):
        self.client = data_client
        self.analyzer = analyzer
        self.scorer = TraderScorer()
    
    async def find_top_traders(
        self,
        min_trades: int = 50,
        min_pnl: float = 1000,
        min_win_rate: float = 0.5,
        days: int = 30
    ) -> list[tuple[str, float, TraderMetrics]]:
        """Discover top performing traders."""
        leaderboard = await self.client.get_leaderboard(limit=500)
        
        candidates = []
        for trader in leaderboard:
            try:
                metrics = await self.analyzer.analyze_trader(
                    trader["address"],
                    days=days
                )
                
                # Apply filters
                if (metrics.total_trades >= min_trades and
                    metrics.total_pnl >= min_pnl and
                    metrics.win_rate >= min_win_rate):
                    
                    score = self.scorer.calculate_score(metrics)
                    candidates.append((trader["address"], score, metrics))
            except Exception as e:
                # Skip traders with errors
                continue
        
        return sorted(candidates, key=lambda x: x[1], reverse=True)
    
    async def find_market_specialists(
        self,
        market_category: str,
        min_trades_in_category: int = 20
    ) -> list[str]:
        """Find traders who specialize in specific market categories."""
        # Implementation would query by category
        pass
    
    async def find_original_traders(
        self,
        min_originality_score: float = 0.7
    ) -> list[str]:
        """
        Find traders who make original trades (not copy trading).
        
        Originality is measured by:
        - Trade timing (not consistently after other traders)
        - Position uniqueness (not mirroring others)
        - Contrarian indicators
        """
        leaderboard = await self.client.get_leaderboard(limit=200)
        original_traders = []
        
        for trader in leaderboard:
            activity = await self.client.get_trader_activity(
                trader["address"],
                limit=100
            )
            
            originality = await self._calculate_originality(activity)
            
            if originality >= min_originality_score:
                original_traders.append(trader["address"])
        
        return original_traders
    
    async def _calculate_originality(
        self,
        trades: list[dict]
    ) -> float:
        """Calculate how original a trader's trades are."""
        # Compare trade timing with market average
        # Check for unique position entries
        # Measure contrarian behavior
        return 0.5  # Placeholder


class CopyTradingManager:
    def __init__(
        self,
        data_client: PolymarketDataClient,
        trading_service,  # Your trading service
        config: dict
    ):
        self.client = data_client
        self.trading = trading_service
        self.tracked_traders: dict[str, dict] = {}
        self.copy_delay = config.get("copy_delay_seconds", 30)
        self.size_multiplier = config.get("size_multiplier", 0.25)
        self.max_position_pct = config.get("max_position_pct", 0.1)
    
    def add_trader(
        self,
        address: str,
        multiplier: float = None,
        markets: list[str] = None
    ):
        """Add a trader to copy."""
        self.tracked_traders[address] = {
            "multiplier": multiplier or self.size_multiplier,
            "markets": markets,  # None = all markets
            "last_trade": None
        }
    
    def remove_trader(self, address: str):
        """Stop copying a trader."""
        self.tracked_traders.pop(address, None)
    
    async def process_trade(self, trade: dict):
        """Process a trade from tracked trader."""
        address = trade["trader_address"]
        
        if address not in self.tracked_traders:
            return
        
        config = self.tracked_traders[address]
        
        # Check market filter
        if config["markets"] and trade["market_id"] not in config["markets"]:
            return
        
        # Wait for delay
        await asyncio.sleep(self.copy_delay)
        
        # Calculate size
        size = trade["size"] * config["multiplier"]
        
        # Apply max position limit
        portfolio = await self.trading.get_portfolio()
        max_size = portfolio["value"] * self.max_position_pct / trade["price"]
        size = min(size, max_size)
        
        # Execute copy trade
        await self.trading.place_order(
            token_id=trade["token_id"],
            side=trade["side"],
            price=trade["price"],
            size=size,
            metadata={"copy_source": address}
        )
```

## Real-Time Monitoring

```python
import asyncio
from collections import defaultdict
from typing import Callable, Awaitable

class LiveTraderMonitor:
    def __init__(self, tracked_addresses: list[str]):
        self.tracked = set(tracked_addresses)
        self.callbacks: dict[str, list[Callable]] = defaultdict(list)
        self._running = False
    
    def on_trade(self, callback: Callable[[dict], Awaitable[None]]):
        """Register callback for trade events."""
        self.callbacks["trade"].append(callback)
        return callback
    
    def on_position_change(self, callback: Callable[[dict], Awaitable[None]]):
        """Register callback for position changes."""
        self.callbacks["position"].append(callback)
        return callback
    
    async def start(self):
        """Start monitoring tracked traders."""
        self._running = True
        
        async for event in self._watch_events():
            if not self._running:
                break
            
            if event.get("trader") in self.tracked:
                event_type = event.get("type", "trade")
                
                for callback in self.callbacks[event_type]:
                    try:
                        await callback(event)
                    except Exception as e:
                        print(f"Callback error: {e}")
    
    def stop(self):
        """Stop monitoring."""
        self._running = False
    
    def add_trader(self, address: str):
        """Add trader to watch list."""
        self.tracked.add(address)
    
    def remove_trader(self, address: str):
        """Remove trader from watch list."""
        self.tracked.discard(address)
    
    async def _watch_events(self):
        """Watch for on-chain events."""
        # Implementation would use WebSocket or polling
        while self._running:
            # Poll for new events
            await asyncio.sleep(5)
            yield {}  # Placeholder
```
