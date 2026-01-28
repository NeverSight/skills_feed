---
name: financial-analysis-agent
description: Create agents for financial analysis, investment research, and portfolio management. Covers financial data processing, risk analysis, and recommendation generation. Use when building investment analysis tools, robo-advisors, portfolio trackers, or financial intelligence systems.
---

# Financial Analysis Agent

Build intelligent financial analysis agents that evaluate investments, assess risks, and generate data-driven recommendations.

## Financial Data Integration

See [examples/financial_data_collector.py](examples/financial_data_collector.py) for the `FinancialDataCollector` class that:
- Integrates with yfinance for stock data
- Retrieves financial statements (income, balance sheet, cash flow)
- Fetches key metrics (market cap, PE ratio, dividend yield, etc.)

## Financial Analysis Techniques

### Technical Analysis
See [examples/technical_analyzer.py](examples/technical_analyzer.py) for `TechnicalAnalyzer`:
- Moving averages calculation
- Relative Strength Index (RSI)
- Support and resistance level identification

### Fundamental Analysis
See [examples/fundamental_analyzer.py](examples/fundamental_analyzer.py) for `FundamentalAnalyzer`:
- Profitability ratios (gross margin, operating margin, net margin, ROA, ROE)
- Valuation ratios (PE, PB, PEG, price-to-sales)
- Liquidity ratios (current ratio, quick ratio, debt-to-equity)

### Risk Assessment
See [examples/risk_analyzer.py](examples/risk_analyzer.py) for `RiskAnalyzer`:
- Volatility calculation
- Value at Risk (VaR) assessment
- Sharpe Ratio calculation
- Company risk assessment

## Investment Recommendations

See [examples/investment_recommender.py](examples/investment_recommender.py) for `InvestmentRecommender`:
- Generates recommendations (Strong Buy, Buy, Hold, Sell, Strong Sell)
- Calculates investment scores based on technical and fundamental signals
- Provides confidence levels and risk assessments

## Portfolio Management

See [examples/portfolio_manager.py](examples/portfolio_manager.py) for `PortfolioManager`:
- Calculate portfolio total value
- Rebalance portfolio based on target allocations
- Assess portfolio risk and volatility

## Market Intelligence

Build market intelligence capabilities by:
- Analyzing overall market trends and sector performance
- Calculating market volatility indices
- Fetching economic indicators
- Identifying undervalued, growth, and dividend opportunities

## Best Practices

### Analysis Quality
- ✓ Use multiple data sources
- ✓ Cross-validate findings
- ✓ Document assumptions
- ✓ Consider time horizons
- ✓ Account for fees and taxes

### Risk Management
- ✓ Assess downside risk
- ✓ Implement stop losses
- ✓ Diversify appropriately
- ✓ Position size accordingly
- ✓ Review regularly

### Ethical Considerations
- ✓ Disclose conflicts of interest
- ✓ Avoid market manipulation
- ✓ Base recommendations on analysis
- ✓ Update recommendations regularly
- ✓ Acknowledge limitations

## Tools & Data Sources

### Data APIs
- yfinance
- Alpha Vantage
- IEX Cloud
- Polygon.io
- Yahoo Finance

### Analysis Libraries
- pandas
- NumPy
- scikit-learn
- TA-Lib
- statsmodels

## Getting Started

1. Collect financial data
2. Perform technical analysis
3. Analyze fundamentals
4. Assess risks
5. Generate recommendations
6. Monitor positions
7. Rebalance periodically

