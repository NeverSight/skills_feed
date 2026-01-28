---
name: supabase-mcp-integration
description: Comprehensive Supabase integration covering authentication, database operations, realtime subscriptions, storage, and MCP server patterns for building production-ready backends with PostgreSQL, Auth, and real-time capabilities
---

# Supabase MCP Integration

A comprehensive skill for building production-ready applications using Supabase - the open-source Backend-as-a-Service platform built on PostgreSQL. This skill covers authentication, database operations, real-time subscriptions, storage, TypeScript integration, and Row-Level Security patterns.

## When to Use This Skill

Use this skill when:

- Building full-stack web or mobile applications with PostgreSQL backend
- Implementing authentication (email, OAuth, magic links, MFA) and session management
- Creating real-time applications (chat, collaboration, live dashboards)
- Managing file storage with image optimization and CDN delivery
- Building multi-tenant SaaS applications with fine-grained authorization
- Migrating from Firebase to SQL-based backend
- Requiring type-safe database operations with TypeScript
- Implementing Row-Level Security (RLS) for database authorization
- Building applications with complex queries, joins, and relationships
- Setting up instant REST/GraphQL APIs from database schema

## Core Concepts

### Supabase Platform Architecture

Supabase is an integrated platform built on enterprise-grade open-source components:

**Key Components:**
- **PostgreSQL Database**: Full Postgres with extensions (PostGIS, pg_vector)
- **GoTrue (Auth)**: JWT-based authentication with multiple providers
- **PostgREST**: Auto-generated REST APIs from database schema
- **Realtime**: WebSocket server for database changes, broadcast, and presence
- **Storage**: S3-compatible file storage with CDN and image optimization
- **Edge Functions**: Globally distributed serverless functions (Deno runtime)

**Unified Client Library:**
```typescript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY)

// All features through single client
await supabase.auth.signIn()           // Authentication
await supabase.from('users').select()  // Database
supabase.channel('room').subscribe()   // Realtime
await supabase.storage.from().upload() // Storage
```

### Row-Level Security (RLS)

Database-level authorization using PostgreSQL policies:
- Define access rules directly in the database
- Automatic enforcement on all queries
- Integrated with JWT authentication
- Fine-grained control at row and column level

### JWT-Based Authentication

Supabase Auth uses JSON Web Tokens:
- Issued upon successful authentication
- Automatically included in database queries
- Used for RLS policy evaluation
- Refresh token flow for long sessions

### Type Safety

Automatic TypeScript type generation from database schema:
- Generate types from live database
- Type-safe queries and mutations
- Compile-time error detection
- IDE autocomplete support

## Supabase Client Setup

### Installation

```bash
# npm
npm install @supabase/supabase-js

# yarn
yarn add @supabase/supabase-js

# pnpm
pnpm add @supabase/supabase-js

# bun
bun add @supabase/supabase-js
```

### Environment Configuration

```bash
# .env.local
NEXT_PUBLIC_SUPABASE_URL=https://xyzcompany.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# For server-side operations (keep secure!)
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Security Note:** Never expose the `service_role` key in client-side code.

### Client Initialization Pattern (Recommended)

```typescript
// lib/supabase.ts

import { createClient, SupabaseClient } from '@supabase/supabase-js'
import { Database } from './database.types'

function validateEnvironment() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL
  const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

  if (!url) {
    throw new Error('Missing environment variable: NEXT_PUBLIC_SUPABASE_URL')
  }

  if (!anonKey) {
    throw new Error('Missing environment variable: NEXT_PUBLIC_SUPABASE_ANON_KEY')
  }

  return { url, anonKey }
}

let supabaseInstance: SupabaseClient<Database> | null = null

export function getSupabaseClient(): SupabaseClient<Database> {
  if (!supabaseInstance) {
    const { url, anonKey } = validateEnvironment()

    supabaseInstance = createClient<Database>(url, anonKey, {
      auth: {
        autoRefreshToken: true,
        persistSession: true,
        detectSessionInUrl: true
      },
      global: {
        headers: {
          'X-Application-Name': 'MyApp'
        }
      }
    })
  }

  return supabaseInstance
}

// Export singleton instance
export const supabase = getSupabaseClient()
```

### Configuration Options

```typescript
const options = {
  // Database configuration
  db: {
    schema: 'public'  // Default schema
  },

  // Authentication configuration
  auth: {
    autoRefreshToken: true,     // Automatically refresh tokens
    persistSession: true,        // Persist session to localStorage
    detectSessionInUrl: true,    // Detect session from URL hash
    flowType: 'pkce',           // Use PKCE flow for OAuth
    storage: customStorage,      // Custom storage implementation
    storageKey: 'sb-auth-token' // Storage key for session
  },

  // Global configuration
  global: {
    headers: {
      'X-Application-Name': 'my-app',
      'apikey': SUPABASE_ANON_KEY
    },
    fetch: customFetch  // Custom fetch implementation
  },

  // Realtime configuration
  realtime: {
    params: {
      eventsPerSecond: 10
    },
    timeout: 10000,
    heartbeatInterval: 30000
  }
}

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY, options)
```

### Platform-Specific Setup

**React Native with AsyncStorage:**
```typescript
import AsyncStorage from '@react-native-async-storage/async-storage'
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
  auth: {
    storage: AsyncStorage,
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: false
  }
})
```

**React Native with Expo SecureStore:**
```typescript
import * as SecureStore from 'expo-secure-store'
import { createClient } from '@supabase/supabase-js'

const ExpoSecureStoreAdapter = {
  getItem: (key: string) => SecureStore.getItemAsync(key),
  setItem: (key: string, value: string) => SecureStore.setItemAsync(key, value),
  removeItem: (key: string) => SecureStore.deleteItemAsync(key)
}

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
  auth: {
    storage: ExpoSecureStoreAdapter,
    autoRefreshToken: true,
    persistSession: true
  }
})
```

## Authentication & Authorization

### Email/Password Authentication

**Sign Up:**
```typescript
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'secure-password',
  options: {
    data: {
      // Additional user metadata
      display_name: 'John Doe',
      avatar_url: 'https://example.com/avatar.jpg'
    },
    emailRedirectTo: 'https://yourapp.com/welcome'
  }
})

if (error) {
  console.error('Signup failed:', error.message)
  return
}

console.log('User created:', data.user)
console.log('Session:', data.session)
```

**Sign In:**
```typescript
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'secure-password'
})

if (error) {
  console.error('Login failed:', error.message)
  return
}

console.log('User:', data.user)
console.log('Session token:', data.session?.access_token)
```

### Magic Link (Passwordless)

```typescript
const { data, error } = await supabase.auth.signInWithOtp({
  email: 'user@example.com',
  options: {
    emailRedirectTo: 'https://yourapp.com/login',
    shouldCreateUser: true
  }
})

if (error) {
  console.error('Failed to send magic link:', error.message)
  return
}

console.log('Magic link sent')
```

### One-Time Password (OTP) - Phone

```typescript
// Send OTP
const { data, error } = await supabase.auth.signInWithOtp({
  phone: '+1234567890',
  options: {
    channel: 'sms' // or 'whatsapp'
  }
})

// Verify OTP
const { data: verifyData, error: verifyError } = await supabase.auth.verifyOtp({
  phone: '+1234567890',
  token: '123456',
  type: 'sms'
})
```

### OAuth (Social Login)

```typescript
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google',
  options: {
    redirectTo: 'https://yourapp.com/auth/callback',
    scopes: 'email profile',
    queryParams: {
      access_type: 'offline',
      prompt: 'consent'
    }
  }
})

// Supported providers:
// apple, google, github, gitlab, bitbucket, discord, facebook,
// twitter, microsoft, linkedin, notion, slack, spotify, twitch, etc.
```

### Session Management

```typescript
// Get current session
const { data: { session }, error } = await supabase.auth.getSession()

if (session) {
  console.log('Access token:', session.access_token)
  console.log('User:', session.user)
  console.log('Expires at:', session.expires_at)
}

// Get current user
const { data: { user }, error } = await supabase.auth.getUser()

// Refresh session
const { data, error } = await supabase.auth.refreshSession()

// Sign out
const { error } = await supabase.auth.signOut()
```

### Auth State Changes

```typescript
const { data: { subscription } } = supabase.auth.onAuthStateChange(
  (event, session) => {
    console.log('Auth event:', event)

    switch (event) {
      case 'SIGNED_IN':
        console.log('User signed in:', session?.user)
        break

      case 'SIGNED_OUT':
        console.log('User signed out')
        break

      case 'TOKEN_REFRESHED':
        console.log('Token refreshed')
        break

      case 'USER_UPDATED':
        console.log('User updated:', session?.user)
        break

      case 'PASSWORD_RECOVERY':
        console.log('Password recovery initiated')
        break
    }
  }
)

// Cleanup
subscription.unsubscribe()
```

### User Management

```typescript
// Update user
const { data, error } = await supabase.auth.updateUser({
  email: 'newemail@example.com',
  password: 'new-password',
  data: {
    display_name: 'New Name',
    avatar_url: 'https://example.com/new-avatar.jpg'
  }
})

// Reset password
const { data, error } = await supabase.auth.resetPasswordForEmail(
  'user@example.com',
  {
    redirectTo: 'https://yourapp.com/reset-password'
  }
)

// Update password after reset
const { data: updateData, error: updateError } = await supabase.auth.updateUser({
  password: 'new-secure-password'
})
```

### Multi-Factor Authentication (MFA)

```typescript
// Enroll MFA
const { data: enrollData, error: enrollError } = await supabase.auth.mfa.enroll({
  factorType: 'totp',
  friendlyName: 'My Phone'
})

// Verify enrollment
const { data: verifyData, error: verifyError } = await supabase.auth.mfa.verify({
  factorId: enrollData.id,
  code: '123456'
})

// Challenge (during sign-in)
const { data: challengeData, error: challengeError } = await supabase.auth.mfa.challenge({
  factorId: 'factor-id'
})

// Verify challenge
const { data, error } = await supabase.auth.mfa.verify({
  factorId: 'factor-id',
  challengeId: challengeData.id,
  code: '123456'
})
```

## Database Operations

### SELECT Queries

**Basic Select:**
```typescript
// Select all columns
const { data, error } = await supabase
  .from('users')
  .select()

// Select specific columns
const { data, error } = await supabase
  .from('users')
  .select('id, email, created_at')
```

**Filtering:**
```typescript
// Equal
const { data } = await supabase
  .from('users')
  .select()
  .eq('status', 'active')

// Not equal
const { data } = await supabase
  .from('users')
  .select()
  .neq('role', 'admin')

// Greater than / Less than
const { data } = await supabase
  .from('products')
  .select()
  .gt('price', 100)
  .lte('stock', 10)

// In array
const { data } = await supabase
  .from('users')
  .select()
  .in('id', [1, 2, 3, 4, 5])

// Pattern matching
const { data } = await supabase
  .from('users')
  .select()
  .like('email', '%@gmail.com')

// Case-insensitive pattern matching
const { data } = await supabase
  .from('products')
  .select()
  .ilike('name', '%laptop%')

// Full text search
const { data } = await supabase
  .from('articles')
  .select()
  .textSearch('title', 'postgres database')

// Null checks
const { data } = await supabase
  .from('users')
  .select()
  .is('deleted_at', null)
```

**Ordering and Pagination:**
```typescript
// Order by
const { data } = await supabase
  .from('posts')
  .select()
  .order('created_at', { ascending: false })

// Multiple ordering
const { data } = await supabase
  .from('users')
  .select()
  .order('last_name', { ascending: true })
  .order('first_name', { ascending: true })

// Limit results
const { data } = await supabase
  .from('posts')
  .select()
  .limit(10)

// Pagination with range
const { data } = await supabase
  .from('posts')
  .select()
  .range(0, 9)  // First 10 items (0-indexed)
```

**Joins and Nested Queries:**
```typescript
// One-to-many relationship
const { data } = await supabase
  .from('users')
  .select(`
    id,
    email,
    posts (
      id,
      title,
      created_at
    )
  `)

// Many-to-many with junction table
const { data } = await supabase
  .from('users')
  .select(`
    id,
    email,
    user_roles (
      role:roles (
        id,
        name
      )
    )
  `)

// Nested filtering
const { data } = await supabase
  .from('users')
  .select(`
    id,
    email,
    posts!inner (
      id,
      title
    )
  `)
  .eq('posts.published', true)
```

**Aggregation:**
```typescript
// Count
const { count, error } = await supabase
  .from('users')
  .select('*', { count: 'exact', head: true })

// Count with filtering
const { count } = await supabase
  .from('users')
  .select('*', { count: 'exact', head: true })
  .eq('status', 'active')
```

### INSERT Operations

```typescript
// Insert single row
const { data, error } = await supabase
  .from('users')
  .insert({
    email: 'user@example.com',
    name: 'John Doe',
    age: 30
  })
  .select()  // Return inserted row

// Insert multiple rows
const { data, error } = await supabase
  .from('users')
  .insert([
    { email: 'user1@example.com', name: 'User One' },
    { email: 'user2@example.com', name: 'User Two' },
    { email: 'user3@example.com', name: 'User Three' }
  ])
  .select()

// Upsert (Insert or Update)
const { data, error } = await supabase
  .from('users')
  .upsert({
    id: 1,
    email: 'updated@example.com',
    name: 'Updated Name'
  }, {
    onConflict: 'id'  // Conflict column(s)
  })
  .select()
```

### UPDATE Operations

```typescript
// Update with filter
const { data, error } = await supabase
  .from('users')
  .update({ status: 'inactive' })
  .eq('last_login', null)
  .select()

// Update single row by ID
const { data, error } = await supabase
  .from('users')
  .update({ name: 'New Name' })
  .eq('id', userId)
  .select()
  .single()

// Increment value
const { data, error } = await supabase
  .from('profiles')
  .update({ login_count: supabase.raw('login_count + 1') })
  .eq('id', userId)
```

### DELETE Operations

```typescript
// Delete with filter
const { error } = await supabase
  .from('users')
  .delete()
  .eq('status', 'banned')

// Delete single row
const { error } = await supabase
  .from('posts')
  .delete()
  .eq('id', postId)

// Soft delete pattern
const { error } = await supabase
  .from('users')
  .update({ deleted_at: new Date().toISOString() })
  .eq('id', userId)
```

### RPC (Remote Procedure Calls)

```typescript
// Call function without parameters
const { data, error } = await supabase
  .rpc('get_user_count')

// Call function with parameters
const { data, error } = await supabase
  .rpc('calculate_discount', {
    product_id: 123,
    user_id: 456
  })
```

## Realtime Subscriptions

### Database Change Subscriptions

```typescript
// Listen to all changes
const channel = supabase
  .channel('db-changes')
  .on(
    'postgres_changes',
    {
      event: '*',          // All events: INSERT, UPDATE, DELETE
      schema: 'public',
      table: 'posts'
    },
    (payload) => {
      console.log('Change received:', payload)
      console.log('Event type:', payload.eventType)
      console.log('New data:', payload.new)
      console.log('Old data:', payload.old)
    }
  )
  .subscribe()

// Cleanup
channel.unsubscribe()
```

**Listen to Specific Events:**
```typescript
// INSERT only
const insertChannel = supabase
  .channel('post-inserts')
  .on(
    'postgres_changes',
    {
      event: 'INSERT',
      schema: 'public',
      table: 'posts'
    },
    (payload) => {
      console.log('New post created:', payload.new)
    }
  )
  .subscribe()

// UPDATE only
const updateChannel = supabase
  .channel('post-updates')
  .on(
    'postgres_changes',
    {
      event: 'UPDATE',
      schema: 'public',
      table: 'posts'
    },
    (payload) => {
      console.log('Post updated:', payload.new)
    }
  )
  .subscribe()

// Filter changes for specific rows
const channel = supabase
  .channel('user-posts')
  .on(
    'postgres_changes',
    {
      event: '*',
      schema: 'public',
      table: 'posts',
      filter: `user_id=eq.${userId}`
    },
    (payload) => {
      console.log('User post changed:', payload)
    }
  )
  .subscribe()
```

### Broadcast Messages

```typescript
// Send broadcast
const channel = supabase.channel('room-1')

channel.subscribe((status) => {
  if (status === 'SUBSCRIBED') {
    channel.send({
      type: 'broadcast',
      event: 'cursor-move',
      payload: { x: 100, y: 200, user: 'Alice' }
    })
  }
})

// Receive broadcast
const channel = supabase
  .channel('room-1')
  .on('broadcast', { event: 'cursor-move' }, (payload) => {
    console.log('Cursor moved:', payload)
  })
  .subscribe()
```

### Presence Tracking

```typescript
// Track user presence
const channel = supabase.channel('online-users')

// Set initial state
channel.subscribe(async (status) => {
  if (status === 'SUBSCRIBED') {
    await channel.track({
      user: 'user-1',
      online_at: new Date().toISOString(),
      status: 'online'
    })
  }
})

// Listen to presence changes
channel.on('presence', { event: 'sync' }, () => {
  const state = channel.presenceState()
  console.log('Online users:', state)
})

channel.on('presence', { event: 'join' }, ({ newPresences }) => {
  console.log('Users joined:', newPresences)
})

channel.on('presence', { event: 'leave' }, ({ leftPresences }) => {
  console.log('Users left:', leftPresences)
})

// Cleanup
channel.unsubscribe()
```

## Storage Operations

### Bucket Management

```typescript
// List buckets
const { data: buckets, error } = await supabase
  .storage
  .listBuckets()

// Create bucket
const { data, error } = await supabase
  .storage
  .createBucket('avatars', {
    public: false,           // Private bucket
    fileSizeLimit: 1048576,  // 1MB limit
    allowedMimeTypes: ['image/png', 'image/jpeg']
  })

// Update bucket
const { data, error } = await supabase
  .storage
  .updateBucket('avatars', {
    public: true
  })

// Delete bucket
const { data, error } = await supabase
  .storage
  .deleteBucket('avatars')
```

### File Upload

```typescript
// Standard upload
const file = event.target.files[0]
const filePath = `${userId}/${Date.now()}-${file.name}`

const { data, error } = await supabase
  .storage
  .from('avatars')
  .upload(filePath, file, {
    cacheControl: '3600',
    upsert: false
  })

// Upload with progress tracking
const { data, error } = await supabase
  .storage
  .from('videos')
  .upload(filePath, file, {
    onUploadProgress: (progress) => {
      const percent = (progress.loaded / progress.total) * 100
      console.log(`Upload progress: ${percent.toFixed(2)}%`)
    }
  })
```

### File Download and URLs

```typescript
// Download file
const { data, error } = await supabase
  .storage
  .from('avatars')
  .download('path/to/file.jpg')

// Get public URL (for public buckets)
const { data } = supabase
  .storage
  .from('avatars')
  .getPublicUrl('path/to/file.jpg')

// Create signed URL (for private buckets)
const { data, error } = await supabase
  .storage
  .from('private-files')
  .createSignedUrl('path/to/file.pdf', 60) // Expires in 60 seconds
```

### Image Transformation

```typescript
const { data } = supabase
  .storage
  .from('avatars')
  .getPublicUrl('user-avatar.jpg', {
    transform: {
      width: 200,
      height: 200,
      resize: 'cover',  // or 'contain', 'fill'
      quality: 80,
      format: 'webp'
    }
  })
```

### File Management

```typescript
// List files
const { data, error } = await supabase
  .storage
  .from('avatars')
  .list('user-123', {
    limit: 100,
    offset: 0,
    sortBy: { column: 'name', order: 'asc' }
  })

// Delete files
const { data, error } = await supabase
  .storage
  .from('avatars')
  .remove(['path/to/file1.jpg', 'path/to/file2.jpg'])

// Move file
const { data, error } = await supabase
  .storage
  .from('avatars')
  .move('old/path/file.jpg', 'new/path/file.jpg')

// Copy file
const { data, error } = await supabase
  .storage
  .from('avatars')
  .copy('source/file.jpg', 'destination/file.jpg')
```

## TypeScript Integration

### Generate Database Types

```bash
# Install Supabase CLI
npm install -g supabase

# Login
supabase login

# Generate types
supabase gen types typescript --project-id YOUR_PROJECT_ID > database.types.ts
```

### Use Generated Types

```typescript
import { createClient } from '@supabase/supabase-js'
import { Database } from './database.types'

// Create typed client
const supabase = createClient<Database>(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_ANON_KEY!
)

// Type-safe queries
const { data, error } = await supabase
  .from('users')
  .select('id, email, created_at')
  .eq('id', userId)

// data is typed as:
// Array<{ id: string; email: string; created_at: string }> | null

// Type-safe inserts
const { data, error } = await supabase
  .from('posts')
  .insert({
    title: 'My Post',
    content: 'Content here',
    user_id: userId,
    published: true
  })
  .select()
```

### Helper Types

```typescript
import { Database } from './database.types'

// Get table row type
type User = Database['public']['Tables']['users']['Row']

// Get insert type
type NewUser = Database['public']['Tables']['users']['Insert']

// Get update type
type UserUpdate = Database['public']['Tables']['users']['Update']

// Get enum type
type UserRole = Database['public']['Enums']['user_role']

// Use in functions
function createUser(user: NewUser): Promise<User> {
  // Implementation
}
```

## Row-Level Security (RLS)

### Enable RLS

```sql
-- Enable RLS on a table
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
```

### Common RLS Patterns

**Public Read Access:**
```sql
CREATE POLICY "Public profiles are visible to everyone"
ON profiles
FOR SELECT
TO anon, authenticated
USING (true);
```

**User Can Only See Own Data:**
```sql
CREATE POLICY "Users can only see own data"
ON posts
FOR SELECT
TO authenticated
USING (auth.uid() = user_id);
```

**User Can Only Modify Own Data:**
```sql
CREATE POLICY "Users can insert own posts"
ON posts
FOR INSERT
TO authenticated
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own posts"
ON posts
FOR UPDATE
TO authenticated
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own posts"
ON posts
FOR DELETE
TO authenticated
USING (auth.uid() = user_id);
```

**Multi-Tenant Pattern:**
```sql
CREATE POLICY "Users can only see data from own organization"
ON documents
FOR SELECT
TO authenticated
USING (
  organization_id IN (
    SELECT organization_id
    FROM user_organizations
    WHERE user_id = auth.uid()
  )
);
```

**Role-Based Access Control:**
```sql
CREATE POLICY "Admin can see all users"
ON users
FOR SELECT
TO authenticated
USING (
  auth.jwt() ->> 'role' = 'admin'
  OR auth.uid() = id
);
```

## Best Practices

### Client Initialization

**Use Singleton Pattern:**
- Create single client instance and reuse across app
- Avoid creating new clients on every request
- Store in module-level variable or context

### Error Handling

**Always Check Errors:**
```typescript
const { data, error } = await supabase
  .from('users')
  .select()

if (error) {
  console.error('Error fetching users:', error.message)
  // Handle error appropriately
  return
}

// Use data safely
console.log(data)
```

**Use throwOnError() for Promise Rejection:**
```typescript
try {
  const { data } = await supabase
    .from('users')
    .insert({ name: 'John' })
    .throwOnError()

  console.log('User created:', data)
} catch (error) {
  console.error('Failed to create user:', error)
}
```

### Security

**Never Expose Service Role Key:**
- Use `anon` key in client-side code
- Use `service_role` key only in server-side code
- Keep service role key in server environment variables

**Always Enable RLS:**
- Enable RLS on all tables
- Create appropriate policies for each table
- Test policies thoroughly

**Validate User Input:**
- Never trust client-side data
- Use database constraints and validations
- Validate in both client and database

### Performance

**Use Select Wisely:**
```typescript
// Bad: Fetch all columns
const { data } = await supabase.from('users').select()

// Good: Only fetch needed columns
const { data } = await supabase.from('users').select('id, email')
```

**Use Pagination:**
```typescript
// Bad: Fetch all rows
const { data } = await supabase.from('posts').select()

// Good: Paginate results
const { data } = await supabase
  .from('posts')
  .select()
  .range(0, 9)
  .order('created_at', { ascending: false })
```

**Index Database Columns:**
- Add indexes for frequently queried columns
- Index foreign keys
- Use composite indexes for multi-column queries

### Connection Management

**Reuse Client Instance:**
- Don't create new client for each request
- Use singleton pattern for client initialization
- Consider connection pooling for server-side

**Clean Up Subscriptions:**
```typescript
useEffect(() => {
  const channel = supabase.channel('room-1')

  channel.subscribe(/* ... */)

  return () => {
    channel.unsubscribe()
  }
}, [])
```

## Common Patterns & Workflows

### User Authentication Flow

```typescript
// 1. Sign up
const { data: signUpData, error: signUpError } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'secure-password'
})

// 2. Listen to auth state
supabase.auth.onAuthStateChange((event, session) => {
  if (event === 'SIGNED_IN') {
    // Redirect to dashboard
  }
})

// 3. Protected route check
const { data: { session } } = await supabase.auth.getSession()
if (!session) {
  // Redirect to login
}

// 4. Sign out
await supabase.auth.signOut()
```

### CRUD with RLS

```typescript
// Enable RLS on table
/*
ALTER TABLE todos ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can CRUD own todos"
ON todos
FOR ALL
TO authenticated
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);
*/

// Create
const { data, error } = await supabase
  .from('todos')
  .insert({
    user_id: session.user.id,
    title: 'My Todo',
    completed: false
  })
  .select()

// Read (only user's own todos due to RLS)
const { data, error } = await supabase
  .from('todos')
  .select()

// Update
const { data, error } = await supabase
  .from('todos')
  .update({ completed: true })
  .eq('id', todoId)

// Delete
const { error } = await supabase
  .from('todos')
  .delete()
  .eq('id', todoId)
```

### Real-Time Chat Implementation

```typescript
import { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'

function Chat({ roomId, userId }) {
  const [messages, setMessages] = useState([])

  useEffect(() => {
    // Fetch existing messages
    const fetchMessages = async () => {
      const { data } = await supabase
        .from('messages')
        .select()
        .eq('room_id', roomId)
        .order('created_at', { ascending: true })

      if (data) setMessages(data)
    }

    fetchMessages()

    // Subscribe to new messages
    const channel = supabase
      .channel(`room-${roomId}`)
      .on(
        'postgres_changes',
        {
          event: 'INSERT',
          schema: 'public',
          table: 'messages',
          filter: `room_id=eq.${roomId}`
        },
        (payload) => {
          setMessages((prev) => [...prev, payload.new])
        }
      )
      .subscribe()

    return () => {
      channel.unsubscribe()
    }
  }, [roomId])

  const sendMessage = async (content: string) => {
    await supabase.from('messages').insert({
      room_id: roomId,
      user_id: userId,
      content
    })
  }

  return (
    <div>
      {messages.map((msg) => (
        <div key={msg.id}>{msg.content}</div>
      ))}
    </div>
  )
}
```

### File Upload with Progress

```typescript
async function uploadAvatar(file: File, userId: string) {
  const filePath = `${userId}/${Date.now()}-${file.name}`

  const { data, error } = await supabase.storage
    .from('avatars')
    .upload(filePath, file, {
      cacheControl: '3600',
      upsert: false,
      onUploadProgress: (progress) => {
        const percent = (progress.loaded / progress.total) * 100
        console.log(`Upload: ${percent.toFixed(2)}%`)
      }
    })

  if (error) {
    console.error('Upload failed:', error.message)
    return null
  }

  // Get public URL
  const { data: urlData } = supabase.storage
    .from('avatars')
    .getPublicUrl(filePath)

  // Update user profile with avatar URL
  await supabase
    .from('profiles')
    .update({ avatar_url: urlData.publicUrl })
    .eq('id', userId)

  return urlData.publicUrl
}
```

## Troubleshooting

### Common Issues

**RLS Blocking Queries:**
- Check if RLS is enabled: `ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;`
- Verify policies exist and match your use case
- Test policies with different user contexts
- Use `USING` clause for SELECT/UPDATE/DELETE
- Use `WITH CHECK` clause for INSERT/UPDATE

**Auth Session Not Persisting:**
- Ensure `persistSession: true` in config
- Check if storage (localStorage) is available
- Verify cookies are not blocked
- Check if third-party cookies are enabled (for OAuth)

**Realtime Not Working:**
- Enable realtime on table in Supabase dashboard
- Check if RLS policies allow subscriptions
- Verify channel subscription is successful
- Check network/firewall blocking WebSockets

**Type Generation Errors:**
- Ensure Supabase CLI is installed and updated
- Verify project ID is correct
- Check network connectivity to Supabase
- Try regenerating types with `--debug` flag

### Debug RLS Policies

```sql
-- Test policy as specific user
SET request.jwt.claims.sub = 'user-uuid-here';

-- Run query to see what's visible
SELECT * FROM posts;

-- Reset to admin
RESET request.jwt.claims.sub;
```

### Performance Issues

**Slow Queries:**
- Add indexes on frequently queried columns
- Use `EXPLAIN ANALYZE` to analyze query plan
- Avoid fetching unnecessary columns
- Use pagination for large datasets

**Too Many Connections:**
- Use connection pooling
- Reuse client instance
- Close unused subscriptions
- Consider using Edge Functions for server-side logic

## Production Deployment

### Environment Configuration

```bash
# Production .env
NEXT_PUBLIC_SUPABASE_URL=https://prod-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=prod-anon-key
SUPABASE_SERVICE_ROLE_KEY=prod-service-role-key

# Staging .env
NEXT_PUBLIC_SUPABASE_URL=https://staging-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=staging-anon-key
SUPABASE_SERVICE_ROLE_KEY=staging-service-role-key
```

### Database Migrations

Use Supabase CLI for schema migrations:

```bash
# Initialize migrations
supabase migration new create_posts_table

# Apply migrations
supabase db push

# Generate migration from changes
supabase db diff -f create_users_table
```

### Monitoring

- Enable Supabase Dashboard monitoring
- Set up alerts for errors and performance issues
- Monitor database connections
- Track API usage and quotas
- Set up logging for auth events

### Backup Strategy

- Enable automatic backups in Supabase dashboard
- Configure point-in-time recovery
- Test restoration procedures
- Export schema and data regularly
- Store backups in separate location

### Scaling Considerations

- Upgrade Supabase plan for higher limits
- Use database connection pooling
- Implement caching (Redis, etc.)
- Consider read replicas for heavy read loads
- Use Edge Functions for heavy compute
- Optimize database indexes
- Monitor and optimize slow queries

---

**Skill Version**: 1.0.0
**Last Updated**: October 2025
**Skill Category**: Backend-as-a-Service, Database Integration, Authentication, Real-time
**Compatible With**: React, Next.js, Vue, Angular, React Native, Flutter, Node.js, Deno
