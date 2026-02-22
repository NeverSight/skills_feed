---
name: trailing-icon-alignment
description: Ensures trailing icons remain visually attached to the last line of text when text wraps. Use when implementing inline text with trailing icons, external link indicators, or when fixing trailing icon alignment issues in wrapped text.
license: MIT
metadata:
  version: "1.0.0"
  author: alexcarpenter
---

# Trailing Icon Alignment

Ensures trailing icons always remain visually attached to the last line of text when the text wraps, preventing the icon from being orphaned on a new line.

## Rules

- **MUST**: Use `relative inline-block` on the container element
- **MUST**: Use padding-right (`pr-5` or equivalent) to reserve space for the icon
- **MUST**: Use `absolute inline` positioning on the SVG icon
- **MUST**: Use height on the SVG that matches the line height of the text (`h-6` or equivalent)
- **NEVER**: Place the icon as a flex sibling or block-level sibling — it will not wrap with the text

## Implementation

```html
<a href="/" class="relative inline-block pr-5">
  View documentation
  <svg
    class="absolute ml-1 inline h-lh w-4 shrink-0"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    stroke-width="2"
    stroke-linecap="round"
    stroke-linejoin="round"
  >
    <path d="M7 7h10v10" />
    <path d="M7 17 17 7" />
  </svg>
</a>
```

## Key Points

- `inline-block` on the container causes the trailing padding and icon to stay attached to the last word, wrapping together as a unit
- `pr-5` (padding-right) must be at least as wide as the icon (`w-4`) to prevent text overlap
- `absolute` positions the icon within its container; `inline` keeps it participating in the text flow
- This approach prevents the icon from being orphaned on a new line at narrow widths
