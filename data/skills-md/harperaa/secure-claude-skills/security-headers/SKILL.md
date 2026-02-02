---
name: security-headers
description: Configure security headers to defend against clickjacking, XSS, MIME confusion, and SSL stripping attacks. Use this skill when you need to set up Content-Security-Policy, X-Frame-Options, HSTS, configure middleware headers, or understand browser security features. Triggers include "security headers", "CSP", "content security policy", "X-Frame-Options", "HSTS", "clickjacking", "MIME confusion", "middleware headers".
---

# Security Headers - Defense Against Multiple Attack Types

## Why Security Headers Are Critical

Think of security headers as the walls and moat around your castle. Even if attackers get past the gate (your authentication), the walls (headers) prevent them from moving freely or exfiltrating data.

### The Browser Security Model

Modern browsers have built-in security features, but **they're opt-in**. Without the right headers, browsers allow:
- Your site to be embedded in malicious iframes (clickjacking)
- Scripts from any origin (XSS amplification)
- Insecure HTTP connections (man-in-the-middle attacks)
- MIME type confusion (executing images as scripts)

**Security headers tell the browser: "Enable all your security features for my site."**

### Real-World Consequences of Missing Headers

According to a 2023 security audit of top 10,000 websites by Scott Helme, only **2.8% properly implement all recommended security headers**. The remaining 97.2% are vulnerable to attacks that headers would prevent.

**Magecart Attacks (2018-2020):**
Hundreds of e-commerce sites were compromised by injected payment-stealing JavaScript. **Content-Security-Policy headers would have prevented these scripts from executing**. Sites without CSP lost millions in fraudulent transactions.

## Our Security Headers Architecture

All headers are applied automatically via `middleware.ts` on every request. You don't need to manually set them—they're already protecting you.

### Headers We Apply

1. **Content-Security-Policy (CSP)** - Controls resource loading
2. **X-Frame-Options: DENY** - Prevents clickjacking
3. **X-Content-Type-Options: nosniff** - Prevents MIME confusion
4. **Strict-Transport-Security (HSTS)** - Forces HTTPS (production only)
5. **X-Robots-Tag: noindex, nofollow** - Protects private routes

## Header Descriptions & Implementation

### 1. Content-Security-Policy (CSP)

**What it does:** Controls what resources (scripts, styles, images) can load and from where.

**Our configuration:**
```typescript
// Dynamic CSP based on environment variables
const clerkDomain = process.env.NEXT_PUBLIC_CLERK_FRONTEND_API_URL
  ? new URL(process.env.NEXT_PUBLIC_CLERK_FRONTEND_API_URL).origin
  : '';

const convexDomain = process.env.NEXT_PUBLIC_CONVEX_URL
  ? new URL(process.env.NEXT_PUBLIC_CONVEX_URL).origin
  : '';

const csp = [
  "default-src 'self'",
  `script-src 'self' 'unsafe-inline' 'unsafe-eval' ${clerkDomain} https://js.stripe.com`,
  `style-src 'self' 'unsafe-inline' ${clerkDomain}`,
  `connect-src 'self' ${clerkDomain} ${convexDomain} https://api.stripe.com`,
  `frame-src 'self' ${clerkDomain} https://js.stripe.com https://hooks.stripe.com`,
  "img-src 'self' data: https: blob:",
  "font-src 'self' data:",
  "object-src 'none'",
  "base-uri 'self'",
  "form-action 'self'",
  "frame-ancestors 'none'"
].join('; ');

response.headers.set('Content-Security-Policy', csp);
```

**What This Means:**
- **Scripts:** Only from our domain, Clerk, and Stripe
- **Styles:** Only from our domain and Clerk
- **Connections:** Only to Clerk, Convex, Stripe APIs
- **Frames:** Only Clerk and Stripe
- **Images:** Any HTTPS source (for user avatars, external images)

**Why Dynamic Configuration:**
```typescript
const clerkDomain = process.env.NEXT_PUBLIC_CLERK_FRONTEND_API_URL
  ? new URL(process.env.NEXT_PUBLIC_CLERK_FRONTEND_API_URL).origin
  : ''
```

We don't hardcode Clerk's domain. It comes from environment variables. This means:
- ✅ Different domains for dev/staging/prod (automatic)
- ✅ Easy to change without code modifications
- ✅ No security secrets in codebase

**Trade-off:** We allow `unsafe-inline` and `unsafe-eval` for scripts. This is **required for Next.js and Clerk to function**. We mitigate this risk through input sanitization and validation.

**Prevent Data Exfiltration:**
The `connect-src` directive prevents malicious scripts from sending data to unauthorized domains. Even if XSS bypasses sanitization, the browser blocks unauthorized network requests.

### 2. X-Frame-Options: DENY

**What it prevents:** Clickjacking attacks where your site is embedded in invisible iframe on attacker's site.

**Attack scenario:**
Attacker embeds your "Delete Account" button in an invisible iframe overlay on a game site. Users think they're clicking "Play Game" but actually click "Delete Account."

**Our protection:**
```typescript
response.headers.set('X-Frame-Options', 'DENY');
```

DENY means browsers refuse to embed our site in **ANY** iframe, even our own. Maximum security.

**Alternative values:**
- `DENY` - No iframes at all (most secure, what we use)
- `SAMEORIGIN` - Only our own site can iframe us
- `ALLOW-FROM uri` - Deprecated, don't use

### 3. X-Content-Type-Options: nosniff

**What it prevents:** MIME confusion attacks where browsers execute images as JavaScript.

**Attack scenario:**
Attacker uploads file "avatar.jpg" that contains JavaScript. Old browsers try to be "helpful" and "sniff" the file type, detecting JavaScript, and execute it.

**Our protection:**
```typescript
response.headers.set('X-Content-Type-Options', 'nosniff');
```

`nosniff` tells browsers to **strictly follow Content-Type headers, never guess**.

**Why This Matters:**
Without this header, an attacker could:
1. Upload "image.jpg" containing `<script>evil()</script>`
2. Link to it: `<img src="/uploads/image.jpg">`
3. Browser sniffs file, detects script, executes it
4. XSS achieved despite upload validation

With `nosniff`, browser sees Content-Type: image/jpeg and **refuses to execute** as script.

### 4. Strict-Transport-Security (HSTS) - Production Only

**What it prevents:** SSL stripping attacks where man-in-the-middle downgrades HTTPS to HTTP.

**Attack scenario:**
User types "yourapp.com" (no https://). Browser initially requests HTTP. Attacker intercepts, serves fake HTTP version, steals credentials.

**Our protection:**
```typescript
if (process.env.NODE_ENV === 'production') {
  response.headers.set(
    'Strict-Transport-Security',
    'max-age=31536000; includeSubDomains'
  );
}
```

**Configuration breakdown:**
- `max-age=31536000` - 1 year duration
- `includeSubDomains` - Applies to all subdomains
- Once set, browsers **ONLY use HTTPS** for your domain

**Why production only:**
In development, you're on localhost (HTTP). HSTS would break local development. Our middleware detects environment and enables HSTS only in production.

**Important:** Once HSTS is set for a domain, browsers remember it. If you need to remove it, you must:
1. Set `max-age=0`
2. Wait for all users' browsers to receive the new header
3. This can take months if max-age was long

### 5. X-Robots-Tag: noindex, nofollow (Protected Routes)

**What it prevents:** Search engines indexing private content.

**Why it matters:**
You don't want `/dashboard/payment-details` showing up in Google search results.

**Our implementation:**
```typescript
if (req.nextUrl.pathname.startsWith('/dashboard')) {
  response.headers.set('X-Robots-Tag', 'noindex, nofollow');
}
```

**Applied to:** `/dashboard/*` routes only (public pages should be indexed)

**What this tells search engines:**
- `noindex` - Don't add this page to search results
- `nofollow` - Don't follow links on this page

## Implementation in Middleware

### middleware.ts Pattern

```typescript
import { clerkMiddleware } from '@clerk/nextjs/server';
import { NextResponse } from 'next/server';

export default clerkMiddleware((auth, req) => {
  const response = NextResponse.next();

  // Get dynamic domains from environment
  const clerkDomain = process.env.NEXT_PUBLIC_CLERK_FRONTEND_API_URL
    ? new URL(process.env.NEXT_PUBLIC_CLERK_FRONTEND_API_URL).origin
    : '';

  const convexDomain = process.env.NEXT_PUBLIC_CONVEX_URL
    ? new URL(process.env.NEXT_PUBLIC_CONVEX_URL).origin
    : '';

  // Build CSP dynamically
  const csp = [
    "default-src 'self'",
    `script-src 'self' 'unsafe-inline' 'unsafe-eval' ${clerkDomain} https://js.stripe.com`,
    `style-src 'self' 'unsafe-inline' ${clerkDomain}`,
    `connect-src 'self' ${clerkDomain} ${convexDomain} https://api.stripe.com`,
    `frame-src 'self' ${clerkDomain} https://js.stripe.com https://hooks.stripe.com`,
    "img-src 'self' data: https: blob:",
    "font-src 'self' data:",
    "object-src 'none'",
    "base-uri 'self'",
    "form-action 'self'",
    "frame-ancestors 'none'"
  ].join('; ');

  // Apply security headers
  response.headers.set('Content-Security-Policy', csp);
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('X-Frame-Options', 'DENY');

  // HSTS only in production
  if (process.env.NODE_ENV === 'production') {
    response.headers.set(
      'Strict-Transport-Security',
      'max-age=31536000; includeSubDomains'
    );
  }

  // Prevent indexing of protected routes
  if (req.nextUrl.pathname.startsWith('/dashboard')) {
    response.headers.set('X-Robots-Tag', 'noindex, nofollow');
  }

  return response;
});

export const config = {
  matcher: ['/((?!.*\\..*|_next).*)', '/', '/(api|trpc)(.*)'],
};
```

## Testing Security Headers

### Test All Headers

```bash
curl -I http://localhost:3000

# Expected headers:
# X-Frame-Options: DENY
# X-Content-Type-Options: nosniff
# Content-Security-Policy: default-src 'self'; ...
```

### Test Production HSTS

```bash
# In production
curl -I https://yourapp.com

# Should include:
# Strict-Transport-Security: max-age=31536000; includeSubDomains
```

### Test Protected Route Headers

```bash
curl -I http://localhost:3000/dashboard

# Should include:
# X-Robots-Tag: noindex, nofollow
```

### Online Header Testing

Use these online tools to test your deployed site:
- **Security Headers:** https://securityheaders.com/
- **Mozilla Observatory:** https://observatory.mozilla.org/
- **SSL Labs:** https://www.ssllabs.com/ssltest/

## Customizing CSP for New Integrations

When adding new third-party services:

### Example: Adding Google Analytics

```typescript
// middleware.ts

// Add Google Analytics domain to CSP
const csp = [
  "default-src 'self'",
  `script-src 'self' 'unsafe-inline' 'unsafe-eval' ${clerkDomain} https://js.stripe.com https://www.googletagmanager.com https://www.google-analytics.com`,
  `style-src 'self' 'unsafe-inline' ${clerkDomain}`,
  `connect-src 'self' ${clerkDomain} ${convexDomain} https://api.stripe.com https://www.google-analytics.com https://analytics.google.com`,
  // ... rest of CSP
].join('; ');
```

### Example: Adding Custom CDN

```typescript
const cdnDomain = process.env.NEXT_PUBLIC_CDN_URL
  ? new URL(process.env.NEXT_PUBLIC_CDN_URL).origin
  : '';

const csp = [
  "default-src 'self'",
  `script-src 'self' ${cdnDomain}`,
  `style-src 'self' ${cdnDomain}`,
  `img-src 'self' ${cdnDomain} https:`,
  // ... rest of CSP
].join('; ');
```

## Common CSP Issues & Solutions

### Issue 1: Inline Scripts Blocked

**Symptom:** Scripts in `<script>` tags don't execute

**Solution:** Next.js requires `unsafe-inline` and `unsafe-eval`. Already configured in our CSP.

**Better alternative:** Use nonces (requires SSR changes):
```typescript
const nonce = crypto.randomBytes(16).toString('base64');
script-src 'self' 'nonce-${nonce}'
```

### Issue 2: External Images Not Loading

**Symptom:** User avatars from Gravatar/etc don't show

**Current solution:** `img-src 'self' data: https: blob:` allows all HTTPS images

**Stricter alternative:**
```typescript
`img-src 'self' data: https://gravatar.com https://images.yourapp.com`
```

### Issue 3: WebSocket Connections Failing

**Symptom:** Convex real-time updates don't work

**Solution:** Ensure `connect-src` includes Convex domain:
```typescript
`connect-src 'self' ${convexDomain}`
```

## What Security Headers Prevent

✅ **Clickjacking** (X-Frame-Options)
✅ **XSS amplification** (CSP)
✅ **MIME confusion** (X-Content-Type-Options)
✅ **SSL stripping** (HSTS)
✅ **Search engine exposure of private data** (X-Robots-Tag)
✅ **Data exfiltration** (CSP connect-src)
✅ **Unauthorized resource loading** (CSP default-src)

## Common Mistakes to Avoid

❌ **DON'T hardcode domains in CSP** - Use environment variables
❌ **DON'T enable HSTS in development** - Breaks localhost
❌ **DON'T use X-Frame-Options: ALLOW-FROM** - Deprecated
❌ **DON'T forget to test headers after deployment**
❌ **DON'T set overly permissive CSP** (like `*` wildcards)

✅ **DO use dynamic CSP with environment variables**
✅ **DO test headers with online tools after deployment**
✅ **DO update CSP when adding new third-party services**
✅ **DO keep HSTS production-only**
✅ **DO protect dashboard routes from indexing**

## References

- Mozilla Security Headers Guide: https://infosec.mozilla.org/guidelines/web_security
- OWASP Secure Headers Project: https://owasp.org/www-project-secure-headers/
- Content Security Policy: https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
- HSTS Specification: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security
- Security Headers Checker: https://securityheaders.com/

## Next Steps

- For XSS prevention: Use `input-validation` skill
- For clickjacking tests: Use `security-testing` skill
- Headers are automatic - check `middleware.ts:1` for implementation
- For adding new integrations: Update CSP in middleware.ts
