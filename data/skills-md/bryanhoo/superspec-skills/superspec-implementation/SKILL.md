---
name: superspec-implementation
description: Use when implementing a planned OpenSpec change by applying tasks and validating all artifacts.
user-invocable: true
---

# Superspec Implementation (Apply + Validate)

## Rules (non-negotiable)
- Drive OpenSpec via CLI only (NO OpenSpec slash commands; i.e., commands starting with `/opsx` or `/openspec`).
- It is OK to tell the user to run Superspec skills like `/superspec-plan`; only OpenSpec slash commands are disallowed.
- Prefer JSON output for every OpenSpec call (use `--json`).
- Only implement what the tasks/specs require; do not expand scope.
- Do not proceed if required tasks/artifacts are missing or blocked.

## Change Selection
1. If the user provides a change name, use it as `<change>`.
2. Else run:
   - `openspec list --json`
   Ask the user to confirm/select a change name from the JSON output.

Always print:
- `Selected change: <change>`

## Block If Tasks Missing/Blocked
1. Run:
   - `openspec status --change <change> --json`
2. If the JSON clearly indicates `tasks` is missing or blocked, STOP and tell the user to run `/superspec-plan`.

If the JSON does not clearly indicate whether `tasks` is ready/blocked, show the JSON and ask the user what the status fields mean; do not guess.

## Apply Instructions (gating/progress)
Run:
- `openspec instructions apply --change <change> --json`

From the JSON, extract any gating/progress indicators if present (e.g., tracked file path, completion rules, progress counts).
- If progress information exists, report it during implementation.
- If the JSON is unclear, show it; do not guess.

## Implement Tasks (Mechanical)
Before executing any task line, follow `/superspec-tdd` as a strict enforcement subroutine.

1. Open the `tasks.md` for the selected change.
   - If you cannot determine the path, use the status/apply JSON to locate it.
2. For each unchecked task line (`- [ ] ...`) in order:
   - Parse tags on the line. If tags are missing or unknown, STOP and ask the user.
   - Execute mechanically based on tags:
     - `[TDD][RED]`: write tests only (no production code).
     - `[TDD][VERIFY_RED]`: extract the command from the same line after `Run:` and run it exactly; confirm FAIL contains the `Expected (RED)` substring.
     - `[TDD][GREEN]`: implement minimal production code to satisfy the Scenario.
     - `[TDD][VERIFY_GREEN]`: extract the command from the same line after `Run:` and run it exactly; confirm PASS.
     - `[TDD][REFACTOR]`: refactor without behavior change; then re-run the same Verify Command used for the Scenario and confirm it still passes.
     - `[NON-TDD][DO]`: perform the described non-behavior change (docs-only/config-only (no behavior change)/generated outputs/formatting-renaming only).
     - `[NON-TDD][VERIFY]`: extract the command from the same line after `Verify:` and run it exactly.
   - Do not invent commands. If a VERIFY task does not contain an executable command after `Run:` or `Verify:`, STOP and ask the user.
   - Check off the task by changing it to `- [x] ...`.

Keep edits small and surgical.

## Validate
1. Run:
   - `openspec validate --all --json`
2. If errors exist:
   - Fix them.
   - Re-run `openspec validate --all --json`.
3. Warnings are informational; do not block unless they indicate a real defect.

## Minimal Output Contract
- Always show `Selected change: <change>`.
- If you need user input (e.g., selecting a change, unclear JSON fields), show only the minimal JSON needed.
- Report task progress if apply/status JSON provides it.
- Report validate summary:
  - valid/invalid counts
  - first few errors (if any)

## Common mistakes
- Using OpenSpec slash commands instead of `openspec` CLI.
- Starting implementation when `tasks` is missing/blocked (must send user to `/superspec-plan`).
- Checking off tasks without adding tests that cover delta spec scenarios.
- Running `openspec validate` without `--json` and losing actionable error details.
