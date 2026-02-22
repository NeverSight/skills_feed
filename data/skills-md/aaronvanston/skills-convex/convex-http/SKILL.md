---
name: convex-http
description: HTTP actions for webhooks and API endpoints in Convex. Use when building webhook handlers (Stripe, Clerk, GitHub), creating REST API endpoints, handling file uploads/downloads, or implementing CORS for browser requests.
---

# Convex HTTP Actions

## Basic HTTP Router

```typescript
// convex/http.ts
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";

const http = httpRouter();

http.route({
  path: "/health",
  method: "GET",
  handler: httpAction(async () => {
    return new Response(JSON.stringify({ status: "ok" }), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  }),
});

export default http;
```

## Webhook Handling

```typescript
// convex/http.ts
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";
import { internal } from "./_generated/api";

const http = httpRouter();

http.route({
  path: "/webhooks/stripe",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    const signature = request.headers.get("stripe-signature");
    if (!signature) {
      return new Response("Missing signature", { status: 400 });
    }

    const body = await request.text();

    try {
      await ctx.runAction(internal.stripe.verifyAndProcess, { body, signature });
      return new Response("OK", { status: 200 });
    } catch (error) {
      return new Response("Webhook error", { status: 400 });
    }
  }),
});

export default http;
```

## Webhook Signature Verification

```typescript
// convex/stripe.ts
"use node";

import { internalAction } from "./_generated/server";
import { v } from "convex/values";
import { internal } from "./_generated/api";
import Stripe from "stripe";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export const verifyAndProcess = internalAction({
  args: { body: v.string(), signature: v.string() },
  returns: v.null(),
  handler: async (ctx, args) => {
    const event = stripe.webhooks.constructEvent(
      args.body,
      args.signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    );

    switch (event.type) {
      case "checkout.session.completed":
        await ctx.runMutation(internal.payments.handleCheckout, {
          sessionId: event.data.object.id,
        });
        break;
    }
    return null;
  },
});
```

## CORS Configuration

```typescript
const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
};

// Handle preflight
http.route({
  path: "/api/data",
  method: "OPTIONS",
  handler: httpAction(async () => {
    return new Response(null, { status: 204, headers: corsHeaders });
  }),
});

// Actual endpoint
http.route({
  path: "/api/data",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    const body = await request.json();
    return new Response(JSON.stringify({ success: true }), {
      status: 200,
      headers: { "Content-Type": "application/json", ...corsHeaders },
    });
  }),
});
```

## Path Parameters

Use `pathPrefix` for dynamic routes:

```typescript
http.route({
  pathPrefix: "/api/users/",
  method: "GET",
  handler: httpAction(async (ctx, request) => {
    const url = new URL(request.url);
    const userId = url.pathname.replace("/api/users/", "");

    const user = await ctx.runQuery(internal.users.get, { userId });
    if (!user) return new Response("Not found", { status: 404 });

    return Response.json(user);
  }),
});
```

## API Key Authentication

```typescript
http.route({
  path: "/api/protected",
  method: "GET",
  handler: httpAction(async (ctx, request) => {
    const apiKey = request.headers.get("X-API-Key");
    if (!apiKey) {
      return Response.json({ error: "Missing API key" }, { status: 401 });
    }

    const isValid = await ctx.runQuery(internal.auth.validateApiKey, { apiKey });
    if (!isValid) {
      return Response.json({ error: "Invalid API key" }, { status: 403 });
    }

    const data = await ctx.runQuery(internal.data.getProtected, {});
    return Response.json(data);
  }),
});
```

## File Upload

```typescript
http.route({
  path: "/api/upload",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    const bytes = await request.bytes();
    const contentType = request.headers.get("Content-Type") ?? "application/octet-stream";

    const blob = new Blob([bytes], { type: contentType });
    const storageId = await ctx.storage.store(blob);

    return Response.json({ storageId });
  }),
});
```

## File Download

```typescript
http.route({
  pathPrefix: "/files/",
  method: "GET",
  handler: httpAction(async (ctx, request) => {
    const url = new URL(request.url);
    const fileId = url.pathname.replace("/files/", "") as Id<"_storage">;

    const fileUrl = await ctx.storage.getUrl(fileId);
    if (!fileUrl) return new Response("Not found", { status: 404 });

    return Response.redirect(fileUrl, 302);
  }),
});
```

## Error Handling Helper

```typescript
function jsonResponse(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

http.route({
  path: "/api/process",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    try {
      const body = await request.json();
      if (!body.data) {
        return jsonResponse({ error: "Missing data field" }, 400);
      }
      const result = await ctx.runMutation(internal.process.handle, body);
      return jsonResponse({ success: true, result });
    } catch (error) {
      return jsonResponse({ error: "Internal server error" }, 500);
    }
  }),
});
```

## References

- HTTP Actions: https://docs.convex.dev/functions/http-actions
