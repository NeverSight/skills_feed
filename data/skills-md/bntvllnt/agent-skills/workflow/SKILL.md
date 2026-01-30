---
name: workflow
description: |
  High-velocity solo development workflow. Idea to production same-day.
  8 commands: plan, spike, ship, review, spec-review, done, drop, workflow.
  Auto-activates on: "plan", "spec", "ship", "implement", "build", "make", "write", "change",
  "refactor", "fix", "review", "check code", "review spec", "analyze spec", "challenge spec",
  "done", "finish", "complete", "drop", "abandon",
  "workflow", "what's next", "next step".
license: MIT
compatibility: "Agent-agnostic. Works with Claude Code, OpenCode, Windsurf, Cursor, Codex, Aider, or any agent supporting SKILL.md."
metadata:
  version: "1.0"
---

# Workflow

High-velocity solo development. Idea to production same-day.

## Agent Capabilities

| Capability | Used For | Required | Fallback |
|------------|----------|----------|----------|
| File read/write | Specs, config, history | Yes | — |
| Code search (grep/glob) | Discovery, context | Yes | — |
| Shell/command execution | Quality gates (lint, build, test) | Yes | List commands for user to run |
| Task/todo tracking | Phase management | Recommended | Track in spec Progress section |
| User interaction | Stuck escalation, risk flags | Recommended | Log decisions in spec Notes |
| Web/doc search | Pattern lookup | No | Use embedded patterns |

**Fallback rule:** If your agent lacks a capability, use the fallback. Never skip the workflow step — adapt the method.

## Commands

| Command | Action | Reference |
|---------|--------|-----------|
| `plan {idea}` | Create spec | [plan.md](references/actions/plan.md) |
| `spike {question}` | Time-boxed exploration | [spike.md](references/actions/spike.md) |
| `ship` / `ship {idea}` | Implement + validate | [ship.md](references/actions/ship.md) |
| `review` | Multi-perspective code review | [review.md](references/actions/review.md) |
| `spec-review` | Adversarial spec analysis | [spec-review.md](references/actions/spec-review.md) |
| `done` | Validate + retro + archive | [done.md](references/actions/done.md) |
| `drop` | Abandon, preserve learnings | [drop.md](references/actions/drop.md) |
| `workflow` | Show state + suggest next | [Status](#status-action) (below) |

No flags needed. The agent auto-detects intent from context:
- "review the spec" → manual review pause
- "skip tests" → skip test gate (documented)
- "emergency fix" → bypass spec ceremony
- "production ready" → production validation

## Flow

```
plan {idea} → ship → [implement/review/fix loop] → done
```

Quick mode (<2h): `ship {idea} → done`

## Philosophy

- **Spec-first**: All work needs a spec (creates one if missing)
- **Ship loop**: Build → review → fix until clean
- **Quality gates**: lint → typecheck → build → test (auto-detected per project)
- **Human controls deployment**: Agent codes, you push/deploy
- **Done same-day**: Scope to what ships today
- **Own planning**: Never use the host agent's built-in plan mode (EnterPlanMode, etc.). This skill writes real spec files to `specs/active/`.

## Spec Tiers

| Tier | Size | Spec | Task Tracking |
|------|------|------|---------------|
| trivial | <5 LOC | None — just do it | No |
| micro | <30 LOC | Inline comment in code | No |
| mini | <100 LOC | Spec file, minimal | Yes (if available) |
| standard | 100+ LOC | Full spec with checklist | Yes (if available) |

## Action Router

```
User input
  │
  ├─ "plan", "spec", "design"           → Load references/actions/plan.md
  ├─ "spike", "explore", "investigate"   → Load references/actions/spike.md
  ├─ "ship", "implement", "fix", "build" → Load references/actions/ship.md
  ├─ "review", "check code"              → Load references/actions/review.md
  ├─ "review spec", "analyze spec",
  │  "challenge spec"                    → Load references/actions/spec-review.md
  ├─ "done", "finish", "complete"        → Load references/actions/done.md
  ├─ "drop", "abandon"                   → Load references/actions/drop.md
  └─ "workflow", "what's next", "status" → Status Action (below)
```

**Loading rule:** Read the action file BEFORE executing. The action file contains all logic, task templates, and references needed.

## Status Action

No separate action file — logic is inline here. Detect current state, suggest next action:

```
1. Check specs/active/ for active spec
2. Check git status for uncommitted work
3. Check task list for in-progress items

State → Suggestion:
  No spec, no changes    → "Ready. Run: plan {idea}"
  Active spec, no code   → "Spec ready. Run: ship"
  Active spec, code WIP  → "In progress. Run: ship (resumes)"
  Active spec, code done → "Ready to close. Run: done"
  No spec, dirty tree    → "Uncommitted work. Run: ship (creates spec) or done"
```

Output: Follow [status-output.md](references/templates/status-output.md).

## Project Structure

```
specs/
  active/       ← Current work (0-1 specs)
  shipped/      ← Completed features
  dropped/      ← Abandoned with learnings
  history.log   ← One-line per feature shipped/dropped
```

## Configuration

All behavior is configurable by editing the skill files directly.

| What to change | Edit |
|----------------|------|
| Action logic, gates, limits | `references/actions/{action}.md` |
| Output format | `references/templates/{action}-output.md` |
| Spec structure | `references/spec-template.md` |
| Quality gate commands/levels | `references/quality-gates.md` |
| Session resume, stuck detection | `references/session-management.md` |

## References

Actions:
- [Plan](references/actions/plan.md) | [Ship](references/actions/ship.md) | [Review](references/actions/review.md) | [Spec Review](references/actions/spec-review.md) | [Done](references/actions/done.md) | [Drop](references/actions/drop.md) | [Spike](references/actions/spike.md)

Output templates:
- [Plan + Spec Review](references/templates/plan-output.md) | [Ship](references/templates/ship-output.md) | [Review](references/templates/review-output.md) | [Done](references/templates/done-output.md) | [Drop](references/templates/drop-output.md) | [Spike](references/templates/spike-output.md) | [Status](references/templates/status-output.md)

Specs & gates:
- [Spec template](references/spec-template.md) | [Quality gates](references/quality-gates.md) | [Session management](references/session-management.md) | [Memory update](references/memory-update.md)

Patterns:
- [Implementation](references/patterns/implementation.md) | [Planning](references/patterns/planning.md) | [Debugging](references/patterns/debugging.md) | [Decisions](references/patterns/decisions.md) | [Decomposition](references/patterns/decomposition.md)
