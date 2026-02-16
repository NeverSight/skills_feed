---
name: security-practices
description: OWASP Top 10, authentication, and secure coding practices
domain: software-engineering
version: 1.0.0
tags: [security, owasp, authentication, authorization, encryption, xss, csrf]
triggers:
  keywords:
    primary: [security, owasp, authentication, authorization, encryption, vulnerability]
    secondary: [xss, csrf, sql injection, jwt, oauth, cors, sanitize, validate]
  context_boost: [secure, protect, attack, hack]
  context_penalty: [design, ui, ux]
  priority: high
---

# Security Practices

## Overview

Essential security practices for application development. Covers OWASP Top 10 and secure coding guidelines.

---

## OWASP Top 10

### 1. Injection (SQL, NoSQL, Command)

```typescript
// ❌ SQL Injection vulnerable
const query = `SELECT * FROM users WHERE email = '${email}'`;
// Attack: email = "'; DROP TABLE users; --"

// ✅ Parameterized query
const result = await db.query(
  'SELECT * FROM users WHERE email = $1',
  [email]
);

// ✅ ORM with parameterization
const user = await prisma.user.findUnique({
  where: { email }
});

// ❌ Command injection vulnerable
exec(`ping ${userInput}`);
// Attack: userInput = "google.com; rm -rf /"

// ✅ Use arrays, not string concatenation
execFile('ping', ['-c', '4', hostname]);
```

### 2. Broken Authentication

```typescript
// Strong password requirements
const passwordSchema = z.string()
  .min(12)
  .regex(/[A-Z]/, 'Must contain uppercase')
  .regex(/[a-z]/, 'Must contain lowercase')
  .regex(/[0-9]/, 'Must contain number')
  .regex(/[^A-Za-z0-9]/, 'Must contain special character');

// Secure password hashing
import argon2 from 'argon2';

async function hashPassword(password: string): Promise<string> {
  return argon2.hash(password, {
    type: argon2.argon2id,
    memoryCost: 65536,  // 64 MB
    timeCost: 3,
    parallelism: 4
  });
}

async function verifyPassword(hash: string, password: string): Promise<boolean> {
  return argon2.verify(hash, password);
}

// Rate limiting login attempts
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts
  message: 'Too many login attempts'
});

app.post('/login', loginLimiter, handleLogin);
```

### 3. Cross-Site Scripting (XSS)

```typescript
// ❌ Direct HTML insertion
element.innerHTML = userInput;
// Attack: userInput = "<script>stealCookies()</script>"

// ✅ Use textContent for text
element.textContent = userInput;

// ✅ React auto-escapes by default
function UserName({ name }: { name: string }) {
  return <span>{name}</span>; // Safe
}

// ⚠️ dangerouslySetInnerHTML requires sanitization
import DOMPurify from 'dompurify';

function RichContent({ html }: { html: string }) {
  const sanitized = DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p'],
    ALLOWED_ATTR: ['href']
  });

  return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;
}

// Content Security Policy header
app.use((req, res, next) => {
  res.setHeader('Content-Security-Policy',
    "default-src 'self'; " +
    "script-src 'self' 'unsafe-inline'; " +
    "style-src 'self' 'unsafe-inline'; " +
    "img-src 'self' data: https:;"
  );
  next();
});
```

### 4. Insecure Direct Object References

```typescript
// ❌ No authorization check
app.get('/api/documents/:id', async (req, res) => {
  const doc = await db.documents.findById(req.params.id);
  res.json(doc);
});
// Attack: User can access any document by guessing ID

// ✅ Verify ownership
app.get('/api/documents/:id', auth, async (req, res) => {
  const doc = await db.documents.findById(req.params.id);

  if (!doc) {
    return res.status(404).json({ error: 'Not found' });
  }

  if (doc.ownerId !== req.user.id && !req.user.isAdmin) {
    return res.status(403).json({ error: 'Forbidden' });
  }

  res.json(doc);
});

// ✅ Use UUIDs instead of sequential IDs
// Harder to guess, but still check authorization!
const docId = crypto.randomUUID();
```

### 5. Cross-Site Request Forgery (CSRF)

```typescript
// CSRF token middleware
import csrf from 'csurf';

const csrfProtection = csrf({ cookie: true });

app.get('/form', csrfProtection, (req, res) => {
  res.render('form', { csrfToken: req.csrfToken() });
});

app.post('/submit', csrfProtection, (req, res) => {
  // Token automatically validated
  // ...
});

// In form
<form action="/submit" method="POST">
  <input type="hidden" name="_csrf" value="{{csrfToken}}" />
  <!-- form fields -->
</form>

// SameSite cookies
res.cookie('sessionId', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict' // or 'lax'
});
```

---

## Authentication

### JWT Best Practices

```typescript
import jwt from 'jsonwebtoken';

// Access token (short-lived)
function generateAccessToken(user: User): string {
  return jwt.sign(
    { sub: user.id, role: user.role },
    process.env.JWT_SECRET!,
    { expiresIn: '15m' }
  );
}

// Refresh token (long-lived, stored securely)
function generateRefreshToken(user: User): string {
  const token = jwt.sign(
    { sub: user.id, type: 'refresh' },
    process.env.JWT_REFRESH_SECRET!,
    { expiresIn: '7d' }
  );

  // Store in database to allow revocation
  db.refreshTokens.create({
    userId: user.id,
    token: hashToken(token),
    expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
  });

  return token;
}

// Verify and refresh
async function refreshAccessToken(refreshToken: string) {
  const payload = jwt.verify(refreshToken, process.env.JWT_REFRESH_SECRET!);

  // Check if token is revoked
  const storedToken = await db.refreshTokens.findOne({
    userId: payload.sub,
    token: hashToken(refreshToken)
  });

  if (!storedToken) {
    throw new Error('Token revoked');
  }

  const user = await db.users.findById(payload.sub);
  return generateAccessToken(user);
}
```

### OAuth 2.0 / OIDC

```typescript
import { OAuth2Client } from 'google-auth-library';

const client = new OAuth2Client(
  process.env.GOOGLE_CLIENT_ID,
  process.env.GOOGLE_CLIENT_SECRET,
  'https://myapp.com/auth/google/callback'
);

// Generate auth URL
app.get('/auth/google', (req, res) => {
  const url = client.generateAuthUrl({
    scope: ['openid', 'email', 'profile'],
    state: generateState(req.session.id) // CSRF protection
  });
  res.redirect(url);
});

// Handle callback
app.get('/auth/google/callback', async (req, res) => {
  const { code, state } = req.query;

  // Verify state
  if (!verifyState(state, req.session.id)) {
    return res.status(400).send('Invalid state');
  }

  // Exchange code for tokens
  const { tokens } = await client.getToken(code);

  // Verify ID token
  const ticket = await client.verifyIdToken({
    idToken: tokens.id_token,
    audience: process.env.GOOGLE_CLIENT_ID
  });

  const payload = ticket.getPayload();

  // Create or update user
  const user = await upsertUser({
    email: payload.email,
    name: payload.name,
    picture: payload.picture
  });

  // Create session
  req.session.userId = user.id;
  res.redirect('/dashboard');
});
```

---

## Authorization

### Role-Based Access Control (RBAC)

```typescript
// Define permissions
const PERMISSIONS = {
  admin: ['read', 'write', 'delete', 'admin'],
  editor: ['read', 'write'],
  viewer: ['read']
} as const;

// Middleware
function requirePermission(permission: string) {
  return (req: Request, res: Response, next: NextFunction) => {
    const userPermissions = PERMISSIONS[req.user.role] || [];

    if (!userPermissions.includes(permission)) {
      return res.status(403).json({ error: 'Forbidden' });
    }

    next();
  };
}

// Usage
app.delete('/api/posts/:id', auth, requirePermission('delete'), deletePost);
```

### Attribute-Based Access Control (ABAC)

```typescript
interface Policy {
  effect: 'allow' | 'deny';
  resource: string;
  action: string;
  condition?: (context: Context) => boolean;
}

const policies: Policy[] = [
  {
    effect: 'allow',
    resource: 'document',
    action: 'read',
    condition: (ctx) => ctx.resource.isPublic || ctx.user.id === ctx.resource.ownerId
  },
  {
    effect: 'allow',
    resource: 'document',
    action: 'write',
    condition: (ctx) => ctx.user.id === ctx.resource.ownerId
  },
  {
    effect: 'allow',
    resource: '*',
    action: '*',
    condition: (ctx) => ctx.user.role === 'admin'
  }
];

function isAllowed(user: User, action: string, resource: Resource): boolean {
  const context = { user, resource };

  for (const policy of policies) {
    if (
      (policy.resource === '*' || policy.resource === resource.type) &&
      (policy.action === '*' || policy.action === action)
    ) {
      if (!policy.condition || policy.condition(context)) {
        return policy.effect === 'allow';
      }
    }
  }

  return false; // Deny by default
}
```

---

## Secrets Management

```typescript
// ❌ Never hardcode secrets
const apiKey = 'sk_live_1234567890';

// ✅ Use environment variables
const apiKey = process.env.API_KEY;

// ✅ Use secret managers
import { SecretManagerServiceClient } from '@google-cloud/secret-manager';

const client = new SecretManagerServiceClient();

async function getSecret(name: string): Promise<string> {
  const [version] = await client.accessSecretVersion({
    name: `projects/my-project/secrets/${name}/versions/latest`
  });

  return version.payload.data.toString();
}

// ✅ Rotate secrets regularly
// Store secret versions, not raw secrets
// Use short-lived tokens where possible
```

---

## Input Validation

```typescript
import { z } from 'zod';

// Define strict schemas
const createUserSchema = z.object({
  email: z.string().email().max(255),
  name: z.string().min(1).max(100).regex(/^[\w\s-]+$/),
  age: z.number().int().min(0).max(150).optional()
});

// Validate at boundaries
app.post('/api/users', async (req, res) => {
  const result = createUserSchema.safeParse(req.body);

  if (!result.success) {
    return res.status(400).json({
      error: 'Validation failed',
      details: result.error.flatten()
    });
  }

  // result.data is typed and validated
  const user = await createUser(result.data);
  res.json(user);
});

// File upload validation
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp'];

function validateFile(file: Express.Multer.File) {
  if (file.size > MAX_FILE_SIZE) {
    throw new Error('File too large');
  }

  if (!ALLOWED_TYPES.includes(file.mimetype)) {
    throw new Error('Invalid file type');
  }

  // Also check magic bytes, not just extension
  const fileType = await fileTypeFromBuffer(file.buffer);
  if (!fileType || !ALLOWED_TYPES.includes(fileType.mime)) {
    throw new Error('Invalid file content');
  }
}
```

---

## Security Headers

```typescript
import helmet from 'helmet';

app.use(helmet());

// Or configure individually
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'", "'unsafe-inline'"],
    styleSrc: ["'self'", "'unsafe-inline'"],
    imgSrc: ["'self'", "data:", "https:"],
    connectSrc: ["'self'", "https://api.example.com"],
    fontSrc: ["'self'"],
    objectSrc: ["'none'"],
    frameAncestors: ["'none'"]
  }
}));

app.use(helmet.hsts({
  maxAge: 31536000,
  includeSubDomains: true,
  preload: true
}));
```

---

## Related Skills

- [[authentication]] - Auth patterns
- [[api-design]] - API security
- [[devops-cicd]] - Security in pipelines
