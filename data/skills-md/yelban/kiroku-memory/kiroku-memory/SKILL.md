---
name: kiroku-memory
description: |
  AI Agent long-term memory system with cross-session, cross-project persistence.
  Triggers:
  - /remember - Store memories
  - /recall - Search memories
  - /forget - Delete/archive memories
  - /memory-status - Check status
  - When needing to persist important conversation insights
  - When sharing user preferences across projects
---

# Kiroku Memory

Cross-session, cross-project memory for AI Agents.

## Commands

Execute via `scripts/`:

| Command | Script | Args |
|---------|--------|------|
| `/remember` | `remember.py` | `<content> [--category CAT] [--global]` |
| `/recall` | `recall.py` | `<query> [--context]` |
| `/forget` | `forget.py` | `<query>` |
| `/memory-status` | `memory-status.py` | (none) |

## Scopes

- `global:user` — Cross-project (personal preferences)
- `project:<name>` — Project-specific (architecture decisions)

Default: project directory → project scope; otherwise → global scope.

## Categories (by priority)

`preferences` (1.0) > `facts` (0.9) > `goals` (0.7) > `skills` (0.6) > `relationships` (0.5) > `events` (0.4)

## Hooks

- **SessionStart**: Auto-loads memory context via `/context` API
- **Stop**: Auto-saves important content (dual-phase: regex + async LLM)

## References

- [API Contract](references/api-contract.md) — Endpoint specs
- [Scopes](references/scopes.md) — Scope resolution logic
- [Filtering Rules](references/filtering-rules.md) — What gets saved
- [Retrieval Policy](references/retrieval-policy.md) — Priority & truncation
- [Auto-Save](references/auto-save.md) — Two-phase memory capture details
