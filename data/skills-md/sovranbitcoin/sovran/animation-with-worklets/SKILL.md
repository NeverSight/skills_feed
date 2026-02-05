---
name: animation-with-worklets
description: Provides React Native Worklets guidelines for scheduling functions between JS and UI threads. Applies to tasks involving scheduleOnRN, scheduleOnUI, worklets, thread scheduling, useAnimatedReaction, gesture handlers, or cross-thread function calls.
---

# Worklet Scheduling

## Overview

Guidelines for scheduling functions between JavaScript and UI threads using React Native Worklets. This skill covers when and how to use `scheduleOnRN` and `scheduleOnUI`, proper function definition patterns, and avoiding unnecessary worklet directives.

## When to Apply

Reference these guidelines when:
- Scheduling functions to run on UI thread from JS thread
- Calling JS thread functions from UI thread worklets
- Working with `useAnimatedReaction` or gesture handlers
- Batching shared value updates
- Implementing cross-thread communication in animations

## Key Guidelines

### Don't Use 'worklet' Directive Unless Explicitly Asked

**Never use the `"worklet"` directive unless explicitly requested.** In 99.9% of cases, there is no need to use it. `scheduleOnUI` handles worklet conversion automatically, so the directive is unnecessary. This also applies to gesture detector callbacks - you don't need to add the `"worklet"` directive in gesture handler callbacks.

### Use scheduleOnRN and scheduleOnUI Instead of runOnJS and runOnUI

Use `scheduleOnRN` and `scheduleOnUI` from `react-native-worklets` instead of `runOnJS` and `runOnUI` from `react-native-reanimated`.

**Don't do this:**

```tsx
import { runOnJS, runOnUI } from "react-native-reanimated";
```

**Instead, do this:**

```tsx
import { scheduleOnRN, scheduleOnUI } from "react-native-worklets";
```

### Type Definitions

```tsx
function scheduleOnRN<Args extends unknown[], ReturnValue>(
  fun:
    | ((...args: Args) => ReturnValue)
    | RemoteFunction<Args, ReturnValue>
    | WorkletFunction<Args, ReturnValue>,
  ...args: Args
): void;

function scheduleOnUI<Args extends unknown[], ReturnValue>(
  fun: (...args: Args) => ReturnValue,
  ...args: Args
): void;
```

## Usage Patterns

### Always Define Functions Outside Using useCallback

Both `scheduleOnRN` and `scheduleOnUI` follow the same usage pattern: **always define the function outside using `useCallback` and pass the function reference** (not inline arrow functions).

**When to use:**

- `scheduleOnRN`: Call JavaScript thread functions from UI thread worklets (like in `useAnimatedReaction`, gesture handlers, or `useAnimatedStyle`)
- `scheduleOnUI`: Schedule functions to run on the UI thread

**Don't do this** – inline arrow function:

```tsx
// ❌ scheduleOnRN with inline function
useAnimatedReaction(
  () => currentIndex.get(),
  (nextIndex) => {
    scheduleOnRN(() => {
      setState(newValue);
    });
  }
);

// ❌ scheduleOnUI with inline function
scheduleOnUI(() => {
  scale.set(withSpring(1.2));
});
```

**Instead**, do this – define function outside:

```tsx
// ✅ scheduleOnRN - JS thread function
const updateState = useCallback(() => {
  setState(newValue);
}, [dependencies]);

useAnimatedReaction(
  () => currentIndex.get(),
  (nextIndex) => {
    scheduleOnRN(updateState); // pass function reference
  }
);

// ✅ scheduleOnUI - UI thread function
const updateAnimations = useCallback(() => {
  scale.set(withSpring(1.2));
  opacity.set(withSpring(0.8));
}, []);

scheduleOnUI(updateAnimations); // pass function reference
```

### Passing Arguments

Arguments are passed directly (not as an array) using rest parameter syntax:

```tsx
// Single argument
const updateState = useCallback((newValue: number) => {
  setState(newValue);
}, []);

scheduleOnRN(updateState, newValue); // ✅ correct

// Multiple arguments
const handleUpdate = useCallback((index: number, value: string) => {
  setState({ index, value });
}, []);

scheduleOnRN(handleUpdate, index, value); // ✅ correct - pass directly, not as array
scheduleOnUI(handleUpdate, index, value); // ✅ same pattern for scheduleOnUI
```

## Common Use Cases

### scheduleOnRN Use Cases

- React state setters (`setState`, `setExtendedSlides`, etc.)
- API calls or side effects
- Video player controls (`pause`, `resume`, `seek`)
- Haptic feedback
- Navigation functions

**Example:**

```tsx
// scheduleOnRN example
const pause = useCallback(() => {
  videoPlayerRef.current?.pause();
}, []);

useAnimatedReaction(
  () => isDragging.get(),
  (current) => {
    if (current) {
      scheduleOnRN(pause);
    }
  }
);
```

### scheduleOnUI Use Cases

- Batch multiple shared value updates in the same frame
- UI thread worklet operations

**Example:**

```tsx
// scheduleOnUI example - batch updates
const batchUpdates = useCallback(() => {
  scale.set(withSpring(1.2));
  opacity.set(withSpring(0.8));
}, []);

scheduleOnUI(batchUpdates);
```

## Benefits

- **Automatic Worklet Conversion**: `scheduleOnUI` handles worklet conversion automatically
- **Better Performance**: Batching updates reduces UI thread overhead
- **Type Safety**: Better TypeScript support with proper type definitions
- **Cleaner Code**: No need for `"worklet"` directive in most cases
- **Consistent API**: Unified approach for cross-thread communication
