---
name: beads
description: "Beads (bd) distributed git-backed issue tracker for AI agents: hash-based IDs, dependency graphs, worktrees, molecules, sync. Keywords: bd, beads, issue tracker, git-backed, dependencies, molecules, worktree, sync, AI agents."
version: "0.49.1"
release_date: "2026-01-26"
---

# Beads (bd)

Distributed, git-backed graph issue tracker for AI coding agents. Persistent memory with dependency-aware task tracking.

## Quick Start

```bash
# Install
brew install steveyegge/beads/bd
# or
curl -fsSL https://raw.githubusercontent.com/steveyegge/beads/main/scripts/install.sh | bash

# Initialize in repo (humans run once)
bd init

# Tell your agent
echo "Use 'bd' for task tracking" >> AGENTS.md
```

## When to Use

- AI agent needs persistent task memory across sessions
- Tracking dependencies between tasks (`blocks:`, `depends_on:`)
- Multi-agent/multi-branch workflows (hash-based IDs prevent conflicts)
- Incremental delivery with molecules/gates
- Sync issues with Linear, Jira, GitHub

## Essential Commands

| Command                       | Action                                |
| ----------------------------- | ------------------------------------- |
| `bd ready`                    | List tasks with no open blockers      |
| `bd ready --gated`            | Tasks waiting at gate checkpoints     |
| `bd create "Title" -p 0`      | Create P0 task                        |
| `bd show <id>`                | View task details and audit trail     |
| `bd update <id> --status=X`   | Update status (open/in_progress/done) |
| `bd close <id>`               | Close task                            |
| `bd dep add <child> <parent>` | Link tasks (blocks, related, parent)  |
| `bd list`                     | List issues (default: 50, non-closed) |
| `bd sync`                     | Sync with git/remote                  |

## Hash-Based IDs

Issues use hash-based IDs like `bd-a1b2` to prevent merge conflicts:

```bash
bd create "Fix login bug" -p 1
# Created: bd-x7k3

bd show bd-x7k3
```

### Hierarchical IDs

```
bd-a3f8      (Epic)
bd-a3f8.1    (Task)
bd-a3f8.1.1  (Sub-task)
```

Use `bd children <id>` to view hierarchy.

## References

| File                                    | Purpose                                   |
| --------------------------------------- | ----------------------------------------- |
| [workflow.md](references/workflow.md)   | Daily operations, status flow, sync       |
| [authoring.md](references/authoring.md) | Writing quality issues, EARS patterns     |
| [molecules.md](references/molecules.md) | Molecules, gates, formulas, compounds     |
| [sync.md](references/sync.md)           | Git sync, sync-branch, Linear/Jira import |

## Key Concepts

### Git as Database

Issues stored as JSONL in `.beads/`. Versioned, branched, merged like code.

### Dependency Graph

```bash
bd dep add bd-child bd-parent --blocks   # child blocks parent
bd dep add bd-a bd-b --related           # related items
bd ready                                 # only shows unblocked work
```

### Molecules (Advanced)

Molecules group related issues with gates for incremental delivery:

```bash
bd mol create "Feature X" --steps=3      # Create 3-step molecule
bd mol progress bd-xyz                   # Check progress
bd mol burn bd-xyz                       # Complete molecule
```

### Stealth Mode

Use Beads locally without committing to repo:

```bash
bd init --stealth
```

### Contributor vs Maintainer

```bash
# Contributor (forked repos) — separate planning repo
bd init --contributor

# Maintainer auto-detected via SSH/HTTPS credentials
```

## Configuration

Config stored in `.beads/config.yaml`:

```yaml
sync:
  branch: beads-sync # Sync to separate branch
  remote: origin
daemon:
  auto_start: true
  auto_sync: true
types:
  custom:
    - name: spike
      statuses: [open, in_progress, done]
```

## Agent Integration

### Tell Agent About Beads

Add to `AGENTS.md`:

```markdown
## Task Tracking

Use `bd` for task tracking. Run `bd ready` to find work.
```

### Agent-Optimized Output

```bash
BD_AGENT_MODE=1 bd list --json  # Ultra-compact JSON output
bd list --json                   # Standard JSON output
```

### MCP Plugin

Beads includes Claude Code MCP plugin for direct integration.

## Critical Commands

```bash
# What to work on
bd ready                    # Unblocked tasks
bd ready --pretty           # Formatted output

# Create with dependencies
bd create "Task B" --blocks bd-a1b2

# Doctor (fix issues)
bd doctor                   # Check health
bd doctor --fix             # Auto-fix problems

# Sync
bd sync                     # Full sync
bd sync --import-only       # Import only
```

## Anti-patterns

| ❌ Wrong              | ✅ Correct                  |
| --------------------- | --------------------------- |
| `priority: high`      | `-p 1` (P0-P4 numeric)      |
| Manual JSON editing   | Use `bd` commands           |
| Ignoring `bd ready`   | Always check blockers first |
| Skipping `bd sync`    | Sync regularly              |
| Creating without deps | Declare `--blocks` upfront  |

## Links

- [Releases](https://github.com/steveyegge/beads/releases)
- [Documentation](https://github.com/steveyegge/beads#readme)
- [Community Tools](https://github.com/steveyegge/beads/blob/main/docs/COMMUNITY_TOOLS.md)
