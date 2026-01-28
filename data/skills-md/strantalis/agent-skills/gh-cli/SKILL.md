---
name: gh-cli
description: Standardize all GitHub interactions via the GitHub CLI (`gh`) instead of ad-hoc URLs, UI clicks, or direct REST API calls. Use when you need to read or change GitHub state (repos, issues, pull requests, reviews, check status, Actions workflows/runs, releases, labels, milestones, discussions, gists) and want deterministic output (prefer `--json` + `--jq`). Also use when the user provides a GitHub URL, including deep links like `https://github.com/OWNER/REPO/pull/123`, `.../issues/123`, `.../pull/123/files`, or comment permalinks like `#issuecomment-...`, and you need to fetch the underlying PR/issue/thread and reply. Fall back to `gh api` only when there is no first-class `gh NOUN VERB` command.
---

# GitHub `gh` CLI

## Overview

Use `gh` for GitHub operations with explicit repo targeting, JSON output, and command help-driven discovery of flags/fields. Avoid scraping human-readable output and avoid raw REST calls unless you must (use `gh api` as the controlled fallback).

## Quick start

1. Verify `gh` is installed and authenticated:

```bash
gh --version
gh auth status
```

2. Set explicit repo context (preferred patterns):

```bash
# One-off: target a repo explicitly
gh issue list -R OWNER/REPO --json number,title,url -q '.[] | "\(.number)\t\(.title)\t\(.url)"'

# Repeated work: set a default repo for this shell + directory context
gh repo set-default OWNER/REPO
```

## Operating rules (do not skip)

1. Prefer first-class commands over APIs.
   - Use `gh issue`, `gh pr`, `gh repo`, `gh run`, `gh workflow`, `gh release`, etc.
   - Use `gh api` only when the CLI lacks a dedicated command (document the endpoint and why).

2. Avoid guessing flags/fields; discover them.
   - Use `gh <command> --help` to find flags and supported `--json` fields.
   - Use `gh help formatting` for `--json`, `--jq`, and `--template` patterns.

3. Prefer machine-readable output.
   - Use `--json <fields> -q '<jq>'` instead of parsing table output.
   - When you need just one value, return only that value (not the full blob).

4. Make repo targeting explicit.
   - Prefer `-R OWNER/REPO` when not operating in a known local checkout.
   - If you infer repo from the current directory, confirm it via `gh repo view --json nameWithOwner -q .nameWithOwner`.

5. Treat state changes as production-impacting.
   - Ask for confirmation before creating/closing/merging/deleting.
   - When modifying settings (branch protections, permissions), make changes small and reversible.

## Common tasks (command-first)

Use `skills/gh-cli/references/gh-commands.md` for a categorized command reference with examples for:
- Repos (view/clone/fork/create, defaults, settings)
- Issues (list/view/create/edit/comment/close/reopen)
- PRs (list/view/create/checkout/review/merge/status/checks, review threads/comments, reply workflows)
- Actions (workflows/runs: list/view/watch/rerun/cancel)
- Releases (list/view/create/download)
- Search patterns and deterministic selection
- `gh api` fallback patterns (REST + GraphQL) when required

## Tooling

Run a quick environment/context capture when debugging auth/repo targeting problems:

```bash
./skills/gh-cli/scripts/gh_context.sh
```

This prints `gh` version/auth status and tries to identify the active repo (when run inside a checkout).

Fetch a PR’s review feedback (reviews + PR comments + inline review comments + review threads) as JSON:

```bash
./skills/gh-cli/scripts/pr_feedback.sh -R OWNER/REPO 123
```

Reply back to review feedback:

```bash
# Reply to an inline review comment (REST)
./skills/gh-cli/scripts/pr_review_comment_reply.sh -R OWNER/REPO 123 987654321 --body "Thanks — fixed in 8c0ffee."

# Reply to a review thread (GraphQL)
./skills/gh-cli/scripts/pr_review_thread_reply.sh PRRT_kwDO... --body "Good catch — updated to handle nil."
```
