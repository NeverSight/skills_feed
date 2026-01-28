---
name: backend-websocket
description: Add WebSocket support with authentication to the backend. Use when asked to "add websocket", "add real-time", "add ws support", or "create websocket endpoint".
---

# Backend WebSocket Support

This skill adds WebSocket support to a Koa backend with JWT authentication.

## Overview

WebSocket connections require:
1. JWT authentication as the first message
2. Structured message format for all communication
3. Proper cleanup on disconnect

## Installation

```bash
npm install koa-websocket short-uuid @types/koa-websocket
```

## Implementation

### Step 1: Enable WebSocket Support

Update `apps/backend/src/main.ts`:

```typescript
import Koa from 'koa';
import websockify from 'koa-websocket';
import short from 'short-uuid';

// Create websocket-enabled Koa app
const app = websockify(new Koa());

// ... rest of app setup ...
```

### Step 2: Create Auth Middleware

Create `apps/backend/src/middleware/wsAuth.ts`:

```typescript
import Koa from 'koa';
import short from 'short-uuid';
import { createLogger } from '../lib/logger';

const log = createLogger('ws-auth');

type WsNext = (ctx: Koa.Context) => Promise<void>;

// Your JWT verification function
async function verifyToken(token: string): Promise<{ uid: string; email: string }> {
  // Implement your JWT verification logic
  // This should throw if token is invalid
  throw new Error('Implement verifyToken');
}

/**
 * WebSocket authentication middleware
 * Requires JWT token as first message
 */
export async function wsAuthMiddleware(ctx: Koa.Context, next: WsNext): Promise<void> {
  // Generate unique ID for this connection
  ctx.websocket['_id'] = short.generate();

  log.debug({ connId: ctx.websocket['_id'] }, 'WebSocket connection received, waiting for auth');

  // First message must be authentication
  ctx.websocket.once('message', async (message) => {
    try {
      const data = JSON.parse(message.toString());

      if (data.type !== 'login' || !data.token) {
        log.warn({ connId: ctx.websocket['_id'] }, 'Invalid login message');
        ctx.websocket.send(JSON.stringify({
          type: 'error',
          message: 'First message must be login with token',
        }));
        ctx.websocket.close();
        return;
      }

      // Verify JWT token
      const user = await verifyToken(data.token);
      ctx.state.user = user;

      log.info({ connId: ctx.websocket['_id'], uid: user.uid }, 'WebSocket authenticated');

      ctx.websocket.send(JSON.stringify({
        type: 'auth',
        message: 'Authenticated',
      }));

      // Remove this listener and proceed to route handlers
      ctx.websocket.removeAllListeners('message');
      return next(ctx);

    } catch (err) {
      log.error({ err, connId: ctx.websocket['_id'] }, 'WebSocket auth failed');
      ctx.websocket.send(JSON.stringify({
        type: 'error',
        message: 'Authentication failed',
      }));
      ctx.websocket.close();
    }
  });
}
```

### Step 3: Create WebSocket Route

Create `apps/backend/src/routes/websocket/chat.ts`:

```typescript
import Router from '@koa/router';
import { createLogger } from '../../lib/logger';

const log = createLogger('ws-chat');
const router = new Router();

// Message type definitions
type IncomingMessage =
  | { type: 'chat'; message: string }
  | { type: 'typing'; isTyping: boolean }
  | { type: 'ping' };

type OutgoingMessage =
  | { type: 'chat'; message: string; from: string; timestamp: number }
  | { type: 'typing'; userId: string; isTyping: boolean }
  | { type: 'pong' }
  | { type: 'error'; message: string };

router.all('/chat', async (ctx) => {
  const user = ctx.state.user;
  const connId = ctx.websocket['_id'];

  log.info({ connId, uid: user.uid }, 'Chat WebSocket connected');

  // Handle incoming messages
  ctx.websocket.on('message', async (rawMessage) => {
    try {
      const message: IncomingMessage = JSON.parse(rawMessage.toString());

      switch (message.type) {
        case 'chat':
          // Process chat message
          const response: OutgoingMessage = {
            type: 'chat',
            message: `Echo: ${message.message}`,
            from: 'server',
            timestamp: Date.now(),
          };
          ctx.websocket.send(JSON.stringify(response));
          break;

        case 'typing':
          // Handle typing indicator
          log.debug({ connId, isTyping: message.isTyping }, 'Typing status');
          break;

        case 'ping':
          ctx.websocket.send(JSON.stringify({ type: 'pong' }));
          break;

        default:
          ctx.websocket.send(JSON.stringify({
            type: 'error',
            message: 'Unknown message type',
          }));
      }
    } catch (err) {
      log.error({ err, connId }, 'Error processing message');
      ctx.websocket.send(JSON.stringify({
        type: 'error',
        message: 'Invalid message format',
      }));
    }
  });

  // Handle disconnect
  ctx.websocket.on('close', () => {
    log.info({ connId, uid: user.uid }, 'Chat WebSocket disconnected');
    // Clean up any resources (e.g., remove from active users)
  });

  // Handle errors
  ctx.websocket.on('error', (err) => {
    log.error({ err, connId }, 'WebSocket error');
  });
});

export default router;
```

### Step 4: Mount WebSocket Routes

Update `apps/backend/src/main.ts`:

```typescript
import { wsAuthMiddleware } from './middleware/wsAuth';
import chatWsRoutes from './routes/websocket/chat';
import mount from 'koa-mount';

// WebSocket middleware (authentication)
app.ws.use(wsAuthMiddleware);

// Mount WebSocket routes
app.ws.use(mount('/ws', chatWsRoutes.middleware()));
```

## Client-Side Usage

### Connection Flow

```typescript
class WebSocketClient {
  private ws: WebSocket | null = null;
  private authenticated = false;

  connect(url: string, token: string): Promise<void> {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(url);

      this.ws.onopen = () => {
        // Send authentication message
        this.ws!.send(JSON.stringify({
          type: 'login',
          token: token,
        }));
      };

      this.ws.onmessage = (event) => {
        const message = JSON.parse(event.data);

        if (!this.authenticated) {
          if (message.type === 'auth') {
            this.authenticated = true;
            resolve();
          } else if (message.type === 'error') {
            reject(new Error(message.message));
          }
          return;
        }

        // Handle other messages
        this.handleMessage(message);
      };

      this.ws.onerror = (error) => {
        reject(error);
      };
    });
  }

  send(message: object): void {
    if (!this.authenticated || !this.ws) {
      throw new Error('Not connected');
    }
    this.ws.send(JSON.stringify(message));
  }

  private handleMessage(message: any): void {
    // Handle incoming messages
    console.log('Received:', message);
  }
}

// Usage
const client = new WebSocketClient();
await client.connect('wss://api.example.com/ws/chat', jwtToken);
client.send({ type: 'chat', message: 'Hello!' });
```

## Message Format Convention

Always use structured messages:

```typescript
// Incoming (client -> server)
{
  type: 'message_type',
  // ... payload fields
}

// Outgoing (server -> client)
{
  type: 'message_type',
  // ... payload fields
  timestamp?: number  // optional, for ordering
}

// Error responses
{
  type: 'error',
  message: 'Human readable error message'
}
```

## Best Practices

### 1. Always Authenticate First

```typescript
// Server: reject if first message isn't login
if (data.type !== 'login') {
  ctx.websocket.close();
  return;
}
```

### 2. Generate Connection IDs

```typescript
ctx.websocket['_id'] = short.generate();
// Use in all logs for tracing
```

### 3. Type Your Messages

```typescript
type IncomingMessage =
  | { type: 'chat'; message: string }
  | { type: 'ping' };

// Use discriminated unions for type safety
```

### 4. Handle Cleanup

```typescript
ctx.websocket.on('close', () => {
  // Remove from active connections
  // Cancel any pending operations
  // Clean up subscriptions
});
```

### 5. Add Heartbeat/Ping

```typescript
// Client sends ping periodically
setInterval(() => {
  ws.send(JSON.stringify({ type: 'ping' }));
}, 30000);

// Server responds with pong
case 'ping':
  ctx.websocket.send(JSON.stringify({ type: 'pong' }));
  break;
```

## File Structure

```
apps/backend/src/
├── middleware/
│   └── wsAuth.ts           # WebSocket authentication
├── routes/
│   └── websocket/
│       ├── chat.ts         # Chat WebSocket routes
│       └── notifications.ts # Other WS routes
└── main.ts                 # Mount WS routes
```

## Checklist

1. **Install** dependencies: `npm install koa-websocket short-uuid`
2. **Wrap app** with `websockify()` in main.ts
3. **Create** `middleware/wsAuth.ts` for authentication
4. **Implement** `verifyToken()` with your JWT logic
5. **Create** WebSocket route files in `routes/websocket/`
6. **Mount** routes with `app.ws.use(mount(...))`
7. **Test** connection flow with client
