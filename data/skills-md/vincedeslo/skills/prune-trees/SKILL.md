---
name: prune-trees
description: Remove worktrees already merged into the default branch across every repository under ~/repos/personal and ~/repos/work, using worktrunk (wt) to discover repositories and `wt step prune` to remove them. Previews the removals as one table, waits for approval, then reports what it cleaned up. Use when asked to prune, clean up, clear out, or garbage-collect old, stale, or merged worktrees, or when the user says "prune-trees".
compatibility: Requires bash, worktrunk (`wt`, https://worktrunk.dev) with the experimental `wt step prune` command, jq, git, and checkout roots at ~/repos/personal and ~/repos/work.
---

# prune-trees

Walk every repository under `~/repos/personal` and `~/repos/work` and remove the worktrees whose branches are already integrated into the default branch. Worktrunk is the source of truth for repository and worktree structure, and `wt step prune` performs every removal.

## When to use

The user asks to prune, clean up, clear out, or garbage-collect old, stale, or merged worktrees — personal, work, or both — or says "prune-trees".

## Instructions

1. **Preview first.** Run the walker from this skill directory with no flags; it removes nothing:

   ```bash
   scripts/prune-trees.sh
   ```

   With no arguments it scans `~/repos/personal` and `~/repos/work`. Pass roots as arguments to narrow the scan — `scripts/prune-trees.sh ~/repos/work` for work only.

2. **Show the single table** the script prints — one row per candidate, every repository in the same table — plus the summary counts. Do not split it per root.

3. **Ask for approval.** Removal is destructive, so name the count of worktrees and branches and wait for an explicit yes. Never skip to step 4 on the same turn as step 1.

4. **Apply**, re-using the same roots and `--min-age` as the preview:

   ```bash
   scripts/prune-trees.sh --apply
   ```

5. **Report the result table**, again as a single table, with the summary counts. Name every `failed` and `skipped` row and its detail. Do not retry a failure with `--force`, `-D`, or `git worktree remove`; report and stop.

## Options

| Flag | Effect |
| --- | --- |
| *(none)* | Preview. Runs `wt step prune --dry-run`; nothing is removed. |
| `--apply` | Performs the removals, in the foreground so every outcome is reported. |
| `--min-age <age>` | Skip worktrees younger than this. Worktrunk's default is `1d`. |
| `<root> ...` | Override the default roots. |

## What the script does

For each direct child directory of each root it runs:

```bash
wt -C <dir> --config-set list.json-schema=2 list --format json --no-progressive
```

and reads `items[].worktree.main` — the repository's main worktree. That is the repository identity, which collapses the `repo.branch` worktree siblings in a root into one entry per repository, so each repository is pruned once. A non-git directory makes `wt list` exit non-zero and is skipped.

Then, per repository:

```bash
wt -C <main-worktree> step prune --format json [--dry-run | --foreground] [--min-age <age>]
```

`wt step prune` decides what qualifies, using the same six integration checks as `wt remove` (same commit, ancestor, no added changes, matching trees, merge adds nothing, patch-id match). The script never makes that judgement itself and never invokes `git worktree remove`.

Rows come from the JSON, whose fields differ by mode:

- `kind` — `worktree` for a worktree removal, `branch_only` for a merged branch with no worktree.
- `branch`, `path` — what was removed.
- dry run: `branch_deleted` (a prediction), plus `reason` and `target` — why the candidate qualifies and what it was measured against, rendered as the `DETAIL` column, e.g. `ancestor of master`.
- live run: `branch_outcome` — the executed outcome (`deleted`, `not_attempted`, `retained_unmerged`, `retained_checked_out`, `retained_raced`, `retained_failed`), and `branch_checked_out_at` when a sibling checkout blocked the branch delete.

Results per row: `would remove` / `would delete` in preview, `removed` / `deleted` / `skipped` / `failed` on apply. The summary counts worktrees, branches, clean repositories, skips and failures; the exit status is non-zero if any repository failed or a root is missing.

## Notes

- The script defaults to preview. `--apply` is the only way to remove anything, which is what keeps step 3's approval meaningful.
- `--foreground` is used on apply so the reported outcome is the real one. Without it worktrunk hands the branch delete to a detached process and reports `deferred`, which says nothing about whether the branch is gone.
- Worktrunk always skips locked worktrees and the main worktree, so a repository can never prune itself away.
- The min-age guard exists because a worktree just created from the default branch points at the same commit and so looks merged. Keep the default `1d` unless the user asks otherwise; `--min-age=0s` removes that protection.
- Unapproved project hooks are not auto-approved — the script passes no `--yes`, and such a candidate is skipped rather than run. Pre-approve with `wt config approvals add` if a repository needs it.
- Removals are sequential and each one prunes git metadata, so a root with many repositories takes time. Let it finish.
- Run `wtl` afterwards to inspect what remains.

## Edge cases

- **Unmerged worktree:** never a candidate. Worktrunk lists only integrated branches, so unmerged local work is never offered for removal.
- **Dirty merged worktree:** worktrunk decides; a candidate it declines is reported `skipped` with its reason. Do not force it.
- **Branch checked out in a sibling worktree:** the branch is retained whatever else happens, and the surviving checkout is named in `DETAIL`.
- **Branch-only candidate:** a merged branch with no worktree. Only the ref is deleted; nothing on disk changes.
- **Squash merge with hundreds of commits since the merge point:** falls outside worktrunk's default-branch walk cap and is not a candidate. It needs a deliberate `wt remove -D`, which is the user's call, not this skill's.
- **Missing root:** reported on stderr and counted as a failure; the other root is still scanned.
- **`wt` or `jq` missing from PATH:** the script exits before touching any repository.
