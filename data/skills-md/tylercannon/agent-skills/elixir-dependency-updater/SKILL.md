---
name: elixir-dependency-updater
description: Update Elixir project dependencies including breaking changes. Use when the user asks to update dependencies in an Elixir project, upgrade packages, run mix hex.outdated, handle dependency version bumps and breaking changes, or asks to update mix.exs dependencies.
---

# Update Elixir Dependencies (Strict Checklist)

This skill is intentionally written as a **no-skip** checklist. Agents must follow it exactly.

## Non-negotiables (DO NOT SKIP)

- You may update **all** dependencies marked "Update possible" **in a single batch**.
- Any dependency that is **blocked only by the project's `mix.exs` version constraint** is **NOT truly blocked**. It must be **moved into the update batch** by changing the constraint.
- **Review diffs individually** for each dependency being updated (even in a batch).
- After updating dependencies, run the verification gates:
  - `mix compile --warnings-as-errors` (must pass for both dev and test environments)
  - `mix format --check-formatted`
  - `mix test`
- If any gate fails: **STOP, fix, re-run the failing gate(s) until green, then continue.**
- Never "force" blocked updates caused by transitive constraints. Report them instead.

## Step 0: Identify candidates

Run:

- `mix hex.outdated`

Separate dependencies into two groups initially:

- **Update possible**: dependencies where `Latest > Current` and status shows "Update possible"
- **Update not possible**: dependencies showing "Update not possible"

Then, for each dependency in **Update not possible**, you MUST determine whether it is blocked by:

- the project's own `mix.exs` constraint (fixable), or
- transitive constraints (not fixable without larger coordination)

Do this classification with:

- `mix hex.outdated dep`

Re-classify **Update not possible** dependencies into:

- **Constraint-only blocked (treat as updatable)**: output indicates it is blocked by the project's version constraint in `mix.exs`
- **Transitively blocked (truly blocked)**: output indicates other deps/constraints prevent the update

## Step 1: Batch update all updatable dependencies

The batch list is:

- all **Update possible** deps, plus
- all **Constraint-only blocked (treat as updatable)** deps

### 1A) Review diffs for each dependency (required, do this BEFORE updating)

For each dependency `dep` in the batch list:

- Record `current_version` and `latest_version` from `mix hex.outdated`.
- Try: `mix hex.package diff dep current_version..latest_version`
- If the diff command fails, you must still assess changes by reviewing:
  - Hex package page release notes/changelog (or repository releases)
- While reviewing, specifically look for:
  - API changes (renames, arity changes, removed functions)
  - config changes (new required keys, renamed keys, default changes)
  - behavior changes (error/exception changes, validation changes, callback changes)
- Note any breaking changes that will require code/config updates.

### 1B) Update all constraints in mix.exs

- Edit `mix.exs` and update each dependency's version constraint to allow its `latest_version` (prefer pinning to the shown latest if feasible).
- This MUST include any deps previously reported as **blocked only by the project's `mix.exs` constraint**.

### 1C) Fetch and lock

- Run `mix deps.get` once to update the lock file for all dependencies.

### 1D) Apply required code changes

- Make code/config changes needed for each updated dependency based on the diffs reviewed in step 1A.

### 1E) Verification gates (MUST be green before continuing)

Run in order:

1. `mix compile --warnings-as-errors` (dev environment)
2. `MIX_ENV=test mix compile --warnings-as-errors` (test environment)
3. `mix format --check-formatted`
4. `mix test`

If any step fails: **STOP**, fix the cause, then re-run from the failing step onward until all steps are green.

## Step 2: Handle blocked dependencies

For any dependency classified as **Transitively blocked (truly blocked)**:

- Do not force. Report:
  - dependency name + latest version
  - which dependency is blocking it
  - the exact conflicting version requirement/constraint

## Step 3: Final confirmation and report

Run:

- `mix hex.outdated` (confirm expected updates/blocks)

Then output a short report:

- **Updated**
  - `dep`: `current` → `latest` (breaking: yes/no, notes if yes)
- **Code changes**
  - File-level bullets of what changed and why
- **Blocked**
  - `dep`: blocked by `blocker` (constraint summary)
- **Verification**
  - `mix compile --warnings-as-errors` (dev): pass/fail
  - `MIX_ENV=test mix compile --warnings-as-errors` (test): pass/fail
  - `mix check`: pass/fail
  - `mix test`: pass/fail
