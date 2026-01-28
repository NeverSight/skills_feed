---
name: structural-physics
description: Structural validation and damage systems for Three.js building games. Use when implementing building stability (Fortnite/Rust/Valheim style), damage propagation, cascading collapse, or realistic physics simulation. Supports arcade, heuristic, and realistic physics modes.
---

# Structural Physics

Stability validation and damage systems for building mechanics.

## Quick Start

```javascript
import { HeuristicValidator } from './scripts/heuristic-validator.js';
import { DamageSystem } from './scripts/damage-propagation.js';

// Rust/Valheim style stability
const validator = new HeuristicValidator({ mode: 'heuristic' });
validator.addPiece(piece);
const result = validator.validatePlacement(newPiece);
// result: { valid: true, stability: 0.85, supports: [...] }

// Damage and collapse
const damage = new DamageSystem(validator);
damage.applyDamage(piece, 50, 'physical');
damage.applyExplosiveDamage(position, 100, 10); // radius damage
```

## Reference

See `references/structural-physics-advanced.md` for:
- Physics mode comparison (arcade vs heuristic vs realistic)
- Material properties and decay rates
- Damage state thresholds
- Cascade mechanics

## Scripts

- `scripts/heuristic-validator.js` - Fast validation (Fortnite/Rust/Valheim modes)
- `scripts/stability-optimizer.js` - Caching and batch updates for large structures
- `scripts/damage-propagation.js` - Damage states, fire spread, cascading collapse
- `scripts/physics-engine-lite.js` - Optional realistic stress/strain simulation

## Physics Modes

- **Arcade** (Fortnite): Connectivity only, instant collapse, best for combat
- **Heuristic** (Rust/Valheim): Stability %, predictable rules, best for survival
- **Realistic**: Full stress/strain, computationally expensive, best for engineering sims
