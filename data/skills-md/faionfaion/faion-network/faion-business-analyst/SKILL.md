---
name: faion-business-analyst
description: "Business analysis: requirements engineering, stakeholder analysis, process modeling."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*), Task, AskUserQuestion, TodoWrite
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# BA Domain Skill

**Orchestrator for Business Analysis Framework (BABOK) practices**

---

## Architecture

```
faion-business-analyst (orchestrator)
├── faion-business-analyst:core (21 methodologies)
│   ├── Planning & Governance
│   ├── Elicitation
│   ├── Requirements Lifecycle
│   ├── Strategy Analysis
│   ├── Solution Evaluation
│   └── Modern Practices
└── faion-business-analyst:modeling (7 methodologies)
    ├── Behavioral Models (use cases, user stories)
    ├── Process Models (BPMN)
    ├── Data Models (ERD)
    ├── Decision Models (business rules)
    ├── Interface Models
    └── Validation Models (acceptance criteria)
```

---

## Quick Decision

| If you need... | Sub-Skill | Key File |
|----------------|-----------|----------|
| Define BA approach | ba-core | ba-planning.md |
| Map stakeholders | ba-core | stakeholder-analysis.md |
| Gather requirements | ba-core | elicitation-techniques.md |
| Track/prioritize requirements | ba-core | requirements-traceability.md, requirements-prioritization.md |
| Analyze strategy | ba-core | strategy-analysis.md |
| Evaluate solution | ba-core | solution-assessment.md |
| Model user interactions | ba-modeling | use-case-modeling.md, user-story-mapping.md |
| Map processes | ba-modeling | business-process-analysis.md |
| Model data | ba-modeling | data-analysis.md |
| Define business rules | ba-modeling | decision-analysis.md |
| Design interfaces | ba-modeling | interface-analysis.md |
| Write acceptance criteria | ba-modeling | acceptance-criteria.md |

---

## 6 Knowledge Areas

| # | Knowledge Area | Focus | Sub-Skill |
|---|----------------|-------|-----------|
| 1 | BA Planning & Monitoring | Approach, stakeholders, governance | ba-core |
| 2 | Elicitation & Collaboration | Gather information | ba-core |
| 3 | Requirements Lifecycle | Trace, maintain, prioritize | ba-core |
| 4 | Strategy Analysis | Current/future state, gaps | ba-core |
| 5 | Requirements Analysis & Design | Model, verify, validate | ba-modeling |
| 6 | Solution Evaluation | Measure, assess, improve | ba-core |

---

## Sub-Skills

### faion-business-analyst:core (21 files)
Planning, elicitation, requirements lifecycle, strategy, evaluation, modern practices

**Location:** `~/.claude/skills/faion-business-analyst:core/`

### faion-business-analyst:modeling (7 files)
Use cases, user stories, BPMN, ERD, decision tables, interfaces, acceptance criteria

**Location:** `~/.claude/skills/faion-business-analyst:modeling/`

---

## Navigation

- Main orchestrator: This file
- Detailed overview: [CLAUDE.md](CLAUDE.md)
- Knowledge Areas: [knowledge-areas-detail.md](knowledge-areas-detail.md)
- References: [ref-CLAUDE.md](ref-CLAUDE.md)

---

*BA Domain Skill v3.0 | 28 Methodologies | 2 Sub-Skills | 6 Knowledge Areas*
