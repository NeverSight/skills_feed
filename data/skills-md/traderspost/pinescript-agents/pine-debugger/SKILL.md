---
name: pine-debugger
description: Adds debugging capabilities and troubleshoots Pine Script issues in TradingView's opaque environment. Use when scripts have errors, unexpected behavior, need debugging tools added, or require troubleshooting. Triggers on "debug", "fix", "error", "not working", "wrong values", or troubleshooting requests.
---

# Pine Script Debugger

Specialized in adding debugging tools and troubleshooting Pine Script code in TradingView's often opaque environment.

## Core Responsibilities

### Debug Tool Implementation
- Insert label.new() for value inspection
- Create table-based variable monitors
- Add conditional plotting for testing
- Implement bar_index tracking
- Create calculation flow visualizers

### Issue Identification
- Detect repainting problems
- Find calculation errors
- Identify na value propagation
- Spot logic flow issues
- Diagnose performance bottlenecks

### TradingView Quirk Handling
- Deal with undocumented behaviors
- Work around platform limitations
- Handle execution model oddities
- Debug real-time vs historical differences

## Common Pine Script Syntax Errors

### CRITICAL: Line Continuation Issues

Pine Script does NOT support splitting expressions across multiple lines without proper syntax. This is a frequent source of errors.

**WRONG - Will cause "end of line without line continuation" error:**
```pinescript
// DON'T DO THIS - Ternary split across lines
dollarsText = priceDiff >= 0 ?
    str.format("+${0}", priceDiff) :
    str.format("-${0}", math.abs(priceDiff))
```

**CORRECT - Keep ternary on one line:**
```pinescript
// DO THIS - Entire ternary on one line
dollarsText = priceDiff >= 0 ? str.format("+${0}", priceDiff) : str.format("-${0}", math.abs(priceDiff))
```

## Debugging Toolkit

### 1. Label-Based Debugging
```pinescript
// Debug label showing multiple values
if barstate.islast
    debugText = "RSI: " + str.tostring(rsiValue, "#.##") + "\n" + "MA: " + str.tostring(maValue, "#.##") + "\n" + "Signal: " + (buySignal ? "BUY" : "NEUTRAL")
    label.new(bar_index, high * 1.05, debugText, style=label.style_label_down, color=color.yellow, textcolor=color.black)
```

### 2. Table-Based Monitor
```pinescript
// Real-time variable monitor table
var table debugTable = table.new(position.top_right, 2, 10, bgcolor=color.black, border_width=1)

if barstate.islast
    table.cell(debugTable, 0, 0, "Variable", bgcolor=color.gray, text_color=color.white)
    table.cell(debugTable, 1, 0, "Value", bgcolor=color.gray, text_color=color.white)

    table.cell(debugTable, 0, 1, "Bar Index", text_color=color.white)
    table.cell(debugTable, 1, 1, str.tostring(bar_index), text_color=color.yellow)

    table.cell(debugTable, 0, 2, "Close Price", text_color=color.white)
    table.cell(debugTable, 1, 2, str.tostring(close, "#.####"), text_color=color.yellow)

    table.cell(debugTable, 0, 3, "Signal Active", text_color=color.white)
    table.cell(debugTable, 1, 3, signalActive ? "YES" : "NO", text_color=signalActive ? color.green : color.red)
```

### 3. Historical Value Tracker
```pinescript
// Track historical values for debugging
var array<float> histValues = array.new<float>()
var array<int> histBarIndex = array.new<int>()

if condition
    array.push(histValues, valueToTrack)
    array.push(histBarIndex, bar_index)
    if array.size(histValues) > 50  // Keep last 50 values
        array.shift(histValues)
        array.shift(histBarIndex)

// Display historical values
if barstate.islast and array.size(histValues) > 0
    for i = 0 to math.min(array.size(histValues) - 1, 10)
        label.new(array.get(histBarIndex, i), array.get(histValues, i), str.tostring(array.get(histValues, i)), style=label.style_circle, size=size.tiny)
```

### 4. Repainting Detector
```pinescript
// Detect potential repainting
var bool repaintDetected = false
var float previousValue = na

if not barstate.isrealtime
    if not na(previousValue) and previousValue != value[1]
        repaintDetected := true
    previousValue := value

if barstate.islast and repaintDetected
    label.new(bar_index, high * 1.1, "⚠️ REPAINTING DETECTED", style=label.style_label_down, color=color.red, textcolor=color.white)
```

### 5. Calculation Flow Tracer
```pinescript
// Trace calculation flow
var string calcFlow = ""

calcFlow := "Step 1: Input = " + str.tostring(input) + "\n"
intermediate1 = input * 2
calcFlow := calcFlow + "Step 2: x2 = " + str.tostring(intermediate1) + "\n"
intermediate2 = intermediate1 + 10
calcFlow := calcFlow + "Step 3: +10 = " + str.tostring(intermediate2) + "\n"
result = intermediate2 / 3
calcFlow := calcFlow + "Step 4: /3 = " + str.tostring(result)

if barstate.islast
    label.new(bar_index - 10, high, calcFlow, style=label.style_label_left, size=size.small)
```

## Common Issues and Solutions

### 1. Na Value Propagation
```pinescript
// Debug na propagation
debugNa = "NA Debug:\n"
debugNa := debugNa + "Value1 is " + (na(value1) ? "NA" : "OK") + "\n"
debugNa := debugNa + "Value2 is " + (na(value2) ? "NA" : "OK") + "\n"
debugNa := debugNa + "Result is " + (na(result) ? "NA" : "OK")
```

### 2. Series vs Simple
```pinescript
// Debug series/simple type issues
// Will show compilation error if mixing types incorrectly
debugSeriesType = ta.sma(close, 10)  // series float
debugSimpleType = 10  // simple int
// debugWrong = debugSimpleType[1]  // Error: Cannot use [] on simple
```

### 3. Security Function Issues
```pinescript
// Debug security() calls
[htfValue, htfTime] = request.security(syminfo.tickerid, "D", [close, time])
if barstate.islast
    label.new(bar_index, high, "HTF Close: " + str.tostring(htfValue) + "\n" + "HTF Time: " + str.format_time(htfTime, "yyyy-MM-dd HH:mm"))
```

## Debugging Workflow

1. **Add Initial Debug Points**
   - Insert labels at key calculation points
   - Add table for monitoring variables
   - Plot intermediate values

2. **Trace Execution**
   - Follow calculation flow
   - Check condition evaluations
   - Monitor state changes

3. **Identify Issues**
   - Look for unexpected na values
   - Check for repainting
   - Verify logic conditions

4. **Test Edge Cases**
   - First bars behavior
   - Real-time vs historical
   - Different market conditions

5. **Clean Up**
   - Comment out debug code
   - Or wrap in debug mode flag

## Debug Mode Implementation

```pinescript
debugMode = input.bool(false, "Debug Mode", group="Debug")

// Conditional debugging
if debugMode
    // All debug code here
    label.new(...)
    table.cell(...)
```

TradingView's environment is opaque and changes frequently. Always test thoroughly and provide multiple debugging approaches.
