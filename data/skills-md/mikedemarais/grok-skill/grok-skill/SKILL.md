---
name: grok-skill
description: >
  Search and analyze X (Twitter) using xAI Grok 4 via OpenRouter with Live Search.
  Trigger on prompts that explicitly or implicitly ask to "search Twitter/X", "what's
  trending", "tweets from @handle", "hashtag #…", "what are people saying", or
  that require tweet-level activity/engagement from X.
---

# Grok 4 — X/Twitter Live Search Skill

## Prerequisites

- **OpenRouter API key** required (set as `OPENROUTER_API_KEY` environment variable)
- Get your key at [openrouter.ai](https://openrouter.ai)
- Bun runtime installed

## When to use
Use this Skill whenever the user asks for trends, activity, examples, or evidence **from X/Twitter**:
- "search twitter|x for <query>"
- "what's trending on X"
- "top tweets/threads/hashtags about <topic>"
- "what are people saying about <project>"
- "tweets from @handle", "compare @a vs @b"

## How to run (Claude should execute these)
- Minimal:
  ```bash
  bun scripts/grok.ts --q "<query>"
  ```

- One-off with inline API key:
  ```bash
  OPENROUTER_API_KEY="sk-or-..." bun scripts/grok.ts --q "<query>"
  ```

- With handles and date window (YYYY-MM-DD):
  ```bash
  bun scripts/grok.ts \
    --q "<topic or question>" \
    --mode on \
    --include "@OpenAI" "@AnthropicAI" \
    --from "2025-11-01" --to "2025-11-07" \
    --min-faves 50 --min-views 0 \
    --max 12
  ```

- Output is concise JSON: `summary`, `citations` (tweet URLs), and `usage`. Paste a short synthesis with linked tweets.

## Defaults & notes
- Live Search `mode` defaults to `auto`; use `on` for explicit "search X now".
- If user gives handles, pass them via `--include` (or `--exclude`).
- Use `--from/--to` for time-bounded asks; if unspecified, do not assume dates.
- Keep `--max` modest (8–20) for cost/latency; raise only if sparse.
- `--include` and `--exclude` are **mutually exclusive**.
- Do **not** claim access to private/protected content. Prefer links over long quotes.

## Troubleshooting
- Sparse results → increase `--max` or relax filters; consider removing handles.
- Missing links → they're in `citations` of the JSON output; share the URLs.
