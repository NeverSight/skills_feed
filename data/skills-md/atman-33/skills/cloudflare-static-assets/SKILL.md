---
name: cloudflare-static-assets
description: Configure and use Cloudflare Static Assets with React Router, ensuring compatibility across development and production environments with automatic fallback handling. Use when deploying React Router applications to Cloudflare Workers that need to access files from the public directory.
---

# Cloudflare Static Assets

## Overview

This skill provides a robust solution for handling static assets in React Router applications deployed to Cloudflare Workers. It addresses the common issue where files in the `public` directory work in development (Vite) but fail with 404 errors in production due to differences in how assets are served.

## Problem Context

**Development vs Production Mismatch:**
- **Development (Vite)**: Files in `public/` are automatically served at the root path
- **Production (Cloudflare Workers)**: Static files need to be configured separately as Static Assets

This causes code like `fetch('/data/config.json')` to work locally but fail with 404 in production.

## Solution: Configuration + Utility Functions

### Step 1: Configure `wrangler.jsonc`

Enable Static Assets by adding the `assets` configuration:

```jsonc
{
  "compatibility_date": "2024-11-18",
  "assets": {
    "directory": "./public",
    "binding": "ASSETS"
  }
}
```

### Step 2: Create Utility Functions

Create `app/lib/utils/static-assets.ts` (or similar path) with the following implementation:

```typescript
/**
 * Static Assets Utility
 * 
 * Provides unified access to static files across different environments:
 * - Development (Vite): Uses standard fetch()
 * - Production (Cloudflare Workers): Uses ASSETS binding
 * - Build time (Node.js): Falls back to file system access
 */

interface CloudflareContext {
  cloudflare?: {
    env: Env;
  };
}

/**
 * Determines if we have access to Cloudflare Workers ASSETS binding
 */
function hasAssetsBinding(context?: CloudflareContext): boolean {
  return !!context?.cloudflare?.env?.ASSETS;
}

/**
 * Fetches a static asset with automatic fallback between ASSETS and standard fetch
 */
export async function fetchStaticAsset(
  path: string,
  context?: CloudflareContext,
  request?: Request,
): Promise<Response> {
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;

  // Try Static Assets first if available
  if (hasAssetsBinding(context) && context?.cloudflare?.env?.ASSETS) {
    try {
      const assetUrl = new URL(normalizedPath, "https://example.com");
      const assetRequest = new Request(assetUrl.toString());
      const response = await context.cloudflare.env.ASSETS.fetch(assetRequest);

      if (response.ok) return response;

      // Log fallback only in development
      if (typeof process !== "undefined" && process.env.NODE_ENV === "development") {
        console.warn(
          `[Static Assets] Failed for ${normalizedPath} (${response.status}), using fallback`
        );
      }
    } catch (error) {
      // Log errors only in development
      if (typeof process !== "undefined" && process.env.NODE_ENV === "development") {
        console.warn(`[Static Assets] Error for ${normalizedPath}:`, error);
      }
    }
  }

  // Fallback: Use standard fetch
  let url = normalizedPath;
  if (request) {
    const requestUrl = new URL(request.url);
    url = `${requestUrl.origin}${normalizedPath}`;
  }

  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(
      `Static asset not found: ${normalizedPath} (${response.status})`
    );
  }

  return response;
}

/**
 * Fetches and parses a JSON static asset
 */
export async function fetchStaticJSON<T>(
  path: string,
  context?: CloudflareContext,
  request?: Request,
): Promise<T> {
  try {
    const response = await fetchStaticAsset(path, context, request);
    const json = await response.json();
    return json as T;
  } catch (error) {
    // Log detailed errors only in development
    if (typeof process !== "undefined" && process.env.NODE_ENV === "development") {
      console.error(`Failed to fetch static JSON ${path}:`, error);
    }
    throw new Error(`Failed to load JSON asset: ${path}`);
  }
}

/**
 * Fetches a text static asset
 */
export async function fetchStaticText(
  path: string,
  context?: CloudflareContext,
  request?: Request,
): Promise<string> {
  try {
    const response = await fetchStaticAsset(path, context, request);
    const text = await response.text();
    return text;
  } catch (error) {
    // Log detailed errors only in development
    if (typeof process !== "undefined" && process.env.NODE_ENV === "development") {
      console.error(`Failed to fetch static text ${path}:`, error);
    }
    throw new Error(`Failed to load text asset: ${path}`);
  }
}
```

## Usage Examples

### In React Router Loaders

```typescript
import type { Route } from './+types/route';
import { fetchStaticJSON } from '~/lib/utils/static-assets';

interface AppConfig {
  apiUrl: string;
  features: string[];
}

export async function loader({ request, context }: Route.LoaderArgs) {
  // Same code works in all environments
  const config = await fetchStaticJSON<AppConfig>(
    '/data/config.json',
    context,
    request
  );

  return { config };
}

export default function ConfigPage({ loaderData }: Route.ComponentProps) {
  const { config } = loaderData;
  
  return (
    <div>
      <h1>App Configuration</h1>
      <p>API URL: {config.apiUrl}</p>
      <ul>
        {config.features.map(feature => (
          <li key={feature}>{feature}</li>
        ))}
      </ul>
    </div>
  );
}
```

### Fetching Text Files

```typescript
import { fetchStaticText } from '~/lib/utils/static-assets';

export async function loader({ request, context }: Route.LoaderArgs) {
  const markdown = await fetchStaticText(
    '/content/about.md',
    context,
    request
  );

  return { markdown };
}
```

## Benefits

1. **Environment-Agnostic**: Same code works in development and production
2. **Automatic Fallback**: Gracefully handles missing ASSETS binding
3. **Type Safety**: TypeScript support for JSON parsing
4. **Proper Error Handling**: Detailed logs in development, clean errors in production
5. **Performance**: Uses Cloudflare edge for fast delivery in production

## Important Considerations

### Security
- Ensure sensitive files are not in the `public` directory
- Static assets are publicly accessible

### File Organization
```
project/
├── public/
│   ├── data/
│   │   └── config.json
│   ├── content/
│   │   └── about.md
│   └── images/
│       └── logo.png
├── app/
│   └── lib/
│       └── utils/
│           └── static-assets.ts
└── wrangler.jsonc
```

## References

- [Cloudflare Workers Static Assets Documentation](https://developers.cloudflare.com/workers/static-assets/)
- [React Router Official Documentation](https://reactrouter.com/)
- [Vite Static Asset Handling](https://vitejs.dev/guide/assets.html)
