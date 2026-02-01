---
name: auth
description: |
  Authentication and authorization patterns including OAuth2, JWT, RBAC/ABAC, session management, API keys, password hashing, and MFA.

  USE WHEN: Implementing login flows, access control, identity management, tokens, permissions, session handling, API key authentication, or MFA.
  DO NOT USE: For security vulnerability scanning (use /security-scan), for security audits (use /security-audit), for threat modeling (use /threat-model).

  TRIGGERS: login, logout, signin, signup, authentication, authorization, password, credential, token, JWT, OAuth, OAuth2, OIDC, SSO, SAML, session, cookie, RBAC, ABAC, permissions, roles, MFA, 2FA, TOTP, API key, PKCE.
triggers:
  - login
  - logout
  - signin
  - signup
  - register
  - authentication
  - authorization
  - password
  - credential
  - token
  - JWT
  - OAuth
  - OAuth2
  - OIDC
  - OpenID
  - SSO
  - SAML
  - session
  - cookie
  - refresh token
  - access token
  - bearer
  - authorization header
  - auth header
  - 401
  - 403
  - forbidden
  - unauthorized
  - RBAC
  - ABAC
  - permissions
  - roles
  - access control
  - identity
  - MFA
  - 2FA
  - two-factor
  - multi-factor
  - TOTP
  - API key
  - auth flow
  - PKCE
  - client credentials
---

# Authentication & Authorization

## Overview

This skill covers comprehensive authentication and authorization strategies for modern applications. It includes identity verification (authentication), access control (authorization), and secure credential management across web, mobile, and API contexts.

## When to Use

**software-engineer (Sonnet)** - Use when:

- Implementing standard auth flows (login, logout, password reset)
- Adding JWT or session handling to existing applications
- Implementing RBAC/ABAC patterns with defined requirements
- Integrating with established OAuth2 providers
- Adding MFA or API key authentication

**senior-software-engineer (Opus)** - Escalate to when:

- Designing auth architecture from scratch
- Choosing between authentication strategies (JWT vs sessions, OAuth flows)
- Evaluating trade-offs between different access control models
- Planning token rotation, refresh strategies, or session lifecycle
- Making cross-cutting security decisions

**senior-software-engineer (Opus)** - Request review when:

- Implementing password hashing or credential storage
- Handling sensitive tokens (refresh tokens, API keys)
- Implementing rate limiting or brute force protection
- Adding MFA or step-up authentication
- Dealing with PII, compliance, or regulatory requirements
- ANY authentication/authorization implementation before production
- Setting up identity providers (Keycloak, Auth0, Cognito)
- Configuring SSO, SAML, or OIDC integrations
- Scaling session storage (Redis clusters, distributed sessions)
- Managing secrets, key rotation infrastructure
- Setting up certificate management for JWT signing

## Key Concepts

### OAuth2 Flows

**Authorization Code Flow** - Best for server-side applications:

```typescript
// 1. Redirect user to authorization server
const authUrl = new URL("https://auth.example.com/authorize");
authUrl.searchParams.set("response_type", "code");
authUrl.searchParams.set("client_id", CLIENT_ID);
authUrl.searchParams.set("redirect_uri", REDIRECT_URI);
authUrl.searchParams.set("scope", "openid profile email");
authUrl.searchParams.set("state", generateSecureState());

// 2. Exchange code for tokens (server-side)
async function exchangeCode(code: string): Promise<TokenResponse> {
  const response = await fetch("https://auth.example.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      grant_type: "authorization_code",
      code,
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
      redirect_uri: REDIRECT_URI,
    }),
  });
  return response.json();
}
```

**PKCE Flow** - Required for public clients (SPAs, mobile apps):

```typescript
// Generate code verifier and challenge
function generatePKCE(): { verifier: string; challenge: string } {
  const verifier = base64UrlEncode(crypto.getRandomValues(new Uint8Array(32)));
  const challenge = base64UrlEncode(
    await crypto.subtle.digest("SHA-256", new TextEncoder().encode(verifier)),
  );
  return { verifier, challenge };
}

// Include in authorization request
authUrl.searchParams.set("code_challenge", challenge);
authUrl.searchParams.set("code_challenge_method", "S256");

// Include verifier in token exchange
body.set("code_verifier", verifier);
```

**Client Credentials Flow** - For service-to-service communication:

```typescript
async function getServiceToken(): Promise<string> {
  const response = await fetch("https://auth.example.com/token", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Authorization: `Basic ${btoa(`${CLIENT_ID}:${CLIENT_SECRET}`)}`,
    },
    body: new URLSearchParams({
      grant_type: "client_credentials",
      scope: "api:read api:write",
    }),
  });
  return (await response.json()).access_token;
}
```

### JWT Handling

**Token Structure and Signing**:

```typescript
import jwt from "jsonwebtoken";

interface TokenPayload {
  sub: string; // Subject (user ID)
  iss: string; // Issuer
  aud: string; // Audience
  exp: number; // Expiration
  iat: number; // Issued at
  roles: string[]; // Custom claims
}

// Sign with RS256 (asymmetric - recommended for production)
function signToken(payload: Omit<TokenPayload, "iat" | "exp">): string {
  return jwt.sign(
    { ...payload, iat: Math.floor(Date.now() / 1000) },
    PRIVATE_KEY,
    {
      algorithm: "RS256",
      expiresIn: "15m",
      issuer: "https://api.example.com",
      audience: "https://app.example.com",
    },
  );
}

// Verify token
function verifyToken(token: string): TokenPayload {
  return jwt.verify(token, PUBLIC_KEY, {
    algorithms: ["RS256"],
    issuer: "https://api.example.com",
    audience: "https://app.example.com",
  }) as TokenPayload;
}
```

**Refresh Token Pattern**:

```typescript
interface TokenPair {
  accessToken: string; // Short-lived (15 min)
  refreshToken: string; // Long-lived (7 days), stored securely
}

async function refreshTokens(refreshToken: string): Promise<TokenPair> {
  // Validate refresh token exists in database (allows revocation)
  const storedToken = await db.refreshTokens.findUnique({
    where: { token: hashToken(refreshToken) },
  });

  if (!storedToken || storedToken.expiresAt < new Date()) {
    throw new UnauthorizedError("Invalid refresh token");
  }

  // Rotate refresh token (one-time use)
  await db.refreshTokens.delete({ where: { id: storedToken.id } });

  const newRefreshToken = generateSecureToken();
  await db.refreshTokens.create({
    data: {
      token: hashToken(newRefreshToken),
      userId: storedToken.userId,
      expiresAt: addDays(new Date(), 7),
    },
  });

  return {
    accessToken: signToken({ sub: storedToken.userId, roles: [] }),
    refreshToken: newRefreshToken,
  };
}
```

### RBAC (Role-Based Access Control)

```typescript
// Define roles and permissions
const ROLES = {
  admin: [
    "users:read",
    "users:write",
    "users:delete",
    "reports:read",
    "settings:write",
  ],
  manager: ["users:read", "users:write", "reports:read"],
  user: ["users:read:own", "reports:read:own"],
} as const;

type Role = keyof typeof ROLES;
type Permission = (typeof ROLES)[Role][number];

// Middleware for permission checking
function requirePermission(permission: Permission) {
  return (req: Request, res: Response, next: NextFunction) => {
    const userRoles: Role[] = req.user.roles;
    const userPermissions = userRoles.flatMap((role) => ROLES[role]);

    // Handle :own suffix for resource-level permissions
    const [resource, action, scope] = permission.split(":");
    const basePermission = `${resource}:${action}`;

    const hasPermission =
      userPermissions.includes(permission) ||
      (scope === "own" && userPermissions.includes(basePermission));

    if (!hasPermission) {
      return res.status(403).json({ error: "Forbidden" });
    }
    next();
  };
}

// Usage
app.delete("/users/:id", requirePermission("users:delete"), deleteUser);
```

### ABAC (Attribute-Based Access Control)

```typescript
interface PolicyContext {
  subject: { id: string; roles: string[]; department: string };
  resource: { type: string; owner: string; classification: string };
  action: string;
  environment: { time: Date; ip: string };
}

type Policy = (ctx: PolicyContext) => boolean;

const policies: Policy[] = [
  // Users can access their own resources
  (ctx) => ctx.resource.owner === ctx.subject.id,

  // Managers can access resources in their department
  (ctx) =>
    ctx.subject.roles.includes("manager") &&
    ctx.resource.department === ctx.subject.department,

  // No access to confidential resources outside business hours
  (ctx) => {
    if (ctx.resource.classification === "confidential") {
      const hour = ctx.environment.time.getHours();
      return hour >= 9 && hour < 17;
    }
    return true;
  },
];

function checkAccess(ctx: PolicyContext): boolean {
  return policies.every((policy) => policy(ctx));
}
```

### Session Management

```typescript
import { Redis } from "ioredis";

const redis = new Redis();
const SESSION_TTL = 24 * 60 * 60; // 24 hours

interface Session {
  userId: string;
  createdAt: number;
  lastActivity: number;
  userAgent: string;
  ip: string;
}

async function createSession(userId: string, req: Request): Promise<string> {
  const sessionId = crypto.randomUUID();
  const session: Session = {
    userId,
    createdAt: Date.now(),
    lastActivity: Date.now(),
    userAgent: req.headers["user-agent"] || "",
    ip: req.ip,
  };

  await redis.setex(
    `session:${sessionId}`,
    SESSION_TTL,
    JSON.stringify(session),
  );
  await redis.sadd(`user-sessions:${userId}`, sessionId);

  return sessionId;
}

async function validateSession(sessionId: string): Promise<Session | null> {
  const data = await redis.get(`session:${sessionId}`);
  if (!data) return null;

  const session: Session = JSON.parse(data);

  // Update last activity
  session.lastActivity = Date.now();
  await redis.setex(
    `session:${sessionId}`,
    SESSION_TTL,
    JSON.stringify(session),
  );

  return session;
}

async function invalidateAllUserSessions(userId: string): Promise<void> {
  const sessionIds = await redis.smembers(`user-sessions:${userId}`);
  if (sessionIds.length > 0) {
    await redis.del(...sessionIds.map((id) => `session:${id}`));
    await redis.del(`user-sessions:${userId}`);
  }
}
```

### API Key Strategies

```typescript
interface ApiKey {
  id: string;
  prefix: string; // First 8 chars (for identification)
  hash: string; // Hashed key
  name: string;
  scopes: string[];
  rateLimit: number;
  expiresAt: Date | null;
  lastUsedAt: Date | null;
}

// Generate API key with prefix for easy identification
function generateApiKey(): { key: string; prefix: string; hash: string } {
  const key = `sk_live_${crypto.randomBytes(32).toString("base64url")}`;
  return {
    key,
    prefix: key.substring(0, 16),
    hash: crypto.createHash("sha256").update(key).digest("hex"),
  };
}

// Validate and rate limit
async function validateApiKey(key: string): Promise<ApiKey> {
  const hash = crypto.createHash("sha256").update(key).digest("hex");
  const apiKey = await db.apiKeys.findUnique({ where: { hash } });

  if (!apiKey) throw new UnauthorizedError("Invalid API key");
  if (apiKey.expiresAt && apiKey.expiresAt < new Date()) {
    throw new UnauthorizedError("API key expired");
  }

  // Check rate limit
  const rateLimitKey = `ratelimit:${apiKey.id}`;
  const requests = await redis.incr(rateLimitKey);
  if (requests === 1) await redis.expire(rateLimitKey, 60);
  if (requests > apiKey.rateLimit) {
    throw new TooManyRequestsError("Rate limit exceeded");
  }

  // Update last used (async, don't wait)
  db.apiKeys.update({
    where: { id: apiKey.id },
    data: { lastUsedAt: new Date() },
  });

  return apiKey;
}
```

### Password Hashing

```typescript
import argon2 from "argon2";
import bcrypt from "bcrypt";

// Argon2 (recommended for new implementations)
async function hashPasswordArgon2(password: string): Promise<string> {
  return argon2.hash(password, {
    type: argon2.argon2id, // Hybrid mode
    memoryCost: 65536, // 64 MB
    timeCost: 3, // 3 iterations
    parallelism: 4, // 4 threads
  });
}

async function verifyPasswordArgon2(
  hash: string,
  password: string,
): Promise<boolean> {
  return argon2.verify(hash, password);
}

// bcrypt (widely supported)
const BCRYPT_ROUNDS = 12;

async function hashPasswordBcrypt(password: string): Promise<string> {
  return bcrypt.hash(password, BCRYPT_ROUNDS);
}

async function verifyPasswordBcrypt(
  hash: string,
  password: string,
): Promise<boolean> {
  return bcrypt.compare(password, hash);
}

// Password validation
function validatePasswordStrength(password: string): {
  valid: boolean;
  errors: string[];
} {
  const errors: string[] = [];

  if (password.length < 12)
    errors.push("Password must be at least 12 characters");
  if (!/[A-Z]/.test(password))
    errors.push("Password must contain uppercase letter");
  if (!/[a-z]/.test(password))
    errors.push("Password must contain lowercase letter");
  if (!/[0-9]/.test(password)) errors.push("Password must contain number");
  if (!/[^A-Za-z0-9]/.test(password))
    errors.push("Password must contain special character");

  return { valid: errors.length === 0, errors };
}
```

### MFA Implementation

```typescript
import { authenticator } from "otplib";
import QRCode from "qrcode";

// TOTP Setup
async function setupTOTP(
  userId: string,
  email: string,
): Promise<{ secret: string; qrCode: string }> {
  const secret = authenticator.generateSecret();
  const otpauth = authenticator.keyuri(email, "MyApp", secret);
  const qrCode = await QRCode.toDataURL(otpauth);

  // Store encrypted secret temporarily until verified
  await redis.setex(`mfa-setup:${userId}`, 600, encrypt(secret));

  return { secret, qrCode };
}

// Verify TOTP
function verifyTOTP(secret: string, token: string): boolean {
  return authenticator.verify({ token, secret });
}

// Backup codes generation
function generateBackupCodes(): { codes: string[]; hashes: string[] } {
  const codes = Array.from({ length: 10 }, () =>
    crypto.randomBytes(4).toString("hex").toUpperCase(),
  );
  const hashes = codes.map((code) =>
    crypto.createHash("sha256").update(code).digest("hex"),
  );
  return { codes, hashes };
}

// Complete MFA verification flow
async function verifyMFA(userId: string, code: string): Promise<boolean> {
  const user = await db.users.findUnique({
    where: { id: userId },
    include: { mfaSettings: true },
  });

  if (!user?.mfaSettings?.enabled) return true;

  // Try TOTP first
  if (verifyTOTP(decrypt(user.mfaSettings.totpSecret), code)) {
    return true;
  }

  // Try backup code
  const codeHash = crypto.createHash("sha256").update(code).digest("hex");
  const backupCode = user.mfaSettings.backupCodes.find(
    (bc) => bc.hash === codeHash && !bc.usedAt,
  );

  if (backupCode) {
    await db.backupCodes.update({
      where: { id: backupCode.id },
      data: { usedAt: new Date() },
    });
    return true;
  }

  return false;
}
```

## Security Considerations

**Critical Security Checklist** (for senior-software-engineer review):

1. **Credential Storage**
   - Never log passwords, tokens, or API keys
   - Hash passwords with Argon2id or bcrypt (12+ rounds)
   - Hash API keys before database storage
   - Encrypt refresh tokens and MFA secrets at rest
   - Never return sensitive data in error messages

2. **Token Security**
   - Validate ALL token claims (signature, exp, iss, aud, nbf)
   - Use RS256 or ES256 for JWT signatures (never HS256 in distributed systems)
   - Set minimum token expiration (access: 15 min, refresh: 7 days max)
   - Implement token revocation lists for logout
   - Use PKCE for all public clients (SPAs, mobile)

3. **Attack Prevention**
   - Implement rate limiting on auth endpoints (5 attempts per 15 min)
   - Account lockout after failed login attempts (10 failures = 30 min lockout)
   - Use timing-safe comparison for password/token validation
   - Prevent user enumeration (same error for invalid user/password)
   - Validate redirect URIs against allowlist (prevent open redirects)

4. **Session Security**
   - Set httpOnly, secure, sameSite=strict on cookies
   - Regenerate session ID after privilege escalation
   - Implement absolute timeout (24h) and idle timeout (30min)
   - Clear all sessions on password change
   - Detect and alert on concurrent sessions from different IPs

5. **Transport Security**
   - Require HTTPS for all auth endpoints (HSTS header)
   - Use secure WebSocket (wss://) for real-time auth
   - Validate Content-Type headers (prevent CSRF)
   - Set CORS policies restrictively

6. **Compliance & Privacy**
   - Log authentication events (login, logout, failures) for audit
   - Implement PII data retention policies
   - Support account deletion (GDPR right to erasure)
   - Provide data export (GDPR right to portability)
   - Consider SOC2, HIPAA, PCI-DSS requirements if applicable

**Common Vulnerabilities to Avoid**:

- Timing attacks (use crypto.timingSafeEqual)
- JWT algorithm confusion (always specify allowed algorithms)
- Session fixation (regenerate ID on login)
- Insecure direct object references (verify resource ownership)
- Mass assignment (validate all input fields)
- Broken access control (default deny, explicit allow)

## Best Practices

1. **Token Security**
   - Use short-lived access tokens (15 minutes or less)
   - Store refresh tokens securely (httpOnly cookies, encrypted storage)
   - Implement token rotation for refresh tokens
   - Always validate token signature, expiration, issuer, and audience

2. **Password Security**
   - Use Argon2id for new implementations
   - Never store plaintext passwords
   - Implement account lockout after failed attempts
   - Use secure password reset flows with time-limited tokens

3. **Session Security**
   - Regenerate session ID after authentication
   - Implement absolute and idle timeouts
   - Bind sessions to user agent/IP when appropriate
   - Provide session management UI for users

4. **API Key Security**
   - Hash API keys before storage
   - Use prefixes for key identification
   - Implement scopes and rate limiting
   - Allow key rotation without downtime

5. **MFA Best Practices**
   - Offer multiple MFA methods (TOTP, WebAuthn, SMS backup)
   - Provide backup codes during setup
   - Allow trusted device remembering
   - Require MFA re-verification for sensitive actions

## Examples

### Complete Login Flow with MFA

```typescript
async function login(
  email: string,
  password: string,
  mfaCode?: string,
): Promise<AuthResponse> {
  // Find user
  const user = await db.users.findUnique({ where: { email } });
  if (!user) throw new UnauthorizedError("Invalid credentials");

  // Check account lockout
  if (user.lockedUntil && user.lockedUntil > new Date()) {
    throw new UnauthorizedError("Account temporarily locked");
  }

  // Verify password
  const validPassword = await verifyPasswordArgon2(user.passwordHash, password);
  if (!validPassword) {
    await incrementFailedAttempts(user.id);
    throw new UnauthorizedError("Invalid credentials");
  }

  // Check MFA
  if (user.mfaEnabled) {
    if (!mfaCode) {
      return { requiresMfa: true, mfaToken: generateMfaToken(user.id) };
    }
    const validMfa = await verifyMFA(user.id, mfaCode);
    if (!validMfa) throw new UnauthorizedError("Invalid MFA code");
  }

  // Reset failed attempts
  await db.users.update({
    where: { id: user.id },
    data: { failedAttempts: 0, lockedUntil: null },
  });

  // Generate tokens
  const accessToken = signToken({ sub: user.id, roles: user.roles });
  const refreshToken = await createRefreshToken(user.id);

  return { accessToken, refreshToken };
}
```
