---
name: reanimated-skia-performance
description: "Write and review high-performance React Native animations and 2D graphics using react-native-reanimated (v4+) and @shopify/react-native-skia (Canvas scenes, runtime effects/shaders). Use for: gesture-driven interactions, spring/timing transitions, layout/mount animations, Reanimated CSS transitions/animations, Skia drawings, animated shader uniforms, path/vector interpolation, dev-mode tuning panels (sliders), and diagnosing animation jank (JS thread stalls, excessive re-renders, per-frame allocations)."
---

# Reanimated + Skia Performance

## Defaults

- Keep animation state on the UI thread: `useSharedValue`, `useDerivedValue`, worklets.
- Prefer Reanimated v4 declarative APIs; avoid legacy `Animated`.
- Prefer `shared.get()` / `shared.set()` over `shared.value` in app code (React Compiler friendly).
- Minimize JS↔UI crossings: avoid `scheduleOnRN`/`runOnJS` except for unavoidable side effects.
- For Skia, avoid per-frame React renders: pass `SharedValue`s directly to Skia props/uniforms.

## Workflow

1. Define the effect: what animates, duration/curve, interrupt rules, and gesture input.
2. Choose the renderer:
   - Use Reanimated styles for transforms/opacity/layout.
   - Use Skia for custom drawing, particles, gradients, runtime effects/shaders.
3. Choose the primitive:
   - Use Reanimated CSS transitions/animations for simple declarative style changes.
   - Use `withTiming` for tweens, `withSpring` for physics, `withDecay` for momentum.
   - Use Layout Animations for mount/unmount or layout changes.
4. Implement a single data flow on the UI thread (no `setState` per frame).
5. Do a perf pass (see `references/perf-checklist.md`).

## Patterns

### Shared values (React Compiler safe)

- Read: `progress.get()`
- Write: `progress.set(withTiming(1))`

```ts
import { useEffect } from 'react';
import { useSharedValue, withTiming } from 'react-native-reanimated';

const progress = useSharedValue(0);

useEffect(() => {
  progress.set(withTiming(1, { duration: 400 }));
}, [progress]);
```

### Reanimated v4 CSS transitions

Use for state-driven style changes where you do not need bespoke worklets.

```tsx
import Animated from 'react-native-reanimated';

<Animated.View
  style={{
    width: expanded ? 240 : 160,
    opacity: enabled ? 1 : 0.6,
    transitionProperty: ['width', 'opacity'],
    transitionDuration: 220,
    transitionTimingFunction: 'ease-in-out',
  }}
/>
```

### Reanimated v4 CSS animations (keyframes)

Use for keyframe-like sequences (pulses, wiggles, repeated loops) without writing custom worklets.

Supported settings:
- `animationName` (keyframes object)
- `animationDuration`
- `animationDelay`
- `animationTimingFunction`
- `animationDirection`
- `animationIterationCount`
- `animationFillMode`
- `animationPlayState`

```tsx
import Animated from 'react-native-reanimated';

const pulse = {
  from: { transform: [{ scale: 1 }], opacity: 0.9 },
  '50%': { transform: [{ scale: 1.06 }], opacity: 1 },
  to: { transform: [{ scale: 1 }], opacity: 0.9 },
};

<Animated.View
  style={{
    animationName: pulse,
    animationDuration: '900ms',
    animationDelay: '80ms',
    animationTimingFunction: 'ease-in-out',
    animationDirection: 'alternate',
    animationIterationCount: 'infinite',
    animationFillMode: 'both',
    animationPlayState: paused ? 'paused' : 'running',
  }}
/>
```

### Dev-mode tuning panel (sliders)

Use sliders to tune animation configs or shader uniforms in `__DEV__`.

- Keep the tuning UI in a separate component to avoid re-rendering the animated scene.
- Write slider values into `SharedValue`s via `.set()`.
- For shader tuning: feed `SharedValue`s into uniforms via `useDerivedValue`.
- For animation config tuning: store config params in `SharedValue`s and read them when starting/restarting the animation.

See: `references/dev-tuning.md`.

### Gesture-driven animation (Gesture Builder API)

Update shared values in `onUpdate` and drive visuals via animated styles.

```tsx
import { Gesture, GestureDetector } from 'react-native-gesture-handler';
import Animated, { useAnimatedStyle, useSharedValue, withSpring } from 'react-native-reanimated';

const x = useSharedValue(0);
const gesture = Gesture.Pan()
  .onUpdate((e) => {
    x.set(e.translationX);
  })
  .onEnd(() => {
    x.set(withSpring(0));
  });

const style = useAnimatedStyle(() => ({ transform: [{ translateX: x.get() }] }));

<GestureDetector gesture={gesture}>
  <Animated.View style={style} />
</GestureDetector>;
```

### Skia shader with animated uniforms

- Compile the runtime effect once (`useMemo`).
- Pass uniforms as a `SharedValue<Uniforms>` (Skia detects animated props by `{ value: T }`).
- Do not access `.value` in your app code; pass the `SharedValue` object.

```tsx
import { useMemo } from 'react';
import { Skia, Canvas, Fill, Paint, Shader, type Uniforms } from '@shopify/react-native-skia';
import { useDerivedValue } from 'react-native-reanimated';
import { useClock } from '@shopify/react-native-skia';

const sksl = `
uniform float2 u_resolution;
uniform float u_time;

half4 main(float2 xy) {
  float2 uv = xy / u_resolution;
  float v = 0.5 + 0.5 * sin(u_time * 0.002 + uv.x * 8.0);
  return half4(v, v * 0.6, 1.0 - v, 1.0);
}
`;

const effect = useMemo(() => Skia.RuntimeEffect.Make(sksl), []);
if (!effect) return null;

const clock = useClock(); // ms since first frame
const uniforms = useDerivedValue<Uniforms>(() => ({
  u_resolution: Skia.Point(width, height),
  u_time: clock.get(),
}));

<Canvas style={{ width, height }}>
  <Fill>
    <Paint>
      <Shader source={effect} uniforms={uniforms} />
    </Paint>
  </Fill>
</Canvas>;
```

## Common pitfalls

- Do not read shared values in React render; read them in worklets (`useAnimatedStyle`, `useDerivedValue`).
- Do not call `runOnJS`/`scheduleOnRN` in `onUpdate` unless you must.
- Do not allocate big arrays/paths/images per frame; memoize Skia objects and update via animated props.
- For runtime effects, always provide every uniform declared in the shader; missing uniforms throw.

## References

- Reanimated v4 patterns and repo conventions: `references/reanimated-v4.md`
- Skia Canvas + runtime effects/shaders patterns: `references/skia-shaders.md`
- Dev-mode tuning panels (sliders): `references/dev-tuning.md`
- Performance checklist + debugging: `references/perf-checklist.md`
