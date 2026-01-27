---
name: entry-signals
description: Entry signal patterns with historical success rates. Use when deciding whether to open a position.
---

# Entry Signals

> Last updated: 2026-01-17 16:36 UTC
> Active patterns: 30
> Total samples: 5095
> Confidence threshold: 60%

## Entry Signals

These entry signals have been learned from competition data:

| Signal | Success Rate | Samples | Confidence | Seen |
|--------|-------------|---------|------------|------|
| Multi-timeframe bullish alignment (... | 88% | 164 | 85% | 1x |
| Multi-timeframe bullish alignment (... | 85% | 157 | 75% | 1x |
| Multi-timeframe bullish alignment (... | 85% | 164 | 80% | 1x |
| Multi-timeframe bullish alignment (... | 85% | 164 | 85% | 1x |
| SMA crossover + bullish MACD + neut... | 82% | 184 | 80% | 1x |
| SMA crossover + bullish MACD + neut... | 82% | 184 | 85% | 1x |
| SMA crossover + bullish MACD + neut... | 82% | 184 | 85% | 1x |
| Scaling into existing winning posit... | 80% | 157 | 75% | 1x |
| Scaling into existing winning posit... | 78% | 164 | 80% | 1x |
| Multi-timeframe bullish alignment (... | 75% | 89 | 95% | 1x |
| Multi-timeframe bearish alignment f... | 65% | 103 | 95% | 1x |
| Relative strength divergence (one a... | 45% | 79 | 60% | 1x |
| SMA and MACD bearish signals for sh... | 35% | 50 | 60% | 1x |
| High funding rate alone as bullish ... | 35% | 248 | 75% | 1x |
| High funding rate alone as bullish ... | 35% | 248 | 80% | 1x |
| High funding rate alone as bullish ... | 35% | 247 | 85% | 1x |
| High funding rate alone as bullish ... | 35% | 247 | 85% | 1x |
| Multi-timeframe bearish alignment f... | 35% | 201 | 95% | 1x |
| Positive funding rate interpreted a... | 30% | 208 | 60% | 1x |
| Multi-timeframe bullish alignment (... | 30% | 160 | 95% | 1x |
| RSI overbought + MACD bearish as sh... | 30% | 355 | 95% | 1x |
| Multi-timeframe bullish alignment (... | 25% | 88 | 95% | 1x |
| Negative funding rate as long oppor... | 25% | 180 | 95% | 1x |
| Multi-timeframe bearish alignment f... | 25% | 173 | 95% | 1x |
| Relative strength divergence (one a... | 20% | 72 | 70% | 1x |
| Positive momentum on small timefram... | 20% | 76 | 95% | 1x |
| Contrarian 'bounce back' reasoning ... | 20% | 180 | 95% | 1x |
| Multi-timeframe bullish alignment (... | 18% | 294 | 74% | 2x |
| SMA and MACD bearish signals for sh... | 18% | 50 | 70% | 1x |
| Positive funding rate interpreted a... | 15% | 225 | 70% | 1x |

## Signal Details

### Multi-timeframe bullish alignment (15m, ...
**Success rate**: 88%
**Total samples**: 164
**Confidence**: 85%
**Times confirmed**: 1
**First seen**: 2026-01-14
**Description**: Multi-timeframe bullish alignment (15m, 1h, 4h) WITH explicit risk validation and trade validation checks - skill_aware_oss uses this consistently with strong results (+$1236.81)

### Multi-timeframe bullish alignment (15m, ...
**Success rate**: 85%
**Total samples**: 157
**Confidence**: 75%
**Times confirmed**: 1
**First seen**: 2026-01-14
**Description**: Multi-timeframe bullish alignment (15m, 1h, 4h) combined with explicit risk validation produces profits in trending markets. skill_aware_oss: 'All timeframes bullish, technical indicators show bullish bias, no performance issues'.

### Multi-timeframe bullish alignment (15m, ...
**Success rate**: 85%
**Total samples**: 164
**Confidence**: 80%
**Times confirmed**: 1
**First seen**: 2026-01-14
**Description**: Multi-timeframe bullish alignment (15m, 1h, 4h) WITH explicit risk validation produces profitable entries. skill_aware_oss: 'Multi-timeframe analysis shows strong bullish alignment and high momentum... validation passes'. Success requires both trend confirmation AND risk checks.

### Multi-timeframe bullish alignment (15m, ...
**Success rate**: 85%
**Total samples**: 164
**Confidence**: 85%
**Times confirmed**: 1
**First seen**: 2026-01-14
**Description**: Multi-timeframe bullish alignment (15m, 1h, 4h) WITH explicit risk validation and trade validation passed - produces strong returns in trending markets

### SMA crossover + bullish MACD + neutral B...
**Success rate**: 82%
**Total samples**: 184
**Confidence**: 80%
**Times confirmed**: 1
**First seen**: 2026-01-14
**Description**: SMA crossover + bullish MACD + neutral Bollinger as entry confirmation. agentic_gptoss: 'Technical indicators (SMA crossover, bullish MACD, neutral Bollinger) support a long entry'. Combined with risk calculator validation.

---

## Confidence Guide

| Confidence | Interpretation |
|------------|----------------|
| 90%+ | High confidence - strong historical support |
| 70-90% | Moderate confidence - use with other signals |
| 60-70% | Low confidence - consider as one input |
| <60% | Experimental - needs more data |

*This skill is automatically generated and updated by the Observer Agent.*
