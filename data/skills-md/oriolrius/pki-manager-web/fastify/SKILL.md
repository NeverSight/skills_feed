---
name: Fastify
description: Expert guidance for Fastify web framework including server setup, routing, plugins, hooks, validation, error handling, and TypeScript integration. Use this when building high-performance Node.js web servers and REST APIs.
---

# Fastify

Expert assistance with Fastify - Fast and low overhead web framework for Node.js.

## Overview

Fastify is a highly performant web framework:
- **Fast**: One of the fastest Node.js frameworks
- **Low Overhead**: Minimal resource consumption
- **Schema-based**: JSON Schema validation
- **TypeScript**: Excellent TypeScript support
- **Plugin Architecture**: Extensible with plugins
- **Logging**: Built-in logging with Pino

## Installation

```bash
npm install fastify
npm install --save-dev @types/node

# Common plugins
npm install @fastify/cors          # CORS support
npm install @fastify/websocket     # WebSocket support
npm install @fastify/cookie        # Cookie parsing
npm install @fastify/jwt           # JWT authentication
npm install @fastify/helmet        # Security headers
npm install @fastify/rate-limit    # Rate limiting
```

## Quick Start

```typescript
import Fastify from 'fastify';

const server = Fastify({
  logger: true, // Enable Pino logging
});

server.get('/ping', async (request, reply) => {
  return { pong: 'it worked!' };
});

await server.listen({ port: 3000, host: '0.0.0.0' });
console.log('Server listening on http://localhost:3000');
```

## Server Configuration

```typescript
import Fastify from 'fastify';

const server = Fastify({
  logger: {
    level: 'info',
    transport: {
      target: 'pino-pretty', // Pretty printing in development
    },
  },
  bodyLimit: 1048576, // 1MB body limit
  caseSensitive: true, // Case-sensitive routes
  ignoreTrailingSlash: false,
  requestIdHeader: 'x-request-id',
  requestIdLogLabel: 'reqId',
  trustProxy: true, // Trust proxy headers
});
```

## Routing

### Basic Routes

```typescript
// GET
server.get('/users', async (request, reply) => {
  return [{ id: 1, name: 'John' }];
});

// POST
server.post('/users', async (request, reply) => {
  const { name, email } = request.body;
  return { id: 2, name, email };
});

// PUT
server.put('/users/:id', async (request, reply) => {
  const { id } = request.params;
  const { name } = request.body;
  return { id, name };
});

// DELETE
server.delete('/users/:id', async (request, reply) => {
  const { id } = request.params;
  return { deleted: id };
});

// PATCH
server.patch('/users/:id', async (request, reply) => {
  return { updated: true };
});
```

### Route Parameters

```typescript
// URL parameters
server.get<{
  Params: { id: string };
}>('/users/:id', async (request, reply) => {
  const { id } = request.params; // Typed!
  return { id };
});

// Multiple parameters
server.get<{
  Params: { userId: string; postId: string };
}>('/users/:userId/posts/:postId', async (request, reply) => {
  const { userId, postId } = request.params;
  return { userId, postId };
});

// Query parameters
server.get<{
  Querystring: { search?: string; limit?: number };
}>('/search', async (request, reply) => {
  const { search, limit = 10 } = request.query;
  return { search, limit };
});
```

### TypeScript Types

```typescript
import { FastifyRequest, FastifyReply } from 'fastify';

interface CreateUserBody {
  name: string;
  email: string;
}

interface UserParams {
  id: string;
}

server.post<{
  Body: CreateUserBody;
}>('/users', async (request, reply) => {
  const { name, email } = request.body; // Fully typed
  return { id: '1', name, email };
});

server.get<{
  Params: UserParams;
}>('/users/:id', async (request, reply) => {
  const { id } = request.params;
  return { id };
});
```

## Validation

### JSON Schema Validation

```typescript
const createUserSchema = {
  body: {
    type: 'object',
    required: ['name', 'email'],
    properties: {
      name: { type: 'string', minLength: 2 },
      email: { type: 'string', format: 'email' },
      age: { type: 'number', minimum: 18 },
    },
  },
  response: {
    201: {
      type: 'object',
      properties: {
        id: { type: 'string' },
        name: { type: 'string' },
        email: { type: 'string' },
      },
    },
  },
};

server.post('/users', {
  schema: createUserSchema,
}, async (request, reply) => {
  const { name, email, age } = request.body;
  reply.status(201);
  return { id: '1', name, email };
});
```

## Plugins

### Register Plugins

```typescript
import cors from '@fastify/cors';
import helmet from '@fastify/helmet';
import rateLimit from '@fastify/rate-limit';

// CORS
await server.register(cors, {
  origin: true, // Reflect origin
  credentials: true,
});

// Security headers
await server.register(helmet);

// Rate limiting
await server.register(rateLimit, {
  max: 100, // 100 requests
  timeWindow: '1 minute',
});
```

### Custom Plugin

```typescript
import fp from 'fastify-plugin';

const myPlugin = fp(async (fastify, options) => {
  // Add decorator
  fastify.decorate('myUtility', () => {
    return 'Hello from plugin!';
  });

  // Add hook
  fastify.addHook('onRequest', async (request, reply) => {
    // Do something on every request
  });
}, {
  name: 'my-plugin',
  fastify: '4.x',
});

await server.register(myPlugin);

// Use decorator
server.get('/test', async (request, reply) => {
  return { message: server.myUtility() };
});
```

## Hooks

```typescript
// Application hooks
server.addHook('onRequest', async (request, reply) => {
  // Called before route handler
  request.log.info('Incoming request');
});

server.addHook('preHandler', async (request, reply) => {
  // Called after validation, before handler
  if (!request.headers.authorization) {
    reply.code(401).send({ error: 'Unauthorized' });
  }
});

server.addHook('onSend', async (request, reply, payload) => {
  // Called before sending response
  return payload;
});

server.addHook('onResponse', async (request, reply) => {
  // Called after response sent
  request.log.info({ responseTime: reply.getResponseTime() });
});

server.addHook('onError', async (request, reply, error) => {
  // Called on error
  request.log.error(error);
});
```

## Error Handling

```typescript
// Custom error handler
server.setErrorHandler((error, request, reply) => {
  request.log.error(error);

  if (error.validation) {
    reply.status(400).send({
      error: 'Validation Error',
      message: error.message,
      details: error.validation,
    });
    return;
  }

  reply.status(error.statusCode || 500).send({
    error: error.name,
    message: error.message,
  });
});

// Throw errors in routes
server.get('/error', async (request, reply) => {
  throw new Error('Something went wrong!');
});

// Send error responses
server.get('/not-found', async (request, reply) => {
  reply.code(404).send({ error: 'Not found' });
});
```

## tRPC Integration

```typescript
import { fastifyTRPCPlugin } from '@trpc/server/adapters/fastify';
import { appRouter } from './trpc/router';
import { createContext } from './trpc/context';

// Register tRPC
await server.register(fastifyTRPCPlugin, {
  prefix: '/trpc',
  trpcOptions: {
    router: appRouter,
    createContext,
  },
});
```

## WebSocket Support

```typescript
import websocket from '@fastify/websocket';

await server.register(websocket);

server.get('/ws', { websocket: true }, (connection, request) => {
  connection.socket.on('message', (message) => {
    connection.socket.send('Hello from server!');
  });
});
```

## Testing

```typescript
import { test } from 'node:test';
import Fastify from 'fastify';

test('GET /ping returns pong', async (t) => {
  const server = Fastify();

  server.get('/ping', async () => {
    return { pong: 'it worked!' };
  });

  const response = await server.inject({
    method: 'GET',
    url: '/ping',
  });

  t.assert.strictEqual(response.statusCode, 200);
  t.assert.deepStrictEqual(response.json(), { pong: 'it worked!' });
});
```

## Best Practices

1. **Use Plugins**: Encapsulate functionality in plugins
2. **Schema Validation**: Always validate input with JSON Schema
3. **Error Handling**: Set up global error handler
4. **Logging**: Use built-in Pino logger
5. **TypeScript**: Leverage type safety
6. **Hooks**: Use hooks for cross-cutting concerns
7. **Async/Await**: Use async handlers
8. **Testing**: Use fastify.inject() for testing
9. **Performance**: Enable HTTP/2 for better performance
10. **Security**: Use @fastify/helmet for security headers

## Resources

- Documentation: https://www.fastify.io/docs/latest/
- GitHub: https://github.com/fastify/fastify
- Plugins: https://www.fastify.io/ecosystem/
