---
name: hexgrid-algorithms
description: Hexagonal grid mathematics, coordinate systems, pathfinding, and spatial algorithms for hex-based games. Use when implementing hex grids, calculating hex distances, finding neighbors, pathfinding on hex maps, spreading effects across hexes, or converting between coordinate systems. Triggers on requests involving hexagonal grids, hex coordinates, A* on hex maps, or hex-based game mechanics.
---

# Hexgrid Algorithms

Complete reference for hexagonal grid mathematics and algorithms optimized for game development.

## Coordinate Systems

### Cube Coordinates (Recommended)

Three-axis system where `q + r + s = 0` always.

```typescript
interface CubeCoord {
  q: number;  // Column
  r: number;  // Row  
  s: number;  // Derived: s = -q - r
}

// Constraint: q + r + s must equal 0
function isValidCube(coord: CubeCoord): boolean {
  return coord.q + coord.r + coord.s === 0;
}
```

### Axial Coordinates (Storage-Efficient)

Two-axis system derived from cube (drop s).

```typescript
interface AxialCoord {
  q: number;
  r: number;
}

// Convert to cube
function axialToCube(axial: AxialCoord): CubeCoord {
  return { q: axial.q, r: axial.r, s: -axial.q - axial.r };
}

// Convert from cube
function cubeToAxial(cube: CubeCoord): AxialCoord {
  return { q: cube.q, r: cube.r };
}
```

### Offset Coordinates (Display)

For rendering in standard grid layouts.

```typescript
// Odd-q offset (pointy-top hexes)
function axialToOffset(axial: AxialCoord): { col: number; row: number } {
  const col = axial.q;
  const row = axial.r + Math.floor((axial.q - (axial.q & 1)) / 2);
  return { col, row };
}

function offsetToAxial(col: number, row: number): AxialCoord {
  const q = col;
  const r = row - Math.floor((col - (col & 1)) / 2);
  return { q, r };
}
```

## Core Operations

### Distance

```typescript
function hexDistance(a: CubeCoord, b: CubeCoord): number {
  return Math.max(
    Math.abs(a.q - b.q),
    Math.abs(a.r - b.r),
    Math.abs(a.s - b.s)
  );
}

// Or equivalently:
function hexDistanceAlt(a: CubeCoord, b: CubeCoord): number {
  return (Math.abs(a.q - b.q) + Math.abs(a.r - b.r) + Math.abs(a.s - b.s)) / 2;
}
```

### Neighbors

```typescript
const CUBE_DIRECTIONS: CubeCoord[] = [
  { q: 1, r: -1, s: 0 },  // East
  { q: 1, r: 0, s: -1 },  // Southeast
  { q: 0, r: 1, s: -1 },  // Southwest
  { q: -1, r: 1, s: 0 },  // West
  { q: -1, r: 0, s: 1 },  // Northwest
  { q: 0, r: -1, s: 1 },  // Northeast
];

function getNeighbors(hex: CubeCoord): CubeCoord[] {
  return CUBE_DIRECTIONS.map(dir => ({
    q: hex.q + dir.q,
    r: hex.r + dir.r,
    s: hex.s + dir.s
  }));
}

function getNeighbor(hex: CubeCoord, direction: number): CubeCoord {
  const dir = CUBE_DIRECTIONS[direction];
  return {
    q: hex.q + dir.q,
    r: hex.r + dir.r,
    s: hex.s + dir.s
  };
}
```

### Ring

Get all hexes at exact distance from center.

```typescript
function hexRing(center: CubeCoord, radius: number): CubeCoord[] {
  if (radius === 0) return [center];
  
  const results: CubeCoord[] = [];
  let hex: CubeCoord = {
    q: center.q + CUBE_DIRECTIONS[4].q * radius,
    r: center.r + CUBE_DIRECTIONS[4].r * radius,
    s: center.s + CUBE_DIRECTIONS[4].s * radius
  };
  
  for (let i = 0; i < 6; i++) {
    for (let j = 0; j < radius; j++) {
      results.push({ ...hex });
      hex = getNeighbor(hex, i);
    }
  }
  
  return results;
}
```

### Spiral (All Hexes Within Radius)

```typescript
function hexSpiral(center: CubeCoord, radius: number): CubeCoord[] {
  const results: CubeCoord[] = [center];
  
  for (let r = 1; r <= radius; r++) {
    results.push(...hexRing(center, r));
  }
  
  return results;
}
```

## Pathfinding

### A* for Hex Grids

```typescript
interface PathNode {
  coord: CubeCoord;
  g: number;  // Cost from start
  h: number;  // Heuristic to goal
  f: number;  // Total: g + h
  parent: PathNode | null;
}

function hexKey(coord: CubeCoord): string {
  return `${coord.q},${coord.r}`;
}

function findPath(
  start: CubeCoord,
  goal: CubeCoord,
  isPassable: (coord: CubeCoord) => boolean,
  getCost: (coord: CubeCoord) => number = () => 1
): CubeCoord[] | null {
  const openSet = new Map<string, PathNode>();
  const closedSet = new Set<string>();
  
  const startNode: PathNode = {
    coord: start,
    g: 0,
    h: hexDistance(start, goal),
    f: hexDistance(start, goal),
    parent: null
  };
  
  openSet.set(hexKey(start), startNode);
  
  while (openSet.size > 0) {
    // Get node with lowest f
    let current: PathNode | null = null;
    for (const node of openSet.values()) {
      if (!current || node.f < current.f) {
        current = node;
      }
    }
    
    if (!current) break;
    
    // Check if reached goal
    if (hexKey(current.coord) === hexKey(goal)) {
      const path: CubeCoord[] = [];
      let node: PathNode | null = current;
      while (node) {
        path.unshift(node.coord);
        node = node.parent;
      }
      return path;
    }
    
    // Move current to closed set
    openSet.delete(hexKey(current.coord));
    closedSet.add(hexKey(current.coord));
    
    // Check neighbors
    for (const neighbor of getNeighbors(current.coord)) {
      const key = hexKey(neighbor);
      
      if (closedSet.has(key) || !isPassable(neighbor)) {
        continue;
      }
      
      const g = current.g + getCost(neighbor);
      const existing = openSet.get(key);
      
      if (!existing || g < existing.g) {
        const node: PathNode = {
          coord: neighbor,
          g,
          h: hexDistance(neighbor, goal),
          f: g + hexDistance(neighbor, goal),
          parent: current
        };
        openSet.set(key, node);
      }
    }
  }
  
  return null; // No path found
}
```

## Spreading Algorithms

### Trouble Spread (Farming in Purria)

```typescript
function spreadTrouble(
  cluster: TroubleCluster,
  gridRadius: number,
  occupiedHexes: Set<string>
): CubeCoord[] {
  const newHexes: CubeCoord[] = [];
  const spreadChance = 0.3 + (cluster.severity * 0.1); // 30-80%
  
  for (const hex of cluster.hexCoords) {
    for (const neighbor of getNeighbors(hex)) {
      const key = hexKey(neighbor);
      
      // Skip if already occupied or out of bounds
      if (occupiedHexes.has(key)) continue;
      if (hexDistance({ q: 0, r: 0, s: 0 }, neighbor) > gridRadius) continue;
      
      // Random spread chance
      if (Math.random() < spreadChance) {
        newHexes.push(neighbor);
        occupiedHexes.add(key);
      }
    }
  }
  
  return newHexes;
}
```

### Flood Fill

```typescript
function floodFill(
  start: CubeCoord,
  maxDistance: number,
  isValid: (coord: CubeCoord) => boolean
): CubeCoord[] {
  const visited = new Set<string>();
  const result: CubeCoord[] = [];
  const queue: { coord: CubeCoord; dist: number }[] = [{ coord: start, dist: 0 }];
  
  while (queue.length > 0) {
    const { coord, dist } = queue.shift()!;
    const key = hexKey(coord);
    
    if (visited.has(key) || dist > maxDistance || !isValid(coord)) {
      continue;
    }
    
    visited.add(key);
    result.push(coord);
    
    for (const neighbor of getNeighbors(coord)) {
      queue.push({ coord: neighbor, dist: dist + 1 });
    }
  }
  
  return result;
}
```

## Rendering

### Pixel Coordinates

```typescript
const HEX_SIZE = 50; // Radius in pixels

// Pointy-top hex
function hexToPixel(hex: AxialCoord, size: number = HEX_SIZE): { x: number; y: number } {
  const x = size * (Math.sqrt(3) * hex.q + Math.sqrt(3) / 2 * hex.r);
  const y = size * (3 / 2 * hex.r);
  return { x, y };
}

function pixelToHex(x: number, y: number, size: number = HEX_SIZE): AxialCoord {
  const q = (Math.sqrt(3) / 3 * x - 1 / 3 * y) / size;
  const r = (2 / 3 * y) / size;
  return hexRound({ q, r });
}

// Round fractional hex to nearest hex
function hexRound(hex: AxialCoord): AxialCoord {
  const cube = axialToCube(hex);
  let rq = Math.round(cube.q);
  let rr = Math.round(cube.r);
  let rs = Math.round(cube.s);
  
  const qDiff = Math.abs(rq - cube.q);
  const rDiff = Math.abs(rr - cube.r);
  const sDiff = Math.abs(rs - cube.s);
  
  if (qDiff > rDiff && qDiff > sDiff) {
    rq = -rr - rs;
  } else if (rDiff > sDiff) {
    rr = -rq - rs;
  }
  
  return { q: rq, r: rr };
}
```

### SVG Hex Path

```typescript
function hexCorners(center: { x: number; y: number }, size: number): { x: number; y: number }[] {
  const corners: { x: number; y: number }[] = [];
  for (let i = 0; i < 6; i++) {
    const angle = (Math.PI / 180) * (60 * i - 30); // Pointy-top
    corners.push({
      x: center.x + size * Math.cos(angle),
      y: center.y + size * Math.sin(angle)
    });
  }
  return corners;
}

function hexPath(center: { x: number; y: number }, size: number): string {
  const corners = hexCorners(center, size);
  return corners.map((c, i) => `${i === 0 ? 'M' : 'L'} ${c.x} ${c.y}`).join(' ') + ' Z';
}
```

## Performance Tips

1. **Use string keys** for Map/Set operations: `${q},${r}`
2. **Pre-calculate neighbors** for static grids
3. **Limit pathfinding** with max iterations
4. **Batch render updates** instead of per-hex
5. **Use spatial hashing** for large grids (chunk into regions)
