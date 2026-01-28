---
name: Design System Architect
description: Build scalable, maintainable design systems that unify product experiences. Use when creating component libraries, design tokens, or establishing design standards. Covers atomic design, Storybook, theming, and design system governance.
version: 1.0.0
---

# Design System Architect

**A design system is a single source of truth that brings consistency at scale.**

## Core Principle

Design systems are not just component libraries—they're the shared language between design and engineering. A good design system:

- Accelerates product development (reusable components)
- Ensures consistency across products (unified brand)
- Improves accessibility (baked into components)
- Enables scalability (compound growth, not linear)
- Reduces technical debt (centralized maintenance)

**Goal:** Build once, use everywhere. Maintain once, improve everywhere.

---

## Phase 1: Design Tokens

### What Are Design Tokens?

**Design tokens are the atomic values of your design system.** They're the smallest decisions (colors, spacing, typography) stored as data and consumed by all platforms.

**Why Tokens Matter:**

- Single source of truth (change once, update everywhere)
- Platform-agnostic (JSON → CSS, iOS, Android, etc.)
- Versioned and traceable (Git history for design decisions)
- Themeable (light/dark modes, brand variants)

### Token Structure

```typescript
// tokens/colors.json
{
  "color": {
    "brand": {
      "primary": {
        "50": { "value": "#eff6ff" },
        "100": { "value": "#dbeafe" },
        "200": { "value": "#bfdbfe" },
        "300": { "value": "#93c5fd" },
        "400": { "value": "#60a5fa" },
        "500": { "value": "#3b82f6" },
        "600": { "value": "#2563eb" },
        "700": { "value": "#1d4ed8" },
        "800": { "value": "#1e40af" },
        "900": { "value": "#1e3a8a" },
        "950": { "value": "#172554" }
      }
    },
    "semantic": {
      "background": {
        "primary": { "value": "{color.neutral.50}" },
        "secondary": { "value": "{color.neutral.100}" }
      },
      "text": {
        "primary": { "value": "{color.neutral.900}" },
        "secondary": { "value": "{color.neutral.600}" }
      },
      "feedback": {
        "success": { "value": "#10b981" },
        "warning": { "value": "#f59e0b" },
        "error": { "value": "#ef4444" },
        "info": { "value": "#3b82f6" }
      }
    }
  }
}
```

### Token Categories

**Primitive Tokens** (Raw values):

```json
{
  "color-blue-500": "#3b82f6",
  "space-4": "16px",
  "font-size-base": "16px"
}
```

**Semantic Tokens** (Named by purpose):

```json
{
  "color-primary": "{color-blue-500}",
  "spacing-default": "{space-4}",
  "text-body": "{font-size-base}"
}
```

**Component Tokens** (Component-specific):

```json
{
  "button-padding-x": "{spacing-default}",
  "button-background": "{color-primary}",
  "button-text": "{color-white}"
}
```

### Token Architecture

```
tokens/
├── primitives/
│   ├── colors.json       # Raw color values
│   ├── spacing.json      # 4px, 8px, 16px...
│   ├── typography.json   # Font sizes, weights
│   ├── shadows.json      # Elevation system
│   └── radii.json        # Border radius values
├── semantic/
│   ├── colors.json       # background-primary, text-secondary
│   ├── spacing.json      # spacing-tight, spacing-comfortable
│   └── typography.json   # heading-xl, body-md
└── components/
    ├── button.json       # Button-specific tokens
    ├── input.json        # Input-specific tokens
    └── card.json         # Card-specific tokens
```

### Token Transformation with Style Dictionary

**Install Style Dictionary:**

```bash
npm install --save-dev style-dictionary
```

**config.json:**

```json
{
  "source": ["tokens/**/*.json"],
  "platforms": {
    "css": {
      "transformGroup": "css",
      "buildPath": "dist/css/",
      "files": [
        {
          "destination": "variables.css",
          "format": "css/variables"
        }
      ]
    },
    "js": {
      "transformGroup": "js",
      "buildPath": "dist/js/",
      "files": [
        {
          "destination": "tokens.js",
          "format": "javascript/es6"
        }
      ]
    }
  }
}
```

**Build tokens:**

```bash
npx style-dictionary build
```

**Output (variables.css):**

```css
:root {
  --color-brand-primary-500: #3b82f6;
  --color-semantic-background-primary: #fafafa;
  --space-4: 16px;
  --font-size-base: 16px;
  --button-padding-x: 16px;
}
```

### Dark Mode with Tokens

```json
// tokens/semantic/colors-light.json
{
  "background": {
    "primary": { "value": "#ffffff" },
    "secondary": { "value": "#f9fafb" }
  },
  "text": {
    "primary": { "value": "#111827" },
    "secondary": { "value": "#6b7280" }
  }
}

// tokens/semantic/colors-dark.json
{
  "background": {
    "primary": { "value": "#111827" },
    "secondary": { "value": "#1f2937" }
  },
  "text": {
    "primary": { "value": "#f9fafb" },
    "secondary": { "value": "#d1d5db" }
  }
}
```

**CSS Output:**

```css
:root {
  --background-primary: #ffffff;
  --text-primary: #111827;
}

[data-theme='dark'] {
  --background-primary: #111827;
  --text-primary: #f9fafb;
}
```

---

## Phase 2: Component Architecture

### Atomic Design Methodology

**Atoms** → **Molecules** → **Organisms** → **Templates** → **Pages**

```
atoms/
├── Button/
├── Input/
├── Label/
├── Icon/
└── Text/

molecules/
├── FormField/         # Label + Input + Error
├── SearchBar/         # Input + Icon + Button
└── Card/              # Container + Text + Button

organisms/
├── Header/            # Logo + Nav + SearchBar
├── LoginForm/         # FormFields + Button
└── ProductCard/       # Card + Image + Price + CTA

templates/
├── DashboardLayout/   # Header + Sidebar + Content
└── MarketingLayout/   # Header + Hero + Features + Footer

pages/
├── HomePage/          # MarketingLayout + specific content
└── DashboardPage/     # DashboardLayout + widgets
```

### Component Structure

```
components/
└── Button/
    ├── Button.tsx           # Component implementation
    ├── Button.module.css    # Scoped styles
    ├── Button.stories.tsx   # Storybook stories
    ├── Button.test.tsx      # Unit tests
    ├── Button.types.ts      # TypeScript types
    ├── index.ts             # Public exports
    └── README.md            # Component docs
```

### Button Component (Atomic Example)

**Button.types.ts:**

```typescript
export type ButtonVariant = 'primary' | 'secondary' | 'tertiary' | 'danger'
export type ButtonSize = 'sm' | 'md' | 'lg'

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant
  size?: ButtonSize
  isLoading?: boolean
  leftIcon?: React.ReactNode
  rightIcon?: React.ReactNode
  fullWidth?: boolean
  children: React.ReactNode
}
```

**Button.tsx:**

```typescript
import React from 'react'
import styles from './Button.module.css'
import { ButtonProps } from './Button.types'

export function Button({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  leftIcon,
  rightIcon,
  fullWidth = false,
  disabled,
  children,
  className,
  ...props
}: ButtonProps) {
  const classes = [
    styles.button,
    styles[variant],
    styles[size],
    fullWidth && styles.fullWidth,
    isLoading && styles.loading,
    className
  ].filter(Boolean).join(' ')

  return (
    <button
      className={classes}
      disabled={disabled || isLoading}
      aria-busy={isLoading}
      {...props}
    >
      {leftIcon && <span className={styles.iconLeft}>{leftIcon}</span>}
      <span className={styles.content}>{children}</span>
      {rightIcon && <span className={styles.iconRight}>{rightIcon}</span>}
      {isLoading && (
        <span className={styles.spinner} aria-label="Loading">
          <svg className={styles.spinnerIcon} viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" opacity="0.25" />
            <path d="M12 2a10 10 0 0 1 10 10" stroke="currentColor" strokeWidth="4" fill="none" strokeLinecap="round" />
          </svg>
        </span>
      )}
    </button>
  )
}
```

**Button.module.css:**

```css
.button {
  /* Base */
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  font-family: var(--font-base);
  font-weight: 500;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 150ms ease;
  user-select: none;

  /* Accessibility */
  outline-offset: 2px;
}

.button:focus-visible {
  outline: 2px solid var(--color-focus);
}

.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

/* Variants */
.primary {
  background: var(--button-primary-background);
  color: var(--button-primary-text);
}

.primary:hover:not(:disabled) {
  background: var(--button-primary-background-hover);
}

.secondary {
  background: transparent;
  color: var(--button-secondary-text);
  border: 1px solid var(--button-secondary-border);
}

.secondary:hover:not(:disabled) {
  background: var(--button-secondary-background-hover);
}

.tertiary {
  background: transparent;
  color: var(--button-tertiary-text);
}

.tertiary:hover:not(:disabled) {
  background: var(--button-tertiary-background-hover);
}

.danger {
  background: var(--color-error);
  color: var(--color-white);
}

.danger:hover:not(:disabled) {
  background: var(--color-error-dark);
}

/* Sizes */
.sm {
  padding: var(--space-1) var(--space-3);
  font-size: var(--text-sm);
  height: 32px;
}

.md {
  padding: var(--space-2) var(--space-4);
  font-size: var(--text-base);
  height: 40px;
}

.lg {
  padding: var(--space-3) var(--space-6);
  font-size: var(--text-lg);
  height: 48px;
}

/* Modifiers */
.fullWidth {
  width: 100%;
}

.loading {
  color: transparent;
}

.spinner {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  inset: 0;
}

.spinnerIcon {
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.iconLeft,
.iconRight {
  display: flex;
  align-items: center;
}

.content {
  display: flex;
  align-items: center;
}
```

### FormField Component (Molecule Example)

**FormField.tsx:**

```typescript
import React from 'react'
import styles from './FormField.module.css'

interface FormFieldProps {
  label: string
  error?: string
  hint?: string
  required?: boolean
  children: React.ReactNode
}

export function FormField({
  label,
  error,
  hint,
  required = false,
  children
}: FormFieldProps) {
  const inputId = React.useId()
  const errorId = `${inputId}-error`
  const hintId = `${inputId}-hint`

  // Clone child to pass accessibility props
  const childWithProps = React.cloneElement(
    children as React.ReactElement,
    {
      id: inputId,
      'aria-invalid': !!error,
      'aria-describedby': [
        hint ? hintId : null,
        error ? errorId : null
      ].filter(Boolean).join(' ') || undefined
    }
  )

  return (
    <div className={styles.field}>
      <label htmlFor={inputId} className={styles.label}>
        {label}
        {required && (
          <span className={styles.required} aria-label="required">
            *
          </span>
        )}
      </label>

      {hint && (
        <div id={hintId} className={styles.hint}>
          {hint}
        </div>
      )}

      {childWithProps}

      {error && (
        <div id={errorId} className={styles.error} role="alert">
          {error}
        </div>
      )}
    </div>
  )
}
```

### Component API Design Principles

**1. Sensible Defaults:**

```typescript
// ✅ Good: Works with minimal props
<Button>Click me</Button>

// ✅ Good: Customizable when needed
<Button variant="secondary" size="lg" fullWidth>
  Click me
</Button>
```

**2. Composition Over Configuration:**

```typescript
// ❌ Bad: Too many props
<Modal
  title="Delete Account"
  body="Are you sure?"
  confirmText="Delete"
  cancelText="Cancel"
  onConfirm={handleDelete}
  onCancel={handleCancel}
/>

// ✅ Good: Composable
<Modal>
  <Modal.Header>Delete Account</Modal.Header>
  <Modal.Body>Are you sure?</Modal.Body>
  <Modal.Footer>
    <Button variant="danger" onClick={handleDelete}>Delete</Button>
    <Button variant="secondary" onClick={handleCancel}>Cancel</Button>
  </Modal.Footer>
</Modal>
```

**3. Controlled & Uncontrolled Modes:**

```typescript
// Uncontrolled (internal state)
<Input defaultValue="hello" />

// Controlled (external state)
<Input value={value} onChange={setValue} />
```

**4. Polymorphic Components:**

```typescript
interface ButtonProps<T extends React.ElementType = 'button'> {
  as?: T
  // ... other props
}

// Render as button (default)
<Button onClick={handleClick}>Click</Button>

// Render as link
<Button as="a" href="/dashboard">Dashboard</Button>

// Render as Next.js Link
<Button as={Link} href="/about">About</Button>
```

---

## Phase 3: Storybook Documentation

### Storybook Setup

**Install Storybook:**

```bash
npx storybook@latest init
```

**Button.stories.tsx:**

```typescript
import type { Meta, StoryObj } from '@storybook/react'
import { Button } from './Button'

const meta: Meta<typeof Button> = {
  title: 'Atoms/Button',
  component: Button,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'tertiary', 'danger'],
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg'],
    },
    isLoading: { control: 'boolean' },
    fullWidth: { control: 'boolean' },
    disabled: { control: 'boolean' },
  },
}

export default meta
type Story = StoryObj<typeof Button>

// Primary story
export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Button',
  },
}

// All variants
export const AllVariants: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem' }}>
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="tertiary">Tertiary</Button>
      <Button variant="danger">Danger</Button>
    </div>
  ),
}

// All sizes
export const AllSizes: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
      <Button size="sm">Small</Button>
      <Button size="md">Medium</Button>
      <Button size="lg">Large</Button>
    </div>
  ),
}

// With icons
export const WithIcons: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem' }}>
      <Button leftIcon={<Icon name="plus" />}>Add Item</Button>
      <Button rightIcon={<Icon name="arrow-right" />}>Next</Button>
    </div>
  ),
}

// Loading state
export const Loading: Story = {
  args: {
    isLoading: true,
    children: 'Loading...',
  },
}

// Disabled state
export const Disabled: Story = {
  args: {
    disabled: true,
    children: 'Disabled',
  },
}

// Full width
export const FullWidth: Story = {
  args: {
    fullWidth: true,
    children: 'Full Width Button',
  },
}
```

### MDX Documentation

**Button.mdx:**

````mdx
import { Meta, Story, Canvas, Controls } from '@storybook/blocks'
import * as ButtonStories from './Button.stories'

<Meta of={ButtonStories} />

# Button

Buttons allow users to trigger actions and make choices with a single tap.

## When to Use

- Primary actions (submit forms, complete workflows)
- Secondary actions (cancel, go back)
- Tertiary actions (view details, learn more)
- Dangerous actions (delete, remove)

## Variants

<Canvas of={ButtonStories.AllVariants} />

### Primary

Use for the main action on a page. Limit to one per screen.

### Secondary

Use for less important actions. Can have multiple per screen.

### Tertiary

Use for the least important actions, like "Learn more" links.

### Danger

Use for destructive actions like deleting data.

## Sizes

<Canvas of={ButtonStories.AllSizes} />

- **Small**: Dense UIs, table actions
- **Medium**: Default for most use cases
- **Large**: Hero CTAs, mobile-first designs

## With Icons

<Canvas of={ButtonStories.WithIcons} />

Icons can clarify the button's purpose or indicate direction.

## States

### Loading

<Canvas of={ButtonStories.Loading} />

Show a loading spinner when an async action is in progress.

### Disabled

<Canvas of={ButtonStories.Disabled} />

Disable buttons when an action is not currently available.

## Accessibility

- ✅ Keyboard accessible (Tab, Enter/Space)
- ✅ Focus visible indicator
- ✅ ARIA attributes (aria-busy, aria-disabled)
- ✅ Loading state announced to screen readers

## Props

<Controls />

## Usage

```tsx
import { Button } from '@/components/Button'

function MyComponent() {
  return (
    <Button variant="primary" onClick={handleClick}>
      Click me
    </Button>
  )
}
```
````

````

### Storybook Addons

```bash
# Accessibility testing
npm install --save-dev @storybook/addon-a11y

# Component interactions
npm install --save-dev @storybook/addon-interactions

# Design tokens addon
npm install --save-dev storybook-addon-designs
````

**.storybook/main.ts:**

```typescript
import type { StorybookConfig } from '@storybook/react-vite'

const config: StorybookConfig = {
  stories: ['../src/**/*.stories.@(js|jsx|ts|tsx|mdx)'],
  addons: [
    '@storybook/addon-links',
    '@storybook/addon-essentials',
    '@storybook/addon-interactions',
    '@storybook/addon-a11y',
    'storybook-addon-designs'
  ],
  framework: '@storybook/react-vite'
}

export default config
```

---

## Phase 4: Theming & Customization

### CSS Variables Approach

**tokens.css:**

```css
:root {
  /* Primitives */
  --color-blue-500: #3b82f6;
  --color-red-500: #ef4444;
  --space-4: 16px;

  /* Semantic (can be overridden) */
  --color-primary: var(--color-blue-500);
  --color-danger: var(--color-red-500);
  --spacing-default: var(--space-4);

  /* Component tokens */
  --button-primary-background: var(--color-primary);
  --button-primary-text: white;
  --button-padding: var(--spacing-default);
}

/* Theme override */
[data-theme='brand-red'] {
  --color-primary: #dc2626;
}

[data-theme='dark'] {
  --color-primary: #60a5fa;
  --button-primary-background: var(--color-primary);
}
```

### Theme Provider (React)

**ThemeProvider.tsx:**

```typescript
import React, { createContext, useContext, useEffect, useState } from 'react'

type Theme = 'light' | 'dark' | 'auto'

interface ThemeContextValue {
  theme: Theme
  setTheme: (theme: Theme) => void
  resolvedTheme: 'light' | 'dark'
}

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined)

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>('auto')
  const [resolvedTheme, setResolvedTheme] = useState<'light' | 'dark'>('light')

  useEffect(() => {
    // Load saved theme
    const saved = localStorage.getItem('theme') as Theme
    if (saved) setTheme(saved)
  }, [])

  useEffect(() => {
    // Save theme
    localStorage.setItem('theme', theme)

    // Resolve theme
    if (theme === 'auto') {
      const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      setResolvedTheme(isDark ? 'dark' : 'light')
    } else {
      setResolvedTheme(theme)
    }
  }, [theme])

  useEffect(() => {
    // Apply theme to DOM
    document.documentElement.setAttribute('data-theme', resolvedTheme)
  }, [resolvedTheme])

  return (
    <ThemeContext.Provider value={{ theme, setTheme, resolvedTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider')
  }
  return context
}
```

### Multi-Brand Theming

```typescript
// themes/acme.ts
export const acmeTheme = {
  colors: {
    primary: '#3b82f6',
    secondary: '#8b5cf6'
  },
  typography: {
    fontFamily: 'Inter, sans-serif'
  },
  spacing: {
    unit: 8
  }
}

// themes/contoso.ts
export const contosoTheme = {
  colors: {
    primary: '#dc2626',
    secondary: '#f59e0b'
  },
  typography: {
    fontFamily: 'Roboto, sans-serif'
  },
  spacing: {
    unit: 4
  }
}
```

**Theme Application:**

```typescript
function applyTheme(theme: Theme) {
  Object.entries(theme.colors).forEach(([key, value]) => {
    document.documentElement.style.setProperty(`--color-${key}`, value)
  })

  document.documentElement.style.setProperty('--font-base', theme.typography.fontFamily)

  document.documentElement.style.setProperty('--space-unit', `${theme.spacing.unit}px`)
}
```

---

## Phase 5: Versioning & Governance

### Semantic Versioning

**MAJOR.MINOR.PATCH**

- **MAJOR:** Breaking changes (v1.0.0 → v2.0.0)
  - Removed props
  - Changed prop types
  - Changed default behavior

- **MINOR:** New features, backwards-compatible (v1.0.0 → v1.1.0)
  - New props
  - New components
  - New variants

- **PATCH:** Bug fixes (v1.0.0 → v1.0.1)
  - CSS fixes
  - Accessibility improvements
  - TypeScript fixes

### Changelog

**CHANGELOG.md:**

````markdown
# Changelog

## [2.0.0] - 2024-01-15

### Breaking Changes

- **Button:** Renamed `type` prop to `variant`
- **Input:** Removed `error` prop (use FormField wrapper instead)

### Migration Guide

```typescript
// Before
<Button type="primary">Click</Button>

// After
<Button variant="primary">Click</Button>
```
````

## [1.5.0] - 2024-01-10

### Added

- **Button:** New `isLoading` prop
- **Input:** New `leftIcon` and `rightIcon` props
- **Card:** New component

### Fixed

- **Button:** Focus outline now visible on all browsers
- **Input:** Placeholder color now meets WCAG contrast requirements

## [1.4.1] - 2024-01-05

### Fixed

- **Button:** Loading spinner now centered correctly
- **Modal:** Fixed backdrop z-index issue

````

### Component Lifecycle

**P0 (Must Have):**
- Button, Input, Label, Text, Icon
- FormField, Card, Modal

**P1 (Should Have):**
- Select, Checkbox, Radio, Switch, Textarea
- Tabs, Accordion, Dropdown, Tooltip

**P2 (Nice to Have):**
- DatePicker, Combobox, Slider, Toggle
- Toast, Drawer, Popover

**P3 (Future):**
- DataTable, Calendar, FileUpload
- Charts, Timeline, Stepper

### Deprecation Strategy

**1. Announce deprecation:**
```typescript
/**
 * @deprecated Use `variant` prop instead. Will be removed in v3.0.0.
 */
export interface ButtonProps {
  type?: 'primary' | 'secondary' // Deprecated
  variant?: 'primary' | 'secondary' // New
}
````

**2. Support both (with warning):**

```typescript
export function Button({ type, variant, ...props }: ButtonProps) {
  if (type) {
    console.warn('Button: `type` prop is deprecated. Use `variant` instead.')
  }

  const finalVariant = variant || type || 'primary'
  // ...
}
```

**3. Remove in next major version:**

```typescript
// v3.0.0 - type prop removed entirely
export interface ButtonProps {
  variant?: 'primary' | 'secondary'
}
```

### Design System Governance

**Design System Team:**

- **Owner:** Overall vision and roadmap
- **Designers:** Visual design, UX patterns
- **Engineers:** Implementation, tooling
- **Contributors:** Product teams building components

**Contribution Flow:**

```
1. Proposal → GitHub issue
2. Design Review → Figma mockup
3. API Design → TypeScript interface
4. Implementation → PR with tests + stories
5. Documentation → README + Storybook
6. Release → Semantic versioning + changelog
```

**Proposal Template:**

````markdown
## Component Name

**Problem:** What user need does this solve?

**Usage:** When should this be used?

**API Proposal:**

```typescript
interface ComponentProps {
  // ...
}
```
````

**Design Mockup:** [Link to Figma]

**Accessibility:** How will this be accessible?

**Alternatives Considered:** What else did we explore?

````

---

## Testing Design Systems

### Visual Regression Testing

**Chromatic (Storybook integration):**
```bash
npm install --save-dev chromatic

# Run visual tests
npx chromatic --project-token=YOUR_TOKEN
````

**package.json:**

```json
{
  "scripts": {
    "chromatic": "chromatic --exit-zero-on-changes"
  }
}
```

### Component Testing

```typescript
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Button } from './Button'

describe('Button', () => {
  it('renders children', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByRole('button', { name: 'Click me' })).toBeInTheDocument()
  })

  it('calls onClick when clicked', async () => {
    const user = userEvent.setup()
    const handleClick = jest.fn()

    render(<Button onClick={handleClick}>Click me</Button>)
    await user.click(screen.getByRole('button'))

    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('disables button when loading', () => {
    render(<Button isLoading>Click me</Button>)
    expect(screen.getByRole('button')).toBeDisabled()
    expect(screen.getByLabelText('Loading')).toBeInTheDocument()
  })

  it('applies variant classes', () => {
    render(<Button variant="danger">Delete</Button>)
    expect(screen.getByRole('button')).toHaveClass('danger')
  })
})
```

### Accessibility Testing

```typescript
import { axe, toHaveNoViolations } from 'jest-axe'
expect.extend(toHaveNoViolations)

it('has no accessibility violations', async () => {
  const { container } = render(<Button>Click me</Button>)
  const results = await axe(container)
  expect(results).toHaveNoViolations()
})
```

---

## Publishing & Distribution

### NPM Package Setup

**package.json:**

```json
{
  "name": "@company/design-system",
  "version": "1.0.0",
  "description": "Company design system",
  "main": "dist/index.js",
  "module": "dist/index.esm.js",
  "types": "dist/index.d.ts",
  "files": ["dist", "README.md"],
  "scripts": {
    "build": "rollup -c",
    "prepublishOnly": "npm run build"
  },
  "peerDependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  },
  "publishConfig": {
    "access": "public"
  }
}
```

**rollup.config.js:**

```javascript
import typescript from '@rollup/plugin-typescript'
import postcss from 'rollup-plugin-postcss'

export default {
  input: 'src/index.ts',
  output: [
    {
      file: 'dist/index.js',
      format: 'cjs',
      sourcemap: true
    },
    {
      file: 'dist/index.esm.js',
      format: 'esm',
      sourcemap: true
    }
  ],
  plugins: [
    typescript({ tsconfig: './tsconfig.json' }),
    postcss({
      modules: true,
      extract: 'styles.css'
    })
  ],
  external: ['react', 'react-dom']
}
```

**Publish:**

```bash
npm login
npm version patch  # or minor, major
npm publish
```

### Consumption

```bash
npm install @company/design-system
```

```typescript
import { Button, Input, Card } from '@company/design-system'
import '@company/design-system/dist/styles.css'

function App() {
  return (
    <Card>
      <Input placeholder="Email" />
      <Button variant="primary">Submit</Button>
    </Card>
  )
}
```

---

## Design System Checklist

### Foundation

- [ ] Design tokens (colors, spacing, typography, shadows, radii)
- [ ] Token transformation pipeline (Style Dictionary)
- [ ] Dark mode support
- [ ] Documentation site (Storybook)

### Components

- [ ] Atomic design structure (atoms → organisms)
- [ ] Component API guidelines (sensible defaults, composition)
- [ ] TypeScript types for all components
- [ ] CSS modules or styled-components
- [ ] Accessibility baked in (WCAG 2.1 AA)

### Documentation

- [ ] Storybook stories for all components
- [ ] MDX docs with usage examples
- [ ] Props table (auto-generated)
- [ ] Design guidelines (when to use, when not to use)
- [ ] Code examples

### Testing

- [ ] Unit tests (70%+ coverage)
- [ ] Accessibility tests (jest-axe)
- [ ] Visual regression tests (Chromatic)
- [ ] Manual testing checklist

### Governance

- [ ] Semantic versioning
- [ ] Changelog maintained
- [ ] Contribution guidelines
- [ ] Component lifecycle (P0 → P3)
- [ ] Deprecation strategy

### Distribution

- [ ] NPM package published
- [ ] Storybook deployed
- [ ] Installation guide
- [ ] Migration guides for breaking changes

---

## Tools & Resources

**Token Management:**

- Style Dictionary (token transformation)
- Figma Tokens (sync Figma → code)

**Component Development:**

- Storybook (documentation)
- Chromatic (visual testing)
- React + TypeScript

**Testing:**

- Jest + React Testing Library
- jest-axe (accessibility)
- Playwright (E2E)

**Build & Distribution:**

- Rollup or tsup (bundling)
- NPM (distribution)
- Changesets (versioning)

**Inspiration:**

- [Radix UI](https://www.radix-ui.com/) (accessible primitives)
- [Chakra UI](https://chakra-ui.com/) (themeable components)
- [Material UI](https://mui.com/) (comprehensive system)
- [Ant Design](https://ant.design/) (enterprise-grade)

---

## Related Skills

- `visual-designer` - Design foundations (color, typography, spacing)
- `accessibility-engineer` - WCAG compliance
- `frontend-builder` - React component patterns
- `testing-strategist` - Component testing strategies

---

**A design system is never done—it evolves with your product.** 🎨
