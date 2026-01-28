---
name: designing-zod-schemas
description: "Designs Zod schemas following Zod-first development. Creates validation schemas, branded types, discriminated unions, and transforms. Infers TypeScript types from schemas. Triggers on: Zod schema, z.object, z.infer, validation, branded types, discriminated union, safeParse, refinement."
allowed-tools: "Read, Grep, Glob, Write, Edit"
---

# Zod Schema Designer

## Purpose

Guide the design and implementation of Zod schemas following the project's Zod-first development approach, where schemas are defined before implementing business logic.

## When to Use

- Creating new data structures
- Adding validation to inputs
- Designing configuration schemas
- Implementing type-safe transformations
- Creating test data builders

## Table of Contents

- [Core Principles](#core-principles)
- [Quick Reference](#quick-reference)
- [Schema Patterns](#schema-patterns)
- [Project Schema Location](#project-schema-location)
- [References](#references)

## Core Principles

### Zod-First Development

1. **Define Schema First**: Schema is the source of truth
2. **Infer Types**: Use `z.infer<>` instead of manual type definitions
3. **Share Validation**: Same schema for runtime validation and tests
4. **Compose Schemas**: Build complex schemas from primitives

### Decision Guide

| Need | Pattern | Example |
|------|---------|---------|
| Basic validation | Primitives | `z.string().min(1)` |
| Domain safety | Branded types | `transform((v) => v as EntitySlug)` |
| Multiple types | Discriminated union | `z.discriminatedUnion('type', [...])` |
| Cross-field rules | Refinement | `.refine((data) => ...)` |
| Data normalization | Transform | `.transform((v) => v.trim())` |
| Partial updates | Partial schema | `Schema.partial()` |

## Quick Reference

### Common Schema Shapes

```typescript
import { z } from 'zod';

// String with constraints
const NameSchema = z.string().min(1).max(100).trim();

// Slug pattern
const SlugSchema = z.string().regex(/^[a-z0-9-]+$/);

// Number with range
const PriceSchema = z.number().min(0).multipleOf(0.01);

// Object schema
const EntitySchema = z.object({
  name: z.string().min(1),
  slug: z.string().regex(/^[a-z0-9-]+$/),
  description: z.string().optional(),
});

// Array with validation
const TagsSchema = z.array(z.string()).min(1).max(10);

// Type inference
type Entity = z.infer<typeof EntitySchema>;
```

### Safe Parsing

```typescript
const result = schema.safeParse(data);

if (!result.success) {
  // Handle errors
  console.error(result.error.issues);
} else {
  // Use validated data
  const validData = result.data;
}
```

## Schema Patterns

For detailed patterns and examples, see:

- **[Primitive Patterns](references/primitive-patterns.md)**: Strings, numbers, enums, branded types
- **[Object Patterns](references/object-patterns.md)**: Objects, discriminated unions, arrays, transforms, refinements
- **[Testing Patterns](references/testing-patterns.md)**: Test data builders, schema validation tests

## Project Schema Location

```
src/modules/config/schema/
├── schema.ts           # Main configuration schema
├── primitives.ts       # Reusable primitive schemas
├── entities/           # Entity-specific schemas
│   ├── category.ts
│   ├── product.ts
│   └── ...
└── index.ts            # Schema exports
```

## Validation Checkpoints

| Phase | Validate | Command |
|-------|----------|---------|
| Schema defined | No TS errors | `npx tsc --noEmit` |
| Types inferred | `z.infer` works | Check type in IDE |
| Validation works | `safeParse` tests | `pnpm test` |

## Common Mistakes

| Mistake | Issue | Fix |
|---------|-------|-----|
| Manual type definitions | Type drift | Use `z.infer<typeof Schema>` |
| Using `.parse()` directly | Throws on invalid | Use `.safeParse()` for error handling |
| Missing `.optional()` | Runtime errors | Mark optional fields explicitly |
| Complex refinements | Hard to debug | Break into smaller schemas |
| Not using branded types | Type confusion | Use `.brand()` or transform for domain safety |

## External Documentation

For up-to-date Zod patterns, use Context7 MCP:
```
mcp__context7__get-library-docs with context7CompatibleLibraryID: "/colinhacks/zod"
```

## References

- `{baseDir}/src/modules/config/schema/schema.ts` - Main schema definitions
- `{baseDir}/docs/CODE_QUALITY.md#zod-first-development` - Quality standards
- Zod documentation: https://zod.dev

## Related Skills

- **Complete entity workflow**: See `adding-entity-types` for full schema-to-service implementation
- **Testing schemas**: See `analyzing-test-coverage` for test data builders
- **GraphQL type mapping**: See `writing-graphql-operations` for schema-to-GraphQL patterns

## Quick Reference Rule

For a condensed quick reference, see `.claude/rules/config-schema.md` (automatically loaded when editing `src/modules/config/**/*.ts` files).
