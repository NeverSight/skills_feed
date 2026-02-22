---
name: miro-code-review
description: Knowledge and patterns for effective code review visualization
---

# Code Review Skill

This skill provides knowledge and patterns for conducting effective code reviews with visual outputs on Miro boards.

## Core Concepts

### Review Philosophy

Effective code reviews focus on:
1. **Correctness** - Does the code do what it's supposed to?
2. **Security** - Are there vulnerabilities or data exposures?
3. **Maintainability** - Can others understand and modify this code?
4. **Performance** - Are there efficiency concerns?
5. **Consistency** - Does it follow project conventions?

### Visual Review Benefits

Creating visual artifacts helps:
- **Async collaboration** - Reviewers can engage at their own pace
- **Context preservation** - Related docs and diagrams in one place
- **Discussion tracking** - Comments attached to specific items
- **Knowledge sharing** - Junior devs learn from visual explanations

## Risk Assessment Framework

Use the references in this skill for detailed risk assessment criteria:
- `references/risk-assessment.md` - File and change risk scoring
- `references/review-patterns.md` - Common review patterns and anti-patterns

## Visualization Patterns

### When to Use Each Artifact

| Artifact | Best For |
|----------|----------|
| **Table** | File lists, structured comparisons, status tracking |
| **Document** | Summaries, detailed analysis, checklists |
| **Flowchart** | Process flows, decision trees, bug fix context |
| **Class Diagram** | Structural changes, refactoring, OOP patterns |
| **Sequence Diagram** | API interactions, message flows, integrations |
| **ER Diagram** | Database changes, data model updates |

### Layout Guidelines

```
┌─────────────────────────────────────────────────────────┐
│                    MIRO BOARD LAYOUT                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  x=-2000          x=0              x=2000      x=4000   │
│  ┌─────────┐      ┌─────────┐      ┌─────────┐         │
│  │ Summary │      │  Table  │      │ Diagram │  y=0    │
│  │   Doc   │      │ (files) │      │  (arch) │         │
│  └─────────┘      └─────────┘      └─────────┘         │
│                                                         │
│  ┌─────────┐                       ┌─────────┐         │
│  │ Detail  │                       │ Diagram │  y=1500 │
│  │   Doc   │                       │ (flow)  │         │
│  └─────────┘                       └─────────┘         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

