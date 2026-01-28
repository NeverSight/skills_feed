---
name: nodejs-best-practices
description: Clean, maintainable Node.js code following industry best practices. Use when writing Express routes, services, database queries, error handling, or tests. Covers PostgreSQL connection pooling, transactions, async/await patterns, and Jest testing.
---

# Node.js Best Practices Skill

## Overview

This skill ensures clean, maintainable, production-ready Node.js code. It covers Express application structure, PostgreSQL database patterns, error handling, testing, and security.

## Project Structure

Organize code into distinct layers:

```
server/
├── index.js           # App setup, middleware mounting
├── routes/            # HTTP handling only, no business logic
├── services/          # Business logic, database operations
├── data/              # Static data, definitions, constants
├── db/                # Database connection, migrations
└── auth/              # Authentication middleware
```

**Routes** handle HTTP concerns (parsing requests, sending responses).
**Services** contain business logic and database operations.
**Data** modules export static definitions and pure functions.

## Core Principles

### 1. Separation of Concerns

Routes should delegate to services, not contain business logic:

```javascript
// GOOD: Route delegates to service
router.post('/:gameId/action', async (req, res) => {
  try {
    const result = await gameService.processAction(
      req.params.gameId, req.session.userId, req.body
    );
    res.json(result);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});
```

### 2. Consistent Async/Await

Use async/await consistently. Never mix with callbacks:

```javascript
// GOOD: Clean async/await
async function getUser(userId) {
  const result = await pool.query('SELECT * FROM users WHERE id = $1', [userId]);
  return result.rows[0] || null;
}
```

### 3. Always Use Parameterized Queries

Never interpolate user input into SQL:

```javascript
// GOOD: Parameterized (safe)
await pool.query('SELECT * FROM users WHERE id = $1', [userId]);

// BAD: SQL injection vulnerability
await pool.query(`SELECT * FROM users WHERE id = ${userId}`);
```

### 4. Proper Error Handling

Always handle errors - never swallow them:

```javascript
router.post('/:id/action', async (req, res) => {
  try {
    const result = await processAction(req.params.id, req.body);
    res.json({ success: true, ...result });
  } catch (error) {
    console.error('Action failed:', error);
    res.status(400).json({ error: error.message });
  }
});
```

## Database Patterns

See [DATABASE.md](DATABASE.md) for complete database patterns including:
- Connection pooling configuration
- Transaction handling with proper rollback
- Row locking with `FOR UPDATE`
- N+1 query prevention

### Quick Reference

```javascript
// Connection pool (singleton)
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,
  idleTimeoutMillis: 30000
});

// Transaction pattern
const client = await pool.connect();
try {
  await client.query('BEGIN');
  // ... operations ...
  await client.query('COMMIT');
} catch (error) {
  await client.query('ROLLBACK');
  throw error;
} finally {
  client.release();  // ALWAYS release
}
```

## Testing Patterns

See [TESTING.md](TESTING.md) for complete testing patterns including:
- Mocking the database pool
- Testing transaction rollbacks
- Route testing patterns

### Quick Reference

```javascript
// Mock database at top of test file
jest.mock('../../server/db', () => ({
  pool: { query: jest.fn(), connect: jest.fn(), on: jest.fn() }
}));

// Reset mocks between tests
beforeEach(() => {
  jest.clearAllMocks();
});

// Mock transaction client
const mockClient = { query: jest.fn(), release: jest.fn() };
pool.connect.mockResolvedValue(mockClient);
```

## Express Patterns

### Middleware Order

```javascript
app.set('trust proxy', 1);        // 1. Proxy settings
app.use(express.json());          // 2. Body parsing
app.use(sessionMiddleware);       // 3. Session
app.use(express.static('public')); // 4. Static files
app.use('/api', routes);          // 5. Routes
app.use(errorHandler);            // 6. Error handler (last)
```

### Authentication Middleware

```javascript
function requireAuth(req, res, next) {
  if (!req.session?.userId) {
    return res.status(401).json({ error: 'Not authenticated' });
  }
  next();
}

router.use(requireAuth);  // Apply to all routes in file
```

### Input Validation

Validate early in route handlers:

```javascript
router.post('/:gameId/action', async (req, res) => {
  const { actionType } = req.body;
  if (!actionType) {
    return res.status(400).json({ error: 'Action type is required' });
  }
  // Proceed with validated input...
});
```

## Security Essentials

### Environment Variables

```javascript
// GOOD: From environment
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

// BAD: Hardcoded credentials
const pool = new Pool({ connectionString: 'postgres://user:pass@host/db' });
```

### Password Hashing

```javascript
const bcrypt = require('bcrypt');
const SALT_ROUNDS = 10;

await bcrypt.hash(password, SALT_ROUNDS);    // Hash
await bcrypt.compare(password, hash);         // Verify
```

### Session Configuration

```javascript
app.use(session({
  secret: process.env.SESSION_SECRET,
  cookie: {
    secure: process.env.NODE_ENV === 'production',
    httpOnly: true,
    maxAge: 24 * 60 * 60 * 1000
  }
}));
```

## Performance Tips

### Parallel Operations

Use Promise.all for independent operations:

```javascript
const [game, players, state] = await Promise.all([
  getGameById(gameId),
  getGamePlayers(gameId),
  getGameState(gameId)
]);
```

### Health Checks

Include database status:

```javascript
app.get('/health', async (req, res) => {
  const dbHealthy = await db.healthCheck();
  res.status(dbHealthy ? 200 : 503).json({
    status: dbHealthy ? 'healthy' : 'degraded',
    database: dbHealthy ? 'connected' : 'disconnected'
  });
});
```

## When This Skill Activates

Use this skill when:
- Writing Express routes or middleware
- Creating service layer functions
- Working with PostgreSQL queries
- Implementing database transactions
- Writing Jest tests for Node.js code
- Handling errors and edge cases
- Setting up authentication or sessions
