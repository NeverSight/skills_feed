---
name: dayuse-vibes
description: Use this skill when generating code, creating features, writing TypeScript, building components, implementing functionality, or helping with any coding task. Enforces professional standards for non-developers doing "vibe coding" - ensures DDD architecture, strict TypeScript (no any), systematic testing, linting, Zod validation, and Result pattern for errors.
---

# Dayuse Vibe Coding Standards

This skill ensures that code generated for non-developers meets professional standards while remaining understandable.

## Core Principles

When generating code, you MUST follow these rules:

1. **TypeScript only** - All code must use strict TypeScript
2. **No `any` type** - The `any` type is strictly forbidden
3. **DDD Architecture** - Organize code according to Domain-Driven Design
4. **Systematic testing** - Every feature requires tests
5. **Mandatory linting** - Code must pass ESLint and Prettier
6. **Zod validation** - Validate external inputs with Zod
7. **Result Pattern** - Use Result<T, E> instead of throw/catch
8. **Security by default** - Security audit, authorization checks, and no hardcoded secrets

---

## DDD Architecture

Organize code into 4 distinct layers:

```
src/
├── domain/           # Business logic (THE WHAT)
│   ├── entities/     # Business objects with identity
│   ├── value-objects/# Immutable objects without identity
│   ├── repositories/ # Data access interfaces
│   └── services/     # Complex business operations
│
├── application/      # Use Cases (THE HOW)
│   ├── use-cases/    # Unit business operations
│   └── dtos/         # Data Transfer Objects
│
├── infrastructure/   # Technical details (THE WHERE)
│   ├── repositories/ # DB/API implementations
│   ├── services/     # External services
│   └── persistence/  # DB configuration
│
└── interfaces/       # Entry points (THE WHO)
    ├── http/         # REST controllers
    ├── cli/          # CLI commands
    └── events/       # Event handlers
```

### Layer Rules

| Layer | Depends on | Contains |
|-------|------------|----------|
| Domain | Nothing | Entities, Value Objects, Repository Interfaces |
| Application | Domain | Use Cases, DTOs |
| Infrastructure | Domain | Repository Implementations, External services |
| Interfaces | Application | Controllers, CLI, Event Handlers |

---

## Strict TypeScript

### Required Configuration

All projects must have the following in `tsconfig.json`:

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noImplicitReturns": true,
    "noUncheckedIndexedAccess": true
  }
}
```

### Alternatives to the `any` Type

| Instead of `any` | Use | When |
|-------------------|-----|------|
| `any` | `unknown` | Truly unknown type (requires Type Guard) |
| `any[]` | `T[]` | Typed arrays |
| `any` | Specific interface | Known structure |
| `any` | Union types | Multiple possible types |
| `any` | Generic `<T>` | Reusable components |
| `any` | `Record<string, unknown>` | Object dictionaries |

### Type Guard Pattern

```typescript
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'name' in value
  );
}
```

---

## Validation with Zod

Use Zod to validate ALL external inputs:

```typescript
import { z } from 'zod';

// Define the schema
const CreateUserSchema = z.object({
  name: z.string().min(2).max(100),
  email: z.string().email(),
  age: z.number().int().positive().optional(),
});

// Infer the TypeScript type
type CreateUserInput = z.infer<typeof CreateUserSchema>;

// Validate data
function validateInput(data: unknown): Result<CreateUserInput, ValidationError> {
  const result = CreateUserSchema.safeParse(data);
  if (!result.success) {
    return err(new ValidationError(result.error.issues));
  }
  return ok(result.data);
}
```

---

## Result Pattern

Never use throw/catch for business errors. Use the Result Pattern instead:

```typescript
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

// Helpers
const ok = <T>(data: T): Result<T, never> => ({ success: true, data });
const err = <E>(error: E): Result<never, E> => ({ success: false, error });

// Usage
function createUser(input: CreateUserInput): Result<User, UserError> {
  if (await userExists(input.email)) {
    return err(new EmailAlreadyExistsError(input.email));
  }
  const user = new User(generateId(), input.name, input.email);
  return ok(user);
}

// Consumption
const result = createUser(input);
if (!result.success) {
  // Handle the error
  return handleError(result.error);
}
// Use result.data
```


---

## Security and Authorization (Zero Trust)

The AI must adopt a **Zero Trust** approach: never trust inputs or implicit state.

### 1. Systematic Authorization Checks

Every business action must verify **WHO** is performing it and whether they have the **RIGHT** to do so.

```typescript
// ❌ BAD: Assumes the user has permission because they are authenticated
function deleteProject(projectId: string, user: User) {
  return projectRepo.delete(projectId);
}

// ✅ GOOD: Explicit permission check (Business Logic)
function deleteProject(projectId: string, user: User): Result<void, AppError> {
  const project = await projectRepo.findById(projectId);

  // Ownership or role check
  if (project.ownerId !== user.id && user.role !== 'ADMIN') {
    return err(new UnauthorizedError("You do not have permission to delete this project"));
  }

  return projectRepo.delete(projectId);
}
```

### 2. No Hardcoded Secrets

NEVER write API keys, tokens, passwords, or certificates directly in code.

```typescript
// ❌ FORBIDDEN
const API_KEY = "sk-1234567890abcdef";

// ✅ REQUIRED
const API_KEY = process.env.OPENAI_API_KEY;
```

### 3. Input Sanitization

Never insert raw user data into:
- HTML (XSS risk)
- SQL queries (SQL Injection risk)
- System commands (Command Injection risk)

Use Zod to validate the format and escaping libraries for display.

---

## Testing with Vitest

### Test Location

Place tests alongside source files:

```
src/domain/entities/
├── user.ts
└── user.test.ts
```

### Test Structure

```typescript
import { describe, it, expect, beforeEach } from 'vitest';

describe('User', () => {
  describe('changeName', () => {
    it('should update name when valid', () => {
      // Arrange
      const user = new User('1', 'John', email);

      // Act
      user.changeName('Jane');

      // Assert
      expect(user.name).toBe('Jane');
    });

    it('should return error when name too short', () => {
      const user = new User('1', 'John', email);
      const result = user.changeName('J');
      expect(result.success).toBe(false);
    });
  });
});
```

### Tests Required For

- All domain Entities and Value Objects
- All application Use Cases
- All public functions
- Edge cases and error handling

---

## Linting

### Commands to Run

Before completing ANY code task:

```bash
npm run lint        # Check for issues
npm run lint:fix    # Auto-fix issues
npm run format      # Format with Prettier
npm run test        # Run tests
```

### Full Verification Script

```bash
npm run lint:fix && npm run format && npm run test
```

---

## Code Generation Workflow

For each new feature:

### 1. Determine the Layer
- Pure business logic? -> `domain/`
- Operation orchestration? -> `application/`
- External integration? -> `infrastructure/`
- Entry point? -> `interfaces/`

### 2. Create with Proper Types
- Define interfaces first
- Use explicit types everywhere
- Never use `any`
- Validate inputs with Zod

### 3. Handle Errors with Result
- Define specific error types
- Return Result instead of throw
- Document error cases

### 4. Write Tests
- Create the test file alongside the source
- Test the happy path
- Test error cases

### 5. Verify Quality
```bash
npm run lint:fix && npm run format && npm run test
```

---

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Files | kebab-case | `user-repository.ts` |
| Classes | PascalCase | `UserRepository` |
| Interfaces | PascalCase | `UserRepository` |
| Functions | camelCase | `createUser` |
| Constants | SCREAMING_SNAKE | `MAX_RETRY_COUNT` |
| Types | PascalCase | `CreateUserDTO` |
| Zod Schemas | PascalCase + Schema | `CreateUserSchema` |

---

## Additional Resources

For detailed guides, refer to:

- **[references/ddd-architecture.md](references/ddd-architecture.md)** - Complete DDD Patterns
- **[references/typescript-patterns.md](references/typescript-patterns.md)** - Alternatives to the any type
- **[references/testing-guide.md](references/testing-guide.md)** - Complete Vitest Guide
- **[references/linting-setup.md](references/linting-setup.md)** - ESLint/Prettier Configuration
- **[references/zod-validation.md](references/zod-validation.md)** - Validation with Zod
- **[references/result-pattern.md](references/result-pattern.md)** - Detailed Result Pattern

---

## Quick Reference

```
ALWAYS:
✓ Strict TypeScript
✓ Explicit types everywhere
✓ Tests for all code
✓ Linter before finishing
✓ DDD structure
✓ Zod for external inputs
✓ Result for business errors
✓ Permission checks

NEVER:
✗ any type
✗ Skip tests
✗ Ignore linter errors
✗ Infrastructure logic in domain
✗ throw/catch for business errors
✗ Unvalidated data
✗ Hardcoded secrets/API keys
```
