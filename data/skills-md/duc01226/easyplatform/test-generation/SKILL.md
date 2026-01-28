---
name: test-generation
version: 2.0.1
description: Use when the user asks to generate test cases, create test specifications, write unit tests, create QA documentation, or analyze test coverage. Triggers on keywords like "test", "test case", "unit test", "QA", "coverage", "Given When Then", "BDD", "TDD", "spec".
infer: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, TodoWrite
---

> **Skill Variant:** Use this skill for **interactive test writing** where the user is actively engaged and can provide feedback. For autonomous test generation, use `tasks-test-generation` instead.

# Test Case Generation

You are to operate as an expert full-stack QA engineer and SDET to analyze features and generate comprehensive test cases (Given...When...Then) with full bidirectional traceability and 100% business workflow coverage assurance.

**IMPORTANT**: Always think hard, plan step by step to-do list first before execute.

**Prerequisites:** **MUST READ** `.claude/skills/shared/anti-hallucination-protocol.md` before executing.

---

## PHASE 1: EXTERNAL MEMORY-DRIVEN TEST ANALYSIS

Build a structured knowledge model in `.ai/workspace/analysis/[feature-name].analysis.md`.

### PHASE 1A: INITIALIZATION AND DISCOVERY

1. **Initialize** the analysis file with standard headings
2. **Discovery searches** for all feature-related files
3. Prioritize: **Domain Entities, Commands, Queries, Event Handlers, Controllers, Background Jobs, Consumers, Frontend Components**

### PHASE 1B: SYSTEMATIC FILE ANALYSIS FOR TESTING

**IMPORTANT: MUST DO WITH TODO LIST**

For each file, document in `## Knowledge Graph`:
- Standard fields plus testing-specific:
- `coverageTargets`, `edgeCases`, `businessScenarios`
- `detailedFunctionalRequirements`, `detailedTestCases` (Given...When...Then)

---

## PHASE 2: OVERALL ANALYSIS

Write comprehensive summary: end-to-end workflows, architectural patterns, business logic workflows, integration points.

---

## PHASE 3: APPROVAL GATE

**CRITICAL**: Present test plan with coverage analysis for explicit approval. **DO NOT** proceed without it.

---

## PHASE 4: EXECUTION

Write test cases and coverage analysis into `.ai/workspace/specs/[feature-name].ai_spec_doc.md`.

Generate test cases in **4 priority groups**: Critical, High, Medium, Low.

### Test Case Format

```markdown
#### TC-001: [Test Case Name]

**Feature Module:** [Module]
**Business Requirement:** BR-XXX
**Priority:** Critical/High/Medium/Low

**Given** [initial context]
**And** [additional context]
**When** [action performed]
**Then** the system should:
- [Expected outcome 1]
- [Expected outcome 2]

**Test Data:**
- [Required test data]

**Edge Cases to Validate:**
- [Edge case 1]
```

---

## PHASE 5: Review Table of Contents

Update `## Table of Contents` with detailed sub-section links.

---

## Test Case Guidelines

- **Evidence-based testing**: Base test cases on actual code behavior
- **Complete coverage**: Cover all conditional logic paths
- **Component tracing**: Include workflow between components
- **Priority classification**: Critical (P0), High (P1), Medium (P2), Low (P3)
- **BDD format**: Use Given/When/Then consistently
- **Traceability**: Link test cases to requirements bidirectionally

## Related

- `qa-engineer`
- `test-specs-docs`
- `tasks-test-generation`
- `debugging`

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**
- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
