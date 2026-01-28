---
name: r3f-textures
description: React Three Fiber textures - useTexture, texture loading, environment maps, texture configuration. Use when loading images, working with PBR texture sets, cubemaps, HDR environments, or optimizing texture usage.
---

# React Three Fiber Textures

## Quick Start

```tsx
import { Canvas } from '@react-three/fiber'
import { useTexture } from '@react-three/drei'

function TexturedBox() {
  const texture = useTexture('/textures/wood.jpg')

  return (
    <mesh>
      <boxGeometry />
      <meshStandardMaterial map={texture} />
    </mesh>
  )
}

export default function App() {
  return (
    <Canvas>
      <ambientLight />
      <TexturedBox />
    </Canvas>
  )
}
```

## useTexture Hook (Drei)

The recommended way to load textures in R3F.

### Single Texture

```tsx
import { useTexture } from '@react-three/drei'

function SingleTexture() {
  const texture = useTexture('/textures/color.jpg')

  return (
    <mesh>
      <planeGeometry args={[5, 5]} />
      <meshBasicMaterial map={texture} />
    </mesh>
  )
}
```

### Multiple Textures (Array)

```tsx
function MultipleTextures() {
  const [colorMap, normalMap, roughnessMap] = useTexture([
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

### Named Object (Recommended for PBR)

```tsx
function PBRTextures() {
  // Named object automatically spreads to material
  const textures = useTexture({
    map: '/textures/color.jpg',
    normalMap: '/textures/normal.jpg',
    roughnessMap: '/textures/roughness.jpg',
    metalnessMap: '/textures/metalness.jpg',
    aoMap: '/textures/ao.jpg',
    displacementMap: '/textures/displacement.jpg',
  })

  return (
    <mesh>
      <sphereGeometry args={[1, 64, 64]} />
      <meshStandardMaterial
        {...textures}
        displacementScale={0.1}
      />
    </mesh>
  )
}
```

### With Texture Configuration

```tsx
import { useTexture } from '@react-three/drei'
import * as THREE from 'three'

function ConfiguredTextures() {
  const textures = useTexture({
    map: '/textures/color.jpg',
    normalMap: '/textures/normal.jpg',
  }, (textures) => {
    // Configure textures after loading
    Object.values(textures).forEach(texture => {
      texture.wrapS = texture.wrapT = THREE.RepeatWrapping
      texture.repeat.set(4, 4)
    })
  })

  return (
    <mesh>
      <planeGeometry args={[10, 10]} />
      <meshStandardMaterial {...textures} />
    </mesh>
  )
}
```

### Preloading

```tsx
import { useTexture } from '@react-three/drei'

// Preload at module level
useTexture.preload('/textures/hero.jpg')
useTexture.preload(['/tex1.jpg', '/tex2.jpg'])

function Component() {
  // Will be instant if preloaded
  const texture = useTexture('/textures/hero.jpg')
}
```

## useLoader (Core R3F)

For more control over loading.

```tsx
import { useLoader } from '@react-three/fiber'
import { TextureLoader } from 'three'

function WithUseLoader() {
  const texture = useLoader(TextureLoader, '/textures/color.jpg')

  // Multiple textures
  const [color, normal] = useLoader(TextureLoader, [
    '/textures/color.jpg',
    '/textures/normal.jpg',
  ])

  return (
    <mesh>
      <boxGeometry />
      <meshStandardMaterial map={color} normalMap={normal} />
    </mesh>
  )
}

// Preload
useLoader.preload(TextureLoader, '/textures/color.jpg')
```

## Texture Configuration

### Wrapping Modes

```tsx
import * as THREE from 'three'

function ConfigureWrapping() {
  const texture = useTexture('/textures/tile.jpg', (tex) => {
    // Wrapping
    tex.wrapS = THREE.RepeatWrapping      // Horizontal: ClampToEdgeWrapping, RepeatWrapping, MirroredRepeatWrapping
    tex.wrapT = THREE.RepeatWrapping      // Vertical

    // Repeat
    tex.repeat.set(4, 4)                  // Tile 4x4

    // Offset
    tex.offset.set(0.5, 0.5)              // Shift UV

    // Rotation
    tex.rotation = Math.PI / 4            // Rotate 45 degrees
    tex.center.set(0.5, 0.5)              // Rotation pivot
  })

  return (
    <mesh>
      <planeGeometry args={[10, 10]} />
      <meshStandardMaterial map={texture} />
    </mesh>
  )
}
```

### Filtering

```tsx
function ConfigureFiltering() {
  const texture = useTexture('/textures/color.jpg', (tex) => {
    // Minification (texture larger than screen pixels)
    tex.minFilter = THREE.LinearMipmapLinearFilter  // Smooth with mipmaps (default)
    tex.minFilter = THREE.NearestFilter             // Pixelated
    tex.minFilter = THREE.LinearFilter              // Smooth, no mipmaps

    // Magnification (texture smaller than screen pixels)
    tex.magFilter = THREE.LinearFilter   // Smooth (default)
    tex.magFilter = THREE.NearestFilter  // Pixelated (retro style)

    // Anisotropic filtering (sharper at angles)
    tex.anisotropy = 16  // Usually renderer.capabilities.getMaxAnisotropy()

    // Generate mipmaps
    tex.generateMipmaps = true  // Default
  })
}
```

### Color Space

Important for accurate colors.

```tsx
function ConfigureColorSpace() {
  const [colorMap, normalMap, roughnessMap] = useTexture([
    '/textures/color.jpg',
    '/textures/normal.jpg',
    '/textures/roughness.jpg',
  ], (textures) => {
    // Color/albedo textures should use sRGB
    textures[0].colorSpace = THREE.SRGBColorSpace

    // Data textures (normal, roughness, metalness, ao) use Linear
    // This is the default, so usually no action needed
    // textures[1].colorSpace = THREE.LinearSRGBColorSpace
    // textures[2].colorSpace = THREE.LinearSRGBColorSpace
  })
}
```

## Environment Maps

### useEnvironment Hook

```tsx
import { useEnvironment, Environment } from '@react-three/drei'

// Use as texture
function EnvMappedSphere() {
  const envMap = useEnvironment({ preset: 'sunset' })

  return (
    <mesh>
      <sphereGeometry args={[1, 64, 64]} />
      <meshStandardMaterial
        metalness={1}
        roughness={0}
        envMap={envMap}
      />
    </mesh>
  )
}

// Or use Environment component for scene-wide
function Scene() {
  return (
    <>
      <Environment preset="sunset" background />
      <Mesh />
    </>
  )
}
```

### HDR Environment

```tsx
import { useEnvironment } from '@react-three/drei'

function HDREnvironment() {
  const envMap = useEnvironment({ files: '/hdri/studio.hdr' })

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

### Cube Map

```tsx
import { useCubeTexture } from '@react-three/drei'

function CubeMapTexture() {
  const envMap = useCubeTexture(
    ['px.jpg', 'nx.jpg', 'py.jpg', 'ny.jpg', 'pz.jpg', 'nz.jpg'],
    { path: '/textures/cube/' }
  )

  return (
    <mesh>
      <sphereGeometry args={[1, 64, 64]} />
      <meshStandardMaterial envMap={envMap} metalness={1} roughness={0} />
    </mesh>
  )
}
```

## Video Textures

```tsx
import { useVideoTexture } from '@react-three/drei'

function VideoPlane() {
  const texture = useVideoTexture('/videos/sample.mp4', {
    start: true,
    loop: true,
    muted: true,
  })

  return (
    <mesh>
      <planeGeometry args={[16, 9].map(x => x * 0.5)} />
      <meshBasicMaterial map={texture} toneMapped={false} />
    </mesh>
  )
}
```

## Canvas Textures

```tsx
import { useRef, useEffect } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

function CanvasTexture() {
  const meshRef = useRef()
  const textureRef = useRef()

  useEffect(() => {
    const canvas = document.createElement('canvas')
    canvas.width = 256
    canvas.height = 256
    const ctx = canvas.getContext('2d')

    // Draw on canvas
    ctx.fillStyle = 'red'
    ctx.fillRect(0, 0, 256, 256)
    ctx.fillStyle = 'white'
    ctx.font = '48px Arial'
    ctx.fillText('Hello', 50, 150)

    textureRef.current = new THREE.CanvasTexture(canvas)
  }, [])

  // Update texture dynamically
  useFrame(({ clock }) => {
    if (textureRef.current) {
      const canvas = textureRef.current.image
      const ctx = canvas.getContext('2d')
      ctx.fillStyle = `hsl(${clock.elapsedTime * 50}, 100%, 50%)`
      ctx.fillRect(0, 0, 256, 256)
      textureRef.current.needsUpdate = true
    }
  })

  return (
    <mesh ref={meshRef}>
      <planeGeometry args={[2, 2]} />
      <meshBasicMaterial map={textureRef.current} />
    </mesh>
  )
}
```

## Data Textures

```tsx
import { useMemo } from 'react'
import * as THREE from 'three'

function NoiseTexture() {
  const texture = useMemo(() => {
    const size = 256
    const data = new Uint8Array(size * size * 4)

    for (let i = 0; i < size * size; i++) {
      const value = Math.random() * 255
      data[i * 4] = value
      data[i * 4 + 1] = value
      data[i * 4 + 2] = value
      data[i * 4 + 3] = 255
    }

    const texture = new THREE.DataTexture(data, size, size)
    texture.needsUpdate = true
    return texture
  }, [])

  return (
    <mesh>
      <planeGeometry args={[2, 2]} />
      <meshBasicMaterial map={texture} />
    </mesh>
  )
}
```

## Render Targets

Render to texture.

```tsx
import { useFBO } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'
import { useRef } from 'react'

function RenderToTexture() {
  const fbo = useFBO(512, 512)
  const meshRef = useRef()
  const otherSceneRef = useRef()

  useFrame(({ gl, camera }) => {
    // Render other scene to FBO
    gl.setRenderTarget(fbo)
    gl.render(otherSceneRef.current, camera)
    gl.setRenderTarget(null)
  })

  return (
    <>
      {/* Scene to render to texture */}
      <group ref={otherSceneRef}>
        <mesh position={[0, 0, -5]}>
          <sphereGeometry args={[1, 32, 32]} />
          <meshStandardMaterial color="red" />
        </mesh>
      </group>

      {/* Display the texture */}
      <mesh ref={meshRef}>
        <planeGeometry args={[4, 4]} />
        <meshBasicMaterial map={fbo.texture} />
      </mesh>
    </>
  )
}
```

## Texture Atlas / Sprite Sheet

```tsx
import { useTexture } from '@react-three/drei'
import { useState } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

function SpriteAnimation() {
  const texture = useTexture('/textures/spritesheet.png')
  const [frame, setFrame] = useState(0)

  // Configure texture
  texture.wrapS = texture.wrapT = THREE.ClampToEdgeWrapping
  texture.repeat.set(1/4, 1/4)  // 4x4 sprite sheet

  useFrame(({ clock }) => {
    const newFrame = Math.floor(clock.elapsedTime * 10) % 16
    if (newFrame !== frame) {
      setFrame(newFrame)
      const col = newFrame % 4
      const row = Math.floor(newFrame / 4)
      texture.offset.set(col / 4, 1 - (row + 1) / 4)
    }
  })

  return (
    <mesh>
      <planeGeometry args={[1, 1]} />
      <meshBasicMaterial map={texture} transparent />
    </mesh>
  )
}
```

## Material Texture Maps Reference

```tsx
<meshStandardMaterial
  // Base color (sRGB)
  map={colorTexture}

  // Surface detail (Linear)
  normalMap={normalTexture}
  normalScale={[1, 1]}

  // Roughness (Linear, grayscale)
  roughnessMap={roughnessTexture}
  roughness={1}  // Multiplier

  // Metalness (Linear, grayscale)
  metalnessMap={metalnessTexture}
  metalness={1}  // Multiplier

  // Ambient Occlusion (Linear, requires uv2)
  aoMap={aoTexture}
  aoMapIntensity={1}

  // Self-illumination (sRGB)
  emissiveMap={emissiveTexture}
  emissive="#ffffff"
  emissiveIntensity={1}

  // Vertex displacement (Linear)
  displacementMap={displacementTexture}
  displacementScale={0.1}
  displacementBias={0}

  // Alpha (Linear)
  alphaMap={alphaTexture}
  transparent={true}

  // Environment reflection
  envMap={envTexture}
  envMapIntensity={1}

  // Lightmap (requires uv2)
  lightMap={lightmapTexture}
  lightMapIntensity={1}
/>
```

## Second UV Channel (for AO/Lightmaps)

```tsx
import { useEffect, useRef } from 'react'

function MeshWithUV2() {
  const meshRef = useRef()

  useEffect(() => {
    // Copy uv to uv2 for aoMap/lightMap
    const geometry = meshRef.current.geometry
    geometry.setAttribute('uv2', geometry.attributes.uv)
  }, [])

  return (
    <mesh ref={meshRef}>
      <boxGeometry />
      <meshStandardMaterial
        aoMap={aoTexture}
        aoMapIntensity={1}
      />
    </mesh>
  )
}
```

## Suspense Loading

```tsx
import { Suspense } from 'react'
import { useTexture } from '@react-three/drei'

function TexturedMesh() {
  const texture = useTexture('/textures/large.jpg')
  return (
    <mesh>
      <boxGeometry />
      <meshStandardMaterial map={texture} />
    </mesh>
  )
}

function Fallback() {
  return (
    <mesh>
      <boxGeometry />
      <meshBasicMaterial color="gray" wireframe />
    </mesh>
  )
}

function Scene() {
  return (
    <Suspense fallback={<Fallback />}>
      <TexturedMesh />
    </Suspense>
  )
}
```

## Performance Tips

1. **Use power-of-2 dimensions**: 256, 512, 1024, 2048
2. **Compress textures**: Use KTX2/Basis for web
3. **Enable mipmaps**: For distant objects
4. **Limit texture size**: 2048 usually sufficient
5. **Reuse textures**: Same texture = better batching
6. **Preload important textures**: Avoid pop-in

```tsx
// Preload critical textures
useTexture.preload('/textures/hero.jpg')

// Check texture memory
useFrame(({ gl }) => {
  console.log('Textures:', gl.info.memory.textures)
})

// Dispose unused textures (R3F usually handles this)
texture.dispose()
```

## See Also

- `r3f-materials` - Applying textures to materials
- `r3f-loaders` - Asset loading patterns
- `r3f-shaders` - Custom texture sampling
