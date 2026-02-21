---
name: animating-react-native-expo
description: >-
  Builds performant animations and gesture-driven interactions in React Native (Expo) apps using React Native Reanimated v4 and React Native Gesture Handler (GestureDetector / hook API).
  Use when implementing UI motion, transitions, layout/entering/exiting animations, CSS-style transitions/animations, interactive gestures (pan/pinch/swipe/drag), scroll-linked animations, worklets/shared values, or debugging animation performance and threading issues.
---

# React Native (Expo) animations — Reanimated v4 + Gesture Handler

## Defaults (pick these unless there’s a reason not to)

1) **Simple state change** (hover/pressed/toggled, small style changes): use **Reanimated CSS Transitions**.
2) **Mount/unmount + layout changes** (lists, accordions, reflow): use **Reanimated Layout Animations**.
3) **Interactive / per-frame** (gestures, scroll, physics, drag): use **Shared Values + worklets** (UI thread).

If an existing codebase already uses a different pattern, stay consistent and only migrate when necessary.

## Quick start

### Install (Expo)
```bash
npx expo install react-native-reanimated react-native-worklets react-native-gesture-handler
```

Run the setup check (optional):
```bash
node {baseDir}/scripts/check-setup.mjs
```

### 1) Shared value + `withTiming`
```tsx
import { Pressable } from 'react-native';
import Animated, { useSharedValue, useAnimatedStyle, withTiming } from 'react-native-reanimated';

export function FadeInBox() {
  const opacity = useSharedValue(0);

  const style = useAnimatedStyle(() => ({ opacity: opacity.value }));

  return (
    <Pressable onPress={() => (opacity.value = withTiming(opacity.value ? 0 : 1, { duration: 200 }))}>
      <Animated.View style={[{ width: 80, height: 80 }, style]} />
    </Pressable>
  );
}
```

### 2) Pan gesture driving translation (UI thread)
```tsx
import Animated, { useSharedValue, useAnimatedStyle, withSpring } from 'react-native-reanimated';
import { GestureDetector, usePanGesture } from 'react-native-gesture-handler';

export function Draggable() {
  const x = useSharedValue(0);
  const y = useSharedValue(0);

  const pan = usePanGesture({
    onUpdate: (e) => {
      x.value = e.translationX;
      y.value = e.translationY;
    },
    onDeactivate: () => {
      x.value = withSpring(0);
      y.value = withSpring(0);
    },
  });

  const style = useAnimatedStyle(() => ({ transform: [{ translateX: x.value }, { translateY: y.value }] }));

  return (
    <GestureDetector gesture={pan}>
      <Animated.View style={[{ width: 100, height: 100 }, style]} />
    </GestureDetector>
  );
}
```

### 3) CSS-style transition (best for “style changes when state changes”)
```tsx
import Animated from 'react-native-reanimated';

export function ExpandingCard({ expanded }: { expanded: boolean }) {
  return (
    <Animated.View
      style={{
        width: expanded ? 260 : 180,
        transitionProperty: 'width',
        transitionDuration: 220,
      }}
    />
  );
}
```

## Workflow (copy this and tick it off)

- [ ] Identify the driver: **state**, **layout**, **gesture**, or **scroll**.
- [ ] Choose the primitive:
  - [ ] state → CSS transition / CSS animation
  - [ ] layout/mount → entering/exiting/layout transitions
  - [ ] gesture/scroll → shared values + worklets
- [ ] Keep per-frame work on the **UI thread** (worklets); avoid React state updates every frame.
- [ ] If a JS-side effect is required (navigation, analytics, state set), call it via `scheduleOnRN`.
- [ ] Verify on-device (Hermes inspector), not “Remote JS Debugging”.

## Core patterns

### Shared values are the “wire format” between runtimes
- Use `useSharedValue` for numbers/strings/objects that must be read/written from both UI and JS.
- Derive styles with `useAnimatedStyle`.
- Prefer `withTiming` for UI tweens; `withSpring` for physics.

### UI thread vs JS thread: the only rule that matters
- Gesture callbacks and animated styles should stay workletized (UI runtime).
- Only bridge to JS when you must (via `scheduleOnRN`).

See: [references/worklets-and-threading.md](references/worklets-and-threading.md)

### Gesture Handler: use one API style per subtree
- Default to **hook API** (`usePanGesture`, `useTapGesture`, etc.).
- Do **not** nest GestureDetectors that use different API styles (hook vs builder).
- Do **not** reuse the same gesture instance across multiple detectors.

See: [references/gestures.md](references/gestures.md)

### CSS Transitions (Reanimated 4)
Use when a style value changes due to React state/props and you just want it to animate.

Rules of thumb:
- Always set `transitionProperty` + `transitionDuration`.
- Avoid `transitionProperty: 'all'` (perf + surprise animations).
- Discrete properties (e.g. `flexDirection`) won’t transition smoothly; use Layout Animations instead.

See: [references/css-transitions-and-animations.md](references/css-transitions-and-animations.md)

### Layout animations
Use when elements enter/exit, or when layout changes due to conditional rendering/reflow.

Prefer presets first (entering/exiting, keyframes, layout transitions). Only reach for fully custom layout animations when presets can’t express the motion.

See: [references/layout-animations.md](references/layout-animations.md)

### Scroll-linked animations
Prefer Reanimated scroll handlers/shared values; keep worklet bodies tiny. For full recipes, see:

- [references/recipes.md](references/recipes.md)

## Troubleshooting checklist

1) **“Failed to create a worklet” / worklet not running**
- Ensure the correct Babel plugin is configured for your environment.
  - Expo: handled by `babel-preset-expo` when installed via `expo install`.
  - Bare RN: Reanimated 4 uses `react-native-worklets/plugin`.

2) **Gesture callbacks not firing / weird conflicts**
- Ensure the app root is wrapped with `GestureHandlerRootView`.
- Don’t reuse gestures across detectors; don’t mix hook and builder API in nested detectors.

3) **Needing to call JS from a worklet**
- Use `scheduleOnRN(fn, ...args)`.
- `fn` must be defined in JS scope (component body or module scope), not created inside a worklet.

4) **Jank / dropped frames**
- Check for large objects captured into worklets; capture primitives instead.
- Avoid `transitionProperty: 'all'`.
- Don’t set React state every frame.

See: [references/debugging-and-performance.md](references/debugging-and-performance.md)

## Bundled references (open only when needed)

- [references/setup-and-compat.md](references/setup-and-compat.md): Expo vs bare setup, New Architecture requirement, common incompatibilities.
- [references/worklets-and-threading.md](references/worklets-and-threading.md): UI runtime, `scheduleOnUI`/`scheduleOnRN`, closure capture, migration notes.
- [references/gestures.md](references/gestures.md): GestureDetector, hook API patterns, composition, gotchas.
- [references/css-transitions-and-animations.md](references/css-transitions-and-animations.md): Reanimated 4 CSS transitions/animations quick reference.
- [references/layout-animations.md](references/layout-animations.md): entering/exiting/layout transitions and how to pick.
- [references/recipes.md](references/recipes.md): copy-paste components (drag, swipe, pinch, bottom sheet-ish, scroll effects).
- [references/debugging-and-performance.md](references/debugging-and-performance.md): diagnosing worklet issues, profiling, common perf traps.

## Quick search

```bash
grep -Rni "scheduleOnRN" {baseDir}/references
grep -Rni "transitionProperty" {baseDir}/references
grep -Rni "usePanGesture" {baseDir}/references
```

## Primary docs

- Reanimated (v4): https://docs.swmansion.com/react-native-reanimated/
- Gesture Handler (latest): https://docs.swmansion.com/react-native-gesture-handler/
- Expo Reanimated: https://docs.expo.dev/versions/latest/sdk/reanimated/
- Expo Gesture Handler: https://docs.expo.dev/versions/latest/sdk/gesture-handler/
