---
name: typescript
description: Type-safe development patterns for JARVIS AI Assistant
model: sonnet
risk_level: MEDIUM
version: 1.0.0
---

# TypeScript Development Skill

> **File Organization**: This skill uses split structure. See `references/` for advanced patterns and security examples.

## 1. Overview

This skill provides TypeScript expertise for the JARVIS AI Assistant, ensuring type safety across the entire codebase including Vue components, API routes, 3D rendering, and state management.

**Risk Level**: MEDIUM - Type system prevents runtime errors, enforces contracts, but misconfiguration can lead to security gaps

**Primary Use Cases**:
- Defining type-safe interfaces for JARVIS system data
- Runtime validation with Zod schemas
- Generic patterns for reusable HUD components
- Strict null checking to prevent crashes

## 2. Core Responsibilities

### 2.1 Fundamental Principles

1. **TDD First**: Write tests before implementation - red, green, refactor
2. **Performance Aware**: Apply memoization, lazy loading, and efficient patterns
3. **Strict Mode Always**: Enable all strict compiler options - no shortcuts
4. **Explicit Types at Boundaries**: Always type function parameters and return values at module boundaries
5. **Runtime Validation**: TypeScript types disappear at runtime - use Zod for external data
6. **No Any Escape Hatch**: Use `unknown` instead of `any`, then narrow with type guards
7. **Immutable by Default**: Prefer `readonly` and `as const` for data integrity
8. **Discriminated Unions**: Use tagged unions for state machines and error handling
9. **Branded Types**: Create nominal types for IDs and sensitive values

## 3. Technology Stack & Versions

### 3.1 Recommended Versions

| Package | Version | Security Notes |
|---------|---------|----------------|
| typescript | ^5.3.0 | Latest stable with improved type inference |
| zod | ^3.22.0 | Runtime validation, schema-first |
| @types/node | ^20.0.0 | Match Node.js version |

### 3.2 Compiler Configuration

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true,
    "noPropertyAccessFromIndexSignature": true,
    "forceConsistentCasingInFileNames": true,
    "verbatimModuleSyntax": true,
    "moduleResolution": "bundler",
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"]
  }
}
```

## 4. Implementation Patterns

### 4.1 Branded Types for Security

```typescript
// types/branded.ts
declare const __brand: unique symbol

type Brand<T, B> = T & { [__brand]: B }

// ✅ Prevent accidental mixing of IDs
export type UserId = Brand<string, 'UserId'>
export type SessionId = Brand<string, 'SessionId'>
export type CommandId = Brand<string, 'CommandId'>

// Factory functions with validation
export function createUserId(id: string): UserId {
  if (!/^usr_[a-zA-Z0-9]{16}$/.test(id)) {
    throw new Error('Invalid user ID format')
  }
  return id as UserId
}

// ✅ Type system prevents mixing IDs
function getUser(id: UserId): User { /* ... */ }
function getSession(id: SessionId): Session { /* ... */ }

// This won't compile:
// getUser(sessionId) // Error: SessionId not assignable to UserId
```

### 4.2 Discriminated Unions for State

```typescript
// types/jarvis-state.ts

// ✅ Type-safe state machine
type JARVISState =
  | { status: 'idle' }
  | { status: 'listening'; startTime: number }
  | { status: 'processing'; commandId: CommandId }
  | { status: 'responding'; response: string; confidence: number }
  | { status: 'error'; error: JARVISError; retryCount: number }

// ✅ Exhaustive handling
function handleState(state: JARVISState): string {
  switch (state.status) {
    case 'idle':
      return 'Ready'
    case 'listening':
      return `Listening for ${Date.now() - state.startTime}ms`
    case 'processing':
      return `Processing ${state.commandId}`
    case 'responding':
      return `${state.response} (${state.confidence}%)`
    case 'error':
      return `Error: ${state.error.message}`
    default:
      // ✅ Compile-time exhaustiveness check
      const _exhaustive: never = state
      return _exhaustive
  }
}
```

### 4.3 Runtime Validation with Zod

```typescript
// schemas/command.ts
import { z } from 'zod'

// ✅ Schema-first approach
export const commandSchema = z.object({
  id: z.string().regex(/^cmd_[a-zA-Z0-9]{16}$/),
  action: z.enum(['navigate', 'control', 'query', 'configure']),
  target: z.string().min(1).max(100),
  parameters: z.record(z.unknown()).optional(),
  timestamp: z.number().int().positive(),
  priority: z.number().min(0).max(10).default(5)
})

// ✅ Infer TypeScript type from schema
export type Command = z.infer<typeof commandSchema>

// ✅ Parse with full validation
export function parseCommand(data: unknown): Command {
  return commandSchema.parse(data)
}

// ✅ Safe parse for error handling
export function tryParseCommand(data: unknown): Command | null {
  const result = commandSchema.safeParse(data)
  return result.success ? result.data : null
}
```

### 4.4 Generic Patterns for HUD Components

```typescript
// ✅ Generic with constraints - ensures type safety for metrics
interface MetricConfig<T extends Record<string, number>> {
  metrics: T
  thresholds: { [K in keyof T]: { warning: number; critical: number } }
}

type SystemMetrics = { cpu: number; memory: number }
const config: MetricConfig<SystemMetrics> = {
  metrics: { cpu: 45, memory: 72 },
  thresholds: {
    cpu: { warning: 70, critical: 90 },
    memory: { warning: 80, critical: 95 }
  }
}
```

### 4.5 Type Guards for Narrowing

```typescript
// ✅ Type predicate for safe narrowing
function isSuccessResponse<T>(
  response: APIResponse<T>
): response is APIResponse<T> & { success: true; data: T } {
  return response.success && response.data !== undefined
}

// Usage - type automatically narrowed
if (isSuccessResponse(response)) {
  return response.data // ✅ Type is T, not T | undefined
}
```

### 4.6 Utility Types for JARVIS

```typescript
// types/utilities.ts

// ✅ Deep readonly for immutable state
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K]
}

// ✅ Make specific keys required
type RequireKeys<T, K extends keyof T> = T & Required<Pick<T, K>>

// ✅ Extract event payloads
type EventPayload<T> = T extends { payload: infer P } ? P : never

// ✅ Async function return type
type AsyncReturnType<T extends (...args: any[]) => Promise<any>> =
  T extends (...args: any[]) => Promise<infer R> ? R : never
```

## 5. Implementation Workflow (TDD)

### Step 1: Write Failing Test First

```typescript
// tests/utils/command-parser.test.ts
import { describe, it, expect } from 'vitest'
import { parseCommand } from '@/utils/command-parser'

describe('parseCommand', () => {
  it('should parse valid command', () => {
    expect(parseCommand('open settings')).toEqual({
      action: 'open', target: 'settings', parameters: {}
    })
  })

  it('should extract parameters', () => {
    expect(parseCommand('set volume to 80')).toEqual({
      action: 'set', target: 'volume', parameters: { value: 80 }
    })
  })

  it('should throw on empty command', () => {
    expect(() => parseCommand('')).toThrow('Command cannot be empty')
  })
})
```

### Step 2: Implement Minimum to Pass

Write only code needed to make tests green.

### Step 3: Refactor if Needed

Improve code quality while keeping tests green.

### Step 4: Run Full Verification

```bash
npx vitest run              # Unit tests
npx eslint . --ext .ts,.tsx # Linting
npx tsc --noEmit            # Type checking
```

## 6. Performance Patterns

### 6.1 Memoization

```typescript
// ❌ BAD - Recalculates on every render
const processed = data.map(item => heavyTransform(item))

// ✅ GOOD - Memoized computation
import { computed } from 'vue'
const processed = computed(() => data.value.map(item => heavyTransform(item)))
```

### 6.2 Lazy Loading

```typescript
// ❌ BAD - Loads everything upfront
import { HeavyChart } from '@/components/HeavyChart'

// ✅ GOOD - Lazy load heavy components
import { defineAsyncComponent } from 'vue'
const HeavyChart = defineAsyncComponent(() => import('@/components/HeavyChart'))
```

### 6.3 Debounce/Throttle

```typescript
// ❌ BAD - API call on every keystroke
const handleSearch = (q: string) => fetchResults(q)

// ✅ GOOD - Debounced search (300ms delay)
import { useDebounceFn } from '@vueuse/core'
const debouncedSearch = useDebounceFn((q: string) => fetchResults(q), 300)
```

### 6.4 Efficient Data Structures

```typescript
// ❌ BAD - O(n) lookup
const user = users.find(u => u.id === id)

// ✅ GOOD - O(1) lookup with Map
const userMap = new Map(users.map(u => [u.id, u]))
const user = userMap.get(id)

// ✅ GOOD - O(1) membership check with Set
const allowed = new Set(['read', 'write'])
const hasAccess = allowed.has(permission)
```

### 6.5 Parallel Async Operations

```typescript
// ❌ BAD - Sequential (total = sum of times)
const user = await fetchUser()
const metrics = await fetchMetrics()

// ✅ GOOD - Parallel (total = max of times)
const [user, metrics] = await Promise.all([fetchUser(), fetchMetrics()])

// ✅ GOOD - With error handling
const results = await Promise.allSettled([fetchUser(), fetchMetrics()])
```

## 7. Security Standards

### 7.1 Known Vulnerabilities

TypeScript itself has a strong security record. Main risks come from:

| Risk Area | Description | Mitigation |
|-----------|-------------|------------|
| Type Erasure | Types don't exist at runtime | Use Zod for external data validation |
| Any Type | Disables type checking | Enable noImplicitAny, use unknown |
| Type Assertions | Can bypass type system | Avoid `as`, use type guards instead |

### 7.2 OWASP Top 10 Coverage

| OWASP Category | TypeScript Mitigation |
|----------------|----------------------|
| A03 Injection | Typed APIs prevent string interpolation in queries |
| A04 Insecure Design | Strong typing enforces secure interfaces |
| A08 Software Integrity | Compile-time checks catch errors before deployment |

### 7.3 Secure Type Patterns

```typescript
// ❌ DANGEROUS - Type assertion bypasses safety
const userData = apiResponse as User

// ✅ SECURE - Runtime validation
const userData = userSchema.parse(apiResponse)

// ❌ DANGEROUS - any disables all checks
function process(data: any) { /* ... */ }

// ✅ SECURE - unknown requires narrowing
function process(data: unknown) {
  const validated = commandSchema.parse(data)
  // Now safely typed
}
```

## 8. Testing & Quality

```typescript
// Type testing with vitest
import { expectTypeOf } from 'vitest'

describe('Type Safety', () => {
  it('should enforce branded types', () => {
    expectTypeOf(createUserId('usr_1234567890123456')).toEqualTypeOf<UserId>()
  })
})

// Schema validation tests
describe('Command Schema', () => {
  it('should reject invalid IDs', () => {
    expect(() => commandSchema.parse({ id: 'invalid' })).toThrow()
  })

  it('should accept valid commands', () => {
    const result = commandSchema.parse({ id: 'cmd_1234567890123456', action: 'query' })
    expect(result.action).toBe('query')
  })
})
```

## 9. Common Mistakes & Anti-Patterns

### 9.1 Critical Security Anti-Patterns

#### Never: Use Type Assertions for External Data

```typescript
// ❌ DANGEROUS - No runtime validation
const user = JSON.parse(data) as User

// ✅ SECURE - Validate at runtime
const user = userSchema.parse(JSON.parse(data))
```

#### Never: Ignore Null/Undefined Checks

```typescript
// ❌ DANGEROUS - Runtime crash if undefined
function getConfig(key: string) {
  return config[key].value  // May be undefined!
}

// ✅ SECURE - Explicit null handling
function getConfig(key: string): string | undefined {
  return config[key]?.value
}
```

#### Never: Use Index Signatures Without Checks

```typescript
// ❌ DANGEROUS - No type safety
const handlers: Record<string, Handler> = {}
handlers['cmd'].execute()  // May be undefined!

// ✅ SECURE - Explicit lookup with check
const handler = handlers['cmd']
if (handler) {
  handler.execute()
}
```

### 9.2 Performance Anti-Patterns

#### Avoid: Excessive Type Complexity

```typescript
// ❌ BAD - Unreadable, slow compilation
type DeepPartialRecord<T> = T extends object
  ? { [K in keyof T]?: DeepPartialRecord<T[K]> }
  : T extends Array<infer U>
  ? Array<DeepPartialRecord<U>>
  : T

// ✅ GOOD - Simple, clear types
interface PartialConfig {
  theme?: Partial<ThemeConfig>
  metrics?: Partial<MetricsConfig>
}
```

## 10. Pre-Deployment Checklist

### Phase 1: Before Writing Code

- [ ] Write failing tests first (TDD)
- [ ] Define types and interfaces for new features
- [ ] Plan Zod schemas for external data
- [ ] Identify performance-critical paths
- [ ] Review existing patterns in codebase

### Phase 2: During Implementation

- [ ] `strict: true` enabled in tsconfig
- [ ] `noUncheckedIndexedAccess: true` enabled
- [ ] `noImplicitAny: true` enabled
- [ ] No `any` types in production code
- [ ] All external data validated with Zod
- [ ] Branded types for sensitive IDs
- [ ] Discriminated unions for state machines
- [ ] Memoization applied to expensive computations
- [ ] Lazy loading for heavy components
- [ ] Efficient data structures (Map/Set) for lookups

### Phase 3: Before Committing

- [ ] All tests pass (`npx vitest run`)
- [ ] No linting errors (`npx eslint .`)
- [ ] No TypeScript errors (`npx tsc --noEmit`)
- [ ] All API inputs validated at runtime
- [ ] No type assertions on external data
- [ ] Performance patterns applied where needed

## 11. Summary

TypeScript provides compile-time safety for JARVIS development:

1. **Strict Configuration**: Enable all strict options for maximum safety
2. **Runtime Validation**: Types disappear at runtime - use Zod
3. **Branded Types**: Prevent mixing of IDs and sensitive values
4. **Type Guards**: Safely narrow `unknown` data with predicates

**Remember**: TypeScript only checks at compile time. Every boundary with external data must have runtime validation.

---

**References**:
- `references/advanced-patterns.md` - Complex type patterns
- `references/security-examples.md` - Secure typing practices
