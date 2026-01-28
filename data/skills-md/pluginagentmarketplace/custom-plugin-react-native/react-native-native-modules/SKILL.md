---
name: react-native-native-modules
description: Master native modules - Turbo Modules, JSI, Fabric, and platform bridging
sasmp_version: "1.3.0"
bonded_agent: 04-react-native-native
bond_type: PRIMARY_BOND
version: "2.0.0"
updated: "2025-01"
---

# React Native Native Modules Skill

> Learn to build native modules for iOS and Android using Turbo Modules, JSI, and the new architecture.

## Prerequisites

- React Native intermediate knowledge
- Basic iOS (Swift/Objective-C) or Android (Kotlin/Java)
- Understanding of async/sync patterns

## Learning Objectives

After completing this skill, you will be able to:
- [ ] Create native modules for iOS and Android
- [ ] Implement Turbo Modules with Codegen
- [ ] Bridge third-party SDKs
- [ ] Handle native events
- [ ] Debug native code issues

---

## Topics Covered

### 1. Turbo Module Spec
```typescript
// specs/NativeCalculator.ts
import type { TurboModule } from 'react-native';
import { TurboModuleRegistry } from 'react-native';

export interface Spec extends TurboModule {
  add(a: number, b: number): number;           // Sync
  multiply(a: number, b: number): Promise<number>; // Async
}

export default TurboModuleRegistry.getEnforcing<Spec>('Calculator');
```

### 2. iOS Implementation (Swift)
```swift
@objc(Calculator)
class Calculator: NSObject {
  @objc static func requiresMainQueueSetup() -> Bool { false }

  @objc func add(_ a: Double, b: Double) -> Double {
    return a + b
  }

  @objc func multiply(_ a: Double, b: Double,
    resolve: @escaping RCTPromiseResolveBlock,
    reject: @escaping RCTPromiseRejectBlock) {
    resolve(a * b)
  }
}
```

### 3. Android Implementation (Kotlin)
```kotlin
@ReactModule(name = "Calculator")
class CalculatorModule(reactContext: ReactApplicationContext) :
    ReactContextBaseJavaModule(reactContext) {

  override fun getName() = "Calculator"

  @ReactMethod(isBlockingSynchronousMethod = true)
  fun add(a: Double, b: Double): Double = a + b

  @ReactMethod
  fun multiply(a: Double, b: Double, promise: Promise) {
    promise.resolve(a * b)
  }
}
```

### 4. Native Events
```typescript
import { NativeEventEmitter, NativeModules } from 'react-native';

const { MyModule } = NativeModules;
const emitter = new NativeEventEmitter(MyModule);

// Subscribe
const subscription = emitter.addListener('onProgress', (data) => {
  console.log('Progress:', data.percent);
});

// Cleanup
subscription.remove();
```

### 5. When to Use Native Modules

| Scenario | Solution |
|----------|----------|
| Access native APIs | Native module |
| Performance-critical | JSI/Turbo Module |
| Third-party SDK | Bridge wrapper |
| UI component | Fabric component |

---

## Quick Start Example

```typescript
// JavaScript usage
import NativeCalculator from './specs/NativeCalculator';

// Sync call (blocks JS thread briefly)
const sum = NativeCalculator.add(5, 3);
console.log('Sum:', sum); // 8

// Async call (non-blocking)
const product = await NativeCalculator.multiply(5, 3);
console.log('Product:', product); // 15
```

---

## Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| "Module not found" | Not linked | Run `pod install` |
| Crash on sync | Main thread | Use async or background |
| Type mismatch | Codegen issue | Regenerate specs |

---

## Validation Checklist

- [ ] Module loads on both platforms
- [ ] Sync methods don't block UI
- [ ] Async methods resolve correctly
- [ ] Events fire and cleanup properly

---

## Usage

```
Skill("react-native-native-modules")
```

**Bonded Agent**: `04-react-native-native`
