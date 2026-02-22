---
name: address-pr-comments
description: Address GitHub pull request review comments using gh CLI. Use when asked to process PR feedback, especially mixed human + AI bot reviews (for example CodeRabbit prompts), triage validity, apply fixes, and prepare concise responses with evidence.
---

# Address PR Comments

## Overview

Collect PR feedback with `gh`, classify AI/bot vs human comments, validate each comment against current code, implement only valid changes, and summarize what was addressed vs rejected.

## Workflow

Address PR comments in this order:

1. Resolve target PR.
2. Verify `gh` availability/auth.
3. Collect comments (top-level, reviews, inline).
4. Classify source (AI/bot vs human).
5. Validate each comment before changing code.
6. Apply fixes and run targeted checks.
7. Commit each resolved comment locally (no push).
8. Summarize addressed/rejected items with rationale.

## 1. Resolve PR

If user did not provide a PR number, infer from current branch:

```bash
gh pr view --json number,title,url
```

If that fails, ask the user for PR number or URL.

## 2. Verify GH CLI

```bash
gh --version
gh auth status
```

If missing or unauthenticated, stop and report the blocker clearly.

## 3. Collect Feedback

Use the helper script for normalized output:

```bash
python3 ./scripts/list_comments.py --pr <number> --json
```

The script aggregates:
- Top-level comments
- Review submissions
- Inline review comments from unresolved threads by default (including outdated unresolved threads)
- AI-prompt snippets when present in bot comments

To include resolved inline threads too:

```bash
python3 ./scripts/list_comments.py --pr <number> --json --include-resolved
```

## 4. Classify + Prioritize

Prioritize:
1. Human reviewer blocking concerns
2. High-confidence AI comments with concrete evidence
3. Lint/style/nit comments

Treat bots as advisory. Do not apply suggestions blindly.

## 5. Validate Before Fixing

Use the checklist in `references/validation-checklist.md`.

Mark each comment as one of:
- `valid`
- `invalid`
- `already_fixed`
- `out_of_scope`
- `needs_clarification`

For AI bot comments containing a "Prompt for AI Agents" block, parse and verify each requested change against current files and repo conventions before editing.

## 6. Implement + Verify

Apply fixes one validated comment at a time.

Run checks relevant to changed files only, scoped to the modified paths (e.g., type checks, linting, tests).

## 7. Commit Each Resolved Comment (No Push)

For every `valid` comment you resolve:

1. Stage only the files needed for that single comment.
2. Examine recent commits (`git log --oneline -10`) to understand the repository's commit message style. If a commit message generation skill is installed, use it. Otherwise, write a concise commit message from the staged diff that follows the same conventions.
3. Create exactly one local commit for that resolved comment.
4. Do **not** push.

Rules:
- Do not combine multiple resolved comments into one commit unless technically inseparable.
- If inseparable, note all linked comment URLs in your final report for that commit.
- Do not commit comments marked `invalid`, `already_fixed`, `out_of_scope`, or `needs_clarification`.

## 8. Report Back

Provide:
- Addressed comments (with file references and commit hashes)
- Rejected comments (with reason)
- Any unclear comments that need reviewer clarification
- What checks were run and results

## Quick Commands

```bash
# Current branch PR
gh pr view --json number,title,url

# Structured comment dump
python3 ./scripts/list_comments.py --json

# Structured comment dump for a specific PR
python3 ./scripts/list_comments.py --pr <number> --json

# Include resolved inline threads
python3 ./scripts/list_comments.py --pr <number> --json --include-resolved

# Per-comment local commit workflow (no push)
git add <files-for-one-comment>
git diff --staged --stat
git commit -m "<conventional-commit-message>"
# DO NOT: git push
```
