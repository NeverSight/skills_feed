---
name: Critical Review
description: Critical and uncompromising review of work done
---

# Skill: Critical Review

## When to use this skill

- **After every implementation** - Validate work quality
- **Before a significant commit** - Ensure no technical debt is introduced
- **Before a release** - Full audit of modified code
- **When in doubt** - Objectively evaluate an approach

## Available templates

| Template | Usage |
|----------|-------|
| `templates/quick_checklist.md` | Quick validation checklist |
| `templates/review_report.md` | Detailed review report |

## Critical posture

> **Fundamental rule**: Never accept mediocre code. 
> Be your own harshest critic.

### Questions to ask SYSTEMATICALLY

#### 1. Code quality

- [ ] Is the code readable by another developer without explanation?
- [ ] Is there duplicate code that could be factored?
- [ ] Are variable/function names explicit?
- [ ] Is cyclomatic complexity reasonable?
- [ ] Do functions do one thing only (SRP)?

#### 2. Error handling

- [ ] Are all error cases handled properly?
- [ ] Are there hidden `.unwrap()`?
- [ ] Are error messages informative?
- [ ] Are errors propagated correctly?

#### 3. Tests

- [ ] Do tests cover nominal AND edge cases?
- [ ] Are tests independent from each other?
- [ ] Do tests document expected behavior?
- [ ] Would tests fail if the code was broken?

#### 4. Architecture

- [ ] Does the code respect DDD architecture?
- [ ] Are there dependencies in the wrong direction (domain → infrastructure)?
- [ ] Is coupling minimal between modules?
- [ ] Is the code easily testable?

#### 5. Performance

- [ ] Are there unnecessary allocations in hot paths?
- [ ] Are data structures appropriate?
- [ ] Are there blocking operations in async code?

## Evaluation grid

After each implementation, self-evaluate honestly:

| Criterion | Score | Description |
|-----------|-------|-------------|
| **Readability** | 1-5 | Does the code read like prose? |
| **Robustness** | 1-5 | Does it handle all edge cases? |
| **Testability** | 1-5 | Are tests complete and relevant? |
| **Maintainability** | 1-5 | Could another dev modify it easily? |
| **Performance** | 1-5 | Is the code efficient? |

**Minimum acceptable score: 3/5 on each criterion**

## Red flags to detect

### Critical code smells

```rust
// ❌ RED FLAG: unwrap without context
let value = some_option.unwrap();

// ❌ RED FLAG: potential hidden panic
let index = vec[user_input];

// ❌ RED FLAG: f64 for money
let total: f64 = price * quantity;

// ❌ RED FLAG: excessive clone
for item in collection.clone() { ... }

// ❌ RED FLAG: function too long (>50 lines)
fn do_everything() { /* 200 lines */ }

// ❌ RED FLAG: comment explaining obscure code
// This does X because Y (code should be self-explanatory)
```

### Architectural anti-patterns

| Anti-pattern | Symptom | Solution |
|--------------|---------|----------|
| God class | File >500 lines | Decompose into modules |
| Spaghetti | Circular dependencies | Invert dependencies |
| Anemic domain | Entities without behavior | Enrich domain model |
| Leaky abstraction | Implementation details exposed | Encapsulate correctly |

## Critical review checklist

Before considering work as complete:

### Mandatory
- [ ] No `.unwrap()` in production
- [ ] No `f64` for monetary calculations
- [ ] Tests pass and are relevant
- [ ] Clippy without warnings
- [ ] Documentation up to date

### Recommended
- [ ] Review diff before commit
- [ ] Re-read after a break
- [ ] Manual test of happy path

## Critical report format

After a review, document findings:

```markdown
## Critical Review - [Feature/Module]

### Positive points
- ...

### Points to improve
- **P0 (blocking)**: ...
- **P1 (important)**: ...
- **P2 (desirable)**: ...

### Technical debt identified
- ...

### Score: X/5
```

## Reference

For an in-depth analysis of the complete project, see:
`.agent/CRITICAL_ANALYSIS_PROMPT.md`
