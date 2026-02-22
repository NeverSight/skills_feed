---
name: architecture
description: Architectural decision-making framework combining requirements analysis, trade-off evaluation, ADR documentation, Clean Architecture, DDD principles, and code quality guidelines. Use when making architecture decisions, analyzing system design, writing code, or evaluating trade-offs.
allowed-tools: Read, Glob, Grep
---

# Architecture Decision Framework

> "Requirements drive architecture. Trade-offs inform decisions. ADRs capture rationale."

## Selective Reading Rule

**Read ONLY files relevant to the request!** Check the content map, find what you need.

| File | Description | When to Read |
|------|-------------|--------------|
| `context-discovery.md` | Questions to ask, project classification | Starting architecture design |
| `trade-off-analysis.md` | ADR templates, trade-off framework | Documenting decisions |
| `pattern-selection.md` | Decision trees, anti-patterns | Choosing patterns |
| `examples.md` | MVP, SaaS, Enterprise examples | Reference implementations |
| `patterns-reference.md` | Quick lookup for patterns | Pattern comparison |

---

## Core Principle

**"Simplicity is the ultimate sophistication."**

- Start simple
- Add complexity ONLY when proven necessary
- You can always add patterns later
- Removing complexity is MUCH harder than adding it

---

## Code Style Rules

### General Principles

- **Early return pattern**: Always use early returns over nested conditions for better readability
- Avoid code duplication through creation of reusable functions and modules
- Decompose long (80+ lines) components/functions into smaller ones. Keep in same file if single-use; split if file exceeds 200 lines
- Keep functions focused and under 50 lines when possible
- Avoid deep nesting (max 3 levels)
- Proper error handling with typed catch blocks

### Library-First Approach

- **ALWAYS search for existing solutions before writing custom code**
  - Check package registries for existing libraries
  - Evaluate existing services/SaaS solutions
  - Consider third-party APIs for common functionality
- **Custom code IS justified when:**
  - Specific business logic unique to the domain
  - Performance-critical paths with special requirements
  - When external dependencies would be overkill
  - Security-sensitive code requiring full control
- Remember: Every line of custom code is a liability that needs maintenance, testing, and documentation

### Architecture and Design

- **Clean Architecture & DDD Principles:**
  - Follow domain-driven design and ubiquitous language
  - Separate domain entities from infrastructure concerns
  - Keep business logic independent of frameworks
  - Define use cases clearly and keep them isolated
- **Naming Conventions:**
  - **AVOID** generic names: `utils`, `helpers`, `common`, `shared`
  - **USE** domain-specific names: `OrderCalculator`, `UserAuthenticator`, `InvoiceGenerator`
  - Follow bounded context naming patterns
  - Each module should have a single, clear purpose
- **Separation of Concerns:**
  - Do NOT mix business logic with UI components
  - Keep database queries out of controllers
  - Maintain clear boundaries between contexts

### Anti-Patterns to Avoid

- **NIH (Not Invented Here) Syndrome**: Don't build what already exists (auth, state management, form validation)
- **Generic Naming**: No `utils.js` with 50 unrelated functions, no `helpers/misc.js` as a dumping ground
- **Poor Boundaries**: Mixing business logic with UI, database queries in controllers, unclear separation of concerns

---

## Tech Stack Coverage

**Languages:** TypeScript, JavaScript, Python, Go, Swift, Kotlin
**Frontend:** React, Next.js, React Native, Flutter
**Backend:** Node.js, Express, GraphQL, REST APIs
**Database:** PostgreSQL, Prisma, NeonDB, Supabase
**DevOps:** Docker, Kubernetes, Terraform, GitHub Actions
**Cloud:** AWS, GCP, Azure

---

## Validation Checklist

Before finalizing architecture:

- [ ] Requirements clearly understood
- [ ] Constraints identified
- [ ] Each decision has trade-off analysis
- [ ] Simpler alternatives considered
- [ ] ADRs written for significant decisions
- [ ] Team expertise matches chosen patterns
- [ ] Code follows Clean Architecture boundaries
- [ ] No premature optimization or over-engineering
