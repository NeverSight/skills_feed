---
name: r3f-materials
description: Three.js materials in R3F, built-in materials (Standard, Physical, Basic, etc.), ShaderMaterial with custom GLSL, uniforms binding and animation, and material properties. Use when choosing materials, creating custom shaders, or binding dynamic uniforms.
---

# R3F Materials

Materials define surface appearance—color, texture, reflectivity, transparency, and custom shader effects.

## Quick Start

```tsx
// Built-in material
<mesh>
  <boxGeometry />
  <meshStandardMaterial color="hotpink" metalness={0.8} roughness={0.2} />
</mesh>

// Custom shader
<mesh>
  <planeGeometry />
  <shaderMaterial
    uniforms={{ uTime: { value: 0 } }}
    vertexShader={vertexShader}
    fragmentShader={fragmentShader}
  />
</mesh>
```

## Built-in Materials

### Material Comparison

| Material | Lighting | Use Case | Performance |
|----------|----------|----------|-------------|
| `MeshBasicMaterial` | None | UI, unlit, debug | Fastest |
| `MeshStandardMaterial` | PBR | General 3D | Good |
| `MeshPhysicalMaterial` | PBR+ | Glass, car paint | Slower |
| `MeshLambertMaterial` | Diffuse | Matte surfaces | Fast |
| `MeshPhongMaterial` | Specular | Shiny plastic | Fast |
| `MeshToonMaterial` | Cel-shaded | Stylized | Good |
| `MeshNormalMaterial` | None | Debug normals | Fastest |
| `MeshDepthMaterial` | None | Depth passes | Fastest |

### MeshBasicMaterial (Unlit)

```tsx
<meshBasicMaterial
  color="#ff0000"           // Base color
  map={texture}             // Color texture
  transparent={true}        // Enable transparency
  opacity={0.5}             // Transparency level
  alphaMap={alphaTexture}   // Transparency texture
  side={THREE.DoubleSide}   // Render both sides
  wireframe={true}          // Wireframe mode
  fog={false}               // Ignore scene fog
/>
```

### MeshStandardMaterial (PBR)

```tsx
<meshStandardMaterial
  // Base
  color="#ffffff"
  map={colorTexture}
  
  // PBR properties
  metalness={0.5}           // 0 = dielectric, 1 = metal
  metalnessMap={metalMap}
  roughness={0.5}           // 0 = mirror, 1 = diffuse
  roughnessMap={roughMap}
  
  // Normal mapping
  normalMap={normalTexture}
  normalScale={[1, 1]}
  
  // Ambient occlusion
  aoMap={aoTexture}
  aoMapIntensity={1}
  
  // Displacement
  displacementMap={dispMap}
  displacementScale={0.1}
  
  // Emission
  emissive="#000000"
  emissiveMap={emissiveTexture}
  emissiveIntensity={1}
  
  // Environment
  envMap={cubeTexture}
  envMapIntensity={1}
/>
```

### MeshPhysicalMaterial (Advanced PBR)

```tsx
<meshPhysicalMaterial
  // Inherits all MeshStandardMaterial props, plus:
  
  // Clearcoat (car paint, lacquer)
  clearcoat={1}
  clearcoatRoughness={0.1}
  clearcoatNormalMap={ccNormal}
  
  // Transmission (glass, water)
  transmission={0.9}        // 0 = opaque, 1 = fully transmissive
  thickness={0.5}           // Volume thickness
  ior={1.5}                 // Index of refraction
  
  // Sheen (fabric, velvet)
  sheen={1}
  sheenRoughness={0.5}
  sheenColor="#ff00ff"
  
  // Iridescence (soap bubbles, oil slicks)
  iridescence={1}
  iridescenceIOR={1.3}
  iridescenceThicknessRange={[100, 400]}
/>
```

### MeshToonMaterial (Cel-shaded)

```tsx
<meshToonMaterial
  color="#6fa8dc"
  gradientMap={gradientTexture}  // 3-5 color ramp texture
/>

// Create gradient texture
const gradientTexture = useMemo(() => {
  const canvas = document.createElement('canvas');
  canvas.width = 4;
  canvas.height = 1;
  const ctx = canvas.getContext('2d')!;
  
  // 4-step toon shading
  ctx.fillStyle = '#444'; ctx.fillRect(0, 0, 1, 1);
  ctx.fillStyle = '#888'; ctx.fillRect(1, 0, 1, 1);
  ctx.fillStyle = '#bbb'; ctx.fillRect(2, 0, 1, 1);
  ctx.fillStyle = '#fff'; ctx.fillRect(3, 0, 1, 1);
  
  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.NearestFilter;
  texture.magFilter = THREE.NearestFilter;
  
  return texture;
}, []);
```

## Common Properties (All Materials)

```tsx
<meshStandardMaterial
  // Rendering
  transparent={false}
  opacity={1}
  alphaTest={0}           // Discard pixels below threshold
  alphaToCoverage={false} // MSAA alpha
  
  // Faces
  side={THREE.FrontSide}  // FrontSide | BackSide | DoubleSide
  
  // Depth
  depthTest={true}
  depthWrite={true}
  
  // Stencil
  stencilWrite={false}
  stencilFunc={THREE.AlwaysStencilFunc}
  
  // Blending
  blending={THREE.NormalBlending}
  
  // Other
  visible={true}
  fog={true}
  toneMapped={true}
/>
```

## Textures

### Loading Textures

```tsx
import { useTexture } from '@react-three/drei';

function TexturedMesh() {
  const [colorMap, normalMap, roughnessMap] = useTexture([
    '/textures/color.jpg',
    '/textures/normal.jpg',
    '/textures/roughness.jpg'
  ]);
  
  return (
    <mesh>
      <boxGeometry />
      <meshStandardMaterial 
        map={colorMap}
        normalMap={normalMap}
        roughnessMap={roughnessMap}
      />
    </mesh>
  );
}
```

### Texture Settings

```tsx
import { useTexture } from '@react-three/drei';
import * as THREE from 'three';

const texture = useTexture('/texture.jpg', (tex) => {
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  tex.repeat.set(4, 4);
  tex.anisotropy = 16;  // Sharper at angles
});
```

## ShaderMaterial

Full control via GLSL vertex and fragment shaders:

```tsx
import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

const vertexShader = `
  varying vec2 vUv;
  varying vec3 vNormal;
  
  void main() {
    vUv = uv;
    vNormal = normalize(normalMatrix * normal);
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`;

const fragmentShader = `
  uniform float uTime;
  uniform vec3 uColor;
  varying vec2 vUv;
  varying vec3 vNormal;
  
  void main() {
    float pulse = sin(uTime * 2.0) * 0.5 + 0.5;
    vec3 color = mix(uColor, vec3(1.0), pulse * 0.3);
    
    // Simple rim lighting
    float rim = 1.0 - dot(vNormal, vec3(0.0, 0.0, 1.0));
    color += rim * 0.5;
    
    gl_FragColor = vec4(color, 1.0);
  }
`;

function CustomShaderMesh() {
  const materialRef = useRef<THREE.ShaderMaterial>(null!);
  
  useFrame(({ clock }) => {
    materialRef.current.uniforms.uTime.value = clock.elapsedTime;
  });
  
  return (
    <mesh>
      <sphereGeometry args={[1, 32, 32]} />
      <shaderMaterial
        ref={materialRef}
        vertexShader={vertexShader}
        fragmentShader={fragmentShader}
        uniforms={{
          uTime: { value: 0 },
          uColor: { value: new THREE.Color('#ff6b6b') }
        }}
      />
    </mesh>
  );
}
```

## Uniforms

### Uniform Types

```tsx
uniforms={{
  // Scalars
  uFloat: { value: 1.0 },
  uInt: { value: 1 },
  uBool: { value: true },
  
  // Vectors
  uVec2: { value: new THREE.Vector2(1, 2) },
  uVec3: { value: new THREE.Vector3(1, 2, 3) },
  uVec4: { value: new THREE.Vector4(1, 2, 3, 4) },
  uColor: { value: new THREE.Color('#ff0000') },
  
  // Matrices
  uMat3: { value: new THREE.Matrix3() },
  uMat4: { value: new THREE.Matrix4() },
  
  // Textures
  uTexture: { value: texture },
  uCubeTexture: { value: cubeTexture },
  
  // Arrays
  uFloatArray: { value: [1.0, 2.0, 3.0] },
  uVec3Array: { value: [new THREE.Vector3(), new THREE.Vector3()] }
}}
```

### Animating Uniforms

```tsx
function AnimatedShader() {
  const materialRef = useRef<THREE.ShaderMaterial>(null!);
  
  useFrame(({ clock, mouse }) => {
    const uniforms = materialRef.current.uniforms;
    
    uniforms.uTime.value = clock.elapsedTime;
    uniforms.uMouse.value.set(mouse.x, mouse.y);
    uniforms.uResolution.value.set(window.innerWidth, window.innerHeight);
  });
  
  return (
    <shaderMaterial
      ref={materialRef}
      uniforms={{
        uTime: { value: 0 },
        uMouse: { value: new THREE.Vector2() },
        uResolution: { value: new THREE.Vector2() }
      }}
      // ...
    />
  );
}
```

### Shared Uniforms

```tsx
// Create shared uniform object
const globalUniforms = useMemo(() => ({
  uTime: { value: 0 },
  uGlobalColor: { value: new THREE.Color('#00ff00') }
}), []);

// Update in useFrame
useFrame(({ clock }) => {
  globalUniforms.uTime.value = clock.elapsedTime;
});

// Use in multiple materials
<mesh>
  <boxGeometry />
  <shaderMaterial uniforms={{ ...globalUniforms, uLocalProp: { value: 1 } }} />
</mesh>

<mesh position={[2, 0, 0]}>
  <sphereGeometry />
  <shaderMaterial uniforms={{ ...globalUniforms, uLocalProp: { value: 2 } }} />
</mesh>
```

## RawShaderMaterial

No built-in uniforms/attributes—full control:

```tsx
<rawShaderMaterial
  vertexShader={`
    precision highp float;
    
    // Must declare all inputs manually
    attribute vec3 position;
    attribute vec2 uv;
    
    uniform mat4 projectionMatrix;
    uniform mat4 modelViewMatrix;
    
    varying vec2 vUv;
    
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `}
  fragmentShader={`
    precision highp float;
    
    varying vec2 vUv;
    
    void main() {
      gl_FragColor = vec4(vUv, 0.0, 1.0);
    }
  `}
/>
```

## Material Extensions

### Extend Existing Materials

```tsx
import { extend } from '@react-three/fiber';
import { shaderMaterial } from '@react-three/drei';

// Create extended material
const GradientMaterial = shaderMaterial(
  // Uniforms
  { uColorA: new THREE.Color('#ff0000'), uColorB: new THREE.Color('#0000ff') },
  // Vertex
  `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  // Fragment
  `
    uniform vec3 uColorA;
    uniform vec3 uColorB;
    varying vec2 vUv;
    void main() {
      gl_FragColor = vec4(mix(uColorA, uColorB, vUv.y), 1.0);
    }
  `
);

// Register with R3F
extend({ GradientMaterial });

// Use in JSX
function Gradient() {
  return (
    <mesh>
      <planeGeometry args={[2, 2]} />
      <gradientMaterial uColorA="#ff0000" uColorB="#0000ff" />
    </mesh>
  );
}
```

## Performance Tips

| Technique | When to Use |
|-----------|-------------|
| Share materials | Multiple meshes, same appearance |
| Use cheaper materials | Distant objects (Basic vs Standard) |
| Limit texture size | Mobile, large scene |
| Disable unneeded features | `fog={false}`, `toneMapped={false}` |

### Material Reuse

```tsx
// Define once
const sharedMaterial = useMemo(() => (
  <meshStandardMaterial color="red" roughness={0.5} />
), []);

// Reuse (same GPU program)
{items.map((item, i) => (
  <mesh key={i} position={item.pos}>
    <boxGeometry />
    {sharedMaterial}
  </mesh>
))}
```

## File Structure

```
r3f-materials/
├── SKILL.md
├── references/
│   ├── pbr-properties.md     # PBR material deep-dive
│   ├── uniform-types.md      # Complete uniform reference
│   └── shader-templates.md   # Common shader patterns
└── scripts/
    ├── materials/
    │   ├── gradient.ts       # Gradient shader material
    │   ├── fresnel.ts        # Fresnel/rim effect
    │   └── dissolve.ts       # Dissolve effect
    └── utils/
        └── uniform-helpers.ts # Uniform animation utilities
```

## Reference

- `references/pbr-properties.md` — Deep-dive into PBR material properties
- `references/uniform-types.md` — All uniform types and GLSL mappings
- `references/shader-templates.md` — Common shader effect patterns
