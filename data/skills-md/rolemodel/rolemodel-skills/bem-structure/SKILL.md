---
name: bem-structure
description: Expert guidance for writing, refactoring, and structuring CSS using BEM (Block Element Modifier) methodology. Provides proper CSS class naming conventions, component structure, and Optics design system integration for maintainable, scalable stylesheets.
metadata:
  triggers:
    - css review
    - bem structure
    - bem methodology
    - css best practices
    - refactor css
    - bem-ify
---

## Overview

This skill guides AI in writing CSS using the BEM (Block Element Modifier) methodology for creating maintainable, scalable, and reusable stylesheets with clear naming conventions and component structure, while exercising judgment about scope, risk, and architectural impact. It also should use BEM in conjunction with Optics, our RoleModel design system, so that it's not recreating things that already exist. If there is already an Optics component that fits the need, it should be used and/or overridden as necessary instead of creating a new BEM block.

The agent should prioritize clarity, predictability, and minimal unintended side effects.

Keywords: CSS review, BEM structure, BEM methodology, CSS best practices, Refactor CSS, Review CSS, Fix my CSS, Fix my BEM, BEM-ify my CSS

## What is BEM?

BEM stands for **Block Element Modifier** - a methodology that helps you create reusable components and code sharing in front-end development.

| Pattern | Syntax | Example |
|---------|--------|---------|
| **Block** | `.block` | `.card` |
| **Element** | `.block__element` | `.card__title` |
| **Block Modifier** | `.block--modifier` | `.card--elevated` |
| **Element Modifier** | `.block__element--modifier` | `.card__title--large` |
| **Multi-word names** | `.block-name` | `.user-profile` |

### Naming Convention

- As with any other development, intention revealing names are important.
- In BEM, the intention we are trying to convey in naming is not based on the styling that gets applied or its appearance, but rather its purpose in the interface. 
- Specific styling typically makes for bad naming with the exception of modifiers (small, large, padded, etc.). 
- Naming after the specific workflow can, in certain cases, be acceptable. (calendar with days). 
- Naming after the shared type of workflow tends to be the sweet spot. (form, table, card, button). 
- Naming after the broader UI abstraction is not always necessary, but can be used for abstract cases with no context required (primary, large, etc). 
- Be specific enough to convey purpose clearly, but general enough to allow for reuse if applicable. Reuse won't always be possible or desirable, so don't push it too far. 
- Try to use names that are explicit and not open to interpretation. This will need to be considered most often for modifiers.
- Use flat BEM classes with explicit `&` usage for modifiers.
- DOM structure does not need to follow CSS class structure.

If you're not able to follow these guidelines due to project constraints or other reasons, please document the reasons for the deviation in the chat output.

### Basic Syntax

✅ GOOD (Do this)
```css
.block {
  .block__element {
    &.block__element--modifier { }
  }
  
  &.block--modifier { }
}
```
``` html
<div class="block">
  <div class="block__element">...</div>
  <div class="block__element block__element--modifier">...</div>
</div>

<div class="block block--modifier">
  <div class="block__element">...</div>
  <div class="block__element">...</div>
</div>
```

🚫 BAD (Don't do this)
```css
.block {
  .block--modifier { } /* Use `&` before all Modifier class names */
}

.block_element { /* Use `__` between Blocks and Elements and nest Element within the Block */
  &.block__element-modifier { } /* Use `--` between the Modifier and its Element */
}
```
``` html
<div class="block">...</div>  
<div class="block__element">...</div> <!-- Incorrect; Element has become the Block -->
  <div class="block__element--modifier">...</div> <!-- Incorrect; Modifier must be accompanied by a corresponding Element -->
</div>

<div class="block__element"> <!-- Incorrect; Element must be accompanied by a corresponding Block -->
  <div class="block__element">...</div> <!-- Incorrect; Do not nest an element within itself -->
</div>
```

## Rule Summary

- All class names MUST be fully explicit BEM. Nesting is allowed for organization, but selectors should not rely on tag names or IDs.
- `&` may be used only as a textual reference to the full selector
- `&` MUST NOT be used to construct class names (`&--`, `&__`)
- Nesting is for organization only; explicit BEM class names are required. Nested selectors may be used to scope elements under their block if desired.
- `&` may be used to co-locate modifiers with their Block or Element while keeping selectors explicit.

✅ GOOD (Do this)
```css
.card {
  &.card--featured {}
  &.card--compact {}
  &.card--featured {
    &.card--compact {}
  }
}
```

🚫 BAD (Don't do this)
```css
.card {
  &--featured {}
  &__title {}
  &__title--large {}
}
```
---
### Block
Encapsulates a standalone entity that is meaningful on its own. While blocks can be nested and interact with each other, semantically they remain equal; there is no precedence or hierarchy. Holistic entities without DOM representation (such as controllers or models) can be blocks as well.

#### Naming:
Block names may consist of lowercase Latin letters, digits, and dashes. To form a CSS class, add a short prefix for namespacing: `.block`. Spaces in long block names are replaced by dash.

#### HTML: 
Any DOM node can be a block if it accepts a class name.

✅ GOOD (Do this)
```html
<div class="card">...</div>
<div class="button">...</div>
<div class="menu">...</div>
<div class="header">...</div>
<div class="search-form">...</div>
<div class="user-profile">...</div>
<div class="modal">...</div>
<div class="navigation">...</div>
<div class="dropdown-menu">...</div>
```

🚫 BAD (Don't do this)
```html
<div class="searchForm">...</div>
<div class="button_primary">...</div>
<div class="userProfile">...</div>
<div class="dropdown__menu">...</div>  <!-- Don't use element syntax for blocks -->
```

#### CSS:
Use class name selector only. No tag name or IDs. No dependency on other blocks/elements on a page.

✅ GOOD (Do this)
```css
.card { }
.button { }
.menu { }
.header { }
.search-form { }
.user-profile { }
.modal { }
.navigation { }
.dropdown-menu { }
```

🚫 BAD (Don't do this)
```css
.searchForm {}
.button_primary {}
.userProfile {}
.dropdown__menu {} /* Don't use element syntax for blocks */
}
```
---
### Element
Parts of a block and have no standalone meaning. Any element is semantically tied to its block.

#### Naming:
Element names may consist of lowercase Latin letters, digits, dashes and underscores. CSS class is formed as block name plus two underscores plus element name: `.block__elem`. Spaces in long element names are replaced by dash.

#### HTML: 
Any DOM node within a block can be an element. Within a given block, all elements are semantically equal. An element should not be used outside of the block that contains it in the CSS.

✅ GOOD (Do this)
```html
<div class='block'>
  <div class='block__element'>
    <div class='block2'>
      <div class='block2__element'>...</div>
    </div>
  </div>
</div>
```

🚫 BAD (Don't do this)
```html
<div class='block'>
  <div class='block__element'>
    <div class='element__element'>...</div> <!-- Incorrect; element has become the block -->
  </div>
</div>
```

#### CSS:
In the CSS, elements should be nested inside of the block they belong to. The structure doesn't need to match the DOM structure.

✅ GOOD (Do this)
```css
/* Card block with elements */
.card { /* This is the block; elements are inside */
  .card__header { }
  .card__title { }
  .card__body { }
  .card__footer { }
  .card__image { }
}

/* Menu block with elements */
.menu {
  .menu__item { }
  .menu__link { }
  .menu__icon { }
}

/* Search form block with elements */
.search-form {
  .search-form__input { }
  .search-form__button { }
  .search-form__label { }
}
```

🚫 BAD (Don't do this)
```css
/* Don't create deeply nested element names */
.menu {
  .menu__item { }
  .menu__item__link { } /* Improper naming structure */
  .menu__item__link__icon { } /* Improper naming structure */
}
```
---
### Modifier
Flags on blocks or elements. Use them to change appearance, behavior or state.

#### Naming: 
Modifier names may consist of lowercase Latin letters, digits, dashes and underscores. CSS class is formed as block’s or element’s name plus two dashes: `.block--modifier` or `.block__elem--modifier` and `.block--color-black` with `.block--color-red`. Spaces in complicated modifiers are replaced by dash. 

Modifiers should be used over creating separate elements when:
- The change is a simple state change (e.g., active, disabled, highlighted)
- The change is a simple appearance change (e.g., size, color, layout)
- The change does not introduce new content or functionality that would require additional elements

If you have a default state for an element and another that would be a modifier, add the default styles to the base element and use the modifier to override those styles when the modifier is applied. Don't create an exclusive element for the default and also don't create two modifiers for this case.

🚫 BAD (Don't do this)
```css
.music-entry__artwork-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.music-entry__artwork-placeholder {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--color-tan) 0%, var(--color-beige) 100%);
}
```
✅ GOOD (Do this)
```css
.music-entry__artwork-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  
  &.music-entry__artwork-image--placeholder {
    object-fit: unset;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, var(--color-tan) 0%, var(--color-beige) 100%);
  }
}
```

#### HTML:
Modifier is an extra class name which you add to a block/element DOM node. Add modifier classes only to blocks/elements they modify, and keep the original class. To be clear, a modifier class should always be used in conjunction with its base block/element class.

✅ GOOD (Do this)
```html
<div class="block block--modifier">...</div>
<div class="block block--size-big block--shadow-yes">...</div>
```

🚫 BAD (Don't do this)
```html
<div class="block--modifier utility">...</div> <!-- Missing base block class and using utility class -->
```

#### CSS: 
✅ GOOD (Do this)
```css
.menu {
  .menu__item {
    &.menu__item--active { }
  }
  .menu__link { }
  .menu__icon { }
  
  &.menu--padded { }
}
```

🚫 BAD (Don't do this)
```css
.menu {
  .menu__item {
    .menu__item--active { } /* No ampersand */
  }
  
  .menu__link { }
  .menu-link-active { } /* Bad name structure */
  .menu__icon { }
  
  .menu__padded { } /* Improper modifier structure; should be using `&` and `--`, not `__` */
}
```

## Miscellaneous Rules
- Classes only (no IDs)
- Flat classes and selectors only
- No tag-based styling
- No styling based on DOM hierarchy
- One conceptual responsibility per Block
- Blocks can contain blocks if needed
- Elements do not exist outside their Block
- Use **kebab-case** for multi-word names: `.user-profile`, `.dropdown-menu`
- Use **double underscore** (`__`) to separate block from element in element names
- Use **double dash** (`--`) to separate block/element from modifier in modifier names
- Keep names semantic, descriptive, and intention-revealing (not appearance-based)
- Avoid abbreviations that aren't universally understood

### Syntax Example
Suppose you have block form with modifiers `theme: "xmas"` and `simple: true` and with elements `input` and `submit`, and element `submit` with its own modifier `disabled: true` for not submitting form while it is not filled:

✅ GOOD (Do this)
```html
<form class="form form--theme-xmas form--simple">
  <input class="form__input" type="text" />
  <input
    class="form__submit form__submit--disabled"
    type="submit" />
</form>
```

```css
.form {
  .form__input { }
  .form__submit {
    &.form__submit--disabled { }
  }
  
  &.form--simple { }
  &.form--theme-xmas { }
}
```

🚫 BAD (Don't do this)
```html
<form class="form form-simple form--theme-xmas "> <!-- Incorrect; cannot have multiple blocks -->
  <input class="form_input" type="text" /> <!-- Incorrect; must use `__` between Block and Element  -->
  <input
    class="form__submit--disabled" <!-- Incorrect; missing Element -->
    type="submit" />
</form>
```

```css
.form {
  .form__input { }
  .form_submit { /* Use `__` between Block and Element */
    .form__submit--disabled { } /* Use `&` before all Modifier class names */
  }
  
  &.form-simple { }  /* Use `--` between Element and Modifier */
}

&.form--theme-xmas { } /* Must nest Elements and Modifiers within Block */
```
