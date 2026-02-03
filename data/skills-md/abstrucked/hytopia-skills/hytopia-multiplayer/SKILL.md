---
name: hytopia-multiplayer
description: Helps implement multiplayer features in HYTOPIA SDK games. Use when users need player management, server-authoritative gameplay, networking, or state synchronization. Covers Player class, server authority, network optimization, and player data.
---

# HYTOPIA Multiplayer

This skill helps you implement multiplayer features in HYTOPIA SDK games.

## When to Use This Skill

Use this skill when the user:

- Wants to manage multiple players in a game
- Needs server-authoritative gameplay mechanics
- Asks about player data persistence
- Wants to optimize network performance
- Needs player authentication or identification
- Asks about player teams, groups, or parties

## Core Multiplayer Concepts

### Player Management

```typescript
import { World, Player } from 'hytopia';

// Access all players
const players = world.players;

// Get specific player
const player = world.getPlayer(playerId);

// Iterate over players
for (const player of world.players) {
  player.sendMessage('Hello!');
}

// Count players
const playerCount = world.players.length;
```

### Player Events

```typescript
import { World, Player } from 'hytopia';

world.onPlayerJoin = (player: Player) => {
  console.log(`${player.username} joined (${player.id})`);
  
  // Send welcome message
  player.sendMessage(`Welcome ${player.username}!`);
  
  // Broadcast to others
  world.broadcast(`${player.username} has joined the game!`, [player.id]);
  
  // Spawn player at location
  player.setPosition({ x: 0, y: 100, z: 0 });
};

world.onPlayerLeave = (player: Player) => {
  console.log(`${player.username} left`);
  world.broadcast(`${player.username} has left the game.`);
};
```

### Player Data

```typescript
import { Player } from 'hytopia';

// Set custom data on player
player.setData('score', 0);
player.setData('kills', 0);
player.setData('inventory', []);

// Get player data
const score = player.getData('score');
const inventory = player.getData('inventory') || [];

// Persist data (saved across sessions)
player.setPersistedData('level', 5);
const level = player.getPersistedData('level');
```

## Server Authority

### Server-Authoritative Movement

```typescript
import { Player } from 'hytopia';

// Server controls all movement - client sends inputs only
player.onInput = (input) => {
  // Process input on server
  if (input.isPressed('w')) {
    // Calculate new position server-side
    const newPosition = calculateMovement(player, input);
    player.setPosition(newPosition);
  }
};

// Never trust client position
// Always validate: check speed, bounds, collision
```

### State Synchronization

```typescript
import { Entity } from 'hytopia';

class GameEntity extends Entity {
  // Only sync what needs to be visible
  syncProperties = ['position', 'rotation', 'health'];
  
  tick(deltaTime: number) {
    // Server updates state
    this.updateAI(deltaTime);
    
    // Changes automatically sync to clients
    // for properties in syncProperties
  }
}
```

### Anti-Cheat Basics

```typescript
import { Player } from 'hytopia';

function validatePlayerMovement(player: Player, newPos: Vector3) {
  const oldPos = player.position;
  const distance = oldPos.distance(newPos);
  const maxDistance = player.maxSpeed * deltaTime;
  
  // Check if moved too fast
  if (distance > maxDistance * 1.1) {  // 10% tolerance
    console.warn(`Possible speed hack: ${player.username}`);
    player.setPosition(oldPos);  // Revert
    return false;
  }
  
  // Check if in bounds
  if (!world.isInBounds(newPos)) {
    player.setPosition(oldPos);
    return false;
  }
  
  return true;
}
```

## Network Optimization

### Efficient Broadcasting

```typescript
import { World } from 'hytopia';

// Send to all players
world.broadcast('Game starting!');

// Send to specific players
world.broadcast('Team message', [], [player1.id, player2.id]);

// Send to all except some
world.broadcast('Secret message', [player1.id]);

// Send to nearby players only
function broadcastToNearby(origin: Vector3, message: string, radius: number) {
  for (const player of world.players) {
    if (player.position.distance(origin) <= radius) {
      player.sendMessage(message);
    }
  }
}
```

### Property Sync Optimization

```typescript
import { Entity } from 'hytopia';

class OptimizedEntity extends Entity {
  // Only sync when changed
  private _health: number = 100;
  
  get health() { return this._health; }
  set health(value: number) {
    if (this._health !== value) {
      this._health = value;
      this.sync('health', value);  // Manual sync only on change
    }
  }
  
  // Don't sync internal state
  private pathfindingTarget: Vector3;  // Server-only
  private lastUpdate: number;          // Server-only
}
```

## Player Teams/Groups

```typescript
import { Player } from 'hytopia';

// Simple team system
const teams = new Map<string, Player[]>();

function assignTeam(player: Player, teamName: string) {
  // Remove from old team
  const oldTeam = player.getData('team');
  if (oldTeam) {
    const oldPlayers = teams.get(oldTeam) || [];
    teams.set(oldTeam, oldPlayers.filter(p => p.id !== player.id));
  }
  
  // Add to new team
  player.setData('team', teamName);
  const teamPlayers = teams.get(teamName) || [];
  teamPlayers.push(player);
  teams.set(teamName, teamPlayers);
  
  // Notify team
  for (const teammate of teamPlayers) {
    teammate.sendMessage(`${player.username} joined ${teamName}!`);
  }
}

function getTeamPlayers(teamName: string): Player[] {
  return teams.get(teamName) || [];
}
```

## Best Practices

1. **Server is authoritative** - Never trust client data
2. **Validate all inputs** - Check bounds, rates, permissions
3. **Sync minimally** - Only send what clients need to know
4. **Use spatial partitioning** - Don't broadcast to distant players
5. **Rate limit** - Prevent spam and DoS
6. **Graceful degradation** - Handle lag and packet loss

## Common Patterns

### Player Spawn System

```typescript
const spawnPoints = [
  { x: 10, y: 100, z: 10 },
  { x: -10, y: 100, z: 10 },
  { x: 10, y: 100, z: -10 },
  { x: -10, y: 100, z: -10 }
];

function spawnPlayer(player: Player) {
  const spawnIndex = world.players.length % spawnPoints.length;
  player.setPosition(spawnPoints[spawnIndex]);
  player.setHealth(100);
  player.clearInventory();
}
```

### Leaderboard

```typescript
function updateLeaderboard() {
  const sorted = [...world.players].sort((a, b) => 
    (b.getData('score') || 0) - (a.getData('score') || 0)
  );
  
  const leaderboard = sorted.slice(0, 10).map((p, i) => 
    `${i + 1}. ${p.username}: ${p.getData('score') || 0}`
  ).join('\n');
  
  world.broadcast('=== Leaderboard ===\n' + leaderboard);
}
```
