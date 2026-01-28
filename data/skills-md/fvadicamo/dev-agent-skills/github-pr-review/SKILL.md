---
name: github-pr-review
description: Handles PR review comments and feedback resolution. Use when user wants to resolve PR comments, handle review feedback, fix review comments, address PR review, check review status, respond to reviewer, or verify PR readiness. Fetches comments via GitHub CLI, classifies by severity, applies fixes with user confirmation, commits with proper format, replies to threads.
---

# GitHub PR Review

Resolves Pull Request review comments with severity-based prioritization, fix application, and thread replies.

## Quick Start

```bash
# 1. Check project-specific instructions
cat .claude/CLAUDE.md 2>/dev/null | head -50  # Review project conventions

# 2. Get PR and repo info
PR=$(gh pr view --json number -q '.number')
REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner')

# 3. Fetch and list comments by severity
gh api repos/$REPO/pulls/$PR/comments | python3 -c "
import json, sys
comments = [c for c in json.load(sys.stdin) if not c.get('in_reply_to_id')]
def sev(b): return 'CRITICAL' if 'critical' in b.lower() else 'HIGH' if 'high' in b.lower() else 'MEDIUM' if 'medium' in b.lower() else 'LOW'
for s in ['CRITICAL','HIGH','MEDIUM','LOW']:
    cs = [c for c in comments if sev(c['body'])==s]
    if cs: print(f'{s} ({len(cs)}): ' + ', '.join(f\"#{c['id]}\" for c in cs))
"

# 4. For each comment: read -> analyze -> fix -> verify -> commit -> reply
# 5. Run tests: make test (or project-specific command)
# 6. Push when all fixes verified
```

## Pre-Review Checklist

Before processing comments, verify:

1. **Project conventions**: Read `.claude/CLAUDE.md`, `.kiro/steering/`, or similar
2. **Commit format**: Check `git log --oneline -5` for project style
3. **Test command**: Identify test runner (`make test`, `pytest`, `npm test`)
4. **Branch status**: `git status` to ensure clean working tree

## Core Workflow

### 1. Fetch PR Comments

```bash
PR=$(gh pr view --json number -q '.number')
REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner')
gh api repos/$REPO/pulls/$PR/comments > /tmp/pr_comments.json
```

### 2. Classify by Severity

Process in order: CRITICAL > HIGH > MEDIUM > LOW

| Severity | Indicators | Action |
|----------|------------|--------|
| CRITICAL | `critical.svg`, "security", "vulnerability" | Must fix |
| HIGH | `high-priority.svg`, "High Severity" | Should fix |
| MEDIUM | `medium-priority.svg`, "Medium Severity" | Recommended |
| LOW | `low-priority.svg`, "style", "nit" | Optional |

### 3. Process Each Comment

For each comment:

**a. Show context**
```
Comment #123456789 (HIGH) - app/auth.py:45
"The validation logic should use constant-time comparison..."
```

**b. Read affected code and propose fix**

**c. Confirm with user before applying**

**d. Apply fix if approved**

**e. Verify fix addresses ALL issues in the comment**

### 4. Commit Changes

Use **git-commit skill** format for review fixes:

```bash
git add <files>
git commit -m "fix(scope): address review comment #ID

Brief explanation of what was wrong and how it's fixed.
Addresses review comment #123456789."
```

**Review fix commit rules** (see git-commit skill for full details):
- First line: `type(scope): subject` (max 50 chars)
- Types: `fix`, `refactor`, `security`, `test`, `style`, `perf`
- Reference the comment ID in body
- Explain what was wrong and how it's fixed

### 5. Reply to Thread

```bash
COMMIT=$(git rev-parse --short HEAD)
gh api repos/$REPO/pulls/$PR/comments \
  --input - <<< '{"body": "Fixed in '"$COMMIT"'. Replaced set lookup with hmac.compare_digest.", "in_reply_to": 123456789}'
```

**Standard Reply Templates**:

| Situation | Template |
|-----------|----------|
| Fixed | `Fixed in [hash]. [brief description of fix]` |
| Won't fix | `Won't fix: [reason - e.g., out of scope, acceptable risk]` |
| By design | `By design: [explanation of why current behavior is intentional]` |
| Deferred | `Deferred to [issue/task number]. Will address in future iteration.` |
| Acknowledged | `Acknowledged. [brief note, e.g., "acceptable for MVP"]` |

No emojis. Keep it minimal and professional.

### 6. Run Tests

```bash
make test  # or project-specific command
```

All tests must pass before pushing.

### 7. Push

```bash
git push
```

### 8. Submit Review (Optional)

After addressing all comments, formally submit a review:

```bash
# Approve the PR (use after all comments resolved)
gh pr review $PR --approve --body "All review comments addressed. Ready to merge."

# Or request changes if issues remain
gh pr review $PR --request-changes --body "Addressed X comments, Y issues remain."

# Or just comment without approval decision
gh pr review $PR --comment --body "Partial progress: fixed A and B, working on C."
```

**When to use each**:
- `--approve`: All comments addressed, PR is ready
- `--request-changes`: Critical issues remain unresolved
- `--comment`: Progress update, no approval decision yet

## Batch Commit Strategy

Organize commits by impact when addressing multiple comments:

| Change Type | Strategy |
|-------------|----------|
| Functional (CRITICAL/HIGH) | Separate commit per fix |
| Cosmetic (MEDIUM/LOW) | Single batch commit |

**Workflow:**
1. Fix CRITICAL/HIGH → separate commits each
2. Collect all cosmetic fixes
3. Apply cosmetics → single `style:` commit
4. Run tests once
5. Push all together

## Pre-Merge Checklist

Before closing/merging PR, verify (or use **github-pr-merge** skill for automated validation):

- [ ] All CRITICAL and HIGH comments addressed
- [ ] All MEDIUM comments addressed or justified skip
- [ ] Replies posted to all resolved threads
- [ ] Tests passing (`make test` or equivalent)
- [ ] Linting passing (`make lint` or equivalent)
- [ ] CI checks green (`gh pr checks`)
- [ ] No unresolved conversations

**TIP**: After resolving all comments, use the `github-pr-merge` skill to execute the merge with full pre-merge validation.

## Reply to Threads API

**Important**: Use `--input -` with JSON for `in_reply_to`:

```bash
# Correct syntax
gh api repos/$REPO/pulls/$PR/comments \
  --input - <<< '{"body": "Fixed in abc123. Brief explanation.", "in_reply_to": 123456789}'
```

**Do NOT use**: `-f in_reply_to=...` (doesn't work)

## Avoiding Review Loops

When bots review every push:

1. **Batch fixes**: Accumulate all fixes, push once
2. **Draft PR**: Convert to draft during fixes
3. **Commit keywords**: Some bots respect `[skip ci]` or `[skip review]`

## Severity Detection

**Gemini badges**:
- `critical.svg` -> CRITICAL
- `high-priority.svg` -> HIGH
- `medium-priority.svg` -> MEDIUM
- `low-priority.svg` -> LOW

**Cursor comments**:
- `<!-- **High Severity** -->` -> HIGH
- `<!-- **Medium Severity** -->` -> MEDIUM

**Fallback keywords**: "security", "vulnerability", "injection" -> CRITICAL

## Important Rules

- **ALWAYS** read project conventions (CLAUDE.md, etc.) before starting
- **ALWAYS** confirm before modifying files
- **ALWAYS** verify ALL issues in multi-issue comments are fixed
- **ALWAYS** run tests before pushing
- **ALWAYS** reply to resolved threads using standard templates
- **ALWAYS** submit formal review (`gh pr review`) after addressing all comments
- **NEVER** use emojis in commit messages or thread replies
- **NEVER** skip HIGH/CRITICAL comments without explicit user approval
- **Functional fixes** -> separate commits (one per fix)
- **Cosmetic fixes** -> batch into single `style:` commit

## Related Skills

- **git-commit** - Commit message format and conventions (use for review fix commits)
- **github-pr-merge** - Execute merge after review is complete (use after fixing all comments)
