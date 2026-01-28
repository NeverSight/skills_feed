---
name: supabase-rls
description: Supabase Row Level Security policies. Use when creating RLS policies, securing tables, or implementing multi-tenant data isolation.
---

# Supabase Row Level Security (RLS)

## Enable RLS on Table

```sql
-- Always enable RLS
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
```

## Common Policy Patterns

### User Can Only See Own Data
```sql
CREATE POLICY "Users view own data"
ON projects FOR SELECT
TO authenticated
USING (auth.uid() = user_id);
```

### User Can Insert Own Data
```sql
CREATE POLICY "Users insert own data"
ON projects FOR INSERT
TO authenticated
WITH CHECK (auth.uid() = user_id);
```

### User Can Update Own Data
```sql
CREATE POLICY "Users update own data"
ON projects FOR UPDATE
TO authenticated
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);
```

### User Can Delete Own Data
```sql
CREATE POLICY "Users delete own data"
ON projects FOR DELETE
TO authenticated
USING (auth.uid() = user_id);
```

## Multi-Tenant Patterns

### Team-Based Access
```sql
-- Users can see projects in their teams
CREATE POLICY "Team members view projects"
ON projects FOR SELECT
TO authenticated
USING (
  team_id IN (
    SELECT team_id FROM team_members
    WHERE user_id = auth.uid()
  )
);
```

### Role-Based Access
```sql
-- Check user role for admin access
CREATE POLICY "Admins can do everything"
ON projects FOR ALL
TO authenticated
USING (
  EXISTS (
    SELECT 1 FROM user_roles
    WHERE user_id = auth.uid()
    AND role = 'admin'
  )
);
```

## Service Role Bypass

For server-side operations that need to bypass RLS:

```typescript
import { createClient } from '@supabase/supabase-js';

// This bypasses RLS - use carefully!
const supabaseAdmin = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!, // Not ANON key!
  { auth: { persistSession: false } }
);
```

## Testing Policies

```sql
-- Test as specific user
SET request.jwt.claim.sub = 'user-uuid-here';

-- Run query and check results
SELECT * FROM projects;

-- Reset
RESET request.jwt.claim.sub;
```

## Security Checklist
- [ ] RLS enabled on all tables with user data
- [ ] Service role key only on server, never client
- [ ] Policies cover all operations (SELECT, INSERT, UPDATE, DELETE)
- [ ] No policies use functions that could be exploited
- [ ] Test policies with different user roles
