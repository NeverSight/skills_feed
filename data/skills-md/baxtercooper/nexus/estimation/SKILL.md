---
name: estimation
description: Use before committing to a task. Provides complexity analysis and scope assessment. Invoke when user asks "how complex" or before large features.
version: 1.0.0
---

# Estimation Skill

> **Core Principle**: Estimate before committing.

## When to Invoke

- Before starting a large or complex task
- When user asks about complexity or scope
- Before providing time commitments
- When decomposing tasks for orchestration
- When uncertain about task scope

---

## Complexity Factors

Assess each factor to determine overall complexity:

| Factor | Weight | Questions to Ask |
|--------|--------|------------------|
| Files to modify | High | How many files? How spread across codebase? |
| New patterns required | High | Does this require patterns not in codebase? |
| External dependencies | High | New APIs, services, or integrations? |
| Test coverage needed | Medium | Unit, integration, e2e tests required? |
| Documentation updates | Low | README, API docs, comments needed? |
| Breaking changes | High | Will this break existing functionality? |
| Unknown territory | High | Are you familiar with this code area? |

### Complexity Scoring

```
LOW: 1-2 files, existing patterns, no new dependencies
MEDIUM: 3-5 files, minor new patterns, limited dependencies
HIGH: 6+ files, new patterns, new dependencies, cross-cutting
UNKNOWN: Cannot assess without more exploration
```

---

## Estimation Protocol

### Step 1: Scope Analysis

```
1. What is the task asking for?
2. What files will likely need changes?
3. What patterns exist for similar features?
4. What dependencies are involved?
5. What testing is required?
```

### Step 2: Factor Assessment

For each complexity factor:
- Score as: none (0), low (1), medium (2), high (3)
- Note specific concerns

### Step 3: Risk Identification

```
Risks to identify:
- Areas of uncertainty
- Potential blockers
- Dependencies on external factors
- Technical debt implications
```

### Step 4: Output Estimation

Use the template below.

---

## Output Template

```yaml
estimation:
  timestamp: [ISO 8601]
  task: |
    [Task description]

  scope:
    files_affected:
      known:
        - [file1.ts - reason]
        - [file2.ts - reason]
      likely:
        - [file3.ts - reason]
      unknown: [count or "cannot determine"]

    changes_required:
      - type: [new_file | modification | deletion]
        description: [what change]
      - type: [type]
        description: [what change]

  complexity:
    overall: [low | medium | high | unknown]
    factors:
      files_to_modify: [0-3]
      new_patterns: [0-3]
      external_dependencies: [0-3]
      test_coverage: [0-3]
      documentation: [0-3]
      breaking_changes: [0-3]
      unknown_territory: [0-3]
    total_score: [sum]

  risks:
    - risk: "[Risk description]"
      likelihood: [low | medium | high]
      impact: [low | medium | high]
      mitigation: "[How to address]"

  unknowns:
    - "[What you couldn't determine]"
    - "[What needs clarification]"

  recommendations:
    approach: |
      [Recommended approach]
    alternatives:
      - "[Alternative approach 1]"
    next_steps:
      - "[First step]"
      - "[Second step]"

  confidence: 0.0
  evidence:
    - "[What you examined]"
```

---

## Complexity Thresholds

### Low Complexity (Score 0-5)
- Can likely be completed in single session
- Straightforward implementation
- Well-understood patterns

### Medium Complexity (Score 6-10)
- May require multiple sessions
- Some exploration needed
- Some new patterns required

### High Complexity (Score 11+)
- Definitely requires planning
- Significant exploration needed
- Consider breaking into phases

### Unknown Complexity
- Cannot assess without more information
- Recommend context-gathering first
- Ask user clarifying questions

---

## Rules

> [!CRITICAL]
> NEVER estimate without understanding scope.
> ALWAYS include unknowns.

### Do
- List specific files you expect to change
- Identify risks and unknowns
- Provide confidence level
- Recommend next steps

### Don't
- Give point estimates (use ranges/categories)
- Promise delivery timelines
- Understate complexity to seem helpful
- Skip the unknown factors

---

## Integration with Other Skills

| After Estimation | Invoke |
|------------------|--------|
| Need more context | → `context-gathering` skill |
| Ready to plan implementation | → `writing-plans` skill |
| Ready to execute | → `orchestration` skill |

### Chaining Rules

1. **IF** unknowns are significant **THEN** invoke `context-gathering` first
2. **IF** complexity is high **THEN** recommend phased approach
3. **AFTER** estimation accepted **THEN** proceed to `writing-plans`

---

## Example

**Task**: "Add user authentication to the API"

```yaml
estimation:
  timestamp: "2024-01-15T10:00:00Z"
  task: |
    Add user authentication to the existing Express API

  scope:
    files_affected:
      known:
        - src/routes/auth.ts - new route file
        - src/middleware/auth.ts - new middleware
        - src/models/user.ts - user model changes
      likely:
        - src/routes/index.ts - route registration
        - tests/auth.test.ts - new tests
      unknown: 2-3 additional files for utilities

    changes_required:
      - type: new_file
        description: Authentication routes (login, register, logout)
      - type: new_file
        description: Auth middleware for protected routes
      - type: modification
        description: Add auth to existing protected routes

  complexity:
    overall: medium
    factors:
      files_to_modify: 2
      new_patterns: 2
      external_dependencies: 2
      test_coverage: 2
      documentation: 1
      breaking_changes: 1
      unknown_territory: 1
    total_score: 11

  risks:
    - risk: "Password hashing library choice"
      likelihood: low
      impact: medium
      mitigation: "Use bcrypt, well-established"
    - risk: "JWT secret management"
      likelihood: medium
      impact: high
      mitigation: "Environment variable, document required setup"

  unknowns:
    - "Which routes should be protected?"
    - "OAuth integration needed?"
    - "Session vs JWT preference?"

  recommendations:
    approach: |
      Implement JWT-based auth with bcrypt password hashing.
      Start with login/register, add middleware, then protect routes.
    alternatives:
      - "Session-based auth with express-session"
      - "OAuth with passport.js"
    next_steps:
      - "Clarify auth requirements with user"
      - "Create detailed plan with writing-plans skill"

  confidence: 0.7
  evidence:
    - "Reviewed existing routes structure"
    - "Checked package.json for auth libraries"
    - "Examined similar features in codebase"
```
