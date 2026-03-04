---
name: news-sentiment
description: Extract structured, source-attributed sentiment context for one symbol.
---

# news-sentiment

Extract structured, source-attributed sentiment context for one symbol.

## Scripted execution

- Runner: `skills/news-sentiment/scripts/news_run.py`
- Shared lifecycle client: `skills/market-context/scripts/market_context_run_api.py`
- Shared validator: `skills/market-context/scripts/validate_market_context_payload.py`

Use `news_run.py` to:

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
- `payload.items` (headline, sentiment, source)
- `citations`

## Rules

- Prefer recency over volume.
- Mark missing sources explicitly.
