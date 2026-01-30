---
name: objective
description: >
  This skill should be used when managing objectives - coherent goals that require 2+ plans/PRs
  to complete. Use when users want to create multi-plan tracking issues, log progress across
  related PRs, capture lessons learned, or coordinate work that spans multiple erk-plans.
  Objectives are human-first coordination documents, not executable plans.
---

# Objective Skill

## Overview

Objectives are coordination documents for goals requiring multiple plans/PRs to complete. Unlike
erk-plans (single executable implementations), objectives track progress across related work and
capture lessons learned along the way.

**Scope range:**

- Small: Feature requiring 2-3 related PRs
- Medium: Refactor spanning several plans
- Large: Long-running strategic direction emitting many plans

## Objective vs Erk-Plan

| Aspect   | Erk-Plan                         | Objective                           |
| -------- | -------------------------------- | ----------------------------------- |
| Purpose  | Single executable implementation | Coordinate 2+ related plans/PRs     |
| Scope    | One PR or tightly-coupled change | Multiple plans toward coherent goal |
| Body     | Machine-parseable metadata       | Human-readable markdown             |
| Comments | Session context dumps            | Action logs + lessons               |
| Label    | `erk-plan`                       | `erk-objective`                     |
| Tooling  | `erk plan submit/implement`      | Manual updates via comments         |

## Key Design Principles

1. **Human-first** - Plain markdown, no machine-generated metadata
2. **Incremental capture** - Each action gets its own comment
3. **Lessons as first-class** - Every action comment includes lessons learned
4. **Clear roadmap** - Status visible at a glance in the body
5. **Body stays current** - Update body when roadmap status changes
6. **Steelthread-first** - Each phase starts with minimal vertical slice proving the concept works
7. **One PR per sub-phase** - Sub-phases (1A, 1B, 1C) are sized for coherent single PRs
8. **Always shippable** - System remains functional after each merged PR
9. **Body is source of truth** - Body always contains complete current state; comments are the changelog
10. **Two-step for all changes** - Every addition (context, decisions, phases) gets a comment AND body update
11. **Context over code** - Provide references to patterns, not prescriptive implementations
12. **Session handoff ready** - Body should be self-contained for any session to pick up and implement

## Quick Reference

### Creating an Objective

```bash
gh issue create --title "Objective: [Title]" --label "erk-objective" --body "$(cat <<'EOF'
# Objective: [Title]

> [1-2 sentence summary]

## Goal

[What success looks like - concrete end state]

## Design Decisions

1. **[Decision name]**: [What was decided]

## Roadmap

### Phase 1A: [Name] Steelthread (1 PR)

Minimal vertical slice proving the concept works.

| Step | Description | Status | PR |
|------|-------------|--------|-----|
| 1A.1 | [Minimal infrastructure] | pending | |
| 1A.2 | [Wire into one command] | pending | |

**Test:** [End-to-end acceptance test for steelthread]

### Phase 1B: Complete [Name] (1 PR)

Fill out remaining functionality.

| Step | Description | Status | PR |
|------|-------------|--------|-----|
| 1B.1 | [Extend to remaining commands] | pending | |
| 1B.2 | [Full test coverage] | pending | |

**Test:** [Full acceptance criteria]

## Current Focus

**Next action:** [What should happen next]
EOF
)"
```

### Logging an Action

Post an action comment after completing work. See [format.md](references/format.md#action-comment-template) for full template.

```bash
gh issue comment <issue-number> --body "$(cat <<'EOF'
## Action: [Brief title]
**Date:** YYYY-MM-DD | **PR:** #123 | **Phase/Step:** 1A.2
### What Was Done
### Lessons Learned
### Roadmap Updates
EOF
)"
```

After posting, update the issue body (roadmap statuses, "Current Focus").

### Spawning an Erk-Plan

To implement a specific roadmap step, create an erk-plan that references the objective:

```bash
erk plan create --title "Implement [step description]" --body "Part of Objective #123, Step 1.2"
```

## Workflow Summary

1. **Create objective** - When starting multi-plan work
2. **Log actions** - After completing each significant piece of work
3. **Update body** - Keep roadmap status current
4. **Spawn erk-plans** - For individual implementation steps
5. **Close** - When goal achieved or abandoned (proactively ask when all steps done)

## Resources

### references/

- `format.md` - Complete templates, examples, and update patterns
- `workflow.md` - Creating objectives, spawning plans, steelthread structuring
- `updating.md` - Quick reference for the two-step update workflow
- `closing.md` - Closing triggers and procedures
