---
name: component-documenter
description: Write professional documentation including README files, Storybook 9 stories, API docs, usage examples, and migration guides
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Component Documenter

Expert skill for creating comprehensive, user-friendly documentation for component libraries. Specializes in Storybook 9, README files, API documentation, usage guides, and migration documentation.

## Technology Stack (2025)

### Documentation Tools
- **Storybook 9** - Component development platform
- **MDX 3** - Markdown + JSX documentation
- **TypeDoc** - API documentation from TypeScript
- **Docusaurus 3** / **VitePress 2** - Documentation sites

### Addons
- **@storybook/addon-a11y** - Accessibility testing
- **@storybook/addon-essentials** - Core addons
- **@storybook/test** - Testing integration
- **storybook-dark-mode** - Theme switching

## Storybook 9 Configuration

### Main Config
```typescript
// .storybook/main.ts
import type { StorybookConfig } from '@storybook/react-vite'

const config: StorybookConfig = {
  stories: ['../src/**/*.mdx', '../src/**/*.stories.@(js|jsx|ts|tsx)'],
  addons: [
    '@storybook/addon-essentials',
    '@storybook/addon-a11y',
    '@storybook/addon-interactions',
  ],
  framework: {
    name: '@storybook/react-vite',
    options: {},
  },
  docs: {
    autodocs: 'tag',
  },
  typescript: {
    reactDocgen: 'react-docgen-typescript',
  },
}

export default config
```

### Preview Config
```typescript
// .storybook/preview.ts
import type { Preview } from '@storybook/react'
import '../src/styles/globals.css'

const preview: Preview = {
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
    docs: {
      toc: true,
    },
    a11y: {
      element: '#storybook-root',
      config: {},
      options: {},
    },
  },
  decorators: [
    (Story) => (
      <div className="p-4">
        <Story />
      </div>
    ),
  ],
}

export default preview
```

## Story Examples

### Component Story (CSF 3)
```typescript
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react'
import { fn } from '@storybook/test'
import { Button } from './Button'

const meta = {
  title: 'Components/Button',
  component: Button,
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['default', 'destructive', 'outline', 'secondary', 'ghost', 'link'],
      description: 'Visual style variant',
    },
    size: {
      control: 'select',
      options: ['default', 'sm', 'lg', 'icon'],
    },
    disabled: {
      control: 'boolean',
    },
  },
  args: {
    onClick: fn(),
  },
} satisfies Meta<typeof Button>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {
  args: {
    children: 'Button',
  },
}

export const Primary: Story = {
  args: {
    variant: 'default',
    children: 'Primary Button',
  },
}

export const Secondary: Story = {
  args: {
    variant: 'secondary',
    children: 'Secondary Button',
  },
}

export const Destructive: Story = {
  args: {
    variant: 'destructive',
    children: 'Delete',
  },
}

export const AllSizes: Story = {
  render: () => (
    <div className="flex items-center gap-4">
      <Button size="sm">Small</Button>
      <Button size="default">Default</Button>
      <Button size="lg">Large</Button>
    </div>
  ),
}

export const AllVariants: Story = {
  render: () => (
    <div className="flex flex-wrap gap-4">
      <Button variant="default">Default</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="outline">Outline</Button>
      <Button variant="ghost">Ghost</Button>
      <Button variant="link">Link</Button>
      <Button variant="destructive">Destructive</Button>
    </div>
  ),
}

export const WithIcon: Story = {
  args: {
    children: (
      <>
        <PlusIcon className="mr-2 h-4 w-4" />
        Add Item
      </>
    ),
  },
}

export const Loading: Story = {
  args: {
    disabled: true,
    children: (
      <>
        <LoaderIcon className="mr-2 h-4 w-4 animate-spin" />
        Loading...
      </>
    ),
  },
}

export const Disabled: Story = {
  args: {
    disabled: true,
    children: 'Disabled',
  },
}
```

### MDX Documentation
```mdx
{/* Button.mdx */}
import { Meta, Canvas, Controls, Story } from '@storybook/blocks'
import * as ButtonStories from './Button.stories'

<Meta of={ButtonStories} />

# Button

A versatile button component for user interactions.

## Overview

The Button component provides a consistent way to trigger actions throughout your application.

<Canvas of={ButtonStories.Default} />

## Props

<Controls />

## Variants

### Primary (Default)
Use for the main call-to-action on a page.

<Canvas of={ButtonStories.Primary} />

### Secondary
Use for secondary actions that complement the primary action.

<Canvas of={ButtonStories.Secondary} />

### Destructive
Use for dangerous or irreversible actions.

<Canvas of={ButtonStories.Destructive} />

## Sizes

<Canvas of={ButtonStories.AllSizes} />

## States

### Loading
Shows a loading indicator when an async action is in progress.

<Canvas of={ButtonStories.Loading} />

### Disabled
Prevents interaction when an action is not available.

<Canvas of={ButtonStories.Disabled} />

## Accessibility

- Uses semantic `<button>` element
- Keyboard accessible (Enter, Space)
- Focus visible indicator
- Disabled state properly communicated

## Best Practices

### Do
- Use primary buttons for main actions
- Keep button text concise (2-4 words)
- Use loading state for async actions

### Don't
- Use too many primary buttons on one page
- Use ambiguous labels like "Click here"
- Nest interactive elements inside buttons
```

## README Templates

### Library README
```markdown
# @myorg/ui-library

Modern React 19 component library with TypeScript, Tailwind CSS 4, and full accessibility.

[![npm](https://img.shields.io/npm/v/@myorg/ui-library)](https://www.npmjs.com/package/@myorg/ui-library)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Features

- **50+ Components** - Buttons, inputs, modals, and more
- **TypeScript First** - Full type safety
- **Accessible** - WCAG 2.1 AA compliant
- **Dark Mode** - Built-in theming
- **Tree-shakeable** - Import only what you need

## Installation

\`\`\`bash
npm install @myorg/ui-library
\`\`\`

## Quick Start

\`\`\`tsx
import { Button, Input } from '@myorg/ui-library'
import '@myorg/ui-library/styles.css'

function App() {
  return (
    <div>
      <Button variant="default">Click me</Button>
      <Input placeholder="Enter text..." />
    </div>
  )
}
\`\`\`

## Documentation

- [Storybook](https://storybook.myorg.com)
- [API Reference](https://docs.myorg.com/api)
- [Examples](https://github.com/myorg/ui-library/tree/main/examples)

## Requirements

- React 19+
- Tailwind CSS 4+

## License

MIT
```

### Component README
```markdown
# Button

Versatile button component with multiple variants, sizes, and states.

## Import

\`\`\`tsx
import { Button } from '@myorg/ui-library'
\`\`\`

## Usage

\`\`\`tsx
<Button variant="default" size="default">
  Click me
</Button>
\`\`\`

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| variant | 'default' \| 'secondary' \| 'outline' \| 'ghost' \| 'link' \| 'destructive' | 'default' | Visual style |
| size | 'default' \| 'sm' \| 'lg' \| 'icon' | 'default' | Size |
| disabled | boolean | false | Disabled state |
| asChild | boolean | false | Render as child element |

## Accessibility

- Keyboard: Enter, Space to activate
- Screen reader: Announces as button
- Focus: Visible focus ring
```

## API Documentation

### JSDoc Comments
```typescript
/**
 * Button component for user interactions.
 *
 * @example
 * ```tsx
 * <Button variant="default" onClick={() => alert('Clicked!')}>
 *   Click me
 * </Button>
 * ```
 */
export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement>,
  VariantProps<typeof buttonVariants> {
  /**
   * Render button as child element using Radix Slot
   * @default false
   */
  asChild?: boolean
}
```

## Migration Guide Template

```markdown
# Migration Guide: v1 to v2

## Breaking Changes

### Button Component

#### Variant names changed

**Before (v1):**
\`\`\`tsx
<Button color="primary">Click</Button>
\`\`\`

**After (v2):**
\`\`\`tsx
<Button variant="default">Click</Button>
\`\`\`

## New Features

### Server Components Support

Components now support React 19 Server Components by default.

\`\`\`tsx
// Server Component (default)
import { Card } from '@myorg/ui-library'

// Client Component (when needed)
'use client'
import { Button } from '@myorg/ui-library'
\`\`\`

## Migration Steps

1. Update package: \`npm install @myorg/ui-library@2\`
2. Run codemod: \`npx @myorg/codemod v1-to-v2\`
3. Test application
4. Fix any remaining issues
```

## Best Practices

### Writing Style
1. **Clear and Concise**: Simple language
2. **Examples First**: Show code before explaining
3. **Progressive Disclosure**: Basic → Advanced
4. **Consistent Formatting**: Same patterns
5. **Scannable**: Headings, lists, tables

### Accessibility Documentation
1. Document keyboard shortcuts
2. List ARIA attributes used
3. Describe screen reader behavior
4. Note focus management

## When to Use This Skill

Activate when you need to:
- Write or update README files
- Create Storybook 9 stories
- Generate API documentation
- Write usage guides
- Create migration guides
- Document component props
- Write tutorials

## Output Format

Provide:
1. **Complete Documentation**: README, stories, guides
2. **Code Examples**: Working, tested examples
3. **Props Tables**: Complete prop documentation
4. **Accessibility Notes**: Keyboard, ARIA, screen reader
5. **Migration Guide**: When updating versions
