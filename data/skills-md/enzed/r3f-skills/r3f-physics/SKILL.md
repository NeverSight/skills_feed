---
name: r3f-physics
description: React Three Fiber physics with Rapier - RigidBody, colliders, forces, joints, sensors. Use when adding physics simulation, collision detection, character controllers, or creating interactive physics-based experiences.
---

# React Three Fiber Physics (Rapier)

## Quick Start

```tsx
import { Canvas } from '@react-three/fiber'
import { Physics, RigidBody, CuboidCollider } from '@react-three/rapier'
import { Suspense } from 'react'

function Scene() {
  return (
    <Canvas>
      <Suspense fallback={null}>
        <Physics debug>
          {/* Falling box */}
          <RigidBody>
            <mesh>
              <boxGeometry />
              <meshStandardMaterial color="orange" />
            </mesh>
          </RigidBody>

          {/* Static ground */}
          <CuboidCollider position={[0, -2, 0]} args={[10, 0.5, 10]} />
        </Physics>
      </Suspense>

      <ambientLight />
      <directionalLight position={[5, 5, 5]} />
    </Canvas>
  )
}
```

## Installation

```bash
npm install @react-three/rapier
```

## Physics Component

The root component that creates the physics world.

```tsx
import { Physics } from '@react-three/rapier'

<Canvas>
  <Suspense fallback={null}>
    <Physics
      gravity={[0, -9.81, 0]}    // Gravity vector
      debug={false}               // Show collider wireframes
      timeStep={1/60}             // Fixed timestep (or "vary" for variable)
      paused={false}              // Pause simulation
      interpolate={true}          // Smooth rendering between physics steps
      colliders="cuboid"          // Default collider type for all RigidBodies
      updateLoop="follow"         // "follow" (sync with frame) or "independent"
    >
      {/* Physics objects */}
    </Physics>
  </Suspense>
</Canvas>
```

### On-Demand Rendering

For performance optimization with static scenes:

```tsx
<Canvas frameloop="demand">
  <Physics updateLoop="independent">
    {/* Physics only triggers render when bodies are active */}
  </Physics>
</Canvas>
```

## RigidBody

Makes objects participate in physics simulation.

### Basic Usage

```tsx
import { RigidBody } from '@react-three/rapier'

// Dynamic body (affected by forces/gravity)
<RigidBody>
  <mesh>
    <boxGeometry />
    <meshStandardMaterial color="red" />
  </mesh>
</RigidBody>

// Fixed body (immovable)
<RigidBody type="fixed">
  <mesh>
    <boxGeometry args={[10, 0.5, 10]} />
    <meshStandardMaterial color="gray" />
  </mesh>
</RigidBody>

// Kinematic body (moved programmatically)
<RigidBody type="kinematicPosition">
  <mesh>
    <sphereGeometry />
    <meshStandardMaterial color="blue" />
  </mesh>
</RigidBody>
```

### RigidBody Types

| Type | Description |
|------|-------------|
| `dynamic` | Affected by forces, gravity, collisions (default) |
| `fixed` | Immovable, infinite mass |
| `kinematicPosition` | Moved via setNextKinematicTranslation |
| `kinematicVelocity` | Moved via setNextKinematicRotation |

### RigidBody Properties

```tsx
<RigidBody
  // Transform
  position={[0, 5, 0]}
  rotation={[0, Math.PI / 4, 0]}
  scale={1}

  // Physics
  type="dynamic"
  mass={1}
  restitution={0.5}           // Bounciness (0-1)
  friction={0.5}              // Surface friction
  linearDamping={0}           // Slows linear velocity
  angularDamping={0}          // Slows angular velocity
  gravityScale={1}            // Multiplier for gravity

  // Collider generation
  colliders="cuboid"          // "cuboid" | "ball" | "hull" | "trimesh" | false

  // Constraints
  lockTranslations={false}    // Prevent all translation
  lockRotations={false}       // Prevent all rotation
  enabledTranslations={[true, true, true]}  // Lock specific axes
  enabledRotations={[true, true, true]}     // Lock specific axes

  // Sleeping
  canSleep={true}
  ccd={false}                 // Continuous collision detection (fast objects)

  // Naming (for collision events)
  name="player"
/>
```

## Colliders

### Automatic Colliders

RigidBody auto-generates colliders from child meshes:

```tsx
// Global default
<Physics colliders="hull">
  <RigidBody>
    <Torus />  {/* Gets hull collider */}
  </RigidBody>
</Physics>

// Per-body override
<Physics colliders={false}>
  <RigidBody colliders="cuboid">
    <Box />
  </RigidBody>

  <RigidBody colliders="ball">
    <Sphere />
  </RigidBody>
</Physics>
```

### Collider Types

| Type | Description | Best For |
|------|-------------|----------|
| `cuboid` | Box shape | Boxes, crates |
| `ball` | Sphere shape | Balls, spherical objects |
| `hull` | Convex hull | Complex convex shapes |
| `trimesh` | Triangle mesh | Concave/complex static geometry |

### Manual Colliders

```tsx
import {
  CuboidCollider,
  BallCollider,
  CapsuleCollider,
  CylinderCollider,
  ConeCollider,
  HeightfieldCollider,
  TrimeshCollider,
  ConvexHullCollider
} from '@react-three/rapier'

// Standalone collider (static)
<CuboidCollider position={[0, -2, 0]} args={[10, 0.5, 10]} />

// Inside RigidBody (compound collider)
<RigidBody position={[0, 5, 0]}>
  <mesh>
    <boxGeometry />
    <meshStandardMaterial />
  </mesh>

  {/* Additional colliders */}
  <BallCollider args={[0.5]} position={[0, 1, 0]} />
  <CapsuleCollider args={[0.5, 1]} position={[0, -1, 0]} />
</RigidBody>

// Collider args reference
<CuboidCollider args={[halfWidth, halfHeight, halfDepth]} />
<BallCollider args={[radius]} />
<CapsuleCollider args={[halfHeight, radius]} />
<CylinderCollider args={[halfHeight, radius]} />
<ConeCollider args={[halfHeight, radius]} />
```

### Mesh Colliders

For complex shapes:

```tsx
import { MeshCollider } from '@react-three/rapier'

<RigidBody colliders={false}>
  <MeshCollider type="trimesh">
    <mesh geometry={complexGeometry}>
      <meshStandardMaterial />
    </mesh>
  </MeshCollider>
</RigidBody>

// Convex hull for dynamic bodies
<RigidBody colliders={false}>
  <MeshCollider type="hull">
    <mesh geometry={someGeometry} />
  </MeshCollider>
</RigidBody>
```

## Applying Forces

### Using Refs

```tsx
import { RigidBody, RapierRigidBody } from '@react-three/rapier'
import { useRef, useEffect } from 'react'

function ForcefulBox() {
  const rigidBody = useRef<RapierRigidBody>(null)

  useEffect(() => {
    if (rigidBody.current) {
      // One-time impulse (instantaneous)
      rigidBody.current.applyImpulse({ x: 0, y: 10, z: 0 }, true)

      // Continuous force (apply each frame)
      rigidBody.current.addForce({ x: 0, y: 10, z: 0 }, true)

      // Torque (rotation)
      rigidBody.current.applyTorqueImpulse({ x: 0, y: 5, z: 0 }, true)
      rigidBody.current.addTorque({ x: 0, y: 5, z: 0 }, true)
    }
  }, [])

  return (
    <RigidBody ref={rigidBody}>
      <mesh>
        <boxGeometry />
        <meshStandardMaterial color="red" />
      </mesh>
    </RigidBody>
  )
}
```

### In useFrame

```tsx
import { useFrame } from '@react-three/fiber'

function ContinuousForce() {
  const rigidBody = useRef<RapierRigidBody>(null)

  useFrame(() => {
    if (rigidBody.current) {
      // Apply force every frame
      rigidBody.current.addForce({ x: 0, y: 20, z: 0 }, true)
    }
  })

  return (
    <RigidBody ref={rigidBody} gravityScale={0.5}>
      <mesh>
        <sphereGeometry />
        <meshStandardMaterial color="blue" />
      </mesh>
    </RigidBody>
  )
}
```

### Getting/Setting Position

```tsx
import { vec3, quat, euler } from '@react-three/rapier'

function PositionControl() {
  const rigidBody = useRef<RapierRigidBody>(null)

  const teleport = () => {
    if (rigidBody.current) {
      // Get current transform
      const position = vec3(rigidBody.current.translation())
      const rotation = quat(rigidBody.current.rotation())

      // Set new transform
      rigidBody.current.setTranslation({ x: 0, y: 10, z: 0 }, true)
      rigidBody.current.setRotation({ x: 0, y: 0, z: 0, w: 1 }, true)

      // Set velocities
      rigidBody.current.setLinvel({ x: 0, y: 0, z: 0 }, true)
      rigidBody.current.setAngvel({ x: 0, y: 0, z: 0 }, true)
    }
  }

  return (
    <RigidBody ref={rigidBody}>
      <mesh onClick={teleport}>
        <boxGeometry />
        <meshStandardMaterial />
      </mesh>
    </RigidBody>
  )
}
```

## Collision Events

### On RigidBody

```tsx
<RigidBody
  name="player"
  onCollisionEnter={({ manifold, target, other }) => {
    console.log('Collision with', other.rigidBodyObject?.name)
    console.log('Contact point', manifold.solverContactPoint(0))
  }}
  onCollisionExit={({ target, other }) => {
    console.log('Collision ended with', other.rigidBodyObject?.name)
  }}
  onContactForce={({ totalForce }) => {
    console.log('Contact force:', totalForce)
  }}
  onSleep={() => console.log('Body went to sleep')}
  onWake={() => console.log('Body woke up')}
>
  <mesh>
    <boxGeometry />
    <meshStandardMaterial />
  </mesh>
</RigidBody>
```

### On Colliders

```tsx
<CuboidCollider
  args={[1, 1, 1]}
  onCollisionEnter={(payload) => console.log('Collider hit')}
  onCollisionExit={(payload) => console.log('Collider exit')}
/>
```

## Sensors

Detect overlaps without physical collision:

```tsx
<RigidBody>
  {/* Visible mesh */}
  <mesh>
    <boxGeometry />
    <meshStandardMaterial />
  </mesh>

  {/* Invisible sensor trigger */}
  <CuboidCollider
    args={[2, 2, 2]}
    sensor
    onIntersectionEnter={() => console.log('Entered trigger zone')}
    onIntersectionExit={() => console.log('Exited trigger zone')}
  />
</RigidBody>

// Goal detection example
<RigidBody type="fixed">
  <GoalPosts />
  <CuboidCollider
    args={[5, 5, 1]}
    sensor
    onIntersectionEnter={() => console.log('Goal!')}
  />
</RigidBody>
```

## Collision Groups

Control which objects can collide:

```tsx
import { interactionGroups } from '@react-three/rapier'

// Group 0, interacts with groups 0, 1, 2
<CuboidCollider collisionGroups={interactionGroups(0, [0, 1, 2])} />

// Group 12, interacts with all groups
<CuboidCollider collisionGroups={interactionGroups(12)} />

// Groups 0 and 5, only interacts with group 7
<CuboidCollider collisionGroups={interactionGroups([0, 5], 7)} />

// On RigidBody (applies to all auto-generated colliders)
<RigidBody collisionGroups={interactionGroups(1, [1, 2])}>
  <mesh>...</mesh>
</RigidBody>
```

## Joints

Connect rigid bodies together.

### Fixed Joint

Bodies don't move relative to each other:

```tsx
import { useFixedJoint, RapierRigidBody } from '@react-three/rapier'

function FixedJointExample() {
  const bodyA = useRef<RapierRigidBody>(null)
  const bodyB = useRef<RapierRigidBody>(null)

  useFixedJoint(bodyA, bodyB, [
    [0, 0, 0],      // Position in bodyA's local space
    [0, 0, 0, 1],   // Orientation in bodyA's local space (quaternion)
    [0, -1, 0],     // Position in bodyB's local space
    [0, 0, 0, 1],   // Orientation in bodyB's local space
  ])

  return (
    <>
      <RigidBody ref={bodyA} position={[0, 5, 0]}>
        <mesh><boxGeometry /><meshStandardMaterial color="red" /></mesh>
      </RigidBody>
      <RigidBody ref={bodyB} position={[0, 4, 0]}>
        <mesh><boxGeometry /><meshStandardMaterial color="blue" /></mesh>
      </RigidBody>
    </>
  )
}
```

### Revolute Joint (Hinge)

Rotation around one axis:

```tsx
import { useRevoluteJoint } from '@react-three/rapier'

function HingeDoor() {
  const frame = useRef<RapierRigidBody>(null)
  const door = useRef<RapierRigidBody>(null)

  useRevoluteJoint(frame, door, [
    [0.5, 0, 0],    // Joint position in frame's local space
    [-0.5, 0, 0],   // Joint position in door's local space
    [0, 1, 0],      // Rotation axis
  ])

  return (
    <>
      <RigidBody ref={frame} type="fixed">
        <mesh><boxGeometry args={[0.1, 2, 0.1]} /></mesh>
      </RigidBody>
      <RigidBody ref={door}>
        <mesh><boxGeometry args={[1, 2, 0.1]} /></mesh>
      </RigidBody>
    </>
  )
}
```

### Spherical Joint (Ball-Socket)

Rotation in all directions:

```tsx
import { useSphericalJoint } from '@react-three/rapier'

function BallJoint() {
  const bodyA = useRef<RapierRigidBody>(null)
  const bodyB = useRef<RapierRigidBody>(null)

  useSphericalJoint(bodyA, bodyB, [
    [0, -0.5, 0],   // Position in bodyA's local space
    [0, 0.5, 0],    // Position in bodyB's local space
  ])

  return (
    <>
      <RigidBody ref={bodyA} type="fixed" position={[0, 3, 0]}>
        <mesh><sphereGeometry args={[0.2]} /></mesh>
      </RigidBody>
      <RigidBody ref={bodyB} position={[0, 2, 0]}>
        <mesh><boxGeometry /></mesh>
      </RigidBody>
    </>
  )
}
```

### Prismatic Joint (Slider)

Translation along one axis:

```tsx
import { usePrismaticJoint } from '@react-three/rapier'

function Slider() {
  const track = useRef<RapierRigidBody>(null)
  const slider = useRef<RapierRigidBody>(null)

  usePrismaticJoint(track, slider, [
    [0, 0, 0],      // Position in track's local space
    [0, 0, 0],      // Position in slider's local space
    [1, 0, 0],      // Axis of translation
  ])

  return (
    <>
      <RigidBody ref={track} type="fixed">
        <mesh><boxGeometry args={[5, 0.1, 0.1]} /></mesh>
      </RigidBody>
      <RigidBody ref={slider}>
        <mesh><boxGeometry args={[0.5, 0.5, 0.5]} /></mesh>
      </RigidBody>
    </>
  )
}
```

### Spring Joint

Elastic connection:

```tsx
import { useSpringJoint } from '@react-three/rapier'

function SpringConnection() {
  const anchor = useRef<RapierRigidBody>(null)
  const ball = useRef<RapierRigidBody>(null)

  useSpringJoint(anchor, ball, [
    [0, 0, 0],      // Position in anchor's local space
    [0, 0, 0],      // Position in ball's local space
    2,              // Rest length
    1000,           // Stiffness
    10,             // Damping
  ])

  return (
    <>
      <RigidBody ref={anchor} type="fixed" position={[0, 5, 0]}>
        <mesh><sphereGeometry args={[0.1]} /></mesh>
      </RigidBody>
      <RigidBody ref={ball} position={[0, 3, 0]}>
        <mesh><sphereGeometry args={[0.5]} /></mesh>
      </RigidBody>
    </>
  )
}
```

### Rope Joint

Maximum distance constraint:

```tsx
import { useRopeJoint } from '@react-three/rapier'

function RopeConnection() {
  const anchor = useRef<RapierRigidBody>(null)
  const weight = useRef<RapierRigidBody>(null)

  useRopeJoint(anchor, weight, [
    [0, 0, 0],      // Position in anchor's local space
    [0, 0, 0],      // Position in weight's local space
    3,              // Max distance (rope length)
  ])

  return (
    <>
      <RigidBody ref={anchor} type="fixed" position={[0, 5, 0]}>
        <mesh><sphereGeometry args={[0.1]} /></mesh>
      </RigidBody>
      <RigidBody ref={weight} position={[0, 2, 0]}>
        <mesh><sphereGeometry args={[0.5]} /></mesh>
      </RigidBody>
    </>
  )
}
```

### Motorized Joints

```tsx
import { useRevoluteJoint } from '@react-three/rapier'
import { useFrame } from '@react-three/fiber'

function MotorizedWheel({ bodyA, bodyB }) {
  const joint = useRevoluteJoint(bodyA, bodyB, [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 1],  // Rotation axis
  ])

  useFrame(() => {
    if (joint.current) {
      // Configure motor: velocity, damping
      joint.current.configureMotorVelocity(10, 2)
    }
  })

  return null
}
```

## Instanced Physics

Efficient physics for many identical objects:

```tsx
import { InstancedRigidBodies, RapierRigidBody } from '@react-three/rapier'
import { useRef, useMemo } from 'react'

function InstancedBalls() {
  const COUNT = 100
  const rigidBodies = useRef<RapierRigidBody[]>(null)

  const instances = useMemo(() => {
    return Array.from({ length: COUNT }, (_, i) => ({
      key: `ball-${i}`,
      position: [
        (Math.random() - 0.5) * 10,
        Math.random() * 10 + 5,
        (Math.random() - 0.5) * 10,
      ] as [number, number, number],
      rotation: [0, 0, 0] as [number, number, number],
    }))
  }, [])

  return (
    <InstancedRigidBodies
      ref={rigidBodies}
      instances={instances}
      colliders="ball"
    >
      <instancedMesh args={[undefined, undefined, COUNT]}>
        <sphereGeometry args={[0.5]} />
        <meshStandardMaterial color="orange" />
      </instancedMesh>
    </InstancedRigidBodies>
  )
}
```

## Accessing the World

```tsx
import { useRapier } from '@react-three/rapier'
import { useEffect } from 'react'

function WorldAccess() {
  const { world, rapier } = useRapier()

  useEffect(() => {
    // Change gravity
    world.setGravity({ x: 0, y: -20, z: 0 })

    // Iterate over bodies
    world.bodies.forEach((body) => {
      console.log(body.translation())
    })
  }, [world])

  return null
}
```

### Manual Stepping

```tsx
function ManualStep() {
  const { step } = useRapier()

  const advancePhysics = () => {
    step(1 / 60)  // Advance by one frame
  }

  return <button onClick={advancePhysics}>Step</button>
}
```

### World Snapshots

Save and restore physics state:

```tsx
function SnapshotSystem() {
  const { world, setWorld, rapier } = useRapier()
  const snapshot = useRef<Uint8Array>()

  const saveState = () => {
    snapshot.current = world.takeSnapshot()
  }

  const loadState = () => {
    if (snapshot.current) {
      setWorld(rapier.World.restoreSnapshot(snapshot.current))
    }
  }

  return (
    <>
      <button onClick={saveState}>Save</button>
      <button onClick={loadState}>Load</button>
    </>
  )
}
```

## Attractors

From `@react-three/rapier-addons`:

```tsx
import { Attractor } from '@react-three/rapier-addons'

// Attract nearby bodies
<Attractor
  position={[0, 0, 0]}
  range={10}
  strength={5}
  type="linear"        // "static" | "linear" | "newtonian"
/>

// Repel bodies
<Attractor range={10} strength={-5} position={[5, 0, 0]} />

// Selective attraction (only affect certain groups)
<Attractor
  range={10}
  strength={10}
  collisionGroups={interactionGroups(0, [2, 3])}
/>
```

## Debug Visualization

```tsx
<Physics debug>
  {/* All colliders shown as wireframes */}
</Physics>

// Conditional debug
<Physics debug={process.env.NODE_ENV === 'development'}>
  ...
</Physics>
```

## Performance Tips

1. **Use appropriate collider types**: `cuboid` and `ball` are fastest
2. **Avoid `trimesh` for dynamic bodies**: Use `hull` instead
3. **Enable sleeping**: Bodies at rest stop computing
4. **Use collision groups**: Reduce collision checks
5. **Limit active bodies**: Too many dynamic bodies hurts performance
6. **Use instanced bodies**: For many identical objects
7. **Fixed timestep**: More stable than variable

```tsx
// Performance-optimized setup
<Physics
  timeStep={1/60}
  colliders="cuboid"
  gravity={[0, -9.81, 0]}
>
  {/* Use collision groups to limit checks */}
  <RigidBody collisionGroups={interactionGroups(0, [0, 1])}>
    ...
  </RigidBody>
</Physics>
```

## See Also

- `r3f-fundamentals` - R3F basics and hooks
- `r3f-interaction` - User input and controls
- `r3f-animation` - Combining physics with animation
