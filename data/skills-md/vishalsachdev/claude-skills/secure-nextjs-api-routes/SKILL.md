---
name: secure-nextjs-api-routes
description: A comprehensive security middleware system for Next.js 13+ App Router API routes that provides authentication, rate limiting, CSRF protection, audit logging, and security headers in a composable, production-ready pattern. Use when building secure Next.js APIs that need protection against common web vulnerabilities.
---

# Secure Next.js API Routes

A comprehensive security middleware system for Next.js 13+ App Router API routes that provides authentication, rate limiting, CSRF protection, audit logging, and security headers in a composable, production-ready pattern.

## When to use this skill

- Creating new Next.js API routes that need security
- Adding authentication requirements to endpoints
- Implementing rate limiting for API endpoints
- Protecting against CSRF attacks on state-changing operations
- Adding audit logging for security events
- Enforcing request size limits and method restrictions
- Setting security headers automatically

## Core Components

This skill consists of 4 integrated modules:

1. **Security Middleware** (`lib/security-middleware.ts`) - Main composable wrapper
2. **CSRF Protection** (`lib/csrf-protection.ts`) - Double-submit cookie pattern
3. **Rate Limiter** (`lib/rate-limiter.ts`) - Supabase-backed rate limiting
4. **Audit Logger** (`lib/audit-logger.ts`) - Security event tracking

## Implementation Steps

### Step 1: Create the Security Middleware

Create `lib/security-middleware.ts`:

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { RateLimiter, RATE_LIMITS, rateLimitResponse } from '@/lib/rate-limiter';
import { AuditLogger, AuditAction } from '@/lib/audit-logger';
import { createClient } from '@/lib/supabase/server';
import { validateCSRF, injectCSRFToken } from '@/lib/csrf-protection';

export interface SecurityMiddlewareConfig {
  rateLimit?: {
    windowMs: number;
    maxRequests: number;
  };
  requireAuth?: boolean;
  maxBodySize?: number; // In bytes
  allowedMethods?: string[];
  csrfProtection?: boolean;
}

/**
 * Security middleware for API routes
 */
export function withSecurity(
  handler: (req: NextRequest) => Promise<NextResponse>,
  config: SecurityMiddlewareConfig = {}
) {
  return async function securedHandler(req: NextRequest): Promise<NextResponse> {
    try {
      // 1. Check allowed methods
      if (config.allowedMethods && !config.allowedMethods.includes(req.method)) {
        return NextResponse.json(
          { error: 'Method not allowed' },
          { status: 405 }
        );
      }

      // 2. Check authentication if required
      if (config.requireAuth) {
        const supabase = await createClient();
        const { data: { user }, error } = await supabase.auth.getUser();

        if (error || !user) {
          await AuditLogger.logSecurityEvent(
            AuditAction.UNAUTHORIZED_ACCESS,
            { endpoint: req.url }
          );

          return NextResponse.json(
            { error: 'Authentication required' },
            { status: 401 }
          );
        }
      }

      // 3. Apply rate limiting
      if (config.rateLimit) {
        const rateLimitResult = await RateLimiter.check(
          req.url,
          config.rateLimit
        );

        if (!rateLimitResult.allowed) {
          await AuditLogger.logRateLimitExceeded(
            req.url,
            'api-endpoint'
          );

          return rateLimitResponse(rateLimitResult) || NextResponse.json(
            { error: 'Rate limit exceeded' },
            { status: 429 }
          );
        }
      }

      // 4. Check content size (for POST/PUT/PATCH)
      if (['POST', 'PUT', 'PATCH'].includes(req.method) && config.maxBodySize) {
        const contentLength = req.headers.get('content-length');
        if (contentLength && parseInt(contentLength) > config.maxBodySize) {
          return NextResponse.json(
            { error: 'Request body too large' },
            { status: 413 }
          );
        }
      }

      // 5. CSRF Protection for state-changing operations
      if (config.csrfProtection && ['POST', 'PUT', 'PATCH', 'DELETE'].includes(req.method)) {
        const csrfValidation = await validateCSRF(req);
        if (!csrfValidation.valid) {
          await AuditLogger.logSecurityEvent(
            AuditAction.UNAUTHORIZED_ACCESS,
            {
              endpoint: req.url,
              reason: 'CSRF validation failed',
              error: csrfValidation.error
            }
          );

          return NextResponse.json(
            { error: csrfValidation.error || 'CSRF validation failed' },
            { status: 403 }
          );
        }
      }

      // 6. Add security headers to response
      const response = await handler(req);

      // Add security headers
      response.headers.set('X-Content-Type-Options', 'nosniff');
      response.headers.set('X-Frame-Options', 'DENY');
      response.headers.set('X-XSS-Protection', '1; mode=block');
      response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
      response.headers.set('Permissions-Policy', 'camera=(), microphone=(), geolocation=()');

      // Add CORS headers if needed
      const origin = req.headers.get('origin');
      if (origin && isAllowedOrigin(origin)) {
        response.headers.set('Access-Control-Allow-Origin', origin);
        response.headers.set('Access-Control-Allow-Credentials', 'true');
      }

      // Inject new CSRF token for subsequent requests (if CSRF is enabled)
      if (config.csrfProtection) {
        const { response: csrfResponse } = injectCSRFToken(response);
        return csrfResponse;
      }

      return response;
    } catch (error) {
      console.error('Security middleware error:', error);
      return NextResponse.json(
        { error: 'Internal server error' },
        { status: 500 }
      );
    }
  };
}

/**
 * Check if origin is allowed for CORS
 */
function isAllowedOrigin(origin: string): boolean {
  const allowedOrigins = [
    process.env.NEXT_PUBLIC_BASE_URL,
    'http://localhost:3000',
    'http://localhost:3001',
  ].filter(Boolean);

  return allowedOrigins.includes(origin);
}

/**
 * Preset security configurations
 */
export const SECURITY_PRESETS = {
  PUBLIC: {
    rateLimit: RATE_LIMITS.API_GENERAL,
    maxBodySize: 1024 * 1024, // 1MB
    allowedMethods: ['GET', 'POST']
  },
  AUTHENTICATED: {
    requireAuth: true,
    rateLimit: RATE_LIMITS.AUTH_GENERATION,
    maxBodySize: 5 * 1024 * 1024, // 5MB
    allowedMethods: ['GET', 'POST', 'PUT', 'DELETE'],
    csrfProtection: true
  },
  STRICT: {
    requireAuth: true,
    rateLimit: {
      windowMs: 60 * 1000,
      maxRequests: 10
    },
    maxBodySize: 512 * 1024, // 512KB
    allowedMethods: ['POST'],
    csrfProtection: true
  }
};
```

### Step 2: Create CSRF Protection

Create `lib/csrf-protection.ts`:

```typescript
import { NextRequest, NextResponse } from 'next/server';
import crypto from 'crypto';

const CSRF_TOKEN_HEADER = 'X-CSRF-Token';
const CSRF_TOKEN_COOKIE = 'csrf-token';
const TOKEN_LENGTH = 32;

export function generateCSRFToken(): string {
  return crypto.randomBytes(TOKEN_LENGTH).toString('hex');
}

export function setCSRFTokenCookie(response: NextResponse, token: string): void {
  response.cookies.set(CSRF_TOKEN_COOKIE, token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
    path: '/',
    maxAge: 60 * 60 * 24 // 24 hours
  });
}

export function getCSRFTokenFromCookie(request: NextRequest): string | null {
  return request.cookies.get(CSRF_TOKEN_COOKIE)?.value || null;
}

export function getCSRFTokenFromHeader(request: NextRequest): string | null {
  return request.headers.get(CSRF_TOKEN_HEADER);
}

export function validateCSRFToken(
  cookieToken: string | null,
  headerToken: string | null
): boolean {
  if (!cookieToken || !headerToken) return false;
  if (cookieToken !== headerToken) return false;
  if (cookieToken.length !== TOKEN_LENGTH * 2) return false;
  return true;
}

export async function validateCSRF(request: NextRequest): Promise<{ valid: boolean; error?: string }> {
  if (['GET', 'HEAD', 'OPTIONS'].includes(request.method)) {
    return { valid: true };
  }

  const cookieToken = getCSRFTokenFromCookie(request);
  const headerToken = getCSRFTokenFromHeader(request);

  if (!validateCSRFToken(cookieToken, headerToken)) {
    return {
      valid: false,
      error: 'Invalid or missing CSRF token'
    };
  }

  return { valid: true };
}

export function injectCSRFToken(response: NextResponse): { token: string; response: NextResponse } {
  const token = generateCSRFToken();
  setCSRFTokenCookie(response, token);
  response.headers.set('X-CSRF-Token', token);
  return { token, response };
}
```

### Step 3: Create Rate Limiter

Create `lib/rate-limiter.ts`:

```typescript
import { createClient } from '@/lib/supabase/server';
import { headers } from 'next/headers';
import { NextResponse } from 'next/server';
import crypto from 'crypto';

interface RateLimitConfig {
  windowMs: number;
  maxRequests: number;
  identifier?: string;
}

interface RateLimitResult {
  allowed: boolean;
  remaining: number;
  resetAt: Date;
  retryAfter?: number;
}

export class RateLimiter {
  private static async getIdentifier(customId?: string): Promise<string> {
    if (customId) return customId;

    const supabase = await createClient();
    const { data: { user } } = await supabase.auth.getUser();

    if (user) return `user:${user.id}`;

    // For anonymous users, use IP address hash
    const headersList = await headers();
    const forwardedFor = headersList.get('x-forwarded-for');
    const realIp = headersList.get('x-real-ip');
    const ip = forwardedFor?.split(',')[0] || realIp || 'unknown';

    const hash = crypto.createHash('sha256').update(ip).digest('hex');
    return `anon:${hash.substring(0, 16)}`;
  }

  static async check(
    key: string,
    config: RateLimitConfig
  ): Promise<RateLimitResult> {
    const identifier = await this.getIdentifier(config.identifier);
    const rateLimitKey = `ratelimit:${key}:${identifier}`;

    const supabase = await createClient();
    const now = Date.now();
    const windowStart = now - config.windowMs;

    try {
      // Clean up old entries
      await supabase
        .from('rate_limits')
        .delete()
        .lt('timestamp', new Date(windowStart).toISOString());

      // Count recent requests
      const { data: recentRequests, error } = await supabase
        .from('rate_limits')
        .select('id')
        .eq('key', rateLimitKey)
        .gte('timestamp', new Date(windowStart).toISOString());

      if (error) throw error;

      const requestCount = recentRequests?.length || 0;
      const remaining = Math.max(0, config.maxRequests - requestCount);
      const resetAt = new Date(now + config.windowMs);

      if (requestCount >= config.maxRequests) {
        const { data: oldestRequest } = await supabase
          .from('rate_limits')
          .select('timestamp')
          .eq('key', rateLimitKey)
          .order('timestamp', { ascending: true })
          .limit(1)
          .single();

        let retryAfter = Math.ceil(config.windowMs / 1000);
        if (oldestRequest) {
          const oldestTime = new Date(oldestRequest.timestamp).getTime();
          retryAfter = Math.ceil((oldestTime + config.windowMs - now) / 1000);
        }

        return { allowed: false, remaining: 0, resetAt, retryAfter };
      }

      // Record this request
      await supabase.from('rate_limits').insert({
        key: rateLimitKey,
        timestamp: new Date(now).toISOString(),
        identifier
      });

      return { allowed: true, remaining: remaining - 1, resetAt };
    } catch (error) {
      console.error('Rate limiter error:', error);
      return {
        allowed: true,
        remaining: config.maxRequests,
        resetAt: new Date(now + config.windowMs)
      };
    }
  }
}

export const RATE_LIMITS = {
  API_GENERAL: {
    windowMs: 60 * 1000,
    maxRequests: 60
  },
  AUTH_GENERATION: {
    windowMs: 60 * 60 * 1000,
    maxRequests: 20
  },
  ANON_GENERATION: {
    windowMs: 24 * 60 * 60 * 1000,
    maxRequests: 3
  }
};

export function rateLimitResponse(result: RateLimitResult): NextResponse | null {
  const headers: HeadersInit = {
    'X-RateLimit-Remaining': result.remaining.toString(),
    'X-RateLimit-Reset': result.resetAt.toISOString()
  };

  if (!result.allowed && result.retryAfter) {
    headers['Retry-After'] = result.retryAfter.toString();

    return NextResponse.json(
      {
        error: 'Rate limit exceeded',
        message: `Too many requests. Please try again in ${result.retryAfter} seconds.`,
        retryAfter: result.retryAfter,
        resetAt: result.resetAt
      },
      { status: 429, headers }
    );
  }

  return null;
}
```

### Step 4: Create Audit Logger

Create `lib/audit-logger.ts`:

```typescript
import { createClient } from '@/lib/supabase/server';

export enum AuditAction {
  UNAUTHORIZED_ACCESS = 'unauthorized_access',
  RATE_LIMIT_EXCEEDED = 'rate_limit_exceeded',
  CSRF_VALIDATION_FAILED = 'csrf_validation_failed',
  INVALID_INPUT = 'invalid_input',
  SECURITY_EVENT = 'security_event'
}

export class AuditLogger {
  static async logSecurityEvent(
    action: AuditAction,
    metadata?: Record<string, unknown>
  ): Promise<void> {
    try {
      const supabase = await createClient();
      const { data: { user } } = await supabase.auth.getUser();

      await supabase.from('audit_logs').insert({
        action,
        user_id: user?.id || null,
        metadata,
        timestamp: new Date().toISOString()
      });
    } catch (error) {
      console.error('Failed to log audit event:', error);
    }
  }

  static async logRateLimitExceeded(
    endpoint: string,
    resourceType: string
  ): Promise<void> {
    await this.logSecurityEvent(AuditAction.RATE_LIMIT_EXCEEDED, {
      endpoint,
      resourceType
    });
  }
}
```

### Step 5: Create Database Tables

Run this SQL in your Supabase SQL editor:

```sql
-- Rate limiting table
CREATE TABLE IF NOT EXISTS rate_limits (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  key TEXT NOT NULL,
  identifier TEXT NOT NULL,
  timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_rate_limits_key_timestamp ON rate_limits(key, timestamp);
CREATE INDEX idx_rate_limits_timestamp ON rate_limits(timestamp);

-- Audit logs table
CREATE TABLE IF NOT EXISTS audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  action TEXT NOT NULL,
  user_id UUID REFERENCES auth.users(id),
  metadata JSONB,
  timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);
```

### Step 6: Create Client-Side CSRF Fetch Helper

Create `lib/csrf-client.ts`:

```typescript
export async function csrfFetch(
  url: string,
  options: RequestInit = {}
): Promise<Response> {
  // Get CSRF token from cookie
  const csrfToken = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrf-token='))
    ?.split('=')[1];

  // Add CSRF token to headers for state-changing requests
  const method = options.method?.toUpperCase() || 'GET';
  const needsCSRF = ['POST', 'PUT', 'PATCH', 'DELETE'].includes(method);

  const headers = new Headers(options.headers);
  if (needsCSRF && csrfToken) {
    headers.set('X-CSRF-Token', csrfToken);
  }

  return fetch(url, {
    ...options,
    headers
  });
}
```

## Usage Examples

### Example 1: Public API Route with Rate Limiting

```typescript
// app/api/public-data/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { withSecurity, SECURITY_PRESETS } from '@/lib/security-middleware';

async function handler(req: NextRequest) {
  // Your handler logic
  const data = await fetchPublicData();
  return NextResponse.json({ data });
}

export const GET = withSecurity(handler, SECURITY_PRESETS.PUBLIC);
```

### Example 2: Authenticated Route with CSRF Protection

```typescript
// app/api/user/notes/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { withSecurity, SECURITY_PRESETS } from '@/lib/security-middleware';

async function handler(req: NextRequest) {
  const body = await req.json();
  // Your authenticated handler logic
  return NextResponse.json({ success: true });
}

export const POST = withSecurity(handler, SECURITY_PRESETS.AUTHENTICATED);
```

### Example 3: Custom Security Configuration

```typescript
// app/api/sensitive-operation/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { withSecurity } from '@/lib/security-middleware';

async function handler(req: NextRequest) {
  // Highly sensitive operation
  return NextResponse.json({ success: true });
}

export const POST = withSecurity(handler, {
  requireAuth: true,
  csrfProtection: true,
  rateLimit: {
    windowMs: 60 * 60 * 1000, // 1 hour
    maxRequests: 5 // Only 5 requests per hour
  },
  maxBodySize: 100 * 1024, // 100KB max
  allowedMethods: ['POST']
});
```

### Example 4: Client-Side Usage with CSRF

```typescript
// Client component
import { csrfFetch } from '@/lib/csrf-client';

async function saveNote(noteData) {
  const response = await csrfFetch('/api/notes', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(noteData)
  });

  return response.json();
}
```

## Security Best Practices

1. **Always use SECURITY_PRESETS** for consistency unless you need custom config
2. **Enable CSRF protection** for all state-changing operations (POST, PUT, PATCH, DELETE)
3. **Use strict rate limits** for expensive operations (AI generation, file uploads)
4. **Log security events** for monitoring and incident response
5. **Keep audit logs** for compliance and debugging
6. **Use csrfFetch** on client-side for all authenticated mutations
7. **Set appropriate maxBodySize** to prevent DoS attacks
8. **Review audit logs** regularly for suspicious activity

## Common Pitfalls

1. **Forgetting CSRF tokens on client**: Always use `csrfFetch` for mutations
2. **Too lenient rate limits**: Start strict, loosen based on usage patterns
3. **Not handling 429 responses**: Show user-friendly retry messages
4. **Logging sensitive data**: Never log passwords, tokens, or PII in audit logs
5. **Missing database indices**: Rate limiting table needs indices for performance
6. **Not cleaning up old records**: Set up a cron job to delete old rate_limits rows

## Environment Variables Required

```bash
# .env.local
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
CSRF_SALT=your-random-secret-salt  # Optional, generates random if not set
```

## Testing Your Implementation

```typescript
// Test rate limiting
for (let i = 0; i < 100; i++) {
  const response = await fetch('/api/protected');
  console.log(response.status); // Should get 429 after limit
}

// Test CSRF protection
const response = await fetch('/api/protected', {
  method: 'POST',
  // Missing CSRF token - should fail with 403
});

// Test authentication
const response = await fetch('/api/authenticated');
// Should return 401 if not logged in
```

## Next Steps

After implementing this skill:

1. Add monitoring for rate limit events
2. Set up alerts for repeated unauthorized access attempts
3. Create a dashboard to view audit logs
4. Implement IP-based blocking for repeated violations
5. Add request fingerprinting for additional security
