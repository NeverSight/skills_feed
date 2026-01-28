---
name: architecture-design-critique
description: Perform a codebase-wide architectural review through a Ports & Adapters (hexagonal architecture) lens. Assess boundary violations, coupling issues, and dependency direction. Produces a prioritized improvement roadmap. Use when reviewing architecture for testability/portability, assessing technical debt, planning refactoring efforts, or evaluating codebase health. Triggers on requests like "review the architecture", "assess coupling", "hexagonal analysis", "check boundary violations", or "architecture critique".
---

# Architecture Design Critique

Assess how well a codebase separates core domain logic from infrastructure concerns. Three phases with distinct mindsets to prevent jumping to recommendations without understanding what exists.

**Key questions answered**: Can you swap your database without rewriting business logic? Can you test domain rules without spinning up external services? Will the architecture support 10x growth?

### Ports & Adapters in 30 Seconds

The core idea: your domain logic (business rules, core algorithms) should never directly depend on infrastructure (databases, HTTP, file systems, external APIs). Instead:

- **Ports**: Interfaces that define what the domain needs (e.g., `UserRepository`, `PaymentGateway`)
- **Adapters**: Implementations that connect ports to real infrastructure (e.g., `PostgresUserRepository`, `StripePaymentGateway`)

Dependencies point inward: adapters depend on ports, never the reverse. This makes the core testable, portable, and resistant to infrastructure churn.

### Output Structure

**Before starting, ask the user for an output directory** (e.g., `./docs/architecture/` or `./reviews/`).

Create a subfolder with a meaningful name based on the project or focus area:
```
{output-directory}/
└── {project-name}-architecture-review/
    ├── 01-inventory.md      # Phase 1: Architectural Inventory
    ├── 02-assessment.md     # Phase 2: Architectural Assessment
    └── 03-roadmap.md        # Phase 3: Improvement Roadmap
```

**Naming the subfolder**: Use the project name or a descriptive label, e.g.:
- `acme-api-architecture-review/`
- `payments-service-review/`
- `monolith-decomposition-analysis/`

Write each document as you complete its phase. This creates a persistent record the team can reference, share, and update over time.

---

## Phase 1: Research

**Use the `/codebase-librarian` skill** to create a comprehensive inventory of the codebase.

The librarian skill will systematically catalog:
- Project foundation (language, tooling, dependencies)
- Entry points (HTTP, CLI, workers, consumers)
- Services and module boundaries
- Infrastructure (databases, caches, queues, external APIs)
- Domain model (entities, relationships)
- Data flows (end-to-end request traces)
- Existing patterns and conventions

**Output**: Save the inventory to `01-inventory.md` in the review folder.

The goal is to know exactly what exists before any critique begins. No opinions—just facts.

---

## Phase 2: Critique

**Persona: Senior Platform Engineer with Strong Design Taste**

*Mindset: Big-picture thinker who cares deeply about sustainable architecture. You've seen codebases thrive and rot. You focus on structural integrity, not cosmetic issues. Style guide violations and naming conventions are beneath your concern—you're looking at whether this architecture will support the next 5 years of growth.*

### Focus Areas

| Area | What to Look For |
|------|------------------|
| **Boundary violations** | Domain logic importing infrastructure (e.g., `Order.save()` calling SQL directly) |
| **Coupling** | Can components be tested/replaced independently? |
| **Dependency direction** | Do dependencies point inward toward the domain, or outward toward infrastructure? |
| **Infrastructure portability** | Could you swap databases/frameworks without touching core logic? |
| **Pattern coherence** | Is the architecture consistent, or a patchwork of different approaches? |
| **Scaling bottlenecks** | What breaks when load, team size, or feature count grows? |

### What to Ignore

Don't waste time on:
- Code style and formatting
- Naming conventions
- Minor duplication
- Individual function implementations
- Test coverage numbers

These matter, but they're not architectural. Stay at the structural level.

### Critique Process

```
1. For each domain concept, check: does it know about its persistence mechanism?
2. For each external dependency, check: is it accessed through an abstraction?
3. Trace a feature addition: how many layers need to change?
4. Imagine swapping the database: what files would you touch?
5. Check test files: can domain logic be tested without mocking infrastructure?
```

### Output Format

Write findings to `02-assessment.md` using this structure:

```markdown
# Architectural Assessment: [Project Name]

## Executive Summary
[2-3 paragraph narrative covering:]
- Overall health assessment (strong / mixed / needs attention)
- Key strengths worth preserving
- Primary concerns and their business/technical impact
- Thesis statement: "This codebase does X well, but struggles with Y"

## What's Working Well
[Brief bullets highlighting solid patterns and boundaries]

## Detailed Findings

### Finding 1: [Descriptive Title]

**Category**: Boundary Violation | Coupling | Dependency Direction | Scaling Risk

**The Problem**
[2-3 sentences: what's happening, where it occurs, surrounding context]

**Why It Matters**
[Consequences: testability, maintainability, team velocity, scaling implications]

**Evidence**
- `file.py:123` - [code reference with explanation]
- `other_file.py:45` - [additional evidence]

**Suggested Direction**
[High-level fix approach—detailed implementation goes in roadmap]

---

[Repeat for each significant finding]
```

Reference specific files and line numbers. Be direct about problems—sugarcoating doesn't help. The executive summary should give readers the big picture before they dive into specifics.

---

## Phase 3: Priority Ranking

**Persona: Seasoned Engineering Manager (Technical Leader)**

*Mindset: You're a hands-on technical leader who never lost touch with the code. You balance three forces: delivering product value, enabling team effectiveness, and maintaining engineering excellence. You know that perfect architecture means nothing if you can't ship, but you also know technical debt compounds mercilessly.*

### Evaluation Criteria

For each issue identified in Phase 2, assess:

| Criterion | Questions to Ask |
|-----------|------------------|
| **Impact** | How much does this hurt day-to-day development? |
| **Effort** | How much work to fix? Days, weeks, or months? |
| **Risk** | What could go wrong? What's the blast radius if it fails? |
| **Dependencies** | Does this block other improvements? |
| **Business alignment** | Does fixing this enable upcoming product needs? |

### Priority Tiers

**Quick Wins** (days, not weeks)
- High impact, low risk
- Can be done opportunistically alongside feature work
- Examples: extract interface, move misplaced file, add missing abstraction boundary

**Medium-term** (weeks)
- Meaningful effort but clear path forward
- Requires dedicated time but pays dividends
- Examples: introduce repository pattern, consolidate duplicate infrastructure, establish module boundaries

**Long-term Projects** (quarters)
- Architectural changes requiring sustained investment
- Must be balanced against feature delivery
- Examples: decompose monolith, introduce domain events, migrate data layer

### Output Format

Write findings to `03-roadmap.md` using this structure:

```markdown
# Improvement Roadmap: [Project Name]

## Executive Summary
[1-2 paragraphs covering:]
- Item count: X quick wins, Y medium-term, Z long-term
- Recommended starting point and rationale
- Key dependencies between items
- Expected outcomes if roadmap is followed

## Quick Wins

### 1. [Descriptive Title]

**Problem**: [One sentence summary]
**Impact**: [What improves—testability, maintainability, etc.]

**Implementation Approach**

Step-by-step guidance with code examples:

1. Create the port interface:
   ```python
   class CachePort(Protocol):
       def get(self, key: str) -> Optional[str]: ...
       def set(self, key: str, value: str, ttl: int) -> None: ...
   ```

2. Implement the adapter:
   ```python
   class RedisCacheAdapter(CachePort):
       def __init__(self, client: Redis):
           self._client = client
       # ... implementation
   ```

3. Wire it up:
   - Modify constructor to accept port
   - Update composition root / dependency injection

**Files to Modify**
- `domain/ports/cache.py` (new)
- `infrastructure/redis_cache.py` (new)
- `services/planner.py:117-121` (inject dependency)

**Verification**
- Existing tests should pass unchanged
- Add unit test with mock cache implementation

---

## Medium-term

### 2. [Title]
[Same structure as above with appropriate depth]

---

## Long-term

### 3. [Title]
[Same structure—can be higher-level for larger efforts]
```

Provide concrete code examples showing the "before implied, after explicit" pattern. Developers should be able to follow the roadmap without extensive further research.

---

## Architectural Red Flags

Quick reference for common violations to look for:

### Boundary Violations
- Domain entities with `save()`, `load()`, or `delete()` methods that call infrastructure
- Business logic inside HTTP handlers or database repositories
- Domain models importing ORM decorators or framework code
- Validation rules living in controllers instead of domain

### Coupling Smells
- Everything imports a "god" utility module
- Circular dependencies between packages
- Feature A directly instantiates Feature B's internal classes
- Configuration scattered across multiple layers

### Dependency Direction Issues
- Core domain package imports from infrastructure package
- Business rules reference specific database types (e.g., `postgres.Connection`)
- Domain entities have JSON/XML serialization annotations

### Missing Abstractions
- Direct `fetch()` or HTTP client calls in business logic
- Raw SQL queries in service classes
- File system operations mixed with domain calculations

---

**Example output**: See [references/example-output.md](references/example-output.md) for a complete e-commerce codebase critique example.
