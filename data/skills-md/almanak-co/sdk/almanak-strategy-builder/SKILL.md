---
name: almanak-strategy-builder
description: >-
  Build, test, and deploy DeFi trading strategies using the Almanak SDK.
  ALWAYS use this skill when the user mentions almanak, DeFi strategy,
  trading strategy, yield farming, liquidity provision, token swap,
  borrowing, lending, perpetuals, staking, vault deposit, bridging tokens,
  backtesting, paper trading, or on-chain execution. Use for writing
  strategy.py files, composing intents (Swap, LP, Borrow, Supply, Perp,
  Bridge, Stake, Vault, Prediction), working with config.json strategy
  parameters, running almanak strat or almanak gateway CLI commands, or
  debugging strategy execution on Anvil forks. Do NOT use for general
  smart contract development, Solidity code, or non-strategy SDK internals.
metadata:
  version: "2.0.0"
  author: Almanak
  license: Apache-2.0
---

# Almanak Strategy Builder

You are helping a quant build DeFi strategies using the Almanak SDK.
Strategies are Python classes that return Intent objects. The framework handles
compilation to transactions, execution, and state management.

<!-- almanak-sdk-start: quick-start -->

## Quick Start

```bash
# Install
pip install almanak

# Scaffold a new strategy
almanak strat new --template mean_reversion --name my_rsi --chain arbitrum

# Run on local Anvil fork (auto-starts gateway + Anvil)
cd my_rsi
almanak strat run --network anvil --once

# Run a single iteration on mainnet
almanak strat run --once

# Browse and copy a working demo strategy
almanak strat demo
```

**Minimal strategy (3 files):**

```
my_strategy/
  strategy.py    # IntentStrategy subclass with decide() method
  config.json    # Runtime parameters (chain, tokens, thresholds)
  .env           # Secrets (ALMANAK_PRIVATE_KEY, ALCHEMY_API_KEY)
```

For Anvil testing, add `anvil_funding` to `config.json` so your wallet is auto-funded on fork start
(see [Configuration](#configuration) below).

```python
# strategy.py
from decimal import Decimal
from almanak.framework.strategies import IntentStrategy, MarketSnapshot, almanak_strategy
from almanak.framework.intents import Intent

@almanak_strategy(
    name="my_strategy",
    version="1.0.0",
    supported_chains=["arbitrum"],
    supported_protocols=["uniswap_v3"],
    intent_types=["SWAP", "HOLD"],
)
class MyStrategy(IntentStrategy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trade_size = Decimal(str(self.config.get("trade_size_usd", "100")))

    def decide(self, market: MarketSnapshot) -> Intent | None:
        rsi = market.rsi("WETH", period=14)
        if rsi.value < 30:
            return Intent.swap(
                from_token="USDC", to_token="WETH",
                amount_usd=self.trade_size, max_slippage=Decimal("0.005"),
            )
        return Intent.hold(reason=f"RSI={rsi.value:.1f}, waiting")
```

> **Note:** `amount_usd=` requires a live price oracle from the gateway. If swaps revert with
> "Too little received", switch to `amount=` (token units) which bypasses USD-to-token conversion.
> Always verify pricing on first live run with `--dry-run --once`.

<!-- almanak-sdk-end: quick-start -->

<!-- almanak-sdk-start: core-concepts -->

## Core Concepts

### IntentStrategy

All strategies inherit from `IntentStrategy` and implement one method:

```python
def decide(self, market: MarketSnapshot) -> Intent | None
```

The framework calls `decide()` on each iteration with a fresh `MarketSnapshot`.
Return an `Intent` object (swap, LP, borrow, etc.) or `Intent.hold()`.

### Lifecycle

1. `__init__`: Extract config parameters, set up state
2. `decide(market)`: Called each iteration - return an Intent
3. `on_intent_executed(intent, success, result)`: Optional callback after execution
4. `get_status()`: Optional - return dict for monitoring dashboards
5. `supports_teardown()` / `generate_teardown_intents()`: Optional safe shutdown

### @almanak_strategy Decorator

Attaches metadata used by the framework and CLI:

```python
@almanak_strategy(
    name="my_strategy",              # Unique identifier
    description="What it does",      # Human-readable description
    version="1.0.0",                 # Strategy version
    author="Your Name",              # Optional
    tags=["trading", "rsi"],         # Optional tags for discovery
    supported_chains=["arbitrum"],   # Which chains this runs on
    supported_protocols=["uniswap_v3"],  # Which protocols it uses
    intent_types=["SWAP", "HOLD"],   # Intent types it may return
)
```

### Config Access

In `__init__`, read parameters from `self.config` (dict loaded from config.json):

```python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.trade_size = Decimal(str(self.config.get("trade_size_usd", "100")))
    self.rsi_period = int(self.config.get("rsi_period", 14))
    self.base_token = self.config.get("base_token", "WETH")
```

Also available: `self.chain` (str), `self.wallet_address` (str).

<!-- almanak-sdk-end: core-concepts -->

<!-- almanak-sdk-start: intent-vocabulary -->

## Intent Reference

All intents are created via `Intent` factory methods. Import:

```python
from almanak.framework.intents import Intent
```

### Trading

**Intent.swap** - Exchange tokens on a DEX

```python
Intent.swap(
    from_token="USDC",           # Token to sell
    to_token="WETH",             # Token to buy
    amount_usd=Decimal("1000"),  # Amount in USD (use amount_usd OR amount)
    amount=Decimal("500"),       # Amount in token units (alternative to amount_usd)
    max_slippage=Decimal("0.005"),  # Max slippage (0.5%)
    protocol="uniswap_v3",      # Optional: specific DEX
    chain="arbitrum",            # Optional: override chain
    destination_chain="base",    # Optional: cross-chain swap
)
```

Use `amount="all"` to swap the entire balance.

**`amount=` vs `amount_usd=`**: Use `amount_usd=` to specify trade size in USD (requires a live
price oracle from the gateway). Use `amount=` to specify exact token units (more reliable for live
trading since it bypasses USD-to-token conversion). When in doubt, prefer `amount=` for mainnet.

### Liquidity Provision

**Intent.lp_open** - Open a concentrated LP position

```python
Intent.lp_open(
    pool="WETH/USDC",               # Pool identifier
    amount0=Decimal("1.0"),          # Amount of token0
    amount1=Decimal("2000"),         # Amount of token1
    range_lower=Decimal("1800"),     # Lower price bound
    range_upper=Decimal("2200"),     # Upper price bound
    protocol="uniswap_v3",          # Default: uniswap_v3
    chain=None,                      # Optional override
)
```

**Intent.lp_close** - Close an LP position

```python
Intent.lp_close(
    position_id="12345",     # NFT token ID from lp_open result
    pool="WETH/USDC",        # Optional pool identifier
    collect_fees=True,       # Collect accumulated fees
    protocol="uniswap_v3",
)
```

**Intent.collect_fees** - Harvest LP fees without closing

```python
Intent.collect_fees(
    pool="WETH/USDC",
    protocol="traderjoe_v2",
)
```

### Lending / Borrowing

**Intent.supply** - Deposit collateral into a lending protocol

```python
Intent.supply(
    protocol="aave_v3",
    token="WETH",
    amount=Decimal("10"),
    use_as_collateral=True,   # Enable as collateral (default: True)
    market_id=None,           # Required for Morpho Blue
)
```

**Intent.borrow** - Borrow tokens against collateral

```python
Intent.borrow(
    protocol="aave_v3",
    collateral_token="WETH",
    collateral_amount=Decimal("10"),
    borrow_token="USDC",
    borrow_amount=Decimal("5000"),
    interest_rate_mode="variable",  # Aave: "variable" or "stable"
    market_id=None,                 # Required for Morpho Blue
)
```

**Intent.repay** - Repay borrowed tokens

```python
Intent.repay(
    protocol="aave_v3",
    token="USDC",
    amount=Decimal("5000"),
    repay_full=False,        # Set True to repay entire debt
    market_id=None,
)
```

**Intent.withdraw** - Withdraw from lending protocol

```python
Intent.withdraw(
    protocol="aave_v3",
    token="WETH",
    amount=Decimal("10"),
    withdraw_all=False,      # Set True to withdraw everything
    market_id=None,
)
```

### Perpetuals

**Intent.perp_open** - Open a perpetual futures position

```python
Intent.perp_open(
    market="ETH/USD",
    collateral_token="USDC",
    collateral_amount=Decimal("1000"),
    size_usd=Decimal("5000"),
    is_long=True,
    leverage=Decimal("5"),
    max_slippage=Decimal("0.01"),
    protocol="gmx_v2",
)
```

**Intent.perp_close** - Close a perpetual futures position

```python
Intent.perp_close(
    market="ETH/USD",
    collateral_token="USDC",
    is_long=True,
    size_usd=None,               # None = close full position
    max_slippage=Decimal("0.01"),
    protocol="gmx_v2",
)
```

### Bridging

**Intent.bridge** - Cross-chain token transfer

```python
Intent.bridge(
    token="USDC",
    amount=Decimal("1000"),
    from_chain="arbitrum",
    to_chain="base",
    max_slippage=Decimal("0.005"),
    preferred_bridge=None,       # Optional: specific bridge protocol
)
```

### Staking

**Intent.stake** - Liquid staking deposit

```python
Intent.stake(
    protocol="lido",
    token_in="ETH",
    amount=Decimal("10"),
    receive_wrapped=True,    # Receive wrapped token (e.g., wstETH)
)
```

**Intent.unstake** - Withdraw from liquid staking

```python
Intent.unstake(
    protocol="lido",
    token_in="wstETH",
    amount=Decimal("10"),
)
```

### Flash Loans

**Intent.flash_loan** - Borrow and repay in a single transaction

```python
Intent.flash_loan(
    provider="aave",         # "aave", "balancer", "morpho", or "auto"
    token="USDC",
    amount=Decimal("100000"),
    callback_intents=[...],  # Intents to execute with the borrowed funds
)
```

### Vaults (ERC-4626)

**Intent.vault_deposit** - Deposit into an ERC-4626 vault

```python
Intent.vault_deposit(
    vault="0x...",           # Vault contract address
    asset_token="USDC",
    amount=Decimal("1000"),
)
```

**Intent.vault_redeem** - Redeem shares from an ERC-4626 vault

```python
Intent.vault_redeem(
    vault="0x...",
    shares_amount=Decimal("1000"),
)
```

### Prediction Markets

```python
Intent.prediction_buy(protocol="polymarket", market="...", amount_usd=Decimal("100"))
Intent.prediction_sell(protocol="polymarket", market="...", amount_shares=Decimal("50"))
Intent.prediction_redeem(protocol="polymarket", market="...")
```

### Cross-Chain

**Intent.ensure_balance** - Meta-intent that resolves to a `BridgeIntent` (if balance is insufficient) or `HoldIntent` (if already met). Call `.resolve(market)` before returning from `decide()`.

```python
intent = Intent.ensure_balance(
    token="USDC",
    min_amount=Decimal("1000"),
    target_chain="arbitrum",
    max_slippage=Decimal("0.005"),
    preferred_bridge=None,
)
# Must resolve before returning - returns BridgeIntent or HoldIntent
resolved = intent.resolve(market)
return resolved
```

### Control Flow

**Intent.hold** - Do nothing this iteration

```python
Intent.hold(reason="RSI in neutral zone")
```

**Intent.sequence** - Execute multiple intents in order

```python
Intent.sequence(
    intents=[
        Intent.swap(from_token="USDC", to_token="WETH", amount_usd=Decimal("1000")),
        Intent.supply(protocol="aave_v3", token="WETH", amount=Decimal("0.5")),
    ],
    description="Buy WETH then supply to Aave",
)
```

### Chained Amounts

Use `"all"` to reference the full output of a prior intent:

```python
Intent.sequence(intents=[
    Intent.swap(from_token="USDC", to_token="WETH", amount_usd=Decimal("1000")),
    Intent.supply(protocol="aave_v3", token="WETH", amount="all"),  # Uses swap output
])
```

<!-- almanak-sdk-end: intent-vocabulary -->

<!-- almanak-sdk-start: market-snapshot-api -->

## Market Data API

The `MarketSnapshot` passed to `decide()` provides these methods:

### Prices

```python
price = market.price("WETH")                    # Decimal, USD price
price = market.price("WETH", quote="USDC")      # Price in USDC terms

pd = market.price_data("WETH")                  # PriceData object
pd.price             # Decimal - current price
pd.price_24h_ago     # Decimal
pd.change_24h_pct    # Decimal
pd.high_24h          # Decimal
pd.low_24h           # Decimal
pd.timestamp         # datetime
```

### Balances

```python
bal = market.balance("USDC")
bal.balance       # Decimal - token amount
bal.balance_usd   # Decimal - USD value
bal.symbol        # str
bal.address       # str - token contract address
```

`TokenBalance` supports numeric comparisons: `bal > Decimal("100")`.

### Technical Indicators

All indicators accept `token`, `period` (int), and `timeframe` (str, default `"4h"`).

```python
rsi = market.rsi("WETH", period=14, timeframe="4h")
rsi.value          # Decimal (0-100)
rsi.is_oversold    # bool (value < 30)
rsi.is_overbought  # bool (value > 70)
rsi.signal         # "BUY" | "SELL" | "HOLD"

macd = market.macd("WETH", fast_period=12, slow_period=26, signal_period=9)
macd.macd_line     # Decimal
macd.signal_line   # Decimal
macd.histogram     # Decimal
macd.is_bullish_crossover  # bool
macd.is_bearish_crossover  # bool

bb = market.bollinger_bands("WETH", period=20, std_dev=2.0)
bb.upper_band      # Decimal
bb.middle_band     # Decimal
bb.lower_band      # Decimal
bb.bandwidth        # Decimal
bb.percent_b        # Decimal (0.0 = at lower band, 1.0 = at upper band)
bb.is_squeeze       # bool

stoch = market.stochastic("WETH", k_period=14, d_period=3)
stoch.k_value       # Decimal
stoch.d_value       # Decimal
stoch.is_oversold   # bool
stoch.is_overbought # bool

atr_val = market.atr("WETH", period=14)
atr_val.value       # Decimal (absolute)
atr_val.value_percent  # Decimal, percentage points (2.62 means 2.62%, not 0.0262)
atr_val.is_high_volatility  # bool

sma = market.sma("WETH", period=20)
ema = market.ema("WETH", period=12)
# Both return MAData with: .value, .is_price_above, .is_price_below, .signal

adx = market.adx("WETH", period=14)
adx.adx             # Decimal (0-100, trend strength)
adx.plus_di          # Decimal (+DI)
adx.minus_di         # Decimal (-DI)
adx.is_strong_trend  # bool (adx >= 25)
adx.is_uptrend       # bool (+DI > -DI)
adx.is_downtrend     # bool (-DI > +DI)

obv = market.obv("WETH")
obv.obv              # Decimal (OBV value)
obv.signal_line      # Decimal (SMA of OBV)
obv.is_bullish       # bool (OBV > signal)
obv.is_bearish       # bool (OBV < signal)

cci = market.cci("WETH", period=20)
cci.value            # Decimal
cci.is_oversold      # bool (value <= -100)
cci.is_overbought    # bool (value >= 100)

ich = market.ichimoku("WETH")
ich.tenkan_sen       # Decimal (conversion line)
ich.kijun_sen        # Decimal (base line)
ich.senkou_span_a    # Decimal (leading span A)
ich.senkou_span_b    # Decimal (leading span B)
ich.cloud_top        # Decimal
ich.cloud_bottom     # Decimal
ich.is_bullish_crossover  # bool (tenkan > kijun)
ich.is_above_cloud   # bool
ich.signal           # "BUY" | "SELL" | "HOLD"
```

### Multi-Token Queries

```python
prices = market.prices(["WETH", "WBTC"])           # dict[str, Decimal]
balances = market.balances(["USDC", "WETH"])        # dict[str, Decimal]
usd_val = market.balance_usd("WETH")               # Decimal - USD value of holdings
total = market.total_portfolio_usd()                # Decimal
```

### OHLCV Data

```python
df = market.ohlcv("WETH", timeframe="1h", limit=100)  # pd.DataFrame
# Columns: open, high, low, close, volume
```

### Pool and DEX Data

```python
pool = market.pool_price("0x...")                   # DataEnvelope[PoolPrice]
pool = market.pool_price_by_pair("WETH", "USDC")   # DataEnvelope[PoolPrice]
reserves = market.pool_reserves("0x...")            # PoolReserves
history = market.pool_history("0x...", resolution="1h")  # DataEnvelope[list[PoolSnapshot]]
analytics = market.pool_analytics("0x...")          # DataEnvelope[PoolAnalytics]
best = market.best_pool("WETH", "USDC", metric="fee_apr")  # DataEnvelope[PoolAnalyticsResult]
```

### Price Aggregation and Slippage

```python
twap = market.twap("WETH/USDC", window_seconds=300)       # DataEnvelope[AggregatedPrice]
lwap = market.lwap("WETH/USDC")                           # DataEnvelope[AggregatedPrice]
depth = market.liquidity_depth("0x...")                    # DataEnvelope[LiquidityDepth]
slip = market.estimate_slippage("WETH", "USDC", Decimal("10000"))  # DataEnvelope[SlippageEstimate]
best_dex = market.best_dex_price("WETH", "USDC", Decimal("1"))    # BestDexResult
```

### Lending and Funding Rates

```python
rate = market.lending_rate("aave_v3", "USDC", side="supply")   # LendingRate
best = market.best_lending_rate("USDC", side="supply")         # BestRateResult
fr = market.funding_rate("binance", "ETH-PERP")               # FundingRate
spread = market.funding_rate_spread("ETH-PERP", "binance", "hyperliquid")  # FundingRateSpread
```

### Impermanent Loss

```python
il = market.il_exposure("position_id", fees_earned=Decimal("50"))  # ILExposure
proj = market.projected_il("WETH", "USDC", price_change_pct=Decimal("0.1"))  # ProjectedILResult
```

### Prediction Markets

```python
mkt = market.prediction("market_id")                    # PredictionMarket
price = market.prediction_price("market_id", "YES")     # Decimal
positions = market.prediction_positions("market_id")     # list[PredictionPosition]
orders = market.prediction_orders("market_id")           # list[PredictionOrder]
```

### Yield and Analytics

```python
yields = market.yield_opportunities("USDC", min_tvl=100_000, sort_by="apy")  # DataEnvelope[list[YieldOpportunity]]
gas = market.gas_price()                                # GasPrice
health = market.health()                                # HealthReport
signals = market.wallet_activity(action_types=["SWAP", "LP_OPEN"])  # list
```

### Context Properties

```python
market.chain            # str - current chain name
market.wallet_address   # str - wallet address
market.timestamp        # datetime - snapshot timestamp
```

<!-- almanak-sdk-end: market-snapshot-api -->

<!-- almanak-sdk-start: state-management -->

## State Management

`self.state` is a dict that persists across iterations **and restarts**. The runner calls
`load_state()` on startup, restoring previously saved state from the StateManager (SQLite locally,
gateway when deployed). Write to `self.state` during `decide()` or `on_intent_executed()` and
changes are automatically persisted after each iteration.

```python
def decide(self, market):
    # Read state (survives restarts)
    last_trade = self.state.get("last_trade_time")
    position_id = self.state.get("lp_position_id")

    # Write state (persisted automatically after each iteration)
    self.state["last_trade_time"] = datetime.now().isoformat()
    self.state["consecutive_holds"] = self.state.get("consecutive_holds", 0) + 1
```

Use `--fresh` to clear saved state when starting over: `almanak strat run --fresh --once`.

For strategies that need custom serialization (e.g., Decimal fields, complex objects), override
`get_persistent_state()` and `load_persistent_state()`:

```python
def get_persistent_state(self) -> dict:
    """Called by framework to serialize state for persistence."""
    return {
        "phase": self.state.get("phase", "idle"),
        "position_id": self.state.get("position_id"),
        "entry_price": str(self.state.get("entry_price", "0")),
    }

def load_persistent_state(self, saved: dict) -> None:
    """Called by framework on startup to restore state."""
    self.state["phase"] = saved.get("phase", "idle")
    self.state["position_id"] = saved.get("position_id")
    self.state["entry_price"] = Decimal(saved.get("entry_price", "0"))
```

### on_intent_executed Callback

After execution, access results (position IDs, swap amounts) via the callback. The framework
automatically enriches `result` with protocol-specific data - no manual receipt parsing needed.

```python
# In your strategy file, import logging at the top:
# import logging
# logger = logging.getLogger(__name__)

def on_intent_executed(self, intent, success: bool, result):

    if not success:
        logger.warning(f"Intent failed: {intent.intent_type}")
        return

    # Capture LP position ID (enriched automatically by ResultEnricher)
    if result.position_id is not None:
        self.state["lp_position_id"] = result.position_id
        logger.info(f"Opened LP position {result.position_id}")

        # Store range bounds for rebalancing strategies (keep as Decimal)
        if (
            hasattr(intent, "range_lower") and intent.range_lower is not None
            and hasattr(intent, "range_upper") and intent.range_upper is not None
        ):
            self.state["range_lower"] = intent.range_lower
            self.state["range_upper"] = intent.range_upper

    # Capture swap amounts
    if result.swap_amounts:
        self.state["last_swap"] = {
            "amount_in": str(result.swap_amounts.amount_in),
            "amount_out": str(result.swap_amounts.amount_out),
        }
        logger.info(
            f"Swapped {result.swap_amounts.amount_in} -> {result.swap_amounts.amount_out}"
        )
```

<!-- almanak-sdk-end: state-management -->

<!-- almanak-sdk-start: configuration -->

## Configuration

### config.json

```json
{
    "strategy_id": "my_rsi_strategy",
    "chain": "arbitrum",
    "base_token": "WETH",
    "quote_token": "USDC",
    "rsi_period": 14,
    "rsi_oversold": 30,
    "rsi_overbought": 70,
    "trade_size_usd": 1000,
    "max_slippage_bps": 50,
    "anvil_funding": {
        "USDC": "10000",
        "WETH": "5"
    }
}
```

Required fields: `strategy_id`, `chain`.
All other fields are strategy-specific and accessed via `self.config.get(key, default)`.

### .env

```bash
# Required
ALMANAK_PRIVATE_KEY=0x...

# RPC access (set at least one)
ALCHEMY_API_KEY=your_key
# RPC_URL=https://...

# Optional
# ENSO_API_KEY=
# COINGECKO_API_KEY=
# ALMANAK_API_KEY=
```

### anvil_funding

When running on Anvil (`--network anvil`), the framework auto-funds the wallet
with tokens specified in `anvil_funding`. Values are in token units (not USD).

<!-- almanak-sdk-end: configuration -->

<!-- almanak-sdk-start: token-resolution -->

## Token Resolution

Use `get_token_resolver()` for all token lookups. Never hardcode addresses.

```python
from almanak.framework.data.tokens import get_token_resolver

resolver = get_token_resolver()

# Resolve by symbol
token = resolver.resolve("USDC", "arbitrum")
# -> ResolvedToken(symbol="USDC", address="0xaf88...", decimals=6, chain="arbitrum")

# Resolve by address
token = resolver.resolve("0xaf88d065e77c8cC2239327C5EDb3A432268e5831", "arbitrum")

# Convenience
decimals = resolver.get_decimals("arbitrum", "USDC")  # -> 6
address = resolver.get_address("arbitrum", "USDC")     # -> "0xaf88..."

# For DEX swaps (auto-wraps native tokens: ETH->WETH, MATIC->WMATIC)
token = resolver.resolve_for_swap("ETH", "arbitrum")   # -> WETH

# Resolve trading pair
usdc, weth = resolver.resolve_pair("USDC", "WETH", "arbitrum")
```

Resolution order: memory cache -> disk cache -> static registry -> gateway on-chain lookup.

Never default to 18 decimals. If the token is unknown, `TokenNotFoundError` is raised.

<!-- almanak-sdk-end: token-resolution -->

<!-- almanak-sdk-start: backtesting -->

## Backtesting

### PnL Backtest (historical prices, no on-chain execution)

```bash
almanak strat backtest pnl -s my_strategy \
    --start 2024-01-01 --end 2024-06-01 \
    --initial-capital 10000
```

### Paper Trading (Anvil fork with real execution, PnL tracking)

```bash
almanak strat backtest paper -s my_strategy \
    --duration 3600 --interval 60 \
    --initial-capital 10000
```

Paper trading runs the full strategy loop on an Anvil fork with real transaction
execution, equity curve tracking, and JSON result logs.

### Parameter Sweep

```bash
almanak strat backtest sweep -s my_strategy \
    --start 2024-01-01 --end 2024-06-01 \
    --param "rsi_oversold:20,25,30" \
    --param "rsi_overbought:70,75,80"
```

Runs the PnL backtest across all parameter combinations and ranks by Sharpe ratio.

### Programmatic Backtesting

```python
from almanak.framework.backtesting import BacktestEngine

engine = BacktestEngine(
    strategy_class=MyStrategy,
    config={...},
    start_date="2024-01-01",
    end_date="2024-06-01",
    initial_capital=10000,
)
results = engine.run()
results.sharpe_ratio
results.max_drawdown
results.total_return
results.plot()  # Matplotlib equity curve
```

### Backtesting Limitations

- **OHLCV data**: The PnL backtester uses historical close prices from CoinGecko. Indicators that require OHLCV data (ATR, Stochastic, Ichimoku) need a paid CoinGecko tier or an external data source.
- **RPC for paper trading**: Paper trading requires an RPC endpoint. Alchemy free tier is recommended for performance; public RPCs work but are slow.
- **No CWD auto-discovery**: Backtest CLI commands (`backtest pnl`, `backtest paper`, `backtest sweep`) require an explicit `-s strategy_name` flag. They do not auto-discover strategies from the current directory like `strat run` does.
- **Percentage fields**: `total_return_pct` and similar `_pct` result fields are decimal fractions (0.33 = 33%), not percentages.

<!-- almanak-sdk-end: backtesting -->

<!-- almanak-sdk-start: cli-commands -->

## CLI Commands

### Strategy Management

```bash
almanak strat new                     # Interactive strategy scaffolding
almanak strat new -t mean_reversion -n my_rsi -c arbitrum  # Non-interactive
almanak strat demo                    # Browse and copy a working demo strategy
```

**Templates:** `blank`, `dynamic_lp`, `mean_reversion`, `bollinger`, `basis_trade`, `lending_loop`, `copy_trader`

### Running Strategies

```bash
almanak strat run --once              # Single iteration (from strategy dir)
almanak strat run -d path/to/strat --once  # Explicit directory
almanak strat run --network anvil --once   # Local Anvil fork
almanak strat run --interval 30       # Continuous (30s between iterations)
almanak strat run --dry-run --once    # No transactions submitted
almanak strat run --fresh --once      # Clear state before running
almanak strat run --id abc123 --once  # Resume previous run
almanak strat run --dashboard         # Launch live monitoring dashboard
```

### Backtesting

```bash
almanak strat backtest pnl -s my_strategy            # Historical PnL simulation
almanak strat backtest paper -s my_strategy            # Paper trading on Anvil fork
almanak strat backtest sweep -s my_strategy           # Parameter sweep optimization
```

### Teardown

```bash
almanak strat teardown plan           # Preview teardown intents
almanak strat teardown execute        # Execute teardown
```

### Gateway

```bash
almanak gateway                       # Start standalone gateway
almanak gateway --network anvil       # Gateway for local Anvil testing
almanak gateway --port 50052          # Custom port
```

### Agent Skill Management

```bash
almanak agent install                 # Auto-detect platforms and install
almanak agent install -p claude       # Install for specific platform
almanak agent install -p all          # Install for all 9 platforms
almanak agent update                  # Update installed skill files
almanak agent status                  # Check installation status
```

### Documentation

```bash
almanak docs path                     # Path to bundled LLM docs
almanak docs dump                     # Print full LLM docs
almanak docs agent-skill              # Path to bundled agent skill
almanak docs agent-skill --dump       # Print agent skill content
```

<!-- almanak-sdk-end: cli-commands -->

<!-- almanak-sdk-start: supported-chains -->

## Supported Chains and Protocols

### Chains

| Chain | Enum Value | Config Name |
|-------|-----------|-------------|
| Ethereum | `ETHEREUM` | `ethereum` |
| Arbitrum | `ARBITRUM` | `arbitrum` |
| Optimism | `OPTIMISM` | `optimism` |
| Base | `BASE` | `base` |
| Avalanche | `AVALANCHE` | `avalanche` |
| Polygon | `POLYGON` | `polygon` |
| BSC | `BSC` | `bsc` |
| Sonic | `SONIC` | `sonic` |
| Plasma | `PLASMA` | `plasma` |
| Blast | `BLAST` | `blast` |
| Mantle | `MANTLE` | `mantle` |
| Berachain | `BERACHAIN` | `berachain` |

<!-- almanak-sdk-end: supported-chains -->

<!-- almanak-sdk-start: supported-protocols -->

### Protocols

| Protocol | Enum Value | Type | Config Name |
|----------|-----------|------|-------------|
| Uniswap V3 | `UNISWAP_V3` | DEX / LP | `uniswap_v3` |
| PancakeSwap V3 | `PANCAKESWAP_V3` | DEX / LP | `pancakeswap_v3` |
| SushiSwap V3 | `SUSHISWAP_V3` | DEX / LP | `sushiswap_v3` |
| TraderJoe V2 | `TRADERJOE_V2` | DEX / LP | `traderjoe_v2` |
| Aerodrome | `AERODROME` | DEX / LP | `aerodrome` |
| Enso | `ENSO` | Aggregator | `enso` |
| Pendle | `PENDLE` | Yield | `pendle` |
| MetaMorpho | `METAMORPHO` | Lending | `metamorpho` |
| LiFi | `LIFI` | Bridge | `lifi` |
| Vault | `VAULT` | ERC-4626 | `vault` |
| Curve | `CURVE` | DEX / LP | `curve` |
| Balancer | `BALANCER` | DEX / LP | `balancer` |
| Aave V3 | * | Lending | `aave_v3` |
| Morpho Blue | * | Lending | `morpho_blue` |
| Compound V3 | * | Lending | `compound_v3` |
| GMX V2 | * | Perps | `gmx_v2` |
| Hyperliquid | * | Perps | `hyperliquid` |
| Polymarket | * | Prediction | `polymarket` |
| Kraken | * | CEX | `kraken` |
| Lido | * | Staking | `lido` |
| Lagoon | * | Vault | `lagoon` |

\* These protocols do not have a `Protocol` enum value. Use the string config name (e.g., `protocol="aave_v3"`) in intents. They are resolved by the intent compiler and transaction builder directly.

### Networks

| Network | Enum Value | Description |
|---------|-----------|-------------|
| Mainnet | `MAINNET` | Production chains |
| Anvil | `ANVIL` | Local fork for testing |
| Sepolia | `SEPOLIA` | Testnet |

### Protocol-Specific Notes

**GMX V2 (Perpetuals)**

- **Market format**: Use slash separator: `"BTC/USD"`, `"ETH/USD"`, `"LINK/USD"` (not dash).
- **Two-step execution**: GMX V2 uses a keeper-based execution model. When you call `Intent.perp_open()`, the SDK submits an order creation transaction. A GMX keeper then executes the actual position change in a separate transaction. `on_intent_executed(success=True)` fires when the order creation TX confirms, **not** when the keeper executes the position. Strategies should poll position state before relying on it.
- **Minimum position size**: GMX V2 enforces a minimum position size of approximately $11 net of fees. Orders below this threshold are silently rejected by the keeper with no on-chain error.
- **Collateral approvals**: Handled automatically by the intent compiler (same as LP opens).
- **Position monitoring**: `get_all_positions()` may not return positions immediately after opening due to keeper delay. Allow a few seconds before querying.
- **Supported chains**: Arbitrum, Avalanche.
- **Collateral tokens**: USDC, USDT (chain-dependent).

<!-- almanak-sdk-end: supported-protocols -->

<!-- almanak-sdk-start: common-patterns -->

## Common Patterns

### RSI Mean Reversion (Trading)

```python
def decide(self, market):
    rsi = market.rsi(self.base_token, period=self.rsi_period)
    quote_bal = market.balance(self.quote_token)
    base_bal = market.balance(self.base_token)

    if rsi.is_oversold and quote_bal.balance_usd >= self.trade_size:
        return Intent.swap(
            from_token=self.quote_token, to_token=self.base_token,
            amount_usd=self.trade_size, max_slippage=Decimal("0.005"),
        )
    if rsi.is_overbought and base_bal.balance_usd >= self.trade_size:
        return Intent.swap(
            from_token=self.base_token, to_token=self.quote_token,
            amount_usd=self.trade_size, max_slippage=Decimal("0.005"),
        )
    return Intent.hold(reason=f"RSI={rsi.value:.1f} in neutral zone")
```

### LP Rebalancing

```python
def decide(self, market):
    price = market.price(self.base_token)
    position_id = self.state.get("lp_position_id")

    if position_id:
        # Check if price is out of range - close and reopen
        if price < self.state.get("range_lower") or price > self.state.get("range_upper"):
            return Intent.lp_close(position_id=position_id, protocol="uniswap_v3")

    # Open new position centered on current price
    atr = market.atr(self.base_token)
    half_range = price * (atr.value_percent / Decimal("100")) * 2  # value_percent is percentage points
    return Intent.lp_open(
        pool="WETH/USDC",
        amount0=Decimal("1"), amount1=Decimal("2000"),
        range_lower=price - half_range,
        range_upper=price + half_range,
    )
```

### Multi-Step with IntentSequence

```python
def decide(self, market):
    return Intent.sequence(
        intents=[
            Intent.swap(from_token="USDC", to_token="WETH", amount_usd=Decimal("5000")),
            Intent.supply(protocol="aave_v3", token="WETH", amount="all"),
            Intent.borrow(
                protocol="aave_v3",
                collateral_token="WETH", collateral_amount=Decimal("0"),
                borrow_token="USDC", borrow_amount=Decimal("3000"),
            ),
        ],
        description="Leverage loop: buy WETH, supply, borrow USDC",
    )
```

### Alerting

```python
from almanak.framework.alerting import AlertManager

class MyStrategy(IntentStrategy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alerts = AlertManager.from_config(self.config.get("alerting", {}))

    def decide(self, market):
        rsi = market.rsi("WETH")
        if rsi.value < 20:
            self.alerts.send("Extreme oversold: RSI={:.1f}".format(rsi.value), level="warning")
        # ... trading logic
```

### Safe Teardown

Implement teardown so the strategy can cleanly exit positions:

```python
def supports_teardown(self) -> bool:
    return True

def generate_teardown_intents(self, mode, market=None) -> list[Intent]:
    intents = []
    position_id = self.state.get("lp_position_id")
    if position_id:
        intents.append(Intent.lp_close(position_id=position_id))
    # Swap all base token back to quote
    intents.append(Intent.swap(
        from_token=self.base_token, to_token=self.quote_token,
        amount="all", max_slippage=Decimal("0.03"),
    ))
    return intents
```

### Error Handling

Always wrap `decide()` in try/except and return `Intent.hold()` on error:

```python
def decide(self, market):
    try:
        # ... strategy logic
    except Exception as e:
        logger.exception(f"Error in decide(): {e}")
        return Intent.hold(reason=f"Error: {e}")
```

### Execution Failure Tracking (Circuit Breaker)

The framework retries each failed intent up to `max_retries` (default: 3) with
exponential backoff. However, after all retries are exhausted the strategy
**continues running** and will attempt the same trade on the next iteration.
Without a circuit breaker, this creates an infinite loop of reverted transactions
that burn gas without any hope of success.

**Always track consecutive execution failures in persistent state** and stop
trading (or enter an extended cooldown) after a threshold is reached:

```python
MAX_CONSECUTIVE_FAILURES = 3     # Stop after 3 rounds of failed intents
FAILURE_COOLDOWN_SECONDS = 1800  # 30-min cooldown before retrying

def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.consecutive_failures = 0
    self.failure_cooldown_until = 0.0

def decide(self, market):
    try:
        now = time.time()

        # Circuit breaker: skip trading while in cooldown
        if now < self.failure_cooldown_until:
            remaining = int(self.failure_cooldown_until - now)
            return Intent.hold(
                reason=f"Circuit breaker active, cooldown {remaining}s remaining"
            )

        # Circuit breaker: enter cooldown after too many failures
        if self.consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
            self.failure_cooldown_until = now + FAILURE_COOLDOWN_SECONDS
            self.consecutive_failures = 0
            logger.warning(
                f"Circuit breaker tripped after {MAX_CONSECUTIVE_FAILURES} "
                f"consecutive failures, cooling down {FAILURE_COOLDOWN_SECONDS}s"
            )
            return Intent.hold(reason="Circuit breaker tripped")

        # ... normal strategy logic ...

    except Exception as e:
        logger.exception(f"Error in decide(): {e}")
        return Intent.hold(reason=f"Error: {e}")

def on_intent_executed(self, intent, success: bool, result):
    if success:
        self.consecutive_failures = 0   # Reset on success
    else:
        self.consecutive_failures += 1
        logger.warning(
            f"Intent failed ({self.consecutive_failures}/{MAX_CONSECUTIVE_FAILURES})"
        )

def get_persistent_state(self) -> dict:
    return {
        "consecutive_failures": self.consecutive_failures,
        "failure_cooldown_until": self.failure_cooldown_until,
    }

def load_persistent_state(self, state: dict) -> None:
    self.consecutive_failures = int(state.get("consecutive_failures", 0))
    self.failure_cooldown_until = float(state.get("failure_cooldown_until", 0))
```

**Important:** Only update trade-timing state (e.g. `last_trade_ts`) inside
`on_intent_executed` when `success=True`, not when the intent is created. Setting
it at creation time means a failed trade still resets the interval timer, causing
the strategy to wait before retrying — or worse, to keep retrying on a fixed
schedule with no failure awareness.

### Handling Gas and Slippage Errors (Sadflow Hook)

Override `on_sadflow_enter` to react to specific error types during intent
retries. This hook is called before each retry attempt and lets you modify the
transaction (e.g. increase gas or slippage) or abort early:

```python
from almanak.framework.intents.state_machine import SadflowAction

class MyStrategy(IntentStrategy):
    def on_sadflow_enter(self, error_type, attempt, context):
        # Abort immediately on insufficient funds — retrying won't help
        if error_type == "INSUFFICIENT_FUNDS":
            return SadflowAction.abort("Insufficient funds, stopping retries")

        # Increase gas limit for gas-related errors
        if error_type == "GAS_ERROR" and context.action_bundle:
            modified = self._increase_gas(context.action_bundle)
            return SadflowAction.modify(modified, reason="Increased gas limit")

        # For slippage errors ("Too little received"), abort after 1 attempt
        # since retrying with the same parameters will produce the same result
        if error_type == "SLIPPAGE" and attempt >= 1:
            return SadflowAction.abort("Slippage error persists, aborting")

        # Default: let the framework retry with backoff
        return None
```

**Error types** passed to `on_sadflow_enter` (from `_categorize_error` in `state_machine.py`):
- `GAS_ERROR` — gas estimation failed or gas limit exceeded
- `INSUFFICIENT_FUNDS` — wallet balance too low
- `SLIPPAGE` — "Too little received" or similar DEX revert
- `TIMEOUT` — transaction confirmation timed out
- `NONCE_ERROR` — nonce mismatch or conflict
- `REVERT` — generic transaction revert
- `RATE_LIMIT` — RPC or API rate limit hit
- `NETWORK_ERROR` — connection or network failure
- `COMPILATION_PERMANENT` — unsupported protocol/chain (non-retriable)
- `None` — unclassified error

<!-- almanak-sdk-end: common-patterns -->

<!-- almanak-sdk-start: going-live -->

## Going Live Checklist

Before deploying to mainnet:

- [ ] Test on Anvil with `--network anvil --once` until `decide()` works correctly
- [ ] Run `--dry-run --once` on mainnet to verify compilation without submitting transactions
- [ ] Use `amount=` (token units) for swaps if `amount_usd=` causes reverts (see swap reference above)
- [ ] Override `get_persistent_state()` / `load_persistent_state()` if your strategy tracks positions or phase state
- [ ] Verify token approvals for all protocols used (auto-handled for most, but verify on first run)
- [ ] Fund wallet on the correct chain with sufficient tokens plus gas (ETH/AVAX/MATIC)
- [ ] Note your instance ID after first successful iteration (needed for `--id` resume)
- [ ] Start with small amounts and monitor the first few iterations

<!-- almanak-sdk-end: going-live -->

<!-- almanak-sdk-start: troubleshooting -->

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `TokenNotFoundError` | Token symbol not in registry | Use exact symbol (e.g., "WETH" not "ETH" for swaps). Check `resolver.resolve("TOKEN", "chain")`. |
| `Gateway not available` | Gateway not running | Use `almanak strat run` (auto-starts gateway) or start manually with `almanak gateway`. |
| `ALMANAK_PRIVATE_KEY not set` | Missing .env | Add `ALMANAK_PRIVATE_KEY=0x...` to your `.env` file. |
| `Anvil not found` | Foundry not installed | Install: `curl -L https://foundry.paradigm.xyz \| bash && foundryup` |
| `RSI data unavailable` | Insufficient price history | The gateway needs time to accumulate data. Try a longer timeframe or wait. |
| `Insufficient balance` | Wallet doesn't have enough tokens | For Anvil: add `anvil_funding` to config.json. For mainnet: fund the wallet. |
| `Slippage exceeded` | Trade too large or pool illiquid | Increase `max_slippage` or reduce trade size. |
| `Too little received` (repeated reverts) | Placeholder prices used for slippage calculation, or stale price data | Ensure real price feeds are active (not placeholder). Implement `on_sadflow_enter` to abort on persistent slippage errors. Add a circuit breaker to stop retrying the same failing trade. |
| Transactions keep reverting after max retries | Strategy re-emits the same failing intent on subsequent iterations | Track `consecutive_failures` in persistent state and enter cooldown after a threshold. See the "Execution Failure Tracking" pattern. |
| Gas wasted on reverted transactions | No circuit breaker; framework retries 3x per intent, then strategy retries next iteration indefinitely | Implement `on_intent_executed` callback to count failures and `on_sadflow_enter` to abort non-recoverable errors early. |
| Intent compilation fails | Wrong parameter types | Ensure amounts are `Decimal`, not `float`. Use `Decimal(str(value))`. |

### Debugging Tips

- Use `--verbose` flag for detailed logging: `almanak strat run --once --verbose`
- Use `--dry-run` to test decide() without submitting transactions
- Use `--log-file out.json` for machine-readable JSON logs
- Check strategy state: `self.state` persists between iterations
- Paper trade first: `almanak strat backtest paper -s my_strategy` runs real execution on Anvil

<!-- almanak-sdk-end: troubleshooting -->
