---
name: r3f-interaction
description: React Three Fiber interaction - pointer events, controls, gestures, selection. Use when handling user input, implementing click detection, adding camera controls, or creating interactive 3D experiences.
---

# React Three Fiber Interaction

## Quick Start

```tsx
import { Canvas } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'

function InteractiveMesh() {
  return (
    <mesh
      onClick={(e) => console.log('Clicked!', e.point)}
      onPointerOver={(e) => console.log('Hover')}
      onPointerOut={(e) => console.log('Unhover')}
    >
      <boxGeometry />
      <meshStandardMaterial color="hotpink" />
    </mesh>
  )
}

export default function App() {
  return (
    <Canvas>
      <ambientLight />
      <InteractiveMesh />
      <OrbitControls />
    </Canvas>
  )
}
```

## Pointer Events

R3F provides built-in pointer events on mesh elements.

### Available Events

```tsx
<mesh
  // Click events
  onClick={(e) => {}}           // Click (pointerdown + pointerup on same object)
  onDoubleClick={(e) => {}}     // Double click
  onContextMenu={(e) => {}}     // Right click

  // Pointer events
  onPointerDown={(e) => {}}     // Pointer pressed
  onPointerUp={(e) => {}}       // Pointer released
  onPointerMove={(e) => {}}     // Pointer moved while over object
  onPointerOver={(e) => {}}     // Pointer enters object
  onPointerOut={(e) => {}}      // Pointer leaves object
  onPointerEnter={(e) => {}}    // Pointer enters object (no bubbling)
  onPointerLeave={(e) => {}}    // Pointer leaves object (no bubbling)
  onPointerMissed={(e) => {}}   // Click that missed all objects

  // Wheel
  onWheel={(e) => {}}           // Mouse wheel

  // Touch
  onPointerCancel={(e) => {}}   // Touch cancelled
>
  <boxGeometry />
  <meshStandardMaterial />
</mesh>
```

### Event Object

```tsx
function InteractiveMesh() {
  const handleClick = (event) => {
    // Stop propagation to parent objects
    event.stopPropagation()

    // Event properties
    console.log({
      object: event.object,           // The mesh that was clicked
      point: event.point,             // World coordinates of intersection
      distance: event.distance,       // Distance from camera
      face: event.face,               // Intersected face
      faceIndex: event.faceIndex,     // Face index
      uv: event.uv,                   // UV coordinates at intersection
      normal: event.normal,           // Face normal
      camera: event.camera,           // Current camera
      ray: event.ray,                 // Ray used for intersection
      intersections: event.intersections, // All intersections
      nativeEvent: event.nativeEvent, // Original DOM event
      delta: event.delta,             // Click distance (useful for drag detection)
    })
  }

  return (
    <mesh onClick={handleClick}>
      <boxGeometry />
      <meshStandardMaterial />
    </mesh>
  )
}
```

### Hover Effects

```tsx
import { useState } from 'react'

function HoverableMesh() {
  const [hovered, setHovered] = useState(false)

  return (
    <mesh
      onPointerOver={(e) => {
        e.stopPropagation()
        setHovered(true)
        document.body.style.cursor = 'pointer'
      }}
      onPointerOut={(e) => {
        setHovered(false)
        document.body.style.cursor = 'default'
      }}
      scale={hovered ? 1.2 : 1}
    >
      <boxGeometry />
      <meshStandardMaterial color={hovered ? 'hotpink' : 'orange'} />
    </mesh>
  )
}
```

### Selective Raycasting

```tsx
// Disable raycasting for specific objects
<mesh raycast={() => null}>
  <boxGeometry />
  <meshStandardMaterial />
</mesh>

// Or use layers
<mesh
  layers={1}  // Only raycast against layer 1
  onClick={() => console.log('clicked')}
>
  <boxGeometry />
  <meshStandardMaterial />
</mesh>
```

## Camera Controls

### OrbitControls

```tsx
import { OrbitControls } from '@react-three/drei'

function Scene() {
  return (
    <>
      <mesh>
        <boxGeometry />
        <meshStandardMaterial />
      </mesh>

      <OrbitControls
        makeDefault                    // Use as default controls
        enableDamping                  // Smooth movement
        dampingFactor={0.05}
        enableZoom={true}
        enablePan={true}
        enableRotate={true}
        autoRotate={false}
        autoRotateSpeed={2}
        minDistance={2}
        maxDistance={50}
        minPolarAngle={0}              // Top limit
        maxPolarAngle={Math.PI / 2}    // Horizon limit
        minAzimuthAngle={-Math.PI / 4} // Left limit
        maxAzimuthAngle={Math.PI / 4}  // Right limit
        target={[0, 1, 0]}             // Look-at point
      />
    </>
  )
}
```

### OrbitControls with Ref

```tsx
import { OrbitControls } from '@react-three/drei'
import { useRef, useEffect } from 'react'

function Scene() {
  const controlsRef = useRef()

  useEffect(() => {
    // Access controls methods
    if (controlsRef.current) {
      controlsRef.current.reset()
      controlsRef.current.target.set(0, 1, 0)
      controlsRef.current.update()
    }
  }, [])

  return <OrbitControls ref={controlsRef} />
}
```

### MapControls

Top-down map-style controls.

```tsx
import { MapControls } from '@react-three/drei'

<MapControls
  enableDamping
  dampingFactor={0.05}
  screenSpacePanning={false}  // Pan in world space
  maxPolarAngle={Math.PI / 2}
/>
```

### FlyControls

Free-flying camera controls.

```tsx
import { FlyControls } from '@react-three/drei'

<FlyControls
  movementSpeed={10}
  rollSpeed={Math.PI / 24}
  dragToLook
/>
```

### FirstPersonControls

FPS-style controls.

```tsx
import { FirstPersonControls } from '@react-three/drei'

<FirstPersonControls
  movementSpeed={10}
  lookSpeed={0.1}
  lookVertical
/>
```

### PointerLockControls

Lock pointer for FPS games.

```tsx
import { PointerLockControls } from '@react-three/drei'
import { useRef } from 'react'

function Scene() {
  const controlsRef = useRef()

  return (
    <>
      <PointerLockControls ref={controlsRef} />

      {/* Click to lock pointer */}
      <mesh onClick={() => controlsRef.current?.lock()}>
        <planeGeometry args={[10, 10]} />
        <meshBasicMaterial color="green" />
      </mesh>
    </>
  )
}
```

### CameraControls

Advanced camera controls with smooth transitions.

```tsx
import { CameraControls } from '@react-three/drei'
import { useRef } from 'react'

function Scene() {
  const controlsRef = useRef()

  const focusOnObject = async () => {
    // Smooth transition to target
    await controlsRef.current?.setLookAt(
      5, 3, 5,    // Camera position
      0, 0, 0,    // Look-at target
      true        // Enable transition
    )
  }

  return (
    <>
      <CameraControls ref={controlsRef} />

      <mesh onClick={focusOnObject}>
        <boxGeometry />
        <meshStandardMaterial color="red" />
      </mesh>
    </>
  )
}
```

### TrackballControls

Unconstrained rotation controls.

```tsx
import { TrackballControls } from '@react-three/drei'

<TrackballControls
  rotateSpeed={2.0}
  zoomSpeed={1.2}
  panSpeed={0.8}
  staticMoving={true}
/>
```

### ArcballControls

Arc-based rotation controls.

```tsx
import { ArcballControls } from '@react-three/drei'

<ArcballControls
  enableAnimations
  dampingFactor={25}
/>
```

## Transform Controls

Gizmo for moving/rotating/scaling objects.

```tsx
import { TransformControls, OrbitControls } from '@react-three/drei'
import { useRef, useState } from 'react'

function Scene() {
  const meshRef = useRef()
  const [mode, setMode] = useState('translate')
  const orbitRef = useRef()

  return (
    <>
      <OrbitControls ref={orbitRef} makeDefault />

      <TransformControls
        object={meshRef}
        mode={mode}  // 'translate' | 'rotate' | 'scale'
        space="local"  // 'local' | 'world'
        onMouseDown={() => {
          // Disable orbit while transforming
          if (orbitRef.current) orbitRef.current.enabled = false
        }}
        onMouseUp={() => {
          if (orbitRef.current) orbitRef.current.enabled = true
        }}
      />

      <mesh ref={meshRef}>
        <boxGeometry />
        <meshStandardMaterial color="orange" />
      </mesh>

      {/* Mode switching buttons in HTML */}
      <div className="controls">
        <button onClick={() => setMode('translate')}>Move</button>
        <button onClick={() => setMode('rotate')}>Rotate</button>
        <button onClick={() => setMode('scale')}>Scale</button>
      </div>
    </>
  )
}
```

### PivotControls

Alternative transform gizmo with pivot point.

```tsx
import { PivotControls } from '@react-three/drei'

function Scene() {
  return (
    <PivotControls
      anchor={[0, 0, 0]}         // Anchor point
      depthTest={false}          // Always visible
      lineWidth={2}              // Axis line width
      axisColors={['red', 'green', 'blue']}
      scale={1}                  // Gizmo scale
      fixed={false}              // Fixed screen size
    >
      <mesh>
        <boxGeometry />
        <meshStandardMaterial color="orange" />
      </mesh>
    </PivotControls>
  )
}
```

## Drag Controls

### useDrag from @use-gesture/react

```bash
npm install @use-gesture/react
```

```tsx
import { useDrag } from '@use-gesture/react'
import { useSpring, animated } from '@react-spring/three'
import { useThree } from '@react-three/fiber'

function DraggableMesh() {
  const { size, viewport } = useThree()
  const aspect = size.width / viewport.width

  const [spring, api] = useSpring(() => ({
    position: [0, 0, 0],
    config: { mass: 1, tension: 280, friction: 60 }
  }))

  const bind = useDrag(({ movement: [mx, my], down }) => {
    api.start({
      position: down ? [mx / aspect, -my / aspect, 0] : [0, 0, 0]
    })
  })

  return (
    <animated.mesh {...bind()} position={spring.position}>
      <boxGeometry />
      <meshStandardMaterial color="hotpink" />
    </animated.mesh>
  )
}
```

### DragControls (Drei)

```tsx
import { DragControls, OrbitControls } from '@react-three/drei'
import { useRef } from 'react'

function Scene() {
  const meshRef = useRef()
  const orbitRef = useRef()

  return (
    <>
      <OrbitControls ref={orbitRef} makeDefault />

      <DragControls
        onDragStart={() => {
          if (orbitRef.current) orbitRef.current.enabled = false
        }}
        onDragEnd={() => {
          if (orbitRef.current) orbitRef.current.enabled = true
        }}
      >
        <mesh ref={meshRef}>
          <boxGeometry />
          <meshStandardMaterial color="orange" />
        </mesh>
      </DragControls>
    </>
  )
}
```

## Keyboard Controls

### KeyboardControls (Drei)

```tsx
import { KeyboardControls, useKeyboardControls } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'
import { useRef } from 'react'

// Define key mappings
const keyMap = [
  { name: 'forward', keys: ['ArrowUp', 'KeyW'] },
  { name: 'backward', keys: ['ArrowDown', 'KeyS'] },
  { name: 'left', keys: ['ArrowLeft', 'KeyA'] },
  { name: 'right', keys: ['ArrowRight', 'KeyD'] },
  { name: 'jump', keys: ['Space'] },
  { name: 'sprint', keys: ['ShiftLeft'] },
]

function Player() {
  const meshRef = useRef()
  const [, getKeys] = useKeyboardControls()

  useFrame((state, delta) => {
    const { forward, backward, left, right, jump, sprint } = getKeys()

    const speed = sprint ? 10 : 5

    if (forward) meshRef.current.position.z -= speed * delta
    if (backward) meshRef.current.position.z += speed * delta
    if (left) meshRef.current.position.x -= speed * delta
    if (right) meshRef.current.position.x += speed * delta
    if (jump) meshRef.current.position.y += speed * delta
  })

  return (
    <mesh ref={meshRef}>
      <boxGeometry />
      <meshStandardMaterial color="blue" />
    </mesh>
  )
}

export default function App() {
  return (
    <KeyboardControls map={keyMap}>
      <Canvas>
        <ambientLight />
        <Player />
      </Canvas>
    </KeyboardControls>
  )
}
```

### Subscribe to Key Changes

```tsx
import { useKeyboardControls } from '@react-three/drei'
import { useEffect } from 'react'

function KeyListener() {
  const jumpPressed = useKeyboardControls((state) => state.jump)

  useEffect(() => {
    if (jumpPressed) {
      console.log('Jump!')
    }
  }, [jumpPressed])

  return null
}
```

## Selection System

### Click to Select

```tsx
import { useState } from 'react'

function SelectableScene() {
  const [selected, setSelected] = useState(null)

  return (
    <>
      {[[-2, 0, 0], [0, 0, 0], [2, 0, 0]].map((position, i) => (
        <mesh
          key={i}
          position={position}
          onClick={(e) => {
            e.stopPropagation()
            setSelected(i)
          }}
        >
          <boxGeometry />
          <meshStandardMaterial
            color={selected === i ? 'hotpink' : 'orange'}
            emissive={selected === i ? 'hotpink' : 'black'}
            emissiveIntensity={0.3}
          />
        </mesh>
      ))}

      {/* Click on empty space to deselect */}
      <mesh
        position={[0, -1, 0]}
        rotation={[-Math.PI / 2, 0, 0]}
        onClick={() => setSelected(null)}
      >
        <planeGeometry args={[20, 20]} />
        <meshStandardMaterial color="gray" />
      </mesh>
    </>
  )
}
```

### Multi-Select with Outline

```tsx
import { useState } from 'react'
import { EffectComposer, Outline, Selection, Select } from '@react-three/postprocessing'

function MultiSelectScene() {
  const [selected, setSelected] = useState(new Set())

  const toggleSelect = (id, event) => {
    event.stopPropagation()
    setSelected((prev) => {
      const next = new Set(prev)
      if (event.shiftKey) {
        // Multi-select with shift
        if (next.has(id)) {
          next.delete(id)
        } else {
          next.add(id)
        }
      } else {
        // Single select
        next.clear()
        next.add(id)
      }
      return next
    })
  }

  return (
    <Selection>
      <EffectComposer autoClear={false}>
        <Outline
          blur
          visibleEdgeColor={0xffffff}
          edgeStrength={10}
        />
      </EffectComposer>

      {[0, 1, 2, 3, 4].map((id) => (
        <Select key={id} enabled={selected.has(id)}>
          <mesh
            position={[(id - 2) * 2, 0, 0]}
            onClick={(e) => toggleSelect(id, e)}
          >
            <boxGeometry />
            <meshStandardMaterial color="orange" />
          </mesh>
        </Select>
      ))}
    </Selection>
  )
}
```

## Screen-Space to World-Space

### Get World Position from Click

```tsx
import { useThree } from '@react-three/fiber'
import * as THREE from 'three'

function ClickToPlace() {
  const { camera, raycaster, pointer } = useThree()
  const planeRef = useRef()

  const handleClick = (event) => {
    // Create intersection plane
    const plane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0)
    const intersection = new THREE.Vector3()

    // Cast ray from pointer
    raycaster.setFromCamera(pointer, camera)
    raycaster.ray.intersectPlane(plane, intersection)

    console.log('World position:', intersection)
  }

  return (
    <mesh
      ref={planeRef}
      rotation={[-Math.PI / 2, 0, 0]}
      onClick={handleClick}
    >
      <planeGeometry args={[100, 100]} />
      <meshBasicMaterial visible={false} />
    </mesh>
  )
}
```

### World Position to Screen Position

```tsx
import { useThree, useFrame } from '@react-three/fiber'
import { Html } from '@react-three/drei'
import * as THREE from 'three'

function WorldToScreen({ target }) {
  const { camera, size } = useThree()

  const getScreenPosition = (worldPos) => {
    const vector = worldPos.clone()
    vector.project(camera)

    return {
      x: (vector.x * 0.5 + 0.5) * size.width,
      y: (1 - (vector.y * 0.5 + 0.5)) * size.height
    }
  }

  // Or use Html component which handles this automatically
  return (
    <Html position={target}>
      <div className="label">Label</div>
    </Html>
  )
}
```

## Gesture Recognition

### usePinch and useWheel

```tsx
import { usePinch, useWheel } from '@use-gesture/react'
import { useSpring, animated } from '@react-spring/three'

function ZoomableMesh() {
  const [spring, api] = useSpring(() => ({
    scale: 1,
    config: { mass: 1, tension: 200, friction: 30 }
  }))

  usePinch(
    ({ offset: [s] }) => {
      api.start({ scale: s })
    },
    { target: window }
  )

  useWheel(
    ({ delta: [, dy] }) => {
      api.start({ scale: spring.scale.get() - dy * 0.001 })
    },
    { target: window }
  )

  return (
    <animated.mesh scale={spring.scale}>
      <boxGeometry />
      <meshStandardMaterial color="cyan" />
    </animated.mesh>
  )
}
```

## Scroll Controls

```tsx
import { Canvas } from '@react-three/fiber'
import { ScrollControls, Scroll, useScroll } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'
import { useRef } from 'react'

function AnimatedOnScroll() {
  const meshRef = useRef()
  const scroll = useScroll()

  useFrame(() => {
    const offset = scroll.offset // 0 to 1
    meshRef.current.rotation.y = offset * Math.PI * 2
    meshRef.current.position.y = offset * 5
  })

  return (
    <mesh ref={meshRef}>
      <boxGeometry />
      <meshStandardMaterial color="orange" />
    </mesh>
  )
}

export default function App() {
  return (
    <Canvas>
      <ScrollControls pages={3} damping={0.25}>
        <Scroll>
          <AnimatedOnScroll />
        </Scroll>

        {/* HTML content that scrolls */}
        <Scroll html>
          <h1 style={{ position: 'absolute', top: '10vh' }}>Page 1</h1>
          <h1 style={{ position: 'absolute', top: '110vh' }}>Page 2</h1>
          <h1 style={{ position: 'absolute', top: '210vh' }}>Page 3</h1>
        </Scroll>
      </ScrollControls>
    </Canvas>
  )
}
```

## Presentation Controls

For product showcases with limited rotation.

```tsx
import { PresentationControls } from '@react-three/drei'

function ProductShowcase() {
  return (
    <PresentationControls
      global                 // Apply to whole scene
      snap                   // Snap back when released
      speed={1}              // Rotation speed
      zoom={1}               // Zoom speed
      rotation={[0, 0, 0]}   // Initial rotation
      polar={[-Math.PI / 4, Math.PI / 4]}    // Vertical limits
      azimuth={[-Math.PI / 4, Math.PI / 4]}  // Horizontal limits
      config={{ mass: 1, tension: 170, friction: 26 }}
    >
      <mesh>
        <boxGeometry />
        <meshStandardMaterial color="gold" />
      </mesh>
    </PresentationControls>
  )
}
```

## Performance Tips

1. **Stop propagation**: Prevent unnecessary raycasts
2. **Use layers**: Filter raycast targets
3. **Simpler collision meshes**: Use invisible simple geometry
4. **Throttle events**: Limit onPointerMove frequency
5. **Disable controls when not needed**: `enabled={false}`

```tsx
// Use simpler geometry for raycasting
function OptimizedInteraction() {
  return (
    <group>
      {/* Complex visible mesh */}
      <mesh raycast={() => null}>
        <torusKnotGeometry args={[1, 0.4, 100, 16]} />
        <meshStandardMaterial color="purple" />
      </mesh>

      {/* Simple invisible collision mesh */}
      <mesh onClick={() => console.log('clicked')}>
        <sphereGeometry args={[1.5]} />
        <meshBasicMaterial visible={false} />
      </mesh>
    </group>
  )
}

// Throttle pointer move events
import { useMemo, useCallback } from 'react'
import throttle from 'lodash/throttle'

function ThrottledHover() {
  const handleMove = useMemo(
    () => throttle((e) => {
      console.log('Move', e.point)
    }, 100),
    []
  )

  return (
    <mesh onPointerMove={handleMove}>
      <boxGeometry />
      <meshStandardMaterial />
    </mesh>
  )
}
```

## See Also

- `r3f-fundamentals` - Canvas and scene setup
- `r3f-animation` - Animating interactions
- `r3f-postprocessing` - Visual feedback effects (outline, selection)
