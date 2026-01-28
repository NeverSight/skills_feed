---
name: Type Hints
description: Python type hints, type checking, and static analysis with mypy
version: "2.1.0"
sasmp_version: "1.3.0"
bonded_agent: 07-best-practices
bond_type: PRIMARY_BOND

# Skill Configuration
retry_strategy: exponential_backoff
observability:
  logging: true
  metrics: type_coverage_percent
---

# Python Type Hints Skill

## Overview
Master Python type hints for better code quality, IDE support, and static type checking with mypy.

## Topics Covered

### Basic Type Hints
- Variable annotations
- Function signatures
- Return types
- Optional types
- Union types

### Advanced Typing
- Generic types
- TypeVar and ParamSpec
- Protocol and structural typing
- Literal types
- TypedDict

### Type Checking
- mypy configuration
- Strict mode settings
- Type ignore comments
- Stub files (.pyi)
- Type coverage

### Runtime Types
- typing_extensions
- Pydantic validation
- Runtime type checking
- Dataclasses with types
- attrs integration

### Best Practices
- Gradual typing strategy
- Third-party type stubs
- CI type checking
- Documentation with types
- Type-driven development

## Prerequisites
- Python fundamentals
- OOP concepts

## Learning Outcomes
- Write type-annotated code
- Configure mypy properly
- Use generic types
- Implement protocols
