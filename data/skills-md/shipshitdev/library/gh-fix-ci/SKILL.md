---
name: gh-fix-ci
description: Inspect GitHub PR checks with gh, pull failing GitHub Actions logs, summarize failure context, then create a fix plan and implement after user approval. Use when a user asks to debug or fix failing PR CI/CD checks on GitHub Actions and wants a plan plus code changes; for external checks (e.g., Buildkite), only report the details URL and mark them out of scope.
---

# GH Fix CI

Use this skill to diagnose failing GitHub Actions checks on a PR and propose a fix plan.

## Workflow

1) Verify auth:
   - `gh auth status -h github.com`
2) Identify the PR:
   - `gh pr view --json number,title,url`
   - If no PR is found, ask for the PR URL.
3) List checks:
   - `gh pr checks`
4) For GitHub Actions failures, fetch logs:
   - `gh run view <run-id> --log`
   - If you only have a job id: `gh run view --job <job-id> --log`
5) Summarize the root cause and impacted files.
6) Propose a fix plan and get user approval before changing code.
7) For external checks (non-GitHub Actions), report the details URL and mark as out of scope.

## Notes

- Do not rerun CI unless the user asks.
- Keep the failure summary concise and actionable.
