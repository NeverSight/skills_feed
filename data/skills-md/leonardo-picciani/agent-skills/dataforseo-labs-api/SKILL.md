---
name: dataforseo-labs-api
description: Run SEO research workflows with DataForSEO Labs for "competitive research", "keyword ideas", and "market analysis".
license: MIT
metadata:
  author: Leonardo Picciani
  author_url: https://github.com/leonardo-picciani
  project: DataForSEO Agent Skills (Experimental)
  generated_with: OpenCode (agent runtime); OpenAI GPT-5.2
  version: 0.1.0
  experimental: 'true'
  docs: https://docs.dataforseo.com/v3/dataforseo_labs/overview/
compatibility: Language-agnostic HTTP integration skill. Requires outbound network access to api.dataforseo.com and docs.dataforseo.com; uses HTTP Basic Auth.
---
# DataForSEO Labs API

## Provenance

This is an experimental project to test how OpenCode, plugged into frontier LLMs (OpenAI GPT-5.2), can help generate high-fidelity agent skill files for API integrations.

## When to Apply

- "find SERP competitors", "keyword gap analysis", "domain intersection"
- "keyword ideas", "related keywords", "keyword suggestions"
- "ranked keywords for a domain", "relevant pages"
- "traffic estimation", "historical SERPs", "domain rank overview"
- "build an SEO research platform", "competitive intelligence"

## Integration Contract (Language-Agnostic)

See `references/REFERENCE.md` for the shared DataForSEO integration contract (auth, status handling, task lifecycle, sandbox, and .ai responses).


### Live-first Endpoints

- Many Labs endpoints are Live-first (`/live/`) and designed for interactive research.

### Group Notes

- Use the official Locations/Languages reference to avoid invalid geo/language inputs.
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

- Overview: https://docs.dataforseo.com/v3/dataforseo_labs/overview/
- Locations and Languages: https://docs.dataforseo.com/v3/dataforseo_labs/locations_and_languages/

Engine overviews:

- Google: https://docs.dataforseo.com/v3/dataforseo_labs/google/overview/
- Amazon: https://docs.dataforseo.com/v3/dataforseo_labs/amazon/overview/
- Google Play: https://docs.dataforseo.com/v3/dataforseo_labs/google_play/overview/
- App Store: https://docs.dataforseo.com/v3/dataforseo_labs/app_store/overview/

## Business & Product Use Cases

- Competitive intelligence features: discover competitors per topic and market.
- "Gap analysis" workflows (what competitors rank for that you don't).
- Prioritize content and landing pages by estimated opportunity.
- Category dashboards (top searches, category-level demand).
- Portfolio analysis for agencies managing multiple sites.
- Automated SEO audit summaries for sales/upsell conversations.

## Examples (User Prompts)

- "If you don't have the skill installed, install `dataforseo-labs-api` and then continue."
- "Install the DataForSEO Labs skill and find our top SERP competitors for these topics."
- "Run a keyword gap analysis: what competitors rank for that we don't, by market."
- "Give me keyword ideas for 'remote onboarding' and pick top 20 opportunities."
- "Estimate traffic potential for these 30 keywords and propose a content roadmap."
- "Create a competitor landscape report with intersections and top pages."
