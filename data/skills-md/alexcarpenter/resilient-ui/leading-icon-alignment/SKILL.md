---
name: leading-icon-alignment
description: Ensures leading icons in lists are properly aligned to the first line of text when text wraps, preventing icons from vertically centering across multiple lines. Use when implementing list items with leading icons, SVG icons in flex containers, or when fixing icon alignment issues in wrapped text.
license: MIT
metadata:
  version: "1.0.0"
  author: alexcarpenter
---

# Leading Icon Alignment

Ensures leading icons within lists are always properly aligned to the first line of text when the text wraps, rather than centering vertically across the full height of the wrapped text.

## Rules

- **MUST**: Use `flex` on the list item container
- **MUST**: Use height on the SVG that matches the line height of the adjacent text `height: 1lh` (or `h-lh` in Tailwind)
- **MUST**: Use `flex-shrink: 0` (`shrink-0` in Tailwind) on the icon to prevent it from compressing at narrow widths
- **NEVER**: Use `align-items: center` (`items-center` in Tailwind) on the flex container — it vertically centers the icon across all lines of wrapped text instead of aligning to the first line

## Implementation

```html
<ul>
  <li class="flex gap-2">
    <svg
      class="h-lh w-4 shrink-0"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
    >
      <circle cx="12" cy="12" r="10" />
      <path d="m9 12 2 2 4-4" />
    </svg>
    Lorem ipsum dolor sit amet consectetur adipisicing elit.
  </li>
</ul>
```

## Key Points

- The SVG height uses (`h-lh`) to match the text line height so the icon visually centers within the first line of text
- `shrink-0` prevents the icon from compressing when the container is narrow — without it the icon distorts before text wraps
- Flex defaults to `align-items: stretch`, but because the SVG has a fixed height, it effectively sits at the top — aligned to the first line
- `gap-2` provides consistent spacing between icon and text without needing padding or margin on either element
