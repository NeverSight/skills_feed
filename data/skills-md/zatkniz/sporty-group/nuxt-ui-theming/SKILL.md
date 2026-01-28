---
name: nuxt-ui-theming
description: Help customize Nuxt UI component themes and colors. Use when users ask about styling, theming, or customizing component appearance.
---

# Nuxt UI Theming Guide

Assist with customizing Nuxt UI component themes, colors, and appearance.

## When to Use

**DO USE** when:
- User wants to customize component appearance
- Questions about theme configuration
- Need to change colors or design tokens
- Want to create custom component variants
- Questions about the `ui` prop

**DO NOT USE** when:
- Basic component usage (covered in instructions)
- Finding which components exist (use nuxt-ui-component-finder)

## Theming Levels

### 1. Global Configuration (`nuxt.config.ts`)

```typescript
export default defineNuxtConfig({
  ui: {
    // Change component prefix (default: 'U')
    prefix: 'Nuxt',
    
    // Define theme colors
    theme: {
      colors: ['primary', 'secondary', 'success', 'error'],
      transitions: true,
      defaultVariants: {
        color: 'primary',
        size: 'md'
      }
    }
  }
})
```

### 2. App Configuration (`app/app.config.ts`)

```typescript
export default defineAppConfig({
  ui: {
    // Global component defaults
    button: {
      default: {
        color: 'primary',
        size: 'md'
      }
    }
  }
})
```

### 3. Component Level (`ui` prop)

```vue
<UButton
  :ui="{
    base: 'font-bold',
    variant: {
      solid: 'bg-blue-500 hover:bg-blue-600'
    }
  }"
>
  Custom Button
</UButton>
```

### 4. Utility Classes (`class` prop)

```vue
<UButton class="shadow-lg rounded-full">
  Button with classes
</UButton>
```

## Color System

### Semantic Colors

Default semantic colors (configurable):
- `primary` - Main brand color
- `secondary` - Secondary brand color
- `success` - Success states (green)
- `error` - Error states (red)
- `warning` - Warning states (yellow/orange)
- `info` - Info states (blue)
- `neutral` - Neutral/gray

### Using Colors

```vue
<template>
  <UButton color="primary">Primary</UButton>
  <UButton color="error">Error</UButton>
  <UAlert color="success">Success message</UAlert>
</template>
```

### Custom Colors

Add custom colors in Tailwind config:

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  ui: {
    theme: {
      colors: ['primary', 'secondary', 'brand', 'accent']
    }
  }
})
```

## Component Customization

### Using `ui` Prop

The `ui` prop accepts an object matching the component's theme structure:

```vue
<template>
  <!-- Button customization -->
  <UButton
    :ui="{
      base: 'relative disabled:cursor-not-allowed',
      variant: {
        solid: 'bg-{color}-500 hover:bg-{color}-600',
        outline: 'border-2 border-{color}-500'
      },
      size: {
        lg: 'px-6 py-3 text-lg'
      }
    }"
  >
    Custom Button
  </UButton>

  <!-- Card customization -->
  <UCard
    :ui="{
      header: { 
        base: 'border-b',
        padding: 'px-6 py-4' 
      },
      body: { padding: 'p-6' }
    }"
  >
    <template #header>Header</template>
    Body content
  </UCard>
</template>
```

### Slots-Based Theming

Components use slots for theme customization:

```vue
<UCard
  :ui="{
    header: { base: 'bg-gray-50' },
    body: { base: 'space-y-4' },
    footer: { base: 'bg-gray-50' }
  }"
>
  <template #header>Custom Header Styling</template>
  Body with custom spacing
  <template #footer>Custom Footer</template>
</UCard>
```

## Common Patterns

### Creating Reusable Themed Components

```vue
<!-- components/BrandButton.vue -->
<template>
  <UButton
    v-bind="$attrs"
    :ui="{
      variant: {
        solid: 'bg-gradient-to-r from-purple-500 to-pink-500'
      }
    }"
  >
    <slot />
  </UButton>
</template>
```

### Dark Mode Styling

```vue
<UButton
  :ui="{
    variant: {
      solid: 'bg-blue-500 dark:bg-blue-600'
    }
  }"
>
  Dark mode aware
</UButton>
```

### Responsive Theming

```vue
<UCard
  :ui="{
    body: {
      padding: 'p-4 md:p-6 lg:p-8'
    }
  }"
>
  Responsive padding
</UCard>
```

## Process

### User wants to customize a component:

1. Identify component (e.g., "Button")
2. Use `mcp_nuxt-ui_get-component-metadata` to see theme structure
3. Provide `ui` prop example for requested customization
4. Suggest global config if change should be app-wide

### User wants to change brand colors:

1. Explain semantic color system
2. Show `nuxt.config.ts` theme.colors configuration
3. Provide Tailwind color palette setup if needed
4. Show component usage with new colors

### User wants custom variants:

1. Get component theme structure
2. Show how to extend variants with `ui` prop
3. Suggest creating wrapper component for reuse

## Resources

- [Theming Documentation](https://ui.nuxt.com/docs/getting-started/theme)
- [Design System](https://ui.nuxt.com/docs/getting-started/theme/design-system)
- [Tailwind Variants](https://ui.nuxt.com/docs/getting-started/theme/tailwind-variants)

## Tips

- Use `ui` prop for component-level customization
- Use `app.config.ts` for app-wide defaults
- Use `class` prop for simple utility class additions
- Color placeholders like `{color}` are replaced at runtime
- Dark mode classes (`dark:`) work automatically with color mode
- Check component metadata for available theme slots
