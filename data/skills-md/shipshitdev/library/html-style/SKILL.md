---
name: html-style
description: >
  Apply opinionated styling to barebones HTML. Use when user has plain/unstyled
  HTML and wants to apply consistent visual styling. Triggers: style this HTML,
  apply styling, make this look good, /html-style, or when user shares HTML that
  needs CSS. Transforms tables, lists, status indicators, buttons, and layouts
  into a cohesive design system.
---

# html-style

Transform barebones HTML into styled output using a specific design system.

## Workflow

1. Read the user's HTML
2. Identify elements to style (tables, lists, status text, buttons, sections)
3. Inject `<style>` block from `assets/base.css`
4. Add appropriate classes to HTML elements
5. Add interactive JS if needed (copy buttons, drafts, collapsible sections)

## Quick Class Reference

| Element | Class | Effect |
|---------|-------|--------|
| Status text | `.stale` `.warm` `.pending` | Red/green/orange inline text |
| Trend | `.trend-up` `.trend-down` | Green ↑ / Red ↓ |
| Category tag | `.tag-group` `.tag-dm` `.tag-money` | Blue/purple/orange pill |
| Status pill | `.status-success` `.status-error` `.status-pending` | Filled green/red/orange |
| Filter toggle | `.filter` `.filter.active` | Outline / filled black |
| Time filter | `.pill` `.pill.active` | Small pill, black when active |
| Stat box | `.stat` > `.stat-value` + `.stat-label` | 28px number, 12px label |
| Table | default or `.table-styled` | Minimal or colored values |
| Section header | `.section-header` | Dark bar with white text |
| Collapsible | `<details>` + `<summary>` | Native HTML collapse |
| Insight | `.insight` | Italic, yellow background |
| Tier | `.tier-gold` `.tier-silver` `.tier-bronze` | Row background colors |

## Element Styling Rules

### Tables

- Default: minimal borders, no hover
- Add `.table-styled` for: hover effect, `.positive`/`.negative` cell colors, `.highlight` rows
- Sortable: add `th.sortable` with `<a href="?sort=col">Col ▼</a>`

### Status Indicators

- **Text status** (`.stale`/`.warm`/`.pending`): Use for inline status in sentences
- **Status pills** (`.status-*`): Use for badge-style indicators, typically with icon (✓ ✗ ◷)
- **Trends** (`.trend-up`/`.trend-down`): Use for numeric changes, adds arrow automatically

### Sections

Use `.section-header` with emoji prefix for visual breaks:

```html
<div class="section-header">🔴 URGENT</div>
<div class="section-header">🟠 PENDING</div>
```

### Interactive Elements

When HTML has drafts or copy buttons, add this JS:

```javascript
function saveDraft(el) {
    localStorage.setItem('draft:' + el.dataset.threadId, el.textContent);
}
function copyToClipboard(text, btn) {
    navigator.clipboard.writeText(text).then(() => {
        btn.textContent = 'Copied!';
        setTimeout(() => btn.textContent = 'Copy', 1500);
    });
}
```

### Deep Links

Convert URLs to native app links:

- Telegram: `tg://resolve?domain=username`
- SMS: `sms:+14155551234`

## Theme

- **Default**: Light (`background: #fff`)
- **Dark mode**: Add `class="dark"` to `<body>` when user requests dark theme or context is trading/real-time

## Compatibility with Structure Skills

When styling output from `quick-view` or `table-filters`, these class mappings apply:

### quick-view classes

| Their Class | Style As |
|-------------|----------|
| `.type-user` | `.status-pending` (blue border) |
| `.type-draft` | `.status-pending` (orange border) |
| `.type-done` | `.status-success` (green border) |
| `.source` | Already styled (muted, small) |
| `.meta` | Already styled (muted header) |
| `.actions` | Inline button group |

### table-filters classes

| Their Class | Style As |
|-------------|----------|
| `.filter-bar` | Flex row with gap |
| `.filter-chips` | Inline chip container |
| `.chip` | Dark pill with `.chip-remove` |
| `.filter-menu` | Dropdown panel (`.filter-menu`) |
| `.empty-state` | Centered, muted text |

The `base.css` includes styles for these classes automatically.

## Resources

- **Full style reference**: Read [references/style-guide.md](references/style-guide.md) for detailed CSS patterns and examples
- **Base CSS**: Inject [assets/base.css](assets/base.css) into `<style>` tag in `<head>`
