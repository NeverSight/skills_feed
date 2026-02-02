---
name: code-review
description: "Review code changes using CodeRabbit CLI - supports uncommitted files (task mode) or all PR files vs main branch (pr mode). Catches bugs, security issues, and code quality problems before committing or when reviewing pull requests. Use when: (1) Reviewing uncommitted changes before committing (task mode), (2) Reviewing all changed files in a PR against main branch (pr mode), (3) Working on subtasks and want to check progress, (4) Need feedback on work-in-progress code, (5) Preparing PR for merge, (6) When CodeRabbit review is needed, (7) For bug detection and security scanning, or (8) For automated code quality assessment. Triggers: review code, check code quality, review changes, code review, review PR, check for bugs, security scan, review uncommitted, finalize code, pre-commit review."
metadata:
  author: ai-dev-atelier
  version: "1.0"
---

# Code Review

## Two Modes

### Task Mode (Uncommitted Files)

Reviews only uncommitted files in the working directory. Use for work-in-progress code before committing.

**Command**: `bash skills/code-review/scripts/review-run.sh task`

**How it works**:
- Scans all uncommitted files (git status shows as modified/untracked)
- Sends files to CodeRabbit for review
- Saves results to `.ada/data/reviews/task-review-{timestamp}.md`

### PR Mode (All Files vs Main)

Reviews all changed files in the current branch compared to the main branch. Use for complete PR review.

**Command**: `bash skills/code-review/scripts/review-run.sh pr`

**How it works**:
- Compares current branch against main branch (or configured base branch)
- Reviews all changed files in the diff
- Saves results to `.ada/data/reviews/pr-review-{timestamp}.md`

## Tools

- `ada::review:task` - Review uncommitted changes
- `ada::review:pr` - Review all PR files vs main branch
- `ada::review:read` - Read latest review results
- `ada::review:cleanup` - Clean up old review files

## Workflow

### Task Mode Workflow

1. **Make code changes**: Edit files without committing
2. **Run review**: Execute `bash skills/code-review/scripts/review-run.sh task`
   - CodeRabbit analyzes uncommitted files
   - Review is saved to `.ada/data/reviews/`
3. **Read results**: Run `bash skills/code-review/scripts/review-read.sh` to view the latest review
   - Shows issues, suggestions, and code quality feedback
4. **Address issues**: Fix bugs, security issues, or code quality problems
5. **Re-review** (optional): Run `ada::review:task` again to verify fixes
6. **Finalize**: Run `ada::agent:finalize` to ensure code quality before committing

### PR Mode Workflow

1. **Ensure branch is ready**: Make sure all changes are committed
2. **Run review**: Execute `bash skills/code-review/scripts/review-run.sh pr`
   - CodeRabbit compares branch against main
   - Reviews all changed files in the PR
3. **Read results**: Run `bash skills/code-review/scripts/review-read.sh` to view the latest review
4. **Address issues**: Fix all critical issues before merging
5. **Finalize**: Run `ada::agent:finalize` and `bash skills/docs-check/scripts/check-docs.sh` to ensure completeness
6. **Clean up** (optional): Run `bash skills/code-review/scripts/review-cleanup.sh` to remove old review files

### Reading Review Results

Use `bash skills/code-review/scripts/review-read.sh` to display the most recent review:
- Shows review content with issues and suggestions
- Displays statistics (files reviewed, issues found)
- Lists files that were reviewed

## Examples

```bash
# Task mode
bash skills/code-review/scripts/review-run.sh task
bash skills/code-review/scripts/review-read.sh

# PR mode
bash skills/code-review/scripts/review-run.sh pr
bash skills/code-review/scripts/review-read.sh

# Complete workflow
bash skills/code-review/scripts/review-run.sh task && bash skills/code-review/scripts/review-read.sh
bash skills/code-quality/scripts/finalize.sh agent
bash skills/docs-check/scripts/check-docs.sh
```

## References

- [Documentation Guide](references/documentation-guide.md) - For when to document changes

## Output

Review results are saved to `.ada/data/reviews/` directory:
- `{type}-review-{timestamp}.md` - Review content
- `{type}-review-{timestamp}.json` - Metadata with statistics

### Integration with Other Skills

- Run `ada::code-quality` after review to ensure reviewed code meets quality standards
- Run `ada::docs:check` after review to ensure documentation is updated with code changes
- Use `ada::pr-review` to manage GitHub PR comments after CodeRabbit review

## Best Practices

- Run task reviews frequently during development
- Run PR reviews before submitting PRs
- Address review issues before finalizing
- Use `ada::review:cleanup` periodically to manage disk space
- Combine with `ada::code-quality` and `ada::docs:check` for complete workflow
