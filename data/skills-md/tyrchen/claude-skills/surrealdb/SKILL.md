---
name: surrealdb
description: Write production-ready SurrealDB queries and operations using SurrealQL. Use when users need to create schemas, write CRUD queries, model graph relationships, build authentication systems, optimize performance, or work with SurrealDB in any capacity.
---

# SurrealDB - Production-Ready Query Generator

Generate solid, high-quality, production-ready SurrealDB queries and operations using SurrealQL for multi-model database applications including document, graph, and relational patterns.

## When to Use This Skill

Use this skill when the user wants to:

- **Write SurrealQL queries** (SELECT, CREATE, UPDATE, DELETE, UPSERT)
- **Design database schemas** (SCHEMAFULL/SCHEMALESS tables, field definitions)
- **Model relationships** (record links, graph edges with RELATE, nested data)
- **Implement authentication** (DEFINE ACCESS, SCOPE, permissions, RBAC)
- **Create indexes** for performance optimization
- **Write custom functions** using DEFINE FUNCTION
- **Build real-time applications** with LIVE queries
- **Implement transactions** for data consistency
- **Migrate from SQL/NoSQL** to SurrealDB
- **Debug or optimize existing SurrealQL**

## SurrealQL Quick Reference

### Core Statement Syntax

```sql
-- SELECT with graph traversal
SELECT *, ->friends->person AS mutual_friends FROM person:alice;

-- CREATE with specific ID
CREATE person:john SET name = 'John', age = 30;

-- UPDATE with operators
UPDATE person SET age += 1, tags += 'senior' WHERE age >= 65;

-- DELETE with conditions
DELETE person WHERE active = false;

-- UPSERT (create if not exists, update if exists)
UPSERT user:email@example.com SET email = 'email@example.com', visits += 1;

-- RELATE for graph edges
RELATE person:alice->follows->person:bob SET since = time::now();
```

### Data Types

```sql
-- Basic types
string, int, float, bool, datetime, duration, decimal, uuid

-- Complex types
array, object, record<table>, option<type>

-- Special types
geometry (point, line, polygon), bytes, null, none
```

### Essential Functions

```sql
-- Time functions
time::now()                    -- Current timestamp
time::floor(datetime, 1d)      -- Floor to day
duration::from::days(7)        -- Create duration

-- String functions
string::is::email($value)      -- Validate email
string::concat($a, ' ', $b)    -- Concatenate
string::split($s, ',')         -- Split to array
string::lowercase($s)          -- Lowercase

-- Array functions
array::len($arr)               -- Array length
array::push($arr, $item)       -- Add to array
array::distinct($arr)          -- Remove duplicates
array::flatten($arr)           -- Flatten nested arrays

-- Crypto functions
crypto::argon2::generate($password)           -- Hash password
crypto::argon2::compare($hash, $password)     -- Verify password

-- Math functions
math::sum($arr)                -- Sum values
math::mean($arr)               -- Average
math::max($arr)                -- Maximum

-- Record functions
record::id($record)            -- Get record ID
record::table($record)         -- Get table name

-- Type functions
type::is::string($val)         -- Type check
type::thing($table, $id)       -- Create record ID
```

## Instructions for Writing SurrealDB Queries

### Step 1: Understand the Data Model

Before writing any SurrealQL:

1. **What is the data structure?** (Document, graph, relational, or hybrid?)
2. **What relationships exist?** (One-to-many, many-to-many, graph traversals?)
3. **What access patterns?** (Read-heavy, write-heavy, real-time?)
4. **What consistency requirements?** (Eventual, strong, transactional?)

### Step 2: Choose Schema Strategy

**SCHEMAFULL** - Use when:
- Data structure is well-defined
- Type safety is critical
- Validation rules are needed
- Production workloads

**SCHEMALESS** - Use when:
- Rapid prototyping
- Evolving data structures
- Flexible document storage

```sql
-- SCHEMAFULL with validation
DEFINE TABLE user SCHEMAFULL;
DEFINE FIELD email ON user TYPE string ASSERT string::is::email($value);
DEFINE FIELD password ON user TYPE string;
DEFINE FIELD created_at ON user TYPE datetime DEFAULT time::now();
DEFINE FIELD status ON user TYPE string DEFAULT 'active'
    ASSERT $value IN ['active', 'inactive', 'suspended'];

-- SCHEMALESS (flexible)
DEFINE TABLE event SCHEMALESS;
```

### Step 3: Design Relationships

Choose the right relationship model:

**Record Links** - Simple, direct references:
```sql
-- One-to-many via array of record IDs
CREATE user:alice SET
    name = 'Alice',
    friends = [user:bob, user:carol];

-- Fetch with link resolution
SELECT *, friends.* FROM user:alice;
```

**Graph Edges (RELATE)** - Complex relationships with metadata:
```sql
-- Create relationship with properties
RELATE user:alice->follows->user:bob SET
    since = time::now(),
    notifications = true;

-- Traverse graph
SELECT
    ->follows->user AS following,
    <-follows<-user AS followers
FROM user:alice;

-- Multi-hop traversal
SELECT ->follows->user->follows->user AS friends_of_friends
FROM user:alice;
```

**Embedded Documents** - Denormalized data:
```sql
CREATE order SET
    customer = { name: 'Alice', email: 'alice@example.com' },
    items = [
        { product: 'Widget', quantity: 2, price: 29.99 },
        { product: 'Gadget', quantity: 1, price: 49.99 }
    ],
    total = 109.97;
```

### Step 4: Implement Authentication

**Record-Level Access with DEFINE ACCESS:**
```sql
-- Define user access
DEFINE ACCESS user_auth ON DATABASE TYPE RECORD
    SIGNUP (
        CREATE user SET
            email = $email,
            password = crypto::argon2::generate($password),
            created_at = time::now()
    )
    SIGNIN (
        SELECT * FROM user
        WHERE email = $email
        AND crypto::argon2::compare(password, $password)
    )
    DURATION FOR TOKEN 24h, FOR SESSION 7d;

-- Define table permissions
DEFINE TABLE post SCHEMAFULL
    PERMISSIONS
        FOR select WHERE published = true OR author = $auth.id
        FOR create WHERE $auth.id != NONE
        FOR update WHERE author = $auth.id
        FOR delete WHERE author = $auth.id;
```

### Step 5: Optimize with Indexes

```sql
-- Unique index
DEFINE INDEX unique_email ON user FIELDS email UNIQUE;

-- Composite index
DEFINE INDEX order_lookup ON order FIELDS customer, status;

-- Full-text search index
DEFINE ANALYZER english TOKENIZERS blank FILTERS lowercase, snowball(english);
DEFINE INDEX content_search ON article FIELDS content
    SEARCH ANALYZER english BM25;

-- Verify index usage
EXPLAIN SELECT * FROM user WHERE email = 'test@example.com';
```

### Step 6: Write Transactions

```sql
BEGIN TRANSACTION;

-- Transfer funds between accounts
LET $amount = 100;
UPDATE account:alice SET balance -= $amount;
UPDATE account:bob SET balance += $amount;
CREATE transaction SET
    from = account:alice,
    to = account:bob,
    amount = $amount,
    timestamp = time::now();

COMMIT TRANSACTION;
```

## Common Query Patterns

### CRUD Operations

**Create with validation:**
```sql
CREATE user CONTENT {
    email: 'user@example.com',
    name: 'John Doe',
    roles: ['user'],
    metadata: {
        source: 'signup',
        ip: '192.168.1.1'
    }
};
```

**Select with filtering and pagination:**
```sql
SELECT * FROM user
WHERE status = 'active'
    AND created_at > time::now() - 30d
ORDER BY created_at DESC
LIMIT 20
START 0;
```

**Update with operators:**
```sql
-- Increment/decrement
UPDATE user:alice SET login_count += 1;

-- Array manipulation
UPDATE user:alice SET tags += 'premium', tags -= 'trial';

-- Conditional update
UPDATE user SET status = 'inactive'
WHERE last_login < time::now() - 90d;
```

**Upsert pattern:**
```sql
UPSERT user:email@example.com SET
    email = 'email@example.com',
    last_seen = time::now(),
    visits += 1;
```

### Graph Queries

**Social network - friends of friends:**
```sql
SELECT
    id,
    name,
    array::distinct(->follows->user->follows->user) AS suggested_friends
FROM user:alice
WHERE suggested_friends != user:alice;
```

**E-commerce - product recommendations:**
```sql
-- Find products bought by users who bought this product
SELECT
    <-purchased<-user->purchased->product AS related_products,
    count() AS frequency
FROM product:widget123
GROUP BY related_products
ORDER BY frequency DESC
LIMIT 10;
```

**Knowledge graph - recursive traversal:**
```sql
-- Find all ancestors up to 5 levels
SELECT
    ->parent->(1..5)->category AS ancestors
FROM category:electronics;
```

### Analytics Queries

**Aggregations:**
```sql
SELECT
    status,
    count() AS total,
    math::mean(age) AS avg_age,
    math::min(created_at) AS first_created
FROM user
GROUP BY status;
```

**Time-series analysis:**
```sql
SELECT
    time::floor(timestamp, 1h) AS hour,
    count() AS events,
    math::sum(value) AS total_value
FROM metrics
WHERE timestamp > time::now() - 24h
GROUP BY hour
ORDER BY hour;
```

### Subqueries and Computed Fields

**Subquery in SELECT:**
```sql
SELECT
    *,
    (SELECT count() FROM post WHERE author = $parent.id) AS post_count,
    (SELECT VALUE title FROM post WHERE author = $parent.id LIMIT 5) AS recent_posts
FROM user;
```

**LET for complex queries (CTE alternative):**
```sql
LET $active_users = (SELECT id FROM user WHERE status = 'active');
LET $recent_orders = (SELECT * FROM order WHERE created_at > time::now() - 7d);

SELECT * FROM $recent_orders
WHERE customer IN $active_users.id;
```

## Schema Design Patterns

### User Profile with Nested Objects

```sql
DEFINE TABLE user SCHEMAFULL;
DEFINE FIELD email ON user TYPE string ASSERT string::is::email($value);
DEFINE FIELD password ON user TYPE string;
DEFINE FIELD profile ON user TYPE object;
DEFINE FIELD profile.name ON user TYPE string;
DEFINE FIELD profile.avatar ON user TYPE option<string>;
DEFINE FIELD profile.bio ON user TYPE option<string>;
DEFINE FIELD settings ON user TYPE object DEFAULT {};
DEFINE FIELD settings.notifications ON user TYPE bool DEFAULT true;
DEFINE FIELD settings.theme ON user TYPE string DEFAULT 'light';
DEFINE FIELD created_at ON user TYPE datetime DEFAULT time::now();
DEFINE FIELD updated_at ON user TYPE datetime VALUE time::now();

DEFINE INDEX unique_email ON user FIELDS email UNIQUE;
```

### E-commerce Schema

```sql
-- Products
DEFINE TABLE product SCHEMAFULL;
DEFINE FIELD name ON product TYPE string;
DEFINE FIELD description ON product TYPE string;
DEFINE FIELD price ON product TYPE decimal;
DEFINE FIELD inventory ON product TYPE int DEFAULT 0;
DEFINE FIELD categories ON product TYPE array<record<category>>;
DEFINE FIELD active ON product TYPE bool DEFAULT true;

DEFINE INDEX product_search ON product FIELDS name, description
    SEARCH ANALYZER blank BM25;

-- Orders
DEFINE TABLE order SCHEMAFULL;
DEFINE FIELD customer ON order TYPE record<user>;
DEFINE FIELD items ON order TYPE array;
DEFINE FIELD items.*.product ON order TYPE record<product>;
DEFINE FIELD items.*.quantity ON order TYPE int;
DEFINE FIELD items.*.price ON order TYPE decimal;
DEFINE FIELD status ON order TYPE string DEFAULT 'pending'
    ASSERT $value IN ['pending', 'processing', 'shipped', 'delivered', 'cancelled'];
DEFINE FIELD total ON order TYPE decimal;
DEFINE FIELD created_at ON order TYPE datetime DEFAULT time::now();

DEFINE INDEX order_customer ON order FIELDS customer;
DEFINE INDEX order_status ON order FIELDS status, created_at;
```

### Graph Relationship Schema

```sql
-- Define edge table
DEFINE TABLE follows SCHEMAFULL TYPE RELATION;
DEFINE FIELD in ON follows TYPE record<user>;
DEFINE FIELD out ON follows TYPE record<user>;
DEFINE FIELD since ON follows TYPE datetime DEFAULT time::now();
DEFINE FIELD notifications ON follows TYPE bool DEFAULT true;

-- Prevent duplicate follows
DEFINE INDEX unique_follow ON follows FIELDS in, out UNIQUE;
```

## Custom Functions

```sql
-- Calculate user engagement score
DEFINE FUNCTION fn::engagement_score($user_id: record<user>) {
    LET $posts = (SELECT count() FROM post WHERE author = $user_id);
    LET $comments = (SELECT count() FROM comment WHERE author = $user_id);
    LET $likes_received = (SELECT count() FROM like WHERE post.author = $user_id);

    RETURN ($posts * 5) + ($comments * 2) + $likes_received;
};

-- Usage
SELECT *, fn::engagement_score(id) AS score FROM user;

-- Validate and normalize email
DEFINE FUNCTION fn::normalize_email($email: string) {
    IF !string::is::email($email) {
        THROW "Invalid email format";
    };
    RETURN string::lowercase(string::trim($email));
};

-- Pagination helper
DEFINE FUNCTION fn::paginate($table: string, $page: int, $per_page: int) {
    LET $offset = ($page - 1) * $per_page;
    RETURN (SELECT * FROM type::table($table) LIMIT $per_page START $offset);
};
```

## Real-Time (LIVE Queries)

```sql
-- Subscribe to changes on a table
LIVE SELECT * FROM post WHERE published = true;

-- Subscribe to specific record changes
LIVE SELECT * FROM user:alice;

-- Subscribe with graph traversal
LIVE SELECT *, ->comments->comment AS comments FROM post;

-- Kill a live query
KILL $live_query_id;
```

## Performance Best Practices

### 1. Use Specific Record IDs Instead of Scans

```sql
-- FAST: Direct ID access
SELECT * FROM user:alice;

-- SLOW: Table scan
SELECT * FROM user WHERE id = 'alice';
```

### 2. Select Only Needed Fields

```sql
-- BETTER: Specific fields
SELECT name, email FROM user;

-- AVOID: All fields when not needed
SELECT * FROM user;
```

### 3. Use Indexes Effectively

```sql
-- Create index for common queries
DEFINE INDEX active_users ON user FIELDS status, created_at;

-- Query uses index
SELECT * FROM user
WHERE status = 'active'
ORDER BY created_at DESC;
```

### 4. Batch Operations

```sql
-- BETTER: Single batch insert
INSERT INTO log [
    { level: 'info', message: 'Start' },
    { level: 'info', message: 'Processing' },
    { level: 'info', message: 'Complete' }
];

-- AVOID: Multiple separate inserts
```

### 5. Use Transactions for Related Operations

```sql
BEGIN TRANSACTION;
-- Multiple related operations
COMMIT TRANSACTION;
```

## Common Anti-patterns to Avoid

### 1. Missing Field Existence Checks

```sql
-- WRONG: Field might not exist
SELECT * FROM user WHERE profile.name = 'John';

-- CORRECT: Check existence first (in application logic)
-- Or use SCHEMAFULL tables with proper defaults
```

### 2. N+1 Query Problem

```sql
-- WRONG: Fetching related data in loops
-- (in application: for each user, fetch their posts)

-- CORRECT: Use record links and fetch in one query
SELECT *, posts.* FROM user FETCH posts;
```

### 3. Not Using Appropriate Relationship Model

```sql
-- WRONG: String IDs for relationships
CREATE user SET friend_ids = ['alice', 'bob'];

-- CORRECT: Record links
CREATE user SET friends = [user:alice, user:bob];
```

### 4. Over-fetching with Graph Traversals

```sql
-- WRONG: Unbounded traversal
SELECT ->*->* FROM user:alice;

-- CORRECT: Bounded traversal
SELECT ->(1..3)->follows->user FROM user:alice;
```

## Debugging and Testing

### Explain Query Execution

```sql
EXPLAIN SELECT * FROM user WHERE email = 'test@example.com';
EXPLAIN FULL SELECT * FROM user WHERE email = 'test@example.com';
```

### Check Table Info

```sql
INFO FOR TABLE user;
INFO FOR DB;
INFO FOR NS;
```

### Test Queries with Parameters

```sql
LET $email = 'test@example.com';
SELECT * FROM user WHERE email = $email;
```

## Output Format

When generating SurrealDB queries, always provide:

1. **Complete SurrealQL statements** with proper syntax
2. **Schema definitions** when creating tables/fields
3. **Index recommendations** for query patterns
4. **Example data** for testing
5. **Explanation** of design decisions
6. **Performance considerations** if relevant

## Reference Files

- **[SurrealQL Syntax Reference](./references/surrealql_syntax.md)** - Complete language reference
- **[Schema Patterns](./references/schema_patterns.md)** - Common schema designs
- **[Graph Relationships](./references/graph_relationships.md)** - Relationship modeling patterns
- **[Security & Auth](./references/security_auth.md)** - Authentication and permissions

## Version Compatibility

- **SurrealDB 2.x**: Latest features, GraphQL support, improved performance
- **SurrealDB 1.x**: Legacy version, use `scope` instead of `access`

Always verify target SurrealDB version before generating queries.
