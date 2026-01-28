---
name: typescript-strict
description: Enforce TypeScript strict mode practices and type safety in Tetris codebase. Use when writing game logic, handling errors, improving type safety, or fixing type errors. Auto-triggers on phrases like "fix type errors", "improve type safety", "handle this error", or "make this type-safe". Focuses on Result<T,E> pattern, proper type guards, and avoiding type assertions.
allowed-tools: Read, Edit, Grep, Glob, Bash(bun run typecheck*)
---

# TypeScript Strict Mode Enforcer

Ensure strict TypeScript practices and type safety across the Tetris codebase.

## Core Principles

1. **No `any` Types**: Use `unknown` and type guards instead
2. **No Type Assertions**: Use type guards and narrowing
3. **No Non-null Assertions (`!`)**: Use optional chaining and type guards
4. **Result<T, E> Pattern**: For game logic error handling
5. **Exhaustive Type Checking**: Handle all union type cases

## Type Safety Patterns

### 1. Replace `any` with `unknown`

```typescript
// ❌ Prohibited
function process(data: any) {
  return data.value
}

// ✅ Required
function process(data: unknown) {
  if (isValidData(data)) {
    return data.value  // Type-safe after guard
  }
  return null
}

function isValidData(data: unknown): data is ValidData {
  return (
    typeof data === 'object' &&
    data !== null &&
    'value' in data
  )
}
```

### 2. Avoid Type Assertions

```typescript
// ❌ Prohibited
const element = document.getElementById('game') as HTMLCanvasElement

// ✅ Required
const element = document.getElementById('game')
if (element instanceof HTMLCanvasElement) {
  // Type-safe usage
}
```

### 3. Use Optional Chaining

```typescript
// ❌ Prohibited
const score = gameState!.score!.value

// ✅ Required
const score = gameState?.score?.value ?? 0
```

### 4. Result<T, E> Pattern for Game Logic

```typescript
type Result<T, E> = { ok: true; value: T } | { ok: false; error: E }

// ✅ Recommended for game logic
export const rotatePiece = (
  piece: Piece,
  board: Board
): Result<Piece, RotationError> => {
  const rotated = calculateRotation(piece)

  if (hasCollision(rotated, board)) {
    return { ok: false, error: 'COLLISION' }
  }

  return { ok: true, value: rotated }
}

// Usage
const result = rotatePiece(currentPiece, board)
if (result.ok) {
  setPiece(result.value)
} else {
  handleError(result.error)
}
```

### 5. Exhaustive Type Checking

```typescript
type Direction = 'UP' | 'DOWN' | 'LEFT' | 'RIGHT'

function move(direction: Direction): void {
  switch (direction) {
    case 'UP':
      return moveUp()
    case 'DOWN':
      return moveDown()
    case 'LEFT':
      return moveLeft()
    case 'RIGHT':
      return moveRight()
    default:
      // Exhaustiveness check
      const _exhaustive: never = direction
      throw new Error(`Unhandled direction: ${_exhaustive}`)
  }
}
```

## Type Guard Patterns

### Basic Type Guards

```typescript
// String type guard
function isString(value: unknown): value is string {
  return typeof value === 'string'
}

// Object type guard
function isGameState(value: unknown): value is GameState {
  return (
    typeof value === 'object' &&
    value !== null &&
    'board' in value &&
    'currentPiece' in value &&
    'score' in value
  )
}

// Array type guard
function isStringArray(value: unknown): value is string[] {
  return Array.isArray(value) && value.every((item) => typeof item === 'string')
}
```

### Advanced Type Guards

```typescript
// Discriminated union type guard
type Shape =
  | { type: 'circle'; radius: number }
  | { type: 'square'; side: number }
  | { type: 'rectangle'; width: number; height: number }

function isCircle(shape: Shape): shape is Extract<Shape, { type: 'circle' }> {
  return shape.type === 'circle'
}

// Usage
if (isCircle(shape)) {
  console.log(shape.radius)  // Type-safe
}
```

## Error Handling Patterns

### 1. Result Type for Errors

```typescript
type ParseError = 'INVALID_FORMAT' | 'MISSING_FIELD' | 'TYPE_MISMATCH'

function parseConfig(data: unknown): Result<Config, ParseError> {
  if (!isObject(data)) {
    return { ok: false, error: 'INVALID_FORMAT' }
  }

  if (!('boardSize' in data)) {
    return { ok: false, error: 'MISSING_FIELD' }
  }

  if (typeof data.boardSize !== 'number') {
    return { ok: false, error: 'TYPE_MISMATCH' }
  }

  return { ok: true, value: data as Config }
}
```

### 2. Never Type for Unreachable Code

```typescript
function assertNever(value: never): never {
  throw new Error(`Unexpected value: ${value}`)
}

// Usage in exhaustive checks
type PieceType = 'I' | 'O' | 'T' | 'S' | 'Z' | 'J' | 'L'

function getPieceColor(type: PieceType): string {
  switch (type) {
    case 'I': return 'cyan'
    case 'O': return 'yellow'
    case 'T': return 'purple'
    case 'S': return 'green'
    case 'Z': return 'red'
    case 'J': return 'blue'
    case 'L': return 'orange'
    default:
      return assertNever(type)  // Compile error if case missed
  }
}
```

## Type Safety Checklist

- [ ] No `any` types (use `unknown` + type guards)
- [ ] No type assertions (`as`)
- [ ] No non-null assertions (`!`)
- [ ] Result<T, E> for game logic errors
- [ ] Proper type guards for narrowing
- [ ] Exhaustive union type handling
- [ ] Optional chaining (`?.`) for nullable values

## Type Checking

```bash
# Run TypeScript type checker
bun run typecheck

# Watch mode during development
bun x tsc --noEmit --watch
```

## When This Skill Activates

- "Fix type errors"
- "Improve type safety"
- "Handle this error properly"
- "Make this type-safe"
- "Add type guards"
- "Remove type assertions"

