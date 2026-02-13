---
name: ship
description: Deploy approved features to production. Creates PRs, runs pre-deployment checks, and updates TASKS.md. Use after /document completes. Supports task IDs for easier invocation.
model: haiku
---

# /ship - Deployment Agent

> **Model:** haiku (scripted deployment commands)

## Command Flags

| Flag | Short | Description |
|------|-------|-------------|
| `--help` | `-h` | Show available commands and options |
| `--version` | `-v` | Show workflow skills version |

### Flag Handling

**On `-h` or `--help`:**
```
/ship - Deployment Agent

Usage:
  /ship {ID}                         Create PR for a task
  /ship -h, --help                   Show this help message
  /ship -v, --version                Show version

Arguments:
  {ID}    Task ID (number) or task filename (e.g., 001-auth-jwt)

Pre-deployment checks:
  - Build passes
  - TypeScript compiles
  - Lint passes

Creates:
  - Feature branch: feature/{ID}-{task-name}
  - Pull Request with task documentation links

Examples:
  /ship 1                            # Ship task #1
  /ship 001-auth-jwt                 # Using task filename

Next: Merge PR, then /release
```

**On `-v` or `--version`:**
Display:
```
Workflow Skills v1.4.1
https://github.com/eljun/claude-skills
```

---

## When to Use

Invoke `/ship {ID}` when:
- Task is in "Approved" status in TASKS.md
- Documentation is complete
- Ready to deploy to production

**Example:** `/ship 1` or `/ship 001-dashboard-redesign`

## Task ID Resolution

The `{ID}` can be:
- **Numeric ID:** `1`, `2`, `3` → Looks up in TASKS.md, finds matching task document
- **Padded ID:** `001`, `002` → Same as numeric
- **Full filename:** `001-dashboard-redesign` → Direct file reference

## Workflow

```
/ship {ID}
       ↓
1. Resolve task ID → find task document
2. Verify task is approved in TASKS.md
3. Check Automation field (manual | auto)
4. Move to "Ready to Ship" in TASKS.md
5. Run pre-deployment checks
6. Create/update branch (feature/{ID}-{task-name})
7. Create Pull Request (with task ID reference)
8. Update TASKS.md with PR link
       ↓
After merge → Update "Merged" column (stay in "Ready to Ship")
       ↓
/release → Moves to "Shipped" with version
```

**IMPORTANT:** Items stay in "Ready to Ship" even after merge. Only `/release` moves items to "Shipped" with the release version. This ensures proper release tracking.

## Auto Mode Behavior

When task document has `Automation: auto`:

After PR is created, the automation pipeline completes:
```
[AUTO] Pipeline complete!

Task: #{ID} - {Task Title}
Branch: feature/{ID}-{task-name}
PR: #{number} - {link}

Pre-deployment checks:
- Build: PASS
- TypeScript: PASS
- Lint: PASS

The PR is ready for your review and merge.
TASKS.md updated to "Ready to Ship"
```

**Note:** In auto mode, we still create the PR and notify you - you decide when to merge. The automation does NOT auto-merge.

## Multi-Task Commit Tracking

When shipping a task that was implemented as part of multi-task execution, commits are tracked via the `[task-{ID}]` prefix:

```bash
# Find all commits for a specific task
git log --oneline --grep="\[task-1\]"

# Example output:
# a1b2c3d [task-1] feat: Add JWT authentication middleware
# e4f5g6h [task-1] feat: Add token refresh logic
```

This allows `/ship` to:
1. Identify which changes belong to which task
2. Generate accurate PR descriptions
3. Reference specific commits in the PR body

## Pre-Deployment Checklist

**IMPORTANT — Context Efficiency:**
The task document and test report contain all the context you need. Do NOT perform broad codebase exploration. Focus only on deployment-related checks below.

### 1. Verify Approval Status

Check TASKS.md:
- Task must be in "Approved" section
- Feature doc exists
- Test report shows PASS

### 2. Review Changes

```bash
git status
git diff main...HEAD
```

Verify:
- All intended files are changed
- No unintended changes
- No sensitive files (`.env`, credentials)

### 3. Run Pre-Deployment Checks

```bash
# Build check
pnpm build

# Type check
pnpm typecheck

# Lint check
pnpm lint
```

All must pass before creating PR.

---

## Update TASKS.md

Move task to "Ready to Ship":

```markdown
## Ready to Ship

| ID | Task | Branch | PR | Merged | Task Doc |
|----|------|--------|----|--------|----------|
| 1 | Quick Actions Redesign | feature/1-quick-actions | Pending | No | [001-quick-actions.md](...) |
```

**Note:** The "Merged" column tracks merge status. Items stay here until `/release` is run.

---

## Git Workflow

### Branch Strategy

Use task ID in branch names for clarity:
```
feature/{ID}-{task-name}     - New features (e.g., feature/1-auth-jwt)
fix/{ID}-{task-name}         - Bug fixes (e.g., fix/2-login-redirect)
enhance/{ID}-{task-name}     - Enhancements (e.g., enhance/3-dashboard)
```

### If Branch Doesn't Exist

```bash
git checkout -b feature/{ID}-{task-name}
git add -A
git commit -m "[task-{ID}] feat: {description}

{Detailed description of changes}

Task: docs/task/{ID}-{task-name}.md
Test: docs/testing/{ID}-{task-name}.md

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
git push -u origin feature/{ID}-{task-name}
```

### If Branch Exists

```bash
git checkout feature/{ID}-{task-name}
git add -A
git commit -m "[task-{ID}] feat: {description}

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
git push
```

---

## Create Pull Request

Use GitHub CLI to create PR:

```bash
gh pr create --title "[Task #{ID}] {PR Title}" --body "$(cat <<'EOF'
## Summary

{2-3 bullet points describing the changes}

## Task Documentation

- **Task ID:** #{ID}
- **Task Doc:** [docs/task/{ID}-{task-name}.md](link)
- **Test Report:** [docs/testing/{ID}-{task-name}.md](link)
- **Feature Doc:** [docs/features/{feature}.md](link)

## Changes

| File | Change |
|------|--------|
| `path/to/file` | Description |

## Commits

{List commits with [task-{ID}] prefix}

## Testing

- [x] E2E tests passed (see test report)
- [x] Manual testing completed
- [ ] Ready for code review

## Screenshots

{If UI changes, include before/after}

---

Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

---

## PR Checklist

Before creating PR, verify:

### Code Quality
- [ ] Build passes (`pnpm build`)
- [ ] No TypeScript errors
- [ ] Lint passes (`pnpm lint`)
- [ ] No console.log statements
- [ ] No commented-out code

### Documentation
- [ ] Task document complete
- [ ] Test report shows PASS
- [ ] Feature documentation updated
- [ ] User guide updated (if user-facing)

### Security
- [ ] No hardcoded secrets
- [ ] No `.env` files included
- [ ] API keys not exposed
- [ ] Proper auth checks in place

### Testing
- [ ] E2E tests pass
- [ ] Manual testing done
- [ ] Edge cases handled

---

## Update TASKS.md with PR

After PR is created:

```markdown
## Ready to Ship

| ID | Task | Branch | PR | Merged | Task Doc |
|----|------|--------|----|--------|----------|
| 1 | Quick Actions Redesign | feature/1-quick-actions | [#123](link) | No | [001-quick-actions.md](...) |
```

---

## Post-Merge Actions

After PR is merged, **update the "Merged" column but keep in "Ready to Ship"**:

### 1. Update TASKS.md Merged Status

```markdown
## Ready to Ship

| ID | Task | Branch | PR | Merged | Task Doc |
|----|------|--------|----|--------|----------|
| 1 | Quick Actions Redesign | feature/1-quick-actions | [#123](link) | ✅ Jan 26 | [001-quick-actions.md](...) |
```

**IMPORTANT:** Do NOT move to "Shipped" yet. Items stay in "Ready to Ship" until `/release` is run. This allows `/release` to:
1. Know which items need to be included in the release
2. Properly track which release each feature belongs to

### 2. Update Task Document Status

Update task document to reflect merge:

```markdown
> **Status:** MERGED
> **Merged:** {Date}
> **PR:** #{number}
```

### 3. When to Run /release

After one or more items are merged, run `/release` to:
- Create versioned release with changelog
- Move ALL merged items from "Ready to Ship" to "Shipped"
- Tag each item with the release version

```markdown
## Shipped

| ID | Task | PR | Release | Shipped |
|----|------|-----|---------|---------|
| 1 | Quick Actions Redesign | [#123](link) | v1.2.0 | Jan 26 |
```

---

## Handling Issues

### Build Fails

1. Fix the build errors
2. Commit fixes
3. Re-run checks
4. Continue with PR

### PR Review Requested Changes

1. Make requested changes
2. Commit with descriptive message
3. Push to branch
4. Re-request review

### Merge Conflicts

1. Fetch latest main
2. Rebase or merge main into branch
3. Resolve conflicts
4. Push updated branch

---

## Deployment Verification

After merge, verify deployment:

### Vercel (Web)
- Check Vercel dashboard for deployment status
- Verify preview URL works
- Check production URL after deploy

---

## Rollback Procedure

If issues found in production:

1. **Quick fix:** Create hotfix branch, PR, merge
2. **Revert:** `git revert {commit}` and create PR
3. **Document:** Add to test report what was missed

---

## Summary Output

**Check the task document for `Automation: auto` field.**

### Manual Mode
```
Deployment initiated for: #{ID} - {Task Title}

Branch: feature/{ID}-{task-name}
PR: #{number} - {link}

Pre-deployment checks:
- Build: PASS
- TypeScript: PASS
- Lint: PASS

TASKS.md updated to "Ready to Ship"

Next Steps:
  1. Review and merge the PR
  2. After merging, run /release to create versioned release
```

### Auto Mode
```
[AUTO] Pipeline complete!

Task: #{ID} - {Task Title}
Automation: Full pipeline executed

Summary:
├── /task ✓ (task document created)
├── /implement ✓ (code written)
├── /test ✓ (tests passed)
├── /document ✓ (docs updated)
└── /ship ✓ (PR created)

Branch: feature/{ID}-{task-name}
PR: #{number} - {link}

Pre-deployment checks:
- Build: PASS
- TypeScript: PASS
- Lint: PASS

The PR is ready for your review and merge.
```

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| `/implement` | If fixes needed before shipping |
| `/test` | If additional testing needed |
| `/document` | If docs need updates |
| `/release` | After multiple items merged, create versioned release |

## Recommended Plugins (Install Separately)

These plugins must be installed separately. **Once installed, they MUST be invoked** — do not skip them:

| Plugin | Install From | When to Invoke |
|--------|--------------|----------------|
| `vercel-react-best-practices` | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | React/Next.js code fixes |
| `supabase-postgres-best-practices` | [supabase/agent-skills](https://github.com/supabase/agent-skills) | Database-related fixes |
