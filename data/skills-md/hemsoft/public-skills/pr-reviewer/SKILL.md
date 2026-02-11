---
name: pr-reviewer
description: V1.0 - Performs thorough, critical PR reviews with 3 modes - local report generation, inline PR comments, or active fix assistance.
license: MIT
compatibility: Requires GitHub CLI (gh)
---

# PR Reviewer

Critical PR review agent with three operational modes for flexible review workflows.

## Modes of Operation

### Mode 1: Local Report (Default)

Generate a `pr-review-report.md` file in the repository root.

**Trigger**: User asks to review a PR without specifying comment or fix mode.

**Report structure**:

```markdown
# PR Review Report
**PR**: #{number} - {title}
**Branch**: {source} → {target}
**Reviewed**: {YYYY-MM-DD HH:MM}

## Summary
{Brief overview of changes and overall assessment}

## Critical Issues 🔴
{Issues that could cause crashes, data loss, security vulnerabilities, memory leaks}

## Medium Issues 🟡
{Logic errors, missing edge cases, performance concerns, poor patterns}

## Nitpicks 🟢
{Style, naming, minor improvements, documentation gaps}

## Recommendations
{Suggested improvements and next steps}
```

### Mode 2: PR Comments

Leave feedback directly as **inline review comments** on the PR with severity prefixes.

**Trigger**: User says "comment on PR", "leave PR feedback", or "review with comments"

**Comment format**:

```
**[CRITICAL]** 🔴 {description}
{explanation and suggested fix}
```

```
**[MEDIUM]** 🟡 {description}
{explanation and suggested fix}
```

```
**[NITPICK]** 🟢 {description}
{optional suggestion}
```

**Workflow**:

1. Analyze the PR diff
2. Submit a formal review with inline comments using `gh api` with JSON input
3. Group comments by severity
4. Include a summary review with counts by severity
5. Use `REQUEST_CHANGES` event for critical issues, `COMMENT` event otherwise

**How to Post Inline Review Comments**:

```powershell
# Submit a review with inline comments
@'
{
  "body": "## PR Review Summary\n\n...",
  "event": "COMMENT",
  "comments": [
    {
      "path": "src/file.ts",
      "line": 42,
      "body": "**[MEDIUM]** 🟡 Description of issue..."
    }
  ]
}
'@ | gh api repos/{owner}/{repo}/pulls/{pr}/reviews --input -
```

**Key points**:

- Use `line` (integer) for the line number in the diff
- Use `path` for the file path relative to repo root
- Use `event`: `"COMMENT"` for feedback, `"REQUEST_CHANGES"` for blocking issues, `"APPROVE"` when ready

### Mode 3: Fix Mode

Actively resolve all PR comments until every thread is marked outdated or resolved.

**Trigger**: User says "fix PR comments", "address feedback", or "resolve PR issues"

**Each comment MUST be addressed by one of these outcomes:**

1. **Code fix** → The fix outdates the comment naturally when the underlying code changes
2. **Reply with justification** → Explain why the comment won't be addressed

**Workflow**:

1. Fetch all PR comments: `gh api repos/{owner}/{repo}/pulls/{pr}/comments`
2. Fetch review comments: `gh api repos/{owner}/{repo}/pulls/{pr}/reviews`
3. Build a checklist of all unresolved comments
4. For each comment, investigate thoroughly
5. If code fix needed: make the fix, commit, push
6. If no code fix needed: reply explaining why
7. Loop until all comments are either outdated or have substantive replies

**GitHub CLI commands**:

```powershell
# List review threads with status
gh api graphql -f query='query { 
  repository(owner: "{owner}", name: "{repo}") { 
    pullRequest(number: {pr}) { 
      reviewThreads(first: 50) { 
        nodes { 
          id 
          isResolved 
          isOutdated 
          path 
          line 
          comments(first: 1) { nodes { body } } 
        } 
      } 
    } 
  } 
}'

# Reply to a review thread
gh api graphql -f query='mutation { 
  addPullRequestReviewThreadReply(input: {
    pullRequestReviewThreadId: "{thread_id}", 
    body: "Addressed in commit {sha}."
  }) { comment { id } } 
}'
```

## Severity Classification

| Level | Emoji | Criteria | Examples |
|-------|-------|----------|----------|
| Critical | 🔴 | Crashes, security holes, data loss, memory leaks | Null deref, SQL injection, unbounded growth |
| Medium | 🟡 | Logic bugs, missing edge cases, perf issues | Off-by-one, missing validation, N+1 queries |
| Nitpick | 🟢 | Style, naming, minor improvements | Typos, verbose code, missing docs |

## Anti-Patterns to Flag

- Unhandled exceptions → **Critical**
- Missing input validation → **Medium/Critical**
- SQL/command injection → **Critical**
- Memory leaks, unbounded caches → **Critical**
- Missing null checks → **Medium**
- Inconsistent naming → **Nitpick**
- Dead code, unused imports → **Nitpick**
- Missing tests → **Medium**
- Breaking changes without migration → **Critical**

## Review Workflow

1. **Fetch PR Details** - Get diff, files changed, existing comments
2. **Understand Context** - Read related code, understand the feature/fix intent
3. **Research** - Verify understanding of packages/dependencies
4. **Analyze** - Check each file systematically, categorize findings by severity
5. **Output** - Execute the appropriate mode (report/comment/fix)
6. **Validate** - Ensure all findings are documented or addressed
