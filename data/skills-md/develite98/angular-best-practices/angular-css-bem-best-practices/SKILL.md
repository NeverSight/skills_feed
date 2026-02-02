---
name: angular-css-bem-best-practices
description: Angular + BEM CSS methodology guide for creating reusable components and shareable front-end code. Enforces component-scoped BEM blocks, max 2-level nesting, proper component decomposition, semantic element naming, correct modifier patterns, and flat selectors. Use when writing, reviewing, or refactoring Angular component styles. Triggers on tasks involving CSS, SCSS, SASS, component styling, BEM naming, or CSS architecture.
license: MIT
metadata:
  author: community
  version: "1.0.0"
---

# Angular + BEM CSS Best Practices

A methodology guide for combining Angular's component architecture with BEM (Block Element Modifier) CSS naming convention to create reusable components and enable code sharing in front-end development. Contains 6 rules with bad/good examples in CSS, SCSS, and SASS.

## When to Apply

Reference these guidelines when:
- Writing CSS/SCSS/SASS for Angular components
- Naming CSS classes in Angular templates
- Reviewing component styles for consistency
- Deciding whether to split a component based on styling complexity
- Setting up CSS architecture for a new Angular project
- Refactoring existing styles to follow BEM methodology

## Core Principles

- **1 Component = 1 BEM Block** — The block name matches the component selector
- **Max 2 Levels** — Only `Block` and `Block__Element`, never `Block__Element__SubElement`
- **Split When Deep** — If you need a third level, extract a child component
- **Flat Selectors** — No descendant, child, or tag-qualified selectors
- **Semantic Names** — Element names describe _what_, not _how_ or _where_
- **Modifiers for Variants** — Use `--modifier` for states and variants, always with the base class

## Rule Categories by Priority

| Priority | Rule | Impact | File |
|----------|------|--------|------|
| 1 | Block = Component Selector | CRITICAL | `bem-block-selector` |
| 2 | Max 2 Levels of Nesting | CRITICAL | `bem-max-nesting` |
| 3 | Split Child Components | CRITICAL | `bem-split-components` |
| 4 | Element Naming Conventions | HIGH | `bem-element-naming` |
| 5 | Modifier Patterns | HIGH | `bem-modifier-patterns` |
| 6 | No Cascading Selectors | HIGH | `bem-no-cascading` |

## Quick Reference

### 1. Block = Component Selector (CRITICAL)

- `bem-block-selector` - BEM block name must match the Angular component selector (minus prefix)

### 2. Maximum 2 Levels (CRITICAL)

- `bem-max-nesting` - Never nest beyond `.block__element` — no `.block__element__subelement`

### 3. Split Child Components (CRITICAL)

- `bem-split-components` - Extract child components when BEM depth would exceed 2 levels

### 4. Element Naming (HIGH)

- `bem-element-naming` - Use semantic, descriptive kebab-case names for BEM elements

### 5. Modifier Patterns (HIGH)

- `bem-modifier-patterns` - Use `--modifier` correctly for states and variants with Angular class bindings

### 6. No Cascading (HIGH)

- `bem-no-cascading` - Avoid descendant, child, and tag-qualified selectors — keep BEM flat

## BEM Cheat Sheet

```
.block                    → Component root (matches selector)
.block__element           → Child part of the component
.block--modifier          → Variant of the entire block
.block__element--modifier → Variant of a single element

✅ .user-card
✅ .user-card__avatar
✅ .user-card--featured
✅ .user-card__name--highlighted

❌ .user-card__header__title       (3 levels)
❌ .user-card .user-card__avatar   (descendant selector)
❌ div.user-card                   (tag-qualified)
```

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/bem-block-selector.md
rules/bem-max-nesting.md
rules/bem-split-components.md
rules/bem-element-naming.md
rules/bem-modifier-patterns.md
rules/bem-no-cascading.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code examples (CSS, SCSS, SASS)
- Correct code examples (CSS, SCSS, SASS)
- Angular component integration patterns
- Summary table and references

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
