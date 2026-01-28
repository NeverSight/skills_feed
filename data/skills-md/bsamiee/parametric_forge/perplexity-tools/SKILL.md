---
name: perplexity-tools
type: complex
depth: base
description: >-
  Executes Perplexity AI queries via unified Python CLI. Use when conducting
  web research, asking questions with citations, deep research tasks, reasoning
  problems, or searching for up-to-date information.
---

# [H1][PERPLEXITY-TOOLS]
>**Dictum:** *Specialized models optimize response quality.*

<br>

Execute Perplexity AI queries via unified Python CLI.

[IMPORTANT] Commands require `--query`. API key auto-injected via 1Password.

```bash
# Quick question—citations (sonar)
uv run .claude/skills/perplexity-tools/scripts/perplexity.py ask --query "What is Effect-TS?"

# Deep research (sonar-deep-research)
uv run .claude/skills/perplexity-tools/scripts/perplexity.py research --query "React 19 new features"
uv run .claude/skills/perplexity-tools/scripts/perplexity.py research --query "Vite 7 migration" --strip-thinking

# Reasoning task (sonar-reasoning-pro)
uv run .claude/skills/perplexity-tools/scripts/perplexity.py reason --query "Compare Vite vs Webpack"
uv run .claude/skills/perplexity-tools/scripts/perplexity.py reason --query "Effect vs RxJS" --strip-thinking

# Web search (sonar)
uv run .claude/skills/perplexity-tools/scripts/perplexity.py search --query "Nx 22 Crystal" --max-results 5
```

---
## [1][OUTPUT]

Commands return: `{"status": "success|error", ...}`.

| [INDEX] | [CMD]      | [RESPONSE]                       |
| :-----: | ---------- | -------------------------------- |
|   [1]   | `ask`      | `{query, response, citations[]}` |
|   [2]   | `research` | `{query, response, citations[]}` |
|   [3]   | `reason`   | `{query, response}`              |
|   [4]   | `search`   | `{query, results[]}`             |
