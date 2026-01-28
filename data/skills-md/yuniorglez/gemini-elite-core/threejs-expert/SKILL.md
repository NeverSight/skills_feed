---
name: threejs-expert
description: Senior WebGPU & 3D Graphics Architect for 2026. Specialized in Three.js v172+, WebGPU-first rendering, TSL (Three Shader Language), and high-performance React 19 integration via `@react-three/fiber` and `@react-three/drei`. Expert in building immersive, low-latency, and accessible 3D experiences for the modern web.
---

# 🧊 Skill: threejs-expert (v1.0.0)

## Executive Summary
Senior WebGPU & 3D Graphics Architect for 2026. Specialized in Three.js v172+, WebGPU-first rendering, TSL (Three Shader Language), and high-performance React 19 integration via `@react-three/fiber` and `@react-three/drei`. Expert in building immersive, low-latency, and accessible 3D experiences for the modern web.

---

## 📋 The Conductor's Protocol

1.  **Requirement Decomposition**: Analyze if the 3D scene needs WebGPU (default for 2026) or if a WebGL 2 fallback is necessary for legacy support.
2.  **Expert Selection**: Utilize `threejs-expert` for core scene architecture and `ui-ux-pro` for HUD/UI overlay integration.
3.  **Sequential Activation**:
    `activate_skill(name="threejs-expert")` → `activate_skill(name="react-expert")` → `activate_skill(name="tailwind4-expert")`.
4.  **Verification**: Always use `stats-gl` and `renderer.info` to verify draw calls and VRAM usage.

---

## 🛠️ Mandatory Protocols (2026 Standards)

### 1. WebGPU & TSL First
As of 2026, `WebGPURenderer` is the production standard. Always prioritize asynchronous initialization and TSL for shaders.
- **Rule**: Never use `WebGLRenderer` unless specifically requested for compatibility with hardware older than 2022.
- **Initialization**: Always `await renderer.init()` before the first render loop.

### 2. React 19 & Next.js 16 Integration
- **Direct Mutations**: Use `useFrame` for all frame-by-frame updates (rotations, positions). NEVER use `setState` inside the render loop.
- **PPR (Partial Prerendering)**: Wrap `<Canvas>` in `<Suspense>` to allow Next.js 16 to stream the 3D scene while serving the static shell instantly.
- **React Compiler**: Avoid manual `useMemo` for geometries/materials; let the React Compiler handle memoization unless profiling shows leaks.

### 3. Asset & Performance Hardening
- **Compression**: Use Draco for `.glb` and KTX2 (Basis Universal) for textures.
- **Draw Call Budget**: Keep under 100 draw calls. Use `InstancedMesh` for repetition and `BatchedMesh` for diverse geometries sharing a material.
- **Cleanup**: Explicitly call `.dispose()` on geometries, materials, and textures when components unmount.

---

## 🚀 Show, Don't Just Tell (Implementation Patterns)

### Quick Start: Modern WebGPU Canvas (React 19)
```tsx
"use client";

import { Canvas, useFrame } from "@react-three/fiber";
import { useRef, Suspense } from "react";
import * as THREE from "three";

function RotatingBox() {
  const meshRef = useRef<THREE.Mesh>(null!);

  // Native mutation in React 19 / R3F loop
  useFrame((state, delta) => {
    meshRef.current.rotation.x += delta;
    meshRef.current.rotation.y += delta * 0.5;
  });

  return (
    <mesh ref={meshRef}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="royalblue" />
    </mesh>
  );
}

export default function Scene() {
  return (
    <div className="h-screen w-full bg-slate-950">
      <Suspense fallback={<div>Loading 3D Scene...</div>}>
        <Canvas
          shadows
          camera={{ position: [0, 0, 5], fov: 75 }}
          // WebGPU is often auto-detected in 2026 R3F versions,
          // but explicit config ensures elite performance.
          gl={(canvas) => {
            const renderer = new THREE.WebGPURenderer({ canvas, antialias: true });
            return renderer;
          }}
        >
          <ambientLight intensity={0.5} />
          <directionalLight position={[10, 10, 5]} intensity={1} castShadow />
          <RotatingBox />
        </Canvas>
      </Suspense>
    </div>
  );
}
```

### Advanced Pattern: TSL Shader & Compute (Procedural)
```tsx
import { nodeFrame } from 'three/addons/renderers/webgpu/utils/NodeFrame.js';
import { texture, uv, color, mix, oscSine, timerLocal } from 'three/tsl';

// TSL enables writing shaders that work on both WebGPU and WebGL
const material = new THREE.MeshStandardNodeMaterial();
const time = timerLocal();
const animatedColor = mix(color(0xff0000), color(0x0000ff), oscSine(time));
material.colorNode = animatedColor;
```

---

## 🛡️ The Do Not List (Anti-Patterns)

1.  **DO NOT** create `new THREE.Vector3()` or `new THREE.Color()` inside `useFrame`. It causes massive GC pressure.
2.  **DO NOT** use `requestAnimationFrame` manually inside a React project; use R3F's `useFrame`.
3.  **DO NOT** ignore `renderer.init()`. In WebGPU, failing to await initialization leads to race conditions and black screens.
4.  **DO NOT** use high-poly models for background elements. Use `LOD` (Level of Detail) or `Impostors`.
5.  **DO NOT** load assets without `Suspense`. It blocks the main thread and ruins the UX.

---

## 📂 Progressive Disclosure (Deep Dives)

- **[Performance & Optimization](./references/performance.md)**: Draco, KTX2, Instancing, and BatchedMesh.
- **[WebGPU & TSL Deep Dive](./references/webgpu-tsl.md)**: Moving from GLSL to TSL and Compute Shaders.
- **[Next.js 16 & PPR Integration](./references/nextjs-integration.md)**: Streaming 3D content and proxy boundaries.
- **[React-Three-Fiber Patterns](./references/r3f-patterns.md)**: Hooks, Portals, and Advanced Composition.

---

## 🛠️ Specialized Tools & Scripts

- `scripts/validate-assets.ts`: Checks for uncompressed textures or high-poly counts in the project.
- `scripts/generate-tsl-boilerplate.py`: Scaffolds a TSL shader node.

---

## 🎓 Learning Resources
- [Three.js Manual (v172+)](https://threejs.org/manual/)
- [React Three Fiber Docs](https://docs.pmnd.rs/react-three-fiber)
- [WebGPU Explorer 2026](https://webgpu.rocks/)

---
*Updated: January 23, 2026 - 15:45*
