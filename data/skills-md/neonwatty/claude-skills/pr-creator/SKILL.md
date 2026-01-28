---
name: pr-creator
description: Creates a pull request from current changes, monitors GitHub CI, and debugs any failures until CI passes. Use this when the user says "create pr", "make a pr", "open pull request", "submit pr", or "pr for these changes". Does NOT merge - stops when CI passes and provides the PR link.
---

# PR Creator Skill

You are a developer preparing changes for review. Your job is to commit changes, create a PR, monitor CI, fix any failures, and notify the user when the PR is ready for merge.

## Task List Integration

**CRITICAL:** This skill uses Claude Code's task list system for progress tracking and session recovery. You MUST use TaskCreate, TaskUpdate, and TaskList tools throughout execution.

### Why Task Lists Matter Here
- **CI run tracking:** Each CI attempt becomes a task with pass/fail status
- **Fix iteration visibility:** User sees "CI Run #3: fixing lint errors"
- **Session recovery:** If interrupted during CI monitoring, resume watching the same run
- **Audit trail:** Track all fixes made across multiple CI iterations

### Task Hierarchy
```
[Main Task] "Create PR: [branch-name]"
  └── [CI Task] "CI Run #1" (status: failed, reason: lint errors)
      └── [Fix Task] "Fix: lint errors"
  └── [CI Task] "CI Run #2" (status: failed, reason: test failures)
      └── [Fix Task] "Fix: test failures"
  └── [CI Task] "CI Run #3" (status: passed)
```

### Session Recovery Check
**At the start of this skill, always check for existing tasks:**
```
1. Call TaskList to check for existing PR tasks
2. If a "Create PR" task exists with status in_progress:
   - Check its metadata for PR URL and current CI run ID
   - Resume monitoring that CI run
3. If CI tasks exist, check their status to understand current state
4. If no tasks exist, proceed with fresh execution
```

## Process

### Step 1: Check Git Status

**Create the main PR task:**
```
TaskCreate:
- subject: "Create PR: [branch-name or 'pending']"
- description: |
    Create pull request from current changes.
    Starting: git status check
- activeForm: "Checking git status"

TaskUpdate:
- taskId: [pr task ID]
- status: "in_progress"
```

Run these commands to understand the current state:

```bash
git status
git diff --stat
git log --oneline -5
```

**Verify before proceeding:**
- There are changes to commit (staged or unstaged)
- You're on a feature branch (not main/master) OR need to create one
- The branch is not already ahead with unpushed commits that have a PR

**If no changes exist:**
- Inform the user: "No changes detected. Nothing to commit."
- Mark task as completed with metadata indicating no changes
- Stop here.

**Update task with branch info:**
```
TaskUpdate:
- taskId: [pr task ID]
- subject: "Create PR: [actual-branch-name]"
- metadata: {"branch": "[branch-name]", "changesDetected": true}
```

### Step 2: Create Branch (if needed)

If currently on main/master:
```bash
git checkout -b <descriptive-branch-name>
```

Branch naming convention:
- `feat/short-description` for features
- `fix/short-description` for bug fixes
- `refactor/short-description` for refactoring
- `docs/short-description` for documentation

### Step 3: Stage and Commit Changes

```bash
# Stage all changes
git add -A

# Review what's staged
git diff --cached --stat

# Create commit with descriptive message
git commit -m "$(cat <<'EOF'
<type>: <short summary>

<optional longer description>
EOF
)"
```

**Commit message guidelines:**
- Use conventional commits: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`
- First line: 50 chars max, imperative mood
- Body: wrap at 72 chars, explain what and why

### Step 4: Push Branch

```bash
git push -u origin <branch-name>
```

### Step 5: Create Pull Request

```bash
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<1-3 bullet points describing what this PR does>

## Changes
<list of key changes>

## Test Plan
<how to verify this works>
EOF
)"
```

**Capture the PR URL** from the output and store in task metadata:
```
TaskUpdate:
- taskId: [pr task ID]
- metadata: {
    "prUrl": "https://github.com/owner/repo/pull/123",
    "prNumber": 123,
    "prTitle": "[title]",
    "commits": [count]
  }
```

### Step 6: Monitor CI

**Create a CI run task for tracking:**
```
TaskCreate:
- subject: "CI Run #[N]: monitoring"
- description: |
    Monitoring CI run for PR #[number]
    Run ID: [run-id]
    Started: [timestamp]
- activeForm: "Monitoring CI Run #[N]"

TaskUpdate:
- taskId: [ci task ID]
- addBlockedBy: [pr task ID]  # Links CI run to main PR task
- status: "in_progress"
```

Wait for CI to start, then monitor:

```bash
# List workflow runs for this PR
gh run list --branch <branch-name> --limit 5

# Watch a specific run (blocking)
gh run watch <run-id>

# Or check status without blocking
gh run view <run-id>
```

**Poll every 30-60 seconds** until CI completes.

**Store run ID in task for session recovery:**
```
TaskUpdate:
- taskId: [ci task ID]
- metadata: {"runId": "[run-id]", "status": "running"}
```

### Step 7: Handle CI Results

#### If CI Passes:

**Update CI task as passed:**
```
TaskUpdate:
- taskId: [ci task ID]
- subject: "CI Run #[N]: passed ✅"
- status: "completed"
- metadata: {"runId": "[run-id]", "status": "passed", "completedAt": "[timestamp]"}
```

**Update main PR task:**
```
TaskUpdate:
- taskId: [pr task ID]
- metadata: {"ciStatus": "passed", "ciRunCount": [N]}
```

- **STOP HERE** - do not merge
- Report to user:
  ```
  ✅ PR is ready for review!

  **PR:** <url>
  **Branch:** <branch-name>
  **CI Status:** All checks passed

  The PR is ready to be reviewed and merged.
  ```

#### If CI Fails:

**Update CI task as failed:**
```
TaskUpdate:
- taskId: [ci task ID]
- subject: "CI Run #[N]: failed ❌"
- status: "completed"
- metadata: {"runId": "[run-id]", "status": "failed", "failureReason": "[brief reason]"}
```

1. **Get failure details:**
   ```bash
   gh run view <run-id> --log-failed
   ```

2. **Analyze the failure:**
   - Identify which job/step failed
   - Read the error message
   - Determine the fix

3. **Create a fix task:**
   ```
   TaskCreate:
   - subject: "Fix: [failure reason]"
   - description: |
       Fixing CI failure from Run #[N]
       Failure: [detailed error]
       Files to modify: [list if known]
   - activeForm: "Fixing [failure reason]"

   TaskUpdate:
   - taskId: [fix task ID]
   - addBlockedBy: [ci task ID]  # Links fix to the failed CI run
   - status: "in_progress"
   ```

4. **Fix the issue:**
   - Make necessary code changes
   - Stage and commit the fix:
     ```bash
     git add -A
     git commit -m "fix: <what was fixed>"
     git push
     ```

5. **Mark fix task as completed:**
   ```
   TaskUpdate:
   - taskId: [fix task ID]
   - status: "completed"
   - metadata: {"filesModified": ["file1.ts", "file2.ts"], "commitHash": "[hash]"}
   ```

6. **Return to Step 6** - monitor the new CI run (increment run number)

**Repeat until CI passes.**

### Step 8: Final Report

**Mark main PR task as completed:**
```
TaskUpdate:
- taskId: [pr task ID]
- status: "completed"
- metadata: {
    "prUrl": "[url]",
    "prNumber": [number],
    "branch": "[branch-name]",
    "ciStatus": "passed",
    "ciRunCount": [N],
    "merged": false
  }
```

**Generate report from task data:**

Call `TaskList` to get all CI run and fix tasks, then generate the summary:

```markdown
## PR Ready for Review

**PR:** [#<number> <title>](<url>)
**Branch:** `<branch-name>` → `main`
**Commits:** <count>
**CI Status:** ✅ All checks passed

### Changes Included
- <change 1>
- <change 2>

### CI Runs
[Generated from CI run tasks:]
- Run #1: ❌ Failed (lint errors) → Fixed in commit [hash]
- Run #2: ❌ Failed (test failures) → Fixed in commit [hash]
- Run #3: ✅ Passed

### Fixes Applied
[Generated from fix tasks:]
- Fix: lint errors - modified [files]
- Fix: test failures - modified [files]

### Next Steps
1. Request review from team
2. Address any review feedback
3. Merge when approved

**Note:** This PR has NOT been merged. Please review and merge manually.
```

### Session Recovery

If resuming from an interrupted session:

**Recovery decision tree:**
```
TaskList shows:
├── PR task in_progress, no CI tasks
│   └── PR was created, start monitoring CI (Step 6)
├── PR task in_progress, CI task in_progress
│   └── Resume monitoring CI run from task metadata runId
├── PR task in_progress, CI task failed, no fix task
│   └── Analyze failure and create fix task (Step 7)
├── PR task in_progress, fix task in_progress
│   └── Continue fixing, then push and monitor new CI run
├── PR task completed
│   └── PR is done, show final report
└── No tasks exist
    └── Fresh start (Step 1)
```

**Resuming CI monitoring:**
```
1. Get runId from latest CI task metadata
2. Check if run is still active: gh run view <runId>
3. If still running, continue monitoring
4. If completed, process result (Step 7)
5. If new run started, create new CI task and monitor that
```

**Always inform user when resuming:**
```
Resuming PR creation session:
- PR: [url from task metadata]
- Branch: [branch from task metadata]
- CI Runs: [count] attempts
- Current state: [in_progress task description]
- Resuming: [next action]
```

## Important Rules

1. **NEVER merge the PR** - only create it and ensure CI passes
2. **NEVER force push** unless explicitly asked
3. **NEVER push to main/master directly**
4. **Continue fixing until CI passes** - don't give up after one failure
5. **Preserve commit history** - don't squash unless asked

## Error Handling

**Authentication issues:**
```bash
gh auth status
```
If not authenticated, inform user to run `gh auth login`.

**Branch conflicts:**
```bash
git fetch origin main
git rebase origin/main
# or
git merge origin/main
```
Resolve conflicts if any, then continue.

**PR already exists:**
```bash
gh pr view --web
```
Inform user a PR already exists for this branch.

## CI Debugging Tips

**Common failures and fixes:**

| Failure | Likely Cause | Fix |
|---------|--------------|-----|
| Lint errors | Code style violations | Run `npm run lint -- --fix` or equivalent |
| Type errors | TypeScript issues | Fix type annotations |
| Test failures | Broken tests | Fix tests or update snapshots |
| Build failures | Compilation errors | Fix syntax/import errors |
| Timeout | Slow tests | Optimize or increase timeout |

**Read the logs carefully** - the error message usually tells you exactly what's wrong.
