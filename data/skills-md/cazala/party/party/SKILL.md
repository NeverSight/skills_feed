---
name: party
description: "Programmatic guide for the @cazala/party library: engine setup, modules, particles, and performance across CPU + WebGPU."
version: 0.1.0
license: MIT
tags: [party, particles, physics, webgpu, cpu, simulation, typescript]
---

# Party

Reusable guidance for using the `@cazala/party` library programmatically: engine setup, runtime selection, particles, modules, and performance constraints across CPU + WebGPU.

## When to use this skill

- You need to instantiate the Party engine in a custom app (not the playground).
- You want examples for adding particles, configuring modules, or using oscillators.
- You need performance-safe patterns for WebGPU (avoiding full readbacks).

## Quick start (minimal)

```ts
import {
  Engine,
  Environment,
  Boundary,
  Collisions,
  Particles,
  Trails,
} from "@cazala/party";

const canvas = document.querySelector("canvas")!;

const forces = [
  new Environment({ gravityStrength: 600, gravityDirection: "down" }),
  new Boundary({ mode: "bounce", restitution: 0.9, friction: 0.1 }),
  new Collisions({ restitution: 0.85 }),
];

const render = [
  new Trails({ trailDecay: 10, trailDiffuse: 4 }),
  new Particles({ colorType: 2, hue: 0.55 }),
];

const engine = new Engine({ canvas, forces, render, runtime: "auto" });

await engine.initialize();
engine.play();
```

## Core concepts

### Particle shape

```ts
type IParticle = {
  position: { x: number; y: number };
  velocity: { x: number; y: number };
  size: number;
  mass: number;
  color: { r: number; g: number; b: number; a: number }; // 0..1 floats
};
```

- Pinned particles: `mass < 0`
- Removed particles: `mass === 0`

### Runtime selection

- `"auto"` tries WebGPU first, then falls back to CPU on `initialize()`.
- WebGPU has higher throughput but GPU → CPU readbacks are expensive.

### Engine lifecycle

```ts
await engine.initialize();
engine.play();   // start loop
engine.pause();  // pause loop
engine.stop();   // cancel loop
engine.destroy(); // clean up
```

### Module system

Modules are typed force or render units:

- **Force**: apply acceleration/velocity changes or constraints.
- **Render**: draw particles/lines or post-process scene texture.

Each module exposes inputs and helpers, and can be toggled:

```ts
const boundary = new Boundary();
boundary.setEnabled(false);
boundary.setRestitution(0.8);
```

## Common tasks

### Add particles

```ts
for (let i = 0; i < 200; i++) {
  engine.addParticle({
    position: { x: Math.random() * 500, y: Math.random() * 500 },
    velocity: { x: (Math.random() - 0.5) * 6, y: (Math.random() - 0.5) * 6 },
    mass: 1,
    size: 3,
    color: { r: 1, g: 1, b: 1, a: 1 },
  });
}
```

### Bulk set particles

```ts
engine.setParticles(particlesArray);
```

### Use the Spawner utility

```ts
import { Spawner } from "@cazala/party";

const spawner = new Spawner();
const particles = spawner.initParticles({
  count: 5000,
  shape: "text",
  text: "Party",
  center: { x: 0, y: 0 },
  position: { x: 0, y: 0 },
  align: { horizontal: "center", vertical: "center" },
  textSize: 80,
  size: 3,
  mass: 1,
  colors: ["#ffffff"],
});

engine.setParticles(particles);
```

### Local queries without full readback (WebGPU-safe)

```ts
const { particles, truncated } = engine.getParticlesInRadius(
  { x: 0, y: 0 },
  120,
  { maxResults: 200 }
);
```

### Export + import module settings

```ts
const settings = engine.export();
engine.import(settings);
```

### Oscillate a module input

```ts
engine.addOscillator({
  moduleName: "boundary",
  inputName: "restitution",
  min: 0.4,
  max: 0.95,
  speedHz: 0.2,
});
```

## Performance notes

- WebGPU `getParticles()` performs a full GPU → CPU readback; avoid in hot paths.
- Prefer `getParticlesInRadius(...)`, `setParticle(...)`, or `setParticleMass(...)`.
- Tune `cellSize`, `maxNeighbors`, and `constrainIterations` for performance.
- For large scenes, limit processing with `setMaxParticles(value)`.

## API quick map

- Engine: `initialize()`, `play()`, `pause()`, `stop()`, `destroy()`
- View: `setSize(w,h)`, `setCamera(x,y)`, `setZoom(z)`
- Particles: `addParticle`, `setParticles`, `setParticle`, `setParticleMass`, `getParticle`
- Queries: `getParticlesInRadius`, `getCount`, `getFPS`
- Modules: `getModule(name)`, module setters, `setEnabled(bool)`
- Serialization: `export()`, `import(settings)`
- Oscillators: `addOscillator`, `removeOscillator`, `clearOscillators`

## Sources

- Core library user guide: `docs/user-guide.md`
