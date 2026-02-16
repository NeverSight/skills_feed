---
name: database
description: Database design, SQL, NoSQL, and data management patterns
domain: development-stacks
version: 1.1.0
tags: [postgresql, mysql, mongodb, redis, prisma, migrations, indexing]
triggers:
  keywords:
    primary: [database, sql, postgresql, mysql, mongodb, redis, db]
    secondary: [query, schema, migration, index, orm, prisma, nosql]
  context_boost: [data, storage, persistence, backend]
  context_penalty: [frontend, css, ui]
  priority: high
collaboration:
  prerequisites:
    - skill: backend
      reason: Database is typically used within backend context
  delegation_triggers:
    - trigger: API for data access patterns
      delegate_to: backend
      context: Repository pattern, service layer design
    - trigger: Data validation at API level
      delegate_to: api-design
      context: Request validation, error responses
    - trigger: Database integration tests
      delegate_to: testing-strategies
      context: Test data setup, cleanup strategies
  receives_context_from:
    - skill: backend
      receives:
        - Expected query patterns
        - Transaction requirements
        - Caching strategy
    - skill: api-design
      receives:
        - Pagination requirements
        - Filtering capabilities
  provides_context_to:
    - skill: backend
      provides:
        - Connection pool configuration
        - Query optimization hints
        - Index usage recommendations
    - skill: testing-strategies
      provides:
        - Test database setup scripts
        - Seed data patterns
---

# Database Development

## Overview

Database design, query optimization, and data management patterns for relational and NoSQL databases.

---

## PostgreSQL

### Schema Design

```sql
-- Users table with proper constraints
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100),
    role VARCHAR(20) DEFAULT 'user' CHECK (role IN ('user', 'admin', 'moderator')),
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'suspended', 'deleted')),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Posts with foreign key
CREATE TABLE posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL UNIQUE,
    content TEXT,
    excerpt VARCHAR(500),
    status VARCHAR(20) DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'archived')),
    author_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Many-to-many with junction table
CREATE TABLE tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) NOT NULL UNIQUE,
    slug VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE post_tags (
    post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
    tag_id UUID REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, tag_id)
);

-- Indexes
CREATE INDEX idx_posts_author ON posts(author_id);
CREATE INDEX idx_posts_status ON posts(status) WHERE status = 'published';
CREATE INDEX idx_posts_published_at ON posts(published_at DESC) WHERE status = 'published';
CREATE INDEX idx_users_email_lower ON users(LOWER(email));

-- Full-text search
ALTER TABLE posts ADD COLUMN search_vector tsvector;
CREATE INDEX idx_posts_search ON posts USING GIN(search_vector);

CREATE OR REPLACE FUNCTION update_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.excerpt, '')), 'B') ||
        setweight(to_tsvector('english', COALESCE(NEW.content, '')), 'C');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER posts_search_update
BEFORE INSERT OR UPDATE ON posts
FOR EACH ROW EXECUTE FUNCTION update_search_vector();
```

### Advanced Queries

```sql
-- Common Table Expressions (CTE)
WITH post_stats AS (
    SELECT
        author_id,
        COUNT(*) as post_count,
        AVG(LENGTH(content)) as avg_length
    FROM posts
    WHERE status = 'published'
    GROUP BY author_id
)
SELECT
    u.name,
    u.email,
    ps.post_count,
    ps.avg_length
FROM users u
JOIN post_stats ps ON u.id = ps.author_id
ORDER BY ps.post_count DESC
LIMIT 10;

-- Window functions
SELECT
    p.title,
    p.published_at,
    u.name as author,
    ROW_NUMBER() OVER (PARTITION BY p.author_id ORDER BY p.published_at DESC) as author_rank,
    COUNT(*) OVER (PARTITION BY p.author_id) as author_total_posts,
    p.published_at - LAG(p.published_at) OVER (PARTITION BY p.author_id ORDER BY p.published_at) as days_since_last
FROM posts p
JOIN users u ON p.author_id = u.id
WHERE p.status = 'published';

-- Recursive CTE (hierarchical data)
WITH RECURSIVE category_tree AS (
    -- Base case
    SELECT id, name, parent_id, 0 as depth, ARRAY[name] as path
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    -- Recursive case
    SELECT c.id, c.name, c.parent_id, ct.depth + 1, ct.path || c.name
    FROM categories c
    JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT * FROM category_tree ORDER BY path;

-- JSONB queries
SELECT
    id,
    metadata->>'theme' as theme,
    metadata->'preferences'->>'notifications' as notifications
FROM users
WHERE metadata @> '{"verified": true}'
AND metadata->'preferences' ? 'dark_mode';

-- Update JSONB
UPDATE users
SET metadata = jsonb_set(
    metadata,
    '{lastLogin}',
    to_jsonb(NOW())
)
WHERE id = $1;
```

### Performance Optimization

```sql
-- Analyze query plan
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT p.*, u.name as author_name
FROM posts p
JOIN users u ON p.author_id = u.id
WHERE p.status = 'published'
ORDER BY p.published_at DESC
LIMIT 20;

-- Partial index for common queries
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';

-- Covering index (index-only scan)
CREATE INDEX idx_posts_list ON posts(status, published_at DESC)
INCLUDE (title, slug, excerpt, author_id);

-- BRIN index for time-series data
CREATE INDEX idx_events_created ON events USING BRIN(created_at);

-- Table partitioning
CREATE TABLE events (
    id UUID DEFAULT gen_random_uuid(),
    event_type VARCHAR(50),
    payload JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
) PARTITION BY RANGE (created_at);

CREATE TABLE events_2024_q1 PARTITION OF events
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE events_2024_q2 PARTITION OF events
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');
```

---

## MongoDB

### Schema Design

```javascript
// User document with embedded data
const userSchema = {
  _id: ObjectId,
  email: String,
  passwordHash: String,
  profile: {
    name: String,
    avatar: String,
    bio: String,
  },
  preferences: {
    theme: String,
    notifications: {
      email: Boolean,
      push: Boolean,
    },
  },
  roles: [String],
  createdAt: Date,
  updatedAt: Date,
};

// Post with references
const postSchema = {
  _id: ObjectId,
  title: String,
  slug: String,
  content: String,
  authorId: ObjectId,  // Reference to users
  tags: [String],      // Denormalized for read performance
  stats: {
    views: Number,
    likes: Number,
    comments: Number,
  },
  status: String,
  publishedAt: Date,
  createdAt: Date,
};

// Indexes
db.users.createIndex({ email: 1 }, { unique: true });
db.posts.createIndex({ authorId: 1, publishedAt: -1 });
db.posts.createIndex({ tags: 1 });
db.posts.createIndex({ title: "text", content: "text" });
```

### Aggregation Pipeline

```javascript
// Complex aggregation
db.posts.aggregate([
  // Match published posts
  { $match: { status: "published" } },

  // Lookup author
  {
    $lookup: {
      from: "users",
      localField: "authorId",
      foreignField: "_id",
      as: "author",
    },
  },
  { $unwind: "$author" },

  // Group by author
  {
    $group: {
      _id: "$author._id",
      authorName: { $first: "$author.profile.name" },
      postCount: { $sum: 1 },
      totalViews: { $sum: "$stats.views" },
      avgLikes: { $avg: "$stats.likes" },
      posts: {
        $push: {
          title: "$title",
          publishedAt: "$publishedAt",
        },
      },
    },
  },

  // Sort by post count
  { $sort: { postCount: -1 } },

  // Limit to top 10
  { $limit: 10 },

  // Project final shape
  {
    $project: {
      _id: 0,
      authorId: "$_id",
      authorName: 1,
      postCount: 1,
      totalViews: 1,
      avgLikes: { $round: ["$avgLikes", 2] },
      recentPosts: { $slice: ["$posts", 5] },
    },
  },
]);

// Faceted search
db.products.aggregate([
  { $match: { $text: { $search: "laptop" } } },
  {
    $facet: {
      results: [
        { $sort: { score: { $meta: "textScore" } } },
        { $skip: 0 },
        { $limit: 20 },
      ],
      priceRanges: [
        {
          $bucket: {
            groupBy: "$price",
            boundaries: [0, 500, 1000, 2000, Infinity],
            default: "Other",
            output: { count: { $sum: 1 } },
          },
        },
      ],
      brands: [{ $group: { _id: "$brand", count: { $sum: 1 } } }],
      totalCount: [{ $count: "count" }],
    },
  },
]);
```

---

## Redis

### Data Structures

```typescript
import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);

// String operations
await redis.set('user:123:name', 'John');
await redis.setex('session:abc', 3600, JSON.stringify(sessionData)); // with TTL
const name = await redis.get('user:123:name');

// Hash operations
await redis.hset('user:123', {
  name: 'John',
  email: 'john@example.com',
  role: 'admin',
});
const user = await redis.hgetall('user:123');
await redis.hincrby('user:123', 'loginCount', 1);

// List operations (queues)
await redis.lpush('queue:emails', JSON.stringify(emailJob));
const job = await redis.brpop('queue:emails', 0); // Blocking pop

// Set operations
await redis.sadd('user:123:followers', 'user:456', 'user:789');
await redis.sadd('user:456:followers', 'user:123', 'user:789');
const mutualFollowers = await redis.sinter(
  'user:123:followers',
  'user:456:followers'
);

// Sorted set (leaderboard)
await redis.zadd('leaderboard', 100, 'player1', 95, 'player2', 110, 'player3');
const topPlayers = await redis.zrevrange('leaderboard', 0, 9, 'WITHSCORES');
const rank = await redis.zrevrank('leaderboard', 'player1');

// HyperLogLog (unique counts)
await redis.pfadd('pageviews:2024-01-15', 'user:123', 'user:456');
const uniqueViews = await redis.pfcount('pageviews:2024-01-15');
```

### Caching Patterns

```typescript
// Cache-aside pattern
async function getCachedUser(userId: string): Promise<User> {
  const cacheKey = `user:${userId}`;

  // Try cache first
  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }

  // Cache miss - fetch from DB
  const user = await db.user.findUnique({ where: { id: userId } });

  if (user) {
    // Store in cache with TTL
    await redis.setex(cacheKey, 3600, JSON.stringify(user));
  }

  return user;
}

// Cache invalidation
async function updateUser(userId: string, data: UpdateUserInput) {
  const user = await db.user.update({
    where: { id: userId },
    data,
  });

  // Invalidate cache
  await redis.del(`user:${userId}`);

  return user;
}

// Rate limiting
async function checkRateLimit(userId: string, limit: number, window: number) {
  const key = `ratelimit:${userId}`;
  const current = await redis.incr(key);

  if (current === 1) {
    await redis.expire(key, window);
  }

  return current <= limit;
}
```

---

## Prisma ORM

### Schema Definition

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  password  String
  name      String?
  role      Role     @default(USER)

  posts     Post[]
  comments  Comment[]
  profile   Profile?

  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([email])
}

model Profile {
  id     String  @id @default(cuid())
  bio    String?
  avatar String?

  user   User   @relation(fields: [userId], references: [id], onDelete: Cascade)
  userId String @unique
}

model Post {
  id          String    @id @default(cuid())
  title       String
  slug        String    @unique
  content     String?
  published   Boolean   @default(false)
  publishedAt DateTime?

  author   User   @relation(fields: [authorId], references: [id])
  authorId String

  tags     Tag[]
  comments Comment[]

  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([authorId, published])
  @@index([publishedAt(sort: Desc)])
}

model Tag {
  id    String @id @default(cuid())
  name  String @unique
  slug  String @unique
  posts Post[]
}

model Comment {
  id      String @id @default(cuid())
  content String

  author   User   @relation(fields: [authorId], references: [id])
  authorId String

  post   Post   @relation(fields: [postId], references: [id], onDelete: Cascade)
  postId String

  createdAt DateTime @default(now())
}

enum Role {
  USER
  ADMIN
  MODERATOR
}
```

### Query Patterns

```typescript
import { PrismaClient, Prisma } from '@prisma/client';

const prisma = new PrismaClient();

// Basic queries
const users = await prisma.user.findMany({
  where: {
    role: 'USER',
    email: { contains: '@example.com' },
  },
  select: {
    id: true,
    email: true,
    name: true,
    _count: { select: { posts: true } },
  },
  orderBy: { createdAt: 'desc' },
  take: 10,
  skip: 0,
});

// Complex query with relations
const postsWithAuthor = await prisma.post.findMany({
  where: {
    published: true,
    OR: [
      { title: { contains: searchTerm, mode: 'insensitive' } },
      { content: { contains: searchTerm, mode: 'insensitive' } },
    ],
  },
  include: {
    author: {
      select: { id: true, name: true, profile: true },
    },
    tags: true,
    _count: { select: { comments: true } },
  },
  orderBy: { publishedAt: 'desc' },
});

// Transactions
const [post, notification] = await prisma.$transaction([
  prisma.post.create({
    data: {
      title: 'New Post',
      slug: 'new-post',
      authorId: userId,
    },
  }),
  prisma.notification.create({
    data: {
      type: 'NEW_POST',
      userId: userId,
    },
  }),
]);

// Interactive transaction
const transfer = await prisma.$transaction(async (tx) => {
  const from = await tx.account.update({
    where: { id: fromAccountId },
    data: { balance: { decrement: amount } },
  });

  if (from.balance < 0) {
    throw new Error('Insufficient funds');
  }

  const to = await tx.account.update({
    where: { id: toAccountId },
    data: { balance: { increment: amount } },
  });

  return { from, to };
});

// Raw queries when needed
const result = await prisma.$queryRaw<Post[]>`
  SELECT p.*, ts_rank(search_vector, to_tsquery(${searchQuery})) as rank
  FROM posts p
  WHERE search_vector @@ to_tsquery(${searchQuery})
  ORDER BY rank DESC
  LIMIT 20
`;
```

---

## Migrations

```bash
# Prisma migrations
npx prisma migrate dev --name add_user_status
npx prisma migrate deploy  # Production
npx prisma db push         # Prototype (no migration files)

# Generate client after schema changes
npx prisma generate
```

```typescript
// Custom migration with data
// prisma/migrations/xxx_add_slug/migration.sql
-- Add slug column
ALTER TABLE posts ADD COLUMN slug VARCHAR(255);

-- Populate existing posts
UPDATE posts SET slug = LOWER(REPLACE(title, ' ', '-'));

-- Make non-nullable and unique
ALTER TABLE posts ALTER COLUMN slug SET NOT NULL;
ALTER TABLE posts ADD CONSTRAINT posts_slug_unique UNIQUE (slug);
```

---

## Related Skills

- [[data-design]] - Data modeling patterns
- [[performance-optimization]] - Query optimization
- [[backend]] - Database integration

