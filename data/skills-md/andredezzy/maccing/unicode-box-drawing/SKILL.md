---
name: unicode-box-drawing
description: Unicode box drawing patterns for ASCII diagrams, flow charts, and structured text layouts in documentation and code comments.
---

# Unicode Box Drawing Patterns

Guidelines for creating properly aligned, readable Unicode box diagrams.

## When to Apply

- Drawing ASCII/Unicode diagrams in code comments or documentation
- Creating flow charts, state machines, or architecture diagrams
- Documenting CLI output formats or terminal interfaces
- Building text-based UI mockups
- Reviewing diagram alignment issues
- Writing technical documentation with visual structures

## Rule Categories by Priority

| Priority | Prefix | Category |
|----------|--------|----------|
| CRITICAL | `padding-` | Right-padding and fixed width alignment |
| HIGH | `spacing-` | Breathing room and whitespace |
| HIGH | `layout-` | Centering and nested box calculations |
| MEDIUM | `chars-` | Character selection and consistency |

## Quick Reference

### Critical Rules

| Rule ID | Description |
|---------|-------------|
| `padding-right` | Every content line MUST be padded to full width before closing │ |
| `padding-fixed-width` | All lines in a box MUST have identical character count |

### High Priority Rules

| Rule ID | Description |
|---------|-------------|
| `spacing-breathing-room` | Empty line after ┌───┐ or ├───┤, and before └───┘ or ├───┤ |
| `layout-centering` | Always center nested boxes and flow diagrams within parent |
| `layout-width-limit` | Keep diagrams under 70 characters for compatibility |
| `layout-nested-math` | Calculate: left_pad + inner_content + right_pad = content_width |

### Character Rules

| Rule ID | Description |
|---------|-------------|
| `chars-single-set` | Never mix Unicode box chars with ASCII on same line |
| `chars-light-lines` | Use light lines (─ │ ┌ ┐ └ ┘) for best compatibility |
| `chars-monospace` | Only renders correctly in monospace fonts |

## Box Width Formula

```
Border formula:    ┌ + (width-2 × ─) + ┐ = total width
Content formula:   │ + (width-2 chars) + │ = total width
                       ↑
                       Content + right-padding spaces
```

For a 65-character wide box:
- Border: `┌` + 63×`─` + `┐` = 65 chars
- Content: `│` + 63 chars (content + padding) + `│` = 65 chars

## Unicode Characters Reference

### Light Lines (Recommended)

```
Corners:     ┌ ┐ └ ┘
Lines:       ─ │
T-junctions: ├ ┤ ┬ ┴
Cross:       ┼
```

### Arrows

```
Simple:      → ← ↓ ↑
Filled:      ▶ ◀ ▼ ▲
Double:      ⇒ ⇐ ⇓ ⇑
```

## Common Patterns

### Simple Box

```
┌───────────────────────────────────────────────────────────────┐
│                           TITLE                               │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│   Content with proper right-padding                           │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### Horizontal Flow

```
┌───────────┐      ┌───────────┐      ┌───────────┐
│  Step 1   │─────▶│  Step 2   │─────▶│  Step 3   │
└───────────┘      └───────────┘      └───────────┘
```

### Vertical Flow

```
┌─────────────────┐
│     Parent      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     Child       │
└─────────────────┘
```

## Pre-Commit Checklist

- [ ] All lines in each box have IDENTICAL character count
- [ ] Content lines have right-padding before closing │
- [ ] Empty line AFTER every ┌───┐ opening
- [ ] Empty line BEFORE every └───┘ closing
- [ ] Empty lines around every ├───┤ divider
- [ ] Nested boxes have breathing room at ALL levels
- [ ] Flow content is CENTERED within parent box
- [ ] Total width ≤ 70 characters
- [ ] No mixed ASCII/Unicode characters

## How to Use

Each rule file in `rules/` contains:
1. Rule explanation with rationale
2. WRONG example showing the anti-pattern
3. CORRECT example showing proper implementation
4. Verification steps

## Recommended Tools

| Tool | URL | Platform |
|------|-----|----------|
| ASCIIFlow | asciiflow.com | Web, free |
| Monodraw | monodraw.helftone.com | macOS, paid |
| Textik | textik.com | Web, free |
| Diagon | arthursonzogni.com/Diagon | Web, free |

## References

- [ASCIIFlow](https://asciiflow.com/): Free web-based Unicode diagram editor
- [Box-drawing characters (Wikipedia)](https://en.wikipedia.org/wiki/Box-drawing_characters)
- [Unicode Box Drawing Block](https://www.unicode.org/charts/PDF/U2500.pdf)
