---
name: r3f-geometry
description: React Three Fiber geometry - built-in shapes, BufferGeometry, instancing with Drei. Use when creating 3D shapes, custom meshes, point clouds, lines, or optimizing with instanced rendering.
---

# React Three Fiber Geometry

## Quick Start

```tsx
import { Canvas } from '@react-three/fiber'

function Scene() {
  return (
    <Canvas>
      <ambientLight />
      <mesh position={[0, 0, 0]}>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial color="hotpink" />
      </mesh>
    </Canvas>
  )
}
```

## Built-in Geometries

All Three.js geometries are available as JSX elements. The `args` prop passes constructor arguments.

### Basic Shapes

```tsx
// BoxGeometry(width, height, depth, widthSegments, heightSegments, depthSegments)
<boxGeometry args={[1, 1, 1]} />
<boxGeometry args={[2, 1, 0.5, 2, 2, 2]} />

// SphereGeometry(radius, widthSegments, heightSegments, phiStart, phiLength, thetaStart, thetaLength)
<sphereGeometry args={[1, 32, 32]} />
<sphereGeometry args={[1, 64, 64]} />  // High quality
<sphereGeometry args={[1, 32, 32, 0, Math.PI]} />  // Hemisphere

// PlaneGeometry(width, height, widthSegments, heightSegments)
<planeGeometry args={[10, 10]} />
<planeGeometry args={[10, 10, 32, 32]} />  // Subdivided for displacement

// CircleGeometry(radius, segments, thetaStart, thetaLength)
<circleGeometry args={[1, 32]} />
<circleGeometry args={[1, 32, 0, Math.PI]} />  // Semicircle

// CylinderGeometry(radiusTop, radiusBottom, height, radialSegments, heightSegments, openEnded)
<cylinderGeometry args={[1, 1, 2, 32]} />
<cylinderGeometry args={[0, 1, 2, 32]} />  // Cone
<cylinderGeometry args={[1, 1, 2, 6]} />   // Hexagonal prism

// ConeGeometry(radius, height, radialSegments, heightSegments, openEnded)
<coneGeometry args={[1, 2, 32]} />

// TorusGeometry(radius, tube, radialSegments, tubularSegments, arc)
<torusGeometry args={[1, 0.4, 16, 100]} />

// TorusKnotGeometry(radius, tube, tubularSegments, radialSegments, p, q)
<torusKnotGeometry args={[1, 0.4, 100, 16, 2, 3]} />

// RingGeometry(innerRadius, outerRadius, thetaSegments, phiSegments)
<ringGeometry args={[0.5, 1, 32]} />
```

### Advanced Shapes

```tsx
// CapsuleGeometry(radius, length, capSegments, radialSegments)
<capsuleGeometry args={[0.5, 1, 4, 16]} />

// Polyhedrons
<dodecahedronGeometry args={[1, 0]} />  // radius, detail
<icosahedronGeometry args={[1, 0]} />
<octahedronGeometry args={[1, 0]} />
<tetrahedronGeometry args={[1, 0]} />

// Higher detail = more subdivisions
<icosahedronGeometry args={[1, 4]} />  // Approximates sphere
```

### Path-Based Shapes

```tsx
import * as THREE from 'three'

// LatheGeometry - revolve points around Y axis
function LatheShape() {
  const points = [
    new THREE.Vector2(0, 0),
    new THREE.Vector2(0.5, 0),
    new THREE.Vector2(0.5, 0.5),
    new THREE.Vector2(0.3, 1),
    new THREE.Vector2(0, 1),
  ]

  return (
    <mesh>
      <latheGeometry args={[points, 32]} />
      <meshStandardMaterial color="gold" side={THREE.DoubleSide} />
    </mesh>
  )
}

// TubeGeometry - extrude along a curve
function TubeShape() {
  const curve = new THREE.CatmullRomCurve3([
    new THREE.Vector3(-2, 0, 0),
    new THREE.Vector3(-1, 1, 0),
    new THREE.Vector3(1, -1, 0),
    new THREE.Vector3(2, 0, 0),
  ])

  return (
    <mesh>
      <tubeGeometry args={[curve, 64, 0.2, 8, false]} />
      <meshStandardMaterial color="blue" />
    </mesh>
  )
}

// ExtrudeGeometry - extrude a 2D shape
function ExtrudedShape() {
  const shape = new THREE.Shape()
  shape.moveTo(0, 0)
  shape.lineTo(1, 0)
  shape.lineTo(1, 1)
  shape.lineTo(0, 1)
  shape.lineTo(0, 0)

  const extrudeSettings = {
    steps: 2,
    depth: 0.5,
    bevelEnabled: true,
    bevelThickness: 0.1,
    bevelSize: 0.1,
    bevelSegments: 3,
  }

  return (
    <mesh>
      <extrudeGeometry args={[shape, extrudeSettings]} />
      <meshStandardMaterial color="purple" />
    </mesh>
  )
}
```

## Drei Shape Helpers

@react-three/drei provides convenient shape components.

```tsx
import {
  Box, Sphere, Plane, Circle, Cylinder, Cone,
  Torus, TorusKnot, Ring, Capsule, Dodecahedron,
  Icosahedron, Octahedron, Tetrahedron, RoundedBox
} from '@react-three/drei'

function DreiShapes() {
  return (
    <>
      {/* All shapes accept mesh props directly */}
      <Box args={[1, 1, 1]} position={[-3, 0, 0]}>
        <meshStandardMaterial color="red" />
      </Box>

      <Sphere args={[0.5, 32, 32]} position={[-1, 0, 0]}>
        <meshStandardMaterial color="blue" />
      </Sphere>

      <Cylinder args={[0.5, 0.5, 1, 32]} position={[1, 0, 0]}>
        <meshStandardMaterial color="green" />
      </Cylinder>

      {/* RoundedBox - box with rounded edges */}
      <RoundedBox
        args={[1, 1, 1]}      // width, height, depth
        radius={0.1}          // border radius
        smoothness={4}        // smoothness of rounded edges
        position={[3, 0, 0]}
      >
        <meshStandardMaterial color="orange" />
      </RoundedBox>
    </>
  )
}
```

## Custom BufferGeometry

### Basic Custom Geometry

```tsx
import { useMemo, useRef } from 'react'
import * as THREE from 'three'

function CustomTriangle() {
  const geometry = useMemo(() => {
    const geo = new THREE.BufferGeometry()

    // Vertices (3 floats per vertex: x, y, z)
    const vertices = new Float32Array([
      -1, -1, 0,  // vertex 0
       1, -1, 0,  // vertex 1
       0,  1, 0,  // vertex 2
    ])

    // Normals (pointing toward camera)
    const normals = new Float32Array([
      0, 0, 1,
      0, 0, 1,
      0, 0, 1,
    ])

    // UVs
    const uvs = new Float32Array([
      0, 0,
      1, 0,
      0.5, 1,
    ])

    geo.setAttribute('position', new THREE.BufferAttribute(vertices, 3))
    geo.setAttribute('normal', new THREE.BufferAttribute(normals, 3))
    geo.setAttribute('uv', new THREE.BufferAttribute(uvs, 2))

    return geo
  }, [])

  return (
    <mesh geometry={geometry}>
      <meshStandardMaterial color="cyan" side={THREE.DoubleSide} />
    </mesh>
  )
}
```

### Indexed Geometry

```tsx
function CustomQuad() {
  const geometry = useMemo(() => {
    const geo = new THREE.BufferGeometry()

    // 4 vertices for a quad
    const vertices = new Float32Array([
      -1, -1, 0,  // 0: bottom-left
       1, -1, 0,  // 1: bottom-right
       1,  1, 0,  // 2: top-right
      -1,  1, 0,  // 3: top-left
    ])

    // Indices to form 2 triangles
    const indices = new Uint16Array([
      0, 1, 2,  // triangle 1
      0, 2, 3,  // triangle 2
    ])

    const normals = new Float32Array([
      0, 0, 1,  0, 0, 1,  0, 0, 1,  0, 0, 1,
    ])

    const uvs = new Float32Array([
      0, 0,  1, 0,  1, 1,  0, 1,
    ])

    geo.setAttribute('position', new THREE.BufferAttribute(vertices, 3))
    geo.setAttribute('normal', new THREE.BufferAttribute(normals, 3))
    geo.setAttribute('uv', new THREE.BufferAttribute(uvs, 2))
    geo.setIndex(new THREE.BufferAttribute(indices, 1))

    return geo
  }, [])

  return (
    <mesh geometry={geometry}>
      <meshStandardMaterial color="lime" side={THREE.DoubleSide} />
    </mesh>
  )
}
```

### Dynamic Geometry

```tsx
import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'

function WavyPlane() {
  const meshRef = useRef()

  useFrame(({ clock }) => {
    const positions = meshRef.current.geometry.attributes.position
    const time = clock.elapsedTime

    for (let i = 0; i < positions.count; i++) {
      const x = positions.getX(i)
      const y = positions.getY(i)
      positions.setZ(i, Math.sin(x * 2 + time) * Math.cos(y * 2 + time) * 0.5)
    }

    positions.needsUpdate = true
    meshRef.current.geometry.computeVertexNormals()
  })

  return (
    <mesh ref={meshRef} rotation={[-Math.PI / 2, 0, 0]}>
      <planeGeometry args={[10, 10, 32, 32]} />
      <meshStandardMaterial color="royalblue" side={THREE.DoubleSide} />
    </mesh>
  )
}
```

## Drei Instancing

Efficient rendering of many identical objects.

### Instances Component

```tsx
import { Instances, Instance } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'
import { useRef } from 'react'

function InstancedBoxes() {
  const count = 1000

  return (
    <Instances limit={count} range={count}>
      <boxGeometry args={[0.5, 0.5, 0.5]} />
      <meshStandardMaterial />

      {Array.from({ length: count }, (_, i) => (
        <AnimatedInstance key={i} index={i} />
      ))}
    </Instances>
  )
}

function AnimatedInstance({ index }) {
  const ref = useRef()

  // Random initial position
  const position = useMemo(() => [
    (Math.random() - 0.5) * 20,
    (Math.random() - 0.5) * 20,
    (Math.random() - 0.5) * 20,
  ], [])

  const color = useMemo(() =>
    ['red', 'blue', 'green', 'yellow', 'purple'][index % 5],
  [index])

  useFrame(({ clock }) => {
    const t = clock.elapsedTime
    ref.current.rotation.x = t + index
    ref.current.rotation.y = t * 0.5 + index
  })

  return (
    <Instance
      ref={ref}
      position={position}
      color={color}
      scale={0.5 + Math.random() * 0.5}
    />
  )
}
```

### Merged Geometry

For static instances, merge geometry for best performance:

```tsx
import { Merged } from '@react-three/drei'
import { useMemo } from 'react'
import * as THREE from 'three'

function MergedMeshes() {
  // Create geometries to merge
  const meshes = useMemo(() => ({
    Sphere: new THREE.SphereGeometry(0.5, 32, 32),
    Box: new THREE.BoxGeometry(1, 1, 1),
    Cone: new THREE.ConeGeometry(0.5, 1, 32),
  }), [])

  return (
    <Merged meshes={meshes}>
      {({ Sphere, Box, Cone }) => (
        <>
          <Sphere position={[-2, 0, 0]} color="red" />
          <Sphere position={[-2, 2, 0]} color="orange" />
          <Box position={[0, 0, 0]} color="blue" />
          <Box position={[0, 2, 0]} color="cyan" />
          <Cone position={[2, 0, 0]} color="green" />
          <Cone position={[2, 2, 0]} color="lime" />
        </>
      )}
    </Merged>
  )
}
```

## Points (Particle Systems)

### Basic Points

```tsx
import { Points, Point, PointMaterial } from '@react-three/drei'

function ParticleField() {
  const count = 5000

  return (
    <Points limit={count}>
      <PointMaterial
        transparent
        vertexColors
        size={0.05}
        sizeAttenuation
        depthWrite={false}
      />
      {Array.from({ length: count }, (_, i) => (
        <Point
          key={i}
          position={[
            (Math.random() - 0.5) * 10,
            (Math.random() - 0.5) * 10,
            (Math.random() - 0.5) * 10,
          ]}
          color={`hsl(${Math.random() * 360}, 100%, 50%)`}
        />
      ))}
    </Points>
  )
}
```

### Buffer-Based Points (High Performance)

```tsx
import { useMemo, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

function BufferParticles() {
  const count = 10000
  const pointsRef = useRef()

  const { positions, colors } = useMemo(() => {
    const positions = new Float32Array(count * 3)
    const colors = new Float32Array(count * 3)

    for (let i = 0; i < count; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 10
      positions[i * 3 + 1] = (Math.random() - 0.5) * 10
      positions[i * 3 + 2] = (Math.random() - 0.5) * 10

      colors[i * 3] = Math.random()
      colors[i * 3 + 1] = Math.random()
      colors[i * 3 + 2] = Math.random()
    }

    return { positions, colors }
  }, [])

  useFrame(({ clock }) => {
    pointsRef.current.rotation.y = clock.elapsedTime * 0.1
  })

  return (
    <points ref={pointsRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={count}
          array={positions}
          itemSize={3}
        />
        <bufferAttribute
          attach="attributes-color"
          count={count}
          array={colors}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial size={0.05} vertexColors sizeAttenuation />
    </points>
  )
}
```

## Lines

### Basic Line

```tsx
import { Line } from '@react-three/drei'

function BasicLine() {
  const points = [
    [0, 0, 0],
    [1, 1, 0],
    [2, 0, 0],
    [3, 1, 0],
  ]

  return (
    <Line
      points={points}
      color="red"
      lineWidth={2}
    />
  )
}
```

### Curved Line

```tsx
import { CatmullRomLine, QuadraticBezierLine, CubicBezierLine } from '@react-three/drei'

function CurvedLines() {
  return (
    <>
      {/* Smooth curve through points */}
      <CatmullRomLine
        points={[[0, 0, 0], [1, 1, 0], [2, 0, 0], [3, 1, 0]]}
        color="blue"
        lineWidth={2}
        segments={64}
      />

      {/* Quadratic bezier */}
      <QuadraticBezierLine
        start={[0, 0, 0]}
        mid={[1, 2, 0]}
        end={[2, 0, 0]}
        color="green"
        lineWidth={2}
      />

      {/* Cubic bezier */}
      <CubicBezierLine
        start={[0, 0, 0]}
        midA={[0.5, 2, 0]}
        midB={[1.5, -1, 0]}
        end={[2, 0, 0]}
        color="purple"
        lineWidth={2}
      />
    </>
  )
}
```

### Dashed Line

```tsx
<Line
  points={[[0, 0, 0], [5, 0, 0]]}
  color="white"
  lineWidth={2}
  dashed
  dashScale={50}
  dashSize={0.5}
  dashOffset={0}
  gapSize={0.2}
/>
```

## Edges and Wireframe

```tsx
import { Edges } from '@react-three/drei'

function BoxWithEdges() {
  return (
    <mesh>
      <boxGeometry />
      <meshStandardMaterial color="orange" />
      <Edges
        scale={1.1}
        threshold={15}  // Display edges with angle > 15 degrees
        color="black"
      />
    </mesh>
  )
}

// Wireframe material
function WireframeBox() {
  return (
    <mesh>
      <boxGeometry />
      <meshBasicMaterial color="cyan" wireframe />
    </mesh>
  )
}
```

## Text Geometry

### Using Drei Text3D

```tsx
import { Text3D, Center } from '@react-three/drei'

function Text3DExample() {
  return (
    <Center>
      <Text3D
        font="/fonts/helvetiker_regular.typeface.json"
        size={1}
        height={0.2}
        curveSegments={12}
        bevelEnabled
        bevelThickness={0.02}
        bevelSize={0.02}
        bevelOffset={0}
        bevelSegments={5}
      >
        Hello R3F
        <meshStandardMaterial color="gold" />
      </Text3D>
    </Center>
  )
}
```

## Geometry Utilities

### Center Geometry

```tsx
import { Center } from '@react-three/drei'

function CenteredModel() {
  return (
    <Center>
      <mesh>
        <boxGeometry args={[2, 1, 0.5]} />
        <meshStandardMaterial />
      </mesh>
    </Center>
  )
}

// With options
<Center top left>  {/* Align to top-left */}
  <Model />
</Center>

// Get bounding info
<Center onCentered={({ width, height, depth, boundingBox }) => {
  console.log('Dimensions:', width, height, depth)
}}>
  <Model />
</Center>
```

### Compute Bounds

```tsx
import { useBounds, Bounds } from '@react-three/drei'

function FitToView() {
  return (
    <Bounds fit clip observe margin={1.2}>
      <SelectToZoom />
    </Bounds>
  )
}

function SelectToZoom() {
  const bounds = useBounds()

  return (
    <mesh
      onClick={(e) => {
        e.stopPropagation()
        bounds.refresh(e.object).fit()
      }}
    >
      <boxGeometry />
      <meshStandardMaterial />
    </mesh>
  )
}
```

## Performance Tips

1. **Reuse geometries**: Same geometry instance = better batching
2. **Use Instances**: For many identical objects
3. **Merge static meshes**: Use `<Merged>` for static scenes
4. **Appropriate segment counts**: Balance quality vs performance
5. **Dispose unused geometry**: R3F handles this automatically

```tsx
// Good segment counts
<sphereGeometry args={[1, 32, 32]} />   // Standard quality
<sphereGeometry args={[1, 64, 64]} />   // High quality
<sphereGeometry args={[1, 16, 16]} />   // Performance mode

// Reuse geometry
const sharedGeometry = useMemo(() => new THREE.BoxGeometry(), [])

<mesh geometry={sharedGeometry} position={[0, 0, 0]} />
<mesh geometry={sharedGeometry} position={[2, 0, 0]} />
<mesh geometry={sharedGeometry} position={[4, 0, 0]} />
```

## See Also

- `r3f-fundamentals` - JSX elements and refs
- `r3f-materials` - Materials for meshes
- `r3f-shaders` - Custom vertex manipulation
