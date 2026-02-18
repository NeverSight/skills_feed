---
name: encore-service
description: Structure and organize Encore.ts services.
---

# Encore Service Structure

## Instructions

### Creating a Service

Every Encore service needs an `encore.service.ts` file:

```typescript
// encore.service.ts
import { Service } from "encore.dev/service";

export default new Service("my-service");
```

### Minimal Service Structure

```
my-service/
├── encore.service.ts    # Service definition (required)
├── api.ts               # API endpoints
└── db.ts                # Database (if needed)
```

## Application Patterns

### Single Service (Recommended Start)

Best for new projects - start simple, split later if needed:

```
my-app/
├── package.json
├── encore.app
├── encore.service.ts
├── api.ts
├── db.ts
└── migrations/
    └── 001_initial.up.sql
```

### Multi-Service

For distributed systems with clear domain boundaries:

```
my-app/
├── encore.app
├── package.json
├── user/
│   ├── encore.service.ts
│   ├── api.ts
│   └── db.ts
├── order/
│   ├── encore.service.ts
│   ├── api.ts
│   └── db.ts
└── notification/
    ├── encore.service.ts
    └── api.ts
```

### Large Application (System-based)

Group related services into systems:

```
my-app/
├── encore.app
├── commerce/
│   ├── order/
│   │   └── encore.service.ts
│   ├── cart/
│   │   └── encore.service.ts
│   └── payment/
│       └── encore.service.ts
├── identity/
│   ├── user/
│   │   └── encore.service.ts
│   └── auth/
│       └── encore.service.ts
└── comms/
    ├── email/
    │   └── encore.service.ts
    └── push/
        └── encore.service.ts
```

## Service-to-Service Calls

Import other services from `~encore/clients`:

```typescript
import { user } from "~encore/clients";

export const getOrderWithUser = api(
  { method: "GET", path: "/orders/:id", expose: true },
  async ({ id }): Promise<OrderWithUser> => {
    const order = await getOrder(id);
    const orderUser = await user.get({ id: order.userId });
    return { ...order, user: orderUser };
  }
);
```

## When to Split Services

Split when you have:

| Signal | Action |
|--------|--------|
| Different scaling needs | Split (e.g., auth vs analytics) |
| Different deployment cycles | Split |
| Clear domain boundaries | Split |
| Shared database tables | Keep together |
| Tightly coupled logic | Keep together |
| Just organizing code | Use folders, not services |

## Service with Middleware

```typescript
import { Service } from "encore.dev/service";
import { middleware } from "encore.dev/api";

const loggingMiddleware = middleware(
  { target: { all: true } },
  async (req, next) => {
    console.log(`Request: ${req.requestMeta?.path}`);
    return next(req);
  }
);

export default new Service("my-service", {
  middlewares: [loggingMiddleware],
});
```

## Guidelines

- Services cannot be nested within other services
- Start with one service, split when there's a clear reason
- Use `~encore/clients` for cross-service calls (never direct imports)
- Each service can have its own database
- Service names should be lowercase, descriptive
- Don't create services just for code organization - use folders instead
