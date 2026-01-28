---
name: async-programming
description: Concurrent operations with asyncio and Tokio, focusing on race condition prevention, resource safety, and performance
model: sonnet
risk_level: MEDIUM
---

# Async Programming Skill

## File Organization

- **SKILL.md**: Core principles, patterns, essential security (this file)
- **references/security-examples.md**: Race condition and resource safety examples
- **references/advanced-patterns.md**: Advanced async patterns and optimization

## Validation Gates

### Gate 0.1: Domain Expertise Validation
- **Status**: PASSED
- **Expertise Areas**: asyncio, Tokio, race conditions, resource management, concurrent safety

### Gate 0.2: Vulnerability Research
- **Status**: PASSED (3+ issues for MEDIUM-RISK)
- **Research Date**: 2025-11-20
- **Issues**: CVE-2024-12254 (asyncio memory), Redis race condition (CVE-2023-28858/9)

### Gate 0.11: File Organization Decision
- **Decision**: Split structure (MEDIUM-RISK, ~400 lines main + references)

---

## 1. Overview

**Risk Level**: MEDIUM

**Justification**: Async programming introduces race conditions, resource leaks, and timing-based vulnerabilities. While not directly exposed to external attacks, improper async code can cause data corruption, deadlocks, and security-sensitive race conditions like double-spending or TOCTOU (time-of-check-time-of-use).

You are an expert in asynchronous programming patterns for Python (asyncio) and Rust (Tokio). You write concurrent code that is free from race conditions, properly manages resources, and handles errors gracefully.

### Core Expertise Areas
- Race condition identification and prevention
- Async resource management (connections, locks, files)
- Error handling in concurrent contexts
- Performance optimization for async workloads
- Graceful shutdown and cancellation

---

## 2. Core Principles

1. **TDD First**: Write async tests before implementation using pytest-asyncio
2. **Performance Aware**: Use asyncio.gather, semaphores, and avoid blocking calls
3. **Identify Race Conditions**: Recognize shared state accessed across await points
4. **Protect Shared State**: Use locks, atomic operations, or message passing
5. **Manage Resources**: Ensure cleanup happens even on cancellation
6. **Handle Errors**: Don't let one task's failure corrupt others
7. **Avoid Deadlocks**: Consistent lock ordering, timeouts on locks

### Decision Framework

| Situation | Approach |
|-----------|----------|
| Shared mutable state | Use asyncio.Lock or RwLock |
| Database transaction | Use atomic operations, SELECT FOR UPDATE |
| Resource cleanup | Use async context managers |
| Task coordination | Use asyncio.Event, Queue, or Semaphore |
| Background tasks | Track tasks, handle cancellation |

---

## 3. Implementation Workflow (TDD)

### Step 1: Write Failing Test First

```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_concurrent_counter_safety():
    """Test counter maintains consistency under concurrent access."""
    counter = SafeCounter()  # Not implemented yet - will fail

    async def increment_many():
        for _ in range(100):
            await counter.increment()

    # Run 10 concurrent incrementers
    await asyncio.gather(*[increment_many() for _ in range(10)])

    # Must be exactly 1000 (no lost updates)
    assert await counter.get() == 1000

@pytest.mark.asyncio
async def test_resource_cleanup_on_cancellation():
    """Test resources are cleaned up even when task is cancelled."""
    cleanup_called = False

    async def task_with_resource():
        nonlocal cleanup_called
        async with managed_resource() as resource:  # Not implemented yet
            await asyncio.sleep(10)  # Long operation
        cleanup_called = True

    task = asyncio.create_task(task_with_resource())
    await asyncio.sleep(0.1)
    task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await task

    assert cleanup_called  # Cleanup must happen
```

### Step 2: Implement Minimum to Pass

```python
import asyncio
from contextlib import asynccontextmanager

class SafeCounter:
    def __init__(self):
        self._value = 0
        self._lock = asyncio.Lock()

    async def increment(self) -> int:
        async with self._lock:
            self._value += 1
            return self._value

    async def get(self) -> int:
        async with self._lock:
            return self._value

@asynccontextmanager
async def managed_resource():
    resource = await acquire_resource()
    try:
        yield resource
    finally:
        await release_resource(resource)  # Always runs
```

### Step 3: Refactor Following Patterns

Apply performance patterns, add timeouts, improve error handling.

### Step 4: Run Full Verification

```bash
# Run async tests
pytest tests/ -v --asyncio-mode=auto

# Check for blocking calls
python -m asyncio debug

# Run with concurrency stress test
pytest tests/ -v -n auto --asyncio-mode=auto
```

---

## 4. Performance Patterns

### Pattern 1: asyncio.gather for Concurrency

```python
# BAD - Sequential execution
async def fetch_all_sequential(urls: list[str]) -> list[str]:
    results = []
    for url in urls:
        result = await fetch(url)  # Waits for each
        results.append(result)
    return results  # Total time: sum of all fetches

# GOOD - Concurrent execution
async def fetch_all_concurrent(urls: list[str]) -> list[str]:
    return await asyncio.gather(*[fetch(url) for url in urls])
    # Total time: max of all fetches
```

### Pattern 2: Semaphores for Rate Limiting

```python
# BAD - Unbounded concurrency (may overwhelm server)
async def fetch_many(urls: list[str]):
    return await asyncio.gather(*[fetch(url) for url in urls])

# GOOD - Bounded concurrency with semaphore
async def fetch_many_limited(urls: list[str], max_concurrent: int = 10):
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_with_limit(url: str):
        async with semaphore:
            return await fetch(url)

    return await asyncio.gather(*[fetch_with_limit(url) for url in urls])
```

### Pattern 3: Task Groups (Python 3.11+)

```python
# BAD - Manual task tracking
async def process_items_manual(items):
    tasks = []
    for item in items:
        task = asyncio.create_task(process(item))
        tasks.append(task)
    return await asyncio.gather(*tasks)

# GOOD - Task groups with automatic cleanup
async def process_items_taskgroup(items):
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(process(item)) for item in items]
    return [task.result() for task in tasks]
    # Automatic cancellation on any failure
```

### Pattern 4: Efficient Event Loop Usage

```python
# BAD - Creating new event loop each time
def run_async_bad():
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(main())
    finally:
        loop.close()

# GOOD - Reuse running loop or use asyncio.run
def run_async_good():
    return asyncio.run(main())  # Handles loop lifecycle

# GOOD - For library code, get existing loop
async def library_function():
    loop = asyncio.get_running_loop()
    future = loop.create_future()
    # Use the existing loop
```

### Pattern 5: Avoiding Blocking Calls

```python
# BAD - Blocks event loop
async def process_file_bad(path: str):
    with open(path) as f:  # Blocking I/O
        data = f.read()
    result = hashlib.sha256(data).hexdigest()  # CPU-bound blocks loop
    return result

# GOOD - Non-blocking with aiofiles and executor
import aiofiles

async def process_file_good(path: str):
    async with aiofiles.open(path, 'rb') as f:
        data = await f.read()

    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(
        None, lambda: hashlib.sha256(data).hexdigest()
    )
    return result
```

---

## 5. Technical Foundation

### Version Recommendations

| Component | Version | Notes |
|-----------|---------|-------|
| **Python** | 3.11+ | asyncio improvements, TaskGroup |
| **Rust** | 1.75+ | Stable async |
| **Tokio** | 1.35+ | Async runtime |
| **aioredis** | Use redis-py | Better maintenance |

### Key Libraries

```python
# Python async ecosystem
asyncio           # Core async
aiohttp           # HTTP client
asyncpg           # PostgreSQL
aiofiles          # File I/O
pytest-asyncio    # Testing
```

---

## 6. Implementation Patterns

### Pattern 1: Protecting Shared State with Locks

```python
import asyncio

class SafeCounter:
    """Thread-safe counter for async contexts."""
    def __init__(self):
        self._value = 0
        self._lock = asyncio.Lock()

    async def increment(self) -> int:
        async with self._lock:
            self._value += 1
            return self._value

    async def get(self) -> int:
        async with self._lock:
            return self._value
```

### Pattern 2: Atomic Database Operations

```python
from sqlalchemy.ext.asyncio import AsyncSession

async def transfer_safe(db: AsyncSession, from_id: int, to_id: int, amount: int):
    """Atomic transfer using row locks."""
    async with db.begin():
        stmt = (
            select(Account)
            .where(Account.id.in_([from_id, to_id]))
            .with_for_update()  # Lock rows
        )
        accounts = {a.id: a for a in (await db.execute(stmt)).scalars()}

        if accounts[from_id].balance < amount:
            raise ValueError("Insufficient funds")

        accounts[from_id].balance -= amount
        accounts[to_id].balance += amount
```

### Pattern 3: Resource Management with Context Managers

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_connection():
    """Ensure connection cleanup even on cancellation."""
    conn = await pool.acquire()
    try:
        yield conn
    finally:
        await pool.release(conn)
```

### Pattern 4: Graceful Shutdown

```python
import asyncio, signal

class GracefulApp:
    def __init__(self):
        self.shutdown_event = asyncio.Event()
        self.tasks: set[asyncio.Task] = set()

    async def run(self):
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, self.shutdown_event.set)

        self.tasks.add(asyncio.create_task(self.worker()))
        await self.shutdown_event.wait()

        for task in self.tasks:
            task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)
```

---

## 7. Security Standards

### 7.1 Common Async Vulnerabilities

| Issue | Severity | Mitigation |
|-------|----------|------------|
| Race Conditions | HIGH | Use locks or atomic ops |
| TOCTOU | HIGH | Atomic DB operations |
| Resource Leaks | MEDIUM | Context managers |
| CVE-2024-12254 | HIGH | Upgrade Python |
| Deadlocks | MEDIUM | Lock ordering, timeouts |

### 7.2 Race Condition Detection

```python
# RACE CONDITION - read/await/write pattern
class UserSession:
    async def update(self, key, value):
        current = self.data.get(key, 0)  # Read
        await validate(value)             # Await = context switch
        self.data[key] = current + value  # Write stale value

# FIXED - validate outside lock, atomic update inside
class SafeUserSession:
    async def update(self, key, value):
        await validate(value)
        async with self._lock:
            self.data[key] = self.data.get(key, 0) + value
```

---

## 8. Common Mistakes & Anti-Patterns

### Anti-Pattern 1: Unprotected Shared State

```python
# NEVER - race condition on cache
async def get_or_fetch(self, key):
    if key not in self.data:
        self.data[key] = await fetch(key)
    return self.data[key]

# ALWAYS - lock protection
async def get_or_fetch(self, key):
    async with self._lock:
        if key not in self.data:
            self.data[key] = await fetch(key)
        return self.data[key]
```

### Anti-Pattern 2: Fire and Forget Tasks

```python
# NEVER - task may be garbage collected
asyncio.create_task(background_work())

# ALWAYS - track tasks
task = asyncio.create_task(background_work())
self.tasks.add(task)
task.add_done_callback(self.tasks.discard)
```

### Anti-Pattern 3: Blocking the Event Loop

```python
# NEVER - blocks all async tasks
time.sleep(5)

# ALWAYS - use async
await asyncio.sleep(5)
result = await loop.run_in_executor(None, cpu_bound_func)
```

---

## 9. Pre-Implementation Checklist

### Phase 1: Before Writing Code

- [ ] Write failing tests for race condition scenarios
- [ ] Write tests for resource cleanup on cancellation
- [ ] Identify all shared mutable state
- [ ] Plan lock hierarchy to avoid deadlocks
- [ ] Determine appropriate concurrency limits

### Phase 2: During Implementation

- [ ] Protect all shared state with locks
- [ ] Use async context managers for resources
- [ ] Use asyncio.gather for concurrent operations
- [ ] Apply semaphores for rate limiting
- [ ] Run executor for CPU-bound work
- [ ] Track all created tasks

### Phase 3: Before Committing

- [ ] All async tests pass: `pytest --asyncio-mode=auto`
- [ ] No blocking calls on event loop
- [ ] Timeouts on all external operations
- [ ] Graceful shutdown handles cancellation
- [ ] Race condition tests verify thread safety
- [ ] Lock ordering is consistent (no deadlock potential)

---

## 10. Summary

Your goal is to create async code that is:
- **Test-Driven**: Write async tests first with pytest-asyncio
- **Race-Free**: Protect shared state, use atomic operations
- **Resource-Safe**: Context managers, proper cleanup
- **Performant**: asyncio.gather, semaphores, avoid blocking
- **Resilient**: Handle errors, support cancellation

**Key Performance Rules**:
1. Use `asyncio.gather` for concurrent I/O operations
2. Apply semaphores to limit concurrent connections
3. Use TaskGroup (Python 3.11+) for automatic cleanup
4. Never block event loop - use `run_in_executor` for CPU work
5. Reuse event loops, don't create new ones

**Security Reminder**:
1. Every shared mutable state needs protection
2. Database operations must be atomic (TOCTOU prevention)
3. Always use async context managers for resources
4. Track all tasks for graceful shutdown
5. Test with concurrent load to find race conditions
