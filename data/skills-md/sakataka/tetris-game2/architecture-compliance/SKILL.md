---
name: architecture-compliance
description: Verify Tetris architecture compliance with coding rules and design patterns. Use when reviewing code, implementing features, refactoring, or validating architectural decisions. Auto-triggers on phrases like "review this code", "check architecture", "is this correct?", "refactor this", or "implement feature". Checks for prohibited patterns (classes, enums, any types, hardcoded strings) and required patterns (functional programming, Result type, proper imports).
allowed-tools: Read, Grep, Glob
---

# Architecture Compliance Checker

Automatically verify code compliance with Tetris project architecture rules.

## Prohibited Patterns ❌

### 1. Classes and Enums
```typescript
// ❌ Prohibited
class GameState { }
enum Direction { UP, DOWN, LEFT, RIGHT }

// ✅ Required
type GameState = { /* ... */ }
type Direction = 'UP' | 'DOWN' | 'LEFT' | 'RIGHT'
```

### 2. `any` Type
```typescript
// ❌ Prohibited
function process(data: any) { }

// ✅ Required
function process(data: unknown) {
  if (isValidData(data)) {
    // Type-safe processing
  }
}
```

### 3. Non-null Assertion (`!`)
```typescript
// ❌ Prohibited
const value = optional!.property

// ✅ Required
const value = optional?.property
if (optional) {
  const value = optional.property
}
```

### 4. Hardcoded User-facing Strings
```typescript
// ❌ Prohibited
<button>Start Game</button>

// ✅ Required
<button>{t('game.start')}</button>
```

### 5. Interface in React Components
```typescript
// ❌ Prohibited (in React components)
interface Props {
  value: string
}

// ✅ Required
type Props = {
  value: string
}
```

### 6. External Imports (outside `/src`)
```typescript
// ❌ Prohibited
import { util } from '../../../utils'

// ✅ Required
import { util } from '@/utils'  // Cross-directory
import { util } from './utils'  // Same directory
```

## Required Patterns ✅

### 1. Functional Programming
```typescript
// ✅ Pure functions preferred
export const calculateScore = (params: ScoreParams): number => {
  // Pure function logic
}

// ❌ Classes not allowed
class ScoreCalculator { }
```

### 2. Result<T, E> Pattern (Game Logic)
```typescript
// ✅ Required for game logic
type Result<T, E> = { ok: true; value: T } | { ok: false; error: E }

export const placePiece = (
  board: Board,
  piece: Piece,
  position: Position
): Result<Board, PlacementError> => {
  if (!isValidPosition(board, piece, position)) {
    return { ok: false, error: 'INVALID_POSITION' }
  }
  return { ok: true, value: updatedBoard }
}
```

### 3. Proper Import Conventions
```typescript
// ✅ Cross-directory imports
import { Board } from '@/game/board'
import { Piece } from '@/game/pieces'

// ✅ Same-directory imports
import { helper } from './helper'
import { utils } from './utils'
```

### 4. Co-located Tests
```
src/game/
├── board.ts
├── board.test.ts       # ✅ Co-located
├── pieces.ts
└── pieces.test.ts      # ✅ Co-located
```

### 5. Type-safe i18n
```typescript
// ✅ All UI strings use i18n
import { useTranslation } from 'react-i18next'

const { t } = useTranslation()
return <div>{t('game.title')}</div>
```

### 6. `useId()` for Dynamic IDs
```typescript
// ❌ Static IDs
<label htmlFor="game-input">

// ✅ Dynamic IDs
const id = useId()
<label htmlFor={id}>
```

## Compliance Check Process

### 1. Automated Detection

```bash
# Check for prohibited classes
rg "^class\s+\w+" src/

# Check for enums
rg "^enum\s+\w+" src/

# Check for any types
rg ":\s*any(\s|;|,|\))" src/

# Check for non-null assertions
rg "\!\." src/

# Check for hardcoded strings
rg '"[A-Z][a-zA-Z\s]{3,}"' src/ui/
```

### 2. Manual Review Checklist

- [ ] No classes or enums
- [ ] No `any` types
- [ ] No non-null assertions (`!`)
- [ ] All UI strings use i18n
- [ ] Game logic uses Result<T, E>
- [ ] Imports follow `@/` or `./` conventions
- [ ] Tests are co-located
- [ ] Type aliases instead of interfaces in React

## When This Skill Activates

- "Review this code"
- "Check if this follows the architecture"
- "Is this implementation correct?"
- "Refactor this to match our patterns"
- "Validate this against our rules"
- "Does this comply with our standards?"

## Quick Reference

This document contains all prohibited and required patterns inline above.
See `.claude/rules/` for additional architectural guidelines.
