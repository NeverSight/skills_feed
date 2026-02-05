---
name: outseta
description: Outseta is an all-in-one operating system for SaaS founders, combining CRM, authentication, billing, and customer support into a single platform. It is designed to handle the "business logic" of a SaaS product so developers can focus on the "functional logic". Use when the user needs to integrate authentication, billing, or CRM features using Outseta.
---

# Outseta Synopsis

Outseta is an all-in-one operating system for SaaS founders, combining CRM, authentication, billing, and customer support into a single platform. It is designed to handle the "business logic" of a SaaS product so developers can focus on the "functional logic."

## Core Architecture

### 1. Relational Data Model (B2B First)

Outseta's CRM is structured to support team-based SaaS out of the box:

- **Person:** An individual user identified by a `Uid`.
- **Account:** A company or team entity. This is where **Subscriptions** and **Billing** reside.
- **PersonAccount:** A join entity linking People to Accounts. This allows for complex relationships where one user can be part of multiple organizations.
- **Source of Truth:** Treat Outseta as the primary source of truth for identity and payment status.

### 2. Authentication & Security

- **JWT (JSON Web Tokens):** Outseta uses JWTs for session management. These tokens contain claims like `PersonUid` and `AccountUid`.
- **Verification:** Verify tokens server-side using Outseta's **JWKS (JSON Web Key Set)**.
- **Gated Content:** Use the Outseta script to automatically show/hide UI elements based on the user's subscription plan or login status using `data-outseta-*` attributes.

### 3. Integration Patterns

#### Frontend (React)

- **AuthProvider**: Use the `AuthProvider` pattern to manage authentication state. See [`templates/react-authprovider.tsx`](templates/react-authprovider.tsx).
- **useAuth Hook**: Access user data and authentication methods via the `useAuth` hook.
- **Conditional Rendering**: Prefer React conditional rendering over `data-o-*` attributes for a more robust experience in SPA.

```tsx
const { user, logout, openLogin } = useAuth();
return (
  <>
    {!user ? (
      <Button onClick={() => openLogin()}>Login</Button>
    ) : (
      <Button onClick={() => logout()}>Logout</Button>
    )}
  </>
);
```

#### Frontend (No-Code/Low-Code)

- **Magic Script**: Include `<script src="https://cdn.outseta.com/outseta.min.js"></script>` in your head.
- **Widgets**: Trigger widgets via data attributes (e.g., `data-outseta-auth="login"`) or the `Outseta` global object.
- **Lifecycle Events**: Use `Outseta.on('event', callback)` to react to login, logout, or profile updates.
- **Gated Content**: Use the Outseta script to automatically show/hide UI elements based on the user's subscription plan or login status using `data-o-*` attributes (e.g., `data-o-anonymous="1"`, `data-o-authenticated="1"`). Note: In React apps, prefer the `AuthProvider` pattern for more reliable state management.

- **JWT Validation:** Extract the token from the `Authorization` header and validate it against Outseta's public keys.
- **Webhooks:** Use **Activity Notifications** to sync data. Common events include:
  - `Person_Added` / `Person_Updated`
  - `Account_Added` / `Account_Updated`
  - `Subscription_Created` / `Subscription_Updated`
- **Security:** Always verify webhook signatures using the SHA256 secret provided in the Outseta dashboard.

#### REST API

- Use for server-to-server communication, custom onboarding, or administrative tasks.
- Base URL: `https://your-domain.outseta.com/api/v1/`

See [REST API](references/rest-api.md)

## Key Developer Concepts

- **Uid:** The unique identifier for any entity in Outseta. Use this as the foreign key in your local database (e.g., Convex).
- **Account Stage:** Tracks where a customer is in their lifecycle (e.g., Trialing, Active, Past Due, Cancelled).
- **Embeds:** The term Outseta uses for its overlay widgets (Sign up, Login, Profile, Help Desk).

## MCP Server

The Outseta MCP Server can be used to further gain understanding of the Outseta concepts and how to use it through it's knowledge base, support examples as well as find reference documentation on the REST API.

- Knowledge_Base
- REST_API_Reference
- Examples (if you can't find an answer in the knowledge base)

## Embed Examples (pure JS/HTML only)

- **Login:** Standard login widget. See [`login.html`](templates/login.html)
- **Signup:** Registration widget with optional defaults. See [`signup.html`](templates/signup.html)
- **Profile:** User profile and subscription management. See [`profile.html`](templates/profile.html)
- **Logout:** Logout button and link patterns. See [`logout.html`](templates/logout.html)
- **Lead Capture:** Custom lead capture forms. See [`leadcapture.html`](templates/leadcapture.html)
- **Email List:** Email list subscription forms. See [`emaillist.html`](templates/emaillist.html)
- **Support:** Support ticket and knowledge base integration. See [`support.html`](templates/support.html)

## React Examples (must use with React)

- **Embed Widgets**: A collection of the embeds rendered as React Components. See [`react-widgets.tsx`](templates/react-widgets.tsx)
- **Example App**: A bare bones React app with Outseta integration. See [`react-app.tsx`](templates/react-app.tsx)
- **Auth Provider**: A React Auth Provider integrated with Outseta. See [`react-authprovider.tsx`](templates/react-authprovider.tsx)
- **Protected Route**: Protect React routes with Outseta. See [`react-protectedroute.tsx`](templates/react-protectedroute.tsx)
- **Purchase Add-on**: Trigger the purchase dialog for a specific add-on. See [`react-purchase-addon.tsx`](templates/react-purchase-addon.tsx)

## NodeJS Examples

- **Express App**: A simple Express NodeJS with Outseta webhook integration. See: [`nodejs-express.js`](templates/nodejs-express.js)
- **Verify Webhook**: Code snippet to verify the authenticity of a webhook call. See: [`nodejs-verify-webhook.js`](templates/nodejs-verify-webhook.js)
- **Track Usage**: An example how to implement usage based billing and pricing. See: [`nodejs-track-usage.md`](references/nodejs-track-usage.md) and [`nodejs-track-usage.js`](templates/nodejs-track-usage.js)
- **Verify JWT**: An example how to verify a JWT token. See: [`nodejs-verify-jwt.md`](references/nodejs-verify-jwt.md) and [`nodejs-verify-jwt.js`](templates/nodejs-verify-jwt.js)
- **Generate JWT**: Generate a User JWT token to access the API. See: [`nodejs-generate-jwt.md`](references/nodejs-generate-jwt.md) and [`nodejs-generate-jwt.js`](templates/nodejs-generate-jwt.js)
