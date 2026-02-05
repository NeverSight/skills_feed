---
name: nodejs-coding
description: Node.js backend coding guidelines with Express/Fastify, TypeScript, and modern patterns. Use when building Node.js APIs.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Edit
  - Write
---

# Node.js Coding Guidelines

**IMPORTANT:** This skill covers Node.js backend development with TypeScript.

## Quick Start Checklist

Before writing Node.js code:
- [ ] Use TypeScript (never plain JavaScript)
- [ ] Use ES6 imports (not require)
- [ ] Add input validation (Zod recommended)
- [ ] Centralize error handling with middleware
- [ ] Never use async without await or proper handling
- [ ] Always handle Promise rejections

---

## Import Conventions

### Use ES6 Imports (Never CommonJS)

```typescript
// ❌ WRONG - CommonJS require (legacy)
const express = require('express');
const { userService } = require('./services/user.service');

// ✅ CORRECT - ES6 imports
import express from 'express';
import { userService } from './services/user.service';
import type { User } from './models/user.model';
```

**Enable ES6 in TypeScript:**
```json
// tsconfig.json
{
  "compilerOptions": {
    "module": "Node16",
    "moduleResolution": "Node16",
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true
  }
}
```

### Import Organization

```typescript
// 1. External dependencies (alphabetical)
import cors from 'cors';
import express, { Request, Response, NextFunction } from 'express';
import helmet from 'helmet';
import { z } from 'zod';

// 2. Internal absolute (if using path aliases)
import { config } from '@/config';
import { logger } from '@/utils/logger';

// 3. Internal relative
import { userService } from './services/user.service';
import { userRepository } from './repositories/user.repository';

// 4. Types (separate)
import type { CreateUserDto, User } from './models/user.model';
import type { AppError } from './utils/errors';
```

**Why separate type imports:**
- Helps with tree shaking (removes unused code)
- Prevents circular dependency issues
- Makes dependencies clearer

---

## Project Structure

```
src/
├── config/              # Configuration
│   └── index.ts         # Environment variables
├── controllers/         # Route handlers (thin layer)
│   └── user.controller.ts
├── services/           # Business logic
│   └── user.service.ts
├── repositories/       # Data access
│   └── user.repository.ts
├── middleware/         # Express middleware
│   ├── errorHandler.ts
│   ├── validate.ts
│   └── auth.ts
├── models/             # Types and validation schemas
│   └── user.model.ts
├── utils/              # Utilities
│   ├── errors.ts
│   └── logger.ts
├── routes/             # Route definitions
│   └── user.routes.ts
├── app.ts              # App setup (no server start)
└── server.ts           # Entry point (starts server)
```

---

## Configuration

### Environment Variables with Validation

```typescript
// src/config/index.ts
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().min(1, 'DATABASE_URL is required'),
  REDIS_URL: z.string().optional(),
  JWT_SECRET: z.string().min(32, 'JWT_SECRET must be at least 32 characters'),
  LOG_LEVEL: z.enum(['debug', 'info', 'warn', 'error']).default('info'),
});

// Validate on startup - fails fast if config is wrong
export const config = envSchema.parse(process.env);

export type Config = z.infer<typeof envSchema>;
```

**Why validate on startup:**
- App fails immediately if config is wrong
- Clear error messages about what's missing
- No runtime surprises later

---

## Express App Setup

### Complete Production-Ready Setup

```typescript
// src/app.ts
import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import rateLimit from 'express-rate-limit';
import compression from 'compression';
import { errorHandler } from './middleware/errorHandler';
import { requestLogger } from './middleware/requestLogger';
import { userRoutes } from './routes/user.routes';

const app = express();

// Security middleware
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
    },
  },
}));

// CORS - configure for production
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:3000'],
  credentials: true,
}));

// Rate limiting
app.use(rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP',
}));

// Body parsing
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Compression
app.use(compression());

// Request logging
app.use(requestLogger);

// Routes
app.use('/api/users', userRoutes);
app.use('/api/health', (req, res) => res.json({ status: 'ok' }));

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    code: 'NOT_FOUND',
    message: `Route ${req.method} ${req.path} not found`,
  });
});

// Error handler - MUST be last
app.use(errorHandler);

export { app };
```

---

## Controller Pattern

### Thin Controllers (Best Practice)

```typescript
// src/controllers/user.controller.ts
import { Request, Response, NextFunction } from 'express';
import { userService } from '../services/user.service';

export const userController = {
  async getAll(req: Request, res: Response, next: NextFunction) {
    try {
      const users = await userService.findAll();
      res.json({ data: users });
    } catch (error) {
      next(error);  // Pass to error handler
    }
  },

  async getById(req: Request, res: Response, next: NextFunction) {
    try {
      const user = await userService.findById(req.params.id);
      res.json({ data: user });
    } catch (error) {
      next(error);
    }
  },

  async create(req: Request, res: Response, next: NextFunction) {
    try {
      const user = await userService.create(req.body);
      res.status(201).json({ data: user });
    } catch (error) {
      next(error);
    }
  },

  async update(req: Request, res: Response, next: NextFunction) {
    try {
      const user = await userService.update(req.params.id, req.body);
      res.json({ data: user });
    } catch (error) {
      next(error);
    }
  },

  async delete(req: Request, res: Response, next: NextFunction) {
    try {
      await userService.delete(req.params.id);
      res.status(204).send();
    } catch (error) {
      next(error);
    }
  },
};
```

**Why thin controllers:**
- Controllers should only: parse request, call service, return response
- Business logic goes in services
- Easy to test (just mock the service)

---

## Service Layer

### Business Logic Implementation

```typescript
// src/services/user.service.ts
import { userRepository } from '../repositories/user.repository';
import { CreateUserDto, UpdateUserDto, User } from '../models/user.model';
import { NotFoundError, ConflictError, ValidationError } from '../utils/errors';
import { logger } from '../utils/logger';

export const userService = {
  async findAll(): Promise<User[]> {
    return userRepository.findAll();
  },

  async findById(id: string): Promise<User> {
    const user = await userRepository.findById(id);
    if (!user) {
      throw new NotFoundError(`User with id ${id} not found`);
    }
    return user;
  },

  async create(dto: CreateUserDto): Promise<User> {
    // Check for duplicates
    const existing = await userRepository.findByEmail(dto.email);
    if (existing) {
      throw new ConflictError('Email already registered');
    }

    logger.info({ email: dto.email }, 'Creating new user');

    const user = await userRepository.create(dto);
    
    logger.info({ userId: user.id }, 'User created successfully');
    
    return user;
  },

  async update(id: string, dto: UpdateUserDto): Promise<User> {
    const existing = await userRepository.findById(id);
    if (!existing) {
      throw new NotFoundError(`User with id ${id} not found`);
    }

    // If email is being changed, check it's not taken
    if (dto.email && dto.email !== existing.email) {
      const duplicate = await userRepository.findByEmail(dto.email);
      if (duplicate) {
        throw new ConflictError('Email already registered');
      }
    }

    return userRepository.update(id, dto);
  },

  async delete(id: string): Promise<void> {
    const existing = await userRepository.findById(id);
    if (!existing) {
      throw new NotFoundError(`User with id ${id} not found`);
    }

    await userRepository.delete(id);
  },
};
```

---

## Common Node.js Mistakes

### Mistake 1: Unhandled Promise Rejections

**The Problem:**
```typescript
// ❌ WRONG - Unhandled rejection crashes the process
app.get('/users', async (req, res) => {
  const users = await userService.findAll();  // If this throws, app crashes!
  res.json(users);
});

// ❌ WRONG - Missing await
app.get('/users', async (req, res) => {
  const users = userService.findAll();  // Forgot await!
  res.json(users);  // Returns Promise, not actual data
});
```

**Why it crashes:**
- Unhandled promise rejection terminates Node.js process
- In Express, unhandled errors in async routes crash the server

**Solutions:**

**Option 1: try-catch in each route**
```typescript
app.get('/users', async (req, res, next) => {
  try {
    const users = await userService.findAll();
    res.json(users);
  } catch (error) {
    next(error);  // Pass to error handler
  }
});
```

**Option 2: Wrap async routes (Recommended)**
```typescript
// utils/asyncHandler.ts
export const asyncHandler = (fn: Function) => {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
};

// Usage
app.get('/users', asyncHandler(async (req, res) => {
  const users = await userService.findAll();
  res.json(users);
}));
```

**Option 3: Use framework that handles this (e.g., Fastify)**
```typescript
// Fastify handles async errors automatically
fastify.get('/users', async (req, res) => {
  const users = await userService.findAll();  // Errors caught automatically
  return users;
});
```

### Mistake 2: Blocking the Event Loop

**The Problem:**
```typescript
// ❌ WRONG - CPU-intensive work blocks all requests
app.post('/process', (req, res) => {
  const result = heavyComputation(req.body.data);  // Takes 5 seconds
  res.json(result);
});

// While this runs, NO OTHER REQUESTS are processed!
```

**Why it's bad:**
- Node.js is single-threaded
- CPU-intensive work blocks the event loop
- All other requests wait

**Solutions:**

**Option 1: Offload to worker thread**
```typescript
import { Worker } from 'worker_threads';

app.post('/process', async (req, res) => {
  const worker = new Worker('./workers/heavyComputation.js');
  worker.postMessage(req.body.data);
  
  worker.once('message', (result) => {
    res.json(result);
  });
});
```

**Option 2: Use child process**
```typescript
import { fork } from 'child_process';

app.post('/process', async (req, res) => {
  const child = fork('./processes/compute.js');
  child.send(req.body.data);
  
  child.once('message', (result) => {
    child.kill();
    res.json(result);
  });
});
```

**Option 3: Break into smaller chunks**
```typescript
// If possible, break work into smaller async chunks
app.post('/process', async (req, res) => {
  const chunks = splitIntoChunks(req.body.data, 100);
  const results = [];
  
  for (const chunk of chunks) {
    const result = await processChunk(chunk);
    results.push(result);
    // Yield to event loop between chunks
    await new Promise(resolve => setImmediate(resolve));
  }
  
  res.json(combineResults(results));
});
```

### Mistake 3: Memory Leaks

**The Problem:**
```typescript
// ❌ WRONG - Event listeners accumulate
app.get('/events', (req, res) => {
  const emitter = new EventEmitter();
  
  emitter.on('data', (data) => {
    res.write(data);
  });
  
  // If client disconnects, emitter and listeners stay in memory!
});

// ❌ WRONG - Closures capture large objects
function createHandler() {
  const hugeData = loadHugeDataset();  // 100MB
  
  return function handler(req, res) {
    // This closure keeps hugeData in memory forever
    res.json({ status: 'ok' });
  };
}

app.get('/api', createHandler());
```

**Solutions:**

**Clean up event listeners:**
```typescript
app.get('/events', (req, res) => {
  const emitter = new EventEmitter();
  
  const onData = (data: string) => {
    res.write(data);
  };
  
  const onClose = () => {
    emitter.off('data', onData);
    emitter.off('end', onEnd);
    res.end();
  };
  
  const onEnd = () => {
    emitter.off('data', onData);
    emitter.off('close', onClose);
    res.end();
  };
  
  emitter.on('data', onData);
  emitter.once('end', onEnd);
  emitter.once('close', onClose);
  
  // Also clean up if client disconnects
  req.on('close', onClose);
});
```

**Avoid capturing large objects:**
```typescript
// ✅ CORRECT - Load data only when needed
function createHandler() {
  return async function handler(req, res) {
    const data = await loadDataIfNeeded();  // Load on demand
    res.json({ data });
  };
}

// ✅ CORRECT - Use WeakMap for caches
const cache = new WeakMap();

function process(obj) {
  if (cache.has(obj)) {
    return cache.get(obj);
  }
  const result = expensiveOperation(obj);
  cache.set(obj, result);
  return result;
}
```

### Mistake 4: Not Handling Process Errors

**The Problem:**
```typescript
// ❌ WRONG - No error handling
process.on('unhandledRejection', (reason, promise) => {
  console.log('Unhandled Rejection at:', promise, 'reason:', reason);
});

// Or worse - nothing at all!
```

**Why it's critical:**
- Unhandled errors crash the process
- In production, this means downtime
- Error logs may be lost

**Solution:**
```typescript
// src/server.ts
process.on('unhandledRejection', (reason, promise) => {
  logger.error('Unhandled Rejection at:', promise, 'reason:', reason);
  // Graceful shutdown
  gracefulShutdown();
});

process.on('uncaughtException', (error) => {
  logger.error('Uncaught Exception:', error);
  // Cannot recover, must exit
  process.exit(1);
});

// Graceful shutdown function
async function gracefulShutdown() {
  logger.info('Starting graceful shutdown...');
  
  // Close server (stop accepting new connections)
  server.close(async () => {
    logger.info('Server closed');
    
    // Close database connections
    await db.close();
    logger.info('Database connections closed');
    
    // Flush logs
    await logger.flush();
    
    process.exit(0);
  });
  
  // Force shutdown after 30 seconds
  setTimeout(() => {
    logger.error('Forced shutdown');
    process.exit(1);
  }, 30000);
}

// Handle termination signals
process.on('SIGTERM', gracefulShutdown);
process.on('SIGINT', gracefulShutdown);
```

### Mistake 5: Not Validating Input

**The Problem:**
```typescript
// ❌ WRONG - No validation
app.post('/users', async (req, res) => {
  const user = await db.user.create(req.body);  // Could be anything!
  res.json(user);
});

// ❌ WRONG - Manual validation (error-prone)
app.post('/users', async (req, res) => {
  if (!req.body.email || !req.body.email.includes('@')) {
    return res.status(400).json({ error: 'Invalid email' });
  }
  if (!req.body.name || req.body.name.length < 2) {
    return res.status(400).json({ error: 'Name too short' });
  }
  // ... more manual validation
});
```

**Solution with Zod:**
```typescript
import { z } from 'zod';

// Define schema once, use everywhere
const createUserSchema = z.object({
  email: z.string()
    .min(1, 'Email is required')
    .email('Invalid email format'),
  name: z.string()
    .min(2, 'Name must be at least 2 characters')
    .max(100, 'Name must be less than 100 characters'),
  age: z.number()
    .int('Age must be a whole number')
    .min(18, 'Must be at least 18')
    .optional(),
});

// Validation middleware
export function validate(schema: z.ZodSchema) {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      const validated = await schema.parseAsync(req.body);
      req.body = validated;  // Replace with validated data
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        const messages = error.errors.map(e => `${e.path.join('.')}: ${e.message}`);
        return res.status(400).json({
          code: 'VALIDATION_ERROR',
          messages,
        });
      }
      next(error);
    }
  };
}

// Usage
app.post('/users', validate(createUserSchema), async (req, res) => {
  // req.body is now validated and typed
  const user = await userService.create(req.body);
  res.status(201).json(user);
});
```

---

## Error Handling

### Complete Error Handling Setup

```typescript
// src/utils/errors.ts
export class AppError extends Error {
  constructor(
    public message: string,
    public statusCode: number = 500,
    public code: string = 'INTERNAL_ERROR'
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string, id?: string) {
    super(
      id ? `${resource} with id ${id} not found` : `${resource} not found`,
      404,
      'NOT_FOUND'
    );
  }
}

export class ConflictError extends AppError {
  constructor(message: string) {
    super(message, 409, 'CONFLICT');
  }
}

export class ValidationError extends AppError {
  constructor(message: string) {
    super(message, 400, 'VALIDATION_ERROR');
  }
}

export class UnauthorizedError extends AppError {
  constructor(message: string = 'Unauthorized') {
    super(message, 401, 'UNAUTHORIZED');
  }
}

export class ForbiddenError extends AppError {
  constructor(message: string = 'Forbidden') {
    super(message, 403, 'FORBIDDEN');
  }
}

// src/middleware/errorHandler.ts
import { Request, Response, NextFunction } from 'express';
import { AppError } from '../utils/errors';
import { logger } from '../utils/logger';

export function errorHandler(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  // Log all errors
  logger.error({
    error: error.message,
    stack: error.stack,
    path: req.path,
    method: req.method,
    requestId: req.requestId,
  }, 'Error occurred');

  // Handle known application errors
  if (error instanceof AppError) {
    return res.status(error.statusCode).json({
      code: error.code,
      message: error.message,
      ...(process.env.NODE_ENV === 'development' && { stack: error.stack }),
    });
  }

  // Handle Zod validation errors
  if (error.name === 'ZodError') {
    return res.status(400).json({
      code: 'VALIDATION_ERROR',
      message: 'Invalid request data',
      details: error.errors,
    });
  }

  // Handle JWT errors
  if (error.name === 'JsonWebTokenError') {
    return res.status(401).json({
      code: 'INVALID_TOKEN',
      message: 'Invalid authentication token',
    });
  }

  // Handle database errors
  if (error.code === 'P2002') {  // Prisma unique constraint
    return res.status(409).json({
      code: 'DUPLICATE_ENTRY',
      message: 'Resource already exists',
    });
  }

  // Unknown error - don't expose details
  res.status(500).json({
    code: 'INTERNAL_ERROR',
    message: process.env.NODE_ENV === 'production' 
      ? 'An unexpected error occurred' 
      : error.message,
  });
}
```

---

## Logging

### Structured Logging with Pino

```typescript
// src/utils/logger.ts
import pino from 'pino';

export const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  transport: process.env.NODE_ENV !== 'production' 
    ? { target: 'pino-pretty' }
    : undefined,
  base: {
    service: process.env.APP_NAME,
    environment: process.env.NODE_ENV,
  },
  redact: {
    paths: ['password', '*.password', 'token', 'authorization'],
    remove: true,
  },
});

// Child logger for requests
export function requestLogger(req: Request, res: Response, next: NextFunction) {
  const requestId = req.headers['x-request-id'] || crypto.randomUUID();
  req.requestId = requestId;
  
  const childLogger = logger.child({
    requestId,
    path: req.path,
    method: req.method,
  });
  
  req.log = childLogger;
  
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = Date.now() - start;
    childLogger.info({
      statusCode: res.statusCode,
      duration,
    }, 'Request completed');
  });
  
  next();
}
```

---

## Database Best Practices

### Connection Pooling

```typescript
// ❌ WRONG - New connection per request
app.get('/users', async (req, res) => {
  const client = new pg.Client();  // ❌ New connection every time!
  await client.connect();
  const users = await client.query('SELECT * FROM users');
  await client.end();
  res.json(users.rows);
});

// ✅ CORRECT - Use connection pool
import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,  // Maximum pool size
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

app.get('/users', async (req, res) => {
  const client = await pool.connect();  // Reuses existing connection
  try {
    const users = await client.query('SELECT * FROM users');
    res.json(users.rows);
  } finally {
    client.release();  // Return to pool
  }
});
```

### Query Parameterization (Prevent SQL Injection)

```typescript
// ❌ WRONG - SQL Injection vulnerability
app.get('/users', async (req, res) => {
  const { email } = req.query;
  const result = await pool.query(`SELECT * FROM users WHERE email = '${email}'`);
  // attacker: email = ' OR '1'='1
});

// ✅ CORRECT - Parameterized queries
app.get('/users', async (req, res) => {
  const { email } = req.query;
  const result = await pool.query(
    'SELECT * FROM users WHERE email = $1',
    [email]  // Parameters escaped automatically
  );
  res.json(result.rows);
});
```

---

## Production Checklist

- [ ] TypeScript strict mode enabled
- [ ] Input validation on all endpoints
- [ ] Error handling middleware
- [ ] Request logging with correlation IDs
- [ ] Rate limiting configured
- [ ] Security headers (helmet)
- [ ] CORS properly configured
- [ ] Graceful shutdown handling
- [ ] Process error handlers (uncaughtException, unhandledRejection)
- [ ] Health check endpoint
- [ ] Database connection pooling
- [ ] Secrets in environment variables (never in code)
- [ ] Log rotation configured
- [ ] Memory monitoring

---

## Best Practices Summary

### Always Do
- ✅ Use TypeScript with strict mode
- ✅ Validate all inputs with Zod
- ✅ Use async/await (not callbacks)
- ✅ Handle all Promise rejections
- ✅ Use connection pooling
- ✅ Centralize error handling
- ✅ Add request logging
- ✅ Implement graceful shutdown

### Never Do
- ❌ Use require() (use ES6 imports)
- ❌ Ignore Promise rejections
- ❌ Block the event loop with CPU work
- ❌ Concatenate strings into SQL
- ❌ Expose stack traces in production
- ❌ Store secrets in code
- ❌ Ignore memory leaks
- ❌ Skip input validation

---

## Common AI Coding Mistakes (Autonomous Mode)

**When coding without user feedback, avoid these AI-specific errors:**

### 1. Unhandled Promise Rejections

**The Mistake:** Forgetting to catch async errors
```typescript
// ❌ WRONG - Unhandled rejection crashes the process
app.get('/users', async (req, res) => {
  const users = await db.getUsers();  // If this throws = crash!
  res.json(users);
});

// ✅ CORRECT - Try-catch
app.get('/users', async (req, res, next) => {
  try {
    const users = await db.getUsers();
    res.json(users);
  } catch (error) {
    next(error);
  }
});

// ✅ CORRECT - Error handler middleware
app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ error: 'Internal server error' });
});
```

### 2. Memory Leaks with Event Listeners

**The Mistake:** Adding listeners without removing them
```typescript
// ❌ WRONG - Listener accumulates
app.get('/events', (req, res) => {
  const emitter = new EventEmitter();
  emitter.on('data', (data) => res.write(data));
  // Never removed!
});

// ✅ CORRECT - Clean up
app.get('/events', (req, res) => {
  const emitter = new EventEmitter();
  const onData = (data) => res.write(data);
  emitter.on('data', onData);
  
  req.on('close', () => {
    emitter.off('data', onData);  // Clean up!
  });
});
```

### 3. Forgetting await

**The Mistake:** Calling async function without await
```typescript
// ❌ WRONG - Missing await
app.post('/users', async (req, res) => {
  const user = db.createUser(req.body);  // Forgot await!
  res.json(user);  // Returns Promise, not user
});

// ✅ CORRECT - Always await async functions
app.post('/users', async (req, res) => {
  const user = await db.createUser(req.body);
  res.json(user);
});
```

### 4. SQL Injection via String Concatenation

**The Mistake:** Building SQL with string concatenation
```typescript
// ❌ WRONG - SQL Injection
app.get('/users', async (req, res) => {
  const { email } = req.query;
  const query = `SELECT * FROM users WHERE email = '${email}'`;
  // Attacker: email = "' OR '1'='1"
  const users = await db.query(query);
});

// ✅ CORRECT - Parameterized queries
app.get('/users', async (req, res) => {
  const { email } = req.query;
  const users = await db.query(
    'SELECT * FROM users WHERE email = $1',
    [email]
  );
});
```

### 5. Autonomous Decision Checklist

**Before generating code, verify:**

- [ ] All async functions have await
- [ ] All promises have error handling (try-catch or .catch())
- [ ] No string concatenation into SQL queries
- [ ] Event listeners have matching remove listener
- [ ] No console.log left in production code
- [ ] All environment variables are validated
- [ ] Secrets are not hardcoded

**When uncertain about an API:**
```typescript
// Add a comment documenting uncertainty
// UNCERTAIN: Not sure if db.query() returns array or object
// ASSUMPTION: Assuming it returns array like pg
// REVIEW: Please verify return type matches your DB driver
const users = await db.query('SELECT * FROM users');
```
