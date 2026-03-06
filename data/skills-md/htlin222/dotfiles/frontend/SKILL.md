---
name: frontend
description: Build React components, responsive layouts, and handle state management. Use for UI development, styling, or frontend performance.
---

# Frontend Development

Build modern, accessible, performant frontend applications.

## When to Use

- Creating UI components
- Implementing responsive designs
- State management setup
- Frontend performance optimization
- Accessibility improvements

## Focus Areas

### Component Architecture

- Functional components with hooks
- Props interface with TypeScript
- Composition over inheritance
- Reusable, testable components

### Styling

- Tailwind CSS or CSS-in-JS
- Mobile-first responsive design
- Design system integration
- Dark mode support

### State Management

- React Context for simple state
- Zustand/Redux for complex state
- Server state with React Query/SWR

### Performance

- Lazy loading and code splitting
- Memoization (useMemo, useCallback)
- Virtual lists for large datasets
- Image optimization

### Accessibility

- Semantic HTML
- ARIA labels where needed
- Keyboard navigation
- Screen reader testing

## Component Template

```tsx
interface Props {
  title: string;
  onAction?: () => void;
}

export function Component({ title, onAction }: Props) {
  return (
    <div role="region" aria-label={title}>
      <h2>{title}</h2>
      <button onClick={onAction}>Action</button>
    </div>
  );
}
```

## Performance Budgets

- Load time: <3s on 3G, <1s on WiFi
- Bundle: <500KB initial
- LCP: <2.5s, FID: <100ms, CLS: <0.1

## Examples

**Input:** "Create a search component"
**Action:** Build accessible search with debounced input, loading states, results display

**Input:** "Make this responsive"
**Action:** Add breakpoints, mobile-first styles, test on multiple viewports
