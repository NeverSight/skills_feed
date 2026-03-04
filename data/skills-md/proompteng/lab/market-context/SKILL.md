---
name: market-context
description: Build a normalized market-context JSON bundle for a single symbol and timestamp.
---

# market-context

Build a normalized market-context JSON bundle for a single symbol and timestamp.

## Scripted workflow

- Run lifecycle API client: `skills/market-context/scripts/market_context_run_api.py`
- Finalize payload validator: `skills/market-context/scripts/validate_market_context_payload.py`
- JSON Schemas:
  - `skills/market-context/schemas/market-context-run-start.schema.json`
  - `skills/market-context/schemas/market-context-run-progress.schema.json`
  - `skills/market-context/schemas/market-context-run-evidence.schema.json`

### Lifecycle endpoints

- `POST /api/torghut/market-context/runs/start`
- `POST /api/torghut/market-context/runs/progress`
- `POST /api/torghut/market-context/runs/evidence`
- `POST /api/torghut/market-context/runs/finalize`
- `GET /api/torghut/market-context/runs/{requestId}`

### Example sequence

```bash
python3 skills/market-context/scripts/market_context_run_api.py start \
  --callback-url "<callbackUrl>" \
  --request-id "<requestId>" \
  --symbol "<symbol>" \
  --domain "<fundamentals|news>" \
  --reason "<reason>"

python3 skills/market-context/scripts/market_context_run_api.py progress \
  --callback-url "<callbackUrl>" \
  --request-id "<requestId>" \
  --seq 1 \
  --status running \
  --message "collection_started"

python3 skills/market-context/scripts/validate_market_context_payload.py \
  --domain "<fundamentals|news>" \
  --file /tmp/market-context.json

python3 skills/market-context/scripts/market_context_run_api.py finalize \
  --callback-url "<callbackUrl>" \
  --request-id "<requestId>" \
  --payload-file /tmp/market-context.json \
  --expect-status 200
```

## Output contract

Return JSON with keys:

- `context_version`
- `as_of_utc`
- `symbol`
- `freshness_seconds`
- `source_count`
- `quality_score`
- `payload`
- `citations`

## Rules

- Use UTC ISO timestamps.
- Include stale or missing domains in `payload.risk_flags`.
- Keep quality scoring deterministic from source freshness.
