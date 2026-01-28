---
name: supabase-database
description: Supabase database operations including queries, CRUD operations, RLS policies, and PostgreSQL functions. Use when querying tables, managing data, implementing RLS, or writing database functions.
---

# Supabase Database Skill

Database operations, queries, and Row Level Security.

## Quick Reference

| Operation | JavaScript | SQL |
|-----------|------------|-----|
| Select all | `supabase.from('table').select('*')` | `SELECT * FROM table` |
| Select columns | `supabase.from('table').select('col1,col2')` | `SELECT col1, col2 FROM table` |
| Filter | `.eq('col', 'value')` | `WHERE col = 'value'` |
| Insert | `.insert({ col: 'value' })` | `INSERT INTO table (col) VALUES ('value')` |
| Update | `.update({ col: 'value' }).eq('id', 1)` | `UPDATE table SET col = 'value' WHERE id = 1` |
| Delete | `.delete().eq('id', 1)` | `DELETE FROM table WHERE id = 1` |

## Basic Queries

### Select

```javascript
// All rows
const { data, error } = await supabase
  .from('users')
  .select('*')

// Specific columns
const { data, error } = await supabase
  .from('users')
  .select('id, name, email')

// With count
const { data, count, error } = await supabase
  .from('users')
  .select('*', { count: 'exact' })
```

### Insert

```javascript
// Single row
const { data, error } = await supabase
  .from('users')
  .insert({ name: 'John', email: 'john@example.com' })
  .select()

// Multiple rows
const { data, error } = await supabase
  .from('users')
  .insert([
    { name: 'John', email: 'john@example.com' },
    { name: 'Jane', email: 'jane@example.com' }
  ])
  .select()
```

### Update

```javascript
const { data, error } = await supabase
  .from('users')
  .update({ name: 'John Doe' })
  .eq('id', 1)
  .select()
```

### Upsert

```javascript
const { data, error } = await supabase
  .from('users')
  .upsert({ id: 1, name: 'John', email: 'john@example.com' })
  .select()
```

### Delete

```javascript
const { error } = await supabase
  .from('users')
  .delete()
  .eq('id', 1)
```

## Filters

### Comparison Operators

```javascript
// Equal
.eq('col', 'value')

// Not equal
.neq('col', 'value')

// Greater than
.gt('col', 10)

// Greater or equal
.gte('col', 10)

// Less than
.lt('col', 10)

// Less or equal
.lte('col', 10)
```

### Pattern Matching

```javascript
// LIKE (case sensitive)
.like('name', '%John%')

// ILIKE (case insensitive)
.ilike('name', '%john%')
```

### List Operations

```javascript
// IN array
.in('status', ['active', 'pending'])

// Contains (array column contains value)
.contains('tags', ['sports', 'news'])

// Contained by (value contained by array column)
.containedBy('tags', ['sports', 'news', 'tech'])

// Overlaps (any match)
.overlaps('tags', ['sports', 'tech'])
```

### Range Operations

```javascript
// Between (exclusive)
.range('price', 10, 100)

// In range type column
.rangeGt('date_range', '2025-01-01')
.rangeLt('date_range', '2025-12-31')
```

### Null Checks

```javascript
// Is null
.is('deleted_at', null)

// Is not null
.not('deleted_at', 'is', null)
```

### Boolean Operators

```javascript
// AND (chain filters)
.eq('status', 'active')
.eq('verified', true)

// OR
.or('status.eq.active,status.eq.pending')

// NOT
.not('status', 'eq', 'deleted')
```

## Ordering & Pagination

```javascript
// Order by
const { data } = await supabase
  .from('posts')
  .select('*')
  .order('created_at', { ascending: false })

// Multiple order
.order('category', { ascending: true })
.order('created_at', { ascending: false })

// Limit
.limit(10)

// Range (pagination)
.range(0, 9)  // First 10 rows

// Single row
.single()

// Maybe single (0 or 1)
.maybeSingle()
```

## Relations (Joins)

### One-to-Many

```javascript
// Users with their posts
const { data } = await supabase
  .from('users')
  .select(`
    id,
    name,
    posts (
      id,
      title,
      content
    )
  `)
```

### Many-to-One

```javascript
// Posts with author
const { data } = await supabase
  .from('posts')
  .select(`
    id,
    title,
    users (
      id,
      name
    )
  `)
```

### Inner Join

```javascript
// Only users with posts
const { data } = await supabase
  .from('users')
  .select(`
    id,
    name,
    posts!inner (
      id,
      title
    )
  `)
```

### Many-to-Many

```javascript
// Posts with tags through junction table
const { data } = await supabase
  .from('posts')
  .select(`
    id,
    title,
    post_tags (
      tags (
        id,
        name
      )
    )
  `)
```

## Row Level Security (RLS)

### Enable RLS

```sql
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
```

### Basic Policies

```sql
-- Users can read their own data
CREATE POLICY "Users can view own data"
ON users FOR SELECT
TO authenticated
USING (auth.uid() = id);

-- Users can insert their own data
CREATE POLICY "Users can insert own data"
ON users FOR INSERT
TO authenticated
WITH CHECK (auth.uid() = id);

-- Users can update their own data
CREATE POLICY "Users can update own data"
ON users FOR UPDATE
TO authenticated
USING (auth.uid() = id)
WITH CHECK (auth.uid() = id);

-- Users can delete their own data
CREATE POLICY "Users can delete own data"
ON users FOR DELETE
TO authenticated
USING (auth.uid() = id);
```

### Helper Functions

```sql
-- Current user ID
auth.uid()

-- Current user role (anon, authenticated, service_role)
auth.role()

-- Full JWT as JSON
auth.jwt()

-- Check specific JWT claim
auth.jwt()->>'email'
auth.jwt()->'app_metadata'->>'role'
```

### Performance Optimization

```sql
-- Wrap auth functions in SELECT for performance
CREATE POLICY "Fast policy"
ON users FOR SELECT
TO authenticated
USING ((SELECT auth.uid()) = user_id);

-- Add indexes for RLS columns
CREATE INDEX idx_posts_user_id ON posts(user_id);
```

## RPC (Remote Procedure Call)

### Define Function

```sql
CREATE OR REPLACE FUNCTION search_users(query text)
RETURNS TABLE(id uuid, name text, email text)
LANGUAGE sql STABLE
AS $$
  SELECT id, name, email
  FROM users
  WHERE name ILIKE '%' || query || '%'
     OR email ILIKE '%' || query || '%'
  ORDER BY name;
$$;
```

### Call Function

```javascript
const { data, error } = await supabase
  .rpc('search_users', { query: 'john' })
```

## TypeScript Types

### Generate Types

```bash
supabase gen types typescript --local > database.types.ts
```

### Use Types

```typescript
import { Database } from './database.types'

type User = Database['public']['Tables']['users']['Row']
type NewUser = Database['public']['Tables']['users']['Insert']
type UpdateUser = Database['public']['Tables']['users']['Update']

const supabase = createClient<Database>(url, key)

const { data } = await supabase
  .from('users')
  .select('*')
// data is User[] | null
```

## References

- [rls-policies.md](references/rls-policies.md) - Complete RLS patterns
- [query-operators.md](references/query-operators.md) - All filter operators
- [postgres-functions.md](references/postgres-functions.md) - Writing SQL functions
