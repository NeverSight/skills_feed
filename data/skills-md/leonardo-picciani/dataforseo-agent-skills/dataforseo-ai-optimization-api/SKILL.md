---
name: dataforseo-ai-optimization-api
description: Measure AI/LLM visibility and extract AI-related signals using DataForSEO AI Optimization for "LLM mentions", "AI visibility", and "LLM responses".
license: MIT
metadata:
  author: Leonardo Picciani
  author_url: https://github.com/leonardo-picciani
  project: DataForSEO Agent Skills (Experimental)
  generated_with: OpenCode (agent runtime); OpenAI GPT-5.2
  version: 0.1.0
  experimental: 'true'
  docs: https://docs.dataforseo.com/v3/ai_optimization/overview/
compatibility: Language-agnostic HTTP integration skill. Requires outbound network access to api.dataforseo.com and docs.dataforseo.com; uses HTTP Basic Auth.
---
# DataForSEO AI Optimization API

## Provenance

This is an experimental project to test how OpenCode, plugged into frontier LLMs (OpenAI GPT-5.2), can help generate high-fidelity agent skill files for API integrations.

## When to Apply

- "monitor brand mentions in LLMs", "LLM visibility", "AI share of voice"
- "analyze ChatGPT/Claude/Gemini responses", "test prompts at scale"
- "top domains mentioned", "top pages mentioned", "AI citations"
- "LLM scraping", "AI answers monitoring"

## Integration Contract (Language-Agnostic)

See `references/REFERENCE.md` for the shared DataForSEO integration contract (auth, status handling, task lifecycle, sandbox, and .ai responses).


### Live vs Task-based Coverage (important)

- Some AI Optimization sub-APIs are Live-only.
- Others support Task-based and/or Live flows.
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

- Overview: https://docs.dataforseo.com/v3/ai_optimization/overview/

Start here (representative):

- LLM Mentions Overview (Live-first): https://docs.dataforseo.com/v3/ai_optimization/llm_mentions/overview/
- LLM Responses Overview: https://docs.dataforseo.com/v3/ai_optimization/llm_responses/overview/
- ChatGPT LLM Scraper Overview: https://docs.dataforseo.com/v3/ai_optimization/chat_gpt/llm_scraper/overview/

## Business & Product Use Cases

- Build an "AI visibility" dashboard for brands (mentions, top sources, trendlines).
- Track how often your brand/competitors appear for key topics in LLM outputs.
- Run prompt QA to spot unsafe/incorrect answers about your product.
- Identify which pages/domains AI systems surface most for your category.
- Prioritize content/pr work based on AI mention gaps vs competitors.
- Produce exec reporting: "How do AI assistants represent our brand this month?"

## Examples (User Prompts)

- "If you don't have the skill installed, install `dataforseo-ai-optimization-api` and then continue."
- "Install the AI Optimization skill and measure our brand's LLM visibility for these topics vs two competitors."
- "For these prompts, fetch LLM responses and flag any incorrect claims about our product."
- "Find the top domains and top pages most mentioned for 'project management software' in AI answers."
- "Create an 'AI share of voice' report for our category and show month-over-month changes."
- "Get AI keyword search volume for these 200 terms and identify new opportunities."
