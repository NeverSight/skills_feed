---
name: reactive-polling
description: Poll for changes to any value and trigger React re-renders when it changes.
---

# Reactive Polling

Poll for changes to any value and trigger React re-renders when it changes.

## Technique

Create a `useReactive` hook that uses `useFrame` to periodically check a selector function. When the value changes, update React state to trigger a re-render. Throttle with a configurable FPS.

## Key Concepts

- Selector function returns the value to watch
- Compare with previous value to detect changes
- Only update state when value actually changes
- Throttle polling with `useFrame`'s `fps` option
- Use sparingly for values that don't change frequently

## Usage

```tsx
const useReactive = <T,>(selector: () => T, fps = 30): T => {
  const [reactiveValue, setReactiveValue] = useState<T>(selector())
  const previousValueRef = useRef(reactiveValue)

  useFrame(
    () => {
      const newValue = selector()
      if (previousValueRef.current !== newValue) {
        previousValueRef.current = newValue
        setReactiveValue(newValue)
      }
    },
    { fps }
  )

  return reactiveValue
}

// Usage
const isAboveZero = useReactive(() => position.y > 0)
```

---

This skill is part of [verekia](https://x.com/verekia)'s [**r3f-gamedev**](https://github.com/verekia/r3f-gamedev).
