---
name: fastify-routes
description: Guide for creating Fastify route handlers with TypeBox schemas and OpenAPI documentation. Use when adding new routes to app/src/routes/.
---

# Fastify Route Development

This skill provides patterns for creating Fastify routes with TypeBox validation and OpenAPI documentation.

## Directory Structure

Routes are located in `app/src/routes/`. Each route file exports a default async function that registers routes on a Fastify instance.

## Route Template

```typescript
import { type FastifyPluginAsyncTypebox, Type } from "@fastify/type-provider-typebox";
import { ErrorModelSchema } from "../schemas/index.js";

const routes: FastifyPluginAsyncTypebox = async (fastify) => {
  fastify.get(
    "/endpoint",
    {
      schema: {
        description: "Endpoint description for OpenAPI docs",
        tags: ["tag-name"],
        summary: "Short summary",
        querystring: Type.Object({
          param: Type.String({ description: "Query parameter" }),
        }),
        response: {
          200: Type.Object({
            status: Type.Literal("ok"),
            data: Type.String({ description: "Response data" }),
          }),
          422: ErrorModelSchema,
          500: ErrorModelSchema,
        },
      },
    },
    async (request, reply) => {
      const { param } = request.query;
      return { status: "ok", data: param };
    },
  );
};

export default routes;
```

## OpenAPI Schema Requirements

1. **Always include schema**: Every route handler must have a schema property
2. **Description and summary**: Required for OpenAPI documentation
3. **Tags**: Group related endpoints
4. **Response codes**: Document all possible response status codes
5. **Error responses**: Use `ErrorModelSchema` from `schemas/index.js` for error status codes (400, 404, 422, 500, 503)
6. **TypeBox types**: Use `Type` from `@fastify/type-provider-typebox`
7. **Schema discoverability**: Only schemas referenced in route definitions appear in OpenAPI `components.schemas`

## Authentication

For protected routes, use the `fastify.authenticate` preHandler:

```typescript
import { ErrorModelSchema } from "../schemas/index.js";

fastify.get(
  "/protected",
  {
    preHandler: [fastify.authenticate],
    schema: {
      description: "Protected endpoint requiring authentication",
      tags: ["protected"],
      response: {
        200: Type.Object({ userId: Type.String() }),
        401: ErrorModelSchema,
        500: ErrorModelSchema,
      },
    },
  },
  async (request) => {
    return { userId: request.user.uid };
  },
);
```

## HTTP Methods

Use appropriate HTTP methods:
- `GET` - Read operations
- `POST` - Create operations
- `PUT` - Full update operations
- `PATCH` - Partial update operations
- `DELETE` - Delete operations

## Error Handling

Use `@fastify/sensible` HTTP error helpers:

```typescript
// Throw errors
throw fastify.httpErrors.notFound("Resource not found");
throw fastify.httpErrors.badRequest("Invalid input");

// Reply methods
reply.notFound("Resource not found");
reply.badRequest("Invalid input");
```

## Existing Routes

- `routes/health.ts` - Simple liveness probe at `/health` (returns `{ status: "healthy" }`)
- `routes/schemas.ts` - Schema discovery at `/schemas/:schemaId`
- `routes/v1.ts` - V1 API router that registers versioned modules under `/v1`
- `modules/hello/routes.ts` - Greeting endpoint at `/v1/hello` (GET and POST)
- `modules/items/routes.ts` - Items collection at `/v1/items` with cursor-based pagination and category filtering

## Testing Requirements

Each route must have a corresponding test file in `app/tests/unit/`. Routes in `src/routes/` have tests in `tests/unit/routes/`, and module routes in `src/modules/` have tests in `tests/unit/modules/`.

## Commands

```bash
cd app
npm run build       # Build and verify TypeScript compilation
npm run check       # Run Biome linter and formatter
npm run test        # Run all tests
```

## Boundaries

- Do not create routes without TypeBox schemas
- Do not skip OpenAPI documentation (description, tags, summary)
- Always add corresponding unit tests for new routes
