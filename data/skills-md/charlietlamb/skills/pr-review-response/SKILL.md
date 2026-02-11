---
name: pr-review-response
description: Extract and respond to comments from a GitHub Pull Request. Use this skill when given a GitHub PR URL to review comments and act on the feedback, or when asked to address PR review feedback.
---

# PR Review Response

This skill helps you extract comments from a GitHub Pull Request and act on the feedback.

## Input

Accept a GitHub PR URL in the format: `https://github.com/{owner}/{repo}/pull/{number}`

Parse the URL to extract:
- `owner`: Repository owner
- `repo`: Repository name
- `number`: PR number

## Extracting Comments

Use the `gh` CLI to fetch all types of PR comments:

### 1. Review Comments (inline comments on code)
```bash
gh api repos/{owner}/{repo}/pulls/{number}/comments
```

These comments include:
- `path`: File path the comment references
- `line` or `original_line`: Line number
- `body`: Comment text
- `diff_hunk`: Code context

### 2. PR Reviews (approval/request changes with summary)
```bash
gh api repos/{owner}/{repo}/pulls/{number}/reviews
```

These include:
- `body`: Review summary
- `state`: APPROVED, CHANGES_REQUESTED, COMMENTED

### 3. General PR Comments (conversation thread)
```bash
gh api repos/{owner}/{repo}/issues/{number}/comments
```

These are discussion comments not tied to specific lines.

## Processing Comments

1. **Group by file**: Organize inline comments by their `path` field
2. **Classify feedback by intent**:
   - **Change requests** — explicit directives to modify code (e.g. "please change", "should be", "fix", "update")
   - **Open questions** — inquiries that require investigation or clarification
   - **Enhancement suggestions** — non-blocking recommendations for improvement
3. **Prioritize**: Address blocking comments (from CHANGES_REQUESTED reviews) first

## Acting on Feedback

For each actionable comment:

1. **Read the referenced file** to understand the current code
2. **Fix problems at the root**: Don't apply superficial fixes. Investigate and address the underlying cause of the issue, not just the symptom mentioned in the comment
3. **Apply requested changes** using the Edit tool
4. **For questions**: Investigate and provide answers or make clarifying changes
5. **For suggestions**: Evaluate and implement if appropriate
6. **Add tests for edge cases**: If the feedback identifies an edge case and the project has testing already set up, add a test to cover that edge case to prevent regression

## Example Workflow

Given `https://github.com/acme/app/pull/42`:

1. Extract: owner=`acme`, repo=`app`, number=`42`
2. Fetch comments:
   ```bash
   gh api repos/acme/app/pulls/42/comments
   gh api repos/acme/app/pulls/42/reviews
   gh api repos/acme/app/issues/42/comments
   ```
3. Parse the JSON responses to identify feedback
4. For each comment with a file path, read that file and apply changes
5. Summarize what was addressed

## Output

After processing, provide a summary of:
- Number of comments found
- Actions taken for each comment
- Any comments that need clarification or manual review
