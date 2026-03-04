---
name: technicals-regime
description: Summarize trend, volatility, and liquidity regime from TA time series.
---

# technicals-regime

Summarize trend, volatility, and liquidity regime from TA time series.

## Output contract

Return JSON keys:

- `context_version`
- `as_of_utc`
- `symbol`
- `freshness_seconds`
- `source_count`
- `quality_score`
- `payload.regime`
- `citations`

## Rules

- Use bounded numeric ranges when possible.
- Emit explicit stale flags when data exceeds freshness SLO.
