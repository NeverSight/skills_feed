---
name: github-pr
description: GitHub PR workflow — creating PRs, posting automated review comments, managing PR feedback cycles. Use when code is reviewed and ready for GitHub.
---

# GitHub PR Workflow

Handles the GitHub-specific stage: creating PRs, posting automated review comments, managing feedback.

## When to Use

- Code review is complete (see code-review skill) and ready for GitHub
- Need automated review comments posted to a PR
- Managing PR feedback cycles

## Automated PR Review

Post automated review comments on a GitHub PR using the orchestration prompt at [references/pr-review-orchestrator.md](references/pr-review-orchestrator.md).

**How it works:**
1. Eligibility check (skip closed, draft, trivial, already-reviewed PRs)
2. Gather CLAUDE.md files from repository
3. Summarize PR changes
4. Launch 5 parallel Sonnet agents:
   - CLAUDE.md compliance audit
   - Shallow bug scan (changes only)
   - Git blame/history context analysis
   - Previous PR comment relevance check
   - Code comment compliance check
5. Score each issue 0-100 with independent Haiku agents
6. Filter issues below 80 confidence
7. Post formatted comment to GitHub via `gh`

**Allowed tools:** `gh issue view/search/list`, `gh pr comment/diff/view/list`

## Creating PRs

See `git-workflow stack` for deciding between merge, PR, or cleanup.

## Typical Flow

1. Complete implementation
2. Self-review with code-review skill (Quick or Deep mode)
3. Fix issues found
4. Open PR (via `git-workflow stack`)
5. Run PR review orchestrator for automated GitHub review
6. Address feedback, push fixes, re-request review

## Reference Files

| Reference | Purpose |
|-----------|---------|
| [references/pr-review-orchestrator.md](references/pr-review-orchestrator.md) | Full orchestration prompt for automated PR review |
