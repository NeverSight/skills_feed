---
name: forge-address-pr-feedback
description: Analyze and address unresolved feedback on a GitHub pull request. Use when the user has received PR review comments and wants to systematically address each piece of feedback, or when the user mentions PR feedback, review comments, or addressing reviewer concerns.
disable-model-invocation: true
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
---

# Address PR Feedback

Analyze and address unresolved feedback on a GitHub pull request.

## Input

The PR number or URL will be provided as: $ARGUMENTS

If no argument is provided, detect the PR from the current branch using `gh pr view --json number`.

## Process

### Step 1: Fetch PR Information and Unresolved Threads

**IMPORTANT**: Use the GraphQL API to get review threads with resolution status. The REST API does NOT provide `isResolved` status.

```bash
# Get PR number and repo info
gh pr view <PR_NUMBER> --json number,title,headRefName,url

# CRITICAL: Use GraphQL to get ALL review threads with resolution status
gh api graphql -f query='
query {
  repository(owner: "<OWNER>", name: "<REPO>") {
    pullRequest(number: <PR_NUMBER>) {
      reviewThreads(first: 100) {
        nodes {
          isResolved
          isOutdated
          path
          line
          id
          comments(first: 10) {
            nodes {
              id
              body
              author {
                login
              }
              url
            }
          }
        }
      }
    }
  }
}'
```

Filter the results to get only unresolved threads:
```bash
# Get unresolved threads with full context
gh api graphql -f query='...' --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved == false)'
```

### Step 2: Process Each Unresolved Thread

For EACH unresolved thread:
1. Read the thread ID, file path, line number, and all comments
2. Read the relevant file and surrounding context
3. Understand what change is being requested
4. Categorize the feedback:
   - **Actionable**: Code change, fix, or improvement needed
   - **Question**: Clarification needed - respond with explanation
   - **Discussion**: Opinion/preference - assess if change improves code
   - **Already addressed**: Change was made but thread not resolved
   - **Won't fix**: Explain why the current approach is preferred
   - **Follow-up issue**: Valid improvement but out of scope - create linked issue

### Step 3: Address and Reply to Each Thread INDIVIDUALLY

**CRITICAL: Reply to each thread IMMEDIATELY after addressing it. Do NOT batch responses into a single collective comment.**

For each unresolved thread, in order:

1. **Make the change** (if actionable):
   - Read the file(s) that need changes
   - Make the requested changes using Edit tool
   - Run the project's lint/format/check commands (see CLAUDE.md or package.json for scripts)

2. **Commit the change** (if code was modified):
   ```bash
   git add <files>
   git commit -m "fix: Address PR feedback - <brief description>"
   ```

3. **Reply DIRECTLY to that specific thread** using GraphQL:
   ```bash
   # Reply to a review thread (NOT a PR comment!)
   gh api graphql -f query='
   mutation {
     addPullRequestReviewThreadReply(input: {
       pullRequestReviewThreadId: "<THREAD_ID>"
       body: "<response>"
     }) {
       comment {
         id
       }
     }
   }'
   ```

   **Alternative using REST API** (reply to the first comment in the thread):
   ```bash
   gh api repos/{owner}/{repo}/pulls/<PR_NUMBER>/comments/<COMMENT_ID>/replies \
     -X POST \
     -f body="<response>"
   ```

4. **Move to the next thread** and repeat

### Step 4: Response Format for Thread Replies

Reply format based on category:
- **Actionable**: "Fixed in commit `<sha>`. <brief explanation of the change>"
- **Question**: "<answer to the question with code references if helpful>"
- **Discussion**: "Good point. <explanation of decision - either made the change or explained why not>"
- **Already addressed**: "This was addressed in commit `<sha>`. <brief explanation>"
- **Won't fix**: "Keeping the current approach because <reason>. Happy to discuss further."
- **Follow-up issue**: "Created #<issue_number> to track this. <brief explanation of why it's out of scope>"

### Step 5: Create Follow-up Issues (When Needed)

If feedback identifies valid improvements that are out of scope for this PR:

```bash
gh issue create \
  --title "<concise description of the follow-up work>" \
  --body "## Context

This issue was identified during PR review of #<PR_NUMBER>.

## Original Feedback

> <quote the reviewer's comment>

## Proposed Solution

<brief description of what should be done>

## Related

- PR: #<PR_NUMBER>
- Review comment: <link to the comment>"
```

### Step 6: Push All Changes

After all threads are addressed:
```bash
git push
```

### Step 7: Summary

Provide a summary of actions taken:
- Number of feedback items addressed
- Commits created (list each)
- Follow-up issues created (with links)
- Any items that need human review or decision

## Important Guidelines

1. **Use GraphQL for thread discovery**: The REST API (`/pulls/{}/comments`) does NOT show resolution status. Always use the GraphQL query to find unresolved threads.

2. **Reply to threads individually**:
   - DO NOT post one collective comment addressing all feedback
   - DO reply directly to each thread as you address it
   - This keeps discussions organized and allows threads to be resolved

3. **Reply immediately after addressing**: Don't wait until the end to reply. Address thread → reply → move to next thread.

4. **Be thorough**: Address ALL unresolved feedback, don't skip items

5. **Be specific**: Reference exact commits, line numbers, and code in responses

6. **Test changes**: Run checks and tests before committing

7. **Granular commits**: One commit per logical change for easy review

8. **Create follow-up issues**: When valid feedback is out of scope, create a linked issue rather than ignoring or scope-creeping the PR

## Example Workflow

```
1. Fetch unresolved threads via GraphQL
2. For thread about "missing null check" in file.ts:149:
   a. Read file.ts
   b. Add null check
   c. Run format/check
   d. Commit: "fix: Add null check for edge case"
   e. Reply to thread: "Fixed in commit `abc123`. Added null check."
3. For thread asking "why use X instead of Y?":
   a. Reply to thread: "Using X because <reason>. Y would require <tradeoff>."
4. For thread about "add tests":
   a. Create issue #123 for test coverage
   b. Reply to thread: "Created #123 to track this - out of scope for this PR."
5. Push all commits
6. Summarize actions taken
```

## Related Skills

**Before:** Use `forge-reflect-pr` to self-review before requesting review.
**After merging:** Use `forge-update-changelog` to document user-facing changes.
**Full workflow:** `forge-setup-project` → `forge-create-issue` → `forge-implement-issue` → `forge-reflect-pr` → `forge-address-pr-feedback` → `forge-update-changelog`

## Example Usage

```
/forge-address-pr-feedback 123
/forge-address-pr-feedback https://github.com/owner/repo/pull/123
/forge-address-pr-feedback  # Uses current branch's PR
```
