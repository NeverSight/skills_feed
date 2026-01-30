---
name: react-use
description: Collection of essential React Hooks for sensors, UI, animations, side-effects, lifecycles, and state management
metadata:
  author: Hairyf
  version: "2026.1.29"
  source: Generated from https://github.com/streamich/react-use, scripts located at https://github.com/hairyf/skills
---

# react-use

> The skill is based on react-use v17.6.0, generated at 2026-01-29.

react-use is a collection of essential React Hooks that provide ready-to-use functionality for common patterns in React applications. It includes hooks for sensors, UI interactions, animations, side-effects, lifecycle management, and state management.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Usage | Import patterns and tree-shaking recommendations | [core-usage](references/core-usage.md) |

## Sensors

Sensor hooks listen to changes in browser APIs and device interfaces, forcing components to re-render with updated state.

| Topic | Description | Reference |
|-------|-------------|-----------|
| useBattery | Tracks device battery status | [sensors-battery](references/sensors-battery.md) |
| useGeolocation | Tracks geo location state of user's device | [sensors-geolocation](references/sensors-geolocation.md) |
| useHover | Tracks mouse hover state of an element | [sensors-hover](references/sensors-hover.md) |
| useHash | Tracks location hash value | [sensors-hash](references/sensors-hash.md) |
| useIdle | Tracks whether user is being inactive | [sensors-idle](references/sensors-idle.md) |
| useIntersection | Tracks an HTML element's intersection | [sensors-intersection](references/sensors-intersection.md) |
| useKey | Tracks key presses | [sensors-key](references/sensors-key.md) |
| useKeyPress | Tracks key press state | [sensors-key-press](references/sensors-key-press.md) |
| useKeyPressEvent | Handles key press events | [sensors-key-press-event](references/sensors-key-press-event.md) |
| useKeyboardJs | Tracks keyboard key combinations | [sensors-keyboard-js](references/sensors-keyboard-js.md) |
| useLocation | Tracks page navigation bar location state | [sensors-location](references/sensors-location.md) |
| useSearchParam | Tracks URL search parameters | [sensors-search-param](references/sensors-search-param.md) |
| useLongPress | Tracks long press gesture | [sensors-long-press](references/sensors-long-press.md) |
| useMedia | Tracks state of a CSS media query | [sensors-media](references/sensors-media.md) |
| useMediaDevices | Tracks state of connected hardware devices | [sensors-media-devices](references/sensors-media-devices.md) |
| useMotion | Tracks state of device's motion sensor | [sensors-motion](references/sensors-motion.md) |
| useMouse | Tracks state of mouse position | [sensors-mouse](references/sensors-mouse.md) |
| useMouseWheel | Tracks deltaY of scrolled mouse wheel | [sensors-mouse-wheel](references/sensors-mouse-wheel.md) |
| useNetworkState | Tracks browser's network connection state | [sensors-network-state](references/sensors-network-state.md) |
| useOrientation | Tracks device's screen orientation | [sensors-orientation](references/sensors-orientation.md) |
| usePageLeave | Triggers when mouse leaves page boundaries | [sensors-page-leave](references/sensors-page-leave.md) |
| useScratch | Tracks mouse click-and-scrub state | [sensors-scratch](references/sensors-scratch.md) |
| useScroll | Tracks an HTML element's scroll position | [sensors-scroll](references/sensors-scroll.md) |
| useScrolling | Tracks whether HTML element is scrolling | [sensors-scrolling](references/sensors-scrolling.md) |
| useStartTyping | Detects when user starts typing | [sensors-start-typing](references/sensors-start-typing.md) |
| useWindowScroll | Tracks Window scroll position | [sensors-window-scroll](references/sensors-window-scroll.md) |
| useWindowSize | Tracks Window dimensions | [sensors-window-size](references/sensors-window-size.md) |
| useMeasure | Tracks an HTML element's dimensions | [sensors-measure](references/sensors-measure.md) |
| useSize | Tracks element size | [sensors-size](references/sensors-size.md) |
| createBreakpoint | Tracks innerWidth with breakpoints | [sensors-breakpoint](references/sensors-breakpoint.md) |
| useScrollbarWidth | Detects browser's native scrollbars width | [sensors-scrollbar-width](references/sensors-scrollbar-width.md) |
| usePinchZoom | Tracks pointer events to detect pinch zoom | [sensors-pinch-zoom](references/sensors-pinch-zoom.md) |

## UI

UI hooks allow you to control and subscribe to state changes of UI elements.

| Topic | Description | Reference |
|-------|-------------|-----------|
| useAudio | Plays audio and exposes its controls | [ui-audio](references/ui-audio.md) |
| useClickAway | Triggers callback when user clicks outside target area | [ui-click-away](references/ui-click-away.md) |
| useCss | Dynamically adjusts CSS | [ui-css](references/ui-css.md) |
| useDrop | Tracks file, link and copy-paste drops | [ui-drop](references/ui-drop.md) |
| useFullscreen | Display an element or video full-screen | [ui-fullscreen](references/ui-fullscreen.md) |
| useSlider | Provides slide behavior over any HTML element | [ui-slider](references/ui-slider.md) |
| useSpeech | Synthesizes speech from a text string | [ui-speech](references/ui-speech.md) |
| useVibrate | Provides physical feedback using Vibration API | [ui-vibrate](references/ui-vibrate.md) |
| useVideo | Plays video, tracks its state, and exposes playback controls | [ui-video](references/ui-video.md) |

## Animations

Animation hooks usually interpolate numeric values over time.

| Topic | Description | Reference |
|-------|-------------|-----------|
| useRaf | Re-renders component on each requestAnimationFrame | [animations-raf](references/animations-raf.md) |
| useInterval | Re-renders component on a set interval | [animations-interval](references/animations-interval.md) |
| useHarmonicIntervalFn | Harmonic interval function | [animations-harmonic-interval](references/animations-harmonic-interval.md) |
| useSpring | Interpolates number over time according to spring dynamics | [animations-spring](references/animations-spring.md) |
| useTimeout | Re-renders component after a timeout | [animations-timeout](references/animations-timeout.md) |
| useTimeoutFn | Calls given function after a timeout | [animations-timeout-fn](references/animations-timeout-fn.md) |
| useTween | Re-renders component while tweening a number from 0 to 1 | [animations-tween](references/animations-tween.md) |
| useUpdate | Returns a callback which re-renders component when called | [animations-update](references/animations-update.md) |

## Side-effects

Side-effect hooks allow your app to trigger various side-effects using browser's API.

| Topic | Description | Reference |
|-------|-------------|-----------|
| useAsync | Resolves an async function | [side-effects-async](references/side-effects-async.md) |
| useAsyncFn | Async function with manual execution | [side-effects-async-fn](references/side-effects-async-fn.md) |
| useAsyncRetry | Async function with retry capability | [side-effects-async-retry](references/side-effects-async-retry.md) |
| useBeforeUnload | Shows browser alert when user tries to reload or close the page | [side-effects-before-unload](references/side-effects-before-unload.md) |
| useCookie | Provides way to read, update and delete a cookie | [side-effects-cookie](references/side-effects-cookie.md) |
| useCopyToClipboard | Copies text to clipboard | [side-effects-copy-to-clipboard](references/side-effects-copy-to-clipboard.md) |
| useDebounce | Debounces a function | [side-effects-debounce](references/side-effects-debounce.md) |
| useError | Error dispatcher | [side-effects-error](references/side-effects-error.md) |
| useFavicon | Sets favicon of the page | [side-effects-favicon](references/side-effects-favicon.md) |
| useLocalStorage | Manages a value in localStorage | [side-effects-local-storage](references/side-effects-local-storage.md) |
| useSessionStorage | Manages a value in sessionStorage | [side-effects-session-storage](references/side-effects-session-storage.md) |
| useLockBodyScroll | Locks scrolling of the body element | [side-effects-lock-body-scroll](references/side-effects-lock-body-scroll.md) |
| useRafLoop | Calls given function inside the RAF loop | [side-effects-raf-loop](references/side-effects-raf-loop.md) |
| useThrottle | Throttles a function | [side-effects-throttle](references/side-effects-throttle.md) |
| useThrottleFn | Throttle function variant | [side-effects-throttle-fn](references/side-effects-throttle-fn.md) |
| useTitle | Sets title of the page | [side-effects-title](references/side-effects-title.md) |
| usePermission | Query permission status for browser APIs | [side-effects-permission](references/side-effects-permission.md) |

## Lifecycles

Lifecycle hooks modify and extend built-in React hooks or imitate React Class component lifecycle patterns.

| Topic | Description | Reference |
|-------|-------------|-----------|
| useEffectOnce | Modified useEffect that only runs once | [lifecycles-effect-once](references/lifecycles-effect-once.md) |
| useEvent | Subscribe to events | [lifecycles-event](references/lifecycles-event.md) |
| useLifecycles | Calls mount and unmount callbacks | [lifecycles-lifecycles](references/lifecycles-lifecycles.md) |
| useMountedState | Tracks if component is mounted | [lifecycles-mounted-state](references/lifecycles-mounted-state.md) |
| useUnmountPromise | Track if component is mounted with promise support | [lifecycles-unmount-promise](references/lifecycles-unmount-promise.md) |
| usePromise | Resolves promise only while component is mounted | [lifecycles-promise](references/lifecycles-promise.md) |
| useLogger | Logs in console as component goes through life-cycles | [lifecycles-logger](references/lifecycles-logger.md) |
| useMount | Calls mount callbacks | [lifecycles-mount](references/lifecycles-mount.md) |
| useUnmount | Calls unmount callbacks | [lifecycles-unmount](references/lifecycles-unmount.md) |
| useUpdateEffect | Run an effect only on updates | [lifecycles-update-effect](references/lifecycles-update-effect.md) |
| useIsomorphicLayoutEffect | useLayoutEffect that works on server | [lifecycles-isomorphic-layout-effect](references/lifecycles-isomorphic-layout-effect.md) |
| useDeepCompareEffect | useEffect with deep comparison | [lifecycles-deep-compare-effect](references/lifecycles-deep-compare-effect.md) |
| useShallowCompareEffect | useEffect with shallow comparison | [lifecycles-shallow-compare-effect](references/lifecycles-shallow-compare-effect.md) |
| useCustomCompareEffect | useEffect with custom comparison function | [lifecycles-custom-compare-effect](references/lifecycles-custom-compare-effect.md) |

## State

State hooks allow you to easily manage state of booleans, arrays, and maps.

| Topic | Description | Reference |
|-------|-------------|-----------|
| createMemo | Factory of memoized hooks | [state-create-memo](references/state-create-memo.md) |
| createReducer | Factory of reducer hooks with custom middleware | [state-create-reducer](references/state-create-reducer.md) |
| createReducerContext | Factory of hooks for sharing state between components | [state-create-reducer-context](references/state-create-reducer-context.md) |
| createStateContext | Factory of hooks for sharing state between components | [state-create-state-context](references/state-create-state-context.md) |
| createGlobalState | Cross component shared state | [state-create-global-state](references/state-create-global-state.md) |
| useDefault | Returns the default value when state is null or undefined | [state-default](references/state-default.md) |
| useGetSet | Returns state getter get() instead of raw state | [state-get-set](references/state-get-set.md) |
| useGetSetState | Combination of useGetSet and useSetState | [state-get-set-state](references/state-get-set-state.md) |
| useLatest | Returns the latest state or props | [state-latest](references/state-latest.md) |
| usePrevious | Returns the previous state or props | [state-previous](references/state-previous.md) |
| usePreviousDistinct | Like usePrevious but with a predicate | [state-previous-distinct](references/state-previous-distinct.md) |
| useObservable | Tracks latest value of an Observable | [state-observable](references/state-observable.md) |
| useRafState | Creates setState method which only updates after requestAnimationFrame | [state-raf-state](references/state-raf-state.md) |
| useSetState | Creates setState method which works like this.setState | [state-set-state](references/state-set-state.md) |
| useToggle | Tracks state of a boolean | [state-toggle](references/state-toggle.md) |
| useCounter | Tracks state of a number | [state-counter](references/state-counter.md) |
| useList | Tracks state of an array | [state-list](references/state-list.md) |
| useMap | Tracks state of an object | [state-map](references/state-map.md) |
| useSet | Tracks state of a Set | [state-set](references/state-set.md) |
| useQueue | Implements simple queue | [state-queue](references/state-queue.md) |
| useStateList | Circularly iterates over an array | [state-state-list](references/state-state-list.md) |
| useStateValidator | Validates state with a validator function | [state-state-validator](references/state-state-validator.md) |
| useStateWithHistory | Stores previous state values and provides handles to travel through them | [state-state-with-history](references/state-state-with-history.md) |
| useMultiStateValidator | Alike useStateValidator but tracks multiple states | [state-multi-state-validator](references/state-multi-state-validator.md) |
| useMediatedState | Like regular useState but with mediation by custom function | [state-mediated-state](references/state-mediated-state.md) |
| useFirstMountState | Check if current render is first | [state-first-mount-state](references/state-first-mount-state.md) |
| useRendersCount | Count component renders | [state-renders-count](references/state-renders-count.md) |
| useMethods | Neat alternative to useReducer | [state-methods](references/state-methods.md) |

## Miscellaneous

| Topic | Description | Reference |
|-------|-------------|-----------|
| useEnsuredForwardedRef | Use a React.forwardedRef safely | [misc-ensured-forwarded-ref](references/misc-ensured-forwarded-ref.md) |
