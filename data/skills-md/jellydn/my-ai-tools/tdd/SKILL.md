---
name: tdd
description: Guides through the complete TDD workflow with Red-Green-Refactor cycle
license: MIT
compatibility: claude, opencode, amp, codex, gemini
hint: Use when doing test-driven development with Red-Green-Refactor cycle
user-invocable: true
metadata:
  audience: all
  workflow: testing
---

# Test-Driven Development (TDD)

Guides you through the complete TDD workflow with Red-Green-Refactor cycle.

## Usage

`/tdd <ACTION> [ARGUMENTS]`

## Actions

- **start <FEATURE>** - Initialize TDD session for a feature
- **red <TEST_NAME>** - Create failing test (Red phase)
- **green** - Run tests and implement code (Green phase)
- **refactor** - Guide refactoring process (Refactor phase)
- **cycle <FEATURE>** - Run complete Red-Green-Refactor cycle
- **watch** - Start test watcher for continuous feedback
- **status** - Show current test status and next steps
- **help** - Show this help

## TDD Principles

### The Red-Green-Refactor Cycle

1. **Red**: Write a failing test that defines desired behavior
2. **Green**: Write minimal code to make the test pass
3. **Refactor**: Improve code quality while keeping tests green

### Best Practices

- Write tests first - Tests define the interface and behavior
- Small steps - Make tiny, incremental changes
- Fast feedback - Run tests frequently for immediate validation
- Clean code - Refactor regularly to maintain quality
- One concept per test - Keep tests focused and atomic
- AAA Pattern - Structure tests as Arrange, Act, Assert
- Black-box testing - Test only public methods and behavior, not implementation details

## Process

### For "start <FEATURE>":

1. Initialize TDD session for the feature
2. Create or identify target source file
3. Create corresponding test file if it doesn't exist
4. Explain the feature requirements and acceptance criteria

### For "red <TEST_NAME>":

1. Create a failing test that describes the desired behavior
2. Ensure test fails for the right reason (not syntax errors)
3. Run tests to confirm red state
4. Explain what the test is validating

### For "green":

1. Implement minimal code to make failing tests pass
2. Focus on making tests pass, not perfect code
3. Run tests to confirm green state
4. Avoid over-engineering at this stage

### For "refactor":

1. Improve code quality while maintaining green tests
2. Remove duplication and improve design
3. Run tests continuously during refactoring
4. Make one refactoring change at a time

## Test Template

A test template is available at `$SKILL_PATH/templates/test-template.md`:

```typescript
import { describe, it, expect } from 'vitest'
import { functionName } from './module'

describe('functionName', () => {
  it('should return formatted output when given valid input', () => {
    // Arrange - Setup test scenario
    const input = 'test input'
    const expectedOutput = 'expected output'

    // Act - Execute the unit under test
    const result = functionName(input)

    // Assert - Verify expected outcome
    expect(result).toBe(expectedOutput)
  })
})
```

## Common Commands

- Run tests: `npm test` or `pnpm test`
- Watch mode: `npm test --watch`
- With coverage: `npm test --coverage`
