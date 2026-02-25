---
name: component-architecture
description: "Load PROACTIVELY when task involves designing or building UI components. Use when user says \"build a component\", \"create a form\", \"add a modal\", \"design the layout\", or \"refactor this page\". Covers component composition and hierarchy, prop design and typing, render optimization (memo, useMemo, useCallback), compound component patterns, controlled vs uncontrolled forms, file organization, and accessibility for React, Vue, and Svelte."
metadata:
  version: 1.0.0
  category: outcome
  tags: [components, react, vue, svelte, composition, rendering, architecture, ui]
---

## Resources
```
scripts/
  validate-components.sh
references/
  component-patterns.md
```

# Component Architecture

This skill guides you through designing and implementing UI components using GoodVibes precision and analysis tools. Use this workflow when building React, Vue, or Svelte components with proper composition, state management, and performance optimization.

## When to Use This Skill

Load this skill when:
- Building new UI components or component libraries
- Refactoring component hierarchies or composition patterns
- Optimizing component render performance
- Organizing component file structures
- Implementing design systems or atomic design patterns
- Migrating between component frameworks
- Reviewing component architecture for maintainability

Trigger phrases: "build component", "create UI", "component structure", "render optimization", "state lifting", "component composition".

## Core Workflow

### Phase 1: Discovery

Before building components, understand existing patterns in the codebase.

#### Step 1.1: Map Component Structure

Use `discover` to find all component files and understand the organization pattern.

```yaml
discover:
  queries:
    - id: react_components
      type: glob
      patterns: ["**/*.tsx", "**/*.jsx"]
    - id: vue_components
      type: glob
      patterns: ["**/*.vue"]
    - id: svelte_components
      type: glob
      patterns: ["**/*.svelte"]
  verbosity: files_only
```

**What this reveals:**
- Framework in use (React, Vue, Svelte, or mixed)
- Component file organization (feature-based, atomic, flat)
- Naming conventions (PascalCase, kebab-case)
- File colocation patterns (components with tests, styles)

#### Step 1.2: Analyze Component Patterns

Use `discover` to find composition patterns, state management, and styling approaches.

```yaml
discover:
  queries:
    - id: composition_patterns
      type: grep
      pattern: "(children|render|slot|as\\s*=)"
      glob: "**/*.{tsx,jsx,vue,svelte}"
    - id: state_management
      type: grep
      pattern: "(useState|useReducer|reactive|writable|createSignal)"
      glob: "**/*.{ts,tsx,js,jsx,vue,svelte}"
    - id: styling_approach
      type: grep
      pattern: "(className|styled|css|tw`|@apply)"
      glob: "**/*.{tsx,jsx,vue,svelte}"
    - id: performance_hooks
      type: grep
      pattern: "(useMemo|useCallback|memo|computed|\\$:)"
      glob: "**/*.{ts,tsx,js,jsx,vue,svelte}"
  verbosity: files_only
```

**What this reveals:**
- Composition strategy (children props, render props, slots)
- State management patterns (hooks, stores, signals)
- Styling solution (CSS modules, Tailwind, styled-components)
- Performance optimization techniques in use

#### Step 1.3: Extract Component Symbols

Use `precision_read` with symbol extraction to understand component exports.

```yaml
precision_read:
  files:
    - path: "src/components/Button/index.tsx"  # Example component
      extract: symbols
  symbol_filter: ["function", "class", "interface", "type"]
  verbosity: standard
```

**What this reveals:**
- Component export patterns (named vs default)
- Props interface definitions
- Helper functions and hooks
- Type definitions and generics

#### Step 1.4: Read Representative Components

Read 2-3 well-structured components to understand implementation patterns.

```yaml
precision_read:
  files:
    - path: "src/components/Button/Button.tsx"
      extract: content
    - path: "src/components/Form/Form.tsx"
      extract: content
  output:
    max_per_item: 100
  verbosity: standard
```

### Phase 2: Decision Making

#### Step 2.1: Choose Component Organization Pattern

Consult `references/component-patterns.md` for the organization decision tree.

**Common patterns:**
- **Atomic Design** - atoms, molecules, organisms, templates, pages
- **Feature-based** - group by feature/domain
- **Flat** - all components in single directory
- **Hybrid** - shared components + feature components

**Decision factors:**
- Team size (larger teams -> more structure)
- Application complexity (complex -> feature-based)
- Design system presence (yes -> atomic design)
- Component reusability (high -> shared/ui directory)

#### Step 2.2: Choose Composition Pattern

See `references/component-patterns.md` for detailed comparison.

**Pattern selection guide:**

| Pattern | Use When | Framework Support |
|---------|----------|-------------------|
| Children props | Simple wrapper components | React, Vue (slots), Svelte |
| Render props | Dynamic rendering logic | React (legacy) |
| Compound components | Related components share state | React, Vue, Svelte |
| Higher-Order Components | Cross-cutting concerns | React (legacy) |
| Hooks/Composables | Logic reuse | React, Vue 3, Svelte |
| Slots | Template-based composition | Vue, Svelte |

**Modern recommendation:**
- **React**: Hooks + children props (avoid HOCs/render props)
- **Vue**: Composition API + slots
- **Svelte**: Actions + slots

#### Step 2.3: Choose State Management Strategy

**Component-level state:**
- Use local state for UI-only concerns (modals, forms, toggles)
- Lift state only when siblings need to share
- Derive state instead of duplicating

**Application-level state:**
- **React**: Context + useReducer, Zustand, Jotai
- **Vue**: Pinia (Vue 3), Vuex (Vue 2)
- **Svelte**: Stores, Context API

See `references/component-patterns.md` for state management decision tree.

### Phase 3: Implementation

#### Step 3.1: Define Component Interface

Start with TypeScript interfaces for props.

**React Example:**

```typescript
import { ReactNode } from 'react';

interface ButtonProps {
  /** Button content */
  children: ReactNode;
  /** Visual style variant */
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  /** Size preset */
  size?: 'sm' | 'md' | 'lg';
  /** Loading state */
  isLoading?: boolean;
  /** Disabled state */
  disabled?: boolean;
  /** Click handler */
  onClick?: () => void;
  /** Additional CSS classes */
  className?: string;
}
```

**Best practices:**
- Document all props with JSDoc comments
- Use discriminated unions for variant props
- Make optional props explicit with `?`
- Provide sensible defaults
- Avoid `any` types

**Vue 3 Example:**

```typescript
import { defineComponent, PropType } from 'vue';

export default defineComponent({
  props: {
    variant: {
      type: String as PropType<'primary' | 'secondary' | 'ghost' | 'danger'>,
      default: 'primary',
    },
    size: {
      type: String as PropType<'sm' | 'md' | 'lg'>,
      default: 'md',
    },
    isLoading: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
});
```

**Svelte Example:**

```typescript
// Button.svelte (Svelte 4)
<script lang="ts">
  export let variant: 'primary' | 'secondary' | 'ghost' | 'danger' = 'primary';
  export let size: 'sm' | 'md' | 'lg' = 'md';
  export let isLoading = false;
  export let disabled = false;
</script>

// Button.svelte (Svelte 5 - using $props rune)
<script lang="ts">
  let { variant = 'primary', size = 'md', isLoading = false, disabled = false }: {
    variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
    size?: 'sm' | 'md' | 'lg';
    isLoading?: boolean;
    disabled?: boolean;
  } = $props();
</script>
```

#### Step 3.2: Implement Component Logic

Follow framework-specific patterns for component implementation.

**React with Composition:**

```typescript
import { forwardRef } from 'react';
import { cn } from '@/lib/utils';
import { Spinner } from './Spinner';

const buttonVariants = {
  variant: {
    primary: 'bg-blue-600 hover:bg-blue-700 text-white',
    secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-900',
    ghost: 'hover:bg-gray-100 text-gray-700',
    danger: 'bg-red-600 hover:bg-red-700 text-white',
  },
  size: {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  },
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      children,
      variant = 'primary',
      size = 'md',
      isLoading = false,
      disabled = false,
      className,
      ...props
    },
    ref
  ) => {
    return (
      <button
        ref={ref}
        className={cn(
          'inline-flex items-center justify-center rounded-md font-medium',
          'transition-colors focus-visible:outline-none focus-visible:ring-2',
          'disabled:pointer-events-none disabled:opacity-50',
          buttonVariants.variant[variant],
          buttonVariants.size[size],
          className
        )}
        disabled={disabled || isLoading}
        aria-busy={isLoading}
        {...props}
      >
        {isLoading ? (
          <>
            <Spinner className="mr-2 h-4 w-4" aria-hidden />
            <span>Loading...</span>
          </>
        ) : (
          children
        )}
      </button>
    );
  }
);

Button.displayName = 'Button';
```

**Key patterns:**
- Use `forwardRef` to expose DOM ref
- Spread `...props` for flexibility
- Compose classNames with utility function
- Handle loading/disabled states
- Add ARIA attributes for accessibility

#### Step 3.3: Organize Component Files

Create component directory with proper file structure.

**Standard structure:**
```
components/
  Button/
    Button.tsx          # Component implementation
    Button.test.tsx     # Unit tests
    Button.stories.tsx  # Storybook stories (if using)
    index.tsx           # Barrel export
    types.ts            # Type definitions (if complex)
```

**Implementation with precision tools:**

```yaml
precision_write:
  files:
    - path: "src/components/Button/Button.tsx"
      content: |
        import { forwardRef } from 'react';
        // ... [full implementation]
    - path: "src/components/Button/index.tsx"
      content: |
        export { Button } from './Button';
        export type { ButtonProps } from './Button';
    - path: "src/components/Button/Button.test.tsx"
      content: |
        import { render, screen } from '@testing-library/react';
        import { Button } from './Button';
        // ... [test cases]
  verbosity: count_only
```

### Phase 4: State Management

#### Step 4.1: Identify State Scope

**Local state (component-only):**
- Form inputs
- Modal open/closed
- Dropdown expanded/collapsed
- Loading states

**Lifted state (parent manages):**
- Form validation across fields
- Multi-step wizard state
- Accordion with single-open behavior

**Global state (app-level):**
- User authentication
- Theme preferences
- Shopping cart
- Notifications

#### Step 4.2: Implement State Patterns

**React - Local State:**

```typescript
import { useState } from 'react';

interface SearchResult {
  id: string;
  title: string;
  description: string;
}

function SearchInput() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);

  const handleSearch = async () => {
    const data = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
    setResults(await data.json());
  };

  return (
    <>
      <input value={query} onChange={(e) => setQuery(e.target.value)} />
      <button onClick={handleSearch}>Search</button>
    </>
  );
}
```

**React - Lifted State:**

```typescript
function SearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);

  return (
    <>
      <SearchInput query={query} onQueryChange={setQuery} />
      <SearchResults results={results} />
    </>
  );
}
```

**React - Derived State:**

```typescript
interface Item {
  id: string;
  category: string;
  name: string;
}

interface FilteredListProps {
  items: Item[];
  filter: string;
}

function FilteredList({ items, filter }: FilteredListProps) {
  // Don't store filtered items in state - derive them
  const filteredItems = items.filter(item => item.category === filter);

  return <ul>{filteredItems.map(item => <li key={item.id}>{item.name}</li>)}</ul>;
}
```

#### Step 4.3: Avoid Prop Drilling

**Use Context for deeply nested props:**

```typescript
import { createContext, useContext } from 'react';

const ThemeContext = createContext({ theme: 'light', toggleTheme: () => {} });

interface ThemeProviderProps {
  children: ReactNode;
}

export function ThemeProvider({ children }: ThemeProviderProps) {
  const [theme, setTheme] = useState('light');
  const toggleTheme = () => setTheme(t => t === 'light' ? 'dark' : 'light');

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export const useTheme = () => useContext(ThemeContext);
```

### Phase 5: Performance Optimization

#### Step 5.1: Identify Render Issues

Use analysis tools to detect performance problems.

```yaml
mcp__plugin_goodvibes_frontend-engine__trace_component_state:
  component_file: "src/components/Dashboard.tsx"
  target_component: "Dashboard"
```

```yaml
mcp__plugin_goodvibes_frontend-engine__analyze_render_triggers:
  component_file: "src/components/ExpensiveList.tsx"
```

**What these reveal:**
- Components re-rendering unnecessarily
- State updates triggering cascade renders
- Props changing on every parent render

#### Step 5.2: Apply Memoization

**Memoize expensive calculations:**

```typescript
import { useMemo } from 'react';

interface DataItem {
  id: string;
  [key: string]: unknown;
}

interface DataTableProps {
  data: DataItem[];
  filters: Record<string, any>;
}

function DataTable({ data, filters }: DataTableProps) {
  const filteredData = useMemo(() => {
    return data.filter(item => matchesFilters(item, filters));
  }, [data, filters]);

  return <table>{/* render filteredData */}</table>;
}
```

**Memoize callback functions:**

```typescript
import { useCallback } from 'react';

function Parent() {
  const [count, setCount] = useState(0);

  // Prevent Child re-render when count changes
  const handleClick = useCallback(() => {
    onClick();
  }, []);

  return <Child onClick={handleClick} />;
}
```

**Memoize components:**

```typescript
import { memo } from 'react';

interface ExpensiveChildProps {
  data: DataItem[];
}

const ExpensiveChild = memo(function ExpensiveChild({ data }: ExpensiveChildProps) {
  // Only re-renders if data changes
  return <div>{/* complex rendering */}</div>;
});
```

#### Step 5.3: Implement Virtualization

For large lists, use virtualization libraries.

```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

interface VirtualListProps<T = unknown> {
  items: T[];
}

function VirtualList({ items }: VirtualListProps) {
  const parentRef = useRef(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
  });

  // Note: Inline styles acceptable here for virtualization positioning
  return (
    <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
      <div style={{ height: `${virtualizer.getTotalSize()}px` }}>
        {virtualizer.getVirtualItems().map(virtualRow => (
          <div
            key={virtualRow.index}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              transform: `translateY(${virtualRow.start}px)`,
            }}
          >
            {items[virtualRow.index].name}
          </div>
        ))}
      </div>
    </div>
  );
}
```

#### Step 5.4: Lazy Load Components

**React lazy loading:**

```typescript
import { lazy, Suspense } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <HeavyComponent />
    </Suspense>
  );
}
```

### Phase 6: Accessibility

#### Step 6.1: Semantic HTML

Use proper HTML elements instead of divs.

```typescript
// Bad
<div onClick={handleClick}>Click me</div>

// Good
<button onClick={handleClick}>Click me</button>
```

#### Step 6.2: ARIA Attributes

Add ARIA labels for screen readers.

```typescript
interface DialogProps {
  isOpen: boolean;
  onClose: () => void;
  children: ReactNode;
}

function Dialog({ isOpen, onClose, children }: DialogProps) {
  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="dialog-title"
      aria-describedby="dialog-description"
    >
      <h2 id="dialog-title">Dialog Title</h2>
      <div id="dialog-description">{children}</div>
      <button onClick={onClose} aria-label="Close dialog">
        X
      </button>
    </div>
  );
}
```

#### Step 6.3: Keyboard Navigation

Ensure all interactive elements are keyboard-accessible.

```typescript
function Dropdown() {
  const [isOpen, setIsOpen] = useState(false);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLButtonElement>) => {
    if (e.key === 'Escape') setIsOpen(false);
    if (e.key === 'Enter' || e.key === ' ') setIsOpen(!isOpen);
  };

  return (
    <div>
      <button
        onClick={() => setIsOpen(!isOpen)}
        onKeyDown={handleKeyDown}
        aria-expanded={isOpen}
        aria-haspopup="true"
      >
        Menu
      </button>
      {isOpen && <div role="menu">{/* menu items */}</div>}
    </div>
  );
}
```

#### Step 6.4: Validate Accessibility

Use frontend analysis tools to check accessibility.

```yaml
mcp__plugin_goodvibes_frontend-engine__get_accessibility_tree:
  component_file: "src/components/Dialog.tsx"
```

### Phase 7: Validation

#### Step 7.1: Type Check

Verify TypeScript compilation.

```yaml
precision_exec:
  commands:
    - cmd: "npm run typecheck"
      expect:
        exit_code: 0
  verbosity: minimal
```

#### Step 7.2: Run Component Validation Script

Use the validation script to ensure quality.

```bash
bash plugins/goodvibes/skills/outcome/component-architecture/scripts/validate-components.sh .
```

See `scripts/validate-components.sh` for the complete validation suite.

#### Step 7.3: Visual Regression Testing

If using Storybook or similar, run visual tests.

```yaml
precision_exec:
  commands:
    - cmd: "npm run test:visual"
      expect:
        exit_code: 0
  verbosity: minimal
```

## Common Anti-Patterns

**DON'T:**
- Store derived state (calculate from existing state)
- Mutate props or state directly
- Use index as key for dynamic lists
- Create new objects/functions in render
- Skip prop validation or TypeScript types
- Use `any` types for component props
- Mix presentation and business logic
- Ignore accessibility (ARIA, keyboard nav)
- Over-optimize (premature memoization)

**DO:**
- Derive state from props when possible
- Treat props and state as immutable
- Use stable, unique keys for list items
- Define functions outside render or use `useCallback`
- Define strict prop types with TypeScript
- Separate container (logic) from presentational components
- Add ARIA attributes for custom components
- Measure before optimizing (React DevTools Profiler)

## Quick Reference

**Discovery Phase:**
```yaml
discover: { queries: [components, patterns, state, styling], verbosity: files_only }
precision_read: { files: [example components], extract: symbols }
```

**Implementation Phase:**
```yaml
precision_write: { files: [Component.tsx, index.tsx, types.ts], verbosity: count_only }
```

**Performance Analysis:**
```yaml
trace_component_state: { component_file: "src/...", target_component: "Name" }
analyze_render_triggers: { component_file: "src/..." }
```

**Accessibility Check:**
```yaml
get_accessibility_tree: { component_file: "src/..." }
```

**Validation Phase:**
```yaml
precision_exec: { commands: [{ cmd: "npm run typecheck" }] }
```

**Post-Implementation:**
```bash
bash scripts/validate-components.sh .
```

For detailed patterns, framework comparisons, and decision trees, see `references/component-patterns.md`.

## Related Skills

Consider using these complementary GoodVibes skills:

- **styling-system** - Design system tokens, theme architecture, and CSS-in-JS patterns
- **state-management** - Global state patterns, store architecture, and data flow
- **testing-strategy** - Component testing, visual regression, and accessibility testing
- **performance-audit** - Bundle analysis, render profiling, and optimization strategies
- **accessibility-audit** - WCAG compliance, screen reader testing, and ARIA patterns
