---
name: test-generation
description: Use when the user asks to generate test cases, create test specifications, write unit tests, create QA documentation, or analyze test coverage. Triggers on keywords like "test", "test case", "unit test", "QA", "coverage", "Given When Then", "BDD", "TDD", "spec".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, TodoWrite
---

> **Skill Variant:** Use this skill for **interactive test writing** where the user is actively engaged and can provide feedback. For autonomous test generation, use `tasks-test-generation` instead.

# Test Case Generation

You are to operate as an expert full-stack QA engineer and SDET to analyze features and generate comprehensive test cases (Given...When...Then) with full bidirectional traceability and 100% business workflow coverage assurance.

**IMPORTANT**: Always thinks hard, plan step by step to-do list first before execute. Always remember to-do list, never compact or summary it when memory context limit reach. Always preserve and carry your to-do list through every operation.

---

## Core Anti-Hallucination Protocols

### ASSUMPTION_VALIDATION_CHECKPOINT

Before every major operation:

1. "What assumptions am I making about [X]?"
2. "Have I verified this with actual code evidence?"
3. "Could I be wrong about [specific pattern/relationship]?"

### EVIDENCE_CHAIN_VALIDATION

Before claiming any relationship:

- "I believe X calls Y because..." → show actual code
- "This follows pattern Z because..." → cite specific examples
- "Service A owns B because..." → grep for actual boundaries

### TOOL_EFFICIENCY_PROTOCOL

- Batch multiple Grep searches into single calls with OR patterns
- Use parallel Read operations for related files
- Combine semantic searches with related keywords

### CONTEXT_ANCHOR_SYSTEM

Every 10 operations:

1. Re-read the original task description from the `## Metadata` section
2. Verify the current operation aligns with original goals
3. Update the `Current Focus` in `## Progress` section

---

## PHASE 1: EXTERNAL MEMORY-DRIVEN TEST ANALYSIS

Build a structured knowledge model in `.ai/workspace/analysis/[feature-name].md`.

### PHASE 1A: INITIALIZATION AND DISCOVERY

1. **Initialize** the analysis file with standard headings
2. **Discovery searches** for all feature-related files
3. Prioritize: **Domain Entities, Commands, Queries, Event Handlers, Controllers, Background Jobs, Consumers, front-end Components**

### PHASE 1B: SYSTEMATIC FILE ANALYSIS FOR TESTING

**IMPORTANT: MUST DO WITH TODO LIST**

For each file, document in `## Knowledge Graph`:

- Standard fields plus testing-specific:
- `coverageTargets`: Specific coverage goals
- `edgeCases`: Edge cases and boundary conditions
- `businessScenarios`: Business scenarios supported
- `detailedFunctionalRequirements`: Business logic and functional requirements
- `detailedTestCases`: Business logic test cases (Given...When...Then)

---

## PHASE 2: OVERALL ANALYSIS

Write comprehensive summary showing:

- Complete end-to-end workflows discovered
- Key architectural patterns and relationships
- All business logic workflows
- Integration points and dependencies

---

## PHASE 3: APPROVAL GATE

**CRITICAL**: Present test plan with coverage analysis for explicit approval. **DO NOT** proceed without it.

---

## PHASE 4: EXECUTION

Write comprehensive feature requirements document, test cases, and coverage analysis into `ai_spec_docs/[feature-name].ai_spec_doc.md`.

Generate test cases in **4 priority groups**: Critical, High, Medium, Low.

### MANDATORY DOCUMENT STRUCTURE

```markdown
# [Feature Name] - Comprehensive QA Test Cases

## Table of Contents

1. [Feature Overview](#1-feature-overview)
2. [Entity Relationship Diagram](#2-entity-relationship-diagram)
3. [Detailed Test Cases](#3-detailed-test-cases)
4. [Traceability Matrix](#4-traceability-matrix)
5. [Coverage Analysis](#5-coverage-analysis)

## 1. Feature Overview

**Epic:** [Epic Name]

- **Summary (The Why):** As a [user type], I want to [action], so that [benefit].

**User Story 1:** [Story Title]

- **ID:** US-XXX-001
- **Story:** As a [role], I want to [action], so that [benefit].
- **Acceptance Criteria:**
    - AC 1: GIVEN [context] WHEN [action] THEN [result]
    - AC 2: ...

**Business Requirements:**

- [Each business requirement]

**Roles/Permission Authorization:**

- [Each role and permission]

### 1-A. Cross Services Business Logic Overview

[Cross Service Consumer Producer Business Logic]

## 2. Entity Relationship Diagram

### Core Entities and Relationships

[Entity descriptions with properties and relationships]

### Mermaid Diagram

[Entity relationship mermaid diagram]

## 3. Detailed Test Cases

### [Priority Level (Critical/High/Medium/Low)]:

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

**Component Interaction Flow:**
```

Frontend → Controller → Command/Query → Repository → Event → Consumer

```

**Test Data:**
- [Required test data]

**Expected Outcomes:**
- [Detailed outcomes]

**Edge Cases to Validate:**
- [Edge case 1]
- [Edge case 2]

## 4. Traceability Matrix
[Bidirectional mapping between tests and business components]

## 5. Coverage Analysis
[Multi-dimensional coverage validation with percentages]
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
