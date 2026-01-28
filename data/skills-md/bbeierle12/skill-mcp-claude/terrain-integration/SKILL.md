---
name: terrain-integration
description: Terrain interaction systems for Three.js building games. Use when implementing slope handling, foundation anchoring (Valheim pattern), terrain modification, auto-leveling, or pillar/support generation. Integrates with structural-physics for ground-based stability.
---

# Terrain Integration

Foundation placement, slope handling, and terrain modification for building systems.

## Quick Start

```javascript
import { TerrainAnalyzer } from './scripts/terrain-analyzer.js';
import { FoundationPlacer } from './scripts/foundation-placer.js';

// Analyze terrain at build location
const analyzer = new TerrainAnalyzer(terrainMesh);
const slopeData = analyzer.analyzeSlope(position, { radius: 4 });
// slopeData: { angle: 15, normal: Vector3, canBuild: true }

// Place foundation with auto-leveling
const placer = new FoundationPlacer({ 
  mode: 'valheim', // or 'rust', 'ark'
  maxSlope: 30,
  autoLevel: true 
});
const result = placer.place(foundationPiece, position, analyzer);
// result: { valid: true, height: 2.3, pillarsNeeded: 2 }
```

## Reference

See `references/terrain-integration-advanced.md` for:
- Slope analysis algorithms and thresholds
- Foundation anchoring patterns (Valheim ground contact rule)
- Auto-leveling strategies
- Terrain modification networking
- Pillar generation for uneven terrain

## Scripts

- `scripts/terrain-analyzer.js` - Slope detection, buildability checks, terrain sampling
- `scripts/foundation-placer.js` - Foundation placement with Valheim/Rust/ARK modes
- `scripts/terrain-modifier.js` - Flatten, raise, lower terrain operations
- `scripts/pillar-generator.js` - Auto-generate support pillars for slopes

## Foundation Modes

- **Valheim**: Ground contact = 100% stability, foundations must touch terrain
- **Rust**: Foundations snap to grid, terrain ignored after placement
- **ARK**: Flexible placement with auto-pillars, moderate slope tolerance

## Integration

Works with `structural-physics` for stability calculations. Grounded foundations feed into the support graph as root nodes with maximum stability.

```javascript
// Integration example
const grounded = placer.place(foundation, pos, analyzer);
if (grounded.valid) {
  foundation.isGrounded = true;
  foundation.stability = 1.0; // Feed to structural-physics
  validator.addPiece(foundation);
}
```
