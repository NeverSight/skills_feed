---
name: supabase-realtime
description: Subscribe to realtime changes in Supabase using WebSocket connections. Use for listening to database changes, presence tracking, and broadcast messaging.
---

# Supabase Realtime

## Overview

This skill provides guidance for working with Supabase Realtime features. Realtime allows you to listen to database changes, broadcast messages, and track presence using WebSocket connections.

**Note:** Realtime operations require WebSocket support, which is more complex in bash. This skill focuses on practical patterns and examples using available tools.

## Prerequisites

**Required environment variables:**
```bash
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_KEY="your-anon-or-service-role-key"
```

**Additional tools:**
- `websocat` or `wscat` for WebSocket connections
- `jq` for JSON processing

**Install websocat:**
```bash
# macOS
brew install websocat

# Linux
wget https://github.com/vi/websocat/releases/download/v1.12.0/websocat.x86_64-unknown-linux-musl
chmod +x websocat.x86_64-unknown-linux-musl
sudo mv websocat.x86_64-unknown-linux-musl /usr/local/bin/websocat
```

## WebSocket Connection

**Connect to Supabase Realtime:**
```bash
SUPABASE_URL="https://your-project.supabase.co"
SUPABASE_KEY="your-anon-key"

# Extract WebSocket URL (replace https:// with wss://)
WS_URL=$(echo "$SUPABASE_URL" | sed 's/https:/wss:/')

# Connect to realtime
websocat "${WS_URL}/realtime/v1/websocket?apikey=${SUPABASE_KEY}&vsn=1.0.0"
```

## Database Change Subscriptions

### Subscribe to Table Changes

**Listen to all changes on a table:**
```bash
#!/bin/bash

SUPABASE_URL="https://your-project.supabase.co"
SUPABASE_KEY="your-anon-key"
WS_URL=$(echo "$SUPABASE_URL" | sed 's/https:/wss:/')

# Create subscription message
SUB_MESSAGE='{
  "topic": "realtime:public:users",
  "event": "phx_join",
  "payload": {},
  "ref": "1"
}'

# Connect and subscribe
echo "$SUB_MESSAGE" | websocat "${WS_URL}/realtime/v1/websocket?apikey=${SUPABASE_KEY}&vsn=1.0.0"
```

**Subscribe to specific events:**
```bash
# Listen for INSERT events only
SUB_MESSAGE='{
  "topic": "realtime:public:users",
  "event": "phx_join",
  "payload": {
    "config": {
      "postgres_changes": [
        {
          "event": "INSERT",
          "schema": "public",
          "table": "users"
        }
      ]
    }
  },
  "ref": "1"
}'

echo "$SUB_MESSAGE" | websocat "${WS_URL}/realtime/v1/websocket?apikey=${SUPABASE_KEY}&vsn=1.0.0"
```

**Subscribe to UPDATE events:**
```bash
SUB_MESSAGE='{
  "topic": "realtime:public:products",
  "event": "phx_join",
  "payload": {
    "config": {
      "postgres_changes": [
        {
          "event": "UPDATE",
          "schema": "public",
          "table": "products"
        }
      ]
    }
  },
  "ref": "1"
}'
```

**Subscribe to DELETE events:**
```bash
SUB_MESSAGE='{
  "topic": "realtime:public:posts",
  "event": "phx_join",
  "payload": {
    "config": {
      "postgres_changes": [
        {
          "event": "DELETE",
          "schema": "public",
          "table": "posts"
        }
      ]
    }
  },
  "ref": "1"
}'
```

**Subscribe to all events (*, INSERT, UPDATE, DELETE):**
```bash
SUB_MESSAGE='{
  "topic": "realtime:public:orders",
  "event": "phx_join",
  "payload": {
    "config": {
      "postgres_changes": [
        {
          "event": "*",
          "schema": "public",
          "table": "orders"
        }
      ]
    }
  },
  "ref": "1"
}'
```

### Filter Subscriptions

**Listen to changes matching a filter:**
```bash
# Only listen to changes where status = 'active'
SUB_MESSAGE='{
  "topic": "realtime:public:users",
  "event": "phx_join",
  "payload": {
    "config": {
      "postgres_changes": [
        {
          "event": "*",
          "schema": "public",
          "table": "users",
          "filter": "status=eq.active"
        }
      ]
    }
  },
  "ref": "1"
}'
```

## Broadcast Messaging

### Send Broadcast Message

**Broadcast a message to a channel:**
```bash
#!/bin/bash

SUPABASE_URL="https://your-project.supabase.co"
SUPABASE_KEY="your-anon-key"
WS_URL=$(echo "$SUPABASE_URL" | sed 's/https:/wss:/')

# Join channel first
JOIN_MESSAGE='{
  "topic": "realtime:chat-room-1",
  "event": "phx_join",
  "payload": {
    "config": {
      "broadcast": {
        "self": true
      }
    }
  },
  "ref": "1"
}'

# Broadcast message
BROADCAST_MESSAGE='{
  "topic": "realtime:chat-room-1",
  "event": "broadcast",
  "payload": {
    "type": "message",
    "event": "new_message",
    "payload": {
      "user": "Alice",
      "message": "Hello, World!"
    }
  },
  "ref": "2"
}'

# Send messages
{
  echo "$JOIN_MESSAGE"
  sleep 1
  echo "$BROADCAST_MESSAGE"
} | websocat "${WS_URL}/realtime/v1/websocket?apikey=${SUPABASE_KEY}&vsn=1.0.0"
```

### Listen to Broadcast Messages

**Receive broadcast messages:**
```bash
# Join channel and listen
JOIN_MESSAGE='{
  "topic": "realtime:chat-room-1",
  "event": "phx_join",
  "payload": {
    "config": {
      "broadcast": {
        "self": false
      }
    }
  },
  "ref": "1"
}'

echo "$JOIN_MESSAGE" | websocat "${WS_URL}/realtime/v1/websocket?apikey=${SUPABASE_KEY}&vsn=1.0.0"
```

## Presence Tracking

### Track Presence

**Join channel with presence:**
```bash
PRESENCE_MESSAGE='{
  "topic": "realtime:lobby",
  "event": "phx_join",
  "payload": {
    "config": {
      "presence": {
        "key": "user-123"
      }
    }
  },
  "ref": "1"
}'

# Track presence state
TRACK_MESSAGE='{
  "topic": "realtime:lobby",
  "event": "presence",
  "payload": {
    "type": "presence",
    "event": "track",
    "payload": {
      "user_id": "123",
      "username": "Alice",
      "status": "online"
    }
  },
  "ref": "2"
}'
```

### Untrack Presence

**Leave presence:**
```bash
UNTRACK_MESSAGE='{
  "topic": "realtime:lobby",
  "event": "presence",
  "payload": {
    "type": "presence",
    "event": "untrack"
  },
  "ref": "3"
}'
```

## Practical Patterns

### Continuous Listener Script

```bash
#!/bin/bash
# listen-to-changes.sh

SUPABASE_URL="https://your-project.supabase.co"
SUPABASE_KEY="your-anon-key"
WS_URL=$(echo "$SUPABASE_URL" | sed 's/https:/wss:/')
TABLE="users"

echo "Listening for changes on $TABLE table..."

# Subscribe to changes
SUB_MESSAGE='{
  "topic": "realtime:public:'"$TABLE"'",
  "event": "phx_join",
  "payload": {
    "config": {
      "postgres_changes": [
        {
          "event": "*",
          "schema": "public",
          "table": "'"$TABLE"'"
        }
      ]
    }
  },
  "ref": "1"
}'

# Listen continuously
echo "$SUB_MESSAGE" | websocat "${WS_URL}/realtime/v1/websocket?apikey=${SUPABASE_KEY}&vsn=1.0.0" | \
while IFS= read -r line; do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $line" | jq '.'
done
```

### Process Changes with Handler

```bash
#!/bin/bash
# process-changes.sh

handle_insert() {
    local record="$1"
    echo "New record inserted:"
    echo "$record" | jq '.payload.record'

    # Your custom logic here
    # Example: Send notification, update cache, etc.
}

handle_update() {
    local old_record="$1"
    local new_record="$2"
    echo "Record updated:"
    echo "Old: $(echo "$old_record" | jq -c '.')"
    echo "New: $(echo "$new_record" | jq -c '.')"
}

handle_delete() {
    local record="$1"
    echo "Record deleted:"
    echo "$record" | jq '.payload.old_record'
}

# Listen and process
websocat "${WS_URL}/realtime/v1/websocket?apikey=${SUPABASE_KEY}&vsn=1.0.0" | \
while IFS= read -r line; do
    event_type=$(echo "$line" | jq -r '.payload.data.type // empty')

    case "$event_type" in
        "INSERT")
            handle_insert "$(echo "$line" | jq '.payload.data')"
            ;;
        "UPDATE")
            handle_update \
                "$(echo "$line" | jq '.payload.data.old_record')" \
                "$(echo "$line" | jq '.payload.data.record')"
            ;;
        "DELETE")
            handle_delete "$(echo "$line" | jq '.payload.data')"
            ;;
    esac
done
```

### Multi-Table Listener

```bash
#!/bin/bash
# listen-multiple-tables.sh

TABLES=("users" "posts" "comments")

for table in "${TABLES[@]}"; do
    (
        echo "Starting listener for $table"
        SUB_MESSAGE='{
          "topic": "realtime:public:'"$table"'",
          "event": "phx_join",
          "payload": {
            "config": {
              "postgres_changes": [{"event": "*", "schema": "public", "table": "'"$table"'"}]
            }
          },
          "ref": "1"
        }'

        echo "$SUB_MESSAGE" | websocat "${WS_URL}/realtime/v1/websocket?apikey=${SUPABASE_KEY}&vsn=1.0.0" | \
        while IFS= read -r line; do
            echo "[$table] $line"
        done
    ) &
done

wait
```

## Message Format

### Subscription Confirmation
```json
{
  "event": "phx_reply",
  "payload": {
    "response": {
      "postgres_changes": [
        {
          "id": "12345",
          "event": "*",
          "schema": "public",
          "table": "users"
        }
      ]
    },
    "status": "ok"
  },
  "ref": "1",
  "topic": "realtime:public:users"
}
```

### INSERT Event
```json
{
  "event": "postgres_changes",
  "payload": {
    "data": {
      "commit_timestamp": "2023-01-01T12:00:00Z",
      "record": {
        "id": 123,
        "name": "John Doe",
        "email": "john@example.com"
      },
      "schema": "public",
      "table": "users",
      "type": "INSERT"
    },
    "ids": [12345]
  },
  "topic": "realtime:public:users"
}
```

### UPDATE Event
```json
{
  "event": "postgres_changes",
  "payload": {
    "data": {
      "commit_timestamp": "2023-01-01T12:00:00Z",
      "old_record": {
        "id": 123,
        "name": "John Doe"
      },
      "record": {
        "id": 123,
        "name": "Jane Doe"
      },
      "schema": "public",
      "table": "users",
      "type": "UPDATE"
    }
  }
}
```

### DELETE Event
```json
{
  "event": "postgres_changes",
  "payload": {
    "data": {
      "commit_timestamp": "2023-01-01T12:00:00Z",
      "old_record": {
        "id": 123,
        "name": "John Doe"
      },
      "schema": "public",
      "table": "users",
      "type": "DELETE"
    }
  }
}
```

## Alternative: REST Polling

For simpler use cases where WebSockets are impractical, consider polling:

```bash
#!/bin/bash
# poll-changes.sh

source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

LAST_TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

while true; do
    # Get records created/updated since last check
    new_records=$(supabase_get "/rest/v1/users?updated_at=gt.${LAST_TIMESTAMP}&order=updated_at.asc")

    if [[ "$new_records" != "[]" ]]; then
        echo "New changes detected:"
        echo "$new_records" | jq '.'

        # Update timestamp
        LAST_TIMESTAMP=$(echo "$new_records" | jq -r '.[-1].updated_at')
    fi

    # Poll every 5 seconds
    sleep 5
done
```

## Realtime Configuration

**Enable Realtime in Supabase Dashboard:**
1. Go to Database > Replication
2. Enable replication for tables you want to listen to
3. Choose which events to publish (INSERT, UPDATE, DELETE)

**Row Level Security:**
Realtime respects RLS policies. Users only receive changes for rows they have access to.

## Limitations

- WebSocket connections require persistent connection management
- Bash is not ideal for WebSocket handling (consider Node.js/Python for production)
- Connection drops require reconnection logic
- Realtime is subject to connection limits based on your Supabase plan

## Use Cases

**Good for Realtime in bash:**
- Development/debugging tools
- Simple monitoring scripts
- Log streaming
- Testing realtime functionality

**Better in other languages:**
- Production chat applications
- Complex presence tracking
- Multi-channel coordination
- Auto-reconnection requirements

## API Documentation

Full Supabase Realtime documentation: https://supabase.com/docs/guides/realtime
