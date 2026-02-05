---
name: gh-address-comments
description: Use when you need to address GitHub PR review or issue comments on the current branch via `gh` CLI and ensure authentication is up-to-date.
---

# PR Comment Handler

Guide to find the open PR for the current branch and address its comments with gh CLI. Run all `gh` commands with elevated network access.

## When to Use
- You are working on a branch with an open GitHub PR and need to resolve review or issue comments.
- The user expects `gh` CLI automation to inspect, summarize, and fix PR comments.
- Authentication must be validated before running additional `gh` commands.

## When NOT to Use
- No PR is open for the current branch or the request is unrelated to reviews/issues.
- The work is not focused on GH PR comments (e.g., new feature coding or debugging).
- The user prefers to handle PR comments manually without `gh`.

Prereq: ensure `gh` is authenticated (for example, run `gh auth login` once), then run `gh auth status` with escalated permissions (include workflow/repo scopes) so `gh` commands succeed. If sandboxing blocks `gh auth status`, rerun it with `sandbox_permissions=require_escalated`.

## 1) Inspect comments needing attention
- Run scripts/fetch_comments.py which will print out all the comments and review threads on the PR

## 2) Ask the user for clarification
- Number all the review threads and comments and provide a short summary of what would be required to apply a fix for it
- Ask the user which numbered comments should be addressed

## 3) If user chooses comments
- Apply fixes for the selected comments

Notes:
- If gh hits auth/rate issues mid-run, prompt the user to re-authenticate with `gh auth login`, then retry.
