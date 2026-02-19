---
name: software-patterns
description: Decision framework for architectural patterns including DI, SOA, Repository, Domain Events, Circuit Breaker, and Anti-Corruption Layer. Use when designing systems, choosing patterns, or reviewing architecture.
version: 1.0.0
languages: all
progressive_disclosure:
  entry_point:
    summary: "Decision framework for choosing and implementing core architectural patterns"
    when_to_use: "When designing new systems, adding integration points, managing complexity, or reviewing existing architecture"
    quick_start: "1. Identify the problem class 2. Check decision tree 3. Apply foundational patterns (DI+SOA) 4. Layer situational patterns as needed"
  references:
    - foundational-patterns.md
    - situational-patterns.md
    - anti-patterns.md
    - decision-trees.md
    - examples.md
tags:
  - architecture
  - patterns
  - design
  - dependency-injection
  - service-oriented
---

# Software Patterns Primer

## Overview

Architectural patterns solve specific structural problems. This skill provides a decision framework for when to apply each pattern, not a catalog to memorize.

**Core philosophy:** Patterns solve problems. No problem? No pattern needed.

## When to Use This Skill

Activate when:
- Designing a new system or major feature
- Adding external service integrations
- Code becomes difficult to test or modify
- Services start calling each other in circles
- Failures in one component cascade to others
- Business logic scatters across multiple locations

## Pattern Hierarchy

### Foundational (Apply by Default)

These patterns provide the structural foundation for maintainable systems. Apply unless you have specific reasons not to.

| Pattern | Problem Solved | Signal to Apply |
|---------|---------------|-----------------|
| **Dependency Injection** | Tight coupling, untestable code | Classes instantiate their own dependencies |
| **Service-Oriented Architecture** | Monolithic tangles, unclear boundaries | Business logic scattered, no clear ownership |

### Situational (Apply When Triggered)

These patterns address specific problems. Don't apply preemptively.

| Pattern | Problem Solved | Signal to Apply |
|---------|---------------|-----------------|
| **Repository** | Data access coupling | Services know about database details |
| **Domain Events** | Circular dependencies, temporal coupling | Service A calls B calls C calls A |
| **Anti-Corruption Layer** | External system coupling | External API changes break your code |
| **Circuit Breaker** | Cascading failures | One slow service takes down everything |

→ [Foundational Patterns Detail](references/foundational-patterns.md)
→ [Situational Patterns Detail](references/situational-patterns.md)

## Quick Decision Tree

```
Is code hard to test?
├─ Yes → Apply Dependency Injection
└─ No → Continue

Is business logic scattered?
├─ Yes → Apply Service-Oriented Architecture
└─ No → Continue

Do services know database details?
├─ Yes → Apply Repository Pattern
└─ No → Continue

Do services call each other in cycles?
├─ Yes → Apply Domain Events
└─ No → Continue

Does external API change break your code?
├─ Yes → Apply Anti-Corruption Layer
└─ No → Continue

Does one slow service break everything?
├─ Yes → Apply Circuit Breaker
└─ No → Current patterns sufficient
```

→ [Complete Decision Trees](references/decision-trees.md)

## Pattern Selection by Problem

### "My code is hard to test"
**Primary:** Dependency Injection
**Why:** Dependencies passed in = dependencies mockable

### "I don't know where business logic lives"
**Primary:** Service-Oriented Architecture
**Secondary:** Repository (if data access is the confusion)
**Why:** Clear boundaries = clear ownership

### "External API changes keep breaking my code"
**Primary:** Anti-Corruption Layer
**Why:** Translation layer absorbs external volatility

### "Services call each other in circles"
**Primary:** Domain Events
**Why:** Publish/subscribe breaks circular dependencies

### "One slow service takes down everything"
**Primary:** Circuit Breaker
**Secondary:** Retry with Backoff
**Why:** Fail fast prevents cascade

### "Database changes ripple through codebase"
**Primary:** Repository Pattern
**Why:** Abstraction layer isolates data access

→ [Real-World Examples](references/examples.md)

## Implementation Priority

When starting a new system:

1. **First:** Establish DI container/pattern
2. **Second:** Define service boundaries (SOA)
3. **Third:** Add Repository for data access
4. **Then:** Layer situational patterns as problems emerge

When refactoring existing system:

1. **First:** Identify the specific pain point
2. **Second:** Apply the minimal pattern that solves it
3. **Third:** Validate improvement before adding more

## Key Principles

**Minimal Sufficient Pattern**
Apply the simplest pattern that solves the problem. Over-architecting creates its own maintenance burden.

**Problem-First Selection**
Never ask "which patterns should I use?" Ask "what problem am I solving?"

**Composition Over Prescription**
Patterns combine. Repository + Domain Events + Circuit Breaker is common for external data sources.

**Explicit Over Implicit**
Dependencies should be visible. Service Locator hides them; DI exposes them.

## Navigation

### Pattern Details
- **[Foundational Patterns](references/foundational-patterns.md)**: DI and SOA implementation guides, when to deviate
- **[Situational Patterns](references/situational-patterns.md)**: Repository, Domain Events, ACL, Circuit Breaker details

### Decision Support
- **[Decision Trees](references/decision-trees.md)**: Complete flowcharts for pattern selection
- **[Anti-Patterns](references/anti-patterns.md)**: Common misapplications and how to recognize them

### Implementation
- **[Examples](references/examples.md)**: Language-agnostic pseudocode for each pattern combination

## Red Flags - STOP

STOP when:
- "Let me add all these patterns upfront" → Apply only what solves current problems
- "This pattern is best practice" → Best practice for what problem?
- "We might need this later" → YAGNI - add when needed
- "Service Locator is simpler" → Hidden dependencies cause testing pain
- "I'll just call this service directly" → Consider if events would decouple better
- "External API is stable, no need for ACL" → APIs always change eventually

**ALL of these mean: STOP. Identify the specific problem first.**

## Integration with Other Skills

- **test-driven-development**: DI enables testability; TDD validates pattern application
- **systematic-debugging**: Clear boundaries (SOA) simplify debugging
- **root-cause-tracing**: Well-structured services have clearer call chains

## Pattern Combinations

Common effective combinations:

| Scenario | Patterns |
|----------|----------|
| New microservice | DI + SOA + Repository |
| External API integration | DI + ACL + Circuit Breaker |
| Event-driven system | DI + SOA + Domain Events |
| Data-heavy application | DI + SOA + Repository + Unit of Work |

---

**Remember:** Patterns exist to solve problems. Start with the problem, not the pattern.
