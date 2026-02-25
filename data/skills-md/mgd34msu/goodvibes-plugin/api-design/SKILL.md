---
name: api-design
description: "Load PROACTIVELY when task involves building or modifying API endpoints. Use when user says \"build an API\", \"add an endpoint\", \"create a REST route\", \"set up GraphQL\", or \"add tRPC procedures\". Covers route design and file organization, request validation with Zod, response formatting, error handling patterns, middleware composition, authentication guards, rate limiting, pagination, and API documentation generation."
metadata:
  version: 1.0.0
  category: outcome
  tags: [api, rest, graphql, trpc, endpoint, route, middleware, validation]
---

## Resources
```
scripts/
  api-checklist.sh
references/
  api-style-guide.md
```

# API Design

This skill guides you through designing and implementing API endpoints using GoodVibes precision and project engine tools. Use this workflow when building REST APIs, GraphQL resolvers, tRPC procedures, or any HTTP endpoint.

## When to Use This Skill

Load this skill when:
- Building a new API endpoint or route
- Implementing request validation or middleware
- Designing error response formats
- Generating API documentation
- Syncing types between frontend and backend
- Migrating between API paradigms (REST to tRPC, etc.)

Trigger phrases: "create an API", "build endpoint", "implement route", "add validation", "GraphQL resolver", "tRPC procedure".

## Core Workflow

### Phase 1: Discovery

Before implementing anything, understand existing patterns.

#### Step 1.1: Map Existing Routes

Use `get_api_routes` to discover all API endpoints in the project.

```yaml
mcp__plugin_goodvibes_project-engine__get_api_routes:
  project_root: "."  # or specific path
```

**What this reveals:**
- Route file locations and naming conventions
- HTTP methods in use (GET, POST, PUT, DELETE, PATCH)
- Route structure (flat vs nested)
- Framework patterns (Next.js App Router, Express, Fastify, tRPC)

#### Step 1.2: Discover Patterns

Use `discover` to find middleware, validation, error handling, and auth patterns.

```yaml
discover:
  queries:
    - id: middleware
      type: grep
      pattern: "(middleware|use\\()"
      glob: "**/*.{ts,js}"
    - id: validation
      type: grep
      pattern: "(z\\.|yup\\.|joi\\.|validator\\.)"
      glob: "**/*.{ts,js}"
    - id: error_handlers
      type: grep
      pattern: "(catch|try|Error|throw)"
      glob: "src/api/**/*.{ts,js}"
    - id: auth_patterns
      type: grep
      pattern: "(auth|jwt|session|bearer|getServerSession)"
      glob: "**/*.{ts,js}"
  verbosity: files_only
```

**What this reveals:**
- Validation library in use (Zod, Yup, Joi)
- Error handling patterns
- Authentication middleware
- Existing route structure

#### Step 1.3: Read Key Files

Read 2-3 representative route files to understand implementation patterns.

```yaml
precision_read:
  files:
    - path: "src/api/users/route.ts"  # or discovered route
      extract: content
    - path: "src/lib/validation.ts"  # or discovered validation file
      extract: outline
  verbosity: standard
```

### Phase 2: Decision Making

Choose the API paradigm that fits your needs. See `references/api-style-guide.md` for the full decision tree.

#### Quick Decision Guide

Consult `references/api-style-guide.md` for the REST vs GraphQL vs tRPC vs Server Actions decision tree.

### Phase 3: Implementation

#### Step 3.1: Define Validation Schema

Create request validation using the project's validation library.

**Example with Zod:**

```typescript
import { z } from 'zod';

export const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
  role: z.enum(['user', 'admin']).default('user'),
});

export type CreateUserInput = z.infer<typeof createUserSchema>;
```

**Best Practices:**
- Validate all inputs (body, query params, headers)
- Use strict schemas (no unknown keys)
- Provide clear error messages
- Export inferred types for reuse

#### Step 3.2: Implement Route Handler

Write the route handler following project conventions.

**Next.js App Router Example:**

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { createUserSchema } from './schema';
import { db } from '@/lib/db';
import { getServerSession } from '@/lib/auth';

export async function POST(request: NextRequest) {
  // 1. Authentication
  const session = await getServerSession();
  if (!session) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    );
  }

  // 2. Parse and validate input
  const body = await request.json();
  const result = createUserSchema.safeParse(body);

  if (!result.success) {
    return NextResponse.json(
      { error: 'Validation failed', details: result.error.flatten() },
      { status: 400 }
    );
  }

  // 3. Authorization check
  if (session.user.role !== 'admin') {
    return NextResponse.json(
      { error: 'Forbidden' },
      { status: 403 }
    );
  }

  // 4. Business logic
  try {
    const user = await db.user.create({
      data: result.data,
    });

    return NextResponse.json(user, { status: 201 });
  } catch (error) {
    console.error('Failed to create user:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

**tRPC Example:**

```typescript
import { z } from 'zod';
import { protectedProcedure, router } from '../trpc';

export const userRouter = router({
  create: protectedProcedure
    .input(
      z.object({
        email: z.string().email(),
        name: z.string().min(2).max(100),
      })
    )
    .mutation(async ({ ctx, input }) => {
      if (ctx.session.user.role !== 'admin') {
        throw new TRPCError({ code: 'FORBIDDEN' });
      }

      return await ctx.db.user.create({
        data: input,
      });
    }),
});
```

#### Step 3.3: Write Using Precision Tools

Use `precision_write` to create route files, validation schemas, and types.

```yaml
precision_write:
  files:
    - path: "src/app/api/users/route.ts"
      content: |
        import { NextRequest, NextResponse } from 'next/server';
        // ... [full handler implementation]
    - path: "src/app/api/users/schema.ts"
      content: |
        import { z } from 'zod';
        export const createUserSchema = z.object({ ... });
  verbosity: count_only
```

### Phase 4: Error Handling

#### Standard Error Response Format

Maintain consistent error responses across all endpoints.

```typescript
interface APIError {
  error: string;           // Human-readable message
  code?: string;           // Machine-readable error code
  details?: unknown;       // Validation errors or additional context
  trace_id?: string;       // For debugging in production
}
```

**HTTP Status Code Guidelines:**
- `200` - Success
- `201` - Created (POST)
- `204` - No Content (DELETE)
- `400` - Bad Request (validation error)
- `401` - Unauthorized (not authenticated)
- `403` - Forbidden (not authorized)
- `404` - Not Found
- `409` - Conflict (duplicate resource)
- `500` - Internal Server Error

#### Error Handling Pattern

```typescript
try {
  // Business logic
} catch (error) {
  // Log for debugging (never expose to client)
  console.error('Operation failed:', error);

  // User-facing error
  return NextResponse.json(
    { error: 'Failed to process request' },
    { status: 500 }
  );
}
```

**Never expose:**
- Stack traces in production
- Database error messages
- File paths or internal structure
- Secrets or credentials

### Phase 5: Documentation

#### Step 5.1: Generate OpenAPI Spec

For REST APIs, generate OpenAPI documentation automatically.

```yaml
mcp__plugin_goodvibes_project-engine__generate_openapi:
  project_root: "."
  output_path: "docs/openapi.yaml"
```

**What this generates:**
- Route paths and HTTP methods
- Request/response schemas
- Authentication requirements
- Example requests/responses

If the tool doesn't exist or fails, manually document endpoints:

```yaml
# In a routes.md file
POST /api/users
Description: Create a new user
Auth: Required (admin)
Body: { email: string, name: string, role?: 'user' | 'admin' }
Response 201: User object
Response 400: Validation error
Response 401: Unauthorized
Response 403: Forbidden
```

#### Step 5.2: Add JSDoc Comments

Document route handlers with JSDoc.

```typescript
/**
 * Create a new user.
 * 
 * @requires Authentication (admin role)
 * @body {CreateUserInput} User data
 * @returns {User} Created user object
 * @throws {401} Unauthorized - Not authenticated
 * @throws {403} Forbidden - Not an admin
 * @throws {400} Bad Request - Validation failed
 */
export async function POST(request: NextRequest) {
  // ...
}
```

### Phase 6: Type Safety

#### Step 6.1: Sync Frontend/Backend Types

Use `sync_api_types` to check type alignment.

```yaml
mcp__plugin_goodvibes_project-engine__sync_api_types:
  backend_dir: "src/app/api"
  frontend_dir: "src/lib/api-client"
```

**What this checks:**
- Request types match between frontend and backend
- Response types are consistent
- No mismatched field names or types
- All endpoints have corresponding client code

#### Step 6.2: Export API Types

Expose types for client consumption.

```typescript
// src/types/api.ts
export type { CreateUserInput, User } from '@/app/api/users/schema';
```

For tRPC, types are automatically inferred:

```typescript
// Client code
import { trpc } from '@/lib/trpc';

const user = await trpc.user.create.mutate({
  email: 'test@example.com',
  name: 'Test User',
}); // Fully typed!
```

### Phase 7: Validation

#### Step 7.1: Validate API Contract

Use `validate_api_contract` to verify responses match spec.

```yaml
mcp__plugin_goodvibes_analysis-engine__validate_api_contract:
  spec_path: "docs/openapi.yaml"
  implementation_dir: "src/app/api"
```

**What this validates:**
- Response schemas match OpenAPI spec
- Status codes are correct
- Required fields are present
- Types are accurate

If the tool doesn't exist, manually test:

```bash
# Use curl or httpie to test endpoints
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","name":"Test"}'
```

#### Step 7.2: Run Type Check

Verify TypeScript compilation.

```yaml
precision_exec:
  commands:
    - cmd: "npm run typecheck"
      expect:
        exit_code: 0
        stderr_empty: true
  verbosity: minimal
```

#### Step 7.3: Run API Checklist Script

Use the validation script to ensure quality.

```bash
bash scripts/api-checklist.sh .
```

See `scripts/api-checklist.sh` for the complete validation suite.

## Middleware Patterns

Implement authentication, CORS, and rate limiting middleware following the patterns in `references/api-style-guide.md`. Always use environment variables for security-sensitive configuration like CORS origins.

## Testing

Test API endpoints with meaningful assertions covering success cases, validation errors, and authentication failures. See `references/api-style-guide.md` for testing patterns.

## Common Anti-Patterns

**DON'T:**
- Trust client input without validation
- Expose database errors to clients
- Use GET for mutations
- Return different response formats per endpoint
- Skip authentication checks
- Ignore authorization (resource ownership)
- Use `any` types in route handlers
- Hardcode sensitive values (API keys, secrets)
- Return 200 for errors

**DO:**
- Validate all inputs with strict schemas
- Use consistent error response format
- Follow HTTP semantics (GET = read, POST = create, etc.)
- Implement proper authentication and authorization
- Use TypeScript for all API code
- Load secrets from environment variables
- Return appropriate status codes
- Log errors for debugging (don't expose them)

## Quick Reference

**Discovery Phase:**
```yaml
get_api_routes: { project_root: "." }
discover: { queries: [middleware, validation, auth], verbosity: files_only }
precision_read: { files: [route examples], extract: content }
```

**Implementation Phase:**
```yaml
precision_write: { files: [route, schema, types], verbosity: count_only }
```

**Validation Phase:**
```yaml
generate_openapi: { project_root: ".", output_path: "docs/openapi.yaml" }
validate_api_contract: { spec_path: "docs/openapi.yaml" }
sync_api_types: { backend_dir: "src/api", frontend_dir: "src/lib" }
precision_exec: { commands: [{ cmd: "npm run typecheck" }] }
```

**Post-Implementation:**
```bash
bash scripts/api-checklist.sh .
```

For detailed decision trees and framework-specific patterns, see `references/api-style-guide.md`.
