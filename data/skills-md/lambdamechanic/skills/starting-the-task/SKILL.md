---
name: starting-the-task
description: "A short checklist for kicking off work effectively: plan, branch, track with bd, and set up validation."
---

# Starting the Task

Use this checklist any time you begin work on a bd issue (or whenever the user says “start working on …”). It ensures the effort is grounded, observable, and reversible.

1. **Understand the Task**
   - Read the bd issue (and any linked discoveries or docs) end-to-end.
   - Confirm acceptance criteria, dependencies, and blockers. Ask clarifying questions before touching code.

2. **Environment Readiness**
   - Run `cargo test` (or the project’s canonical smoke suite) on `main` to ensure the baseline is green before you diverge.
   - If tests fail, stop and coordinate—don’t start stacking new work on a broken branch.

3. **Branch & Tracking**
   - Create a fresh branch for the effort, even if you expect a small change.
     ```bash
     git checkout -b <short-task-name>
     ```
   - `bd update <id> --status in_progress --notes "Starting work"` so the tracker reflects the new ownership/status.
   - If multiple repos are involved, repeat for each.

4. **Open a Draft PR (immediately)**
   - As soon as you create the branch, open a **draft PR** so CI runs and stakeholders can track progress. If a PR already exists for the parent effort, continue on that one.
   - Source the PR title/description from the bd issue: include its summary, acceptance criteria, and a link/reference to the bd id.
   - Preferred command (uses GitHub CLI):
     ```bash
     scripts/pr-draft.sh "<short title incl. bd id>" [body.md]
     ```
     Fallback: `gh pr create --draft --title "..." --body-file body.md` after `git push -u origin <branch>`.

5. **Sync & Tooling**
   - Ensure `git pull --rebase` (or equivalent) so you’re working from the latest remote `main`.
   - Verify `gh auth status` so PR creation won’t fail later.

6. **Plan Tests Early**
   - Decide how you’ll prove the change works (unit tests, integration, manual steps). Capture this in notes or the eventual PR description so reviewers know what to expect.

Only after these steps are complete should you begin coding. If circumstances prevent any step (e.g., CI down, baseline broken), note it explicitly in bd and get confirmation before proceeding.
