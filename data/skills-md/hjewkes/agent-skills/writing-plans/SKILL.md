---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

# Writing Plans

## Overview

Write implementation plans as a **plan directory** — a tight orchestration plan for the coordinator plus per-task briefing files for agents. Assume agents have zero codebase context. Document everything they need: which files to touch, complete code, testing, validation criteria. DRY. YAGNI. TDD. Frequent commits.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Context:** This should be run in a dedicated worktree (created by brainstorming skill).

**Save plans to:** `.claude/plans/YYYY-MM-DD-<feature-name>/`

See [references/plan-lifecycle.md](references/plan-lifecycle.md) for directory lifecycle (creation, execution, cleanup, stale detection).

## Plan Directory Structure

```
.claude/plans/YYYY-MM-DD-<feature-name>/
  plan.md              # Orchestration plan (<200 lines)
  manifest.json        # Machine-readable task/wave metadata
  briefings/
    task-01.md         # Per-task agent briefing
    task-02.md
    ...
```

## Format Specifications

See [references/formats.md](references/formats.md) for plan.md template, manifest.json schema, and briefing authoring rules.

Briefing file template: [references/briefing-template.md](references/briefing-template.md).

## Execution Handoff

After saving the plan directory, offer execution choice:

**"Plan complete and saved to `.claude/plans/<plan-id>/`. Structure: `plan.md` (orchestration), `manifest.json` (metadata), `briefings/task-NN.md` (per-task specs). Two execution options:**

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?"**

**If Subagent-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use subagent-driven-development
- Stay in this session
- Fresh subagent per task + code review

**If Parallel Session chosen:**
- Guide them to open new session in worktree
- **REQUIRED SUB-SKILL:** New session uses executing-plans
