---
name: r3f-shaders
description: React Three Fiber shaders - GLSL, shaderMaterial, uniforms, custom effects. Use when creating custom visual effects, modifying vertices, writing fragment shaders, or extending built-in materials.
---

# React Three Fiber Shaders

## Quick Start

```tsx
import { Canvas, useFrame, extend } from '@react-three/fiber'
import { shaderMaterial } from '@react-three/drei'
import { useRef } from 'react'
import * as THREE from 'three'

// Create custom shader material
const ColorShiftMaterial = shaderMaterial(
  // Uniforms
  { time: 0, color: new THREE.Color(0.2, 0.0, 0.1) },
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
      gl_FragColor = vec4(vUv.x + sin(time), vUv.y + cos(time), color.b, 1.0);
    }
  `
)

// Extend so it can be used as JSX
extend({ ColorShiftMaterial })

function ShaderMesh() {
  const materialRef = useRef()

  useFrame(({ clock }) => {
    materialRef.current.time = clock.elapsedTime
  })

  return (
    <mesh>
      <planeGeometry args={[2, 2]} />
      {/* key={Material.key} enables HMR for shader development */}
      <colorShiftMaterial ref={materialRef} key={ColorShiftMaterial.key} />
    </mesh>
  )
}

export default function App() {
  return (
    <Canvas>
      <ShaderMesh />
    </Canvas>
  )
}
```

## shaderMaterial (Drei)

The recommended way to create shader materials in R3F.

### Basic Pattern

```tsx
import { shaderMaterial } from '@react-three/drei'
import { extend } from '@react-three/fiber'
import * as THREE from 'three'

// 1. Define the material
const MyShaderMaterial = shaderMaterial(
  // Uniforms object
  {
    time: 0,
    color: new THREE.Color(1, 0, 0),
    opacity: 1,
    map: null,
  },
  // Vertex shader (GLSL)
  `
    varying vec2 vUv;
    varying vec3 vPosition;

    void main() {
      vUv = uv;
      vPosition = position;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  // Fragment shader (GLSL)
  `
    uniform float time;
    uniform vec3 color;
    uniform float opacity;
    uniform sampler2D map;
    varying vec2 vUv;

    void main() {
      vec4 texColor = texture2D(map, vUv);
      gl_FragColor = vec4(color * texColor.rgb, opacity);
    }
  `
)

// 2. Extend R3F
extend({ MyShaderMaterial })

// 3. Use in component
function MyMesh() {
  const materialRef = useRef()

  useFrame(({ clock }) => {
    materialRef.current.time = clock.elapsedTime
  })

  return (
    <mesh>
      <boxGeometry />
      {/* key prop enables Hot Module Replacement during development */}
      <myShaderMaterial
        ref={materialRef}
        key={MyShaderMaterial.key}
        color="hotpink"
        transparent
        opacity={0.8}
      />
    </mesh>
  )
}
```

### Hot Module Replacement (HMR)

The `key` prop on shaderMaterial enables live shader editing without page refresh:

```tsx
const MyMaterial = shaderMaterial(
  { time: 0 },
  vertexShader,
  fragmentShader
)

extend({ MyMaterial })

// MyMaterial.key changes when shader code changes
<myMaterial key={MyMaterial.key} />
```

When you edit shader code, the material automatically updates. Without `key`, you'd need to refresh the page to see changes.

### TypeScript Support

```tsx
import { shaderMaterial } from '@react-three/drei'
import { extend, Object3DNode } from '@react-three/fiber'
import * as THREE from 'three'

// Define uniform types
type WaveMaterialUniforms = {
  time: number
  amplitude: number
  color: THREE.Color
}

const WaveMaterial = shaderMaterial(
  {
    time: 0,
    amplitude: 0.5,
    color: new THREE.Color('hotpink'),
  } as WaveMaterialUniforms,
  // vertex shader
  `...`,
  // fragment shader
  `...`
)

// Extend with proper types
extend({ WaveMaterial })

// Declare for TypeScript
declare module '@react-three/fiber' {
  interface ThreeElements {
    waveMaterial: Object3DNode<
      typeof WaveMaterial & THREE.ShaderMaterial,
      typeof WaveMaterial
    >
  }
}
```

## Raw THREE.ShaderMaterial

For full control without Drei helper.

```tsx
import { useFrame } from '@react-three/fiber'
import { useMemo, useRef } from 'react'
import * as THREE from 'three'

function CustomShaderMesh() {
  const materialRef = useRef()

  const shaderMaterial = useMemo(() => {
    return new THREE.ShaderMaterial({
      uniforms: {
        time: { value: 0 },
        color: { value: new THREE.Color('cyan') },
        resolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) },
      },
      vertexShader: `
        varying vec2 vUv;
        void main() {
          vUv = uv;
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
      `,
      fragmentShader: `
        uniform float time;
        uniform vec3 color;
        uniform vec2 resolution;
        varying vec2 vUv;

        void main() {
          vec2 st = gl_FragCoord.xy / resolution;
          float pattern = sin(st.x * 20.0 + time) * sin(st.y * 20.0 + time);
          gl_FragColor = vec4(color * pattern, 1.0);
        }
      `,
      side: THREE.DoubleSide,
      transparent: true,
    })
  }, [])

  useFrame(({ clock }) => {
    shaderMaterial.uniforms.time.value = clock.elapsedTime
  })

  return (
    <mesh material={shaderMaterial}>
      <planeGeometry args={[4, 4, 32, 32]} />
    </mesh>
  )
}
```

## Uniforms

### Common Uniform Types

```tsx
const MyMaterial = shaderMaterial(
  {
    // Numbers
    time: 0,
    intensity: 1.5,

    // Vectors
    resolution: new THREE.Vector2(1920, 1080),
    lightPosition: new THREE.Vector3(5, 10, 5),
    bounds: new THREE.Vector4(0, 0, 1, 1),

    // Color (becomes vec3)
    color: new THREE.Color('#ff0000'),

    // Matrices
    customMatrix: new THREE.Matrix4(),

    // Textures
    map: null,        // sampler2D
    cubeMap: null,    // samplerCube

    // Arrays
    positions: [new THREE.Vector3(), new THREE.Vector3(), new THREE.Vector3()],
  },
  vertexShader,
  fragmentShader
)
```

### GLSL Declarations

```glsl
// In shader code
uniform float time;
uniform float intensity;
uniform vec2 resolution;
uniform vec3 lightPosition;
uniform vec3 color;  // THREE.Color becomes vec3
uniform vec4 bounds;
uniform mat4 customMatrix;
uniform sampler2D map;
uniform samplerCube cubeMap;
uniform vec3 positions[3];
```

### Updating Uniforms

```tsx
function AnimatedShader() {
  const materialRef = useRef()

  useFrame(({ clock, mouse, viewport }) => {
    // Direct value update
    materialRef.current.time = clock.elapsedTime

    // Vector update
    materialRef.current.resolution.set(viewport.width, viewport.height)

    // Color update
    materialRef.current.color.setHSL((clock.elapsedTime * 0.1) % 1, 1, 0.5)

    // Or via uniforms object (for THREE.ShaderMaterial)
    // materialRef.current.uniforms.time.value = clock.elapsedTime
  })

  return (
    <mesh>
      <boxGeometry />
      <myShaderMaterial ref={materialRef} />
    </mesh>
  )
}
```

## Varyings

Pass data from vertex to fragment shader.

```glsl
// Vertex shader
varying vec2 vUv;
varying vec3 vNormal;
varying vec3 vPosition;
varying vec3 vWorldPosition;

void main() {
  vUv = uv;
  vNormal = normalize(normalMatrix * normal);
  vPosition = position;
  vWorldPosition = (modelMatrix * vec4(position, 1.0)).xyz;

  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}

// Fragment shader
varying vec2 vUv;
varying vec3 vNormal;
varying vec3 vPosition;
varying vec3 vWorldPosition;

void main() {
  // Use interpolated values
  gl_FragColor = vec4(vNormal * 0.5 + 0.5, 1.0);
}
```

## Common Shader Patterns

### Texture Sampling

```tsx
import { useTexture } from '@react-three/drei'

function TexturedShaderMesh() {
  const texture = useTexture('/textures/color.jpg')
  const materialRef = useRef()

  return (
    <mesh>
      <planeGeometry args={[2, 2]} />
      <myShaderMaterial ref={materialRef} map={texture} />
    </mesh>
  )
}

// Shader
const TextureMaterial = shaderMaterial(
  { map: null },
  `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  `
    uniform sampler2D map;
    varying vec2 vUv;

    void main() {
      vec4 texColor = texture2D(map, vUv);
      gl_FragColor = texColor;
    }
  `
)
```

### Vertex Displacement

```tsx
const WaveMaterial = shaderMaterial(
  { time: 0, amplitude: 0.5, frequency: 2.0 },
  `
    uniform float time;
    uniform float amplitude;
    uniform float frequency;
    varying vec2 vUv;

    void main() {
      vUv = uv;
      vec3 pos = position;

      // Wave displacement
      pos.z += sin(pos.x * frequency + time) * amplitude;
      pos.z += sin(pos.y * frequency + time) * amplitude;

      gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
    }
  `,
  `
    varying vec2 vUv;
    void main() {
      gl_FragColor = vec4(vUv, 1.0, 1.0);
    }
  `
)

extend({ WaveMaterial })

function WavePlane() {
  const ref = useRef()

  useFrame(({ clock }) => {
    ref.current.time = clock.elapsedTime
  })

  return (
    <mesh rotation={[-Math.PI / 2, 0, 0]}>
      <planeGeometry args={[10, 10, 64, 64]} />
      <waveMaterial ref={ref} />
    </mesh>
  )
}
```

### Fresnel Effect

```tsx
const FresnelMaterial = shaderMaterial(
  { fresnelColor: new THREE.Color('cyan'), baseColor: new THREE.Color('navy') },
  `
    varying vec3 vNormal;
    varying vec3 vWorldPosition;

    void main() {
      vNormal = normalize(normalMatrix * normal);
      vWorldPosition = (modelMatrix * vec4(position, 1.0)).xyz;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  `
    uniform vec3 fresnelColor;
    uniform vec3 baseColor;
    varying vec3 vNormal;
    varying vec3 vWorldPosition;

    void main() {
      vec3 viewDirection = normalize(cameraPosition - vWorldPosition);
      float fresnel = pow(1.0 - dot(viewDirection, vNormal), 3.0);

      gl_FragColor = vec4(mix(baseColor, fresnelColor, fresnel), 1.0);
    }
  `
)
```

### Noise Functions

```glsl
// Simple random
float random(vec2 st) {
  return fract(sin(dot(st.xy, vec2(12.9898, 78.233))) * 43758.5453);
}

// Value noise
float noise(vec2 st) {
  vec2 i = floor(st);
  vec2 f = fract(st);

  float a = random(i);
  float b = random(i + vec2(1.0, 0.0));
  float c = random(i + vec2(0.0, 1.0));
  float d = random(i + vec2(1.0, 1.0));

  vec2 u = f * f * (3.0 - 2.0 * f);

  return mix(a, b, u.x) + (c - a) * u.y * (1.0 - u.x) + (d - b) * u.x * u.y;
}

// FBM (Fractal Brownian Motion)
float fbm(vec2 st) {
  float value = 0.0;
  float amplitude = 0.5;

  for (int i = 0; i < 5; i++) {
    value += amplitude * noise(st);
    st *= 2.0;
    amplitude *= 0.5;
  }

  return value;
}
```

### Gradient

```glsl
// Linear gradient
vec3 gradient = mix(colorA, colorB, vUv.y);

// Radial gradient
float dist = distance(vUv, vec2(0.5));
vec3 radial = mix(centerColor, edgeColor, dist * 2.0);

// Smooth gradient
float t = smoothstep(0.0, 1.0, vUv.y);
vec3 smooth = mix(colorA, colorB, t);
```

### Dissolve Effect

```tsx
const DissolveMaterial = shaderMaterial(
  { progress: 0, noiseScale: 10.0, edgeColor: new THREE.Color('orange') },
  `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  `
    uniform float progress;
    uniform float noiseScale;
    uniform vec3 edgeColor;
    varying vec2 vUv;

    float random(vec2 st) {
      return fract(sin(dot(st.xy, vec2(12.9898, 78.233))) * 43758.5453);
    }

    float noise(vec2 st) {
      vec2 i = floor(st);
      vec2 f = fract(st);
      float a = random(i);
      float b = random(i + vec2(1.0, 0.0));
      float c = random(i + vec2(0.0, 1.0));
      float d = random(i + vec2(1.0, 1.0));
      vec2 u = f * f * (3.0 - 2.0 * f);
      return mix(a, b, u.x) + (c - a) * u.y * (1.0 - u.x) + (d - b) * u.x * u.y;
    }

    void main() {
      float n = noise(vUv * noiseScale);

      if (n < progress) {
        discard;
      }

      float edge = smoothstep(progress, progress + 0.1, n);
      vec3 baseColor = vec3(0.5);

      gl_FragColor = vec4(mix(edgeColor, baseColor, edge), 1.0);
    }
  `
)
```

## Extending Built-in Materials

### onBeforeCompile

Modify existing material shaders.

```tsx
import { useRef, useEffect } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

function ModifiedStandardMaterial() {
  const materialRef = useRef()
  const shaderRef = useRef()

  useEffect(() => {
    if (materialRef.current) {
      materialRef.current.onBeforeCompile = (shader) => {
        // Add custom uniform
        shader.uniforms.time = { value: 0 }
        shaderRef.current = shader

        // Add uniform declaration
        shader.vertexShader = 'uniform float time;\n' + shader.vertexShader

        // Modify vertex shader
        shader.vertexShader = shader.vertexShader.replace(
          '#include <begin_vertex>',
          `
            #include <begin_vertex>
            transformed.y += sin(position.x * 10.0 + time) * 0.1;
          `
        )
      }
    }
  }, [])

  useFrame(({ clock }) => {
    if (shaderRef.current) {
      shaderRef.current.uniforms.time.value = clock.elapsedTime
    }
  })

  return (
    <mesh>
      <planeGeometry args={[5, 5, 32, 32]} />
      <meshStandardMaterial ref={materialRef} color="green" />
    </mesh>
  )
}
```

### Common Injection Points

```javascript
// Vertex shader chunks
'#include <begin_vertex>'       // After position is calculated
'#include <project_vertex>'     // After gl_Position
'#include <beginnormal_vertex>' // Normal calculation start

// Fragment shader chunks
'#include <color_fragment>'     // After diffuse color
'#include <output_fragment>'    // Final output
'#include <fog_fragment>'       // After fog applied
```

## GLSL Built-in Functions

### Math Functions

```glsl
// Basic
abs(x), sign(x), floor(x), ceil(x), fract(x)
mod(x, y), min(x, y), max(x, y), clamp(x, min, max)
mix(a, b, t), step(edge, x), smoothstep(edge0, edge1, x)

// Trigonometry
sin(x), cos(x), tan(x)
asin(x), acos(x), atan(y, x), atan(x)

// Exponential
pow(x, y), exp(x), log(x), sqrt(x)
```

### Vector Functions

```glsl
length(v), distance(p0, p1), dot(x, y), cross(x, y)
normalize(v), reflect(I, N), refract(I, N, eta)
```

## Instanced Shaders

```tsx
import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

function InstancedShaderMesh({ count = 1000 }) {
  const meshRef = useRef()

  // Create instance attributes
  const { offsets, colors } = useMemo(() => {
    const offsets = new Float32Array(count * 3)
    const colors = new Float32Array(count * 3)

    for (let i = 0; i < count; i++) {
      offsets[i * 3] = (Math.random() - 0.5) * 20
      offsets[i * 3 + 1] = (Math.random() - 0.5) * 20
      offsets[i * 3 + 2] = (Math.random() - 0.5) * 20

      colors[i * 3] = Math.random()
      colors[i * 3 + 1] = Math.random()
      colors[i * 3 + 2] = Math.random()
    }

    return { offsets, colors }
  }, [count])

  const shaderMaterial = useMemo(() => {
    return new THREE.ShaderMaterial({
      uniforms: {
        time: { value: 0 }
      },
      vertexShader: `
        attribute vec3 offset;
        attribute vec3 instanceColor;
        varying vec3 vColor;

        void main() {
          vColor = instanceColor;
          vec3 pos = position + offset;
          gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
        }
      `,
      fragmentShader: `
        varying vec3 vColor;

        void main() {
          gl_FragColor = vec4(vColor, 1.0);
        }
      `
    })
  }, [])

  useFrame(({ clock }) => {
    shaderMaterial.uniforms.time.value = clock.elapsedTime
  })

  return (
    <instancedMesh ref={meshRef} args={[null, null, count]} material={shaderMaterial}>
      <boxGeometry args={[0.5, 0.5, 0.5]}>
        <instancedBufferAttribute attach="attributes-offset" args={[offsets, 3]} />
        <instancedBufferAttribute attach="attributes-instanceColor" args={[colors, 3]} />
      </boxGeometry>
    </instancedMesh>
  )
}
```

## External Shader Files

### With Vite/Webpack

```tsx
// shaders/vertex.glsl
varying vec2 vUv;
void main() {
  vUv = uv;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}

// shaders/fragment.glsl
uniform float time;
varying vec2 vUv;
void main() {
  gl_FragColor = vec4(vUv, sin(time), 1.0);
}

// Component.tsx
import vertexShader from './shaders/vertex.glsl?raw'
import fragmentShader from './shaders/fragment.glsl?raw'

const MyMaterial = shaderMaterial(
  { time: 0 },
  vertexShader,
  fragmentShader
)
```

### Vite Config for GLSL

```javascript
// vite.config.js
import glsl from 'vite-plugin-glsl'

export default {
  plugins: [glsl()]
}
```

## Material Properties

```tsx
<myShaderMaterial
  // Rendering
  transparent={true}
  opacity={1.0}
  side={THREE.DoubleSide}
  depthTest={true}
  depthWrite={true}

  // Blending
  blending={THREE.NormalBlending}
  // NormalBlending, AdditiveBlending, SubtractiveBlending, MultiplyBlending

  // Wireframe
  wireframe={false}

  // Custom uniforms
  time={0}
  color="hotpink"
/>
```

## Debugging Shaders

```tsx
function DebugShaderMesh() {
  const materialRef = useRef()

  useEffect(() => {
    // Log compiled shaders
    if (materialRef.current) {
      console.log('Vertex:', materialRef.current.vertexShader)
      console.log('Fragment:', materialRef.current.fragmentShader)
    }
  }, [])

  return (
    <mesh>
      <boxGeometry />
      {/* Debug with visual output */}
      <shaderMaterial
        ref={materialRef}
        fragmentShader={`
          varying vec2 vUv;
          void main() {
            // Debug UV
            gl_FragColor = vec4(vUv, 0.0, 1.0);

            // Debug normals (in vertex: vNormal = normal)
            // gl_FragColor = vec4(vNormal * 0.5 + 0.5, 1.0);
          }
        `}
        vertexShader={`
          varying vec2 vUv;
          void main() {
            vUv = uv;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
          }
        `}
      />
    </mesh>
  )
}
```

## Performance Tips

1. **Minimize uniforms**: Group related values into vectors
2. **Avoid conditionals**: Use `mix`/`step` instead of `if/else`
3. **Precalculate in JS**: Move static calculations out of shaders
4. **Use textures for lookup**: Complex functions as texture lookups
5. **Limit overdraw**: Avoid unnecessary transparent objects

```glsl
// Instead of:
if (value > 0.5) {
  color = colorA;
} else {
  color = colorB;
}

// Use:
color = mix(colorB, colorA, step(0.5, value));
```

## See Also

- `r3f-materials` - Built-in material types
- `r3f-postprocessing` - Full-screen shader effects
- `r3f-textures` - Texture sampling in shaders
