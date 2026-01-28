---
name: xai-stock-sentiment
description: Real-time stock sentiment analysis using Twitter/X data via Grok. Use when analyzing stock ticker sentiment, tracking retail investor mood, or gauging market reaction to events.
version: 1.0.0
---

# xAI Stock Sentiment Analysis

Real-time stock sentiment from Twitter/X using Grok's native integration - a unique capability for financial analysis.

## Quick Start

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),
    base_url="https://api.x.ai/v1"
)

def get_stock_sentiment(ticker: str) -> dict:
    """Get real-time sentiment for a stock ticker."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Analyze X sentiment for ${ticker} stock.

            Search recent posts and return JSON:
            {{
                "ticker": "{ticker}",
                "sentiment": {{
                    "overall": "bullish" | "bearish" | "neutral",
                    "score": -1.0 to 1.0,
                    "confidence": 0.0 to 1.0
                }},
                "metrics": {{
                    "bullish_percent": 0-100,
                    "bearish_percent": 0-100,
                    "neutral_percent": 0-100,
                    "volume": "high" | "medium" | "low",
                    "velocity": "increasing" | "stable" | "decreasing"
                }},
                "key_drivers": ["driver1", "driver2"],
                "notable_mentions": [
                    {{"user": "@handle", "summary": "...", "influence": "high/med/low"}}
                ],
                "risks": ["risk1", "risk2"],
                "catalysts": ["catalyst1", "catalyst2"]
            }}"""
        }]
    )
    return response.choices[0].message.content

# Example
sentiment = get_stock_sentiment("AAPL")
print(sentiment)
```

## Financial Handles to Track

```python
FINANCIAL_INFLUENCERS = [
    # Breaking News
    "DeItaone",
    "FirstSquawk",
    "LiveSquawk",

    # Options Flow
    "unusual_whales",
    "OptionsHawk",

    # Analysis
    "jimcramer",
    "Carl_C_Icahn",
    "elerianm",

    # Retail Sentiment
    "wallstreetbets",
    "StockMarketNewz"
]
```

## Sentiment Functions

### Single Stock Analysis
```python
def analyze_single_stock(ticker: str, timeframe: str = "24h") -> dict:
    """Comprehensive single stock sentiment analysis."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Perform deep sentiment analysis for ${ticker} on X.
            Timeframe: Last {timeframe}

            Return comprehensive JSON:
            {{
                "ticker": "{ticker}",
                "timestamp": "current time",
                "sentiment_analysis": {{
                    "overall_score": -1 to 1,
                    "label": "very bullish/bullish/neutral/bearish/very bearish",
                    "confidence": 0 to 1,
                    "sample_size": n
                }},
                "breakdown": {{
                    "retail_sentiment": {{
                        "score": -1 to 1,
                        "volume": "high/med/low",
                        "trending_hashtags": [...]
                    }},
                    "influencer_sentiment": {{
                        "score": -1 to 1,
                        "key_opinions": [...]
                    }},
                    "news_reaction": {{
                        "recent_news": [...],
                        "reaction_sentiment": -1 to 1
                    }}
                }},
                "trading_signals": {{
                    "momentum": "bullish/bearish/neutral",
                    "volume_trend": "increasing/stable/decreasing",
                    "unusual_activity": true/false,
                    "options_chatter": "calls heavy/puts heavy/balanced/minimal"
                }},
                "catalysts": {{
                    "upcoming": [...],
                    "recent": [...]
                }},
                "risks": [...],
                "summary": "2-3 sentence summary"
            }}"""
        }]
    )
    return response.choices[0].message.content
```

### Multi-Stock Comparison
```python
def compare_stocks(tickers: list) -> dict:
    """Compare sentiment across multiple stocks."""
    tickers_str = ", ".join([f"${t}" for t in tickers])

    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Compare X sentiment for: {tickers_str}

            Return JSON:
            {{
                "comparison": [
                    {{
                        "ticker": "...",
                        "sentiment_score": -1 to 1,
                        "volume": "high/med/low",
                        "trend": "improving/stable/declining",
                        "key_driver": "..."
                    }}
                ],
                "rankings": {{
                    "most_bullish": "TICKER",
                    "most_bearish": "TICKER",
                    "highest_volume": "TICKER",
                    "best_momentum": "TICKER"
                }},
                "sector_sentiment": "...",
                "recommendation": "..."
            }}"""
        }]
    )
    return response.choices[0].message.content
```

### Earnings Reaction
```python
def earnings_reaction(ticker: str) -> dict:
    """Analyze X reaction to earnings announcement."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Analyze X reaction to ${ticker} earnings.

            Search for post-earnings discussion and return JSON:
            {{
                "ticker": "{ticker}",
                "earnings_reaction": {{
                    "immediate_sentiment": "positive/negative/mixed",
                    "sentiment_score": -1 to 1,
                    "surprise_reaction": "beat expectations/met/missed"
                }},
                "key_topics": {{
                    "positives_mentioned": [...],
                    "concerns_raised": [...],
                    "guidance_reaction": "..."
                }},
                "influencer_reactions": [
                    {{"user": "@handle", "stance": "bullish/bearish", "key_point": "..."}}
                ],
                "price_action_sentiment": {{
                    "pre_market_mood": "...",
                    "opening_reaction": "..."
                }},
                "forward_outlook": "bullish/bearish/cautious"
            }}"""
        }]
    )
    return response.choices[0].message.content
```

### Sector Sentiment
```python
def sector_sentiment(sector: str, tickers: list = None) -> dict:
    """Analyze sentiment for an entire sector."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Analyze X sentiment for the {sector} sector.
            {"Key tickers to focus on: " + ", ".join([f"${t}" for t in tickers]) if tickers else ""}

            Return JSON:
            {{
                "sector": "{sector}",
                "overall_sentiment": {{
                    "score": -1 to 1,
                    "label": "bullish/bearish/neutral",
                    "trend": "improving/stable/declining"
                }},
                "key_themes": [...],
                "leaders": [
                    {{"ticker": "...", "sentiment": ..., "reason": "..."}}
                ],
                "laggards": [
                    {{"ticker": "...", "sentiment": ..., "reason": "..."}}
                ],
                "sector_catalysts": [...],
                "macro_factors": [...]
            }}"""
        }]
    )
    return response.choices[0].message.content
```

### Unusual Activity Detection
```python
def detect_unusual_activity(ticker: str) -> dict:
    """Detect unusual sentiment or activity for a stock."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Check for unusual activity on X for ${ticker}.

            Look for:
            - Unusual volume of mentions
            - Sudden sentiment shifts
            - Whale/insider mentions
            - Breaking news
            - Options flow chatter

            Return JSON:
            {{
                "ticker": "{ticker}",
                "unusual_activity_detected": true/false,
                "alerts": [
                    {{
                        "type": "volume_spike/sentiment_shift/news_break/whale_alert/options_unusual",
                        "severity": "high/medium/low",
                        "description": "...",
                        "source": "..."
                    }}
                ],
                "normal_baseline": {{
                    "typical_mention_volume": "...",
                    "typical_sentiment": ...
                }},
                "current_state": {{
                    "mention_volume": "...",
                    "sentiment": ...
                }},
                "deviation": "significant/moderate/minor/none",
                "recommended_action": "..."
            }}"""
        }]
    )
    return response.choices[0].message.content
```

## Integration with Price Data

```python
def sentiment_with_price(ticker: str, price_data: dict) -> dict:
    """Combine sentiment with price data for context."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Analyze ${ticker} sentiment in context of price action:

            Current Price: ${price_data.get('price', 'N/A')}
            Change: {price_data.get('change_percent', 'N/A')}%
            52-Week High: ${price_data.get('high_52w', 'N/A')}
            52-Week Low: ${price_data.get('low_52w', 'N/A')}

            Search X for current sentiment and analyze:
            1. Is sentiment aligned with price action?
            2. Any divergence signals?
            3. Support/resistance levels mentioned?

            Return JSON with sentiment-price analysis."""
        }]
    )
    return response.choices[0].message.content
```

## Watchlist Monitoring

```python
def monitor_watchlist(tickers: list) -> dict:
    """Monitor sentiment for a watchlist of stocks."""
    tickers_str = ", ".join([f"${t}" for t in tickers])

    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Monitor X sentiment for watchlist: {tickers_str}

            Return JSON:
            {{
                "timestamp": "...",
                "stocks": [
                    {{
                        "ticker": "...",
                        "sentiment_score": -1 to 1,
                        "change_from_yesterday": -1 to 1,
                        "alert_level": "none/watch/action",
                        "key_update": "..."
                    }}
                ],
                "alerts": [
                    {{"ticker": "...", "alert_type": "...", "message": "..."}}
                ],
                "market_mood": "risk-on/risk-off/mixed"
            }}"""
        }]
    )
    return response.choices[0].message.content
```

## Best Practices

### 1. Time Your Queries
- Pre-market: Catch overnight sentiment
- Market open: Capture opening reaction
- After hours: Earnings reactions

### 2. Combine Data Sources
```python
# Best signal = sentiment + price + volume
x_sentiment = get_stock_sentiment(ticker)
price_data = finnhub.get_quote(ticker)
fundamentals = fmp.get_financials(ticker)
```

### 3. Filter for Quality
Focus on verified accounts and high-follower influencers.

### 4. Watch for Manipulation
- Sudden coordinated pumps
- Bot-like patterns
- Unrealistic claims

## Related Skills
- `xai-x-search` - Raw X search
- `xai-sentiment` - General sentiment
- `xai-crypto-sentiment` - Crypto focus
- `xai-financial-integration` - Data integration
- `finnhub-api` - Price data
- `fmp-api` - Fundamentals

## References
- [xAI Cookbook](https://docs.x.ai/cookbook)
- [Agent Tools](https://x.ai/news/grok-4-1-fast/)
