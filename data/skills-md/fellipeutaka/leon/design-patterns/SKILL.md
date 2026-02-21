---
name: design-patterns
description: |
  Apply Gang of Four design patterns to solve architectural problems in TypeScript.
  Use when refactoring code architecture, implementing extensible systems, decoupling
  components, or following SOLID principles. Covers all 22 GoF patterns: Creational
  (Factory Method, Abstract Factory, Builder, Prototype, Singleton), Structural
  (Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy), and Behavioral
  (Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State,
  Strategy, Template Method, Visitor).
---

# Design Patterns

Proven architectural patterns for building maintainable, extensible, and testable
TypeScript codebases. All 22 Gang of Four patterns with practical implementations.

## When to Apply

Reference these patterns when:

- Solving recurring architectural problems
- Refactoring tightly coupled code
- Building plugin/extension systems
- Making code more testable via dependency injection
- Reviewing PRs with architectural concerns
- Choosing between inheritance and composition

## Pattern Categories

### Creational Patterns

Create objects flexibly, hiding creation logic from consumers.

| Pattern              | Intent                                                    |
| -------------------- | --------------------------------------------------------- |
| **Factory Method**   | Delegate object creation to subclasses                    |
| **Abstract Factory** | Create families of related objects without concrete types  |
| **Builder**          | Construct complex objects step-by-step                    |
| **Prototype**        | Clone existing objects instead of building from scratch    |
| **Singleton**        | Ensure exactly one instance with global access             |

See `references/CREATIONAL.md` for implementations.

### Structural Patterns

Compose classes and objects into larger, flexible structures.

| Pattern       | Intent                                                        |
| ------------- | ------------------------------------------------------------- |
| **Adapter**   | Make incompatible interfaces work together                     |
| **Bridge**    | Separate abstraction from implementation                       |
| **Composite** | Treat individual objects and compositions uniformly            |
| **Decorator** | Attach responsibilities dynamically without subclassing        |
| **Facade**    | Simplify complex subsystem with a unified interface            |
| **Flyweight** | Share common state to reduce memory across many objects        |
| **Proxy**     | Control access to an object through a substitute               |

See `references/STRUCTURAL.md` for implementations.

### Behavioral Patterns

Manage algorithms, responsibilities, and communication between objects.

| Pattern                      | Intent                                                  |
| ---------------------------- | ------------------------------------------------------- |
| **Chain of Responsibility**  | Pass requests along a handler chain                     |
| **Command**                  | Encapsulate requests as objects for queuing/undo         |
| **Iterator**                 | Traverse collections without exposing internals          |
| **Mediator**                 | Centralize complex communication between objects         |
| **Memento**                  | Capture and restore object state                         |
| **Observer**                 | Notify dependents automatically on state changes         |
| **State**                    | Alter behavior when internal state changes               |
| **Strategy**                 | Swap algorithms at runtime                               |
| **Template Method**          | Define algorithm skeleton, let subclasses override steps |
| **Visitor**                  | Add operations to objects without modifying them         |

See `references/BEHAVIORAL.md` for implementations.

## Pattern Selection Guide

| Problem                                    | Pattern(s)                          |
| ------------------------------------------ | ----------------------------------- |
| Need to decouple object creation           | Factory Method, Abstract Factory    |
| Complex object with many optional fields   | Builder                             |
| Expensive object creation, need copies     | Prototype                           |
| Global shared resource (config, pool)      | Singleton                           |
| Incompatible third-party interface         | Adapter                             |
| Multiple dimensions of variation           | Bridge                              |
| Tree structures (files, UI, org charts)    | Composite                           |
| Add features without subclassing           | Decorator                           |
| Simplify complex API surface               | Facade                              |
| Thousands of similar objects, memory heavy | Flyweight                           |
| Lazy loading, access control, caching      | Proxy                               |
| Flexible request processing pipeline       | Chain of Responsibility             |
| Undo/redo, task queues, macros             | Command                             |
| Custom collection traversal                | Iterator                            |
| Many-to-many object communication          | Mediator                            |
| Snapshots, save/restore state              | Memento                             |
| Event systems, reactive updates            | Observer                            |
| Object behavior depends on its state       | State                               |
| Swappable algorithms (sort, compress, etc) | Strategy                            |
| Algorithm with fixed steps, variable parts | Template Method                     |
| Operations across heterogeneous objects    | Visitor                             |

## Best Practices

### DO

- Choose patterns that solve actual problems you're facing now
- Prefer composition over inheritance
- Use dependency injection to decouple components
- Keep pattern implementations simple — avoid gold-plating
- Document *why* a pattern was chosen (not just which one)
- Consider testability when choosing patterns
- Combine patterns when appropriate (e.g., Strategy + Factory)

### DON'T

- Apply patterns preemptively for hypothetical future needs
- Force a pattern where a simple function/object suffices
- Create unnecessary abstraction layers
- Use Singleton as a disguised global variable
- Choose inheritance when composition works better
- Ignore team familiarity — a simpler pattern everyone knows beats a "better" one nobody understands

## SOLID Quick Reference

| Principle                 | Summary                                              | Related Patterns                         |
| ------------------------- | ---------------------------------------------------- | ---------------------------------------- |
| **S**ingle Responsibility | One class, one reason to change                      | Strategy, Command, Observer              |
| **O**pen/Closed           | Open for extension, closed for modification          | Decorator, Strategy, Template Method     |
| **L**iskov Substitution   | Subtypes must be substitutable for base types        | Factory Method, Abstract Factory         |
| **I**nterface Segregation | Prefer small, focused interfaces                     | Adapter, Facade                          |
| **D**ependency Inversion  | Depend on abstractions, not concretions              | All patterns using interfaces/abstract   |
