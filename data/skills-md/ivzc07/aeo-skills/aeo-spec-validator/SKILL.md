---
name: aeo-spec-validator
description: Validate that tasks are sufficiently defined before execution. Returns score 0-100.
---

# AEO Spec Validator

**Purpose:** Validate task specifications and score them 0-100 to ensure they're sufficiently defined before execution.

## When to Use

Invoke this skill when:
- User provides a task description
- Before starting any implementation work
- When task is ambiguous or unclear

## Scoring System (0-100)

### Clarity Indicators (0-50 points)

**Objective Clarity (15 points):**
- **15 pts:** Explicit, unambiguous objective
  - Example: "Add email validation to signup form with regex check"
- **10 pts:** Clear but minor ambiguities
  - Example: "Add email validation to signup"
- **5 pts:** Vague objective
  - Example: "Improve signup process"
- **0 pts:** No clear objective

**Acceptance Criteria (15 points):**
- **15 pts:** Specific, testable criteria defined
  - Example: "Must validate RFC 5322 format, reject + aliases, show inline errors"
- **10 pts:** General criteria mentioned
  - Example: "Must validate email format and show errors"
- **5 pts:** Implied criteria
  - Example: "Should work for valid emails"
- **0 pts:** No criteria mentioned

**Context Provided (10 points):**
- **10 pts:** Full context (where, why, constraints)
  - Example: "For the signup form in /pages/auth/signup.tsx, using existing validator utility"
- **5 pts:** Partial context
  - Example: "For the signup form"
- **0 pts:** No context

**Dependencies Identified (10 points):**
- **10 pts:** All dependencies listed (libraries, services, APIs)
  - Example: "Uses validator.js library, calls POST /api/validate"
- **5 pts:** Some dependencies mentioned
  - Example: "Uses validator library"
- **0 pts:** No dependencies mentioned

### Quality Indicators (0-30 points)

**Tech Stack Specified (10 points):**
- **10 pts:** Specific technologies/libraries named
- **5 pts:** General tech mentioned (e.g., "use a validation library")
- **0 pts:** No tech mentioned

**Test Requirements (10 points):**
- **10 pts:** Test cases specified
  - Example: "Test valid emails, invalid formats, edge cases (+ alias)"
- **5 pts:** General testing mentioned
  - Example: "Should have tests"
- **0 pts:** No testing mentioned

**Performance/Security (10 points):**
- **10 pts:** Explicit requirements
  - Example: "Must reject in <100ms, prevent email injection"
- **5 pts:** General concerns mentioned
  - Example: "Should be fast and secure"
- **0 pts:** No mention

### Risk Assessment (0-20 points)

**Scope (10 points):**
- **10 pts:** Small, well-defined scope (1-2 files, <100 LOC)
- **5 pts:** Medium scope (3-5 files, 100-500 LOC)
- **0 pts:** Large scope (5+ files, 500+ LOC)

**Complexity (10 points):**
- **10 pts:** Simple CRUD or clear logic
- **5 pts:** Moderate complexity (multiple systems, integration)
- **0 pts:** High complexity (architectural changes, unknowns)

## Ambiguity Detection

Automatically detect and penalize these red flags:

**Subjective Terms (-5 each):**
- "fast", "quick", "performant"
- "good", "better", "optimal"
- "simple", "clean", "elegant"
- "user-friendly", "intuitive"

**Vague Verbs (-10 each):**
- "improve" (without specifics)
- "optimize" (without metrics)
- "enhance" (without details)
- "fix" (without describing what's broken)

**Missing Constraints (-5 each):**
- No performance requirements
- No error handling specified
- No edge cases mentioned
- No security considerations (for sensitive areas)

## Scoring Examples

### Example 1: Well-Defined Spec (Score: 92/100)

```
Task: Add email validation to the signup form in /pages/auth/signup.tsx

Requirements:
- Validate using RFC 5322 format via validator.js library
- Reject email addresses with + aliases
- Show inline error message "Invalid email format" on blur
- Call POST /api/validate-email to check if already registered
- Tests: valid emails, invalid formats, + alias rejection, duplicates

Score Breakdown:
- Objective clarity: 15/15 (explicit)
- Acceptance criteria: 15/15 (specific, testable)
- Context: 10/10 (file location, existing utility)
- Dependencies: 10/10 (validator.js, API endpoint)
- Tech stack: 10/10 (validator.js named)
- Test requirements: 10/10 (specific test cases)
- Performance/security: 7/10 (missing perf req)
- Scope: 10/10 (single file)
- Complexity: 5/10 (integration but clear)

Total: 92/100 → PROCEED
```

### Example 2: Poor Spec (Score: 28/100)

```
Task: Improve the signup

Score Breakdown:
- Objective clarity: 5/15 (vague)
- Acceptance criteria: 0/15 (none)
- Context: 0/10 (none)
- Dependencies: 0/10 (none)
- Tech stack: 0/10 (none)
- Test requirements: 0/10 (none)
- Performance/security: 0/10 (none)
- Scope: 8/10 (assume small)
- Complexity: 5/10 (assume simple)

Ambiguity Penalties:
- "Improve" (vague verb): -10
- "signup" (subjective good?): 0

Total: 28/100 → REFUSE

Feedback:
❌ SPEC INSUFFICIENT (28/100)

Missing:
• Specific acceptance criteria
• What to improve about signup?
• Context (which signup flow?)
• Dependencies and tech stack
• Test requirements

Please provide:
1. What specific improvement is needed?
2. Acceptance criteria for "done"
3. Which signup form/page?
4. Any constraints or requirements
```

## Actions by Score Range

### **80-100: PROCEED**
- Well-defined spec
- Proceed with confidence calculation
- Note: "Spec score: XX/100 - well-defined"

### **60-79: MINOR GAPS**
- Generally clear, some details missing
- Proceed but note assumptions
- Format:
  ```
  ⚠️ SPEC HAS MINOR GAPS (68/100)

  Assumptions:
  • Using existing test framework
  • Standard error handling
  • No special performance requirements

  Proceeding with these assumptions. Correct if wrong.
  ```

### **40-59: MAJOR GAPS**
- Significant ambiguities
- Ask clarifying questions before proceeding
- Format:
  ```
  ❌ SPEC NEEDS CLARIFICATION (45/100)

  Missing Details:
  • Which file(s) should be modified?
  • What validation library to use?
  • Acceptance criteria not specified
  • No test requirements

  Please clarify:
  1. Where should this be implemented?
  2. What tech stack/libraries?
  3. What defines "done"?
  ```

### **< 40: UNACCEPTABLE**
- Too vague to execute
- Refuse task
- Request complete spec
- Format:
  ```
  ❌ CANNOT PROCEED - SPEC TOO UNCLEAR (28/100)

  This task is too vague. Please provide:

  1. **Objective:** What exactly needs to be done?
  2. **Acceptance Criteria:** How do we know it's done?
  3. **Context:** Where/why is this needed?
  4. **Dependencies:** What libraries/services?

  Example of a good spec:
  "Add email validation to /pages/auth/signup.tsx using validator.js.
   Must validate RFC 5322 format, reject + aliases, show inline errors.
   Tests for valid, invalid, and duplicate emails."
  ```

## Integration Flow

1. **Invoke:** Called by aeo-core during Phase 0
2. **Score:** Analyze task and calculate score
3. **Return:** Score + feedback if needed
4. **Decision:** aeo-core uses score for confidence calculation

## Examples for Reference

Show these examples if user asks for clarification:

### Good Spec Template

```
[Task Name]

**Objective:** [Specific action to take]

**Location:** [File paths, components, modules]

**Requirements:**
- [Requirement 1]
- [Requirement 2]

**Dependencies:**
- Libraries: [list]
- Services: [list]
- APIs: [list]

**Acceptance Criteria:**
- [Criteria 1 - testable]
- [Criteria 2 - testable]

**Tests:**
- [Test case 1]
- [Test case 2]

**Constraints:**
- Performance: [requirements]
- Security: [requirements]
```

### Common Mistakes

❌ "Make it faster"
✅ "Reduce API response time from 2s to <500ms by adding caching"

❌ "Fix the bug"
✅ "Fix null reference error in UserService.getUser() when user ID not found"

❌ "Add authentication"
✅ "Add JWT authentication to /api/* routes using bcrypt for password hashing"
