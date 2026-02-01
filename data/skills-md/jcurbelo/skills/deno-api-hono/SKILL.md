---
name: deno-api-hono
description: Guidelines for building production-ready HTTP APIs with Deno and Hono framework. Use when creating REST APIs, web services, microservices, or any HTTP server using Deno runtime and Hono. Covers authentication, rate limiting, validation, and deployment patterns.
---

# Deno API with Hono

You are an expert in Deno and TypeScript development with deep knowledge of
building secure, scalable HTTP APIs using the Hono framework, Deno's native
TypeScript support, and modern web standards.

## TypeScript General Guidelines

### Basic Principles

- Use English for all code and documentation
- Always declare types for variables and functions (parameters and return
  values)
- Avoid using `any` type - create necessary types instead
- Use JSDoc to document public classes and methods
- Write concise, maintainable, and technically accurate code
- Use functional and declarative programming patterns
- No configuration needed - Deno runs TypeScript natively

### Nomenclature

- Use PascalCase for types and interfaces
- Use camelCase for variables, functions, and methods
- Use kebab-case for file and directory names
- Use UPPERCASE for environment variables
- Use descriptive variable names with auxiliary verbs: `isLoading`, `hasError`,
  `canDelete`
- Start each function with a verb

### Functions

- Write short functions with a single purpose
- Use arrow functions for simple operations and consistency
- Use async/await for asynchronous operations
- Prefer the RO-RO pattern (Receive Object, Return Object) for multiple
  parameters

### Types and Interfaces

- Prefer interfaces over types for object shapes (better for extensibility in
  APIs)
- Avoid enums; use const objects with `as const`
- Use Zod for runtime validation with inferred types
- Use `readonly` for immutable properties

---

## Questions to Ask First

Before implementing, clarify these with the user to determine which patterns to
apply:

1. **Authentication**: "What authentication method do you need - JWT tokens, API
   keys, or both?"
2. **Rate limiting**: "Do you need rate limiting? If yes, do you want to use
   Upstash Redis or in-memory?"
3. **Database**: "What database will you use - Upstash Redis, PostgreSQL, or
   none (stateless)?"
4. **Logging**: "Do you need structured logging with @std/log, or is console.log
   sufficient?"
5. **Validation**: "Do you want request validation with Zod, or manual
   validation?"
6. **Deployment**: "Will this deploy to Deno Deploy, Docker, or run standalone?"

---

## Guides

The following sections are **templates and patterns** to apply based on the
user's answers above. Adapt them to the specific use case.

---

## Project Structure

```
project/
├── deno.json                 # Configuration, tasks, and imports
├── .env                      # Environment variables (gitignored)
├── .env.example              # Environment variables template
└── src/
    ├── main.ts              # Entry point
    ├── config/              # Configuration layer
    │   ├── env.ts           # Environment variables with validation
    │   └── logger.ts        # Logging (if needed)
    ├── routes/              # Route handlers
    │   ├── index.ts         # Main app and route registration
    │   └── <domain>.ts      # Domain-specific routes
    ├── services/            # Business logic layer
    │   └── <domain>.ts      # Domain-specific services
    ├── types/               # TypeScript definitions
    │   └── api.ts           # API types
    └── utils/               # Utility functions
        └── api.ts           # Response helpers
```

## deno.json Configuration

```json
{
  "tasks": {
    "dev": "deno run --allow-net --allow-env --allow-read --watch src/main.ts",
    "start": "deno run --allow-net --allow-env --allow-read src/main.ts",
    "check": "deno fmt --check && deno check src/**/*.ts"
  },
  "imports": {
    "@std/dotenv": "jsr:@std/dotenv@0.225",
    "hono": "jsr:@hono/hono"
  },
  "deploy": {
    "entrypoint": "src/main.ts"
  }
}
```

**Add imports based on needs:**

```bash
# Always needed
deno add jsr:@std/dotenv jsr:@hono/hono

# If using JWT authentication
deno add jsr:@hono/hono/jwt npm:djwt

# If using Upstash Redis
deno add npm:@upstash/redis npm:@upstash/ratelimit

# If using structured logging
deno add jsr:@std/log
```

## Quality Checks

Always run before committing:

```bash
deno fmt
deno check src/**/*.ts

# Or use task
deno task check
```

## Environment Configuration

**Guide**: Always use `@std/dotenv`. Never hardcode secrets.

```typescript
// src/config/env.ts
import "@std/dotenv/load";

const assertEnv = (name: string): string => {
  const value = Deno.env.get(name);
  if (!value) {
    console.error(`Missing ${name} environment variable`);
    Deno.exit(1);
  }
  return value;
};

export const PORT = Number(Deno.env.get("PORT") ?? 8000);

// Add based on user's answers:
// export const JWT_SECRET = assertEnv("JWT_SECRET");
// export const ADMIN_API_KEY = assertEnv("ADMIN_API_KEY");
// export const UPSTASH_REDIS_URL = assertEnv("UPSTASH_REDIS_URL");
```

**.env.example:**

```
PORT=8000
# Add based on needs:
# JWT_SECRET="your_secret"
# ADMIN_API_KEY="your_api_key"
# UPSTASH_REDIS_URL="your_url"
# UPSTASH_REDIS_TOKEN="your_token"
```

## Hono App Initialization

**Guide**: Basic setup for all APIs.

```typescript
// src/main.ts
import { initializeRoutes } from "./routes/index.ts";

initializeRoutes();
```

```typescript
// src/routes/index.ts
import { Hono } from "hono";
import { PORT } from "../config/env.ts";

export const initializeRoutes = (): void => {
  const app = new Hono();

  // Mount routes based on domains
  // app.route("/auth", authRoutes);
  // app.route("/users", userRoutes);

  app.get("/", (c) => c.json({ message: "API is running" }));
  app.get("/health", (c) => c.json({ status: "ok" }));

  Deno.serve({ port: PORT }, app.fetch);
};
```

## Route Patterns

**Guide**: Use arrow functions. Keep routes thin, move logic to services.

```typescript
// src/routes/<domain>.ts
import { Hono } from "hono";
import type { Context } from "hono";
import { errorResponse, successResponse } from "../utils/api.ts";
import type { CreateRequest, CreateResponse } from "../types/api.ts";

const app = new Hono();

app.post("/", async (c: Context) => {
  const body = await c.req.json<CreateRequest>();
  const { name, email } = body;

  if (!name || !email) {
    return errorResponse(c, "Missing required fields", 400);
  }

  // Call service layer
  const result = await createItem(name, email);

  if (!result.success) {
    return errorResponse(c, result.reason || "Failed", 400);
  }

  return successResponse(c, result.data);
});

export default app;
```

## Response Patterns

**Guide**: Standardized responses for consistency.

```typescript
// src/utils/api.ts
import type { Context } from "hono";

type ApiSuccessResponse<T> = { success: true; data: T };
type ApiErrorResponse = { success: false; error: string };

export const successResponse = <T>(c: Context, data: T): Response => {
  const response: ApiSuccessResponse<T> = { success: true, data };
  return c.json(response);
};

export const errorResponse = (
  c: Context,
  error: string,
  status: number,
): Response => {
  const response: ApiErrorResponse = { success: false, error };
  return c.json(response, status);
};
```

## Type Definitions

**Guide**: Define types for all requests and responses.

```typescript
// src/types/api.ts
export type CreateRequest = {
  name: string;
  email: string;
};

export type CreateResponse = {
  id: string;
  createdAt: string;
};

// Service result pattern
export type ServiceResult<T> = {
  success: boolean;
  data?: T;
  reason?: string;
};
```

## Middleware: API Key Authentication

**Guide**: Apply if user wants API key authentication.

```typescript
import type { Context } from "hono";
import { ADMIN_API_KEY } from "../config/env.ts";
import { errorResponse } from "../utils/api.ts";

const apiKeyAuth = async (
  c: Context,
  next: () => Promise<void>,
): Promise<Response | void> => {
  const apiKey = c.req.header("x-api-key");

  if (!apiKey) {
    return errorResponse(c, "Missing API key", 401);
  }

  if (apiKey !== ADMIN_API_KEY) {
    return errorResponse(c, "Invalid API key", 401);
  }

  await next();
};

// Usage in routes
app.use("/*", apiKeyAuth);
```

## Middleware: JWT Authentication

**Guide**: Apply if user wants JWT authentication.

```typescript
import { Hono } from "hono";
import { jwt } from "hono/jwt";
import { JWT_SECRET } from "../config/env.ts";

const app = new Hono();

app.use("/*", jwt({ secret: JWT_SECRET }));

app.get("/protected", (c) => {
  const payload = c.get("jwtPayload");
  return c.json({ userId: payload.sub });
});
```

**JWT Token Generation (if needed):**

```typescript
// src/services/jwt.ts
import { create, verify } from "djwt";

const encoder = new TextEncoder();
const keyData = encoder.encode(JWT_SECRET);

const jwtKey = await crypto.subtle.importKey(
  "raw",
  keyData,
  { name: "HMAC", hash: "SHA-256" },
  false,
  ["sign", "verify"],
);

export const generateToken = async (userId: string): Promise<string> => {
  const now = Math.floor(Date.now() / 1000);
  return create(
    { alg: "HS256", typ: "JWT" },
    { sub: userId, exp: now + 3600 },
    jwtKey,
  );
};

export const verifyToken = async (token: string): Promise<unknown> => {
  return verify(token, jwtKey);
};
```

## Database: Upstash Redis

**Guide**: Apply if user wants Redis/Upstash.

```typescript
// src/services/redis.ts
import { Redis } from "@upstash/redis";
import { UPSTASH_REDIS_TOKEN, UPSTASH_REDIS_URL } from "../config/env.ts";

const redis = new Redis({
  url: UPSTASH_REDIS_URL,
  token: UPSTASH_REDIS_TOKEN,
});

export default redis;

// Usage patterns:
// await redis.set(`user:${id}`, userData);
// const user = await redis.get<User>(`user:${id}`);
// await redis.setex(`session:${id}`, 3600, sessionData); // with TTL
```

## Rate Limiting

**Guide**: Apply if user wants rate limiting with Upstash.

```typescript
// src/services/ratelimit.ts
import { Ratelimit } from "@upstash/ratelimit";
import redis from "./redis.ts";

export const apiRateLimit = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(100, "1 m"),
  prefix: "@app/ratelimit",
});

// Usage in routes:
app.post("/action", async (c: Context) => {
  const identifier = c.req.header("x-user-id") || "anonymous";
  const { success } = await apiRateLimit.limit(identifier);

  if (!success) {
    return errorResponse(c, "Rate limit exceeded", 429);
  }

  // Continue...
});
```

## Logging

**Guide**: Apply if user wants structured logging.

```typescript
// src/config/logger.ts
import { ConsoleHandler, getLogger, setup } from "@std/log";

export const initializeLogger = (): void => {
  setup({
    handlers: {
      console: new ConsoleHandler("DEBUG"),
    },
    loggers: {
      default: { level: "DEBUG", handlers: ["console"] },
    },
  });
};

class LoggerWrapper {
  private logger = getLogger();

  private format = (msg: unknown, ...args: unknown[]): string =>
    [msg, ...args]
      .map((p) => (typeof p === "object" ? JSON.stringify(p) : String(p)))
      .join(" ");

  debug = (msg: unknown, ...args: unknown[]): void =>
    this.logger.debug(this.format(msg, ...args));
  info = (msg: unknown, ...args: unknown[]): void =>
    this.logger.info(this.format(msg, ...args));
  warn = (msg: unknown, ...args: unknown[]): void =>
    this.logger.warn(this.format(msg, ...args));
  error = (msg: unknown, ...args: unknown[]): void =>
    this.logger.error(this.format(msg, ...args));
}

export const logger = new LoggerWrapper();
```

## Request Validation with Zod

**Guide**: Apply if user wants Zod validation.

```typescript
import { z } from "zod";

const CreateUserSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
});

app.post("/users", async (c: Context) => {
  const body = await c.req.json();
  const parsed = CreateUserSchema.safeParse(body);

  if (!parsed.success) {
    return errorResponse(c, parsed.error.message, 400);
  }

  const { name, email } = parsed.data;
  // Continue with validated data...
});
```

## HTTP Status Codes

| Code | Usage                          |
| ---- | ------------------------------ |
| 200  | Success                        |
| 400  | Bad request / validation error |
| 401  | Unauthorized                   |
| 403  | Forbidden                      |
| 429  | Rate limit exceeded            |
| 500  | Internal server error          |

## Security Model

Deno is secure by default. Request only necessary permissions:

```bash
# Run with specific permissions
deno run --allow-net --allow-env --allow-read src/main.ts

# Permission flags
--allow-net=:8000           # Listen on specific port only
--allow-read=./src          # Read access to source files
--allow-env=PORT,API_KEY    # Specific environment variables
```

## Testing with Built-in Test Runner

**Guide**: Apply when user needs API endpoint tests.

```typescript
// src/routes/users_test.ts
import { assertEquals } from "@std/assert";
import { describe, it } from "@std/testing/bdd";
import app from "./users.ts";

describe("Users API", () => {
  it("GET /users returns 200", async () => {
    const res = await app.request("/users");
    assertEquals(res.status, 200);
  });

  it("POST /users validates input", async () => {
    const res = await app.request("/users", {
      method: "POST",
      body: JSON.stringify({ name: "" }),
      headers: { "Content-Type": "application/json" },
    });
    assertEquals(res.status, 400);
  });
});
```

```bash
# Run tests
deno test --allow-net --allow-env
```

## Built-in Tooling

```bash
# Formatting (uses Deno defaults)
deno fmt

# Linting
deno lint

# Type checking
deno check src/**/*.ts

# Dependency inspection
deno info src/main.ts

# Compile to standalone executable
deno compile --allow-net --allow-env --allow-read src/main.ts
```

## Web Standards

Deno and Hono embrace web standards. Use:

- `fetch()` for HTTP requests to external APIs
- `Request` and `Response` objects (native to Hono)
- `URL` and `URLSearchParams` for URL manipulation
- `Web Crypto API` for cryptography
- `Streams API` for large response bodies
- `FormData` for multipart data handling
- `Headers` for request/response headers

## Performance

- Use `Deno.serve()` via Hono for high-performance HTTP
- Leverage streaming responses for large payloads
- Use connection pooling for database connections
- Compile to standalone executables for deployment
- Use Deno Deploy for edge deployment

## Run Commands

```bash
# Development with hot reload
deno task dev

# Production
deno task start

# Format and check
deno task check

# Direct execution
deno run --allow-net --allow-env --allow-read src/main.ts
```
