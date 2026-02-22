---
name: ralph-wiggum-loop
description: Use when context window exhaustion is a concern or when addressing a large volume of PR comments — spawns a fresh agent session per comment via an external shell loop. For an in-session approach, use pr-review-loop or copilot-review-loop instead.
license: MIT
compatibility: Requires gh CLI. Works with any agent that accepts piped instructions (claude -p, codex exec, etc.). PR branch must be checked out locally.
metadata:
  author: Pietro Di Bello
  version: "1.1.0"
allowed-tools: Bash(gh:*)
---

# Ralph Wiggum Loop

## Overview

The [Ralph Wiggum pattern](https://ghuntley.com/ralph/): an external shell loop
that spawns a **fresh agent session per PR comment**. Each invocation reads a
plan file, does exactly one unit of work (triage or fix), then exits. The shell
loop handles repetition.

This avoids context window exhaustion and works with any agent.

## How to invoke

This skill is **not invoked via chat**. Instead, you run a shell loop in your
terminal — the loop pipes `CODE_REVIEW_PLAN.md` to a fresh agent session for
each iteration:

```bash
# Claude
while [ ! -f PR_REVIEW_DONE ]; do
  cat CODE_REVIEW_PLAN.md | claude -p --dangerously-skip-permissions
done

# Codex
while [ ! -f PR_REVIEW_DONE ]; do
  cat CODE_REVIEW_PLAN.md | codex exec --yolo -
done
```

See **Setup** below to get `CODE_REVIEW_PLAN.md` into your project.

## Setup (once per PR)

1. Copy `CODE_REVIEW_PLAN.md` from this skill to your project root:
   ```bash
   # Project-local install (default — installed without --global):
   cp .agents/skills/ralph-wiggum-loop/CODE_REVIEW_PLAN.md .

   # Global install (installed with --global):
   cp ~/.claude/skills/ralph-wiggum-loop/CODE_REVIEW_PLAN.md .
   ```

   The path depends on how the skill was installed. Check `.agents/skills/` first (project-local); if not found, use your global skills directory.

2. Optionally add both files to `.gitignore`:
   ```
   CODE_REVIEW_PLAN.md
   PR_COMMENTS_PLAN.md
   PR_REVIEW_DONE
   .pr-review/
   ```

3. Start the loop:

   **Claude:**
   ```bash
   while [ ! -f PR_REVIEW_DONE ]; do
     cat CODE_REVIEW_PLAN.md | claude -p --dangerously-skip-permissions
   done
   ```

   **Codex:**
   ```bash
   while [ ! -f PR_REVIEW_DONE ]; do
     cat CODE_REVIEW_PLAN.md | codex exec --yolo -
   done
   ```

   **Any agent that accepts stdin:**
   ```bash
   while [ ! -f PR_REVIEW_DONE ]; do
     cat CODE_REVIEW_PLAN.md | <agent-command>
   done
   ```

## How it works

| Iteration | `PR_COMMENTS_PLAN.md` exists? | What the agent does |
|-----------|-------------------------------|---------------------|
| 1st | No | Fetches all PR comments, triages them, writes the file |
| 2nd–N | Yes | Fixes the topmost unresolved comment, marks it done |
| Final | Yes, all resolved | Writes `PR_REVIEW_DONE`, loop terminates |

Each session is minimal: one triage pass or one comment fix.

## State files (in project root)

- `CODE_REVIEW_PLAN.md` — the instruction file (static, copied once)
- `PR_COMMENTS_PLAN.md` — triage + progress state (generated, updated each run)
- `PR_REVIEW_DONE` — written by the agent when all comments are addressed; stops the loop
- `.pr-review/plan-<id>.md` — per-comment plan for non-trivial fixes (deleted after resolution)

## Cleanup

```bash
rm -f CODE_REVIEW_PLAN.md PR_COMMENTS_PLAN.md PR_REVIEW_DONE
rm -rf .pr-review/
```

## Do Not

- Run the loop with `--dangerously-skip-permissions` on a repository you do not fully trust
- Let the loop run unattended past the first few iterations without reviewing what the agent committed
- Bundle all PR feedback into one large commit (each agent session commits at most one fix)
- Delete `PR_COMMENTS_PLAN.md` while the loop is running — this is the shared state file
