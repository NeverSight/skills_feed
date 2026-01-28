---
name: xai-financial-integration
description: Integrate xAI Grok sentiment with FinnHub, Twelve Data, Alpha Vantage, and FMP financial APIs. Use when combining social sentiment with price data, fundamentals, and news for comprehensive analysis.
version: 1.0.0
---

# xAI Financial Integration

Combine Grok's real-time Twitter/X sentiment with traditional financial data APIs for comprehensive analysis.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      xAI Grok API                           │
│         (Real-time X sentiment, web search)                 │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                   Integration Layer                          │
│   Combine sentiment + price + fundamentals + news           │
└─────────────────────────────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│   FinnHub     │   │  Twelve Data  │   │     FMP       │
│  (Quotes,     │   │  (Indicators, │   │ (Fundamentals,│
│   News)       │   │   History)    │   │   DCF)        │
└───────────────┘   └───────────────┘   └───────────────┘
```

## Quick Start

```python
import os
from openai import OpenAI
import requests

# Initialize clients
xai_client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),
    base_url="https://api.x.ai/v1"
)

FINNHUB_KEY = os.getenv("FINNHUB_API_KEY")
TWELVEDATA_KEY = os.getenv("TWELVEDATA_API_KEY")
FMP_KEY = os.getenv("FMP_API_KEY")

def comprehensive_analysis(ticker: str) -> dict:
    """Complete analysis combining sentiment + price + fundamentals."""

    # 1. Get price data from FinnHub
    price = requests.get(
        f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_KEY}"
    ).json()

    # 2. Get fundamentals from FMP
    fundamentals = requests.get(
        f"https://financialmodelingprep.com/stable/key-metrics?symbol={ticker}&apikey={FMP_KEY}"
    ).json()

    # 3. Get sentiment from xAI
    sentiment_response = xai_client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Analyze X sentiment for ${ticker} given this context:

            Current Price: ${price.get('c', 'N/A')}
            Change: {price.get('dp', 0):.2f}%

            Return JSON with sentiment analysis and trading signals."""
        }]
    )
    sentiment = sentiment_response.choices[0].message.content

    return {
        "ticker": ticker,
        "price": price,
        "fundamentals": fundamentals[0] if fundamentals else {},
        "sentiment": sentiment
    }
```

## Integration Functions

### Price + Sentiment Correlation
```python
def price_sentiment_analysis(ticker: str) -> dict:
    """Analyze correlation between price action and sentiment."""

    # Get price data
    price = requests.get(
        f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_KEY}"
    ).json()

    # Get sentiment with price context
    response = xai_client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Analyze ${ticker} sentiment in context of price:

            Current: ${price['c']:.2f}
            Change: {price['dp']:.2f}%
            High: ${price['h']:.2f}
            Low: ${price['l']:.2f}

            Return JSON:
            {{
                "sentiment_score": -1 to 1,
                "price_sentiment_alignment": "aligned/divergent/neutral",
                "divergence_signal": {{
                    "detected": true/false,
                    "type": "bullish divergence/bearish divergence/none",
                    "interpretation": "..."
                }},
                "trading_signal": "buy/sell/hold",
                "confidence": 0 to 1,
                "rationale": "..."
            }}"""
        }]
    )
    return response.choices[0].message.content
```

### Technical + Sentiment
```python
def technical_sentiment_analysis(ticker: str) -> dict:
    """Combine technical indicators with sentiment."""

    # Get RSI from Twelve Data
    rsi = requests.get(
        f"https://api.twelvedata.com/rsi?symbol={ticker}&interval=1day&outputsize=1&apikey={TWELVEDATA_KEY}"
    ).json()

    # Get SMA
    sma = requests.get(
        f"https://api.twelvedata.com/sma?symbol={ticker}&interval=1day&time_period=20&outputsize=1&apikey={TWELVEDATA_KEY}"
    ).json()

    rsi_value = rsi.get('values', [{}])[0].get('rsi', 'N/A')
    sma_value = sma.get('values', [{}])[0].get('sma', 'N/A')

    # Combine with sentiment
    response = xai_client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Analyze ${ticker} combining technicals and X sentiment:

            Technical Indicators:
            - RSI(14): {rsi_value}
            - SMA(20): ${sma_value}

            Search X for sentiment and return JSON:
            {{
                "technical_signal": "overbought/neutral/oversold",
                "sentiment_signal": "bullish/neutral/bearish",
                "confluence": {{
                    "signals_aligned": true/false,
                    "strength": "strong/moderate/weak"
                }},
                "recommendation": {{
                    "action": "buy/sell/hold",
                    "entry_zone": "...",
                    "stop_loss": "...",
                    "confidence": 0 to 1
                }}
            }}"""
        }]
    )
    return response.choices[0].message.content
```

### Fundamental + Sentiment
```python
def fundamental_sentiment_analysis(ticker: str) -> dict:
    """Combine fundamental data with sentiment."""

    # Get fundamentals from FMP
    metrics = requests.get(
        f"https://financialmodelingprep.com/stable/key-metrics?symbol={ticker}&period=annual&limit=1&apikey={FMP_KEY}"
    ).json()

    ratios = requests.get(
        f"https://financialmodelingprep.com/stable/financial-ratios?symbol={ticker}&period=annual&limit=1&apikey={FMP_KEY}"
    ).json()

    m = metrics[0] if metrics else {}
    r = ratios[0] if ratios else {}

    # Combine with sentiment
    response = xai_client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Analyze ${ticker} combining fundamentals and X sentiment:

            Fundamentals:
            - P/E Ratio: {r.get('priceEarningsRatio', 'N/A')}
            - P/B Ratio: {r.get('priceToBookRatio', 'N/A')}
            - ROE: {r.get('returnOnEquity', 'N/A')}
            - Debt/Equity: {r.get('debtEquityRatio', 'N/A')}

            Search X for what investors are saying about valuation.

            Return JSON:
            {{
                "fundamental_view": "undervalued/fairly valued/overvalued",
                "sentiment_on_valuation": {{
                    "score": -1 to 1,
                    "key_concerns": [...],
                    "bullish_arguments": [...]
                }},
                "smart_money_sentiment": "...",
                "retail_sentiment": "...",
                "valuation_consensus": "...",
                "investment_thesis": "..."
            }}"""
        }]
    )
    return response.choices[0].message.content
```

### News + Sentiment Validation
```python
def news_sentiment_validation(ticker: str) -> dict:
    """Validate news sentiment against X reaction."""

    # Get news from FinnHub
    from datetime import datetime, timedelta
    end = datetime.now()
    start = end - timedelta(days=3)

    news = requests.get(
        f"https://finnhub.io/api/v1/company-news?symbol={ticker}"
        f"&from={start.strftime('%Y-%m-%d')}&to={end.strftime('%Y-%m-%d')}"
        f"&token={FINNHUB_KEY}"
    ).json()

    headlines = [n['headline'] for n in news[:5]] if news else []

    # Compare with X reaction
    response = xai_client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Compare these news headlines for ${ticker} with X reaction:

            Recent Headlines:
            {chr(10).join(['- ' + h for h in headlines])}

            Search X for reaction to these news items.

            Return JSON:
            {{
                "news_sentiment": "positive/negative/neutral",
                "x_reaction": "positive/negative/neutral",
                "alignment": "aligned/divergent/mixed",
                "notable_reactions": [...],
                "market_interpretation": "...",
                "trading_implication": "..."
            }}"""
        }]
    )
    return response.choices[0].message.content
```

### Multi-Asset Correlation
```python
def multi_asset_sentiment(tickers: list) -> dict:
    """Analyze sentiment correlation across multiple assets."""

    tickers_str = ", ".join([f"${t}" for t in tickers])

    # Get all quotes
    quotes = {}
    for ticker in tickers:
        quote = requests.get(
            f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_KEY}"
        ).json()
        quotes[ticker] = f"${quote['c']:.2f} ({quote['dp']:+.2f}%)"

    quote_summary = "\n".join([f"- {t}: {p}" for t, p in quotes.items()])

    response = xai_client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Analyze X sentiment correlation for: {tickers_str}

            Current Prices:
{quote_summary}

            Return JSON:
            {{
                "individual_sentiment": [
                    {{"ticker": "...", "score": -1 to 1}}
                ],
                "correlations": [
                    {{"pair": "X-Y", "sentiment_correlation": "positive/negative/none"}}
                ],
                "sector_theme": "...",
                "rotation_signals": "...",
                "best_opportunity": "...",
                "relative_strength": [...]
            }}"""
        }]
    )
    return response.choices[0].message.content
```

### Earnings Reaction Analysis
```python
def earnings_reaction_analysis(ticker: str) -> dict:
    """Comprehensive post-earnings analysis."""

    # Get earnings data from FinnHub
    earnings = requests.get(
        f"https://finnhub.io/api/v1/stock/earnings?symbol={ticker}&token={FINNHUB_KEY}"
    ).json()

    latest = earnings[0] if earnings else {}

    response = xai_client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Analyze post-earnings reaction for ${ticker}:

            Last Earnings:
            - EPS Actual: {latest.get('actual', 'N/A')}
            - EPS Estimate: {latest.get('estimate', 'N/A')}
            - Surprise: {latest.get('surprisePercent', 'N/A')}%

            Search X for investor reaction and return JSON:
            {{
                "earnings_result": "beat/met/missed",
                "x_reaction": {{
                    "immediate": "positive/negative/mixed",
                    "sentiment_score": -1 to 1
                }},
                "key_topics": {{
                    "positives": [...],
                    "concerns": [...]
                }},
                "guidance_reaction": "...",
                "analyst_mentions": [...],
                "price_target_sentiment": "...",
                "trading_recommendation": "..."
            }}"""
        }]
    )
    return response.choices[0].message.content
```

## Complete Dashboard

```python
def full_stock_dashboard(ticker: str) -> dict:
    """Complete stock analysis dashboard."""

    # Gather all data
    quote = requests.get(
        f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_KEY}"
    ).json()

    profile = requests.get(
        f"https://finnhub.io/api/v1/stock/profile2?symbol={ticker}&token={FINNHUB_KEY}"
    ).json()

    metrics = requests.get(
        f"https://financialmodelingprep.com/stable/key-metrics?symbol={ticker}&limit=1&apikey={FMP_KEY}"
    ).json()

    # Create comprehensive prompt
    response = xai_client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Create comprehensive dashboard for ${ticker}:

            Company: {profile.get('name', ticker)}
            Sector: {profile.get('finnhubIndustry', 'N/A')}
            Market Cap: ${profile.get('marketCapitalization', 0):,.0f}M

            Price Data:
            - Current: ${quote['c']:.2f}
            - Change: {quote['dp']:.2f}%
            - High/Low: ${quote['h']:.2f} / ${quote['l']:.2f}

            Search X for sentiment and create dashboard JSON:
            {{
                "summary": {{
                    "ticker": "{ticker}",
                    "name": "...",
                    "price": ...,
                    "change_percent": ...
                }},
                "sentiment_analysis": {{
                    "overall_score": -1 to 1,
                    "label": "...",
                    "volume": "high/med/low",
                    "trend": "improving/stable/declining"
                }},
                "key_metrics": {{
                    "pe_ratio": ...,
                    "market_cap": ...,
                    "sector": "..."
                }},
                "social_signals": {{
                    "retail_sentiment": "...",
                    "influencer_sentiment": "...",
                    "news_reaction": "..."
                }},
                "catalysts": {{
                    "upcoming": [...],
                    "recent": [...]
                }},
                "risks": [...],
                "opportunities": [...],
                "recommendation": {{
                    "action": "buy/sell/hold",
                    "confidence": 0 to 1,
                    "rationale": "..."
                }}
            }}"""
        }]
    )
    return response.choices[0].message.content
```

## Environment Setup

```bash
# .env file
XAI_API_KEY=xai-your-key
FINNHUB_API_KEY=your-finnhub-key
TWELVEDATA_API_KEY=your-twelvedata-key
ALPHAVANTAGE_API_KEY=your-alphavantage-key
FMP_API_KEY=your-fmp-key
```

## Related Skills
- `xai-stock-sentiment` - Stock sentiment
- `xai-crypto-sentiment` - Crypto sentiment
- `finnhub-api` - FinnHub integration
- `twelvedata-api` - Twelve Data integration
- `fmp-api` - FMP integration
- `alphavantage-api` - Alpha Vantage integration

## References
- [xAI Documentation](https://docs.x.ai)
- [FinnHub API](https://finnhub.io/docs/api)
- [Twelve Data API](https://twelvedata.com/docs)
- [FMP API](https://site.financialmodelingprep.com/developer/docs)
