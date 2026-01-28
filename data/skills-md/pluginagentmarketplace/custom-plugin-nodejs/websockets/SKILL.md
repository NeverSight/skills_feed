---
name: websockets
description: Implement real-time bidirectional communication with Socket.io and ws library for chat, notifications, and live dashboards
version: "2.1.0"
sasmp_version: "1.3.0"
bonded_agent: 08-nodejs-microservices
bond_type: PRIMARY_BOND
---

# Node.js WebSockets Skill

Master real-time bidirectional communication for building chat apps, live notifications, collaborative tools, and real-time dashboards.

## Quick Start

WebSocket server in 3 steps:
1. **Setup Server** - Socket.io or ws library
2. **Handle Connections** - Manage client lifecycle
3. **Emit Events** - Send/receive messages

## Core Concepts

### Socket.io Server Setup
```javascript
const express = require('express');
const { createServer } = require('http');
const { Server } = require('socket.io');

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: {
    origin: 'http://localhost:3000',
    methods: ['GET', 'POST']
  }
});

io.on('connection', (socket) => {
  console.log('User connected:', socket.id);

  // Handle events
  socket.on('chat:message', (data) => {
    // Broadcast to all clients
    io.emit('chat:message', {
      ...data,
      timestamp: Date.now()
    });
  });

  // Join rooms
  socket.on('room:join', (roomId) => {
    socket.join(roomId);
    socket.to(roomId).emit('room:user-joined', socket.id);
  });

  // Handle disconnect
  socket.on('disconnect', () => {
    console.log('User disconnected:', socket.id);
  });
});

httpServer.listen(3000);
```

### Socket.io Client
```javascript
import { io } from 'socket.io-client';

const socket = io('http://localhost:3000', {
  auth: { token: 'jwt-token-here' }
});

socket.on('connect', () => {
  console.log('Connected:', socket.id);
});

socket.on('chat:message', (message) => {
  console.log('Received:', message);
});

// Send message
socket.emit('chat:message', {
  text: 'Hello!',
  userId: 'user123'
});
```

## Learning Path

### Beginner (1-2 weeks)
- ✅ Socket.io server setup
- ✅ Basic event emission
- ✅ Connect/disconnect handling
- ✅ Simple chat application

### Intermediate (3-4 weeks)
- ✅ Rooms and namespaces
- ✅ Authentication middleware
- ✅ Broadcasting patterns
- ✅ Error handling

### Advanced (5-6 weeks)
- ✅ Horizontal scaling with Redis
- ✅ Binary data transfer
- ✅ Reconnection strategies
- ✅ Performance optimization

## Native ws Library
```javascript
const WebSocket = require('ws');
const { createServer } = require('http');

const server = createServer();
const wss = new WebSocket.Server({ server });

wss.on('connection', (ws, req) => {
  const ip = req.socket.remoteAddress;
  console.log('Client connected from', ip);

  // Handle messages
  ws.on('message', (data) => {
    const message = JSON.parse(data);
    console.log('Received:', message);

    // Echo back
    ws.send(JSON.stringify({
      type: 'echo',
      data: message
    }));
  });

  // Ping/pong heartbeat
  ws.isAlive = true;
  ws.on('pong', () => {
    ws.isAlive = true;
  });

  ws.on('close', () => {
    console.log('Client disconnected');
  });
});

// Heartbeat interval
const interval = setInterval(() => {
  wss.clients.forEach((ws) => {
    if (!ws.isAlive) return ws.terminate();
    ws.isAlive = false;
    ws.ping();
  });
}, 30000);

wss.on('close', () => clearInterval(interval));

server.listen(3000);
```

## Rooms and Namespaces
```javascript
// Namespaces for feature separation
const chatNamespace = io.of('/chat');
const notificationsNamespace = io.of('/notifications');

chatNamespace.on('connection', (socket) => {
  // Chat-specific logic
  socket.on('message', (msg) => {
    chatNamespace.emit('message', msg);
  });
});

notificationsNamespace.on('connection', (socket) => {
  // Notification-specific logic
  socket.on('subscribe', (topic) => {
    socket.join(topic);
  });
});

// Rooms within namespace
socket.on('join-channel', (channelId) => {
  socket.join(`channel:${channelId}`);

  // Send only to room
  io.to(`channel:${channelId}`).emit('user-joined', {
    userId: socket.userId,
    channelId
  });
});

// Leave room
socket.on('leave-channel', (channelId) => {
  socket.leave(`channel:${channelId}`);
});
```

## Authentication Middleware
```javascript
const jwt = require('jsonwebtoken');

// Socket.io middleware
io.use((socket, next) => {
  const token = socket.handshake.auth.token;

  if (!token) {
    return next(new Error('Authentication required'));
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    socket.userId = decoded.id;
    socket.userRole = decoded.role;
    next();
  } catch (err) {
    next(new Error('Invalid token'));
  }
});

// Namespace-level auth
const adminNamespace = io.of('/admin');
adminNamespace.use((socket, next) => {
  if (socket.userRole !== 'admin') {
    return next(new Error('Admin access required'));
  }
  next();
});
```

## Scaling with Redis Adapter
```javascript
const { createAdapter } = require('@socket.io/redis-adapter');
const { createClient } = require('redis');

const pubClient = createClient({ url: 'redis://localhost:6379' });
const subClient = pubClient.duplicate();

Promise.all([pubClient.connect(), subClient.connect()]).then(() => {
  io.adapter(createAdapter(pubClient, subClient));
  console.log('Redis adapter connected');
});

// Now events are broadcast across all server instances
io.emit('notification', { message: 'Hello from any server!' });
```

## Real-Time Patterns

### Chat Application
```javascript
// Server
io.on('connection', (socket) => {
  socket.on('chat:join', ({ room, username }) => {
    socket.join(room);
    socket.to(room).emit('chat:user-joined', { username });
  });

  socket.on('chat:message', ({ room, message }) => {
    io.to(room).emit('chat:message', {
      user: socket.userId,
      message,
      timestamp: Date.now()
    });
  });

  socket.on('chat:typing', ({ room }) => {
    socket.to(room).emit('chat:typing', { user: socket.userId });
  });
});
```

### Live Notifications
```javascript
// Server
function sendNotification(userId, notification) {
  io.to(`user:${userId}`).emit('notification', notification);
}

// Join user's personal room
socket.on('authenticate', () => {
  socket.join(`user:${socket.userId}`);
});

// From any service
notificationService.on('new', (userId, data) => {
  sendNotification(userId, data);
});
```

### Live Dashboard
```javascript
// Server: broadcast metrics periodically
setInterval(async () => {
  const metrics = await getSystemMetrics();
  io.emit('metrics:update', metrics);
}, 1000);

// Or on-demand updates
database.onChange((change) => {
  io.to(`dashboard:${change.collection}`).emit('data:update', change);
});
```

## Error Handling
```javascript
// Client-side reconnection
const socket = io({
  reconnection: true,
  reconnectionAttempts: 5,
  reconnectionDelay: 1000,
  reconnectionDelayMax: 5000
});

socket.on('connect_error', (err) => {
  console.log('Connection error:', err.message);
});

socket.on('reconnect', (attemptNumber) => {
  console.log('Reconnected after', attemptNumber, 'attempts');
});

socket.on('reconnect_failed', () => {
  console.log('Failed to reconnect');
  // Fallback to polling or show offline UI
});

// Server-side error handling
socket.on('error', (error) => {
  console.error('Socket error:', error);
});
```

## Unit Test Template
```javascript
const { createServer } = require('http');
const { Server } = require('socket.io');
const Client = require('socket.io-client');

describe('WebSocket Server', () => {
  let io, serverSocket, clientSocket;

  beforeAll((done) => {
    const httpServer = createServer();
    io = new Server(httpServer);
    httpServer.listen(() => {
      const port = httpServer.address().port;
      clientSocket = Client(`http://localhost:${port}`);
      io.on('connection', (socket) => {
        serverSocket = socket;
      });
      clientSocket.on('connect', done);
    });
  });

  afterAll(() => {
    io.close();
    clientSocket.close();
  });

  it('should receive message from client', (done) => {
    serverSocket.on('hello', (arg) => {
      expect(arg).toBe('world');
      done();
    });
    clientSocket.emit('hello', 'world');
  });

  it('should broadcast to clients', (done) => {
    clientSocket.on('broadcast', (arg) => {
      expect(arg).toBe('everyone');
      done();
    });
    io.emit('broadcast', 'everyone');
  });
});
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Connection drops | No heartbeat | Enable pingInterval/pingTimeout |
| Messages not received | Wrong room | Verify room membership |
| Scaling issues | No Redis | Add Redis adapter |
| Memory leak | Listeners not removed | Clean up on disconnect |

## When to Use

Use WebSockets when:
- Real-time bidirectional communication
- Low-latency updates needed
- Live notifications/chat
- Collaborative applications
- Gaming/trading platforms

## Related Skills

- Express REST API (HTTP fallback)
- Microservices (distributed events)
- Redis (pub/sub scaling)

## Resources

- [Socket.io Documentation](https://socket.io/docs/)
- [ws Library](https://github.com/websockets/ws)
- [Redis Adapter](https://socket.io/docs/v4/redis-adapter/)
