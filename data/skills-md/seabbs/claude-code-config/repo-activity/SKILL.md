---
name: repo-activity
description: Analyse GitHub repository activity including issues, PRs, contributors, and engagement
---

Analyse GitHub repository activity and current state.

## Usage
`/repo-activity [<owner/repo>]` - If no repo specified, uses current git repository.

## Analysis Sections

### Issues
- Total open/closed, by label, recently active (7d), stale (>30d), average close time

### Pull Requests
- Open PRs with review status, recently merged (7d), review turnaround, awaiting review, drafts

### Activity Metrics
- Commit frequency, active contributors (30d), code review participation, release cadence

### Detailed Summaries
- Each open issue with latest comment preview
- Each open PR with review status and changes summary

## Implementation
1. Check for repo context using `git remote -v` if no repo specified
2. Use `gh api` to fetch repository data
3. Analyse patterns in issue and PR lifecycle
4. Generate markdown report to `<repo>-activity-<date>.md`

## Auto-Exit When Standalone
**IMPORTANT**: If this command is being run as a standalone request, automatically exit after completing all phases successfully.
