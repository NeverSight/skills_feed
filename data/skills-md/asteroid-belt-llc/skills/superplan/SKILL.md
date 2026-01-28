---
name: superplan
description: Use when starting significant features, epics, or complex tasks. Creates multi-phase implementation plans with parallelizable phases, poker estimates, TDD-first acceptance criteria, and quality gates. Detects tech stack from CLAUDE.md/AGENTS.md (bypassing internet research if complete) or via codebase scan.
metadata:
  version: "3.0"
  generated-at: "2025-01-25"
compatibility: Internet access used for best practices research (bypassed if CLAUDE.md/AGENTS.md provides complete tech stack). Works with any codebase.
---

# Superplan: Comprehensive Feature Planning

## Overview

Superplan creates detailed, executable implementation plans that enable parallel agent execution. Each plan includes everything needed to implement a feature: requirements, architecture, code changes, tests, and acceptance criteria.

## When to Use Superplan

- Starting a new feature or epic
- Complex tasks requiring multiple phases
- Tasks that could benefit from parallel execution by multiple agents
- When you need comprehensive documentation of implementation decisions

## Core Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SUPERPLAN WORKFLOW                          │
├─────────────────────────────────────────────────────────────────────┤
│  1. INTAKE          →  Gather story/requirements from user          │
│  2. DETECT          →  Check CLAUDE.md/AGENTS.md, then scan         │
│  3. INTERVIEW       →  Ask clarifying questions                     │
│  4. RESEARCH        →  Look up best practices (BYPASS if docs OK)   │
│  5. EXPLORE         →  Understand existing codebase patterns        │
│  6. REFACTOR ASSESS →  Evaluate if refactoring should precede work  │
│  7. ARCHITECT       →  Design solution with diagrams                │
│  8. PHASE           →  Break into parallelizable phases + ESTIMATES │
│  9. DETAIL          →  Specify code deltas per phase                │
│ 10. TEST            →  Define failing tests per phase (TDD)         │
│ 11. DOCUMENT        →  Write plan to docs/<feature>-plan.md         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Reference Index - MUST READ Before Each Phase

**References are loaded on demand. Read BEFORE starting the relevant phase.**

| When | Reference | What You Get |
|------|-----------|--------------|
| **Before ANY parallel operation** | [Sub-Agent Syntax](references/SUBAGENT-SYNTAX.md) | Exact prompts for launching parallel agents |
| **Phase 3: Interview** | [Interview Guide](references/INTERVIEW-GUIDE.md) | Question templates by feature size |
| **Phase 5: Explore** | [Explore Prompts](references/EXPLORE-PROMPTS.md) | Exact prompts for codebase exploration agents |
| **Phase 6: Refactor** | [Refactoring Research](references/REFACTORING-RESEARCH.md) | Mikado, Strangler Fig, Branch by Abstraction |
| **Phase 7: Architect** | [Architecture Templates](references/ARCHITECTURE-TEMPLATES.md) | API, data model, component tree templates |
| **Phase 9: Detail** | [Task Micro-Structure](references/TASK-MICROSTRUCTURE.md) | 5-step TDD format for each task |
| **Phase 10: Test** | [TDD Discipline](references/TDD-DISCIPLINE.md) | TDD rules, rationalizations, red flags |
| **Phase 10: Test** | [Testing Pyramid](references/TESTING-PYRAMID.md) | Unit/integration/E2E examples |
| **Phase 10: Test** | [Command Outputs](references/COMMAND-OUTPUTS.md) | Expected test output format |
| **Phase 11: Document** | [Plan Template](references/PLAN-TEMPLATE.md) | Complete plan file structure |

**DO NOT SKIP REFERENCES.** They contain exact prompts, templates, and formats that are NOT duplicated here.

---

## CRITICAL: Parallel Execution with Sub-Agents

**YOU MUST USE SUB-AGENTS** for parallelizable operations.

> **STOP. Read [Sub-Agent Syntax](references/SUBAGENT-SYNTAX.md) NOW** before launching any parallel operation.

| Operation | Action |
|-----------|--------|
| Independent file reads | Multiple Read tasks in single message |
| Code searches | Parallel Explore agents |
| Parallel phases (1A, 1B, 1C) | Parallel general-purpose agents |

---

## Poker Planning Estimates

All phases MUST include Fibonacci estimates: **1, 2, 3, 5, 8, 13, 21**

| Size | Meaning | Example |
|------|---------|---------|
| 1 | Trivial | Config value, typo fix |
| 2 | Small | Single file, simple function |
| 3 | Medium | Multi-file, new component |
| 5 | Large | Feature module, API endpoint |
| 8 | X-Large | Complex feature with dependencies |
| 13 | Epic chunk | Major subsystem change |
| 21 | Too big | **Split into smaller tasks** |

---

## Phase 1: INTAKE - Gather Requirements

Ask the user to provide their story/requirements:
- Copy/paste story text directly
- Provide a link to a ticket (Jira, Linear, GitHub Issue)
- Use an MCP tool to fetch the story
- Describe the feature verbally

**Output**: Source, Type (User Story/Technical Task/Bug Fix/Epic), Raw Requirements, Initial Understanding.

---

## Phase 2: DETECT - Technology Stack Analysis

### Step 1: Check for CLAUDE.md or AGENTS.md

If found AND complete (all boxes checked), BYPASS codebase scan AND Phase 4 Research.

Completeness checklist:
- [ ] Primary language(s) identified
- [ ] Major framework(s) identified
- [ ] Build/package tools identified
- [ ] Quality tools identified (linter, formatter, type checker)
- [ ] Test framework identified

### Step 2: Detection (if needed)

Launch parallel Explore agents to detect: Languages, Frameworks, Build Tools, Quality Tools, Testing Tools.

**Output**: Tech stack summary, bootstrap requirements, research bypass status.

---

## Phase 3: INTERVIEW - Clarifying Questions

Ask 3-5 questions, then **WAIT FOR ANSWERS**.

**Required Questions**:
1. "What is the MVP? What can we defer to v2?"
2. "What is explicitly OUT of scope?"
3. "Are there performance/security requirements?"
4. "What test coverage do you expect?"

> **STOP. Read [Interview Guide](references/INTERVIEW-GUIDE.md) NOW** for question templates before asking.

---

## Phase 4: RESEARCH - Best Practices Lookup

**BYPASS if** DETECT found complete tech stack in CLAUDE.md/AGENTS.md.

Otherwise, launch parallel web searches:
- `[Language] [YEAR] best practices`
- `[Framework] [YEAR] patterns`
- `[Framework] security guidelines`

**Output**: Sources consulted, key findings, specific recommendations.

---

## Phase 5: EXPLORE - Codebase Analysis

> **STOP. Read [Explore Prompts](references/EXPLORE-PROMPTS.md) NOW** for exact agent prompts before launching.

Launch 3 parallel Explore agents:
1. **Pattern Discovery** - Find similar implementations
2. **Integration Points** - Identify files to modify
3. **Technical Debt Scan** - Check for issues in affected areas

**Output**: Similar implementations table, integration points table, technical debt table.

---

## Phase 6: REFACTOR/REWRITE ASSESSMENT

Evaluate if refactoring should precede feature work.

> **STOP. Read [Refactoring Research](references/REFACTORING-RESEARCH.md) NOW** for methodologies before assessing.

### Confidence Levels

| Level | Description | Action |
|-------|-------------|--------|
| LOW | Code is clean | Proceed to ARCHITECT |
| MEDIUM | Some smells present | Note debt, ask user preference |
| HIGH | Significant issues | Recommend refactor phases |
| CRITICAL | Major rewrite needed | Propose Mikado/Strangler Fig |

If HIGH or CRITICAL, ask permission to add refactoring phases.

---

## Phase 7: ARCHITECT - Solution Design

> **STOP. Read [Architecture Templates](references/ARCHITECTURE-TEMPLATES.md) NOW** for templates before designing.

For each component, answer:
- [ ] What new components are being added?
- [ ] How do they connect to existing components?
- [ ] What is the data flow?

Required outputs:
- System context diagram
- API design (if applicable) with all response codes
- Data model (if applicable) with migration scripts
- Component tree (if UI)

---

## Phase 8: PHASE - Parallel Work Breakdown

Break work into phases with poker estimates that can be executed in parallel.

### Phase Design Principles

1. **Independence**: Phases executable without waiting for others
2. **Testability**: Each phase independently testable
3. **Estimated Size**: Target 3-8 points per phase
4. **Quality Gated**: Each phase includes Definition of Done
5. **Context Managed**: Each phase ends with a CHECKPOINT for compaction

### CHECKPOINT: Context Compaction Between Phases

**EVERY phase MUST end with a CHECKPOINT instruction.** This enables `/superbuild` to run `/compact` automatically in BUILD-ALL mode, preserving context across long implementations.

#### CHECKPOINT Format

```markdown
- [ ] **CHECKPOINT: Run `/compact focus on: [Phase N] complete, [key artifacts], [Phase N+1] goals`**
```

#### CHECKPOINT Focus Points

The focus directive tells `/compact` what to preserve:
- **Completed work**: What was built, key decisions made
- **Key artifacts**: File paths, API contracts, data models created
- **Next phase goals**: What the upcoming phase needs to accomplish
- **Blockers/dependencies**: Any issues that affect future phases

#### Example Phase with CHECKPOINT

```markdown
## Phase 1: Authentication System
- [ ] Task 1.1: Create auth models in `src/models/auth.ts`
- [ ] Task 1.2: Implement JWT handling in `src/services/jwt.ts`
- [ ] Task 1.3: Add auth middleware in `src/middleware/auth.ts`
- [ ] **CHECKPOINT: Run `/compact focus on: Phase 1 complete, auth models and JWT service created, Phase 2 needs API endpoints`**

## Phase 2: API Endpoints
- [ ] Task 2.1: Create `/api/auth/login` endpoint
...
```

**Output**: Phase dependency diagram + table with estimates:

| Phase | Name | Depends On | Parallel With | Estimate | Status |
|-------|------|------------|---------------|----------|--------|

---

## Phase 9: DETAIL - Code Deltas Per Phase

> **STOP. Read [Task Micro-Structure](references/TASK-MICROSTRUCTURE.md) NOW** for 5-step TDD format before detailing tasks.

### Code Delta Format

- `path/to/file.ts (CREATE)` - new file with full content
- `path/to/file.ts:45-67 (MODIFY)` - existing file with line range and diff

**NEVER use** pseudocode, `// ... rest of file`, or vague descriptions.

---

## Phase 10: TEST - TDD Acceptance Criteria

> **STOP. Read [Command Outputs](references/COMMAND-OUTPUTS.md) NOW** for expected output format before writing tests.

### Testing Pyramid

- **Unit Tests (80%)**: Business logic, utilities
- **Integration Tests (15%)**: API contracts, database
- **E2E Tests (5%)**: Critical user journeys only

### Test-First Workflow

For each task:
1. Write test (will fail)
2. Run test, confirm failure with expected output
3. Implement code
4. Run test, confirm pass with expected output
5. All existing tests still pass

> **Also read [Testing Pyramid](references/TESTING-PYRAMID.md)** for unit/integration/E2E examples.

---

## Definition of Done - REQUIRED PER PHASE

Every phase MUST include this checklist:

```markdown
### Definition of Done
- [ ] Code passes linter
- [ ] Code passes formatter
- [ ] Code passes type checker
- [ ] All new tests pass
- [ ] All existing tests pass
- [ ] Test coverage >= 80% for new code
- [ ] No new warnings introduced
```

---

## Phase Completion: Conventional Commit Message

At the end of EVERY phase, output (but do not commit):

```
PHASE [X] COMPLETE - Conventional Commit Message:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<type>(<scope>): <short summary>

<body - detailed description>

Files changed:
- path/to/file.ts (CREATE/MODIFY/DELETE)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  DO NOT COMMIT - User will handle git operations
```

---

## Phase 11: DOCUMENT - Write the Plan

Write the complete plan to `docs/<feature>-plan.md`.

> **STOP. Read [Plan Template](references/PLAN-TEMPLATE.md) NOW** for complete structure before writing.

### Execution Handoff

After saving, present options:

```
PLAN COMPLETE: docs/<feature>-plan.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXECUTION OPTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Option 1: Execute Now (This Session)
  Run `/superbuild docs/<feature>-plan.md`

Option 2: Execute in Fresh Session
  Start new session and run `/superbuild docs/<feature>-plan.md`

Option 3: Review First
  Read through the plan, suggest modifications, then execute

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Which option would you like?
```

### Multi-File Strategy

If plan exceeds ~4,000 lines, split into:
- `<feature>-plan-1.md`: Overview, Requirements, Architecture
- `<feature>-plan-2.md`: Implementation Phases
- `<feature>-plan-N.md`: Remaining phases, Appendix

---

## Quick Reference

See **Reference Index** at top of this document for when to read each reference.

| Phase | Key Action | Must Read Before Starting |
|-------|------------|---------------------------|
| 1-2 | Gather requirements, detect stack | - |
| 3 | Interview (WAIT for answers) | Interview Guide |
| 4 | Research (if needed) | - |
| 5 | Explore codebase | Explore Prompts |
| 6 | Refactor assessment | Refactoring Research |
| 7 | Architecture design | Architecture Templates |
| 8-9 | Phase breakdown + code deltas | Task Micro-Structure |
| 10 | TDD tests | TDD Discipline, Testing Pyramid, Command Outputs |
| 11 | Write plan + handoff | Plan Template |
| ANY | Parallel operations | Sub-Agent Syntax |
