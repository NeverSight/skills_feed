---
name: mongodb-atlas-checker
description: Verify MongoDB Atlas setup and configuration for backend applications. Checks connection strings, environment variables, connection pooling, and ensures proper setup for Next.js and NestJS applications.
version: 1.0.0
tags:
  - mongodb
  - atlas
  - database
  - backend
  - nestjs
  - nextjs
---

# MongoDB Atlas Checker

Verify MongoDB Atlas setup and configuration. Identifies configuration issues, missing environment variables, incorrect connection strings, and ensures proper database setup.

## When to Use

- Verifying MongoDB Atlas backend setup
- Checking connection string configuration
- Validating environment variable setup
- Troubleshooting database connection issues
- Auditing database setup before deployment

## Quick Checklist

### 1. Environment Variables

- [ ] `MONGODB_URI` exists (not hardcoded)
- [ ] Uses `mongodb+srv://` protocol (required for Atlas)
- [ ] Includes database name
- [ ] Includes `retryWrites=true&w=majority`
- [ ] No credentials in `.env.example`

### 2. Connection String Format

```
mongodb+srv://<username>:<password>@<cluster-host>/<database>?retryWrites=true&w=majority
```

### 3. Driver Installation

- [ ] `mongoose` or `mongodb` package installed
- [ ] In dependencies (not devDependencies)

### 4. Connection Setup

- [ ] Singleton pattern (Next.js)
- [ ] `MongooseModule.forRoot()` (NestJS)
- [ ] Error handling implemented

### 5. Atlas Configuration

- [ ] IP whitelist configured
- [ ] Database user exists with permissions
- [ ] SSL/TLS enabled (default with `mongodb+srv://`)

## Common Issues

| Issue | Solution |
|-------|----------|
| Missing `MONGODB_URI` | Add to `.env.local` or `.env` |
| Wrong protocol | Use `mongodb+srv://` not `mongodb://` |
| Multiple connections (Next.js) | Use singleton pattern |
| Connection timeout | Check IP whitelist in Atlas |
| Auth failed | Verify credentials, URL-encode special chars |

## Recommended Connection Options

```typescript
{
  retryWrites: true,
  w: 'majority',
  maxPoolSize: 10,
  serverSelectionTimeoutMS: 5000,
  bufferCommands: false,
}
```

---

**For detailed setup patterns, verification scripts, and complete examples:** `references/full-guide.md`
