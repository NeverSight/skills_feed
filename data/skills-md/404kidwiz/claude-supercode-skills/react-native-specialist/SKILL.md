---
name: react-native-specialist
description: Expert in React Native (New Architecture), TurboModules, Fabric, and Expo. Specializes in native module development and performance optimization.
---

# React Native Specialist

## Purpose

Provides React Native development expertise specializing in the "New Architecture" (Fabric/TurboModules), JSI, and Expo workflows. Builds high-performance cross-platform mobile applications with custom native modules and optimized JavaScript-to-native bridges.

## When to Use

- Building high-performance React Native apps with the New Architecture
- Writing custom Native Modules or View Managers (TurboModules/Fabric)
- Configuring Expo pipelines (EAS Build, Updates, Config Plugins)
- Debugging native crashes (Xcode/Android Studio) or bridge bottlenecks
- Migrating from Old Architecture (Bridge) to New Architecture (JSI)
- Integrating complex native SDKs (Maps, WebRTC, Bluetooth)

## Examples

### Example 1: New Architecture Migration

**Scenario:** Migrating a large production app from Bridge to Fabric/TurboModules.

**Implementation:**
1. Enabled New Architecture flags progressively
2. Converted Native Modules to TurboModules
3. Implemented Fabric components for complex UIs
4. Used Codegen to generate native bridge code
5. Tested thoroughly with new architecture enabled

**Results:**
- 40% faster UI rendering
- 30% smaller bundle size
- Improved type safety across native boundaries
- Better crash reporting and debugging

### Example 2: Custom Native Module

**Scenario:** Need to integrate Bluetooth Low Energy for a fitness app.

**Implementation:**
1. Created TypeScript Native Module interface
2. Implemented native code (Swift for iOS, Kotlin for Android)
3. Exposed RNTurboModule for cross-platform access
4. Added proper memory management and lifecycle handling
5. Implemented comprehensive error handling

**Results:**
- BLE operations working seamlessly on both platforms
- Type-safe bridge prevents runtime errors
- 50% less code than traditional native modules
- Maintained through RN upgrades

### Example 3: Performance Optimization

**Scenario:** App experiencing janky scrolling and memory issues.

**Implementation:**
1. Enabled Hermes engine
2. Replaced FlatList with FlashList
3. Implemented memoization (useMemo, useCallback)
4. Added lazy loading for images and heavy components
5. Optimized native bridge communication

**Results:**
- Scrolling now consistently 60fps
- Memory usage reduced by 40%
- App launch time reduced by 35%
- Crash rate reduced by 60%

## Best Practices

### Architecture

- **New Architecture**: Enable and use Fabric/TurboModules
- **Native Modules**: Use Codegen for type safety
- **Navigation**: Use React Navigation or Expo Router
- **State Management**: Choose appropriate solution (Zustand, Redux)

### Performance

- **Hermes**: Enable for better startup and runtime
- **Memoization**: Use useMemo, useCallback, React.memo
- **Lists**: Use FlashList for large lists
- **Images**: Lazy load and cache appropriately

### Native Integration

- **Lifecycle Management**: Handle app state changes
- **Error Boundaries**: Catch native errors gracefully
- **Permissions**: Request and handle gracefully
- **Testing**: Test on both platforms regularly

### Development

- **Expo Workflow**: Use Expo for faster development
- **EAS Build**: Use for CI/CD builds
- **Updates**: Use EAS Update for over-the-air updates
- **TypeScript**: Use for all code

---
---

## 2. Decision Framework

### Architecture Selection

```
Which architecture to use?
│
├─ **New Architecture (Default for 0.76+)**
│  ├─ **TurboModules:** Lazy-loaded native modules (Sync/Async).
│  ├─ **Fabric:** C++ Shadow Tree for UI (No bridge serialization).
│  ├─ **Codegen:** Type-safe spec for Native <-> JS communication.
│  └─ **Bridgeless Mode:** Removes the legacy bridge entirely.
│
└─ **Old Architecture (Legacy)**
   ├─ **Bridge:** Async JSON serialization (Slow for large data).
   └─ **Maintenance:** Only for unmigrated legacy libraries.
```

### Expo vs CLI

| Feature | Expo (Managed) | React Native CLI (Bare) |
|---------|----------------|-------------------------|
| **Setup** | Instant (`create-expo-app`) | Complex (JDK, Xcode, Pods) |
| **Native Code** | **Config Plugins** (Auto-modifies native files) | Direct file editing (`AppDelegate.m`) |
| **Upgrades** | `npx expo install --fix` (Stable sets) | Manual diffing (Upgrade Helper) |
| **Builds** | **EAS Build** (Cloud) | Local or CI (Fastlane) |
| **Updates** | **EAS Update** (OTA) | CodePush (Microsoft) |

### Performance Strategy

1.  **JSI:** Direct C++ calls. No JSON serialization.
2.  **Reanimated:** UI thread animations (Worklets).
3.  **FlashList:** Recycling views (replaces FlatList).
4.  **Hermes:** Bytecode precompilation (Instant startup).

**Red Flags → Escalate to `mobile-developer` (Native):**
- Modifying the React Native engine core (C++)
- Debugging obscure ProGuard/R8 crashes
- Writing low-level Metal/OpenGL renderers from scratch

---
---

## 3. Core Workflows

### Workflow 1: Creating a TurboModule (New Arch)

**Goal:** Access native battery level synchronously via JSI.

**Steps:**

1.  **Define Spec (`NativeBattery.ts`)**
    ```typescript
    import type { TurboModule } from 'react-native';
    import { TurboModuleRegistry } from 'react-native';

    export interface Spec extends TurboModule {
      getBatteryLevel(): number;
    }

    export default TurboModuleRegistry.getEnforcing<Spec>('RTNBattery');
    ```

2.  **Generate Code**
    -   Run `yarn codegen`. Generates C++ interfaces.

3.  **Implement iOS (`RTNBattery.mm`)**
    ```objectivec
    - (NSNumber *)getBatteryLevel {
      [UIDevice currentDevice].batteryMonitoringEnabled = YES;
      return @([UIDevice currentDevice].batteryLevel);
    }
    
    - (std::shared_ptr<facebook::react::TurboModule>)getTurboModule:
        (const facebook::react::ObjCTurboModule::InitParams &)params {
      return std::make_shared<facebook::react::NativeBatterySpecJSI>(params);
    }
    ```

4.  **Implement Android (`BatteryModule.kt`)**
    ```kotlin
    class BatteryModule(context: ReactApplicationContext) : NativeBatterySpec(context) {
      override fun getName() = "RTNBattery"
      
      override fun getBatteryLevel(): Double {
        val manager = context.getSystemService(Context.BATTERY_SERVICE) as BatteryManager
        return manager.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY).toDouble()
      }
    }
    ```

---
---

### Workflow 3: Reanimated Worklets

**Goal:** 60fps drag gesture on the UI thread.

**Steps:**

1.  **Setup**
    ```tsx
    import { useSharedValue, useAnimatedStyle, withSpring } from 'react-native-reanimated';
    import { GestureDetector, Gesture } from 'react-native-gesture-handler';
    ```

2.  **Implementation**
    ```tsx
    function Ball() {
      const offset = useSharedValue({ x: 0, y: 0 });

      const gesture = Gesture.Pan()
        .onUpdate((e) => {
          // Runs on UI thread
          offset.value = { x: e.translationX, y: e.translationY };
        })
        .onEnd(() => {
          offset.value = withSpring({ x: 0, y: 0 }); // Snap back
        });

      const style = useAnimatedStyle(() => ({
        transform: [{ translateX: offset.value.x }, { translateY: offset.value.y }]
      }));

      return (
        <GestureDetector gesture={gesture}>
          <Animated.View style={[styles.ball, style]} />
        </GestureDetector>
      );
    }
    ```

---
---

## 5. Anti-Patterns & Gotchas

### ❌ Anti-Pattern 1: "Bridge Crossing" Animations

**What it looks like:**
-   Using `Animated.timing` with `useNativeDriver: false`.
-   Calculating layout in `useEffect` and `setState`.

**Why it fails:**
-   Runs on JS thread. Drops frames if JS is busy (fetching data).

**Correct approach:**
-   Use **Reanimated** or `useNativeDriver: true`.

### ❌ Anti-Pattern 2: Large Bundles without Hermes

**What it looks like:**
-   JSC (JavaScriptCore) used on Android.
-   Startup takes 5 seconds.

**Why it fails:**
-   JSC parses JS at runtime. Hermes runs precompiled bytecode.

**Correct approach:**
-   Enable **Hermes** in `podfile` / `build.gradle` (Default in new Expo).

### ❌ Anti-Pattern 3: Styles in Render

**What it looks like:**
-   `style={{ width: 100, height: 100 }}`

**Why it fails:**
-   Creates new object every render. Forces diffing.

**Correct approach:**
-   `StyleSheet.create` or `const style = { ... }` outside component.

---
---

## 7. Quality Checklist

**Performance:**
-   [ ] **Hermes:** Enabled.
-   [ ] **Memoization:** `useMemo`/`useCallback` used for expensive props.
-   [ ] **Lists:** `FlashList` used instead of `FlatList`.

**Architecture:**
-   [ ] **New Arch:** Fabric/TurboModules enabled (if libraries support).
-   [ ] **Navigation:** Native screens used (React Navigation / Expo Router).

**Native:**
-   [ ] **Permissions:** Handled gracefully (not crashing if denied).
-   [ ] **Upgrades:** React Native version is recent (within 2 minor versions).

## Anti-Patterns

### Architecture Anti-Patterns

- **Bridge Overuse**: Heavy use of Old Architecture bridge - migrate to New Architecture
- **Unnecessary Native**: Pure JS logic wrapped in native - keep it simple
- **State Management Sprawl**: Multiple conflicting state solutions - standardize on one
- **Navigation Nesting**: Deeply nested navigators - keep navigation shallow

### Performance Anti-Patterns

- **Re-render Everything**: No React.memo or optimization - optimize component re-renders
- **FlatList Abuse**: Using FlatList for all lists - use appropriate list components
- **Memory Leaks**: Not cleaning up subscriptions - use cleanup in useEffect
- **Bridge Bottleneck**: Heavy bridge communication - minimize cross-bridge calls

### Development Anti-Patterns

- **Debug Mode in Production**: Not building for production - always test production builds
- **No Hermes**: Not using Hermes engine - enable for better performance
- **Large Bundles**: No bundle optimization - use RAM bundles and compression
- **Manual Linking**: Manual native linking when not needed - use autolinking

### Testing Anti-Patterns

- **No E2E Testing**: Only unit tests - add Maestro or Detox tests
- **Platform Conditionals**: Too many platform checks - abstract platform differences
- **Hardcoded Dimensions**: Fixed pixel values - use relative sizing
- **Missing testID**: No accessibility identifiers - add testID for testing
