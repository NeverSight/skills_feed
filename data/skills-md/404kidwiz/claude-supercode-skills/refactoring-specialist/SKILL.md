---
name: refactoring-specialist
description: Expert in improving code structure without changing behavior. Specializes in Design Patterns, SOLID principles, and Anti-Corruption Layers.
---

# Refactoring Specialist

## Purpose
Provides expertise in systematically improving code quality and structure without altering external behavior. Specializes in applying design patterns, enforcing SOLID principles, and managing technical debt through incremental refactoring strategies.

## When to Use
- Improving code readability and maintainability
- Reducing code duplication and complexity
- Applying design patterns to solve structural problems
- Breaking apart monolithic classes or functions
- Introducing proper abstraction layers
- Preparing codebase for new feature development
- Migrating legacy code to modern patterns
- Establishing anti-corruption layers between systems

## Quick Start
**Invoke this skill when:**
- Improving code readability and maintainability
- Reducing code duplication and complexity
- Applying design patterns to solve structural problems
- Breaking apart monolithic classes or functions
- Introducing proper abstraction layers

**Do NOT invoke when:**
- Adding new features (refactor first, then add) → use appropriate domain skill
- Debugging runtime errors → use debugger
- Reviewing code for security issues → use security-auditor
- Optimizing performance bottlenecks → use performance-engineer

## Decision Framework
```
Code Smell Detected?
├── Duplication → Extract Method/Class, Template Method pattern
├── Long Method → Extract Method, Decompose Conditional
├── Large Class → Extract Class, Single Responsibility
├── Feature Envy → Move Method to appropriate class
├── Primitive Obsession → Introduce Value Objects
├── Shotgun Surgery → Move related changes together
└── Divergent Change → Split by responsibility
```

## Core Workflows

### 1. Safe Refactoring Cycle
1. Ensure comprehensive test coverage exists
2. Identify specific code smell to address
3. Apply smallest possible refactoring step
4. Run tests to verify behavior unchanged
5. Commit the change
6. Repeat until smell eliminated

### 2. Pattern Introduction
1. Identify recurring structural problem
2. Select appropriate design pattern
3. Create new structure alongside existing code
4. Migrate consumers incrementally
5. Remove old implementation
6. Document pattern usage for team

### 3. Anti-Corruption Layer Implementation
1. Identify boundary between systems/domains
2. Define clean interface for internal domain
3. Create adapter/translator layer
4. Route all cross-boundary calls through ACL
5. Evolve internal model independently

## Best Practices
- Always refactor with tests as a safety net
- Make small, incremental changes with frequent commits
- Refactor before adding new features, not during
- Use IDE refactoring tools for mechanical transformations
- Document why patterns were applied, not just what
- Prioritize refactoring by business value and risk

## Anti-Patterns
- **Big Bang refactoring** → Use incremental strangler pattern
- **Refactoring without tests** → Add characterization tests first
- **Over-engineering** → Apply patterns only when needed
- **Refactoring during feature work** → Separate refactoring commits
- **Ignoring team conventions** → Align with existing codebase style
