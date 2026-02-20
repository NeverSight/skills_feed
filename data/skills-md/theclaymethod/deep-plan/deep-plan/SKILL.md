---
name: deep-plan
description: Structured research → plan → annotate → implement workflow for non-trivial features. Separates planning from execution using persistent markdown artifacts (.claude/research.md, .claude/plan.md). Use when explicitly invoked via /deep-plan for feature development, refactors, migrations, or any multi-file change where architecture decisions matter.
license: MIT
metadata:
  author: claytonkim
  version: "1.0.0"
---

# Deep Plan

Disciplined workflow that prevents wasted effort by separating thinking from typing. Never write code until the user has reviewed and approved a written plan.

## Workflow

```
Research → Plan → [Interview] → Annotate (1-6x) → Todo List → Implement → Feedback → Archive
```

`[Interview]` is optional — an interactive Q&A to resolve ambiguities before annotation. See Phase 2 reference for triggers and process.

**Critical guard**: Do NOT advance to the next phase unless the user explicitly says to. When in doubt, ask.

## Phases

Each phase has detailed instructions in its reference file. Read the relevant file when entering that phase.

| Phase | File | Artifact | Guard |
|-------|------|----------|-------|
| 1. Research | [references/phase-1-research.md](references/phase-1-research.md) | `.claude/research.md` | Wait for user review |
| 2. Plan | [references/phase-2-plan.md](references/phase-2-plan.md) | `.claude/plan.md` | Do not implement yet |
| 3. Annotate | [references/phase-3-annotate.md](references/phase-3-annotate.md) | User edits plan.md | Do not implement yet |
| 4. Todo List | [references/phase-4-todo.md](references/phase-4-todo.md) | Checkboxes in plan.md | Wait for user approval |
| 5. Implement | [references/phase-5-implement.md](references/phase-5-implement.md) | Mark tasks `[x]` | Run typecheck continuously |
| 6. Feedback | [references/phase-6-feedback.md](references/phase-6-feedback.md) | Terse corrections | Revert if directionally wrong |
| 7. Archive | [references/phase-7-archive.md](references/phase-7-archive.md) | `docs/completed-tasks/` | — |

## Templates

Use these when creating artifacts:
- Research: `assets/templates/research-template.md`
- Plan: `assets/templates/plan-template.md`

## Scripts

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `scripts/check_annotations.py <file>` | Find unaddressed user annotations | Before updating plan in Phase 3 |
| `scripts/plan_progress.py <file>` | Report task completion (X/Y) | During Phase 5 implementation |
| `scripts/archive_plan.py <file> --name <slug>` | Move plan to docs/completed-tasks/ | Phase 7 archive |

## Reference Files

| File | Purpose |
|------|---------|
| `references/annotation-guide.md` | How users write effective annotations |
| `references/phase-*.md` | Detailed instructions per phase |

## Hard Constraints

These are non-negotiable. Violating any of these is a workflow failure.

| Constraint | Applies To |
|------------|------------|
| **Never write code without an approved plan.** No exceptions. | All phases |
| **"Don't implement yet" is absolute.** Do not start coding during research, planning, or annotation phases, even if the plan looks complete. | Phases 1-4 |
| **All research goes into a persistent file.** Never summarize findings only in chat. Write `.claude/research.md`. | Phase 1 |
| **Read source files before proposing changes.** Every code snippet in the plan must reference real files you've actually read. Never design in a vacuum. | Phase 2 |
| **Address every annotation.** Do not skip, deprioritize, or silently drop any user note. | Phase 3 |
| **Do not use `any` or `unknown` types.** Maintain strict typing throughout. | Phase 5 |
| **Do not add unnecessary comments or jsdocs.** Code should be self-documenting. | Phase 5 |
| **Run typecheck continuously.** Catch problems during implementation, not after. | Phase 5 |
| **Do not stop until all tasks are completed.** Don't pause mid-implementation for confirmation unless blocked. | Phase 5 |
| **Mark tasks complete in the plan as you go.** The plan document is the single source of truth for progress. | Phase 5 |
| **Scope is what the plan says.** If the user cut something, it stays cut. Don't sneak it back in. Don't add unrequested features. | All phases |

## Key Principles

- **The plan is shared mutable state.** Both you and the user edit it. It persists across compaction.
- **Single long sessions.** Research through implementation in one conversation.
- **Implementation should be boring.** Creative decisions happen in annotation cycles.
- **Never speculate about unread code.** If the plan references a file, read it first.
- **Scope discipline.** If the user cuts something from the plan, it's cut. Don't sneak it back in.

## Credit

This workflow is based on [How I Use Claude Code](https://boristane.com/blog/how-i-use-claude-code/) by [Boris Tane](https://boristane.com).
