---
name: aidlc
description: "AI-DLC (AI-Driven Development Life Cycle) workflow orchestration. Use when user says 'Using AI-DLC' or needs structured software development with requirements, design, and implementation through Inception, Construction, and Operations phases."
license: MIT
metadata:
  author: konippi
  version: "1.0.0"
---

# AI-DLC Core Workflow

AI-DLC is an adaptive software development workflow that intelligently tailors itself to your specific needs.

## Activation Triggers

Use this skill when:
- User request starts with "Using AI-DLC, ..."
- Complex software development requiring structured planning
- Projects needing requirements analysis, design, and implementation

## MANDATORY: Rule Details Loading

**CRITICAL**: When performing any phase, you MUST read and use relevant content from `references/` directory.

**Common Rules**: ALWAYS load at workflow start:
- Load `references/common/process-overview.md` for workflow overview
- Load `references/common/session-continuity.md` for session resumption
- Load `references/common/content-validation.md` for validation requirements
- Load `references/common/question-format-guide.md` for question formatting

## The Three-Phase Lifecycle

### INCEPTION PHASE - Planning & Architecture
**Purpose**: Determines WHAT to build and WHY

| Stage | Execution | Details |
|-------|-----------|---------|
| Workspace Detection | ALWAYS | `references/inception/workspace-detection.md` |
| Reverse Engineering | CONDITIONAL | `references/inception/reverse-engineering.md` |
| Requirements Analysis | ALWAYS | `references/inception/requirements-analysis.md` |
| User Stories | CONDITIONAL | `references/inception/user-stories.md` |
| Workflow Planning | ALWAYS | `references/inception/workflow-planning.md` |
| Application Design | CONDITIONAL | `references/inception/application-design.md` |
| Units Generation | CONDITIONAL | `references/inception/units-generation.md` |

### CONSTRUCTION PHASE - Design, Implementation & Test
**Purpose**: Determines HOW to build it

| Stage | Execution | Details |
|-------|-----------|---------|
| Functional Design | CONDITIONAL | `references/construction/functional-design.md` |
| NFR Requirements | CONDITIONAL | `references/construction/nfr-requirements.md` |
| NFR Design | CONDITIONAL | `references/construction/nfr-design.md` |
| Infrastructure Design | CONDITIONAL | `references/construction/infrastructure-design.md` |
| Code Generation | ALWAYS | `references/construction/code-generation.md` |
| Build and Test | ALWAYS | `references/construction/build-and-test.md` |

### OPERATIONS PHASE - Placeholder
**Purpose**: How to DEPLOY and RUN it (future expansion)

See `references/operations/operations.md` for details.

## Key Principles

1. **Adaptive Execution**: Only execute stages that add value
2. **Flexible Depth**: Adjust depth based on complexity (minimal/standard/comprehensive)
3. **Human-in-the-Loop**: Explicit approval required at every critical decision point
4. **Complete Audit Trail**: Log ALL interactions with ISO 8601 timestamps
5. **User Control**: User can request stage inclusion/exclusion

## Workflow Initialization

1. Create `aidlc-docs/aidlc-state.md` using `references/common/state-template.md`
2. Create `aidlc-docs/audit.md` using `references/common/audit-template.md`
3. Display welcome message from `references/common/welcome-message.md` (once per workflow)
4. Execute Workspace Detection
5. Proceed through phases based on workflow plan

## Directory Structure

```
<WORKSPACE-ROOT>/
├── [project-specific structure]
│
└── aidlc-docs/
    ├── inception/
    │   ├── plans/
    │   ├── reverse-engineering/
    │   ├── requirements/
    │   ├── user-stories/
    │   └── application-design/
    ├── construction/
    │   ├── plans/
    │   ├── {unit-name}/
    │   └── build-and-test/
    ├── operations/
    ├── aidlc-state.md
    └── audit.md
```

## Stage Execution Pattern

All stages follow the **Planning → Generation** pattern:

### Part 1: Planning
1. Create plan with checkboxes for each step
2. Generate context-appropriate questions using [Answer]: tags
3. Collect user answers
4. Analyze answers for ambiguities
5. Create follow-up questions if ambiguities found
6. Wait for explicit approval

### Part 2: Generation
1. Load approved plan
2. Execute each step sequentially
3. Mark checkboxes [x] immediately after completion
4. Generate artifacts
5. Present completion message
6. Wait for explicit approval

## Critical Rules

- **NEVER proceed without explicit user approval**
- **ALWAYS log interactions in audit.md**
- **NEVER summarize user input in audit log - capture complete raw input**
- **Application code goes to workspace root, NEVER to aidlc-docs/**
- **ALWAYS use multiple choice question format with [Answer]: tags**
- **ALWAYS validate content before file creation**

## Reference Files

For detailed guidance, load the appropriate reference file:

### Common
- `references/common/process-overview.md`
- `references/common/question-format-guide.md`
- `references/common/content-validation.md`
- `references/common/depth-levels.md`
- `references/common/terminology.md`
- `references/common/session-continuity.md`
- `references/common/error-handling.md`
- `references/common/overconfidence-prevention.md`
- `references/common/ascii-diagram-standards.md`
- `references/common/state-template.md`
- `references/common/audit-template.md`
- `references/common/welcome-message.md`
- `references/common/workflow-changes.md`

### Inception
- `references/inception/workspace-detection.md`
- `references/inception/reverse-engineering.md`
- `references/inception/requirements-analysis.md`
- `references/inception/user-stories.md`
- `references/inception/workflow-planning.md`
- `references/inception/application-design.md`
- `references/inception/units-generation.md`

### Construction
- `references/construction/functional-design.md`
- `references/construction/nfr-requirements.md`
- `references/construction/nfr-design.md`
- `references/construction/infrastructure-design.md`
- `references/construction/code-generation.md`
- `references/construction/build-and-test.md`

### Operations
- `references/operations/operations.md`
