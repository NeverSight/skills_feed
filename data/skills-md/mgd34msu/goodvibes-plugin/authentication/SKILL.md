---
name: authentication
description: "Load PROACTIVELY when task involves user identity, login, or access control. Use when user says \"add authentication\", \"set up login\", \"add OAuth\", \"protect these routes\", \"implement RBAC\", or \"add sign-up\". Covers session management, JWT tokens, OAuth2 flows, password reset, email verification, protected route middleware, role-based access control, and security hardening (CSRF, rate limiting, token rotation)."
metadata:
  version: 1.0.0
  category: outcome
  tags: [auth, login, sign-up, session, jwt, oauth, middleware, rbac]
---

## Resources
```
scripts/
  auth-checklist.sh
references/
  decision-tree.md
```

# Authentication Implementation Workflow

This skill orchestrates complete authentication implementation from discovery through testing. It replaces library-specific skills (clerk, nextauth, lucia, auth0, firebase-auth, supabase-auth, passport) with a unified workflow that adapts to your stack.

## When to Use This Skill

Use when implementing:
- User login and sign-up flows
- Session management (cookies, JWT, server-side sessions)
- OAuth integration (Google, GitHub, etc.)
- Protected routes and API endpoints
- Middleware-based authentication
- Role-based access control (RBAC)
- Token refresh mechanisms
- Password reset flows

## Prerequisites

Before starting:
1. Understand project framework (Next.js, Remix, Express, etc.)
2. Have database schema planned (if using database-backed auth)
3. Know authentication approach (managed service vs self-hosted)
4. Access to environment variable configuration

## Workflow Steps

### Step 1: Discovery

Use `discover` to understand existing authentication patterns:

```yaml
discover:
  queries:
    - id: existing-auth
      type: grep
      pattern: "(useAuth|getSession|withAuth|requireAuth|protect|authenticate)"
      glob: "**/*.{ts,tsx,js,jsx}"
    - id: middleware-files
      type: glob
      patterns:
        - "**/middleware.{ts,js}"
        - "**/auth/**/*.{ts,js}"
        - "**/_middleware.{ts,js}"
    - id: session-handling
      type: grep
      pattern: "(session|jwt|token|cookie)"
      glob: "**/*.{ts,tsx,js,jsx}"
    - id: protected-routes
      type: grep
      pattern: "(protected|private|requireAuth|withAuth)"
      glob: "**/*.{ts,tsx,js,jsx}"
  verbosity: files_only
```

**What to look for:**
- Existing auth hooks, utilities, or middleware
- Session storage mechanism (cookies, localStorage, server-side)
- Protected route patterns
- Auth provider setup (if using third-party)

**Decision Point:** If auth is already partially implemented, read existing files to understand the pattern before extending it.

### Step 2: Detect Stack

Use `detect_stack` to determine framework and identify auth approach:

```yaml
detect_stack:
  path: "."
```

**Framework Detection:**
- **Next.js (App Router)**: Use middleware.ts + Server Actions + cookies
- **Next.js (Pages Router)**: Use getServerSideProps + API routes + NextAuth
- **Remix**: Use loader/action auth + session cookies
- **Express/Fastify**: Use middleware + session store
- **tRPC**: Use context + middleware
- **GraphQL**: Use context + directives

**Consult Decision Tree:** Read `references/decision-tree.md` to choose between managed (Clerk, Auth0), self-hosted (NextAuth, Lucia), or serverless (Supabase Auth) based on framework and requirements.

### Step 3: Implementation Planning

Based on framework and decision tree, plan which files to create/modify:

**Common Files Needed:**

1. **Middleware** (`middleware.ts`, `auth.middleware.ts`)
   - Intercept requests
   - Verify authentication status
   - Redirect unauthenticated users

2. **Auth Utilities** (`lib/auth.ts`, `utils/auth.ts`)
   - Session creation/validation
   - Token generation/verification
   - Password hashing (bcrypt, argon2)

3. **Auth API Routes** (`/api/auth/login`, `/api/auth/signup`, `/api/auth/logout`)
   - Handle authentication requests
   - Set session cookies
   - Return auth state

4. **Protected Route Wrappers** (`withAuth`, `requireAuth`)
   - HOCs or server utilities
   - Check auth before rendering
   - Redirect or return 401

5. **Client Hooks** (`useAuth`, `useSession`)
   - Access current user
   - Manage client-side auth state
   - Trigger login/logout

**Framework-Specific Patterns:**

**Next.js App Router:**
```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('session')?.value;
  
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  
  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*']
};
```

**Remix:**
```typescript
// app/utils/session.server.ts
import { createCookieSessionStorage } from '@remix-run/node';

const { getSession, commitSession, destroySession } =
  createCookieSessionStorage({
    cookie: {
      name: '__session',
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      secrets: [process.env.SESSION_SECRET],
      sameSite: 'lax'
    }
  });

export { getSession, commitSession, destroySession };
```

**Express:**
```typescript
// middleware/auth.ts
import jwt from 'jsonwebtoken';
import type { Request, Response, NextFunction } from 'express';

export function requireAuth(req: Request, res: Response, next: NextFunction) {
  const token = req.headers.authorization?.replace(/^bearer\s+/i, '');
  
  if (!token) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  
  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET!);
    req.user = payload;
    next();
  } catch (err) {
    return res.status(401).json({ error: 'Invalid token' });
  }
}
```

### Step 4: Write Configuration and Core Files

Use `precision_write` in batch mode to create auth infrastructure:

```yaml
precision_write:
  files:
    - path: "middleware.ts"
      content: |
        # Framework-specific middleware (see patterns above)
    - path: "lib/auth.ts"
      content: |
        # Session validation, token generation
    - path: "app/api/auth/login/route.ts"
      content: |
        # Login endpoint implementation
    - path: "app/api/auth/signup/route.ts"
      content: |
        # Sign-up endpoint with validation
    - path: "app/api/auth/logout/route.ts"
      content: |
        # Logout and session cleanup
  verbosity: minimal
```

**CRITICAL: No Placeholders**
- Implement full validation (zod, yup, etc.)
- Include proper error handling
- Hash passwords with bcrypt/argon2
- Use secure session configuration
- Add CSRF protection where applicable

### Step 5: Install Dependencies

Use `precision_exec` to install required packages:

```yaml
precision_exec:
  commands:
    # For JWT-based auth
    - cmd: "npm install jsonwebtoken bcryptjs"
    - cmd: "npm install -D @types/jsonwebtoken @types/bcryptjs"
    
    # For session-based auth
    - cmd: "npm install express-session connect-redis"
    - cmd: "npm install -D @types/express-session"
    
    # For managed services
    - cmd: "npm install @clerk/nextjs"  # Clerk
    - cmd: "npm install next-auth"      # NextAuth
    - cmd: "npm install better-auth"    # Better Auth (replaces deprecated Lucia)
  verbosity: minimal
```

**Run Database Migrations (if needed):**

```yaml
precision_exec:
  commands:
    - cmd: "npx prisma migrate dev --name add_user_auth"
      timeout_ms: 60000
    - cmd: "npx prisma generate"
  verbosity: standard
```

### Step 6: Security Verification

Use analysis-engine tools to verify security:

**1. Scan for Hardcoded Secrets:**

```yaml
scan_for_secrets:
  paths:
    - "lib/auth.ts"
    - "app/api/auth/**/*.ts"
    - "middleware.ts"
```

**Expected Result:** Zero secrets found. All API keys, JWT secrets, and credentials must be in `.env` files.

**If secrets found:**
- Move to `.env` or `.env.local`
- Use `process.env.VAR_NAME` to access
- Add to `.gitignore` if not already present

**2. Audit Environment Variables:**

```yaml
env_audit:
  check_documented: true
```

**Expected Result:** All auth-related env vars documented in `.env.example` or README.

**Required Variables (typical):**
- `JWT_SECRET` or `SESSION_SECRET`
- `DATABASE_URL` (if using database)
- OAuth credentials (`GOOGLE_CLIENT_ID`, `GITHUB_CLIENT_SECRET`, etc.)
- `NEXTAUTH_URL` and `NEXTAUTH_SECRET` (for NextAuth)

**3. Validate Implementation:**

```yaml
# Use precision_grep to validate critical security patterns
precision_grep:
  queries:
    - id: password_hashing
      pattern: "bcrypt|argon2|hashPassword"
      path: "lib"
      glob: "**/*.ts"
    - id: httpOnly_cookies
      pattern: "httpOnly.*true|httpOnly:\s*true"
      path: "."
      glob: "**/*.ts"
    - id: csrf_protection
      pattern: "csrf|CsrfToken|verifyCsrfToken"
      path: "."
      glob: "**/*.ts"
  output:
    format: "count_only"
```

### Step 7: Protected Routes Implementation

Create route protection utilities:

**Server-Side Protection (Next.js App Router):**

```typescript
// lib/auth.ts
import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';

export async function requireAuth() {
  const cookieStore = await cookies();
  const session = cookieStore.get('session')?.value;
  
  if (!session) {
    redirect('/login');
  }
  
  const user = await validateSession(session);
  if (!user) {
    redirect('/login');
  }
  
  return user;
}
```

**Client-Side Hook (React):**

```typescript
// hooks/useAuth.ts
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

export function useAuth(options?: { redirectTo?: string }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  
  useEffect(() => {
    fetch('/api/auth/me')
      .then(res => res.ok ? res.json() : null)
      .then(data => {
        if (!data && options?.redirectTo) {
          router.push(options.redirectTo);
        } else {
          setUser(data);
        }
      })
      .finally(() => setLoading(false));
  }, [options?.redirectTo, router]);
  
  return { user, loading };
}
```

**Apply to Routes:**

Use `precision_edit` to add auth checks to existing routes:

```yaml
precision_edit:
  files:
    - path: "app/dashboard/page.tsx"
      edits:
        - find: "export default function DashboardPage()"
          replace: |
            export default async function DashboardPage() {
              const user = await requireAuth();
          hints:
            near_line: 1
```

### Step 8: Test Implementation

Use `suggest_test_cases` to generate auth-specific test scenarios:

```yaml
suggest_test_cases:
  file: "lib/auth.ts"
  category: "authentication"
```

**Expected Test Cases:**
- Valid login with correct credentials
- Login failure with incorrect password
- Sign-up with valid data
- Sign-up with duplicate email
- Protected route redirects unauthenticated users
- Session token refresh
- Logout clears session
- CSRF token validation
- Password reset flow

**Run Validation Script:**

```bash
bash scripts/auth-checklist.sh .
```

**Expected Exit Code:** 0 (all checks pass)

**Manual Testing Checklist:**
1. Sign up new user
2. Verify password is hashed in database
3. Log in with credentials
4. Access protected route (should succeed)
5. Log out
6. Access protected route (should redirect to login)
7. Test OAuth flow (if implemented)
8. Verify session persists across page reloads
9. Test token expiration and refresh

## Common Patterns by Framework

### Next.js (App Router)

**Session Management:**
- Use cookies() from 'next/headers'
- Set httpOnly, secure, sameSite cookies
- Validate in middleware.ts and Server Components

**Protected Routes:**
- Server-side: await requireAuth() in page/layout
- Client-side: useAuth() hook with redirectTo
- API routes: check cookies in route handlers

**OAuth:**
- Use NextAuth for simplicity
- Or implement manual OAuth flow with redirect URIs

### Remix

**Session Management:**
- Use createCookieSessionStorage
- Validate in loaders
- Commit session in actions

**Protected Routes:**
- Check session in loader, throw redirect() if unauthenticated
- Use getSession() utility consistently

**OAuth:**
- Use remix-auth strategies
- Handle callbacks in dedicated routes

### Express/Fastify

**Session Management:**
- Use express-session + Redis store
- Or JWT tokens in Authorization header

**Protected Routes:**
- Middleware functions: requireAuth, optionalAuth
- Apply to specific routes or globally

**OAuth:**
- Use passport.js strategies
- Configure serialize/deserialize user

## Error Handling

Follow error-recovery protocol for auth failures:

### Login Failures

```typescript
try {
  const user = await validateCredentials(email, password);
  await createSession(user.id);
  return { success: true };
} catch (err) {
  if (err instanceof InvalidCredentialsError) {
    // Don't leak whether email exists
    return { error: 'Invalid email or password' };
  }
  if (err instanceof UserLockedError) {
    return { error: 'Account locked. Contact support.' };
  }
  throw err; // Unexpected error
}
```

### Session Validation Failures

```typescript
export async function validateSession(token: string) {
  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET!);
    return await getUserById(payload.userId);
  } catch (err) {
    if (err instanceof jwt.TokenExpiredError) {
      return null; // Let caller handle (refresh or re-login)
    }
    if (err instanceof jwt.JsonWebTokenError) {
      return null; // Invalid token
    }
    throw err; // Unexpected error
  }
}
```

### Database Errors

```typescript
try {
  const user = await db.user.create({
    data: { email, passwordHash }
  });
} catch (err) {
  if (err.code === 'P2002') {
    // Prisma unique constraint violation
    return { error: 'Email already registered' };
  }
  throw err;
}
```

## Security Checklist

Before marking implementation complete:

- [ ] Passwords hashed with bcrypt (cost 10+) or argon2
- [ ] Session tokens are random (crypto.randomBytes) or signed JWT
- [ ] Cookies are httpOnly, secure (in prod), sameSite: 'lax' or 'strict'
- [ ] CSRF protection enabled (for cookie-based auth)
- [ ] Rate limiting on login/signup endpoints
- [ ] Input validation on all auth endpoints
- [ ] No sensitive data in error messages
- [ ] Environment variables documented in .env.example
- [ ] No hardcoded secrets in source code
- [ ] Session expiration configured (1-7 days typical)
- [ ] Logout clears all auth tokens/sessions
- [ ] OAuth redirect URIs whitelisted

## References

- `references/decision-tree.md` - Managed vs self-hosted vs serverless comparison
- `.goodvibes/memory/patterns.json` - Project-specific auth patterns
- `scripts/auth-checklist.sh` - Automated validation script

## Troubleshooting

### "Session not persisting across requests"

**Likely Causes:**
- Cookie not being set (check response headers)
- httpOnly preventing client-side access (expected)
- sameSite: 'strict' blocking cross-origin (use 'lax')
- Cookie domain mismatch

**Fix:**
1. Check cookie configuration in auth code
2. Verify cookies are in response: `precision_exec: { cmd: "curl -v localhost:3000/api/auth/login" }`
3. Ensure middleware reads cookies correctly

### "JWT token invalid after server restart"

**Likely Causes:**
- JWT_SECRET changes between restarts
- Secret not in .env file
- Different secret in different environments

**Fix:**
1. Move JWT_SECRET to .env: `JWT_SECRET=<random-256-bit-hex>`
2. Generate with: `openssl rand -hex 32`
3. Never commit .env to git

### "OAuth callback fails with redirect_uri_mismatch"

**Likely Causes:**
- Callback URL not whitelisted in OAuth provider dashboard
- http vs https mismatch
- Port number missing

**Fix:**
1. Check OAuth provider settings
2. Add callback URL exactly as it appears in error
3. For local dev, use http://localhost:3000/api/auth/callback/google (example)

### "Protected routes not redirecting"

**Likely Causes:**
- Middleware not configured correctly
- Matcher pattern doesn't match route
- Session validation failing silently

**Fix:**
1. Check middleware.ts config.matcher
2. Add logging to middleware to verify it's running
3. Test session validation independently

## Next Steps After Implementation

1. **Add role-based access control (RBAC):**
   - Add `role` field to User model
   - Create permission checking utilities
   - Protect admin routes

2. **Implement password reset:**
   - Generate reset tokens
   - Send email with reset link
   - Validate token and update password

3. **Add email verification:**
   - Generate verification tokens on signup
   - Send verification email
   - Verify token and mark user as verified

4. **Set up refresh tokens:**
   - Issue short-lived access tokens (15 min)
   - Issue long-lived refresh tokens (7 days)
   - Rotate refresh tokens on use

5. **Add audit logging:**
   - Log all login attempts (success and failure)
   - Track IP addresses and user agents
   - Monitor for suspicious activity

## Summary

This workflow provides:
- Framework-agnostic authentication implementation
- Security-first approach with validation
- Integration with GoodVibes precision tools
- Automated verification via scripts
- Error handling and troubleshooting

Follow each step sequentially, using precision tools for all file operations and validation.
