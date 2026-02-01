---
name: dataforseo-backlinks-api
description: Retrieve backlink profiles and bulk link metrics using DataForSEO Backlinks for "backlink audit", "referring domains", and "link monitoring".
license: MIT
metadata:
  author: Leonardo Picciani
  author_url: https://github.com/leonardo-picciani
  project: DataForSEO Agent Skills (Experimental)
  generated_with: OpenCode (agent runtime); OpenAI GPT-5.2
  version: 0.1.0
  experimental: 'true'
  docs: https://docs.dataforseo.com/v3/backlinks/overview/
compatibility: Language-agnostic HTTP integration skill. Requires outbound network access to api.dataforseo.com and docs.dataforseo.com; uses HTTP Basic Auth.
---
# DataForSEO Backlinks API

## Provenance

This is an experimental project to test how OpenCode, plugged into frontier LLMs (OpenAI GPT-5.2), can help generate high-fidelity agent skill files for API integrations.

## When to Apply

- "get backlinks for domain/url", "referring domains", "anchors report"
- "monitor new and lost backlinks", "link velocity", "timeseries backlinks"
- "bulk backlink checks", "bulk ranks", "spam score checks"
- "competitor backlink research", "link gap analysis"

## Integration Contract (Language-Agnostic)

See `references/REFERENCE.md` for the shared DataForSEO integration contract (auth, status handling, task lifecycle, sandbox, and .ai responses).


### Live-first Endpoints

- Backlinks endpoints are typically Live-first and support pagination-like controls (e.g., result limits) and filtering/sorting.
- The Index endpoint provides up-to-the-moment information about the backlinks database.
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

- Overview: https://docs.dataforseo.com/v3/backlinks/overview/
- Index: https://docs.dataforseo.com/v3/backlinks/index/

Core endpoints:

- Summary (Live): https://docs.dataforseo.com/v3/backlinks/summary/live/
- Backlinks (Live): https://docs.dataforseo.com/v3/backlinks/backlinks/live/
- Referring Domains (Live): https://docs.dataforseo.com/v3/backlinks/referring_domains/live/

## Business & Product Use Cases

- Link monitoring: alerts for new/lost backlinks and anchor shifts.
- Link building: find competitor links and prioritize outreach targets.
- Risk management: detect suspicious patterns and possible negative SEO.
- Agency reporting: monthly link growth and top referring domains.
- M&A diligence: evaluate a domain's authority/link profile before acquisition.
- Publisher partnerships: identify strong referring networks for co-marketing.

## Examples (User Prompts)

- "If you don't have the skill installed, install `dataforseo-backlinks-api` and then continue."
- "Install the Backlinks skill and audit our backlink profile: top ref domains, anchors, and spam risks."
- "Track new and lost backlinks weekly and alert me to big drops."
- "Find competitor backlinks we don't have and suggest outreach targets."
- "Run a bulk check of these 200 domains: ranks + referring domains count."
- "Analyze anchor distribution and flag over-optimized patterns."
