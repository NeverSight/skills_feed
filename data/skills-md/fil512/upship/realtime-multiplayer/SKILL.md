---
name: realtime-multiplayer
description: Real-time multiplayer game networking with Socket.io. Use when implementing WebSocket connections, game state synchronization, room management, reconnection handling, or optimistic updates. Covers latency compensation and conflict resolution.
---

# Real-Time Multiplayer Skill

## Overview

This skill provides expertise for building real-time multiplayer games using WebSockets and Socket.io. It covers connection management, state synchronization, latency handling, and the specific challenges of turn-based games with real-time updates.

## Core Architecture

### Client-Server Model for Games

```
┌─────────────┐     WebSocket      ┌─────────────┐
│   Client    │◄──────────────────►│   Server    │
│  (Browser)  │                    │  (Node.js)  │
└─────────────┘                    └─────────────┘
      │                                   │
      ▼                                   ▼
┌─────────────┐                    ┌─────────────┐
│  Local UI   │                    │ Game State  │
│   State     │                    │  (Source    │
│  (Optimistic)                    │   of Truth) │
└─────────────┘                    └─────────────┘
```

**Key Principle:** The server is the authoritative source of truth. Clients can have optimistic local state for responsiveness, but server state always wins on conflict.

### Socket.io Setup Pattern

```javascript
// Server setup
const io = require('socket.io')(server, {
  cors: { origin: process.env.CLIENT_URL },
  pingTimeout: 60000,
  pingInterval: 25000
});

io.on('connection', (socket) => {
  // Join game room
  socket.on('join-game', ({ gameId, playerId }) => {
    socket.join(`game:${gameId}`);
    socket.gameId = gameId;
    socket.playerId = playerId;
  });

  // Handle game actions
  socket.on('game-action', async (action) => {
    const result = await processAction(socket.gameId, socket.playerId, action);
    if (result.success) {
      // Broadcast to all players in game
      io.to(`game:${socket.gameId}`).emit('state-update', result.newState);
    } else {
      // Send error only to acting player
      socket.emit('action-error', result.error);
    }
  });

  // Handle disconnection
  socket.on('disconnect', () => {
    handlePlayerDisconnect(socket.gameId, socket.playerId);
  });
});
```

## Room Management

### Game Rooms Pattern

Each game instance should be a Socket.io room:

```javascript
// Room naming convention
const roomName = `game:${gameId}`;

// Player joins game
socket.join(roomName);

// Broadcast to all players in game
io.to(roomName).emit('event', data);

// Send to specific player
io.to(playerSocketId).emit('private-event', data);

// Send to all except sender
socket.to(roomName).emit('event', data);
```

### Player Presence Tracking

```javascript
const gamePresence = new Map(); // gameId -> Set of playerIds

function trackPresence(gameId, playerId, isOnline) {
  if (!gamePresence.has(gameId)) {
    gamePresence.set(gameId, new Set());
  }

  const players = gamePresence.get(gameId);
  if (isOnline) {
    players.add(playerId);
  } else {
    players.delete(playerId);
  }

  // Notify other players
  io.to(`game:${gameId}`).emit('presence-update', {
    playerId,
    isOnline,
    onlinePlayers: Array.from(players)
  });
}
```

## State Synchronization

### Event Types

Define clear event categories:

```javascript
// Server -> Client events
const ServerEvents = {
  STATE_SYNC: 'state-sync',       // Full state (on join/reconnect)
  STATE_UPDATE: 'state-update',   // Partial state change
  ACTION_RESULT: 'action-result', // Response to player action
  PLAYER_JOINED: 'player-joined',
  PLAYER_LEFT: 'player-left',
  GAME_STARTED: 'game-started',
  TURN_CHANGED: 'turn-changed',
  GAME_ENDED: 'game-ended'
};

// Client -> Server events
const ClientEvents = {
  JOIN_GAME: 'join-game',
  LEAVE_GAME: 'leave-game',
  GAME_ACTION: 'game-action',
  REQUEST_SYNC: 'request-sync',
  PING: 'ping'
};
```

### Delta Updates vs Full Sync

```javascript
// Send delta updates for efficiency
function sendDelta(gameId, changes) {
  io.to(`game:${gameId}`).emit('state-update', {
    type: 'delta',
    changes,
    version: gameState.version
  });
}

// Send full state on reconnect or desync
function sendFullSync(socket, gameState) {
  socket.emit('state-sync', {
    type: 'full',
    state: gameState,
    version: gameState.version
  });
}
```

### Version Vectors for Consistency

```javascript
// Track state version to detect desync
let stateVersion = 0;

function applyAction(action) {
  // Validate and apply
  const newState = reducer(currentState, action);
  stateVersion++;

  return {
    state: newState,
    version: stateVersion
  };
}

// Client requests sync if versions mismatch
socket.on('state-update', ({ version, changes }) => {
  if (version !== localVersion + 1) {
    socket.emit('request-sync'); // Ask for full state
  }
});
```

## Handling Disconnections

### Reconnection Strategy

```javascript
// Client-side reconnection
const socket = io(SERVER_URL, {
  reconnection: true,
  reconnectionAttempts: 10,
  reconnectionDelay: 1000,
  reconnectionDelayMax: 5000
});

socket.on('connect', () => {
  if (currentGameId) {
    // Rejoin game room after reconnect
    socket.emit('join-game', {
      gameId: currentGameId,
      playerId: myPlayerId,
      lastVersion: localStateVersion // For delta sync
    });
  }
});

socket.on('disconnect', () => {
  showReconnectingUI();
});
```

### Grace Period for Disconnects

```javascript
// Server-side: Don't immediately remove disconnected players
const disconnectTimers = new Map();

function handlePlayerDisconnect(gameId, playerId) {
  // Mark as disconnected but give grace period
  updatePresence(gameId, playerId, false);

  const timer = setTimeout(() => {
    // After grace period, handle as true disconnect
    handlePlayerTimeout(gameId, playerId);
  }, 60000); // 60 second grace period

  disconnectTimers.set(`${gameId}:${playerId}`, timer);
}

function handlePlayerReconnect(gameId, playerId) {
  // Cancel timeout if player reconnects
  const key = `${gameId}:${playerId}`;
  if (disconnectTimers.has(key)) {
    clearTimeout(disconnectTimers.get(key));
    disconnectTimers.delete(key);
  }
  updatePresence(gameId, playerId, true);
}
```

## Turn-Based Game Patterns

### Turn Timer Implementation

```javascript
class TurnTimer {
  constructor(gameId, onTimeout) {
    this.gameId = gameId;
    this.onTimeout = onTimeout;
    this.timer = null;
  }

  start(playerId, durationMs) {
    this.clear();
    const endTime = Date.now() + durationMs;

    // Broadcast timer start to all clients
    io.to(`game:${this.gameId}`).emit('turn-timer', {
      playerId,
      endTime,
      durationMs
    });

    this.timer = setTimeout(() => {
      this.onTimeout(playerId);
    }, durationMs);
  }

  clear() {
    if (this.timer) {
      clearTimeout(this.timer);
      this.timer = null;
    }
  }
}
```

### Action Validation

```javascript
// Always validate on server
async function processAction(gameId, playerId, action) {
  const game = await getGame(gameId);

  // Validate it's player's turn
  if (game.currentPlayer !== playerId) {
    return { success: false, error: 'Not your turn' };
  }

  // Validate action is legal
  const validationResult = validateAction(game.state, action);
  if (!validationResult.valid) {
    return { success: false, error: validationResult.reason };
  }

  // Apply action
  const newState = applyAction(game.state, action);
  await saveGame(gameId, newState);

  return { success: true, newState };
}
```

## Optimistic Updates

### Client-Side Pattern

```javascript
// For responsive UI, apply optimistically then reconcile
function handlePlayerAction(action) {
  // 1. Optimistically apply locally
  const optimisticState = reducer(localState, action);
  renderUI(optimisticState);

  // 2. Send to server
  socket.emit('game-action', action, (response) => {
    if (response.success) {
      // 3a. Server confirmed - update to authoritative state
      localState = response.state;
    } else {
      // 3b. Server rejected - rollback
      localState = previousState;
      showError(response.error);
    }
    renderUI(localState);
  });
}
```

## Security Considerations

### Never Trust the Client

```javascript
// BAD: Client sends new state
socket.on('update-state', (newState) => {
  gameState = newState; // Never do this!
});

// GOOD: Client sends action, server validates and applies
socket.on('game-action', (action) => {
  if (isValidAction(gameState, action, socket.playerId)) {
    gameState = applyAction(gameState, action);
    broadcast(gameState);
  }
});
```

### Rate Limiting

```javascript
const rateLimit = require('socket.io-rate-limit');

io.use(rateLimit({
  windowMs: 1000,
  max: 10 // Max 10 messages per second per client
}));
```

## Testing Multiplayer

### Simulating Multiple Clients

```javascript
// Test helper for multiple socket connections
async function createTestClients(count, gameId) {
  const clients = [];
  for (let i = 0; i < count; i++) {
    const socket = io(SERVER_URL);
    await new Promise(resolve => socket.on('connect', resolve));
    socket.emit('join-game', { gameId, playerId: `player-${i}` });
    clients.push(socket);
  }
  return clients;
}
```

### Testing Reconnection

```javascript
it('should handle reconnection gracefully', async () => {
  const client = await createTestClient(gameId);

  // Force disconnect
  client.disconnect();

  // Wait and reconnect
  await sleep(1000);
  client.connect();

  // Should receive full state sync
  const state = await waitForEvent(client, 'state-sync');
  expect(state).toBeDefined();
});
```

## When This Skill Activates

Use this skill when:
- Setting up WebSocket/Socket.io connections
- Implementing game room management
- Building state synchronization
- Handling player disconnection/reconnection
- Implementing turn timers
- Adding optimistic updates
- Securing multiplayer communications
