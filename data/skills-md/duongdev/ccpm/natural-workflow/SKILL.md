---
name: natural-workflow
description: Guide users through CCPM's streamlined 6-command workflow (plan/work/sync/commit/verify/done). Auto-activates when users ask about starting tasks, committing changes, or completing work. Provides step-by-step guidance for the complete development lifecycle.
activation-triggers:
  - How do I start working on a task
  - How do I commit my changes
  - I'm done with my work
  - How do I save my progress
  - What's the workflow
  - Create and plan a task
  - How do I verify my changes
  - Create a pull request
  - Complete a task
  - What commands should I use
  - Walk me through the process
  - How do I use CCPM
---

# Natural Workflow Skill

Welcome to CCPM's natural workflow guide! This skill teaches you the **6-command lifecycle** that takes you from task creation to completion.

## Why Natural Workflow?

CCPM's natural workflow commands (`plan`, `work`, `sync`, `commit`, `verify`, `done`) are designed to feel **intuitive and conversational**, following the natural progression of development work:

1. **Plan** the work
2. **Work** on implementation
3. **Sync** progress to your team
4. **Commit** code changes
5. **Verify** quality
6. **Done** - complete and create PR

Instead of remembering complex command hierarchies like `/ccpm:plan`, `/ccpm:work`, or `/ccpm:done`, you use simple verbs that match how you think about work.

## The 6 Commands

### 1. `/ccpm:plan` - Create or Update Task Plans

The starting point for any work. This command intelligently detects what you want to do and helps you plan it.

**What it does:**
- Creates a new Linear task with a comprehensive implementation plan
- Plans an existing task that doesn't have a plan yet
- Updates an existing plan when requirements change

**3 Modes:**

```bash
# CREATE - New task
/ccpm:plan "Add user authentication"
/ccpm:plan "Fix login button" my-project JIRA-123

# PLAN - Plan existing task
/ccpm:plan PSN-27

# UPDATE - Change the plan
/ccpm:plan PSN-27 "Also add email notifications"
```

**Behind the scenes:**
- Auto-detects your project context
- Gathers research from Jira, Confluence, and codebase
- Generates implementation checklist (5-10 specific subtasks)
- Identifies files to modify
- Estimates complexity (low/medium/high)
- Saves everything to Linear

**Next command:** `/ccpm:work`

---

### 2. `/ccpm:work` - Start or Resume Implementation

Begin coding or resume work on an in-progress task.

**What it does:**
- Starts implementation if task is planned but not yet started
- Shows progress and next action if work is in progress
- Prevents accidental work on completed tasks

**Usage:**

```bash
# Auto-detect from branch name
/ccpm:work
# Works with branches like: feature/PSN-27-add-auth

# Explicit issue ID
/ccpm:work PSN-27
```

**START mode** (fresh task):
- Updates status to "In Progress"
- Analyzes codebase with smart agents
- Creates implementation plan in Linear
- Shows you what to do next

**RESUME mode** (continue work):
- Shows current progress (% complete)
- Lists remaining checklist items
- Suggests next action
- Shows quick command shortcuts

**Next command:** `/ccpm:sync` or `/ccpm:commit`

---

### 3. `/ccpm:sync` - Save Progress to Linear

Keep your team updated by syncing your progress to Linear.

**What it does:**
- Detects what you've changed in git
- Auto-marks checklist items as complete
- Adds progress comment to Linear
- Gives you a clear summary of work done

**Usage:**

```bash
# Auto-detect issue from branch
/ccpm:sync

# With custom summary
/ccpm:sync PSN-27 "Completed authentication endpoints"

# Auto-detect with summary
/ccpm:sync "Finished UI components"
```

**Interactive mode:**
- Shows all uncommitted changes
- AI analyzes your code changes against checklist items
- Suggests which items you completed
- Asks you to confirm (or manually select items)

**Quick sync mode:**
- If you provide a summary, skips the interactive part
- Just adds a comment with your summary
- Fast and simple

**Next command:** `/ccpm:commit`

---

### 4. `/ccpm:commit` - Create Conventional Git Commits

Make clean, meaningful git commits that follow best practices.

**What it does:**
- Auto-detects commit type (feat/fix/docs/etc) from your changes
- Generates meaningful commit message from issue context
- Links commits to Linear issues
- Follows conventional commits format

**Usage:**

```bash
# Auto-detect everything
/ccpm:commit

# With explicit message
/ccpm:commit "Add JWT token validation"

# Full conventional format
/ccpm:commit "fix(PSN-27): resolve login handler"
```

**Smart detection:**
- Extracts issue ID from your branch name
- Fetches issue title from Linear
- Analyzes changed files to determine commit type
- Generates professional commit message

**Confirmation:**
- Shows exactly what will be committed
- Lets you edit the message if needed
- Creates commit with all proper formatting

**Output:**
```
✅ Commit created successfully!
Commit: feat(PSN-27): Add user authentication
Next steps:
  /ccpm:sync        # Sync progress to Linear
  /ccpm:work        # Continue working
  git push          # Push to remote
```

**Next command:** `/ccpm:verify`

---

### 5. `/ccpm:verify` - Run Quality Checks and Verification

Before completing, make sure everything is production-ready.

**What it does:**
- Runs automated quality checks (linting, tests, build)
- Performs final code review and verification
- Identifies issues that need fixing
- Confirms work meets acceptance criteria

**Usage:**

```bash
# Auto-detect from branch
/ccpm:verify

# Explicit issue ID
/ccpm:verify PSN-27
```

**Sequential checks:**
1. **Linting** - Code style and format
2. **Tests** - Unit and integration tests pass
3. **Build** - Project builds successfully
4. **Code Review** - Final quality assessment
5. **Verification** - Acceptance criteria met

**If issues found:**
- Shows exactly what failed
- Suggests fixes
- Use `/ccpm:verify PSN-27` to get help fixing
- Run `/ccpm:verify` again once fixed

**All clear?**
- Shows "Ready for completion"
- Suggests: `/ccpm:done PSN-27`

**Next command:** `/ccpm:done`

---

### 6. `/ccpm:done` - Finalize and Create PR

Complete your work and get it ready for merge.

**What it does:**
- Creates GitHub pull request automatically
- Updates Linear status to "Done"
- Optionally syncs with Jira/Slack (with confirmation)
- Cleans up and summarizes the work

**Usage:**

```bash
# Auto-detect from branch
/ccpm:done

# Explicit issue ID
/ccpm:done PSN-27
```

**Pre-flight checks:**
1. ✅ On feature branch (not main/master)
2. ✅ All changes committed
3. ✅ Branch pushed to remote
4. ✅ Verification passed

**PR Creation:**
- Generates PR title from issue
- Creates description with checklist
- Links to related issues
- Sets reviewers if configured

**Linear Update:**
- Moves issue to "Done"
- Adds completion comment
- Closes task lifecycle

**External Sync** (if configured):
- Shows what will be posted to Slack/Jira
- Asks for explicit confirmation
- Only posts after you approve

**Next:** Your work is merged and complete!

---

## Complete Workflow Examples

### Example 1: Simple Feature (3 Commands)

**Scenario:** Adding a simple UI component

```bash
# 1. Create and plan
/ccpm:plan "Add dark mode toggle to settings"

# ... review the plan ...
# ✅ 4 subtasks
# 📁 2 files to modify
# ⚡ Complexity: Low

# 2. Start working
git checkout -b feature/PSN-30-dark-mode
/ccpm:work PSN-30

# ... write code, make commits ...
git commit -m "feat(PSN-30): add dark mode toggle"

# 3. Complete
/ccpm:verify PSN-30
/ccpm:done PSN-30

# ✅ PR created and ready for review!
```

**Time spent on CCPM:** ~2 minutes total
**Token usage:** ~15k (vs 40k+ with manual approaches)

---

### Example 2: Complex Feature with Changes (6 Commands)

**Scenario:** Adding user authentication with email notifications

```bash
# 1. Plan the work
/ccpm:plan "Add JWT authentication with email"
# Creates PSN-31 with 8 subtasks

# 2. Start implementation
git checkout -b duongdev/PSN-31-auth
/ccpm:work PSN-31

# ... write auth endpoints ...

# 3. Sync progress
/ccpm:sync PSN-31
# Shows: 3 files modified, +240 lines
# Marks checklist items complete

# 4. Continue implementation
# ... add email notifications ...

# 5. Commit changes
/ccpm:commit PSN-31
# Auto-generates: feat(PSN-31): Add JWT authentication

# 6. Fix a checklist requirement
# Realize: "Need to add password reset"
/ccpm:plan PSN-31 "Also add password reset flow"
# Updates plan, shows impact

# 7. Sync final changes
/ccpm:sync PSN-31 "Completed auth with password reset"

# 8. Verify everything
/ccpm:verify PSN-31
# ✅ Tests: 24/24 passing
# ✅ Linting: Clean
# ✅ Build: Success

# 9. Complete
/ccpm:done PSN-31
# PR created: "Add JWT authentication with email"
# Linear: Moved to Done
```

**Workflow flexibility:**
- Updated plan mid-way when requirements changed
- Synced progress multiple times
- Made meaningful commits throughout
- Verified quality before completion

---

### Example 3: Bug Fix (Abbreviated Workflow)

**Scenario:** Fixing a login button that doesn't respond to clicks

```bash
# 1. Plan quick fix
/ccpm:plan "Fix login button click handler" my-app JIRA-456

# 2. Start and complete in one session
/ccpm:work PSN-32
# ... locate the bug ...
# ... fix it ...

# 3. Commit the fix
/ccpm:commit "fix: resolve login button click handler"

# 4. Verify
/ccpm:verify PSN-32
# ✅ No regression tests
# ✅ Build passes
# ✅ Fix verified

# 5. Complete
/ccpm:done PSN-32
```

**Quick turnaround:** 15 minutes total workflow

---

## Auto-Detection Features

### Git Branch Detection

All 6 commands can auto-detect your current issue from your git branch name:

```bash
# These branch names all work:
git checkout -b feature/PSN-27-add-auth
git checkout -b duongdev/PSN-27-add-auth
git checkout -b PSN-27-authentication

# Then these work without the issue ID:
/ccpm:work          # Auto-detects PSN-27
/ccpm:sync          # Auto-detects PSN-27
/ccpm:commit        # Auto-detects PSN-27
/ccpm:verify        # Auto-detects PSN-27
/ccpm:done          # Auto-detects PSN-27
```

### Smart Context from Linear

Commands automatically fetch information from Linear:

- **Issue title** → Used in commit messages, PR titles, and summaries
- **Implementation checklist** → Updated as you sync progress
- **Team/project** → Used for proper organization
- **Status** → Updated automatically at each step

### Code Analysis

When you run `/ccpm:sync`, the system:
- Analyzes your git changes
- Matches files modified against checklist items
- Suggests which items you completed
- Pre-selects high-confidence matches

---

## Best Practices

### When to Sync

**Sync frequently** during long tasks:
- After implementing each major feature
- Before switching to a different task
- When taking a break
- Multiple times per day

```bash
# Don't wait until the end
/ccpm:sync "Completed JWT endpoints"
# ... more work ...
/ccpm:sync "Added token refresh logic"
# ... more work ...
/ccpm:sync "Implemented logout"
```

### Branch Naming for Auto-Detection

Use a consistent pattern:

```bash
# Good - includes issue ID clearly
feature/PSN-27-add-auth
duongdev/PSN-27-add-auth
PSN-27

# Also works
PSN-27-authentication
feature-PSN-27
```

### Commit Frequency

Commit often, sync progress:

```bash
# Three small commits
git commit -m "feat(PSN-27): add auth endpoints"
git commit -m "feat(PSN-27): add JWT validation"
git commit -m "feat(PSN-27): add login form"

# One sync to update checklist
/ccpm:sync "Completed auth implementation"
```

### Plan Updates During Implementation

If requirements change, update the plan:

```bash
# Original plan: Basic email notifications
/ccpm:plan PSN-31

# ... midway through, discover: Need SMS too
/ccpm:plan PSN-31 "Also add SMS notifications"

# System shows impact, you decide
# Continue with updated scope or simplify
```

### Before `/ccpm:done`

Ensure three things:
1. **All committed** - No uncommitted changes
2. **Branch pushed** - Your feature branch on remote
3. **Verification passed** - `/ccpm:verify` shows green

---

## When to Use Each Command

### Use `/ccpm:plan`
- Starting a new task
- Requirements changed mid-project
- Need to break down complex work
- Setting up clear checklist

### Use `/ccpm:work`
- Beginning implementation
- Resuming after a break
- Checking what's next in checklist
- Setting up proper context

### Use `/ccpm:sync`
- After completing a significant piece
- Multiple times during long tasks
- When switching to different work
- Before taking a break

### Use `/ccpm:commit`
- Every meaningful set of changes
- After testing locally
- When ready to push
- Before verification

### Use `/ccpm:verify`
- Before declaring work complete
- When you think all checklist items done
- Before creating PR
- To catch issues early

### Use `/ccpm:done`
- All checks passing
- Ready for code review
- Team needs to see your PR
- Task should be marked complete

---

## Integration with Other CCPM Commands

### For More Detailed Control

If you need more control than natural workflow provides:

```bash
# Instead of:
/ccpm:plan "title"

# Use detailed version:
/ccpm:plan "title" project-id jira-ticket

# Instead of:
/ccpm:work PSN-29

# Use:
/ccpm:work PSN-29

# Instead of:
/ccpm:sync PSN-29

# Use:
/ccpm:sync PSN-29 "detailed summary"

# Instead of:
/ccpm:done PSN-29

# Use:
/ccpm:done PSN-29
```

Natural workflow versions are optimized for the common path. Detailed versions provide more options.

### Utilities and Monitoring

Check your progress anytime:

```bash
# View current status
/ccpm:work PSN-29

# See what's next
/ccpm:work PSN-29

# View project progress
/ccpm:sync my-project

# Get insights
/ccpm:work PSN-29
```

---

## Error Scenarios and Recovery

### Issue Not Found

```
❌ Error fetching issue: Issue not found

Suggestions:
  - Verify the issue ID is correct (format: PROJ-123)
  - Check you have access to this Linear team
  - Ensure the issue hasn't been deleted
```

**Fix:** Double-check the issue ID and team access

### Branch Detection Failed

```
❌ Could not detect issue ID from branch

Current branch: main

Usage: /ccpm:work [ISSUE-ID]
Example: /ccpm:work PSN-29
```

**Fix:** Either:
- Rename your branch to include issue ID
- Provide issue ID explicitly: `/ccpm:work PSN-29`

### Uncommitted Changes

```
⚠️  You have uncommitted changes

Please commit first:
  /ccpm:commit
```

**Fix:** Run `/ccpm:commit` to stage and commit your changes

### Verification Failed

```
❌ Tests failed: 2 failures in __tests__/auth.test.ts

Use `/ccpm:verify PSN-29` to get help
```

**Fix:**
- Review the failure
- Fix the code
- Run tests locally
- Run `/ccpm:verify` again

---

## Common Workflows by Project Type

### Web Application (React/Node)

```bash
/ccpm:plan "Add user dashboard page"
git checkout -b feature/PSN-40-dashboard
/ccpm:work PSN-40

# ... implement React components ...
npm test                    # Test locally
/ccpm:commit               # Commit with auto-format
/ccpm:sync "UI complete"   # Update checklist

# ... implement backend API ...
/ccpm:sync "API endpoints done"
npm test && npm run build   # Verify locally
/ccpm:verify PSN-40        # Run CCPM verification
/ccpm:done PSN-40         # Create PR
```

### API/Backend Service

```bash
/ccpm:plan "Add user authentication endpoint"
git checkout -b feature/PSN-41-auth-api
/ccpm:work PSN-41

# ... implement endpoint ...
/ccpm:commit "feat: add JWT authentication"
/ccpm:sync "Auth endpoints complete"

# ... add tests ...
/ccpm:commit "test: add auth endpoint tests"
/ccpm:verify PSN-41
/ccpm:done PSN-41
```

### Documentation/Config

```bash
/ccpm:plan "Update API documentation"
git checkout -b feature/PSN-42-docs
/ccpm:work PSN-42

# ... update markdown files ...
/ccpm:commit "docs: update API docs"
/ccpm:verify PSN-42    # Builds docs, validates
/ccpm:done PSN-42     # Simpler verification for docs
```

---

## Tips for Success

1. **Plan first** - Taking 5 minutes to plan saves 30 minutes of rework
2. **Sync regularly** - Don't wait until done; update progress throughout
3. **Use meaningful commits** - Small, focused commits are easier to review
4. **Check before verifying** - Run tests locally before `/ccpm:verify`
5. **Read error messages** - They tell you exactly what's needed
6. **Take advantage of auto-detection** - Use good branch naming to save typing
7. **Ask for help** - Run commands again or use detailed versions if stuck

---

## Next Steps

Ready to start? Pick an approach:

**If you have a task to start:**
```bash
/ccpm:plan "your task description"
```

**If you're already working on something:**
```bash
/ccpm:work          # Auto-detect from branch
```

**If you just finished some work:**
```bash
/ccpm:sync          # Save progress
/ccpm:verify        # Check quality
/ccpm:done         # Complete
```

**If you need help:**
```bash
/ccpm:work PSN-29
/ccpm:work
```

---

## Summary

The natural workflow is designed to be **intuitive**, **efficient**, and **powerful**:

| Command | Purpose | Time | Tokens |
|---------|---------|------|--------|
| `/ccpm:plan` | Create & plan task | 1-2 min | ~2.5k |
| `/ccpm:work` | Start implementation | 30 sec | ~5k |
| `/ccpm:sync` | Update progress | 1 min | ~2.1k |
| `/ccpm:commit` | Make git commit | 30 sec | ~1.5k |
| `/ccpm:verify` | Quality checks | 1-2 min | ~2.8k |
| `/ccpm:done` | Complete & PR | 1 min | ~2.1k |

**Total typical workflow: 5-10 minutes, ~16k tokens** (vs 40-50 minutes, 50k+ tokens with manual approaches)

Happy shipping! 🚀
