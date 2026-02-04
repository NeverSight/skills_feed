---
name: mql5-indicator-patterns
description: MQL5 indicator development patterns. TRIGGERS - MQL5 indicator, OnCalculate, indicator buffers, MetaTrader 5.
allowed-tools: Read, Grep, Edit, Write
---

# MQL5 Visual Indicator Patterns

Battle-tested patterns for creating custom MQL5 indicators with proper display, buffer management, and real-time updates.

## When to Use This Skill

Use this skill when:

- Creating custom MQL5 indicators for MetaTrader 5
- Debugging indicator display or buffer issues
- Setting up OnCalculate with proper warmup handling
- Implementing new bar detection patterns

## Quick Reference

### Essential Patterns

**Display Scale** (for small values < 1.0):

```mql5
IndicatorSetDouble(INDICATOR_MINIMUM, 0.0);
IndicatorSetDouble(INDICATOR_MAXIMUM, 0.1);
```

**Buffer Setup** (visible + hidden):

```mql5
SetIndexBuffer(0, BufVisible, INDICATOR_DATA);        // Visible
SetIndexBuffer(1, BufHidden, INDICATOR_CALCULATIONS); // Hidden
```

**New Bar Detection** (prevents drift):

```mql5
static int last_processed_bar = -1;
bool is_new_bar = (i > last_processed_bar);
```

**Warmup Calculation**:

```mql5
int StartCalcPosition = underlying_warmup + own_warmup;
PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartCalcPosition);
```

---

## Common Pitfalls

**Blank Display**: Set explicit scale (see Display Scale reference)

**Rolling Window Drift**: Use new bar detection with hidden buffer (see Recalculation reference)

**Misaligned Plots**: Calculate correct PLOT_DRAW_BEGIN (see Complete Template reference)

**Forward-Indexed Arrays**: Always set `ArraySetAsSeries(buffer, false)`

---

## Key Patterns

**For production MQL5 indicators**:

1. Explicit scale for small values (< 1.0 range)
2. Hidden buffers for recalculation tracking
3. New bar detection prevents rolling window drift
4. Static variables maintain state efficiently
5. Proper warmup calculation prevents misalignment
6. Forward indexing for code clarity

These patterns solve the most common indicator development issues encountered in real-world MT5 development.

---

## Troubleshooting

| Issue                     | Cause                          | Solution                                              |
| ------------------------- | ------------------------------ | ----------------------------------------------------- |
| Blank indicator window    | Scale not set for small values | Set INDICATOR_MINIMUM/MAXIMUM explicitly              |
| Values drifting over time | Rolling window not reset       | Use new bar detection with hidden buffer              |
| Misaligned plot start     | Wrong PLOT_DRAW_BEGIN          | Calculate: underlying_warmup + own_warmup             |
| Reversed array indexing   | Series mode enabled            | Call ArraySetAsSeries(buffer, false)                  |
| Buffer values incorrect   | Wrong INDICATOR_DATA type      | Use INDICATOR_CALCULATIONS for hidden buffers         |
| Compile error on buffer   | Buffer count mismatch          | Match #property indicator_buffers with SetIndexBuffer |
| Indicator not updating    | OnCalculate return wrong       | Return rates_total to signal successful calculation   |
| Performance issues        | Recalculating all bars         | Only recalculate from prev_calculated onwards         |

---

## Reference Documentation

For detailed information, see:

- [Display Scale](./references/display-scale.md) - Fix blank indicator windows for small values
- [Buffer Patterns](./references/buffer-patterns.md) - Visible and hidden buffer architecture
- [Recalculation](./references/recalculation.md) - Bar detection and rolling window state management
- [Complete Template](./references/complete-template.md) - Full working example with all patterns
- [Debugging](./references/debugging.md) - Checklist for troubleshooting display issues
