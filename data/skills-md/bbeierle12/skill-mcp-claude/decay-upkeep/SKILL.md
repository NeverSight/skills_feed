---
name: decay-upkeep
description: Building decay and upkeep systems for survival games. Use when implementing timer-based decay, Tool Cupboard patterns (Rust-style protection radius), resource upkeep costs, or server performance management through automatic cleanup. Balances gameplay and server health.
---

# Decay & Upkeep

Timer-based building decay and resource-based upkeep for survival games.

## Quick Start

```javascript
import { DecayManager } from './scripts/decay-manager.js';
import { UpkeepSystem } from './scripts/upkeep-system.js';
import { ToolCupboard } from './scripts/tool-cupboard.js';

// Decay without protection
const decay = new DecayManager({ 
  mode: 'rust',
  decayMultiplier: 1.0 
});
decay.addPiece(piece);
decay.tick(deltaTime); // Called every frame/tick

// Tool Cupboard protection
const tc = new ToolCupboard({
  radius: 30,
  upkeepCost: { wood: 100, stone: 50 }
});
tc.setPosition(position);
tc.depositResources({ wood: 500, stone: 250 });
// Protected pieces won't decay while upkeep is paid
```

## Reference

See `references/decay-upkeep-advanced.md` for:
- Decay rate formulas by material
- Tool Cupboard mechanics (Rust pattern)
- Upkeep scaling with base size
- Server performance benefits
- Anti-raid delay mechanics

## Scripts

- `scripts/decay-manager.js` - Tick-based decay, material rates, damage states
- `scripts/upkeep-system.js` - Resource drain, calculation, UI data
- `scripts/tool-cupboard.js` - Protection radius, authorization, resource storage
- `scripts/cleanup-scheduler.js` - Server-side cleanup of abandoned structures

## Decay Modes

- **Rust**: Linear decay over 8-24 hours (material dependent), prevented by Tool Cupboard
- **ARK**: Slower decay (days to weeks), tribe-based protection
- **Minecraft**: No decay (creative/survival), optional via mods

## Design Philosophy

Decay serves dual purposes in survival games: gameplay balance (prevents infinite hoarding) and server performance (removes abandoned bases). The Tool Cupboard pattern elegantly ties both together—players must actively maintain bases, and inactive players' structures automatically clean up.
