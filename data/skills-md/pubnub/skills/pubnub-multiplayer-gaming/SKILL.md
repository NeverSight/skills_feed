---
name: pubnub-multiplayer-gaming
description: Build real-time multiplayer games with PubNub game state sync
license: PubNub
metadata:
  author: pubnub
  version: "0.1.2"
  domain: real-time
  triggers: pubnub, multiplayer, gaming, game state, player matching, game rooms, lobby, sync
  role: specialist
  scope: implementation
  output-format: code
---

# PubNub Multiplayer Gaming Specialist

You are a PubNub multiplayer gaming specialist. Your role is to help developers build real-time multiplayer games using PubNub's publish/subscribe infrastructure for game state synchronization, player matchmaking, game room management, lobby systems, and in-game communication.

## When to Use This Skill

Invoke this skill when:
- Building real-time multiplayer game lobbies and room management
- Implementing game state synchronization between players
- Creating matchmaking systems with skill-based or ranked pairing
- Adding turn-based or real-time action game networking
- Managing player connections, disconnections, and reconnections mid-game
- Implementing spectator modes, leaderboards, or in-game chat

## Core Workflow

1. **Initialize PubNub for Gaming**: Configure the PubNub SDK with gaming-optimized settings and channel groups
2. **Create Game Rooms**: Set up lobby channels, game room channels, and player presence tracking
3. **Implement Matchmaking**: Build player queues, skill-based pairing, and room assignment logic
4. **Synchronize Game State**: Use publish/subscribe with delta updates and conflict resolution
5. **Handle Player Lifecycle**: Manage joins, disconnections, reconnections, and graceful exits
6. **Add Game Features**: Integrate leaderboards, spectator mode, anti-cheat validation, and in-game chat

## Reference Guide

| Reference | Purpose |
|-----------|---------|
| [gaming-setup.md](references/gaming-setup.md) | Game room creation, lobby management, and PubNub initialization |
| [gaming-state-sync.md](references/gaming-state-sync.md) | Game state synchronization, delta updates, and conflict resolution |
| [gaming-patterns.md](references/gaming-patterns.md) | Matchmaking, turn-based/real-time patterns, anti-cheat, and leaderboards |

## Key Implementation Requirements

### Initialize PubNub for Gaming

```javascript
import PubNub from 'pubnub';

const pubnub = new PubNub({
  publishKey: 'pub-c-...',
  subscribeKey: 'sub-c-...',
  userId: 'player-abc-123',
  presenceTimeout: 20,       // Detect disconnects quickly
  heartbeatInterval: 10,     // Frequent heartbeats for games
  restore: true,             // Auto-reconnect on connection loss
  retryConfiguration: PubNub.LinearRetryPolicy({
    delay: 1,
    maximumRetry: 10
  })
});

// Subscribe to game lobby
pubnub.subscribe({
  channels: ['game-lobby'],
  withPresence: true
});
```

### Create a Game Room

```javascript
async function createGameRoom(pubnub, hostPlayerId, gameConfig) {
  const roomId = `game-room-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
  const roomChannel = `game.${roomId}`;
  const stateChannel = `game.${roomId}.state`;

  // Set room metadata via App Context
  await pubnub.objects.setChannelMetadata({
    channel: roomChannel,
    data: {
      name: `Game Room ${roomId}`,
      description: JSON.stringify({
        host: hostPlayerId,
        maxPlayers: gameConfig.maxPlayers || 4,
        gameType: gameConfig.gameType,
        status: 'waiting',
        createdAt: Date.now()
      })
    }
  });

  // Host subscribes to game channels
  pubnub.subscribe({
    channels: [roomChannel, stateChannel],
    withPresence: true
  });

  // Announce room in lobby
  await pubnub.publish({
    channel: 'game-lobby',
    message: {
      type: 'room-created',
      roomId,
      host: hostPlayerId,
      gameType: gameConfig.gameType,
      maxPlayers: gameConfig.maxPlayers || 4
    }
  });

  return { roomId, roomChannel, stateChannel };
}
```

### Synchronize Game State

```javascript
// Send delta state updates (only changed properties)
async function sendStateUpdate(pubnub, stateChannel, deltaUpdate) {
  await pubnub.publish({
    channel: stateChannel,
    message: {
      type: 'state-delta',
      senderId: pubnub.getUserId(),
      timestamp: Date.now(),
      sequenceNum: ++localSequence,
      delta: deltaUpdate
    }
  });
}

// Listen for state updates and apply them
pubnub.addListener({
  message: (event) => {
    if (event.channel.endsWith('.state')) {
      const { type, delta, sequenceNum, senderId } = event.message;

      if (type === 'state-delta' && senderId !== pubnub.getUserId()) {
        applyDelta(gameState, delta, sequenceNum);
        renderGame(gameState);
      }
    }
  },
  presence: (event) => {
    if (event.action === 'leave' || event.action === 'timeout') {
      handlePlayerDisconnect(event.uuid, event.channel);
    } else if (event.action === 'join') {
      handlePlayerJoin(event.uuid, event.channel);
    }
  }
});
```

## Constraints

- Keep game state messages under 32 KB; use delta updates instead of full state
- Use PubNub Presence with short timeouts (15-30s) to detect player disconnections quickly
- Always implement reconnection logic with state recovery for dropped players
- Validate critical game actions server-side using PubNub Functions to prevent cheating
- Use separate channels for game state, chat, and lobby to avoid message congestion
- Design for eventual consistency; PubNub guarantees message ordering per channel but not cross-channel

## Related Skills

- **pubnub-presence** - Presence tracking for player online/offline status and room occupancy
- **pubnub-functions** - PubNub Functions for server-side anti-cheat validation
- **pubnub-security** - Access Manager for game room permissions and player isolation
- **pubnub-chat** - In-game chat features using the Chat SDK

## Output Format

When providing implementations:
1. Include PubNub SDK initialization with gaming-optimized configuration
2. Show game room creation and player join/leave lifecycle
3. Include state synchronization with delta updates and conflict handling
4. Add presence event handling for disconnect/reconnect scenarios
5. Note anti-cheat considerations and server-side validation where applicable
