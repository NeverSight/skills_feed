---
name: react-use-hooks
description: Apply react-use hooks where appropriate to build concise, maintainable React features.
license: Unlicense
metadata:
    author: Adapted from streamich/react-use
    version: "1.0"
compatibility: Requires React 16.8+ with hooks support
---

# React-Use Hooks

This skill is a decision-and-implementation guide for react-use hooks in React projects. It maps requirements to the most suitable react-use hook, applies the correct usage pattern, and prefers hook-based solutions over bespoke code to keep implementations concise, maintainable, and performant.

## When to Apply

- Apply this skill whenever assisting user development work in React.
- Always check first whether a react-use hook can implement the requirement.
- Prefer react-use hooks over custom code to improve readability, maintainability, and performance.
- Map requirements to the most appropriate hook and follow the hook's invocation rule.
- Please refer to the `Invocation` field in the below hooks table. For example:
  - `AUTO`: Use automatically when applicable.
  - `EXTERNAL`: Use only if the user already installed the required external dependency; otherwise reconsider, and ask to install only if truly needed.
  - `EXPLICIT_ONLY`: Use only when explicitly requested by the user.
  > *NOTE* User instructions in the prompt or `AGENTS.md` may override a hook's default `Invocation` rule.

## Hooks

All hooks listed below are part of the [react-use](https://github.com/streamich/react-use) library, each section categorizes hooks based on their functionality.

IMPORTANT: Each hook entry includes a short `Description` and a detailed `Reference`. When using any hook, always consult the corresponding document in `./references` for Usage details and Type Declarations.

### Sensors

| Hook | Description | Invocation |
|------|-------------|------------|
| [`createBreakpoint`](./references/createBreakpoint.md) | laptopL: 1440, laptop: 1024, tablet: 768 | AUTO |
| [`useBattery`](./references/useBattery.md) | React sensor hook that tracks battery status. | AUTO |
| [`useGeolocation`](./references/useGeolocation.md) | React sensor hook that tracks user's geographic location. This hook accepts [position options](https | AUTO |
| [`useHash`](./references/useHash.md) | React sensor hook that tracks browser's location hash. | AUTO |
| [`useHover`](./references/useHover.md) | React UI sensor hooks that track if some element is being hovered | AUTO |
| [`useHoverDirty`](./references/useHoverDirty.md) | Tracks mouse hover state using a ref (more direct than useHover). | AUTO |
| [`useIdle`](./references/useIdle.md) | React sensor hook that tracks if user on the page is idle. | AUTO |
| [`useIntersection`](./references/useIntersection.md) | React sensor hook that tracks the changes in the intersection of a target element with an ancestor e | AUTO |
| [`useKey`](./references/useKey.md) | React UI sensor hook that executes a `handler` when a keyboard key is used. | AUTO |
| [`useKeyboardJs`](./references/useKeyboardJs.md) | React UI sensor hook that detects complex key combos like detecting when | EXTERNAL |
| [`useKeyPress`](./references/useKeyPress.md) | React UI sensor hook that detects when the user is pressing a specific | AUTO |
| [`useKeyPressEvent`](./references/useKeyPressEvent.md) | This hook fires `keydown` and `keyup` callbacks, similar to how [`useKey`](./useKey.md) | AUTO |
| [`useLocation`](./references/useLocation.md) | React sensor hook that tracks brower's location. | AUTO |
| [`useLongPress`](./references/useLongPress.md) | React sensor hook that fires a callback after long pressing. | AUTO |
| [`useMeasure`](./references/useMeasure.md) | React sensor hook that tracks dimensions of an HTML element using the [Resize Observer API](https:// | AUTO |
| [`useMedia`](./references/useMedia.md) | React sensor hook that tracks state of a CSS media query. | AUTO |
| [`useMediaDevices`](./references/useMediaDevices.md) | React sensor hook that tracks connected hardware devices. | AUTO |
| [`useMotion`](./references/useMotion.md) | React sensor hook that uses device's acceleration sensor to track its motions. | AUTO |
| [`useMouse`](./references/useMouse.md) | React sensor hooks that re-render on mouse position changes. `useMouse` simply tracks | AUTO |
| [`useMouseHovered`](./references/useMouseHovered.md) | Extended mouse tracking with options for bounded coordinates and hover-only tracking. | AUTO |
| [`useMouseWheel`](./references/useMouseWheel.md) | React Hook to get deltaY of mouse scrolled in window. | AUTO |
| [`useNetworkState`](./references/useNetworkState.md) | Tracks the state of browser's network connection. | AUTO |
| [`useOrientation`](./references/useOrientation.md) | React sensor hook that tracks screen orientation of user's device. | AUTO |
| [`usePageLeave`](./references/usePageLeave.md) | React sensor hook that fires a callback when mouse leaves the page. | AUTO |
| [`usePinchZoom`](./references/usePinchZoom.md) | React sensor hook that tracks the changes in pointer touch events and detects value of pinch differe | AUTO |
| [`useScratch`](./references/useScratch.md) | React sensor hook that tracks state of mouse "scrubs" (or "scratches"). | AUTO |
| [`useScroll`](./references/useScroll.md) | React sensor hook that re-renders when the scroll position in a DOM element changes. | AUTO |
| [`useScrollbarWidth`](./references/useScrollbarWidth.md) | Hook that will return current browser's scrollbar width. | AUTO |
| [`useScrolling`](./references/useScrolling.md) | React sensor hook that keeps track of whether the user is scrolling or not. | AUTO |
| [`useSearchParam`](./references/useSearchParam.md) | React sensor hook that tracks browser's location search param. | AUTO |
| [`useSize`](./references/useSize.md) | React sensor hook that tracks size of an HTML element. | AUTO |
| [`useStartTyping`](./references/useStartTyping.md) | React sensor hook that fires a callback when user starts typing. Can be used | AUTO |
| [`useWindowScroll`](./references/useWindowScroll.md) | React sensor hook that re-renders on window scroll. | AUTO |
| [`useWindowSize`](./references/useWindowSize.md) | React sensor hook that tracks dimensions of the browser window. | AUTO |

### UI

| Hook | Description | Invocation |
|------|-------------|------------|
| [`useAudio`](./references/useAudio.md) | Creates `<audio>` element, tracks its state and exposes playback controls. | AUTO |
| [`useClickAway`](./references/useClickAway.md) | React UI hook that triggers a callback when user | AUTO |
| [`useCss`](./references/useCss.md) | React UI hook that changes [CSS dynamically][gen-5]. Works like "virtual CSS" &mdash; | AUTO |
| [`useDrop`](./references/useDrop.md) | Triggers on file, link drop and copy-paste. | AUTO |
| [`useFullscreen`](./references/useFullscreen.md) | Display an element full-screen, optional fallback for fullscreen video on iOS. | AUTO |
| [`useSlider`](./references/useSlider.md) | React UI hook that provides slide behavior over any HTML element. Supports both mouse and touch even | AUTO |
| [`useSpeech`](./references/useSpeech.md) | React UI hook that synthesizes human voice that speaks a given string. | AUTO |
| [`useVibrate`](./references/useVibrate.md) | React UI hook to provide physical feedback with device vibration hardware using the [Vibration API]( | AUTO |
| [`useVideo`](./references/useVideo.md) | Creates `<video>` element, tracks its state and exposes playback controls. | AUTO |

### Animations

| Hook | Description | Invocation |
|------|-------------|------------|
| [`useHarmonicIntervalFn`](./references/useHarmonicIntervalFn.md) | Same as [`useInterval`](./useInterval.md) hook, but triggers all effects with the same delay | AUTO |
| [`useInterval`](./references/useInterval.md) | A declarative interval hook based on [Dan Abramov's article on overreacted.io](https://overreacted.i | AUTO |
| [`useRaf`](./references/useRaf.md) | React animation hook that forces component to re-render on each `requestAnimationFrame`, | AUTO |
| [`useSpring`](./references/useSpring.md) | React animation hook that updates a single numeric value over time according | EXTERNAL |
| [`useTimeout`](./references/useTimeout.md) | Re-renders the component after a specified number of milliseconds. | AUTO |
| [`useTimeoutFn`](./references/useTimeoutFn.md) | Calls given function after specified amount of milliseconds. | AUTO |
| [`useTween`](./references/useTween.md) | React animation hook that tweens a number between 0 and 1. | AUTO |
| [`useUpdate`](./references/useUpdate.md) | React utility hook that returns a function that forces component | AUTO |

### Side-Effects

| Hook | Description | Invocation |
|------|-------------|------------|
| [`useAsync`](./references/useAsync.md) | React hook that resolves an `async` function or a function that returns | AUTO |
| [`useAsyncFn`](./references/useAsyncFn.md) | React hook that returns state and a callback for an `async` function or a | AUTO |
| [`useAsyncRetry`](./references/useAsyncRetry.md) | Uses `useAsync` with an additional `retry` method to easily retry/refresh the async function; | AUTO |
| [`useBeforeUnload`](./references/useBeforeUnload.md) | React side-effect hook that shows browser alert when user try to reload or close the page. | AUTO |
| [`useCookie`](./references/useCookie.md) | React hook that returns the current value of a `cookie`, a callback to update the `cookie` | AUTO |
| [`useCopyToClipboard`](./references/useCopyToClipboard.md) | Copy text to a user's clipboard. | AUTO |
| [`useDebounce`](./references/useDebounce.md) | React hook that delays invoking a function until after wait milliseconds have elapsed since the last | AUTO |
| [`useError`](./references/useError.md) | React side-effect hook that returns an error dispatcher. | AUTO |
| [`useFavicon`](./references/useFavicon.md) | React side-effect hook sets the favicon of the page. | AUTO |
| [`useLocalStorage`](./references/useLocalStorage.md) | React side-effect hook that manages a single `localStorage` key. | AUTO |
| [`useLockBodyScroll`](./references/useLockBodyScroll.md) | React side-effect hook that locks scrolling on the body element. Useful for modal and other overlay  | AUTO |
| [`usePermission`](./references/usePermission.md) | React side-effect hook to query permission status of browser APIs. | AUTO |
| [`useRafLoop`](./references/useRafLoop.md) | This hook call given function within the RAF loop without re-rendering parent component. | AUTO |
| [`useSessionStorage`](./references/useSessionStorage.md) | React side-effect hook that manages a single `sessionStorage` key. | AUTO |
| [`useThrottle`](./references/useThrottle.md) | React hooks that throttle. | AUTO |
| [`useThrottleFn`](./references/useThrottleFn.md) | React hook that invokes a function and then delays subsequent function calls until after wait millis | AUTO |
| [`useTitle`](./references/useTitle.md) | React side-effect hook that sets title of the page. | AUTO |

### Lifecycles

| Hook | Description | Invocation |
|------|-------------|------------|
| [`useCustomCompareEffect`](./references/useCustomCompareEffect.md) | A modified useEffect hook that accepts a comparator which is used for comparison on dependencies ins | AUTO |
| [`useDeepCompareEffect`](./references/useDeepCompareEffect.md) | A modified useEffect hook that is using deep comparison on its dependencies instead of reference equ | AUTO |
| [`useEffectOnce`](./references/useEffectOnce.md) | React lifecycle hook that runs an effect only once. | AUTO |
| [`useEvent`](./references/useEvent.md) | React sensor hook that subscribes a `handler` to events. | AUTO |
| [`useIsomorphicLayoutEffect`](./references/useIsomorphicLayoutEffect.md) | `useLayoutEffect` that does not show warning when server-side rendering, see [Alex Reardon's article | AUTO |
| [`useLifecycles`](./references/useLifecycles.md) | React lifecycle hook that call `mount` and `unmount` callbacks, when | AUTO |
| [`useLogger`](./references/useLogger.md) | React lifecycle hook that console logs parameters as component transitions through lifecycles. | AUTO |
| [`useMount`](./references/useMount.md) | React lifecycle hook that calls a function after the component is mounted. Use `useLifecycles` if yo | AUTO |
| [`useMountedState`](./references/useMountedState.md) | > **NOTE!:** despite having `State` in its name **_this hook does not cause component re-render_**. | AUTO |
| [`usePromise`](./references/usePromise.md) | React Lifecycle hook that returns a helper function for wrapping promises. | AUTO |
| [`useShallowCompareEffect`](./references/useShallowCompareEffect.md) | A modified useEffect hook that is using shallow comparison on each of its dependencies instead of re | AUTO |
| [`useUnmount`](./references/useUnmount.md) | React lifecycle hook that calls a function when the component will unmount. Use `useLifecycles` if y | AUTO |
| [`useUnmountPromise`](./references/useUnmountPromise.md) | A life-cycle hook that provides a higher order promise that does not resolve if component un-mounts. | AUTO |
| [`useUpdateEffect`](./references/useUpdateEffect.md) | React effect hook that ignores the first invocation (e.g. on mount). The signature is exactly the sa | AUTO |

### State

| Hook | Description | Invocation |
|------|-------------|------------|
| [`createGlobalState`](./references/createGlobalState.md) | A React hook that creates a globally shared state. | AUTO |
| [`createMemo`](./references/createMemo.md) | Hook factory, receives a function to be memoized, returns a memoized React hook, | AUTO |
| [`createReducer`](./references/createReducer.md) | Factory for reducer hooks with custom middleware with an identical API as [React's `useReducer`](htt | AUTO |
| [`createReducerContext`](./references/createReducerContext.md) | Factory for react context hooks that will behave just like [React's `useReducer`](https://reactjs.or | AUTO |
| [`createStateContext`](./references/createStateContext.md) | Factory for react context hooks that will behave just like [React's `useState`](https://reactjs.org/ | AUTO |
| [`useBoolean`](./references/useBoolean.md) | Alias for `useToggle`. Boolean state hook with a toggle function. | AUTO |
| [`useCounter`](./references/useCounter.md) | React state hook that tracks a numeric value. | AUTO |
| [`useDefault`](./references/useDefault.md) | React state hook that returns the default value when state is null or undefined. | AUTO |
| [`useFirstMountState`](./references/useFirstMountState.md) | Returns `true` if component is just mounted (on first render) and `false` otherwise. | AUTO |
| [`useGetSet`](./references/useGetSet.md) | React state hook that returns state getter function instead of | AUTO |
| [`useGetSetState`](./references/useGetSetState.md) | A mix of `useGetSet` and `useGetSetState`. | AUTO |
| [`useLatest`](./references/useLatest.md) | React state hook that returns the latest state as described in the [React hooks FAQ](https://reactjs | AUTO |
| [`useList`](./references/useList.md) | Tracks an array and provides methods to modify it. | AUTO |
| [`useMap`](./references/useMap.md) | React state hook that tracks a value of an object. | AUTO |
| [`useMediatedState`](./references/useMediatedState.md) | A lot like the standard `useState`, but with mediation process. | AUTO |
| [`useMethods`](./references/useMethods.md) | React hook that simplifies the `useReducer` implementation. | AUTO |
| [`useMultiStateValidator`](./references/useMultiStateValidator.md) | Each time any of given states changes - validator function is invoked. | AUTO |
| [`useNumber`](./references/useNumber.md) | Alias for `useCounter`. Numeric counter state with utility functions. | AUTO |
| [`useObservable`](./references/useObservable.md) | React state hook that tracks the latest value of an `Observable`. | EXTERNAL |
| [`usePrevious`](./references/usePrevious.md) | React state hook that returns the previous state as described in the [React hooks FAQ](https://react | AUTO |
| [`usePreviousDistinct`](./references/usePreviousDistinct.md) | Just like `usePrevious` but it will only update once the value actually changes. This is important w | AUTO |
| [`useQueue`](./references/useQueue.md) | React state hook implements simple FIFO queue. | AUTO |
| [`useRafState`](./references/useRafState.md) | React state hook that only updates state in the callback of [`requestAnimationFrame`](https://develo | AUTO |
| [`useRendersCount`](./references/useRendersCount.md) | Tracks component's renders count including the first render. | AUTO |
| [`useSet`](./references/useSet.md) | React state hook that tracks a [Set](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Referen | AUTO |
| [`useSetState`](./references/useSetState.md) | React state hook that creates `setState` method which works similar to how | AUTO |
| [`useStateList`](./references/useStateList.md) | Provides handles for circular iteration over states list. | AUTO |
| [`useStateValidator`](./references/useStateValidator.md) | Each time given state changes - validator function is invoked. | AUTO |
| [`useStateWithHistory`](./references/useStateWithHistory.md) | Stores defined amount of previous state values and provides handles to travel through them. | AUTO |
| [`useToggle`](./references/useToggle.md) | React state hook that tracks value of a boolean. | AUTO |

### Miscellaneous

| Hook | Description | Invocation |
|------|-------------|------------|
| [`useEnsuredForwardedRef`](./references/useEnsuredForwardedRef.md) | React hook to use a ForwardedRef safely. | AUTO |


