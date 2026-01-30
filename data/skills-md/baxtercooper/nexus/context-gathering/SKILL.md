---
name: context-gathering
description: Use when entering an unfamiliar codebase, starting a new feature, or before any implementation task. Provides structured exploration protocol to understand before acting.
version: 1.0.0
---

# Context Gathering Skill

> **Core Principle**: Understand before acting.

## When to Invoke

- Starting work in an unfamiliar codebase
- Beginning a new feature implementation
- Before modifying code you haven't worked with before
- When requirements reference parts of the system you don't understand
- After a context switch to a different area of the codebase

## Exploration Protocol

Execute these phases in order. Do not skip phases.

### Phase 1: Architecture

**Objective**: Build mental map of the system.

```
1. Read documentation:
   - README.md (project purpose, setup)
   - docs/ directory (if exists)
   - CONTRIBUTING.md (conventions)
   - ARCHITECTURE.md (if exists)

2. Identify entry points:
   - Main entry file (main.py, index.ts, etc.)
   - CLI entry points
   - API routes/handlers
   - Event handlers

3. Map directory structure:
   - What does each top-level directory contain?
   - Where does business logic live?
   - Where are tests?
   - Where is configuration?
```

### Phase 2: Patterns

**Objective**: Understand existing conventions.

```
1. Find similar features:
   - Search for implementations like what you'll build
   - Note how they're structured
   - Identify reusable patterns

2. Identify coding conventions:
   - Naming patterns (camelCase, snake_case, etc.)
   - File organization (one class per file? grouped by feature?)
   - Error handling patterns
   - Logging patterns

3. Note test patterns:
   - Test file naming
   - Test structure (describe/it, test classes, etc.)
   - Mocking patterns
   - Test data patterns
```

### Phase 3: Dependencies

**Objective**: Understand external connections.

```
1. Check dependency files:
   - package.json / requirements.txt / Cargo.toml / etc.
   - Lock files for exact versions

2. Identify external services:
   - Databases
   - APIs
   - Message queues
   - Cache systems

3. Note version constraints:
   - Language version requirements
   - Framework version requirements
   - Breaking change warnings
```

### Phase 4: Document Findings

**Objective**: Create actionable summary.

Use the output template below to capture findings.

---

## Output Template

After exploration, produce this structured summary:

```yaml
context_gathering:
  timestamp: [ISO 8601]
  target: "[Area being explored]"

  project_understanding:
    purpose: |
      [What the project does - 1-2 sentences]
    architecture: |
      [How it's structured - key components and their relationships]
    tech_stack:
      - [Language/Framework 1]
      - [Language/Framework 2]

  relevant_files:
    entry_points:
      - path: [file path]
        purpose: [what it does]
    similar_implementations:
      - path: [file path]
        relevance: [why it's relevant to current task]
    test_examples:
      - path: [file path]
        pattern: [what pattern it demonstrates]

  conventions_noted:
    naming: "[pattern observed]"
    file_structure: "[pattern observed]"
    error_handling: "[pattern observed]"
    testing: "[pattern observed]"

  dependencies:
    internal:
      - "[Module/package this code depends on]"
    external:
      - name: "[package name]"
        version: "[version]"
        purpose: "[why it's used]"

  gaps_in_understanding:
    - "[Thing you couldn't figure out]"
    - "[Area that needs clarification]"

  confidence: 0.0
  evidence:
    - "[File read]"
    - "[Search performed]"
```

---

## Exploration Checklist

Before proceeding to implementation, verify:

- [ ] I know where to put new code
- [ ] I found at least one similar implementation to reference
- [ ] I understand the test patterns to follow
- [ ] I identified all external dependencies relevant to my task
- [ ] I documented any gaps in understanding
- [ ] I have confidence >= 0.7 in my understanding

> [!CRITICAL]
> If confidence < 0.7, DO NOT proceed to implementation.
> Either gather more context or escalate gaps to user.

---

## Anti-Patterns

### What NOT to Do

| Anti-Pattern | Problem | Instead |
|--------------|---------|---------|
| "I'll figure it out as I go" | Leads to inconsistent code | Complete exploration first |
| Skipping documentation | Miss important constraints | Always check docs first |
| Assuming conventions | Introduces inconsistency | Verify patterns in existing code |
| Ignoring test patterns | Tests won't fit project style | Study existing tests |
| Starting with implementation | May require extensive rework | Understand then implement |

---

## Integration with Other Skills

| After Context Gathering | Invoke |
|-------------------------|--------|
| Ready to plan implementation | → `writing-plans` skill |
| Multiple approaches identified | → `orchestration` skill to decompose |
| Writing new code | → `tdd` skill |

### Chaining Rules

1. **ALWAYS** complete context gathering before writing new code
2. **IF** gaps remain **THEN** ask user for clarification before proceeding
3. **IF** similar implementations found **THEN** reference them in your plan
4. **AFTER** context gathered **THEN** invoke `writing-plans` for implementation

---

## Example

**Task**: "Add a new API endpoint for user preferences"

**Context Gathering Output**:

```yaml
context_gathering:
  timestamp: "2024-01-15T10:30:00Z"
  target: "User preferences API endpoint"

  project_understanding:
    purpose: |
      REST API backend for user management application
    architecture: |
      Express.js with layered architecture: routes → controllers → services → repositories
    tech_stack:
      - Node.js 18
      - Express.js 4.x
      - PostgreSQL with Prisma ORM

  relevant_files:
    entry_points:
      - path: src/routes/index.ts
        purpose: Route registration
    similar_implementations:
      - path: src/routes/users.ts
        relevance: Similar CRUD endpoint structure
      - path: src/controllers/users.controller.ts
        relevance: Controller pattern to follow
      - path: src/services/users.service.ts
        relevance: Service layer pattern
    test_examples:
      - path: tests/routes/users.test.ts
        pattern: Integration tests with supertest

  conventions_noted:
    naming: "camelCase for variables, PascalCase for classes"
    file_structure: "Feature-based: routes/, controllers/, services/"
    error_handling: "Custom AppError class with HTTP status codes"
    testing: "Jest with supertest, one test file per route file"

  dependencies:
    internal:
      - "src/middleware/auth.ts (authentication)"
      - "src/utils/validators.ts (input validation)"
    external:
      - name: "express"
        version: "^4.18.0"
        purpose: "Web framework"
      - name: "prisma"
        version: "^5.0.0"
        purpose: "Database ORM"

  gaps_in_understanding:
    - "Unclear if preferences should be separate table or JSON column in users table"

  confidence: 0.75
  evidence:
    - "Read: src/routes/users.ts"
    - "Read: src/controllers/users.controller.ts"
    - "Read: tests/routes/users.test.ts"
    - "Searched: 'preferences' in codebase - no existing implementation"
```

**Next Step**: Ask user about database schema preference, then proceed to `writing-plans` skill.
