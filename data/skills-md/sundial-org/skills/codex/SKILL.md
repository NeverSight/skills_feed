---
name: codex
description: Run OpenAI's Codex CLI agent in non-interactive mode using `codex exec`. Use when delegating coding tasks to Codex, running Codex in scripts/automation, or when needing a second agent to work on a task in parallel.
---

# Codex CLI (Non-Interactive)

Codex is OpenAI's coding agent. Use `codex exec` to run it non-interactively from any cli agent.

## When to Use Codex

Use Codex when:
- **Parallel work**: Delegate a task while continuing other work
- **Second opinion**: Get an independent implementation or review
- **Long-running tasks**: Offload tasks that may take many iterations
- **Code review**: Use `codex exec review` for PR/diff reviews

Do NOT use Codex for:
- Simple file reads/edits you can do directly
- Tasks requiring back-and-forth conversation
- Tasks needing your current context

## Quick Reference

```bash
# Analysis (read-only, default)
codex exec "describe the architecture of this codebase"

# Allow file edits
codex exec --full-auto "fix the failing tests"

# Code review
codex exec review --uncommitted
codex exec review --base main

# Structured JSON output
codex exec --output-schema schema.json -o result.json "extract metadata"

# Continue previous session (inherits original sandbox settings)
codex exec resume --last "now add tests"
```

## Core Concepts

### Output Streams

Progress goes to stderr, final result to stdout. To capture only the result:
```bash
codex exec "summarize the repo" 2>/dev/null > summary.txt
```

To see progress while capturing result:
```bash
codex exec "generate changelog" 2>&1 | tee output.txt
```

### Sandbox Modes

In non-interactive mode, **no approval prompts are possible**. Permissions must be set upfront:

| Mode | Flag | Behavior |
|------|------|----------|
| Read-only | (default) | Reads anywhere, writes/commands blocked |
| Workspace-write | `--full-auto` | Pre-approves edits and commands in workspace |
| Full access | `--yolo` | No restrictions. Use in isolated environments only |

**Choose based on task:**
- Analysis/explanation → default (read-only)
- Fix bugs/implement features → `--full-auto`
- Needs network or system access → `--yolo` (dangerous)

Note: `~/.codex/config.toml` can set project trust levels that override defaults.

### Models

Default model is `gpt-5.2-codex`. Override with `-m`:
```bash
codex exec -m gpt-5 "explain this code"
```

### Authentication

By default, the user should already be authenticated. If not, set `CODEX_API_KEY`:
```bash
CODEX_API_KEY=sk-... codex exec "task"
```

## Code Review

Built-in review subcommand:
```bash
# Review uncommitted changes
codex exec review --uncommitted

# Review against a base branch
codex exec review --base main

# Review a specific commit
codex exec review --commit abc123
```

## Structured Output

Use `--output-schema` for JSON output. **Important**: OpenAI requires `additionalProperties: false` on all object types.

```bash
codex exec --output-schema schema.json -o result.json "extract API endpoints"
```

Schema example:
```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "endpoints": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "path": { "type": "string" },
          "method": { "type": "string" }
        },
        "required": ["path", "method"],
        "additionalProperties": false
      }
    }
  },
  "required": ["name", "endpoints"],
  "additionalProperties": false
}
```

## Session Resume

Resume continues a previous session, **inheriting its sandbox settings**:
```bash
# Start a task
codex exec --full-auto "implement rate limiter"

# Continue later (inherits --full-auto from original)
codex exec resume --last "add unit tests"

# Or resume by session ID
codex exec resume <SESSION_ID> "follow-up task"
```

**Note**: Cannot pass `--full-auto` to resume; it inherits from the original session.

## JSONL Event Stream

For programmatic use, `--json` outputs structured events:
```bash
codex exec --json "analyze code" 2>/dev/null | jq -c 'select(.type == "item.completed")'
```

## Performance & Best Practices

### Execution Time
Complex tasks typically take **60-120+ seconds**. Simple analysis tasks complete in 10-30 seconds.

- Tasks may continue executing even after your timeout
- Always check if files were modified regardless of timeout status
- Use `tail -f <output_file>` to monitor long-running background tasks

### Task Granularity
Break complex work into focused tasks:

```bash
# Good: Focused, single-purpose tasks
codex exec --full-auto "add star ratings to the skill cards"
codex exec --full-auto "add a search filter to the toolbar"

# Avoid: Multi-feature requests in one task
codex exec --full-auto "add ratings, search, filters, modal, and animations"
```

### Concurrent Editing
**Avoid running multiple Codex sessions on the same file simultaneously.** While it may work, concurrent edits risk merge conflicts or overwrites.

### Large Files
Files over ~2000 lines slow execution as Codex reads the entire file multiple times. Consider:
- Splitting into multiple files when possible
- Using specific line references in prompts
- Breaking incremental changes into smaller tasks

## Error Handling

Common errors:
- **Timeout**: Long tasks may timeout. Check if work completed anyway, or use resume to continue.
- **Sandbox blocked**: Task needs writes but running in read-only. Use `--full-auto`.
- **Schema validation**: Missing `additionalProperties: false` in schema objects.
- **Model not supported**: Some models unavailable with ChatGPT auth. Use default `gpt-5.2-codex`.

## Detailed References

- **[exec-reference.md](references/exec-reference.md)**: Complete flag reference
- **[prompting.md](references/prompting.md)**: Effective prompts and workflow patterns

## Project Context

Codex reads `AGENTS.md` files for project instructions:
- `~/.codex/AGENTS.md` - Global defaults
- `<repo>/AGENTS.md` - Project-specific

```markdown
# AGENTS.md
- Run `npm test` after modifying JS files
- Use pnpm for dependencies
```
