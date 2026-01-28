---
name: pr-review
description: This skill processes unresolved GitHub PR review discussions. Activated when the user provides a GitHub PR link (github.com/.../pull/...) or mentions "PR review", "review PR", "process review comments", etc.
argument-hint: [pr-url]
user-invocable: true
---

# GitHub PR Review Skill

## Overview

This skill automatically processes unresolved GitHub Pull Request review discussions by analyzing the code context, validating feedback, and taking appropriate actions. It intelligently categorizes feedback as valid, invalid, or already addressed, then creates action plans or posts clarifying responses accordingly.

## Supported Actions

| Action Type | When Used | Outcome |
|-------------|-----------|---------|
| Create Todo | Valid feedback needing fixes | Adds task to todo list |
| Reply & Resolve | Invalid or misunderstood feedback | Posts clarifying comment, resolves thread |
| Confirm & Resolve | Already fixed feedback | Posts confirmation, resolves thread |
| Escalate | Ambiguous or complex feedback | Asks user for guidance |

## Discussion Classification

### Valid Feedback
Legitimate issues that require code changes:
- Missing error handling
- Type safety concerns
- Performance problems
- Security vulnerabilities
- Logic errors

### Invalid Feedback
Misunderstandings or incorrect observations:
- Code already handles the mentioned case
- Reviewer misread the implementation
- Feedback based on outdated context
- Incorrect assumptions

### Already Addressed
Feedback that has been fixed since review:
- Changes made in recent commits
- Fixed in different files
- Resolved through refactoring

## Workflow

### 1. Verify GitHub CLI Installation

**Check if gh CLI is available:**

```bash
gh --version
```

**Expected output:**
- Success: `gh version X.Y.Z (YYYY-MM-DD)`
- Failure: Command not found error

**If not installed, display installation guide:**

```
GitHub CLI (gh) is not installed.

Installation:
  macOS:          brew install gh
  Ubuntu/Debian:  sudo apt install gh
  Windows:        winget install GitHub.cli
  Linux (other):  See https://github.com/cli/cli#installation

After installation, authenticate:
  gh auth login
```

**Verify authentication:**

```bash
gh auth status
```

**If not authenticated:**
```
Please authenticate with GitHub:
  gh auth login

Follow the prompts to complete authentication.
```

### 2. Parse PR URL

**Extract repository and PR information from argument:**

URL format: `https://github.com/{owner}/{repo}/pull/{number}`

**Extraction logic:**
```bash
url="$ARGUMENTS"
owner=$(echo "$url" | sed -n 's#.*/github.com/\([^/]*\)/.*#\1#p')
repo=$(echo "$url" | sed -n 's#.*/github.com/[^/]*/\([^/]*\)/.*#\1#p')
pr_number=$(echo "$url" | sed -n 's#.*/pull/\([0-9]*\).*#\1#p')
```

**Example:**
```
Input:  https://github.com/anthropics/claude-code/pull/123
Output: owner=anthropics, repo=claude-code, pr_number=123
```

**Validation:**
- Ensure all three values are non-empty
- Verify PR number is numeric
- Confirm URL matches expected pattern

**If URL invalid:**
```
Error: Invalid GitHub PR URL

Expected format: https://github.com/OWNER/REPO/pull/NUMBER
Example: https://github.com/anthropics/claude-code/pull/123
```

### 3. Fetch Unresolved Discussions

**Query GitHub GraphQL API for review threads:**

```bash
gh api graphql -f query='
  query($owner: String!, $repo: String!, $pr: Int!) {
    repository(owner: $owner, name: $repo) {
      pullRequest(number: $pr) {
        title
        author { login }
        reviewThreads(first: 100) {
          nodes {
            id
            isResolved
            isOutdated
            path
            line
            comments(first: 10) {
              nodes {
                id
                body
                author { login }
                createdAt
              }
            }
          }
        }
      }
    }
  }
' -f owner="$owner" -f repo="$repo" -F pr="$pr_number"
```

**Response structure:**
```json
{
  "data": {
    "repository": {
      "pullRequest": {
        "reviewThreads": {
          "nodes": [
            {
              "id": "PRRT_...",
              "isResolved": false,
              "isOutdated": false,
              "path": "src/auth.ts",
              "line": 45,
              "comments": {
                "nodes": [
                  {
                    "body": "This needs null checking",
                    "author": {"login": "reviewer"},
                    "createdAt": "2024-01-01T12:00:00Z"
                  }
                ]
              }
            }
          ]
        }
      }
    }
  }
}
```

**Filter for unresolved threads:**
- Extract threads where `isResolved: false`
- Optionally include `isOutdated: true` threads (may be relevant)
- Store thread ID, path, line, and all comments

**If no unresolved discussions:**
```
✓ All review discussions have been resolved

PR: [PR Title]
Status: No pending feedback
```

### 4. Analyze Each Discussion

For each unresolved thread, perform comprehensive analysis:

#### 4.1 Read Local Code

**Fetch the file at the specified path:**

```bash
# Read the file with context around the line
Read file_path="$path"
```

**Extract relevant section:**
- Focus on the specific line mentioned
- Include 10 lines before and after for context
- Identify function/class scope

#### 4.2 Fetch PR Diff

**Get the complete PR diff:**

```bash
gh pr diff "$pr_number" -R "$owner/$repo"
```

**Parse diff for the specific file:**
- Locate changes to the file mentioned in comment
- Identify if the line was added, modified, or is context
- Check if subsequent commits modified this area

#### 4.3 Review Comment Thread

**Analyze all comments in the thread:**
- First comment: Original reviewer feedback
- Subsequent comments: Author responses and discussion
- Extract key concerns and questions
- Identify if conversation reached conclusion

#### 4.4 Compare States

**Determine the current state:**

1. **Has code changed since review?**
   - Check git log for commits after review comment timestamp
   - Compare current code to PR diff

2. **Does current code address the concern?**
   - Valid feedback: Code still has the issue
   - Invalid feedback: Code already handles it
   - Already addressed: Fixed in later commits

3. **Is feedback contextually correct?**
   - Reviewer may have missed related code
   - Check imports and dependencies
   - Verify assumptions in the comment

### 5. Categorize and Process

#### Type A: Valid Feedback (Needs Fix)

**Identification:**
- Issue exists in current code
- Feedback is technically correct
- Change would improve code quality

**Action:**
```bash
# Add to todo list using TodoWrite
TodoWrite:
  - content: "Fix [issue] in [file]:[line]"
  - status: "pending"
```

**Example:**
```
Discussion: "Missing null check for user.profile"
Current code: No null check present
Category: Valid Feedback

Action: Added todo "Add null check for user.profile in auth.ts:45"
```

#### Type B: Invalid Feedback (Misunderstanding)

**Identification:**
- Code already handles the concern
- Reviewer misunderstood implementation
- Feedback based on incorrect assumption

**Action:**
```bash
# Post clarifying comment
gh api graphql -f query='
  mutation($threadId: ID!, $body: String!) {
    addPullRequestReviewThreadReply(input: {
      pullRequestReviewThreadId: $threadId
      body: $body
    }) {
      comment { id }
    }
  }
' -f threadId="$thread_id" -f body="[polite clarification]"

# Resolve the thread
gh api graphql -f query='
  mutation($threadId: ID!) {
    resolveReviewThread(input: {threadId: $threadId}) {
      thread { isResolved }
    }
  }
' -f threadId="$thread_id"
```

**Comment template:**
```
Thank you for the feedback! This is actually already handled:

[Explanation with code reference]

The [specific mechanism] ensures [desired behavior].

Reference: [file]:[line]
```

**Example:**
```
Discussion: "Variable 'token' is unused"
Current code: Variable used on line 67
Category: Invalid Feedback

Reply: "Thank you for checking! The 'token' variable is actually used
        on line 67 in the authentication middleware. Here's the usage:

        ```typescript
        if (token) {
          return validateToken(token);
        }
        ```"
Action: Resolved thread
```

#### Type C: Already Addressed

**Identification:**
- Issue existed at review time
- Fixed in subsequent commits
- Current code is correct

**Action:**
```bash
# Post confirmation comment
gh api graphql -f query='[same mutation as Type B]' \
  -f threadId="$thread_id" \
  -f body="This has been addressed in commit [hash]. [Brief explanation]"

# Resolve thread
gh api graphql -f query='[same resolve mutation]' -f threadId="$thread_id"
```

**Comment template:**
```
This has been addressed in commit [short-hash].

Changes made:
[Brief summary of the fix]

Current implementation:
[Code snippet if helpful]
```

**Example:**
```
Discussion: "Add TypeScript types for User interface"
Current code: User interface fully typed
Category: Already Addressed

Reply: "This has been addressed in commit abc123f. Added comprehensive
        TypeScript types for the User interface including optional fields."
Action: Resolved thread
```

#### Type D: Ambiguous or Complex

**Identification:**
- Feedback requires design decision
- Multiple valid approaches exist
- User input needed for direction

**Action:**
```bash
# Ask user for guidance using AskUserQuestion
AskUserQuestion:
  question: "[Reviewer] suggests [approach]. How would you like to proceed?"
  options:
    - Implement suggested approach
    - Explain current approach to reviewer
    - Discuss alternative solution
```

### 6. Generate Summary Report

**After processing all discussions, create summary:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PR Review Processing Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PR: [PR Title] (#[number])
Repository: [owner]/[repo]

Summary:
  Total discussions:    [X]
  Valid feedback:       [Y] → Added to todo list
  Invalid feedback:     [Z] → Clarified and resolved
  Already addressed:    [W] → Confirmed and resolved
  Escalated:           [N] → Requires user input

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Action Items Created:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. [file]:[line] - [description]
2. [file]:[line] - [description]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Resolved Discussions:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ [file]:[line] - [reason for resolution]
✓ [file]:[line] - [reason for resolution]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Examples

### Example 1: Valid Null Check Feedback

**Review comment:**
```
src/auth.ts:45
"This function should handle null user profiles"
```

**Analysis:**
```bash
# Read file
Read src/auth.ts

# Check lines 35-55
function getProfile(user) {
  return user.profile.name;  // Line 45 - no null check
}
```

**Outcome:**
```
Category: Valid Feedback
Action: Added todo "Add null check for user.profile in auth.ts:45"
```

### Example 2: Misunderstood Variable Usage

**Review comment:**
```
src/api.ts:120
"Variable 'cache' is declared but never used"
```

**Analysis:**
```bash
# Read file
Read src/api.ts

# Check lines 110-140
const cache = new Map();  // Line 120

function getData(key) {
  if (cache.has(key)) {   // Line 130 - using cache
    return cache.get(key);
  }
  // ...
}
```

**Outcome:**
```
Category: Invalid Feedback

Reply posted:
"Thank you for reviewing! The 'cache' variable is actually used in the
getData function on lines 130-132 for memoization. Here's the usage:

```typescript
if (cache.has(key)) {
  return cache.get(key);
}
```

The cache improves performance by storing previously fetched data."

Action: Resolved thread
```

### Example 3: Already Fixed Type Issue

**Review comment:**
```
src/types.ts:15
"Missing return type annotation"
```

**Analysis:**
```bash
# Check current code
Read src/types.ts

# Line 15 now has type annotation
function calculate(): number {  // Line 15 - type added
  return 42;
}

# Check git log
git log --oneline --since="[review date]" src/types.ts
# Shows: "a1b2c3d feat(types): add return type annotations"
```

**Outcome:**
```
Category: Already Addressed

Reply posted:
"This has been addressed in commit a1b2c3d. Added return type annotations
to all exported functions including this one.

Current implementation:
```typescript
function calculate(): number {
  return 42;
}
```"

Action: Resolved thread
```

## Technical Requirements

### Required Tools

| Tool | Purpose | Installation | Check Command |
|------|---------|--------------|---------------|
| GitHub CLI | API access | `brew install gh` | `gh --version` |
| Git | Local repository | Built-in or package manager | `git --version` |
| jq | JSON parsing | `brew install jq` | `jq --version` |

### API Requirements

- **GitHub API**: GraphQL endpoint access
- **Authentication**: Valid GitHub token with repo scope
- **Rate limits**: ~5000 requests/hour (authenticated)
- **Permissions**: Read access to repository, write access to PR comments

### Minimum Versions

- **gh CLI**: 2.0.0 or higher
- **Git**: 2.0 or higher
- **jq**: 1.6 or higher

## Best Practices

1. **Always read local code** before making judgments
2. **Be polite and professional** in all responses
3. **Provide code references** to support clarifications
4. **Resolve threads only after posting comments**
5. **Group related todos** for efficiency
6. **Include commit hashes** when mentioning fixes
7. **Ask for user input** when uncertain
8. **Check git history** to understand recent changes

## Limitations

1. **Local context only**: Analysis based on local repository state
2. **100 discussions max**: GraphQL query limited to first 100 threads
3. **10 comments per thread**: Comment fetch limited to first 10
4. **No file history**: Cannot analyze full file evolution
5. **Requires authentication**: Must have GitHub access token
6. **Rate limiting**: May hit API limits on large PRs

## Error Handling

### Common Errors and Solutions

**Error: gh: command not found**
- **Cause**: GitHub CLI not installed
- **Solution**: Install with `brew install gh` or platform equivalent

**Error: To get started with GitHub CLI, run: gh auth login**
- **Cause**: Not authenticated with GitHub
- **Solution**: Run `gh auth login` and follow prompts

**Error: GraphQL: Could not resolve to a PullRequest**
- **Cause**: Invalid PR number or URL
- **Solution**: Verify PR exists and URL is correct

**Error: Resource not accessible by personal access token**
- **Cause**: Insufficient permissions
- **Solution**: Re-authenticate with `gh auth refresh -s repo`

**Error: API rate limit exceeded**
- **Cause**: Too many API requests
- **Solution**: Wait for rate limit reset (check `gh api rate_limit`)

## Advanced Features

### Batch Processing

For PRs with many discussions:
```bash
# Process in batches of 10
for i in {0..9}; do
  # Process discussion $i
  # Add delay to avoid rate limiting
  sleep 1
done
```

### Draft Responses

Before posting, optionally show draft responses to user:
```
Draft response for [file]:[line]:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Response text]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Post this response? [y/n]
```

### Filter by Reviewer

Process discussions from specific reviewer:
```bash
# Filter threads by comment author
jq '.data.repository.pullRequest.reviewThreads.nodes[] |
    select(.comments.nodes[0].author.login == "specific-reviewer")'
```

## References

- **GitHub CLI**: https://cli.github.com/
- **GitHub GraphQL API**: https://docs.github.com/en/graphql
- **PR Review API**: https://docs.github.com/en/rest/pulls/reviews

## Notes

- Always post comments before resolving threads (order matters)
- Responses should be professional and technically accurate
- Include code snippets when clarifying implementation details
- Reference specific lines/commits to support arguments
- Never resolve threads without explanation
- Escalate to user when feedback is ambiguous or requires design decision
