---
name: slidev-themes
description: Use and customize Slidev themes. Use this skill to apply themes, configure theme options, and create custom themes.
---

# Slidev Themes

This skill covers using, customizing, and creating themes for Slidev presentations. Themes provide consistent styling, layouts, and components across your slides.

## When to Use This Skill

- Choosing a theme for your presentation
- Customizing theme colors and styles
- Ejecting and modifying themes
- Creating your own theme
- Understanding theme structure

## Using Themes

### Setting a Theme

In your first slide's frontmatter:

```yaml
---
theme: seriph
---
```

### Theme Name Conventions

- Official themes: Use short name (`seriph`, `default`)
- NPM packages: Use full name (`slidev-theme-custom`)
- Local themes: Use path (`./my-theme`)

### Auto-Installation

Slidev automatically prompts to install missing themes:

```bash
? The theme "seriph" was not found, do you want to install it now? (Y/n)
```

### Manual Installation

```bash
npm install slidev-theme-seriph
```

## Official Themes

### default

The built-in default theme.

```yaml
---
theme: default
---
```

- Clean, minimal design
- Light and dark mode support
- Standard layouts

### seriph

Elegant theme with serif typography.

```yaml
---
theme: seriph
---
```

- Elegant serif fonts
- Sophisticated styling
- Professional appearance

### apple-basic

Apple keynote-inspired design.

```yaml
---
theme: apple-basic
---
```

- Clean, modern look
- Apple-style aesthetics
- Minimal distractions

### bricks

Colorful, vibrant theme.

```yaml
---
theme: bricks
---
```

- Bold colors
- Playful design
- Good for creative content

### shibainu

Theme featuring Shiba Inu styling.

```yaml
---
theme: shibainu
---
```

## Community Themes

Find more at the [Theme Gallery](https://sli.dev/resources/theme-gallery):

Popular community themes include:
- `slidev-theme-penguin`
- `slidev-theme-purplin`
- `slidev-theme-geist`
- `slidev-theme-dracula`
- `slidev-theme-eloc`

### Installing Community Themes

```bash
npm install slidev-theme-penguin
```

```yaml
---
theme: penguin
---
```

## Theme Configuration

### themeConfig

Pass configuration to themes:

```yaml
---
theme: seriph
themeConfig:
  primary: '#5d8392'
  secondary: '#8b5cf6'
  tertiary: '#3b82f6'
  darkBg: '#1a1a2e'
  lightBg: '#f8fafc'
---
```

### Available Options

Each theme defines its own options. Check theme documentation for:
- Color customization
- Font settings
- Layout options
- Component variants

### Common themeConfig Options

```yaml
themeConfig:
  # Colors
  primary: '#3b82f6'
  secondary: '#10b981'
  background: '#ffffff'
  text: '#1e293b'

  # Typography
  fontFamily: 'Inter'
  fontSize: '16px'

  # Layout
  padding: '2rem'
```

## Color Schema

### Auto (Default)

```yaml
---
colorSchema: auto
---
```

Follows system preference.

### Force Light

```yaml
---
colorSchema: light
---
```

### Force Dark

```yaml
---
colorSchema: dark
---
```

## Ejecting Themes

### Why Eject?

To fully customize a theme's source code:
- Modify layouts
- Change components
- Deep style customization

### How to Eject

```bash
slidev theme eject
```

This copies the theme to your project's local files.

### Ejected Structure

```
my-presentation/
├── slides.md
├── theme/
│   ├── layouts/
│   │   ├── default.vue
│   │   ├── cover.vue
│   │   └── ...
│   ├── components/
│   ├── styles/
│   │   └── index.css
│   └── setup/
│       └── main.ts
└── package.json
```

### Using Ejected Theme

```yaml
---
theme: ./theme
---
```

## Creating Custom Themes

### Theme Structure

```
slidev-theme-mytheme/
├── package.json
├── layouts/
│   ├── default.vue
│   ├── cover.vue
│   ├── center.vue
│   └── two-cols.vue
├── components/
│   └── MyComponent.vue
├── styles/
│   └── index.css
└── setup/
    ├── main.ts
    └── shiki.ts
```

### package.json

```json
{
  "name": "slidev-theme-mytheme",
  "version": "1.0.0",
  "keywords": [
    "slidev-theme",
    "slidev"
  ],
  "engines": {
    "slidev": ">=0.40.0"
  },
  "slidev": {
    "colorSchema": "both",
    "highlighter": "shiki",
    "fonts": {
      "sans": "Inter",
      "mono": "Fira Code"
    }
  }
}
```

### Basic Layout

```vue
<!-- layouts/default.vue -->
<template>
  <div class="slidev-layout default">
    <slot />
  </div>
</template>

<style scoped>
.default {
  padding: 2rem;
  height: 100%;
}
</style>
```

### Cover Layout

```vue
<!-- layouts/cover.vue -->
<script setup>
defineProps({
  background: {
    type: String,
    default: ''
  }
})
</script>

<template>
  <div
    class="slidev-layout cover"
    :style="{
      backgroundImage: background ? `url(${background})` : undefined
    }"
  >
    <div class="content">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.cover {
  display: flex;
  align-items: center;
  justify-content: center;
  background-size: cover;
  background-position: center;
}

.content {
  text-align: center;
}
</style>
```

### Global Styles

```css
/* styles/index.css */
:root {
  --slidev-theme-primary: #3b82f6;
  --slidev-theme-secondary: #10b981;
  --slidev-theme-text: #1e293b;
  --slidev-theme-background: #ffffff;
}

.dark {
  --slidev-theme-text: #f1f5f9;
  --slidev-theme-background: #0f172a;
}

.slidev-layout {
  color: var(--slidev-theme-text);
  background: var(--slidev-theme-background);
}

h1 {
  color: var(--slidev-theme-primary);
  font-weight: 700;
}

a {
  color: var(--slidev-theme-secondary);
}
```

### Theme Components

```vue
<!-- components/ThemedCard.vue -->
<script setup>
defineProps({
  title: String,
  variant: {
    type: String,
    default: 'primary'
  }
})
</script>

<template>
  <div :class="['themed-card', `variant-${variant}`]">
    <h3 v-if="title">{{ title }}</h3>
    <slot />
  </div>
</template>

<style scoped>
.themed-card {
  padding: 1.5rem;
  border-radius: 0.5rem;
  margin: 1rem 0;
}

.variant-primary {
  background: var(--slidev-theme-primary);
  color: white;
}

.variant-secondary {
  background: var(--slidev-theme-secondary);
  color: white;
}
</style>
```

## Theme with Config

### Accepting Configuration

```vue
<!-- layouts/default.vue -->
<script setup>
import { useSlideContext } from '@slidev/client'

const { $slidev } = useSlideContext()
const primaryColor = $slidev.themeConfigs?.primary || '#3b82f6'
</script>

<template>
  <div class="layout" :style="{ '--primary': primaryColor }">
    <slot />
  </div>
</template>
```

### Default Config

In `setup/main.ts`:

```typescript
import { defineAppSetup } from '@slidev/types'

export default defineAppSetup(({ app }) => {
  app.provide('themeDefaults', {
    primary: '#3b82f6',
    secondary: '#10b981',
  })
})
```

## Publishing Themes

### Prepare for NPM

1. Ensure `package.json` has correct fields
2. Add README with usage instructions
3. Include screenshots

### Publish

```bash
npm publish
```

### Submit to Gallery

Open a PR to Slidev's theme gallery repository.

## Theme Best Practices

### 1. Support Both Color Schemes

```css
/* Light mode */
.slidev-layout {
  background: #ffffff;
  color: #1e293b;
}

/* Dark mode */
.dark .slidev-layout {
  background: #0f172a;
  color: #f1f5f9;
}
```

### 2. Use CSS Variables

```css
:root {
  --theme-primary: #3b82f6;
}

.primary {
  color: var(--theme-primary);
}
```

### 3. Provide Common Layouts

Essential layouts:
- `default`
- `cover`
- `center`
- `two-cols`
- `section`
- `end`

### 4. Document Configuration

README should include:
- Available themeConfig options
- Example usage
- Screenshots
- Layout descriptions

### 5. Test Thoroughly

- Test all layouts
- Test light and dark modes
- Test with real content
- Test export to PDF

## Output Format

When configuring themes:

```yaml
---
theme: [theme-name]
colorSchema: [auto|light|dark]
themeConfig:
  primary: '[color]'
  secondary: '[color]'
  [other options specific to theme]
---
```

**THEME SELECTION:**
- Chosen theme: [name]
- Reason: [why this theme fits]

**CUSTOMIZATION:**
- Primary color: [hex]
- Secondary color: [hex]
- Custom options: [list]

**ADDITIONAL FILES (if ejected):**
- layouts/[modified].vue
- styles/index.css
