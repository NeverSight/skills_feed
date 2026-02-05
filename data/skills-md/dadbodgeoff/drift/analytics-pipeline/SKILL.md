---
name: analytics-pipeline
description: Real-time analytics with Redis counters, periodic PostgreSQL flush, and time-series aggregation. High-performance event tracking without database bottlenecks.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: data-processing
  time: 6h
  source: drift-masterguide
---

# Analytics Pipeline

High-performance analytics with Redis counters and periodic database flush.

## When to Use This Skill

- Need high-throughput event tracking (thousands/second)
- Want real-time counters without database bottlenecks
- Building dashboards with time-series data
- Tracking user activity, feature usage, or page views

## Core Concepts

Write to Redis for speed, flush to PostgreSQL for persistence. Redis handles high write throughput, periodic workers batch-flush to the database.


```
Events → Redis Counters → Periodic Flush Worker → PostgreSQL → Dashboard Queries
```

## Implementation

### Python

```python
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, List
import redis.asyncio as redis


class AnalyticsEventType(str, Enum):
    GENERATION_COMPLETED = "generation_completed"
    USER_SIGNUP = "user_signup"
    FEATURE_USED = "feature_used"
    PAGE_VIEW = "page_view"


@dataclass
class AnalyticsEvent:
    event_type: AnalyticsEventType
    user_id: Optional[str] = None
    properties: Optional[Dict] = None
    timestamp: Optional[datetime] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)


class AnalyticsKeys:
    """Redis key patterns for analytics counters."""
    PREFIX = "analytics"

    @staticmethod
    def daily_counter(event_type: str, date: datetime = None) -> str:
        d = date or datetime.now(timezone.utc)
        return f"analytics:counter:{event_type}:{d.strftime('%Y-%m-%d')}"

    @staticmethod
    def hourly_counter(event_type: str, date: datetime = None) -> str:
        d = date or datetime.now(timezone.utc)
        return f"analytics:counter:{event_type}:{d.strftime('%Y-%m-%d:%H')}"

    @staticmethod
    def user_daily_counter(user_id: str, event_type: str, date: datetime = None) -> str:
        d = date or datetime.now(timezone.utc)
        return f"analytics:user:{user_id}:{event_type}:{d.strftime('%Y-%m-%d')}"

    @staticmethod
    def pending_flush_set() -> str:
        return "analytics:pending_flush"


class AnalyticsService:
    """High-performance analytics using Redis counters."""
    COUNTER_TTL = 7 * 24 * 60 * 60  # 7 days

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    async def track_event(self, event: AnalyticsEvent) -> None:
        pipe = self.redis.pipeline()

        # Daily counter
        daily_key = AnalyticsKeys.daily_counter(event.event_type.value, event.timestamp)
        pipe.incr(daily_key)
        pipe.expire(daily_key, self.COUNTER_TTL)

        # Hourly counter
        hourly_key = AnalyticsKeys.hourly_counter(event.event_type.value, event.timestamp)
        pipe.incr(hourly_key)
        pipe.expire(hourly_key, self.COUNTER_TTL)

        # Per-user counter
        if event.user_id:
            user_key = AnalyticsKeys.user_daily_counter(event.user_id, event.event_type.value, event.timestamp)
            pipe.incr(user_key)
            pipe.expire(user_key, self.COUNTER_TTL)

        # Track for flush
        pipe.sadd(AnalyticsKeys.pending_flush_set(), 
                  f"{event.event_type.value}:{event.timestamp.strftime('%Y-%m-%d')}")

        await pipe.execute()

    async def get_daily_count(self, event_type: AnalyticsEventType, date: datetime = None) -> int:
        key = AnalyticsKeys.daily_counter(event_type.value, date)
        count = await self.redis.get(key)
        return int(count) if count else 0

    async def get_hourly_counts(self, event_type: AnalyticsEventType, date: datetime = None) -> Dict[int, int]:
        d = date or datetime.now(timezone.utc)
        pipe = self.redis.pipeline()
        for hour in range(24):
            hour_dt = d.replace(hour=hour, minute=0, second=0, microsecond=0)
            pipe.get(AnalyticsKeys.hourly_counter(event_type.value, hour_dt))
        results = await pipe.execute()
        return {hour: int(count) if count else 0 for hour, count in enumerate(results)}
```


```python
class AnalyticsFlushWorker:
    """Periodically flushes Redis counters to PostgreSQL."""
    FLUSH_INTERVAL = 300  # 5 minutes
    BATCH_SIZE = 100

    def __init__(self, redis_client: redis.Redis, pg_pool):
        self.redis = redis_client
        self.pg = pg_pool
        self._running = False

    async def start(self) -> None:
        self._running = True
        while self._running:
            try:
                await self.flush()
            except Exception as e:
                logger.error(f"Flush error: {e}")
            await asyncio.sleep(self.FLUSH_INTERVAL)

    async def flush(self) -> int:
        pending = await self.redis.smembers(AnalyticsKeys.pending_flush_set())
        if not pending:
            return 0

        flushed = 0
        pending_list = list(pending)

        for i in range(0, len(pending_list), self.BATCH_SIZE):
            batch = pending_list[i:i + self.BATCH_SIZE]
            counters = await self._collect_counters(batch)

            if counters:
                await self._write_to_postgres(counters)
                flushed += len(counters)
                await self.redis.srem(AnalyticsKeys.pending_flush_set(), *batch)

        return flushed

    async def _collect_counters(self, pending_keys: List[str]) -> List[tuple]:
        counters = []
        pipe = self.redis.pipeline()

        for pending in pending_keys:
            parts = pending.split(":", 1)
            if len(parts) != 2:
                continue
            event_type, date = parts
            key = AnalyticsKeys.daily_counter(event_type, datetime.fromisoformat(date))
            pipe.getdel(key)  # Atomic get-and-delete

        results = await pipe.execute()

        for pending, count in zip(pending_keys, results):
            if count:
                parts = pending.split(":", 1)
                counters.append((parts[0], parts[1], int(count)))

        return counters

    async def _write_to_postgres(self, counters: List[tuple]) -> None:
        async with self.pg.acquire() as conn:
            await conn.executemany("""
                INSERT INTO analytics_daily (event_type, date, count, updated_at)
                VALUES ($1, $2, $3, NOW())
                ON CONFLICT (event_type, date)
                DO UPDATE SET count = analytics_daily.count + EXCLUDED.count, updated_at = NOW()
            """, counters)
```

## Usage Examples

```python
# Track events
analytics = AnalyticsService(redis_client)

await analytics.track_event(AnalyticsEvent(
    event_type=AnalyticsEventType.GENERATION_COMPLETED,
    user_id="user_123",
    properties={"model": "gpt-4"},
))

# Query real-time counts
today_count = await analytics.get_daily_count(AnalyticsEventType.GENERATION_COMPLETED)
hourly = await analytics.get_hourly_counts(AnalyticsEventType.GENERATION_COMPLETED)

# Start flush worker
worker = AnalyticsFlushWorker(redis_client, pg_pool)
asyncio.create_task(worker.start())
```

## Best Practices

1. Use Redis pipelines for batched counter updates
2. Set TTL on counters to prevent memory growth
3. Use GETDEL for atomic flush to prevent double-counting
4. Upsert on flush to handle duplicate dates gracefully
5. Separate user vs global analytics tables for query efficiency

## Common Mistakes

- Not setting TTL on Redis keys (memory leak)
- Using GET then DEL instead of GETDEL (race condition)
- Flushing too frequently (database load)
- Not batching flush operations

## Related Patterns

- metrics-collection (system metrics)
- intelligent-cache (caching strategies)
