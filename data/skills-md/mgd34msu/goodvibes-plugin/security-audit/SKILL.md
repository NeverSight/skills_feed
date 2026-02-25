---
name: security-audit
description: "Load PROACTIVELY when task involves security review, vulnerability assessment, or hardening. Use when user says \"check for security issues\", \"audit for vulnerabilities\", \"scan for secrets\", \"review auth security\", or \"check OWASP compliance\". Covers authentication and session security, authorization and access control, input validation and injection prevention, data protection and encryption, dependency vulnerability scanning, API security (CORS, rate limiting, headers), and infrastructure hardening. Produces structured reports with severity ratings."
metadata:
  version: "1.0.0"
  category: quality
  tags: [security, audit, authentication, authorization, owasp, vulnerabilities]
---

## Resources
```
scripts/
  validate-security-audit.sh
references/
  security-patterns.md
```

# Security Audit

This skill guides you through performing comprehensive security audits on codebases to identify vulnerabilities, insecure patterns, and configuration issues. Use this when conducting security reviews, preparing for production deployments, or responding to security incidents.

## When to Use This Skill

- Conducting pre-deployment security reviews
- Responding to security incidents or vulnerability reports
- Performing periodic security audits on existing codebases
- Validating security controls after major feature additions
- Preparing for security compliance audits (SOC 2, ISO 27001)
- Onboarding new team members to security standards

## Audit Methodology

A systematic security audit follows these phases:

### Phase 1: Reconnaissance

**Objective:** Understand the application architecture, tech stack, and attack surface.

**Use precision_grep to map the codebase:**
```yaml
precision_grep:
  queries:
    - id: auth_patterns
      pattern: "(session|token|auth|login|password|jwt)"
      glob: "**/*.{ts,tsx,js,jsx}"
    - id: api_endpoints
      pattern: "(router\\.(get|post|put|delete)|export.*GET|export.*POST)"
      glob: "**/*.{ts,tsx,js,jsx}"
    - id: database_queries
      pattern: "(prisma\\.|db\\.|query\\(|execute\\()"
      glob: "**/*.{ts,tsx,js,jsx}"
    - id: env_usage
      pattern: "process\\.env\\."
      glob: "**/*.{ts,tsx,js,jsx}"
  output:
    format: minimal
```

**Identify critical components:**
- Authentication flows (login, registration, password reset)
- Authorization middleware and guards
- API endpoints (public vs authenticated)
- Database access patterns
- File upload/download handlers
- Payment processing logic
- Admin panels or privileged operations

### Phase 2: Authentication Audit

**Objective:** Verify secure authentication implementation.

#### Check for Weak Session Management

**Search for session configuration issues:**
```yaml
precision_grep:
  queries:
    - id: session_config
      pattern: "(session|cookie).*secure.*false|httpOnly.*false|sameSite.*(none|lax)"
      glob: "**/*.{ts,tsx,js,jsx}"
    - id: jwt_secrets
      pattern: "jwt\\.sign.*secret.*[\"'][^\"']{1,20}[\"']|new.*JwtStrategy"
      glob: "**/*.{ts,tsx,js,jsx}"
  output:
    format: standard
```

**Common vulnerabilities:**
- Session cookies without `httpOnly` flag (exposes to XSS)
- Session cookies without `secure` flag (allows HTTP transmission)
- Weak JWT secrets (under 32 bytes entropy)
- Sessions without expiration (immortal sessions)
- No session invalidation on logout

**Secure session example:**
```typescript
import { cookies } from 'next/headers';

export async function createSession(userId: string) {
  const sessionToken = await generateSecureToken();
  const expiresAt = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000); // 7 days

  await db.session.create({
    data: {
      token: sessionToken,
      userId,
      expiresAt,
    },
  });

  cookies().set('session', sessionToken, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
    expires: expiresAt,
    path: '/',
  });
}

export async function invalidateSession(sessionToken: string) {
  await db.session.delete({ where: { token: sessionToken } });
  cookies().delete('session');
}
```

#### Check for Password Security Issues

**Search for weak password handling:**
```yaml
precision_grep:
  queries:
    - id: password_storage
      pattern: "password.*=.*(req\\.body|params|query)|password.*toString|password.*text"
      glob: "**/*.{ts,tsx,js,jsx}"
    - id: password_hashing
      pattern: "(bcrypt|argon2|scrypt|pbkdf2)"
      glob: "**/*.{ts,tsx,js,jsx}"
  output:
    format: verbose
```

**Common vulnerabilities:**
- Passwords stored in plain text
- Weak hashing algorithms (MD5, SHA1, SHA256 without salt)
- No password complexity requirements
- Password hints or recovery questions
- Passwords logged or exposed in error messages

**Secure password hashing:**
```typescript
import { hash, verify } from '@node-rs/argon2';

export async function hashPassword(password: string): Promise<string> {
  return await hash(password, {
    memoryCost: 19456, // 19 MB
    timeCost: 2,
    outputLen: 32,
    parallelism: 1,
  });
}

export async function verifyPassword(
  hash: string,
  password: string
): Promise<boolean> {
  try {
    return await verify(hash, password);
  } catch {
    return false;
  }
}
```

#### Check for MFA Implementation

**Search for MFA patterns:**
```yaml
precision_grep:
  queries:
    - id: mfa_usage
      pattern: "(totp|authenticator|2fa|mfa|otp)"
      glob: "**/*.{ts,tsx,js,jsx}"
  output:
    format: minimal
```

**MFA best practices:**
- TOTP (Time-based One-Time Password) using authenticator apps
- Backup codes for account recovery
- SMS OTP as fallback (not primary)
- WebAuthn/FIDO2 for hardware keys
- Rate limiting on OTP verification

### Phase 3: Authorization Audit

**Objective:** Ensure proper access controls and permission checks.

#### Check for Missing Authorization Checks

**Identify API endpoints:**
```yaml
precision_grep:
  queries:
    - id: api_routes
      pattern: "export async function (GET|POST|PUT|DELETE|PATCH)"
      glob: "**/api/**/*.{ts,tsx,js,jsx}"
    - id: auth_middleware
      pattern: "(requireAuth|withAuth|authorize|checkPermission)"
      glob: "**/*.{ts,tsx,js,jsx}"
  output:
    format: locations
```

**Manual review checklist:**
- Do all authenticated endpoints verify user identity?
- Do endpoints check resource ownership (user can only access their own data)?
- Are admin routes protected by role checks?
- Is authorization checked server-side (not just client-side)?

**Common vulnerabilities:**
- Insecure Direct Object Reference (IDOR): `/api/users/123` returns any user
- Privilege escalation: Regular user can access admin functions
- Missing authorization: Endpoints rely on client-side checks only

**Secure authorization pattern:**
```typescript
import { auth } from '@/lib/auth';
import { db } from '@/lib/db';
import { NextResponse } from 'next/server';

export async function GET(
  req: Request,
  { params }: { params: { id: string } }
) {
  const session = await auth();
  
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const post = await db.post.findUnique({
    where: { id: params.id },
    select: { id: true, title: true, content: true, authorId: true },
  });

  if (!post) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 });
  }

  // Check ownership
  if (post.authorId !== session.user.id) {
    return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
  }

  return NextResponse.json(post);
}
```

#### Check for Role-Based Access Control (RBAC)

**Search for role definitions:**
```yaml
precision_grep:
  queries:
    - id: role_checks
      pattern: "(role.*===|role.*includes|hasRole|checkRole|permissions)"
      glob: "**/*.{ts,tsx,js,jsx}"
  output:
    format: matches
```

**RBAC implementation:**
```typescript
type Role = 'user' | 'admin' | 'moderator';

type Permission = 
  | 'posts:read'
  | 'posts:write'
  | 'posts:delete'
  | 'users:manage'
  | 'settings:admin';

const rolePermissions: Record<Role, Permission[]> = {
  user: ['posts:read', 'posts:write'],
  moderator: ['posts:read', 'posts:write', 'posts:delete'],
  admin: ['posts:read', 'posts:write', 'posts:delete', 'users:manage', 'settings:admin'],
};

export function hasPermission(role: Role, permission: Permission): boolean {
  return rolePermissions[role].includes(permission);
}

export function requirePermission(permission: Permission) {
  return async (req: Request) => {
    const session = await auth();
    
    if (!session || !hasPermission(session.user.role, permission)) {
      throw new Error('Insufficient permissions');
    }
  };
}
```

### Phase 4: Input Validation Audit

**Objective:** Prevent injection attacks and malicious input.

#### Check for SQL Injection

**Search for unsafe database queries:**
```yaml
precision_grep:
  queries:
    - id: raw_sql
      pattern: "(\\$executeRaw|\\$queryRaw|db\\.query|connection\\.query).*\\$\\{|.*`.*\\$\\{"
      glob: "**/*.{ts,tsx,js,jsx}"
    - id: string_concatenation
      pattern: "(SELECT|INSERT|UPDATE|DELETE).*\\+.*req\\.(body|query|params)"
      glob: "**/*.{ts,tsx,js,jsx}"
  output:
    format: verbose
```

**Common vulnerabilities:**
- String concatenation in SQL queries
- Unsanitized user input in raw SQL
- Dynamic table/column names from user input

**Secure database queries:**
```typescript
// UNSAFE - SQL injection vulnerable
export async function getUserByEmail(email: string) {
  const query = `SELECT * FROM users WHERE email = '${email}'`;
  return await db.$queryRawUnsafe(query);
}

// SAFE - Parameterized query
export async function getUserByEmail(email: string) {
  return await db.user.findUnique({
    where: { email },
  });
}

// SAFE - Raw query with parameters
export async function searchUsers(query: string) {
  return await db.$queryRaw`
    SELECT id, name, email 
    FROM users 
    WHERE name ILIKE ${'%' + query + '%'}
    LIMIT 20
  `;
}
```

#### Check for XSS (Cross-Site Scripting)

**Search for unsafe rendering:**
```yaml
precision_grep:
  queries:
    - id: dangerous_html
      pattern: "(dangerouslySetInnerHTML|innerHTML|outerHTML)"
      glob: "**/*.{tsx,jsx}"
    - id: unescaped_output
      pattern: "(v-html|\\[innerHTML\\])"
      glob: "**/*.{vue,html}"
  output:
    format: locations
```

**Common vulnerabilities:**
- Rendering unsanitized user input with `dangerouslySetInnerHTML`
- Using `innerHTML` to insert user-provided content
- Disabling auto-escaping in template engines

**Secure rendering:**
```typescript
import DOMPurify from 'isomorphic-dompurify';

// UNSAFE - XSS vulnerable
export function UnsafeComment({ content }: { content: string }) {
  return <div dangerouslySetInnerHTML={{ __html: content }} />;
}

// SAFE - Auto-escaped by React
export function SafeComment({ content }: { content: string }) {
  return <div>{content}</div>;
}

// SAFE - Sanitized HTML if needed
export function SafeRichComment({ html }: { html: string }) {
  const sanitized = DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'a'],
    ALLOWED_ATTR: ['href'],
  });
  return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;
}
```

#### Check for Command Injection

**Search for shell command execution:**
```yaml
precision_grep:
  queries:
    - id: shell_exec
      pattern: "(exec|spawn|execSync|spawnSync|execFile).*req\\.(body|query|params)"
      glob: "**/*.{ts,tsx,js,jsx}"
  output:
    format: verbose
```

**Common vulnerabilities:**
- User input passed directly to shell commands
- Unsanitized file paths in file operations

**Secure command execution:**
```typescript
import { spawn } from 'child_process';
import { z } from 'zod';

const allowedCommands = ['convert', 'resize', 'compress'] as const;
const commandSchema = z.enum(allowedCommands);

// UNSAFE - Command injection vulnerable
export async function processImage(filename: string) {
  exec(`convert ${filename} output.png`);
}

// SAFE - Validated input and array arguments
export async function processImage(command: string, filename: string) {
  const validCommand = commandSchema.parse(command);
  const sanitizedFilename = filename.replace(/[^a-zA-Z0-9._-]/g, '');
  
  return new Promise((resolve, reject) => {
    const child = spawn('imagemagick', [validCommand, sanitizedFilename, 'output.png']);
    child.on('exit', (code) => {
      if (code === 0) resolve(undefined);
      else reject(new Error('Processing failed'));
    });
  });
}
```

#### Check for Path Traversal

**Search for file operations:**
```yaml
precision_grep:
  queries:
    - id: file_operations
      pattern: "(readFile|writeFile|unlink|stat|createReadStream).*req\\.(body|query|params)"
      glob: "**/*.{ts,tsx,js,jsx}"
  output:
    format: locations
```

**Common vulnerabilities:**
- User-controlled file paths without validation
- Missing path normalization (allowing `../` sequences)

**Secure file handling:**
```typescript
import path from 'path';
import fs from 'fs/promises';

const UPLOADS_DIR = path.join(process.cwd(), 'uploads');

// UNSAFE - Path traversal vulnerable
export async function getFile(filename: string) {
  return await fs.readFile(`./uploads/${filename}`);
}

// SAFE - Path validation with defense against encoded traversals
export async function getFile(filename: string) {
  // Decode URL-encoded sequences (e.g., %2e%2e%2f -> ../)
  const decoded = decodeURIComponent(filename);
  const safePath = path.normalize(decoded).replace(/^(\.\.\/)+/, '');
  const fullPath = path.resolve(path.join(UPLOADS_DIR, safePath));
  
  // Ensure resolved path is within UPLOADS_DIR (prevents prefix collision)
  if (!fullPath.startsWith(UPLOADS_DIR + path.sep) && fullPath !== UPLOADS_DIR) {
    throw new Error('Invalid file path');
  }
  
  return await fs.readFile(fullPath);
}
```

### Phase 5: Data Protection Audit

**Objective:** Ensure sensitive data is encrypted and properly handled.

#### Check for Encryption at Rest

**Search for sensitive data storage:**
```yaml
precision_grep:
  queries:
    - id: sensitive_fields
      pattern: "(ssn|credit.*card|bank.*account|passport|drivers.*license)"
      glob: "**/*.{ts,tsx,js,jsx,prisma}"
    - id: encryption_usage
      pattern: "(encrypt|decrypt|cipher|crypto)"
      glob: "**/*.{ts,tsx,js,jsx}"
  output:
    format: minimal
```

**Encryption best practices:**
- Use AES-256-GCM for symmetric encryption
- Store encryption keys in secure key management (AWS KMS, HashiCorp Vault)
- Never commit encryption keys to version control
- Rotate encryption keys periodically

**Secure encryption implementation:**
```typescript
import { createCipheriv, createDecipheriv, randomBytes } from 'crypto';

const ALGORITHM = 'aes-256-gcm';
const ENCRYPTION_KEY = process.env.ENCRYPTION_KEY;
if (!ENCRYPTION_KEY) throw new Error('ENCRYPTION_KEY environment variable is required');
const KEY = Buffer.from(ENCRYPTION_KEY, 'hex'); // 32 bytes

export function encrypt(plaintext: string): string {
  const iv = randomBytes(16);
  const cipher = createCipheriv(ALGORITHM, KEY, iv);
  
  let encrypted = cipher.update(plaintext, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  
  const authTag = cipher.getAuthTag();
  
  // Return: iv:authTag:ciphertext
  return `${iv.toString('hex')}:${authTag.toString('hex')}:${encrypted}`;
}

export function decrypt(ciphertext: string): string {
  const [ivHex, authTagHex, encrypted] = ciphertext.split(':');
  
  const iv = Buffer.from(ivHex, 'hex');
  const authTag = Buffer.from(authTagHex, 'hex');
  
  const decipher = createDecipheriv(ALGORITHM, KEY, iv);
  decipher.setAuthTag(authTag);
  
  let decrypted = decipher.update(encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  
  return decrypted;
}
```

#### Check for PII Handling

**Search for personally identifiable information:**
```yaml
precision_grep:
  queries:
    - id: pii_fields
      pattern: "(email|phone|address|name|dob|birth.*date)"
      glob: "**/*.prisma"
    - id: logging_pii
      pattern: "(console\\.log|logger\\.(info|debug|warn)).*\\.(email|phone|ssn)"
      glob: "**/*.{ts,tsx,js,jsx}"
  output:
    format: locations
```

**PII protection checklist:**
- Minimize PII collection (only collect what's necessary)
- Redact PII in logs and error messages
- Implement data retention policies (auto-delete old data)
- Provide user data export (GDPR/CCPA compliance)
- Provide user data deletion (right to be forgotten)

#### Check for Secrets Management

**Search for hardcoded secrets:**
```yaml
precision_grep:
  queries:
    - id: hardcoded_secrets
      pattern: "(api.*key.*=.*[\"'][a-zA-Z0-9]{20,}|secret.*=.*[\"'][a-zA-Z0-9]{20,}|password.*=.*[\"'][^\"']{8,})"
      glob: "**/*.{ts,tsx,js,jsx}"
    - id: committed_env
      pattern: ".*"
      glob: ".env"
  output:
    format: verbose
```

**Common vulnerabilities:**
- API keys hardcoded in source code
- `.env` files committed to version control
- Secrets exposed in client-side code
- Default credentials not changed

**Secure secrets management:**
```typescript
import { z } from 'zod';

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  NEXTAUTH_SECRET: z.string().min(32),
  STRIPE_SECRET_KEY: z.string().startsWith('sk_'),
  OPENAI_API_KEY: z.string().startsWith('sk-'),
});

export const env = envSchema.parse({
  DATABASE_URL: process.env.DATABASE_URL,
  NEXTAUTH_SECRET: process.env.NEXTAUTH_SECRET,
  STRIPE_SECRET_KEY: process.env.STRIPE_SECRET_KEY,
  OPENAI_API_KEY: process.env.OPENAI_API_KEY,
});

// Ensure .env is in .gitignore
// Use .env.example (without values) to document required variables
// Use secrets management in production (Vercel Env Vars, AWS Secrets Manager)
```

### Phase 6: Dependency Audit

**Objective:** Identify and remediate vulnerable dependencies.

#### Run Automated Vulnerability Scanners

**Use npm audit:**
```yaml
precision_exec:
  commands:
    - cmd: "npm audit --json"
      timeout_ms: 30000
  verbosity: standard
```

**Check for outdated packages:**
```yaml
precision_exec:
  commands:
    - cmd: "npm outdated --json"
      timeout_ms: 10000
  verbosity: minimal
```

**Prioritize fixes:**
- **Critical/High:** Fix immediately before deployment
- **Moderate:** Fix within 30 days
- **Low:** Fix during regular maintenance

#### Check for Supply Chain Attacks

**Verify lockfile integrity:**
```yaml
precision_exec:
  commands:
    - cmd: "npm audit signatures"
      timeout_ms: 30000
  verbosity: standard
```

**Checklist:**
- Commit lockfiles (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`)
- Review dependency changes in PRs
- Use `npm ci` in CI/CD (not `npm install`)
- Pin dependency versions in critical projects
- Use tools like Socket.dev for dependency analysis

### Phase 7: API Security Audit

**Objective:** Secure API endpoints against common attacks.

#### Check for Rate Limiting

**Search for rate limiting implementation:**
```yaml
precision_grep:
  queries:
    - id: rate_limit_usage
      pattern: "(rateLimit|rate.*limiter|Ratelimit|upstash.*ratelimit)"
      glob: "**/*.{ts,tsx,js,jsx}"
  output:
    format: minimal
```

**Implement rate limiting:**
```typescript
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';
import { NextResponse } from 'next/server';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '10 s'), // 10 requests per 10 seconds
  analytics: true,
});

export async function POST(req: Request) {
  const ip = req.headers.get('x-forwarded-for') ?? 'unknown';
  const { success, limit, reset, remaining } = await ratelimit.limit(ip);

  if (!success) {
    return NextResponse.json(
      { error: 'Too many requests' },
      { 
        status: 429,
        headers: {
          'X-RateLimit-Limit': limit.toString(),
          'X-RateLimit-Remaining': remaining.toString(),
          'X-RateLimit-Reset': new Date(reset).toISOString(),
        },
      }
    );
  }

  // Process request
  return NextResponse.json({ success: true });
}
```

#### Check for CORS Configuration

**Search for CORS setup:**
```yaml
precision_grep:
  queries:
    - id: cors_config
      pattern: "(Access-Control-Allow-Origin|cors\\(|corsOptions)"
      glob: "**/*.{ts,tsx,js,jsx}"
  output:
    format: matches
```

**Common vulnerabilities:**
- Wildcard CORS (`Access-Control-Allow-Origin: *`) with credentials
- Overly permissive origin whitelist
- Missing preflight request handling

**Secure CORS configuration:**
```typescript
import { NextResponse } from 'next/server';

const ALLOWED_ORIGINS = [
  'https://example.com',
  'https://app.example.com',
];

export async function GET(req: Request) {
  const origin = req.headers.get('origin');
  
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };
  
  if (origin && ALLOWED_ORIGINS.includes(origin)) {
    headers['Access-Control-Allow-Origin'] = origin;
    headers['Access-Control-Allow-Credentials'] = 'true';
  }
  
  return NextResponse.json({ data: 'response' }, { headers });
}
```

#### Webhook Signature Verification

**Best practice:** Use `crypto.timingSafeEqual()` for comparing webhook signatures to prevent timing attacks:
```typescript
import crypto from 'crypto';

export function verifyWebhookSignature(payload: string, signature: string, secret: string): boolean {
  const expectedSignature = crypto.createHmac('sha256', secret).update(payload).digest('hex');
  const signatureBuffer = Buffer.from(signature);
  const expectedBuffer = Buffer.from(expectedSignature);
  
  // Prevent timing attacks - constant-time comparison
  if (signatureBuffer.length !== expectedBuffer.length) return false;
  return crypto.timingSafeEqual(signatureBuffer, expectedBuffer);
}
```

#### CORS Preflight Handling

```typescript
export async function OPTIONS(req: Request) {
  const origin = req.headers.get('origin');
  
  const headers: Record<string, string> = {
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Max-Age': '86400', // 24 hours
  };
  
  if (origin && ALLOWED_ORIGINS.includes(origin)) {
    headers['Access-Control-Allow-Origin'] = origin;
    headers['Access-Control-Allow-Credentials'] = 'true';
  }
  
  return new NextResponse(null, { status: 204, headers });
}
```

#### Check for CSRF Protection

**Search for CSRF implementation:**
```yaml
precision_grep:
  queries:
    - id: csrf_tokens
      pattern: "(csrf|csrfToken|xsrf)"
      glob: "**/*.{ts,tsx,js,jsx}"
  output:
    format: minimal
```

**CSRF protection strategies:**
- Use SameSite cookies (`sameSite: 'strict'` or `'lax'`)
- Implement CSRF tokens for state-changing operations
- Require custom headers for API requests (e.g., `X-Requested-With`)
- Verify `Origin` and `Referer` headers

#### Check for Content Security Policy (CSP)

**Search for CSP headers:**
```yaml
precision_grep:
  queries:
    - id: csp_headers
      pattern: "Content-Security-Policy"
      glob: "**/*.{ts,tsx,js,jsx,json}"
  output:
    format: locations
```

**Implement CSP:**
```typescript
// next.config.js
const ContentSecurityPolicy = `
  default-src 'self';
  // WARNING: 'unsafe-eval' and 'unsafe-inline' significantly weaken CSP. Use nonces or hashes instead.
  script-src 'self' 'unsafe-eval' 'unsafe-inline' https://cdn.vercel-insights.com;
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  font-src 'self' data:;
  connect-src 'self' https://api.example.com;
  frame-ancestors 'none';
  base-uri 'self';
  form-action 'self';
`;

module.exports = {
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'Content-Security-Policy',
            value: ContentSecurityPolicy.replace(/\n/g, ''),
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
          {
            key: 'Permissions-Policy',
            value: 'camera=(), microphone=(), geolocation=()',
          },
        ],
      },
    ];
  },
};
```

### Phase 8: Infrastructure Security Audit

**Objective:** Harden deployment infrastructure.

#### Check Docker Security

**Search for Dockerfile:**
```yaml
precision_read:
  files:
    - path: "Dockerfile"
      extract: content
  verbosity: minimal
```

**Docker security checklist:**
- Use minimal base images (alpine, distroless)
- Run as non-root user
- Multi-stage builds to reduce attack surface
- No secrets in image layers (use build args)
- Pin base image versions (avoid `latest` tag)
- Scan images for vulnerabilities (`docker scan`, Trivy)

**Secure Dockerfile:**
```dockerfile
FROM node:20-alpine AS base

FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app/public ./public

USER nextjs

EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/api/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"

CMD ["node", "server.js"]
```

#### Check Environment Variable Security

**Search for env file usage:**
```yaml
precision_glob:
  patterns:
    - ".env*"
    - "*.env"
  verbosity: count_only
```

**Verify .gitignore:**
```yaml
precision_read:
  files:
    - path: ".gitignore"
      extract: content
  verbosity: minimal
```

**Environment security checklist:**
- `.env` files in `.gitignore`
- Use `.env.example` (without values) to document variables
- Use secrets management in production (not `.env` files)
- Separate environments (development, staging, production)
- Rotate secrets regularly

#### Check TLS Configuration

**Verify HTTPS enforcement:**
```yaml
precision_grep:
  queries:
    - id: https_redirect
      pattern: "(https|ssl|tls|hsts|Strict-Transport-Security)"
      glob: "**/*.{ts,tsx,js,jsx,json}"
  output:
    format: minimal
```

**TLS best practices:**
- Enforce HTTPS (redirect HTTP to HTTPS)
- Enable HSTS (Strict-Transport-Security)
- Use TLS 1.2+ (disable TLS 1.0, 1.1)
- Use strong cipher suites
- Implement certificate pinning for mobile apps

## Audit Reporting

Structure your audit findings in this format:

### Executive Summary

```markdown
## Security Audit Report

**Application:** [Name]
**Audit Date:** [Date]
**Auditor:** [Name/Team]
**Scope:** [Components audited]

### Summary
- Total findings: X
- Critical: Y
- High: Z
- Medium: A
- Low: B

### Risk Assessment
[Overall risk level: Critical/High/Medium/Low]
```

### Detailed Findings

For each vulnerability:

```markdown
### [SEVERITY] Finding #X: [Title]

**Category:** [Authentication/Authorization/Input Validation/etc.]
**Severity:** [Critical/High/Medium/Low]
**CWE:** [CWE-XXX if applicable]

**Description:**
[Clear description of the vulnerability]

**Location:**
- File: `path/to/file.ts`
- Lines: 42-58

**Impact:**
[What can an attacker do? What data is at risk?]

**Proof of Concept:**
```typescript
// Example exploit code or reproduction steps
```

**Remediation:**
```typescript
// Secure code example
```

**References:**
- [OWASP Link]
- [CWE Link]
```

### Severity Classification

| Severity | Criteria |
|----------|----------|
| **Critical** | Remote code execution, authentication bypass, sensitive data exposure |
| **High** | Privilege escalation, SQL injection, XSS in critical flows |
| **Medium** | Information disclosure, CSRF, weak authentication |
| **Low** | Minor information leaks, missing security headers |

## Precision Tool Workflows

### Full Security Scan Workflow

Run a comprehensive security scan using precision_grep:

```yaml
precision_grep:
  queries:
    # Authentication issues
    - id: weak_auth
      pattern: "(password.*plain|password.*clear|md5|sha1)\\("
      glob: "**/*.{ts,tsx,js,jsx}"
    
    # SQL injection
    - id: sql_injection
      pattern: "(\\$queryRaw|\\$executeRaw).*\\$\\{|query.*\\+.*params"
      glob: "**/*.{ts,tsx,js,jsx}"
    
    # XSS
    - id: xss
      pattern: "(dangerouslySetInnerHTML|innerHTML|v-html)"
      glob: "**/*.{tsx,jsx,vue}"
    
    # Command injection
    - id: command_injection
      pattern: "(exec|spawn).*\\(.*req\\.(body|query)"
      glob: "**/*.{ts,tsx,js,jsx}"
    
    # Path traversal
    - id: path_traversal
      pattern: "(readFile|writeFile).*req\\.(body|query|params)"
      glob: "**/*.{ts,tsx,js,jsx}"
    
    # Hardcoded secrets
    - id: hardcoded_secrets
      pattern: "(api.*key.*=.*[\"'][a-zA-Z0-9]{20,}|sk_live)"
      glob: "**/*.{ts,tsx,js,jsx}"
    
    # Insecure cookies
    - id: insecure_cookies
      pattern: "(httpOnly.*false|secure.*false|sameSite.*none)"
      glob: "**/*.{ts,tsx,js,jsx}"
  
  output:
    format: locations
```

### Batch Security Audit

Use discover + batch for efficient auditing:

```yaml
discover:
  queries:
    - id: auth_files
      type: glob
      patterns: ["**/auth/**/*.{ts,tsx,js,jsx}", "**/api/auth/**/*.{ts,tsx,js,jsx}"]
    - id: api_routes
      type: glob
      patterns: ["**/api/**/*.{ts,tsx,js,jsx}"]
    - id: db_files
      type: grep
      pattern: "(prisma|db|database)"
      glob: "**/*.{ts,tsx,js,jsx}"
  verbosity: files_only
```

Then batch read and analyze:

```yaml
precision_read:
  files: [/* Use discovered files */]
  extract: symbols
  symbol_filter: ["function", "class"]
  verbosity: standard
```

## Automated Security Testing

Integrate security checks into CI/CD:

```yaml
# .github/workflows/security.yml
name: Security Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run npm audit
        run: npm audit --audit-level=high
      
      - name: Run Snyk security scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
      
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          severity: 'CRITICAL,HIGH'
      
      - name: Run OWASP ZAP scan
        uses: zaproxy/action-baseline@v0.7.0
        with:
          target: 'http://localhost:3000'
```

## Common Security Mistakes

### 1. Trusting Client-Side Validation

**Problem:** Relying on client-side checks for security.

**Solution:** Always validate on the server.

```typescript
// UNSAFE - Client-side only
export function ClientForm() {
  const [email, setEmail] = useState('');
  
  const isValid = email.includes('@');
  
  return (
    <form onSubmit={() => fetch('/api/subscribe', {
      method: 'POST',
      body: JSON.stringify({ email }),
    })}>
      <input value={email} onChange={(e) => setEmail(e.target.value)} />
      <button disabled={!isValid}>Subscribe</button>
    </form>
  );
}

// SAFE - Server-side validation
export async function POST(req: Request) {
  const body = await req.json();
  
  const schema = z.object({
    email: z.string().email(),
  });
  
  const result = schema.safeParse(body);
  
  if (!result.success) {
    return NextResponse.json(
      { error: result.error.flatten() },
      { status: 400 }
    );
  }
  
  // Process valid email
  await subscribeUser(result.data.email);
  return NextResponse.json({ success: true });
}
```

### 2. Exposing Sensitive Data in API Responses

**Problem:** Returning more data than needed.

**Solution:** Use explicit `select` to limit fields.

```typescript
// UNSAFE - Returns password hash
export async function GET(req: Request) {
  const user = await db.user.findUnique({ where: { id: userId } });
  return NextResponse.json(user);
}

// SAFE - Excludes sensitive fields
export async function GET(req: Request) {
  const user = await db.user.findUnique({
    where: { id: userId },
    select: {
      id: true,
      name: true,
      email: true,
      avatar: true,
      // passwordHash excluded
    },
  });
  return NextResponse.json(user);
}
```

### 3. Logging Sensitive Data

**Problem:** Writing PII or secrets to logs.

**Solution:** Redact sensitive data before logging.

```typescript
// UNSAFE - Logs password
export async function login(email: string, password: string) {
  console.log('Login attempt:', { email, password });
  // ...
}

// SAFE - Redacts password
export async function login(email: string, password: string) {
  console.log('Login attempt:', { email, password: '[REDACTED]' });
  // ...
}
```

## Post-Audit Actions

After completing the audit:

1. **Prioritize findings by severity and exploitability**
2. **Create tickets for each finding** (link to audit report)
3. **Fix critical/high issues immediately**
4. **Run validation script** to verify remediations
5. **Schedule follow-up audit** after fixes
6. **Update security documentation** with lessons learned
7. **Train team** on common vulnerabilities found

## Validation

Run the validation script after audit remediation:

```bash
./scripts/validate-security-audit.sh /path/to/project
```

The script checks for:
- Common vulnerability patterns
- Secure authentication implementation
- Input validation coverage
- Secrets management
- Security headers configuration
- Dependency vulnerabilities

## Further Reading

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [SANS Top 25 Software Errors](https://www.sans.org/top25-software-errors/)
