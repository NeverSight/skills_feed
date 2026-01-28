---
name: faion-sdd
description: "SDD workflow: specs, designs, implementation plans, quality gates."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*), Task, Skill, AskUserQuestion, TodoWrite
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# SDD Domain Skill (Orchestrator)

**Communication: User's language. Docs/code: English.**

---

## Philosophy

**"Intent is the source of truth"** - specification is the main artifact, code is just its implementation.

**No Time Estimates:** Use complexity levels (Low/Medium/High) and token estimates (~Xk) instead.

---

## Architecture

This skill orchestrates 2 sub-skills:

| Sub-Skill | Scope | Methodologies |
|-----------|-------|---------------|
| **faion-sdd-planning** | Specs, design docs, impl-plans, tasks, templates, workflows | 28 |
| **faion-sdd-execution** | Quality gates, reflexion, patterns, memory, code review, context | 20 |

**Total:** 48 methodologies

---

## Workflow Overview

```
CONSTITUTION → SPEC → DESIGN → IMPL-PLAN → TASKS → EXECUTE → DONE
      |          |        |          |          |         |        |
   project    feature  technical   100k rule   atomic   agent    learn
   principles  intent   approach   compliance   units  execution reflect
```

---

## When to Use Which Sub-Skill

### Use faion-sdd-planning for:
- Writing specifications (WHAT + WHY)
- Creating design documents (HOW)
- Breaking down implementation plans (TASKS)
- Task creation from impl-plans
- Template usage
- Workflow navigation

### Use faion-sdd-execution for:
- Task execution workflows
- Quality gate validation (L1-L6)
- Code review cycles
- Reflexion learning (PDCA)
- Pattern/mistake memory management
- Context management strategies
- Task parallelization analysis

---

## Quick Decision Tree

| If you need... | Invoke | Why |
|----------------|--------|-----|
| Write spec | faion-sdd-planning | Documentation phase |
| Write design doc | faion-sdd-planning | Documentation phase |
| Create impl-plan | faion-sdd-planning | Documentation phase |
| Create tasks | faion-sdd-planning | Documentation phase |
| Get templates | faion-sdd-planning | Templates stored there |
| Run quality gates | faion-sdd-execution | Validation phase |
| Execute tasks | faion-sdd-execution | Execution phase |
| Code review | faion-sdd-execution | Review phase |
| Learn patterns | faion-sdd-execution | Learning phase |
| Check mistakes | faion-sdd-execution | Learning phase |
| Parallelize tasks | faion-sdd-execution | Optimization phase |

---

## Directory Structure

```
.aidocs/
├── constitution.md                    # Project principles
├── contracts.md                       # API contracts
├── roadmap.md                         # Milestones
└── features/
    ├── backlog/                       # Waiting for grooming
    ├── todo/                          # Ready for execution
    ├── in-progress/                   # Being worked on
    └── done/                          # Completed
        └── {NN}-{feature}/
            ├── spec.md                # WHAT and WHY
            ├── design.md              # HOW
            ├── implementation-plan.md # Tasks breakdown
            └── tasks/
                ├── backlog/
                ├── todo/              # Ready tasks
                ├── in-progress/       # Executing
                └── done/              # Completed
```

**Lifecycle:** `backlog/ → todo/ → in-progress/ → done/`

---

## Agents

| Agent | Purpose | Sub-Skill |
|-------|---------|-----------|
| faion-task-executor-agent | Execute SDD tasks autonomously | execution |
| faion-task-creator-agent | Create detailed TASK_*.md files | planning |
| faion-sdd-reviewer-agent | Quality gate reviews | execution |
| faion-hallucination-checker-agent | Validate task completion | execution |

---

## Memory Storage

**Location:** Project-local `.aidocs/memory/` (not global)

```
.aidocs/memory/
├── patterns.md           # Learned patterns
├── mistakes.md           # Errors and solutions
├── decisions.md          # Key decisions
└── session.md            # Session state
```

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-net](../faion-net/CLAUDE.md) | Parent orchestrator |
| [faion-feature-executor](../faion-feature-executor/CLAUDE.md) | Executes SDD tasks in sequence |
| [faion-software-developer](../faion-software-developer/CLAUDE.md) | Implements code from tasks |
| [faion-product-manager](../faion-product-manager/CLAUDE.md) | Provides product specs |
| [faion-software-architect](../faion-software-architect/CLAUDE.md) | Provides design documents |

---

*faion-sdd v4.0 (Orchestrator)*
*Sub-skills: faion-sdd-planning (28) + faion-sdd-execution (20)*
