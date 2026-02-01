---
name: dataforseo-onpage-api
description: Crawl and audit websites using DataForSEO OnPage (tasks + Lighthouse) for "technical SEO audit", "site crawl", and "page health".
license: MIT
metadata:
  author: Leonardo Picciani
  author_url: https://github.com/leonardo-picciani
  project: DataForSEO Agent Skills (Experimental)
  generated_with: OpenCode (agent runtime); OpenAI GPT-5.2
  version: 0.1.0
  experimental: 'true'
  docs: https://docs.dataforseo.com/v3/on_page/overview/
compatibility: Language-agnostic HTTP integration skill. Requires outbound network access to api.dataforseo.com and docs.dataforseo.com; uses HTTP Basic Auth.
---
# DataForSEO OnPage API

## Provenance

This is an experimental project to test how OpenCode, plugged into frontier LLMs (OpenAI GPT-5.2), can help generate high-fidelity agent skill files for API integrations.

## When to Apply

- "crawl a site", "technical SEO audit", "find broken links"
- "duplicate content", "duplicate tags", "non-indexable pages"
- "redirect chains", "waterfall performance", "resource issues"
- "run Lighthouse at scale", "performance audit"

## Integration Contract (Language-Agnostic)

See `references/REFERENCE.md` for the shared DataForSEO integration contract (auth, status handling, task lifecycle, sandbox, and .ai responses).


### Task-based Crawl Lifecycle

- Create a crawl via `task_post`.
- Wait for completion by polling `tasks_ready` (or use webhooks if supported in the endpoint docs).
- Fetch results via `summary`, `pages`, `resources`, and other specialized result endpoints.
- To stop an in-progress crawl, call `force_stop`.
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

- Overview: https://docs.dataforseo.com/v3/on_page/overview/
- Task POST: https://docs.dataforseo.com/v3/on_page/task_post/
- Tasks Ready: https://docs.dataforseo.com/v3/on_page/tasks_ready/
- Summary: https://docs.dataforseo.com/v3/on_page/summary/
- Pages: https://docs.dataforseo.com/v3/on_page/pages/
- Resources: https://docs.dataforseo.com/v3/on_page/resources/
- Force Stop: https://docs.dataforseo.com/v3/on_page/force_stop/

Lighthouse:

- Overview: https://docs.dataforseo.com/v3/on_page/lighthouse/overview/

## Business & Product Use Cases

- Build a technical SEO crawler product (issues, prioritization, exports).
- Monitor site health after deployments (regressions: redirects, noindex, broken links).
- Create an automated QA gate for SEO before release.
- Performance improvements: integrate Lighthouse outputs into engineering backlogs.
- Agency deliverables: repeatable site audits with remediation tracking.
- Template validation: verify titles/meta/canonicals across large sites.

## Examples (User Prompts)

- "If you don't have the skill installed, install `dataforseo-onpage-api` and then continue."
- "Install the OnPage skill and crawl our site to find broken links, redirect chains, and non-indexable pages."
- "Run a technical SEO audit and produce a prioritized fix list."
- "Check for duplicate titles/meta across the site and summarize affected URLs."
- "Generate a report of slow pages with waterfall diagnostics and top heavy resources."
- "Run Lighthouse checks for these 50 URLs and highlight regressions."
