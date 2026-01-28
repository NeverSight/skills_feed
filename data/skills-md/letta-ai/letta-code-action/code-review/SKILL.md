---
name: code-review
description: Skill for handling PR code reviews. Use when triggered by a PR review comment, review request, or when asked to review code changes. Provides workflow for reading review comments, understanding feedback, and iterating on changes.
---

# Code Review Skill

You are handling a PR code review interaction. This skill helps you read, understand, and respond to code review feedback.

## When This Skill Applies

- Triggered by `pull_request_review` or `pull_request_review_comment` events
- User asks you to address review feedback
- User requests a code review of their changes

## Reading Review Comments

### Get All Reviews on a PR

```bash
# List all reviews (approved, changes requested, commented)
gh api repos/$GITHUB_REPOSITORY/pulls/<number>/reviews

# Get a specific review's comments
gh api repos/$GITHUB_REPOSITORY/pulls/<number>/reviews/<review_id>/comments
```

### Get Review Comments (Line-Level Feedback)

```bash
# All line-level review comments on the PR
gh api repos/$GITHUB_REPOSITORY/pulls/<number>/comments

# Filter by specific path
gh api repos/$GITHUB_REPOSITORY/pulls/<number>/comments | jq '.[] | select(.path == "src/example.ts")'
```

### Understanding Review Comment Structure

Key fields in review comments:

- `path`: File being commented on
- `line` / `original_line`: Line number in the diff
- `body`: The reviewer's comment text
- `diff_hunk`: Code context around the comment
- `in_reply_to_id`: If this is a reply to another comment

## Responding to Review Feedback

### Workflow for Addressing Feedback

1. **Read the review comments** to understand what changes are requested
2. **Read the relevant files** using the paths from the comments
3. **Make the requested changes** using Edit tool
4. **Commit and push** to update the PR
5. **Update your tracking comment** to summarize what was addressed

### Replying to Review Comments

```bash
# Reply to a specific review comment
gh api repos/$GITHUB_REPOSITORY/pulls/<number>/comments \
  -X POST \
  -f body="Fixed in the latest commit" \
  -f in_reply_to=<comment_id>
```

### Marking Conversations as Resolved

After addressing feedback, the reviewer typically resolves the conversation. You can indicate you've addressed it by:

1. Replying to the comment explaining what you changed
2. Updating your tracking comment with a summary

## Providing Code Review Feedback

When asked to review code changes:

### Quick Review Checklist

- **Correctness**: Does the code do what it's supposed to?
- **Security**: Are there any security vulnerabilities?
- **Performance**: Are there obvious performance issues?
- **Readability**: Is the code clear and maintainable?
- **Tests**: Are changes tested appropriately?

### Viewing PR Changes

```bash
# View the diff
gh pr diff <number> --repo $GITHUB_REPOSITORY

# View changed files list
gh pr view <number> --repo $GITHUB_REPOSITORY --json files

# Compare with base branch (use two dots for shallow clones in GitHub Actions)
git diff origin/$BASE_BRANCH..HEAD
```

### Providing Feedback

Post your review feedback to your tracking comment. Structure it clearly:

- Group feedback by file
- Reference specific line numbers
- Distinguish between required changes and suggestions
- Be constructive and specific

## Submitting Interactive Reviews

Use `gh pr review` to submit formal GitHub reviews that appear in the PR's review UI.

### Approve a PR

```bash
gh pr review <number> --approve --body "LGTM! Changes look good."
```

### Request Changes

```bash
gh pr review <number> --request-changes --body "Please address the following issues..."
```

### Leave a Comment Review (without approval/rejection)

```bash
gh pr review <number> --comment --body "Some observations about the code..."
```

## Adding Line-Level Comments

To add comments on specific lines of code (shown inline in GitHub's diff view):

### Create a Review with Line Comments

```bash
# First, get the latest commit SHA
COMMIT_SHA=$(gh pr view <number> --json headRefOid --jq '.headRefOid')

# Create a review comment on a specific position in the diff
# Note: position is the line number in the diff (not the file), starting from 1
gh api repos/$GITHUB_REPOSITORY/pulls/<number>/comments \
  -X POST \
  -f body="Consider using a more descriptive variable name here" \
  -f commit_id="$COMMIT_SHA" \
  -f path="src/example.ts" \
  -F position=10
```

### Key Fields for Line Comments

- `commit_id`: The SHA of the commit to comment on (use latest)
- `path`: File path relative to repo root
- `position`: Position in the diff (line number in the diff hunk, starting at 1)
- `body`: Your comment text

**Note:** The `position` is the line number within the diff, not the line number in the file. Count lines from the start of the diff hunk.

## Iterating on Changes

When you need to make additional changes after initial feedback:

```bash
# Ensure you're on the PR branch
gh pr checkout <number>

# Make changes, then commit
git add <files>
git commit -m "fix: address review feedback"

# Push to update the PR
git push origin HEAD
```

## Important Notes

1. **Read before responding** - Always read the full review context before making changes
2. **Address all comments** - Don't leave feedback unaddressed
3. **Communicate clearly** - Update your tracking comment to show what you've addressed
4. **Test your changes** - Run tests after making review-requested changes
