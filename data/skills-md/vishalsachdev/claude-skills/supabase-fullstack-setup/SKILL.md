---
name: supabase-fullstack-setup
description: Complete guide to integrating Supabase with Next.js 13+ App Router, including authentication, database setup, Row Level Security (RLS), and common patterns for production apps. Use when starting a new Next.js project with Supabase, need authentication with social providers, or building apps with user-specific data.
---

# Supabase Full-Stack Setup for Next.js

Complete guide to integrating Supabase with Next.js 13+ App Router, including authentication, database setup, Row Level Security (RLS), and common patterns for production apps.

## When to use this skill

- Starting a new Next.js project with Supabase
- Need authentication with social providers
- Building apps with user-specific data (notes, favorites, etc.)
- Want real-time subscriptions
- Need secure server-side and client-side data access
- Implementing rate limiting or audit logs with database
- Building SaaS applications

## Core Setup

### Step 1: Install Dependencies

```bash
npm install @supabase/supabase-js @supabase/ssr
# or
pnpm add @supabase/supabase-js @supabase/ssr
```

### Step 2: Environment Variables

Create `.env.local`:

```bash
NEXT_PUBLIC_SUPABASE_URL=your-project-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

Get these from: https://app.supabase.com/project/_/settings/api

### Step 3: Create Supabase Clients

**Server Client** (`lib/supabase/server.ts`):

```typescript
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export async function createClient() {
  const cookieStore = await cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll()
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            )
          } catch {
            // Called from Server Component - middleware will handle
          }
        },
      },
    }
  )
}
```

**Browser Client** (`lib/supabase/client.ts`):

```typescript
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}
```

### Step 4: Authentication Setup

**Auth Context** (`contexts/auth-context.tsx`):

```typescript
'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import { createClient } from '@/lib/supabase/client';
import type { User } from '@supabase/supabase-js';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const supabase = createClient();

  useEffect(() => {
    // Get initial session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null);
      setLoading(false);
    });

    // Listen for auth changes
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null);
    });

    return () => subscription.unsubscribe();
  }, []);

  const signIn = async (email: string, password: string) => {
    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });
    if (error) throw error;
  };

  const signUp = async (email: string, password: string) => {
    const { error} = await supabase.auth.signUp({
      email,
      password,
    });
    if (error) throw error;
  };

  const signOut = async () => {
    const { error } = await supabase.auth.signOut();
    if (error) throw error;
  };

  return (
    <AuthContext.Provider value={{ user, loading, signIn, signUp, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
```

### Step 5: Database Schema Examples

**Video Analysis Table**:

```sql
CREATE TABLE video_analyses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  youtube_id TEXT NOT NULL UNIQUE,
  user_id UUID REFERENCES auth.users(id),
  title TEXT NOT NULL,
  author TEXT,
  thumbnail_url TEXT,
  duration INTEGER,
  transcript JSONB,
  topics JSONB,
  summary TEXT,
  suggested_questions JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_video_analyses_youtube_id ON video_analyses(youtube_id);
CREATE INDEX idx_video_analyses_user_id ON video_analyses(user_id);
```

**Notes Table**:

```sql
CREATE TABLE notes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) NOT NULL,
  video_id UUID REFERENCES video_analyses(id) ON DELETE CASCADE,
  source TEXT NOT NULL,
  source_id TEXT,
  text TEXT NOT NULL,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_notes_user_id ON notes(user_id);
CREATE INDEX idx_notes_video_id ON notes(video_id);
```

**Favorites Table**:

```sql
CREATE TABLE user_favorites (
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  video_analysis_id UUID REFERENCES video_analyses(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (user_id, video_analysis_id)
);
```

**Rate Limiting Table**:

```sql
CREATE TABLE rate_limits (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  key TEXT NOT NULL,
  identifier TEXT NOT NULL,
  timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_rate_limits_key_timestamp ON rate_limits(key, timestamp);
CREATE INDEX idx_rate_limits_timestamp ON rate_limits(timestamp);
```

### Step 6: Row Level Security (RLS)

```sql
-- Enable RLS
ALTER TABLE notes ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_favorites ENABLE ROW LEVEL SECURITY;

-- Notes policies
CREATE POLICY "Users can view their own notes"
  ON notes FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own notes"
  ON notes FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own notes"
  ON notes FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own notes"
  ON notes FOR DELETE
  USING (auth.uid() = user_id);

-- Favorites policies
CREATE POLICY "Users can view their own favorites"
  ON user_favorites FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can add favorites"
  ON user_favorites FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can remove favorites"
  ON user_favorites FOR DELETE
  USING (auth.uid() = user_id);
```

## Usage Examples

### Example 1: Server-Side Data Fetching

```typescript
// app/my-notes/page.tsx
import { createClient } from '@/lib/supabase/server';

export default async function MyNotesPage() {
  const supabase = await createClient();

  const { data: { user } } = await supabase.auth.getUser();

  if (!user) {
    redirect('/login');
  }

  const { data: notes } = await supabase
    .from('notes')
    .select('*')
    .eq('user_id', user.id)
    .order('created_at', { ascending: false });

  return (
    <div>
      <h1>My Notes</h1>
      {notes?.map(note => (
        <div key={note.id}>{note.text}</div>
      ))}
    </div>
  );
}
```

### Example 2: Client-Side Mutations

```typescript
'use client';

import { createClient } from '@/lib/supabase/client';
import { useAuth } from '@/contexts/auth-context';

export function CreateNoteForm({ videoId }: { videoId: string }) {
  const { user } = useAuth();
  const supabase = createClient();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const text = formData.get('text') as string;

    const { error } = await supabase
      .from('notes')
      .insert({
        user_id: user!.id,
        video_id: videoId,
        source: 'custom',
        text
      });

    if (error) {
      console.error('Error creating note:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <textarea name="text" required />
      <button type="submit">Save Note</button>
    </form>
  );
}
```

### Example 3: API Route with Auth

```typescript
// app/api/notes/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@/lib/supabase/server';

export async function GET(request: NextRequest) {
  const supabase = await createClient();

  const { data: { user } } = await supabase.auth.getUser();

  if (!user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const videoId = request.nextUrl.searchParams.get('videoId');

  const { data: notes, error } = await supabase
    .from('notes')
    .select('*')
    .eq('user_id', user.id)
    .eq('video_id', videoId);

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }

  return NextResponse.json({ notes });
}

export async function POST(request: NextRequest) {
  const supabase = await createClient();

  const { data: { user } } = await supabase.auth.getUser();

  if (!user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const body = await request.json();

  const { data: note, error } = await supabase
    .from('notes')
    .insert({
      user_id: user.id,
      ...body
    })
    .select()
    .single();

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }

  return NextResponse.json({ note });
}
```

### Example 4: Real-time Subscriptions

```typescript
'use client';

import { useEffect, useState } from 'react';
import { createClient } from '@/lib/supabase/client';
import { useAuth } from '@/contexts/auth-context';

export function RealtimeNotes({ videoId }: { videoId: string }) {
  const [notes, setNotes] = useState<any[]>([]);
  const { user } = useAuth();
  const supabase = createClient();

  useEffect(() => {
    if (!user) return;

    // Fetch initial notes
    supabase
      .from('notes')
      .select('*')
      .eq('user_id', user.id)
      .eq('video_id', videoId)
      .then(({ data }) => setNotes(data || []));

    // Subscribe to changes
    const channel = supabase
      .channel('notes-changes')
      .on(
        'postgres_changes',
        {
          event: '*',
          schema: 'public',
          table: 'notes',
          filter: `user_id=eq.${user.id}`
        },
        (payload) => {
          if (payload.eventType === 'INSERT') {
            setNotes(prev => [...prev, payload.new]);
          } else if (payload.eventType === 'DELETE') {
            setNotes(prev => prev.filter(n => n.id !== payload.old.id));
          } else if (payload.eventType === 'UPDATE') {
            setNotes(prev => prev.map(n =>
              n.id === payload.new.id ? payload.new : n
            ));
          }
        }
      )
      .subscribe();

    return () => {
      channel.unsubscribe();
    };
  }, [user, videoId]);

  return (
    <div>
      {notes.map(note => (
        <div key={note.id}>{note.text}</div>
      ))}
    </div>
  );
}
```

### Example 5: Social Auth

```typescript
// Sign in with Google
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google',
  options: {
    redirectTo: `${window.location.origin}/auth/callback`
  }
});

// Sign in with GitHub
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'github',
  options: {
    redirectTo: `${window.location.origin}/auth/callback`
  }
});

// Auth callback route (app/auth/callback/route.ts)
import { createClient } from '@/lib/supabase/server';
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const code = searchParams.get('code');

  if (code) {
    const supabase = await createClient();
    await supabase.auth.exchangeCodeForSession(code);
  }

  return NextResponse.redirect(new URL('/', request.url));
}
```

## Best Practices

1. **Always use RLS** - Never trust client-side security
2. **Separate clients** - Use server client for sensitive operations
3. **Type your data** - Generate types from database schema
4. **Handle auth state** - Use context for user state
5. **Clean up subscriptions** - Unsubscribe in useEffect cleanup
6. **Use transactions** - For multi-table operations
7. **Index foreign keys** - Performance for joins and filters

## Common Pitfalls

1. **Forgetting RLS** - Data exposed without policies
2. **Using wrong client** - Server client in browser code
3. **Not handling errors** - Always check error objects
4. **Subscription leaks** - Forgetting to unsubscribe
5. **Missing indices** - Slow queries on large tables
6. **Hard-coded IDs** - Use auth.uid() in RLS policies

## Database Patterns

### Pattern 1: Soft Deletes

```sql
ALTER TABLE notes ADD COLUMN deleted_at TIMESTAMPTZ;

-- Policy for soft delete
CREATE POLICY "Users see non-deleted notes"
  ON notes FOR SELECT
  USING (auth.uid() = user_id AND deleted_at IS NULL);
```

### Pattern 2: Audit Trail

```sql
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  action TEXT NOT NULL,
  table_name TEXT NOT NULL,
  record_id UUID,
  old_data JSONB,
  new_data JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Pattern 3: Automatic Timestamps

```sql
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_notes_updated_at
  BEFORE UPDATE ON notes
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();
```

## Type Generation

```bash
# Install Supabase CLI
npm install -g supabase

# Generate types
supabase gen types typescript --project-id your-project-id > lib/database.types.ts
```

Usage:

```typescript
import { Database } from '@/lib/database.types';

type Note = Database['public']['Tables']['notes']['Row'];
type NoteInsert = Database['public']['Tables']['notes']['Insert'];
type NoteUpdate = Database['public']['Tables']['notes']['Update'];
```

## Next Steps

1. Set up database migrations
2. Configure storage buckets for files
3. Add email templates for auth
4. Set up Edge Functions for complex logic
5. Configure custom SMTP for emails
6. Add database backups

## Related Skills

- **Secure Next.js API Routes** - Protect Supabase endpoints
- **Type-Safe Form Validation** - Validate before database insert
- **Resilient Async Operations** - Handle Supabase calls safely

---

Built from production Supabase setup in [TLDW](https://github.com/vishalsachdev/tldw)
