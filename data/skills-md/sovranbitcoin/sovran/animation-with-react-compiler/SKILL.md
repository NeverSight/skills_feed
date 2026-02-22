---
name: animation-with-react-compiler
description: Provides React Native Reanimated guidelines for using shared values with React Compiler. Applies to tasks involving useSharedValue, shared values, React Compiler compatibility, or accessing/modifying shared value values.
---

# Animation with React Compiler

## Overview

Guidelines for using React Native Reanimated shared values with React Compiler. When using React Compiler, you must use the `get()` and `set()` methods instead of directly accessing the `value` property to ensure compatibility with React Compiler standards.

## When to Apply

Reference these guidelines when:
- Working with React Compiler enabled projects
- Using `useSharedValue` in components
- Accessing or modifying shared value values
- Ensuring React Compiler compatibility with Reanimated

## Key Guideline

### Use get() and set() Methods Instead of .value

When working with the React Compiler, you should refrain from accessing and modifying the `value` property directly. Instead, use the `get()` and `set()` methods. They're the alternative API for `useSharedValue`, compliant with the React Compiler standards.

**Don't do this** – accessing `.value` directly:

```tsx
function App() {
  const sv = useSharedValue(100);

  const animatedStyle = useAnimatedStyle(() => {
    "worklet";
    return { width: sv.value * 100 }; // ❌ Direct property access
  });

  const handlePress = () => {
    sv.value = sv.value + 1; // ❌ Direct property modification
  };
}
```

**Instead**, use `get()` and `set()` methods:

```tsx
function App() {
  const sv = useSharedValue(100);

  const animatedStyle = useAnimatedStyle(() => {
    "worklet";
    return { width: sv.get() * 100 }; // ✅ Using get() method
  });

  const handlePress = () => {
    sv.set((value) => value + 1); // ✅ Using set() method
  };
}
```

## Usage Patterns

### Reading Shared Values

```tsx
// ✅ In worklets (useAnimatedStyle, useDerivedValue, etc.)
const animatedStyle = useAnimatedStyle(() => {
  return { opacity: sv.get() };
});

// ✅ In useEffect or callbacks
useEffect(() => {
  console.log(sv.get());
}, []);
```

### Modifying Shared Values

```tsx
// ✅ Direct value assignment
sv.set(100);

// ✅ Using updater function
sv.set((currentValue) => currentValue + 1);

// ✅ With animation functions
sv.set(withSpring(1.2));
sv.set(withTiming(0.8, { duration: 300 }));
```

## Benefits

- **React Compiler Compatible**: Works seamlessly with React Compiler
- **Consistent API**: Provides a consistent method-based API
- **Type Safety**: Better TypeScript support and type inference
- **Future Proof**: Aligns with React Compiler standards and best practices

