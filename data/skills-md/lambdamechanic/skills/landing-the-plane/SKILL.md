---
name: landing-the-plane
description: Checklist for finishing work, pushing a branch, and opening a ready-for-review PR with tests and tracker updates.
---

# Landing the Plane

When someone asks you to "land the plane", they want you to wrap up the current body of work cleanly—no loose ends, no hidden surprises. Use this checklist any time that phrase shows up.

> **Non-negotiable:** landing the plane always ends with a pushed branch and an open (non-draft) pull request. Even if the work started on `main`, cut a feature branch, push it, create the PR, and flip it out of draft before you check this box.

## 1. Quality Gates
- Run the full automated test suite plus linters/formatters that the project relies on *in the feature branch you’ll merge*.
- Confirm that the code you wrote is covered by automated tests; add or expand tests if any path would otherwise go unverified.
- When a review uncovers a bug/regression, follow this micro-loop before touching the fix:
  1. **Write (or extend) a failing test** that reproduces the issue. Default to a generative `proptest!` so the failing input can shrink and be re-run later.
  2. Run the pre-commit suite, commit that red test by itself, and push so the failing state is visible on the PR/branch.
  3. Implement the fix in a separate commit, push it, and reply to the original feedback thread with the fixing commit hash/summary.
  4. Comment `@codex review` (or ping the human reviewer) to kick off the next review once the fix is in place.

### Transactional upgrades check (sticky failure prevention)

If the work touches any multi-item “apply/upgrade” loop, add property/integration tests that prove these invariants:

- Atomicity on failure: if any target fails during the apply loop, previously processed targets are rolled back (or the lockfile is advanced in step with on-disk changes). The repository must never land in a state where on-disk contents and lockfile disagree, causing future runs to refuse to proceed.
- Lockfile sync: the lock is only written after all filesystem changes succeed; it always captures the exact commit SHA/digest that landed so later upgrades/status checks have an immutable reference point.
- Cross-device safety: staging/swap logic works when the install root lives on a different filesystem (e.g., rename EXDEV). Include a test that simulates cross-device behavior and asserts correctness.
- Symlink preservation: upgrades preserve symlinks inside upgraded trees (recreate symlinks on Unix; best-effort on Windows).

Reject “done” until these tests exist and pass on CI across all OS targets in the matrix.

## 2. Code & Repo Hygiene
- Strip out temporary logging, printlns, dbg! calls, feature flags, sleep statements, and other debug aids that should not ship.
- Remove throwaway files, scripts, or notes that were only needed during exploration.
- Remove untracked build artifacts, log files, or editor temp files that accidentally appeared. Ensure `.gitignore` is correct.

## 3. Git & Branch Workflow
- Check `git status -sb`, `git stash list`, and `git branch --merged` to ensure there are no forgotten stashes or half-merged branches related to the work.
- Rebase the feature branch on the latest `main` (or `git pull --rebase`) so the PR is merge-ready.
- Squash or reorder commits into one or more coherent changesets with descriptive messages.
- Push the branch to GitHub and open a PR via `gh pr create` with an informative title/body summarizing the change, testing, and linked bd issues. Landing the plane is **not complete** until a ready-for-review PR exists (even if you iterated on `main`, create a branch at the end and push that history), but usually we will have created a draft PR already.
- If the PR started as a draft, convert it to "Ready for review" as part of this step so reviewers can pick it up immediately.
- Preferred helper command to flip to ready:
  ```bash
  scripts/pr-ready.sh
  ```
  Or via GitHub CLI directly: `gh pr ready`.
- Once the PR is ready, comment `@codex review` to trigger the automated review. If Codex leaves feedback, address every comment, push the fixes, **reply directly on each feedback thread with the commit hash (or summary) that resolves it**, and comment `@codex review` again until Codex reports no remaining issues.
 - Before asking for final review, check for any unresolved Codex inline threads without a human reply:
   ```bash
   scripts/codex-unreplied.sh [<pr-number>]
   ```
   Reply inline or resolve threads, then re-run to ensure it prints nothing.

### Codex Review Trigger (exact string)

- To request a Codex review, your PR comment must contain exactly: `@codex review`.
- Put it in its own comment (not just the PR body) so the trigger is reliably detected.
- Finish any `bd update` calls (notes/status changes) **before** your final commit/push so `.beads/issues.jsonl` in the PR matches the tracker state.

## 4. Tracking & Documentation
- Update/close beads issues and GitHub tickets linked to the work, ensuring status, notes, and acceptance criteria are satisfied.
- Refresh any affected docs (README, QUICKSTART, ADRs, runbooks) so they reflect the new reality.

## 5. Final QA & Communication
- Re-run the tests one last time after the final rebase.
- Post the PR link + testing summary back into bd, commit and push so it's persisted.
- Run `GH_WAIT_INTERVAL=15 ./scripts/gh-wait-for-merge.py --interval 15` (or similar) at the end. Let it surface any failing checks, fixing issues one-by-one until it exits cleanly. Only stop the script early if you have approval to hand off unresolved failures.
- Verify CI is green. If it fails, fix or document the failure reason before claiming you’ve landed the plane.
- Double-check for leftover git stashes, unpushed commits, or edge cases noted earlier.
- Comment "@codex review" on the PR with `gh` when you think you're done; it's not fully done until the reviewer reports no issues found.
- When you report back (to the user, bd, etc.), include a direct URL to the PR (full https://github.com/... link). Do not use only an abbreviation like `#123`.

Working through this list ensures the feature is truly finished, both trackers agree, and reviewers have a clear, reproducible artifact to look at.
