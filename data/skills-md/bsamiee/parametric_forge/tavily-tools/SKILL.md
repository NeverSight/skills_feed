---
name: tavily-tools
type: complex
depth: base
description: >-
  Executes Tavily AI web operations via unified Python CLI. Use when searching
  the web, extracting content from URLs, crawling websites, or mapping site
  structure.
---

# [H1][TAVILY-TOOLS]
>**Dictum:** *Command-specific arguments enforce correct invocation.*

<br>

Execute Tavily AI web operations through unified Python CLI.

[IMPORTANT] `search` requires `--query`; `extract` requires `--urls`; `crawl`/`map` require `--url`. 1Password injects API key automatically.

```bash
# Search
uv run .claude/skills/tavily-tools/scripts/tavily.py search --query "Vite 7 new features"
uv run .claude/skills/tavily-tools/scripts/tavily.py search --query "React 19" --topic news
uv run .claude/skills/tavily-tools/scripts/tavily.py search --query "Effect-TS" --search-depth advanced --max-results 20

# Extract content from URLs
uv run .claude/skills/tavily-tools/scripts/tavily.py extract --urls "https://example.com"
uv run .claude/skills/tavily-tools/scripts/tavily.py extract --urls "https://a.com,https://b.com" --format text

# Crawl website
uv run .claude/skills/tavily-tools/scripts/tavily.py crawl --url "https://docs.effect.website"
uv run .claude/skills/tavily-tools/scripts/tavily.py crawl --url "https://nx.dev" --max-depth 3 --max-breadth 50

# Map site structure
uv run .claude/skills/tavily-tools/scripts/tavily.py map --url "https://nx.dev"
uv run .claude/skills/tavily-tools/scripts/tavily.py map --url "https://effect.website" --max-depth 2 --limit 200
```

---
## [1][OUTPUT]

Commands return: `{"status": "success|error", ...}`.

| [INDEX] | [CMD]     | [RESPONSE]                             |
| :-----: | --------- | -------------------------------------- |
|   [1]   | `search`  | `{query, results[], images[], answer}` |
|   [2]   | `extract` | `{urls[], results[], failed[]}`        |
|   [3]   | `crawl`   | `{base_url, results[], urls_crawled}`  |
|   [4]   | `map`     | `{base_url, urls[], total_mapped}`     |
