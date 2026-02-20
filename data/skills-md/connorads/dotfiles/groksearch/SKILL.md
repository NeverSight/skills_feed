---
name: groksearch
description: Search X and the web using Grok (xAI) API, then summarise results with top sources.
argument-hint: "[query]"
---

# groksearch

Search X and the web using Grok's server-side tools and return a concise summary with top sources.

This skill uses Grok's own `x_search` and `web_search` tools (not Claude WebSearch).

## Usage

Run the script using absolute path (do NOT cd to the skill directory first):

```bash
uv run ~/.claude/skills/groksearch/scripts/groksearch.py "your query"
```

### Common options

```bash
# X + Web (default)
uv run ~/.claude/skills/groksearch/scripts/groksearch.py "your query" --sources both

# X only
uv run ~/.claude/skills/groksearch/scripts/groksearch.py "your query" --sources x

# Web only
uv run ~/.claude/skills/groksearch/scripts/groksearch.py "your query" --sources web

# Last 14 days
uv run ~/.claude/skills/groksearch/scripts/groksearch.py "your query" --days 14

# Explicit date range
uv run ~/.claude/skills/groksearch/scripts/groksearch.py "your query" --from-date 2026-01-01 --to-date 2026-01-31

# No date filtering
uv run ~/.claude/skills/groksearch/scripts/groksearch.py "your query" --no-date
```

## API Key

Provide the xAI API key in one of these ways (highest priority first):

1. `--api-key` argument
2. `XAI_API_KEY` environment variable
3. `~/.config/groksearch/.env` file

Example config file:

```bash
mkdir -p ~/.config/groksearch
cat > ~/.config/groksearch/.env << 'EOF'
XAI_API_KEY=
EOF
chmod 600 ~/.config/groksearch/.env
```

## Output

The script prints:
- Query, sources, and date range
- A concise summary with key points
- A short list of top source URLs (from Grok citations)
