---
name: slidev-navigation
description: Master Slidev navigation and keyboard shortcuts. Use this skill for efficient slide control, custom shortcuts, and navigation customization.
---

# Slidev Navigation

This skill covers all navigation features in Slidev, including keyboard shortcuts, navigation bar, overview mode, and customizing navigation behavior.

## When to Use This Skill

- Learning navigation controls
- Customizing keyboard shortcuts
- Setting up presentation navigation
- Configuring navigation bar
- Creating custom navigation components

## Default Keyboard Shortcuts

### Basic Navigation

| Key | Action |
|-----|--------|
| `Space` | Next animation or slide |
| `→` / `Right` | Next animation or slide |
| `←` / `Left` | Previous animation or slide |
| `↑` / `Up` | Previous slide (skip animations) |
| `↓` / `Down` | Next slide (skip animations) |

### Mode Toggles

| Key | Action |
|-----|--------|
| `o` | Toggle overview mode |
| `d` | Toggle dark mode |
| `f` | Toggle fullscreen |
| `p` | Toggle presenter mode |

### Navigation Jumps

| Key | Action |
|-----|--------|
| `g` | Go to specific slide |
| `Home` | Go to first slide |
| `End` | Go to last slide |

### Other Controls

| Key | Action |
|-----|--------|
| `Esc` | Exit fullscreen/overview/drawing |
| `e` | Toggle drawing mode |
| `r` | Toggle recording |

## Navigation Bar

### Location

Bottom-left corner of the slide (appears on hover).

### Available Buttons

- **Home**: Go to first slide
- **Previous**: Previous slide/animation
- **Current/Total**: Click to open go-to dialog
- **Next**: Next slide/animation
- **Presenter**: Open presenter mode
- **Camera**: Toggle camera view
- **Record**: Start/stop recording
- **Drawing**: Toggle drawing mode
- **Overview**: Open slide overview
- **Dark Mode**: Toggle dark/light
- **Fullscreen**: Toggle fullscreen
- **Export**: Export options
- **Info**: Presentation info

## Overview Mode

### Accessing

- Press `o` key
- Click overview button in navigation bar
- Navigate to `/overview` URL

### Features

- Grid view of all slides
- Click any slide to navigate
- Keyboard navigation within overview
- Search slides (if implemented)

### Overview Navigation

| Key | Action |
|-----|--------|
| `←` `→` `↑` `↓` | Navigate grid |
| `Enter` | Select slide |
| `Esc` / `o` | Close overview |

## Go-To Dialog

### Opening

- Press `g` key
- Click slide number in navigation bar

### Usage

1. Dialog opens
2. Type slide number
3. Press Enter

### Quick Jump

```
g → 15 → Enter
```

Goes directly to slide 15.

## Customizing Shortcuts

### Configuration File

Create `setup/shortcuts.ts`:

```typescript
import { defineShortcutsSetup } from '@slidev/types'

export default defineShortcutsSetup((nav, base) => {
  return [
    ...base, // Keep default shortcuts
    {
      key: 'enter',
      fn: () => nav.next(),
      autoRepeat: true,
    },
    {
      key: 'backspace',
      fn: () => nav.prev(),
      autoRepeat: true,
    },
    {
      key: 'ctrl+f',
      fn: () => nav.go(1),
    },
  ]
})
```

### Shortcut Properties

| Property | Type | Description |
|----------|------|-------------|
| `key` | string | Key combination |
| `fn` | function | Action to perform |
| `autoRepeat` | boolean | Repeat when held |

### Key Syntax

```typescript
// Single key
{ key: 'enter', fn: () => {} }

// Modifier + key
{ key: 'ctrl+s', fn: () => {} }

// Multiple modifiers
{ key: 'ctrl+shift+s', fn: () => {} }
```

### Available Modifiers

- `ctrl`
- `shift`
- `alt`
- `meta` (Cmd on Mac)

## Navigation API

### In Components

```vue
<script setup>
import { useNav } from '@slidev/client'

const {
  currentSlideNo,  // Current slide number (ref)
  currentPage,     // Current page number
  total,           // Total slides
  clicks,          // Current click count
  next,            // Go to next
  prev,            // Go to previous
  go,              // Go to slide number
  nextSlide,       // Next slide (skip animations)
  prevSlide,       // Previous slide (skip animations)
} = useNav()
</script>
```

### Navigation Functions

```vue
<template>
  <!-- Custom navigation buttons -->
  <button @click="nav.prev()">Previous</button>
  <button @click="nav.next()">Next</button>
  <button @click="nav.go(1)">Go to Start</button>
  <button @click="nav.go(total.value)">Go to End</button>
</template>

<script setup>
import { useNav } from '@slidev/client'
const nav = useNav()
</script>
```

## Custom Navigation Components

### Slide Progress Bar

```vue
<!-- components/ProgressBar.vue -->
<script setup>
import { computed } from 'vue'
import { useNav } from '@slidev/client'

const { currentSlideNo, total } = useNav()
const progress = computed(() =>
  (currentSlideNo.value / total.value) * 100
)
</script>

<template>
  <div class="fixed top-0 left-0 right-0 h-1 bg-gray-200">
    <div
      class="h-full bg-blue-500 transition-all"
      :style="{ width: `${progress}%` }"
    />
  </div>
</template>
```

### Custom Page Number

```vue
<!-- components/PageNumber.vue -->
<script setup>
import { useNav } from '@slidev/client'
const { currentSlideNo, total } = useNav()
</script>

<template>
  <div class="fixed bottom-4 right-4 text-sm">
    {{ currentSlideNo }} / {{ total }}
  </div>
</template>
```

### Navigation Buttons

```vue
<!-- components/NavButtons.vue -->
<script setup>
import { useNav } from '@slidev/client'
const { prev, next, currentSlideNo, total } = useNav()
</script>

<template>
  <div class="fixed bottom-4 flex gap-2">
    <button
      @click="prev()"
      :disabled="currentSlideNo === 1"
      class="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
    >
      Previous
    </button>
    <button
      @click="next()"
      :disabled="currentSlideNo === total"
      class="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
    >
      Next
    </button>
  </div>
</template>
```

## Touch Navigation

### Default Behavior

- Swipe left: Next slide
- Swipe right: Previous slide

### Touch Areas

Screen is divided into:
- Left third: Previous
- Right two-thirds: Next

## Mouse Navigation

### Click Areas

- Left side of slide: Previous
- Right side of slide: Next

### Disable Click Navigation

```yaml
---
# In frontmatter
---
```

Custom CSS to disable:
```css
.slidev-page {
  pointer-events: none;
}
```

## URL Navigation

### Direct Slide Access

```
http://localhost:3030/5      # Slide 5
http://localhost:3030/10     # Slide 10
```

### Presenter Mode

```
http://localhost:3030/presenter
http://localhost:3030/presenter/5  # Presenter at slide 5
```

### Overview Mode

```
http://localhost:3030/overview
```

## Slide Numbering

### Default Numbering

Slides numbered 1 to N based on order.

### Custom Slide IDs

```yaml
---
routeAlias: introduction
---
```

Access via:
```
http://localhost:3030/introduction
```

### Link to Slide by ID

```markdown
[Go to Introduction](/introduction)
```

## Navigation Events

### Watch Navigation

```vue
<script setup>
import { watch } from 'vue'
import { useNav } from '@slidev/client'

const { currentSlideNo } = useNav()

watch(currentSlideNo, (newSlide, oldSlide) => {
  console.log(`Navigated from ${oldSlide} to ${newSlide}`)
})
</script>
```

## Best Practices

### 1. Learn Core Shortcuts

Essential for smooth presenting:
- `Space` / `→` - Forward
- `←` - Back
- `o` - Overview
- `g` - Go to

### 2. Custom Shortcuts for Your Style

```typescript
// If you prefer Enter/Backspace
{
  key: 'enter',
  fn: () => nav.next(),
}
```

### 3. Hide Navigation for Clean Presentations

CSS to hide nav bar:
```css
.slidev-nav {
  display: none;
}
```

### 4. Add Progress Indicator

Global bottom component for progress.

### 5. Practice Navigation

Before presenting:
- Run through all slides
- Practice overview jumping
- Test any custom shortcuts

## Output Format

When configuring navigation:

```typescript
// setup/shortcuts.ts
import { defineShortcutsSetup } from '@slidev/types'

export default defineShortcutsSetup((nav, base) => {
  return [
    ...base, // Keep defaults

    // Custom shortcuts
    { key: '[key]', fn: () => nav.[action]() },
  ]
})
```

**NAVIGATION PLAN:**
- Forward: [key]
- Backward: [key]
- Overview: [key]
- Jump: [method]

**CUSTOM COMPONENTS:**
- Progress bar: [yes/no]
- Page numbers: [yes/no]
- Custom buttons: [yes/no]
