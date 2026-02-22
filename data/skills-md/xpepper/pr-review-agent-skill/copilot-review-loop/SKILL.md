---
name: copilot-review-loop
description: Use when you want GitHub Copilot to review a PR and automatically address its feedback within the current agent session. For any reviewer (human or bot), use pr-review-loop; for a fresh-context-per-comment approach, use ralph-wiggum-loop.
license: MIT
compatibility: Requires gh CLI. The gh-copilot-review extension is recommended (gh extension install ChrisCarini/gh-copilot-review). PR branch must be checked out locally.
metadata:
  author: Pietro Di Bello
  version: "1.1.0"
allowed-tools: Bash(gh:*)
---

# Copilot Review Loop

## Purpose

Automate an iterative Copilot-driven review loop: trigger a GitHub Copilot
review, address its feedback one comment at a time, then re-trigger Copilot
to review again. Repeat up to 2 cycles until all critical issues are resolved.

This is an **in-session** loop — one long agent context that iterates internally.
It is not the [Ralph Wiggum pattern](https://ghuntley.com/ralph/), which is an
external shell loop that spawns a fresh agent session per comment. For that,
see the `ralph-wiggum-loop` skill instead.

## Typical invocations

Users trigger this skill with prompts like:

- "Request a Copilot review on this PR and address the feedback"
- "Trigger a GitHub Copilot review and fix the issues it finds"
- "Run copilot-review-loop on PR #42"
- "Use copilot-review-loop to get and address Copilot's review comments"

## Prerequisites

- `gh` CLI (required)
- `gh-copilot-review` extension (recommended — see `references/gh-copilot-review-guide.md`)
  ```bash
  gh extension install ChrisCarini/gh-copilot-review
  ```
  Fallback if not installed: `gh pr review --request copilot`
- `pr-review-loop` skill (optional — if installed, the inner loop is delegated to it)
- The PR branch must be checked out locally

## Process

### Step 1 — Pre-flight

Inspect the project for safeguard conventions by checking these files (if they exist):
- `CLAUDE.md`, `AGENTS.md`
- `Makefile`
- `.github/workflows/`
- `README.md`

Identify all required safeguards (tests, compilation, linting, formatting, etc.).
Run all of them. If any fail, stop immediately and report — do not proceed.

### Step 2 — Outer loop (max 2 iterations)

Repeat up to 2 times:

#### 2a. Request Copilot review

Check if `gh-copilot-review` extension is installed:
```bash
gh extension list | grep copilot-review
```

If installed (preferred):
```bash
gh copilot-review [<number> | <url>]
```

If not installed (fallback):
```bash
gh pr review --request copilot
```

#### 2b. Wait for Copilot to complete

Read `references/gh-copilot-review-guide.md` for the polling approach.

Record the current count of unresolved `copilot[bot]` comments before triggering.
Poll every 30 seconds until new comments appear. If no new comments after 10 minutes,
stop and report timeout — do not proceed.

#### 2c. Collect unresolved Copilot comments

Fetch all unresolved comments authored by `copilot[bot]`. Ignore comments from
human reviewers (those are handled by the `pr-review-loop` skill).

```bash
gh api repos/{owner}/{repo}/pulls/{pr}/comments \
  --jq '.[] | select(.user.login == "copilot[bot]")'
```

Fetch all Copilot comments. Use the count recorded before triggering (step 2b) to identify which are new.

If there are no unresolved Copilot comments, stop — nothing to do.

#### 2d. Address comments — inner loop

**If `pr-review-loop` skill is available:**
Invoke the `pr-review-loop` skill, passing only the Copilot comments collected
in step 2c as the scope. It will handle triage, one-at-a-time fixes, and replies.

**If `pr-review-loop` skill is NOT available:**
Follow this process for each comment, one at a time (MUST_FIX first, then SHOULD_FIX):

Triage using the five categories defined in `references/triage-guide.md`
(MUST_FIX, SHOULD_FIX, PARK, OUT_OF_SCOPE, NEEDS_CLARIFICATION). Read that file before triaging.

For each MUST_FIX and SHOULD_FIX comment:

1. **Assess complexity:**
   - Trivial (rename, small fix): fix directly
   - Non-trivial: write plan to `.pr-review/plan-<comment-id>.md` first

2. **Run safeguards** — all must pass before touching code

3. **Fix, park, or ask for clarification**
   - Fix or park as usual.
   - If mid-assessment the intent is genuinely ambiguous: post one focused question (see format below), do **not** resolve the thread, skip steps 4–8, move on.

   **Clarification question format:**
   ```bash
   cat > /tmp/pr-review-reply-{comment_id}.md <<'EOF'
   Thanks for the feedback! Before I make a change, I want to make sure I understand what you're after:

   <one specific, focused question>
   EOF

   jq -n --rawfile body /tmp/pr-review-reply-{comment_id}.md '{body:$body}' > /tmp/pr-review-reply-{comment_id}.json

   gh api repos/{owner}/{repo}/pulls/{pull_number}/comments/{comment_id}/replies \
     --input /tmp/pr-review-reply-{comment_id}.json
   ```

   Ask exactly **one** question. Leave the thread unresolved so the reviewer's answer re-surfaces it.

4. **Run safeguards again** — all must pass

5. **Commit and push:**
   ```bash
   git add <changed files>
   git commit -m "<conventional commit describing the fix>"
   git push
   ```

6. **Reply to the comment** — explain fix, deferral, or rejection

7. **Resolve the comment on GitHub**

8. **Delete plan file** if one was created:
   ```bash
   rm .pr-review/plan-<comment-id>.md
   ```

#### 2e. Check stop conditions

Stop iterating if any of:
- No MUST_FIX Copilot comments remain after this pass
- Only OUT_OF_SCOPE or NEEDS_CLARIFICATION Copilot comments remain (awaiting reviewer input)
- This was the 10th iteration

Otherwise continue to the next iteration (back to step 2a).

### Step 3 — Summary

Post a final comment on the PR:

```
## Copilot Review Loop — Summary

Completed N Copilot review cycle(s).

### Fixed
- [commit abc1234] <description> (Copilot comment #<id>)
- ...

### Parked
- <description> — deferred, tracked in #<issue>
- ...

### Rejected
- <description> — <reason>
- ...

### Awaiting Clarification
- Asked Copilot: "<question>" — thread left open (comment #<id>)
- ...
```

Omit any section that has no entries.

## Resumability

This skill can be interrupted and restarted in a fresh context at any point.

On restart:
1. Run pre-flight (Step 1)
2. Check for an existing `.pr-review/plan-*.md` — if found, continue mid-fix from step 2d
3. Re-fetch unresolved Copilot comments — already-resolved ones won't appear
4. Continue the outer loop from the current state

## State Directory

`.pr-review/` at the repo root (should be gitignored by the project).
- `plan-<comment-id>.md` — plan for the comment currently in progress (deleted after resolution)

## Do Not

- Bundle all PR feedback into one large commit
- Make multiple unrelated changes in a single commit
- Push all changes at once without intermediate commits
- Leave Copilot comments unresolved after addressing them
- Proceed to the next Copilot review cycle if MUST_FIX items remain unresolved
