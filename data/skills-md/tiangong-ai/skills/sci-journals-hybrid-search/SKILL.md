---
name: sci-journals-hybrid-search
description: Supabase edge function sci_search for hybrid search over scientific journal chunks with optional journal/date filters, chunk expansion (extK), and metadata retrieval. Use when integrating or debugging sci_search requests, filters, or result shaping.
---

# SCI Journals Hybrid Search

## Required parameters
- `data`: JSON payload containing the `query` string (optional `topK`, `extK`, `filter`, `datefilter`, `getMeta`).
- `TIANGONG_AI_APIKEY`: send as `x-api-key: <TIANGONG_AI_APIKEY>`.

## Quick start
- Endpoint: `https://qyyqlnwqwgvzxnccnbgm.supabase.co/functions/v1/sci_search`
- Header: `x-region: us-east-1`
- Requires `x-api-key: <TIANGONG_AI_APIKEY>`.
- Body: JSON with `query` string (optional `topK`, `extK`, `filter`, `datefilter`, `getMeta`); `assets/example-request.json` shows the format.

- Example call:
  ```bash
  curl -sS --location --request POST "https://qyyqlnwqwgvzxnccnbgm.supabase.co/functions/v1/sci_search" \
    --header 'Content-Type: application/json' \
    --header 'x-region: us-east-1' \
    --header "x-api-key: $TIANGONG_AI_APIKEY" \
    --data @assets/example-request.json
  ```

## Request & output
- POST `{ "query": string, "topK"?: number, "extK"?: number, "filter"?: object, "datefilter"?: object, "getMeta"?: boolean }`.
- `extK` expands each topK hit by N adjacent chunks (before/after), then merges into combined chunks.
- `filter` can constrain journals (see `references/request-response.md`).
- `datefilter` can constrain by UNIX seconds (see `references/request-response.md`).
- Responses: 200 with `{ data }` or `[]`; 400 if `query` missing; 500 on backend errors.

## References
- `references/env.md`
- `references/request-response.md`
- `references/testing.md`

## Assets
- `assets/example-request.json`
