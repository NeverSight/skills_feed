---
name: next
description: Next.js framework for building React applications with App Router, Server Components, and optimized performance. Use when working with Next.js apps, routing, data fetching, caching, Server Actions, or building full-stack React applications.
metadata:
  author: Hairyf
  version: "2026.1.30"
  source: Generated from https://github.com/vercel/next.js, scripts located at https://github.com/antfu/skills
---

Next.js is a React framework for building full-stack web applications. It provides file-system based routing, Server Components, automatic code splitting, image optimization, and built-in performance optimizations. Next.js supports both static site generation (SSG) and server-side rendering (SSR), making it ideal for building modern web applications.

> The skill is based on Next.js v16.2.0-canary.16, generated at 2026-01-30.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| File-System Routing | Routes defined by folder structure, layouts, and pages | [core-routing](references/core-routing.mdx) |
| Server and Client Components | Understanding when to use Server vs Client Components | [core-server-client-components](references/core-server-client-components.mdx) |
| Navigation | Linking, prefetching, and client-side transitions | [core-navigation](references/core-navigation.mdx) |

## Data Fetching

| Topic | Description | Reference |
|-------|-------------|-----------|
| Server Components | Fetching data in Server Components with fetch, ORMs, and databases | [data-fetching-server](references/data-fetching-server.mdx) |
| Client Components | Fetching data in Client Components with use hook and third-party libraries | [data-fetching-client](references/data-fetching-client.mdx) |
| Streaming | Streaming data and components with Suspense and loading.tsx | [data-streaming](references/data-streaming.mdx) |

## Caching and Revalidation

| Topic | Description | Reference |
|-------|-------------|-----------|
| Caching Strategies | Caching fetch requests, cache tagging, and revalidation | [caching-revalidation](references/caching-revalidation.mdx) |

## Server Actions

| Topic | Description | Reference |
|-------|-------------|-----------|
| Server Functions | Creating and using Server Actions for data mutations | [server-actions](references/server-actions.mdx) |

## File Conventions

| Topic | Description | Reference |
|-------|-------------|-----------|
| Dynamic Routes | Dynamic segments, catch-all routes, and route parameters | [file-conventions-dynamic-routes](references/file-conventions-dynamic-routes.mdx) |
| Loading and Error | Handling loading states and errors with loading.tsx and error.tsx | [file-conventions-loading-error](references/file-conventions-loading-error.mdx) |

## API Reference

| Topic | Description | Reference |
|-------|-------------|-----------|
| Built-in Components | Link, Image, Script, and Font components | [api-components](references/api-components.mdx) |
