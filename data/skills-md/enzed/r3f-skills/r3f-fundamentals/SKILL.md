---
name: r3f-fundamentals
description: React Three Fiber fundamentals - Canvas, hooks (useFrame, useThree), JSX elements, events, refs. Use when setting up R3F scenes, creating components, handling the render loop, or working with Three.js objects in React.
---

# React Three Fiber Fundamentals

## Quick Start

```tsx
import { Canvas } from '@react-three/fiber'
import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'

function RotatingBox() {
  const meshRef = useRef()

  useFrame((state, delta) => {
    meshRef.current.rotation.x += delta
    meshRef.current.rotation.y += delta * 0.5
  })

  return (
    <mesh ref={meshRef}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="hotpink" />
    </mesh>
  )
}

export default function App() {
  return (
    <Canvas camera={{ position: [0, 0, 5], fov: 75 }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[5, 5, 5]} />
      <RotatingBox />
    </Canvas>
  )
}
```

## Canvas Component

The root component that creates the WebGL context, scene, camera, and renderer.

```tsx
import { Canvas } from '@react-three/fiber'

function App() {
  return (
    <Canvas
      // Camera configuration
      camera={{
        position: [0, 5, 10],
        fov: 75,
        near: 0.1,
        far: 1000,
      }}
      // Or use orthographic
      orthographic
      camera={{ zoom: 50, position: [0, 0, 100] }}

      // Renderer settings
      gl={{
        antialias: true,
        alpha: true,
        powerPreference: 'high-performance',
        preserveDrawingBuffer: true,  // For screenshots
      }}
      dpr={[1, 2]}  // Pixel ratio min/max

      // Shadows
      shadows  // or shadows="soft" | "basic" | "percentage"

      // Color management
      flat  // Disable automatic sRGB color management

      // Frame loop control
      frameloop="demand"  // 'always' | 'demand' | 'never'

      // Event handling
      eventSource={document.getElementById('root')}
      eventPrefix="client"  // 'offset' | 'client' | 'page' | 'layer' | 'screen'

      // Callbacks
      onCreated={(state) => {
        console.log('Canvas ready:', state.gl, state.scene, state.camera)
      }}
      onPointerMissed={() => console.log('Clicked background')}

      // Styling
      style={{ width: '100%', height: '100vh' }}
    >
      <Scene />
    </Canvas>
  )
}
```

### Canvas Defaults

R3F sets sensible defaults:
- Renderer: antialias, alpha, outputColorSpace = SRGBColorSpace
- Camera: PerspectiveCamera at [0, 0, 5]
- Scene: Automatic resize handling
- Events: Pointer events enabled

## useFrame Hook

Subscribe to the render loop. Called every frame (typically 60fps).

```tsx
import { useFrame } from '@react-three/fiber'
import { useRef } from 'react'

function AnimatedMesh() {
  const meshRef = useRef()

  useFrame((state, delta, xrFrame) => {
    // state: Full R3F state (see useThree)
    // delta: Time since last frame in seconds
    // xrFrame: XR frame if in VR/AR mode

    // Animate rotation
    meshRef.current.rotation.y += delta

    // Access clock
    const elapsed = state.clock.elapsedTime
    meshRef.current.position.y = Math.sin(elapsed) * 2

    // Access pointer position (-1 to 1)
    const { x, y } = state.pointer
    meshRef.current.rotation.x = y * 0.5
    meshRef.current.rotation.z = x * 0.5
  })

  return (
    <mesh ref={meshRef}>
      <boxGeometry />
      <meshStandardMaterial color="orange" />
    </mesh>
  )
}
```

### useFrame with Priority

Control render order with priority (higher = later).

```tsx
// Default priority is 0
useFrame((state, delta) => {
  // Runs first
}, -1)

useFrame((state, delta) => {
  // Runs after priority -1
}, 0)

// Manual rendering with positive priority
useFrame((state, delta) => {
  // Take over rendering
  state.gl.render(state.scene, state.camera)
}, 1)
```

### Conditional useFrame

```tsx
function ConditionalAnimation({ active }) {
  useFrame((state, delta) => {
    if (!active) return  // Skip when inactive
    meshRef.current.rotation.y += delta
  })
}
```

## useThree Hook

Access the R3F state store.

```tsx
import { useThree } from '@react-three/fiber'

function CameraInfo() {
  // Get full state (triggers re-render on any change)
  const state = useThree()

  // Selective subscription (recommended)
  const camera = useThree((state) => state.camera)
  const gl = useThree((state) => state.gl)
  const scene = useThree((state) => state.scene)
  const size = useThree((state) => state.size)

  // Available state properties:
  // gl: WebGLRenderer
  // scene: Scene
  // camera: Camera
  // raycaster: Raycaster
  // pointer: Vector2 (normalized -1 to 1)
  // mouse: Vector2 (deprecated, use pointer)
  // clock: Clock
  // size: { width, height, top, left }
  // viewport: { width, height, factor, distance, aspect }
  // performance: { current, min, max, debounce, regress }
  // events: Event handlers
  // set: State setter
  // get: State getter
  // invalidate: Trigger re-render (for frameloop="demand")
  // advance: Advance one frame (for frameloop="never")

  return null
}
```

### Common useThree Patterns

```tsx
// Responsive to viewport
function ResponsiveObject() {
  const viewport = useThree((state) => state.viewport)
  return (
    <mesh scale={[viewport.width / 4, viewport.height / 4, 1]}>
      <planeGeometry />
      <meshBasicMaterial color="blue" />
    </mesh>
  )
}

// Manual render trigger
function TriggerRender() {
  const invalidate = useThree((state) => state.invalidate)

  const handleClick = () => {
    // Trigger render when using frameloop="demand"
    invalidate()
  }
}

// Update camera
function CameraController() {
  const camera = useThree((state) => state.camera)
  const set = useThree((state) => state.set)

  useEffect(() => {
    camera.position.set(10, 10, 10)
    camera.lookAt(0, 0, 0)
  }, [camera])
}
```

## JSX Elements

All Three.js objects are available as JSX elements (camelCase).

### Meshes

```tsx
// Basic mesh structure
<mesh
  position={[0, 0, 0]}       // x, y, z
  rotation={[0, Math.PI, 0]} // Euler angles in radians
  scale={[1, 2, 1]}          // x, y, z or single number
  visible={true}
  castShadow
  receiveShadow
>
  <boxGeometry args={[1, 1, 1]} />
  <meshStandardMaterial color="red" />
</mesh>

// With ref
const meshRef = useRef()
<mesh ref={meshRef} />
// meshRef.current is the THREE.Mesh
```

### Geometry args

Constructor arguments via `args` prop:

```tsx
// BoxGeometry(width, height, depth, widthSegments, heightSegments, depthSegments)
<boxGeometry args={[1, 1, 1, 1, 1, 1]} />

// SphereGeometry(radius, widthSegments, heightSegments)
<sphereGeometry args={[1, 32, 32]} />

// PlaneGeometry(width, height, widthSegments, heightSegments)
<planeGeometry args={[10, 10]} />

// CylinderGeometry(radiusTop, radiusBottom, height, radialSegments)
<cylinderGeometry args={[1, 1, 2, 32]} />
```

### Groups

```tsx
<group position={[5, 0, 0]} rotation={[0, Math.PI / 4, 0]}>
  <mesh position={[-1, 0, 0]}>
    <boxGeometry />
    <meshStandardMaterial color="red" />
  </mesh>
  <mesh position={[1, 0, 0]}>
    <boxGeometry />
    <meshStandardMaterial color="blue" />
  </mesh>
</group>
```

### Nested Properties

Use dashes for nested properties:

```tsx
<mesh
  position-x={5}
  rotation-y={Math.PI}
  scale-z={2}
>
  <meshStandardMaterial
    color="red"
    metalness={0.8}
    roughness={0.2}
  />
</mesh>

// Shadow camera properties
<directionalLight
  castShadow
  shadow-mapSize={[2048, 2048]}
  shadow-camera-left={-10}
  shadow-camera-right={10}
  shadow-camera-top={10}
  shadow-camera-bottom={-10}
/>
```

### attach Prop

Control how children attach to parents:

```tsx
<mesh>
  <boxGeometry />
  {/* Default: attaches as 'material' */}
  <meshStandardMaterial />
</mesh>

{/* Explicit attach */}
<mesh>
  <boxGeometry attach="geometry" />
  <meshStandardMaterial attach="material" />
</mesh>

{/* Array attachment */}
<mesh>
  <boxGeometry />
  <meshStandardMaterial attach="material-0" color="red" />
  <meshStandardMaterial attach="material-1" color="blue" />
</mesh>

{/* Custom attachment with function */}
<someObject>
  <texture
    attach={(parent, self) => {
      parent.map = self
      return () => { parent.map = null }  // Cleanup
    }}
  />
</someObject>
```

## Event Handling

R3F provides React-style events on 3D objects.

```tsx
function InteractiveBox() {
  const [hovered, setHovered] = useState(false)
  const [clicked, setClicked] = useState(false)

  return (
    <mesh
      onClick={(e) => {
        e.stopPropagation()  // Prevent bubbling
        setClicked(!clicked)

        // Event properties:
        console.log(e.object)      // THREE.Mesh
        console.log(e.point)       // Vector3 - intersection point
        console.log(e.distance)    // Distance from camera
        console.log(e.face)        // Intersected face
        console.log(e.faceIndex)   // Face index
        console.log(e.uv)          // UV coordinates
        console.log(e.normal)      // Face normal
        console.log(e.pointer)     // Normalized pointer coords
        console.log(e.ray)         // Raycaster ray
        console.log(e.camera)      // Camera
        console.log(e.delta)       // Distance moved (drag events)
      }}
      onContextMenu={(e) => console.log('Right click')}
      onDoubleClick={(e) => console.log('Double click')}
      onPointerOver={(e) => {
        e.stopPropagation()
        setHovered(true)
        document.body.style.cursor = 'pointer'
      }}
      onPointerOut={(e) => {
        setHovered(false)
        document.body.style.cursor = 'default'
      }}
      onPointerDown={(e) => console.log('Pointer down')}
      onPointerUp={(e) => console.log('Pointer up')}
      onPointerMove={(e) => console.log('Moving over mesh')}
      onWheel={(e) => console.log('Wheel:', e.deltaY)}
      scale={hovered ? 1.2 : 1}
    >
      <boxGeometry />
      <meshStandardMaterial color={clicked ? 'hotpink' : 'orange'} />
    </mesh>
  )
}
```

### Event Propagation

Events bubble up through the scene graph:

```tsx
<group onClick={(e) => console.log('Group clicked')}>
  <mesh onClick={(e) => {
    e.stopPropagation()  // Stop bubbling to group
    console.log('Mesh clicked')
  }}>
    <boxGeometry />
    <meshStandardMaterial />
  </mesh>
</group>
```

## primitive Element

Use existing Three.js objects directly:

```tsx
import * as THREE from 'three'

// Existing object
const geometry = new THREE.BoxGeometry()
const material = new THREE.MeshStandardMaterial({ color: 'red' })
const mesh = new THREE.Mesh(geometry, material)

function Scene() {
  return <primitive object={mesh} position={[0, 1, 0]} />
}

// Common with loaded models
function Model({ gltf }) {
  return <primitive object={gltf.scene} />
}
```

## extend Function

Register custom Three.js classes for JSX use:

```tsx
import { extend } from '@react-three/fiber'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'

// Extend once (usually at module level)
extend({ OrbitControls })

// Now use as JSX
function Scene() {
  const { camera, gl } = useThree()
  return <orbitControls args={[camera, gl.domElement]} />
}

// TypeScript declaration
declare global {
  namespace JSX {
    interface IntrinsicElements {
      orbitControls: ReactThreeFiber.Object3DNode<OrbitControls, typeof OrbitControls>
    }
  }
}
```

## Refs and Imperative Access

```tsx
import { useRef, useEffect } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

function MeshWithRef() {
  const meshRef = useRef<THREE.Mesh>(null)
  const materialRef = useRef<THREE.MeshStandardMaterial>(null)

  useEffect(() => {
    if (meshRef.current) {
      // Direct Three.js access
      meshRef.current.geometry.computeBoundingBox()
      console.log(meshRef.current.geometry.boundingBox)
    }
  }, [])

  useFrame(() => {
    if (materialRef.current) {
      materialRef.current.color.setHSL(Math.random(), 1, 0.5)
    }
  })

  return (
    <mesh ref={meshRef}>
      <boxGeometry />
      <meshStandardMaterial ref={materialRef} />
    </mesh>
  )
}
```

## Performance Patterns

### Avoiding Re-renders

```tsx
// BAD: Creates new object every render
<mesh position={[x, y, z]} />

// GOOD: Mutate existing position
const meshRef = useRef()
useFrame(() => {
  meshRef.current.position.x = x
})
<mesh ref={meshRef} />

// GOOD: Use useMemo for static values
const position = useMemo(() => [x, y, z], [x, y, z])
<mesh position={position} />
```

### Component Isolation

```tsx
// Isolate animated components to prevent parent re-renders
function Scene() {
  return (
    <>
      <StaticEnvironment />
      <AnimatedObject />  {/* Only this re-renders on animation */}
    </>
  )
}

function AnimatedObject() {
  const ref = useRef()
  useFrame((_, delta) => {
    ref.current.rotation.y += delta
  })
  return <mesh ref={ref}><boxGeometry /></mesh>
}
```

### Dispose

R3F auto-disposes geometries, materials, and textures. Override with:

```tsx
<mesh dispose={null}>  {/* Prevent auto-dispose */}
  <boxGeometry />
  <meshStandardMaterial />
</mesh>
```

## Common Patterns

### Fullscreen Canvas

```tsx
// styles.css
html, body, #root {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}

// App.tsx
<Canvas style={{ width: '100%', height: '100%' }}>
```

### Responsive Canvas

```tsx
function ResponsiveScene() {
  const { viewport } = useThree()

  return (
    <mesh scale={Math.min(viewport.width, viewport.height) / 5}>
      <boxGeometry />
      <meshStandardMaterial />
    </mesh>
  )
}
```

### Forwarding Refs

```tsx
import { forwardRef } from 'react'

const CustomMesh = forwardRef((props, ref) => {
  return (
    <mesh ref={ref} {...props}>
      <boxGeometry />
      <meshStandardMaterial color="orange" />
    </mesh>
  )
})

// Usage
const meshRef = useRef()
<CustomMesh ref={meshRef} position={[0, 1, 0]} />
```

## Debugging with Leva

Leva provides a GUI for tweaking parameters in real-time during development.

### Installation

```bash
npm install leva
```

### Basic Controls

```tsx
import { useControls } from 'leva'

function DebugMesh() {
  const { position, color, scale, visible } = useControls({
    position: { value: [0, 0, 0], step: 0.1 },
    color: '#ff0000',
    scale: { value: 1, min: 0.1, max: 5, step: 0.1 },
    visible: true,
  })

  return (
    <mesh position={position} scale={scale} visible={visible}>
      <boxGeometry />
      <meshStandardMaterial color={color} />
    </mesh>
  )
}
```

### Organized Folders

```tsx
import { useControls, folder } from 'leva'

function DebugScene() {
  const { lightIntensity, lightColor, shadowMapSize } = useControls({
    Lighting: folder({
      lightIntensity: { value: 1, min: 0, max: 5 },
      lightColor: '#ffffff',
      shadowMapSize: { value: 1024, options: [512, 1024, 2048, 4096] },
    }),
    Camera: folder({
      fov: { value: 75, min: 30, max: 120 },
      near: { value: 0.1, min: 0.01, max: 1 },
    }),
  })

  return (
    <directionalLight
      intensity={lightIntensity}
      color={lightColor}
      shadow-mapSize={[shadowMapSize, shadowMapSize]}
    />
  )
}
```

### Button Actions

```tsx
import { useControls, button } from 'leva'

function DebugActions() {
  const meshRef = useRef()

  useControls({
    'Reset Position': button(() => {
      meshRef.current.position.set(0, 0, 0)
    }),
    'Random Color': button(() => {
      meshRef.current.material.color.setHex(Math.random() * 0xffffff)
    }),
    'Log State': button(() => {
      console.log(meshRef.current.position)
    }),
  })

  return <mesh ref={meshRef}>...</mesh>
}
```

### Hide in Production

```tsx
import { Leva } from 'leva'

function App() {
  return (
    <>
      {/* Hide Leva panel in production */}
      <Leva hidden={process.env.NODE_ENV === 'production'} />

      <Canvas>
        <Scene />
      </Canvas>
    </>
  )
}
```

### Monitor Values (Read-Only)

```tsx
import { useControls, monitor } from 'leva'
import { useFrame } from '@react-three/fiber'

function PerformanceMonitor() {
  const [fps, setFps] = useState(0)

  useControls({
    FPS: monitor(() => fps, { graph: true, interval: 100 }),
  })

  useFrame((state) => {
    // Update FPS display
    setFps(Math.round(1 / state.clock.getDelta()))
  })

  return null
}
```

### Integration with useFrame

```tsx
function AnimatedDebugMesh() {
  const meshRef = useRef()

  const { speed, amplitude, enabled } = useControls('Animation', {
    enabled: true,
    speed: { value: 1, min: 0, max: 5 },
    amplitude: { value: 1, min: 0, max: 3 },
  })

  useFrame(({ clock }) => {
    if (!enabled) return
    meshRef.current.position.y = Math.sin(clock.elapsedTime * speed) * amplitude
  })

  return (
    <mesh ref={meshRef}>
      <sphereGeometry />
      <meshStandardMaterial color="cyan" />
    </mesh>
  )
}
```

## See Also

- `r3f-geometry` - Geometry creation
- `r3f-materials` - Material configuration
- `r3f-lighting` - Lights and shadows
- `r3f-interaction` - Controls and user input
