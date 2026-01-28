---
name: r3f-postprocessing
description: React Three Fiber post-processing - @react-three/postprocessing, bloom, DOF, screen effects. Use when adding visual effects, color grading, blur, glow, or creating custom screen-space shaders.
---

# React Three Fiber Post-Processing

## Quick Start

```tsx
import { Canvas } from '@react-three/fiber'
import { EffectComposer, Bloom, Vignette } from '@react-three/postprocessing'

function Scene() {
  return (
    <Canvas>
      <ambientLight />
      <mesh>
        <boxGeometry />
        <meshStandardMaterial color="hotpink" emissive="hotpink" emissiveIntensity={2} />
      </mesh>

      <EffectComposer>
        <Bloom luminanceThreshold={0.5} luminanceSmoothing={0.9} intensity={1.5} />
        <Vignette offset={0.5} darkness={0.5} />
      </EffectComposer>
    </Canvas>
  )
}
```

## Installation

```bash
npm install @react-three/postprocessing postprocessing
```

## EffectComposer

The container for all post-processing effects.

```tsx
import { EffectComposer } from '@react-three/postprocessing'

function Scene() {
  return (
    <Canvas>
      {/* Scene content */}
      <mesh>...</mesh>

      {/* Post-processing - must be inside Canvas, after scene content */}
      <EffectComposer
        enabled={true}           // Toggle all effects
        depthBuffer={true}       // Enable depth buffer
        stencilBuffer={false}    // Enable stencil buffer
        autoClear={true}         // Auto clear before render
        multisampling={8}        // MSAA samples (0 to disable)
      >
        {/* Effects go here */}
      </EffectComposer>
    </Canvas>
  )
}
```

## Common Effects

### Bloom (Glow)

```tsx
import { EffectComposer, Bloom } from '@react-three/postprocessing'
import { BlendFunction } from 'postprocessing'

<EffectComposer>
  <Bloom
    intensity={1.0}              // Bloom intensity
    luminanceThreshold={0.9}     // Brightness threshold
    luminanceSmoothing={0.025}   // Smoothness of threshold
    mipmapBlur={true}            // Enable mipmap blur
    radius={0.8}                 // Bloom radius
    levels={8}                   // Mipmap levels
    blendFunction={BlendFunction.ADD}
  />
</EffectComposer>

// For objects to glow, use emissive materials
<mesh>
  <boxGeometry />
  <meshStandardMaterial
    color="black"
    emissive="#ff00ff"
    emissiveIntensity={2}
    toneMapped={false}  // Important for values > 1
  />
</mesh>
```

### Selective Bloom

```tsx
import { EffectComposer, Bloom, Selection, Select } from '@react-three/postprocessing'

function Scene() {
  return (
    <Canvas>
      <Selection>
        <EffectComposer>
          <Bloom
            luminanceThreshold={0}
            intensity={2}
            mipmapBlur
          />
        </EffectComposer>

        {/* This mesh will bloom */}
        <Select enabled>
          <mesh>
            <sphereGeometry />
            <meshStandardMaterial emissive="red" emissiveIntensity={2} toneMapped={false} />
          </mesh>
        </Select>

        {/* This mesh will NOT bloom */}
        <mesh position={[2, 0, 0]}>
          <boxGeometry />
          <meshStandardMaterial color="blue" />
        </mesh>
      </Selection>
    </Canvas>
  )
}
```

### Depth of Field

```tsx
import { EffectComposer, DepthOfField } from '@react-three/postprocessing'

<EffectComposer>
  <DepthOfField
    focusDistance={0}     // Focus distance (0 = auto)
    focalLength={0.02}    // Camera focal length
    bokehScale={2}        // Bokeh size
    height={480}          // Resolution height
  />
</EffectComposer>

// With target object
import { useRef } from 'react'

function Scene() {
  const targetRef = useRef()

  return (
    <>
      <mesh ref={targetRef} position={[0, 0, -5]}>
        <boxGeometry />
        <meshStandardMaterial color="red" />
      </mesh>

      <EffectComposer>
        <DepthOfField
          target={targetRef}
          focalLength={0.02}
          bokehScale={2}
        />
      </EffectComposer>
    </>
  )
}
```

### Vignette

```tsx
import { EffectComposer, Vignette } from '@react-three/postprocessing'

<EffectComposer>
  <Vignette
    offset={0.5}          // Vignette size
    darkness={0.5}        // Vignette intensity
    eskil={false}         // Use Eskil's vignette technique
  />
</EffectComposer>
```

### Noise

```tsx
import { EffectComposer, Noise } from '@react-three/postprocessing'
import { BlendFunction } from 'postprocessing'

<EffectComposer>
  <Noise
    premultiply            // Multiply noise with input
    blendFunction={BlendFunction.ADD}
    opacity={0.5}
  />
</EffectComposer>
```

### Chromatic Aberration

```tsx
import { EffectComposer, ChromaticAberration } from '@react-three/postprocessing'
import { BlendFunction } from 'postprocessing'

<EffectComposer>
  <ChromaticAberration
    offset={[0.002, 0.002]}    // Color offset
    radialModulation={true}    // Apply radially
    modulationOffset={0.5}
    blendFunction={BlendFunction.NORMAL}
  />
</EffectComposer>
```

### SSAO (Screen Space Ambient Occlusion)

```tsx
import { EffectComposer, SSAO } from '@react-three/postprocessing'
import { BlendFunction } from 'postprocessing'

<EffectComposer>
  <SSAO
    blendFunction={BlendFunction.MULTIPLY}
    samples={30}              // Amount of samples
    radius={5}                // Occlusion radius
    intensity={30}            // Occlusion intensity
    luminanceInfluence={0.6}
    color="black"
    worldDistanceThreshold={100}
    worldDistanceFalloff={5}
    worldProximityThreshold={0.01}
    worldProximityFalloff={0.01}
  />
</EffectComposer>
```

### Outline

```tsx
import { EffectComposer, Outline, Selection, Select } from '@react-three/postprocessing'

function Scene() {
  return (
    <Canvas>
      <Selection>
        <EffectComposer autoClear={false}>
          <Outline
            visibleEdgeColor={0xffffff}    // Visible edge color
            hiddenEdgeColor={0x22090a}     // Hidden edge color
            edgeStrength={2.5}             // Edge strength
            pulseSpeed={0}                 // Pulse animation speed
            blur                           // Enable blur
            xRay                           // Show behind objects
          />
        </EffectComposer>

        {/* Outlined object */}
        <Select enabled>
          <mesh>
            <boxGeometry />
            <meshStandardMaterial color="orange" />
          </mesh>
        </Select>

        {/* Non-outlined object */}
        <mesh position={[2, 0, 0]}>
          <sphereGeometry />
          <meshStandardMaterial color="blue" />
        </mesh>
      </Selection>
    </Canvas>
  )
}
```

### Color Grading

```tsx
import { EffectComposer, BrightnessContrast, HueSaturation } from '@react-three/postprocessing'

<EffectComposer>
  <BrightnessContrast
    brightness={0}     // -1 to 1
    contrast={0}       // -1 to 1
  />
  <HueSaturation
    hue={0}           // Hue rotation in radians
    saturation={0}    // -1 to 1
  />
</EffectComposer>
```

### Tone Mapping

```tsx
import { EffectComposer, ToneMapping } from '@react-three/postprocessing'
import { ToneMappingMode } from 'postprocessing'

<EffectComposer>
  <ToneMapping
    mode={ToneMappingMode.ACES_FILMIC}
    // Modes: LINEAR, REINHARD, REINHARD2, OPTIMIZED_CINEON, CINEON, ACES_FILMIC, AGX, NEUTRAL
    resolution={256}
    whitePoint={4.0}
    middleGrey={0.6}
    minLuminance={0.01}
    averageLuminance={1.0}
    adaptationRate={1.0}
  />
</EffectComposer>
```

### Glitch

```tsx
import { EffectComposer, Glitch } from '@react-three/postprocessing'
import { GlitchMode } from 'postprocessing'

<EffectComposer>
  <Glitch
    delay={[1.5, 3.5]}           // Min/max delay between glitches
    duration={[0.6, 1.0]}        // Min/max duration
    strength={[0.3, 1.0]}        // Min/max strength
    mode={GlitchMode.SPORADIC}   // DISABLED, SPORADIC, CONSTANT_MILD, CONSTANT_WILD
    active                       // Enable/disable
    ratio={0.85}                 // Glitch ratio (0 = none, 1 = always)
  />
</EffectComposer>
```

### Pixelation

```tsx
import { EffectComposer, Pixelation } from '@react-three/postprocessing'

<EffectComposer>
  <Pixelation
    granularity={5}    // Pixel size
  />
</EffectComposer>
```

### Scanline

```tsx
import { EffectComposer, Scanline } from '@react-three/postprocessing'
import { BlendFunction } from 'postprocessing'

<EffectComposer>
  <Scanline
    blendFunction={BlendFunction.OVERLAY}
    density={1.25}     // Line density
    opacity={0.5}      // Effect opacity
  />
</EffectComposer>
```

### Grid

```tsx
import { EffectComposer, Grid } from '@react-three/postprocessing'
import { BlendFunction } from 'postprocessing'

<EffectComposer>
  <Grid
    blendFunction={BlendFunction.OVERLAY}
    scale={1.0}        // Grid scale
    lineWidth={0.0}    // Line width
  />
</EffectComposer>
```

### DotScreen

```tsx
import { EffectComposer, DotScreen } from '@react-three/postprocessing'
import { BlendFunction } from 'postprocessing'

<EffectComposer>
  <DotScreen
    blendFunction={BlendFunction.NORMAL}
    angle={Math.PI * 0.5}    // Pattern angle
    scale={1.0}              // Pattern scale
  />
</EffectComposer>
```

### SMAA (Anti-Aliasing)

```tsx
import { EffectComposer, SMAA } from '@react-three/postprocessing'

<EffectComposer multisampling={0}>  {/* Disable MSAA when using SMAA */}
  <SMAA />
</EffectComposer>
```

### FXAA (Anti-Aliasing)

```tsx
import { EffectComposer, FXAA } from '@react-three/postprocessing'

<EffectComposer multisampling={0}>
  <FXAA />
</EffectComposer>
```

## Combining Multiple Effects

```tsx
import { EffectComposer, Bloom, Vignette, ChromaticAberration, Noise, SMAA } from '@react-three/postprocessing'
import { BlendFunction } from 'postprocessing'

function PostProcessing() {
  return (
    <EffectComposer multisampling={0}>
      {/* Glow effect */}
      <Bloom
        intensity={1.5}
        luminanceThreshold={0.9}
        luminanceSmoothing={0.025}
        mipmapBlur
      />

      {/* Color aberration */}
      <ChromaticAberration
        offset={[0.001, 0.001]}
        radialModulation
        modulationOffset={0.5}
      />

      {/* Film grain */}
      <Noise
        premultiply
        blendFunction={BlendFunction.ADD}
        opacity={0.2}
      />

      {/* Vignette */}
      <Vignette
        offset={0.3}
        darkness={0.5}
      />

      {/* Anti-aliasing (should be last) */}
      <SMAA />
    </EffectComposer>
  )
}
```

## Custom Effects

### Using postprocessing Effect Class

```tsx
import { forwardRef, useMemo } from 'react'
import { Effect, BlendFunction } from 'postprocessing'
import { Uniform } from 'three'

// Fragment shader
const fragmentShader = `
  uniform float time;
  uniform float intensity;

  void mainImage(const in vec4 inputColor, const in vec2 uv, out vec4 outputColor) {
    vec2 distortedUv = uv;
    distortedUv.x += sin(uv.y * 10.0 + time) * 0.01 * intensity;

    vec4 color = texture2D(inputBuffer, distortedUv);
    outputColor = color;
  }
`

// Effect class
class WaveDistortionEffect extends Effect {
  constructor({ intensity = 1.0, blendFunction = BlendFunction.NORMAL } = {}) {
    super('WaveDistortionEffect', fragmentShader, {
      blendFunction,
      uniforms: new Map([
        ['time', new Uniform(0)],
        ['intensity', new Uniform(intensity)],
      ]),
    })
  }

  update(renderer, inputBuffer, deltaTime) {
    this.uniforms.get('time').value += deltaTime
  }
}

// React component wrapper
export const WaveDistortion = forwardRef(({ intensity = 1.0, blendFunction }, ref) => {
  const effect = useMemo(() => new WaveDistortionEffect({ intensity, blendFunction }), [intensity, blendFunction])
  return <primitive ref={ref} object={effect} dispose={null} />
})

// Usage
<EffectComposer>
  <WaveDistortion intensity={0.5} />
</EffectComposer>
```

### Shader with wrapEffect

```tsx
import { wrapEffect } from '@react-three/postprocessing'
import { Effect, BlendFunction } from 'postprocessing'
import { Uniform } from 'three'

class InvertEffect extends Effect {
  constructor({ blendFunction = BlendFunction.NORMAL } = {}) {
    super('InvertEffect', `
      void mainImage(const in vec4 inputColor, const in vec2 uv, out vec4 outputColor) {
        outputColor = vec4(1.0 - inputColor.rgb, inputColor.a);
      }
    `, {
      blendFunction,
    })
  }
}

export const Invert = wrapEffect(InvertEffect)

// Usage
<EffectComposer>
  <Invert />
</EffectComposer>
```

## Conditional Effects

```tsx
import { useState } from 'react'
import { EffectComposer, Bloom, Vignette, Glitch } from '@react-three/postprocessing'

function ConditionalPostProcessing() {
  const [effects, setEffects] = useState({
    bloom: true,
    vignette: true,
    glitch: false,
  })

  return (
    <>
      <EffectComposer>
        {effects.bloom && (
          <Bloom intensity={1.5} luminanceThreshold={0.9} />
        )}
        {effects.vignette && (
          <Vignette offset={0.5} darkness={0.5} />
        )}
        {effects.glitch && (
          <Glitch delay={[1, 3]} duration={[0.5, 1]} strength={[0.3, 1]} />
        )}
      </EffectComposer>

      {/* UI to toggle effects */}
      <div className="controls">
        <button onClick={() => setEffects(e => ({ ...e, bloom: !e.bloom }))}>
          Toggle Bloom
        </button>
        <button onClick={() => setEffects(e => ({ ...e, vignette: !e.vignette }))}>
          Toggle Vignette
        </button>
        <button onClick={() => setEffects(e => ({ ...e, glitch: !e.glitch }))}>
          Toggle Glitch
        </button>
      </div>
    </>
  )
}
```

## Animated Effects

```tsx
import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { EffectComposer, Bloom, ChromaticAberration } from '@react-three/postprocessing'

function AnimatedEffects() {
  const bloomRef = useRef()
  const chromaticRef = useRef()

  useFrame(({ clock }) => {
    const t = clock.elapsedTime

    // Animate bloom intensity
    if (bloomRef.current) {
      bloomRef.current.intensity = 1 + Math.sin(t) * 0.5
    }

    // Animate chromatic aberration
    if (chromaticRef.current) {
      const offset = Math.sin(t * 2) * 0.002
      chromaticRef.current.offset.set(offset, offset)
    }
  })

  return (
    <EffectComposer>
      <Bloom ref={bloomRef} luminanceThreshold={0.9} />
      <ChromaticAberration ref={chromaticRef} />
    </EffectComposer>
  )
}
```

## N8AO (High Quality AO)

```tsx
import { EffectComposer } from '@react-three/postprocessing'
import { N8AO } from '@react-three/postprocessing'

<EffectComposer>
  <N8AO
    aoRadius={0.5}
    intensity={1}
    aoSamples={6}
    denoiseSamples={4}
    denoiseRadius={12}
    distanceFalloff={1}
    color="black"
    quality="low"   // low, medium, high, ultra
    halfRes={false}
  />
</EffectComposer>
```

## God Rays

```tsx
import { EffectComposer, GodRays } from '@react-three/postprocessing'
import { useRef } from 'react'

function Scene() {
  const sunRef = useRef()

  return (
    <Canvas>
      {/* Sun mesh (light source for god rays) */}
      <mesh ref={sunRef} position={[0, 5, -10]}>
        <sphereGeometry args={[1]} />
        <meshBasicMaterial color="#ffddaa" />
      </mesh>

      <EffectComposer>
        {sunRef.current && (
          <GodRays
            sun={sunRef}
            blendFunction={BlendFunction.SCREEN}
            samples={60}
            density={0.96}
            decay={0.9}
            weight={0.4}
            exposure={0.6}
            clampMax={1}
            blur
          />
        )}
      </EffectComposer>
    </Canvas>
  )
}
```

## LUT (Color Lookup Table)

```tsx
import { EffectComposer, LUT } from '@react-three/postprocessing'
import { LUTCubeLoader } from 'postprocessing'
import { useLoader } from '@react-three/fiber'

function ColorGradedScene() {
  const texture = useLoader(LUTCubeLoader, '/luts/cinematic.cube')

  return (
    <EffectComposer>
      <LUT lut={texture} />
    </EffectComposer>
  )
}
```

## Blend Functions

```tsx
import { BlendFunction } from 'postprocessing'

// Available blend functions:
BlendFunction.SKIP           // Skip blending
BlendFunction.ADD            // Additive
BlendFunction.ALPHA          // Alpha
BlendFunction.AVERAGE        // Average
BlendFunction.COLOR          // Color
BlendFunction.COLOR_BURN     // Color Burn
BlendFunction.COLOR_DODGE    // Color Dodge
BlendFunction.DARKEN         // Darken
BlendFunction.DIFFERENCE     // Difference
BlendFunction.DIVIDE         // Divide
BlendFunction.DST            // Destination
BlendFunction.EXCLUSION      // Exclusion
BlendFunction.HARD_LIGHT     // Hard Light
BlendFunction.HARD_MIX       // Hard Mix
BlendFunction.HUE            // Hue
BlendFunction.INVERT         // Invert
BlendFunction.INVERT_RGB     // Invert RGB
BlendFunction.LIGHTEN        // Lighten
BlendFunction.LINEAR_BURN    // Linear Burn
BlendFunction.LINEAR_DODGE   // Linear Dodge
BlendFunction.LINEAR_LIGHT   // Linear Light
BlendFunction.LUMINOSITY     // Luminosity
BlendFunction.MULTIPLY       // Multiply
BlendFunction.NEGATION       // Negation
BlendFunction.NORMAL         // Normal
BlendFunction.OVERLAY        // Overlay
BlendFunction.PIN_LIGHT      // Pin Light
BlendFunction.REFLECT        // Reflect
BlendFunction.SATURATION     // Saturation
BlendFunction.SCREEN         // Screen
BlendFunction.SET            // Set
BlendFunction.SOFT_LIGHT     // Soft Light
BlendFunction.SRC            // Source
BlendFunction.SUBTRACT       // Subtract
BlendFunction.VIVID_LIGHT    // Vivid Light
```

## Performance Tips

1. **Limit effect count**: Each effect adds rendering overhead
2. **Use multisampling wisely**: Higher values = slower performance
3. **Disable when not needed**: Toggle `enabled` prop
4. **Lower resolution**: Some effects have resolution props
5. **Profile with DevTools**: Monitor GPU usage

```tsx
// Disable all effects
<EffectComposer enabled={performanceMode}>
  ...
</EffectComposer>

// Reduce effect quality on mobile
const isMobile = /iPhone|iPad|Android/i.test(navigator.userAgent)

<EffectComposer multisampling={isMobile ? 0 : 8}>
  <Bloom mipmapBlur={!isMobile} radius={isMobile ? 0.4 : 0.8} />
  {!isMobile && <SSAO samples={16} />}
</EffectComposer>
```

## See Also

- `r3f-shaders` - Custom shader development
- `r3f-materials` - Emissive materials for bloom
- `r3f-fundamentals` - Canvas and renderer setup
