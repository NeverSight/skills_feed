---
name: websocket-engineer
description: Expert in real-time communication systems, including WebSockets, Socket.IO, SSE, and WebRTC.
---

# WebSocket & Real-Time Engineer

## Purpose

Provides real-time communication expertise specializing in WebSocket architecture, Socket.IO, and event-driven systems. Builds low-latency, bidirectional communication systems scaling to millions of concurrent connections.

## When to Use

- Building chat apps, live dashboards, or multiplayer games
- Scaling WebSocket servers horizontally (Redis Adapter)
- Implementing "Server-Sent Events" (SSE) for one-way updates
- Troubleshooting connection drops, heartbeat failures, or CORS issues
- Designing stateful connection architectures
- Migrating from polling to push technology

## Examples

### Example 1: Real-Time Chat Application

**Scenario:** Building a scalable chat platform for enterprise use.

**Implementation:**
1. Designed WebSocket architecture with Socket.IO
2. Implemented Redis Adapter for horizontal scaling
3. Created room-based message routing
4. Added message persistence and history
5. Implemented presence system (online/offline)

**Results:**
- Supports 100,000+ concurrent connections
- 50ms average message delivery
- 99.99% connection stability
- Seamless horizontal scaling

### Example 2: Live Dashboard System

**Scenario:** Real-time analytics dashboard with sub-second updates.

**Implementation:**
1. Implemented WebSocket server with low latency
2. Created efficient message batching strategy
3. Added Redis pub/sub for multi-server support
4. Implemented client-side update coalescing
5. Added compression for large payloads

**Results:**
- Dashboard updates in under 100ms
- Handles 10,000 concurrent dashboard views
- 80% reduction in server load vs polling
- Zero data loss during reconnections

### Example 3: Multiplayer Game Backend

**Scenario:** Low-latency multiplayer game server.

**Implementation:**
1. Implemented WebSocket server with binary protocols
2. Created authoritative server architecture
3. Added client-side prediction and reconciliation
4. Implemented lag compensation algorithms
5. Set up server-side physics and collision detection

**Results:**
- 30ms end-to-end latency
- Supports 1000 concurrent players per server
- Smooth gameplay despite network variations
- Cheat-resistant server authority

## Best Practices

### Connection Management

- **Heartbeats**: Implement ping/pong for connection health
- **Reconnection**: Automatic reconnection with backoff
- **State Cleanup**: Proper cleanup on disconnect
- **Connection Limits**: Prevent resource exhaustion

### Scaling

- **Horizontal Scaling**: Use Redis Adapter for multi-server
- **Sticky Sessions**: Proper load balancer configuration
- **Message Routing**: Efficient routing for broadcast/unicast
- **Rate Limiting**: Prevent abuse and overload

### Performance

- **Message Batching**: Batch messages where appropriate
- **Compression**: Compress messages (permessage-deflate)
- **Binary Protocols**: Use binary for performance-critical data
- **Connection Pooling**: Efficient client connection reuse

### Security

- **Authentication**: Validate on handshake
- **TLS**: Always use WSS
- **Input Validation**: Validate all incoming messages
- **Rate Limiting**: Limit connection/message rates

---
---

## 2. Decision Framework

### Protocol Selection

```
What is the communication pattern?
│
├─ **Bi-directional (Chat/Game)**
│  ├─ Low Latency needed? → **WebSockets (Raw)**
│  ├─ Fallbacks/Auto-reconnect needed? → **Socket.IO**
│  └─ P2P Video/Audio? → **WebRTC**
│
├─ **One-way (Server → Client)**
│  ├─ Stock Ticker / Notifications? → **Server-Sent Events (SSE)**
│  └─ Large File Download? → **HTTP Stream**
│
└─ **High Frequency (IoT)**
   └─ Constrained device? → **MQTT** (over TCP/WS)
```

### Scaling Strategy

| Scale | Architecture | Backend |
|-------|--------------|---------|
| **< 10k Users** | Monolith Node.js | Single Instance |
| **10k - 100k** | Clustering | Node.js Cluster + Redis Adapter |
| **100k - 1M** | Microservices | Go/Elixir/Rust + NATS/Kafka |
| **Global** | Edge | Cloudflare Workers / PubNub / Pusher |

### Load Balancer Config

*   **Sticky Sessions:** **REQUIRED** for Socket.IO (handshake phase).
*   **Timeouts:** Increase idle timeouts (e.g., 60s+).
*   **Headers:** `Upgrade: websocket`, `Connection: Upgrade`.

**Red Flags → Escalate to `security-engineer`:**
- Accepting connections from any Origin (`*`) with credentials
- No Rate Limiting on connection requests (DoS risk)
- Sending JWTs in URL query params (Logged in proxy logs) - Use Cookie or Initial Message instead

---
---

## 3. Core Workflows

### Workflow 1: Scalable Socket.IO Server (Node.js)

**Goal:** Chat server capable of scaling across multiple cores/instances.

**Steps:**

1.  **Install Dependencies**
    ```bash
    npm install socket.io redis @socket.io/redis-adapter
    ```

2.  **Implementation (`server.js`)**
    ```javascript
    const { Server } = require("socket.io");
    const { createClient } = require("redis");
    const { createAdapter } = require("@socket.io/redis-adapter");

    const pubClient = createClient({ url: "redis://localhost:6379" });
    const subClient = pubClient.duplicate();

    Promise.all([pubClient.connect(), subClient.connect()]).then(() => {
      const io = new Server(3000, {
        adapter: createAdapter(pubClient, subClient),
        cors: {
          origin: "https://myapp.com",
          methods: ["GET", "POST"]
        }
      });

      io.on("connection", (socket) => {
        // User joins a room (e.g., "chat-123")
        socket.on("join", (room) => {
          socket.join(room);
        });

        // Send message to room (propagates via Redis to all nodes)
        socket.on("message", (data) => {
          io.to(data.room).emit("chat", data.text);
        });
      });
    });
    ```

---
---

### Workflow 3: Production Tuning (Linux)

**Goal:** Handle 50k concurrent connections on a single server.

**Steps:**

1.  **File Descriptors**
    -   Increase limit: `ulimit -n 65535`.
    -   Edit `/etc/security/limits.conf`.

2.  **Ephemeral Ports**
    -   Increase range: `sysctl -w net.ipv4.ip_local_port_range="1024 65535"`.

3.  **Memory Optimization**
    -   Use `ws` (lighter) instead of Socket.IO if features not needed.
    -   Disable "Per-Message Deflate" (Compression) if CPU is high.

---
---

## 5. Anti-Patterns & Gotchas

### ❌ Anti-Pattern 1: Stateful Monolith

**What it looks like:**
-   Storing `users = []` array in Node.js memory.

**Why it fails:**
-   When you scale to 2 servers, User A on Server 1 cannot talk to User B on Server 2.
-   Memory leaks crash the process.

**Correct approach:**
-   Use **Redis** as the state store (Adapter).
-   Stateless servers, Stateful backend (Redis).

### ❌ Anti-Pattern 2: The "Thundering Herd"

**What it looks like:**
-   Server restarts. 100,000 clients reconnect instantly.
-   Server crashes again due to CPU spike.

**Why it fails:**
-   Connection handshakes are expensive (TLS + Auth).

**Correct approach:**
-   **Randomized Jitter:** Clients wait `random(0, 10s)` before reconnecting.
-   **Exponential Backoff:** Wait 1s, then 2s, then 4s...

### ❌ Anti-Pattern 3: Blocking the Event Loop

**What it looks like:**
-   `socket.on('message', () => { heavyCalculation(); })`

**Why it fails:**
-   Node.js is single-threaded. One heavy task blocks *all* 10,000 connections.

**Correct approach:**
-   Offload work to a **Worker Thread** or **Message Queue** (RabbitMQ/Bull).

---
---

## 7. Quality Checklist

**Scalability:**
-   [ ] **Adapter:** Redis/NATS adapter configured for multi-node.
-   [ ] **Load Balancer:** Sticky sessions enabled (if using polling fallback).
-   [ ] **OS Limits:** File descriptors limit increased.

**Resilience:**
-   [ ] **Reconnection:** Exponential backoff + Jitter implemented.
-   [ ] **Heartbeat:** Ping/Pong interval configured (< LB timeout).
-   [ ] **Fallback:** Socket.IO fallbacks (HTTP Long Polling) enabled/tested.

**Security:**
-   [ ] **WSS:** TLS enabled (Secure WebSockets).
-   [ ] **Auth:** Handshake validates credentials properly.
-   [ ] **Rate Limit:** Connection rate limiting active.

## Anti-Patterns

### Connection Management Anti-Patterns

- **No Heartbeats**: Not detecting dead connections - implement ping/pong
- **Memory Leaks**: Not cleaning up closed connections - implement proper cleanup
- **Infinite Reconnects**: Reloop without backoff - implement exponential backoff
- **Sticky Sessions Required**: Not designing for stateless - use Redis for state

### Scaling Anti-Patterns

- **Single Server**: Not scaling beyond one instance - use Redis adapter
- **No Load Balancing**: Direct connections to servers - use proper load balancer
- **Broadcast Storm**: Sending to all connections blindly - target specific connections
- **Connection Saturation**: Too many connections per server - scale horizontally

### Performance Anti-Patterns

- **Message Bloat**: Large unstructured messages - use efficient message formats
- **No Throttling**: Unlimited send rates - implement rate limiting
- **Blocking Operations**: Synchronous processing - use async processing
- **No Monitoring**: Operating blind - implement connection metrics

### Security Anti-Patterns

- **No TLS**: Using unencrypted connections - always use WSS
- **Weak Auth**: Simple token validation - implement proper authentication
- **No Rate Limits**: Vulnerable to abuse - implement connection/message limits
- **CORS Exposed**: Open cross-origin access - configure proper CORS
