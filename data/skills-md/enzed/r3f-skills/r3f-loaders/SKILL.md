---
name: r3f-loaders
description: React Three Fiber asset loading - useGLTF, useLoader, Suspense patterns, preloading. Use when loading 3D models, textures, HDR environments, or managing loading states.
---

# React Three Fiber Loaders

## Quick Start

```tsx
import { Canvas } from '@react-three/fiber'
import { useGLTF, OrbitControls } from '@react-three/drei'
import { Suspense } from 'react'

function Model() {
  const { scene } = useGLTF('/models/robot.glb')
  return <primitive object={scene} />
}

export default function App() {
  return (
    <Canvas>
      <ambientLight />
      <Suspense fallback={null}>
        <Model />
      </Suspense>
      <OrbitControls />
    </Canvas>
  )
}
```

## useGLTF (Drei)

The recommended way to load GLTF/GLB models.

### Basic Usage

```tsx
import { useGLTF } from '@react-three/drei'

function Model() {
  const gltf = useGLTF('/models/robot.glb')

  // gltf contains:
  // - scene: THREE.Group (the main scene)
  // - nodes: Object of named meshes
  // - materials: Object of named materials
  // - animations: Array of AnimationClip

  return <primitive object={gltf.scene} />
}
```

### Using Nodes and Materials

```tsx
function Model() {
  const { nodes, materials } = useGLTF('/models/robot.glb')

  return (
    <group>
      {/* Use specific meshes */}
      <mesh
        geometry={nodes.Body.geometry}
        material={materials.Metal}
        position={[0, 0, 0]}
      />
      <mesh
        geometry={nodes.Head.geometry}
        material={materials.Plastic}
        position={[0, 1, 0]}
      />
    </group>
  )
}
```

### With TypeScript (gltfjsx)

Generate typed components using gltfjsx:

```bash
npx gltfjsx model.glb --types
```

```tsx
// Generated component
import { useGLTF } from '@react-three/drei'
import { GLTF } from 'three-stdlib'

type GLTFResult = GLTF & {
  nodes: {
    Body: THREE.Mesh
    Head: THREE.Mesh
  }
  materials: {
    Metal: THREE.MeshStandardMaterial
    Plastic: THREE.MeshStandardMaterial
  }
}

export function Model(props: JSX.IntrinsicElements['group']) {
  const { nodes, materials } = useGLTF('/model.glb') as GLTFResult

  return (
    <group {...props} dispose={null}>
      <mesh geometry={nodes.Body.geometry} material={materials.Metal} />
      <mesh geometry={nodes.Head.geometry} material={materials.Plastic} />
    </group>
  )
}

useGLTF.preload('/model.glb')
```

### Draco Compression

```tsx
import { useGLTF } from '@react-three/drei'

function Model() {
  // Drei automatically handles Draco if the file is Draco-compressed
  const { scene } = useGLTF('/models/compressed.glb')
  return <primitive object={scene} />
}

// Or specify Draco decoder path
useGLTF.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/')
```

### Preloading

```tsx
import { useGLTF } from '@react-three/drei'

// Preload at module level
useGLTF.preload('/models/robot.glb')
useGLTF.preload(['/model1.glb', '/model2.glb'])

function Model() {
  // Will be instant if preloaded
  const { scene } = useGLTF('/models/robot.glb')
  return <primitive object={scene} />
}
```

### Processing Loaded Model

```tsx
function Model() {
  const { scene } = useGLTF('/models/robot.glb')

  useEffect(() => {
    // Enable shadows on all meshes
    scene.traverse((child) => {
      if (child.isMesh) {
        child.castShadow = true
        child.receiveShadow = true
      }
    })
  }, [scene])

  return <primitive object={scene} />
}
```

## useLoader (Core R3F)

For loading any Three.js asset.

### Basic Texture Loading

```tsx
import { useLoader } from '@react-three/fiber'
import { TextureLoader } from 'three'

function TexturedMesh() {
  const texture = useLoader(TextureLoader, '/textures/color.jpg')

  return (
    <mesh>
      <boxGeometry />
      <meshStandardMaterial map={texture} />
    </mesh>
  )
}
```

### Multiple Assets

```tsx
function MultiTexture() {
  const [colorMap, normalMap, roughnessMap] = useLoader(TextureLoader, [
    '/textures/color.jpg',
    '/textures/normal.jpg',
    '/textures/roughness.jpg',
  ])

  return (
    <mesh>
      <sphereGeometry args={[1, 64, 64]} />
      <meshStandardMaterial
        map={colorMap}
        normalMap={normalMap}
        roughnessMap={roughnessMap}
      />
    </mesh>
  )
}
```

### With Extensions (Draco)

```tsx
import { useLoader } from '@react-three/fiber'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader'

function Model() {
  const gltf = useLoader(GLTFLoader, '/model.glb', (loader) => {
    const dracoLoader = new DRACOLoader()
    dracoLoader.setDecoderPath('https://www.gstatic.com/draco/v1/decoders/')
    loader.setDRACOLoader(dracoLoader)
  })

  return <primitive object={gltf.scene} />
}
```

### Progress Callback

```tsx
function Model() {
  const gltf = useLoader(
    GLTFLoader,
    '/model.glb',
    undefined,  // extensions
    (progress) => {
      console.log(`Loading: ${(progress.loaded / progress.total) * 100}%`)
    }
  )

  return <primitive object={gltf.scene} />
}
```

### Preloading

```tsx
import { useLoader } from '@react-three/fiber'
import { TextureLoader } from 'three'

// Preload
useLoader.preload(TextureLoader, '/textures/color.jpg')
useLoader.preload(TextureLoader, ['/tex1.jpg', '/tex2.jpg'])

// Clear cache
useLoader.clear(TextureLoader, '/textures/color.jpg')
```

## Drei Loader Hooks

### useTexture

```tsx
import { useTexture } from '@react-three/drei'

// Single
const texture = useTexture('/texture.jpg')

// Array
const [color, normal] = useTexture(['/color.jpg', '/normal.jpg'])

// Named object (spreads directly to material)
const textures = useTexture({
  map: '/color.jpg',
  normalMap: '/normal.jpg',
  roughnessMap: '/roughness.jpg',
})
<meshStandardMaterial {...textures} />

// With callback for configuration
const texture = useTexture('/texture.jpg', (tex) => {
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping
  tex.repeat.set(4, 4)
})

// Preload
useTexture.preload('/texture.jpg')
```

### useCubeTexture

```tsx
import { useCubeTexture } from '@react-three/drei'

function EnvMap() {
  const envMap = useCubeTexture(
    ['px.jpg', 'nx.jpg', 'py.jpg', 'ny.jpg', 'pz.jpg', 'nz.jpg'],
    { path: '/textures/cube/' }
  )

  return (
    <mesh>
      <sphereGeometry />
      <meshStandardMaterial envMap={envMap} metalness={1} roughness={0} />
    </mesh>
  )
}
```

### useEnvironment

```tsx
import { useEnvironment } from '@react-three/drei'

// Preset
const envMap = useEnvironment({ preset: 'sunset' })
// Presets: apartment, city, dawn, forest, lobby, night, park, studio, sunset, warehouse

// Custom HDR file
const envMap = useEnvironment({ files: '/hdri/studio.hdr' })

// Cube map
const envMap = useEnvironment({
  files: ['px.jpg', 'nx.jpg', 'py.jpg', 'ny.jpg', 'pz.jpg', 'nz.jpg'],
  path: '/textures/',
})
```

### useVideoTexture

```tsx
import { useVideoTexture } from '@react-three/drei'

function VideoPlane() {
  const texture = useVideoTexture('/video.mp4', {
    start: true,
    loop: true,
    muted: true,
    crossOrigin: 'anonymous',
  })

  return (
    <mesh>
      <planeGeometry args={[16/9 * 2, 2]} />
      <meshBasicMaterial map={texture} toneMapped={false} />
    </mesh>
  )
}
```

### useFont

```tsx
import { useFont, Text3D } from '@react-three/drei'

// Preload font
useFont.preload('/fonts/helvetiker.json')

function Text() {
  return (
    <Text3D font="/fonts/helvetiker.json" size={1} height={0.2}>
      Hello
      <meshStandardMaterial color="gold" />
    </Text3D>
  )
}
```

## Suspense Patterns

### Basic Suspense

```tsx
import { Suspense } from 'react'

function Scene() {
  return (
    <Canvas>
      <Suspense fallback={<Loader />}>
        <Model />
      </Suspense>
    </Canvas>
  )
}

function Loader() {
  return (
    <mesh>
      <boxGeometry />
      <meshBasicMaterial color="gray" wireframe />
    </mesh>
  )
}
```

### Loading Progress UI

```tsx
import { useProgress, Html } from '@react-three/drei'

function Loader() {
  const { active, progress, errors, item, loaded, total } = useProgress()

  return (
    <Html center>
      <div className="loader">
        <div className="progress-bar">
          <div style={{ width: `${progress}%` }} />
        </div>
        <p>{Math.round(progress)}% loaded</p>
        <p>Loading: {item}</p>
      </div>
    </Html>
  )
}

function App() {
  return (
    <Canvas>
      <Suspense fallback={<Loader />}>
        <Scene />
      </Suspense>
    </Canvas>
  )
}
```

### Drei Loader Component

```tsx
import { Loader } from '@react-three/drei'

function App() {
  return (
    <>
      <Canvas>
        <Suspense fallback={null}>
          <Scene />
        </Suspense>
      </Canvas>
      {/* HTML loading overlay */}
      <Loader />
    </>
  )
}
```

## Other Model Formats

### OBJ + MTL

```tsx
import { useLoader } from '@react-three/fiber'
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader'
import { MTLLoader } from 'three/examples/jsm/loaders/MTLLoader'

function OBJModel() {
  const materials = useLoader(MTLLoader, '/model.mtl')
  const obj = useLoader(OBJLoader, '/model.obj', (loader) => {
    materials.preload()
    loader.setMaterials(materials)
  })

  return <primitive object={obj} />
}
```

### FBX

```tsx
import { useFBX } from '@react-three/drei'

function FBXModel() {
  const fbx = useFBX('/model.fbx')

  return <primitive object={fbx} scale={0.01} />
}

// Preload
useFBX.preload('/model.fbx')
```

### STL

```tsx
import { useLoader } from '@react-three/fiber'
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader'

function STLModel() {
  const geometry = useLoader(STLLoader, '/model.stl')

  return (
    <mesh geometry={geometry}>
      <meshStandardMaterial color="gray" />
    </mesh>
  )
}
```

### PLY

```tsx
import { useLoader } from '@react-three/fiber'
import { PLYLoader } from 'three/examples/jsm/loaders/PLYLoader'

function PLYModel() {
  const geometry = useLoader(PLYLoader, '/model.ply')

  useEffect(() => {
    geometry.computeVertexNormals()
  }, [geometry])

  return (
    <mesh geometry={geometry}>
      <meshStandardMaterial vertexColors />
    </mesh>
  )
}
```

## Clone for Multiple Instances

```tsx
import { useGLTF, Clone } from '@react-three/drei'

function Trees() {
  const { scene } = useGLTF('/models/tree.glb')

  return (
    <>
      <Clone object={scene} position={[0, 0, 0]} />
      <Clone object={scene} position={[5, 0, 0]} />
      <Clone object={scene} position={[-5, 0, 0]} />
      <Clone object={scene} position={[0, 0, 5]} scale={1.5} />
    </>
  )
}
```

## Error Handling

```tsx
import { useGLTF } from '@react-three/drei'
import { ErrorBoundary } from 'react-error-boundary'

function ModelWithErrorHandling() {
  return (
    <ErrorBoundary fallback={<FallbackModel />}>
      <Suspense fallback={<Loader />}>
        <Model />
      </Suspense>
    </ErrorBoundary>
  )
}

function FallbackModel() {
  return (
    <mesh>
      <boxGeometry />
      <meshBasicMaterial color="red" wireframe />
    </mesh>
  )
}
```

## Asset Caching

```tsx
import { useGLTF, useTexture } from '@react-three/drei'

// Assets are automatically cached by URL
// Same URL = same asset instance

function Scene() {
  // These all reference the same cached asset
  const model1 = useGLTF('/model.glb')
  const model2 = useGLTF('/model.glb')
  const model3 = useGLTF('/model.glb')

  // Clear cache if needed
  useGLTF.clear('/model.glb')
}
```

## Performance Tips

1. **Preload critical assets**: Avoid loading during interaction
2. **Use Draco compression**: Smaller file sizes
3. **Use LOD models**: Different detail levels for distance
4. **Clone instead of reload**: For multiple instances
5. **Lazy load non-critical**: Load on demand

```tsx
// Preload strategy
useGLTF.preload('/models/hero.glb')      // Critical
useTexture.preload('/textures/main.jpg')  // Critical

function LazyModel({ visible }) {
  // Only load when visible
  const { scene } = useGLTF(visible ? '/models/detail.glb' : null)
  return scene ? <primitive object={scene} /> : null
}
```

## See Also

- `r3f-animation` - Playing loaded animations
- `r3f-textures` - Texture configuration
- `r3f-materials` - Materials from loaded models
