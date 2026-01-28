---
name: websocket
description: Real-time bidirectional communication with security focus on CSWSH prevention, authentication, and message validation
model: sonnet
risk_level: HIGH
---

# WebSocket Security Skill

## File Organization

- **SKILL.md**: Core principles, patterns, essential security (this file)
- **references/security-examples.md**: CSWSH examples and authentication patterns
- **references/advanced-patterns.md**: Connection management, scaling patterns
- **references/threat-model.md**: Attack scenarios including CSWSH

## Validation Gates

**Gate 0.2**: PASSED (5+ vulnerabilities documented) - CVE-2024-23898, CVE-2024-26135, CVE-2023-0957

---

## 1. Overview

**Risk Level**: HIGH

**Justification**: WebSocket connections bypass Same-Origin Policy protections, making them vulnerable to Cross-Site WebSocket Hijacking (CSWSH). Persistent connections require careful authentication, session management, and input validation.

You are an expert in WebSocket security, understanding the unique vulnerabilities of persistent bidirectional connections.

### Core Expertise Areas
- CSWSH (Cross-Site WebSocket Hijacking) prevention
- Origin header validation and token-based authentication
- Message validation and per-message authorization
- Rate limiting and connection lifecycle security

---

## 2. Core Responsibilities

### Fundamental Principles

1. **TDD First**: Write tests before implementation - test security boundaries, connection lifecycle
2. **Performance Aware**: Optimize for low latency (<50ms), connection pooling, backpressure
3. **Validate Origin**: Always check Origin header against explicit allowlist
4. **Authenticate First**: Verify identity before accepting messages
5. **Authorize Each Action**: Don't assume connection equals unlimited access
6. **Validate All Messages**: Treat WebSocket messages as untrusted input
7. **Limit Resources**: Rate limit messages, timeout idle connections

### Security Decision Framework

| Situation | Approach |
|-----------|----------|
| New connection | Validate Origin, require authentication token |
| Each message | Validate format, check authorization for action |
| Sensitive operations | Re-verify session, log action |
| Idle connection | Timeout after inactivity period |
| Error condition | Close connection, log details |

---

## 3. Technical Foundation

### Version Recommendations

| Component | Version | Notes |
|-----------|---------|-------|
| **FastAPI/Starlette** | 0.115+ | WebSocket support |
| **websockets** | 12.0+ | Python WebSocket library |

### Security Configuration

```python
WEBSOCKET_CONFIG = {
    "max_message_size": 1024 * 1024,  # 1MB
    "max_connections_per_ip": 10,
    "idle_timeout_seconds": 300,
    "messages_per_minute": 60,
}

# NEVER use "*" for origins
ALLOWED_ORIGINS = ["https://app.example.com", "https://admin.example.com"]
```

---

## 4. Implementation Workflow (TDD)

### Step 1: Write Failing Test First

```python
import pytest
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient

# Test security boundaries first
@pytest.mark.asyncio
async def test_origin_validation_rejects_invalid():
    """CSWSH prevention - must reject invalid origins."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        # This should fail until origin validation is implemented
        with pytest.raises(Exception):
            async with client.websocket_connect(
                "/ws?token=valid",
                headers={"Origin": "https://evil.com"}
            ):
                pass

@pytest.mark.asyncio
async def test_authentication_required():
    """Must reject connections without valid token."""
    with TestClient(app) as client:
        with pytest.raises(Exception):
            with client.websocket_connect("/ws") as ws:
                pass

@pytest.mark.asyncio
async def test_message_authorization():
    """Each message action must be authorized."""
    with TestClient(app) as client:
        with client.websocket_connect(
            "/ws?token=readonly_user",
            headers={"Origin": "https://app.example.com"}
        ) as ws:
            ws.send_json({"action": "delete", "id": "123"})
            response = ws.receive_json()
            assert response.get("error") == "Permission denied"
```

### Step 2: Implement Minimum to Pass

```python
# Implement only what's needed to pass the test
async def validate_origin(websocket: WebSocket) -> bool:
    origin = websocket.headers.get("origin")
    if not origin or origin not in ALLOWED_ORIGINS:
        await websocket.close(code=4003, reason="Invalid origin")
        return False
    return True
```

### Step 3: Refactor and Verify

```bash
# Run all WebSocket tests
pytest tests/websocket/ -v --asyncio-mode=auto

# Check for security issues
bandit -r src/websocket/

# Verify no regressions
pytest tests/ -v
```

---

## 5. Performance Patterns

### Pattern 1: Connection Pooling

```python
# BAD - Create new connection for each request
ws = await create_connection(user_id)  # Expensive!

# GOOD - Reuse connections from pool
class ConnectionPool:
    def __init__(self, max_size: int = 100):
        self.connections: dict[str, WebSocket] = {}

    async def get_or_create(self, user_id: str) -> WebSocket:
        if user_id not in self.connections:
            self.connections[user_id] = await create_connection(user_id)
        return self.connections[user_id]
```

### Pattern 2: Message Batching

```python
# BAD - Send messages one at a time
for item in items:
    await websocket.send_json({"type": "item", "data": item})

# GOOD - Batch messages to reduce overhead
await websocket.send_json({"type": "batch", "data": items[:50]})
```

### Pattern 3: Binary Protocols

```python
# BAD - JSON for high-frequency data (~80 bytes)
await websocket.send_json({"x": 123.456, "y": 789.012, "z": 456.789})

# GOOD - Binary format (20 bytes)
import struct
await websocket.send_bytes(struct.pack('!3f', 123.456, 789.012, 456.789))
```

### Pattern 4: Heartbeat Optimization

```python
# BAD - Fixed frequent heartbeats
HEARTBEAT_INTERVAL = 5  # Every 5 seconds

# GOOD - Adaptive heartbeats based on activity
interval = 60 if (time() - last_activity) < 60 else 30
```

### Pattern 5: Backpressure Handling

```python
# BAD - Blocks on slow clients
await ws.send_json(message)

# GOOD - Timeout and bounded queue
from collections import deque
queue = deque(maxlen=100)  # Drop oldest when full
try:
    await asyncio.wait_for(ws.send_json(message), timeout=1.0)
except asyncio.TimeoutError:
    pass  # Client too slow
```

---

## 6. Implementation Patterns

### Pattern 1: Origin Validation (Critical for CSWSH Prevention)

```python
from fastapi import WebSocket

async def validate_origin(websocket: WebSocket) -> bool:
    """Validate WebSocket origin against allowlist."""
    origin = websocket.headers.get("origin")
    if not origin or origin not in ALLOWED_ORIGINS:
        await websocket.close(code=4003, reason="Invalid origin")
        return False
    return True

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    if not await validate_origin(websocket):
        return
    await websocket.accept()
```

### Pattern 2: Token-Based Authentication

```python
from jose import jwt, JWTError

async def authenticate_websocket(websocket: WebSocket) -> User | None:
    """Authenticate via token (not cookies - vulnerable to CSWSH)."""
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=4001, reason="Authentication required")
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user = await user_service.get(payload.get("sub"))
        if not user:
            await websocket.close(code=4001, reason="User not found")
            return None
        return user
    except JWTError:
        await websocket.close(code=4001, reason="Invalid token")
        return None
```

### Pattern 3: Per-Message Authorization

```python
from pydantic import BaseModel, field_validator

class WebSocketMessage(BaseModel):
    action: str
    data: dict

    @field_validator('action')
    @classmethod
    def validate_action(cls, v):
        if v not in {'subscribe', 'unsubscribe', 'send', 'query'}:
            raise ValueError(f'Invalid action: {v}')
        return v

async def handle_message(websocket: WebSocket, user: User, raw_data: dict):
    try:
        message = WebSocketMessage(**raw_data)
    except ValueError:
        await websocket.send_json({"error": "Invalid message format"})
        return

    if not user.has_permission(f"ws:{message.action}"):
        await websocket.send_json({"error": "Permission denied"})
        return

    result = await handlers[message.action](user, message.data)
    await websocket.send_json(result)
```

### Pattern 4: Connection Manager with Rate Limiting

```python
from collections import defaultdict
from time import time

class SecureConnectionManager:
    def __init__(self):
        self.connections: dict[str, WebSocket] = {}
        self.message_counts: dict[str, list[float]] = defaultdict(list)
        self.connections_per_ip: dict[str, int] = defaultdict(int)

    async def connect(self, websocket: WebSocket, user_id: str, ip: str) -> bool:
        if self.connections_per_ip[ip] >= WEBSOCKET_CONFIG["max_connections_per_ip"]:
            await websocket.close(code=4029, reason="Too many connections")
            return False
        await websocket.accept()
        self.connections[user_id] = websocket
        self.connections_per_ip[ip] += 1
        return True

    def check_rate_limit(self, user_id: str) -> bool:
        now = time()
        self.message_counts[user_id] = [
            ts for ts in self.message_counts[user_id] if ts > now - 60
        ]
        if len(self.message_counts[user_id]) >= WEBSOCKET_CONFIG["messages_per_minute"]:
            return False
        self.message_counts[user_id].append(now)
        return True
```

### Pattern 5: Complete Secure Handler

```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    if not await validate_origin(websocket):
        return
    user = await authenticate_websocket(websocket)
    if not user:
        return

    ip = websocket.client.host
    if not await manager.connect(websocket, user.id, ip):
        return

    try:
        while True:
            raw = await asyncio.wait_for(
                websocket.receive_json(),
                timeout=WEBSOCKET_CONFIG["idle_timeout_seconds"]
            )
            if not manager.check_rate_limit(user.id):
                await websocket.send_json({"error": "Rate limited"})
                continue
            await handle_message(websocket, user, raw)
    except (WebSocketDisconnect, asyncio.TimeoutError):
        pass
    finally:
        manager.disconnect(user.id, ip)
```

---

## 7. Security Standards

### Domain Vulnerability Landscape

| CVE ID | Severity | Description | Mitigation |
|--------|----------|-------------|------------|
| CVE-2024-23898 | HIGH | Jenkins CSWSH - command execution | Validate Origin |
| CVE-2024-26135 | HIGH | MeshCentral CSWSH - config leak | Origin + SameSite |
| CVE-2023-0957 | CRITICAL | Gitpod CSWSH - account takeover | Origin + token auth |

### OWASP Top 10 Mapping

| Category | Mitigations |
|----------|-------------|
| A01 Access Control | Origin validation, per-message authz |
| A02 Crypto Failures | TLS/WSS only, signed tokens |
| A03 Injection | Validate all message content |
| A07 Auth Failures | Token auth, session validation |

### CSWSH Prevention Summary

```python
async def secure_websocket_handler(websocket: WebSocket):
    # 1. VALIDATE ORIGIN (Critical)
    if websocket.headers.get("origin") not in ALLOWED_ORIGINS:
        await websocket.close(code=4003)
        return
    # 2. AUTHENTICATE with token (not cookies)
    user = await validate_token(websocket.query_params.get("token"))
    if not user:
        await websocket.close(code=4001)
        return
    # 3. Accept only after validation
    await websocket.accept()
    # 4. AUTHORIZE each message, 5. RATE LIMIT, 6. TIMEOUT idle
```

---

## 8. Common Mistakes & Anti-Patterns

### No Origin Validation

```python
# NEVER - vulnerable to CSWSH
@app.websocket("/ws")
async def vulnerable(websocket: WebSocket):
    await websocket.accept()  # Accepts any origin!

# ALWAYS - validate origin first
if websocket.headers.get("origin") not in ALLOWED_ORIGINS:
    await websocket.close(code=4003)
    return
```

### Cookie-Only Authentication

```python
# NEVER - cookies sent automatically in CSWSH attacks
session = websocket.cookies.get("session")

# ALWAYS - require explicit token parameter
token = websocket.query_params.get("token")
```

### No Per-Message Authorization

```python
# NEVER - assumes connection = full access
if data["action"] == "delete":
    await delete_resource(data["id"])

# ALWAYS - check permission for each action
if not user.has_permission("delete"):
    return {"error": "Permission denied"}
```

### No Input Validation

```python
# NEVER - trust WebSocket messages
await db.execute(f"SELECT * FROM {data['table']}")  # SQL injection!

# ALWAYS - validate with Pydantic
message = WebSocketMessage(**data)
```

---

## 9. Pre-Implementation Checklist

### Phase 1: Before Writing Code

- [ ] Write failing tests for security boundaries (CSWSH, auth, authz)
- [ ] Write failing tests for connection lifecycle (connect, disconnect, timeout)
- [ ] Write failing tests for message validation and rate limiting
- [ ] Review threat model in `references/threat-model.md`
- [ ] Identify performance requirements (latency, throughput, connections)

### Phase 2: During Implementation

- [ ] Origin validation against explicit allowlist
- [ ] Token-based authentication (not cookie-only)
- [ ] Per-message authorization checks
- [ ] Rate limiting and idle timeout implemented
- [ ] All messages validated with Pydantic
- [ ] Connection pooling for efficiency
- [ ] Backpressure handling for slow clients

### Phase 3: Before Committing

- [ ] All security tests pass: `pytest tests/websocket/ -v`
- [ ] No security issues: `bandit -r src/websocket/`
- [ ] WSS (TLS) enforced in production config
- [ ] CSWSH test coverage verified
- [ ] Performance benchmarks meet targets (<50ms latency)
- [ ] No regressions: `pytest tests/ -v`

---

## 10. Summary

**Security Goals**:
- **CSWSH-Resistant**: Origin validation, token auth
- **Properly Authorized**: Per-message permission checks
- **Rate Limited**: Prevent message flooding
- **Validated**: All messages treated as untrusted

**Critical Reminders**: ALWAYS validate Origin, use token auth (not cookies), authorize EACH message, use WSS in production.
