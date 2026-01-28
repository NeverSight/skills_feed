---
name: r3f-lighting
description: React Three Fiber lighting - light types, shadows, Environment component, IBL. Use when adding lights, configuring shadows, setting up environment lighting, or optimizing lighting performance.
---

# React Three Fiber Lighting

## Quick Start

```tsx
import { Canvas } from '@react-three/fiber'

function Scene() {
  return (
    <Canvas shadows>
      {/* Ambient fill */}
      <ambientLight intensity={0.5} />

      {/* Main light with shadows */}
      <directionalLight
        position={[5, 5, 5]}
        intensity={1}
        castShadow
        shadow-mapSize={[2048, 2048]}
      />

      {/* Objects */}
      <mesh castShadow receiveShadow>
        <boxGeometry />
        <meshStandardMaterial color="orange" />
      </mesh>

      {/* Ground */}
      <mesh receiveShadow rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.5, 0]}>
        <planeGeometry args={[10, 10]} />
        <meshStandardMaterial color="#888" />
      </mesh>
    </Canvas>
  )
}
```

## Light Types Overview

| Light | Description | Shadow Support | Cost |
|-------|-------------|----------------|------|
| ambientLight | Uniform everywhere | No | Very Low |
| hemisphereLight | Sky/ground gradient | No | Very Low |
| directionalLight | Parallel rays (sun) | Yes | Low |
| pointLight | Omnidirectional (bulb) | Yes | Medium |
| spotLight | Cone-shaped | Yes | Medium |
| rectAreaLight | Area light (window) | No* | High |

## ambientLight

Illuminates all objects equally. No direction, no shadows.

```tsx
<ambientLight
  color="#ffffff"  // or color={new THREE.Color('#ffffff')}
  intensity={0.5}
/>
```

## hemisphereLight

Gradient from sky to ground. Good for outdoor scenes.

```tsx
<hemisphereLight
  color="#87ceeb"        // Sky color
  groundColor="#8b4513"  // Ground color
  intensity={0.6}
  position={[0, 50, 0]}
/>
```

## directionalLight

Parallel light rays. Simulates distant light (sun).

```tsx
<directionalLight
  color="#ffffff"
  intensity={1}
  position={[5, 10, 5]}

  // Shadow configuration
  castShadow
  shadow-mapSize={[2048, 2048]}
  shadow-camera-near={0.5}
  shadow-camera-far={50}
  shadow-camera-left={-10}
  shadow-camera-right={10}
  shadow-camera-top={10}
  shadow-camera-bottom={-10}
  shadow-bias={-0.0001}
  shadow-normalBias={0.02}
/>

// With target (light points at target)
function DirectionalWithTarget() {
  const lightRef = useRef()

  return (
    <>
      <directionalLight
        ref={lightRef}
        position={[5, 10, 5]}
        target-position={[0, 0, 0]}
      />
    </>
  )
}
```

## pointLight

Emits light in all directions. Like a light bulb.

```tsx
<pointLight
  color="#ffffff"
  intensity={1}
  position={[0, 5, 0]}
  distance={100}  // Maximum range (0 = infinite)
  decay={2}       // Light falloff (physically correct = 2)

  // Shadows
  castShadow
  shadow-mapSize={[1024, 1024]}
  shadow-camera-near={0.5}
  shadow-camera-far={50}
  shadow-bias={-0.005}
/>
```

## spotLight

Cone-shaped light. Like a flashlight.

```tsx
<spotLight
  color="#ffffff"
  intensity={1}
  position={[0, 10, 0]}
  angle={Math.PI / 6}     // Cone angle (max Math.PI/2)
  penumbra={0.5}          // Soft edge (0-1)
  distance={100}          // Range
  decay={2}               // Falloff

  // Target
  target-position={[0, 0, 0]}

  // Shadows
  castShadow
  shadow-mapSize={[1024, 1024]}
  shadow-camera-near={0.5}
  shadow-camera-far={50}
  shadow-camera-fov={30}
  shadow-bias={-0.0001}
/>

// SpotLight helper
import { useHelper } from '@react-three/drei'
import { SpotLightHelper } from 'three'

function SpotLightWithHelper() {
  const lightRef = useRef()
  useHelper(lightRef, SpotLightHelper, 'cyan')

  return <spotLight ref={lightRef} position={[0, 5, 0]} />
}
```

## rectAreaLight

Rectangular area light. Great for soft, realistic lighting.

```tsx
import { RectAreaLightHelper } from 'three/examples/jsm/helpers/RectAreaLightHelper'

function AreaLight() {
  const lightRef = useRef()

  return (
    <>
      <rectAreaLight
        ref={lightRef}
        color="#ffffff"
        intensity={5}
        width={4}
        height={2}
        position={[0, 5, 0]}
        rotation={[-Math.PI / 2, 0, 0]}  // Point downward
      />
    </>
  )
}

// Note: RectAreaLight only works with MeshStandardMaterial and MeshPhysicalMaterial
// Does not cast shadows natively
```

## Shadow Setup

### Enable Shadows on Canvas

```tsx
<Canvas
  shadows  // or shadows="soft" | "basic" | "percentage" | "variance"
>
```

### Shadow Types

```tsx
// Basic shadows (fastest, hard edges)
<Canvas shadows="basic">

// PCF shadows (default, filtered)
<Canvas shadows>

// Soft shadows (PCFSoft, softer edges)
<Canvas shadows="soft">

// VSM shadows (variance shadow map)
<Canvas shadows="variance">
```

### Configure Shadow-Casting Objects

```tsx
// Light must cast shadows
<directionalLight castShadow />

// Objects must cast and/or receive shadows
<mesh castShadow receiveShadow>
  <boxGeometry />
  <meshStandardMaterial />
</mesh>

// Ground typically only receives
<mesh receiveShadow>
  <planeGeometry args={[100, 100]} />
  <meshStandardMaterial />
</mesh>
```

### Shadow Camera Helper

```tsx
import { useHelper } from '@react-three/drei'
import { CameraHelper } from 'three'

function LightWithShadowHelper() {
  const lightRef = useRef()

  // Visualize shadow camera frustum
  useHelper(lightRef.current?.shadow.camera, CameraHelper)

  return (
    <directionalLight
      ref={lightRef}
      castShadow
      shadow-camera-left={-10}
      shadow-camera-right={10}
      shadow-camera-top={10}
      shadow-camera-bottom={-10}
    />
  )
}
```

## Drei Lighting Helpers

### Environment

HDR environment lighting with presets or custom files.

```tsx
import { Environment } from '@react-three/drei'

// Preset environments
<Environment
  preset="sunset"  // apartment, city, dawn, forest, lobby, night, park, studio, sunset, warehouse
  background       // Also use as background
  backgroundBlurriness={0}  // Background blur
  backgroundIntensity={1}   // Background brightness
  environmentIntensity={1}  // Lighting intensity
/>

// Custom HDR file
<Environment files="/hdri/studio.hdr" />

// Cube map (6 images)
<Environment
  files={['px.png', 'nx.png', 'py.png', 'ny.png', 'pz.png', 'nz.png']}
  path="/textures/cube/"
/>

// Ground projection
<Environment
  preset="city"
  ground={{
    height: 15,
    radius: 100,
    scale: 100,
  }}
/>
```

### Lightformer

Create custom light shapes inside Environment.

```tsx
import { Environment, Lightformer } from '@react-three/drei'

<Environment>
  <Lightformer
    form="ring"          // circle, ring, rect
    intensity={2}
    color="white"
    scale={10}
    position={[0, 5, -5]}
    target={[0, 0, 0]}   // Point at target
  />

  <Lightformer
    form="rect"
    intensity={1}
    color="red"
    scale={[5, 2]}
    position={[-5, 5, 0]}
  />
</Environment>
```

### Sky

Procedural sky with sun.

```tsx
import { Sky } from '@react-three/drei'

<Sky
  distance={450000}
  sunPosition={[0, 1, 0]}   // Or calculate from inclination/azimuth
  inclination={0.6}         // Sun elevation (0 = horizon, 0.5 = zenith)
  azimuth={0.25}            // Sun rotation around horizon
  turbidity={10}            // Haziness
  rayleigh={2}              // Light scattering
  mieCoefficient={0.005}
  mieDirectionalG={0.8}
/>
```

### Stars

Starfield background.

```tsx
import { Stars } from '@react-three/drei'

<Stars
  radius={100}      // Sphere radius
  depth={50}        // Depth of star distribution
  count={5000}      // Number of stars
  factor={4}        // Size factor
  saturation={0}    // Color saturation
  fade              // Fade at edges
  speed={1}         // Twinkle speed
/>
```

### Stage

Quick lighting setup for product showcase.

```tsx
import { Stage } from '@react-three/drei'

<Stage
  preset="rembrandt"  // rembrandt, portrait, upfront, soft
  intensity={1}
  shadows="contact"   // false, 'contact', 'accumulative', true
  environment="city"
  adjustCamera={1.2}  // Adjust camera to fit content
>
  <Model />
</Stage>
```

### ContactShadows

Fast fake shadows without shadow mapping.

```tsx
import { ContactShadows } from '@react-three/drei'

<ContactShadows
  position={[0, -0.5, 0]}
  opacity={0.5}
  scale={10}
  blur={1}
  far={10}
  resolution={256}
  color="#000000"
  frames={1}        // Render once (for static scenes)
/>

// For animated scenes
<ContactShadows frames={Infinity} />
```

### AccumulativeShadows

Soft, accumulated shadows.

```tsx
import { AccumulativeShadows, RandomizedLight } from '@react-three/drei'

<AccumulativeShadows
  position={[0, -0.5, 0]}
  scale={10}
  color="#316d39"
  opacity={0.8}
  frames={100}
  temporal          // Smooth accumulation over time
>
  <RandomizedLight
    amount={8}
    radius={4}
    ambient={0.5}
    intensity={1}
    position={[5, 5, -10]}
    bias={0.001}
  />
</AccumulativeShadows>
```

### SoftShadows

Enable PCF soft shadows globally.

```tsx
import { SoftShadows } from '@react-three/drei'

<Canvas shadows>
  <SoftShadows
    size={25}
    samples={10}
    focus={0}
  />
</Canvas>
```

### BakeShadows

Bake shadows for static scenes.

```tsx
import { BakeShadows } from '@react-three/drei'

<Canvas shadows>
  <BakeShadows />  {/* Bakes shadows once on mount */}
</Canvas>
```

## Common Lighting Setups

### Three-Point Lighting

```tsx
function ThreePointLighting() {
  return (
    <>
      {/* Key light (main) */}
      <directionalLight
        position={[5, 5, 5]}
        intensity={1}
        castShadow
      />

      {/* Fill light (softer, opposite side) */}
      <directionalLight
        position={[-5, 3, 5]}
        intensity={0.5}
      />

      {/* Back light (rim lighting) */}
      <directionalLight
        position={[0, 5, -5]}
        intensity={0.3}
      />

      {/* Ambient fill */}
      <ambientLight intensity={0.2} />
    </>
  )
}
```

### Outdoor Daylight

```tsx
import { Sky, Environment } from '@react-three/drei'

function OutdoorLighting() {
  return (
    <>
      <Sky sunPosition={[100, 100, 100]} />
      <Environment preset="dawn" />

      <directionalLight
        position={[50, 100, 50]}
        intensity={1.5}
        castShadow
        shadow-mapSize={[2048, 2048]}
        shadow-camera-far={200}
        shadow-camera-left={-50}
        shadow-camera-right={50}
        shadow-camera-top={50}
        shadow-camera-bottom={-50}
      />

      <hemisphereLight
        color="#87ceeb"
        groundColor="#8b4513"
        intensity={0.5}
      />
    </>
  )
}
```

### Studio Lighting

```tsx
import { Environment, Lightformer, ContactShadows } from '@react-three/drei'

function StudioLighting() {
  return (
    <>
      <Environment resolution={256}>
        {/* Key light */}
        <Lightformer
          form="rect"
          intensity={4}
          position={[5, 5, -5]}
          scale={[10, 5]}
          target={[0, 0, 0]}
        />

        {/* Fill light */}
        <Lightformer
          form="rect"
          intensity={2}
          position={[-5, 5, 5]}
          scale={[10, 5]}
        />

        {/* Rim light */}
        <Lightformer
          form="ring"
          intensity={1}
          position={[0, 5, -10]}
          scale={5}
        />
      </Environment>

      <ContactShadows
        position={[0, -0.5, 0]}
        opacity={0.5}
        blur={2}
      />
    </>
  )
}
```

## Animated Lighting

```tsx
import { useFrame } from '@react-three/fiber'
import { useRef } from 'react'

function AnimatedLight() {
  const lightRef = useRef()

  useFrame(({ clock }) => {
    const t = clock.elapsedTime

    // Orbit around scene
    lightRef.current.position.x = Math.cos(t) * 5
    lightRef.current.position.z = Math.sin(t) * 5

    // Pulsing intensity
    lightRef.current.intensity = 1 + Math.sin(t * 2) * 0.5

    // Color cycling
    lightRef.current.color.setHSL((t * 0.1) % 1, 1, 0.5)
  })

  return (
    <pointLight ref={lightRef} position={[5, 3, 0]} castShadow />
  )
}
```

## Light Helpers

```tsx
import { useHelper } from '@react-three/drei'
import {
  DirectionalLightHelper,
  PointLightHelper,
  SpotLightHelper,
  HemisphereLightHelper,
} from 'three'

function LightWithHelpers() {
  const dirLightRef = useRef()
  const pointLightRef = useRef()
  const spotLightRef = useRef()
  const hemiLightRef = useRef()

  useHelper(dirLightRef, DirectionalLightHelper, 5, 'red')
  useHelper(pointLightRef, PointLightHelper, 1, 'green')
  useHelper(spotLightRef, SpotLightHelper, 'blue')
  useHelper(hemiLightRef, HemisphereLightHelper, 5, 'yellow', 'brown')

  return (
    <>
      <directionalLight ref={dirLightRef} position={[5, 5, 5]} />
      <pointLight ref={pointLightRef} position={[-5, 5, 0]} />
      <spotLight ref={spotLightRef} position={[0, 5, 5]} />
      <hemisphereLight ref={hemiLightRef} />
    </>
  )
}
```

## Performance Tips

1. **Limit light count**: Each light adds shader complexity
2. **Use baked lighting**: For static scenes
3. **Smaller shadow maps**: 512-1024 often sufficient
4. **Tight shadow frustums**: Only cover needed area
5. **Disable unused shadows**: Not all lights need shadows
6. **Use Environment**: More efficient than many lights

```tsx
// Selective shadows
<mesh castShadow={isHero}>
  <boxGeometry />
</mesh>

// Only update shadows when needed
<ContactShadows frames={isAnimating ? Infinity : 1} />

// Use layers to exclude objects from lights
<directionalLight layers={1} />
<mesh layers={1}>  {/* Affected by light */}
<mesh layers={2}>  {/* Not affected */}
```

## See Also

- `r3f-materials` - Material light response
- `r3f-textures` - Environment maps
- `r3f-postprocessing` - Bloom and light effects
