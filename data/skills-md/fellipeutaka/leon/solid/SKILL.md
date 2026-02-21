---
name: solid
description: |
  Apply SOLID principles to write flexible, maintainable, and testable code.
  Use when designing classes, interfaces, and module boundaries. Covers Single
  Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and
  Dependency Inversion with practical TypeScript examples and detection heuristics.
---

# SOLID Principles

Five principles for building software that is easy to understand, extend, and
maintain. They reduce coupling, increase cohesion, and make code testable.

## When to Apply

Reference these principles when:

- Designing new classes, modules, or interfaces
- Refactoring code with too many responsibilities
- Reviewing PRs for architectural concerns
- Breaking apart god objects or fat interfaces
- Deciding where to draw module boundaries
- Making code more testable

## Quick Reference

| Principle | One-Liner | Red Flag |
| --------- | --------- | -------- |
| **S**RP | One reason to change | "This class handles X *and* Y *and* Z" |
| **O**CP | Add, don't modify | Growing `if/else` or `switch` chains for types |
| **L**SP | Subtypes are substitutable | Type-checking or special-casing in calling code |
| **I**SP | Small, focused interfaces | Empty method implementations or `throw new Error("Not implemented")` |
| **D**IP | Depend on abstractions | `new ConcreteClass()` inside business logic |

See `references/PRINCIPLES.md` for detailed explanations and TypeScript examples.

## Detection Checklist

Ask these questions for every class and module:

| Question | Violated Principle |
| -------- | ------------------ |
| Does this class have multiple reasons to change? | SRP |
| Do I need to modify existing code to add a new variant? | OCP |
| Does calling code need type-checks or special cases for subtypes? | LSP |
| Are implementors forced to stub out unused methods? | ISP |
| Does high-level logic directly instantiate infrastructure? | DIP |

## Applying SOLID at Different Scales

| Scale | SRP | OCP | LSP | ISP | DIP |
| ----- | --- | --- | --- | --- | --- |
| **Function** | Does one thing | — | — | — | Takes abstractions as params |
| **Class** | One reason to change | Extend via composition | Subtypes honor contracts | Implements only what it uses | Constructor injection |
| **Module** | One bounded context | Plugin architecture | Interchangeable implementations | Thin public API | Depends inward |
| **Service** | Single domain | New features = new services | API contract stability | Minimal API surface | Abstractions at boundaries |

## Relationships Between Principles

- **SRP + ISP**: Splitting responsibilities often means splitting interfaces too
- **OCP + DIP**: Depending on abstractions is what makes extension without modification possible
- **LSP + OCP**: If subtypes are substitutable, you can extend behavior by adding new subtypes
- **DIP + ISP**: Small focused interfaces make dependency inversion practical

## Common Anti-Patterns

| Anti-Pattern | Violated Principles | Fix |
| ------------ | ------------------- | --- |
| God class doing everything | SRP | Extract focused classes |
| `switch` on type across codebase | OCP, LSP | Replace with polymorphism |
| Subclass that throws "not supported" | LSP, ISP | Redesign hierarchy, split interface |
| Fat interface with 20 methods | ISP | Split into role-based interfaces |
| Business logic importing DB driver | DIP | Inject repository interface |
| Service creating its own dependencies | DIP | Constructor injection |

## Best Practices

### DO

- Start with SRP — it's the foundation for all others
- Use interfaces to define boundaries between components
- Let violations emerge from real problems, then fix them
- Prefer composition over inheritance for extending behavior
- Keep interfaces small and role-specific
- Inject dependencies through constructors

### DON'T

- Apply SOLID dogmatically to trivial code (a 5-line utility doesn't need an interface)
- Create abstractions before you have at least two implementations
- Confuse SRP with "single method" — it's about reasons to change, not size
- Force Liskov compliance on classes that shouldn't be in the same hierarchy
- Over-segregate interfaces into single-method fragments when a cohesive group makes sense
