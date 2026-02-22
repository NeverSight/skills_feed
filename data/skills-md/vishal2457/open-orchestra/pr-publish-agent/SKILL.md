---
name: pr-publish-agent
version: 1.2.0
description: Pushes the current branch, creates a PR linked to the configured tracker issue, comments the PR link on the issue, and moves the issue to In review.
---

# PR Publish Agent

## Purpose

Publish implementation work by pushing the branch, opening a PR linked to the configured tracker issue, and transitioning the issue to review.

## Runtime Configuration

- Read `/orchestra-config.json` from the repository root before starting.
- Read `issue_tracker` and use only the configured tracker MCP for ticket operations.
- Use the MCP mapped to `issue_tracker` in `orchestra-config.json`.
- If the configured issue tracker MCP is unavailable, stop immediately and do not proceed with the task.
- For every tracker comment/status update, include: `Skill-Version: pr-publish-agent@1.2.0`.
- Immediately stop if `gh` CLI is unavailable.

## When to Invoke

- After implementation is complete
- When code is ready for review

## Required Inputs

- Parent issue ID
- Parent issue URL
- Parent issue tag `implementation-done` (legacy `implemented` accepted during migration)
- Current local branch with committed changes
- Repository default base branch (for example `main`)

## Outputs

- Branch pushed to remote
- Pull request created and linked to the configured tracker issue
- Parent issue tags:
- `pr-published` when PR is created and linked
- `open-pr-publish-questions` when publish is blocked
- Parent issue comment containing PR URL
- Parent issue status moved to `In review`
- Structured parent handoff comment:

```text
Workflow-Handoff:
From: pr-publish-agent
To: pr-review-agent
Status: ready|blocked
Open-Questions: none|<question list>
Skill-Version: pr-publish-agent@1.2.0
```

## Procedure

1. Read `/orchestra-config.json` from the repository root, set the issue tracker context, and verify the configured tracker MCP is available.
2. Validate parent issue has tag `implementation-done` (or legacy `implemented`).
3. Check only prior-stage open-question signal:
- If tag `open-implementation-questions` exists, read only the latest `Workflow-Handoff` from `implementation-agent`, then stop.
4. Confirm there are committed changes on the current branch.
5. Push the current branch to origin.
6. Create a PR targeting the repository base branch.
7. Link the configured tracker issue in the PR title or PR body using the issue ID and URL.
8. Capture the PR URL.
9. If publishing is blocked (missing permissions, merge-base uncertainty, missing issue linkage):
- Add `open-pr-publish-questions`.
- Add `Workflow-Handoff` with `Status: blocked`.
- Stop and wait for clarifications.
10. If publishing is successful:
- Remove `open-pr-publish-questions` if present.
- Add tag `pr-published`.
- Add a concise parent issue comment with PR URL and short review request.
- Move parent issue status to `In review`.
- Add `Workflow-Handoff` with `Status: ready` and `Open-Questions: none`.
11. Invoke `pr-review-agent` with the same parent issue ID unless `open-pr-publish-questions` is present.

## Suggested Command Pattern

- Push branch: `git push -u origin <branch>`
- Create PR: `gh pr create --base <base-branch> --head <branch> --title "<issue-id>: <short title>" --body "Tracker: <issue-url>"`

## Guardrails

- Do not create a PR if there are no committed changes.
- Do not move issue status to `In review` until PR creation succeeds.
- Ensure the PR references the correct tracker issue ID and URL.
- Do not run tracker operations unless the MCP for the configured `issue_tracker` is available.
- Do not include raw build/lint output dumps (for example full `pnpm list` or `pnpm build` logs) in PR title/body or issue comments.
- For open-question checks, do not read full comment history; read only the previous agent's latest `Workflow-Handoff` comment.

## Handoff

Primary consumer: `pr-review-agent` (auto-invoke when unblocked).
