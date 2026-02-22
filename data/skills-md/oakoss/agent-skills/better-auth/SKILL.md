---
name: better-auth
description: |
  Self-hosted TypeScript auth framework with social auth, 2FA, passkeys, organizations, RBAC, and 15+ plugins. Supports Drizzle/Prisma/Kysely adapters. Self-hosted alternative to Clerk/Auth.js.

  Use when: configuring auth, adding plugins, social OAuth, multi-tenant SaaS, organizations with teams and RBAC, two-factor authentication (TOTP/OTP/backup codes), email verification, password reset flows, session management, rate limiting, CSRF and cookie security, Expo/mobile, D1 adapter errors, TanStack Start integration, additionalFields bugs, admin plugin, migrating from NextAuth, migrating from Clerk, migrating from Supabase Auth, or troubleshooting auth issues.
license: MIT
metadata:
  author: oakoss
  version: '1.2'
---

# better-auth

**Package**: better-auth@1.4.15 (ESM-only since v1.4.0)
**Docs**: <https://better-auth.com/docs> | **GitHub**: <https://github.com/better-auth/better-auth>

## Environment Setup

| Variable             | Purpose                                                               |
| -------------------- | --------------------------------------------------------------------- |
| `BETTER_AUTH_SECRET` | Encryption secret (min 32 chars). Generate: `openssl rand -base64 32` |
| `BETTER_AUTH_URL`    | Base URL (e.g., `https://example.com`)                                |

Only define `baseURL`/`secret` in config if env vars are NOT set. CLI looks for `auth.ts` in: `./`, `./lib`, `./utils`, or `./src`.

## Core Config Options

| Option             | Notes                                         |
| ------------------ | --------------------------------------------- |
| `appName`          | Optional display name                         |
| `baseURL`          | Only if `BETTER_AUTH_URL` not set             |
| `basePath`         | Default `/api/auth`. Set `/` for root.        |
| `secret`           | Only if `BETTER_AUTH_SECRET` not set          |
| `database`         | Required unless using stateless mode (v1.4+)  |
| `secondaryStorage` | Redis/KV for sessions and rate limits         |
| `emailAndPassword` | `{ enabled: true }` to activate               |
| `socialProviders`  | `{ google: { clientId, clientSecret }, ... }` |
| `plugins`          | Array of plugins                              |
| `trustedOrigins`   | CSRF whitelist                                |

## Plugin Reference

| Plugin        | Description                                                                        |
| ------------- | ---------------------------------------------------------------------------------- |
| twoFactor     | TOTP, email OTP, backup codes                                                      |
| organization  | Multi-tenant orgs, teams, invitations, RBAC                                        |
| admin         | User management, impersonation, banning                                            |
| passkey       | WebAuthn passwordless login                                                        |
| magicLink     | Email-based passwordless login                                                     |
| jwt           | JWT tokens with key rotation, JWKS                                                 |
| oauthProvider | Build your own OAuth 2.1 provider (separate `@better-auth/oauth-provider` package) |
| sso           | Enterprise SSO with OIDC, OAuth2, SAML 2.0 (separate `@better-auth/sso` package)   |
| scim          | Enterprise user provisioning (separate `@better-auth/scim` package)                |
| stripe        | Payment and subscription management                                                |
| bearer        | API token auth for mobile/CLI                                                      |
| apiKey        | Token-based auth with rate limits                                                  |
| oneTap        | Google One Tap frictionless sign-in                                                |
| anonymous     | Guest user access without PII                                                      |
| genericOAuth  | Custom OAuth providers with PKCE                                                   |
| emailOTP      | Email-based one-time password auth                                                 |
| phoneNumber   | Phone/SMS-based OTP sign-in                                                        |
| username      | Username-based sign-in (alternative to email)                                      |
| multiSession  | Multiple accounts in same browser                                                  |
| openAPI       | Interactive API docs at `/api/auth/reference`                                      |

## Session Strategies

| Strategy          | Format                  | Use Case          |
| ----------------- | ----------------------- | ----------------- |
| Compact (default) | Base64url + HMAC-SHA256 | Smallest, fastest |
| JWT               | Standard JWT            | Interoperable     |
| JWE               | A256CBC-HS512 encrypted | Most secure       |

## Getting Started

For new projects or first-time Better Auth setup, use the official interactive setup skill:

```bash
npx skills add better-auth/skills -s create-auth-skill
```

This walks through framework detection, database selection, auth method choices, plugin setup, and generates the initial configuration.

## Anti-Patterns

| Anti-Pattern                             | Correct Approach                                                               |
| ---------------------------------------- | ------------------------------------------------------------------------------ |
| Using `d1Adapter`                        | Use Drizzle or Kysely adapter with `provider: "sqlite"`                        |
| Using table name in config               | Use ORM model name, not DB table name                                          |
| Forgetting CLI after plugin changes      | Re-run `npx @better-auth/cli@latest generate`                                  |
| `tanstackStartCookies()` not last plugin | Must be the last plugin in array (TanStack Start)                              |
| Checking `session` for login state       | Check `session?.user` — session object is always truthy                        |
| Missing `nodejs_compat` flag             | Required in `wrangler.toml` for Cloudflare Workers                             |
| Kysely CamelCasePlugin with auth         | Use separate Kysely instance without the plugin                                |
| Using old `reactStartCookies` import     | Renamed to `tanstackStartCookies` from `better-auth/tanstack-start` in v1.4.14 |

## Common Mistakes

| Mistake                                                                | Correct Pattern                                                                                |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Setting `baseURL` and `secret` in config when env vars are already set | Only define these in config if `BETTER_AUTH_URL` and `BETTER_AUTH_SECRET` env vars are NOT set |
| Using CommonJS require syntax with better-auth v1.4+                   | better-auth is ESM-only since v1.4.0; use `import` syntax exclusively                          |
| Not re-running CLI generate after adding or changing plugins           | Always run `npx @better-auth/cli@latest generate` after plugin changes to update DB schema     |
| Checking `session` object truthy state for login detection             | Check `session?.user` instead; the session object itself is always truthy                      |
| Using `d1Adapter` directly for Cloudflare D1                           | Use Drizzle or Kysely adapter with `provider: "sqlite"` for D1 compatibility                   |

## Breaking Changes

| Version | Change                                                                                           |
| ------- | ------------------------------------------------------------------------------------------------ |
| v1.4.14 | `reactStartCookies` renamed to `tanstackStartCookies` (import from `better-auth/tanstack-start`) |
| v1.4.6  | `allowImpersonatingAdmins` defaults to `false`                                                   |
| v1.4.0  | ESM-only (no CommonJS); SSO, SCIM, OAuth Provider moved to separate packages                     |
| v1.3.0  | Multi-team table structure: new `teamMembers` table needed                                       |

## Delegation

When working on auth, delegate to:

- `application-security` — Security architecture and threat modeling
- `database` — Drizzle ORM schema and migrations
- `tanstack-start` — TanStack Start integration patterns

## Resources

- **Docs**: <https://better-auth.com/docs>
- **Options Reference**: <https://better-auth.com/docs/reference/options>
- **LLMs.txt**: <https://better-auth.com/llms.txt>
- **Changelog**: <https://www.better-auth.com/changelogs>
- **TanStack Start**: <https://www.better-auth.com/docs/integrations/tanstack>
- **Expo**: <https://www.better-auth.com/docs/integrations/expo>

## References

- [Database Adapters](references/database-adapters.md) — Drizzle, Kysely, Prisma adapters, Cloudflare Workers factory pattern
- [Session Management](references/sessions.md) — Cookie cache, stateless sessions, storage priority, freshAge constraints
- [Plugins and Social Auth](references/plugins.md) — Plugin setup, OAuth 2.1 provider, admin RBAC, social provider scopes
- [Email and Password](references/email-password.md) — Verification, password reset, timing attack prevention, hashing (scrypt, argon2), token security
- [Two-Factor Authentication](references/two-factor.md) — TOTP, email/SMS OTP, backup codes, trusted devices, 2FA session flow
- [Organizations](references/organizations.md) — Multi-tenant orgs, teams, invitations, RBAC, dynamic access control, lifecycle hooks
- [Configuration](references/configuration.md) — User/account config, rate limiting, hooks, CSRF, trusted origins, cookie/OAuth security, production checklist
- [Framework Integration](references/frameworks.md) — TanStack Start setup, Expo/React Native, client imports, type safety
- [Migration Guides](references/migration-guides.md) — Migrate from NextAuth/Auth.js, Clerk, or Supabase Auth with schema mappings and session strategies
- [Troubleshooting](references/troubleshooting.md) — D1 consistency, CORS, OAuth redirect, admin 403, nanostore refresh, known bugs
