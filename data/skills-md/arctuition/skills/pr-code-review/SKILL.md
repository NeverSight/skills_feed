---
name: pr-code-review
description: Perform GitHub pull request code reviews using the gh CLI. Use when asked to review a PR, inspect PR diffs, leave inline review comments on specific lines, or produce a severity-based summary (high/medium/low) of findings.
---

# PR Code Review

Use this skill to review GitHub PRs end-to-end with the gh CLI, leave inline comments tied to specific code lines, and conclude with a severity summary.

## Quick workflow

1. Identify the PR context.
2. Collect and read diffs.
3. Analyze and draft findings.
4. Post inline comments on the relevant code lines.
5. Provide a severity summary (high/medium/low).

## Step-by-step

### 1) Identify PR and scope

- Resolve the PR number or URL and repository.
- Capture metadata to anchor comments and fetch commit IDs.

Suggested commands (see references/gh-cli.md):

- `gh pr view <pr> --json number,title,headRefOid,baseRefName,headRefName,author,changedFiles,additions,deletions`
- `gh pr view <pr> --json files --jq '.files[] | {path,additions,deletions}'`

### 2) Read the diff efficiently

- Start with file list and high-churn areas.
- Use patch output when you need line numbers.
- For larger PRs, break the diff into files and review sequentially.

Suggested commands:

- `gh pr diff <pr> --name-only`
- `gh pr diff <pr> --patch`
- `gh pr diff <pr> --patch --color=never > /tmp/pr.diff`

### 3) Analyze and record findings

- Classify each issue as High / Medium / Low severity.
- For each issue, capture: file path, line number, summary, reasoning, and recommended fix.
- Keep comments crisp and actionable.

### 4) Post inline comments in the PR

- Prefer inline comments tied to exact file/line.
- If inline comments are not possible, fall back to a general review comment.

Primary path (inline comment via GitHub API using `gh api`):

- Use `headRefOid` as `commit_id`.
- Use file path and line number from the patch output.

Fallback path (general review comment):

- Use `gh pr review --comment -b "..."` or `gh pr comment -b "..."`.

See references/gh-cli.md for examples.

### 5) Final summary by severity

Provide a final summary grouped by severity:

- **High**: issues that can cause correctness, security, data loss, or outage.
- **Medium**: issues that affect reliability, maintainability, or performance.
- **Low**: minor style issues, low-risk refactors, or optional improvements.

Include counts and short titles of each issue, and mention any files that were not reviewed (if any).

## Output format

- Use short, direct sentences.
- Always include file path and line number with each inline comment.
- End with a severity summary in three sections: High / Medium / Low.

## References

- `references/gh-cli.md` for command patterns and inline comment API usage.
