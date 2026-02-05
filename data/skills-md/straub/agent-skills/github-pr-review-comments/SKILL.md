---
name: github-pr-review-comments
description: Comprehensive workflow for managing GitHub PR review comments using gh CLI and GraphQL API. Use when asked to address review comments, find unreplied comments, reply to review threads, or resolve/unresolve review conversations. Supports finding ALL comments across pagination boundaries, replying to threads, and resolving conversations.
compatibility: Requires gh CLI installed and authenticated (gh auth login)
---

# GitHub PR Review Comments

This skill provides a comprehensive workflow for managing PR review comments using the `gh` CLI and GitHub's GraphQL API.

## When to Use This Skill

Use this skill when:
- Asked to address PR review comments
- Finding unreplied or unresolved review threads
- Replying to review comments
- Resolving or unresolving review threads
- Working with review threads programmatically (coding agents, automation)

## Finding All Review Comments (Reliable Method)

**CRITICAL**: PR review comments are paginated and span multiple review rounds. Simple queries will miss comments. Use this comparison approach:

### Step 1: Get ALL Original Comment IDs

```bash
gh api repos/{owner}/{repo}/pulls/{pr}/comments --paginate \
  --jq '[.[] | select(.in_reply_to_id == null)] | .[].id' \
  | sort -n > /tmp/all_original_comments.txt
```

This finds all "top-level" review comments (not replies).

### Step 2: Check Your Username

```bash
gh api user -q .login
```

### Step 3: Get ALL Comment IDs That Have Your Replies

```bash
gh api repos/{owner}/{repo}/pulls/{pr}/comments --paginate \
  --jq '[.[] | select(.user.login == "{your_username}" and .in_reply_to_id != null)] | .[].in_reply_to_id' \
  | sort -n > /tmp/replied_comments.txt
```

### Step 4: Find Unreplied Comments (Set Difference)

```bash
comm -23 /tmp/all_original_comments.txt /tmp/replied_comments.txt
```

This shows comment IDs that don't have your reply yet.

## Why Simple Approaches Fail

- **Time-based filtering** misses comments from earlier review rounds added to the same PR
- **Non-paginated queries** miss comments beyond the first page (typically 30-100 per page)
- **Counting reviews vs comments** is misleading - a single review can have many comments
- **The PR "comments" field** only shows issue-style comments, not review comments

## Getting Comment Details

Once you have unreplied comment IDs, get full details:

```bash
gh api repos/{owner}/{repo}/pulls/{pr}/comments --paginate \
  --jq '[.[] | select(.id == {id1} or .id == {id2})] | .[] | {id, path, line, body}'
```

Replace `{id1}`, `{id2}` with actual comment IDs.

## Replying to Review Comments

### Basic Reply to a Comment

```bash
gh api repos/{owner}/{repo}/pulls/{pr}/comments/{comment_id}/replies \
  -X POST -f body='Your response here'
```

### Response Format Best Practices

- Start with status emoji:
  - ✅ for addressed/fixed
  - 🔄 for acknowledged/will fix
  - 💭 for discussion/clarification needed
- Reference specific commits when fixes are made: `**FIXED** in commit abc1234`
- Be concise but clear about what action was taken
- Group related fixes into single commits with descriptive messages

### Example Responses

```bash
# Fixed issue
gh api repos/owner/repo/pulls/123/comments/456/replies \
  -X POST -f body='✅ **FIXED** in commit abc1234 - Refactored to use async/await pattern'

# Acknowledged
gh api repos/owner/repo/pulls/123/comments/789/replies \
  -X POST -f body='🔄 Good catch! Will fix in next commit'
```

## Working with Review Threads (GraphQL API)

The GitHub GraphQL API provides powerful capabilities for managing review threads.

### Fetch Unresolved Review Threads

```bash
gh api graphql -f query='
{
  repository(owner: "OWNER", name: "REPO") {
    pullRequest(number: PR_NUMBER) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          comments(first: 100) {
            nodes {
              id
              body
              author { login }
              path
              line
            }
          }
        }
      }
    }
  }
}'
```

### Reply to a Review Thread

Use the thread ID from `reviewThreads.nodes[].id` (format: `PRRT_kwDO...`), NOT the comment ID:

```bash
gh api graphql -f query='
mutation {
  addPullRequestReviewThreadReply(input: {
    pullRequestReviewThreadId: "PRRT_kwDO..."
    body: "Your reply here"
  }) {
    comment { id }
  }
}'
```

### Resolve a Review Thread

```bash
gh api graphql -f query='
mutation {
  resolveReviewThread(input: {threadId: "PRRT_kwDO..."}) {
    thread { id isResolved }
  }
}'
```

Thread IDs are in the `id` field of each thread node (format: `PRRT_kwDO...`).

### Unresolve a Review Thread

```bash
gh api graphql -f query='
mutation {
  unresolveReviewThread(input: {threadId: "PRRT_kwDO..."}) {
    thread { id isResolved }
  }
}'
```

## Workflow: Addressing All Review Comments

1. **Find unreplied comments** using the comparison method above
2. **Get comment details** for each unreplied comment
3. **Make necessary code changes** to address the feedback
4. **Commit changes** with descriptive messages
5. **Reply to each comment** with status and commit reference
6. **Resolve threads** when appropriate (only after fix is confirmed and pushed)

## Examples

### Example 1: Find and List All Unreplied Comments for PR #42

```bash
# Set variables
OWNER="myorg"
REPO="myrepo"
PR="42"

# Step 1: Get all original comment IDs
gh api repos/$OWNER/$REPO/pulls/$PR/comments --paginate \
  --jq '[.[] | select(.in_reply_to_id == null)] | .[].id' \
  | sort -n > /tmp/all_original_comments.txt

# Step 2: Get your username
USERNAME=$(gh api user -q .login)

# Step 3: Get comment IDs you've replied to
gh api repos/$OWNER/$REPO/pulls/$PR/comments --paginate \
  --jq "[.[] | select(.user.login == \"$USERNAME\" and .in_reply_to_id != null)] | .[].in_reply_to_id" \
  | sort -n > /tmp/replied_comments.txt

# Step 4: Find unreplied comment IDs
UNREPLIED=$(comm -23 /tmp/all_original_comments.txt /tmp/replied_comments.txt)

# Step 5: Get details for unreplied comments
for id in $UNREPLIED; do
  gh api repos/$OWNER/$REPO/pulls/$PR/comments --paginate \
    --jq "[.[] | select(.id == $id)] | .[] | {id, path, line, body, author: .user.login}"
done
```

### Example 2: Reply to Multiple Comments After Fix

```bash
OWNER="myorg"
REPO="myrepo"
PR="42"
COMMIT="abc1234"

# Reply to comment about async refactoring
gh api repos/$OWNER/$REPO/pulls/$PR/comments/111/replies \
  -X POST -f body="✅ **FIXED** in commit $COMMIT - Refactored to use async/await"

# Reply to comment about error handling
gh api repos/$OWNER/$REPO/pulls/$PR/comments/222/replies \
  -X POST -f body="✅ **FIXED** in commit $COMMIT - Added try/catch with proper error logging"
```

### Example 3: Get All Unresolved Threads and Reply

```bash
OWNER="myorg"
REPO="myrepo"
PR="42"

# Fetch unresolved threads
THREADS=$(gh api graphql -f query="
{
  repository(owner: \"$OWNER\", name: \"$REPO\") {
    pullRequest(number: $PR) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          comments(first: 1) {
            nodes { body path }
          }
        }
      }
    }
  }
}")

echo "$THREADS" | jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved == false)'

# Reply to a specific thread and resolve it
THREAD_ID="PRRT_kwDOAbc123"

gh api graphql -f query="
mutation {
  addPullRequestReviewThreadReply(input: {
    pullRequestReviewThreadId: \"$THREAD_ID\"
    body: \"✅ Fixed in latest commit\"
  }) {
    comment { id }
  }
}"

gh api graphql -f query="
mutation {
  resolveReviewThread(input: {threadId: \"$THREAD_ID\"}) {
    thread { id isResolved }
  }
}"
```

## Guidelines

- **Always paginate** when fetching PR comments - use `--paginate` flag
- **Use set comparison** (comm command) to reliably find unreplied comments
- **Reply before resolving** - add a comment explaining the fix before marking as resolved
- **Reference commits** in replies so reviewers can verify the fix
- **Group related changes** into single commits with clear messages
- **Test your fixes** before replying to ensure the issue is actually addressed
- **Be specific** in replies about what changed and why
- **Keep replies concise** but informative
- **Use emojis** consistently for status (✅ fixed, 🔄 in progress, 💭 discussion)

## Notes

### REST API vs GraphQL API

- **REST API** (`gh api repos/.../pulls/.../comments`):
  - Better for listing and filtering comments
  - Simpler for replies
  - Requires pagination for complete results

- **GraphQL API** (`gh api graphql`):
  - Better for fetching threads with nested structure
  - Required for resolving/unresolving threads
  - More efficient for complex queries (fewer API calls)
  - Thread IDs have format `PRRT_kwDO...`

### Comment ID vs Thread ID

- **Comment IDs** are numeric (e.g., `123456789`)
- **Thread IDs** are GraphQL node IDs (e.g., `PRRT_kwDOAbc123...`)
- Use comment IDs for REST API replies
- Use thread IDs for GraphQL thread operations

### Automation Considerations

For coding agents and automation:
- Store comment IDs and thread IDs for tracking
- Batch operations where possible to reduce API calls
- Add delays between API calls to respect rate limits
- Log all API responses for debugging
- Handle errors gracefully (comment might be deleted, PR might be closed)

### Future Enhancement

When `gh pr review-thread` command becomes available ([gh cli #12419](https://github.com/cli/cli/issues/12419)), it will provide:
- `gh pr review-thread resolve <thread-id>`
- `gh pr review-thread unresolve <thread-id>`
- `gh pr review-thread list --unresolved`

Until then, use the GraphQL mutations shown above.
