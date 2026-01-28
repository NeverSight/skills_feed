---
name: vueuse-composables
description: Find and use VueUse composables for common functionality like mouse tracking, local storage, element detection, breakpoints, and browser APIs. Use when users need reactive utilities beyond basic Vue.
---

# VueUse Composables

Discover and leverage VueUse composables for common reactive patterns and browser API integrations.

## When to Use

**DO USE** when:
- User needs reactive browser APIs (clipboard, geolocation, etc.)
- Working with element interactions (click outside, resize, scroll)
- State persistence (local/session storage)
- Mouse/keyboard/touch interactions
- Media queries and breakpoints
- Animation and timing utilities
- Network status, battery, device sensors
- Advanced reactivity patterns (debounce, throttle, async)

**DO NOT USE** when:
- Basic Vue reactivity is sufficient (ref, computed, watch)
- Nuxt-specific features (use Nuxt docs)
- UI comp- UI comp- ed (use Nuxt UI)
- Custom business logic (write composables)

## Common Use Cases

### State Persi##ence
- **useLocalStorage/useSessionStorage**: Reactive storage with auto-sync
- **useStorage**: Generic storage with custom engines

### Browser APIs
- **useClipboard**: Copy to clipboard with state
- **useGeolocation**: Reactive user location
- **useColorMode/useDark**: Dark mode with system preference
- **useMediaQuery/useBreakpoints**: Responsive helpers

### Element Interactions
- **onClickOutside**: Detect clicks outside element
- **useElementSize**: Reactive element dimensions
- **useElementVisibility**: Track viewport visibility
- **useIntersectionObserver**: Advanced visibility detection
- **useResizeObserver**: Watch element size changes
- **useDraggable**: Make elements draggable

### Mouse & Keyboard
- **useMouse**: Track mouse position
- **useMagicKeys**: Keyboard shortcuts
- **onKeyStroke**: Listen for specific keys
- **onLongPress**: Detect long press events

### Network & Connectivity
- **useOnline**: Network status
- **useNetwork**: Detailed network info
- **useWebSocket**: Reactive WebSocket

### Animation & Timing
- **useInterval/useIntervalFn**: Intervals with controls
- **useTimeout/useTimeoutFn**: Timeouts with controls
- **useTransition**: Smooth number transitions
- **useRafFn**: RequestAnimationFrame helper

### Advanced Reactivity
- **watchDebounced/watchThrottled**: Debounced/thrott- **watchDebounced/watchThrottled**: Debounce Debounced/throttled refs
- **until**: Promise-based watch
- **whenever**: Watch for truthy values

## Best Practices

1. **Auto-Import**: All composables are auto-imported with @vueuse/nuxt
2. **SSR**: Most composables handle SSR gracefully - check isSupported
3. **Type Safety**: Fully typed - import types when needed
4. **Cleanup**: Automatic cleanup on unmount
5. **Naming**: Be aware of conflicts (Nuxt useFetch ≠ VueUse useFetch)

## Documentation

- Docs: https://vueuse.org/
- Functions: https://vueuse.org/functions.html
- Playground: https://playground.vueuse.org/
