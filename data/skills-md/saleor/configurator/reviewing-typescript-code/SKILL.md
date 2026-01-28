---
name: reviewing-typescript-code
description: "TypeScript code quality patterns for writing and reviewing code. Covers type safety, clean code, functional patterns, Zod usage, and error handling. Triggers on: add entity, create service, add repository, create comparator, add formatter, deployment stage, GraphQL query, GraphQL mutation, bootstrap method, diff support, command handler, Zod schema, error class, implement feature, add function, refactor code, clean code, functional patterns, map filter reduce, satisfies operator, type guard, code review, PR review, check implementation, audit code, fix types."
allowed-tools: "Read, Grep, Glob"
---

# TypeScript Code Quality Patterns

## Purpose

Guide for writing and reviewing TypeScript code with proper type safety, clean code principles, functional programming patterns, error handling, and project-specific conventions for the Saleor Configurator codebase.

## When to Use

**Configurator-Specific Tasks (Primary Triggers):**
- Adding new entity types (category, product, channel, tax, etc.)
- Creating services (`*Service` classes)
- Adding repository methods (`*Repository` classes)
- Creating comparators for diff engine (`*Comparator` classes)
- Adding formatters for output (`*Formatter` classes)
- Implementing deployment stages
- Writing GraphQL queries/mutations
- Creating Zod schemas for validation
- Adding error classes (`*Error` extends `BaseError`)
- Implementing bootstrap methods (idempotent create/update)
- Adding diff support for entities

**General Writing Tasks:**
- Implementing new features or services
- Adding new functions or methods
- Creating TypeScript classes or modules
- Writing transformation logic
- Refactoring existing code to clean patterns

**Review Tasks:**
- Reviewing code before committing
- Analyzing pull request changes
- Checking implementation quality
- Auditing existing code for improvements

## Table of Contents

- [Quality Checklist](#quality-checklist)
  - [Type Safety Analysis](#1-type-safety-analysis)
  - [Clean Code Principles](#2-clean-code-principles)
  - [Functional Programming Patterns](#3-functional-programming-patterns)
  - [Zod Schema Usage](#4-zod-schema-usage)
  - [Error Handling](#5-error-handling)
  - [Performance Considerations](#6-performance-considerations)
- [Review Output Format](#review-output-format)
- [Project-Specific Conventions](#project-specific-conventions)
- [References](#references)

## Quality Checklist

Use this checklist when **writing new code** to ensure quality from the start, or when **reviewing existing code** to identify improvements.

### 1. Type Safety Analysis

**Critical (Must Fix)**:
- [ ] No `any` types in production code (only allowed in test mocks)
- [ ] No unsafe type assertions (`as unknown as T`)
- [ ] No non-null assertions (`!`) without strong justification
- [ ] Proper type guards for runtime validation

**Best Practices**:
- [ ] Branded types used for domain-specific values (EntitySlug, EntityName)
- [ ] Discriminated unions preferred over inheritance
- [ ] Type inference leveraged where clear
- [ ] Generic constraints properly applied
- [ ] `readonly` used for immutable data
- [ ] `satisfies` operator for type validation with literal preservation

```typescript
// BAD - Avoid these patterns
const result: any = someOperation();
const value = maybeUndefined!;
const data = response as unknown as MyType;

// GOOD - Use these patterns
type EntitySlug = string & { readonly __brand: unique symbol };
const isSlugBasedEntity = (entity: unknown): entity is { slug: string } => { ... };
const ENTITY_TYPES = ['categories', 'products'] as const;

// GOOD - satisfies for type validation while preserving literal types
interface ConfigShape {
  readonly MAX_ITEMS: number;
  readonly TIMEOUT: number;
}
const CONFIG = {
  MAX_ITEMS: 10,
  TIMEOUT: 5000,
} as const satisfies ConfigShape;
// CONFIG.MAX_ITEMS is `10`, not just `number`

// GOOD - Template literal type validation with satisfies
type CliFlag = `--${string}`;
const FLAGS = ["--json", "--verbose"] as const satisfies readonly CliFlag[];
```

### 2. Clean Code Principles

**Function Quality**:
- [ ] Single Responsibility Principle followed
- [ ] Functions are small (< 20 lines ideally)
- [ ] Pure functions where possible (no side effects)
- [ ] Meaningful, declarative names used
- [ ] Arrow functions for consistency

**Naming Conventions**:
- [ ] Functions describe what they do, not how
- [ ] Variables are descriptive and context-specific
- [ ] Boolean names start with `is`, `has`, `should`, `can`
- [ ] Collections use plural names

**DRY (Don't Repeat Yourself)**:
- [ ] Shared utilities extracted to dedicated modules
- [ ] Magic numbers replaced with named constants
- [ ] Repeated logic extracted to helper functions
- [ ] Constants grouped in config objects

**Registry Pattern for Conditionals**:
- [ ] Long if-else chains refactored to registry/strategy pattern
- [ ] Error classification uses matcher registry
- [ ] Type dispatch uses discriminated unions or maps

```typescript
// BAD naming
const data = process(items);
const flag = check(user);

// GOOD naming
const categoriesToProcess = await fetchPendingCategories();
const isEntitySlugUnique = await validateSlugUniqueness(slug);

// BAD - Magic numbers
if (items.length > 10) { truncate(); }
const preview = text.slice(0, 30);

// GOOD - Named constants
const LIMITS = { MAX_ITEMS: 10, MAX_PREVIEW: 30 } as const;
if (items.length > LIMITS.MAX_ITEMS) { truncate(); }
const preview = text.slice(0, LIMITS.MAX_PREVIEW);

// BAD - Long if-else chain
function classify(error: Error): AppError {
  if (error.message.includes("network")) return new NetworkError();
  if (error.message.includes("auth")) return new AuthError();
  if (error.message.includes("validation")) return new ValidationError();
  return new UnexpectedError();
}

// GOOD - Registry pattern
interface ErrorMatcher {
  matches: (msg: string) => boolean;
  create: (error: Error) => AppError;
}
const ERROR_MATCHERS: ErrorMatcher[] = [
  { matches: (m) => m.includes("network"), create: () => new NetworkError() },
  { matches: (m) => m.includes("auth"), create: () => new AuthError() },
];
function classify(error: Error): AppError {
  const matcher = ERROR_MATCHERS.find((m) => m.matches(error.message));
  return matcher?.create(error) ?? new UnexpectedError();
}
```

### 3. Functional Programming Patterns

**Immutability**:
- [ ] No direct mutation of arrays or objects
- [ ] Spread operator or immutable methods used
- [ ] `Map` preferred over object for frequent lookups

**Composition**:
- [ ] Small, composable functions
- [ ] Higher-order functions for reusable logic
- [ ] Pipeline patterns where appropriate

**Imperative to Functional Refactoring**:
- [ ] `for` loops replaced with `map`/`filter`/`reduce`
- [ ] `forEach` with push replaced with spread + `map`
- [ ] Nested loops replaced with `flatMap`
- [ ] Conditional accumulation uses `map` + `filter` with type guards

```typescript
// BAD - Mutation
items.push(newItem);
entity.status = 'active';

// GOOD - Immutable
const updatedItems = [...items, newItem];
const updatedEntity = { ...entity, status: 'active' };

// BAD - Imperative loop with push
const lines: string[] = [];
for (const item of items) {
  lines.push(formatItem(item));
}

// GOOD - Functional map
const lines = items.map(formatItem);

// BAD - forEach with conditional push
const results: Result[] = [];
items.forEach((item) => {
  const match = item.match(regex);
  if (match) {
    results.push({ id: match[1] });
  }
});

// GOOD - map + filter with type guard
const results = items
  .map((item) => {
    const match = item.match(regex);
    return match ? { id: match[1] } : null;
  })
  .filter((r): r is Result => r !== null);

// BAD - Nested forEach
items.forEach((item) => {
  lines.push(`Name: ${item.name}`);
  item.details.forEach((d) => lines.push(`  - ${d}`));
});

// GOOD - flatMap for nested structures
const lines = items.flatMap((item) => [
  `Name: ${item.name}`,
  ...item.details.map((d) => `  - ${d}`),
]);
```

### 4. Zod Schema Usage

**Schema Patterns**:
- [ ] Schemas defined before implementing logic
- [ ] Type inference with `z.infer<>`
- [ ] Reusable schema primitives (EntitySlugSchema, EntityNameSchema)
- [ ] Discriminated unions for variant types
- [ ] Transform and refinement used appropriately

**Validation**:
- [ ] `safeParse` for error handling
- [ ] Detailed error messages with context
- [ ] Schema reuse in tests

```typescript
// GOOD pattern
const CategorySchema = BaseEntitySchema.extend({
  slug: EntitySlugSchema,
  parent: EntitySlugSchema.optional(),
});

type CategoryInput = z.infer<typeof CategorySchema>;
```

### 5. Error Handling

**Error Types**:
- [ ] Specific error types extend `BaseError`
- [ ] GraphQL errors wrapped with `GraphQLError.fromCombinedError()`
- [ ] Zod errors wrapped with `ZodValidationError.fromZodError()`
- [ ] Error messages are actionable

**Error Design**:
- [ ] Error includes relevant context
- [ ] Recovery suggestions provided
- [ ] Error codes for machine processing

```typescript
// GOOD error pattern
class EntityValidationError extends BaseError {
  constructor(message: string, public readonly validationIssues: ValidationIssue[] = []) {
    super(message, 'ENTITY_VALIDATION_ERROR');
  }

  getSuggestions(): string[] {
    return ['Check entity configuration against schema'];
  }
}
```

### 6. Performance Considerations

**Avoid Anti-patterns**:
- [ ] No accumulating spreads in reduce
- [ ] No function creation in loops
- [ ] No unnecessary object creation

**Optimize**:
- [ ] Use `Map` for frequent lookups
- [ ] Lazy evaluation for expensive operations
- [ ] Memoization where appropriate

```typescript
// BAD - Creates new object each iteration
const result = items.reduce((acc, item) => ({ ...acc, [item.id]: item }), {});

// GOOD - Mutates Map directly
const result = items.reduce((acc, item) => acc.set(item.id, item), new Map());
```

## Review Output Format

Structure findings as:

### Critical Issues
Items that must be fixed before merge.

### Important Improvements
Items that should be addressed but aren't blocking.

### Suggestions
Nice-to-have improvements for future consideration.

### Positive Observations
Well-implemented patterns worth highlighting.

## Project-Specific Conventions

- Entity identification: Slug-based (categories, products) vs Name-based (productTypes, pageTypes)
- Service pattern: Constructor DI with validator, repository, logger
- Repository pattern: GraphQL operations encapsulated
- Test pattern: vi.fn() mocks with schema-generated test data

## References

### Skill Reference Files
- **[Anti-Patterns](references/anti-patterns.md)** - Common anti-patterns with corrections
- **[Type Safety Examples](references/type-safety-examples.md)** - Type guards, branded types, discriminated unions

### Project Resources
- See `{baseDir}/docs/CODE_QUALITY.md` for complete coding standards
- See `{baseDir}/docs/ARCHITECTURE.md` for service patterns
- See `{baseDir}/biome.json` for linting rules

## Related Skills

- **Complete entity workflow**: See `adding-entity-types` for architectural patterns
- **Zod standards**: See `designing-zod-schemas` for schema review criteria
- **Pre-commit checks**: See `validating-pre-commit` for quality gate commands

## Quick Reference Rule

For a condensed quick reference, see `.claude/rules/code-quality.md` (automatically loaded when editing `src/**/*.ts` files).
