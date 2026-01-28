---
name: trading-analysis
description: Generate professional investment reports for stocks and ETFs. Use when user requests market analysis, investment reports, stock analysis, or trading recommendations for financial instruments (SPY, AAPL, TSLA, etc.). Creates institutional-grade reports with technical indicators, AI-powered insights, charts, and investment recommendations.
---

# Trading Analysis & Investment Report Generator

This skill generates comprehensive investment reports combining real-time market data, technical analysis, Claude AI insights, and professional visualizations.

## What This Skill Does

- Downloads real-time market data from Yahoo Finance
- Calculates 10+ technical indicators (RSI, MACD, Moving Averages, Bollinger Bands, etc.)
- Analyzes market conditions using Claude AI
- Generates 4 types of professional charts (price, indicators, volatility, dashboard)
- Creates institutional-grade investment reports in Markdown format
- Exports structured data in JSON format

## When to Use This Skill

Use this skill when the user requests:
- Investment reports or analysis for specific stocks/ETFs
- Market analysis with technical indicators
- Trading recommendations based on current market conditions
- Professional reports for clients or portfolio review
- Comparative analysis across multiple symbols

## Input Requirements

**Required:**
- `symbol`: Stock ticker (e.g., SPY, AAPL, TSLA, QQQ)

**Optional:**
- `client_name`: Name of the client/investor (default: "Institutional Investors")
- `report_title`: Custom report title (auto-generated if not provided)
- `period`: Historical data period (default: "6mo")

## Output Files

The skill generates the following files in the `reports/` directory:

1. **Markdown Report** (`{SYMBOL}_analysis_report_{timestamp}.md`)
   - Executive summary with sentiment and recommendation
   - Market overview with price tables
   - Technical analysis with indicators
   - AI-powered market intelligence
   - Investment recommendations with entry/exit criteria
   - Risk assessment
   - Chart references

2. **JSON Data** (`{SYMBOL}_analysis_report_{timestamp}_data.json`)
   - Structured data for programmatic access
   - All metrics and analysis results

3. **Charts** (PNG format, 300 DPI):
   - `{SYMBOL}_price_chart.png`: Price with moving averages
   - `{SYMBOL}_indicators_chart.png`: RSI and MACD
   - `{SYMBOL}_volatility_chart.png`: Historical volatility
   - `{SYMBOL}_summary_dashboard.png`: Performance dashboard

## Example Usage

**Simple request:**
"Generate an investment report for SPY"

**Detailed request:**
"Create a market analysis report for AAPL for Acme Capital with the title 'Q4 2025 AAPL Investment Strategy'"

**Multiple symbols:**
"Generate investment reports for SPY, QQQ, and DIA"

## Report Quality

- **Format**: Institutional-grade, suitable for client presentations
- **Data Accuracy**: Real-time market data with verified calculations
- **Visual Quality**: High-resolution charts (300 DPI, print-ready)
- **AI Analysis**: Claude-powered market sentiment and risk assessment
- **Completeness**: Executive summary, technical analysis, recommendations, disclaimers

## Technical Details

- **Data Source**: Yahoo Finance API
- **AI Model**: Claude 3.7 Sonnet (configurable)
- **Chart Resolution**: 300 DPI (print quality)
- **Report Format**: GitHub-flavored Markdown
- **Processing Time**: ~15-30 seconds per symbol

## Safety & Disclaimers

All reports automatically include:
- Investment disclaimer
- Risk warnings
- Clarification that this is informational, not financial advice
- Recommendation to consult qualified financial advisors

## Notes

- Requires valid Anthropic API key in `.env` file
- Requires internet connection for market data
- Historical data limited by Yahoo Finance availability
- AI analysis is based on technical data, not fundamental analysis
