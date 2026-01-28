---
name: navi-stream
description: Navi Stream language expert for writing quantitative trading indicators and technical analysis scripts. Use when working with .nvs files, technical indicators, market data analysis, or financial computations. Navi Stream is a domain-specific language optimized for real-time streaming data processing and indicator calculations.
---

# Navi Stream Language Skill

Navi Stream (.nvs) is a domain-specific language (DSL) designed specifically for quantitative trading and technical analysis. It is optimized for real-time streaming data processing and technical indicator calculations.

## Core Features

- **Real-time Stream Processing** - Designed for processing market data tick by tick
- **Technical Indicator Library** - Rich built-in technical analysis functions (ta module)
- **Market Data Access** - Direct access to OHLC data (quote module)
- **Visualization Support** - Built-in plotting functions for indicator display
- **Parameterized Configuration** - Support for dynamic parameters and metadata declarations
- **Internationalization** - Native support for multi-language labels
- **Navi Integration** - Can be imported and called by Navi programs

## Quick Reference

### Basic Structure

```nvs
// 1. Metadata declaration
meta {
    title = "MACD",
    overlay = false,
}

// 2. Module imports
use quote, ta;

// 3. Parameter definition
param {
    Length1 = 12,
    Length2 = 26,
    Length3 = 9,
}

// 4. Indicator calculation
let fast_ma = ema(close, Length1);
let slow_ma = ema(close, Length2);

// 5. Export variables
export let hist = fast_ma - slow_ma;
export let signal = ema(hist, Length3);
export let macd = (hist - signal) * 2;
```

### Key Syntax Rules

- File extension: `.nvs`
- Use 4 spaces for indentation
- Single-line comments: `//`
- String interpolation: `` `value: ${x}` ``
- Variable declaration: `let` (immutable), `var` (mutable)

## Metadata System

### Meta Block

```nvs
meta {
    title = "Indicator Name",
    overlay = false,        // false: separate window, true: overlay on price chart
    hideparams = true,      // Hide parameter panel
}
```

### Parameter Declaration

```nvs
param {
    // Simple parameter
    Period = 14,

    // Parameter with metadata
    @meta(title = "MA Period", range = 1..250)
    MA_Period = 20,

    // Multiple parameters
    Short = 12,
    Long = 26,
    Signal = 9,
}

// Use parameters in code
let ma = ema(close, Period);
```

### Internationalization Labels

```nvs
@title_period {
    "en" = "Period",
    "zh-CN" = "周期",
    "zh-HK" = "週期",
}

// Use label
param {
    @meta(title = @title_period)
    period = 14,
}
```

## Market Data Access (quote module)

### Built-in Data Fields

```nvs
use quote;

// Access current period data
let current_price = close;
let high_price = high;
let low_price = low;
let open_price = open;
let vol = volume;
let amt = turnover;

// Access historical data (time series)
let prev_close = close[1];      // Previous period
let prev_high = high[2];        // 2 periods ago
```

**Available data fields:**
- `close` - Close price
- `open` - Open price
- `high` - High price
- `low` - Low price
- `volume` - Volume
- `turnover` - Turnover
- `time` - Timestamp

### Time Series Pattern

```nvs
// Access past data
if (close > close[1]) {
    // Current close is higher than previous period
}

// Multi-period comparison
if (close > high[5]) {
    // Current price breaks above high from 5 periods ago
}
```

## Technical Indicator Functions (ta module)

### Moving Averages

```nvs
use ta;

// Simple moving average
let sma20 = ma(close, 20);

// Exponential moving average
let ema12 = ema(close, 12);
let ema26 = ema(close, 26);

// Apply to different data sources
let high_ma = ema(high, 10);
let low_ma = ema(low, 10);
```

### Common Technical Indicators

```nvs
// MACD
let diff = ema(close, 12) - ema(close, 26);
let dea = ema(diff, 9);
let macd = (diff - dea) * 2;

// Bollinger Bands logic
let mid = ma(close, 20);
let upper = mid * 1.02;
let lower = mid * 0.98;
```

### Helper Functions

```nvs
// Min and max values
let min_val = min(a, b);
let max_val = max(a, b);

// Absolute value
let abs_val = abs(diff);

// Conditional count
let count_up = count(close > open, 10);  // Number of up days in last 10 periods

// Bars since condition met
let bars = barslast(close > ma);
```

## Plotting System

### Plot Function

```nvs
// Basic plotting
plot(value, title: "Title", color: #ff0000);

// Multiple series
plot(ma5, title: "MA5", color: #ddff53, key: "ma5");
plot(ma10, title: "MA10", color: #4781ff, key: "ma10");
plot(ma20, title: "MA20", color: #fc6ebc, key: "ma20");
```

### Shape Drawing

```nvs
// Draw candlestick shapes
stick(top, bottom, color, hollow: true);

// Example: Price range
if (close > open) {
    stick(high, low, #red, hollow: false);
}

// Fill area
fill(upper, lower, #blue);

// Polyline
polyline(value, #green);
```

### Text Annotation

```nvs
// Draw text at specified position
if (buy_signal) {
    drawtext(close * 0.95, "Buy", #red);
}

if (sell_signal) {
    drawtext(close * 1.05, "Sell", #green);
}
```

## Variables and Types

### Variable Declaration

```nvs
// Immutable variable
let price = close;
let ma = ema(close, 20);

// Mutable variable
var counter = 0;
var sum: number = 0.0;

// Export variable (becomes indicator output)
export let signal = cross_signal;
export let macd = macd_value;
```

### Basic Types

```nvs
// Number type (floating point)
let price: number = 100.5;
let volume: number = 1000000;

// Boolean
let is_up = close > open;
let crossed = cross_over(fast, slow);

// String
let message = "Hello";
let label = `Price: ${close}`;

// nil (null value)
let optional_value: number = nil;

// Color
let red = #ff0000;
let blue = #0000ff;
let green = #00ff00;
```

### Array Operations

```nvs
// Create array
var values = array.new::<number>();

// Array operations
if (barstate.is_confirmed) {
    values.unshift(close);  // Insert at beginning
}

let first = values.get(0);   // Get element
let length = values.len();   // Get length

// Iterate array
for (let i in 0..values.len()) {
    let val = values.get(i);
}
```

## Control Flow

### Conditional Statements

```nvs
// if-else
if (close > open) {
    stick(high, low, #red);
} else if (close < open) {
    stick(high, low, #green);
} else {
    stick(high, low, #gray);
}

// Conditional plotting
if (close > ma20) {
    plot(close, color: #red);
}
```

### Loops

```nvs
// Range loop
for (let i in 1..10) {
    sum += values.get(i);
}

// Calculate minimum
let min_val: number = values.get(0);
for (let i in 1..min(n, values.len())) {
    min_val = min(min_val, values.get(i));
}
```

### Function Definition

```nvs
// Custom function
fn calc_average(x: number, y: number): number {
    return (x + y) / 2;
}

// Function with state
fn dllv(x: number, n: number): number {
    var values = array.new::<number>();
    if (barstate.is_confirmed) {
        values.unshift(x);
    }

    let result: number = values.get(0);
    for (let i in 1..min(n, values.len())) {
        result = min(result, values.get(i));
    }
    return result;
}

// Use function
let low_val = dllv(close, 10);
```

## Common Patterns

### Trend Detection

```nvs
// Golden cross and death cross
let golden_cross = fast_ma > slow_ma && fast_ma[1] <= slow_ma[1];
let death_cross = fast_ma < slow_ma && fast_ma[1] >= slow_ma[1];

// Breakout
let breakout = close > high[20];  // Break above 20-period high
let breakdown = close < low[20];   // Break below 20-period low
```

### Divergence Detection

```nvs
// Bullish divergence: price makes new low but indicator doesn't
let price_low = dllv(close, n);
let indicator_low = dllv(diff, n);

let bullish_divergence =
    close < price_low[period] &&    // Price makes new low
    diff > indicator_low[period];    // But indicator doesn't
```

### Multi-Period Analysis

```nvs
// Short, mid, long-term trends
let short_trend = ema(close, 5);
let mid_trend = ema(close, 20);
let long_trend = ema(close, 60);

// Trend alignment
let all_up = short_trend > mid_trend && mid_trend > long_trend;
let all_down = short_trend < mid_trend && mid_trend < long_trend;
```

### Channel System

```nvs
// Price channel
let mid = ema(close, 20);
let upper = mid * 1.02;
let lower = mid * 0.98;

// Draw channel
plot(upper, color: #red);
plot(mid, color: #yellow);
plot(lower, color: #green);

// Breakout signal
if (close > upper) {
    drawtext(close, "Breakout", #red);
}
```

## Integration with Navi

### Calling NVS from Navi

```nv
// Navi code (call_macd.nv)
use nvs.macd;  // Import macd.nvs

struct Candlestick {
    time: int,
    open: float,
    high: float,
    low: float,
    close: float,
    volume: float,
    turnover: float,
}

fn main() throws {
    let indicator = macd.new();  // Create instance

    // Feed data tick by tick
    for (let candle in candlesticks) {
        indicator.execute(
            time: candle.time,
            open: candle.open,
            high: candle.high,
            low: candle.low,
            close: candle.close,
            volume: candle.volume,
            turnover: candle.turnover
        );

        // Access exported variables
        println(`hist=${indicator.hist:?}`);
        println(`signal=${indicator.signal:?}`);
        println(`macd=${indicator.macd:?}`);
    }
}
```

## Best Practices

### Naming Conventions

```nvs
// Parameters: CamelCase or snake_case
param {
    ShortPeriod = 12,
    long_period = 26,
}

// Variables: snake_case
let fast_ma = ema(close, ShortPeriod);
let slow_ma = ema(close, long_period);

// Export variables: lowercase
export let signal = buy_signal;
```

### Parameter Ranges

```nvs
// Set reasonable ranges for parameters
param {
    @meta(range = 1..100)
    Period = 14,  // Limited to 1-100

    @meta(range = 1..250)
    MA_Period = 20,
}
```

### Performance Considerations

```nvs
// Good: Avoid repeated calculations
let ma20 = ema(close, 20);
let signal1 = close > ma20;
let signal2 = ma20 > ma20[1];

// Bad: Repeated calculations
let signal1 = close > ema(close, 20);
let signal2 = ema(close, 20) > ema(close, 20)[1];
```

### Conditional Optimization

```nvs
// Good: Combine conditions
let uptrend = close > ma20 && ma20 > ma60;
if (uptrend) {
    plot(close, color: #red);
}

// Use intermediate variables for readability
let price_above_ma = close > ma20;
let ma_trending_up = ma20 > ma20[1];
let strong_signal = price_above_ma && ma_trending_up;
```

## CLI Commands

```bash
# Navi Stream runs through Navi
navi run script.nv        # Run Navi script that calls .nvs
navi build                # Build project (including nvs modules)
```

## When to Load References

Load reference files from references/ directory when you need detailed information:

- **syntax.md** - Complete syntax reference
- **indicators.md** - Technical indicator functions in detail
- **plotting.md** - Plotting system detailed guide
- **patterns.md** - Common indicator patterns and strategies

Use `Read` tool to load these files from `~/.claude/skills/navi-stream/references/`.

## Examples Directory

The examples/ directory contains runnable code samples:
- `macd.nvs` - MACD indicator example
- `ma_cross.nvs` - Moving average crossover example
- `bollinger.nvs` - Bollinger Bands example
- `rsi.nvs` - RSI indicator example

## Resources

- **Navi Official Website**: https://navi-lang.org
- **Standard Library**: https://navi-lang.org/stdlib/
- **File Extension**: `.nvs`

## Important Notes

- Navi Stream focuses on indicator calculation, not general-purpose programming
- All calculations are streaming - process one data point at a time
- Exported variables become indicator outputs, displayable on charts
- When called from Navi programs, each `execute()` call processes one new data point
