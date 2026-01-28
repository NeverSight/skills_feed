---
name: authentication
description: Complete authentication system with Better Auth, email verification, password reset, protected routes, and account management.
---

# Authentication

Complete authentication system with Better Auth, email verification, password reset, protected routes, and account management.

## Prerequisites

Complete these recipes first (in order):

### Type-Safe Environment Configuration

Type-safe environment variable validation using Zod with a Drizzle-like schema API. Supports server/public fields, feature flags, either-or constraints, and client-side protection.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/config-schema-setup
```

### Neon + Drizzle Setup

Connect a Next.js app to Neon Postgres using Drizzle ORM with optimized connection pooling for Vercel serverless functions.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/neon-drizzle-setup
```

### Next.js on Vercel

Create a Next.js app running on Bun, configure the development environment, and deploy to Vercel with automatic deployments on push.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/nextjs-on-vercel
```

### Shadcn UI & Theming

Add Shadcn UI components with dark mode support using next-themes. Includes theme provider and CSS variables configuration.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/shadcn-ui-setup
```

## Cookbook - Complete These Recipes in Order

### Resend Setup

Configure Resend for transactional emails like password resets and email verification.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/resend-setup
```

### Better Auth Setup

Add user authentication using Better Auth with Drizzle ORM and Neon Postgres. Base setup with email/password authentication.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/better-auth-setup
```

### Better Auth Emails

Add email verification, password reset, and account management emails to Better Auth using Resend.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/better-auth-emails
```

### Better Auth Components

Add UI components and pages for authentication flows including sign in, sign up, forgot password, reset password, and email verification.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/better-auth-components
```

### Better Auth Profile & Account

Add a complete account settings page with profile editing, password changes, email updates, session management, and account deletion.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/better-auth-profile
```

### Better Auth Protected Routes

Add server-side route protection to enforce authentication on specific pages while keeping others public.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/better-auth-protected-routes
```

### Working with Authentication

Use Better Auth for client and server-side authentication. Covers session access, protected routes, sign in/out, and fetching user data.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/using-authentication
```
