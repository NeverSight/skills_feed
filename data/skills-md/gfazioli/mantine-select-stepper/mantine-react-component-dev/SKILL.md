---
name: mantine-react-component-dev
description: Development guidelines and patterns for building React component libraries with Mantine UI, TypeScript, and modern tooling. Use this skill when creating, editing, or maintaining Mantine-based React components, implementing Styles API patterns, managing component composition, or working with TypeScript-safe component factories.
---

# Mantine React Component Development Skill

## When to Use This Skill

Apply this skill when working on:

- **Component Development**: Creating or editing React components built on Mantine's factory pattern
- **TypeScript Patterns**: Implementing polymorphic components, type-safe props, and CSS variables
- **Styles API**: Configuring component styling through Mantine's Styles API system (selectors, vars, modifiers)
- **Component Composition**: Building compound components with static sub-components (e.g., `Component.Target`)
- **Context Management**: Implementing safe context patterns for component state sharing
- **Accessibility**: Ensuring ARIA compliance, keyboard navigation, and focus management
- **Code Review**: Maintaining consistency with established patterns and conventions
- **Documentation**: Writing component demos, MDX docs, and API references

## Project Structure

Components are organized in a monorepo workspace structure:

- **`/package/src/`**: Main component source code
  - `ComponentName.tsx`: Main component implementation
  - `ComponentName.module.css`: Component-scoped styles
  - `ComponentName.context.ts`: Context providers (if needed)
  - `ComponentName.errors.ts`: Error messages
  - `ComponentName.test.tsx`: Jest + Testing Library tests
  - `ComponentName.story.tsx`: Storybook stories
  - `SubComponent/SubComponent.tsx`: Sub-components in their own folders
  - `index.ts`: Public exports

- **`/docs/`**: Next.js documentation site
  - `demos/ComponentName.demo.*.tsx`: Interactive demos
  - `styles-api/ComponentName.styles-api.ts`: Styles API metadata
  - `docs.mdx`: Main documentation page

Refer to existing components in [`./package/src/`](./package/src/) for implementation examples.

## TypeScript Patterns

### Component Factory Pattern

All components use Mantine's polymorphic factory pattern.

```typescript
import { polymorphicFactory, PolymorphicFactory, useProps, useStyles, createVarsResolver } from '@mantine/core';

export type ComponentStylesNames = 'root' | 'element';
export type ComponentCssVariables = {
  root: '--custom-var' | '--another-var';
};

export interface ComponentProps extends BoxProps, StylesApiProps<ComponentFactory> {
  /** Prop description */
  customProp?: string;
}

export type ComponentFactory = PolymorphicFactory<{
  props: ComponentProps;
  defaultComponent: 'div';
  defaultRef: HTMLDivElement;
  stylesNames: ComponentStylesNames;
  vars: ComponentCssVariables;
  staticComponents: {
    SubComponent: typeof SubComponent;
  };
}>;

const defaultProps: Partial<ComponentProps> = {
  customProp: 'default',
};

const varsResolver = createVarsResolver<ComponentFactory>((_, { customProp }) => ({
  root: {
    '--custom-var': customProp,
  },
}));

export const Component = polymorphicFactory<ComponentFactory>((_props, ref) => {
  const props = useProps('Component', defaultProps, _props);
  const { classNames, className, style, styles, unstyled, vars, customProp, ...others } = props;
  
  const getStyles = useStyles<ComponentFactory>({
    name: 'Component',
    classes,
    props,
    className,
    style,
    classNames,
    styles,
    unstyled,
    vars,
    varsResolver,
  });

  return (
    <Box ref={ref} {...getStyles('root')} {...others}>
      {/* component content */}
    </Box>
  );
});

Component.displayName = '@your-scope/Component';
Component.SubComponent = SubComponent;
```

**Key Requirements:**
- Use `unknown` for unconstrained generics; narrow with type guards
- Avoid `any`; use `React.ReactNode` for children
- Define explicit type aliases for style names and CSS variables
- Use `useProps` hook for default prop merging
- Implement `varsResolver` for CSS custom properties

### Context Pattern

For components requiring state sharing, use Mantine's safe context pattern.

```typescript
import { createSafeContext } from '@mantine/core';
import { COMPONENT_ERRORS } from './Component.errors';

interface ComponentContext {
  state: boolean;
  setState: (value: boolean) => void;
}

export const [ComponentContextProvider, useComponentContext] = createSafeContext<ComponentContext>(
  COMPONENT_ERRORS.context
);
```

**Error Definitions** in `Component.errors.ts`:

```typescript
export const COMPONENT_ERRORS = {
  context: 'Component was not found in the tree',
  validation: 'Specific validation message',
};
```

### Sub-Component Pattern

Sub-components access parent context and enforce constraints.

```typescript
import { forwardRef, useProps, isElement, createEventHandler } from '@mantine/core';
import { useComponentContext } from '../Component.context';

export interface SubComponentProps {
  children: React.ReactNode;
  refProp?: string;
}

export const SubComponent = forwardRef<HTMLElement, SubComponentProps>((props, ref) => {
  const { children, ...others } = useProps('SubComponent', {}, props);
  
  if (!isElement(children)) {
    throw new Error(COMPONENT_ERRORS.children);
  }
  
  const ctx = useComponentContext();
  const onClick = createEventHandler(children.props.onClick, () => ctx.toggle());
  
  return cloneElement(children, { onClick, ref });
});
```

## Styles API

Every component exposes a Styles API for customization. Define in [`./docs/styles-api/Component.styles-api.ts`](./docs/styles-api/):

```typescript
import type { ComponentFactory } from '@your-scope/component';
import type { StylesApiData } from '../components/styles-api.types';

export const ComponentStylesApi: StylesApiData<ComponentFactory> = {
  selectors: {
    root: 'Root element',
    element: 'Specific child element',
  },
  vars: {
    root: {
      '--custom-var': 'Controls custom behavior',
      '--another-var': 'Controls another aspect',
    },
  },
  modifiers: [
    { modifier: 'data-active', selector: 'root', condition: '`active` prop is set' }
  ],
};
```

**CSS Module** (`Component.module.css`):

```css
.root {
  /* Use CSS custom properties from varsResolver */
  property: var(--custom-var, fallback);
}

.element {
  /* Scoped class name */
}

/* Data attribute modifiers */
.root[data-active] {
  /* Active state */
}
```

## Component Guidelines

### Controlled vs Uncontrolled State

Use `@mantine/hooks` `useUncontrolled` for dual-mode state:

```typescript
import { useUncontrolled } from '@mantine/hooks';

const [value, setValue] = useUncontrolled({
  value: props.value,
  defaultValue: props.defaultValue,
  finalValue: undefined,
  onChange: props.onChange,
});
```

### Lifecycle Hooks

Use `useDidUpdate` from `@mantine/hooks` for effect-on-update patterns:

```typescript
import { useDidUpdate } from '@mantine/hooks';

useDidUpdate(() => {
  props.onStateChange?.(state);
}, [state]);
```

### Props Validation

Validate props at runtime when type system isn't enough:

```typescript
if (React.Children.count(children) !== 2) {
  throw new Error('Component requires exactly two children');
}
```

### Ref Forwarding

Always support ref forwarding for component composition:

```typescript
export const Component = polymorphicFactory<ComponentFactory>((_props, ref) => {
  return <Box ref={ref} {...others} />;
});
```

## Coding Standards

### Import Order

Prettier auto-sorts imports per [`./.prettierrc.mjs`](./.prettierrc.mjs):

1. CSS imports
2. React
3. Next.js (if applicable)
4. Built-in modules
5. Third-party modules
6. `@mantine/*` packages
7. Local imports (parent then sibling)
8. CSS modules last

### Formatting

- **Print Width**: 100 characters
- **Quotes**: Single quotes
- **Trailing Commas**: ES5-style
- **MDX**: 70 character print width

Run `npm run prettier:write` before committing.

### Linting

ESLint config extends [`eslint-config-mantine`](./eslint.config.mjs):

```javascript
import mantine from 'eslint-config-mantine';
import tseslint from 'typescript-eslint';

export default tseslint.config(...mantine, { 
  ignores: ['**/.next/**', '**/*.{mjs,cjs,js,d.ts,d.mts}'] 
});
```

Run `npm run lint` to check all rules.

### TypeScript Configuration

Primary config ([`./tsconfig.json`](./tsconfig.json)):

- **Target**: ES2015
- **Module**: ESNext with Node resolution
- **JSX**: React (classic runtime)
- **Strict**: Enabled (via mantine config)
- **Skip Lib Check**: true (for faster builds)

**Build config** (`tsconfig.build.json`) isolates compilation scope.

## Testing

Use `@mantine-tests/core` renderer with Testing Library.

```typescript
import React from 'react';
import { render } from '@mantine-tests/core';
import { Component } from './Component';

describe('Component', () => {
  it('renders without crashing', () => {
    const { container } = render(<Component>Content</Component>);
    expect(container).toBeTruthy();
  });

  it('applies custom className', () => {
    const { container } = render(<Component className="custom" />);
    expect(container.querySelector('.custom')).toBeTruthy();
  });

  it('forwards ref', () => {
    const ref = React.createRef<HTMLDivElement>();
    render(<Component ref={ref} />);
    expect(ref.current).toBeTruthy();
  });
});
```

Run tests with `npm run jest`.

## Documentation

### Demos

Create interactive demos in [`./docs/demos/`](./docs/demos/):

```typescript
// Component.demo.basic.tsx
import { Component } from '@your-scope/component';
import { MantineDemo } from '@docs/components';

const code = `
import { Component } from '@your-scope/component';

function Demo() {
  return <Component>Content</Component>;
}
`;

export const basic: MantineDemo = {
  type: 'code',
  component: Demo,
  code,
};
```

**Configurator demos** use `MantineDemo` type `'configurator'` with `controls` object.

### MDX Pages

Main docs page at [`./docs/docs.mdx`](./docs/docs.mdx):

```mdx
import { InstallScript } from './components/InstallScript/InstallScript';
import * as demos from './demos';

## Installation

<InstallScript packages="@your-scope/component" />

## Usage

<Demo data={demos.basic} />

## Props

<PropsTable component="Component" />

## Styles API

<StylesApiTable component="Component" />
```

Refer to existing documentation structure in `/docs` for consistency.

## Accessibility

### ARIA Patterns

- Use semantic HTML elements (`<button>`, `<nav>`, etc.) over `<div>` with roles
- Add ARIA attributes only when semantic HTML is insufficient
- Reference MDN ARIA practices: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA

### Keyboard Navigation

- Ensure all interactive elements are keyboard-accessible
- Use `tabIndex={-1}` for programmatic focus management
- Implement arrow-key navigation for composite widgets

### Focus Management

```typescript
import { useFocusTrap } from '@mantine/hooks';

const focusTrapRef = useFocusTrap(active);
```

### Data Attributes for State

Expose component state via data attributes for CSS and screen readers:

```typescript
<div data-active={isActive} data-disabled={disabled} />
```

## Security and Maintenance

### No Hardcoded Secrets

- Never commit API keys, tokens, or credentials
- Use environment variables for sensitive configuration
- Exclude `.env` files in `.gitignore`

### Dependency Hygiene

- Keep `@mantine/core` and `@mantine/hooks` versions in sync (see [`./package/package.json`](./package/package.json))
- Use `peerDependencies` for React and Mantine packages
- Run `npm run syncpack` to verify version consistency

### Least Privilege

- Minimize scope of React Context providers
- Avoid global state; prefer component-level state
- Use `createSafeContext` to enforce provider boundaries

## Edge Cases and Troubleshooting

### Module Resolution

- Ensure all imports use relative paths for local modules
- Check `package.json` `exports` field for correct entry points
- Verify `tsconfig.json` `paths` if using aliases

### CSS Modules

- Class names are auto-scoped via `hash-css-selector` (see [`./rollup.config.mjs`](./rollup.config.mjs))
- Import CSS modules as `import classes from './Component.module.css'`
- Use `getStyles` helper for className merging

### Polymorphic Components

- Default component is `div`; override with `component` prop
- Ref type must match `defaultRef` in factory definition
- Props are merged: `BoxProps & ComponentProps & { component?: any }`

### Testing Library Queries

- Prefer `getByRole` over `getByTestId`
- Use `screen` for global queries or `container` for scoped
- Mock `window.matchMedia` if needed (see [`./jsdom.mocks.cjs`](./jsdom.mocks.cjs))

### Storybook Integration

- Stories go in `Component.story.tsx` alongside component
- Use CSF3 format with `Meta` and `StoryObj` types
- Stories auto-generate docs from TypeScript types

## File Organization

Maintain consistent file structure per component:

```
package/src/
├── Component.tsx              # Main component
├── Component.module.css       # Scoped styles
├── Component.context.ts       # Context (if needed)
├── Component.errors.ts        # Error constants
├── Component.test.tsx         # Tests
├── Component.story.tsx        # Storybook
├── SubComponent/
│   └── SubComponent.tsx       # Sub-component
└── index.ts                   # Public API
```

**Public API** (`index.ts`):

```typescript
export { Component } from './Component';
export type { ComponentProps, ComponentFactory } from './Component';
```

## Commit Hygiene

- Run `npm run test` before committing (includes prettier, typecheck, lint, jest)
- Write clear commit messages: `fix: resolve prop merging issue` or `feat: add keyboard navigation`
- Avoid committing generated files (`dist/`, `.next/`, `out/`)
- Use `.gitignore` to exclude build artifacts

## References

See [`./references/`](./references/) for indexed documentation pointers.

## Related Files

- [ESLint Config](./eslint.config.mjs)
- [Prettier Config](./.prettierrc.mjs)
- [TypeScript Config](./tsconfig.json)
- [Rollup Config](./rollup.config.mjs)
- [Package Source](./package/src/)
- [Documentation](./docs/)
- [Contributing Guide](./CONTRIBUTING.md)
