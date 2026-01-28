---
name: glhf
description: Search Claude Code conversation history to find past solutions, recall commands, and discover related work. Use when looking for previous implementations, finding commands you ran before, or exploring what was done in past sessions.
---

# glhf

Search your Claude Code conversation history using hybrid search (text + semantic).

## Quick Examples

```bash
# Find past solutions (semantic search)
glhf search "authentication" --mode semantic --compact

# Find commands you've run
glhf search "docker" -t Bash --compact

# Check recent sessions
glhf recent -l 10

# Get session overview then dive deeper
glhf session abc123 --summary
glhf session abc123 --limit 50
```

## Commands

| Command    | Purpose                              |
| ---------- | ------------------------------------ |
| `search`   | Find content across all sessions     |
| `session`  | View a specific session's content    |
| `related`  | Find sessions similar to a given one |
| `recent`   | List recent sessions                 |
| `projects` | List all indexed projects            |
| `status`   | Show index stats                     |
| `index`    | Rebuild the search index             |

## Key Search Flags

| Flag                | Purpose                                       |
| ------------------- | --------------------------------------------- |
| `--compact`         | One-line output, fewer tokens                 |
| `--mode semantic`   | Conceptual search (how to X, patterns)        |
| `--mode text`       | Exact keyword matching                        |
| `-t Bash`           | Filter by tool (Bash, Read, Edit, Grep, etc.) |
| `-p .`              | Filter to current project                     |
| `--since 1d`        | Time filter (1h, 2d, 1w, or date)             |
| `--errors`          | Only show error results                       |
| `--show-session-id` | Include session IDs for follow-up             |

## Recommended Patterns

**Find past solutions:**

```bash
glhf search "problem description" --mode semantic --compact
glhf search "specific keyword" --show-session-id --compact
glhf session <id> --summary
```

**Recall commands:**

```bash
glhf search "git rebase" -t Bash --compact
glhf search "cargo" -t Bash --since 1w --compact
```

**Find similar work:**

```bash
glhf recent -l 10
glhf related <session-id> --limit 5
```

**Debug past errors:**

```bash
glhf search "error" --errors --since 1d --compact
```

## Tips

1. **Always use `--compact`** - significantly reduces output tokens
2. **Use `--mode semantic`** for "how to" questions and conceptual searches
3. **Use `--mode text`** for exact keywords and error messages
4. **Chain commands**: search → get session ID → view summary → get full context
5. **Current project/session auto-excluded** when running inside Claude Code
6. **Use `-p .`** to filter to current project when you want to include it
7. **Use `glhf <command> --help`** for complete option documentation
