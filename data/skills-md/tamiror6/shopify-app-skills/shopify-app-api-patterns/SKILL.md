---
name: shopify-app-api-patterns
description: Frontend-backend communication patterns in Shopify Remix apps. Use when adding pages that need backend data, creating data mutations, using loaders and actions, handling authenticated requests, or managing session and authentication in routes.
---

# Shopify App API Patterns

Use this skill when building frontend features that communicate with your app's backend in a Shopify Remix app.

## When to Use

- Adding new pages that fetch data from Shopify or your database
- Creating forms that submit data (mutations)
- Using `useFetcher` for client-side data operations
- Handling authenticated sessions in routes
- Building APIs for app extensions or external services

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Shopify Admin                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Your App (iframe)                       │    │
│  │                                                      │    │
│  │  ┌──────────────┐       ┌──────────────────────┐   │    │
│  │  │   Frontend   │ ───── │   Remix Backend      │   │    │
│  │  │   (React)    │       │   (loaders/actions)  │   │    │
│  │  └──────────────┘       └──────────────────────┘   │    │
│  │                                    │                │    │
│  └────────────────────────────────────│────────────────┘    │
│                                       │                      │
└───────────────────────────────────────│──────────────────────┘
                                        │
                           ┌────────────┴────────────┐
                           │                         │
                    ┌──────▼──────┐          ┌──────▼──────┐
                    │   Prisma    │          │  Shopify    │
                    │   (your DB) │          │  Admin API  │
                    └─────────────┘          └─────────────┘
```

## Data Fetching with Loaders

### Basic Loader Pattern

```typescript
// app/routes/app.dashboard.tsx
import { json, type LoaderFunctionArgs } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";
import { authenticate } from "../shopify.server";
import db from "../db.server";

export const loader = async ({ request }: LoaderFunctionArgs) => {
  // Authenticate and get admin API access
  const { session, admin } = await authenticate.admin(request);
  
  // Fetch from Shopify
  const shopResponse = await admin.graphql(`
    query { shop { name myshopifyDomain } }
  `);
  const { data: shopData } = await shopResponse.json();
  
  // Fetch from your database
  const settings = await db.appSettings.findUnique({
    where: { shop: session.shop }
  });
  
  return json({
    shop: shopData.shop,
    settings
  });
};

export default function Dashboard() {
  const { shop, settings } = useLoaderData<typeof loader>();
  
  return (
    <Page title={`Dashboard - ${shop.name}`}>
      {/* Your UI */}
    </Page>
  );
}
```

### Loader with URL Parameters

```typescript
// app/routes/app.campaigns.$id.tsx
export const loader = async ({ request, params }: LoaderFunctionArgs) => {
  const { session } = await authenticate.admin(request);
  const { id } = params;
  
  const campaign = await db.campaign.findFirst({
    where: { 
      id,
      shop: session.shop 
    }
  });
  
  if (!campaign) {
    throw new Response("Not found", { status: 404 });
  }
  
  return json({ campaign });
};
```

## Data Mutations with Actions

### Form Submission Pattern

```typescript
// app/routes/app.settings.tsx
import { json, type ActionFunctionArgs } from "@remix-run/node";
import { Form, useActionData, useNavigation } from "@remix-run/react";
import { authenticate } from "../shopify.server";

export const action = async ({ request }: ActionFunctionArgs) => {
  const { session } = await authenticate.admin(request);
  const formData = await request.formData();
  
  const intent = formData.get("intent");
  
  if (intent === "updateSettings") {
    const enabled = formData.get("enabled") === "true";
    const message = formData.get("message") as string;
    
    await db.appSettings.upsert({
      where: { shop: session.shop },
      create: { shop: session.shop, enabled, message },
      update: { enabled, message }
    });
    
    return json({ success: true });
  }
  
  return json({ error: "Unknown action" }, { status: 400 });
};

export default function Settings() {
  const actionData = useActionData<typeof action>();
  const navigation = useNavigation();
  const isSubmitting = navigation.state === "submitting";
  
  return (
    <Form method="post">
      <input type="hidden" name="intent" value="updateSettings" />
      {/* Form fields */}
      <Button submit loading={isSubmitting}>
        Save
      </Button>
    </Form>
  );
}
```

## Client-Side Fetching with useFetcher

For operations that shouldn't cause navigation (inline updates, toggles, etc.):

```typescript
import { useFetcher } from "@remix-run/react";

function CampaignRow({ campaign }) {
  const fetcher = useFetcher();
  const isUpdating = fetcher.state !== "idle";
  
  const toggleStatus = () => {
    fetcher.submit(
      { 
        intent: "toggleStatus",
        campaignId: campaign.id,
        enabled: String(!campaign.enabled)
      },
      { method: "post", action: "/app/campaigns" }
    );
  };
  
  return (
    <ResourceItem id={campaign.id}>
      <Text>{campaign.name}</Text>
      <Button 
        onClick={toggleStatus} 
        loading={isUpdating}
      >
        {campaign.enabled ? "Disable" : "Enable"}
      </Button>
    </ResourceItem>
  );
}
```

## API Routes for Extensions/External Services

### Authenticated API Endpoint

```typescript
// app/routes/api.widget-config.tsx
import { json, type LoaderFunctionArgs } from "@remix-run/node";
import { authenticate } from "../shopify.server";

export const loader = async ({ request }: LoaderFunctionArgs) => {
  // For app proxy requests or authenticated API calls
  const { session } = await authenticate.admin(request);
  
  const config = await db.widgetConfig.findUnique({
    where: { shop: session.shop }
  });
  
  return json(config);
};

export const action = async ({ request }: ActionFunctionArgs) => {
  const { session } = await authenticate.admin(request);
  const body = await request.json();
  
  // Whitelist allowed fields - never pass raw body to database
  const { theme, position, welcomeMessage } = body;
  
  const updated = await db.widgetConfig.update({
    where: { shop: session.shop },
    data: { theme, position, welcomeMessage }
  });
  
  return json(updated);
};
```

### Public API (Webhooks, Callbacks)

```typescript
// app/routes/webhooks.tsx
import { type ActionFunctionArgs } from "@remix-run/node";
import { authenticate } from "../shopify.server";

export const action = async ({ request }: ActionFunctionArgs) => {
  const { topic, shop, payload } = await authenticate.webhook(request);
  
  switch (topic) {
    case "ORDERS_CREATE":
      await handleOrderCreated(shop, payload);
      break;
    case "APP_UNINSTALLED":
      await handleAppUninstalled(shop);
      break;
  }
  
  return new Response();
};
```

## Session Handling

### Getting Session in Any Route

```typescript
// Session is available after authenticate.admin()
const { session, admin } = await authenticate.admin(request);

// session contains:
// - session.shop: "store.myshopify.com"
// - session.accessToken: OAuth token
// - session.scope: granted scopes
```

### Checking Scopes

```typescript
export const loader = async ({ request }: LoaderFunctionArgs) => {
  const { session } = await authenticate.admin(request);
  
  const hasOrdersScope = session.scope?.includes("read_orders");
  
  if (!hasOrdersScope) {
    // Redirect to re-auth or show error
    throw new Response("Missing required scope", { status: 403 });
  }
  
  // Continue...
};
```

## File Structure Convention

```
app/
├── routes/
│   ├── app._index.tsx          # /app (dashboard)
│   ├── app.settings.tsx        # /app/settings
│   ├── app.campaigns._index.tsx # /app/campaigns (list)
│   ├── app.campaigns.$id.tsx   # /app/campaigns/:id (detail)
│   ├── app.campaigns.new.tsx   # /app/campaigns/new (create)
│   ├── api.widget-config.tsx   # /api/widget-config
│   └── webhooks.tsx            # /webhooks
├── components/
│   └── ...
├── shopify.server.ts           # Shopify app config
└── db.server.ts                # Prisma client
```

## Best Practices

1. **Always authenticate** - Use `authenticate.admin(request)` for all app routes
2. **Validate ownership** - When fetching by ID, always filter by `session.shop`
3. **Use actions for mutations** - Don't mutate in loaders
4. **Handle loading states** - Use `navigation.state` or `fetcher.state`
5. **Return proper HTTP codes** - 404 for not found, 400 for bad requests
6. **Type your data** - Use `useLoaderData<typeof loader>()` for type safety
7. **Validate and sanitize input** - Never trust user input; validate format and whitelist allowed fields
8. **Avoid mass assignment** - Never pass raw request body directly to database; explicitly select allowed fields

## References

- [Remix Data Loading](https://remix.run/docs/en/main/guides/data-loading)
- [Remix Data Mutations](https://remix.run/docs/en/main/guides/data-writes)
- [@shopify/shopify-app-remix Authentication](https://shopify.dev/docs/api/shopify-app-remix/authenticate)
- [Shopify App Proxy](https://shopify.dev/docs/apps/online-store/app-proxies)
