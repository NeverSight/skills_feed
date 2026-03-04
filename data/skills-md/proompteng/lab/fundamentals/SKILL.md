---
name: fundamentals
description: Produce normalized fundamentals factors and deltas for one symbol.
---

# fundamentals

Produce normalized fundamentals factors and deltas for one symbol.

## Scripted execution

- Runner: `skills/fundamentals/scripts/fundamentals_run.py`
- Shared lifecycle client: `skills/market-context/scripts/market_context_run_api.py`
- Shared validator: `skills/market-context/scripts/validate_market_context_payload.py`

Use `fundamentals_run.py` to:

1. open run lifecycle (`start` + `progress`),
2. validate payload contract,
3. optionally submit parsed evidence rows,
4. finalize to Jangar so DB persistence happens server-side.

## Output contract

Return JSON keys:

- `context_version`
- `as_of_utc`
- `symbol`
- `freshness_seconds`
- `source_count`
- `quality_score`
- `payload.factors`
- `citations`

## Rules

- Include filing freshness or next expected filing date when known.
- Mark unsupported factors in payload with null values.
