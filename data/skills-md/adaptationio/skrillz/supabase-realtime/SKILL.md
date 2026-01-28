---
name: supabase-realtime
description: Supabase Realtime for live subscriptions, broadcasts, and presence. Use when implementing real-time features, live updates, chat, or online presence tracking.
---

# Supabase Realtime Skill

Live subscriptions, broadcasts, and presence.

## Quick Reference

| Feature | Use Case |
|---------|----------|
| Postgres Changes | Database row changes (INSERT, UPDATE, DELETE) |
| Broadcast | Client-to-client messaging (chat, notifications) |
| Presence | Track online users, typing indicators |

## Postgres Changes (Database Subscriptions)

### Enable Realtime on Table

```sql
-- Enable realtime for a table
ALTER PUBLICATION supabase_realtime ADD TABLE posts;

-- Enable for specific columns only
ALTER PUBLICATION supabase_realtime ADD TABLE posts (id, title, status);
```

### Subscribe to All Changes

```javascript
const channel = supabase
  .channel('posts-changes')
  .on(
    'postgres_changes',
    { event: '*', schema: 'public', table: 'posts' },
    (payload) => {
      console.log('Change:', payload)
      // payload.eventType: 'INSERT' | 'UPDATE' | 'DELETE'
      // payload.new: new row data
      // payload.old: previous row data (UPDATE/DELETE only)
    }
  )
  .subscribe()
```

### Subscribe to Specific Events

```javascript
// INSERT only
const channel = supabase
  .channel('new-posts')
  .on(
    'postgres_changes',
    { event: 'INSERT', schema: 'public', table: 'posts' },
    (payload) => console.log('New post:', payload.new)
  )
  .subscribe()

// UPDATE only
const channel = supabase
  .channel('updated-posts')
  .on(
    'postgres_changes',
    { event: 'UPDATE', schema: 'public', table: 'posts' },
    (payload) => console.log('Updated:', payload.old, '->', payload.new)
  )
  .subscribe()

// DELETE only
const channel = supabase
  .channel('deleted-posts')
  .on(
    'postgres_changes',
    { event: 'DELETE', schema: 'public', table: 'posts' },
    (payload) => console.log('Deleted:', payload.old)
  )
  .subscribe()
```

### Filter by Column Value

```javascript
// Only changes where status = 'published'
const channel = supabase
  .channel('published-posts')
  .on(
    'postgres_changes',
    {
      event: '*',
      schema: 'public',
      table: 'posts',
      filter: 'status=eq.published'
    },
    (payload) => console.log('Published post change:', payload)
  )
  .subscribe()

// Filter by user_id
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
    (payload) => console.log('User post change:', payload)
  )
  .subscribe()
```

### Multiple Listeners

```javascript
const channel = supabase
  .channel('all-changes')
  .on(
    'postgres_changes',
    { event: 'INSERT', schema: 'public', table: 'posts' },
    (payload) => console.log('New post:', payload.new)
  )
  .on(
    'postgres_changes',
    { event: 'INSERT', schema: 'public', table: 'comments' },
    (payload) => console.log('New comment:', payload.new)
  )
  .subscribe()
```

## Broadcast (Client-to-Client)

### Send Broadcast

```javascript
const channel = supabase.channel('room-1')

// Subscribe first
channel.subscribe((status) => {
  if (status === 'SUBSCRIBED') {
    // Send message
    channel.send({
      type: 'broadcast',
      event: 'message',
      payload: { text: 'Hello everyone!' }
    })
  }
})
```

### Receive Broadcast

```javascript
const channel = supabase
  .channel('room-1')
  .on('broadcast', { event: 'message' }, (payload) => {
    console.log('Received:', payload.payload)
  })
  .subscribe()
```

### Chat Example

```javascript
const roomId = 'chat-room-123'
const channel = supabase.channel(roomId)

// Listen for messages
channel
  .on('broadcast', { event: 'new-message' }, ({ payload }) => {
    console.log(`${payload.username}: ${payload.message}`)
  })
  .subscribe()

// Send message function
function sendMessage(username, message) {
  channel.send({
    type: 'broadcast',
    event: 'new-message',
    payload: { username, message, timestamp: new Date().toISOString() }
  })
}
```

## Presence (Online Users)

### Track User Presence

```javascript
const channel = supabase.channel('online-users')

// Track current user
channel.subscribe(async (status) => {
  if (status === 'SUBSCRIBED') {
    await channel.track({
      user_id: currentUser.id,
      username: currentUser.name,
      online_at: new Date().toISOString()
    })
  }
})
```

### Listen for Presence Changes

```javascript
const channel = supabase
  .channel('online-users')
  .on('presence', { event: 'sync' }, () => {
    // Get all online users
    const state = channel.presenceState()
    console.log('Online users:', state)
  })
  .on('presence', { event: 'join' }, ({ key, newPresences }) => {
    console.log('User joined:', newPresences)
  })
  .on('presence', { event: 'leave' }, ({ key, leftPresences }) => {
    console.log('User left:', leftPresences)
  })
  .subscribe()
```

### Get Online Users

```javascript
// After subscribing
const state = channel.presenceState()

// state is an object keyed by user key
// { "user-123": [{ user_id: "...", username: "...", online_at: "..." }] }

const onlineUsers = Object.values(state).flat()
console.log('Online count:', onlineUsers.length)
```

### Untrack (Go Offline)

```javascript
await channel.untrack()
```

## React Patterns

### Database Subscription Hook

```javascript
import { useEffect, useState } from 'react'

function usePosts() {
  const [posts, setPosts] = useState([])

  useEffect(() => {
    // Initial fetch
    supabase.from('posts').select('*').then(({ data }) => {
      setPosts(data || [])
    })

    // Subscribe to changes
    const channel = supabase
      .channel('posts-realtime')
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table: 'posts' },
        (payload) => {
          if (payload.eventType === 'INSERT') {
            setPosts(prev => [...prev, payload.new])
          } else if (payload.eventType === 'UPDATE') {
            setPosts(prev =>
              prev.map(post =>
                post.id === payload.new.id ? payload.new : post
              )
            )
          } else if (payload.eventType === 'DELETE') {
            setPosts(prev =>
              prev.filter(post => post.id !== payload.old.id)
            )
          }
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [])

  return posts
}
```

### Presence Hook

```javascript
import { useEffect, useState } from 'react'

function useOnlineUsers(roomId) {
  const [onlineUsers, setOnlineUsers] = useState([])

  useEffect(() => {
    const channel = supabase
      .channel(`room-${roomId}`)
      .on('presence', { event: 'sync' }, () => {
        const state = channel.presenceState()
        setOnlineUsers(Object.values(state).flat())
      })
      .subscribe(async (status) => {
        if (status === 'SUBSCRIBED') {
          await channel.track({
            user_id: currentUser.id,
            username: currentUser.name
          })
        }
      })

    return () => {
      channel.untrack()
      supabase.removeChannel(channel)
    }
  }, [roomId])

  return onlineUsers
}
```

## Subscription Status

```javascript
const channel = supabase
  .channel('my-channel')
  .on('postgres_changes', { ... }, callback)
  .subscribe((status, err) => {
    if (status === 'SUBSCRIBED') {
      console.log('Connected!')
    } else if (status === 'CLOSED') {
      console.log('Disconnected')
    } else if (status === 'CHANNEL_ERROR') {
      console.error('Error:', err)
    }
  })
```

### Status Values

- `SUBSCRIBED` - Successfully connected
- `TIMED_OUT` - Connection timed out
- `CLOSED` - Channel closed
- `CHANNEL_ERROR` - Error occurred

## Cleanup

### Remove Single Channel

```javascript
await supabase.removeChannel(channel)
```

### Remove All Channels

```javascript
await supabase.removeAllChannels()
```

## Access Control

### Enable RLS for Realtime

Realtime respects RLS policies. Users only see changes they have access to.

```sql
-- Policy for realtime
CREATE POLICY "Users see own posts realtime"
ON posts FOR SELECT
TO authenticated
USING (auth.uid() = user_id);
```

### Broadcast Authorization

For broadcast and presence, use RLS on `realtime.messages`:

```sql
-- Create policy for channel access
CREATE POLICY "Channel access"
ON realtime.messages
FOR ALL
TO authenticated
USING (
  realtime.topic() LIKE 'room-' || auth.uid()::text || '%'
);
```

## Old Record Access (REPLICA IDENTITY)

To access `old` record on UPDATE/DELETE:

```sql
-- Enable full replica identity
ALTER TABLE posts REPLICA IDENTITY FULL;
```

## Filter Operators

| Operator | Example |
|----------|---------|
| `eq` | `filter: 'status=eq.active'` |
| `neq` | `filter: 'status=neq.deleted'` |
| `in` | `filter: 'status=in.(active,pending)'` |

**Note**: Only 1 filter per subscription is supported.

## References

- [realtime-patterns.md](references/realtime-patterns.md) - Common patterns
