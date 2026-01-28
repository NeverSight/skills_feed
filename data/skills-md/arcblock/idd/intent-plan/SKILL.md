---
name: intent-plan
description: Transform approved Intent into executable phased plan with strict TDD. Each step requires tests first (happy/bad/edge/security cases), then implementation. Use after /intent-review when ready to start development.
---

# Intent Plan

Transform an approved Intent into a structured, executable development plan with strict TDD discipline.

## Core Principles

1. **Test First, Always**: Every implementation step starts with writing tests
2. **Phased Execution**: Break work into phases with clear deliverables
3. **Verification Gates**: Each phase ends with e2e validation
4. **Automation Priority**: Prefer CLI/script testing over manual/browser testing

## Plan Structure

```
Phase 1: [Phase Name]
├── Step 1.1: [Feature/Component]
│   ├── Unit 1: Write Tests
│   │   ├── Happy path cases
│   │   ├── Bad path cases (detailed, comprehensive)
│   │   ├── Edge cases
│   │   ├── Security vulnerability cases
│   │   ├── Data leak cases
│   │   └── Data damage cases
│   └── Unit 2: Implementation
│       └── Make all tests pass
├── Step 1.2: [Next Feature]
│   ├── Unit 1: Write Tests
│   └── Unit 2: Implementation
└── Phase Gate: E2E Verification
    └── CLI/Script based validation

Phase 2: [Phase Name]
└── ...
```

## Test Requirements

### Unit 1: Test Writing (MUST come first)

Every step begins with comprehensive test coverage:

| Test Category | Description | Examples |
|---------------|-------------|----------|
| **Happy Path** | Normal expected usage | Valid inputs, correct sequences |
| **Bad Path** | Invalid inputs, error conditions | Wrong types, missing required fields, invalid states |
| **Edge Cases** | Boundary conditions | Empty inputs, max values, concurrent access |
| **Security** | Vulnerability prevention | Injection attacks, auth bypass, privilege escalation |
| **Data Leak** | Information exposure | Sensitive data in logs, error messages, responses |
| **Data Damage** | Data integrity | Partial writes, corruption, race conditions |

**Bad cases must be detailed and comprehensive.** A good test suite has more failure tests than success tests.

### Unit 2: Implementation

- Only starts after tests are written
- Goal: Make all tests pass
- No new functionality without corresponding tests

## Phase Gates: E2E Verification

Each phase ends with end-to-end verification:

### Preferred: CLI/Script Testing
```bash
# Example: API verification
curl -X POST http://localhost:3000/api/resource \
  -H "Content-Type: application/json" \
  -d '{"field": "value"}' | jq .

# Example: Database state check
psql -c "SELECT * FROM table WHERE condition"

# Example: File system verification
diff expected_output.json actual_output.json
```

### For Web Projects: Automation-Friendly Design

Design APIs and interfaces that support automated testing:

```
DO:
- Provide health check endpoints
- Return machine-parseable responses (JSON)
- Include test mode / seed data endpoints
- Design idempotent operations

DON'T:
- Require browser interaction for verification
- Depend on visual inspection
- Need manual clicking through UI
```

### When Browser Testing is Unavoidable

If browser/headless testing is truly necessary:
- Use Playwright/Puppeteer with script automation
- Create dedicated test endpoints
- Prefer API calls over UI interaction

## Workflow

```
Read Intent file
    ↓
Analyze scope and complexity
    ↓
Identify logical phases
    ↓
Break each phase into steps
    ↓
For each step, define:
    - Test categories needed
    - Implementation scope
    ↓
Define phase gates (e2e criteria)
    ↓
Present plan for approval
    ↓
User confirms or adjusts
    ↓
Save plan to intent/PLAN.md
```

## Output: PLAN.md Template

```markdown
# Implementation Plan for [Project/Feature]

Generated from: `intent/[name]/INTENT.md`
Date: YYYY-MM-DD

## Overview

- Total Phases: N
- Estimated Complexity: [Low/Medium/High]
- Key Dependencies: [List]

## Phase 1: [Phase Name]

**Goal**: [What this phase delivers]

### Step 1.1: [Component/Feature Name]

**Unit 1: Tests** (Do First)

| Category | Test Cases |
|----------|------------|
| Happy Path | - Case 1: [description] |
|            | - Case 2: [description] |
| Bad Path   | - Invalid input: [specific case] |
|            | - Missing field: [specific case] |
|            | - Wrong state: [specific case] |
| Edge Cases | - Empty input |
|            | - Maximum values |
|            | - Concurrent access |
| Security   | - SQL injection attempt |
|            | - XSS attempt |
|            | - Auth bypass attempt |
| Data Leak  | - Sensitive data in error |
|            | - Logs exposure |
| Data Damage| - Partial write recovery |
|            | - Race condition handling |

**Unit 2: Implementation**

- [ ] Implement [component]
- [ ] Ensure all tests pass
- [ ] Code review criteria: [specific points]

### Step 1.2: [Next Component]

...

### Phase 1 Gate: E2E Verification

```bash
# Verification script
[CLI commands to verify phase completion]
```

**Success Criteria**:
- [ ] Criterion 1
- [ ] Criterion 2

---

## Phase 2: [Phase Name]

...

---

## Final Verification

```bash
# Full system verification script
```

## Risk Mitigation

| Risk | Mitigation | Contingency |
|------|------------|-------------|
| [Risk 1] | [How to prevent] | [If it happens] |

## Notes

- [Any additional context]
```

## Integration with Other Skills

```
/intent-interview     # Create Intent
    ↓
/intent-review        # Approve Intent
    ↓
/intent-plan          # Generate execution plan (THIS SKILL)
    ↓
[Execute: TDD cycles]
    ↓
/intent-sync          # Write back confirmed details
    ↓
/intent-check         # Verify consistency
```

## Tips for Good Plans

1. **Right-size phases**: Each phase should be completable in 1-3 days
2. **Clear dependencies**: Note when steps depend on previous steps
3. **Testable gates**: Phase gates must be automatable
4. **Specific test cases**: "Test error handling" is bad; "Test 404 response when resource not found" is good
5. **Security by default**: Include security tests even if not explicitly requested
