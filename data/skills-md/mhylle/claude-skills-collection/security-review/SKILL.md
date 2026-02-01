---
name: security-review
description: Comprehensive security audit for code changes. Use this skill when implementing authentication, authorization, user input handling, API endpoints, secrets/credentials, payment features, or file uploads. Provides security checklists, vulnerability patterns, and remediation guidance. Integrates with implement-phase as a security quality gate.
allowed-tools: Read, Glob, Grep, Bash
---

# Security Review Skill

This skill ensures all code follows security best practices and identifies potential vulnerabilities before they reach production.

## Design Philosophy

Security is not optional. This skill acts as a **security quality gate** that validates code against common vulnerability patterns (OWASP Top 10) and project-specific security requirements. One vulnerability can compromise the entire platform.

## When to Activate

Trigger this skill when code involves:

- **Authentication or authorization** - Login flows, session management, role checks
- **User input handling** - Forms, query parameters, file uploads
- **API endpoints** - New routes, especially public-facing
- **Secrets or credentials** - API keys, database connections, tokens
- **Payment features** - Financial transactions, billing, subscriptions
- **Sensitive data** - PII, health data, financial records
- **Third-party API integration** - External service connections
- **Database queries** - Especially raw SQL or dynamic queries

## Security Checklist

### 1. Secrets Management

#### BAD - Never Do This
```typescript
const apiKey = "sk-proj-xxxxx"  // Hardcoded secret
const dbPassword = "password123" // In source code
const config = {
  stripe_key: "sk_live_xxxxx"  // Committed to repo
}
```

#### GOOD - Always Do This
```typescript
const apiKey = process.env.OPENAI_API_KEY
const dbUrl = process.env.DATABASE_URL

// Verify secrets exist at startup
if (!apiKey) {
  throw new Error('OPENAI_API_KEY not configured')
}

// Use secret management services for production
// AWS Secrets Manager, HashiCorp Vault, etc.
```

#### Verification Checklist
- [ ] No hardcoded API keys, tokens, or passwords in source
- [ ] All secrets loaded from environment variables
- [ ] `.env`, `.env.local`, `.env.production` in .gitignore
- [ ] No secrets in git history (run `git log -p | grep -i "api_key\|secret\|password"`)
- [ ] Production secrets in secure secret management (Vercel, Railway, AWS SM)
- [ ] Different secrets for dev/staging/production environments

---

### 2. Input Validation

#### BAD - Never Trust User Input
```typescript
// DANGEROUS: No validation
async function createUser(req: Request) {
  const { email, name, role } = req.body
  return db.users.create({ email, name, role }) // role injection!
}

// DANGEROUS: Client-side only validation
if (formData.email.includes('@')) { /* good enough? NO */ }
```

#### GOOD - Validate Everything Server-Side
```typescript
import { z } from 'zod'

const CreateUserSchema = z.object({
  email: z.string().email().max(255),
  name: z.string().min(1).max(100).regex(/^[a-zA-Z\s]+$/),
  age: z.number().int().min(0).max(150).optional()
  // Note: role is NOT accepted from user input
})

export async function createUser(input: unknown) {
  const validated = CreateUserSchema.parse(input)
  return await db.users.create({
    ...validated,
    role: 'user' // Role set server-side, never from input
  })
}
```

#### File Upload Validation
```typescript
function validateFileUpload(file: File) {
  // Size check (5MB max)
  const maxSize = 5 * 1024 * 1024
  if (file.size > maxSize) {
    throw new Error('File too large (max 5MB)')
  }

  // MIME type check (verify actual content, not just header)
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif']
  if (!allowedTypes.includes(file.type)) {
    throw new Error('Invalid file type')
  }

  // Extension check (defense in depth)
  const allowedExtensions = ['.jpg', '.jpeg', '.png', '.gif']
  const extension = file.name.toLowerCase().match(/\.[^.]+$/)?.[0]
  if (!extension || !allowedExtensions.includes(extension)) {
    throw new Error('Invalid file extension')
  }

  // Sanitize filename
  const sanitizedName = file.name.replace(/[^a-zA-Z0-9.-]/g, '_')

  return { ...file, name: sanitizedName }
}
```

#### Verification Checklist
- [ ] All user inputs validated with schemas (zod, yup, joi)
- [ ] Validation happens server-side (client validation is UX only)
- [ ] File uploads restricted by size, type, and extension
- [ ] File contents verified (not just extensions)
- [ ] Whitelist validation preferred over blacklist
- [ ] Error messages don't leak sensitive information
- [ ] No direct use of user input in file paths or system commands

---

### 3. SQL Injection Prevention

#### BAD - Never Concatenate SQL
```typescript
// CRITICAL VULNERABILITY - SQL Injection
const query = `SELECT * FROM users WHERE email = '${userEmail}'`
await db.query(query)

// Also dangerous with template literals
const search = `SELECT * FROM products WHERE name LIKE '%${term}%'`
```

#### GOOD - Always Use Parameterized Queries
```typescript
// Safe - parameterized query with Supabase
const { data } = await supabase
  .from('users')
  .select('*')
  .eq('email', userEmail)

// Safe - parameterized raw SQL
await db.query(
  'SELECT * FROM users WHERE email = $1',
  [userEmail]
)

// Safe - ORM with proper escaping
const user = await prisma.user.findUnique({
  where: { email: userEmail }
})

// Safe - LIKE queries with parameterization
await db.query(
  'SELECT * FROM products WHERE name LIKE $1',
  [`%${term}%`]
)
```

#### Verification Checklist
- [ ] All database queries use parameterized queries or ORM
- [ ] No string concatenation or interpolation in SQL
- [ ] Query builders used correctly (not bypassed)
- [ ] Stored procedures use parameterized inputs
- [ ] Database user has minimal required permissions

---

### 4. Authentication & Authorization

#### BAD - Insecure Token Storage
```typescript
// WRONG: localStorage vulnerable to XSS
localStorage.setItem('token', token)
localStorage.setItem('user', JSON.stringify(user))

// WRONG: No authorization check
async function deleteUser(userId: string) {
  await db.users.delete({ where: { id: userId } }) // Anyone can delete!
}
```

#### GOOD - Secure Token Handling
```typescript
// CORRECT: httpOnly cookies (server-side)
res.setHeader('Set-Cookie', [
  `token=${token}; HttpOnly; Secure; SameSite=Strict; Max-Age=3600; Path=/`
])

// CORRECT: Authorization check before action
export async function deleteUser(userId: string, requesterId: string) {
  const requester = await db.users.findUnique({
    where: { id: requesterId },
    select: { id: true, role: true }
  })

  // Check ownership OR admin role
  if (requester.id !== userId && requester.role !== 'admin') {
    throw new ForbiddenError('Not authorized to delete this user')
  }

  await db.users.delete({ where: { id: userId } })
}
```

#### Row Level Security (Supabase/PostgreSQL)
```sql
-- Enable RLS on all tables with user data
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Users can only view their own data
CREATE POLICY "Users view own data"
  ON users FOR SELECT
  USING (auth.uid() = id);

-- Users can only update their own data
CREATE POLICY "Users update own data"
  ON users FOR UPDATE
  USING (auth.uid() = id);

-- Admin policy (if needed)
CREATE POLICY "Admins can view all"
  ON users FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM users WHERE id = auth.uid() AND role = 'admin'
    )
  );
```

#### Verification Checklist
- [ ] Tokens stored in httpOnly cookies (not localStorage/sessionStorage)
- [ ] Secure and SameSite flags set on cookies
- [ ] Authorization check before every sensitive operation
- [ ] Row Level Security enabled in database (Supabase)
- [ ] Role-based access control implemented correctly
- [ ] Session timeout configured appropriately
- [ ] Password reset tokens single-use and time-limited
- [ ] Failed login attempts tracked and limited

---

### 5. XSS Prevention

#### BAD - Rendering Unsanitized Content
```typescript
// DANGEROUS: Direct HTML injection
function Comment({ html }) {
  return <div dangerouslySetInnerHTML={{ __html: html }} />
}

// DANGEROUS: Eval-like functions
const userCode = getUserInput()
eval(userCode)
new Function(userCode)()
```

#### GOOD - Sanitize All User HTML
```typescript
import DOMPurify from 'isomorphic-dompurify'

function SafeComment({ html }: { html: string }) {
  const clean = DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'p', 'br'],
    ALLOWED_ATTR: [] // No attributes allowed
  })
  return <div dangerouslySetInnerHTML={{ __html: clean }} />
}

// Better: Use markdown instead of HTML
import { marked } from 'marked'
import DOMPurify from 'isomorphic-dompurify'

function MarkdownContent({ markdown }: { markdown: string }) {
  const html = marked(markdown)
  const clean = DOMPurify.sanitize(html)
  return <div dangerouslySetInnerHTML={{ __html: clean }} />
}
```

#### Content Security Policy
```typescript
// next.config.js
const securityHeaders = [
  {
    key: 'Content-Security-Policy',
    value: [
      "default-src 'self'",
      "script-src 'self'", // Remove 'unsafe-inline' 'unsafe-eval' if possible
      "style-src 'self' 'unsafe-inline'", // Needed for most CSS-in-JS
      "img-src 'self' data: https:",
      "font-src 'self'",
      "connect-src 'self' https://api.example.com",
      "frame-ancestors 'none'",
      "base-uri 'self'",
      "form-action 'self'"
    ].join('; ')
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff'
  },
  {
    key: 'X-Frame-Options',
    value: 'DENY'
  }
]
```

#### Verification Checklist
- [ ] All user-provided HTML sanitized with DOMPurify or similar
- [ ] dangerouslySetInnerHTML only used with sanitized content
- [ ] CSP headers configured and tested
- [ ] No eval(), new Function(), or innerHTML with user data
- [ ] React's built-in XSS protection not bypassed unnecessarily
- [ ] URL parameters validated before use in links (javascript: protocol blocked)

---

### 6. CSRF Protection

#### BAD - No CSRF Protection
```typescript
// VULNERABLE: State-changing GET request
app.get('/api/delete-account', async (req, res) => {
  await deleteAccount(req.user.id)
})

// VULNERABLE: No CSRF token verification
app.post('/api/transfer', async (req, res) => {
  await transferMoney(req.body.amount, req.body.to)
})
```

#### GOOD - Implement CSRF Protection
```typescript
import { csrf } from '@/lib/csrf'

export async function POST(request: Request) {
  // Verify CSRF token from header
  const token = request.headers.get('X-CSRF-Token')

  if (!csrf.verify(token)) {
    return NextResponse.json(
      { error: 'Invalid CSRF token' },
      { status: 403 }
    )
  }

  // Process request
}

// Client-side: Include CSRF token in requests
fetch('/api/action', {
  method: 'POST',
  headers: {
    'X-CSRF-Token': csrfToken, // From meta tag or cookie
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(data)
})
```

#### SameSite Cookies (Primary Defense)
```typescript
// Modern browsers: SameSite provides CSRF protection
res.setHeader('Set-Cookie', [
  `session=${sessionId}; HttpOnly; Secure; SameSite=Strict; Path=/`
])
```

#### Verification Checklist
- [ ] All state-changing operations use POST/PUT/DELETE (not GET)
- [ ] CSRF tokens on forms and AJAX requests
- [ ] SameSite=Strict on all authentication cookies
- [ ] Origin header verified on sensitive endpoints
- [ ] Double-submit cookie pattern for APIs (if needed)

---

### 7. Rate Limiting

#### BAD - No Rate Limiting
```typescript
// VULNERABLE: No limits on expensive operation
app.post('/api/search', async (req, res) => {
  const results = await expensiveSearch(req.body.query)
  return res.json(results)
})

// VULNERABLE: No limits on auth endpoints
app.post('/api/login', async (req, res) => {
  // Brute force attack possible
})
```

#### GOOD - Implement Rate Limiting
```typescript
import rateLimit from 'express-rate-limit'

// General API rate limit
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  message: { error: 'Too many requests, please try again later' },
  standardHeaders: true,
  legacyHeaders: false
})

// Strict rate limit for auth endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // 5 attempts per 15 minutes
  message: { error: 'Too many login attempts' },
  skipSuccessfulRequests: true
})

// Very strict for expensive operations
const searchLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 10,
  message: { error: 'Too many search requests' }
})

app.use('/api/', apiLimiter)
app.use('/api/auth/', authLimiter)
app.use('/api/search', searchLimiter)
```

#### Verification Checklist
- [ ] Rate limiting on all API endpoints
- [ ] Stricter limits on authentication endpoints
- [ ] Stricter limits on expensive operations (search, AI, etc.)
- [ ] IP-based rate limiting for unauthenticated requests
- [ ] User-based rate limiting for authenticated requests
- [ ] Rate limit headers returned to clients
- [ ] Graceful handling of rate limit exceeded

---

### 8. Sensitive Data Exposure

#### BAD - Leaking Sensitive Data
```typescript
// WRONG: Logging sensitive data
console.log('User login:', { email, password })
console.log('Payment processed:', { cardNumber, cvv, amount })
console.log('Request body:', req.body) // May contain passwords

// WRONG: Exposing internal errors
catch (error) {
  return res.json({
    error: error.message,
    stack: error.stack, // Stack trace exposed!
    query: sqlQuery // Query exposed!
  })
}

// WRONG: Returning full user object
return res.json({ user }) // Includes password hash, internal IDs, etc.
```

#### GOOD - Protect Sensitive Data
```typescript
// CORRECT: Redact sensitive data in logs
console.log('User login:', { email, userId: user.id })
console.log('Payment processed:', {
  last4: card.number.slice(-4),
  amount,
  userId
})

// CORRECT: Generic error messages to clients
catch (error) {
  // Log full error server-side
  logger.error('Payment failed', {
    error: error.message,
    userId,
    // Never log card numbers, even partial
  })

  // Return generic message to client
  return res.status(500).json({
    error: 'Payment processing failed. Please try again.'
  })
}

// CORRECT: Select specific fields
const user = await db.users.findUnique({
  where: { id: userId },
  select: {
    id: true,
    email: true,
    name: true,
    // Explicitly exclude: passwordHash, internalNotes, etc.
  }
})
return res.json({ user })
```

#### Verification Checklist
- [ ] No passwords, tokens, or full card numbers in logs
- [ ] Error messages generic for end users
- [ ] Detailed errors only in server-side logs
- [ ] No stack traces exposed to clients
- [ ] API responses select specific fields (not SELECT *)
- [ ] Sensitive data encrypted at rest
- [ ] Sensitive data encrypted in transit (HTTPS enforced)
- [ ] PII handling compliant with regulations (GDPR, CCPA)

---

### 9. Blockchain Security (Conditional)

*Only applicable when project involves blockchain/crypto functionality.*

#### BAD - Insecure Blockchain Handling
```typescript
// WRONG: Not verifying wallet ownership
async function claimReward(walletAddress: string) {
  await sendReward(walletAddress) // Anyone can claim!
}

// WRONG: Blind transaction signing
async function processTransaction(tx: any) {
  await wallet.signAndSend(tx) // No validation!
}
```

#### GOOD - Verify Everything
```typescript
import { verify } from '@solana/web3.js'
import nacl from 'tweetnacl'

// Verify wallet ownership with signed message
async function verifyWalletOwnership(
  publicKey: string,
  signature: string,
  message: string
): Promise<boolean> {
  try {
    const messageBytes = new TextEncoder().encode(message)
    const signatureBytes = Buffer.from(signature, 'base64')
    const publicKeyBytes = Buffer.from(publicKey, 'base64')

    return nacl.sign.detached.verify(
      messageBytes,
      signatureBytes,
      publicKeyBytes
    )
  } catch {
    return false
  }
}

// Validate transaction before signing
async function processTransaction(transaction: Transaction) {
  // Verify recipient is expected
  if (transaction.to !== KNOWN_RECIPIENT) {
    throw new Error('Invalid recipient address')
  }

  // Verify amount is within limits
  if (transaction.amount > MAX_TRANSACTION_AMOUNT) {
    throw new Error('Amount exceeds limit')
  }

  // Verify user has sufficient balance
  const balance = await getBalance(transaction.from)
  if (balance < transaction.amount + GAS_BUFFER) {
    throw new Error('Insufficient balance')
  }

  // Log transaction for audit
  await auditLog.record({
    type: 'transaction',
    from: transaction.from,
    to: transaction.to,
    amount: transaction.amount,
    timestamp: new Date()
  })

  return await signAndSend(transaction)
}
```

#### Verification Checklist
- [ ] Wallet signatures verified before granting access
- [ ] Transaction details validated before signing
- [ ] Balance checks before transactions
- [ ] No blind transaction signing
- [ ] Transaction limits enforced
- [ ] Audit logging for all transactions
- [ ] Private keys never exposed in logs or errors
- [ ] Smart contract interactions validated

---

### 10. Dependency Security

#### Regular Security Audits
```bash
# Check for known vulnerabilities
npm audit

# Automatically fix what's possible
npm audit fix

# Check for outdated packages
npm outdated

# Update dependencies
npm update

# For major updates, use interactive mode carefully
npx npm-check-updates -i
```

#### Lock File Management
```bash
# ALWAYS commit lock files
git add package-lock.json  # or yarn.lock, pnpm-lock.yaml

# In CI/CD, use clean install for reproducible builds
npm ci  # Not npm install

# Verify integrity
npm ci --ignore-scripts  # Then run scripts separately if needed
```

#### Verification Checklist
- [ ] No known vulnerabilities (`npm audit` clean or exceptions documented)
- [ ] Dependencies regularly updated
- [ ] Lock files committed to repository
- [ ] Dependabot or similar enabled on GitHub
- [ ] Unused dependencies removed
- [ ] Dependencies from trusted sources only
- [ ] License compliance verified (no GPL in proprietary code, etc.)
- [ ] Postinstall scripts reviewed for new dependencies

---

## Integration with implement-phase

When invoked as part of the implement-phase pipeline (Step 3), this skill provides structured output for orchestration.

### Input Context

```
Security Review for Phase [N]

Context:
- Plan: [path to plan file]
- Phase: [phase number and name]
- Changed files: [list of modified/added files]
- Security-relevant changes: [auth, input, api, secrets, payment, uploads]
```

### Output Format

```
STATUS: PASS | PASS_WITH_ISSUES | FAIL
CATEGORIES_CHECKED: [count of applicable categories reviewed]
ISSUES_FOUND:
- [CRITICAL] [Category]: [Description]
- [HIGH] [Category]: [Description]
- [MEDIUM] [Category]: [Description]
- [LOW] [Category]: [Description]
SEVERITY: CRITICAL | HIGH | MEDIUM | LOW | NONE
RECOMMENDATIONS:
- [Non-blocking improvement suggestions]
REPORT: [Path to detailed report if written]
```

### Severity Levels

| Level | Meaning | Action Required |
|-------|---------|-----------------|
| **CRITICAL** | Active vulnerability, exploitable now | Block deployment, fix immediately |
| **HIGH** | Serious vulnerability, likely exploitable | Block deployment, fix before merge |
| **MEDIUM** | Potential vulnerability, context-dependent | Should fix, may proceed with documented exception |
| **LOW** | Best practice violation, minimal risk | Note for improvement |

### Integration Point in Pipeline

```
implement-phase Pipeline:
  Step 1: Implementation
  Step 2: Functional verification (tests pass)
  Step 3: Code review
  Step 4: SECURITY REVIEW (this skill) <--
  Step 5: Plan synchronization
  Step 6: Completion report

On FAIL:
  - Block phase completion
  - Report blocking issues
  - Require fixes before retry
```

---

## Pre-Deployment Security Checklist

Before ANY production deployment, verify:

### Secrets & Configuration
- [ ] No hardcoded secrets in code
- [ ] All secrets in environment variables
- [ ] Production secrets in secure management
- [ ] Different secrets per environment

### Input & Data
- [ ] All user input validated server-side
- [ ] File uploads validated and sanitized
- [ ] All database queries parameterized
- [ ] Sensitive data encrypted at rest

### Authentication & Authorization
- [ ] Tokens in httpOnly cookies
- [ ] Authorization checks on all operations
- [ ] Row Level Security enabled
- [ ] Session management secure

### Web Security
- [ ] XSS protection (CSP, sanitization)
- [ ] CSRF protection enabled
- [ ] HTTPS enforced
- [ ] Security headers configured

### Infrastructure
- [ ] Rate limiting on all endpoints
- [ ] Error messages don't leak info
- [ ] Logging doesn't include secrets
- [ ] Dependencies up to date

### Compliance
- [ ] CORS properly configured
- [ ] Privacy policy accurate
- [ ] Data handling compliant (GDPR/CCPA)

---

## References

For detailed checklists and examples:
- [security-checklist.md](references/security-checklist.md) - Quick reference checklist
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Common vulnerabilities
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/) - Detailed guidance

---

**Security is everyone's responsibility. When in doubt, ask for a security review.**
