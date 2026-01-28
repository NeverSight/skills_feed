---
name: backend-scaffolding
description: Scaffold a Koa-based backend server with standard structure including config, logging, routes, models, and database setup. Use when asked to "create a backend", "scaffold backend", "set up an API server", or "initialize backend structure".
---

# Backend Scaffolding

Scaffold a Koa-based backend server with configuration, logging, routing with Zod validation, Mongoose models, and database connectivity.

## Structure Overview

```
apps/backend/src/
├── config/
│   └── index.ts          # Centralized configuration (env vars)
├── lib/
│   └── logger/
│       └── index.ts      # Pino logger with pretty printing
├── models/
│   ├── _utils.ts         # Model utilities (generateId, stripId)
│   ├── db.ts             # MongoDB connection
│   └── {Model}.ts        # Mongoose models
├── routes/
│   └── {resource}.ts     # koa-zod-router routes
└── main.ts               # Application entry point
```

## Installation

```bash
npm install koa @koa/cors koa-bodyparser koa-mount koa-static koa-zod-router mongoose pino zod uuid
npm install -D @types/koa @types/koa__cors @types/koa-bodyparser @types/koa-mount @types/koa-static pino-pretty
```

For WebSocket support: `npm install koa-websocket @types/koa-websocket`

## Implementation Steps

### 1. Config Module (`config/index.ts`)

Centralize all environment variables. **Never use `process.env` directly outside this file.**

```typescript
const isDev = process.env.NODE_ENV !== 'production';

const config = {
  isDev,
  port: process.env.PORT || 3333,
  mongo: {
    database: process.env.MONGO_DATABASE || 'myapp',
    protocol: process.env.MONGO_PROTOCOL || 'mongodb',
    host: process.env.MONGO_HOST || 'localhost:27017',
    username: process.env.MONGO_USERNAME || '',
    password: process.env.MONGO_PASSWORD || '',
  },
  logging: {
    level: process.env.LOG_LEVEL || (isDev ? 'debug' : 'info'),
    routeLogging: process.env.ROUTE_LOGGING !== 'false',
  },
};

export default config;
```

### 2. Logger Module (`lib/logger/index.ts`)

```typescript
import pino from 'pino';
import config from '../../config';

export const logger = pino({
  level: config.logging.level,
  transport: config.isDev
    ? { target: 'pino-pretty', options: { colorize: true, translateTime: 'SYS:standard', ignore: 'pid,hostname' } }
    : undefined,
});

export const createLogger = (name: string) => logger.child({ name });
export default logger;
```

### 3. Model Utilities (`models/_utils.ts`)

```typescript
import { v4 as uuidv4 } from 'uuid';

export const generateId = (): string => uuidv4();

export const stripId = (_doc: unknown, ret: Record<string, unknown>) => {
  delete ret._id;
  return ret;
};
```

### 4. Database Connection (`models/db.ts`)

```typescript
import mongoose from 'mongoose';
import config from '../config';
import { createLogger } from '../lib/logger';

const log = createLogger('db');

export async function init() {
  const user = config.mongo.username && config.mongo.password
    ? `${encodeURIComponent(config.mongo.username)}:${encodeURIComponent(config.mongo.password)}@`
    : '';
  const connectionString = `${config.mongo.protocol}://${user}${config.mongo.host}/${config.mongo.database}`;
  await mongoose.connect(connectionString);
  log.info({ database: config.mongo.database }, 'Connected to MongoDB');
}
```

### 5. Models, Routes, and Main Entry Point

See [references/examples.md](references/examples.md) for complete code examples including:
- Example Mongoose model with proper typing
- Example routes with Zod validation (CRUD operations)
- Main entry point with middleware setup
- Shared types definition

## Environment Variables

```bash
PORT=3333
NODE_ENV=development
MONGO_DATABASE=myapp
MONGO_PROTOCOL=mongodb
MONGO_HOST=localhost:27017
MONGO_USERNAME=
MONGO_PASSWORD=
LOG_LEVEL=debug
ROUTE_LOGGING=true
```

## Checklist

1. **Install dependencies**: `npm install`
2. **Start MongoDB**: `docker compose up -d` or local MongoDB
3. **Set environment**: Copy `.env.example` to `.env.local`, run `direnv allow`
4. **Start backend**: `just serve-backend`
5. **Test health**: `curl http://localhost:3333/api`
6. **Test CRUD**: See examples in [references/examples.md](references/examples.md)

## Best Practices

1. **Config**: Always use `config` object, never `process.env` directly
2. **Logging**: Use `createLogger('module-name')`, never `console.log`
3. **Routes**: Use `koa-zod-router` with Zod schemas for validation
4. **Models**: Use `generateId()` for IDs, `stripId` transform for JSON output
5. **Types**: Define shared types in `libs/types`, import via `@{project}/types`
6. **Errors**: Return structured error responses with appropriate status codes
