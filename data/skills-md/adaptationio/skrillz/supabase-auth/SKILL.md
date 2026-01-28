---
name: supabase-auth
description: Setup and manage Supabase authentication including project connection, tokens, login methods, and user management. Use when configuring Supabase access, implementing authentication, or managing users.
---

# Supabase Authentication Skill

Setup and manage Supabase authentication for projects.

## Quick Reference

| Task | Method |
|------|--------|
| Install CLI | `npm install supabase --save-dev` |
| Login to Supabase | `supabase login` |
| Link project | `supabase link --project-ref <ref>` |
| Check status | `supabase status` |
| Get project URL | Dashboard → Settings → API |
| Get anon key | Dashboard → Settings → API |
| Get service key | Dashboard → Settings → API (hidden by default) |

## Environment Variables

```bash
# Required for all Supabase operations
SUPABASE_URL=https://<project-ref>.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# For server-side admin operations (NEVER expose client-side)
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# For CI/CD pipelines
SUPABASE_ACCESS_TOKEN=<personal-access-token>
SUPABASE_DB_PASSWORD=<database-password>
SUPABASE_PROJECT_ID=<project-ref>
```

## Client Initialization

### Browser/Client-Side

```javascript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_ANON_KEY
)
```

### Server-Side (with Service Role)

```javascript
import { createClient } from '@supabase/supabase-js'

const supabaseAdmin = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY,
  {
    auth: {
      autoRefreshToken: false,
      persistSession: false
    }
  }
)
```

## Authentication Methods

### Email/Password

```javascript
// Sign up
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'password123',
  options: {
    data: { full_name: 'John Doe' }  // user metadata
  }
})

// Sign in
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'password123'
})

// Sign out
const { error } = await supabase.auth.signOut()
```

### Magic Link (Passwordless)

```javascript
const { data, error } = await supabase.auth.signInWithOtp({
  email: 'user@example.com',
  options: {
    emailRedirectTo: 'https://yourapp.com/welcome'
  }
})
```

### OAuth Providers

```javascript
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'github',  // or 'google', 'discord', etc.
  options: {
    redirectTo: 'https://yourapp.com/auth/callback'
  }
})
```

### Anonymous Auth

```javascript
const { data, error } = await supabase.auth.signInAnonymously()
```

## Session Management

### Get Current Session

```javascript
// From local storage (fast, no network)
const { data: { session } } = await supabase.auth.getSession()

// Validate with server (secure, use on server-side)
const { data: { user } } = await supabase.auth.getUser()
```

### Listen for Auth Changes

```javascript
const { data: { subscription } } = supabase.auth.onAuthStateChange(
  (event, session) => {
    console.log(event, session)
    // Events: SIGNED_IN, SIGNED_OUT, TOKEN_REFRESHED, USER_UPDATED
  }
)

// Cleanup
subscription.unsubscribe()
```

## Password Recovery

```javascript
// Request reset
const { error } = await supabase.auth.resetPasswordForEmail(
  'user@example.com',
  { redirectTo: 'https://yourapp.com/update-password' }
)

// Update password (after redirect)
const { error } = await supabase.auth.updateUser({
  password: 'new_password'
})
```

## Admin Operations (Server-Side Only)

```javascript
// Create user (bypasses email confirmation)
const { data, error } = await supabaseAdmin.auth.admin.createUser({
  email: 'user@example.com',
  password: 'password123',
  email_confirm: true,
  app_metadata: { role: 'admin' }
})

// Delete user
const { error } = await supabaseAdmin.auth.admin.deleteUser(userId)

// Update user
const { data, error } = await supabaseAdmin.auth.admin.updateUserById(
  userId,
  { app_metadata: { role: 'moderator' } }
)

// List users
const { data, error } = await supabaseAdmin.auth.admin.listUsers()
```

## Security Notes

1. **Never expose service role key** - It bypasses Row Level Security
2. **Use getUser() on server** - Don't trust getSession() for authorization
3. **Use app_metadata for roles** - user_metadata is user-editable
4. **Enable RLS on all tables** - Without it, anyone can access data

## References

- [auth-methods.md](references/auth-methods.md) - All authentication methods in detail
- [session-management.md](references/session-management.md) - Session lifecycle and tokens
- [mfa-setup.md](references/mfa-setup.md) - Multi-factor authentication
