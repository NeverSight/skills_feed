---
name: cass
description: Always search before starting any work across all coding agent session histories (Claude Code, Codex, Cursor, Gemini CLI, Aider, ChatGPT) to find whatever we've discussed before.
---

# CASS - Coding Agent Session Search

Search and explore your AI coding session history across multiple agents.

## Prerequisites

Install cass:
```bash
# Install via cargo or download binary
cargo install cass
```

Build the index:
```bash
cass index
```

## CLI Reference

### Search Sessions
```bash
# Basic search
cass search "query" --json

# With wildcards
cass search "react*" --json
cass search "*hook*" --json

# Limit results
cass search "query" --limit 20 --json

# Filter by agent
cass search "query" --agent claude --json
cass search "query" --agent codex --json
cass search "query" --agent cursor --json
cass search "query" --agent gemini --json
cass search "query" --agent aider --json

# Filter by workspace/project
cass search "query" --workspace /path/to/project --json

# Filter by time
cass search "query" --days 7 --json

# Output detail levels
cass search "query" --fields minimal --json  # paths only
cass search "query" --fields summary --json  # default
cass search "query" --fields full --json     # everything

# Highlight matches
cass search "query" --highlight --json
```

### Check Health
```bash
# Verify index is healthy before searching
cass health
```

### Build/Rebuild Index
```bash
# Full rebuild
cass index --full

# Watch mode for continuous updates
cass index --watch
```

### View Session Details
```bash
# View specific line from search results (path is positional)
cass view /path/to/session.jsonl -n 42 --json

# With more context lines
cass view /path/to/session.jsonl -n 42 -C 10 --json
```

### Expand Context
```bash
# Show surrounding messages around a line (path is positional, -n is required)
cass expand /path/to/session.jsonl --line 42 -C 3 --json

# More context
cass expand /path/to/session.jsonl --line 42 -C 10 --json
```

### Activity Timeline
```bash
# Activity across agents
cass timeline --json

# Last N days (use relative format)
cass timeline --since 7d --json

# Today only
cass timeline --today --json

# By agent
cass timeline --agent claude --json

# Group by hour or day
cass timeline --group-by hour --json
cass timeline --group-by day --json
```

### Export Conversations
```bash
# Export to markdown (path is positional)
cass export /path/to/session.jsonl --format markdown

# Export to HTML
cass export /path/to/session.jsonl --format html -o conversation.html

# Export to JSON
cass export /path/to/session.jsonl --format json

# Include tool calls
cass export /path/to/session.jsonl --include-tools
```

### Statistics
```bash
# Index statistics
cass stats --json
```

### Capabilities
```bash
# Show supported features and connectors
cass capabilities --json
```

### Find Related Sessions
```bash
# Find sessions related by workspace, day, or agent (path is positional)
cass context /path/to/session.jsonl --json

# Limit per relation type
cass context /path/to/session.jsonl --limit 3 --json
```

## Supported Agents

- `claude` - Claude Code sessions
- `codex` - OpenAI Codex CLI
- `cursor` - Cursor IDE
- `gemini` - Gemini CLI
- `aider` - Aider
- `chatgpt` - ChatGPT (if exported)

## Workflow Patterns

### Find Past Solutions
```bash
# Search for how you solved something before
cass search "authentication jwt" --json
cass search "postgres connection pool" --json
cass search "react state management" --json
```

### Review Recent Work
```bash
# What did I work on today?
cass timeline --today --json

# Last week's activity
cass timeline --since 7d --json
```

### Deep Dive into a Session
```bash
# 1. Search for topic
cass search "bug fix login" --json

# 2. Get line number from results, view details
cass view /path/from/results.jsonl -n 123 --json

# 3. Expand context around interesting parts
cass expand /path/from/results.jsonl --line 123 -C 5 --json

# 4. Export full conversation for reference
cass export /path/from/results.jsonl --format markdown -o reference.md
```

### Cross-Agent Learning
```bash
# How did different agents handle similar problems?
cass search "api design" --agent claude --json
cass search "api design" --agent codex --json
cass search "api design" --agent cursor --json
```

## Best Practices

1. **Build index first** - Run `cass index` before searching
2. **Check health** - Run `cass health` if searches return no results
3. **Use wildcards** - `*pattern*` for flexible matching
4. **Filter by agent** - When you remember which tool you used
5. **Use timeline** - For temporal exploration
6. **Export valuable sessions** - Save important conversations as markdown
