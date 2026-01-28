---
name: tdd-workflow
description: Test-driven development guidance for Tetris game logic. Use when writing tests, fixing test failures, improving test coverage, or implementing game mechanics. Auto-triggers on phrases like "write a test", "test this function", "improve coverage", "fix failing tests", or "add game logic". Emphasizes Result<T,E> pattern and property-based testing with fast-check.
allowed-tools: Bash(bun test*), Read, Edit, Grep, Glob
---

# TDD Workflow for Tetris Game

Test-driven development guidance following the project's strict TDD requirements.

## TDD Principles

1. **Test First**: Write tests before implementation
2. **Red-Green-Refactor**: Fail → Pass → Improve
3. **Co-located Tests**: Test files must be next to implementation (`*.test.ts`)
4. **160+ Tests**: Comprehensive coverage for all game logic
5. **Property-based Testing**: Use fast-check for critical game mechanics

## Test Execution

```bash
# Run all tests (160+ tests)
bun test

# Run specific test file
bun test src/game/board.test.ts

# Run tests with coverage
bun test --coverage
```

## Testing Requirements

### ✅ Required Practices

- **Co-located Tests**: Place test files next to implementation
  ```
  src/game/
  ├── board.ts
  ├── board.test.ts       # ✅ Co-located
  ├── pieces.ts
  └── pieces.test.ts      # ✅ Co-located
  ```

- **Result<T, E> Pattern**: Game logic must return Result type
  ```typescript
  type Result<T, E> = { ok: true; value: T } | { ok: false; error: E }

  // Good example
  export const rotatepiece = (piece: Piece): Result<Piece, RotationError> => {
    // ...
  }
  ```

- **Block Bodies in forEach**: Avoid implicit returns in test loops
  ```typescript
  // ✅ Good
  testCases.forEach((testCase) => {
    expect(fn(testCase.input)).toBe(testCase.expected)
  })

  // ❌ Bad (implicit return)
  testCases.forEach(testCase => expect(fn(testCase.input)).toBe(testCase.expected))
  ```

- **Property-based Testing**: Use fast-check for game mechanics
  ```typescript
  import fc from 'fast-check'

  test('piece rotation is reversible', () => {
    fc.assert(
      fc.property(fc.integer(), (rotation) => {
        const piece = rotatePiece(basePiece, rotation)
        const reversed = rotatePiece(piece, -rotation)
        return deepEqual(reversed, basePiece)
      })
    )
  })
  ```

### ❌ Prohibited Practices

- ❌ Relaxing conditions to resolve test errors
- ❌ Skipping tests or using inappropriate mocking
- ❌ Hardcoding outputs or responses
- ❌ Ignoring or hiding error messages
- ❌ Temporary fixes that postpone problems

## TDD Workflow Steps

### 1. Write Failing Test (Red)
```typescript
// src/game/scoring.test.ts
test('T-Spin triple awards 1600 points', () => {
  const result = calculateScore({
    linesCleared: 3,
    isTSpin: true,
    level: 1
  })

  expect(result.ok).toBe(true)
  if (result.ok) {
    expect(result.value).toBe(1600)
  }
})
```

### 2. Implement Minimum Code (Green)
```typescript
// src/game/scoring.ts
export const calculateScore = (params: ScoreParams): Result<number, ScoreError> => {
  if (params.isTSpin && params.linesCleared === 3) {
    return { ok: true, value: 1600 }
  }
  // ... rest of implementation
}
```

### 3. Refactor (Clean)
- Improve code quality while keeping tests green
- Add edge case tests
- Use property-based testing for comprehensive coverage

## When This Skill Activates

- "Write a test for this function"
- "Test this game logic"
- "Improve test coverage"
- "Fix failing tests"
- "Add tests for edge cases"
- "Use TDD to implement this"
- "Property-based test for rotation"

## Test Structure Best Practices

```typescript
// src/game/board.test.ts
import { describe, test, expect } from 'bun:test'
import { createBoard, placePiece } from './board'
import fc from 'fast-check'

describe('Board Operations', () => {
  test('creates empty 20x10 board', () => {
    const board = createBoard()
    expect(board.length).toBe(20)
    expect(board[0].length).toBe(10)
  })

  test('placing piece updates board state', () => {
    const board = createBoard()
    const result = placePiece(board, piece, { x: 4, y: 0 })

    expect(result.ok).toBe(true)
    if (result.ok) {
      expect(result.value.board).not.toBe(board) // Immutability
    }
  })

  // Property-based test
  test('board operations preserve dimensions', () => {
    fc.assert(
      fc.property(fc.array(fc.array(fc.boolean())), (cells) => {
        const board = createBoardFromCells(cells)
        return board.length === 20 && board[0].length === 10
      })
    )
  })
})
```

## Advanced Testing Patterns

See [testing-patterns.md](testing-patterns.md) for:
- Complex Result<T, E> pattern usage
- Property-based testing strategies
- Test organization best practices
- Mocking guidelines
