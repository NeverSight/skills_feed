---
name: pencil-skill
description: Create and edit Pencil (.pen) design files programmatically. Generate UI designs as JSON-based .pen files with themes, variables, components, and layouts. Includes CLI tools for reading, searching, editing, and validating .pen files without requiring the Pencil desktop app. Requires Node.js 18+. Schema version 2.8.
---

# pencil-skill

## 1) Overview
Pencil is a design tool that uses the JSON-based `.pen` format.
Because `.pen` is Git-friendly, it is ideal for agents to create and modify directly.
The key is not generic JSON syntax, but Pencil-specific rules (`ref`, `slot`, `textGrowth`, variable binding).

## 2) Core Document Structure
```json
{
  "version": "2.8",
  "themes": {
    "mode": [
      "light",
      "dark"
    ]
  },
  "variables": {
    "color.surface": {
      "type": "color",
      "value": [
        {
          "theme": {
            "mode": "light"
          },
          "value": "#FFFFFF"
        },
        {
          "theme": {
            "mode": "dark"
          },
          "value": "#111827"
        }
      ]
    }
  },
  "children": []
}
```
- `version` and `children` are required
- `themes` and `variables` are optional, but practically essential for a design system

## 3) List of Object Types
- `rectangle`: basic rectangle
- `ellipse`: circle/arc
- `line`: line
- `polygon`: polygon
- `path`: path geometry
- `text`: text
- `frame`: layout container + can declare slots
- `group`: group container
- `note`: annotation
- `prompt`: prompt memo
- `context`: context memo
- `icon_font`: icon-font-based vector icon
- `ref`: reusable component instance

## 4) Layout (Summary)
Remember only the core properties:
- `layout`: `none | vertical | horizontal`
- `gap`, `padding`
- `justifyContent`: `start | center | end | space_between | space_around`
- `alignItems`: `start | center | end`

Gotcha:
- Child `x`, `y` values are effectively ignored inside flex (`vertical`/`horizontal`) containers

### Practical frame properties
| Property | Type | Description |
|------|------|------|
| `clip` | boolean | Clips content outside the frame bounds when `true`. Default is false |

### General entity properties (all node types)
| Property | Type | Description |
|------|------|------|
| `enabled` | boolean | Hides the node when `false` (applies to all entities, not frame-specific) |

```json
[
  {
    "type": "frame",
    "id": "modal-overlay",
    "clip": true,
    "layout": "vertical"
  },
  {
    "type": "frame",
    "id": "hidden-panel",
    "enabled": false,
    "layout": "vertical"
  }
]
```

## 5) SizingBehavior
- `fit_content`
- `fill_container`
- ``fit_content(${number})``

`width` and `height` can use numbers, variables, or the SizingBehavior values above.

## 6) Graphics Essentials
- `fill`: color / gradient / image / mesh_gradient
- `stroke`: `align`, `thickness`, `join`, `cap`, `dashPattern`, `fill`
- `effect`: `blur`, `background_blur`, `shadow`

Color values are recommended in hex format (`#RGB`, `#RRGGBB`, `#RRGGBBAA`).

## 7) Text Rules (Important)
- Set `textGrowth` first for `text`
- `textGrowth`: `auto | fixed-width | fixed-width-height`
- If you set `width`/`height` without `textGrowth`, behavior may be ignored or inconsistent

## 8) Components (`reusable` + `ref` + `descendants` + `slot`)
### Defining a component
- Add `reusable: true` to a `frame` (or another entity)
- Its `id` acts as the component key

### Creating an instance
- `type: "ref"`
- `ref: "<reusable id>"`

### descendants override
- Keys are child `id` values
- Access deep children with slash paths: `"container/button/label"`

### slot pattern
- Declare `slot: ["body"]` in the component
- Create an internal frame with `name: "body"`
- Inject content through `ref.children`

## 9) Variables
Binding format:
- `"$variable.name"`

Example:
```json
{
  "fill": "$color.surface",
  "padding": "$space.card.padding"
}
```

Validation points:
- The key after `$` must exist in `variables`
- When using theme-based variable values, they must match `themes` axis/value

## 10) IconFont
Supported families:
- `lucide`
- `feather`
- `Material Symbols Outlined`
- `Material Symbols Rounded`
- `Material Symbols Sharp`
- `phosphor`

## 11) Forbidden Patterns
| Pattern | Result |
|---|---|
| `/` in `id` (e.g., `"a/b"`) | ❌ invalid |
| Duplicate `id` values in the same file | ❌ invalid |
| `ref` points to a non-existent reusable id | ❌ invalid |
| `width/height` on text without `textGrowth` | ⚠️ warning (may be ignored) |
| `"$unknown.var"` reference | ⚠️ warning (unresolved variable) |

## Critical Rules

These rules prevent the most common mistakes agents make.

### Rule 1: Component reuse is mandatory
If a matching reusable component exists, you **must reuse it with `ref`**.

1. Check available components with `search-nodes.mjs --reusable`
2. If a matching component exists, insert it as a `ref` instance
3. Customize with `descendants`
4. Create a new one only when no match exists

### Rule 2: Variables are mandatory
**No hardcoding.** Colors, spacing, and typography must use variables.

1. Check existing variables with `get-variables.mjs`
2. Reference values in `"$variable.name"` format
3. If a new variable is needed, register it first with `set-variables.mjs`

### Rule 3: Prevent text overflow
For every text node:
1. Set `textGrowth` first (`auto` or `fixed-width`)
2. If the parent frame has layout, use `fill_container` for width
3. Validate with `validate-pen.mjs` after editing

### Rule 4: Always validate after changes
After each modification:
1. Validate structural/lint with `validate-pen.mjs`
2. Verify structure with `read-tree.mjs --depth 2`

### Rule 5: Reuse assets
For logos, images, and icons:
1. Search existing assets with `search-nodes.mjs --name "logo|brand|icon"`
2. If found, duplicate using `batch-design.mjs` `copy` op
3. Create new assets only when none exist

## 12) Required Checklist for Creation
- [ ] Root `version` and `children` exist
- [ ] `id` is unique and does not use slashes
- [ ] Target reusable component for each `ref` exists
- [ ] `variables` references match real keys (`$...`)
- [ ] `textGrowth` is set before using `width/height` on text
- [ ] When using slot, confirm `slot` declaration, `name` frame, and `ref.children` injection relationship
- [ ] Check theme axis/value consistency when needed

## Property Aliases
The schema defines both singular and plural forms in `$defs`.
On node properties, the canonical key is singular:
- `fill` (value can be single fill or array)
- `stroke` (value can be single stroke or array)
- `effect` (value can be single effect or array)

Scripts accept plural forms (`fills`, `strokes`, `effects`) and normalize them to singular keys on write.

## AGENTS.md (Agent Guide)
`AGENTS.md` is a concise guide with rule summaries and references to individual `rules/*.md` files for full details. To regenerate after editing rules: `node scripts/compile-agents.mjs`

## CLI Tools

These scripts manipulate `.pen` files directly. They work without MCP.

### Read Tools
| Script | Purpose | Usage |
|--------|------|--------|
| `read-tree.mjs` | Print node tree structure | `node scripts/read-tree.mjs file.pen [--depth 2] [--id nodeId]` |
| `search-nodes.mjs` | Search nodes | `node scripts/search-nodes.mjs file.pen --type frame [--reusable] [--name regex]` |
| `get-variables.mjs` | View variables/themes | `node scripts/get-variables.mjs file.pen [--format json]` |
| `find-space.mjs` | Find empty-space coordinates | `node scripts/find-space.mjs file.pen --width 300 --height 200` |

### Write Tools
| Script | Purpose | Usage |
|--------|------|--------|
| `batch-design.mjs` | Insert/update/delete/move/copy nodes | `node scripts/batch-design.mjs file.pen --ops '[{"op":"update","id":"node1","props":{"name":"Header"}}]'` |
| `replace-props.mjs` | Bulk property replacement | `node scripts/replace-props.mjs file.pen --match '{"fill":"#FF0000"}' --replace '{"fill":"$color.primary"}'` |
| `set-variables.mjs` | Add/update variables | `node scripts/set-variables.mjs file.pen --var 'name=type:value'` |

**set-variables.mjs theme syntax (`@theme`):**
```bash
# Single value
node scripts/set-variables.mjs file.pen --var 'color.primary=color:#0D9488'

# Per-theme variable setting — @theme syntax
node scripts/set-variables.mjs file.pen --var 'color.bg=color:#FFFFFF@light,#0F172A@dark'
node scripts/set-variables.mjs file.pen --var 'space.md=number:12'
```

### Validation Tool
| Script | Purpose | Usage |
|--------|------|--------|
| `validate-pen.mjs` | Structural validation + value-type checks + lint | `node scripts/validate-pen.mjs file.pen` |

### batch-design Operations

`batch-design.mjs` accepts operations as a JSON array:

#### insert — Insert a new node
```json
{
  "op": "insert",
  "parentId": "frame-1",
  "node": {
    "type": "text",
    "id": "title",
    "content": "Hello",
    "textGrowth": "auto"
  }
}
```

#### update — Update properties (deep merge)
```json
{
  "op": "update",
  "id": "title",
  "props": {
    "content": "Updated",
    "fill": "$color.primary"
  }
}
```

#### delete — Delete a node
```json
{
  "op": "delete",
  "id": "title"
}
```

#### move — Move to another parent
```json
{
  "op": "move",
  "id": "title",
  "toParentId": "frame-2",
  "index": 0
}
```

#### copy — Duplicate a node
```json
{
  "op": "copy",
  "id": "card-1",
  "newId": "card-2",
  "toParentId": "grid"
}
```

**Notes:**
- `toParentId` is optional. If omitted, the copied node is inserted at the root level.
- During copy, all internal child ids must remain unique → using a `newId` prefix is recommended
- Do not send too many ops at once (25 or fewer recommended)
- Backup is automatically created (`.pen.bak`)

### Standard Workflow

```
1. read-tree.mjs          → Inspect current structure
2. search-nodes.mjs       → Search reusable components
3. get-variables.mjs      → Check variables/themes
4. find-space.mjs         → Calculate frame placement coordinates
5. batch-design.mjs       → Create/modify nodes
6. validate-pen.mjs       → Validate results
```

## Design Rules

Required rules for production-grade design. 41 rules, 8 categories.

### Rule Categories by Priority

| Priority | Category | Impact | Prefix | Rules |
|----------|----------|--------|--------|-------|
| 1 | Layout & Overflow | CRITICAL | `layout-` | 8 |
| 2 | Design Tokens | CRITICAL | `token-` | 5 |
| 3 | Anti-AI Aesthetic | HIGH | `aesthetic-` | 6 |
| 4 | Component System | HIGH | `component-` | 5 |
| 5 | Typography | MEDIUM | `typo-` | 5 |
| 6 | Color System | MEDIUM | `color-` | 4 |
| 7 | Spacing System | MEDIUM | `spacing-` | 4 |
| 8 | Showcase & Style Guide | MEDIUM | `showcase-` | 4 |

### Quick Reference

#### 1. Layout & Overflow (CRITICAL)

- `layout-auto-layout` — Auto Layout is required for all containers
- `layout-sizing` — width/height rules by scenario
- `layout-overflow` — overflow prevention checklist
- `layout-responsive` — responsive simulation (separate frame)
- `layout-spacing-consistency` — gap/padding consistency
- `layout-z-order` — Z-order and overlay placement
- `layout-no-overlap` — prevent element overlap
- `layout-canvas-placement` — Top-level canvas placement, no layer overlap

#### 2. Design Tokens (CRITICAL)

- `token-naming` — naming format: $category.purpose.variant
- `token-semantic-colors` — required semantic color system
- `token-theme-required` — light/dark themes required
- `token-no-hardcode` — no hardcoding
- `token-workflow` — token setup workflow

#### 3. Anti-AI Aesthetic (HIGH)

- `aesthetic-layout` — avoid AI-looking layouts
- `aesthetic-typography` — avoid AI-looking type choices
- `aesthetic-color` — avoid AI-looking colors
- `aesthetic-decoration` — avoid AI-looking decoration
- `aesthetic-content` — avoid AI-looking content
- `aesthetic-checklist` — self-check checklist

#### 4. Component System (HIGH)

- `component-atomic` — apply Atomic Design
- `component-naming` — Figma-standard naming
- `component-variant` — variant patterns
- `component-slot` — slot patterns
- `component-reuse-first` — component reuse first

#### 5. Typography (MEDIUM)

- `typo-scale` — define type scale
- `typo-weight` — font-weight usage rules
- `typo-pairing` — type pairing guide
- `typo-line-height` — line-height rules
- `typo-text-rules` — text layout rules

#### 6. Color System (MEDIUM)

- `color-semantic` — semantic color system
- `color-accessibility` — WCAG 2.1 AA accessibility
- `color-ratio` — 60-30-10 color ratio
- `color-dark-mode` — dark mode rules

#### 7. Spacing System (MEDIUM)

- `spacing-8pt-grid` — 8pt grid system
- `spacing-proximity` — proximity principle
- `spacing-padding` — padding system
- `spacing-forbidden` — forbidden patterns

#### 8. Showcase & Style Guide (MEDIUM)

- `showcase-pre-design` — required pre-design process
- `showcase-design-system` — design-system-first principle
- `showcase-frame` — showcase frame pattern
- `showcase-final-checklist` — final QA checklist

### How to Use

Check each individual rule file for detailed explanations and code examples:

```
rules/layout-auto-layout.md
rules/token-naming.md
rules/aesthetic-layout.md
```

Agent guide with rule summaries: `AGENTS.md` — full rules in `rules/*.md`

## References

### Schema & Types
- [pen-schema.json](references/pen-schema.json): Official JSON Schema (v2.8)
- [pen-types.ts](references/pen-types.ts): TypeScript type definitions

### Conversion Guide
- [pen-to-tailwind.md](references/pen-to-tailwind.md): .pen → Tailwind CSS conversion table
- [component-patterns.md](references/component-patterns.md): UI component patterns

### Examples
- [example-card.pen](assets/example-card.pen): Complete .pen file example
- [reddit-ui.pen](assets/reddit-ui.pen): Reddit-style 3-column UI layout with reusable components
