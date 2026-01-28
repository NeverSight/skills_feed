---
name: postgres-schema-patterns
description: Production-ready PostgreSQL schema patterns for building apps - social features, e-commerce, SaaS, and more. Use when designing databases, building any app with PostgreSQL, or implementing Row Level Security.
license: MIT
metadata:
  author: InsForge
  version: "1.0.0"
---

# PostgreSQL Schema Patterns

Community-maintained schema patterns for building modern applications with PostgreSQL. Contributed by [InsForge](https://insforge.dev).

Each pattern includes schema design, Row Level Security policies, SDK examples, and performance best practices. Works with any PostgREST-based backend.

## When to Use This Skill

Reference these patterns when:
- Designing database schemas for common app features
- Implementing Row Level Security (RLS) policies
- Writing PostgREST/SDK queries with relationships
- Optimizing queries for PostgREST

## Available Patterns

| Pattern | Use Case | Complexity |
|---------|----------|------------|
| [Social Graph](patterns/social-graph.md) | Follows, connections, networks | Medium |
| [Likes](patterns/likes.md) | Likes, favorites, bookmarks | Simple |
| [Nested Comments](patterns/nested-comments.md) | Threaded comments, replies | Medium |
| [Multi-Tenant](patterns/multi-tenant.md) | Organizations, workspaces, SaaS | Advanced |

## Pattern Structure

Each pattern file includes:
- **Schema** - Table definitions with constraints and indexes
- **Row Level Security** - RLS policies for secure access
- **SDK Usage** - Common query patterns (PostgREST-compatible)
- **Best Practices** - Indexing, performance, and optimization tips
- **Common Mistakes** - Pitfalls to avoid

## Quick Reference

### SDK Query Patterns

```javascript
// Foreign key expansion (get related data)
.select('*, author:user_id(id, profile)')

// Count aggregation
.select('*, likes(count)')

// Inner join (filter by related table)
.select('*, likes!inner(id)')
.eq('likes.user_id', currentUserId)

// Check existence without fetching
.select('id')
.single();
const exists = !!data;

// Count without fetching rows
.select('*', { count: 'exact', head: true })
```

### Essential SQL Patterns

```sql
-- Always index foreign keys
CREATE INDEX idx_table_fk ON table(foreign_key_column);

-- Prevent duplicates in junction tables
UNIQUE(user_id, post_id)

-- Self-referential (nested structures)
parent_id UUID REFERENCES same_table(id) ON DELETE CASCADE

-- Cascade deletes for cleanup
REFERENCES parent(id) ON DELETE CASCADE

-- Role-based checks
CHECK (role IN ('owner', 'admin', 'member'))
```

### RLS Essentials

```sql
-- Enable RLS
ALTER TABLE mytable ENABLE ROW LEVEL SECURITY;

-- Public read
CREATE POLICY "Anyone can read" ON mytable
  FOR SELECT USING (true);

-- Owner-only write
CREATE POLICY "Owner can modify" ON mytable
  FOR ALL
  TO authenticated
  USING (uid() = user_id)
  WITH CHECK (uid() = user_id);

-- Use functions for complex checks (better performance)
CREATE FUNCTION is_member(org_id UUID) RETURNS BOOLEAN AS $$
  SELECT EXISTS (SELECT 1 FROM members WHERE organization_id = org_id AND user_id = uid());
$$ LANGUAGE sql SECURITY DEFINER;
```

## About

This skill focuses on **schema design patterns** - how to model common app features in PostgreSQL. Each pattern includes embedded performance tips and best practices.

Maintained by the InsForge team as a contribution to the developer community. PRs welcome!
