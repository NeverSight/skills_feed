---
name: all-green
description: Addresses all PR review comments, resolves merge conflicts, and fixes failing CI checks to get the PR ready to merge. Use when the user wants to make their PR "all green" or ready for merge.
---

# All Green: Get PR Ready to Merge

Your goal is to get this PR to a mergeable state by addressing all blockers: review comments, merge conflicts, and failing checks.

## Workflow

Execute these steps in order:

### 1. Identify the PR

First, determine which PR to work on:

```bash
# Get current branch and find associated PR
gh pr view --json number,title,url,headRefName,baseRefName,mergeable,mergeStateStatus,reviewDecision
```

If no PR exists for the current branch, inform the user and stop.

### 2. Check PR Status

Gather the full picture of what needs to be addressed:

```bash
# Check for merge conflicts
gh pr view --json mergeable,mergeStateStatus

# Get CI check status
gh pr checks
```

### 3. Fetch and Address ALL Review Threads

**CRITICAL: You MUST fetch review threads using the GraphQL API and address every single unresolved one. This is NOT optional. Skipping this step is the #1 cause of PRs not being merge-ready.**

**Step 3a: Fetch all review threads (MANDATORY)**

```bash
gh api graphql -f query='
{
  repository(owner: "{owner}", name: "{repo}") {
    pullRequest(number: {pr_number}) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          comments(first: 5) {
            nodes { body path line author { login } }
          }
        }
      }
    }
  }
}'
```

Filter to unresolved threads: look for `"isResolved": false`. If there are zero unresolved threads, you can skip to step 4. Otherwise, you MUST address every single one.

**Step 3b: For EACH unresolved thread, do ALL of the following:**

1. **Read the comment** to understand what's being requested
2. **Read the relevant code** in the file/line mentioned
3. **Make the requested change** (or explain why not if you disagree)
4. **Reply to the thread** explaining what you did:
   ```bash
   gh api graphql -f query='
   mutation {
     addPullRequestReviewThreadReply(input: {
       pullRequestReviewThreadId: "PRRT_xxx"
       body: "Fixed in commit abc123"
     }) {
       comment { id }
     }
   }'
   ```
5. **Resolve the thread** — this is MANDATORY, do not skip:
   ```bash
   gh api graphql -f query='
   mutation {
     resolveReviewThread(input: {
       threadId: "PRRT_xxx"
     }) {
       thread { isResolved }
     }
   }'
   ```

**Step 3c: Verify all threads are resolved (MANDATORY)**

After addressing all threads, re-run the GraphQL query from step 3a and confirm zero unresolved threads remain. If any remain, go back and address them.

Tips:
- Address comments in file order to avoid line number shifts
- If a comment is unclear, ask the user for clarification
- If you disagree with a suggestion, explain why in your reply and still resolve the thread
- Always reply before resolving so reviewers can see what action was taken
- Commit and push your fixes before replying/resolving so you can reference the commit hash

### 4. Resolve Merge Conflicts

If the PR has merge conflicts:

```bash
# Fetch latest changes
git fetch origin

# Get the base branch name from PR
BASE_BRANCH=$(gh pr view --json baseRefName -q .baseRefName)

# Rebase onto the base branch
git rebase origin/$BASE_BRANCH
```

When resolving conflicts:
- **Read both versions** carefully to understand the intent
- **Preserve both changes** when they're independent
- **Choose the correct version** when they conflict
- **Run type checking** after resolving to catch issues

```bash
# After resolving conflicts
git add <resolved-files>
git rebase --continue

# Verify types still check
npm run tsgo:check
```

### 5. Fix Failing Checks

For each failing check:

```bash
# Get detailed check failure information
gh pr checks --json name,state,conclusion,detailsUrl
```

Common fixes:

**Type errors:**
```bash
npm run tsgo:check  # Identify the errors
# Fix each type error in the reported files
```

**Lint errors:**
```bash
npm run lint        # See lint issues
npm run lint:fix    # Auto-fix what's possible
# Manually fix remaining issues
```

**Test failures:**
```bash
npm test            # Run tests to see failures
# Read failing test files and fix the issues
```

**Build failures:**
- Check for missing imports
- Check for syntax errors
- Verify all dependencies are installed

### 6. Push and Wait for Checks

After all fixes:

```bash
# If you rebased, force push is required
git push --force-with-lease

# If you only added commits
git push
```

Then **wait for checks to complete** using the blocking watch command:

```bash
# Block until checks finish, exit immediately on first failure
gh pr checks --watch --fail-fast
```

This command:
- Blocks until all checks complete (no polling/tokens wasted)
- Exits immediately with status 1 if any check fails (fail-fast)
- Exits with status 0 if all checks pass
- Exits with status 8 if checks are still pending (shouldn't happen with --watch)

### 7. Handle Check Failures

If `gh pr checks --watch --fail-fast` exits with a failure:

```bash
# See which check failed and get the details URL
gh pr checks --json name,state,conclusion,detailsUrl

# View the failed run logs directly
gh run view <run-id> --log-failed
```

Fix the issue, commit, push, and run `gh pr checks --watch --fail-fast` again.

### 8. Verify Merge Readiness

Once checks pass:

```bash
gh pr view --json mergeable,mergeStateStatus,reviewDecision
```

## Important Notes

- **EVERY unresolved review thread must be addressed and resolved** — this is the most important part of getting a PR to green. Do not skip this step or treat it as optional. Always verify with a follow-up GraphQL query that zero unresolved threads remain.
- **Ask before force-pushing** if there might be other collaborators on the branch
- **Run type checking frequently** to catch issues early
- **Commit logically** - group related fixes together
- If checks keep failing after fixes, read the CI logs carefully:
  ```bash
  gh run view <run-id> --log-failed
  ```

## Example Session

```bash
# 1. See what we're dealing with
gh pr view --json number,title,mergeable,mergeStateStatus,reviewDecision
gh pr checks

# 2. MANDATORY: Fetch ALL review threads and find unresolved ones
gh api graphql -f query='{
  repository(owner: "OWNER", name: "REPO") {
    pullRequest(number: PR_NUM) {
      reviewThreads(first: 100) {
        nodes { id isResolved comments(first: 5) { nodes { body path line author { login } } } }
      }
    }
  }
}'

# 3. Address each unresolved thread: read code, make fix, commit

# 4. Push fixes
git push

# 5. Reply to and resolve EVERY addressed thread
gh api graphql -f query='mutation { addPullRequestReviewThreadReply(input: { pullRequestReviewThreadId: "PRRT_xxx", body: "Fixed in abc123 — added encodeURIComponent" }) { comment { id } } }'
gh api graphql -f query='mutation { resolveReviewThread(input: { threadId: "PRRT_xxx" }) { thread { isResolved } } }'

# 6. VERIFY: Re-fetch threads and confirm zero unresolved remain
# (Re-run the GraphQL query from step 2, filter for isResolved: false)

# 7. If there are merge conflicts, rebase
git fetch origin
git rebase origin/main
# ... resolve conflicts ...
git add .
git rebase --continue

# 8. Fix any failing checks
npm run tsgo:check
npm run lint:fix
npm test

# 9. Push and wait for checks (blocks until complete, fails fast)
git push --force-with-lease
gh pr checks --watch --fail-fast

# 10. If checks failed, fix and repeat. Once green:
gh pr view --json mergeable,mergeStateStatus,reviewDecision
```
