---
name: pine-publisher
description: Prepares Pine Scripts for publication in TradingView's community library with proper documentation and compliance. Use when preparing to publish, adding documentation, ensuring House Rules compliance, writing descriptions, or finalizing scripts for release. Triggers on "publish", "release", "documentation", "House Rules", or preparation requests.
---

# Pine Script Publisher

Specialized in preparing scripts for publication in TradingView's community library.

## Core Responsibilities

### Publication Compliance
- Ensure House Rules compliance
- Add required documentation
- Include proper attributions
- Remove any prohibited content

### Documentation Creation
- Write comprehensive descriptions
- Create usage instructions
- Document all parameters
- Add example configurations

### Metadata Optimization
- Create SEO-friendly titles
- Add relevant tags/categories
- Write compelling descriptions
- Include version information

### Professional Presentation
- Clean code formatting
- Consistent naming conventions
- Professional comments
- Example screenshots ready

## TradingView House Rules Compliance

### Required Elements

```pinescript
//@version=6
//@description Comprehensive description of what the indicator/strategy does

// Title must be descriptive and professional
indicator(title="Professional Indicator Name - Clear Description v1.0",
         shorttitle="PRO IND",
         overlay=true)

// ============================================================================
// METADATA
// ============================================================================
// Author: Your Name / Username
// Version: 1.0
// Date: 2024-01-15
// Category: Trend Following / Momentum / Volatility / Volume
//
// Description:
// This indicator/strategy provides [clear explanation of functionality].
// It uses [main components/calculations] to generate [type of signals].
//
// Features:
// • Feature 1 description
// • Feature 2 description
// • Feature 3 description
//
// How to Use:
// 1. Add to your chart
// 2. Configure settings as needed
// 3. Look for [signal types]
// 4. Use in conjunction with [complementary analysis]
//
// ============================================================================
```

### Prohibited Content

- No financial advice
- No promises of profitability
- No external links (except documentation)
- No contact information in code
- No obfuscated/minified code
- No requests for donations/tips
- No malicious code

## Documentation Templates

### IMPORTANT: Script Description Location

**Pine Script descriptions should be written as comments at the top of the .pine file**, immediately after the version declaration and before the indicator/strategy declaration.

### 1. Indicator Documentation (Place at TOP of .pine file)

```pinescript
//@version=6

// ============================================================================
// DOCUMENTATION - THIS GOES AT THE TOP OF YOUR PINE SCRIPT FILE
// ============================================================================
//
// INDICATOR OVERVIEW
// ==================
// This indicator identifies [specific market conditions] by analyzing
// [data sources used]. It is designed for [target audience/use case].
//
// CALCULATION METHOD
// ==================
// The indicator calculates:
// 1. [First calculation] using [formula/method]
// 2. [Second calculation] based on [inputs]
// 3. [Final signal] when [conditions are met]
//
// SIGNALS INTERPRETATION
// ======================
// • Green Triangle: [What it means]
// • Red Triangle: [What it means]
// • Blue Line: [What it represents]
// • Shaded Area: [What it indicates]
//
// SETTINGS GUIDE
// ==============
// Length: Controls the lookback period. Lower = more responsive, Higher = smoother
// Threshold: Sets sensitivity. Range 0-100, default 50
// Mode: Choose between Conservative/Normal/Aggressive
//
// BEST PRACTICES
// ==============
// • Works best on [timeframes]
// • Most effective in [market conditions]
// • Combine with [other indicators] for confirmation
// • Avoid using during [specific conditions]
//
// LIMITATIONS
// ===========
// • May repaint in [specific scenarios]
// • Less effective in [market conditions]
// • Requires at least [X] bars of data
//
// VERSION HISTORY
// ===============
// v1.0 (2024-01-15): Initial release
// v1.1 (2024-02-01): Added multi-timeframe support
// v1.2 (2024-03-01): Performance optimizations
//
// ============================================================================

indicator("Your Indicator Name", shorttitle="Short Name", overlay=true)
```

### 2. Strategy Documentation

```pinescript
// ============================================================================
// STRATEGY DOCUMENTATION
// ============================================================================
//
// STRATEGY LOGIC
// ==============
// Entry Conditions:
// • Long: [Specific conditions for long entry]
// • Short: [Specific conditions for short entry]
//
// Exit Conditions:
// • Take Profit: [TP logic]
// • Stop Loss: [SL logic]
// • Trailing Stop: [If applicable]
//
// RISK MANAGEMENT
// ===============
// • Position Size: [How it's calculated]
// • Maximum Risk: [Risk per trade]
// • Maximum Drawdown: [Expected DD]
//
// BACKTESTING NOTES
// =================
// • Tested Period: [Date range]
// • Best Performance: [Market/Timeframe]
// • Win Rate: [Approximate %]
// • Profit Factor: [Approximate value]
//
// ⚠️ DISCLAIMER
// =============
// Past performance does not guarantee future results. This strategy is
// for educational purposes only. Always conduct your own analysis and
// risk management before trading.
//
// ============================================================================
```

### 3. Input Documentation

```pinescript
// ============================================================================
// INPUTS WITH DETAILED DESCRIPTIONS
// ============================================================================

// Calculation Settings
length = input.int(
    defval=20,
    title="Calculation Length",
    minval=1,
    maxval=200,
    group="Main Settings",
    tooltip="The number of bars used in the calculation. Lower values (5-20) " +
            "provide faster signals but more noise. Higher values (50-200) " +
            "provide smoother, more reliable signals but with greater lag."
)

sensitivity = input.float(
    defval=1.5,
    title="Sensitivity",
    minval=0.1,
    maxval=5.0,
    step=0.1,
    group="Main Settings",
    tooltip="Controls signal sensitivity. Lower values (0.5-1.0) generate " +
            "fewer, more conservative signals. Higher values (2.0-5.0) generate " +
            "more frequent signals. Default 1.5 is balanced."
)

// Display Settings
showSignals = input.bool(
    defval=true,
    title="Show Buy/Sell Signals",
    group="Display Options",
    tooltip="Toggle the display of entry/exit signals on the chart"
)

showInfoPanel = input.bool(
    defval=true,
    title="Show Information Panel",
    group="Display Options",
    tooltip="Display a panel with current indicator values and market statistics"
)

colorScheme = input.string(
    defval="Professional",
    title="Color Scheme",
    options=["Professional", "Classic", "Dark", "Colorful"],
    group="Display Options",
    tooltip="Choose color scheme:\n" +
            "• Professional: Blue/Red with transparency\n" +
            "• Classic: Green/Red traditional\n" +
            "• Dark: Optimized for dark mode\n" +
            "• Colorful: High contrast colors"
)
```

## SEO Optimization

### 1. Title Optimization

```pinescript
// Good titles for discoverability:
"RSI Divergence Scanner with Alerts - Multi Timeframe"
"Bollinger Bands Squeeze Detector Pro v2.0"
"Volume Profile with Support/Resistance Levels"
"Smart Money Concepts - Order Blocks & Fair Value Gaps"

// Include relevant keywords:
// - Indicator type (RSI, MACD, Moving Average)
// - Strategy type (Breakout, Trend Following, Mean Reversion)
// - Special features (Multi-TF, Alerts, Scanner)
// - Version number
```

### 2. Category Tags

```pinescript
// Relevant categories to include in description:
// Categories: Trend Analysis, Momentum, Volatility, Volume, Support/Resistance
// Tags: #RSI #Divergence #Alerts #MultiTimeframe #Scanner
// Markets: Forex, Crypto, Stocks, Futures, Indices
// Timeframes: Scalping (1m-5m), Intraday (15m-1h), Swing (4h-D), Position (W-M)
```

## Publishing Checklist

### Pre-Publication Review

- [ ] Code follows Pine Script v6 standards
- [ ] No syntax errors or warnings
- [ ] All functions work as intended
- [ ] No repainting issues (or clearly documented)
- [ ] Performance optimized (loads quickly)

### Documentation Complete

- [ ] Comprehensive description
- [ ] All inputs documented with tooltips
- [ ] Usage instructions clear
- [ ] Example configurations provided
- [ ] Limitations disclosed
- [ ] Version information included

### Visual Presentation

- [ ] Professional color scheme
- [ ] Clean chart appearance
- [ ] Readable text sizes
- [ ] Mobile-friendly display
- [ ] Screenshot examples ready

### Compliance Check

- [ ] No financial advice
- [ ] No performance guarantees
- [ ] No external promotions
- [ ] No contact information
- [ ] Disclaimer included
- [ ] Attribution for any borrowed code

### Metadata Optimized

- [ ] SEO-friendly title
- [ ] Compelling description
- [ ] Relevant categories selected
- [ ] Appropriate tags added
- [ ] Version number included

## Example Publication-Ready Script Header

```pinescript
//@version=6
//@description Advanced RSI divergence detector with multi-timeframe analysis and customizable alerts

indicator(title="RSI Divergence Pro - MTF Scanner with Alerts v2.0",
         shorttitle="RSI Div Pro",
         overlay=true,
         max_labels_count=500)

// ╔═══════════════════════════════════════════════════════════════════════╗
// ║                        RSI DIVERGENCE PRO v2.0                         ║
// ║                    Multi-Timeframe Scanner with Alerts                 ║
// ╠═══════════════════════════════════════════════════════════════════════╣
// ║ Author: TradingView_Username                                           ║
// ║ Version: 2.0                                                           ║
// ║ Release Date: January 15, 2024                                         ║
// ║ Category: Momentum Indicators                                          ║
// ║ License: Mozilla Public License 2.0                                    ║
// ╠═══════════════════════════════════════════════════════════════════════╣
// ║                            DESCRIPTION                                 ║
// ╠═══════════════════════════════════════════════════════════════════════╣
// ║ This indicator identifies bullish and bearish RSI divergences across   ║
// ║ multiple timeframes. It features:                                      ║
// ║                                                                         ║
// ║ • Regular and hidden divergence detection                              ║
// ║ • Multi-timeframe confluence analysis                                  ║
// ║ • Customizable alert system                                            ║
// ║ • Visual divergence lines and labels                                   ║
// ║ • Performance statistics table                                         ║
// ║                                                                         ║
// ║ Perfect for: Swing traders, reversal traders, multi-TF analysts        ║
// ╠═══════════════════════════════════════════════════════════════════════╣
// ║                          HOW TO USE                                    ║
// ╠═══════════════════════════════════════════════════════════════════════╣
// ║ 1. Add indicator to chart                                              ║
// ║ 2. Configure RSI settings (default: 14)                                ║
// ║ 3. Set divergence sensitivity (1-5)                                    ║
// ║ 4. Enable desired timeframes for scanning                              ║
// ║ 5. Look for divergence signals:                                        ║
// ║    - Green lines/labels: Bullish divergence                            ║
// ║    - Red lines/labels: Bearish divergence                              ║
// ║ 6. Use confluence table for multi-TF confirmation                      ║
// ╠═══════════════════════════════════════════════════════════════════════╣
// ║                          DISCLAIMER                                    ║
// ╠═══════════════════════════════════════════════════════════════════════╣
// ║ This indicator is for educational purposes only. Past performance     ║
// ║ does not guarantee future results. Always do your own analysis.       ║
// ╚═══════════════════════════════════════════════════════════════════════╝
```

A well-published script with proper documentation gets more views, likes, and usage in the TradingView community.
