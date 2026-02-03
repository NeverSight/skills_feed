---
name: hytopia-events
description: Helps handle events and input in HYTOPIA SDK games. Use when users need to respond to player actions, game events, chat commands, or input handling. Covers event listeners, chat commands, player input, and game lifecycle events.
---

# HYTOPIA Events & Input

This skill helps you handle events and input in HYTOPIA SDK games.

## When to Use This Skill

Use this skill when the user:

- Wants to respond to player actions or game events
- Needs to handle chat commands
- Asks about player input (keyboard, mouse, touch)
- Wants to create custom events
- Needs to handle game lifecycle events (start, end, player join/leave)
- Asks about event prioritization or cancellation

## Core Event Concepts

### Event Listeners

```typescript
import { World, Player } from 'hytopia';

// Listen for player join
world.onPlayerJoin = (player: Player) => {
  console.log(`${player.username} joined!`);
  player.sendMessage('Welcome to the game!');
};

// Listen for player leave
world.onPlayerLeave = (player: Player) => {
  console.log(`${player.username} left!`);
};

// Listen for player chat
world.onPlayerChat = (player: Player, message: string) => {
  console.log(`${player.username}: ${message}`);
  return true; // Return false to block message
};
```

### Chat Commands

```typescript
import { World, Player } from 'hytopia';

world.onPlayerChat = (player: Player, message: string) => {
  if (message.startsWith('!')) {
    const args = message.slice(1).split(' ');
    const command = args[0];
    
    switch (command) {
      case 'help':
        player.sendMessage('Available commands: !spawn, !teleport, !kit');
        break;
      case 'spawn':
        player.setPosition({ x: 0, y: 100, z: 0 });
        player.sendMessage('Teleported to spawn!');
        break;
      case 'kit':
        giveStarterKit(player);
        break;
      default:
        player.sendMessage(`Unknown command: ${command}`);
    }
    
    return false; // Don't broadcast command to other players
  }
  
  return true; // Allow normal chat
};
```

### Player Input

```typescript
import { Player, Input } from 'hytopia';

// Handle player input
player.onInput = (input: Input) => {
  if (input.isPressed('space')) {
    // Jump
    player.applyImpulse({ x: 0, y: 10, z: 0 });
  }
  
  if (input.isPressed('e')) {
    // Interact
    handleInteraction(player);
  }
  
  if (input.mouseDelta.x !== 0) {
    // Mouse moved horizontally
    player.rotation.y += input.mouseDelta.x * 0.1;
  }
};
```

### Custom Events

```typescript
import { EventEmitter } from 'hytopia';

// Create custom event emitter
const gameEvents = new EventEmitter();

// Define event types
interface GameEvents {
  'player-kill': { killer: Player; victim: Player };
  'game-start': { map: string };
  'game-end': { winner: Player };
}

// Listen for events
gameEvents.on('player-kill', ({ killer, victim }) => {
  killer.sendMessage(`You eliminated ${victim.username}!`);
  victim.sendMessage(`You were eliminated by ${killer.username}!`);
});

// Emit events
gameEvents.emit('player-kill', { killer: player1, victim: player2 });
```

## Input Handling Patterns

### Movement Input

```typescript
player.onInput = (input: Input) => {
  const moveSpeed = 5;
  const moveDirection = new Vector3(0, 0, 0);
  
  if (input.isPressed('w')) moveDirection.z += 1;
  if (input.isPressed('s')) moveDirection.z -= 1;
  if (input.isPressed('a')) moveDirection.x -= 1;
  if (input.isPressed('d')) moveDirection.x += 1;
  
  if (moveDirection.length() > 0) {
    moveDirection.normalize().multiply(moveSpeed);
    player.velocity.x = moveDirection.x;
    player.velocity.z = moveDirection.z;
  }
};
```

### Mouse/Click Handling

```typescript
player.onInput = (input: Input) => {
  // Left click
  if (input.isMousePressed(0)) {
    const raycast = world.raycast(player.position, player.lookDirection, 5);
    if (raycast.hit && raycast.entity) {
      // Attack entity
      raycast.entity.takeDamage(10);
    }
  }
  
  // Right click
  if (input.isMousePressed(1)) {
    // Place block or use item
    useHeldItem(player);
  }
};
```

## Game Lifecycle Events

```typescript
import { Game } from 'hytopia';

const game = new Game();

game.onStart = () => {
  console.log('Game started!');
  // Initialize game state
};

game.onEnd = () => {
  console.log('Game ended!');
  // Cleanup, save state
};

game.onTick = (deltaTime: number) => {
  // Update game logic every frame
  updateGameTimer(deltaTime);
  checkWinConditions();
};
```

## Best Practices

1. **Keep event handlers short** - delegate to functions for complex logic
2. **Return false to cancel** - prevent default behavior when needed
3. **Use typed events** - define interfaces for custom events
4. **Clean up listeners** - remove listeners when entities despawn
5. **Debounce rapid inputs** - prevent spamming with cooldowns

## Common Mistakes

- Don't forget to return boolean in chat handler
- Don't block all chat when handling commands (return true for normal messages)
- Don't forget input can be null if player disconnects mid-frame
- Don't rely on client-side input alone - validate on server
