---
name: realtime-sync-pro
id: realtime-sync-pro
version: 1.1.0
description: "Master of Low-Latency Synchronization, specialized in WebTransport, Ably LiveSync, and Real-time AI Stream Orchestration."
last_updated: "2026-01-22"
---

# Skill: Realtime Sync Pro (Standard 2026)

**Role:** The Realtime Sync Pro is a specialized architect responsible for high-concurrency, sub-50ms latency synchronization between distributed clients and servers. In 2026, this role masters WebTransport (HTTP/3), Ably's transactional patterns, and the "Live-Feed" orchestration required for real-time AI agents and collaborative UIs.

## 🎯 Primary Objectives
1.  **Extreme Low Latency:** Achieving sub-50ms global synchronization using WebTransport and optimized Pub/Sub edge networks.
2.  **Transactional Integrity:** Implementing the "Transactional Outbox" pattern to ensure database and real-time state never drift.
3.  **Conflict Resolution:** Mastering CRDTs (Conflict-free Replicated Data Types) and Sequence IDs for multi-user collaboration.
4.  **AI Stream Management:** Orchestrating live LLM token streams and multimodal AI feedback in real-time UI.

---

## 🏗️ The 2026 Realtime Stack

### 1. Protocols & Transport
- **WebTransport (HTTP/3):** The modern, bidirectional, multiplexed replacement for WebSockets.
- **Ably LiveSync:** For guaranteed message delivery and sequence tracking.
- **gRPC-Web:** For typed, high-performance service communication.

### 2. State & Sync Engines
- **CRDTs (Yjs / Automerge):** For collaborative editing (Figma-style).
- **Transactional Outbox:** Ensuring DB updates and Sync messages are atomic.
- **Presence APIs:** Tracking user state and intent in real-time.

---

## 🛠️ Implementation Patterns

### 1. WebTransport Bidirectional Stream (2026 Standard)
Replacing legacy WebSockets with multiplexed, unreliable-datagram support for game-like responsiveness.

```typescript
// 2026 Pattern: WebTransport Client
const transport = new WebTransport(serverUrl);
await transport.ready;

const stream = await transport.createBidirectionalStream();
const writer = stream.writable.getWriter();
const reader = stream.readable.getReader();

// Send high-frequency state updates via Datagrams (unreliable/fast)
const datagramWriter = transport.datagrams.writable.getWriter();
datagramWriter.write(new TextEncoder().encode(JSON.stringify(uiState)));
```

### 2. Transactional Outbox Pattern (Database-to-Sync)
Ensuring that a message is ONLY sent to the real-time channel if the database transaction succeeds.

```sql
-- Pattern: Outbox Table in PostgreSQL 18
BEGIN;
  UPDATE users SET status = 'online' WHERE id = 123;
  INSERT INTO realtime_outbox (channel, payload, sequence_id) 
  VALUES ('user_status', '{"status": "online"}', uuid_generate_v7());
COMMIT;
-- A background worker (CDC) picks up the outbox and pushes to Ably/WebTransport
```

### 3. AI Stream Orchestration
Handling token-by-token updates without UI jitter.

```tsx
// Frontend: React 19 + Realtime Stream
function LiveAIResponse({ channelId }) {
  const [tokens, setTokens] = useState("");
  
  useEffect(() => {
    const channel = ably.channels.get(channelId);
    channel.subscribe('token', (msg) => {
      // Use requestAnimationFrame to batch token rendering
      requestAnimationFrame(() => setTokens(prev => prev + msg.data));
    });
  }, [channelId]);
}
```

---

## 🚫 The "Do Not List" (Anti-Patterns)
1.  **NEVER** use real-time messages as the primary "Source of Truth" for state. State lives in the DB; realtime is the "Notification" of change.
2.  **NEVER** use JSON.stringify on high-frequency streams (100Hz+). Use **Protocol Buffers** or **MessagePack**.
3.  **NEVER** ignore "Sequence Drift." If a client misses message N, it must "Rewind" using Sequence IDs.
4.  **NEVER** implement "Global Locks" in real-time. Use **Optimistic UI** and **CRDTs**.

---

## 🛠️ Troubleshooting & Latency Audit

| Issue | Likely Cause | 2026 Corrective Action |
| :--- | :--- | :--- |
| **High Latency (Spikes)** | Head-of-line blocking (TCP) | Switch to WebTransport (UDP-based). |
| **Out-of-Order Data** | Race conditions in async emits | Implement Sequence IDs and a "Re-order Buffer" on the client. |
| **Zombies (Presence)** | Failed heartbeat cleanup | Use "Epidemic Broadcast" protocols for robust presence. |
| **UI Jitter** | Excessive re-renders on sync | Implement a "Buffer-and-Batch" strategy using `useTransition`. |

---

## 📚 Reference Library
- **[WebTransport Deep Dive](./references/1-webtransport-mastery.md):** The future of bidirectional I/O.
- **[Ably LiveSync Patterns](./references/2-ably-livesync-patterns.md):** Guaranteed delivery at scale.
- **[CRDTs & Collaboration](./references/3-crdt-collaboration.md):** Mastering multi-user state.

---

## 📊 Quality Metrics
- **Median Latency:** < 50ms (Global Edge).
- **Message Delivery Guarantee:** 99.999% (via Sequence IDs).
- **Connection Recovery Time:** < 500ms after network swap.

---

## 🔄 Evolution from WebSockets to 2026
- **2011-2022:** WebSockets (Single TCP stream, head-of-line blocking).
- **2023-2024:** Server-Sent Events (SSE) for AI (One-way only).
- **2025-2026:** WebTransport (Multiplexed, UDP-based, unreliable datagrams + reliable streams).

---

**End of Realtime Sync Pro Standard (v1.1.0)**
