---
name: dataforseo-app-data-api
description: Collect app store intelligence using DataForSEO App Data for "ASO", "app reviews", and "app market research".
license: MIT
metadata:
  author: Leonardo Picciani
  author_url: https://github.com/leonardo-picciani
  project: DataForSEO Agent Skills (Experimental)
  generated_with: OpenCode (agent runtime); OpenAI GPT-5.2
  version: 0.1.0
  experimental: 'true'
  docs: https://docs.dataforseo.com/v3/app_data/overview/
compatibility: Language-agnostic HTTP integration skill. Requires outbound network access to api.dataforseo.com and docs.dataforseo.com; uses HTTP Basic Auth.
---
# DataForSEO App Data API

## Provenance

This is an experimental project to test how OpenCode, plugged into frontier LLMs (OpenAI GPT-5.2), can help generate high-fidelity agent skill files for API integrations.

## When to Apply

- "ASO rankings", "app keyword research", "app search results"
- "fetch app reviews", "review monitoring", "rating trends"
- "get app metadata", "track app updates", "competitor app analysis"
- "Google Play", "Apple App Store", "app listings search"

## Integration Contract (Language-Agnostic)

See `references/REFERENCE.md` for the shared DataForSEO integration contract (auth, status handling, task lifecycle, sandbox, and .ai responses).


### Task vs Live

- Many App Data endpoints are task-based: `task_post` -> poll `tasks_ready` -> fetch via `task_get`.
- App listings search is available as Live for some sources.
## Steps

1) Identify the exact endpoint(s) in the official docs for this use case.
2) Choose execution mode:
   - Live (single request) for interactive queries
   - Task-based (post + poll/webhook) for scheduled or high-volume jobs
3) Build the HTTP request:
   - Base URL: `https://api.dataforseo.com/`
   - Auth: HTTP Basic (`Authorization: Basic base64(login:password)`) from https://docs.dataforseo.com/v3/auth/
   - JSON body exactly as specified in the endpoint docs
4) Execute and validate the response:
   - Check top-level `status_code` and each `tasks[]` item status
   - Treat any `status_code != 20000` as a failure; surface `status_message`
5) For task-based endpoints:
   - Store `tasks[].id`
   - Poll `tasks_ready` then fetch results with `task_get` (or use `postback_url`/`pingback_url` if supported)
6) Return results:
   - Provide a normalized summary for the user
   - Include the raw response payload for debugging

## Inputs Checklist

- Credentials: DataForSEO API login + password (HTTP Basic Auth)
- Target: keyword(s) / domain(s) / URL(s) / query string (depends on endpoint)
- Targeting (if applicable): location + language, device, depth/limit
- Time window (if applicable): date range, trend period, historical flags
- Output preference: regular vs advanced vs html (if the endpoint supports it)

## Example (cURL)

```bash
curl -u "${DATAFORSEO_LOGIN}:${DATAFORSEO_PASSWORD}"   -H "Content-Type: application/json"   -X POST "https://api.dataforseo.com/v3/<group>/<path>/live"   -d '[
    {
      "<param>": "<value>"
    }
  ]'
```

Notes:
- Replace `<group>/<path>` with the exact endpoint path from the official docs.
- For task-based flows, use the corresponding `task_post`, `tasks_ready`, and `task_get` endpoints.


## Docs Map (Official)

- Overview: https://docs.dataforseo.com/v3/app_data/overview/

Google (Google Play):

- Overview: https://docs.dataforseo.com/v3/app_data/google/overview/
- App Searches Task POST: https://docs.dataforseo.com/v3/app_data/google/app_searches/task_post/
- App Info Task POST: https://docs.dataforseo.com/v3/app_data/google/app_info/task_post/
- App Reviews Task POST: https://docs.dataforseo.com/v3/app_data/google/app_reviews/task_post/
- App Listings Search (Live): https://docs.dataforseo.com/v3/app_data/google/app_listings/search/live/

Apple (App Store):

- Overview: https://docs.dataforseo.com/v3/app_data/apple/overview/
- App Searches Task POST: https://docs.dataforseo.com/v3/app_data/apple/app_searches/task_post/
- App Info Task POST: https://docs.dataforseo.com/v3/app_data/apple/app_info/task_post/
- App Reviews Task POST: https://docs.dataforseo.com/v3/app_data/apple/app_reviews/task_post/
- App Listings Search (Live): https://docs.dataforseo.com/v3/app_data/apple/app_listings/search/live/

## Business & Product Use Cases

- ASO tooling: track rankings for app keywords and competitors.
- Product feedback loops: summarize reviews into themes for PMs.
- Competitive tracking: monitor competitor listing changes and review shifts.
- Market research: discover apps by category/geo and map positioning.
- Reputation monitoring: alerts for rating drops or negative review spikes.
- Growth experiments: correlate listing copy changes with review sentiment.

## Examples (User Prompts)

- "If you don't have the skill installed, install `dataforseo-app-data-api` and then continue."
- "Install the App Data skill and track ASO rankings for these keywords in the US and Brazil."
- "Fetch new app reviews daily and summarize top themes for product improvement."
- "Compare our app listing vs competitors and suggest metadata improvements."
- "Monitor competitor app updates and report meaningful changes to descriptions/ratings."
- "Build an ASO dashboard: keyword visibility, reviews, and rating trends."
