---
name: postfx-effects
description: Post-processing visual effects including chromatic aberration, vignette, depth of field, film grain, color grading, and LUT support. Use when adding cinematic polish, retro aesthetics, camera simulation, or atmospheric effects to 3D scenes. Essential for mood, style, and visual storytelling.
---

# Post-Processing Effects

Cinematic and stylistic effects using @react-three/postprocessing.

## Quick Start

```bash
npm install @react-three/postprocessing postprocessing
```

```tsx
import { Canvas } from '@react-three/fiber';
import { EffectComposer, ChromaticAberration, Vignette, Noise } from '@react-three/postprocessing';

function CinematicScene() {
  return (
    <Canvas>
      <Scene />
      <EffectComposer>
        <ChromaticAberration offset={[0.002, 0.002]} />
        <Vignette darkness={0.5} offset={0.3} />
        <Noise opacity={0.05} />
      </EffectComposer>
    </Canvas>
  );
}
```

## Core Effects

### Chromatic Aberration

RGB channel separation for lens distortion or glitch effects.

```tsx
import { ChromaticAberration } from '@react-three/postprocessing';
import { BlendFunction } from 'postprocessing';
import { Vector2 } from 'three';

// Subtle cinematic fringing
function SubtleChromaticAberration() {
  return (
    <ChromaticAberration
      offset={new Vector2(0.001, 0.001)}
      radialModulation
      modulationOffset={0.2}
    />
  );
}

// Intense glitch effect
function GlitchChromaticAberration() {
  const offsetRef = useRef();

  useFrame(({ clock }) => {
    if (offsetRef.current) {
      const glitch = Math.random() > 0.95 ? 0.01 : 0.002;
      offsetRef.current.offset.set(glitch, glitch * 0.5);
    }
  });

  return (
    <ChromaticAberration
      ref={offsetRef}
      offset={new Vector2(0.002, 0.002)}
      blendFunction={BlendFunction.NORMAL}
    />
  );
}
```

### Vignette

Darkened edges for focus and cinematic framing.

```tsx
import { Vignette } from '@react-three/postprocessing';

// Soft cinematic vignette
function CinematicVignette() {
  return (
    <Vignette
      offset={0.3}      // Distance from center before darkening
      darkness={0.5}    // How dark edges become
      eskil={false}     // Use natural vignette formula
    />
  );
}

// Harsh spotlight effect
function SpotlightVignette() {
  return <Vignette offset={0.1} darkness={0.9} eskil={true} />;
}
```

### Depth of Field

Simulated camera focus with bokeh blur.

```tsx
import { DepthOfField } from '@react-three/postprocessing';

// Focus on specific distance
function StaticDOF() {
  return (
    <DepthOfField
      focusDistance={0.02}
      focalLength={0.05}
      bokehScale={3}
      height={480}
    />
  );
}

// Focus follows target object
function TrackingDOF({ targetRef }) {
  const dofRef = useRef();
  const { camera } = useThree();

  useFrame(() => {
    if (targetRef.current && dofRef.current) {
      const distance = camera.position.distanceTo(targetRef.current.position);
      dofRef.current.target = distance;
    }
  });

  return <DepthOfField ref={dofRef} focusDistance={0} focalLength={0.02} bokehScale={2} />;
}
```

### Noise / Film Grain

```tsx
import { Noise } from '@react-three/postprocessing';
import { BlendFunction } from 'postprocessing';

// Subtle film grain
function FilmGrain() {
  return <Noise opacity={0.04} blendFunction={BlendFunction.OVERLAY} />;
}

// Heavy VHS noise
function VHSNoise() {
  return <Noise opacity={0.15} blendFunction={BlendFunction.SCREEN} />;
}
```

### Color Grading

```tsx
import { HueSaturation, BrightnessContrast } from '@react-three/postprocessing';

// Desaturated cinematic look
function CinematicGrade() {
  return (
    <>
      <HueSaturation hue={0} saturation={-0.2} />
      <BrightnessContrast brightness={-0.05} contrast={0.1} />
    </>
  );
}

// Warm sunset mood
function SunsetGrade() {
  return (
    <>
      <HueSaturation hue={0.05} saturation={0.15} />
      <BrightnessContrast brightness={0.02} contrast={0.05} />
    </>
  );
}

// Cold sci-fi atmosphere
function SciFiGrade() {
  return (
    <>
      <HueSaturation hue={-0.1} saturation={-0.1} />
      <BrightnessContrast brightness={-0.1} contrast={0.15} />
    </>
  );
}
```

### LUT (Lookup Table)

```tsx
import { LUT } from '@react-three/postprocessing';
import { LookupTexture } from 'postprocessing';

function LUTGrading() {
  const [lut, setLut] = useState(null);

  useEffect(() => {
    LookupTexture.createLookupTexture('/luts/cinematic.cube').then(setLut);
  }, []);

  if (!lut) return null;
  return <LUT lut={lut} tetrahedralInterpolation />;
}
```

### Tone Mapping

```tsx
import { ToneMapping } from '@react-three/postprocessing';
import { ToneMappingMode } from 'postprocessing';

function CinematicToneMapping() {
  return <ToneMapping mode={ToneMappingMode.ACES_FILMIC} />;
}
```

### Scanlines / CRT Effect

```tsx
import { Scanline } from '@react-three/postprocessing';

function CRTScanlines() {
  return <Scanline density={1.25} opacity={0.15} blendFunction={BlendFunction.OVERLAY} />;
}
```

### God Rays

```tsx
import { GodRays } from '@react-three/postprocessing';

function VolumetricLight() {
  const sunRef = useRef();

  return (
    <>
      <mesh ref={sunRef} position={[0, 5, -10]}>
        <sphereGeometry args={[1, 32, 32]} />
        <meshBasicMaterial color="#FFF8E0" />
      </mesh>

      <EffectComposer>
        {sunRef.current && <GodRays sun={sunRef.current} exposure={0.5} decay={0.9} blur />}
      </EffectComposer>
    </>
  );
}
```

## Combining Effects

### Cinematic Stack

```tsx
function CinematicStack() {
  return (
    <EffectComposer>
      <ToneMapping mode={ToneMappingMode.ACES_FILMIC} />
      <HueSaturation saturation={-0.15} />
      <BrightnessContrast brightness={-0.05} contrast={0.1} />
      <ChromaticAberration offset={[0.001, 0.001]} />
      <Vignette darkness={0.4} offset={0.3} />
      <Noise opacity={0.03} blendFunction={BlendFunction.OVERLAY} />
    </EffectComposer>
  );
}
```

### Retro VHS Stack

```tsx
function VHSStack() {
  return (
    <EffectComposer>
      <HueSaturation saturation={-0.3} />
      <BrightnessContrast contrast={0.2} />
      <ChromaticAberration offset={[0.005, 0.002]} />
      <Scanline density={1.5} opacity={0.1} />
      <Noise opacity={0.1} blendFunction={BlendFunction.SCREEN} />
      <Vignette darkness={0.6} offset={0.2} />
    </EffectComposer>
  );
}
```

### Dream Sequence Stack

```tsx
function DreamStack() {
  return (
    <EffectComposer>
      <DepthOfField focusDistance={0.01} focalLength={0.1} bokehScale={4} />
      <Bloom luminanceThreshold={0.3} intensity={0.8} />
      <HueSaturation saturation={0.2} hue={0.05} />
      <BrightnessContrast brightness={0.1} />
      <Vignette darkness={0.3} offset={0.4} />
    </EffectComposer>
  );
}
```

## Animated Effects

### Time-Driven Color Shift

```tsx
function TimeDrivenEffects() {
  const hueRef = useRef();
  const vignetteRef = useRef();

  useFrame(({ clock }) => {
    const t = clock.elapsedTime;
    if (hueRef.current) hueRef.current.hue = Math.sin(t * 0.1) * 0.1;
    if (vignetteRef.current) vignetteRef.current.darkness = 0.4 + Math.sin(t * 2) * 0.1;
  });

  return (
    <EffectComposer>
      <HueSaturation ref={hueRef} saturation={0} hue={0} />
      <Vignette ref={vignetteRef} darkness={0.4} offset={0.3} />
    </EffectComposer>
  );
}
```

### Audio-Reactive Effects

```tsx
function AudioReactiveEffects({ audioData }) {
  const chromaRef = useRef();
  const vignetteRef = useRef();

  useFrame(() => {
    if (!audioData) return;
    const bass = audioData[0] / 255;
    const mid = audioData[4] / 255;

    if (chromaRef.current) {
      const offset = 0.001 + bass * 0.005;
      chromaRef.current.offset.set(offset, offset * 0.5);
    }
    if (vignetteRef.current) {
      vignetteRef.current.darkness = 0.3 + mid * 0.3;
    }
  });

  return (
    <EffectComposer>
      <ChromaticAberration ref={chromaRef} offset={[0.001, 0.001]} />
      <Vignette ref={vignetteRef} darkness={0.4} offset={0.3} />
    </EffectComposer>
  );
}
```

## Temporal Collapse Theme

Effects stack for cosmic countdown aesthetic:

```tsx
function TemporalCollapseEffects() {
  const chromaRef = useRef();

  useFrame(({ clock }) => {
    if (chromaRef.current) {
      const pulse = Math.sin(clock.elapsedTime * 1.5) * 0.001;
      chromaRef.current.offset.set(0.002 + pulse, 0.001 + pulse * 0.5);
    }
  });

  return (
    <EffectComposer>
      <ToneMapping mode={ToneMappingMode.ACES_FILMIC} />
      <HueSaturation hue={-0.05} saturation={-0.1} />
      <BrightnessContrast brightness={-0.05} contrast={0.1} />
      <ChromaticAberration ref={chromaRef} offset={[0.002, 0.001]} />
      <Vignette darkness={0.5} offset={0.25} />
      <Noise opacity={0.02} blendFunction={BlendFunction.OVERLAY} />
    </EffectComposer>
  );
}
```

## Performance Tips

| Technique | Impact | Solution |
|-----------|--------|----------|
| Multiple blur effects | High | Combine DOF with bloom carefully |
| High DOF resolution | High | Use `height={480}` or lower |
| LUT loading | Medium | Preload, cache texture |
| Many effects | Medium | Order effects efficiently |

```tsx
function OptimizedEffects() {
  return (
    <EffectComposer multisampling={0}>
      <ToneMapping mode={ToneMappingMode.ACES_FILMIC} />
      <Vignette darkness={0.4} />
      <Noise opacity={0.02} />
      <Bloom intensity={1} mipmapBlur levels={4} />
    </EffectComposer>
  );
}
```

## Reference

- See `postfx-composer` for EffectComposer setup and render targets
- See `postfx-bloom` for dedicated bloom techniques
- See `postfx-router` for effect selection guidance
