---
name: beads
description: Use this skill to manage work in Beads (bd), a git-backed issue tracker for AI agents, including issue lifecycle, dependencies, sync, and agent hooks.
metadata:
  short-description: Expert guidance for Beads (bd) CLI workflows and agent integration.
---

# Beads Skill

Expert guidance for using Beads (`bd`) to track tasks, dependencies, and workflows in a git-backed issue graph.

## When to trigger
- The user mentions Beads, `bd`, or wants dependency-aware task tracking for agents.
- The task involves `bd init`, `bd ready`, `bd sync`, formulas/molecules, or agent hooks.

## Core rules
- Prefer CLI + hooks (`bd setup <recipe>`) when shell access exists; use MCP only when CLI is unavailable.
- For agent one-shot commands, default to direct mode: `bd --no-daemon ...`.
- Always use `--json` for machine parsing (`bd list`, `bd show`, `bd create`, etc.).
- Use `bd ready` (or `bd list --ready`) to select unblocked work; add dependencies with `bd dep add` before starting.
- Run `bd sync` to export DB state to JSONL; it does **not** commit/push by default.
- Use `bd daemon` (with `--auto-commit/--auto-push`) or `bd sync --full` only when background automation is explicitly needed.
- Default backend is SQLite; use `bd init --backend dolt` for Dolt-backed storage.

## Workflow
1. **Initialize**: verify with `bd status`; if needed, run `bd init` (choose backend and branch). See [references/cli-reference.md](references/cli-reference.md).
2. **Integrate**: install hooks with `bd setup <recipe>` or configure manually. See [references/integrations.md](references/integrations.md).
3. **Manage issues**: create, update status, close with reason; maintain dependencies; use `bd list`, `bd ready`, `bd blocked`, `bd stats`.
4. **Sync + context**: `bd prime` on session start; `bd sync` after issue changes and `bd sync --import` after pull; use `bd sync --status` to verify state.
5. **Advanced workflows**: formulas, molecules, gates (`bd formula`, `bd mol`, `bd gate`). See [references/workflows.md](references/workflows.md).
6. **Recovery**: use `bd status`, `bd daemon status`, and `bd doctor` when sync or database issues appear. See [references/recovery.md](references/recovery.md).

## Output expectations
- Provide exact commands with flags and IDs; prefer `--json` and include `--no-daemon` unless daemon mode is the goal.
- Ask for backend, repo location, and desired workflow if ambiguous.
- Call out whether a command affects git-tracked JSONL vs local DB.

## References
- CLI commands and options: [references/cli-reference.md](references/cli-reference.md)
- Core concepts and storage: [references/concepts.md](references/concepts.md)
- Workflows: formulas, molecules, gates: [references/workflows.md](references/workflows.md)
- Editor/agent integrations + MCP: [references/integrations.md](references/integrations.md)
- Recovery and troubleshooting: [references/recovery.md](references/recovery.md)
