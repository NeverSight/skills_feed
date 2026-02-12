---
name: gainforest-beads
description: GainForest beads (`bd`) planning workflow. Activates on ALL user work requests — task planning, epic management, claiming work, closing tasks with commit links, handling blockers. Use before writing any code.
compatibility: Requires bd CLI (npm install -g @beads/bd), git repository
metadata:
  author: gainforest
  version: "1.1"
---

# GainForest Beads Planning Workflow

You are an agent working inside a team of humans and other agents. Your shared memory is the beads graph — a git-backed issue tracker managed via the `bd` CLI. Everything you plan, claim, and complete is recorded there. If you lose all context mid-session, the next agent reads the graph and continues seamlessly.

Run `bd onboard` and `bd prime` to learn the full CLI.

## When to Apply

**Every time a user asks you to do work.** Feature requests, bug fixes, refactors, investigations — all of it. Don't wait for the user to mention beads.

## Prerequisites

- `bd` CLI installed (`bd version` to verify; `npm install -g @beads/bd` to install)
- The user's GitHub handle (ask if you don't know it — you need it for every bead you create)

## How It Works: Three Phases

Everything follows three phases in strict order: **Plan, Execute, Record.** Never skip or reorder.

---

### Phase 1: Plan

**Goal:** The beads graph reflects what needs to be done before you touch any code.

#### 1a. Sync the graph

Always start here. Every session. No exceptions.

```bash
bd init --quiet
bd sync
```

#### 1b. Find or create an epic

Check if an existing epic covers the user's request:

```bash
bd list --type epic --json
```

If one fits, confirm with the user. If not, create one:

```bash
bd create "Epic: <goal>" -t epic -p <priority> --assignee <user-github-handle> --json
```

#### 1c. Break the epic into tasks

Propose a task breakdown to the user. Iterate until they approve.

```bash
bd create "<detailed task description>" -t task -p <priority> --parent <epic-id> --assignee <user-github-handle> --json
```

#### 1d. Add dependencies (only when justified)

Before adding a dependency, answer: *why can't these run in parallel?*

- Task B needs output from task A? Add it.
- Task A must be tested before B integrates? Add it.
- Same area but truly independent? Don't add one.

```bash
bd dep add <blocked-task> <blocking-task>
```

Document the reasoning in the blocked task's description.

#### 1e. Commit the plan

```bash
bd sync
git add .beads/ && git commit -m "beads: plan tasks for <epic-id>" && git push
```

This makes the plan visible to all team members and agents immediately.

---

### Phase 2: Execute

**Goal:** Work on tasks one at a time, following a strict claim-work-commit-close loop.

#### The loop (repeat for each task):

**Step 1 — Pick.** See what's unblocked:

```bash
bd ready --json
```

**Step 2 — Claim.** This tells everyone you're working on it:

```bash
bd update <task-id> --claim
bd sync
```

**Step 3 — Work.** Write code, fix bugs, whatever the task requires.

**Step 4 — Commit the code.** Include the task ID so the commit is traceable:

```bash
git add <files>
git commit -m "<what you did> (<task-id>)"
```

**Step 5 — Close the bead.** Always close *after* committing — the commit is proof of work, the close is bookkeeping:

```bash
bd close <task-id> --reason "Completed: <commit-hash>"
```

**Step 6 — Sync and push the graph:**

```bash
bd sync
git add .beads/ && git commit -m "beads: close <task-id>" && git push
```

**Step 7 — Loop back to Step 1.** Pick the next unblocked task and repeat. Never skip Steps 4-6.

---

### Phase 3: Handle Problems

**If you hit a blocker** that prevents completing the current task:

1. Mark the task as deferred with a clear explanation:
   ```bash
   bd update <task-id> --status deferred --notes "Blocked: <what went wrong and why>"
   bd sync
   git add .beads/ && git commit -m "beads: defer <task-id> — <reason>" && git push
   ```

2. Ask the user to create new beads tasks that address the blocker. Don't silently work around it.

---

## Rules at a Glance

| # | Rule | Why |
|---|------|-----|
| 1 | Sync first, always | Stale graphs cause duplicate work and conflicts |
| 2 | Plan before code | Unplanned work is invisible to the team |
| 3 | User's handle on every bead | The user owns the work, not the agent |
| 4 | Tasks must survive memory loss | A fresh agent should execute any task from its description alone |
| 5 | Reason about dependencies | Wrong deps block work; missing deps cause integration failures |
| 6 | Claim before working | Prevents two agents from doing the same task |
| 7 | Commit code, then close bead, then next task | The commit is proof; the close is bookkeeping; never skip or reorder |
| 8 | Link the commit on close | `bd close <id> --reason "Completed: <hash>"` — no exceptions |
| 9 | Git-commit `.beads/` after every graph change | This is how the team sees what's happening |
| 10 | Blockers stop work | Defer and escalate; don't silently work around problems |

## Resuming After Context Loss

```bash
bd init --quiet
bd sync
bd list --status open --status in_progress --json   # what exists?
bd ready --json                                      # what's unblocked?
bd show <id> --json                                  # read a task's full context
```

Look at `in_progress` tasks first — someone (possibly you in a past session) was working on them. The task descriptions contain everything you need to continue.

## What Makes a Good Task Description

**Bad:**
> Fix the auth bug

**Good:**
> Fix OAuth callback race condition in `app/api/oauth/callback/route.ts`. When two callbacks arrive within 100ms, the second overwrites the first session in Supabase. Add a mutex or check-and-set pattern on the `atproto_oauth_session` table. Acceptance: concurrent callback test passes. Depends on bd-a3f8.1 (session store refactor) because the fix requires the new `upsert` method.

The difference: the good description lets a stranger complete the task without asking a single question.
