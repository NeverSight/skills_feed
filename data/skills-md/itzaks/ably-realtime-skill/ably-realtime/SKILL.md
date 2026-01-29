---
name: ably-realtime
description: Professional guide to Ably Realtime for building real-time React/TypeScript applications with pub-sub messaging, channels, presence tracking, Spaces (collaborative UI), LiveObjects (shared state), Chat SDK (complete messaging), and LiveSync (database synchronization). Use when working with Ably, real-time messaging, WebSockets, pub-sub, channels, presence, collaborative features, live cursors, avatar stacks, component locking, shared state, conflict-free updates, chat rooms, typing indicators, message reactions, database sync, outbox pattern, useChannel, usePresence, useSpace, useMembers, useCursors, useMessages, useTyping, LiveCounter, LiveMap, or integrating Ably with Neon/PostgreSQL for persistent real-time data.
---

# Ably Realtime for React/TypeScript

Ably Realtime is a platform for building scalable real-time applications with pub-sub messaging, presence tracking, collaborative features, chat, and database synchronization.

## When to Use Each Feature

Ably provides different abstractions for different real-time use cases:

- **Channels (Core Pub-Sub)**: Custom real-time messaging, notifications, live updates, event broadcasting
- **Spaces**: Participant state in collaborative UIs (live cursors, avatar stacks, user locations, component locking)
- **LiveObjects**: Application state synchronization (counters, voting, shared configurations, game state) with conflict-free updates
- **Chat SDK**: Complete messaging apps (1:1 chat, group conversations, livestream chat, support tickets)
- **LiveSync**: Database-to-client synchronization (broadcasting Postgres changes, outbox pattern, transactional consistency)

## Installation

```bash
# Core Ably (required)
npm install ably

# Additional packages (install as needed)
npm install @ably/spaces           # For Spaces
npm install @ably/chat             # For Chat SDK
npm install @ably-labs/models      # For LiveSync Models SDK
```

## Basic Setup

All Ably features require a Realtime client. Create the client outside React components to prevent reconnections on re-renders:

```typescript
// main.tsx or app.tsx
import * as Ably from 'ably';
import { AblyProvider } from 'ably/react';

// Create client OUTSIDE components
const realtimeClient = new Ably.Realtime({
  key: import.meta.env.VITE_ABLY_API_KEY,
  clientId: 'unique-user-id', // Required for Spaces and Chat
});

function Root() {
  return (
    <AblyProvider client={realtimeClient}>
      <App />
    </AblyProvider>
  );
}
```

For production applications, use token authentication instead of API keys. See [references/auth-security.md](references/auth-security.md).

## Quick Start: Channels (Core Pub-Sub)

Basic real-time messaging with channels:

```typescript
import { ChannelProvider, useChannel } from 'ably/react';

// Wrap with ChannelProvider
<ChannelProvider channelName="notifications">
  <NotificationComponent />
</ChannelProvider>

// Use in component
function NotificationComponent() {
  const { publish } = useChannel('notifications', (message) => {
    console.log('Received:', message.data);
    // Update local state with message
  });

  const sendNotification = () => {
    publish('alert', { text: 'New update!', timestamp: Date.now() });
  };

  return <button onClick={sendNotification}>Send</button>;
}
```

For detailed channel operations, presence tracking, and history, see [references/channels/](references/channels/).

## Quick Start: Spaces (Collaborative UI)

Track participant state for collaborative features:

```typescript
import Spaces from '@ably/spaces';
import { SpacesProvider, SpaceProvider, useMembers, useCursors } from '@ably/spaces/react';

// Setup (in root)
const spaces = new Spaces(realtimeClient);

<SpacesProvider client={spaces}>
  <SpaceProvider name="my-collaborative-space">
    <CollaborativeEditor />
  </SpaceProvider>
</SpacesProvider>

// Avatar stack
function AvatarStack() {
  const { self, others } = useMembers();

  return (
    <div>
      <Avatar user={self} />
      {others.map(member => (
        <Avatar key={member.connectionId} user={member} />
      ))}
    </div>
  );
}

// Live cursors
function CursorTracking() {
  const { set } = useCursors((update) => {
    // Render other users' cursors
    renderCursor(update.connectionId, update.position);
  });

  useEffect(() => {
    const handleMove = (e: MouseEvent) => {
      set({ position: { x: e.clientX, y: e.clientY } });
    };
    window.addEventListener('mousemove', handleMove);
    return () => window.removeEventListener('mousemove', handleMove);
  }, [set]);

  return <canvas id="cursor-layer" />;
}
```

For locations, component locking, and advanced patterns, see [references/spaces/](references/spaces/).

## Quick Start: LiveObjects (Shared State)

⚠️ **Public Preview**: LiveObjects API may change before general availability.

Conflict-free shared state synchronization:

```typescript
import { LiveCounter, LiveMap } from "ably/liveobjects";

async function setupSharedState() {
  const channel = realtimeClient.channels.get("game:lobby-1");
  const gameState = await channel.object.get();

  // Create shared counter
  await gameState.set("score", LiveCounter.create(0));

  // Create shared map
  await gameState.set(
    "players",
    LiveMap.create({
      player1: { name: "Alice", ready: false },
      player2: { name: "Bob", ready: false },
    }),
  );

  // Subscribe to changes
  gameState.get("score").subscribe(() => {
    console.log("Score:", gameState.get("score").value());
  });

  // Update values
  await gameState.get("score").increment(10);
  await gameState.get("players").set("player1", { name: "Alice", ready: true });
}
```

React integration:

```typescript
function GameLobby() {
  const [score, setScore] = useState(0);
  const [players, setPlayers] = useState({});

  useEffect(() => {
    let gameState: any;

    async function init() {
      const channel = realtimeClient.channels.get('game:lobby-1');
      gameState = await channel.object.get();

      // Subscribe to updates
      gameState.get('score').subscribe(() => {
        setScore(gameState.get('score').value());
      });

      gameState.get('players').subscribe(() => {
        setPlayers(gameState.get('players').value());
      });
    }

    init();

    return () => {
      // Cleanup subscriptions
    };
  }, []);

  return (
    <div>
      <h2>Score: {score}</h2>
      {Object.entries(players).map(([id, player]: [string, any]) => (
        <div key={id}>{player.name} - {player.ready ? '✓' : '...'}</div>
      ))}
    </div>
  );
}
```

For LiveMap batch operations, composability, and detailed API, see [references/liveobjects/](references/liveobjects/).

## Quick Start: Chat SDK

Purpose-built chat with rooms, messages, typing indicators, and reactions:

```typescript
import { ChatClient } from '@ably/chat';
import { ChatClientProvider, ChatRoomProvider, useMessages, useTyping } from '@ably/chat/react';

// Setup (in root)
const chatClient = new ChatClient(realtimeClient);

<ChatClientProvider client={chatClient}>
  <ChatRoomProvider name="support:ticket-123">
    <ChatRoom />
  </ChatRoomProvider>
</ChatClientProvider>

// Chat component
function ChatRoom() {
  const [messages, setMessages] = useState<Message[]>([]);
  const { currentlyTyping, keystroke } = useTyping();

  const { send, getPreviousMessages } = useMessages({
    listener: (event) => {
      if (event.type === 'created') {
        setMessages(prev => [...prev, event.message]);
      }
    }
  });

  useEffect(() => {
    // Load history
    getPreviousMessages({ limit: 50 }).then(result => {
      setMessages(result.items.reverse());
    });
  }, []);

  const handleSend = (text: string) => {
    send({ text });
  };

  const handleTyping = () => {
    keystroke(); // Triggers typing indicator
  };

  return (
    <div>
      <MessageList messages={messages} />
      {currentlyTyping.length > 0 && (
        <TypingIndicator users={currentlyTyping} />
      )}
      <MessageInput onSend={handleSend} onKeyPress={handleTyping} />
    </div>
  );
}
```

For message updates/deletes, reactions, presence, and room lifecycle, see [references/chat/](references/chat/).

## Quick Start: LiveSync (Database Sync)

Broadcast database changes from PostgreSQL/Neon to clients:

**Backend (Database + Outbox)**:

```sql
-- Outbox table for change events
CREATE TABLE outbox (
  sequence_id serial PRIMARY KEY,
  mutation_id TEXT NOT NULL,
  channel TEXT NOT NULL,
  name TEXT NOT NULL,
  data JSONB,
  processed BOOLEAN DEFAULT false
);

-- Trigger to notify on changes
CREATE FUNCTION outbox_notify() RETURNS trigger AS $$
BEGIN
  PERFORM pg_notify('ably_adbc', '');
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER outbox_trigger
  AFTER INSERT ON outbox
  FOR EACH STATEMENT
  EXECUTE PROCEDURE outbox_notify();
```

```typescript
// API route - transactional write
export async function POST(req: Request) {
  const { documentId, content } = await req.json();

  await db.transaction(async (trx) => {
    // Update application data
    await trx("documents")
      .where({ id: documentId })
      .update({ content, updated_at: new Date() });

    // Insert change event
    await trx("outbox").insert({
      mutation_id: crypto.randomUUID(),
      channel: `document:${documentId}`,
      name: "document.updated",
      data: { id: documentId, content },
    });
  });

  return Response.json({ success: true });
}
```

**Frontend (Subscribe to Changes)**:

```typescript
function DocumentEditor({ documentId }: { documentId: string }) {
  const [content, setContent] = useState('');

  const { channel } = useChannel(`document:${documentId}`, (message) => {
    if (message.name === 'document.updated') {
      setContent(message.data.content);
    }
  });

  useEffect(() => {
    // Load initial state
    fetch(`/api/documents/${documentId}`)
      .then(r => r.json())
      .then(doc => setContent(doc.content));
  }, [documentId]);

  return <textarea value={content} onChange={(e) => setContent(e.target.value)} />;
}
```

For Models SDK with optimistic updates, integration setup, and advanced patterns, see [references/livesync/](references/livesync/).

## Common Patterns

### Pattern: Load History Before Subscribing

```typescript
function ChatWithHistory() {
  const [messages, setMessages] = useState<any[]>([]);

  const { channel } = useChannel('chat', (message) => {
    setMessages(prev => [...prev, message]);
  });

  useEffect(() => {
    async function loadHistory() {
      const history = await channel.history({ limit: 50 });
      setMessages(history.items.reverse());
    }
    loadHistory();
  }, [channel]);

  return <MessageList messages={messages} />;
}
```

### Pattern: Optimistic Updates with Confirmation

```typescript
function OptimisticComment({ postId }: { postId: string }) {
  const [comments, setComments] = useState<Comment[]>([]);
  const pendingMutations = useRef(new Map());

  useChannel(`post:${postId}`, (message) => {
    const mutationId = message.data.mutation_id;

    // Remove optimistic entry, add confirmed
    if (pendingMutations.current.has(mutationId)) {
      setComments(prev => {
        const withoutOptimistic = prev.filter(c => c.id !== mutationId);
        return [...withoutOptimistic, message.data];
      });
      pendingMutations.current.delete(mutationId);
    } else {
      setComments(prev => [...prev, message.data]);
    }
  });

  const addComment = async (text: string) => {
    const mutationId = crypto.randomUUID();
    const optimistic = { id: mutationId, text, pending: true };

    // Add optimistically
    setComments(prev => [...prev, optimistic]);
    pendingMutations.current.set(mutationId, optimistic);

    // Send to backend
    await fetch('/api/comments', {
      method: 'POST',
      body: JSON.stringify({ mutationId, postId, text })
    });
  };

  return <CommentList comments={comments} onAdd={addComment} />;
}
```

### Pattern: Presence with Profile Data

```typescript
import { usePresence, usePresenceListener } from 'ably/react';

function OnlineUsers() {
  usePresence('room', {
    username: 'Alice',
    avatar: '/avatars/alice.jpg',
    status: 'active'
  });

  const { presenceData } = usePresenceListener('room');

  return (
    <div>
      <h3>Online ({presenceData.length})</h3>
      {presenceData.map(member => (
        <div key={member.connectionId}>
          <img src={member.data?.avatar} alt={member.data?.username} />
          <span>{member.data?.username}</span>
          <span>{member.data?.status}</span>
        </div>
      ))}
    </div>
  );
}
```

### Pattern: Connection State Monitoring

```typescript
import { useConnectionStateListener, useAbly } from 'ably/react';

function ConnectionStatus() {
  const ably = useAbly();
  const [state, setState] = useState(ably.connection.state);
  const [error, setError] = useState<string | null>(null);

  useConnectionStateListener((stateChange) => {
    setState(stateChange.current);

    if (stateChange.current === 'failed' || stateChange.current === 'suspended') {
      setError(stateChange.reason?.message || 'Connection issue');
    } else {
      setError(null);
    }
  });

  return (
    <div className={`status-${state}`}>
      {state === 'connected' ? '🟢' : '🔴'} {state}
      {error && <span>{error}</span>}
    </div>
  );
}
```

## TypeScript Types

Ably provides comprehensive TypeScript definitions. Import types as needed:

```typescript
import type * as Ably from "ably";
import type { Message } from "@ably/chat";
import type { SpaceMember, CursorUpdate } from "@ably/spaces";

const handleMessage = (msg: Ably.Message) => {
  console.log(msg.name, msg.data, msg.timestamp);
};

const handleCursor = (update: CursorUpdate) => {
  const position: { x: number; y: number } = update.position;
};
```

## Progressive References

For detailed documentation on specific features:

- **[Core Channels](references/channels/)** - Channel operations, presence, history, connection management
- **[Spaces](references/spaces/)** - Setup, React hooks (useMembers, useCursors, useLocations, useLocks), patterns
- **[LiveObjects](references/liveobjects/)** - Overview, API reference (LiveCounter, LiveMap), composability, batch operations
- **[Chat SDK](references/chat/)** - Setup, React hooks (useMessages, useTyping, useRoomReactions), message CRUD, features
- **[LiveSync](references/livesync/)** - Outbox pattern, integration setup, Models SDK, optimistic updates, React patterns
- **[Auth & Security](references/auth-security.md)** - Token authentication, clientId, capabilities, production best practices

## Troubleshooting

### Connection limit exceeded

Each Realtime client instance creates a connection. Create the client once outside React components:

```typescript
// ❌ Wrong - creates new connection on every render
function App() {
  const client = new Ably.Realtime({ key });
  return <AblyProvider client={client}>...</AblyProvider>;
}

// ✅ Correct - single connection
const client = new Ably.Realtime({ key });
function App() {
  return <AblyProvider client={client}>...</AblyProvider>;
}
```

### Provider nesting issues

Ensure correct provider hierarchy:

```typescript
// For Spaces
<AblyProvider client={realtimeClient}>
  <SpacesProvider client={spacesClient}>
    <SpaceProvider name="space-name">
      {/* Your components */}
    </SpaceProvider>
  </SpacesProvider>
</AblyProvider>

// For Chat
<AblyProvider client={realtimeClient}>
  <ChatClientProvider client={chatClient}>
    <ChatRoomProvider name="room-name">
      {/* Your components */}
    </ChatRoomProvider>
  </ChatClientProvider>
</AblyProvider>
```

### Channel not receiving messages

1. Check channel name matches exactly (case-sensitive)
2. Verify API key has required capabilities
3. Ensure `clientId` is set when using presence or Chat
4. Check connection state with `useConnectionStateListener`

### LiveObjects not syncing

1. Verify LiveObjects is enabled in your Ably app (Dashboard → Settings)
2. Check channel is attached: `channel.state === 'attached'`
3. Ensure proper await on async operations
4. LiveObjects requires Ably protocol version 2 (set automatically)

### Chat messages not persisting

Chat messages persist for 30 days by default. Check:

1. Ably app has Chat enabled
2. Room is properly attached before sending
3. Message has required fields (text or metadata)
4. API key has publish capability

## Best Practices

1. **Single Realtime Client**: Create one client instance per application, share across components
2. **ClientId for Identity**: Always set `clientId` when using Spaces or Chat for user identification
3. **Channel Naming**: Use hierarchical names for organization: `post:123`, `room:lobby:1`, `user:alice:notifications`
4. **Presence Data**: Keep presence data small (under 1KB) for efficiency
5. **History Limits**: Load only necessary history to reduce bandwidth and latency
6. **Error Handling**: Monitor connection state and handle disconnections gracefully
7. **Token Auth in Production**: Never expose API keys in client code, use token authentication
8. **Cleanup**: Unsubscribe from channels and detach when components unmount (hooks handle this automatically)
9. **LiveObjects Conflicts**: Design for eventual consistency, use LiveCounter for numeric aggregations
10. **LiveSync Transactions**: Always write to outbox within same transaction as application data

## Additional Resources

- [Ably Documentation](https://ably.com/docs)
- [React Hooks Documentation](https://ably.com/docs/getting-started/react)
- [Spaces Documentation](https://ably.com/docs/products/spaces)
- [Chat SDK Documentation](https://ably.com/docs/products/chat)
- [LiveObjects Documentation](https://ably.com/docs/products/liveobjects)
- [LiveSync Documentation](https://ably.com/docs/livesync)
