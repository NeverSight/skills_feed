---
name: multiplayer-building
description: Networking systems for multiplayer building games. Use when implementing networked construction, delta synchronization, client prediction, or conflict resolution. Server-authoritative model with optimistic client prediction for responsive gameplay.
---

# Multiplayer Building

Networking layer for multiplayer building games.

## Quick Start

```javascript
import { BuildingNetworkServer, BuildingNetworkClient } from './scripts/building-network-manager.js';

// Server
const server = new BuildingNetworkServer(buildingSystem, {
  tickRate: 20,
  conflictStrategy: 'first_write'
});
server.start();

// Client
const client = new BuildingNetworkClient(buildingSystem);
client.connect('ws://server:8080');
const localPiece = client.placeRequest('wall', position, rotation);
```

## Reference

See `references/multiplayer-networking.md` for:
- Authority model comparison
- Delta compression strategy
- Conflict resolution approaches
- Large structure synchronization

## Scripts

- `scripts/delta-compression.js` - Only sync changed state (Source engine pattern)
- `scripts/client-prediction.js` - Optimistic placement with rollback
- `scripts/conflict-resolver.js` - Handle simultaneous builds (first-write, timestamp, lock-based)
- `scripts/building-network-manager.js` - Complete server/client system

## Architecture

**Server-authoritative** with client prediction:
1. Client predicts placement locally (ghost piece)
2. Server validates and confirms/rejects
3. Client reconciles with server state
4. Delta compression syncs only changes
