---
name: react-guidelines
description: Crucial info when dealing with a React project, these guidelines must always be followed in react contexts.
---

# React Guidelines

This document outlines best practices for building robust, maintainable, and modern React applications with TypeScript.

## 1. General Principles

- **Component Composition**: Build small, focused components and compose them to build complex UIs.
- **Unidirectional Data Flow**: Data flows down (props), actions flow up (callbacks).
- **Immutability**: Treat state as immutable. Use functional updates and immutable patterns.
- **Colocation**: Keep related logic, styles, and tests close to the component.

## 2. TypeScript Integration

- **Strict Typing**: Always use `strict: true` in `tsconfig.json`. avoiding `any` ensures type safety.
- **Props Interfaces**: Define explicit interfaces for component props.

  ```tsx
  interface ButtonProps {
      label: string;
      onClick: () => void;
      variant?: 'primary' | 'secondary';
  }
  ```

- **Discriminated Unions**: Use discriminated unions for state that can be in distinct modes (e.g., handling loading/success/error states).

  ```tsx
  type State = 
      | { status: 'idle' }
      | { status: 'loading' }
      | { status: 'success'; data: User }
      | { status: 'error'; error: Error };
  ```

- **Event Types**: Use React's built-in event types (e.g., `React.ChangeEvent<HTMLInputElement>`, `React.FormEvent`).

## 3. State Management Best Practices

### Derived State (Crucial)

- **Avoid Redundant State**: **Do not** store state that can be calculated from existing props or other state.
- **Calculate on Render**: Compute values directly in the component body.
  - *Bad*:

    ```tsx
    const [filteredList, setFilteredList] = useState([]);
    
    // This is an anti-pattern: syncing state
    useEffect(() => {
        setFilteredList(items.filter(i => i.active));
    }, [items]);
    ```

  - *Good*:

    ```tsx
    // Calculated during render. Always fresh, no sync bugs.
    const filteredList = items.filter(i => i.active); 
    ```

- **Memoization**: Use `useMemo` only if the calculation is computationally expensive.

### useState vs useReducer

- Use `useState` for simple, independent values.
- Use `useReducer` for complex state logic, or when the next state depends on the previous one in complex ways.

## 4. useEffect Usage and Pitfalls

- **Synchronization, Not Data Flow**: `useEffect` is for synchronizing with external systems (APIs, DOM, subscriptions). It is **not** for transforming data or "watching" props to update state.
- **Fetching Data**: When fetching data, handle race conditions (e.g., ignore results if the component unmounts or the query changes).
- **Strict Dependencies**: Always include all variables used in the effect in the dependency array.
- **Cleanup Functions**: Always return a cleanup function for effects that create subscriptions or event listeners.

## 5. Component Patterns

- **Custom Hooks**: Extract logic into custom hooks (`useUser`, `useWindowSize`). This keeps components focused on UI.
- **Container/Presentational**: While strictly rigidly separating them is less common now, separating logically complex data-fetching components from pure UI components is still good practice.
- **Fragments**: Use `<>` (Fragments) to avoid unnecessary DOM wrapper nodes.

## 6. Performance

- **Stable Identity**: Wrap functions passed as props in `useCallback` *only if* the child component is wrapped in `React.memo` or if the function is a dependency of minimal effect.
- **Lists**: Always use a unique, stable `key` for list items. Do not use array index.
- **Lazy Loading**: Use `React.lazy` and `Suspense` for route-level code splitting.
