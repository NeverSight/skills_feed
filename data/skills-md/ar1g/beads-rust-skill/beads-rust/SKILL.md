---
name: beads-rust
description: Manage issues with the beads_rust CLI (`br`). Use when creating, triaging, updating, closing, prioritizing, or linking issues in a repo that uses `.beads`.
license: MIT
domain: project-management
role: specialist
scope: operations
output-format: commands
triggers:
  - br
  - beads
  - beads_rust
  - issue triage
  - backlog
  - dependencies
metadata:
  author: ar1g
  version: 1.0.0
acknowledgements: "Built on beads_rust by @Dicklesworthstone"
---

## Prerequisites

**Step 1 — Detect `br`:**

Always check for `br` before doing anything else:

```bash
command -v br >/dev/null 2>&1
```

If the command succeeds, `br` is available — skip straight to the workflow sections below.

**Step 2 — If `br` is not found:**

Tell the user:

> `br` (beads_rust) is required but was not detected on this system.

Then **offer** to install it via the recommended curl command. Ask clearly and wait for explicit approval — do **not** run the installer without consent.

Recommended install command (run only after user approves):

```bash
curl -fsSL "https://raw.githubusercontent.com/Dicklesworthstone/beads_rust/main/install.sh?$(date +%s)" | bash
```

After the install completes, verify success:

```bash
command -v br >/dev/null 2>&1
```

If verification fails, report the failure and stop.

**Step 3 — If the user declines the install:**

Show the manual alternatives below and stop — do not proceed without `br`.

Manual install via cargo:

```bash
cargo install --git https://github.com/Dicklesworthstone/beads_rust.git
```

Manual install from source:

```bash
git clone https://github.com/Dicklesworthstone/beads_rust.git
cd beads_rust
cargo build --release
cargo install --path .
```

# Beads Rust

Use `br` as the source of truth for issue state. Prefer machine-readable output (`--json`) for
analysis and deterministic updates.

Use this skill when the request involves issue operations in a repo that uses `.beads`, including:
- creating issues
- triaging backlog
- updating priority/status/labels/parent
- linking or removing dependencies
- closing/reopening with evidence
- summarizing ready/blocked queue impact

## Core Rules

1. Read first, mutate second. Use `br show <id> --json` to inspect before updating.
2. Prefer `--json` whenever available.
3. Resolve actor at runtime and pass it via `--actor`; do not ask the user to edit files.
4. Keep changes minimal and scoped to requested issues.
5. Recompute queues after bulk changes.
6. Make closure reasons concrete and auditable.
7. `--format toon` is a token-optimized alternative to `--json` for context-window-sensitive agents. Use `--json` as the safer default.

## Actor Resolution

The agent should choose actor automatically for each mutation batch:
- if `BR_ACTOR` is set, use it
- otherwise use a stable assistant identity (for example model/agent name)
- fallback to `assistant`

Example runtime setup (agent-executed, not user-edited):

```bash
ACTOR="${BR_ACTOR:-assistant}"
```

Use `"$ACTOR"` in mutating commands.

## Verify Workspace

Before any update:

```bash
br where
br ready --json
br blocked --json
br list --status open --sort priority --json
```

If workspace context is wrong or unclear, stop before mutating.

## Standard Workflow

For triage batches:
1. Capture baseline (`ready`, `blocked`, `open list`).
2. Classify each targeted issue.
3. Apply scoped updates.
4. Recompute queues.
5. Report IDs changed and queue deltas.

For single-issue tasks:
1. Verify workspace.
2. Inspect the issue: `br show <id> --json`.
3. Apply requested mutation.
4. Read back state (`--json`) to confirm.
5. Report exact change and rationale.

## Triage Decision Matrix

Use one classification per issue:

- `implemented`
  - close with implementation evidence (commit/PR/file/observable behavior)
- `out-of-scope`
  - close with explicit boundary reason
- `needs-clarification`
  - comment with specific unanswered questions
- `actionable`
  - keep open and correct status/priority/labels/dependencies

During large triage efforts, checkpoint every few updates:

```bash
br ready --json
br blocked --json
```

## Create High-Quality Issues

Bug issues should include:
- concise summary
- reproduction steps
- expected vs actual
- environment/context
- logs or crash pointers

Task/feature issues should include:
- objective
- acceptance criteria
- constraints and non-goals
- dependencies or parent linkage

For rapid capture when only a title is needed, use `br q "<title>"` to get an ID quickly.

Reference command templates:
- `references/command-cookbook.md`

## Update Patterns

Use small idempotent mutations:

```bash
ACTOR="${BR_ACTOR:-assistant}"
br update --actor "$ACTOR" <id> --priority 2 --status in_progress --json
br update --actor "$ACTOR" <id> --add-label reliability --json
br update --actor "$ACTOR" <id> --parent <parent-id> --json
br comments add --actor "$ACTOR" <id> --message "<triage note / evidence>" --json
```

Multiple IDs can be passed to `br update` for batch triage:

```bash
br update --actor "$ACTOR" <id1> <id2> <id3> --priority 2 --add-label triage-reviewed --json
```

Prefer comment-first when facts are incomplete.

## Dependency Hygiene

Use explicit dependencies to keep ready/blocked accurate.

Rules:
- add `blocks` only for real execution ordering constraints
- remove stale dependency links promptly
- verify dependency effects after changes

Commands:

```bash
br dep add <issue-id> <depends-on-id> --type blocks
br dep rm <issue-id> <depends-on-id>
br dep list <issue-id> --json
br blocked --json
```

## Closure Standard

Before closing an issue:
1. provide evidence artifact (commit/PR/path/observed behavior)
2. state what was verified
3. use precise `--reason`

Close/reopen patterns:

```bash
ACTOR="${BR_ACTOR:-assistant}"
br close --actor "$ACTOR" <id> --reason "<specific reason with evidence>" --json
br reopen --actor "$ACTOR" <id> --reason "<reason for reopening>" --json
```

If confidence is low, add clarification comments instead of closing.

For milestone issues, summarize unmet criteria in a comment before closure decisions.

## Reporting Format

When reporting work, include:
1. changed issue IDs and exact mutations
2. reason for each meaningful change
3. queue impact (`ready`, `blocked`)
4. explicit follow-ups needed

Preferred response shape:

```text
Updated:
- <id>: <change>

Closed:
- <id>: <reason + evidence>

Queue impact:
- ready: <summary>
- blocked: <summary>

Needs input:
- <id>: <question>
```

## Safety Guardrails

- Do not modify unrelated issues.
- Do not invent evidence for closure.
- Do not add speculative dependencies.
- Re-run reads with `--json` when output is ambiguous.
- Prefer reversible updates over broad, risky edits.

## Quick Command Reference

Use `references/command-cookbook.md` for concise copy/paste command patterns.
