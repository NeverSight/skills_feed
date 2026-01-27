---
name: codex
description: Execute Codex CLI for code generation, analysis, web search and web fetch. Two capabilities - (1) Code Generation with deep reasoning, (2) Web Search & Fetch for online research.
---

# Codex CLI Integration

Two specialized capabilities for different use cases.

## Capability 1: Code Generation

Deep code analysis and generation with maximum reasoning power.

### When to Use

- Complex code analysis requiring deep understanding
- Large-scale refactoring across multiple files
- Automated code generation with safety controls
- Tasks requiring specialized reasoning models

### Default Configuration

- Model: `gpt-5.2-codex`
- Reasoning: `xhigh` (maximum thinking depth)

### Command Pattern

```bash
codex e -m gpt-5.2-codex -c model_reasoning_effort=xhigh \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  -C <workdir> \
  "<task>"
```

### Parameters

- `<task>` (required): Task description, supports `@file` references
- `-m <model>`: Override model (e.g., `gpt-5.1-codex`, `gpt-5`)
- `-c model_reasoning_effort=<level>`: Override reasoning (low/medium/high/xhigh)
- `-C <workdir>`: Working directory (default: current)

### Examples

Basic code analysis:
```bash
codex e -m gpt-5.2-codex -c model_reasoning_effort=xhigh \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  "explain @src/main.ts"
```

Refactoring with custom model:
```bash
codex e -m gpt-5.1-codex -c model_reasoning_effort=high \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  "refactor @src/utils for performance"
```

Multi-file analysis:
```bash
codex e -m gpt-5.2-codex -c model_reasoning_effort=xhigh \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  -C /path/to/project \
  "analyze @. and find security issues"
```

---

## Capability 2: Web Search & Fetch

Online research with web search and page content fetching.

### When to Use

- Online research and documentation lookup
- Fetch and summarize specific web pages (GitHub repos, docs, articles)
- Current information retrieval
- API documentation search
- Technology comparison and recommendations

### Default Configuration

- Model: `gpt-5.1-codex`
- Reasoning: `high`
- Web search: enabled

### Command Pattern

```bash
codex e -m gpt-5.1-codex -c model_reasoning_effort=high \
  --enable web_search_request \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  "<task>"
```

### Parameters

- `<task>` (required): Search query or research task
- `-m <model>`: Override model
- `-c model_reasoning_effort=<level>`: Override reasoning (low/medium/high/xhigh)
- `--enable web_search_request`: Enable web search (required for this capability)

### Alternative: Config File

Add to `~/.codex/config.toml`:
```toml
[features]
web_search_request = true
```

### Examples

Fetch GitHub repo:
```bash
codex e -m gpt-5.1-codex -c model_reasoning_effort=high \
  --enable web_search_request \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  "Fetch and summarize https://github.com/user/repo"
```

Documentation search:
```bash
codex e -m gpt-5.1-codex -c model_reasoning_effort=high \
  --enable web_search_request \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  "find the latest React 19 hooks documentation"
```

Technology research:
```bash
codex e -m gpt-5.1-codex -c model_reasoning_effort=high \
  --enable web_search_request \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  "compare Vite vs Webpack for React projects in 2024"
```

---

## Session Resume

Both capabilities support session resumption for multi-turn conversations.

### Resume Command

```bash
codex e resume <session_id> "<follow-up task>"
```

### Example

```bash
# First session (code generation)
codex e -m gpt-5.2-codex -c model_reasoning_effort=xhigh \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  "add comments to @utils.js"
# Output includes: thread_id in JSON output

# Continue the conversation
codex e resume <session_id> "now add type hints"
```

---

## Notes

- Requires Codex CLI installed and authenticated
- `@file` syntax references files relative to working directory
- `@.` references entire working directory
- JSON output available with `--json` flag for programmatic use
- All commands use `--dangerously-bypass-approvals-and-sandbox` for automation
- Use `--skip-git-repo-check` to work in any directory
