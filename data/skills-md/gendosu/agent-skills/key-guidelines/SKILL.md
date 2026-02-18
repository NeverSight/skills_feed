---
name: key-guidelines
description: |
  Core development principles and standards for consistent, high-quality code.
  Automatically applies DRY, KISS, YAGNI, SOLID, TDD, and micro-commit methodologies.
model: Haiku
---

# Key Guidelines

## Design Principles
- **DRY (Don't Repeat Yourself)**: Avoid code duplication
- **KISS (Keep It Simple, Stupid)**: Keep designs and code simple
- **YAGNI (You Ain't Gonna Need It)**: Don't implement features until actually needed. Extract methods/functions only when there's a concrete need for reuse, not in anticipation of it
- **SOLID Principles**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **SoC (Separation of Concerns)**: Separate system by concerns (UI, business logic, data access, etc.)

## Development Methodology
- **TDD Approach**: Use TDD methodology (Kent Beck style) to break down tasks during execution
- **Micro-commits**: One change per commit, strictly follow test-driven change cycles (Lucas Rocha's micro-commit methodology)

## Quality & Standards
- **Code Quality**: Run linters and type checkers before committing
- **Security**: Always follow security guidelines and scan for vulnerabilities
- **Documentation**: Keep technical documentation in `docs/` directory
- **Version Control**: Follow conventional commit messages and branching strategy
