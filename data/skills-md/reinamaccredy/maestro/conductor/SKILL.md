---
name: conductor
description: Implementation execution for context-driven development. Trigger with ci, /conductor-implement, or /conductor-* commands. Use when executing tracks with specs/plans. For design phases, see designing skill. For session handoffs, see handoff skill.
---

# Conductor: Implementation Execution

Execute tracks with TDD and parallel routing.

## Entry Points

| Trigger | Action | Reference |
|---------|--------|-----------|
| `/conductor-setup` | Initialize project context | [workflows/setup.md](references/workflows/setup.md) |
| `/conductor-implement` | Execute track (auto-routes if parallel) | [workflows/implement.md](references/workflows/implement.md) |
| `ca`, `/conductor-autonomous` | **Run ralph.sh directly** (no Task/sub-agents) | [workflows/autonomous.md](references/workflows/autonomous.md) |
| `/conductor-status` | Display progress overview | [structure.md](references/structure.md) |
| `/conductor-revise` | Update spec/plan mid-work | [workflows.md#revisions](references/workflows.md#revisions) |

## Related Skills (Not Owned by Conductor)

| For... | Use Skill | Triggers |
|--------|-----------|----------|
| Design phases (1-8) | [designing](../designing/SKILL.md) | `ds`, `cn`, `/conductor-design`, `/conductor-newtrack` |
| Session handoffs | [handoff](../handoff/SKILL.md) | `ho`, `/conductor-finish`, `/conductor-handoff` |

## Quick Reference

| Phase | Purpose | Output | Skill |
|-------|---------|--------|-------|
| Requirements | Understand problem | design.md | designing |
| Plan | Create spec + plan | spec.md + plan.md | designing |
| **Implement** | Build with TDD | Code + tests | **conductor** |
| **Autonomous** | Ralph loop execution | Auto-verified stories | **conductor** |
| Reflect | Verify before shipping | LEARNINGS.md | handoff |

## Core Principles

- **Load core first** - Load [maestro-core](../maestro-core/SKILL.md) for routing table and fallback policies
- **TDD by default** - RED → GREEN → REFACTOR (use `--no-tdd` to disable)
- **Beads integration** - Zero manual `bd` commands in happy path
- **Parallel routing** - `## Track Assignments` in plan.md triggers orchestrator
- **Validation gates** - Automatic checks at each phase transition

## Directory Structure

```
conductor/
├── product.md, tech-stack.md, workflow.md  # Project context
├── code_styleguides/                       # Language-specific style rules
├── CODEMAPS/                               # Architecture docs
├── handoffs/                               # Session context
├── spikes/                                 # Research spikes (pl output)
└── tracks/<track_id>/                      # Per-track work
    ├── design.md, spec.md, plan.md         # Planning artifacts
    └── metadata.json                       # State tracking (includes planning state)
```

See [structure.md](references/structure.md) for full details.

## Beads Integration

All execution routes through orchestrator with Agent Mail coordination:
- Workers claim beads via `bd update --status in_progress`
- Workers close beads via `bd close --reason completed|skipped|blocked`
- File reservations via `file_reservation_paths`
- Communication via `send_message`/`fetch_inbox`

See [beads/integration.md](references/beads/integration.md) for all 13 integration points.

## `/conductor-implement` Auto-Routing

1. Read `metadata.json` - check `orchestrated` flag
2. Read `plan.md` - check for `## Track Assignments`
3. Check `beads.fileScopes` - file-scope based grouping (see [execution/file-scope-extractor](references/execution/file-scope-extractor.md))
4. If parallel detected (≥2 non-overlapping groups) → Load [orchestrator skill](../orchestrator/SKILL.md)
5. Else → Sequential execution with TDD

### File Scope Detection

File scopes determine parallel routing (see [execution/parallel-grouping](references/execution/parallel-grouping.md)):
- Tasks touching same files → sequential (same track)
- Tasks touching different files → parallel (separate tracks)

## Anti-Patterns

- ❌ Manual `bd` commands when workflow commands exist
- ❌ Ignoring validation gate failures
- ❌ Using conductor for design (use [designing](../designing/SKILL.md) instead)
- ❌ Using conductor for handoffs (use [handoff](../handoff/SKILL.md) instead)

## Related

- [designing](../designing/SKILL.md) - Double Diamond design + track creation
- [handoff](../handoff/SKILL.md) - Session cycling and finish workflow
- [tracking](../tracking/SKILL.md) - Issue tracking (beads)
- [orchestrator](../orchestrator/SKILL.md) - Parallel execution
- [maestro-core](../maestro-core/SKILL.md) - Routing policies
