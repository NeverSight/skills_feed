---
name: typebox-schemas
description: Guide for TypeBox schema conventions in Fastify routes and environment validation. Use when defining request/response schemas or validating configuration.
---

# TypeBox Schema Conventions

This skill provides patterns for using TypeBox schemas in this repository.

## Route Schemas (Fastify Context)

Use `FastifyPluginAsyncTypebox` for route plugins to get automatic TypeBox type inference:

```typescript
import { type FastifyPluginAsyncTypebox, Type } from "@fastify/type-provider-typebox";

const routes: FastifyPluginAsyncTypebox = async (fastify) => {
  fastify.get(
    "/endpoint",
    {
      schema: {
        description: "Endpoint description",
        tags: ["tag-name"],
        summary: "Short summary",
        querystring: Type.Object({
          page: Type.Number({ minimum: 1, default: 1 }),
          limit: Type.Number({ minimum: 1, maximum: 100, default: 10 }),
        }),
        params: Type.Object({
          id: Type.String({ format: "uuid" }),
        }),
        body: Type.Object({
          name: Type.String({ minLength: 1, maxLength: 255 }),
          email: Type.String({ format: "email" }),
        }),
        response: {
          200: Type.Object({
            status: Type.Literal("ok"),
            data: Type.Array(Type.Object({
              id: Type.String(),
              name: Type.String(),
            })),
          }),
          400: Type.Object({
            message: Type.String(),
          }),
          404: Type.Object({
            message: Type.String(),
          }),
        },
      },
    },
    async (request, reply) => {
      return { status: "ok", data: [] };
    },
  );
};

export default routes;
```

## Environment Validation (Pre-Fastify)

Use TypeBox standalone for environment validation before Fastify instance creation:

```typescript
import Type from "typebox";
import Value from "typebox/value";

const EnvSchema = Type.Object({
  NODE_ENV: Type.Union(
    [
      Type.Literal("development"),
      Type.Literal("production"),
      Type.Literal("test"),
    ],
    { default: "development" },
  ),
  PORT: Type.Number({ default: 3000 }),
  HOST: Type.String({ default: "0.0.0.0" }),
  LOG_LEVEL: Type.Union(
    [
      Type.Literal("trace"),
      Type.Literal("debug"),
      Type.Literal("info"),
      Type.Literal("warn"),
      Type.Literal("error"),
      Type.Literal("fatal"),
    ],
    { default: "info" },
  ),
});

export const env = Value.Parse(EnvSchema, {
  NODE_ENV: process.env.NODE_ENV ?? "development",
  PORT: process.env.PORT ? Number(process.env.PORT) : undefined,
  HOST: process.env.HOST,
  LOG_LEVEL: process.env.LOG_LEVEL,
});
```

## Import Conventions

```typescript
// Route plugins - use FastifyPluginAsyncTypebox for automatic type inference
import { type FastifyPluginAsyncTypebox, Type } from "@fastify/type-provider-typebox";

// Environment validation - use standalone typebox package
import Type from "typebox";
import Value from "typebox/value";

// Do not use the direct @sinclair/typebox import
// import { Type } from "@sinclair/typebox";  // Do not use
```

## Common Type Patterns

### String Types

```typescript
Type.String()                           // Any string
Type.String({ minLength: 1 })          // Non-empty string
Type.String({ format: "email" })       // Email format
Type.String({ format: "uuid" })        // UUID format
Type.String({ pattern: "^[a-z]+$" })   // Regex pattern
Type.Literal("value")                  // Exact string value
```

### Number Types

```typescript
Type.Number()                          // Any number
Type.Number({ minimum: 0 })            // Non-negative
Type.Number({ minimum: 1, maximum: 100 }) // Range
Type.Integer()                         // Integer only
```

### Object Types

```typescript
Type.Object({
  required: Type.String(),
  optional: Type.Optional(Type.String()),
})
```

### Array Types

```typescript
Type.Array(Type.String())              // Array of strings
Type.Array(Type.Object({ id: Type.String() })) // Array of objects
Type.Array(Type.String(), { minItems: 1 })     // Non-empty array
```

### Union Types

```typescript
Type.Union([
  Type.Literal("option1"),
  Type.Literal("option2"),
  Type.Literal("option3"),
])
```

### With Defaults

```typescript
Type.String({ default: "default-value" })
Type.Number({ default: 10 })
Type.Boolean({ default: false })
```

## OpenAPI Integration

TypeBox schemas automatically generate OpenAPI documentation. Include:

- `description` on schema properties for documentation
- Appropriate format hints (email, uuid, date-time)
- Valid default values
- Proper constraints (minLength, maximum, etc.)

```typescript
Type.Object({
  email: Type.String({
    format: "email",
    description: "User email address",
  }),
  createdAt: Type.String({
    format: "date-time",
    description: "ISO 8601 timestamp",
  }),
})
```

## Testing TypeBox Schemas

Verify response shapes match schemas in tests:

```typescript
it("should return response matching schema", async () => {
  const response = await fastify.inject({
    method: "GET",
    url: "/endpoint",
  });

  expect(response.statusCode).toBe(200);
  const body = response.json();

  // Verify structure matches schema
  expect(body).toHaveProperty("status", "ok");
  expect(body).toHaveProperty("data");
  expect(Array.isArray(body.data)).toBe(true);
});
```

## Commands

```bash
cd app
npm run build       # TypeScript will validate schema types
npm run check       # Run Biome linter
npm run test        # Run tests
```

## Boundaries

- Always use TypeBox for route schemas (not plain JSON Schema)
- Use the correct import for context (Fastify vs standalone)
- Do not use `@sinclair/typebox` directly
