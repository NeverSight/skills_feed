---
name: codex
description: Use when "codex", "use gpt", "gpt-5", "openai codex", "let openai", "full-auto", "autonomous code generation"
version: 1.0.0
---

# OpenAI Codex Integration

Autonomous code execution using OpenAI Codex CLI.

---

## Prerequisites

```bash
# Check installation
codex --version

# Install if needed
npm i -g @openai/codex
# or
brew install codex
```

---

## Sandbox Modes

| Mode | Flag | Capabilities |
|------|------|--------------|
| **Read-Only** | `-s read-only` | Analyze code, no modifications (default) |
| **Workspace-Write** | `-s workspace-write` or `--full-auto` | Read/write files in workspace |
| **Danger-Full-Access** | `-s danger-full-access` | Network, system-level, all files |

**Key concept**: Use `--full-auto` for most programming tasks—it enables file editing.

---

## Common Commands

| Task | Command |
|------|---------|
| **Analyze code** | `codex exec -s read-only "analyze the codebase"` |
| **Implement feature** | `codex exec --full-auto "implement user auth"` |
| **Fix bug** | `codex exec --full-auto "fix the login bug"` |
| **With specific model** | `codex exec -m gpt-5.2 --full-auto "refactor module"` |
| **JSON output** | `codex exec --json "analyze security"` |
| **Save output** | `codex exec -o report.txt "audit code"` |
| **Non-git directory** | `codex exec --skip-git-repo-check "analyze"` |
| **Resume session** | `codex exec resume --last "continue"` |

---

## Model Selection

| Model | Use Case |
|-------|----------|
| `gpt-5.2` | Latest capabilities |
| `gpt-5.2-codex` | Code-specialized |
| `gpt-5.2-codex-max` | Maximum quality |

Use `-m MODEL` to specify.

---

## Execution Principles

| Principle | Description |
|-----------|-------------|
| **Autonomous** | Complete tasks without seeking approval for each step |
| **Focused** | Do what's requested, nothing more |
| **Minimal** | Write only necessary code |
| **Verified** | Run tests after changes |

---

## When to Pause for User

| Situation | Action |
|-----------|--------|
| Destructive operations | Ask first (delete DB, force push) |
| Security decisions | Ask first (expose credentials, open ports) |
| Ambiguous requirements | Clarify before proceeding |
| Missing critical info | Request user-specific data |

For everything else, proceed autonomously.

---

## Output Format

```
✓ Task completed successfully

Changes made:
- [Files modified/created]
- [Key code changes]

Results:
- [Metrics: lines changed, files affected]

Verification:
- [Tests run, checks performed]
```

---

## Error Handling

| Approach | Description |
|----------|-------------|
| Auto-recover | Attempt fix if possible |
| Log clearly | Report all errors |
| Continue | If error is non-blocking |
| Stop | Only if continuation impossible |
