---
name: searxng-api
description: Use when you need to call SearXNG's Search API to run web searches, filter results (engine/category/language/time), paginate, and consume JSON output.
---

# SearXNG API

## What the API can do
- Run meta-search queries and return aggregated results in JSON.
- Filter by engines, categories, language, and time range.
- Paginate results.
- Return suggestions, answers, and infoboxes (when available).

## How to use it
1) Build the endpoint from `SEARXNG_BASE_URL`; if it is unset, use `http://localhost:8080`.
2) Call `/search` (or `/`) with `q=...&format=json`.
3) Parse the JSON response (`results`, `answers`, `suggestions`, etc.).

## Minimal request
- **GET**: `{BASE_URL}/search?q={QUERY}&format=json`
- **POST**: `{BASE_URL}/search` with form data `q=...&format=json`

## References
- `references/searxng-search-api.md` - parameters and response fields
