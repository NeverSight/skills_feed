---
name: r3f-materials
description: React Three Fiber materials - PBR materials, Drei materials, shader materials, material properties. Use when styling meshes, creating custom materials, working with textures, or implementing visual effects.
---

# React Three Fiber Materials

## Quick Start

```tsx
import { Canvas } from '@react-three/fiber'

function Scene() {
  return (
    <Canvas>
      <ambientLight intensity={0.5} />
      <directionalLight position={[5, 5, 5]} />

      <mesh>
        <boxGeometry />
        <meshStandardMaterial
          color="hotpink"
          roughness={0.5}
          metalness={0.5}
        />
      </mesh>
    </Canvas>
  )
}
```

## Material Types Overview

| Material | Use Case | Lighting |
|----------|----------|----------|
| meshBasicMaterial | Unlit, flat colors | No |
| meshLambertMaterial | Matte surfaces, fast | Yes (diffuse) |
| meshPhongMaterial | Shiny, specular | Yes |
| meshStandardMaterial | PBR, realistic | Yes (PBR) |
| meshPhysicalMaterial | Advanced PBR | Yes (PBR+) |
| meshToonMaterial | Cel-shaded | Yes (toon) |
| meshNormalMaterial | Debug normals | No |
| shaderMaterial | Custom GLSL | Custom |

## meshBasicMaterial

No lighting calculations. Always visible, fast.

```tsx
<mesh>
  <boxGeometry />
  <meshBasicMaterial
    color="red"
    transparent
    opacity={0.5}
    side={THREE.DoubleSide}  // FrontSide, BackSide, DoubleSide
    wireframe={false}
    map={colorTexture}
    alphaMap={alphaTexture}
    envMap={envTexture}
    fog={true}
  />
</mesh>
```

## meshStandardMaterial (PBR)

Physically-based rendering. Recommended for realistic results.

```tsx
import { useTexture } from '@react-three/drei'
import * as THREE from 'three'

function PBRMesh() {
  // Load PBR texture set
  const [colorMap, normalMap, roughnessMap, metalnessMap, aoMap] = useTexture([
    '/textures/color.jpg',
    '/textures/normal.jpg',
    '/textures/roughness.jpg',
    '/textures/metalness.jpg',
    '/textures/ao.jpg',
  ])

  return (
    <mesh>
      <sphereGeometry args={[1, 64, 64]} />
      <meshStandardMaterial
        // Base color
        color="#ffffff"
        map={colorMap}

        // PBR properties
        roughness={1}         // 0 = mirror, 1 = diffuse
        roughnessMap={roughnessMap}
        metalness={0}         // 0 = dielectric, 1 = metal
        metalnessMap={metalnessMap}

        // Surface detail
        normalMap={normalMap}
        normalScale={[1, 1]}

        // Ambient occlusion (requires uv2)
        aoMap={aoMap}
        aoMapIntensity={1}

        // Emissive
        emissive="#000000"
        emissiveIntensity={1}
        emissiveMap={emissiveTexture}

        // Environment
        envMap={envTexture}
        envMapIntensity={1}

        // Other
        flatShading={false}
        fog={true}
        transparent={false}
      />
    </mesh>
  )
}
```

## meshPhysicalMaterial (Advanced PBR)

Extends Standard with clearcoat, transmission, sheen, etc.

```tsx
// Glass material
function Glass() {
  return (
    <mesh>
      <sphereGeometry args={[1, 64, 64]} />
      <meshPhysicalMaterial
        color="#ffffff"
        metalness={0}
        roughness={0}
        transmission={1}      // 0 = opaque, 1 = fully transparent
        thickness={0.5}       // Volume thickness for refraction
        ior={1.5}             // Index of refraction (glass ~1.5)
        envMapIntensity={1}
      />
    </mesh>
  )
}

// Car paint
function CarPaint() {
  return (
    <mesh>
      <boxGeometry />
      <meshPhysicalMaterial
        color="#ff0000"
        metalness={0.9}
        roughness={0.5}
        clearcoat={1}              // Clearcoat layer strength
        clearcoatRoughness={0.1}   // Clearcoat roughness
      />
    </mesh>
  )
}

// Fabric/velvet (sheen)
function Fabric() {
  return (
    <mesh>
      <sphereGeometry args={[1, 64, 64]} />
      <meshPhysicalMaterial
        color="#8844aa"
        roughness={0.8}
        sheen={1}
        sheenRoughness={0.5}
        sheenColor="#ff88ff"
      />
    </mesh>
  )
}

// Iridescent (soap bubbles)
function Iridescent() {
  return (
    <mesh>
      <sphereGeometry args={[1, 64, 64]} />
      <meshPhysicalMaterial
        color="#ffffff"
        iridescence={1}
        iridescenceIOR={1.3}
        iridescenceThicknessRange={[100, 400]}
      />
    </mesh>
  )
}
```

## Drei Special Materials

### MeshReflectorMaterial

Realistic mirror-like reflections.

```tsx
import { MeshReflectorMaterial } from '@react-three/drei'

function ReflectiveFloor() {
  return (
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.5, 0]}>
      <planeGeometry args={[10, 10]} />
      <MeshReflectorMaterial
        blur={[400, 100]}         // Blur amount [x, y]
        resolution={1024}         // Reflection resolution
        mixBlur={1}               // Mix blur with reflection
        mixStrength={0.5}         // Reflection strength
        roughness={1}
        depthScale={1.2}
        minDepthThreshold={0.4}
        maxDepthThreshold={1.4}
        color="#333"
        metalness={0.5}
        mirror={0.5}
      />
    </mesh>
  )
}
```

### MeshWobbleMaterial

Animated wobble effect.

```tsx
import { MeshWobbleMaterial } from '@react-three/drei'

function WobblyMesh() {
  return (
    <mesh>
      <torusKnotGeometry args={[1, 0.4, 100, 16]} />
      <MeshWobbleMaterial
        factor={1}       // Wobble amplitude
        speed={2}        // Wobble speed
        color="hotpink"
        metalness={0}
        roughness={0.5}
      />
    </mesh>
  )
}
```

### MeshDistortMaterial

Perlin noise distortion.

```tsx
import { MeshDistortMaterial } from '@react-three/drei'

function DistortedMesh() {
  return (
    <mesh>
      <sphereGeometry args={[1, 64, 64]} />
      <MeshDistortMaterial
        distort={0.5}    // Distortion amount
        speed={2}        // Animation speed
        color="cyan"
        roughness={0.2}
      />
    </mesh>
  )
}
```

### MeshTransmissionMaterial

Better glass/refractive materials.

```tsx
import { MeshTransmissionMaterial } from '@react-three/drei'

function GlassSphere() {
  return (
    <mesh>
      <sphereGeometry args={[1, 64, 64]} />
      <MeshTransmissionMaterial
        backside              // Render backside
        samples={16}          // Refraction samples
        resolution={1024}     // Buffer resolution
        transmission={1}      // Transmission factor
        roughness={0.0}
        thickness={0.5}       // Volume thickness
        ior={1.5}             // Index of refraction
        chromaticAberration={0.06}
        anisotropy={0.1}
        distortion={0.0}
        distortionScale={0.3}
        temporalDistortion={0.5}
        clearcoat={1}
        attenuationDistance={0.5}
        attenuationColor="#ffffff"
        color="#c9ffa1"
      />
    </mesh>
  )
}
```

### MeshDiscardMaterial

Discard fragments - useful for shadows only.

```tsx
import { MeshDiscardMaterial } from '@react-three/drei'

function ShadowOnlyMesh() {
  return (
    <mesh castShadow>
      <boxGeometry />
      <MeshDiscardMaterial />  {/* Invisible but casts shadows */}
    </mesh>
  )
}
```

## Points and Lines Materials

```tsx
// Points material
<points>
  <bufferGeometry />
  <pointsMaterial
    size={0.1}
    sizeAttenuation={true}
    color="white"
    map={spriteTexture}
    transparent
    alphaTest={0.5}
    vertexColors
  />
</points>

// Line materials
<line>
  <bufferGeometry />
  <lineBasicMaterial color="white" linewidth={1} />
</line>

<line>
  <bufferGeometry />
  <lineDashedMaterial
    color="white"
    dashSize={0.5}
    gapSize={0.25}
    scale={1}
  />
</line>
```

## Common Material Properties

All materials share these base properties:

```tsx
<meshStandardMaterial
  // Visibility
  visible={true}
  transparent={false}
  opacity={1}
  alphaTest={0}          // Discard pixels with alpha < value

  // Rendering
  side={THREE.FrontSide} // FrontSide, BackSide, DoubleSide
  depthTest={true}
  depthWrite={true}
  colorWrite={true}

  // Blending
  blending={THREE.NormalBlending}
  // NormalBlending, AdditiveBlending, SubtractiveBlending, MultiplyBlending

  // Polygon offset (z-fighting fix)
  polygonOffset={false}
  polygonOffsetFactor={0}
  polygonOffsetUnits={0}

  // Misc
  dithering={false}
  toneMapped={true}
/>
```

## Dynamic Materials

### Updating Material Properties

```tsx
import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'

function AnimatedMaterial() {
  const materialRef = useRef()

  useFrame(({ clock }) => {
    const t = clock.elapsedTime

    // Update color
    materialRef.current.color.setHSL((t * 0.1) % 1, 1, 0.5)

    // Update properties
    materialRef.current.roughness = (Math.sin(t) + 1) / 2
  })

  return (
    <mesh>
      <boxGeometry />
      <meshStandardMaterial ref={materialRef} />
    </mesh>
  )
}
```

### Shared Materials

```tsx
import { useMemo } from 'react'
import * as THREE from 'three'

function SharedMaterial() {
  // Create once, use many times
  const material = useMemo(() =>
    new THREE.MeshStandardMaterial({ color: 'red' }),
  [])

  return (
    <>
      <mesh position={[-2, 0, 0]} material={material}>
        <boxGeometry />
      </mesh>
      <mesh position={[0, 0, 0]} material={material}>
        <sphereGeometry />
      </mesh>
      <mesh position={[2, 0, 0]} material={material}>
        <coneGeometry />
      </mesh>
    </>
  )
}
```

## Multiple Materials

```tsx
// Different materials per face (BoxGeometry has 6 material groups)
<mesh>
  <boxGeometry />
  <meshStandardMaterial attach="material-0" color="red" />   {/* +X */}
  <meshStandardMaterial attach="material-1" color="green" /> {/* -X */}
  <meshStandardMaterial attach="material-2" color="blue" />  {/* +Y */}
  <meshStandardMaterial attach="material-3" color="yellow" />{/* -Y */}
  <meshStandardMaterial attach="material-4" color="cyan" />  {/* +Z */}
  <meshStandardMaterial attach="material-5" color="magenta" />{/* -Z */}
</mesh>
```

## Material with Textures

```tsx
import { useTexture } from '@react-three/drei'
import * as THREE from 'three'

function TexturedMaterial() {
  // Named object pattern (recommended)
  const textures = useTexture({
    map: '/textures/color.jpg',
    normalMap: '/textures/normal.jpg',
    roughnessMap: '/textures/roughness.jpg',
  })

  // Set texture properties
  Object.values(textures).forEach(texture => {
    texture.wrapS = texture.wrapT = THREE.RepeatWrapping
    texture.repeat.set(2, 2)
  })

  return (
    <mesh>
      <planeGeometry args={[5, 5]} />
      <meshStandardMaterial {...textures} />
    </mesh>
  )
}
```

## Emissive Materials (Glow)

```tsx
// For bloom effect, emissive colors should exceed normal range
<meshStandardMaterial
  color="black"
  emissive="#ff0000"
  emissiveIntensity={2}    // > 1 for bloom
  toneMapped={false}       // Required for colors > 1
/>

// With emissive map
<meshStandardMaterial
  emissive="white"
  emissiveMap={emissiveTexture}
  emissiveIntensity={2}
  toneMapped={false}
/>
```

## Environment Maps

```tsx
import { useEnvironment } from '@react-three/drei'

function EnvMappedMaterial() {
  const envMap = useEnvironment({ preset: 'sunset' })

  return (
    <mesh>
      <sphereGeometry args={[1, 64, 64]} />
      <meshStandardMaterial
        metalness={1}
        roughness={0}
        envMap={envMap}
        envMapIntensity={1}
      />
    </mesh>
  )
}
```

## Custom Shader Materials

See `r3f-shaders` for detailed shader material usage.

```tsx
import { shaderMaterial } from '@react-three/drei'
import { extend } from '@react-three/fiber'

const CustomMaterial = shaderMaterial(
  { time: 0, color: new THREE.Color('hotpink') },
  // Vertex shader
  `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  // Fragment shader
  `
    uniform float time;
    uniform vec3 color;
    varying vec2 vUv;
    void main() {
      gl_FragColor = vec4(color * (sin(time + vUv.x * 10.0) * 0.5 + 0.5), 1.0);
    }
  `
)

extend({ CustomMaterial })

function CustomShaderMesh() {
  const materialRef = useRef()

  useFrame(({ clock }) => {
    materialRef.current.time = clock.elapsedTime
  })

  return (
    <mesh>
      <boxGeometry />
      <customMaterial ref={materialRef} />
    </mesh>
  )
}
```

## Performance Tips

1. **Reuse materials**: Same material instance = batched draw calls
2. **Avoid transparent**: Requires sorting, slower
3. **Use alphaTest over transparent**: When possible, faster
4. **Simpler materials**: Basic > Lambert > Phong > Standard > Physical
5. **Limit texture sizes**: 1024-2048 usually sufficient

```tsx
// Material caching pattern
const materialCache = new Map()

function getCachedMaterial(color) {
  const key = color.toString()
  if (!materialCache.has(key)) {
    materialCache.set(key, new THREE.MeshStandardMaterial({ color }))
  }
  return materialCache.get(key)
}
```

## See Also

- `r3f-textures` - Texture loading and configuration
- `r3f-shaders` - Custom shader development
- `r3f-lighting` - Light interaction with materials
