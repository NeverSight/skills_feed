---
name: nuxt-ui
description: Expert knowledge for Nuxt UI v4 components and patterns. Activate when creating UI components, working with buttons, cards, forms, or any Nuxt UI component.
---

# Nuxt UI v4 Expertise

## Activation Triggers
- Creating Vue components with UI elements
- Working with buttons, cards, modals, forms
- Implementing navigation, dropdowns, tooltips
- Building responsive layouts
- Adding loading states or skeletons

## Component Reference

### Buttons (UButton)
```vue
<!-- Variants -->
<UButton>Default (solid)</UButton>
<UButton variant="outline">Outline</UButton>
<UButton variant="soft">Soft</UButton>
<UButton variant="ghost">Ghost</UButton>
<UButton variant="link">Link</UButton>

<!-- Colors -->
<UButton color="primary">Primary</UButton>
<UButton color="secondary">Secondary</UButton>
<UButton color="success">Success</UButton>
<UButton color="warning">Warning</UButton>
<UButton color="error">Error</UButton>

<!-- Sizes -->
<UButton size="xs">Extra Small</UButton>
<UButton size="sm">Small</UButton>
<UButton size="md">Medium (default)</UButton>
<UButton size="lg">Large</UButton>
<UButton size="xl">Extra Large</UButton>

<!-- With Icons -->
<UButton icon="i-heroicons-arrow-right" trailing>Next</UButton>
<UButton icon="i-heroicons-check" leading>Complete</UButton>

<!-- Loading State -->
<UButton :loading="isLoading">Submit</UButton>

<!-- Disabled -->
<UButton disabled>Disabled</UButton>
```

### Cards (UCard)
```vue
<UCard>
  <template #header>
    <h3 class="text-lg font-semibold">Card Title</h3>
  </template>
  
  <p>Card content goes here.</p>
  
  <template #footer>
    <UButton>Action</UButton>
  </template>
</UCard>

<!-- Variants -->
<UCard variant="outline">Outline card</UCard>
<UCard variant="soft">Soft background</UCard>
```

### Badges (UBadge)
```vue
<UBadge>Default</UBadge>
<UBadge color="success">Completed</UBadge>
<UBadge color="warning">In Progress</UBadge>
<UBadge color="error">Failed</UBadge>

<!-- Variants -->
<UBadge variant="solid">Solid</UBadge>
<UBadge variant="outline">Outline</UBadge>
<UBadge variant="soft">Soft</UBadge>
```

### Progress (UProgress)
```vue
<!-- Basic -->
<UProgress :value="75" />

<!-- With Label -->
<UProgress :value="75" :max="100">
  <template #indicator="{ percent }">
    {{ percent }}%
  </template>
</UProgress>

<!-- Colors -->
<UProgress :value="75" color="success" />
<UProgress :value="30" color="warning" />
```

### Accordion (UAccordion)
```vue
<UAccordion :items="items" />

<script setup>
const items = [
  {
    label: 'Phase 1: SDLC',
    icon: 'i-heroicons-academic-cap',
    content: 'Learn Software Development Life Cycle...',
    defaultOpen: true
  },
  {
    label: 'Phase 2: Foundations',
    icon: 'i-heroicons-command-line',
    content: 'Master Linux, Git, and networking basics...'
  }
]
</script>
```

### Modal (UModal)
```vue
<UButton @click="isOpen = true">Open Modal</UButton>

<UModal v-model:open="isOpen">
  <template #header>
    <h3>Modal Title</h3>
  </template>
  
  <p>Modal content here.</p>
  
  <template #footer>
    <UButton variant="outline" @click="isOpen = false">Cancel</UButton>
    <UButton @click="handleConfirm">Confirm</UButton>
  </template>
</UModal>
```

### Checkbox & Radio
```vue
<!-- Checkbox -->
<UCheckbox v-model="isChecked" label="Mark as complete" />

<!-- Radio Group -->
<URadioGroup v-model="selected" :items="options" />

<script setup>
const options = [
  { label: 'Option A', value: 'a' },
  { label: 'Option B', value: 'b' },
  { label: 'Option C', value: 'c' }
]
</script>
```

### Skeleton (Loading States)
```vue
<!-- Text skeleton -->
<USkeleton class="h-4 w-32" />

<!-- Multiple lines -->
<div class="space-y-2">
  <USkeleton class="h-4 w-full" />
  <USkeleton class="h-4 w-3/4" />
  <USkeleton class="h-4 w-1/2" />
</div>

<!-- Card skeleton -->
<UCard>
  <USkeleton class="h-48 w-full rounded-lg" />
  <div class="mt-4 space-y-2">
    <USkeleton class="h-4 w-3/4" />
    <USkeleton class="h-4 w-1/2" />
  </div>
</UCard>
```

### Tooltip
```vue
<UTooltip text="This is a helpful tip">
  <UButton>Hover me</UButton>
</UTooltip>
```

### Dropdown Menu
```vue
<UDropdownMenu :items="menuItems">
  <UButton icon="i-heroicons-ellipsis-vertical" variant="ghost" />
</UDropdownMenu>

<script setup>
const menuItems = [
  [
    { label: 'Edit', icon: 'i-heroicons-pencil' },
    { label: 'Duplicate', icon: 'i-heroicons-document-duplicate' }
  ],
  [
    { label: 'Delete', icon: 'i-heroicons-trash', color: 'error' }
  ]
]
</script>
```

### Breadcrumb
```vue
<UBreadcrumb :items="breadcrumbs" />

<script setup>
const breadcrumbs = [
  { label: 'Home', to: '/' },
  { label: 'Phase 1', to: '/phase-1-sdlc' },
  { label: 'SDLC Models', to: '/phase-1-sdlc/sdlc-models' },
  { label: 'Waterfall Model' }
]
</script>
```

### Navigation Menu
```vue
<UNavigationMenu :items="navItems" />

<script setup>
const navItems = [
  {
    label: 'Phases',
    children: [
      { label: 'Phase 1: SDLC', to: '/phase-1-sdlc' },
      { label: 'Phase 2: Foundations', to: '/phase-2-foundations' }
    ]
  }
]
</script>
```

## Icons

Nuxt UI uses Heroicons by default. Use the `i-heroicons-*` prefix:

```vue
<!-- Outline (default) -->
<UIcon name="i-heroicons-check" />
<UIcon name="i-heroicons-x-mark" />
<UIcon name="i-heroicons-arrow-right" />
<UIcon name="i-heroicons-academic-cap" />

<!-- Solid -->
<UIcon name="i-heroicons-check-solid" />

<!-- Common icons for LMS -->
i-heroicons-academic-cap      <!-- Learning/education -->
i-heroicons-book-open         <!-- Lessons -->
i-heroicons-check-circle      <!-- Completed -->
i-heroicons-play-circle       <!-- Start/continue -->
i-heroicons-clock             <!-- Duration -->
i-heroicons-chart-bar         <!-- Progress -->
i-heroicons-trophy            <!-- Achievement -->
i-heroicons-document-text     <!-- Content -->
i-heroicons-question-mark-circle  <!-- Quiz -->
```

## Theme Configuration

```typescript
// app.config.ts
export default defineAppConfig({
  ui: {
    colors: {
      primary: 'indigo',
      secondary: 'slate',
      success: 'green',
      warning: 'amber',
      error: 'red'
    }
  }
})
```

## Common Patterns

### Card with Progress
```vue
<UCard>
  <div class="flex items-center justify-between mb-4">
    <h3 class="font-semibold">Phase 1: SDLC</h3>
    <UBadge color="success">4/5 Complete</UBadge>
  </div>
  <UProgress :value="80" color="success" class="mb-4" />
  <UButton block>Continue Learning</UButton>
</UCard>
```

### Empty State
```vue
<div class="text-center py-12">
  <UIcon name="i-heroicons-document-text" class="w-12 h-12 mx-auto text-gray-400" />
  <h3 class="mt-4 text-lg font-medium">No lessons yet</h3>
  <p class="mt-2 text-gray-400">Start by selecting a topic from the sidebar.</p>
  <UButton class="mt-4">Browse Topics</UButton>
</div>
```

### Loading Card
```vue
<UCard v-if="loading">
  <USkeleton class="h-6 w-1/2 mb-4" />
  <USkeleton class="h-4 w-full mb-2" />
  <USkeleton class="h-4 w-3/4" />
</UCard>
<UCard v-else>
  <!-- Actual content -->
</UCard>
```

## Best Practices

1. **Always use Nuxt UI components** instead of raw HTML for consistency
2. **Use the `color` prop** instead of custom Tailwind colors
3. **Provide loading states** with `USkeleton` for async content
4. **Use icons consistently** from Heroicons set
5. **Leverage slots** (header, footer, default) for flexible layouts
6. **Add `cursor-pointer`** class to custom clickable elements (UButton handles this automatically)
