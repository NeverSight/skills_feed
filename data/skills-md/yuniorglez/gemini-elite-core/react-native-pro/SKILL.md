---
name: react-native-pro
id: react-native-pro
version: 1.1.0
description: "Master of React Native (0.78+), specialized in the New Architecture (Fabric), React 19 Hooks, and High-Performance Mobile UX."
last_updated: "2026-01-22"
---

# Skill: React Native Pro (Standard 2026)

**Role:** The React Native Pro is a specialized mobile engineer dedicated to building "Native-Feeling" cross-platform applications. In 2026, React Native 0.78 has fully matured the New Architecture, offering synchronous layouts (Fabric), direct JSI communication, and deep integration with React 19's `use` and `Actions`.

## 🎯 Primary Objectives
1.  **Architecture Mastery:** Leveraging Fabric and TurboModules for high-fidelity rendering and native interop.
2.  **React 19 Hooks:** Utilizing `useActionState`, `useOptimistic`, and `use` to simplify complex data and UI flows.
3.  **Performance Engineering:** Mastering Reanimated 4, Skia, and the React Compiler for 120fps interfaces.
4.  **Native Integration:** Writing custom JSI modules in Rust or C++ for high-performance logic.

---

## 🏗️ The 2026 Mobile Toolbelt

### 1. Core Framework
- **React Native 0.78+:** Requiring the New Architecture by default.
- **React 19:** Native support for Actions and concurrent rendering.
- **Hermes Engine:** Optimized for fast TTI and low memory footprint.

### 2. High-Performance Libraries
- **Reanimated 4:** Worklet-based animations with zero main-thread blocking.
- **Shopify Skia:** For complex 2D graphics and shaders.
- **React Navigation 7+:** Fully typed, performance-optimized routing.

---

## 🛠️ Implementation Patterns

### 1. React 19 Actions in Mobile
Handling data submission with native pending states.

```tsx
import { useActionState } from 'react';

function ProfileForm({ updateProfile }) {
  const [state, action, isPending] = useActionState(updateProfile, null);

  return (
    <View>
      <TextInput name="username" editable={!isPending} />
      <Button onPress={action} title="Save" disabled={isPending} />
      {isPending && <ActivityIndicator />}
    </View>
  );
}
```

### 2. Optimized List Rendering (FlashList)
In 2026, `FlatList` is legacy. We use `FlashList` for near-native list performance.

```tsx
import { FlashList } from "@shopify/flash-list";

<FlashList
  data={items}
  renderItem={({ item }) => <Card item={item} />}
  estimatedItemSize={200}
/>
```

### 3. Native Drawables (Android XML)
Directly using Android Vector Drawables for crisp, high-DPI assets.

---

## 🚫 The "Do Not List" (Anti-Patterns)
1.  **NEVER** use the "Bridge" for high-frequency data (e.g., scroll events). Use **JSI** or **TurboModules**.
2.  **NEVER** perform heavy calculations on the JS main thread. Move to a **Worklet** or **Web Worker**.
3.  **NEVER** use `forwardRef`. Use React 19's direct `ref` as props.
4.  **NEVER** ignore "Cumulative Layout Shift" in mobile. Use `estimatedItemSize` for lists.

---

## 🛠️ Troubleshooting & Debugging

| Issue | Likely Cause | 2026 Corrective Action |
| :--- | :--- | :--- |
| **Dropped Frames (FPS)** | Expensive JS execution during animation | Move animation logic to `useAnimatedStyle` (Reanimated 4). |
| **Memory Leaks** | Uncleaned event listeners in Native Modules | Use `EventEmitter.remove()` and audit TurboModule lifecycle. |
| **Slow Startup (TTI)** | Large bundle size / many dependencies | Use `Lazy` loading for screens and audit `node_modules`. |
| **Layout Mismatch** | Flexbox differences between iOS/Android | Use the `inspector` and prefer `gap` over complex margins. |

---

## 📚 Reference Library
- **[New Architecture](./references/1-new-architecture.md):** Fabric & TurboModules deep dive.
- **[Performance & Reanimated 4](./references/2-performance-and-reanimated.md):** High-speed UX.
- **[Cross-Platform UX](./references/3-cross-platform-ux.md):** Designing for iOS and Android.

---

## 📊 Quality Metrics
- **Frame Rate:** Constant 60/120 fps for all transitions.
- **App Size:** < 15MB for base Squaads mobile apps.
- **TTI (Time to Interactive):** < 1.5s on mid-range devices.

---

## 🔄 Evolution from 0.70 to 0.78
- **0.72:** New Architecture improvements, stable Symlinks.
- **0.74:** Yoga 3.0, Bridgeless by default (internal).
- **0.76:** Fabric and TurboModules enabled by default.
- **0.78:** React 19 integration, Android XML Drawables.

---

**End of React Native Pro Standard (v1.1.0)**
