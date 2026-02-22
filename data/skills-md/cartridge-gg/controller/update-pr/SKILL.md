---
name: update-pr
description: Update an existing pull request with new changes or respond to review feedback. Use when addressing PR comments, making requested changes, or updating a PR after review.
---

# Update Pull Request

## Steps

### 1. Identify the PR

```bash
# List open PRs for current branch
gh pr list --head $(git branch --show-current)

# Or get PR details by number
gh pr view <PR_NUMBER>
```

### 2. Fetch Review Comments

```bash
# View PR reviews and comments
gh pr view <PR_NUMBER> --comments

# View the PR diff to understand context
gh pr diff <PR_NUMBER>
```

### 3. Address Feedback

For each review comment:
1. Read and understand the feedback
2. Make the necessary code changes
3. Stage and commit with a descriptive message

```bash
# Stage changes
git add -u

# Commit with reference to what was addressed
git commit -m "address review: <brief description>"
```

### 4. Push Updates

```bash
# Push to the same branch (PR updates automatically)
git push
```

### 5. Respond to Review Comments (Optional)

If you need to reply to specific comments:

```bash
# Reply to a review comment
gh api repos/{owner}/{repo}/pulls/<PR_NUMBER>/comments/<COMMENT_ID>/replies \
  -f body="Done - updated the implementation as suggested"
```

Or use the GitHub web interface for complex discussions.

### 6. Re-request Review (if needed)

```bash
# Re-request review from specific reviewers
gh pr edit <PR_NUMBER> --add-reviewer <username>
```

## Handling Common Review Requests

### "Please add tests"
1. Identify the appropriate test file in `packages/*/src/__tests__/`
2. Add test cases covering the new functionality
3. Run `pnpm test` to verify

### "Update types"
1. Check TypeScript errors with `pnpm build`
2. Update type definitions as needed
3. Ensure no type errors remain

### "Fix lint issues"
```bash
pnpm format  # Auto-fix formatting
pnpm lint    # Check and fix lint issues
```

### "Update snapshots"
```bash
pnpm test:storybook:update
git add packages/*/__image_snapshots__/
git commit -m "chore: update storybook snapshots"
```

## Squashing Commits (if requested)

If the reviewer asks to squash commits:

```bash
# Interactive rebase to squash
git rebase -i origin/main

# In the editor, change 'pick' to 'squash' for commits to combine
# Save and edit the combined commit message

# Force push (safe for PR branches)
git push --force-with-lease
```

## Example Workflow

```bash
# 1. Fetch latest review comments
gh pr view 42 --comments

# 2. Make changes based on feedback
# ... edit files ...

# 3. Commit and push
git add -u
git commit -m "address review: add error handling for edge case"
git push

# 4. Notify reviewer
echo "Updated PR #42 - addressed all review comments"
```
