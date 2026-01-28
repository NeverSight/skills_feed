---
name: clerk-auth
description: |
  Clerk auth with API version 2025-11-10 breaking changes (billing endpoints, payment_source→payment_method), Next.js v6 async auth(), PKCE for custom OAuth, credential stuffing defense. Use when: troubleshooting "Missing Clerk Secret Key", JWKS errors, authorizedParties CSRF, JWT size limits (1.2KB), 431 header errors (Vite dev mode), or testing with 424242 OTP.
license: MIT
metadata:
  version: 2.0.0
  last_verified: 2025-11-22
  sdk_versions:
    nextjs: 6.35.4
    backend: 2.23.2
    clerk_react: 5.56.2
    testing: 1.13.18
  token_savings: ~52%
  errors_prevented: 11
  breaking_changes: Nov 2025 - API version 2025-11-10 (billing endpoints), Oct 2024 - Next.js v6 async auth()
  keywords:
    - clerk
    - clerk auth
    - api version 2025-11-10
    - billing api breaking changes
    - commerce to billing migration
    - payment_source to payment_method
    - "@clerk/nextjs"
    - "@clerk/backend"
    - "@clerk/clerk-react"
    - next.js v6 async auth
    - next.js 16 support
    - pkce custom oauth
    - credential stuffing defense
    - client trust
    - verifyToken
    - authorizedParties csrf
    - JWT template
    - JWT size limit 1.2kb
    - 431 request header too large
    - vite dev mode clerk
    - "@clerk/testing"
    - 424242 OTP
    - test credentials
    - session token script
    - "Missing Clerk Secret Key"
    - JWKS cache race condition
    - core 2 migration
---

# Clerk Auth - Breaking Changes & Error Prevention Guide

**Package Versions**: @clerk/nextjs@6.35.4, @clerk/backend@2.23.2, @clerk/clerk-react@5.56.2, @clerk/testing@1.13.18
**Breaking Changes**: Nov 2025 - API version 2025-11-10, Oct 2024 - Next.js v6 async auth()
**Last Updated**: 2025-11-22

---

## What's New in v6.35.x & API 2025-11-10 (Nov 2025)

### 1. API Version 2025-11-10 (Nov 10, 2025) - BREAKING CHANGES ⚠️

**Affects:** Applications using Clerk Billing/Commerce APIs

**Critical Changes:**
- **Endpoint URLs:** `/commerce/` → `/billing/` (30+ endpoints)
  ```
  GET /v1/commerce/plans → GET /v1/billing/plans
  GET /v1/commerce/statements → GET /v1/billing/statements
  POST /v1/me/commerce/checkouts → POST /v1/me/billing/checkouts
  ```

- **Field Terminology:** `payment_source` → `payment_method`
  ```typescript
  // OLD (deprecated)
  { payment_source_id: "...", payment_source: {...} }

  // NEW (required)
  { payment_method_id: "...", payment_method: {...} }
  ```

- **Removed Fields:** Plans responses no longer include:
  - `amount`, `amount_formatted` (use `fee.amount` instead)
  - `currency`, `currency_symbol` (use fee objects)
  - `payer_type` (use `for_payer_type`)
  - `annual_monthly_amount`, `annual_amount`

- **Removed Endpoints:**
  - Invoices endpoint (use statements)
  - Products endpoint

- **Null Handling:** Explicit rules - `null` means "doesn't exist", omitted means "not asserting existence"

**Migration:** Update SDK to v6.35.0+ which includes support for API version 2025-11-10.

**Official Guide:** https://clerk.com/docs/guides/development/upgrading/upgrade-guides/2025-11-10

### 2. Next.js v6 Async auth() (Oct 2024) - BREAKING CHANGE ⚠️

**Affects:** All Next.js Server Components using `auth()`

```typescript
// ❌ OLD (v5 - synchronous)
const { userId } = auth()

// ✅ NEW (v6 - asynchronous)
const { userId } = await auth()
```

**Also affects:** `auth.protect()` is now async in middleware

```typescript
// ❌ OLD (v5)
auth.protect()

// ✅ NEW (v6)
await auth.protect()
```

**Compatibility:** Next.js 15, 16 supported. Static rendering by default.

### 3. PKCE Support for Custom OAuth (Nov 12, 2025)

Custom OIDC providers and social connections now support PKCE (Proof Key for Code Exchange) for enhanced security in native/mobile applications where client secrets cannot be safely stored.

**Use case:** Mobile apps, native apps, public clients that can't securely store secrets.

### 4. Client Trust: Credential Stuffing Defense (Nov 14, 2025)

Automatic secondary authentication when users sign in from unrecognized devices:
- Activates for users with valid passwords but no 2FA
- No configuration required
- Included in all Clerk plans

**How it works:** Clerk automatically prompts for additional verification (email code, backup code) when detecting sign-in from new device.

### 5. Next.js 16 Support (Nov 2025)

**@clerk/nextjs v6.35.2+** includes cache invalidation improvements for Next.js 16 during sign-out.

---

## Critical Patterns & Error Prevention

### Next.js v6: Async auth() Helper

**Pattern:**
```typescript
import { auth } from '@clerk/nextjs/server'

export default async function Page() {
  const { userId } = await auth()  // ← Must await

  if (!userId) {
    return <div>Unauthorized</div>
  }

  return <div>User ID: {userId}</div>
}
```

### Cloudflare Workers: authorizedParties (CSRF Prevention)

**CRITICAL:** Always set `authorizedParties` to prevent CSRF attacks

```typescript
import { verifyToken } from '@clerk/backend'

const { data, error } = await verifyToken(token, {
  secretKey: c.env.CLERK_SECRET_KEY,
  // REQUIRED: Prevent CSRF attacks
  authorizedParties: ['https://yourdomain.com'],
})
```

**Why:** Without `authorizedParties`, attackers can use valid tokens from other domains.

**Source:** https://clerk.com/docs/reference/backend/verify-token

---

## JWT Templates - Size Limits & Shortcodes

### JWT Size Limitation: 1.2KB for Custom Claims ⚠️

**Problem**: Browser cookies limited to 4KB. Clerk's default claims consume ~2.8KB, leaving **1.2KB for custom claims**.

**⚠️ Development Note**: When testing custom JWT claims in Vite dev mode, you may encounter **"431 Request Header Fields Too Large"** error. This is caused by Clerk's handshake token in the URL exceeding Vite's 8KB limit. See [Issue #11](#issue-11-431-request-header-fields-too-large-vite-dev-mode) for solution.

**Solution:**
```json
// ✅ GOOD: Minimal claims
{
  "user_id": "{{user.id}}",
  "email": "{{user.primary_email_address}}",
  "role": "{{user.public_metadata.role}}"
}

// ❌ BAD: Exceeds limit
{
  "bio": "{{user.public_metadata.bio}}",  // 6KB field
  "all_metadata": "{{user.public_metadata}}"  // Entire object
}
```

**Best Practice**: Store large data in database, include only identifiers/roles in JWT.

### Available Shortcodes Reference

| Category | Shortcodes | Example |
|----------|-----------|---------|
| **User ID & Name** | `{{user.id}}`, `{{user.first_name}}`, `{{user.last_name}}`, `{{user.full_name}}` | `"John Doe"` |
| **Contact** | `{{user.primary_email_address}}`, `{{user.primary_phone_address}}` | `"john@example.com"` |
| **Profile** | `{{user.image_url}}`, `{{user.username}}`, `{{user.created_at}}` | `"https://..."` |
| **Verification** | `{{user.email_verified}}`, `{{user.phone_number_verified}}` | `true` |
| **Metadata** | `{{user.public_metadata}}`, `{{user.public_metadata.FIELD}}` | `{"role": "admin"}` |
| **Organization** | `org_id`, `org_slug`, `org_role` (in sessionClaims) | `"org:admin"` |

**Advanced Features:**
- **String Interpolation**: `"{{user.last_name}} {{user.first_name}}"`
- **Conditional Fallbacks**: `"{{user.public_metadata.role || 'user'}}"`
- **Nested Metadata**: `"{{user.public_metadata.profile.interests}}"`

**Official Docs**: https://clerk.com/docs/guides/sessions/jwt-templates

---

## Testing with Clerk

### Test Credentials (Fixed OTP: 424242)

**Test Emails** (no emails sent, fixed OTP):
```
john+clerk_test@example.com
jane+clerk_test@gmail.com
```

**Test Phone Numbers** (no SMS sent, fixed OTP):
```
+12015550100
+19735550133
```

**Fixed OTP Code**: `424242` (works for all test credentials)

### Generate Session Tokens (60-second lifetime)

**Script** (`scripts/generate-session-token.js`):
```bash
# Generate token
CLERK_SECRET_KEY=sk_test_... node scripts/generate-session-token.js

# Create new test user
CLERK_SECRET_KEY=sk_test_... node scripts/generate-session-token.js --create-user

# Auto-refresh token every 50 seconds
CLERK_SECRET_KEY=sk_test_... node scripts/generate-session-token.js --refresh
```

**Manual Flow**:
1. Create user: `POST /v1/users`
2. Create session: `POST /v1/sessions`
3. Generate token: `POST /v1/sessions/{session_id}/tokens`
4. Use in header: `Authorization: Bearer <token>`

### E2E Testing with Playwright

Install `@clerk/testing` for automatic Testing Token management:

```bash
npm install -D @clerk/testing
```

**Global Setup** (`global.setup.ts`):
```typescript
import { clerkSetup } from '@clerk/testing/playwright'
import { test as setup } from '@playwright/test'

setup('global setup', async ({}) => {
  await clerkSetup()
})
```

**Test File** (`auth.spec.ts`):
```typescript
import { setupClerkTestingToken } from '@clerk/testing/playwright'
import { test } from '@playwright/test'

test('sign up', async ({ page }) => {
  await setupClerkTestingToken({ page })

  await page.goto('/sign-up')
  await page.fill('input[name="emailAddress"]', 'test+clerk_test@example.com')
  await page.fill('input[name="password"]', 'TestPassword123!')
  await page.click('button[type="submit"]')

  // Verify with fixed OTP
  await page.fill('input[name="code"]', '424242')
  await page.click('button[type="submit"]')

  await expect(page).toHaveURL('/dashboard')
})
```

**Official Docs**: https://clerk.com/docs/guides/development/testing/overview

---

## Known Issues Prevention

This skill prevents **11 documented issues**:

### Issue #1: Missing Clerk Secret Key
**Error**: "Missing Clerk Secret Key or API Key"
**Source**: https://stackoverflow.com/questions/77620604
**Prevention**: Always set in `.env.local` or via `wrangler secret put`

### Issue #2: API Key → Secret Key Migration
**Error**: "apiKey is deprecated, use secretKey"
**Source**: https://clerk.com/docs/upgrade-guides/core-2/backend
**Prevention**: Replace `apiKey` with `secretKey` in all calls

### Issue #3: JWKS Cache Race Condition
**Error**: "No JWK available"
**Source**: https://github.com/clerk/javascript/blob/main/packages/backend/CHANGELOG.md
**Prevention**: Use @clerk/backend@2.17.2 or later (fixed)

### Issue #4: Missing authorizedParties (CSRF)
**Error**: No error, but CSRF vulnerability
**Source**: https://clerk.com/docs/reference/backend/verify-token
**Prevention**: Always set `authorizedParties: ['https://yourdomain.com']`

### Issue #5: Import Path Changes (Core 2)
**Error**: "Cannot find module"
**Source**: https://clerk.com/docs/upgrade-guides/core-2/backend
**Prevention**: Update import paths for Core 2

### Issue #6: JWT Size Limit Exceeded
**Error**: Token exceeds size limit
**Source**: https://clerk.com/docs/backend-requests/making/custom-session-token
**Prevention**: Keep custom claims under 1.2KB

### Issue #7: Deprecated API Version v1
**Error**: "API version v1 is deprecated"
**Source**: https://clerk.com/docs/upgrade-guides/core-2/backend
**Prevention**: Use latest SDK versions (API v2025-11-10)

### Issue #8: ClerkProvider JSX Component Error
**Error**: "cannot be used as a JSX component"
**Source**: https://stackoverflow.com/questions/79265537
**Prevention**: Ensure React 19 compatibility with @clerk/clerk-react@5.56.2+

### Issue #9: Async auth() Helper Confusion
**Error**: "auth() is not a function"
**Source**: https://clerk.com/changelog/2024-10-22-clerk-nextjs-v6
**Prevention**: Always await: `const { userId } = await auth()`

### Issue #10: Environment Variable Misconfiguration
**Error**: "Missing Publishable Key" or secret leaked
**Prevention**: Use correct prefixes (`NEXT_PUBLIC_`, `VITE_`), never commit secrets

### Issue #11: 431 Request Header Fields Too Large (Vite Dev Mode)
**Error**: "431 Request Header Fields Too Large" when signing in
**Source**: Common in Vite dev mode when testing custom JWT claims
**Cause**: Clerk's `__clerk_handshake` token in URL exceeds Vite's 8KB header limit
**Prevention**:

Add to `package.json`:
```json
{
  "scripts": {
    "dev": "NODE_OPTIONS='--max-http-header-size=32768' vite"
  }
}
```

**Temporary Workaround**: Clear browser cache, sign out, sign back in

**Why**: Clerk dev tokens are larger than production; custom JWT claims increase handshake token size

**Note**: This is different from Issue #6 (session token size). Issue #6 is about cookies (1.2KB), this is about URL parameters in dev mode (8KB → 32KB).

---

## Official Documentation

- **Clerk Docs**: https://clerk.com/docs
- **Next.js Guide**: https://clerk.com/docs/references/nextjs/overview
- **React Guide**: https://clerk.com/docs/references/react/overview
- **Backend SDK**: https://clerk.com/docs/reference/backend/overview
- **JWT Templates**: https://clerk.com/docs/guides/sessions/jwt-templates
- **API Version 2025-11-10 Upgrade**: https://clerk.com/docs/guides/development/upgrading/upgrade-guides/2025-11-10
- **Testing Guide**: https://clerk.com/docs/guides/development/testing/overview
- **Context7 Library ID**: `/clerk/clerk-docs`

---

## Package Versions

**Latest (Nov 22, 2025):**
```json
{
  "dependencies": {
    "@clerk/nextjs": "^6.35.4",
    "@clerk/clerk-react": "^5.56.2",
    "@clerk/backend": "^2.23.2",
    "@clerk/testing": "^1.13.18"
  }
}
```

---

**Token Efficiency**:
- **Without skill**: ~5,200 tokens (setup tutorials, JWT templates, testing setup)
- **With skill**: ~2,500 tokens (breaking changes + critical patterns + error prevention)
- **Savings**: ~52% (~2,700 tokens)

**Errors prevented**: 11 documented issues with exact solutions
**Key value**: API 2025-11-10 breaking changes, Next.js v6 async auth(), PKCE for custom OAuth, credential stuffing defense, JWT size limits, 431 header error workaround

---

**Last verified**: 2025-11-22 | **Skill version**: 2.0.0 | **Changes**: Added API version 2025-11-10 breaking changes (billing endpoints), PKCE support, Client Trust defense, Next.js 16 support. Removed tutorials (~480 lines). Updated SDK versions. Focused on breaking changes + error prevention + critical patterns.
