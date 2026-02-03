---
name: use-graphite
description: "Manage stacked PRs with Graphite CLI (gt) instead of git push/gh pr create. Auto-detects Graphite repos and blocks conflicting commands with helpful alternatives. Use when: (1) About to run git push or gh pr create in a Graphite repo, (2) Creating a new branch for a feature, (3) Submitting code for review, (4) Large changes that should be split into reviewable chunks, (5) Hook blocks your git command and suggests gt equivalent. NOT for: repos not initialized with Graphite, git add/commit/status/log. Triggers: git push blocked, gh pr create blocked, create branch, submit PR, stacked PRs, split large PR, gt create, gt submit, graphite workflow."
metadata:
  author: ai-dev-atelier
  version: "1.0"
---

# Use Graphite - Stacked PRs

Graphite enables stacked PRs - chains of dependent PRs that build on each other.
Essential for large changes that would be overwhelming as single PRs.

## Assess Current State First

**Always run these commands to understand where you are:**

```bash
bash skills/use-graphite/scripts/graphite-detect.sh   # Is Graphite active?
gt log short                                           # Current stack structure
git status                                             # Uncommitted changes?
```

**Interpret the output:**

| `gt log short` shows | You are | Next action |
|---------------------|---------|-------------|
| `main` only (no branches) | Not in a stack | `gt create <branch>` to start |
| Branch with `←` marker | On that branch in stack | Continue work, then `gt submit` |
| Multiple branches in tree | Mid-stack | Check which branch, continue or `gt checkout` |
| `(merged)` on parent | Parent merged | `gt sync` to update |
| `(changes requested)` | Review feedback pending | Address feedback, commit, `gt submit` |

**If you have uncommitted changes:**
1. Commit them first: `git add . && git commit -m "..."`
2. Then submit: `gt submit` or `gt submit --stack`

**If unsure which branch you're on:** `git branch --show-current`

## Quick Start

**First, check if Graphite is active:**

```bash
bash skills/use-graphite/scripts/graphite-detect.sh
```

- `enabled: true` → Use `gt` commands for branch/PR operations
- `enabled: false` → Use standard `git`/`gh`, this skill does not apply

## Core Workflow

### Single PR

```bash
# 1. Develop and test FIRST (on current branch or main)
# make changes
# verify locally (run your project's test/lint/build commands)

# 2. THEN create branch and commit verified code
gt create my-feature
git add . && git commit -m "feat: add feature"
gt submit                       # CI should pass (you verified locally)
```

### Stacked PRs (Large Changes)

```bash
# Step 1: Develop and verify schema changes
# make schema changes, verify locally FIRST
gt create step-1-schema
git add . && git commit -m "feat(db): add schema"

# Step 2: Develop and verify API changes (on top of step-1)
# make API changes, verify locally FIRST
gt create step-2-api
git add . && git commit -m "feat(api): add endpoints"

# Step 3: Develop and verify UI changes (on top of step-2)
# make UI changes, verify locally FIRST
gt create step-3-ui
git add . && git commit -m "feat(ui): add panel"

# Submit entire stack (all layers verified)
gt submit --stack
```

**Key pattern:** Each layer follows develop → test → verify → `gt create` → commit.
Only submit when ALL layers are verified locally.

## CRITICAL: CI Must Pass

**Verify BEFORE creating branches and committing.**

Check your project for verification commands (look for `package.json` scripts, `Makefile` targets, `Cargo.toml`, `pyproject.toml`, CI config, or README). Run tests, type checks, linting, and build locally before submitting.

```text
WRONG workflow (commit-and-pray):
1. gt create feature
2. Make changes
3. Commit and gt submit → CI fails
4. Fix → gt submit → CI fails again
5. Repeat 5 times...
Result: 5 failed CI runs, broken commit history

CORRECT workflow (verify-then-commit):
1. Make changes
2. Run tests/lint/build LOCALLY
3. Fix issues until green
4. gt create feature
5. Commit verified code
6. gt submit → CI passes
Result: 1 clean submission
```

**Rule:** If local tests fail, you're not ready to commit. Fix first, verify, then create branch and commit.

## When to Stack

| Scenario | Recommendation |
|----------|----------------|
| Bug fix (< 100 lines) | Single PR |
| Feature (200-500 lines) | 2-3 stacked PRs |
| Large feature (500+ lines) | Always stack |
| Refactor + feature | Stack: refactor first |
| DB migration + code | Stack: migration first |

## DO: Best Practices

| Practice | Why |
|----------|-----|
| **Test before submit** | CI failures waste everyone's time |
| **1 logical change per PR** | Easy to review, easy to revert |
| **Stack by dependency** | schema → API → UI, not random splits |
| **Keep stacks shallow (3-5 PRs)** | Deep stacks are hard to manage |
| **Sync daily** (`gt sync`) | Avoid painful merge conflicts |
| **Use `gt modify -c`** | Not `git commit --amend` in tracked branches |

## DON'T: Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| **Submit without testing** | CI fails, blocks review | Always run tests locally first |
| **Split randomly** | PRs don't make sense alone | Split by logical dependency |
| **10-PR stacks** | Unmergeable, conflicts pile up | Max 3-5 PRs, start new stack |
| **Never sync** | Conflicts grow over time | `gt sync` daily |
| **Use git rebase** | Breaks Graphite tracking | Use `gt restack` instead |
| **Use git push** | Bypasses stack management | Use `gt submit` |
| **Tiny PRs for simple features** | Overhead without benefit | Single PR for <100 lines |

## Command Translation

| Instead of (blocked) | Use (Graphite) |
|---------------------|----------------|
| `git checkout -b feature` | `gt create feature` |
| `git push` | `gt submit` |
| `gh pr create` | `gt submit` |
| `git rebase main` | `gt restack` |
| `git commit --amend` | `gt modify -c` |

## What Graphite Does NOT Replace

Keep using these normally:
- `git add`, `git commit` - staging and committing
- `git status`, `git log`, `git diff` - inspection
- `git stash`, `git checkout <branch>` - switching, stashing

## Updating a Stack

After review feedback on an earlier PR:

```bash
gt checkout step-1-schema
# make changes, TEST LOCALLY
git add . && git commit -m "fix: address review feedback"
gt restack                      # Update dependent branches
gt submit --stack               # Push entire stack
```

## Resuming Work (After Context Loss)

If you're continuing work and unsure of the state:

```bash
# 1. Check current state
gt log short                    # See full stack structure
git status                      # Any uncommitted changes?
git log --oneline -3            # Recent commits

# 2. Common scenarios:
```

| Situation | What to do |
|-----------|------------|
| Stack exists, on correct branch | Continue work, commit, `gt submit` |
| Stack exists, wrong branch | `gt checkout <branch-name>` |
| Changes not pushed | `gt submit` (single) or `gt submit --stack` (all) |
| Need to add to existing stack | `gt create <new-branch>` (adds on top of current) |
| Stack has merge conflicts | `gt sync` then resolve conflicts |
| PRs exist but out of date | `gt sync && gt restack && gt submit --stack` |

## CRITICAL: After Submit - Validate PR Description

**`gt submit` creates PRs in draft mode with empty descriptions.** You MUST fill them.

After every `gt submit`, immediately run:

```bash
# Get the PR number from gt submit output, then:
gh pr view <PR_NUMBER> --json body --jq '.body'
```

**If the body is empty or just contains template placeholders:**

```bash
gh pr edit <PR_NUMBER> --title "feat: meaningful title" --body-file /path/to/pr-body.md
```

**What a complete PR description needs:**
- Summary of what the PR does (2-3 sentences)
- Type of change (bug fix, feature, refactor, etc.)
- How it was tested
- Files changed overview (for larger PRs)

**Never leave PRs with:**
- `Fixes # (issue)` placeholder unfilled
- Empty checkboxes with no selections
- Template comments like `<!-- What does this PR do? -->`
- Just `## Summary` headers with no content

**Workflow reminder:**

```bash
gt submit                           # Creates draft PR
gh pr view <N> --json body --jq '.body'  # Check if body is populated
# If empty/template:
gh pr edit <N> --title "..." --body "..."  # Fill it properly
```

## Emergency Fallback

If `gt` commands fail (auth expired, service down), save your work:

```bash
git add .
git commit -m "wip: saving progress"
git push origin HEAD  # BYPASS_GRAPHITE: gt service unavailable
```

The `# BYPASS_GRAPHITE: <reason>` comment is required to bypass the hook.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `gt: command not found` | `npm install -g @withgraphite/graphite-cli` |
| `Not authenticated` | `gt auth login` |
| `Branch not tracked` | `gt track` then `gt submit` |
| `Stack out of sync` | `gt restack` then `gt submit --stack` |
| `Merge conflict during sync` | Resolve conflicts, `git add`, `git rebase --continue`, then `gt sync` |
| Need to set up new repo | `gt auth login && gt repo init --trunk main` |

## Splitting a Large Commit

If you realize a commit should have been stacked:

```bash
git reset HEAD~1 --soft          # Undo commit, keep changes staged
gt create step-1-types
git add src/types/* && git commit -m "feat: add types"
gt create step-2-impl
git add src/api/* && git commit -m "feat: implement"
gt submit --stack
```

## View Stack Status

```bash
gt log short
```

```text
  main
  └── feat-schema (#234, approved)
      └── feat-api (#235, changes requested)
          └── feat-ui (#236, pending review)
```

## Scripts

| Script | Purpose |
|--------|---------|
| `graphite-detect.sh` | Check if Graphite is active |
| `graphite-block-hook.sh` | PreToolUse hook (blocks conflicting commands) |

## References

- `references/graphite-workflow.md` - Extended stacking examples, team patterns, CI integration

## Integration

| When | Related Skill | Action |
|------|---------------|--------|
| Before submit | `code-quality` | Run checks, ensure CI will pass |
| After changes | `git-commit` | Commit with proper message |
| Before PR | `code-review` | Review your changes |

## Output

Branches and PRs managed via Graphite CLI. View stack: `gt log short`.
