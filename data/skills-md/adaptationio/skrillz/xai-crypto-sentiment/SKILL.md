---
name: xai-crypto-sentiment
description: Real-time cryptocurrency sentiment analysis using Twitter/X via Grok. Use when analyzing crypto sentiment, tracking whale activity, or gauging market fear/greed.
version: 1.0.0
---

# xAI Crypto Sentiment Analysis

Real-time cryptocurrency sentiment from Crypto Twitter (CT) using Grok's native X integration.

## Quick Start

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),
    base_url="https://api.x.ai/v1"
)

def get_crypto_sentiment(coin: str) -> dict:
    """Get real-time sentiment for a cryptocurrency."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Analyze Crypto Twitter sentiment for {coin}.

            Return JSON:
            {{
                "coin": "{coin}",
                "sentiment": {{
                    "overall": "bullish" | "bearish" | "neutral",
                    "score": -1.0 to 1.0,
                    "confidence": 0.0 to 1.0
                }},
                "fear_greed": "extreme fear" | "fear" | "neutral" | "greed" | "extreme greed",
                "metrics": {{
                    "bullish_percent": 0-100,
                    "bearish_percent": 0-100,
                    "mention_volume": "high" | "medium" | "low",
                    "trend": "increasing" | "stable" | "decreasing"
                }},
                "whale_mentions": {{
                    "detected": true/false,
                    "sentiment": "accumulating" | "distributing" | "neutral",
                    "notable": [...]
                }},
                "narratives": ["narrative1", "narrative2"],
                "fud_alerts": [...],
                "fomo_level": "high" | "medium" | "low" | "none"
            }}"""
        }]
    )
    return response.choices[0].message.content

# Example
sentiment = get_crypto_sentiment("Bitcoin")
print(sentiment)
```

## Crypto Twitter Influencers

```python
CRYPTO_INFLUENCERS = [
    # Bitcoin Maxis
    "saborskip",
    "michael_saylor",

    # Analysts
    "CryptoCapo_",
    "Pentosh1",
    "ColdBloodShill",

    # News
    "WatcherGuru",
    "whale_alert",

    # DeFi
    "DefiIgnas",
    "Route2FI",

    # Altcoins
    "AltcoinGordon",
    "CryptoKaleo"
]
```

## Sentiment Functions

### Bitcoin Market Sentiment
```python
def bitcoin_sentiment() -> dict:
    """Get comprehensive Bitcoin sentiment analysis."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": """Analyze Bitcoin sentiment on Crypto Twitter.

            Return JSON:
            {
                "bitcoin": {
                    "sentiment_score": -1 to 1,
                    "fear_greed_index": 0-100,
                    "fear_greed_label": "...",
                    "trend": "bullish/bearish/consolidating"
                },
                "market_structure": {
                    "support_levels_mentioned": [...],
                    "resistance_levels_mentioned": [...],
                    "key_levels": [...]
                },
                "whale_activity": {
                    "accumulation_signals": true/false,
                    "distribution_signals": true/false,
                    "notable_moves": [...]
                },
                "narratives": {
                    "bullish": [...],
                    "bearish": [...]
                },
                "influencer_consensus": {
                    "bullish_count": n,
                    "bearish_count": n,
                    "key_calls": [...]
                },
                "on_chain_mentions": {
                    "exchange_flows": "inflows/outflows/neutral",
                    "wallet_activity": "..."
                },
                "macro_sentiment": {
                    "correlation_to_stocks": "...",
                    "fed_mentions": "...",
                    "institutional_interest": "..."
                }
            }"""
        }]
    )
    return response.choices[0].message.content
```

### Altcoin Season Detection
```python
def detect_altseason() -> dict:
    """Detect if altcoin season is emerging."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": """Analyze Crypto Twitter for altcoin season signals.

            Return JSON:
            {
                "altseason_status": "active" | "emerging" | "not present",
                "confidence": 0 to 1,
                "signals": {
                    "btc_dominance_sentiment": "...",
                    "altcoin_volume": "high/medium/low",
                    "rotation_patterns": "...",
                    "new_narratives": [...]
                },
                "hot_sectors": [
                    {"sector": "...", "sentiment": ..., "top_coins": [...]}
                ],
                "coins_trending": [
                    {"coin": "...", "sentiment": ..., "catalyst": "..."}
                ],
                "risk_level": "high/medium/low",
                "recommendation": "..."
            }"""
        }]
    )
    return response.choices[0].message.content
```

### Token Sentiment Analysis
```python
def analyze_token(token: str, chain: str = None) -> dict:
    """Analyze sentiment for a specific token."""
    chain_context = f" on {chain}" if chain else ""

    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Analyze Crypto Twitter sentiment for {token}{chain_context}.

            Return JSON:
            {{
                "token": "{token}",
                "chain": "{chain or 'unknown'}",
                "sentiment": {{
                    "score": -1 to 1,
                    "label": "...",
                    "volume": "high/medium/low"
                }},
                "community_health": {{
                    "engagement": "high/medium/low",
                    "holder_sentiment": "...",
                    "developer_activity_mentions": "..."
                }},
                "narratives": [...],
                "catalysts": {{
                    "upcoming": [...],
                    "recent": [...]
                }},
                "risks": {{
                    "fud_topics": [...],
                    "concerns_raised": [...],
                    "rug_risk_mentions": true/false
                }},
                "influencer_mentions": [...],
                "comparison_to_competitors": "..."
            }}"""
        }]
    )
    return response.choices[0].message.content
```

### DeFi Protocol Sentiment
```python
def defi_protocol_sentiment(protocol: str) -> dict:
    """Analyze sentiment for a DeFi protocol."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Analyze Crypto Twitter sentiment for {protocol} DeFi protocol.

            Return JSON:
            {{
                "protocol": "{protocol}",
                "sentiment": {{
                    "score": -1 to 1,
                    "trend": "improving/declining/stable"
                }},
                "tvl_sentiment": "growing/stable/declining concern",
                "security_mentions": {{
                    "concerns": [...],
                    "audits_mentioned": [...],
                    "exploit_risk_perception": "high/medium/low"
                }},
                "yield_sentiment": "attractive/fair/unattractive",
                "community_growth": "...",
                "governance_sentiment": "...",
                "competitors_mentioned": [...]
            }}"""
        }]
    )
    return response.choices[0].message.content
```

### NFT Market Sentiment
```python
def nft_sentiment(collection: str = None) -> dict:
    """Analyze NFT market sentiment."""
    target = f"the {collection} collection" if collection else "the NFT market"

    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Analyze Crypto Twitter sentiment for {target}.

            Return JSON:
            {{
                "target": "{collection or 'NFT Market'}",
                "sentiment": {{
                    "score": -1 to 1,
                    "market_phase": "bull/bear/recovery/mania"
                }},
                "volume_sentiment": "high/medium/low",
                "floor_price_sentiment": "stable/rising/falling concern",
                "trending_collections": [...],
                "whale_activity": {{
                    "notable_buys": [...],
                    "notable_sales": [...]
                }},
                "narratives": [...],
                "mint_sentiment": "hot/cooling/cold"
            }}"""
        }]
    )
    return response.choices[0].message.content
```

### Whale Alert Monitoring
```python
def monitor_whale_alerts() -> dict:
    """Monitor whale activity mentions on CT."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": """Search Crypto Twitter for recent whale alerts and large transactions.

            Focus on @whale_alert and similar accounts.

            Return JSON:
            {
                "timestamp": "...",
                "recent_whale_moves": [
                    {
                        "coin": "...",
                        "amount_usd": "...",
                        "direction": "exchange_inflow/exchange_outflow/wallet_transfer",
                        "interpretation": "bullish/bearish/neutral",
                        "source": "..."
                    }
                ],
                "exchange_flow_summary": {
                    "net_flow": "inflows/outflows/balanced",
                    "interpretation": "..."
                },
                "accumulation_signals": [...],
                "distribution_signals": [...],
                "notable_wallet_activity": [...]
            }"""
        }]
    )
    return response.choices[0].message.content
```

### FOMO/FUD Detection
```python
def detect_fomo_fud(coin: str) -> dict:
    """Detect FOMO or FUD patterns for a cryptocurrency."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Analyze Crypto Twitter for FOMO and FUD signals around {coin}.

            Return JSON:
            {{
                "coin": "{coin}",
                "fomo_analysis": {{
                    "level": "extreme/high/moderate/low/none",
                    "triggers": [...],
                    "warning_signs": [...],
                    "sustainability": "likely/unlikely"
                }},
                "fud_analysis": {{
                    "level": "extreme/high/moderate/low/none",
                    "sources": [...],
                    "legitimacy": "valid concerns/coordinated/mixed",
                    "topics": [...]
                }},
                "manipulation_signals": {{
                    "detected": true/false,
                    "type": "pump/dump/coordinated/organic",
                    "evidence": [...]
                }},
                "contrarian_signal": {{
                    "extreme_fear": true/false,
                    "extreme_greed": true/false,
                    "actionable": "..."
                }}
            }}"""
        }]
    )
    return response.choices[0].message.content
```

## Crypto Market Dashboard

```python
def crypto_market_dashboard() -> dict:
    """Get overall crypto market sentiment dashboard."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": """Create a comprehensive Crypto Twitter market dashboard.

            Return JSON:
            {
                "timestamp": "...",
                "market_sentiment": {
                    "overall": -1 to 1,
                    "fear_greed": 0-100,
                    "trend": "bullish/bearish/neutral"
                },
                "bitcoin": {
                    "sentiment": ...,
                    "key_levels": [...]
                },
                "ethereum": {
                    "sentiment": ...,
                    "key_topics": [...]
                },
                "top_trending_coins": [
                    {"coin": "...", "sentiment": ..., "reason": "..."}
                ],
                "sector_performance": [
                    {"sector": "L1/L2/DeFi/NFT/Meme", "sentiment": ...}
                ],
                "hot_narratives": [...],
                "risk_alerts": [...],
                "whale_summary": "...",
                "recommended_focus": [...]
            }"""
        }]
    )
    return response.choices[0].message.content
```

## Best Practices

### 1. Crypto-Specific Considerations
- CT is highly volatile - sentiment can shift quickly
- Bot activity is prevalent - look for organic signals
- Influencer manipulation is common - verify across sources

### 2. Timing Matters
- US/EU overlap often sees highest activity
- Asian session can have different sentiment
- Weekend sentiment differs from weekdays

### 3. Filter for Quality
```python
# Focus on accounts with history, not fresh accounts pumping
"Focus on accounts older than 6 months with consistent posting history"
```

### 4. Watch for Coordinated Activity
```python
# Detect potential pump and dump schemes
"Flag any coordinated posting patterns or sudden volume spikes from new accounts"
```

## Related Skills
- `xai-stock-sentiment` - Stock analysis
- `xai-x-search` - Raw X search
- `xai-sentiment` - General sentiment
- `xai-financial-integration` - Price data integration

## References
- [xAI Agent Tools](https://x.ai/news/grok-4-1-fast/)
- [Crypto Sentiment Guide](https://docs.x.ai/cookbook)
