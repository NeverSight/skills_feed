---
name: sentry-pr-code-review
description: Review a project's PRs to check for issues detected in code review by Seer Bug Prediction. Use when asked to review or fix issues identified by Sentry in PR comments, or to find recent PRs with Sentry feedback.
---

# Sentry Code Review

Review and fix issues identified by Sentry bot in GitHub PR comments.

## Invoke This Skill When

- User asks to "review Sentry comments" or "fix Sentry issues" on a PR
- User shares a PR URL/number and mentions Sentry feedback
- User asks to "address Sentry review" or "resolve Sentry findings"
- User wants to find PRs with unresolved Sentry comments

## Workflow

### Phase 1: Fetch Sentry Comments

```bash
gh api repos/{owner}/{repo}/pulls/{PR_NUMBER}/comments \
  --jq '.[] | select(.user.login | startswith("sentry")) | {file: .path, line: .line, body: .body}'
```

**Only process comments from `sentry[bot]`** - ignore other bots.

### Phase 2: Parse Each Comment

Extract from the markdown body:
- **Bug description**: Line starting with `**Bug:**`
- **Severity/Confidence**: In `<sub>Severity: X | Confidence: X.XX</sub>`
- **Analysis**: Inside `<summary>🔍 <b>Detailed Analysis</b></summary>` block
- **Suggested Fix**: Inside `<summary>💡 <b>Suggested Fix</b></summary>` block
- **AI Prompt**: Inside `<summary>🤖 <b>Prompt for AI Agent</b></summary>` block

### Phase 3: Verify & Fix

For each issue:
1. Read the file at the specified line
2. Confirm issue still exists in current code
3. Review related code to understand if its an actual issue or not 
4. Implement fix (suggested or your own)
5. Consider edge cases

### Phase 4: Summarize and Report Results

```markdown
## Sentry Review: PR #[number]

### Resolved
| File:Line | Issue | Severity | Fix Applied |
|-----------|-------|----------|-------------|
| path:123  | desc  | HIGH     | what done   |

### Manual Review Required
| File:Line | Issue | Reason |
|-----------|-------|--------|

**Summary:** X resolved, Y need manual review
```

## Common Issue Types

| Category | Examples |
|----------|----------|
| Type Safety | Missing null checks, unsafe type assertions |
| Error Handling | Swallowed errors, missing boundaries |
| Validation | Permissive inputs, missing sanitization |
| Config | Missing env vars, incorrect paths |
