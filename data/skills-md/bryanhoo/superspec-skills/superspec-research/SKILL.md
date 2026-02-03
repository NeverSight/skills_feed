---
name: superspec-research
description: Use when the user needs proposal/specs research artifacts produced for a Superspec (superspec-rpi) OpenSpec change.
user-invocable: true
---

# Superspec Research

## Rules (non-negotiable)
- Drive OpenSpec via CLI only (NO OpenSpec slash commands; i.e., commands starting with `/opsx` or `/openspec`).
- Prefer JSON output for every OpenSpec call that supports it (use `--json`).
  - If a required command does not support `--json` (e.g., `openspec new change`), run it without `--json` and continue with the next JSON-capable command (typically `openspec status --change <change> --json`).
- Keep changes scoped to `proposal` and `specs` artifacts only.
- If `proposal` is not complete, run the brainstorming prelude before writing `proposal.md` (see `skills/superspec-brainstorm/SKILL.md`).

## Change Selection
1. If the user provides a change name, use it as `<change>`.
2. Else run:
   - `openspec list --json`
   Ask the user to confirm/select a change name from the JSON output.
3. If there are no changes (or user wants a new one), ask for:
   - change name (kebab-case)
   - one-sentence description
   Then run:
   - `openspec new change <change> --schema superspec-rpi --description "<description>"`

Always print:
- `Selected change: <change>`

## Artifact Loop (proposal + specs)
Repeat until BOTH `proposal` and `specs` are complete.

### 0. Inspect status
Run:
- `openspec status --change <change> --json`

Parse the JSON to determine, for artifacts `proposal` and `specs`:
- whether each is `ready` vs `complete`
- whether `specs` is blocked by missing `proposal`

If the JSON schema is unclear, show the JSON and ask the user what the status fields mean; do not guess.

### 1. Blocked behavior
If `specs` is blocked by missing `proposal`, create `proposal` first (even if `specs` looks ready).

### 1.5 Brainstorming prelude (proposal inputs)
If `proposal` is ready (and not complete), do a short clarification pass BEFORE writing files:
- Follow `skills/superspec-brainstorm/SKILL.md` as a subroutine.
- Do NOT run `openspec` during brainstorming.
- Do NOT write or modify any files during brainstorming.
- Keep a "Brainstorming Notes" block as working notes.

Exit brainstorming when:
- You have concrete bullets for intent, background, in-scope, out-of-scope, constraints, affected specs, and success criteria.
- Affected Specs names are decided (kebab-case), because they drive `specs/<kebab-name>/spec.md`.

Then proceed to create/update `proposal.md` using OpenSpec instructions, using the notes to fill the template precisely.

If you believe you already know all the answers, you still MUST produce the "Brainstorming Notes" block before writing `proposal.md`.

### 2. Create/Update proposal
If `proposal` is ready (and not complete):
1. Run:
   - `openspec instructions proposal --change <change> --json`
2. From the JSON, extract at minimum:
   - `outputPath` (where to write)
   - `template` and/or `instruction` content
3. Write the proposal content to the concrete `outputPath` (typically `proposal.md`).

If `outputPath` is not a concrete file path (unexpected), STOP and show the full JSON.

Proposal must be concise and must include a filled "Affected Specs" section (it drives specs file creation).

After writing, print:
- `Wrote proposal: <outputPath>`

### 3. Create/Update specs
If `specs` is ready (and not complete):
1. Run:
   - `openspec instructions specs --change <change> --json`
2. Read dependencies from the JSON (e.g., `requires`) and ensure proposal exists; if not, go create proposal.
3. Treat `outputPath` patterns like `specs/**/spec.md` as a hint ONLY. Do not write wildcard paths.
4. Determine concrete spec files from the proposal "Affected Specs".

Create one delta spec per affected capability (new/modified/removed), at:
- `specs/<kebab-name>/spec.md`

Each delta spec MUST:
- Be a delta (changes only), structured into:
  - `## ADDED Requirements`
  - `## MODIFIED Requirements`
  - `## REMOVED Requirements`
- Use normative language per requirement (MUST/SHALL).
- For every ADDED/MODIFIED/REMOVED requirement, include Given/When/Then scenarios:
  - at least one happy path (if applicable)
  - at least one edge/failure case
  - every `#### Scenario:` MUST include a `##### Test Obligation` block with: `Type` (unit|integration|e2e), `Test File`, `Test Name`, `Verify Command`, `Expected (RED)`, and `Key Assertions`. If any field is missing, ask the user; do not guess.

After writing, print:
- `Wrote specs: <path1>[, <path2> ...]`

### 4. Re-check
After creating proposal or specs, re-run:
- `openspec status --change <change> --json`

Stop the loop only when both artifacts show complete.

## Minimal Output Contract
- Always show `Selected change: <change>`.
- For each artifact you write, show exactly which artifact and the concrete path(s).
- On any error, show the exact command that failed (including `--json`).

## Common mistakes
- Using OpenSpec slash commands (anything starting with `/opsx` or `/openspec`) instead of the `openspec` CLI.
- Treating wildcard `outputPath` (e.g., `specs/**/spec.md`) as a real file path; always write concrete files like `specs/<kebab-name>/spec.md`.
- Guessing `openspec` JSON fields instead of showing the JSON and asking the user.
