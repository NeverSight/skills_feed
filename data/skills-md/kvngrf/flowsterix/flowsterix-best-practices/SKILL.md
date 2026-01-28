---
name: flowsterix-best-practices
description: Use when user asks to "create a tour", "add onboarding flow", "implement guided walkthrough", "set up Flowsterix", "add tour steps", "configure step targeting", "handle async content in tour", or needs help with tour overlays, popovers, step advance rules, or TourHUD configuration.
version: 0.1.0
metadata:
  tags: flowsterix, tour, onboarding, walkthrough, guide, react
---

# Flowsterix Best Practices

Flowsterix is a state machine-based guided tour library for React applications. Flows are declarative step sequences with automatic progression rules, lifecycle hooks, and persistence.

## Quick Start

### Installation

```bash
# Core packages
npm install @flowsterix/core @flowsterix/react motion

# Recommended: Add preconfigured shadcn components
npx shadcn@latest add https://flowsterix.com/r/tour-hud.json
```

**Prefer the shadcn components** - they provide polished, accessible UI out of the box and follow the design patterns shown in the examples.

### Minimal Example

```tsx
import { createFlow, type FlowDefinition } from '@flowsterix/core'
import { TourProvider, TourHUD } from '@flowsterix/react'
import type { ReactNode } from 'react'

const onboardingFlow: FlowDefinition<ReactNode> = createFlow({
  id: 'onboarding',
  version: { major: 1, minor: 0 },
  autoStart: true,
  steps: [
    {
      id: 'welcome',
      target: 'screen',
      advance: [{ type: 'manual' }],
      content: <p>Welcome to our app!</p>,
    },
    {
      id: 'feature',
      target: { selector: '[data-tour-target="main-feature"]' },
      advance: [{ type: 'event', event: 'click', on: 'target' }],
      content: <p>Click this button to continue</p>,
    },
  ],
})

export function App({ children }) {
  return (
    <TourProvider flows={[onboardingFlow]} storageNamespace="my-app">
      <TourHUD overlay={{ showRing: true }} />
      {children}
    </TourProvider>
  )
}
```

## Core Concepts

### FlowDefinition

```tsx
createFlow({
  id: string,                          // Unique identifier
  version: { major: number, minor: number },  // For storage migrations
  steps: Step[],                       // Array of tour steps
  autoStart?: boolean,                 // Start on mount (default: false)
  resumeStrategy?: 'chain' | 'current', // How to run onResume hooks
  hud?: FlowHudOptions,                // UI configuration
  migrate?: (ctx) => FlowState | null, // Version migration handler
})
```

### Step Anatomy

```tsx
{
  id: string,                    // Unique within flow
  target: StepTarget,            // What to highlight
  content: ReactNode,            // Popover content
  advance?: AdvanceRule[],       // When to move to next step
  placement?: StepPlacement,     // Popover position
  route?: string | RegExp,       // Only show on matching routes
  waitFor?: StepWaitFor,         // Block until condition met
  targetBehavior?: StepTargetBehavior,  // Scroll/visibility handling
  onEnter?: (ctx) => void,       // Fires when step activates
  onResume?: (ctx) => void,      // Fires when resuming from storage
  onExit?: (ctx) => void,        // Fires when leaving step
  controls?: { back?, next? },   // Button visibility
}
```

### Step Targets

```tsx
// Full-screen overlay (no element highlight)
target: 'screen'

// CSS selector (recommended: use data attributes)
target: {
  selector: '[data-tour-target="feature"]'
}

// Dynamic node resolution
target: {
  getNode: () => document.querySelector('.dynamic-el')
}
```

**Always use `data-tour-target` attributes** instead of CSS classes for stability.

## Advance Rules

Rules define when a step automatically progresses. First matching rule wins.

| Type        | Usage               | Example                                            |
| ----------- | ------------------- | -------------------------------------------------- |
| `manual`    | Next button only    | `{ type: 'manual' }`                               |
| `event`     | DOM event on target | `{ type: 'event', event: 'click', on: 'target' }`  |
| `delay`     | Timer-based         | `{ type: 'delay', ms: 3000 }`                      |
| `route`     | URL change          | `{ type: 'route', to: '/dashboard' }`              |
| `predicate` | Polling condition   | `{ type: 'predicate', check: (ctx) => isReady() }` |

```tsx
// Combine rules for flexibility
advance: [
  { type: 'event', event: 'click', on: 'target' },
  { type: 'delay', ms: 10000 }, // Fallback after 10s
]
```

## React Integration

### TourProvider Props

```tsx
<TourProvider
  flows={[flow1, flow2]} // Flow definitions
  storageNamespace="my-app" // localStorage key prefix
  persistOnChange={true} // Auto-save state changes
  backdropInteraction="block" // 'block' | 'passthrough'
  lockBodyScroll={false} // Prevent page scroll
  analytics={{
    // Event handlers
    onFlowStart: (p) => track('tour_start', p),
    onStepEnter: (p) => track('step_view', p),
  }}
/>
```

### useTour Hook

```tsx
const {
  activeFlowId, // Currently active flow ID or null
  state, // FlowState: status, stepIndex, version
  activeStep, // Current Step object
  startFlow, // (flowId, options?) => start a flow
  next, // () => advance to next step
  back, // () => go to previous step
  pause, // () => pause the flow
  cancel, // (reason?) => cancel the flow
  complete, // () => mark flow complete
} = useTour()
```

### TourHUD Configuration

```tsx
<TourHUD
  overlay={{
    padding: 12, // Padding around highlight
    radius: 12, // Border radius of cutout
    showRing: true, // Glow effect around target
    blurAmount: 6, // Backdrop blur (px)
  }}
  popover={{
    maxWidth: 360,
    offset: 16, // Distance from target
  }}
  controls={{
    showSkip: true,
    skipMode: 'hold', // 'click' | 'hold' (hold-to-confirm)
  }}
  progress={{
    show: true,
    variant: 'dots', // 'dots' | 'bar' | 'fraction'
  }}
/>
```

## Common Mistakes

1. **Missing `data-tour-target` attributes** - Tour cannot find elements

   ```tsx
   // Bad: fragile to styling changes
   target: {
     selector: '.btn-primary'
   }

   // Good: semantic and stable
   target: {
     selector: '[data-tour-target="submit-btn"]'
   }
   ```

2. **No `waitFor` for async content** - Step shows before content ready

   ```tsx
   // Add waitFor when targeting dynamically loaded elements
   waitFor: { selector: '[data-tour-target="api-result"]', timeout: 8000 }
   ```

3. **Ignoring sticky headers** - Target scrolls behind fixed navigation

   ```tsx
   targetBehavior: {
     scrollMargin: { top: 80 },  // Height of sticky header
     scrollMode: 'start',
   }
   ```

4. **Wrong version format** - Use object, not number

   ```tsx
   // Bad
   version: 1

   // Good
   version: { major: 1, minor: 0 }
   ```

5. **Forgetting `onResume` hooks** - UI state not restored after reload
   ```tsx
   // Bad: UI broken after page reload
   onEnter: () => ensureMenuOpen(),

   // Good: Both hooks restore UI state
   onEnter: () => ensureMenuOpen(),
   onResume: () => ensureMenuOpen(),
   onExit: () => ensureMenuClosed(),
   ```

## Shadcn Components

The shadcn registry provides preconfigured, polished components. **Always prefer these over custom implementations.**

> **Important**: The tour components require shadcn CSS variables (`--popover`, `--border`, `--destructive`, etc.). If you're not using shadcn/ui, see [CSS Setup](references/css-setup.md) for the required variables.

### Available Components

| Component           | Install Command                                                  | Usage                            |
| ------------------- | ---------------------------------------------------------------- | -------------------------------- |
| `tour-hud`          | `npx shadcn@latest add https://flowsterix.com/r/tour-hud.json`   | Full HUD with overlay & popover  |
| `step-content`      | `npx shadcn@latest add https://flowsterix.com/r/step-content.json` | Step layout primitives           |

### Step Content Primitives

Use these components for consistent step styling:

```tsx
import {
  StepContent,
  StepTitle,
  StepText,
  StepHint,
} from '@/components/step-content'

content: (
  <StepContent>
    <StepTitle>Feature Discovery</StepTitle>
    <StepText>
      This is the main explanation text with muted styling.
    </StepText>
    <StepHint>Click the button to continue.</StepHint>
  </StepContent>
)
```

- `StepContent` - Grid container with proper spacing
- `StepTitle` - Semibold heading (supports `size="lg"` for welcome screens)
- `StepText` - Muted paragraph text
- `StepHint` - Italic hint text for user instructions

## Lifecycle Hooks

Lifecycle hooks synchronize UI state with tour progression. **Use them when steps target elements inside collapsible panels, modals, drawers, or other dynamic UI.**

### When to Use Each Hook

| Hook       | Fires When                    | Purpose                                |
| ---------- | ----------------------------- | -------------------------------------- |
| `onEnter`  | Step activates (fresh start)  | Open UI, prepare state                 |
| `onResume` | Step restores from storage    | Restore UI after page reload           |
| `onExit`   | Leaving step (next/back/skip) | Clean up, close UI                     |

### Common Patterns

**1. Opening/Closing Drawers & Menus**

```tsx
// Helper functions to toggle menu state
const ensureMenuOpen = () => {
  const panel = document.querySelector('[data-tour-target="menu-panel"]')
  if (!(panel instanceof HTMLElement)) return
  const isClosed = panel.classList.contains('-translate-x-full')
  if (isClosed) {
    document.querySelector('[data-tour-target="menu-button"]')?.click()
  }
}

const ensureMenuClosed = () => {
  const panel = document.querySelector('[data-tour-target="menu-panel"]')
  if (!(panel instanceof HTMLElement)) return
  const isClosed = panel.classList.contains('-translate-x-full')
  if (!isClosed) {
    panel.querySelector('[aria-label="Close menu"]')?.click()
  }
}
```

**2. Step Targeting Element Inside Drawer**

```tsx
{
  id: 'menu-link',
  target: { selector: '[data-tour-target="api-link"]' },
  onEnter: () => ensureMenuOpen(),   // Open drawer on fresh entry
  onResume: () => ensureMenuOpen(),  // Open drawer on page reload
  onExit: () => ensureMenuClosed(),  // Close drawer when leaving
  advance: [{ type: 'route', to: '/api-demo' }],
  content: (
    <StepContent>
      <StepTitle>API Demo</StepTitle>
      <StepText>Click to explore the API features.</StepText>
    </StepContent>
  ),
}
```

**3. Expanding Nested Accordions**

```tsx
const ensureAccordionExpanded = () => {
  ensureMenuOpen() // Parent must be open first
  const submenu = document.querySelector('[data-tour-target="submenu"]')
  if (submenu) return // Already expanded
  document.querySelector('[data-tour-target="accordion-toggle"]')?.click()
}

{
  id: 'submenu-item',
  target: { selector: '[data-tour-target="submenu"]' },
  onResume: () => ensureAccordionExpanded(),
  content: ...
}
```

**4. Closing UI When Moving Away**

```tsx
{
  id: 'feature-grid',
  target: { selector: '#feature-grid' },
  onEnter: () => {
    setTimeout(() => ensureMenuClosed(), 0) // Allow menu click to register first
  },
  onResume: () => ensureMenuClosed(),
  content: ...
}
```

### Critical Rules

1. **Always implement `onResume` when you have `onEnter`** - Users may reload the page mid-tour
2. **Check state before acting** - Don't toggle already-open menus
3. **Use `setTimeout` for sequential actions** - Give previous clicks time to register
4. **Keep hooks idempotent** - Safe to call multiple times

## Step Placements

```
'auto' | 'top' | 'bottom' | 'left' | 'right' |
'top-start' | 'top-end' | 'bottom-start' | 'bottom-end' |
'left-start' | 'left-end' | 'right-start' | 'right-end' |
'auto-start' | 'auto-end'
```

## Additional Resources

- [CSS Setup](references/css-setup.md) - Required shadcn CSS variables
- [Flow Patterns](references/flow-patterns.md) - Targeting, advance rules, waitFor
- [React Integration](references/react-integration.md) - Hooks, events, step content
- [Router Adapters](references/router-adapters.md) - TanStack, React Router, Next.js
- [Advanced Patterns](references/advanced-patterns.md) - Versions, storage, migrations

## Examples

- [Basic Flow](examples/basic-flow.tsx) - Simple 3-step onboarding
- [Async Content](examples/waitfor-async.tsx) - waitFor patterns
- [Lifecycle Hooks](examples/lifecycle-hooks.tsx) - UI synchronization
- [Router Sync](examples/router-sync.tsx) - All 4 router adapters
