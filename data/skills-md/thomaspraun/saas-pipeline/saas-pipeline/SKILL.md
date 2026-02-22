---
name: saas-pipeline
description: "Use when starting a new SaaS project, checking project status, advancing to the next phase, viewing the project dashboard, or when the user mentions 'pipeline', 'saas-pipeline', 'next phase', 'project status', 'dashboard', 'idea to launch'. Orchestrates 28 skills across 8 phases: idea, business, product, architecture, design, implementation, deployment, marketing."
---

# SaaS Pipeline Coordinator

Coordinate, never execute. Read project state, route to the correct skill, track progress, delegate all work.

- **Explicit invocation only** - activate only when invoked
- **Stack-agnostic** - read tech stack from project's `CLAUDE.md` (`## Tech Stack`). If absent, ask before phase 4
- **Progressive disclosure** - load `references/phase-N-*.md` only when entering a phase
- **No duplication** - delegate to skills, never reimplement their work
- **Desync safety** - verify actual file existence, not just status.json claims
- **Skill-aware delegation** - MANDATORY: every subagent prompt must include a `=== READ FIRST ===` block with relevant skills (see [Skill Injection Rule](#skill-injection-rule))

---

## State Management

### Initialize

When `.claude/saas-project/` does not exist, create it with `status.json`:

```json
{
  "project_name": "<ask user>",
  "created_at": "<ISO-8601>",
  "updated_at": "<ISO-8601>",
  "current_phase": 1,
  "stack": { "frontend": "<from CLAUDE.md or null>", "backend": "<from CLAUDE.md or null>" },
  "phases": {
    "1-idea": { "status": "pending", "started_at": null, "completed_at": null, "outputs": [] },
    "2-business": { "status": "pending", "started_at": null, "completed_at": null, "outputs": [] },
    "3-product": { "status": "pending", "started_at": null, "completed_at": null, "outputs": [] },
    "4-architecture": { "status": "pending", "started_at": null, "completed_at": null, "outputs": [] },
    "5-design": { "status": "pending", "started_at": null, "completed_at": null, "outputs": [] },
    "6-implementation": { "status": "pending", "started_at": null, "completed_at": null, "outputs": [] },
    "7-deployment": { "status": "pending", "started_at": null, "completed_at": null, "outputs": [] },
    "8-marketing": { "status": "pending", "started_at": null, "completed_at": null, "outputs": [] }
  }
}
```

### Update

After each significant action, update `updated_at`, phase `status`/timestamps, `outputs` array, and `current_phase`.

---

## Router

Execute on every invocation:

### Step 1: Load State

Read `.claude/saas-project/status.json`. If missing, initialize first.

### Step 2: Classify Intent

| Intent | Action |
|--------|--------|
| "what's next" / no clear intent | Auto-route (Step 3) |
| "status" / "dashboard" | Show dashboard |
| "go to phase N" / "start phase N" | Validate prerequisites, execute |
| Specific skill name | Verify phase, delegate |
| "team" / "parallel" | Evaluate parallelism (see Agent Teams) |
| "skip to N" | Check required outputs exist, allow if yes |

### Step 3: Auto-Route

```
phase = phases[current_phase]
IF pending   → read references/phase-N-*.md, invoke first skill
IF in_progress → find next pending skill in phase, invoke it
IF completed → advance current_phase, start next
```

### Skill Injection Rule

**MANDATORY for every subagent dispatch.** Always run the scan — never skip it.

Before dispatching any agent (Task tool or Agent Team):

1. Scan `~/.claude/skills/` — match skill names/descriptions to the agent's task technology and type
2. Select up to 4-5 relevant skills
3. For each selected skill, read its SKILL.md and check for a Reference Guide table or `references/` directory. Include references whose topics match the agent's task
4. Prepend a `=== READ FIRST ===` block listing each skill's SKILL.md AND its matching references. If no skills match, dispatch without the block — not every task needs skills

```
=== READ FIRST ===
Read: ~/.claude/skills/{skill-a}/SKILL.md
Read: ~/.claude/skills/{skill-a}/references/{matching-ref}.md
Read: ~/.claude/skills/{skill-b}/SKILL.md
=== END READ ===
```

**Example — Flutter frontend implementer (skill with references):**

The flutter-expert SKILL.md has a Reference Guide table. Task involves Riverpod state and navigation → include those references:

```
Task("Implement Task 2: User dashboard screen

=== READ FIRST ===
Read: ~/.claude/skills/flutter-expert/SKILL.md
Read: ~/.claude/skills/flutter-expert/references/riverpod-state.md
Read: ~/.claude/skills/flutter-expert/references/gorouter-navigation.md
Read: ~/.claude/skills/flutter-expert/references/widget-patterns.md
Read: ~/.claude/skills/test-driven-development/SKILL.md
=== END READ ===

=== TASK ===
You are implementing Task 2: User dashboard screen
[... full task text, context, requirements ...]
=== END TASK ===
")
```

**Example — backend implementer (skill without references):**

nodejs-backend-patterns has no reference files, so only SKILL.md is needed:

```
Task("Implement Task 3: Auth module

=== READ FIRST ===
Read: ~/.claude/skills/nodejs-backend-patterns/SKILL.md
Read: ~/.claude/skills/test-driven-development/SKILL.md
=== END READ ===

=== TASK ===
You are implementing Task 3: Auth module
[... full task text, context, requirements ...]
=== END TASK ===
")
```

**When using `subagent-driven-development`:** its implementer-prompt.md does NOT include skill injection. You MUST prepend the `=== READ FIRST ===` block before the template content — the block goes at the very top, before "You are implementing Task N."

For the full scanning algorithm, see `references/skill-injection-protocol.md`.

### Dashboard

Display on status requests:

```
╔══════════════════════════════════════════════╗
║          PROJECT: {project_name}             ║
║          Stack: {frontend} + {backend}       ║
╠══════════════════════════════════════════════╣
║  Phase 1 - Idea          ████████████ 100%   ║
║  Phase 2 - Business      ████████░░░░  67%   ║
║  Phase 3 - Product       ░░░░░░░░░░░░   0%   ║
║  Phase 4 - Architecture  ░░░░░░░░░░░░   0%   ║
║  Phase 5 - Design        ░░░░░░░░░░░░   0%   ║
║  Phase 6 - Implementation░░░░░░░░░░░░   0%   ║
║  Phase 7 - Deployment    ░░░░░░░░░░░░   0%   ║
║  Phase 8 - Marketing     ░░░░░░░░░░░░   0%   ║
║                                              ║
║  Current: Phase 2 → Next: startup-biz-models ║
╚══════════════════════════════════════════════╝
```

Calculate percentage: skills completed / total skills in phase.

---

## The 8 Phases

When entering a phase, read its reference file for detailed workflow.

| # | Phase | Skills | Key Output | Exit Gate | Reference |
|---|-------|--------|------------|-----------|-----------|
| 1 | Idea | brainstorming | Design doc | Committed to repo | `references/phase-1-idea.md` |
| 2 | Business | business-model-canvas → startup-business-models | Canvas + pricing | Score >= 60, pricing defined | `references/phase-2-business.md` |
| 3 | Product | product-manager-toolkit → product-marketing-context | PRD + context | PRD with acceptance criteria | `references/phase-3-product.md` |
| 4 | Architecture | ux-flow-designer → backend-architect, ui-ux-pro-max + stack discovery | Arch docs + API contracts | Contracts defined | `references/phase-4-architecture.md` |
| 5 | Design | ui-ux-pro-max | Design system | Colors, typography, components | `references/phase-5-design.md` |
| 6 | Implementation | writing-plans → git-worktrees → {executing-plans OR subagent-dev} + TDD + debug + review + verify → finish-branch | Working code | Tests pass, review approved | `references/phase-6-implementation.md` |
| 7 | Deployment | docker-expert | Dockerfile + compose | Containers healthy | `references/phase-7-deployment.md` |
| 8 | Marketing | landing-page-copywriter, email-sequence, marketing-ideas, CRO-expert, remotion | Marketing assets | Landing + emails live | `references/phase-8-marketing.md` |

### Gateway Skills

Always invoke these before their dependent work:

| Skill | Gate For |
|-------|----------|
| brainstorming | Any creative/feature work |
| product-marketing-context | All marketing skills (phase 8) |
| test-driven-development | Implementation code (phase 6) |
| verification-before-completion | Any completion claim |

### Utility Skills (always available)

`find-skills` (discover/install), `skill-creator` (create custom), `dispatching-parallel-agents` (orchestrate teams)

---

## Agent Teams

Three parallelism opportunities via `dispatching-parallel-agents`. Always offer sequential as alternative.

Before dispatching agents, apply the [Skill Injection Rule](#skill-injection-rule). Each agent gets skills matching its domain (frontend tech skills for frontend agent, backend tech skills for backend agent, plus methodology skills like TDD).

### 1. Phases 4+5: Architecture + Design

When project has separate frontend/backend stack:
```
Agent A: backend-architect → API design, data models
Agent B: ui-ux-pro-max → UI architecture + design system
Sync: align API contracts with UI data needs
```

### 2. Phase 6: Frontend + Backend

When API contracts are defined:
```
Agent A: Frontend → implement UI against contracts (mock responses)
Agent B: Backend → implement API endpoints matching contracts
Sync: integration testing
```

### 3. Phase 8: All Marketing

All 5 skills are fully independent:
```
Agent A: landing-page-copywriter
Agent B: email-sequence
Agent C: marketing-ideas
Agent D: conversion-optimization-expert
Agent E: remotion-best-practices
```

On team acceptance: read relevant `references/`, use `dispatching-parallel-agents` to set up, give each agent project context + phase requirements.

---

## Auto-Install Missing Skills

On every invocation, verify skills for current and next phase are installed.

```
FOR each skill in current_phase:
  CHECK ~/.claude/skills/{skill-name}/ exists
  IF missing → read references/install-commands.md, inform user, offer install command, block phase if declined
```

---

## Stack-Specific Skill Discovery

Discover stack-matching skills dynamically. Never hardcode stack-to-skill mappings.

**Trigger at:**
1. Project initialization (after reading stack from CLAUDE.md)
2. Phase 4 start (before architecture work)

```
READ stack from CLAUDE.md
FOR each technology in stack:
  CHECK ~/.claude/skills/ for matching skill
  IF not found → RUN: npx skills find {technology}
  PRESENT results, OFFER install with -g -y
```

---

## Non-Linear Navigation

- **Skip ahead**: allowed if target phase's required inputs exist (phase 4 needs design doc, phase 6 needs architecture + contracts, phase 8 needs `.claude/product-marketing-context.md`)
- **Go back**: always allowed, never deletes previous outputs
- **Partial phases**: track individual skill completion; resume from last incomplete skill, not phase start

```
FOR each skill in phase.skills:
  IF output in phase.outputs → skip
  ELSE → next skill to execute
```
