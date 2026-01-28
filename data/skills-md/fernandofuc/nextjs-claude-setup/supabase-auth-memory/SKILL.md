---
name: supabase-auth-memory
description: Standardize authentication and persistent memory storage using Supabase PostgreSQL. Use when building SaaS apps that need user auth, cross-device sync, and conversation history.
license: MIT
---

# Supabase Auth + Memory System

## Purpose
Implement user authentication and persistent AI conversation memory using Supabase as unified backend.

## When to Use
- Need user authentication in SaaS app
- Want conversation history across devices
- Building multi-tenant AI applications
- Need SQL-based memory for agents
- Syncing state between localStorage and cloud

## Quick Start

### Installation
```bash
npm install @supabase/supabase-js
npm install zustand zustand/middleware
```

### Environment Variables
```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key  # Backend only
```

## Database Schema

### Core Tables

```sql
-- Conversations table
CREATE TABLE conversations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  metadata JSONB DEFAULT '{}'::jsonb,

  -- Indexes
  CONSTRAINT conversations_user_id_fkey FOREIGN KEY (user_id)
    REFERENCES auth.users(id) ON DELETE CASCADE
);

CREATE INDEX idx_conversations_user ON conversations(user_id);
CREATE INDEX idx_conversations_updated ON conversations(updated_at DESC);

-- Messages table
CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
  role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
  content TEXT NOT NULL,
  tool_used TEXT,
  tool_result JSONB,
  reasoning_details JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

  -- Indexes
  CONSTRAINT messages_conversation_id_fkey FOREIGN KEY (conversation_id)
    REFERENCES conversations(id) ON DELETE CASCADE
);

CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_messages_created ON messages(created_at DESC);

-- User preferences (config storage)
CREATE TABLE user_preferences (
  user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  preferences JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Auto-update timestamp trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER conversations_updated_at
BEFORE UPDATE ON conversations
FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

### Row Level Security (RLS) Policies

```sql
-- Enable RLS
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;

-- Conversations policies
CREATE POLICY "Users can view own conversations"
ON conversations FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "Users can create own conversations"
ON conversations FOR INSERT
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own conversations"
ON conversations FOR UPDATE
USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own conversations"
ON conversations FOR DELETE
USING (auth.uid() = user_id);

-- Messages policies
CREATE POLICY "Users can view own messages"
ON messages FOR SELECT
USING (
  conversation_id IN (
    SELECT id FROM conversations WHERE user_id = auth.uid()
  )
);

CREATE POLICY "Users can create messages"
ON messages FOR INSERT
WITH CHECK (
  conversation_id IN (
    SELECT id FROM conversations WHERE user_id = auth.uid()
  )
);

-- User preferences policies
CREATE POLICY "Users can view own preferences"
ON user_preferences FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "Users can upsert own preferences"
ON user_preferences FOR INSERT
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own preferences"
ON user_preferences FOR UPDATE
USING (auth.uid() = user_id);
```

## Frontend Integration

### Supabase Client Setup
```typescript
// lib/supabase.ts
import { createClient } from '@supabase/supabase-js'

export const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)

// Get current user
export async function getCurrentUser() {
  const { data: { user } } = await supabase.auth.getUser()
  return user
}
```

### Zustand Store with Supabase Sync

```typescript
// stores/conversationStore.ts
import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'
import { supabase } from '@/lib/supabase'

interface Message {
  id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  tool_used?: string
  created_at: string
}

interface ConversationStore {
  // State
  messages: Message[]
  conversationId: string | null
  isSyncing: boolean

  // Local actions (optimistic UI)
  addMessage: (message: Omit<Message, 'id' | 'created_at'>) => void
  clearMessages: () => void

  // Supabase sync actions
  createConversation: (title: string) => Promise<string>
  loadConversation: (conversationId: string) => Promise<void>
  saveToSupabase: () => Promise<void>
  syncWithSupabase: () => Promise<void>
}

export const useConversationStore = create<ConversationStore>()(
  persist(
    (set, get) => ({
      // Initial state
      messages: [],
      conversationId: null,
      isSyncing: false,

      // Add message optimistically
      addMessage: (message) => {
        const newMessage: Message = {
          ...message,
          id: crypto.randomUUID(),
          created_at: new Date().toISOString()
        }

        set(state => ({
          messages: [...state.messages, newMessage]
        }))

        // Auto-save to Supabase (non-blocking)
        get().saveToSupabase()
      },

      // Clear messages
      clearMessages: () => set({ messages: [], conversationId: null }),

      // Create new conversation in Supabase
      createConversation: async (title) => {
        const user = await getCurrentUser()
        if (!user) throw new Error('Not authenticated')

        const { data, error } = await supabase
          .from('conversations')
          .insert({ user_id: user.id, title })
          .select()
          .single()

        if (error) throw error

        set({ conversationId: data.id })
        return data.id
      },

      // Load conversation from Supabase
      loadConversation: async (conversationId) => {
        set({ isSyncing: true })

        const { data, error } = await supabase
          .from('messages')
          .select('*')
          .eq('conversation_id', conversationId)
          .order('created_at', { ascending: true })

        if (error) throw error

        set({
          messages: data || [],
          conversationId,
          isSyncing: false
        })
      },

      // Save messages to Supabase
      saveToSupabase: async () => {
        const { messages, conversationId } = get()
        if (!conversationId) return

        set({ isSyncing: true })

        // Find new messages (not yet in Supabase)
        const newMessages = messages.filter(m => !m.id.startsWith('uuid'))

        if (newMessages.length > 0) {
          const { error } = await supabase
            .from('messages')
            .insert(
              newMessages.map(m => ({
                conversation_id: conversationId,
                role: m.role,
                content: m.content,
                tool_used: m.tool_used
              }))
            )

          if (error) console.error('Failed to save to Supabase:', error)
        }

        set({ isSyncing: false })
      },

      // Sync with Supabase (merge local + remote)
      syncWithSupabase: async () => {
        const { conversationId } = get()
        if (!conversationId) return

        await get().loadConversation(conversationId)
      }
    }),
    {
      name: 'conversation-storage',
      storage: createJSONStorage(() => localStorage),

      // Only persist specific fields
      partialize: (state) => ({
        messages: state.messages,
        conversationId: state.conversationId
      })
    }
  )
)
```

### User Preferences Store
```typescript
// stores/preferencesStore.ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { supabase, getCurrentUser } from '@/lib/supabase'

interface Preferences {
  theme: 'light' | 'dark'
  temperature: number
  model: string
  [key: string]: any
}

interface PreferencesStore {
  preferences: Preferences
  updatePreferences: (updates: Partial<Preferences>) => void
  syncWithSupabase: () => Promise<void>
}

export const usePreferencesStore = create<PreferencesStore>()(
  persist(
    (set, get) => ({
      preferences: {
        theme: 'dark',
        temperature: 0.7,
        model: 'openai/gpt-4o'
      },

      updatePreferences: (updates) => {
        set(state => ({
          preferences: { ...state.preferences, ...updates }
        }))

        // Auto-sync to Supabase
        get().syncWithSupabase()
      },

      syncWithSupabase: async () => {
        const user = await getCurrentUser()
        if (!user) return

        const { preferences } = get()

        await supabase
          .from('user_preferences')
          .upsert({
            user_id: user.id,
            preferences
          })
      }
    }),
    {
      name: 'user-preferences',
      onRehydrateStorage: () => (state) => {
        // Load from Supabase after localStorage rehydration
        state?.syncWithSupabase()
      }
    }
  )
)
```

## Real-time Subscriptions

```typescript
// hooks/useRealtimeMessages.ts
import { useEffect } from 'react'
import { supabase } from '@/lib/supabase'
import { useConversationStore } from '@/stores/conversationStore'

export function useRealtimeMessages(conversationId: string) {
  const addMessage = useConversationStore(state => state.addMessage)

  useEffect(() => {
    const channel = supabase
      .channel(`conversation:${conversationId}`)
      .on(
        'postgres_changes',
        {
          event: 'INSERT',
          schema: 'public',
          table: 'messages',
          filter: `conversation_id=eq.${conversationId}`
        },
        (payload) => {
          addMessage(payload.new as any)
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [conversationId, addMessage])
}
```

## Authentication Patterns

### Sign Up
```typescript
async function signUp(email: string, password: string) {
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
    options: {
      emailRedirectTo: `${window.location.origin}/auth/callback`
    }
  })

  if (error) throw error
  return data
}
```

### Sign In
```typescript
async function signIn(email: string, password: string) {
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password
  })

  if (error) throw error
  return data
}
```

### OAuth (Google, GitHub, etc.)
```typescript
async function signInWithOAuth(provider: 'google' | 'github') {
  const { data, error } = await supabase.auth.signInWithOAuth({
    provider,
    options: {
      redirectTo: `${window.location.origin}/auth/callback`
    }
  })

  if (error) throw error
  return data
}
```

## Supabase MCP Integration

### Setup (.mcp.json)
```json
{
  "mcpServers": {
    "supabase": {
      "url": "https://mcp.supabase.com/mcp?project_ref=YOUR_PROJECT_REF",
      "transport": "streamable-http",
      "auth": {
        "type": "oauth"
      }
    }
  }
}
```

### Available MCP Tools
- Create/manage projects
- Design tables & migrations
- Query data with SQL
- Generate TypeScript types
- Manage configurations

## Best Practices

1. **Security First**
   - Always enable RLS on all tables
   - Use service key only on server
   - Validate user ownership in policies

2. **Hybrid Storage**
   - localStorage for offline/instant UX
   - Supabase for cross-device sync
   - Background sync with debouncing

3. **Optimistic UI**
   - Update UI immediately
   - Sync to Supabase in background
   - Handle conflicts gracefully

4. **Real-time Updates**
   - Use subscriptions for collaboration
   - Clean up subscriptions on unmount
   - Debounce rapid updates

5. **Error Handling**
   - Retry failed syncs
   - Show sync status to user
   - Fallback to localStorage

6. **Performance**
   - Index frequently queried columns
   - Use JSONB for flexible metadata
   - Implement pagination for large datasets

## Common Patterns

### Multi-tenant SaaS
```sql
-- Add tenant isolation
CREATE TABLE organizations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE organization_members (
  organization_id UUID REFERENCES organizations(id),
  user_id UUID REFERENCES auth.users(id),
  role TEXT NOT NULL CHECK (role IN ('owner', 'admin', 'member')),
  PRIMARY KEY (organization_id, user_id)
);

-- Update RLS policies for organization isolation
CREATE POLICY "Organization members can view conversations"
ON conversations FOR SELECT
USING (
  user_id IN (
    SELECT user_id FROM organization_members
    WHERE organization_id = (
      SELECT organization_id FROM organization_members
      WHERE user_id = auth.uid()
    )
  )
);
```

## Resources

- [Supabase Docs](https://supabase.com/docs)
- [Supabase MCP Server](https://supabase.com/features/mcp-server)
- [RLS Policies Guide](https://supabase.com/docs/guides/auth/row-level-security)
- [Real-time Guide](https://supabase.com/docs/guides/realtime)
