---
name: rive-web
description: |
  Trigger when: (1) Loading or embedding .riv files on the web,
  (2) Using @rive-app/canvas or @rive-app/webgl packages,
  (3) Controlling Rive state machines from JavaScript,
  (4) Reading/writing Rive inputs or handling events,
  (5) User mentions "Rive runtime" or "Rive animation" in web context.

  Best practices for embedding and controlling Rive animations on the web
  using the official Rive JavaScript/TypeScript runtime.
metadata:
  tags: rive, web, javascript, typescript, animation, runtime
---

# Rive Web Runtime

Embed and control Rive animations on the web with JavaScript/TypeScript.

## Installation

```bash
# Canvas renderer (smaller, good for most cases)
npm install @rive-app/canvas

# WebGL renderer (better for complex animations)
npm install @rive-app/webgl
```

## Quick Start

```typescript
import { Rive } from '@rive-app/canvas';

const rive = new Rive({
  src: 'animation.riv',
  canvas: document.getElementById('canvas') as HTMLCanvasElement,
  autoplay: true,
  onLoad: () => {
    console.log('Animation loaded');
  },
});
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Rive Instance** | Main controller for the animation |
| **State Machine** | Interactive logic built in Rive editor |
| **Inputs** | Variables to control state machine (Boolean, Number, Trigger) |
| **Events** | Signals fired by the state machine |
| **Artboard** | Container for animation content |

## Common Patterns

### Loading Animation

```typescript
const rive = new Rive({
  src: 'animation.riv',           // URL or path
  canvas: canvasElement,
  stateMachines: 'State Machine', // Name from Rive editor
  autoplay: true,
  onLoad: () => {
    // Animation ready
  },
  onStateChange: (event) => {
    // State changed
  },
});
```

### Controlling Inputs

```typescript
// Get inputs
const inputs = rive.stateMachineInputs('State Machine');

// Set boolean
const toggle = inputs.find(i => i.name === 'isActive');
toggle.value = true;

// Set number
const progress = inputs.find(i => i.name === 'progress');
progress.value = 0.75;

// Fire trigger
const click = inputs.find(i => i.name === 'onClick');
click.fire();
```

### Handling Events

```typescript
rive.on('riveevent', (event) => {
  console.log('Event:', event.data.name);
  // Access custom properties
  const data = event.data.properties;
});
```

## Cleanup

```typescript
// Always cleanup when done
rive.cleanup();
```

## Rules

@file rules/loading.md
@file rules/state-machines.md
@file rules/inputs.md
