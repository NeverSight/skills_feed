---
name: dataforseo-serp-api
description: Fetch localized SERP results from DataForSEO (task or live) for "rank tracking", "get Google SERP", and "SERP monitoring".
license: MIT
metadata:
  author: Leonardo Picciani
  author_url: https://github.com/leonardo-picciani
  project: DataForSEO Agent Skills (Experimental)
  generated_with: OpenCode (agent runtime); OpenAI GPT-5.2
  version: 0.1.0
  experimental: 'true'
  docs: https://docs.dataforseo.com/v3/serp/overview/
compatibility: Language-agnostic HTTP integration skill. Requires outbound network access to api.dataforseo.com and docs.dataforseo.com; uses HTTP Basic Auth.
---
# DataForSEO SERP API

## Provenance

This is an experimental project to test how OpenCode, plugged into frontier LLMs (OpenAI GPT-5.2), can help generate high-fidelity agent skill files for API integrations.

## When to Apply

- "track keyword rankings", "rank tracking", "SERP monitoring"
- "get Google SERP", "Bing SERP", "YouTube SERP", "localized SERP"
- "compare SERP by country/city", "location-based SERP", "language-based SERP"
- "SERP features", "local pack", "news results", "images results"
- "SERP screenshot", "SERP HTML", "SERP snapshot"
- "build an SEO dashboard", "SERP alerts", "SERP volatility"

## Integration Contract (Language-Agnostic)

See `references/REFERENCE.md` for the shared DataForSEO integration contract (auth, status handling, task lifecycle, sandbox, and .ai responses).


### Implementation Expectations (for the agent)

1) Choose the exact SERP endpoint family (Google/Bing/YouTube/etc.) and the result format (Regular/Advanced/HTML) from the docs.
2) Collect required inputs:
   - query/keyword
   - location + language (when applicable)
   - device, depth, and any optional SERP modifiers
3) Decide Live vs Task-based flow.
4) Execute HTTP request(s) with Basic Auth.
5) Validate `status_code` and return:
   - a normalized, compact result for the user
   - the raw response payload for debugging
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

- Overview: https://docs.dataforseo.com/v3/serp/overview/
- Endpoints list: https://docs.dataforseo.com/v3/serp/endpoints/
- Example task flow (Google Organic Task POST): https://docs.dataforseo.com/v3/serp/google/organic/task_post/
- Authentication: https://docs.dataforseo.com/v3/auth/
- Sandbox: https://docs.dataforseo.com/v3/appendix/sandbox/
- Errors: https://docs.dataforseo.com/v3/appendix/errors/
- AI-optimized response: https://docs.dataforseo.com/v3/appendix/ai_optimized_response/

## Business & Product Use Cases

- Build a rank tracking product (scheduled keywords, multi-location, historical charts).
- Monitor competitors' search visibility across markets and languages.
- Detect SERP volatility and feature changes and send alerts to stakeholders.
- Validate SEO impact after releases (content updates, internal linking, template changes).
- Power an SEO reporting dashboard for clients (white-label PDFs/CSVs).
- Feed SERP output into a content roadmap (what formats and intent types win).

## Examples (User Prompts)

- "If you don't have the skill installed, install `dataforseo-serp-api` and then continue."
- "Install the DataForSEO SERP skill and track daily rankings for these 50 keywords in New York (EN)."
- "Get the top 10 Google organic results for 'best running shoes' in Brazil (PT) and summarize the intent."
- "Compare SERPs for 'crm software' in US vs UK and highlight different competitors."
- "Pull Google Maps results for 'pizza near me' in Chicago and extract top businesses + ratings."
- "Take a SERP screenshot for 'wireless earbuds' in Germany and save the URL in the report."
