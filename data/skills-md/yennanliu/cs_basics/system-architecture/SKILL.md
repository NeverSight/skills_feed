---
name: system-architecture
description: System design and architecture expert for creating scalable distributed systems. Covers system design interviews, architecture patterns, and real-world case studies like Netflix, Twitter, Uber. Use when designing systems, writing architecture docs, or preparing for system design interviews.
allowed-tools: Read, Glob, Grep, Write
---

# System Architecture Expert

## When to use this Skill

Use this Skill when:
- Designing distributed systems
- Writing system design documentation
- Preparing for system design interviews
- Creating architecture diagrams
- Analyzing trade-offs between design choices
- Reviewing or improving existing system designs

## System Design Framework

### 1. Requirements Gathering (5-10 minutes)

**Functional Requirements:**
- What are the core features?
- What actions can users perform?
- What are the inputs and outputs?

**Non-Functional Requirements:**
- Scale: How many users? How much data?
- Performance: Latency requirements? (p50, p95, p99)
- Availability: What uptime is needed? (99.9%, 99.99%)
- Consistency: Strong or eventual consistency?

**Constraints:**
- Budget limitations
- Technology stack constraints
- Team expertise
- Timeline

**Example Questions:**
```
- How many daily active users?
- What's the read:write ratio?
- What's the average data size?
- What's the peak load vs average load?
- Do we need real-time updates?
- Can we have data loss?
```

### 2. Capacity Estimation (Back-of-the-envelope)

**Calculate:**
```
Traffic:
- DAU = 100M users
- Each user makes 10 requests/day
- QPS = 100M * 10 / 86400 ≈ 11,574 QPS
- Peak QPS = 2-3x average ≈ 30,000 QPS

Storage:
- 100M users * 1KB per user = 100GB
- With 3x replication = 300GB
- Growth: 300GB * 365 days = 109.5TB/year

Bandwidth:
- QPS * average request size
- 11,574 * 10KB = 115.74MB/s
```

**Memory/Cache:**
- 80-20 rule: 20% of data gets 80% of traffic
- Cache = 20% of total data for hot data

### 3. High-Level Design

**Core Components:**
1. **Client Layer** (Web, Mobile, Desktop)
2. **API Gateway / Load Balancer**
3. **Application Servers** (Business logic)
4. **Cache Layer** (Redis, Memcached)
5. **Database** (SQL, NoSQL, or both)
6. **Message Queue** (Kafka, RabbitMQ)
7. **Object Storage** (S3, GCS)
8. **CDN** (CloudFront, Akamai)

**Draw Architecture:**
```
[Clients] → [CDN]
            ↓
        [Load Balancer]
            ↓
    [Application Servers]
        ↙     ↓     ↘
   [Cache] [DB] [Queue] → [Workers]
                            ↓
                      [Object Storage]
```

### 4. Database Design

**SQL vs NoSQL Decision:**

**Use SQL when:**
- ACID transactions required
- Complex queries with JOINs
- Structured data with relationships
- Examples: PostgreSQL, MySQL

**Use NoSQL when:**
- Massive scale (horizontal scaling)
- Flexible schema
- High write throughput
- Examples: Cassandra, DynamoDB, MongoDB

**Sharding Strategy:**
- Hash-based: `user_id % num_shards`
- Range-based: Users 1-100M on shard 1
- Geographic: US users on US shard
- Consistent hashing: For even distribution

**Schema Design:**
```sql
-- Example: URL Shortener
CREATE TABLE urls (
    id BIGSERIAL PRIMARY KEY,
    short_url VARCHAR(10) UNIQUE NOT NULL,
    long_url TEXT NOT NULL,
    user_id BIGINT,
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP,
    click_count INT DEFAULT 0,
    INDEX (short_url),
    INDEX (user_id)
);
```

### 5. Deep Dive Components

**Caching Strategy:**
- **Cache-Aside**: App reads from cache, loads from DB on miss
- **Write-Through**: Write to cache and DB together
- **Write-Behind**: Write to cache, async write to DB

**Eviction Policies:**
- LRU (Least Recently Used) - Most common
- LFU (Least Frequently Used)
- TTL (Time To Live)

**Load Balancing:**
- Round Robin: Simple, equal distribution
- Least Connections: Route to least busy server
- Consistent Hashing: Minimize redistribution
- Weighted: Based on server capacity

**Message Queue Patterns:**
- **Pub/Sub**: One-to-many (notifications)
- **Work Queue**: Task distribution (job processing)
- **Fan-out**: Broadcast to multiple queues

### 6. Scalability Patterns

**Horizontal Scaling:**
- Add more servers
- Use load balancers
- Stateless application servers
- Session stored in cache/DB

**Vertical Scaling:**
- Add more CPU/RAM to servers
- Limited by hardware
- Simpler but has limits

**Microservices:**
```
Monolith:
[Single App] → [DB]

Microservices:
[User Service] → [User DB]
[Post Service] → [Post DB]
[Feed Service] → [Feed DB]
```

**Benefits:**
- Independent scaling
- Technology flexibility
- Fault isolation

**Drawbacks:**
- Increased complexity
- Network latency
- Distributed transactions

### 7. Reliability & Availability

**Replication:**
- Master-Slave: One writer, multiple readers
- Master-Master: Multiple writers (conflict resolution needed)
- Multi-region: Geographic redundancy

**Failover:**
- Active-Passive: Standby server takes over
- Active-Active: Both servers handle traffic

**Rate Limiting:**
- Token bucket algorithm
- Leaky bucket algorithm
- Fixed window counter
- Sliding window log

**Circuit Breaker:**
```
States:
Closed → Normal operation
Open → Reject requests immediately
Half-Open → Test if service recovered
```

### 8. Common System Design Patterns

**Content Delivery:**
- Use CDN for static assets
- Geo-distributed edge servers
- Cache at edge locations

**Data Consistency:**
- **Strong Consistency**: Read reflects latest write (ACID)
- **Eventual Consistency**: Reads eventually reflect write (BASE)
- **CAP Theorem**: Choose 2 of 3: Consistency, Availability, Partition Tolerance

**API Design:**
```
RESTful:
GET    /api/users/{id}
POST   /api/users
PUT    /api/users/{id}
DELETE /api/users/{id}

GraphQL:
query {
  user(id: "123") {
    name
    posts {
      title
    }
  }
}
```

### 9. System Design Template

Use this structure (based on `system_design/00_template.md`):

```markdown
# {System Name}

## 1. Requirements
### Functional
- [List core features]

### Non-Functional
- Scale: [Users, QPS, Data]
- Performance: [Latency requirements]
- Availability: [Uptime target]

## 2. Capacity Estimation
- Traffic: [QPS calculations]
- Storage: [Data size, growth]
- Bandwidth: [Network requirements]

## 3. API Design
```
[endpoint] - [description]
```

## 4. High-Level Architecture
[Diagram]

## 5. Database Schema
[Tables and relationships]

## 6. Detailed Design
### Component 1
[Deep dive]

### Component 2
[Deep dive]

## 7. Scalability
[How to scale each component]

## 8. Trade-offs
[Decisions and alternatives]
```

### 10. Real-World Examples

**Reference case studies in `system_design/`:**
- Netflix: Video streaming, recommendation
- Twitter: Timeline, tweet storage, trending
- Uber: Real-time matching, location tracking
- Instagram: Image storage, feed generation
- WhatsApp: Message delivery, presence

**Common Patterns:**
- **News Feed**: Fan-out on write vs fan-out on read
- **Rate Limiter**: Token bucket with Redis
- **URL Shortener**: Base62 encoding, hash collision
- **Chat System**: WebSocket, message queue
- **Notification**: Push notification service, APNs/FCM

## Interview Tips

**Time Management:**
- Requirements: 10%
- High-level design: 25%
- Deep dive: 50%
- Wrap up: 15%

**Communication:**
- Think out loud
- Ask clarifying questions
- Discuss trade-offs
- Acknowledge limitations

**What interviewers look for:**
- Problem-solving approach
- Technical depth
- Trade-off analysis
- Scale awareness
- Communication skills

## Common Mistakes to Avoid

- Jumping to solution without requirements
- Over-engineering simple problems
- Under-estimating scale requirements
- Ignoring single points of failure
- Not considering monitoring/alerting
- Forgetting about data consistency
- Missing security considerations

## Project Context

- Templates in `system_design/00_template.md`
- Case studies in `system_design/*.md`
- Reference materials in `doc/system_design/`
- Follow the established documentation pattern
