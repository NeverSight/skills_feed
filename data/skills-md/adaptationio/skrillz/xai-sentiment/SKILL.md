---
name: xai-sentiment
description: Real-time sentiment analysis on Twitter/X using Grok. Use when analyzing social sentiment, tracking market mood, or measuring public opinion on topics.
version: 1.0.0
---

# xAI Sentiment Analysis

Real-time sentiment analysis on Twitter/X content using Grok's native integration and built-in NLP capabilities.

## Quick Start

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),
    base_url="https://api.x.ai/v1"
)

def analyze_sentiment(topic: str) -> dict:
    """Analyze sentiment for a topic on X."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Analyze sentiment on X for: {topic}

            Search recent posts and return JSON:
            {{
                "topic": "{topic}",
                "sentiment": "bullish" | "bearish" | "neutral",
                "score": -1.0 to 1.0,
                "confidence": 0.0 to 1.0,
                "positive_percent": 0-100,
                "negative_percent": 0-100,
                "neutral_percent": 0-100,
                "sample_size": number,
                "key_themes": ["theme1", "theme2"],
                "notable_posts": [
                    {{"author": "@handle", "summary": "...", "sentiment": "..."}}
                ]
            }}"""
        }]
    )
    return response.choices[0].message.content

# Example
result = analyze_sentiment("$AAPL stock")
print(result)
```

## Sentiment Score Scale

| Score Range | Label | Description |
|-------------|-------|-------------|
| 0.6 to 1.0 | Very Bullish | Strong positive sentiment |
| 0.2 to 0.6 | Bullish | Moderately positive |
| -0.2 to 0.2 | Neutral | Mixed or balanced |
| -0.6 to -0.2 | Bearish | Moderately negative |
| -1.0 to -0.6 | Very Bearish | Strong negative sentiment |

## Sentiment Analysis Functions

### Basic Sentiment
```python
def get_basic_sentiment(query: str) -> dict:
    """Get simple sentiment score."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Search X for "{query}" and analyze sentiment.
            Return only JSON:
            {{"positive": 0-100, "neutral": 0-100, "negative": 0-100, "score": -1 to 1}}"""
        }]
    )
    return response.choices[0].message.content
```

### Detailed Sentiment Analysis
```python
def get_detailed_sentiment(topic: str, timeframe: str = "24h") -> dict:
    """Get comprehensive sentiment analysis."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Perform detailed sentiment analysis on X for: {topic}
            Timeframe: Last {timeframe}

            Return JSON:
            {{
                "overall_sentiment": {{
                    "label": "bullish/bearish/neutral",
                    "score": -1 to 1,
                    "confidence": 0 to 1
                }},
                "breakdown": {{
                    "positive": {{"percent": 0-100, "count": n}},
                    "negative": {{"percent": 0-100, "count": n}},
                    "neutral": {{"percent": 0-100, "count": n}}
                }},
                "themes": [
                    {{"theme": "...", "sentiment": "...", "frequency": n}}
                ],
                "influencer_sentiment": [
                    {{"handle": "@...", "sentiment": "...", "followers": n}}
                ],
                "trending_hashtags": ["#tag1", "#tag2"],
                "sentiment_drivers": {{
                    "positive_factors": ["..."],
                    "negative_factors": ["..."]
                }}
            }}"""
        }]
    )
    return response.choices[0].message.content
```

### Comparative Sentiment
```python
def compare_sentiment(topics: list) -> dict:
    """Compare sentiment across multiple topics."""
    topics_str = ", ".join(topics)
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Compare X sentiment for: {topics_str}

            Return JSON:
            {{
                "comparison": [
                    {{
                        "topic": "...",
                        "sentiment_score": -1 to 1,
                        "volume": "high/medium/low",
                        "trend": "improving/declining/stable"
                    }}
                ],
                "winner": "most positive topic",
                "loser": "most negative topic",
                "insights": ["..."]
            }}"""
        }]
    )
    return response.choices[0].message.content
```

### Sentiment Over Time
```python
def sentiment_timeline(topic: str, periods: list) -> dict:
    """Track sentiment changes over time."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Analyze how sentiment for "{topic}" has changed on X.

            Return JSON with sentiment for different time periods:
            {{
                "topic": "{topic}",
                "timeline": [
                    {{"period": "last hour", "score": -1 to 1}},
                    {{"period": "last 24 hours", "score": -1 to 1}},
                    {{"period": "last week", "score": -1 to 1}}
                ],
                "trend": "improving/declining/stable",
                "momentum": "accelerating/decelerating/steady",
                "key_events": [
                    {{"time": "...", "event": "...", "impact": "..."}}
                ]
            }}"""
        }]
    )
    return response.choices[0].message.content
```

## Financial Sentiment Analysis

### Stock Sentiment
```python
def stock_sentiment(ticker: str) -> dict:
    """Analyze stock sentiment with financial context."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Analyze X sentiment for ${ticker} stock.

            Return JSON:
            {{
                "ticker": "{ticker}",
                "sentiment": {{
                    "overall": "bullish/bearish/neutral",
                    "score": -1 to 1,
                    "strength": "strong/moderate/weak"
                }},
                "trading_signals": {{
                    "retail_sentiment": "...",
                    "smart_money_mentions": "...",
                    "options_chatter": "..."
                }},
                "catalysts_mentioned": ["earnings", "product", "macro"],
                "price_predictions": {{
                    "bullish_targets": [...],
                    "bearish_targets": [...]
                }},
                "risk_factors": ["..."],
                "recommendation": "..."
            }}"""
        }]
    )
    return response.choices[0].message.content
```

### Crypto Sentiment
```python
def crypto_sentiment(coin: str) -> dict:
    """Analyze cryptocurrency sentiment."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Analyze X sentiment for {coin} cryptocurrency.

            Return JSON:
            {{
                "coin": "{coin}",
                "sentiment_score": -1 to 1,
                "fear_greed_indicator": "extreme fear/fear/neutral/greed/extreme greed",
                "whale_mentions": "high/medium/low",
                "influencer_sentiment": [...],
                "trending_narratives": [...],
                "fud_detection": {{
                    "level": "high/medium/low",
                    "sources": [...]
                }},
                "fomo_detection": {{
                    "level": "high/medium/low",
                    "triggers": [...]
                }}
            }}"""
        }]
    )
    return response.choices[0].message.content
```

## Batch Sentiment Analysis

```python
def batch_sentiment(topics: list) -> list:
    """Analyze sentiment for multiple topics efficiently."""
    topics_formatted = "\n".join([f"- {t}" for t in topics])

    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Analyze X sentiment for each:
{topics_formatted}

Return JSON array:
[
    {{"topic": "...", "score": -1 to 1, "label": "...", "volume": "high/med/low"}}
]"""
        }]
    )
    return response.choices[0].message.content
```

## Sentiment Alerts

```python
def check_sentiment_alert(topic: str, threshold: float = 0.5) -> dict:
    """Check if sentiment has crossed alert threshold."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Check X sentiment for {topic}.
            Alert threshold: {threshold} (positive) or {-threshold} (negative)

            Return JSON:
            {{
                "topic": "{topic}",
                "current_score": -1 to 1,
                "alert_triggered": true/false,
                "alert_type": "bullish/bearish/none",
                "reason": "...",
                "recommended_action": "..."
            }}"""
        }]
    )
    return response.choices[0].message.content
```

## Best Practices

### 1. Request Confidence Scores
Always ask for confidence levels to gauge reliability.

### 2. Specify Sample Size
Request the number of posts analyzed for context.

### 3. Account for Sarcasm
Grok may misinterpret sarcasm - request explicit sarcasm detection:
```python
"Note: Flag any potentially sarcastic posts separately"
```

### 4. Filter by Quality
Combine with handle filtering for higher-quality signals:
```python
"Focus on verified accounts and accounts with >10k followers"
```

### 5. Combine with Price Data
Sentiment is most valuable when combined with price action.

## Limitations

| Limitation | Mitigation |
|------------|------------|
| Sarcasm detection | Request explicit flagging |
| Bot content | Ask to filter suspicious patterns |
| Historical accuracy | Focus on recent data |
| Sample size | Request volume metrics |

## Related Skills
- `xai-x-search` - X search functionality
- `xai-stock-sentiment` - Stock-specific analysis
- `xai-crypto-sentiment` - Crypto analysis
- `xai-financial-integration` - Combine with price data

## References
- [xAI Cookbook - Sentiment Analysis](https://docs.x.ai/cookbook/examples/sentiment_analysis_on_x)
- [Grok 4.1 Fast](https://x.ai/news/grok-4-1-fast/)
