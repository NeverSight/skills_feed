---
name: r3f-fundamentals
description: React Three Fiber core setup, Canvas configuration, scene hierarchy, camera systems, lighting, render loop, and React integration patterns. Use when setting up a new R3F project, configuring the Canvas component, managing scene structure, or understanding the declarative Three.js-in-React paradigm. The foundational skill that all other R3F skills depend on.
---

# React Three Fiber Fundamentals

Declarative Three.js via React components. R3F maps Three.js objects to JSX elements with automatic disposal, reactive updates, and React lifecycle integration.

## Quick Start

```tsx
import { Canvas } from '@react-three/fiber';

function App() {
  return (
    <Canvas>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      <mesh>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial color="hotpink" />
      </mesh>
    </Canvas>
  );
}
```

## Core Principle: Declarative Scene Graph

R3F converts Three.js imperative API to React's declarative model:

| Three.js (Imperative) | R3F (Declarative) |
|----------------------|-------------------|
| `new THREE.Mesh()` | `<mesh>` |
| `mesh.position.set(1, 2, 3)` | `<mesh position={[1, 2, 3]}>` |
| `scene.add(mesh)` | JSX nesting handles hierarchy |
| `mesh.geometry.dispose()` | Automatic on unmount |

## Canvas Configuration

```tsx
import { Canvas } from '@react-three/fiber';

<Canvas
  // Renderer settings
  gl={{ antialias: true, alpha: false, powerPreference: 'high-performance' }}
  dpr={[1, 2]}                    // Device pixel ratio range
  shadows                          // Enable shadow maps
  
  // Camera (default: PerspectiveCamera)
  camera={{ 
    fov: 75, 
    near: 0.1, 
    far: 1000, 
    position: [0, 0, 5] 
  }}
  
  // Or use orthographic
  orthographic
  camera={{ zoom: 50, position: [0, 0, 100] }}
  
  // Performance
  frameloop="demand"              // 'always' | 'demand' | 'never'
  performance={{ min: 0.5 }}      // Adaptive performance
  
  // Events
  onCreated={({ gl, scene, camera }) => {
    // Access Three.js objects after mount
  }}
  
  // Sizing
  style={{ width: '100vw', height: '100vh' }}
/>
```

### Frameloop Modes

| Mode | When to Use |
|------|-------------|
| `always` | Continuous animation (games, simulations) |
| `demand` | Static scenes, only re-render on state change |
| `never` | Manual control via `invalidate()` |

```tsx
// Demand mode with manual invalidation
import { useThree } from '@react-three/fiber';

function Controls() {
  const invalidate = useThree(state => state.invalidate);
  
  const handleDrag = () => {
    // Update state...
    invalidate(); // Request re-render
  };
}
```

## Scene Hierarchy

JSX nesting = Three.js parent-child relationships:

```tsx
<group position={[0, 2, 0]} rotation={[0, Math.PI / 4, 0]}>
  {/* Children inherit parent transforms */}
  <mesh position={[1, 0, 0]}>
    <sphereGeometry args={[0.5, 32, 32]} />
    <meshStandardMaterial color="blue" />
  </mesh>
  
  <mesh position={[-1, 0, 0]}>
    <boxGeometry args={[0.8, 0.8, 0.8]} />
    <meshStandardMaterial color="red" />
  </mesh>
</group>
```

### Common Container Components

```tsx
// Group: Transform container (no rendering)
<group position={[0, 0, 0]} />

// Object3D: Base class, rarely used directly
<object3D />

// Scene: Usually implicit (Canvas creates one)
<scene />
```

## Camera Systems

### Default Perspective Camera

```tsx
<Canvas camera={{ 
  fov: 75,              // Field of view (degrees)
  aspect: width/height, // Auto-calculated
  near: 0.1,            // Near clipping plane
  far: 1000,            // Far clipping plane
  position: [0, 5, 10]
}} />
```

### Custom Camera Component

```tsx
import { PerspectiveCamera } from '@react-three/drei';

function Scene() {
  return (
    <>
      <PerspectiveCamera 
        makeDefault           // Set as active camera
        fov={60} 
        position={[0, 2, 8]} 
      />
      {/* Scene contents */}
    </>
  );
}
```

### Camera Access

```tsx
import { useThree } from '@react-three/fiber';

function CameraController() {
  const { camera } = useThree();
  
  useEffect(() => {
    camera.lookAt(0, 0, 0);
  }, [camera]);
  
  return null;
}
```

## Lighting

### Light Types

```tsx
// Ambient: Uniform, directionless
<ambientLight intensity={0.4} color="#ffffff" />

// Directional: Sun-like, parallel rays
<directionalLight 
  position={[5, 10, 5]} 
  intensity={1} 
  castShadow 
/>

// Point: Radiates from position
<pointLight 
  position={[0, 5, 0]} 
  intensity={1} 
  distance={20}        // Range (0 = infinite)
  decay={2}            // Physical falloff
/>

// Spot: Cone-shaped
<spotLight 
  position={[0, 10, 0]} 
  angle={Math.PI / 6}  // Cone angle
  penumbra={0.5}       // Edge softness
  castShadow 
/>

// Hemisphere: Sky/ground gradient
<hemisphereLight 
  skyColor="#87ceeb" 
  groundColor="#362907" 
  intensity={0.6} 
/>
```

### Shadow Setup

```tsx
<Canvas shadows>
  <directionalLight
    castShadow
    position={[10, 10, 10]}
    shadow-mapSize={[2048, 2048]}
    shadow-camera-far={50}
    shadow-camera-left={-10}
    shadow-camera-right={10}
    shadow-camera-top={10}
    shadow-camera-bottom={-10}
  />
  
  <mesh castShadow>
    <boxGeometry />
    <meshStandardMaterial />
  </mesh>
  
  <mesh receiveShadow rotation={[-Math.PI / 2, 0, 0]} position={[0, -1, 0]}>
    <planeGeometry args={[20, 20]} />
    <meshStandardMaterial />
  </mesh>
</Canvas>
```

## Render Loop (useFrame)

`useFrame` runs every frame (60fps target). This is where animation happens.

```tsx
import { useFrame, useThree } from '@react-three/fiber';
import { useRef } from 'react';

function RotatingBox() {
  const meshRef = useRef<THREE.Mesh>(null!);
  
  useFrame((state, delta) => {
    // state: R3F state (camera, scene, clock, etc.)
    // delta: Time since last frame (seconds)
    
    meshRef.current.rotation.x += delta;
    meshRef.current.rotation.y += delta * 0.5;
  });
  
  return (
    <mesh ref={meshRef}>
      <boxGeometry />
      <meshNormalMaterial />
    </mesh>
  );
}
```

### useFrame State Object

```tsx
useFrame((state) => {
  state.clock        // THREE.Clock
  state.clock.elapsedTime  // Total time (seconds)
  state.camera       // Active camera
  state.scene        // Scene object
  state.gl           // WebGLRenderer
  state.size         // { width, height }
  state.viewport     // { width, height, factor, distance }
  state.mouse        // Normalized mouse position [-1, 1]
  state.raycaster    // THREE.Raycaster
});
```

### Render Priority

```tsx
// Lower priority runs first, higher runs later
// Default is 0

useFrame(() => {
  // Update physics
}, -1);  // Runs before default

useFrame(() => {
  // Update visuals
}, 0);   // Default

useFrame(() => {
  // Post-processing / camera
}, 1);   // Runs after default
```

## Accessing Three.js Objects

### useThree Hook

```tsx
import { useThree } from '@react-three/fiber';

function SceneInfo() {
  const { 
    gl,           // WebGLRenderer
    scene,        // THREE.Scene
    camera,       // Active camera
    size,         // Canvas dimensions
    viewport,     // Viewport in Three.js units
    clock,        // THREE.Clock
    set,          // Update state
    get,          // Get current state
    invalidate,   // Request re-render (demand mode)
    advance,      // Advance one frame (never mode)
  } = useThree();
  
  return null;
}
```

### Refs for Direct Access

```tsx
import { useRef } from 'react';
import * as THREE from 'three';

function DirectAccess() {
  const meshRef = useRef<THREE.Mesh>(null!);
  const materialRef = useRef<THREE.MeshStandardMaterial>(null!);
  
  useEffect(() => {
    // Direct Three.js API access
    meshRef.current.geometry.computeBoundingBox();
    materialRef.current.needsUpdate = true;
  }, []);
  
  return (
    <mesh ref={meshRef}>
      <boxGeometry />
      <meshStandardMaterial ref={materialRef} />
    </mesh>
  );
}
```

## Events

R3F provides pointer events on meshes:

```tsx
<mesh
  onClick={(e) => console.log('click', e.point)}
  onContextMenu={(e) => console.log('right click')}
  onDoubleClick={(e) => console.log('double click')}
  onPointerOver={(e) => console.log('hover')}
  onPointerOut={(e) => console.log('unhover')}
  onPointerDown={(e) => console.log('down')}
  onPointerUp={(e) => console.log('up')}
  onPointerMove={(e) => console.log('move')}
>
  <boxGeometry />
  <meshStandardMaterial />
</mesh>
```

### Event Object

```tsx
onClick={(e) => {
  e.stopPropagation();    // Stop event bubbling
  e.point                 // THREE.Vector3 intersection point
  e.distance              // Distance from camera
  e.object                // Intersected object
  e.face                  // Intersected face
  e.faceIndex             // Face index
  e.uv                    // UV coordinates
  e.camera                // Camera used for raycasting
  e.delta                 // Distance from last event
}}
```

## Suspense & Loading

R3F integrates with React Suspense for async loading:

```tsx
import { Suspense } from 'react';
import { useLoader } from '@react-three/fiber';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';

function Model() {
  const gltf = useLoader(GLTFLoader, '/model.glb');
  return <primitive object={gltf.scene} />;
}

function App() {
  return (
    <Canvas>
      <Suspense fallback={<LoadingSpinner />}>
        <Model />
      </Suspense>
    </Canvas>
  );
}

function LoadingSpinner() {
  const meshRef = useRef<THREE.Mesh>(null!);
  useFrame((_, delta) => {
    meshRef.current.rotation.z += delta * 2;
  });
  
  return (
    <mesh ref={meshRef}>
      <torusGeometry args={[1, 0.2, 16, 32]} />
      <meshBasicMaterial color="white" wireframe />
    </mesh>
  );
}
```

## Dependencies

```json
{
  "dependencies": {
    "@react-three/fiber": "^8.15.0",
    "three": "^0.160.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/three": "^0.160.0"
  }
}
```

## File Structure

```
r3f-fundamentals/
├── SKILL.md
├── references/
│   ├── canvas-props.md       # Complete Canvas prop reference
│   ├── hooks-api.md          # useThree, useFrame, useLoader
│   └── event-system.md       # Event handling deep-dive
└── scripts/
    ├── templates/
    │   ├── basic-scene.tsx   # Minimal starter
    │   ├── lit-scene.tsx     # With proper lighting
    │   └── interactive.tsx   # With events and animation
    └── utils/
        └── canvas-config.ts  # Preset configurations
```

## Reference

- `references/canvas-props.md` — Complete Canvas configuration options
- `references/hooks-api.md` — All R3F hooks with examples
- `references/event-system.md` — Pointer events and raycasting
