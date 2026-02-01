---
name: design-patterns
description: Use when refactoring code or designing flexible systems. Covers creational, structural, and behavioral patterns with Python examples.
---

# Design Patterns

Classic object-oriented design patterns for building flexible, maintainable software.

## When to Use This Skill

Use this skill when:
- **Refactoring code** with complex conditionals or tight coupling
- **Designing systems** that need flexibility for future changes
- **Recognizing anti-patterns** that a design pattern would solve
- **Code reviews** where design decisions need validation
- **Explaining patterns** to team members

## Pattern Categories

### Creational Patterns
Focus on object creation mechanisms:
- **Factory Method** - Decouple object creation from usage
- **Singleton** - Single global instance
- **Builder** - Complex object construction step-by-step
- **Abstract Factory** - Families of related objects

### Structural Patterns
Deal with object composition:
- **Decorator** - Add behaviors dynamically
- **Facade** - Simplify complex subsystems
- **Adapter** - Make incompatible interfaces work together
- **Proxy** - Control access, caching, lazy loading

### Behavioral Patterns
Address communication between objects:
- **Observer** - Event notification/subscription
- **Strategy** - Interchangeable algorithms
- **Command** - Encapsulate requests as objects
- **State** - Behavior based on internal state

## Quick Reference

| Pattern | Use When | Complexity |
|---------|----------|------------|
| Factory Method | Creating objects without specifying exact class | Medium |
| Singleton | Need single global instance | Easy |
| Builder | Complex construction with many optional params | Medium |
| Decorator | Adding behaviors dynamically | Medium |
| Facade | Simplifying complex library/subsystem | Easy |
| Adapter | Integrating incompatible interfaces | Easy |
| Observer | Multiple objects need state change notifications | Medium |
| Strategy | Switching algorithms at runtime | Medium |
| Command | Undo/redo, queuing, scheduling operations | Medium |
| State | Object behavior varies by internal state | Hard |

## Pattern Selection Guide

**Problem: Large constructor with many optional parameters**
- Use: Builder

**Problem: Need to ensure only one instance exists**
- Use: Singleton

**Problem: Class explosion from multiple combinations**
- Use: Decorator (for behaviors) or Strategy (for algorithms)

**Problem: Complex library needs simpler interface**
- Use: Facade

**Problem: Objects need to be notified of changes**
- Use: Observer

**Problem: Large if/else or switch for algorithm selection**
- Use: Strategy

**Problem: Behavior changes based on object state**
- Use: State

## Reference Files

Detailed patterns with code examples:
- `references/creational.md` - Factory, Singleton, Builder, Abstract Factory
- `references/structural.md` - Decorator, Facade, Adapter, Proxy
- `references/behavioral.md` - Observer, Strategy, Command, State

## Key Principles

### SOLID Connection
- **Single Responsibility**: Each pattern isolates concerns
- **Open/Closed**: Decorator, Strategy enable extension without modification
- **Liskov Substitution**: Patterns use interfaces/abstract classes
- **Interface Segregation**: Small, focused interfaces
- **Dependency Inversion**: Depend on abstractions, not concretions

### When NOT to Use Patterns
- **Over-engineering**: Don't add patterns "just in case"
- **Simple problems**: If a simple solution works, use it
- **Premature abstraction**: Wait until you see the pattern emerge
- **Pattern fever**: Not every problem needs a pattern

## Common Anti-Patterns to Refactor

| Anti-Pattern | Symptom | Pattern Solution |
|--------------|---------|------------------|
| God Object | One class does everything | Facade + smaller classes |
| Spaghetti conditionals | Nested if/else for types | Strategy or State |
| Hardcoded dependencies | `new ConcreteClass()` everywhere | Factory Method |
| Copy-paste variations | Similar classes with slight differences | Template Method or Strategy |
| Callback hell | Deeply nested event handlers | Observer or Command |
