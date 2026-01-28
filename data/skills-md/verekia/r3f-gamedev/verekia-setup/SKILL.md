---
name: verekia-setup
description: Verekia's preferred project setup with Next.js Pages Router, Tailwind 4, Prettier, and TypeScript.
---

# Verekia's Project Setup

Installation instructions and boilerplate for setting up a new R3F game project.

## package.json

```json
{
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "serve out"
  },
  "dependencies": {
    "@react-three/drei": "11.0.0-alpha.4",
    "@react-three/fiber": "10.0.0-alpha.1",
    "miniplex": "2.0.0",
    "miniplex-react": "2.0.1",
    "next": "16.1.2",
    "react": "19.2.3",
    "react-dom": "19.2.3",
    "three": "0.182.0",
    "zustand": "5.0.10"
  },
  "devDependencies": {
    "@tailwindcss/postcss": "4.1.18",
    "@types/node": "25.0.9",
    "@types/react": "19.2.8",
    "@types/react-dom": "19.2.3",
    "@types/three": "0.182.0",
    "babel-plugin-react-compiler": "1.0.0",
    "postcss": "8.5.6",
    "prettier-plugin-tailwindcss": "0.7.2",
    "serve": "14.2.5",
    "tailwindcss": "4.1.18",
    "typescript": "5.9.3"
  },
  "overrides": {
    "three": "0.182.0"
  },
  "patchedDependencies": {
    "three@0.182.0": "patches/three@0.182.0.patch",
    "detect-gpu@5.0.70": "patches/detect-gpu@5.0.70.patch"
  }
}
```

Use Bun as package manager and runtime.

## patches/three@0.182.0.patch

Fixes GPUShaderStage SSR error:

```patch
diff --git a/build/three.webgpu.js b/build/three.webgpu.js
index 31ff163d67f4cc5dec060a11bc7151c64f949fd9..823c1c35bca5411a27cbf52c5c3a188001fe0445 100644
--- a/build/three.webgpu.js
+++ b/build/three.webgpu.js
@@ -70604,7 +70604,7 @@ const GPUPrimitiveTopology = {
 	TriangleStrip: 'triangle-strip',
 };

-const GPUShaderStage = ( typeof self !== 'undefined' ) ? self.GPUShaderStage : { VERTEX: 1, FRAGMENT: 2, COMPUTE: 4 };
+const GPUShaderStage = ( typeof self !== 'undefined' && self.GPUShaderStage ) ? self.GPUShaderStage : { VERTEX: 1, FRAGMENT: 2, COMPUTE: 4 };

 const GPUCompareFunction = {
 	Never: 'never',
```

## patches/detect-gpu@5.0.70.patch

Adds missing exports field:

```patch
diff --git a/package.json b/package.json
index 22ffa92b457c0d83c052eab3f1961110d134d1b3..4f5f9ef7a8a80d6f85e3e5b241a87091d95bbe39 100644
--- a/package.json
+++ b/package.json
@@ -7,6 +7,12 @@
   "main": "dist/detect-gpu.umd.js",
   "module": "dist/detect-gpu.esm.js",
   "types": "dist/src/index.d.ts",
+  "exports": {
+    ".": {
+      "import": "./dist/detect-gpu.esm.js",
+      "require": "./dist/detect-gpu.umd.js"
+    }
+  },
   "homepage": "https://github.com/pmndrs/detect-gpu#readme",
   "bugs": {
     "url": "https://github.com/pmndrs/detect-gpu/issues"
```

Run `bun install` to apply patches.

## next.config.mjs

Use the Pages Router with static export:

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  reactCompiler: true,
  output: 'export',
}

export default nextConfig
```

Pages go in `pages/` directory. Each file becomes a route. `'use client'` directives should not be used since we are in the Pages router.

## global.css

Tailwind 4 uses CSS-based configuration with `@import`. No `tailwind.config.js` needed.

```css
@import 'tailwindcss';

body {
  background-color: #111;
  color: #eee;
}

html,
body,
#__next,
canvas {
  height: 100%;
  width: 100%;
}
```

## prettier.config.js

```js
/** @type {import('prettier').Config & import('prettier-plugin-tailwindcss').PluginOptions} */
export default {
  printWidth: 120,
  semi: false,
  singleQuote: true,
  trailingComma: 'es5',
  arrowParens: 'avoid',
  plugins: ['prettier-plugin-tailwindcss'],
}
```

## tsconfig.json

No `src/` folder - files live at the root. Use `@/` for absolute imports.

No need to create tsconfig.json manually. Run `bun run build` and Next.js will create it. Add the `@/` paths to the generated file:

```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": false,
    "noEmit": true,
    "incremental": true,
    "module": "esnext",
    "esModuleInterop": true,
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "react-jsx",
    "paths": { "@/*": ["./*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
  "exclude": ["node_modules"]
}
```

## .gitignore

```
node_modules/
.next/
out/
.DS_Store
.env*.local
*.tsbuildinfo
analyze/
*.blend1
next-env.d.ts
playwright-report/
.last-run.json
```

## Folder Structure

Create these folders and files:

```
entities/
  entities.tsx (empty)
models/
systems/
stores/
  core-store.ts
  ui-store.ts
  local-store.ts
lib/
  ecs.ts
  hooks.ts
  math.ts
components/
  ModelContainer.tsx
r3f.d.ts
```

## Boilerplate: r3f.d.ts

R3F type declarations for WebGPU. Make sure it's included in your `tsconfig.json`.

```ts
import type { ThreeToJSXElements } from '@react-three/fiber'
import type * as THREE from 'three/webgpu'

declare module '@react-three/fiber' {
  interface ThreeElements extends ThreeToJSXElements<typeof THREE> {}
}
```

## Boilerplate: lib/ecs.ts

```tsx
import { World } from 'miniplex'
import createReactAPI from 'miniplex-react'
import { Object3D } from 'three'

type Entity = {
  position?: { x: number; y: number; z: number }
  velocity?: { x: number; y: number; z: number }
  three?: Object3D
}

export const world = new World<Entity>()

export const { Entities } = createReactAPI(world)
```

## Boilerplate: components/ModelContainer.tsx

```tsx
import { ReactNode } from 'react'
import { Object3D } from 'three'
import { world } from '@/lib/ecs'

type Entity = {
  three?: Object3D
}

export const ModelContainer = ({ children, entity }: { children: ReactNode; entity: Entity }) => (
  <group
    ref={ref => {
      if (!ref) return
      world.addComponent(entity, 'three', ref)
      return () => {
        world.removeComponent(entity, 'three')
      }
    }}
  >
    {children}
  </group>
)
```

## Boilerplate: stores/core-store.ts

```ts
import { create } from 'zustand'

const defaultState = {
  isDebugMode: false,
}

type State = typeof defaultState
type Key = keyof State

const useCoreStore = create<State>(() => structuredClone(defaultState))
export const useCore = <K extends Key>(key: K) => useCoreStore(state => state[key])
export const getCore = useCoreStore.getState
export const setCore = <K extends Key>(...args: [key: K, value: State[K]] | [state: Partial<State>]) =>
  useCoreStore.setState(args.length === 2 ? { [args[0]]: args[1] } : args[0])
export const resetCore = () => useCoreStore.setState(structuredClone(defaultState))

// @ts-expect-error Normal
if (typeof window !== 'undefined') window.getCore = getCore
```

## Boilerplate: stores/ui-store.ts

```ts
import { create } from 'zustand'

const defaultState = {
  areSettingsOpen: false,
}

type State = typeof defaultState
type Key = keyof State

export type UIState = State
export type UIKey = Key

const useUIStore = create<State>(() => structuredClone(defaultState))
export const useUI = <K extends Key>(key: K) => useUIStore(state => state[key])
export const getUI = useUIStore.getState
export const setUI = <K extends Key>(...args: [key: K, value: State[K]] | [state: Partial<State>]) =>
  useUIStore.setState(args.length === 2 ? { [args[0]]: args[1] } : args[0])
export const resetUI = () => setUI(structuredClone(defaultState))

export const isAnyModalOpen = () => {
  const ui = getUI()
  return ui.areSettingsOpen
}

export const closeAnyModal = () => {
  if (getUI().areSettingsOpen) {
    setUI('areSettingsOpen', false)
    return true
  }
  return false
}

export const useIsAnyModalOpen = () => {
  const areSettingsOpen = useUI('areSettingsOpen')
  return areSettingsOpen
}

// @ts-expect-error Normal
if (typeof window !== 'undefined') window.getUI = getUI
```

## Boilerplate: stores/local-store.ts

```ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

const defaultState = {
  hello: 'world',
}

type State = typeof defaultState
type Key = keyof State

const useLocalStore = create<State>()(persist(() => structuredClone(defaultState), { name: 'my-game-local' }))
export const useLocal = <K extends Key>(key: K) => useLocalStore(state => state[key])
export const getLocal = useLocalStore.getState
export const setLocal = <K extends Key>(...args: [key: K, value: State[K]] | [state: Partial<State>]) =>
  useLocalStore.setState(args.length === 2 ? { [args[0]]: args[1] } : args[0])
export const resetLocal = () => setLocal(structuredClone(defaultState))

// @ts-expect-error Normal
if (typeof window !== 'undefined') window.getLocal = getLocal
```

## Boilerplate: lib/hooks.ts

```ts
import { useFrame } from '@react-three/fiber/webgpu'
import { useRef, useState } from 'react'

export const useReactive = <T,>(selector: () => T, fps = 30): T => {
  const [reactiveValue, setReactiveValue] = useState<T>(selector())
  const previousValueRef = useRef(reactiveValue)

  useFrame(
    () => {
      const newValue = selector()
      if (previousValueRef.current !== newValue) {
        previousValueRef.current = newValue
        setReactiveValue(newValue)
      }
    },
    { fps }
  )

  return reactiveValue
}

export const useReactiveSlow = <T,>(selector: () => T): T => useReactive(selector, 10)
export const useReactiveFast = <T,>(selector: () => T): T => useReactive(selector, 30)
```

## Boilerplate: lib/math.ts

```ts
// https://lisyarus.github.io/blog/posts/exponential-smoothing.html
// Usage: `mesh.position.x += addSmoothExp(mesh.position.x, targetX, 10, dt)`
export const addSmoothExp = (current: number, target: number, speed: number, dt: number) =>
  (target - current) * (1 - Math.exp(-speed * dt))
```

---

This skill is part of [verekia](https://x.com/verekia)'s [**r3f-gamedev**](https://github.com/verekia/r3f-gamedev).
