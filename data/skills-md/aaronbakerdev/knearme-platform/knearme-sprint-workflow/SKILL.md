---
name: knearme-sprint-workflow
description: Manage KnearMe portfolio development sprints. This skill should be used when starting a work session, deciding what to work on next, or tracking progress on sprint tasks. It provides guidance on sub-agent delegation and sprint file updates.
---

# KnearMe Sprint Workflow

## Overview

This skill guides development of the KnearMe Portfolio platform through 6 sprints. It ensures sprint files stay updated, progress is tracked, and sub-agents are used effectively.

**Sprint Files Location:** `knearme-portfolio/todo/`

## Starting a Work Session

1. **Check Current Sprint Status**
   ```bash
   cat knearme-portfolio/todo/README.md | grep -A 12 "Sprint Overview"
   ```

2. **Read Active Sprint File**
   - Current: `knearme-portfolio/todo/sprint-1-foundation.md`
   - Find incomplete tasks: `grep -n "\[ \]" knearme-portfolio/todo/sprint-1-foundation.md | head -10`

3. **Use TodoWrite Tool** to track session tasks from sprint file

## What to Work on Next

### Priority Order
1. **Blockers** - Tasks preventing other work
2. **Dependencies** - Earlier numbered sections before later ones
3. **Critical path** - Auth → AI → UX → SEO → Polish → Launch
4. **Quick wins** - Small tasks that unblock multiple others

### Finding Next Task
1. Open current sprint file
2. Find first unchecked `[ ]` in lowest incomplete section
3. Verify prerequisites (earlier sections done)
4. If blocked, note in "Notes" section and skip to next independent task

## Updating Sprint Progress

### During Work
- Mark tasks complete immediately: `[ ]` → `[x]`
- Add brief notes for decisions made
- Note blockers preventing completion

### End of Session
1. Commit sprint file changes
2. Update README.md if sprint status changes
3. Note next recommended task for continuity

### Sprint Completion
When all section checkboxes are done:
1. Verify "Definition of Done" criteria met
2. Update README.md: change status from 🔄 to ✅
3. Move to next sprint

## Sub-Agent Patterns

### When to Use Each Agent Type

| Agent Type | Use For |
|------------|---------|
| `Explore` | Understanding codebase, finding patterns, scoping work |
| `Plan` | Architecture decisions, multi-file changes, complex features |
| `feature-dev:code-architect` | Designing new features before implementation |
| `feature-dev:code-reviewer` | After significant code changes |
| `general-purpose` | Complex multi-step tasks |

### Sprint Task → Agent Mapping

| Sprint Task Type | Recommended Pattern |
|------------------|---------------------|
| Database schema creation | Use Supabase MCP `apply_migration` |
| New UI component | `feature-dev:code-architect` → implement |
| New API route | `Explore` existing patterns → implement → `code-reviewer` |
| Multi-file refactor | `Plan` first → parallel implementation |
| Bug fix | `Explore` root cause → fix → test |

### Parallel Agent Work

For independent sprint tasks, launch agents in parallel:
```
Agent 1: Backend/database tasks
Agent 2: Frontend components
Agent 3: Testing/documentation
```

**Example:** In Sprint 1, these can run in parallel:
- Database schema setup (Supabase MCP)
- Auth UI components (feature-dev)
- Profile setup form (feature-dev)

## Quick Reference Commands

```bash
# Check overall progress
grep -c "\[x\]" knearme-portfolio/todo/*.md   # Completed tasks
grep -c "\[ \]" knearme-portfolio/todo/*.md   # Remaining tasks

# Find next task in current sprint
grep -n "\[ \]" knearme-portfolio/todo/sprint-1-foundation.md | head -5

# Check current sprint status
head -20 knearme-portfolio/todo/README.md

# Run progress script
./.claude/skills/knearme-sprint-workflow/scripts/check_progress.sh
```

## Sprint Dependency Chain

```
Sprint 1: Foundation & Auth    ← Start here
    ↓
Sprint 2: AI Pipeline          ← Needs auth working
    ↓
Sprint 3: Core UX              ← Needs AI endpoints
    ↓
Sprint 4: Portfolio & SEO      ← Needs content to display
    ↓
Sprint 5: Polish & PWA         ← Needs features to polish
    ↓
Sprint 6: Launch               ← Final deployment
```

## Important Files

- **Sprint tracking:** `knearme-portfolio/todo/sprint-*.md`
- **Technical docs:** `knearme-portfolio/CLAUDE.md`
- **Contributor guide:** `knearme-portfolio/AGENTS.md`
- **Product specs:** `knearme-portfolio/docs/02-requirements/epics/`
- **Architecture:** `knearme-portfolio/docs/03-architecture/`

## Sprint Overview

| Sprint | Focus | Key Deliverables |
|--------|-------|------------------|
| Sprint 1 | Foundation & Auth | Next.js setup, Supabase, Auth flows, Profile setup |
| Sprint 2 | AI Pipeline | GPT-4V analysis, Whisper transcription, GPT-4o generation |
| Sprint 3 | Core UX | Photo upload, Interview flow, Editing, Publishing |
| Sprint 4 | Portfolio & SEO | Public pages, Schema.org, Sitemap, Performance |
| Sprint 5 | Polish & PWA | Service worker, Accessibility, Testing |
| Sprint 6 | Launch | Production deploy, Monitoring, Onboarding |

## Session Handoff Pattern

At the end of each session, leave a clear handoff:

```markdown
## Session Notes (YYYY-MM-DD)

### Completed
- [x] Task 1
- [x] Task 2

### In Progress
- Task 3 (started, needs X to finish)

### Blockers
- Need clarification on Y

### Next Up
- First incomplete task in sprint file
```

Add this to the sprint file's "Notes" section for continuity.
