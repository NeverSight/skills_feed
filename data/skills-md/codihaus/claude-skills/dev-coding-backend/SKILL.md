---
name: dev-coding-backend
description: Backend implementation patterns and workflows
version: 1.1.0
---

# /dev-coding-backend - Backend Implementation

> **Skill Awareness**: See `skills/_registry.md` for all available skills.
> - **Loaded by**: `/dev-coding` when API/schema work needed
> - **References**: Load tech-specific from `references/` (directus.md, prisma.md, etc.)
> - **After**: Frontend uses API contract documented here

Backend-specific patterns for API, schema, and data layer implementation.

## When Loaded

This skill is loaded by `/dev-coding` when:
- Spec requires API endpoints
- Spec requires schema/database changes
- Spec requires backend logic

## Workflow

### Step 1: Understand Backend Requirements

From the UC spec, extract:

```markdown
## Backend Requirements Checklist

[ ] Schema changes needed?
    - New collections/tables
    - New fields on existing
    - Relations to add

[ ] API endpoints needed?
    - Method + Path
    - Request body
    - Response shape
    - Auth required?

[ ] Business logic?
    - Validation rules
    - Calculations
    - Side effects (emails, notifications)

[ ] External integrations?
    - Third-party APIs
    - Webhooks
    - File storage
```

### Step 2: Schema First (if needed)

**Order matters:** Schema before API

```
1. Design schema based on spec
2. Create/modify collections or tables
3. Set up relations
4. Configure permissions/roles
5. Verify schema is correct
```

**Verification:**
```bash
# For Directus - check collection exists
curl "$DIRECTUS_URL/items/{collection}?limit=1" \
  -H "Authorization: Bearer $TOKEN"

# For Prisma - run migration
npx prisma migrate dev

# For SQL - verify table
psql -c "\\d {table_name}"
```

### Step 3: API Implementation

**For each endpoint in spec:**

```
1. Create route/handler file
2. Implement request parsing
3. Add validation
4. Implement business logic
5. Handle errors
6. Return response
```

**Follow project patterns** (from scout):
- File location (routes/, api/, controllers/)
- Naming convention
- Error handling pattern
- Response format

### Step 4: API Patterns

#### REST Conventions

```
GET    /api/{resource}        → List
GET    /api/{resource}/:id    → Get one
POST   /api/{resource}        → Create
PUT    /api/{resource}/:id    → Update (full)
PATCH  /api/{resource}/:id    → Update (partial)
DELETE /api/{resource}/:id    → Delete
```

#### Request Validation

```typescript
// Always validate input
const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

const result = schema.safeParse(req.body);
if (!result.success) {
  return res.status(400).json({
    error: 'Validation failed',
    details: result.error.issues
  });
}
```

#### Error Handling

```typescript
// Consistent error format
{
  "error": "Error message for client",
  "code": "ERROR_CODE",
  "details": {} // Optional additional info
}

// HTTP status codes
200 - Success
201 - Created
400 - Bad request (validation)
401 - Unauthorized
403 - Forbidden
404 - Not found
409 - Conflict
500 - Server error
```

#### Authentication Check

```typescript
// Verify auth before processing
if (!req.user) {
  return res.status(401).json({ error: 'Unauthorized' });
}

// Check permissions
if (!req.user.permissions.includes('create:posts')) {
  return res.status(403).json({ error: 'Forbidden' });
}
```

### Step 5: Verification

**Test each endpoint:**

```bash
# Test with curl
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"password123"}'

# Expected: 200 with token
# Or: 401 with error message
```

**Verification checklist:**
```
[ ] Endpoint responds
[ ] Correct status codes
[ ] Response matches spec
[ ] Validation rejects bad input
[ ] Auth required endpoints reject anonymous
[ ] Error messages are helpful but not leaky
```

### Step 6: Document for Frontend

After backend complete, document what frontend needs:

```markdown
## API Ready for Frontend

### POST /api/auth/login
- **Auth**: None (public)
- **Request**: `{ email: string, password: string }`
- **Success (200)**: `{ token: string, user: { id, email, name } }`
- **Errors**:
  - 400: Invalid input
  - 401: Invalid credentials

### GET /api/users/me
- **Auth**: Bearer token required
- **Request**: None
- **Success (200)**: `{ id, email, name, role }`
- **Errors**:
  - 401: No/invalid token
```

## Common Patterns

### Database Query Patterns

```typescript
// Pagination
const page = parseInt(req.query.page) || 1;
const limit = parseInt(req.query.limit) || 10;
const offset = (page - 1) * limit;

const items = await db.items.findMany({
  skip: offset,
  take: limit,
  orderBy: { createdAt: 'desc' }
});

// Filtering
const where = {};
if (req.query.status) {
  where.status = req.query.status;
}

// Include relations
const post = await db.posts.findUnique({
  where: { id },
  include: { author: true, comments: true }
});
```

### Transaction Pattern

```typescript
// When multiple operations must succeed together
await db.$transaction(async (tx) => {
  const user = await tx.users.create({ data: userData });
  await tx.profiles.create({ data: { userId: user.id } });
  await tx.settings.create({ data: { userId: user.id } });
  return user;
});
```

### Soft Delete Pattern

```typescript
// Don't actually delete, mark as deleted
await db.posts.update({
  where: { id },
  data: {
    deletedAt: new Date(),
    status: 'deleted'
  }
});

// Query excludes deleted
const posts = await db.posts.findMany({
  where: { deletedAt: null }
});
```

## Security Checklist

```
[ ] Input validated before use
[ ] SQL/NoSQL injection prevented (use parameterized queries)
[ ] Auth checked on protected routes
[ ] Permissions verified for actions
[ ] Sensitive data not logged
[ ] Passwords hashed (never plain text)
[ ] Rate limiting on auth endpoints
[ ] CORS configured correctly
[ ] No secrets in code (use env vars)
```

## Debugging

### API Not Responding

```bash
# Check if server running
curl http://localhost:3000/health

# Check logs
tail -f logs/server.log

# Check port in use
lsof -i :3000
```

### Database Issues

```bash
# Check connection
npx prisma db pull  # Prisma
psql -c "SELECT 1"  # PostgreSQL

# Check migrations
npx prisma migrate status
```

### Auth Issues

```bash
# Test token validity
curl http://localhost:3000/api/users/me \
  -H "Authorization: Bearer $TOKEN"

# Decode JWT (for debugging only)
echo $TOKEN | cut -d. -f2 | base64 -d
```

## Tech-Specific References

Load additional patterns based on detected tech:

| Tech | Reference File |
|------|---------------|
| Directus | `references/directus.md` |
| Node/Express | `references/node.md` |
| Prisma | `references/prisma.md` |
| PostgreSQL | `references/postgresql.md` |
| Supabase | `references/supabase.md` |

These files contain tech-specific patterns, gotchas, and best practices. Add them as your projects use different stacks.
