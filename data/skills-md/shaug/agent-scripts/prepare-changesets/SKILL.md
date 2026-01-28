---
name: prepare-changesets
description: >-
  GitHub-specific workflow to recompose a large, review-ready source branch
  into an ordered chain of smaller changesets (stacked branches + GitHub PRs)
  that preserve behavior and improve reviewability. Use when working with
  GitHub PR stacks via the gh CLI to split monolithic branches, create stacked
  PRs, merge reviewed changesets, and propagate/update downstream PR bases after
  merges.
compatibility: >-
  Requires Git and the GitHub CLI (gh) authenticated to a GitHub repo, plus
  network access to GitHub for PR creation, merging, and base updates.
license: MIT
metadata:
  provider: github
  vcs: git
  pr_cli: gh
  workflow: stacked-prs
  phase_model: two-phase-incremental
  plan_file: .prepare-changesets/plan.json
  dry_run_default: 'true'
---

# Prepare Changesets

Follow the spec and keep the source branch immutable. Use an incremental,
append-only planning approach: propose the next changeset, validate it, then
append the plan.

Always load:

- `references/SPEC.md`
- `references/PLAN_SCHEMA.md`

Use deterministic helpers:

- `scripts/preflight.py`
- `scripts/squash_ref.py`
- `scripts/init_plan.py`
- `scripts/validate.py`
- `scripts/status.py`
- `scripts/create_chain.py`
- `scripts/compare.py`
- `scripts/squash_check.py`
- `scripts/validate_chain.py`
- `scripts/hunk_preview.py`
- `scripts/run.py`
- `scripts/pr_create.py`
- `scripts/merge_propagate.py`
- `scripts/propagate.py`
- `scripts/push_chain.py`
- `scripts/db_compare.py`

## Phase 0: Preflight

Require a clean working tree and valid base/source branches. Treat the source
branch as immutable reference state. Never modify, rebase, or rewrite it as part
of this process. Preflight simulates merging the source into the base on a
temporary branch and runs the test command on the source branch. The source
branch must include the current base HEAD; if it is behind, stop unless the user
explicitly approves proceeding.

Resolve the test command in this order:

- Prefer the repository’s root `AGENTS.md` if it specifies a test command.
- If missing, unclear, or ambiguous, ask once.
- If still unknown, proceed with `--skip-tests` and record that explicitly in
  the plan.

When discovery is unclear, suggest likely commands by inspecting `.github`
workflows, `pyproject.toml`, `package.json` scripts, `justfile`, `Makefile`, and
other standard project entrypoints.

Run:

```bash
skills/prepare-changesets/scripts/preflight.py \
  --base main \
  --source feature/my-large-branch
```

To override the source-behind-base gate (not recommended):

```bash
skills/prepare-changesets/scripts/preflight.py \
  --base main \
  --source feature/my-large-branch \
  --allow-source-behind-base
```

If a specific test command is known or provided by the user, pass it with
`--test-cmd "<repo-specific test command>"`.

Create a local squashed reference for cleaner comparisons:

```bash
skills/prepare-changesets/scripts/squash_ref.py \
  --base main \
  --source feature/my-large-branch
```

This creates `<source-branch>-squashed`. Never push it.

If the squashed branch already exists, ask whether to reuse it. If the user
declines reuse, stop. If reuse is approved, re-run with `--reuse-existing`. If
it must be rebuilt, re-run with `--recreate`.

For a guided end-to-end starter:

```bash
skills/prepare-changesets/scripts/run.py \
  --base main \
  --source feature/my-large-branch \
  --title "My feature title"
```

## Phase 1: Incremental Decompose And Validate

Phase 1 is incremental and append-only. It is valid to propose the next
changeset, create it, validate it, and append the plan in cycles.

1. Inspect the change surface.

Use:

```bash
git diff --stat main..feature/my-large-branch
git diff --name-status main..feature/my-large-branch
```

Use `rg` to find refactors, renames, and flaggable boundaries. Focus on semantic
and conceptual boundaries of change, not just file counts or diff size.

2. Propose an ordered changeset chain.

Honor the decomposition preferences in `references/SPEC.md`, especially:

- separate renames from behavioral changes
- prefer additive-first changesets
- defer user-visible or API-exposed changes
- keep intent cohesive
- do not propose changesets that require future changesets to be partially
  present in order to be understandable or reviewable
- prefer rename-first changesets when they reduce diff noise or stabilize paths

Optimize for reviewer cognitive load (explicit guardrails). These are
rules-of-thumb; ask the user up front whether to accept them or adjust the
thresholds (or replace them with a different litmus, such as strict subsystem
separation).

- Target size: ~200–400 lines of *actual code changes* is the sweet spot for a
  30-minute review. If a changeset exceeds ~800 lines total (including tests and
  docs), split it unless the user explicitly approves the size.
- If a changeset spans multiple subsystems (for example: activities + workflows
  - worker wiring), split by subsystem even if the theme is coherent.
- Keep tests with their closest production changeset, but still split by
  subsystem so each PR has matching tests.
- If a reviewer could not reasonably review the diff in ~30 minutes, it is too
  large; split it.
- When a changeset violates any guardrail, stop and ask the user whether to
  exceed it, then record the approval.
- Exception: allow very large *purely mechanical* changesets (for example, a
  function rename applied uniformly or a global reformat), but only when the
  changeset is exclusively mechanical and clearly documented with guidance for
  spot checks or verification. Do not mix mechanical changes with behavioral
  changes in the same PR.

3. Initialize the plan.

Create a plan template:

```bash
skills/prepare-changesets/scripts/init_plan.py \
  --base main \
  --source feature/my-large-branch \
  --title "My feature title" \
  --changesets 4
```

Then edit `.prepare-changesets/plan.json`. The plan is append-only:

- define cohesive `slug` and `description` per changeset
- choose a `mode` per changeset: `paths`, `patch`, or `hunks`
- for `paths`, use `include_paths` to pull in relevant files
- for `hunks`, use `hunk_selectors` with `file` + `contains`/`range`
- use `all: true` in a selector to include all hunks in a file
- set `allow_partial_files=false` when a file must be fully included
- for `patch`, set `patch_file` under `.prepare-changesets/patches/`
- use `exclude_paths` as a coarse filter to prevent accidental overlap
- document scaffolding, flags, and intentional incompleteness in `pr_notes`
- append new changesets at the end as you learn more
- do not renumber or reorder validated changesets

Validate:

```bash
skills/prepare-changesets/scripts/validate.py
```

For stricter checks (ambiguous selectors, missing patch files, placeholders):

```bash
skills/prepare-changesets/scripts/validate.py --strict
```

`--strict` also warns if `.prepare-changesets/state.json` indicates prior
changeset branch heads have drifted. It runs patch/hunk apply checks on a
temporary branch, so the working tree must be clean.

After a changeset is validated and accepted, treat it as locked. Do not revise,
reinterpret, or reorder earlier validated changesets without explicit user
approval.

4. Create or extend the branch chain.

```bash
skills/prepare-changesets/scripts/create_chain.py
```

Branch names are append-only:

- `<source-branch>-1`
- `<source-branch>-2`
- ...

`create_chain.py` is append-only. It reuses an existing prefix of changeset
branches and creates only the missing suffix. Delete a branch explicitly if it
must be recreated.

`create_chain.py` also records `.prepare-changesets/state.json` with source and
changeset branch heads for drift detection.

5. Validate equivalence and progress.

```bash
skills/prepare-changesets/scripts/compare.py
skills/prepare-changesets/scripts/squash_check.py
```

`compare.py` checks equivalence by merging the chain. `squash_check.py` rebases
the squashed reference onto the chain tip using a temporary branch
`pcs-temp-squash-check-*` to show what remains.

To preview candidate hunks for selectors:

```bash
skills/prepare-changesets/scripts/hunk_preview.py --file path/to/file.ts
```

6. Review each changeset branch.

For each changeset branch:

- review the diff relative to its intended base
- run repo-specific tests when practical
- adjust commits to keep the changeset cohesive

7. Validate incremental mergeability.

Run tests after each changeset merge:

```bash
skills/prepare-changesets/scripts/validate_chain.py --test-cmd "<repo-specific test command>"
```

To run skill unit tests locally:

```bash
python3 -m unittest discover -s skills/prepare-changesets/scripts/tests -p 'test_*.py'
```

8. Open stacked PRs with correct bases.

Before opening PRs, ensure the changeset branches are pushed to the remote. If
the branches are not pushed, `gh pr create` fails with “Head sha can’t be blank”
or “Head ref must be a branch.”

Push the chain (defaults to `origin`):

```bash
skills/prepare-changesets/scripts/push_chain.py
```

Base rules:

- changeset 1 base: `base_branch`
- changeset i>1 base: previous changeset branch

Title rule:

- `<feature_title> (i of N)`
- `N` is derived from the current plan length at PR creation time

Body requirements:

- summarize the overall feature first
- explain what this changeset provides
- call out temporary scaffolding, flags, and intentional incompleteness
- document intent, scope, and temporary compromises only
- do not use PR bodies for marketing, justification, or speculative discussion

If a changeset is primarily renames, add a PR note:

- rename-only / mechanical; no behavior change intended

If a changeset mixes renames and behavior, add a PR note:

- includes rename(s) X → Y plus minimal behavior changes needed to keep the code
  coherent

Use the helper to generate `gh` commands and PR bodies:

```bash
skills/prepare-changesets/scripts/pr_create.py
```

This uses `gh pr create` under the hood and defaults to dry-run. Execute for
real:

```bash
skills/prepare-changesets/scripts/pr_create.py --no-dry-run
```

If `gh` is not authenticated, run `gh auth login` once, then retry.

## Phase 2: Merge And Propagate

Merge in order and propagate forward. Do not renumber or reorder validated
changesets.

Use one of these explicit workflows.

1. Merge a reviewed changeset PR, then propagate and update PR bases.

Dry-run first:

```bash
skills/prepare-changesets/scripts/merge_propagate.py --index i
```

Execute for real:

```bash
skills/prepare-changesets/scripts/merge_propagate.py --index i --no-dry-run
```

By default, the merge uses the repository's default method. Pass
`--method merge|squash|rebase` to override.

If the default merge method cannot be determined (for example, gh cannot read
repo settings), ask the user which merge method to use and re-run with
`--method`.

2. If the PR was merged separately, propagate and clean up downstream PRs.

If you have already synced the local base branch to include the merged
changeset, skip the local merge simulation:

```bash
skills/prepare-changesets/scripts/propagate.py \
  --merged-index i \
  --skip-local-merge \
  --no-dry-run
```

By default, propagation updates downstream PR bases with `gh pr edit --base`.
Disable that with `--no-update-pr-bases`. Add `--push` to push updated branches
with `--force-with-lease` (remote defaults to `origin`).

Propagation strategy:

- `--strategy rebase` (default) rewrites downstream history by rebasing onto the
  new base.
- `--strategy cherry-pick` preserves downstream history and applies the merged
  changeset commits onto each downstream branch. Each downstream branch
  cherry-picks from the original merged changeset branch (not from another
  downstream branch), so conflict resolutions do not cascade.

## Operational Notes

- Prefer explicit plan edits over clever automation.
- Keep `.prepare-changesets/` ignored in the repo (add it to `.gitignore` or
  `.git/info/exclude`); preflight stops unless you override with
  `--allow-recordkeeping-tracked`.
- Keep `.prepare-changesets/plan.json` out of PRs.
- Use the script for mechanical steps and Git for judgment calls.
- For database migrations, follow the validation guidance in
  `references/SPEC.md`.
- Use `db-compare` to run schema dump commands on the source branch and the
  fully merged chain, then diff the outputs.
- If judgment or new information conflicts with the validated plan, stop and
  escalate rather than improvising.
