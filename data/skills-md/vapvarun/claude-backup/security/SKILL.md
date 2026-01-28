---
name: security
description: Web application security best practices including OWASP Top 10, authentication, authorization, input validation, cryptography, and secure coding patterns. Use when implementing security features, reviewing code for vulnerabilities, hardening applications, or fixing security issues.
---

# Web Application Security

Security best practices and vulnerability prevention.

## OWASP Top 10

### 1. Injection (SQL, NoSQL, Command)

```javascript
// BAD: SQL Injection
const query = `SELECT * FROM users WHERE email = '${email}'`;
db.query(query);

// GOOD: Parameterized queries
const query = 'SELECT * FROM users WHERE email = ?';
db.query(query, [email]);

// GOOD: Using ORM
const user = await User.findOne({ where: { email } });

// BAD: Command injection
const output = execSync(`ls ${userInput}`);

// GOOD: Avoid shell, use array
const output = execFileSync('ls', [sanitizedPath]);

// BAD: NoSQL injection
db.users.find({ username: req.body.username, password: req.body.password });

// GOOD: Type validation
const username = String(req.body.username);
const password = String(req.body.password);
db.users.find({ username, password });
```

### 2. Broken Authentication

```javascript
// Password hashing
import bcrypt from 'bcrypt';

const SALT_ROUNDS = 12;

async function hashPassword(password) {
    return bcrypt.hash(password, SALT_ROUNDS);
}

async function verifyPassword(password, hash) {
    return bcrypt.compare(password, hash);
}

// Session management
import session from 'express-session';
import RedisStore from 'connect-redis';

app.use(session({
    store: new RedisStore({ client: redisClient }),
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: false,
    cookie: {
        secure: true,           // HTTPS only
        httpOnly: true,         // No JavaScript access
        sameSite: 'strict',     // CSRF protection
        maxAge: 3600000,        // 1 hour
    },
}));

// Rate limiting
import rateLimit from 'express-rate-limit';

const loginLimiter = rateLimit({
    windowMs: 15 * 60 * 1000,   // 15 minutes
    max: 5,                     // 5 attempts
    message: 'Too many login attempts, try again later',
    standardHeaders: true,
    legacyHeaders: false,
});

app.post('/login', loginLimiter, loginHandler);
```

### 3. Sensitive Data Exposure

```javascript
// Never log sensitive data
// BAD
console.log('User login:', { email, password });

// GOOD
console.log('User login:', { email, password: '[REDACTED]' });

// Encrypt sensitive data at rest
import crypto from 'crypto';

const ENCRYPTION_KEY = Buffer.from(process.env.ENCRYPTION_KEY, 'hex');
const IV_LENGTH = 16;

function encrypt(text) {
    const iv = crypto.randomBytes(IV_LENGTH);
    const cipher = crypto.createCipheriv('aes-256-gcm', ENCRYPTION_KEY, iv);

    let encrypted = cipher.update(text, 'utf8', 'hex');
    encrypted += cipher.final('hex');

    const authTag = cipher.getAuthTag();

    return `${iv.toString('hex')}:${authTag.toString('hex')}:${encrypted}`;
}

function decrypt(encryptedData) {
    const [ivHex, authTagHex, encrypted] = encryptedData.split(':');
    const iv = Buffer.from(ivHex, 'hex');
    const authTag = Buffer.from(authTagHex, 'hex');

    const decipher = crypto.createDecipheriv('aes-256-gcm', ENCRYPTION_KEY, iv);
    decipher.setAuthTag(authTag);

    let decrypted = decipher.update(encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');

    return decrypted;
}
```

### 4. XML External Entities (XXE)

```javascript
// BAD: Default parser may be vulnerable
const parser = new DOMParser();
const doc = parser.parseFromString(xmlString, 'text/xml');

// GOOD: Disable external entities
import { XMLParser } from 'fast-xml-parser';

const parser = new XMLParser({
    allowBooleanAttributes: true,
    ignoreAttributes: false,
    // Disable external entities and DTD processing
});

const result = parser.parse(xmlString);
```

### 5. Broken Access Control

```javascript
// IDOR Prevention
// BAD: Direct object reference
app.get('/api/orders/:id', async (req, res) => {
    const order = await Order.findById(req.params.id);
    res.json(order);  // Any user can access any order!
});

// GOOD: Verify ownership
app.get('/api/orders/:id', async (req, res) => {
    const order = await Order.findOne({
        _id: req.params.id,
        userId: req.user.id,  // Only owner's orders
    });

    if (!order) {
        return res.status(404).json({ error: 'Not found' });
    }

    res.json(order);
});

// Role-based access control
function requireRole(...roles) {
    return (req, res, next) => {
        if (!req.user || !roles.includes(req.user.role)) {
            return res.status(403).json({ error: 'Forbidden' });
        }
        next();
    };
}

app.delete('/api/users/:id', requireRole('admin'), deleteUser);
```

### 6. Security Misconfiguration

```javascript
// Security headers
import helmet from 'helmet';

app.use(helmet({
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            scriptSrc: ["'self'", "'unsafe-inline'"],  // Avoid if possible
            styleSrc: ["'self'", "'unsafe-inline'"],
            imgSrc: ["'self'", 'data:', 'https:'],
            connectSrc: ["'self'", 'https://api.example.com'],
            frameSrc: ["'none'"],
            objectSrc: ["'none'"],
        },
    },
    crossOriginEmbedderPolicy: true,
    crossOriginOpenerPolicy: true,
    crossOriginResourcePolicy: { policy: 'same-site' },
    hsts: {
        maxAge: 31536000,
        includeSubDomains: true,
        preload: true,
    },
}));

// Disable server info
app.disable('x-powered-by');

// Error handling - don't leak stack traces
app.use((err, req, res, next) => {
    console.error(err.stack);  // Log full error

    res.status(500).json({
        error: process.env.NODE_ENV === 'production'
            ? 'Internal server error'
            : err.message,
    });
});
```

### 7. Cross-Site Scripting (XSS)

```javascript
// Input sanitization
import DOMPurify from 'dompurify';
import { JSDOM } from 'jsdom';

const window = new JSDOM('').window;
const purify = DOMPurify(window);

// Sanitize HTML input
const cleanHtml = purify.sanitize(userInput);

// Output encoding
import { encode } from 'html-entities';

const safeOutput = encode(userInput);

// React automatically escapes
function Comment({ text }) {
    return <p>{text}</p>;  // Safe - React escapes
}

// BAD: dangerouslySetInnerHTML
<div dangerouslySetInnerHTML={{ __html: userInput }} />  // XSS risk!

// GOOD: sanitize first
<div dangerouslySetInnerHTML={{ __html: purify.sanitize(userInput) }} />
```

### 8. Insecure Deserialization

```javascript
// BAD: Deserializing untrusted data
const data = JSON.parse(userInput);
eval(data.callback);  // Remote code execution!

// GOOD: Validate schema
import Ajv from 'ajv';

const ajv = new Ajv();
const schema = {
    type: 'object',
    properties: {
        name: { type: 'string', maxLength: 100 },
        age: { type: 'integer', minimum: 0, maximum: 150 },
    },
    required: ['name'],
    additionalProperties: false,
};

const validate = ajv.compile(schema);
const data = JSON.parse(userInput);

if (!validate(data)) {
    throw new Error('Invalid data');
}
```

### 9. Using Components with Known Vulnerabilities

```bash
# Check for vulnerabilities
npm audit
npm audit fix

# Use Snyk for deeper analysis
npx snyk test

# Keep dependencies updated
npx npm-check-updates -u

# Lock file for reproducible builds
npm ci  # Use in CI/CD
```

### 10. Insufficient Logging & Monitoring

```javascript
// Security event logging
import winston from 'winston';

const securityLogger = winston.createLogger({
    level: 'info',
    format: winston.format.json(),
    transports: [
        new winston.transports.File({ filename: 'security.log' }),
    ],
});

// Log security events
function logSecurityEvent(event, details) {
    securityLogger.info({
        timestamp: new Date().toISOString(),
        event,
        ...details,
        ip: details.req?.ip,
        userAgent: details.req?.get('user-agent'),
    });
}

// Usage
app.post('/login', async (req, res) => {
    try {
        const user = await authenticate(req.body);

        logSecurityEvent('LOGIN_SUCCESS', {
            req,
            userId: user.id,
        });

        // ...
    } catch (error) {
        logSecurityEvent('LOGIN_FAILURE', {
            req,
            email: req.body.email,
            reason: error.message,
        });

        // ...
    }
});
```

## Authentication

### JWT Best Practices

```javascript
import jwt from 'jsonwebtoken';

const ACCESS_TOKEN_SECRET = process.env.ACCESS_TOKEN_SECRET;
const REFRESH_TOKEN_SECRET = process.env.REFRESH_TOKEN_SECRET;

// Short-lived access token
function generateAccessToken(user) {
    return jwt.sign(
        { userId: user.id, role: user.role },
        ACCESS_TOKEN_SECRET,
        { expiresIn: '15m', algorithm: 'HS256' }
    );
}

// Long-lived refresh token
function generateRefreshToken(user) {
    return jwt.sign(
        { userId: user.id, tokenVersion: user.tokenVersion },
        REFRESH_TOKEN_SECRET,
        { expiresIn: '7d', algorithm: 'HS256' }
    );
}

// Verify middleware
function authenticate(req, res, next) {
    const authHeader = req.headers.authorization;

    if (!authHeader?.startsWith('Bearer ')) {
        return res.status(401).json({ error: 'Missing token' });
    }

    const token = authHeader.split(' ')[1];

    try {
        const payload = jwt.verify(token, ACCESS_TOKEN_SECRET);
        req.user = payload;
        next();
    } catch (error) {
        if (error.name === 'TokenExpiredError') {
            return res.status(401).json({ error: 'Token expired' });
        }
        return res.status(403).json({ error: 'Invalid token' });
    }
}
```

### OAuth 2.0 / OIDC

```javascript
import { Issuer, generators } from 'openid-client';

// Configure client
const issuer = await Issuer.discover('https://accounts.google.com');
const client = new issuer.Client({
    client_id: process.env.GOOGLE_CLIENT_ID,
    client_secret: process.env.GOOGLE_CLIENT_SECRET,
    redirect_uris: ['https://example.com/callback'],
    response_types: ['code'],
});

// Generate authorization URL
app.get('/auth/google', (req, res) => {
    const codeVerifier = generators.codeVerifier();
    const codeChallenge = generators.codeChallenge(codeVerifier);

    req.session.codeVerifier = codeVerifier;
    req.session.state = generators.state();

    const url = client.authorizationUrl({
        scope: 'openid email profile',
        code_challenge: codeChallenge,
        code_challenge_method: 'S256',
        state: req.session.state,
    });

    res.redirect(url);
});

// Handle callback
app.get('/callback', async (req, res) => {
    const params = client.callbackParams(req);
    const tokenSet = await client.callback(
        'https://example.com/callback',
        params,
        {
            code_verifier: req.session.codeVerifier,
            state: req.session.state,
        }
    );

    const userInfo = await client.userinfo(tokenSet.access_token);
    // Create session, redirect user
});
```

## Input Validation

```javascript
import { z } from 'zod';

// Define schema
const userSchema = z.object({
    email: z.string().email().max(255),
    password: z.string().min(8).max(100),
    name: z.string().min(1).max(100).regex(/^[a-zA-Z\s]+$/),
    age: z.number().int().min(13).max(150).optional(),
});

// Validate
function validateInput(schema) {
    return (req, res, next) => {
        try {
            req.validated = schema.parse(req.body);
            next();
        } catch (error) {
            res.status(400).json({
                error: 'Validation failed',
                details: error.errors,
            });
        }
    };
}

app.post('/users', validateInput(userSchema), createUser);
```

## CSRF Protection

```javascript
import csrf from 'csurf';

// For traditional forms
const csrfProtection = csrf({ cookie: true });

app.get('/form', csrfProtection, (req, res) => {
    res.render('form', { csrfToken: req.csrfToken() });
});

// For SPAs - use SameSite cookies + custom header
// Client sends: X-Requested-With: XMLHttpRequest
app.use((req, res, next) => {
    if (req.method !== 'GET' && req.method !== 'HEAD') {
        if (req.headers['x-requested-with'] !== 'XMLHttpRequest') {
            return res.status(403).json({ error: 'CSRF check failed' });
        }
    }
    next();
});
```

## Security Checklist

### Application

- [ ] Use HTTPS everywhere
- [ ] Validate all input (whitelist approach)
- [ ] Encode all output
- [ ] Use parameterized queries
- [ ] Implement proper authentication
- [ ] Implement proper authorization
- [ ] Hash passwords with bcrypt/argon2
- [ ] Use secure session management
- [ ] Set security headers (helmet)
- [ ] Implement rate limiting
- [ ] Log security events
- [ ] Handle errors without leaking info

### Infrastructure

- [ ] Keep dependencies updated
- [ ] Use secrets management
- [ ] Configure firewalls
- [ ] Enable audit logging
- [ ] Set up intrusion detection
- [ ] Regular security scans
- [ ] Backup encryption
- [ ] Least privilege access

### Development

- [ ] Security code reviews
- [ ] Static analysis (SAST)
- [ ] Dynamic analysis (DAST)
- [ ] Dependency scanning
- [ ] Security training
- [ ] Incident response plan
