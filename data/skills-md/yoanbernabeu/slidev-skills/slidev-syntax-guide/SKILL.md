---
name: slidev-syntax-guide
description: Master Slidev's extended Markdown syntax. Use this skill to write slides with advanced formatting, frontmatter, and special features.
---

# Slidev Syntax Guide

This skill covers Slidev's extended Markdown syntax, including slide separators, frontmatter, notes, MDC syntax, and all the special formatting features available.

## When to Use This Skill

- Learning Slidev's Markdown extensions
- Writing complex slide content
- Using advanced formatting features
- Troubleshooting syntax issues
- Converting standard Markdown to Slidev format

## Slide Separators

### Basic Separator

Use three dashes with blank lines:

```markdown
# Slide 1

Content here

---

# Slide 2

More content
```

### Separator with Frontmatter

Add per-slide configuration:

```markdown
# Slide 1

---
layout: center
class: text-blue-500
---

# Centered Blue Slide
```

## Frontmatter

### Global Configuration (First Slide)

```yaml
---
theme: seriph
title: My Presentation
info: |
  ## Presentation Description
  Multi-line info text
colorSchema: auto
highlighter: shiki
drawings:
  persist: false
transition: slide-left
mdc: true
---
```

### Per-Slide Configuration

```yaml
---
layout: two-cols
class: my-custom-class
transition: fade
clicks: 3
disabled: false
hide: false
---
```

### Common Frontmatter Options

| Option | Type | Description |
|--------|------|-------------|
| `layout` | string | Slide layout name |
| `class` | string | CSS classes |
| `transition` | string | Slide transition |
| `background` | string | Background image/color |
| `clicks` | number | Total clicks for slide |
| `disabled` | boolean | Disable slide |
| `hide` | boolean | Hide from navigation |
| `preload` | boolean | Preload heavy content |

## Speaker Notes

### Comment Syntax

```markdown
# My Slide

Visible content

<!--
These are speaker notes.
- Point to remember
- Another point

Supports **Markdown** formatting.
-->
```

### Notes Position

Notes must be at the end of the slide, after all content.

## MDC Syntax (Markdown Components)

Enable in frontmatter:

```yaml
---
mdc: true
---
```

### Inline Styles

```markdown
This is [important text]{.text-red-500.font-bold}

This has a [tooltip]{title="Hover me!"}
```

### Block Styles

```markdown
::div{.flex.gap-4}
Content inside a flex container
::

::section{#my-section .bg-blue-100}
Section with ID and class
::
```

### Component Syntax

```markdown
:Icon{name="carbon:arrow-right" size="24"}

::Alert{type="warning"}
Warning message here
::
```

## Lists

### Standard Lists

```markdown
- Item 1
- Item 2
  - Nested item
  - Another nested
- Item 3

1. First
2. Second
3. Third
```

### Click-Animated Lists

```markdown
<v-clicks>

- Appears first
- Appears second
- Appears third

</v-clicks>
```

Or with depth:

```markdown
<v-clicks depth="2">

- Parent 1
  - Child 1.1
  - Child 1.2
- Parent 2
  - Child 2.1

</v-clicks>
```

## Images

### Basic Image

```markdown
![Alt text](/images/photo.jpg)
```

### Sized Image

```markdown
![Alt text](/images/photo.jpg){width=400}
```

### Styled Image

```markdown
![Alt text](/images/photo.jpg){.rounded-lg.shadow-xl}
```

### Background Image (via frontmatter)

```yaml
---
background: /images/cover.jpg
class: text-white
---

# Title Over Image
```

## Links

### Standard Links

```markdown
[Slidev Documentation](https://sli.dev)
```

### Navigation Links

```markdown
[Go to slide 5](/5)
[Go to slide with ID](#my-slide)
```

### External Link with New Tab

```markdown
<a href="https://sli.dev" target="_blank">Open in new tab</a>
```

## Tables

```markdown
| Feature | Supported |
|---------|-----------|
| Markdown | ✅ |
| Vue Components | ✅ |
| Animations | ✅ |
| Export | ✅ |
```

## Blockquotes

```markdown
> This is a quote
> spanning multiple lines

> [!NOTE]
> GitHub-style callout
```

## Horizontal Rules

```markdown
Content above

---

Content below (this also creates a new slide!)
```

Use `<hr>` for a rule without slide break:

```markdown
Content above

<hr>

Content below (same slide)
```

## HTML in Markdown

### Inline HTML

```markdown
This is <span class="text-red-500">red text</span> inline.
```

### Block HTML

```markdown
<div class="grid grid-cols-2 gap-4">
  <div>Column 1</div>
  <div>Column 2</div>
</div>
```

## Escaping

### Escape Code Block Markers

Use more backticks than the content:

````markdown
Here's how to write a code block:

```js
const x = 1
```
````

### Escape Frontmatter

```markdown
\---
This is not frontmatter
\---
```

## Slots Syntax

For layouts with multiple content areas:

```markdown
---
layout: two-cols
---

# Left side content

::right::

# Right side content
```

### Named Slots

```markdown
---
layout: my-custom-layout
---

::header::
Header content

::default::
Main content

::footer::
Footer content
```

## Global Layers

### Top Layer (Above All Slides)

Create `global-top.vue`:

```vue
<template>
  <div class="absolute top-0 left-0 p-4">
    <img src="/logo.png" class="h-8" />
  </div>
</template>
```

### Bottom Layer (Below All Slides)

Create `global-bottom.vue`:

```vue
<template>
  <div class="absolute bottom-0 right-0 p-4 text-sm">
    © 2025 My Company
  </div>
</template>
```

## Scoped Styles

Add CSS for a single slide:

```markdown
# Styled Slide

<style>
h1 {
  color: #2563eb;
  font-size: 3em;
}
</style>
```

## Special Characters

### Emojis

```markdown
🚀 Rocket launch!
👋 Hello world!
```

### Icons (with UnoCSS)

```markdown
<carbon-arrow-right class="inline" />
<mdi-github class="text-2xl" />
```

## Best Practices

1. **Consistent Frontmatter**: Use the same structure across slides
2. **Meaningful IDs**: Add IDs to slides you'll link to
3. **Organize Notes**: Keep speaker notes concise and actionable
4. **Use MDC Sparingly**: Don't overuse inline styles
5. **Test Separators**: Ensure blank lines around `---`

## Common Syntax Errors

❌ **Missing blank lines**
```markdown
# Slide 1
---
# Slide 2
```

✓ **Correct**
```markdown
# Slide 1

---

# Slide 2
```

❌ **Invalid YAML**
```yaml
---
theme:default
---
```

✓ **Correct YAML**
```yaml
---
theme: default
---
```

❌ **Notes before content**
```markdown
<!--
Notes first
-->
# Heading
```

✓ **Notes at end**
```markdown
# Heading

Content

<!--
Notes at the end
-->
```

## Output Format

When writing Slidev content, follow this structure:

```markdown
---
[FRONTMATTER: theme, layout, class, etc.]
---

# [SLIDE TITLE]

[MAIN CONTENT]
- Use Markdown formatting
- Include code blocks where relevant
- Add images with proper paths

[OPTIONAL: Vue components or HTML]

<!--
[SPEAKER NOTES]
- Key points to mention
- Timing notes
-->
```
