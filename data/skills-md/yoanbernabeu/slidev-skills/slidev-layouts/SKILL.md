---
name: slidev-layouts
description: Use built-in and custom Slidev layouts effectively. Use this skill to structure slides with cover, two-cols, image layouts and more.
---

# Slidev Layouts

This skill covers all built-in Slidev layouts and teaches you how to use them effectively for different types of content. You'll also learn how to create custom layouts.

## When to Use This Skill

- Choosing the right layout for your content
- Creating visually structured slides
- Using multi-column layouts
- Adding background images
- Building custom layouts

## Using Layouts

Specify a layout in the slide's frontmatter:

```markdown
---
layout: center
---

# Centered Content
```

## Built-in Layouts

### default

The basic layout for general content.

```markdown
---
layout: default
---

# Default Layout

Any content works here:
- Lists
- Code blocks
- Images
- Tables
```

### center

Centers content both horizontally and vertically.

```markdown
---
layout: center
---

# Big Statement

Perfect for impactful single messages
```

**Best for**: Quotes, key takeaways, section titles

### cover

The opening slide with prominent title display.

```markdown
---
layout: cover
background: /images/cover.jpg
---

# Presentation Title

Subtitle or author name
```

**Options**:
- `background`: Image URL or color

**Best for**: First slide, section openers

### intro

Introduction slide with author/presenter info.

```markdown
---
layout: intro
---

# My Presentation

## A Journey Through Code

<div class="absolute bottom-10">
  <span class="font-700">
    John Doe
  </span>
  <br>
  <span class="text-sm opacity-50">
    Senior Developer @ TechCorp
  </span>
</div>
```

### section

Marks the beginning of a new section.

```markdown
---
layout: section
---

# Part 1

Getting Started
```

**Best for**: Dividing presentation into logical sections

### statement

Emphasizes a single statement or quote.

```markdown
---
layout: statement
---

# Code is poetry
```

**Best for**: Powerful quotes, key messages

### quote

Displays a quotation with attribution.

```markdown
---
layout: quote
---

# "Any fool can write code that a computer can understand. Good programmers write code that humans can understand."

Martin Fowler
```

### fact

Highlights important facts or statistics.

```markdown
---
layout: fact
---

# 100%

of developers love Slidev*

<small>*citation needed</small>
```

**Best for**: Statistics, numbers, key facts

### two-cols

Two-column layout with left/right content.

```markdown
---
layout: two-cols
---

# Left Column

- Point 1
- Point 2
- Point 3

::right::

# Right Column

```js
const code = 'here'
```
```

**Slot**: `::right::` separates columns

### two-cols-header

Two columns with a spanning header.

```markdown
---
layout: two-cols-header
---

# Comparison

::left::

## Option A

- Feature 1
- Feature 2

::right::

## Option B

- Feature X
- Feature Y
```

**Slots**: `::left::` and `::right::`

### image

Full-slide background image.

```markdown
---
layout: image
image: /images/photo.jpg
backgroundSize: cover
---
```

**Options**:
- `image`: Image path
- `backgroundSize`: CSS background-size (cover, contain, etc.)

### image-left

Image on left, content on right.

```markdown
---
layout: image-left
image: /images/diagram.png
backgroundSize: contain
---

# Explanation

The diagram shows:
- Component A
- Component B
- Their relationship
```

### image-right

Image on right, content on left.

```markdown
---
layout: image-right
image: /images/screenshot.png
---

# Feature Overview

Our new feature includes:
- Fast performance
- Easy to use
- Beautiful design
```

### iframe

Embeds a webpage.

```markdown
---
layout: iframe
url: https://sli.dev
---
```

**Options**:
- `url`: URL to embed

### iframe-left / iframe-right

Iframe with content on the opposite side.

```markdown
---
layout: iframe-right
url: https://example.com
---

# Live Demo

Check out the live example on the right
```

### full

Uses the entire screen without padding.

```markdown
---
layout: full
---

<div class="w-full h-full bg-gradient-to-r from-blue-500 to-purple-600">
  <h1 class="text-white text-center pt-40">Full Screen</h1>
</div>
```

### none

No styling applied - complete blank slate.

```markdown
---
layout: none
---

<div class="custom-everything">
  Completely custom content
</div>
```

### end

Final slide of the presentation.

```markdown
---
layout: end
---

# Thank You!

Questions?
```

## Layout Quick Reference

| Layout | Use Case |
|--------|----------|
| `default` | General content |
| `center` | Single focused message |
| `cover` | Opening slide |
| `intro` | Author introduction |
| `section` | Section divider |
| `statement` | Bold statement |
| `quote` | Quotations |
| `fact` | Statistics/numbers |
| `two-cols` | Side-by-side content |
| `two-cols-header` | Comparison with header |
| `image` | Full background image |
| `image-left` | Image + text |
| `image-right` | Text + image |
| `iframe` | Embedded webpage |
| `full` | Edge-to-edge content |
| `end` | Closing slide |

## Creating Custom Layouts

### Basic Custom Layout

Create `layouts/my-layout.vue`:

```vue
<template>
  <div class="slidev-layout my-layout">
    <slot />
  </div>
</template>

<style scoped>
.my-layout {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
```

### Layout with Named Slots

```vue
<!-- layouts/split-header.vue -->
<template>
  <div class="slidev-layout split-header">
    <header class="header">
      <slot name="header" />
    </header>
    <main class="content">
      <div class="left">
        <slot name="left" />
      </div>
      <div class="right">
        <slot name="right" />
      </div>
    </main>
  </div>
</template>

<style scoped>
.split-header {
  display: grid;
  grid-template-rows: auto 1fr;
  height: 100%;
}
.header {
  padding: 1rem 2rem;
  border-bottom: 1px solid #e5e7eb;
}
.content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  padding: 2rem;
}
</style>
```

Usage:

```markdown
---
layout: split-header
---

::header::
# Comparison Overview

::left::
## Before

Old approach details

::right::
## After

New approach details
```

### Layout with Props

```vue
<!-- layouts/branded.vue -->
<script setup>
defineProps({
  logo: {
    type: String,
    default: '/logo.png'
  },
  color: {
    type: String,
    default: '#3b82f6'
  }
})
</script>

<template>
  <div class="slidev-layout branded">
    <img :src="logo" class="logo" />
    <div class="content" :style="{ borderColor: color }">
      <slot />
    </div>
  </div>
</template>
```

Usage:

```markdown
---
layout: branded
logo: /company-logo.png
color: '#ef4444'
---

# Branded Content
```

## Theme Layouts

Themes often provide additional layouts. For example, the `seriph` theme includes variations like:

- `default` with refined typography
- `cover` with elegant styling
- Custom layouts specific to the theme

Check theme documentation for available layouts.

## Best Practices

1. **Match Layout to Content**: Use `center` for emphasis, `two-cols` for comparisons
2. **Consistent Section Markers**: Use `section` layout consistently
3. **Image Quality**: Use high-resolution images for `cover` and `image` layouts
4. **Test Responsiveness**: Check how layouts appear at different sizes
5. **Don't Overcrowd**: Layouts work best with focused content

## Common Layout Patterns

### Presentation Structure

```markdown
---
layout: cover
---
# Title

---
layout: intro
---
# About Me

---
layout: section
---
# Part 1

---
layout: default
---
# Content...

---
layout: section
---
# Part 2

---
layout: end
---
# Thank You
```

### Feature Comparison

```markdown
---
layout: two-cols-header
---

# React vs Vue

::left::
## React
- JSX syntax
- Large ecosystem
- Facebook backing

::right::
## Vue
- Template syntax
- Gentle learning curve
- Community driven
```

## Output Format

When recommending layouts, provide:

```
SLIDE STRUCTURE:
1. [layout: cover] - Opening with title
2. [layout: intro] - Speaker introduction
3. [layout: section] - Topic 1 header
4. [layout: default/two-cols] - Content slides
5. [layout: section] - Topic 2 header
6. [layout: image-right] - Demo/screenshot
7. [layout: fact] - Key statistic
8. [layout: end] - Closing

LAYOUT RECOMMENDATION:
- For this content type, use [layout]
- Reason: [explanation]

EXAMPLE:
---
layout: [recommended]
[additional options if needed]
---

[Content structure]
```
