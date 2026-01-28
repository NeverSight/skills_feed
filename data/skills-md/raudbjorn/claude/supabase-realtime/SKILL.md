---
name: supabase-realtime
description: Comprehensive guide for implementing Supabase Realtime features with best practices, scalable patterns, and migration strategies. Use when building realtime features in Supabase applications including messaging, notifications, presence, live updates, collaborative features, or migrating from postgres_changes to broadcast. Covers client setup, database triggers with realtime.broadcast_changes, RLS authorization, naming conventions, and performance optimization.
---

# Supabase Realtime

Expert implementation guide for Supabase Realtime features focusing on scalable patterns and best practices.

## Core Principles

**Always use `broadcast` over `postgres_changes`** - postgres_changes is single-threaded and doesn't scale. Use broadcast with database triggers for all database change notifications.

**Use dedicated topics** - Never broadcast to global topics. Use granular patterns like `room:123:messages`, `user:456:notifications`.

**Private channels by default** - Set `private: true` for all database-triggered channels. Enable private-only mode in production.

## Quick Reference

### Naming Conventions
- **Topics**: `scope:entity:id` (e.g., `room:123:messages`)
- **Events**: `entity_action` in snake_case (e.g., `message_created`)

### Client Setup Pattern
```javascript
const channel = supabase.channel('room:123:messages', {
  config: { 
    broadcast: { self: true, ack: true },
    private: true  // Required for RLS
  }
})

// Set auth before subscribing
await supabase.realtime.setAuth()

channel
  .on('broadcast', { event: 'message_created' }, handler)
  .subscribe((status, err) => {
    if (status === 'SUBSCRIBED') console.log('Connected')
  })

// Cleanup
supabase.removeChannel(channel)
```

### Database Trigger Pattern
```sql
-- Use realtime.broadcast_changes for database events
CREATE OR REPLACE FUNCTION notify_table_changes()
RETURNS TRIGGER AS $$
BEGIN
  PERFORM realtime.broadcast_changes(
    TG_TABLE_NAME || ':' || COALESCE(NEW.id, OLD.id)::text,
    TG_OP,
    TG_OP,
    TG_TABLE_NAME,
    TG_TABLE_SCHEMA,
    NEW,
    OLD
  );
  RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER messages_broadcast_trigger
  AFTER INSERT OR UPDATE OR DELETE ON messages
  FOR EACH ROW EXECUTE FUNCTION notify_table_changes();
```

### RLS Authorization
```sql
-- Required for private channels
CREATE POLICY "room_members_can_read" ON realtime.messages
FOR SELECT TO authenticated
USING (
  topic LIKE 'room:%' AND
  EXISTS (
    SELECT 1 FROM room_members
    WHERE user_id = auth.uid()
    AND room_id = SPLIT_PART(topic, ':', 2)::uuid
  )
);

-- Required index for performance
CREATE INDEX idx_room_members_user_room ON room_members(user_id, room_id);
```

## Implementation Checklist
- ✅ Use `broadcast` not `postgres_changes`
- ✅ Dedicated topics per room/user/entity
- ✅ Set `private: true` for database triggers
- ✅ Create indexes for all RLS policy columns
- ✅ Include cleanup/unsubscribe logic
- ✅ Check channel state before subscribing
- ✅ Use consistent naming conventions

## Scripts

- **[scripts/create_broadcast_trigger.sql](scripts/create_broadcast_trigger.sql)** - Generic broadcast trigger function
- **[scripts/migrate_from_postgres_changes.sql](scripts/migrate_from_postgres_changes.sql)** - Migration helper script

## Advanced Topics

- **Framework Integration**: See [references/framework_patterns.md](references/framework_patterns.md)
- **Performance Optimization**: See [references/performance_scaling.md](references/performance_scaling.md)
- **Migration Guide**: See [references/migration_guide.md](references/migration_guide.md)
