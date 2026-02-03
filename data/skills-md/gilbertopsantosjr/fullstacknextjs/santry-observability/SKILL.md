---
name: santry-observability
description: "Guide for implementing observability Next.js with Sentry for server actions using ZSA (Zod Server Actions)"
---

## Observability with Sentry

### Installation

```bash
npm install @sentry/nextjs
npx @sentry/wizard@latest -i nextjs
```

### Configuration

```typescript
// sentry.client.config.ts
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
});

// sentry.server.config.ts
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 1.0,
});
```

### Tracking Server Action Errors

```typescript
"use server";

import * as Sentry from "@sentry/nextjs";
import { createServerAction } from "zsa";
import z from "zod";

export const createPaymentAction = createServerAction()
  .input(z.object({ 
    amount: z.number().positive(), 
    userId: z.string() 
  }))
  .onError(async ({ err, input }) => {
    // Automatically capture errors to Sentry
    Sentry.captureException(err, {
      tags: {
        action: "createPayment",
        userId: input.userId,
      },
      contexts: {
        action: {
          input: input,
          timestamp: new Date().toISOString(),
        },
      },
    });
  })
  .handler(async ({ input }) => {
    return await PaymentService.create(input);
  });
```

### Transaction Tracing

```typescript
"use server";

import * as Sentry from "@sentry/nextjs";
import { createServerAction } from "zsa";
import z from "zod";

export const processOrderAction = createServerAction()
  .input(z.object({ orderId: z.string() }))
  .handler(async ({ input }) => {
    return await Sentry.startSpan(
      {
        name: "processOrderAction",
        op: "server.action",
        attributes: {
          orderId: input.orderId,
        },
      },
      async (span) => {
        // Step 1: Validate order
        const validationSpan = Sentry.startInactiveSpan({
          name: "validateOrder",
          op: "validation",
        });
        const order = await OrderService.validate(input.orderId);
        validationSpan?.end();

        // Step 2: Process payment
        const paymentSpan = Sentry.startInactiveSpan({
          name: "processPayment",
          op: "payment",
        });
        const payment = await PaymentService.process(order);
        paymentSpan?.end();

        // Step 3: Update inventory
        const inventorySpan = Sentry.startInactiveSpan({
          name: "updateInventory",
          op: "inventory",
        });
        await InventoryService.update(order.items);
        inventorySpan?.end();

        span.setStatus({ code: 1, message: "success" });
        return { orderId: order.id, status: "completed" };
      }
    );
  });
```

### User Context & Breadcrumbs

```typescript
"use server";

import * as Sentry from "@sentry/nextjs";
import { authedProcedure } from "@/lib/procedures";
import z from "zod";

export const updateProfileAction = authedProcedure
  .createServerAction()
  .input(z.object({ name: z.string(), email: z.string().email() }))
  .onStart(async () => {
    Sentry.addBreadcrumb({
      category: "action",
      message: "Profile update started",
      level: "info",
    });
  })
  .handler(async ({ input, ctx }) => {
    // Set user context for all events
    Sentry.setUser({
      id: ctx.user.id,
      email: ctx.user.email,
      username: ctx.user.name,
    });

    Sentry.addBreadcrumb({
      category: "action",
      message: "Updating user profile",
      level: "info",
      data: { userId: ctx.user.id },
    });

    try {
      const result = await UserService.updateProfile(ctx.user.id, input);
      
      Sentry.addBreadcrumb({
        category: "action",
        message: "Profile updated successfully",
        level: "info",
      });

      return result;
    } catch (error) {
      Sentry.addBreadcrumb({
        category: "action",
        message: "Profile update failed",
        level: "error",
        data: { error: (error as Error).message },
      });
      throw error;
    }
  });
```

### Custom Error Boundaries with Sentry

```typescript
// components/error-boundary.tsx
"use client";

import * as Sentry from "@sentry/nextjs";
import { useEffect } from "react";

export function ActionErrorBoundary({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    Sentry.captureException(error, {
      tags: {
        component: "ActionErrorBoundary",
      },
    });
  }, [error]);

  return (
    <div className="error-container">
      <h2>Something went wrong!</h2>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

### Performance Monitoring

```typescript
"use server";

import * as Sentry from "@sentry/nextjs";
import { createServerAction } from "zsa";
import z from "zod";

export const searchAction = createServerAction()
  .input(z.object({ query: z.string(), filters: z.record(z.any()).optional() }))
  .handler(async ({ input }) => {
    const transaction = Sentry.startTransaction({
      name: "searchAction",
      op: "server.action",
      data: {
        query: input.query,
        filtersCount: Object.keys(input.filters || {}).length,
      },
    });

    try {
      const span1 = transaction.startChild({
        op: "db.query",
        description: "Search database",
      });
      const results = await db.search(input.query);
      span1.finish();

      const span2 = transaction.startChild({
        op: "processing",
        description: "Apply filters",
      });
      const filtered = applyFilters(results, input.filters);
      span2.finish();

      transaction.setStatus("ok");
      return filtered;
    } catch (error) {
      transaction.setStatus("internal_error");
      Sentry.captureException(error);
      throw error;
    } finally {
      transaction.finish();
    }
  });
```

### Integration with Procedures

```typescript
// lib/procedures.ts
"use server";

import * as Sentry from "@sentry/nextjs";
import { createServerActionProcedure } from "zsa";

export const authedProcedure = createServerActionProcedure()
  .handler(async () => {
    const session = await auth();
    
    if (!session?.user) {
      Sentry.captureMessage("Unauthenticated access attempt", {
        level: "warning",
        tags: { procedure: "authedProcedure" },
      });
      throw new Error("Not authenticated");
    }

    // Set user context for all subsequent operations
    Sentry.setUser({
      id: session.user.id,
      email: session.user.email,
      role: session.user.role,
    });

    Sentry.addBreadcrumb({
      category: "auth",
      message: "User authenticated",
      level: "info",
      data: { userId: session.user.id },
    });

    return { 
      user: { 
        id: session.user.id, 
        email: session.user.email, 
        role: session.user.role 
      } 
    };
  });
```

### Best Practices for Sentry Integration

1. **Always capture context** - Include user ID, action name, and relevant input in error reports
2. **Use breadcrumbs** - Track action lifecycle (start, validation, processing, completion)
3. **Set appropriate log levels** - `error` for failures, `warning` for auth issues, `info` for normal flow
4. **Scrub sensitive data** - Never log passwords, tokens, or PII
5. **Use transaction tracing** - Group related operations for performance analysis
6. **Set user context early** - In procedures, not in individual actions
7. **Tag errors properly** - Use consistent tags (action name, feature, user role) for filtering
8. **Monitor performance** - Track slow actions with custom spans

### Environment Variables

```bash
# .env.local
NEXT_PUBLIC_SENTRY_DSN=your-client-dsn
SENTRY_DSN=your-server-dsn
SENTRY_AUTH_TOKEN=your-auth-token
SENTRY_ORG=your-org
SENTRY_PROJECT=your-project
```