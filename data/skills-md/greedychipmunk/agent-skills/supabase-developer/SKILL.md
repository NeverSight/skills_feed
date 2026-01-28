---
name: supabase-developer
description: Expert Supabase development with PostgreSQL, authentication, Row Level Security, Storage, Edge Functions, and Realtime subscriptions
---

# Supabase Developer Skill

## Overview

This skill provides comprehensive expertise in building production-ready applications with **Supabase**, the open-source Firebase alternative. It covers database design, authentication, Row Level Security (RLS), file storage, Edge Functions, and real-time subscriptions.

## Core Capabilities

### Database & PostgreSQL
- **Schema Design**: Normalized tables with proper relationships and indexes
- **Migrations**: Version-controlled database changes
- **Queries**: Complex queries with joins, CTEs, and aggregations
- **Functions**: PostgreSQL stored procedures and triggers
- **Extensions**: PostGIS, pg_vector, pgcrypto, and more

### Authentication
- **Email/Password**: Traditional authentication flow
- **Magic Links**: Passwordless email authentication
- **OAuth Providers**: Google, GitHub, Discord, Twitter, and more
- **Phone Auth**: SMS-based authentication
- **Multi-Factor Authentication**: TOTP and SMS verification
- **Session Management**: JWT tokens and refresh handling

### Row Level Security (RLS)
- **Policy Design**: Secure data access patterns
- **User-based Access**: Policies tied to authenticated users
- **Role-based Access**: Custom roles and permissions
- **Organization-based**: Multi-tenant security patterns
- **Performance**: Optimized RLS with proper indexing

### Storage
- **File Uploads**: Direct and resumable uploads
- **Access Control**: Bucket policies and RLS integration
- **Transformations**: Image resizing and optimization
- **CDN**: Global content delivery
- **Signed URLs**: Temporary access tokens

### Edge Functions
- **Deno Runtime**: TypeScript/JavaScript edge computing
- **API Routes**: Custom backend logic
- **Webhooks**: Event-driven integrations
- **Scheduled Tasks**: Cron-based functions (pg_cron)
- **Third-party APIs**: External service integrations

### Realtime
- **Database Changes**: Listen to INSERT, UPDATE, DELETE
- **Broadcast**: Publish messages to channels
- **Presence**: Track online users and state
- **Postgres Changes**: Row-level change subscriptions

## Implementation Patterns

### Project Structure
```
├── supabase/
│   ├── config.toml           # Project configuration
│   ├── migrations/           # Database migrations
│   │   ├── 20240101000000_initial_schema.sql
│   │   └── 20240102000000_add_profiles.sql
│   ├── functions/            # Edge Functions
│   │   ├── hello-world/
│   │   │   └── index.ts
│   │   └── _shared/          # Shared utilities
│   │       └── cors.ts
│   └── seed.sql              # Development seed data
├── src/
│   ├── lib/
│   │   └── supabase.ts       # Client initialization
│   ├── types/
│   │   └── database.types.ts # Generated types
│   └── ...
└── package.json
```

### Database Schema Example

```sql
-- Users profile extension
create table public.profiles (
  id uuid references auth.users on delete cascade primary key,
  username text unique not null,
  full_name text,
  avatar_url text,
  created_at timestamptz default now() not null,
  updated_at timestamptz default now() not null
);

-- Enable RLS
alter table public.profiles enable row level security;

-- RLS Policies
create policy "Public profiles are viewable by everyone"
  on public.profiles for select
  using (true);

create policy "Users can update their own profile"
  on public.profiles for update
  using (auth.uid() = id);

-- Trigger for updated_at
create trigger handle_updated_at
  before update on public.profiles
  for each row execute function moddatetime(updated_at);
```

### Client Initialization

```typescript
// src/lib/supabase.ts
import { createClient } from '@supabase/supabase-js'
import type { Database } from '@/types/database.types'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient<Database>(
  supabaseUrl,
  supabaseAnonKey
)
```

### Authentication Patterns

```typescript
// Sign up with email
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'secure-password',
  options: {
    data: {
      full_name: 'John Doe'
    }
  }
})

// Sign in with OAuth
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google',
  options: {
    redirectTo: `${window.location.origin}/auth/callback`
  }
})

// Get current user
const { data: { user } } = await supabase.auth.getUser()

// Listen to auth changes
supabase.auth.onAuthStateChange((event, session) => {
  if (event === 'SIGNED_IN') {
    // Handle sign in
  }
})
```

### Database Queries

```typescript
// Select with relations
const { data: posts, error } = await supabase
  .from('posts')
  .select(`
    id,
    title,
    content,
    author:profiles(username, avatar_url),
    comments(id, content, created_at)
  `)
  .eq('published', true)
  .order('created_at', { ascending: false })
  .range(0, 9)

// Insert with returning
const { data: post, error } = await supabase
  .from('posts')
  .insert({
    title: 'New Post',
    content: 'Content here',
    author_id: user.id
  })
  .select()
  .single()

// Update with filters
const { error } = await supabase
  .from('posts')
  .update({ published: true })
  .eq('id', postId)
  .eq('author_id', user.id)

// Delete with cascade
const { error } = await supabase
  .from('posts')
  .delete()
  .eq('id', postId)
```

### Storage Operations

```typescript
// Upload file
const { data, error } = await supabase.storage
  .from('avatars')
  .upload(`${userId}/avatar.png`, file, {
    cacheControl: '3600',
    upsert: true
  })

// Get public URL
const { data: { publicUrl } } = supabase.storage
  .from('avatars')
  .getPublicUrl(`${userId}/avatar.png`)

// Download file
const { data, error } = await supabase.storage
  .from('documents')
  .download('report.pdf')

// Create signed URL
const { data, error } = await supabase.storage
  .from('private')
  .createSignedUrl('file.pdf', 3600)
```

### Realtime Subscriptions

```typescript
// Subscribe to database changes
const channel = supabase
  .channel('posts-changes')
  .on(
    'postgres_changes',
    {
      event: '*',
      schema: 'public',
      table: 'posts',
      filter: 'published=eq.true'
    },
    (payload) => {
      console.log('Change:', payload)
    }
  )
  .subscribe()

// Broadcast messages
const channel = supabase.channel('room-1')
channel.subscribe((status) => {
  if (status === 'SUBSCRIBED') {
    channel.send({
      type: 'broadcast',
      event: 'cursor',
      payload: { x: 100, y: 200 }
    })
  }
})

// Presence tracking
const channel = supabase.channel('online-users')
channel.on('presence', { event: 'sync' }, () => {
  const state = channel.presenceState()
  console.log('Online users:', state)
})
channel.subscribe(async (status) => {
  if (status === 'SUBSCRIBED') {
    await channel.track({ user_id: user.id, online_at: new Date() })
  }
})

// Cleanup
supabase.removeChannel(channel)
```

### Edge Function Example

```typescript
// supabase/functions/send-email/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
    )

    const { email, subject, body } = await req.json()

    // Your email sending logic here

    return new Response(
      JSON.stringify({ success: true }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  }
})
```

## Best Practices

### Security
- Always enable RLS on public tables
- Use service role key only server-side
- Validate inputs in Edge Functions
- Implement proper auth checks
- Use parameterized queries
- Review RLS policies regularly

### Performance
- Add indexes for frequently queried columns
- Use `select()` to limit returned columns
- Implement pagination with `range()`
- Use database functions for complex operations
- Enable connection pooling in production
- Use `head: true` for count-only queries

### Architecture
- Keep migrations small and focused
- Use database triggers for side effects
- Implement proper error handling
- Generate and use TypeScript types
- Organize Edge Functions by domain
- Use shared utilities in `_shared/`

### Development Workflow
- Use Supabase CLI for local development
- Test RLS policies before deployment
- Seed database for consistent testing
- Use branching for schema changes
- Document all RLS policies

## Scripts

This skill includes executable scripts in the `scripts/` folder:

### Project Setup
- **setup-project.sh**: Initialize new Supabase project with configuration
  ```bash
  ./scripts/setup-project.sh <project-name>
  ```

- **local-dev.sh**: Start local Supabase development environment
  ```bash
  ./scripts/local-dev.sh [--reset]
  ```

### Database
- **create-migration.sh**: Create a new timestamped migration file
  ```bash
  ./scripts/create-migration.sh <migration-name>
  ```

- **run-migrations.sh**: Apply pending migrations
  ```bash
  ./scripts/run-migrations.sh [--local|--remote]
  ```

- **seed-database.sh**: Seed database with test data
  ```bash
  ./scripts/seed-database.sh
  ```

- **generate-types.sh**: Generate TypeScript types from database schema
  ```bash
  ./scripts/generate-types.sh [--output PATH]
  ```

- **link-project.sh**: Link local project to remote Supabase project
  ```bash
  ./scripts/link-project.sh <project-ref>
  ```

### Edge Functions
- **create-function.sh**: Create a new Edge Function with boilerplate
  ```bash
  ./scripts/create-function.sh <function-name>
  ```

- **deploy-function.sh**: Deploy Edge Function to production
  ```bash
  ./scripts/deploy-function.sh <function-name> [--all]
  ```

- **serve-functions.sh**: Run Edge Functions locally for testing
  ```bash
  ./scripts/serve-functions.sh
  ```

### Testing & Security
- **setup-testing.sh**: Set up testing environment with Vitest
  ```bash
  ./scripts/setup-testing.sh
  ```

- **run-tests.sh**: Run tests with various options
  ```bash
  ./scripts/run-tests.sh [--watch] [--ui] [--coverage]
  ```

- **test-rls.sh**: Test RLS policies with different user contexts
  ```bash
  ./scripts/test-rls.sh <table-name>
  ```

- **backup-database.sh**: Create database backup
  ```bash
  ./scripts/backup-database.sh [--output PATH]
  ```

## Templates

This skill includes production-ready templates in the `templates/` folder:

### Database
- **schema-base.sql**: Complete base schema with profiles, posts, comments, RLS policies, triggers, and indexes
- **rls-policies.sql**: Comprehensive RLS policy patterns library (10+ patterns including user-owned, org-based, role-based, time-based, and more)

### Client Code
- **supabase-client.ts**: Type-safe client initialization with browser, server, and admin clients plus utility functions
- **auth-helpers.ts**: Complete authentication utilities including email/password, OAuth, magic links, phone auth, MFA, and React hooks
- **storage-helpers.ts**: File upload/download utilities with progress tracking, image compression, bucket management, and React hooks

### Edge Functions
- **edge-function-complete.ts**: Complete Edge Function template with CORS, authentication, validation, error handling, and common patterns (webhooks, scheduled tasks, email, external APIs, rate limiting)

## Resources

This skill includes detailed reference guides in the `resources/` folder:

- **database-patterns.md**: Schema design, queries, migrations, and PostgreSQL features
- **authentication.md**: Auth flows, providers, sessions, and MFA
- **row-level-security.md**: RLS policy patterns and multi-tenant security
- **storage.md**: File storage, access control, and transformations
- **edge-functions.md**: Deno runtime, deployment, and best practices
- **realtime.md**: Subscriptions, broadcast, and presence
- **client-libraries.md**: JavaScript, Python, and other client usage

---

**Specialization**: Supabase Full-Stack Development
**Version**: 1.0
**Last Updated**: January 2026
