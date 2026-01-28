---
name: performance-at-scale
description: Spatial indexing and world streaming for Three.js building games with thousands of pieces. Use when optimizing building games, implementing spatial queries, chunk loading, or profiling performance. Includes spatial hash grids, octrees, chunk managers, and benchmarking tools.
---

# Performance at Scale

Spatial indexing and world streaming for large-scale building systems.

## Quick Start

```javascript
import { SpatialHashGrid } from './scripts/spatial-hash-grid.js';
import { Octree } from './scripts/octree.js';

// Uniform distribution - use hash grid
const grid = new SpatialHashGrid(10);
grid.insert(piece, piece.position);
const nearby = grid.queryRadius(position, 15);

// Clustered bases - use octree
const octree = new Octree(bounds, { maxDepth: 8 });
octree.insert(piece);
const inBox = octree.queryBox(min, max);
```

## Reference

See `references/performance-at-scale.md` for detailed guidance on:
- Spatial partitioning selection (when to use grid vs octree)
- Chunk loading strategies
- Instancing and LOD
- Memory management

## Scripts

- `scripts/spatial-hash-grid.js` - O(1) queries for uniform distribution
- `scripts/octree.js` - Adaptive queries for clustered objects
- `scripts/chunk-manager.js` - World streaming for large maps
- `scripts/performance-profiler.js` - Benchmarking utilities

## Selection Guide

| Pieces | Distribution | Use |
|--------|-------------|-----|
| <1,000 | Any | Array |
| 1-5k | Uniform | SpatialHashGrid |
| 1-5k | Clustered | Octree |
| 5k+ | Any | ChunkManager + Octree per chunk |
