---
name: superspec-plan
description: Use when planning artifacts are needed and proposal/specs already exist for an OpenSpec change.
user-invocable: true
---

# Superspec Plan

## Rules (non-negotiable)
- Drive OpenSpec via CLI only (NO OpenSpec slash commands; i.e., commands starting with `/opsx` or `/openspec`).
- Prefer JSON output for every OpenSpec call (use `--json`).
- Keep changes scoped to `design` and `tasks` artifacts only.

## Change Selection
1. If the user provides a change name, use it as `<change>`.
2. Else run:
   - `openspec list --json`
   Ask the user to confirm/select a change name from the JSON output.
3. If there are no changes (or the user wants a new one), STOP and tell the user to run `/superspec-research` first to create proposal/specs for a new change.

Always print:
- `Selected change: <change>`

## Artifact Loop (design + tasks)
Repeat until BOTH `design` and `tasks` are complete.

### 0. Inspect status
Run:
- `openspec status --change <change> --json`

Parse the JSON to determine, for artifacts `design` and `tasks`:
- whether each is `ready` vs `complete`
- whether either is blocked (and why)

If the JSON schema is unclear, show the JSON and ask the user what the status fields mean; do not guess.

### 1. Blocked behavior
If `design` is blocked due to missing `proposal` or `specs`, STOP and tell the user to run `/superspec-research`.

If `tasks` is blocked due to missing `proposal` or `specs` (directly or indirectly), STOP and tell the user to run `/superspec-research`.

If either artifact is blocked for some other reason, STOP, show the status JSON, and ask the user what to do.

Note: If `tasks` is blocked only due to missing `design`, create `design` first (this skill owns `design`).

### 2. Create/Update design
If `design` is ready (and not complete):
1. Run:
   - `openspec instructions design --change <change> --json`
2. From the JSON, extract at minimum:
   - `outputPath` (where to write)
   - `template` and/or `instruction` content
   - dependency inputs (especially `proposal.md` and delta specs under `specs/**/spec.md`)
3. Read the dependencies indicated by the JSON (proposal + delta specs) and write `design.md` to the concrete `outputPath` using the provided template/instructions.

If `outputPath` is not a concrete file path (unexpected), STOP and show the full JSON.

Design must be grounded strictly in proposal + delta specs (no extra scope), and should cover:
- technical approach and key decisions
- data/control flow
- interfaces/contracts that change
- specific files/modules expected to change
- test strategy mapped to scenarios
- `## Test Commands (mechanical)` with default Verify Command(s) per Test Obligation `Type` (unit|integration|e2e)

After writing, print:
- `Wrote design: <outputPath>`

### 3. Create/Update tasks
If `tasks` is ready (and not complete):
1. Run:
   - `openspec instructions tasks --change <change> --json`
2. From the JSON, extract at minimum:
   - `outputPath` (where to write)
   - `template` and/or `instruction` content
   - dependency inputs (especially `design.md`)
3. Read the dependencies indicated by the JSON (especially `design.md` and delta specs under `specs/**/spec.md`) and write `tasks.md` to the concrete `outputPath`.

Hard requirements for `tasks.md`:
- ONLY checkbox tasks, one per line, in this exact form:
  - `- [ ] X.Y <task>`
- Tasks are ordered by dependency.
- Each task is individually verifiable (a human can check it off with a clear done condition).
- No non-checkbox bullets, no paragraphs, no headers.

TDD compilation rules (non-negotiable):
- Compile tasks at Scenario granularity.
- For each `#### Scenario:` in delta specs under `specs/**/spec.md`, generate exactly 5 tasks with tags:
  - `- [ ] N.1 [TDD][RED] Spec:<capability> Scenario:<name> Write failing test: <Test File>::<Test Name>`
  - `- [ ] N.2 [TDD][VERIFY_RED] Run: <Verify Command> (expect FAIL contains: "<Expected (RED)>")`
  - `- [ ] N.3 [TDD][GREEN] Implement minimal production code to satisfy Scenario:<name>`
  - `- [ ] N.4 [TDD][VERIFY_GREEN] Run: <Verify Command> (expect PASS)`
  - `- [ ] N.5 [TDD][REFACTOR] Refactor (no behavior change), keep tests green`
- `Verify Command` resolution order:
  1) Scenario `##### Test Obligation` -> `Verify Command`
  2) `design.md` -> `## Test Commands (mechanical)` (type-matched default)
  3) STOP and ask the user (do not guess)
- [NON-TDD] allowed ONLY for: docs-only, config-only (no behavior change), generated outputs, formatting/renaming only.
  - For each [NON-TDD] unit generate exactly 2 tasks:
    - `- [ ] N.1 [NON-TDD][DO] <action>`
    - `- [ ] N.2 [NON-TDD][VERIFY] <mechanical verification command>`
  - VERIFY must be mechanical (command output / file existence / OpenSpec validate), not a manual check.

If `outputPath` is not a concrete file path (unexpected), STOP and show the full JSON.

After writing, print:
- `Wrote tasks: <outputPath>`

### 4. Re-check
After creating design or tasks, re-run:
- `openspec status --change <change> --json`

Stop the loop only when both artifacts show complete.

## Minimal Output Contract
- Always show `Selected change: <change>`.
- For each artifact you write, show exactly which artifact and the concrete path(s).
- On any error, show the exact command that failed (including `--json`).

## Common mistakes
- Writing non-checkbox tasks (anything other than `- [ ] X.Y ...`) in `tasks.md`.
- Using OpenSpec slash commands (anything starting with `/opsx` or `/openspec`) instead of the `openspec` CLI.
- Skipping the blocked rule (if proposal/specs are missing, stop and send the user to `/superspec-research`).
