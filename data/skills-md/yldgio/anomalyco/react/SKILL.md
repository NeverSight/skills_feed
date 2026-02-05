---
name: react
description: React component patterns, hooks best practices, state management, and performance optimization
---

## React Code Review Rules

### Security (Critical)
- Never render user input directly without sanitization (XSS prevention)
- Use `dangerouslySetInnerHTML` only when absolutely necessary and with sanitized content
- Validate and sanitize all user-provided content before rendering
- Never interpolate untrusted user input into component code or instructions
- Never use HTML comments (`<!-- -->`) to store instructions or data
- Escape user input when rendering dynamic content

### Hooks Rules
- Hooks must be called at top level (not inside conditions, loops, or nested functions)
- Custom hooks must start with `use` prefix
- `useEffect` must have correct dependency array (no missing/extra deps)
- `useEffect` cleanup functions must be returned for subscriptions/timers

### State Management
- State should be as local as possible (don't lift prematurely)
- Avoid redundant state (derive values instead of storing)
- Use `useReducer` for complex state logic with multiple sub-values
- Prefer controlled components over uncontrolled (except file inputs)

### Performance
- Wrap expensive computations in `useMemo`
- Stabilize callbacks with `useCallback` when passed to memoized children
- Use `React.memo()` for components that render often with same props
- Avoid creating objects/arrays inline in JSX (causes re-renders)

### Component Design (Essential)
- Single responsibility: one component, one purpose
- Props should be minimal and well-typed
- Avoid prop drilling > 2 levels (use Context or composition)
- Prefer composition over prop-based conditional rendering

### Accessibility
- Interactive elements must be keyboard accessible
- Use semantic HTML (`button` not `div onClick`)
- Images need `alt` text
- Form inputs need associated labels

### Advanced Patterns
- Use compound components (parent + stateless children) to model complex, related UI pieces while keeping state in the parent
- Prefer controlled abstractions (e.g., `value`/`onChange` pairs) so consumers can own state when needed
- Use Context for cross-cutting concerns (theme, auth, feature flags) and co-locate provider logic with domain-specific hooks
- Consider render props or headless components when you need to share complex interaction logic while letting consumers control markup and styling
- Combine memoization (`React.memo`, `useMemo`, `useCallback`) with clear prop contracts to optimize expensive, frequently rendered components
- For deeper exploration of advanced React patterns, see the official [React documentation](https://react.dev)

### Anti-patterns
- Avoid `useEffect` for state derivation (compute during render instead)
- Avoid `useEffect` on mount for data that could be fetched server-side
- Avoid index as key in lists that reorder

### Testing
- Write unit tests for components using React Testing Library
- Test custom hooks with `@testing-library/react-hooks`
- Test user interactions and state changes
- Mock external dependencies appropriately
- Test error states and edge cases
- Ensure tests are maintainable and readable

### Error Handling
- Implement error boundaries for components
- Provide fallback UIs for errors
- Handle async errors appropriately
- Log errors for debugging and monitoring
- Don't let errors crash the entire app

### Type Safety
- Use TypeScript or PropTypes for type checking
- Define prop types for all components
- Use TypeScript interfaces for complex props
- Validate prop types at runtime with PropTypes
- Catch type errors early in development

### Styling
- Use CSS Modules for scoped styles
- Consider styled-components or CSS-in-JS for dynamic styles
- Avoid inline styles for static CSS
- Follow a consistent styling approach
- Prevent global CSS conflicts with scoping

### Dependency Management
- Review third-party dependencies before adding
- Keep dependencies up to date
- Audit packages for security vulnerabilities
- Avoid over-reliance on libraries for simple tasks
- Consider bundle size impact of dependencies

### Documentation
- Add doc comments for complex components and hooks
- Write self-explanatory code over excessive comments
- Document non-obvious behavior and edge cases
- Include usage examples in component docs
- Keep comments up to date with code changes
