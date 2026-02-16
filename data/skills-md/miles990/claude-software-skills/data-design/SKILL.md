---
name: data-design
description: Data modeling, schema design, and data architecture
domain: software-design
version: 1.0.0
tags: [data-modeling, schema, normalization, denormalization, etl, data-governance]
triggers:
  keywords:
    primary: [data model, schema design, erd, entity relationship, data architecture]
    secondary: [normalization, denormalization, etl, data warehouse, data lake, olap]
  context_boost: [database, analytics, backend, enterprise]
  context_penalty: [frontend, ui, mobile]
  priority: high
---

# Data Design

## Overview

Principles for designing data structures, schemas, and data flows that are efficient, maintainable, and scalable.

---

## Data Modeling

### Entity-Relationship Diagrams

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│    User     │       │    Order    │       │   Product   │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id (PK)     │──┐    │ id (PK)     │    ┌──│ id (PK)     │
│ email       │  │    │ user_id(FK) │←───┘  │ name        │
│ name        │  └───→│ status      │       │ price       │
│ created_at  │       │ total       │       │ stock       │
└─────────────┘       │ created_at  │       └─────────────┘
                      └─────────────┘              │
                             │                     │
                      ┌──────┴──────┐              │
                      ↓             ↓              │
               ┌─────────────┐                     │
               │ OrderItem   │                     │
               ├─────────────┤                     │
               │ id (PK)     │                     │
               │ order_id(FK)│                     │
               │ product_id  │─────────────────────┘
               │ quantity    │
               │ price       │
               └─────────────┘
```

### Relationship Types

| Type | Description | Example |
|------|-------------|---------|
| 1:1 | One to one | User ↔ Profile |
| 1:N | One to many | User → Orders |
| M:N | Many to many | Students ↔ Courses |

```sql
-- 1:1 (profile extends user)
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE
);

CREATE TABLE profiles (
  user_id INTEGER PRIMARY KEY REFERENCES users(id),
  bio TEXT,
  avatar_url VARCHAR(255)
);

-- 1:N (user has many orders)
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  total DECIMAL(10,2)
);

-- M:N (students ↔ courses via junction table)
CREATE TABLE enrollments (
  student_id INTEGER REFERENCES students(id),
  course_id INTEGER REFERENCES courses(id),
  enrolled_at TIMESTAMP DEFAULT NOW(),
  PRIMARY KEY (student_id, course_id)
);
```

---

## Normalization

### Normal Forms

| Form | Rule | Example Violation |
|------|------|-------------------|
| 1NF | Atomic values, no repeating groups | `tags: "a,b,c"` |
| 2NF | 1NF + no partial dependencies | Non-key depends on part of composite key |
| 3NF | 2NF + no transitive dependencies | `zip → city` in orders table |
| BCNF | Every determinant is a candidate key | Rare edge cases |

```sql
-- ❌ Violates 1NF (non-atomic)
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  tags VARCHAR(255)  -- "electronics,sale,featured"
);

-- ✅ 1NF compliant
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255)
);

CREATE TABLE product_tags (
  product_id INTEGER REFERENCES products(id),
  tag VARCHAR(50),
  PRIMARY KEY (product_id, tag)
);

-- ❌ Violates 3NF (transitive dependency)
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  customer_zip VARCHAR(10),
  customer_city VARCHAR(100)  -- Depends on zip, not order
);

-- ✅ 3NF compliant
CREATE TABLE customers (
  id SERIAL PRIMARY KEY,
  zip VARCHAR(10),
  city VARCHAR(100)
);

CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  customer_id INTEGER REFERENCES customers(id)
);
```

---

## Denormalization

### When to Denormalize

```
Normalize for:
✅ Write-heavy workloads
✅ Data integrity requirements
✅ Storage efficiency
✅ Flexibility in queries

Denormalize for:
✅ Read-heavy workloads
✅ Complex joins hurting performance
✅ Reporting/analytics
✅ Known access patterns
```

### Denormalization Patterns

```sql
-- Computed columns
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  items JSONB,
  item_count INTEGER GENERATED ALWAYS AS (jsonb_array_length(items)) STORED,
  total DECIMAL(10,2)
);

-- Duplicated data for read performance
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  author_id INTEGER REFERENCES users(id),
  author_name VARCHAR(100),  -- Duplicated from users
  author_avatar VARCHAR(255), -- Duplicated from users
  content TEXT
);

-- Materialized view for complex queries
CREATE MATERIALIZED VIEW monthly_sales AS
SELECT
  DATE_TRUNC('month', created_at) as month,
  product_id,
  SUM(quantity) as units_sold,
  SUM(total) as revenue
FROM order_items
GROUP BY 1, 2;

-- Refresh periodically
REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_sales;
```

---

## Schema Design Patterns

### Soft Deletes

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255),
  deleted_at TIMESTAMP NULL,
  -- Partial unique index
  CONSTRAINT unique_active_email UNIQUE (email) WHERE deleted_at IS NULL
);

-- Query active users only
SELECT * FROM users WHERE deleted_at IS NULL;
```

### Audit Trail

```sql
CREATE TABLE audit_log (
  id SERIAL PRIMARY KEY,
  table_name VARCHAR(100),
  record_id INTEGER,
  action VARCHAR(10),  -- INSERT, UPDATE, DELETE
  old_data JSONB,
  new_data JSONB,
  changed_by INTEGER REFERENCES users(id),
  changed_at TIMESTAMP DEFAULT NOW()
);

-- Trigger for automatic auditing
CREATE OR REPLACE FUNCTION audit_trigger()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO audit_log (table_name, record_id, action, old_data, new_data, changed_by)
  VALUES (
    TG_TABLE_NAME,
    COALESCE(NEW.id, OLD.id),
    TG_OP,
    CASE WHEN TG_OP != 'INSERT' THEN to_jsonb(OLD) END,
    CASE WHEN TG_OP != 'DELETE' THEN to_jsonb(NEW) END,
    current_setting('app.user_id', true)::INTEGER
  );
  RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;
```

### Multi-Tenancy

```sql
-- Row-level security
CREATE TABLE organizations (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255)
);

CREATE TABLE projects (
  id SERIAL PRIMARY KEY,
  org_id INTEGER REFERENCES organizations(id),
  name VARCHAR(255)
);

-- Enable RLS
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

CREATE POLICY org_isolation ON projects
  USING (org_id = current_setting('app.org_id')::INTEGER);

-- Set org context per request
SET app.org_id = 123;
SELECT * FROM projects; -- Only sees org 123's projects
```

### Versioning / History

```sql
-- Version table pattern
CREATE TABLE documents (
  id SERIAL PRIMARY KEY,
  current_version_id INTEGER
);

CREATE TABLE document_versions (
  id SERIAL PRIMARY KEY,
  document_id INTEGER REFERENCES documents(id),
  version INTEGER,
  content TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  created_by INTEGER REFERENCES users(id),
  UNIQUE (document_id, version)
);

-- Temporal tables (PostgreSQL)
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  price DECIMAL(10,2),
  valid_from TIMESTAMP DEFAULT NOW(),
  valid_to TIMESTAMP DEFAULT 'infinity'
);

-- Query historical state
SELECT * FROM products
WHERE valid_from <= '2024-01-01' AND valid_to > '2024-01-01';
```

---

## NoSQL Schema Design

### Document Store (MongoDB)

```javascript
// Embedded vs Referenced

// ✅ Embed when: data is accessed together, 1:few relationship
{
  _id: ObjectId("..."),
  title: "Blog Post",
  author: {
    name: "John",
    email: "john@example.com"
  },
  comments: [
    { user: "Jane", text: "Great post!", date: ISODate("...") }
  ]
}

// ✅ Reference when: data is accessed independently, 1:many or M:N
{
  _id: ObjectId("..."),
  title: "Blog Post",
  authorId: ObjectId("..."),  // Reference to users collection
  commentIds: [ObjectId("..."), ObjectId("...")]
}

// ❌ Anti-pattern: Unbounded arrays
{
  _id: ObjectId("..."),
  logs: [...] // Can grow to millions, hits 16MB limit
}

// ✅ Better: Bucket pattern
{
  _id: ObjectId("..."),
  sensorId: "sensor-123",
  date: ISODate("2024-01-15"),
  readings: [...] // Max ~1000 per document
}
```

### Key-Value Store (Redis)

```python
# Naming conventions
user:123              # User object
user:123:sessions     # User's sessions (set)
user:123:orders       # User's orders (list)
order:456             # Order object
orders:pending        # Queue of pending orders (list)
products:category:electronics  # Products in category (set)

# Expiration patterns
session:{token}       # Expires after 30 min
rate_limit:ip:1.2.3.4 # Expires after 1 min
cache:api:/users/123  # Expires after 5 min
```

---

## Data Pipeline Design

### ETL vs ELT

```
ETL (Extract, Transform, Load):
Source → Transform (external) → Data Warehouse
Use: Traditional, when transformation is complex

ELT (Extract, Load, Transform):
Source → Data Lake/Warehouse → Transform (in-place)
Use: Modern, leverages warehouse compute power
```

### Event Sourcing

```typescript
// Events are the source of truth
interface Event {
  id: string;
  aggregateId: string;
  type: string;
  payload: unknown;
  timestamp: Date;
  version: number;
}

// Event store
class EventStore {
  async append(aggregateId: string, events: Event[]) {
    await db.events.insertMany(events);
  }

  async getEvents(aggregateId: string): Promise<Event[]> {
    return db.events
      .find({ aggregateId })
      .sort({ version: 1 })
      .toArray();
  }
}

// Rebuild state from events
function rebuildAccount(events: Event[]): Account {
  return events.reduce((account, event) => {
    switch (event.type) {
      case 'AccountOpened':
        return { balance: 0, ...event.payload };
      case 'MoneyDeposited':
        return { ...account, balance: account.balance + event.payload.amount };
      case 'MoneyWithdrawn':
        return { ...account, balance: account.balance - event.payload.amount };
      default:
        return account;
    }
  }, {} as Account);
}
```

---

## Data Governance

### Data Quality Dimensions

| Dimension | Description | Example Check |
|-----------|-------------|---------------|
| Accuracy | Correct values | Email format validation |
| Completeness | No missing data | Required fields present |
| Consistency | Same across systems | User ID matches in all tables |
| Timeliness | Up to date | Last updated within 24h |
| Uniqueness | No duplicates | Unique email per user |

### Schema Evolution

```sql
-- Safe migrations

-- ✅ Adding nullable column
ALTER TABLE users ADD COLUMN phone VARCHAR(20) NULL;

-- ✅ Adding column with default
ALTER TABLE users ADD COLUMN status VARCHAR(20) DEFAULT 'active';

-- ⚠️ Making column non-null (multi-step)
-- Step 1: Add with default
ALTER TABLE users ADD COLUMN verified BOOLEAN DEFAULT false;
-- Step 2: Backfill data
UPDATE users SET verified = true WHERE email_verified_at IS NOT NULL;
-- Step 3: Add constraint
ALTER TABLE users ALTER COLUMN verified SET NOT NULL;

-- ❌ Dangerous: Renaming column
-- Instead: Add new, migrate data, remove old (over multiple deploys)
```

---

## Related Skills

- [[database]] - Database implementation
- [[architecture-patterns]] - Data architecture patterns
- [[api-design]] - Data in APIs
