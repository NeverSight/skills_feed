---
name: nchan-expert
description: Expert guidance for Nchan, a scalable pub/sub server for Nginx. Use this skill when you need to configure Nchan endpoints (publisher/subscriber), set up horizontal scaling with Redis, implement security patterns (authorization, X-Accel-Redirect), or troubleshoot Nchan performance and metrics.
---

# Nchan Expert

## Overview
This skill provides procedural knowledge for configuring, optimizing, and securing Nchan, the high-performance pub/sub module for Nginx. It is based on the core [Nchan documentation](https://nchan.io).

## Core Capabilities

### 1. Endpoint Configuration
Map Nginx locations to pub/sub endpoints.
- **Publishers:** Use `nchan_publisher` to create endpoints that accept messages via HTTP POST or Websockets.
- **Subscribers:** Use `nchan_subscriber` to support Websocket, EventSource (SSE), Long-Polling, and more.
- **PubSub:** Use `nchan_pubsub` for locations that act as both.

### 2. Scalability & Storage
Configure local memory storage and Redis for horizontal scaling.
- **Redis Modes:** Implement Distributed (shared), Backup (persistence), or Nostore (broadcast) modes.
- **Redis Cluster:** Set up high availability and sharding.
- See [references/storage.md](references/storage.md) for implementation details.

### 3. Security & Access Control
Secure channels using standardized patterns:
- **Authorization:** Use `nchan_authorize_request` to delegate auth to an upstream application.
- **Internal Redirects:** Implement `X-Accel-Redirect` to hide internal channel IDs.
- **ACLs:** Apply standard Nginx `allow`/`deny` directives for publisher endpoints.
- See [references/security.md](references/security.md) for patterns.

### 4. Advanced Messaging Features
- **Multiplexing:** Subscribe to up to 255 channels over a single connection.
- **Channel Groups:** Use `nchan_channel_group` for accounting and namespace isolation.
- **Upstream Hooks:** Use `nchan_publisher_upstream_request` to mutate messages before publication.

### 5. Monitoring & Introspection
- **Stub Status:** Monitor real-time metrics via `nchan_stub_status`.
- **Channel Events:** Track channel lifecycle events for debugging.
- **Variables:** Utilize Nchan-specific variables like `$nchan_channel_id` and `$nchan_subscriber_count`.
- See [references/variables.md](references/variables.md) for the full reference.

### 6. Testing & Validation
- **Verify Handshakes:** Use `curl` with `--http1.1` and a valid 16-byte `Sec-WebSocket-Key`.
- **Troubleshoot:** Resolve issues with HTTP/2 negotiation and strict proxy key enforcement (e.g., Cloudflare/Render).
- See [references/testing.md](references/testing.md) for commands and troubleshooting steps.

### 7. Containerization
- **Compile Module:** Use multi-stage builds to compile Nchan for Nginx Alpine.
- **Harden Security:** Run as a non-root user and implement container healthchecks.
- See [references/docker.md](references/docker.md) for the Dockerfile pattern and configuration.

## Resources

- **[references/directives.md](references/directives.md)**: Comprehensive list of configuration directives.
- **[references/variables.md](references/variables.md)**: Nchan-specific Nginx variables.
- **[references/security.md](references/security.md)**: Security and authorization patterns.
- **[references/storage.md](references/storage.md)**: Memory and Redis storage configuration.
- **[references/testing.md](references/testing.md)**: Minimal testing patterns with curl (stats, pub/sub, wss) and handshake troubleshooting.
- **[references/docker.md](references/docker.md)**: Docker containerization and multi-stage build patterns.