---
name: project-harness
description: Orchestrates long-running AI development sessions with human checkpoint control. Uses ohno for task management, manages progress tracking, routes work to appropriate skills, and implements supervised/semi-auto/autonomous modes. Use this skill when starting work sessions, resuming interrupted work, or managing multi-session projects.
---

# Project Harness

Orchestrate AI-assisted development with configurable human control.

## Core Concept

This skill bridges the gap between fully manual Claude Code sessions and runaway autonomous agents. It provides structured handoffs between sessions while giving you control over when to intervene.

**Integrated with [ohno](https://github.com/srstomp/ohno)** for task management via MCP.

```
┌─────────────────────────────────────────────────────────────┐
│                    SESSION START                            │
│                          │                                  │
│                          ▼                                  │
│              ┌──────────────────────┐                       │
│              │ ohno: get_session_   │                       │
│              │       context()      │                       │
│              └──────────┬───────────┘                       │
│                          │                                  │
│              ┌──────────────────────┐                       │
│              │ ohno serve           │◄── Browser access     │
│              └──────────┬───────────┘                       │
│                          │                                  │
│              ┌──────────────────────┐                       │
│              │ ohno: get_next_task()│                       │
│              └──────────┬───────────┘                       │
│                          │                                  │
│              ┌──────────────────────┐                       │
│              │ WORKTREE DECISION    │◄── Smart defaults     │
│              └──────────┬───────────┘                       │
│                          │                                  │
│              ┌──────────────────────┐                       │
│              │ Route to skill       │                       │
│              └──────────┬───────────┘                       │
│                          │                                  │
│              ┌──────────────────────┐                       │
│              │ CHECKPOINT (by mode) │◄── Human decision     │
│              └──────────┬───────────┘                       │
│                          │                                  │
│              ┌──────────────────────┐                       │
│              │ WORKTREE COMPLETION  │◄── Merge/PR/Keep      │
│              └──────────┬───────────┘                       │
│                          │                                  │
│              ┌──────────────────────┐                       │
│              │ ohno: done + sync    │                       │
│              │ Git commit           │                       │
│              └──────────────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

## Subagent Execution Model

Tasks are implemented by fresh subagents, not inline in the coordinator session.

### Why Subagents?

| Problem | Subagent Solution |
|---------|-------------------|
| Context degradation in long sessions | Fresh context per task |
| Accumulated assumptions | Each task starts clean |
| Token limit issues | Context discarded after task |

### Coordinator vs Implementer

| Coordinator (this session) | Implementer (subagent) |
|---------------------------|------------------------|
| Reads ohno tasks | Receives task from coordinator |
| Extracts context | Works with provided context |
| Dispatches subagents | Implements, tests, commits |
| Processes results | Reports back |
| Updates ohno | No ohno access |
| Triggers hooks | No hook access |

See [references/subagent-dispatch.md](references/subagent-dispatch.md) for details.

## Parallel Execution

When running with `--parallel N`, multiple implementers run simultaneously.

### Benefits

| Benefit | Description |
|---------|-------------|
| Throughput | N independent tasks process in ~1x time instead of Nx |
| Resource utilization | Better use of available API capacity |
| Faster feedback | Complete more work per session |

### Tradeoffs

| Tradeoff | Mitigation |
|----------|------------|
| Git conflicts | Auto-rebase, manual fallback |
| No shared learning | Agents already isolated in sequential mode |
| Higher token usage | N concurrent contexts |

### Recommended Settings

| Scenario | Parallel Count |
|----------|----------------|
| Default (safe) | 1 (sequential) |
| Independent tasks | 2-3 |
| Large backlog | 3-4 |
| Maximum | 5 |

### Dependency Handling

The ohno `blockedBy` graph is the safety mechanism:
- Tasks with unmet dependencies are not dispatched
- If Task B depends on Task A, B waits for A to complete
- No additional conflict detection - trust the dependency graph

## Quick Start

### 1. Initialize ohno

```bash
npx @stevestomp/ohno-cli init
```

### 2. Create Project Context (optional)

Create `.claude/PROJECT.md` for shared project context:

```markdown
# Project Name

## Overview
Brief description of the project.

## Tech Stack
- Framework: Next.js 14
- Database: PostgreSQL
- Styling: Tailwind CSS

## Conventions
- Use TypeScript strict mode
- Follow existing patterns in codebase
```

### 3. Start Session

Use ohno MCP tools or CLI:

```bash
# Get context from previous sessions
npx @stevestomp/ohno-cli context

# See all tasks
npx @stevestomp/ohno-cli tasks

# Get recommended next task
npx @stevestomp/ohno-cli next

# Start kanban board
npx @stevestomp/ohno-cli serve
```

---

## Operating Modes

### SUPERVISED Mode (Default)

Human reviews after every task. Maximum control, slower pace.

**Checkpoint behavior:**
- Task complete → PAUSE
- Story complete → PAUSE
- Epic complete → PAUSE

**Use when**: Starting new projects, unfamiliar domains, critical code.

### SEMI-AUTO Mode

Human reviews at story/epic boundaries. Good balance.

**Checkpoint behavior:**
- Task complete → Log and continue
- Story complete → PAUSE
- Epic complete → PAUSE

**Use when**: Established patterns, routine implementation.

### AUTONOMOUS Mode

Human reviews at epic boundaries only. Maximum speed.

**Checkpoint behavior:**
- Task complete → Skip
- Story complete → Log and continue
- Epic complete → PAUSE

**Use when**: Well-defined specs, trusted patterns, time pressure.

---

## Session Protocol

### Starting a Session

```markdown
## Session Start Checklist

1. [ ] Get session context: `ohno context` or MCP get_session_context()
2. [ ] Read .claude/PROJECT.md if exists
3. [ ] Check task list: `ohno tasks`
4. [ ] Start kanban: `ohno serve`
5. [ ] Check git status - clean working directory?
6. [ ] Get next task: `ohno next`
7. [ ] Announce plan - tell human what you'll do
```

**Using ohno MCP:**
```
1. get_session_context() → Understand previous session
2. get_tasks() → See all work
3. get_next_task() → Pick what to do
```

---

## Worktree Isolation

After getting the next task, decide whether to isolate work in a git worktree.

### Decision Priority

Evaluate in order - first match wins:

```
1. Explicit flags (from /work command arguments)
   --worktree    → Always use worktree
   --in-place    → Never use worktree

2. Smart defaults by task type
   feature, bug, spike → Worktree
   chore, docs         → In-place
   test                → Inherit from sibling tasks in story

3. Fallback
   Unknown type → Worktree (safer default)
```

### Worktree Setup

When using a worktree:

**Step 1: Check for existing story worktree**
```bash
# If task belongs to a story, check for reusable worktree
git worktree list --porcelain | grep "story-{story_id}-"
```
If found, `cd` into existing worktree and skip to task work.

**Step 2: Create new worktree**
```bash
# Generate name from task/story
NAME="task-{id}-{slug}" or "story-{story_id}-{slug}"

# Get base branch
BASE=$(git symbolic-ref refs/remotes/origin/HEAD | sed 's|refs/remotes/origin/||')

# Create worktree with new branch
git worktree add -b $NAME .worktrees/$NAME $BASE
```

**Step 3: Ensure ignored**
```bash
# Add to .gitignore if not already
echo ".worktrees/" >> .gitignore  # (check first)
```

**Step 4: Install dependencies**
```bash
cd .worktrees/$NAME

# Detect package manager and install
if [ -f bun.lockb ]; then bun install
elif [ -f pnpm-lock.yaml ]; then pnpm install
elif [ -f yarn.lock ]; then yarn install
elif [ -f package-lock.json ]; then npm install
fi
```

**Step 5: Announce and continue**
```markdown
## Worktree Setup

Creating worktree for feature task: {title}
  ✓ Branch created: task-42-user-auth
  ✓ Worktree ready at .worktrees/task-42-user-auth
  ✓ Dependencies installed (bun, 4.2s)

Ready to work.
```

### In-Place Work

When working in-place (chore/docs or `--in-place` flag):

```markdown
## Working In-Place

Chore task: {title}
Working directly on current branch (no worktree).
```

No worktree setup, no completion prompts.

---

## Worktree Completion

After a task completes (reviews pass), handle the worktree based on context.

### Task Within a Story

Commit and continue - no prompt needed:

```markdown
Task 42 complete (part of Story 12).

  ✓ Committed to story-12-user-auth branch

Story has 2 more tasks remaining.
Continue with next task? [Y/n]
```

Stay in worktree for remaining story tasks.

### Standalone Task or Story Complete

Prompt user for worktree disposition:

```markdown
[Task 42 complete / Story 12 complete]

What would you like to do?

  1. Merge to main (Recommended)
  2. Create Pull Request
  3. Keep worktree (continue later)
  4. Discard work

Which option?
```

**Option implementations:**

| Option | Commands |
|--------|----------|
| Merge | `git checkout main && git merge --no-ff {branch} && git worktree remove .worktrees/{name} && git branch -d {branch}` |
| PR | `git push -u origin {branch} && gh pr create --title "{task-title}" --body "Closes task #{id}"` |
| Keep | Do nothing - worktree remains for later |
| Discard | `git worktree remove --force .worktrees/{name} && git branch -D {branch}` |

### In-Place Completion

If working in-place, skip worktree prompts entirely. Standard commit flow only.

---

## Hook Integration

Hooks execute automatically at lifecycle points. Do not call manually.

### Work Loop with Hooks

```
[pre-session hooks]  <- Verify clean state

WHILE tasks remain:
  [pre-task hooks]   <- Check blockers

  1. Get next task (ohno next)
  2. Start task (ohno start <id>)
  3. WORKTREE DECISION         <- Smart defaults or flags
  4. Setup worktree (if needed) <- Create branch, install deps
  5. Extract task context
  6. Dispatch subagent          <- Fresh context per task
  7. Process subagent result

  [post-task hooks]  <- GUARANTEED: sync, commit

  8. WORKTREE COMPLETION        <- Merge/PR/Keep (if worktree)
  9. CHECKPOINT based on mode

[post-session hooks] <- Final sync, summary
```

### Work Loop with Hooks (Parallel)

```
[pre-session hooks]  <- Verify clean state

WHILE tasks remain:
  [pre-task hooks]   <- Check blockers (per task)

  1. Get up to N tasks (ohno)
  2. Filter by dependencies
  3. WORKTREE DECISION (per task) <- Smart defaults or flags
  4. Setup worktrees (if needed)  <- May reuse story worktrees
  5. Dispatch N subagents         <- PARALLEL: single message, N Task tools
  6. Wait for results
  7. Process each result:
     - Reviews (sequential per task)
     - Commit (may conflict)

  [post-task hooks]  <- Per completed task

  8. WORKTREE COMPLETION          <- Per task, based on context
  9. CHECKPOINT based on mode

[post-session hooks] <- Final sync, summary
```

### Hook Execution Output

When hooks run, you'll see:

```markdown
## Hooks: post-task

| Action | Status | Time |
|--------|--------|------|
| sync | ✓ | 0.3s |
| commit | ✓ | 0.5s |

Continuing...
```

### Mode-Specific Behavior

| Mode | post-task hooks |
|------|-----------------|
| supervised | sync only |
| semi-auto | sync, commit |
| autonomous | sync, commit, quick-test |

### Hook Failures

Hooks are fail-safe:
- Warnings don't stop the session
- Critical failures pause for human input
- All results logged for review

See `hooks/HOOKS.md` for configuration.

---

### During Work

For each task:

```markdown
## Task: [task-id] Create grid component

### Plan
- Create responsive grid using CSS Grid
- Support 1-4 column layouts
- Add to component library

### Implementation
[Work happens here]

### Verification
- [ ] Component renders
- [ ] Responsive breakpoints work
- [ ] Exported from index

### Post-Task
Hooks handle: sync, commit (mode-dependent)
Checkpoint triggers based on mode
```

### Ending a Session

```markdown
## Session End Checklist

1. [ ] Session notes logged via ohno
2. [ ] No broken code left
3. [ ] Clear summary of what was done
4. [ ] Clear next steps documented

*Note: post-session hooks handle final sync and summary automatically.*
```

---

## Checkpoint Protocol

### PAUSE Checkpoint

Agent stops completely and waits for human input.

```markdown
## CHECKPOINT: Task Complete

**Completed**: task-abc123 - Create grid component
**Status**: Awaiting your review
**Kanban**: http://localhost:3456 (run `ohno serve`)

### What I Did
- Created `GridLayout.tsx` component
- Added responsive breakpoints (sm, md, lg, xl)
- Exported from components/index.ts

### What I'd Do Next
- task-def456: Create dashboard header

### Your Options
1. **Continue** - Proceed to next task
2. **Modify** - Change approach before continuing
3. **Pause** - Stop session here
4. **Switch** - Work on different task

Waiting for your decision...
```

### REVIEW Checkpoint

Agent continues but flags work for later review.

```markdown
## REVIEW FLAG: Story Complete

**Completed**: Dashboard Layout (3 tasks)
**Continuing to**: Dashboard Widgets
**Kanban**: Synced ✓

Flagged for review.
```

### NOTIFY Checkpoint

Agent logs and continues without stopping.

```markdown
## ✓ Task Complete: task-abc123 - Create grid component
Kanban synced → Continuing to next task...
```

---

## Skill Routing

Based on task type, load relevant skill for domain knowledge:

| Task Type | Skill |
|-----------|-------|
| API design | api-design |
| API tests | api-testing |
| Architecture | architecture-review |
| SDK/package | sdk-development |

**Note**: Design work routes to `/design:*` commands

### Skill Invocation

When routing to a skill:

```markdown
## Invoking Skill: api-design

**Context**: Feature - API Endpoints
**Task**: task-xyz - Design user endpoints

Reading skill documentation...
[Skill takes over for this task]
```

---

## ohno Integration

### MCP Tools Available

**Query Tools:**
- `get_session_context()` - Previous session notes, blockers, in-progress tasks
- `get_project_status()` - Overall project statistics
- `get_tasks()` - List all tasks
- `get_task(id)` - Get specific task details
- `get_next_task()` - Recommended next task
- `get_blocked_tasks()` - Tasks with blockers

**Update Tools:**
- `start_task(id)` - Mark task in-progress
- `complete_task(id, notes)` - Mark task done
- `log_activity(message)` - Log session activity
- `set_blocker(id, reason)` - Block a task
- `resolve_blocker(id)` - Unblock a task

### CLI Commands

```bash
# Session management
ohno context              # Get session context
ohno status               # Project statistics

# Task management
ohno tasks                # List all tasks
ohno next                 # Get recommended next task
ohno start <id>           # Start working on task
ohno done <id> --notes    # Complete task with notes
ohno block <id> <reason>  # Set blocker
ohno unblock <id>         # Resolve blocker

# Kanban
ohno serve                # Start kanban server
ohno sync                 # Sync kanban HTML
```

---

## Error Recovery

### Build Failures

```markdown
## ⚠️ Build Failed

**Error**: TypeScript compilation error in Dashboard.tsx
**Line 47**: Property 'user' does not exist on type '{}'

### Recovery Plan
1. Check recent changes (git diff)
2. Identify breaking change
3. Fix type error
4. Verify build passes
5. Block task if needed: `ohno block <id> "Build failure"`
6. Continue or escalate

Proceeding with recovery...
```

### Blocked Tasks

```bash
# Block a task
ohno block task-abc123 "Waiting for API spec"

# View blocked tasks
ohno tasks --status blocked

# Resolve blocker
ohno unblock task-abc123
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Skipping verification | Start on broken code | Always verify first |
| No git commits | Can't recover from errors | Commit every task |
| No kanban sync | Stale visual state | Run `ohno sync` after changes |
| Giant tasks | Lose progress on failure | Keep tasks ≤8 hours |
| Ignoring checkpoints | Lose human control | Respect mode settings |
| No session context | Next session confused | Use `ohno context` |
| Autonomous on new project | Bad patterns amplified | Start supervised |

---

## References

- [references/session-protocol.md](references/session-protocol.md) — Detailed session management
- [references/checkpoint-types.md](references/checkpoint-types.md) — Checkpoint configuration
- [references/skill-routing.md](references/skill-routing.md) — Skill selection logic
