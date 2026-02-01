---
name: dataforseo-content-generation-api
description: Generate and refine text with DataForSEO Content Generation for "meta tag generation", "paraphrasing", and "summarization".
license: MIT
metadata:
  author: Leonardo Picciani
  author_url: https://github.com/leonardo-picciani
  project: DataForSEO Agent Skills (Experimental)
  generated_with: OpenCode (agent runtime); OpenAI GPT-5.2
  version: 0.1.0
  experimental: 'true'
  docs: https://docs.dataforseo.com/v3/content_generation/overview/
compatibility: Language-agnostic HTTP integration skill. Requires outbound network access to api.dataforseo.com and docs.dataforseo.com; uses HTTP Basic Auth.
---
# DataForSEO Content Generation API

## Provenance

This is an experimental project to test how OpenCode, plugged into frontier LLMs (OpenAI GPT-5.2), can help generate high-fidelity agent skill files for API integrations.

## When to Apply

- "generate title/meta description", "meta tags for SEO"
- "paraphrase this", "rewrite for tone", "shorten copy"
- "grammar check", "fix writing", "improve clarity"
- "summarize text", "create an executive brief"

## Integration Contract (Language-Agnostic)

See `references/REFERENCE.md` for the shared DataForSEO integration contract (auth, status handling, task lifecycle, sandbox, and .ai responses).


### Live-first Endpoints

- Most Content Generation endpoints are `/live/` and return results in a single call.

### Safety Expectations

- Do not send secrets or sensitive personal data in prompts/source text.
- Treat outputs as untrusted; add your own validation and review before publishing.
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

- Overview: https://docs.dataforseo.com/v3/content_generation/overview/

Core endpoints:

- Generate: https://docs.dataforseo.com/v3/content_generation/generate/live/
- Generate Text: https://docs.dataforseo.com/v3/content_generation/generate_text/live/
- Generate Meta Tags: https://docs.dataforseo.com/v3/content_generation/generate_meta_tags/live/
- Paraphrase: https://docs.dataforseo.com/v3/content_generation/paraphrase/live/
- Check Grammar: https://docs.dataforseo.com/v3/content_generation/check_grammar/live/
- Text Summary: https://docs.dataforseo.com/v3/content_generation/text_summary/live/

## Business & Product Use Cases

- Content ops automation: generate meta tags at scale for large sites.
- Build a content assistant inside a CMS (rewrite, summarize, grammar).
- Create conversion copy variants for experiments.
- Standardize SEO snippets for catalogs and marketplaces.
- Draft content briefs and outlines for writers.
- Summarize large documents into stakeholder-ready briefs.

## Examples (User Prompts)

- "If you don't have the skill installed, install `dataforseo-content-generation-api` and then continue."
- "Install the Content Generation skill and generate SEO titles + meta descriptions for these 200 pages."
- "Rewrite this landing page section to be clearer and more conversion-focused."
- "Paraphrase this text into 3 tones: professional, friendly, concise."
- "Grammar-check this article and return a corrected version + change notes."
- "Summarize this long article into a 5-bullet executive brief."
