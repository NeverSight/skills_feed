---
name: canvas-component-composability
description:
  Design Canvas-ready React components with slots and decomposition-first
  patterns. Use when (1) Designing a component's prop/slot structure, (2) A
  component is growing too large, (3) Deciding between props vs slots, (4)
  Refactoring monolithic components, (5) Modeling repeatable list/grid content.
  Ensures Canvas compatibility.
---

Prefer small, focused components over monolithic ones with many props. When a
component starts accumulating many unrelated props, decompose it into smaller,
composable pieces.

## Reference map

Load references only as needed:

- Repeatable lists/grids and array-to-slot conversion:
  `references/repeatable-content.md`
- Slot interactivity in empty flex/grid containers:
  `references/repeatable-content.md` ("Slot container minimum size" section)

## Signs a component should be decomposed

Consider breaking up a component when it has:

- More than 6-8 props that serve distinct purposes
- Props for elements that make sense as standalone components (breadcrumbs,
  titles, metadata, navigation)
- Built-in layout assumptions that limit where the component can be used
- Multiple distinct visual sections that could be reused independently

## Use slots for flexible composition

Slots are the primary mechanism for composability. Instead of passing complex
data through props, use slots to let parent components accept child components.
This matches how Canvas users build pages by placing components inside other
components.

### When to use slots vs props

| Use slots for                         | Use props for                       |
| ------------------------------------- | ----------------------------------- |
| Variable number of child components   | Single, required values (text, URL) |
| Content that users should compose     | Configuration options (size, color) |
| Complex nested structures             | Simple data (strings, booleans)     |
| Content that varies between instances | Content consistent across instances |

### Declare slots in component.yml

Declare slots in `component.yml` and render them as named props in JSX.

For exact slot schema and constraints (map vs `[]`, slot keys, `children`
handling), follow `canvas-component-metadata` as the source of truth.

## Common decomposition patterns

### Page-level elements should be separate components

Elements that appear on many pages but are not always needed together should be
separate components.

### Extract repeated patterns into small components

When the same combination of elements is repeated, extract it:

- Date + category/tag -> `article-meta`
- Cover image + download button -> `resource-cover`
- Label + value pairs -> `metadata-item`
- Icon + text link -> `icon-link`

### Use layout components instead of built-in layouts

Do not bake two-column or grid layouts into content components. Use layout
components and compose content into them.

## When not to decompose

Keep components together when:

- They always appear together and never make sense separately
- They share significant internal state that would be awkward to lift up
- The visual design tightly couples them (for example, overlapping elements,
  shared backgrounds)
- Decomposition would create components with only 1-2 props that are not useful
  elsewhere
