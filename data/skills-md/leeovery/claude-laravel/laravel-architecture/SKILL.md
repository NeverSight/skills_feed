---
name: laravel-architecture
description: High-level architecture decisions, patterns, and project structure. Use when user asks about architecture decisions, project structure, pattern selection, or mentions how to organize, which pattern to use, best practices, architecture.
---

# Laravel Architecture

High-level architectural guidance for Laravel applications.

## Core Concepts

**[philosophy.md](references/philosophy.md)** - Foundational principles:
- Declarative code above all else
- Strict separation of concerns
- Type safety first
- All core architectural principles

**[patterns.md](references/patterns.md)** - Pattern overview:
- Actions for domain logic
- DTOs for data transfer
- State machines for complex state
- Services for external integration
- Workflows for multi-step processes
- Value objects for domain values

**[decisions.md](references/decisions.md)** - Pattern selection:
- When to use each pattern
- Decision flowcharts
- Architectural trade-offs
- Common scenarios

**[structure.md](references/structure.md)** - Directory structure:
- Complete project organization
- File placement rules
- Namespace conventions
- Web vs API distinction

**[examples.md](references/examples.md)** - Reference implementations:
- Complete working examples
- End-to-end workflows
- Real-world patterns

**[checklist.md](references/checklist.md)** - Implementation checklist:
- Setup tasks
- Feature development workflow
- Production deployment steps

## Core Principles

1. **Actions contain domain logic** - Business logic lives in invokable action classes
2. **Never pass primitives** - Always use DTOs for data transfer
3. **Thin HTTP layer** - Controllers only handle HTTP concerns
4. **Custom query builders** - Type-safe queries over scopes
5. **Strict typing** - `declare(strict_types=1)` in every file

## Quick Decision Tree

Need to...
- **Handle domain logic?** → Action
- **Transfer data?** → DTO
- **Validate user input?** → Form Request
- **Simple state field?** → Enum
- **Complex state transitions?** → State Machine
- **External API?** → Service with Saloon
- **Background processing?** → Job (delegates to Action)

Read decision flowcharts in **[decisions.md](references/decisions.md)** for detailed guidance.
