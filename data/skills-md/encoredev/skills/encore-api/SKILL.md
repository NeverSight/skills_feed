---
name: encore-api
description: Create type-safe API endpoints with Encore.ts.
---

# Encore API Endpoints

## Instructions

When creating API endpoints with Encore.ts, follow these patterns:

### 1. Import the API module

```typescript
import { api } from "encore.dev/api";
```

### 2. Define typed request/response interfaces

Always define explicit TypeScript interfaces for request and response types:

```typescript
interface CreateUserRequest {
  email: string;
  name: string;
}

interface CreateUserResponse {
  id: string;
  email: string;
  name: string;
}
```

### 3. Create the endpoint

```typescript
export const createUser = api(
  { method: "POST", path: "/users", expose: true },
  async (req: CreateUserRequest): Promise<CreateUserResponse> => {
    // Implementation
  }
);
```

## API Options

| Option | Type | Description |
|--------|------|-------------|
| `method` | string | HTTP method: GET, POST, PUT, PATCH, DELETE |
| `path` | string | URL path, supports `:param` and `*wildcard` |
| `expose` | boolean | If true, accessible from outside (default: false) |
| `auth` | boolean | If true, requires authentication |

## Parameter Types

### Path Parameters

```typescript
// Path: "/users/:id"
interface GetUserRequest {
  id: string;  // Automatically mapped from :id
}
```

### Query Parameters

```typescript
import { Query } from "encore.dev/api";

interface ListUsersRequest {
  limit?: Query<number>;
  offset?: Query<number>;
}
```

### Headers

```typescript
import { Header } from "encore.dev/api";

interface WebhookRequest {
  signature: Header<"X-Webhook-Signature">;
  payload: string;
}
```

## Request Validation

Encore validates requests at runtime using TypeScript types. Add constraints for stricter validation:

```typescript
import { api, Min, Max, MinLen, MaxLen, IsEmail, IsURL } from "encore.dev/api";

interface CreateUserRequest {
  email: string & IsEmail;                    // Must be valid email
  username: string & MinLen<3> & MaxLen<20>;  // 3-20 characters
  age: number & Min<13> & Max<120>;           // Between 13 and 120
  website?: string & IsURL;                   // Optional, must be URL if provided
}
```

### Available Validators

| Validator | Applies To | Example |
|-----------|-----------|---------|
| `Min<N>` | number | `age: number & Min<18>` |
| `Max<N>` | number | `count: number & Max<100>` |
| `MinLen<N>` | string, array | `name: string & MinLen<1>` |
| `MaxLen<N>` | string, array | `tags: string[] & MaxLen<10>` |
| `IsEmail` | string | `email: string & IsEmail` |
| `IsURL` | string | `link: string & IsURL` |

### Validation Error Response

Invalid requests return 400 with details:

```json
{
  "code": "invalid_argument",
  "message": "validation failed",
  "details": { "field": "email", "error": "must be a valid email" }
}
```

## Raw Endpoints

Use `api.raw` for webhooks or when you need direct request/response access:

```typescript
export const stripeWebhook = api.raw(
  { expose: true, path: "/webhooks/stripe", method: "POST" },
  async (req, res) => {
    const sig = req.headers["stripe-signature"];
    // Handle raw request...
    res.writeHead(200);
    res.end();
  }
);
```

## Error Handling

Use `APIError` for proper HTTP error responses:

```typescript
import { APIError, ErrCode } from "encore.dev/api";

// Throw with error code
throw new APIError(ErrCode.NotFound, "user not found");

// Or use shorthand
throw APIError.notFound("user not found");
throw APIError.invalidArgument("email is required");
throw APIError.unauthenticated("invalid token");
```

## Common Error Codes

| Code | HTTP Status | Usage |
|------|-------------|-------|
| `NotFound` | 404 | Resource doesn't exist |
| `InvalidArgument` | 400 | Bad input |
| `Unauthenticated` | 401 | Missing/invalid auth |
| `PermissionDenied` | 403 | Not allowed |
| `AlreadyExists` | 409 | Duplicate resource |

## Static Assets

Serve static files (HTML, CSS, JS, images) with `api.static`:

```typescript
import { api } from "encore.dev/api";

// Serve files from ./assets under /static/*
export const assets = api.static(
  { expose: true, path: "/static/*path", dir: "./assets" }
);

// Serve at root (use !path for fallback routing)
export const frontend = api.static(
  { expose: true, path: "/!path", dir: "./dist" }
);

// Custom 404 page
export const app = api.static(
  { expose: true, path: "/!path", dir: "./public", notFound: "./404.html" }
);
```

## Guidelines

- Always use `import` not `require`
- Define explicit interfaces for type safety
- Use `expose: true` only for public endpoints
- Use `api.raw` for webhooks, `api` for everything else
- Throw `APIError` instead of returning error objects
- Path parameters are automatically extracted from the path pattern
- Use validation constraints (`Min`, `MaxLen`, etc.) for user input
