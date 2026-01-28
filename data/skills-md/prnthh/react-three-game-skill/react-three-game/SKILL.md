---
name: react-three-game
description: react-three-game, a JSON-first 3D game engine built on React Three Fiber, WebGPU, and Rapier Physics.
---

# react-three-game

Instructions for the agent to follow when this skill is activated.

## When to use

generate 3D scenes, games and physics simulations in React.

## Agent Workflow: JSON → GLB

Agents can programmatically generate 3D assets:

1. Create a JSON prefab following the GameObject schema
2. Load it in `PrefabEditor` to render the Three.js scene
3. Export the scene to GLB format using `exportGLB` or `exportGLBData`

```tsx
import { useRef, useEffect } from 'react';
import { PrefabEditor, exportGLBData } from 'react-three-game';
import type { PrefabEditorRef } from 'react-three-game'

const jsonPrefab = {
  root: {
    id: "scene",
    children: [
      {
        id: "cube",
        components: {
          transform: { type: "Transform", properties: { position: [0, 0, 0] } },
          geometry: { type: "Geometry", properties: { geometryType: "box", args: [1, 1, 1] } },
          material: { type: "Material", properties: { color: "#ff0000" } }
        }
      }
    ]
  }
};

function AgentExporter() {
  const editorRef = useRef<PrefabEditorRef>(null);

  useEffect(() => {
    const timer = setTimeout(async () => {
      const sceneRoot = editorRef.current?.rootRef.current?.root;
      if (!sceneRoot) return;
      
      const glbData = await exportGLBData(sceneRoot);
      // glbData is an ArrayBuffer ready for upload/storage
    }, 1000); // Wait for scene to render
    
    return () => clearTimeout(timer);
  }, []);

  return <PrefabEditor ref={editorRef} initialPrefab={jsonPrefab} />;
}
```

## Core Concepts

### Asset Paths and Public Directory

**All asset paths are relative to `/public`** and omit the `/public` prefix:

```json
{
  "texture": "/textures/floor.png",
  "model": "/models/car.glb",
  "font": "/fonts/font.ttf"
}
```

Path `"/any/path/file.ext"` refers to `/public/any/path/file.ext`.
### GameObject Structure

Every game object follows this schema:

```typescript
interface GameObject {
  id: string;
  disabled?: boolean;
  components?: Record<string, { type: string; properties: any }>;
  children?: GameObject[];
}
```

### Prefab JSON Format

Scenes are defined as JSON prefabs with a root node containing children:

```json
{
  "root": {
    "id": "scene",
    "children": [
      {
        "id": "my-object",
        "components": {
          "transform": { "type": "Transform", "properties": { "position": [0, 0, 0] } },
          "geometry": { "type": "Geometry", "properties": { "geometryType": "box" } },
          "material": { "type": "Material", "properties": { "color": "#ff0000" } }
        }
      }
    ]
  }
}
```

## Built-in Components

| Component | Type | Key Properties |
|-----------|------|----------------|
| Transform | `Transform` | `position: [x,y,z]`, `rotation: [x,y,z]` (radians), `scale: [x,y,z]` |
| Geometry | `Geometry` | `geometryType`: box/sphere/plane/cylinder, `args`: dimension array |
| Material | `Material` | `color`, `texture?`, `metalness?`, `roughness?`, `repeat?`, `repeatCount?` |
| Physics | `Physics` | `type`: dynamic/fixed/kinematicPosition/kinematicVelocity, `mass?`, `restitution?`, `friction?`, `linearDamping?`, `angularDamping?`, `gravityScale?`, `sensor?`, `activeCollisionTypes?: 'all'` (enable kinematic/fixed collision detection), plus any Rapier RigidBody props - [See advanced physics guide](./rules/ADVANCED_PHYSICS.md) |
| Model | `Model` | `filename` (GLB/FBX path), `instanced?` for GPU batching |
| SpotLight | `SpotLight` | `color`, `intensity`, `angle`, `penumbra`, `distance?`, `castShadow?` |
| DirectionalLight | `DirectionalLight` | `color`, `intensity`, `castShadow?`, `targetOffset?: [x,y,z]` |
| AmbientLight | `AmbientLight` | `color`, `intensity` |
| Text | `Text` | `text`, `font`, `size`, `depth`, `width`, `align`, `color` |

### Text Component

Requires `hb.wasm` and a font file (TTF/WOFF) in `/public/fonts/`:
- hb.wasm: https://github.com/prnthh/react-three-game/raw/refs/heads/main/docs/public/fonts/hb.wasm
- Sample font: https://github.com/prnthh/react-three-game/raw/refs/heads/main/docs/public/fonts/NotoSans-Regular.ttf

Font property: `"font": "/fonts/NotoSans-Regular.ttf"`

### Geometry Args by Type

| geometryType | args array |
|--------------|------------|
| `box` | `[width, height, depth]` |
| `sphere` | `[radius, widthSegments, heightSegments]` |
| `plane` | `[width, height]` |
| `cylinder` | `[radiusTop, radiusBottom, height, radialSegments]` |

### Material Textures

```json
{
  "material": {
    "type": "Material",
    "properties": {
      "color": "white",
      "texture": "/textures/floor.png",
      "repeat": true,
      "repeatCount": [4, 4]
    }
  }
}
```

### Rotations

Use radians: `1.57` = 90°, `3.14` = 180°, `-1.57` = -90°

## Common Patterns

### Usage Modes

**GameCanvas + PrefabRoot**: Pure renderer for embedding prefab data in standard R3F applications. Minimal wrapper - just renders the prefab as Three.js objects. Requires manual `<Physics>` setup. Physics always active. Use this to integrate prefabs into larger R3F scenes.

```jsx
import { Physics } from '@react-three/rapier';
import { GameCanvas, PrefabRoot } from 'react-three-game';

<GameCanvas>
  <Physics>
    <PrefabRoot data={prefabData} />
    <CustomComponent />
  </Physics>
</GameCanvas>
```

**PrefabEditor**: Managed scene with editor UI and play/pause controls for physics. Full authoring tool for level design and prototyping. Includes canvas, physics, transform gizmos, and inspector. Physics only runs in play mode. Can pass R3F components as children.

```jsx
import { PrefabEditor } from 'react-three-game';

<PrefabEditor initialPrefab={prefabData}>
  <CustomComponent />
</PrefabEditor>
```

### Tree Utilities

```typescript
import { findNode, updateNode, updateNodeById, deleteNode, cloneNode, exportGLBData } from 'react-three-game';

const node = findNode(root, nodeId);
const updated = updateNode(root, nodeId, n => ({ ...n, disabled: true }));  // or updateNodeById (identical)
const afterDelete = deleteNode(root, nodeId);
const cloned = cloneNode(node);
const glbData = await exportGLBData(sceneRoot);
```

## Hybrid JSON + R3F Children Pattern

**Prefabs define static scene structure, R3F children add dynamic behavior**:

```tsx
import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { PrefabEditor, findNode } from 'react-three-game';
import type { PrefabEditorRef } from 'react-three-game';

function DynamicLight() {
  const lightRef = useRef<THREE.SpotLight>(null!);
  
  useFrame(({ clock }) => {
    lightRef.current.intensity = 100 + Math.sin(clock.elapsedTime) * 50;
  });
  
  return <spotLight ref={lightRef} position={[10, 15, 10]} angle={0.5} />;
}

<PrefabEditor initialPrefab={staticScenePrefab}>
  <DynamicLight />
  <CustomController />
</PrefabEditor>
```

**Use cases**: Player controllers, AI behaviors, procedural animation, real-time effects.

## Quick Reference Examples

```json
// Static geometry with physics (floor, wall, platform, ramp)
{ "id": "floor", "components": {
  "transform": { "type": "Transform", "properties": { "position": [0, -0.5, 0] } },
  "geometry": { "type": "Geometry", "properties": { "geometryType": "box", "args": [40, 1, 40] } },
  "material": { "type": "Material", "properties": { "texture": "/textures/floor.png", "repeat": true, "repeatCount": [20, 20] } },
  "physics": { "type": "Physics", "properties": { "type": "fixed" } }
}}

// Lighting
{ "id": "spot", "components": {
  "transform": { "type": "Transform", "properties": { "position": [10, 15, 10] } },
  "spotlight": { "type": "SpotLight", "properties": { "intensity": 200, "angle": 0.8, "castShadow": true } }
}}

// 3D Text
{ "id": "title", "components": {
  "transform": { "type": "Transform", "properties": { "position": [0, 3, 0] } },
  "text": { "type": "Text", "properties": { "text": "Welcome", "font": "/fonts/font.ttf", "size": 1, "depth": 0.1 } }
}}

// GLB Model
{ "id": "tree", "components": {
  "transform": { "type": "Transform", "properties": { "position": [0, 0, 0], "scale": [1.5, 1.5, 1.5] } },
  "model": { "type": "Model", "properties": { "filename": "/models/tree.glb" } }
}}
```

## Editor

### Basic Usage

```jsx
import { PrefabEditor } from 'react-three-game';

<PrefabEditor initialPrefab={sceneData} onPrefabChange={setSceneData} />
```

Keyboard shortcuts: **T** (Translate), **R** (Rotate), **S** (Scale)

### Camera Control

By default, `PrefabEditor` uses an orbit camera. **Override it by adding a custom camera with `makeDefault`**:

```tsx
import { PerspectiveCamera } from '@react-three/drei';
import { PrefabEditor } from 'react-three-game';

<PrefabEditor initialPrefab={prefab}>
  <PerspectiveCamera makeDefault position={[0, 5, 10]} fov={75} />
</PrefabEditor>
```

Any R3F camera component works: `PerspectiveCamera`, `OrthographicCamera`, or custom camera controllers.

### Programmatic Updates

```jsx
import { useRef } from 'react';
import { PrefabEditor, updateNodeById } from 'react-three-game';
import type { PrefabEditorRef } from 'react-three-game';

function Scene() {
  const editorRef = useRef<PrefabEditorRef>(null);

  const moveBall = () => {
    const prefab = editorRef.current!.prefab;
    const newRoot = updateNodeById(prefab.root, "ball", node => ({
      ...node,
      components: {
        ...node.components,
        transform: {
          ...node.components!.transform!,
          properties: { ...node.components!.transform!.properties, position: [5, 0, 0] }
        }
      }
    }));
    editorRef.current!.setPrefab({ ...prefab, root: newRoot });
  };

  return <PrefabEditor ref={editorRef} initialPrefab={sceneData} />;
}
```

**PrefabEditorRef**: `prefab`, `setPrefab()`, `screenshot()`, `exportGLB()`, `rootRef`

### GLB Export

```tsx
import { exportGLBData } from 'react-three-game';

const glbData = await exportGLBData(editorRef.current!.rootRef.current!.root);
```

### Runtime Animation

```tsx
import { useRef } from "react";
import { useFrame } from "@react-three/fiber";
import { PrefabEditor, updateNodeById } from "react-three-game";

function Animator({ editorRef }) {
  useFrame(() => {
    const prefab = editorRef.current!.prefab;
    const newRoot = updateNodeById(prefab.root, "ball", node => ({
      ...node,
      components: {
        ...node.components,
        transform: {
          ...node.components!.transform!,
          properties: { ...node.components!.transform!.properties, position: [x, y, z] }
        }
      }
    }));
    editorRef.current!.setPrefab({ ...prefab, root: newRoot });
  });
  return null;
}

function Scene() {
  const editorRef = useRef(null);
  return (
    <PrefabEditor ref={editorRef} initialPrefab={data}>
      <Animator editorRef={editorRef} />
    </PrefabEditor>
  );
}
```

### Custom Component

```tsx
import { Component, registerComponent, FieldRenderer } from 'react-three-game';

const MyComponent: Component = {
  name: 'MyComponent',
  Editor: ({ component, onUpdate }) => (
    <FieldRenderer fields={[{ name: 'speed', type: 'number', step: 0.1 }]} values={component.properties} onChange={onUpdate} />
  ),
  View: ({ properties, children }) => <group>{children}</group>,
  defaultProperties: { speed: 1 }
};

registerComponent(MyComponent);
```

**Field types**: `vector3`, `number`, `string`, `color`, `boolean`, `select`, `custom`

## Game Events

A general-purpose event system for game-wide communication. Handles physics events, gameplay events, and any custom events.

### Core API

```tsx
import { gameEvents, useGameEvent } from 'react-three-game';

// Emit events
gameEvents.emit('player:death', { playerId: 'p1', cause: 'lava' });
gameEvents.emit('score:change', { delta: 100, total: 500 });

// Subscribe (React hook - auto cleanup on unmount)
useGameEvent('player:death', (payload) => {
  showGameOver(payload.cause);
}, []);

// Subscribe (manual - returns unsubscribe function)
const unsub = gameEvents.on('score:change', (payload) => {
  updateUI(payload.total);
});
unsub(); // cleanup
```

### Built-in Physics Events

Physics components automatically emit these events:

| Event | When | Payload |
|-------|------|---------|
| `sensor:enter` | Something enters a sensor collider | `{ sourceEntityId, targetEntityId, targetRigidBody }` |
| `sensor:exit` | Something exits a sensor collider | `{ sourceEntityId, targetEntityId, targetRigidBody }` |
| `collision:enter` | A collision starts | `{ sourceEntityId, targetEntityId, targetRigidBody }` |
| `collision:exit` | A collision ends | `{ sourceEntityId, targetEntityId, targetRigidBody }` |

**Collision filtering**: By default, kinematic/fixed bodies don't detect each other. For kinematic sensors or projectiles to detect walls/floors, add `"activeCollisionTypes": "all"` to the Physics properties.

See [Advanced Physics](./rules/ADVANCED_PHYSICS.md) for sensor setup and collision handling patterns.

### TypeScript: Typed Custom Events

Extend `GameEventMap` for type-safe custom events:

```typescript
declare module 'react-three-game' {
  interface GameEventMap {
    'player:death': { playerId: string; cause: string };
    'score:change': { delta: number; total: number };
    'level:complete': { levelId: number; time: number };
  }
}
```

### Common Patterns

```tsx
// Gameplay controller
function GameController() {
  const [score, setScore] = useState(0);

  useGameEvent('score:change', ({ total }) => setScore(total), []);
  useGameEvent('player:death', () => setGameOver(true), []);

  return <ScoreUI score={score} />;
}

// Pickup system
useGameEvent('sensor:enter', (payload) => {
  if (payload.sourceEntityId.startsWith('coin-')) {
    gameEvents.emit('score:change', { delta: 10, total: score + 10 });
    removeEntity(payload.sourceEntityId);
  }
}, [score]);
```

