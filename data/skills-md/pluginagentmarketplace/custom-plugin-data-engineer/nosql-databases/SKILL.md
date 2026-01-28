---
name: nosql-databases
description: MongoDB, Redis, Cassandra, DynamoDB, and distributed database patterns for scalable applications
sasmp_version: "1.3.0"
bonded_agent: 01-data-engineer
bond_type: SECONDARY_BOND
skill_version: "2.0.0"
last_updated: "2025-01"
complexity: intermediate
estimated_mastery_hours: 110
prerequisites: [python-programming, sql-databases]
unlocks: [big-data, cloud-platforms]
---

# NoSQL Databases

Production-grade NoSQL database patterns with MongoDB, Redis, Cassandra, and DynamoDB.

## Quick Start

```python
# MongoDB with PyMongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client.analytics
events = db.events

# Create index for query performance
events.create_index([("user_id", 1), ("timestamp", -1)])
events.create_index([("event_type", 1)])

# Insert with retry pattern
def insert_event(event: dict, retries: int = 3):
    event["_id"] = f"{event['user_id']}_{event['timestamp'].isoformat()}"
    event["created_at"] = datetime.utcnow()

    for attempt in range(retries):
        try:
            events.insert_one(event)
            return True
        except DuplicateKeyError:
            return False  # Already exists
        except Exception as e:
            if attempt == retries - 1:
                raise
    return False

# Aggregation pipeline
pipeline = [
    {"$match": {"event_type": "purchase", "timestamp": {"$gte": datetime(2024, 1, 1)}}},
    {"$group": {"_id": "$user_id", "total_purchases": {"$sum": "$amount"}, "count": {"$sum": 1}}},
    {"$sort": {"total_purchases": -1}},
    {"$limit": 100}
]
top_customers = list(events.aggregate(pipeline))
```

## Core Concepts

### 1. Redis for Caching & Real-time

```python
import redis
import json
from datetime import timedelta

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Cache pattern with TTL
def get_user_profile(user_id: str) -> dict:
    cache_key = f"user:{user_id}:profile"

    # Try cache first
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)

    # Cache miss - fetch from DB
    profile = fetch_from_database(user_id)

    # Set with 1 hour TTL
    r.setex(cache_key, timedelta(hours=1), json.dumps(profile))
    return profile

# Rate limiting
def check_rate_limit(user_id: str, limit: int = 100, window: int = 60) -> bool:
    key = f"rate:{user_id}:{int(time.time()) // window}"
    current = r.incr(key)

    if current == 1:
        r.expire(key, window)

    return current <= limit

# Real-time leaderboard with sorted sets
def update_leaderboard(user_id: str, score: float):
    r.zadd("leaderboard:daily", {user_id: score})

def get_top_users(n: int = 10) -> list:
    return r.zrevrange("leaderboard:daily", 0, n-1, withscores=True)

# Pub/Sub for event streaming
def publish_event(channel: str, event: dict):
    r.publish(channel, json.dumps(event))

def subscribe_events(channel: str):
    pubsub = r.pubsub()
    pubsub.subscribe(channel)
    for message in pubsub.listen():
        if message['type'] == 'message':
            yield json.loads(message['data'])
```

### 2. DynamoDB Patterns

```python
import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Events')

# Single table design pattern
def put_event(event: dict):
    item = {
        'PK': f"USER#{event['user_id']}",
        'SK': f"EVENT#{event['timestamp']}#{event['event_id']}",
        'GSI1PK': f"TYPE#{event['event_type']}",
        'GSI1SK': f"DATE#{event['timestamp'][:10]}",
        'data': event
    }
    table.put_item(Item=item)

# Query by user
def get_user_events(user_id: str, limit: int = 100):
    response = table.query(
        KeyConditionExpression=Key('PK').eq(f"USER#{user_id}") & Key('SK').begins_with("EVENT#"),
        ScanIndexForward=False,
        Limit=limit
    )
    return response['Items']

# Query by event type (using GSI)
def get_events_by_type(event_type: str, date: str):
    response = table.query(
        IndexName='GSI1',
        KeyConditionExpression=Key('GSI1PK').eq(f"TYPE#{event_type}") & Key('GSI1SK').eq(f"DATE#{date}")
    )
    return response['Items']

# Batch write with exponential backoff
def batch_write_events(events: list):
    with table.batch_writer() as batch:
        for event in events:
            batch.put_item(Item=event)
```

### 3. Cassandra for Time Series

```python
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement, SimpleStatement
from datetime import datetime

cluster = Cluster(['node1', 'node2', 'node3'])
session = cluster.connect('analytics')

# Create table with time-based partitioning
session.execute("""
    CREATE TABLE IF NOT EXISTS events_by_day (
        date date,
        user_id uuid,
        event_time timestamp,
        event_type text,
        data text,
        PRIMARY KEY ((date), event_time, user_id)
    ) WITH CLUSTERING ORDER BY (event_time DESC)
""")

# Insert with prepared statement
insert_stmt = session.prepare("""
    INSERT INTO events_by_day (date, user_id, event_time, event_type, data)
    VALUES (?, ?, ?, ?, ?)
""")

def insert_event(event: dict):
    session.execute(insert_stmt, [
        event['timestamp'].date(),
        event['user_id'],
        event['timestamp'],
        event['event_type'],
        json.dumps(event['data'])
    ])

# Query by date range
def get_events_for_date(date: datetime.date):
    rows = session.execute(
        "SELECT * FROM events_by_day WHERE date = %s",
        [date]
    )
    return list(rows)
```

## Tools & Technologies

| Tool | Purpose | Version (2025) |
|------|---------|----------------|
| **MongoDB** | Document store | 7.0+ |
| **Redis** | Cache, pub/sub | 7.2+ |
| **Cassandra** | Time series, wide column | 5.0+ |
| **DynamoDB** | Managed key-value | Latest |
| **Elasticsearch** | Search, analytics | 8.12+ |
| **ScyllaDB** | High-perf Cassandra | 5.4+ |

## Troubleshooting Guide

| Issue | Symptoms | Root Cause | Fix |
|-------|----------|------------|-----|
| **Hot Partition** | High latency on some keys | Uneven partition key | Redesign partition key |
| **Memory Pressure** | Redis evictions, slow queries | Data > memory | Eviction policy, clustering |
| **Query Timeout** | Slow reads in Cassandra | Missing index, large partition | Add index, limit partition size |
| **Consistency Issues** | Stale reads | Eventual consistency | Use appropriate consistency level |

## Best Practices

```python
# ✅ DO: Design for access patterns (NoSQL)
# Primary key = partition key + sort key

# ✅ DO: Use connection pooling
pool = redis.ConnectionPool(max_connections=20)
r = redis.Redis(connection_pool=pool)

# ✅ DO: Set TTLs on cache data
r.setex(key, ttl_seconds, value)

# ✅ DO: Handle eventual consistency
# Read-your-writes with consistent reads where needed

# ❌ DON'T: Use NoSQL for complex joins
# ❌ DON'T: Store unbounded data in single document
# ❌ DON'T: Ignore partition sizing
```

## Resources

- [MongoDB University](https://university.mongodb.com/)
- [Redis University](https://university.redis.com/)
- [DynamoDB Guide](https://www.dynamodbguide.com/)

---

**Skill Certification Checklist:**
- [ ] Can design document schemas for MongoDB
- [ ] Can implement caching patterns with Redis
- [ ] Can model time series data in Cassandra
- [ ] Can use DynamoDB single-table design
- [ ] Can choose appropriate consistency levels
