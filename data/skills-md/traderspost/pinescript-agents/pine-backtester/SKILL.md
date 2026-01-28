---
name: pine-backtester
description: Implements comprehensive backtesting capabilities for Pine Script indicators and strategies. Use when adding performance metrics, trade analysis, equity curves, win rates, drawdown tracking, or statistical validation. Triggers on "backtest", "performance", "metrics", "win rate", "drawdown", or testing requests.
---

# Pine Script Backtester

Specialized in adding comprehensive testing and validation capabilities to Pine Script indicators and strategies.

## Core Responsibilities

### Strategy Performance Metrics
- Win rate and profit factor
- Maximum drawdown analysis
- Sharpe and Sortino ratios
- Risk-adjusted returns
- Trade distribution analysis

### Indicator Accuracy Testing
- Signal accuracy measurements
- False positive/negative rates
- Lag analysis
- Divergence detection accuracy
- Multi-timeframe validation

### Statistical Analysis
- Monte Carlo simulations
- Walk-forward analysis
- Confidence intervals
- Statistical significance tests
- Correlation analysis

## Backtesting Components

### 1. Comprehensive Strategy Metrics Table
```pinescript
// Strategy Performance Metrics
var table metricsTable = table.new(position.bottom_right, 2, 15, bgcolor=color.new(color.black, 90))

if barstate.islastconfirmedhistory
    wins = strategy.wintrades
    losses = strategy.losstrades
    totalTrades = wins + losses
    winRate = totalTrades > 0 ? (wins / totalTrades) * 100 : 0

    avgWin = strategy.grossprofit / math.max(wins, 1)
    avgLoss = math.abs(strategy.grossloss) / math.max(losses, 1)
    profitFactor = avgLoss > 0 ? avgWin / avgLoss : 0

    // Drawdown calculation
    var float maxEquity = strategy.initial_capital
    var float maxDrawdown = 0.0
    currentEquity = strategy.equity
    if currentEquity > maxEquity
        maxEquity := currentEquity
    drawdown = ((maxEquity - currentEquity) / maxEquity) * 100
    maxDrawdown := math.max(maxDrawdown, drawdown)

    // Populate table
    table.cell(metricsTable, 0, 0, "METRIC", bgcolor=color.gray, text_color=color.white)
    table.cell(metricsTable, 1, 0, "VALUE", bgcolor=color.gray, text_color=color.white)

    table.cell(metricsTable, 0, 1, "Total Trades", text_color=color.white)
    table.cell(metricsTable, 1, 1, str.tostring(totalTrades), text_color=color.yellow)

    table.cell(metricsTable, 0, 2, "Win Rate", text_color=color.white)
    table.cell(metricsTable, 1, 2, str.tostring(winRate, "#.##") + "%", text_color=winRate > 50 ? color.green : color.red)

    table.cell(metricsTable, 0, 3, "Profit Factor", text_color=color.white)
    table.cell(metricsTable, 1, 3, str.tostring(profitFactor, "#.##"), text_color=profitFactor > 1 ? color.green : color.red)

    table.cell(metricsTable, 0, 4, "Max Drawdown", text_color=color.white)
    table.cell(metricsTable, 1, 4, str.tostring(maxDrawdown, "#.##") + "%", text_color=maxDrawdown < 20 ? color.green : color.red)

    table.cell(metricsTable, 0, 5, "Net Profit", text_color=color.white)
    netProfit = strategy.netprofit
    table.cell(metricsTable, 1, 5, str.tostring(netProfit, "#,###.##"), text_color=netProfit > 0 ? color.green : color.red)
```

### 2. Trade Distribution Analysis
```pinescript
// Trade distribution tracking
var array<float> tradeReturns = array.new<float>()
var array<int> tradeDurations = array.new<int>()
var int tradeStartBar = 0

if strategy.position_size != strategy.position_size[1]
    if strategy.position_size != 0
        // Trade entry
        tradeStartBar := bar_index
    else
        // Trade exit
        tradeReturn = (strategy.equity - strategy.equity[bar_index - tradeStartBar]) / strategy.equity[bar_index - tradeStartBar] * 100
        array.push(tradeReturns, tradeReturn)
        array.push(tradeDurations, bar_index - tradeStartBar)

// Calculate distribution stats
if barstate.islastconfirmedhistory and array.size(tradeReturns) > 0
    avgReturn = array.avg(tradeReturns)
    stdReturn = array.stdev(tradeReturns)
    medianReturn = array.median(tradeReturns)
    maxReturn = array.max(tradeReturns)
    minReturn = array.min(tradeReturns)

    // Display distribution
    table.cell(metricsTable, 0, 6, "Avg Return", text_color=color.white)
    table.cell(metricsTable, 1, 6, str.tostring(avgReturn, "#.##") + "%", text_color=avgReturn > 0 ? color.green : color.red)

    table.cell(metricsTable, 0, 7, "Std Dev", text_color=color.white)
    table.cell(metricsTable, 1, 7, str.tostring(stdReturn, "#.##") + "%", text_color=color.yellow)
```

### 3. Sharpe Ratio Calculation
```pinescript
// Sharpe Ratio calculation
var array<float> returns = array.new<float>()
var float previousEquity = strategy.initial_capital

if bar_index > 0
    currentReturn = (strategy.equity - previousEquity) / previousEquity
    array.push(returns, currentReturn)
    if array.size(returns) > 252  // Keep 1 year of daily returns
        array.shift(returns)
    previousEquity := strategy.equity

if barstate.islastconfirmedhistory and array.size(returns) > 30
    avgReturn = array.avg(returns) * 252  // Annualized
    stdReturn = array.stdev(returns) * math.sqrt(252)  // Annualized
    riskFreeRate = 0.02  // 2% risk-free rate
    sharpeRatio = stdReturn > 0 ? (avgReturn - riskFreeRate) / stdReturn : 0

    table.cell(metricsTable, 0, 8, "Sharpe Ratio", text_color=color.white)
    table.cell(metricsTable, 1, 8, str.tostring(sharpeRatio, "#.##"), text_color=sharpeRatio > 1 ? color.green : sharpeRatio > 0 ? color.yellow : color.red)
```

### 4. Indicator Accuracy Testing
```pinescript
// For indicators: Track signal accuracy
var int truePositives = 0
var int falsePositives = 0
var int trueNegatives = 0
var int falseNegatives = 0

// Define what constitutes a successful signal (example: price moves 1% in signal direction)
targetMove = input.float(1.0, "Target Move %", group="Backtest Settings")
lookforward = input.int(10, "Bars to Confirm", group="Backtest Settings")

if barstate.isconfirmed and bar_index > lookforward
    // Check if past signal was correct
    if buySignal[lookforward]
        priceChange = (close - close[lookforward]) / close[lookforward] * 100
        if priceChange >= targetMove
            truePositives += 1
        else
            falsePositives += 1
    else if sellSignal[lookforward]
        priceChange = (close[lookforward] - close) / close[lookforward] * 100
        if priceChange >= targetMove
            trueNegatives += 1
        else
            falseNegatives += 1

// Display accuracy metrics
if barstate.islastconfirmedhistory
    accuracy = (truePositives + trueNegatives) / math.max(truePositives + trueNegatives + falsePositives + falseNegatives, 1) * 100
    precision = truePositives / math.max(truePositives + falsePositives, 1) * 100
    recall = truePositives / math.max(truePositives + falseNegatives, 1) * 100

    table.cell(metricsTable, 0, 9, "Signal Accuracy", text_color=color.white)
    table.cell(metricsTable, 1, 9, str.tostring(accuracy, "#.##") + "%", text_color=accuracy > 60 ? color.green : color.red)
```

### 5. Equity Curve Visualization
```pinescript
// Plot equity curve (for strategies)
plot(strategy.equity, "Equity Curve", color=color.blue, linewidth=2)

// Add drawdown visualization
equityMA = ta.sma(strategy.equity, 20)
plot(equityMA, "Equity MA", color=color.orange, linewidth=1)

// Underwater equity (drawdown visualization)
var float peakEquity = strategy.initial_capital
peakEquity := math.max(peakEquity, strategy.equity)
drawdownValue = (peakEquity - strategy.equity) / peakEquity * 100

// Plot drawdown as histogram
plot(drawdownValue, "Drawdown %", color=color.red, style=plot.style_histogram, histbase=0)
```

### 6. Multi-Timeframe Validation
```pinescript
// Test indicator on multiple timeframes
htf1_signal = request.security(syminfo.tickerid, "60", buySignal)
htf2_signal = request.security(syminfo.tickerid, "240", buySignal)
htf3_signal = request.security(syminfo.tickerid, "D", buySignal)

// Confluence scoring
confluenceScore = 0
confluenceScore += buySignal ? 1 : 0
confluenceScore += htf1_signal ? 1 : 0
confluenceScore += htf2_signal ? 1 : 0
confluenceScore += htf3_signal ? 1 : 0

// Track confluence performance
var array<float> confluenceReturns = array.new<float>()
if confluenceScore >= 3 and barstate.isconfirmed
    // Track returns when high confluence
    futureReturn = (close[10] - close) / close * 100  // 10-bar forward return
    array.push(confluenceReturns, futureReturn)
```

### 7. Walk-Forward Analysis
```pinescript
// Simple walk-forward testing
lookbackPeriod = input.int(100, "Training Period", group="Walk-Forward")
forwardPeriod = input.int(20, "Testing Period", group="Walk-Forward")

// Optimize parameters on lookback period
var float optimalParam = na
if bar_index % (lookbackPeriod + forwardPeriod) == 0
    // Re-optimize parameters based on past performance
    // This is simplified - real implementation would test multiple values
    optimalParam := ta.sma(close, lookbackPeriod) > close ? 20 : 50

// Use optimized parameters
maLength = int(optimalParam)
ma = ta.sma(close, maLength)
```

## Testing Checklist

- [ ] Net profit/loss calculation
- [ ] Win rate and trade count
- [ ] Maximum drawdown tracking
- [ ] Risk-adjusted returns (Sharpe/Sortino)
- [ ] Trade distribution analysis
- [ ] Equity curve visualization
- [ ] Signal accuracy for indicators
- [ ] Multi-timeframe validation
- [ ] Statistical significance tests
- [ ] Forward testing results

## Output Format

Always provide:
1. Performance metrics table
2. Equity curve visualization
3. Drawdown analysis
4. Trade distribution stats
5. Risk metrics
6. Recommendations for improvement

Backtesting in Pine Script has limitations. Past performance doesn't guarantee future results. Always include appropriate disclaimers.
