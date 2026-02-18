---
name: realtime-systems
description: WebSocket, real-time communication, and event-driven architectures
domain: development-stacks
version: 1.0.0
tags: [websocket, socket-io, sse, pubsub, real-time, events]
triggers:
  keywords:
    primary: [realtime, real-time, websocket, socket.io, sse, pubsub]
    secondary: [event driven, push, streaming, live, notification, kafka, rabbitmq]
  context_boost: [chat, collaboration, live update, sync]
  context_penalty: [batch, static, frontend]
  priority: medium
---

# Real-time Systems

## Overview

Building real-time applications with WebSocket, Server-Sent Events, and event-driven architectures.

---

## WebSocket

### Server Implementation (Node.js)

```typescript
import { WebSocketServer, WebSocket } from 'ws';
import { createServer } from 'http';
import { v4 as uuid } from 'uuid';

const server = createServer();
const wss = new WebSocketServer({ server });

interface Client {
  id: string;
  ws: WebSocket;
  userId?: string;
  rooms: Set<string>;
}

const clients = new Map<string, Client>();
const rooms = new Map<string, Set<string>>();

wss.on('connection', (ws, req) => {
  const clientId = uuid();
  const client: Client = {
    id: clientId,
    ws,
    rooms: new Set(),
  };

  clients.set(clientId, client);
  console.log(`Client connected: ${clientId}`);

  // Handle messages
  ws.on('message', (data) => {
    try {
      const message = JSON.parse(data.toString());
      handleMessage(client, message);
    } catch (error) {
      console.error('Invalid message:', error);
    }
  });

  // Handle disconnection
  ws.on('close', () => {
    // Leave all rooms
    client.rooms.forEach(room => leaveRoom(client, room));
    clients.delete(clientId);
    console.log(`Client disconnected: ${clientId}`);
  });

  // Send connection confirmation
  send(ws, { type: 'connected', clientId });
});

function handleMessage(client: Client, message: any) {
  switch (message.type) {
    case 'authenticate':
      client.userId = message.userId;
      break;

    case 'join':
      joinRoom(client, message.room);
      break;

    case 'leave':
      leaveRoom(client, message.room);
      break;

    case 'message':
      broadcastToRoom(message.room, {
        type: 'message',
        from: client.userId,
        content: message.content,
        timestamp: Date.now(),
      }, client.id);
      break;

    case 'ping':
      send(client.ws, { type: 'pong' });
      break;
  }
}

function joinRoom(client: Client, room: string) {
  if (!rooms.has(room)) {
    rooms.set(room, new Set());
  }
  rooms.get(room)!.add(client.id);
  client.rooms.add(room);

  // Notify room members
  broadcastToRoom(room, {
    type: 'user_joined',
    userId: client.userId,
    room,
  }, client.id);
}

function leaveRoom(client: Client, room: string) {
  rooms.get(room)?.delete(client.id);
  client.rooms.delete(room);

  // Notify room members
  broadcastToRoom(room, {
    type: 'user_left',
    userId: client.userId,
    room,
  });
}

function broadcastToRoom(room: string, message: any, excludeClientId?: string) {
  const roomClients = rooms.get(room);
  if (!roomClients) return;

  roomClients.forEach(clientId => {
    if (clientId !== excludeClientId) {
      const client = clients.get(clientId);
      if (client?.ws.readyState === WebSocket.OPEN) {
        send(client.ws, message);
      }
    }
  });
}

function send(ws: WebSocket, message: any) {
  ws.send(JSON.stringify(message));
}

server.listen(8080);
```

### Client Implementation

```typescript
class WebSocketClient {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private messageHandlers = new Map<string, Set<Function>>();
  private messageQueue: any[] = [];

  constructor(private url: string) {}

  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        console.log('WebSocket connected');
        this.reconnectAttempts = 0;
        this.flushMessageQueue();
        resolve();
      };

      this.ws.onmessage = (event) => {
        const message = JSON.parse(event.data);
        this.handleMessage(message);
      };

      this.ws.onclose = (event) => {
        console.log('WebSocket closed:', event.code, event.reason);
        this.attemptReconnect();
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        reject(error);
      };
    });
  }

  private attemptReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      return;
    }

    this.reconnectAttempts++;
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);

    console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);

    setTimeout(() => {
      this.connect().catch(() => {});
    }, delay);
  }

  send(message: any) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    } else {
      // Queue message for when connection is restored
      this.messageQueue.push(message);
    }
  }

  private flushMessageQueue() {
    while (this.messageQueue.length > 0) {
      const message = this.messageQueue.shift();
      this.send(message);
    }
  }

  private handleMessage(message: any) {
    const handlers = this.messageHandlers.get(message.type);
    handlers?.forEach(handler => handler(message));

    // Also emit to wildcard handlers
    const wildcardHandlers = this.messageHandlers.get('*');
    wildcardHandlers?.forEach(handler => handler(message));
  }

  on(type: string, handler: Function) {
    if (!this.messageHandlers.has(type)) {
      this.messageHandlers.set(type, new Set());
    }
    this.messageHandlers.get(type)!.add(handler);

    // Return unsubscribe function
    return () => {
      this.messageHandlers.get(type)?.delete(handler);
    };
  }

  // Convenience methods
  joinRoom(room: string) {
    this.send({ type: 'join', room });
  }

  leaveRoom(room: string) {
    this.send({ type: 'leave', room });
  }

  sendMessage(room: string, content: string) {
    this.send({ type: 'message', room, content });
  }

  disconnect() {
    this.ws?.close();
    this.ws = null;
  }
}

// Usage
const ws = new WebSocketClient('wss://api.example.com/ws');

ws.on('connected', (msg) => {
  console.log('Connected with ID:', msg.clientId);
  ws.joinRoom('general');
});

ws.on('message', (msg) => {
  console.log(`[${msg.from}]: ${msg.content}`);
});

await ws.connect();
```

---

## Socket.IO

### Server

```typescript
import { Server } from 'socket.io';
import { createServer } from 'http';
import { createAdapter } from '@socket.io/redis-adapter';
import { createClient } from 'redis';

const httpServer = createServer();
const io = new Server(httpServer, {
  cors: {
    origin: process.env.ALLOWED_ORIGINS?.split(',') || '*',
    credentials: true,
  },
});

// Redis adapter for horizontal scaling
const pubClient = createClient({ url: process.env.REDIS_URL });
const subClient = pubClient.duplicate();

Promise.all([pubClient.connect(), subClient.connect()]).then(() => {
  io.adapter(createAdapter(pubClient, subClient));
});

// Authentication middleware
io.use(async (socket, next) => {
  const token = socket.handshake.auth.token;

  try {
    const user = await verifyToken(token);
    socket.data.user = user;
    next();
  } catch (err) {
    next(new Error('Authentication failed'));
  }
});

// Namespace for chat
const chatNamespace = io.of('/chat');

chatNamespace.on('connection', (socket) => {
  const user = socket.data.user;
  console.log(`User connected: ${user.name}`);

  // Join user's personal room
  socket.join(`user:${user.id}`);

  // Join a chat room
  socket.on('join_room', async (roomId: string) => {
    // Verify access
    const hasAccess = await checkRoomAccess(user.id, roomId);
    if (!hasAccess) {
      socket.emit('error', { message: 'Access denied' });
      return;
    }

    socket.join(roomId);

    // Notify room members
    socket.to(roomId).emit('user_joined', {
      userId: user.id,
      userName: user.name,
    });

    // Send recent messages
    const messages = await getRecentMessages(roomId, 50);
    socket.emit('room_history', { roomId, messages });
  });

  // Leave room
  socket.on('leave_room', (roomId: string) => {
    socket.leave(roomId);
    socket.to(roomId).emit('user_left', {
      userId: user.id,
      userName: user.name,
    });
  });

  // Send message
  socket.on('message', async (data: { roomId: string; content: string }) => {
    const message = {
      id: uuid(),
      roomId: data.roomId,
      userId: user.id,
      userName: user.name,
      content: data.content,
      timestamp: new Date(),
    };

    // Persist message
    await saveMessage(message);

    // Broadcast to room
    chatNamespace.to(data.roomId).emit('message', message);
  });

  // Typing indicator
  socket.on('typing_start', (roomId: string) => {
    socket.to(roomId).emit('user_typing', {
      userId: user.id,
      userName: user.name,
    });
  });

  socket.on('typing_stop', (roomId: string) => {
    socket.to(roomId).emit('user_stopped_typing', {
      userId: user.id,
    });
  });

  // Disconnect
  socket.on('disconnect', () => {
    console.log(`User disconnected: ${user.name}`);
  });
});

// Send to specific user (from anywhere in the app)
function sendToUser(userId: string, event: string, data: any) {
  chatNamespace.to(`user:${userId}`).emit(event, data);
}

httpServer.listen(3000);
```

### Client (React)

```tsx
import { io, Socket } from 'socket.io-client';
import { createContext, useContext, useEffect, useState } from 'react';

// Socket context
const SocketContext = createContext<Socket | null>(null);

export function SocketProvider({ children }: { children: React.ReactNode }) {
  const [socket, setSocket] = useState<Socket | null>(null);
  const { token } = useAuth();

  useEffect(() => {
    if (!token) return;

    const newSocket = io(`${API_URL}/chat`, {
      auth: { token },
      transports: ['websocket'],
    });

    newSocket.on('connect', () => {
      console.log('Socket connected');
    });

    newSocket.on('connect_error', (error) => {
      console.error('Socket connection error:', error);
    });

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, [token]);

  return (
    <SocketContext.Provider value={socket}>
      {children}
    </SocketContext.Provider>
  );
}

export function useSocket() {
  return useContext(SocketContext);
}

// Chat room hook
function useChatRoom(roomId: string) {
  const socket = useSocket();
  const [messages, setMessages] = useState<Message[]>([]);
  const [typingUsers, setTypingUsers] = useState<Set<string>>(new Set());

  useEffect(() => {
    if (!socket || !roomId) return;

    // Join room
    socket.emit('join_room', roomId);

    // Listen for messages
    socket.on('message', (message: Message) => {
      setMessages(prev => [...prev, message]);
    });

    // Room history
    socket.on('room_history', ({ messages }: { messages: Message[] }) => {
      setMessages(messages);
    });

    // Typing indicators
    socket.on('user_typing', ({ userId }: { userId: string }) => {
      setTypingUsers(prev => new Set(prev).add(userId));
    });

    socket.on('user_stopped_typing', ({ userId }: { userId: string }) => {
      setTypingUsers(prev => {
        const next = new Set(prev);
        next.delete(userId);
        return next;
      });
    });

    return () => {
      socket.emit('leave_room', roomId);
      socket.off('message');
      socket.off('room_history');
      socket.off('user_typing');
      socket.off('user_stopped_typing');
    };
  }, [socket, roomId]);

  const sendMessage = (content: string) => {
    socket?.emit('message', { roomId, content });
  };

  const startTyping = () => {
    socket?.emit('typing_start', roomId);
  };

  const stopTyping = () => {
    socket?.emit('typing_stop', roomId);
  };

  return { messages, typingUsers, sendMessage, startTyping, stopTyping };
}
```

---

## Server-Sent Events (SSE)

### Server

```typescript
import express from 'express';

const app = express();

// SSE endpoint
app.get('/events', (req, res) => {
  // Set SSE headers
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  // Send initial connection event
  res.write(`event: connected\ndata: ${JSON.stringify({ time: Date.now() })}\n\n`);

  // Keep-alive interval
  const keepAlive = setInterval(() => {
    res.write(`: keep-alive\n\n`);
  }, 30000);

  // Subscribe to events
  const unsubscribe = eventEmitter.on('update', (data) => {
    res.write(`event: update\ndata: ${JSON.stringify(data)}\n\n`);
  });

  // Handle client disconnect
  req.on('close', () => {
    clearInterval(keepAlive);
    unsubscribe();
  });
});

// With user-specific events
app.get('/events/user/:userId', authenticate, (req, res) => {
  const { userId } = req.params;

  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  // Subscribe to user-specific channel
  const channel = `user:${userId}`;
  const unsubscribe = pubsub.subscribe(channel, (message) => {
    res.write(`event: ${message.type}\ndata: ${JSON.stringify(message.data)}\n\n`);
  });

  req.on('close', () => {
    unsubscribe();
  });
});
```

### Client

```typescript
class EventSourceClient {
  private eventSource: EventSource | null = null;
  private handlers = new Map<string, Set<Function>>();

  connect(url: string) {
    this.eventSource = new EventSource(url);

    this.eventSource.onopen = () => {
      console.log('SSE connected');
    };

    this.eventSource.onerror = (error) => {
      console.error('SSE error:', error);
      // EventSource auto-reconnects
    };

    // Handle named events
    this.handlers.forEach((handlers, eventType) => {
      this.eventSource!.addEventListener(eventType, (event: MessageEvent) => {
        const data = JSON.parse(event.data);
        handlers.forEach(handler => handler(data));
      });
    });
  }

  on(eventType: string, handler: Function) {
    if (!this.handlers.has(eventType)) {
      this.handlers.set(eventType, new Set());

      // Add listener if already connected
      if (this.eventSource) {
        this.eventSource.addEventListener(eventType, (event: MessageEvent) => {
          const data = JSON.parse(event.data);
          this.handlers.get(eventType)?.forEach(h => h(data));
        });
      }
    }

    this.handlers.get(eventType)!.add(handler);

    return () => {
      this.handlers.get(eventType)?.delete(handler);
    };
  }

  close() {
    this.eventSource?.close();
    this.eventSource = null;
  }
}

// Usage
const sse = new EventSourceClient();
sse.on('update', (data) => console.log('Update:', data));
sse.on('notification', (data) => showNotification(data));
sse.connect('/events');
```

---

## Pub/Sub with Redis

```typescript
import Redis from 'ioredis';

const publisher = new Redis(process.env.REDIS_URL);
const subscriber = new Redis(process.env.REDIS_URL);

// Publish event
async function publishEvent(channel: string, event: any) {
  await publisher.publish(channel, JSON.stringify(event));
}

// Subscribe to channel
function subscribe(channel: string, handler: (event: any) => void) {
  subscriber.subscribe(channel);

  subscriber.on('message', (ch, message) => {
    if (ch === channel) {
      handler(JSON.parse(message));
    }
  });
}

// Pattern subscription
function subscribePattern(pattern: string, handler: (channel: string, event: any) => void) {
  subscriber.psubscribe(pattern);

  subscriber.on('pmessage', (pat, channel, message) => {
    if (pat === pattern) {
      handler(channel, JSON.parse(message));
    }
  });
}

// Usage
subscribe('notifications', (event) => {
  console.log('Notification:', event);
});

subscribePattern('room:*', (channel, event) => {
  const roomId = channel.split(':')[1];
  console.log(`Room ${roomId}:`, event);
});

publishEvent('notifications', { type: 'alert', message: 'New message' });
publishEvent('room:123', { type: 'message', content: 'Hello!' });
```

---

## Related Skills

- [[backend]] - Server implementation
- [[system-design]] - Event-driven architecture
- [[cloud-platforms]] - Managed pub/sub services

