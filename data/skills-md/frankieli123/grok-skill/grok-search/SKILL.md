---
name: grok-search
description: Real-time web research/search with sources (outputs JSON).
---

## When to use (aggressive)

- Default to using this skill before answering anything that might be outdated, ambiguous, or requires external confirmation (APIs, versions, errors, docs, releases).
- If you feel even slightly unsure, search first, then answer with evidence.

## Quick start

### Configure (recommended)

Run once to write config:

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\grok-search\configure.ps1"
```

Default config path (recommended): `C:\Users\<you>\.codex\skills\grok-search\config.json` (override with `--config` or `GROK_CONFIG_PATH`).

Write to user-level config instead (optional):

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\grok-search\configure.ps1" -Global
```

### Configure (env vars)

If you prefer env vars:

```powershell
$env:GROK_BASE_URL="https://your-grok-endpoint.example"
$env:GROK_API_KEY="YOUR_API_KEY"
$env:GROK_MODEL="grok-2-latest"
```

### Run

```bash
python scripts/grok_search.py --query "What changed in X recently?"
```

## Output

Prints JSON to stdout:

- `content`: the synthesized answer
- `sources`: best-effort list of URLs (and optional titles/snippets)
- `raw`: raw assistant content (if parsing failed)

## Notes

- Endpoint: `POST {GROK_BASE_URL}/v1/chat/completions` (also supports `{GROK_BASE_URL}/chat/completions` if you set `GROK_BASE_URL` ending with `/v1`).
- You can override model via `--model` or `GROK_MODEL`.
- If your 2api requires custom flags to enable web search, pass them via `--extra-body-json` / `GROK_EXTRA_BODY_JSON`.
