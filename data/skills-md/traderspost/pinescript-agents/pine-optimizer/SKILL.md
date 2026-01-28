---
name: pine-optimizer
description: Optimizes Pine Script for performance, user experience, and visual appeal on TradingView. Use when improving script speed, reducing load time, enhancing UI, organizing inputs, improving colors and visuals, or making scripts more user-friendly. Triggers on "optimize", "improve", "faster", "better UX", "clean up", or enhancement requests.
---

# Pine Script Optimizer

Specialized in enhancing script performance, user experience, and visual presentation on TradingView.

## Core Optimization Areas

### Performance Optimization
- Reduce calculation complexity
- Minimize security() calls
- Optimize array operations
- Cache repeated calculations
- Reduce compilation size

### User Experience Enhancement
- Intuitive input organization
- Helpful tooltips and descriptions
- Smart default values
- Conditional input visibility
- User-friendly alerts

### Visual Optimization
- Professional color schemes
- Adaptive text sizes
- Clean plot styles
- Responsive layouts
- Mobile-friendly displays

### Code Efficiency
- Remove redundant calculations
- Optimize conditional logic
- Reduce memory usage
- Streamline data structures

## Performance Optimization Techniques

### 1. Calculation Caching

```pinescript
// BEFORE - Inefficient
plot(ta.sma(close, 20) > ta.sma(close, 50) ? high : low)
plot(ta.sma(close, 20) > ta.sma(close, 50) ? 1 : 0)

// AFTER - Optimized with caching
sma20 = ta.sma(close, 20)
sma50 = ta.sma(close, 50)
condition = sma20 > sma50
plot(condition ? high : low)
plot(condition ? 1 : 0)
```

### 2. Security Call Optimization

```pinescript
// BEFORE - Multiple security calls
htfClose = request.security(syminfo.tickerid, "D", close)
htfHigh = request.security(syminfo.tickerid, "D", high)
htfLow = request.security(syminfo.tickerid, "D", low)

// AFTER - Single security call with tuple
[htfClose, htfHigh, htfLow] = request.security(syminfo.tickerid, "D", [close, high, low])
```

### 3. Array Operation Optimization

```pinescript
// BEFORE - Inefficient array operations
var array<float> values = array.new<float>()
for i = 0 to 100
    array.push(values, close[i])

// AFTER - Optimized with built-in functions
var array<float> values = array.new<float>(100)
if barstate.isconfirmed
    array.push(values, close)
    if array.size(values) > 100
        array.shift(values)
```

### 4. Conditional Logic Optimization

```pinescript
// BEFORE - Multiple condition checks
signal = close > open and close > close[1] and volume > volume[1] and rsi > 50

// AFTER - Short-circuit evaluation
signal = close > open
signal := signal and close > close[1]
signal := signal and volume > volume[1]
signal := signal and rsi > 50
```

## User Experience Enhancements

### 1. Organized Input Groups

```pinescript
// Organized inputs with groups and tooltips
// ============================================================================
// INPUTS
// ============================================================================

// Moving Average Settings
maLength = input.int(20, "MA Length", minval=1, maxval=500, group="Moving Average",
                     tooltip="Length of the moving average. Lower values are more responsive.")
maType = input.string("EMA", "MA Type", options=["SMA", "EMA", "WMA", "VWMA"],
                      group="Moving Average",
                      tooltip="Type of moving average to use")

// Signal Settings
signalMode = input.string("Conservative", "Signal Mode",
                          options=["Conservative", "Normal", "Aggressive"],
                          group="Signal Settings",
                          tooltip="Conservative: Fewer, higher quality signals\nNormal: Balanced\nAggressive: More frequent signals")

// Visual Settings
showMA = input.bool(true, "Show MA", group="Visual Settings")
showSignals = input.bool(true, "Show Signals", group="Visual Settings")
showTable = input.bool(true, "Show Info Table", group="Visual Settings")

// Color Settings
bullishColor = input.color(color.green, "Bullish Color", group="Colors")
bearishColor = input.color(color.red, "Bearish Color", group="Colors")
neutralColor = input.color(color.gray, "Neutral Color", group="Colors")
```

### 2. Adaptive Color Schemes

```pinescript
// Professional color scheme with transparency
var color BULL_COLOR = color.new(#26a69a, 0)
var color BEAR_COLOR = color.new(#ef5350, 0)
var color BULL_LIGHT = color.new(#26a69a, 80)
var color BEAR_LIGHT = color.new(#ef5350, 80)

// Gradient colors for trends
trendStrength = (close - ta.sma(close, 50)) / ta.sma(close, 50) * 100
gradientColor = color.from_gradient(trendStrength, -2, 2, BEAR_COLOR, BULL_COLOR)

// Dark mode friendly colors
bgColor = color.new(color.black, 95)
textColor = color.new(color.white, 0)
```

### 3. Responsive Table Layout

```pinescript
// Auto-sizing table based on content
var table infoTable = table.new(position.top_right, 2, 1, bgcolor=color.new(color.black, 85))

// Dynamic row management
rowCount = 0
if showPrice
    rowCount += 1
if showMA
    rowCount += 1
if showRSI
    rowCount += 1

// Resize table if needed
if rowCount != table.rows(infoTable)
    table.delete(infoTable)
    infoTable := table.new(position.top_right, 2, rowCount, bgcolor=color.new(color.black, 85))
```

### 4. Smart Alert Messages

```pinescript
// Detailed alert messages with context
alertMessage = "🔔 " + syminfo.ticker + " Alert\n" + "Price: $" + str.tostring(close, "#,###.##") + "\n" + "Signal: " + (buySignal ? "BUY" : sellSignal ? "SELL" : "NEUTRAL") + "\n" + "Strength: " + str.tostring(signalStrength, "#.#") + "/10\n" + "Volume: " + (volume > ta.sma(volume, 20) ? "Above" : "Below") + " average\n" + "Time: " + str.format_time(time, "yyyy-MM-dd HH:mm")

alertcondition(buySignal or sellSignal, "Trade Signal", alertMessage)
```

## Visual Optimization

### 1. Professional Plot Styling

```pinescript
// Clean, professional plotting
ma = ta.ema(close, maLength)

// Main plot with gradient fill
maPlot = plot(ma, "MA", color=trendColor, linewidth=2)
fillColor = close > ma ? BULL_LIGHT : BEAR_LIGHT
fill(plot(close, display=display.none), maPlot, fillColor, "MA Fill")

// Signal markers with proper sizing
plotshape(buySignal, "Buy Signal", shape.triangleup, location.belowbar, BULL_COLOR, size=size.small)
plotshape(sellSignal, "Sell Signal", shape.triangledown, location.abovebar, BEAR_COLOR, size=size.small)
```

### 2. Adaptive Text Sizing

```pinescript
// Dynamic label sizing based on timeframe
labelSize = timeframe.period == "1" ? size.tiny : timeframe.period == "5" ? size.small : timeframe.period == "15" ? size.small : timeframe.period == "60" ? size.normal : timeframe.period == "D" ? size.large : size.normal

if showLabels and buySignal
    label.new(bar_index, low, "BUY", style=label.style_label_up, color=BULL_COLOR, textcolor=color.white, size=labelSize)
```

### 3. Mobile-Friendly Display

```pinescript
// Compact display for mobile devices
compactMode = input.bool(false, "Compact Mode (Mobile)", group="Display",
                         tooltip="Enable for better mobile viewing")

// Adjust plot widths
plotWidth = compactMode ? 1 : 2

// Conditional table display
if not compactMode
    // Show full table
    table.cell(infoTable, 0, 0, "Full Info", text_color=color.white)
else
    // Show essential info only
    table.cell(infoTable, 0, 0, "Signal: " + (buySignal ? "↑" : sellSignal ? "↓" : "−"))
```

## Code Quality Improvements

### 1. Memory Optimization

```pinescript
// Use var for persistent values
var float prevHigh = na
var int barsSinceSignal = 0
var array<float> prices = array.new<float>(100)

// Clear unused arrays
if array.size(prices) > 100
    array.clear(prices)
```

### 2. Error Prevention

```pinescript
// Robust error handling
safeDiv(num, den) => den != 0 ? num / den : 0
safeLookback(src, bars) => bars < bar_index ? src[bars] : src[bar_index]

// NA handling
getValue(src) => na(src) ? 0 : src
```

### 3. Compilation Size Reduction

```pinescript
// Use functions to reduce code duplication
plotSignal(cond, loc, col, txt) =>
    if cond
        label.new(bar_index, loc, txt, color=col, textcolor=color.white)

// Reuse styling variables
var commonStyle = label.style_label_center
var commonSize = size.normal
```

## Optimization Checklist

- [ ] Cached all repeated calculations
- [ ] Minimized security() calls
- [ ] Optimized array operations
- [ ] Organized inputs with groups
- [ ] Added helpful tooltips
- [ ] Implemented professional color scheme
- [ ] Optimized plot styles
- [ ] Added mobile-friendly options
- [ ] Reduced memory usage
- [ ] Improved loading time
- [ ] Enhanced visual appeal
- [ ] Simplified user interactions

Balance optimization with readability. Don't over-optimize at the expense of maintainability.
