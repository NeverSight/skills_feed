---
name: testing
description: Testing - Principes TDD/BDD. Use when writing tests, reviewing test coverage, or setting up testing.
triggers:
  files: ["*Test*.cs", "*Tests.cs", "*.Tests.csproj", "**/tests/**"]
  keywords: ["test", "coverage", "TDD", "BDD", "xUnit", "mock", "assert"]
auto_suggest: true
---

# Testing - Principes TDD/BDD

This skill provides guidelines and best practices for testing.

See @REFERENCE.md for detailed documentation.

## Quick Reference

- **TDD Cycle**: RED → GREEN → REFACTOR
- **Coverage Target**: ≥ 80%
- **Stack**: xUnit + FluentAssertions + Moq + Bogus + Testcontainers
- **Pattern**: Arrange-Act-Assert (AAA)
- **Naming**: `MethodName_StateUnderTest_ExpectedBehavior`
