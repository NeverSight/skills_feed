---
name: openapi-pro
description: Senior API Architect & Integration Engineer for 2026. Specialized in Type-Safe API contracts using OpenAPI 3.1, Zod-First schema derivation, and automated TypeScript client generation. Expert in bridging the gap between Hono backends and Next.js 16 frontends using `openapi-fetch`, `orval`, and unified monorepo type-sharing.
---

# 📄 Skill: openapi-pro (v1.0.0)

## Executive Summary
Senior API Architect & Integration Engineer for 2026. Specialized in Type-Safe API contracts using OpenAPI 3.1, Zod-First schema derivation, and automated TypeScript client generation. Expert in bridging the gap between Hono backends and Next.js 16 frontends using `openapi-fetch`, `orval`, and unified monorepo type-sharing.

---

## 📋 The Conductor's Protocol

1.  **Contract Strategy Selection**: Determine if the project is **Contract-First** (OpenAPI YAML → Code) or **Code-First** (Zod/Hono → OpenAPI YAML).
2.  **Schema Auditing**: Validate the OpenAPI specification for completeness (security schemes, error responses, examples).
3.  **Sequential Activation**:
    `activate_skill(name="openapi-pro")` → `activate_skill(name="prisma-expert")` → `activate_skill(name="next16-expert")`.
4.  **Verification**: Execute `bun x openapi-typescript` or `orval` to verify that generated types match the latest schema.

---

## 🛠️ Mandatory Protocols (2026 Standards)

### 1. Zod-First Contract Derivation
As of 2026, Zod is the source of truth for runtime validation.
- **Rule**: Never manually write OpenAPI YAML if using TypeScript. Use `zod-to-openapi` or Hono's `@hono/zod-openapi` to derive the spec from your schemas.
- **Protocol**: Centralize Zod schemas in a shared monorepo package (e.g., `@repo/api-contract`).

### 2. Type-Safe Fetch Clients
- **Rule**: Avoid generic `axios` or `fetch` wrappers. Use generated clients like `openapi-fetch` that provide sub-millisecond autocomplete and compile-time error checking.
- **Protocol**: Always include `4xx` and `5xx` error definitions in the schema to ensure the client handles failures gracefully.

### 3. OpenAPI 3.1 & JSON Schema Compatibility
- **Rule**: Use OpenAPI 3.1 to leverage full JSON Schema 2020-12 compatibility (including `const`, `dependentSchemas`, and improved `examples`).

### 4. Continuous Generation (DaC)
- **Rule**: Generated files (e.g., `api-client.ts`) should NEVER be edited manually.
- **Protocol**: Add a CI check to ensure the generated client is in sync with the current OpenAPI spec.

---

## 🚀 Show, Don't Just Tell (Implementation Patterns)

### Hono + Zod-OpenAPI (Backend)
```typescript
import { createRoute, z } from '@hono/zod-openapi'

const UserSchema = z.object({
  id: z.string().openapi({ example: '123' }),
  name: z.string().openapi({ example: 'John Doe' }),
})

const route = createRoute({
  method: 'get',
  path: '/users/{id}',
  responses: {
    200: {
      content: { 'application/json': { schema: UserSchema } },
      description: 'Retrieve the user',
    },
  },
})

export type AppRoute = typeof route;
```

### Type-Safe Fetch (Next.js 16 Client)
```typescript
import createClient from "openapi-fetch";
import type { paths } from "@repo/api-contract"; // Generated types

const client = createClient<paths>({ baseUrl: "https://api.example.com" });

const { data, error } = await client.GET("/users/{id}", {
  params: {
    path: { id: "123" },
  },
});

if (error) {
  // Error is fully typed based on the 4xx/5xx definitions in OpenAPI
  console.error(error.message);
}
```

---

## 🛡️ The Do Not List (Anti-Patterns)

1.  **DO NOT** use `any` in your API schemas. Every field must have a type and, ideally, an example.
2.  **DO NOT** forget to define `SecuritySchemes` (JWT, API Keys) in the OpenAPI spec.
3.  **DO NOT** hardcode base URLs in the generated client. Use environment variables.
4.  **DO NOT** publish the OpenAPI spec without validation. Use `redocly lint`.
5.  **DO NOT** mix camelCase and snake_case in the same API. Stick to one standard (camelCase preferred for TS).

---

## 📂 Progressive Disclosure (Deep Dives)

- **[Zod-to-OpenAPI Guide](./references/zod-derivation.md)**: Deriving specs from Zod schemas.
- **[Client Generation with Orval](./references/orval-config.md)**: Advanced configuration for React Query & Fetch.
- **[API Versioning Strategies](./references/versioning.md)**: Header-based vs. URL-based versioning in 2026.
- **[Linting & Validation](./references/linting.md)**: Using Redocly and Spectral for contract quality.

---

## 🛠️ Specialized Tools & Scripts

- `scripts/generate-client.sh`: A wrapper around `openapi-fetch` to generate types and clients.
- `scripts/validate-spec.ts`: Validates the OpenAPI YAML against 2026 "Elite" standards.

---

## 🎓 Learning Resources
- [OpenAPI 3.1 Specification](https://spec.openapis.org/oas/v3.1.0)
- [Hono Zod-OpenAPI Docs](https://hono.dev/examples/zod-openapi)
- [OpenAPI Fetch Guide](https://openapi-ts.dev/openapi-fetch/)

---
*Updated: January 23, 2026 - 19:50*
