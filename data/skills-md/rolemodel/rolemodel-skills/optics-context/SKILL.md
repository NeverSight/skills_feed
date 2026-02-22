---
name: optics-context
description: Use the Optics design framework for styling applications. Apply Optics classes for layout, spacing, typography, colors, and components. Use when working on CSS, styling views, or implementing design system guidelines.
metadata:
  triggers:
    - slim
    - css
    - frontend
    - design-system
    - optics
---

## Discovering Optics Classes
When you need classes follow these steps:

1. Check `skills/optics-context/assets/components.json` for the appropriate component, modifiers, and attributes.
  - Often you may need to modify these components to better fit the context or need. Use BEM CSS structure to create modifiers and variants as needed. Use existing tokens when available to ensure consistency.
2. If you don't find an appropriate component, search in `app/assets/stylesheets` for any relevant components.
3. If nothing is found, create a new component in a CSS file named after the page that we're on.
  - If you're creating new classes, always use existing CSS tokens. You can find these in the `skills/optics-context/assets/tokens.json` file.

### Modifying Optics Classes
When modifying Optics classes, follow these guidelines:

- Always ensure that changes align with the overall design system principles.
- Follow BEM naming conventions for any new classes.
- Add changes to the appropriate CSS file in `app/assets/stylesheets/components/overrides/{component.css}`.
- Ensure that you import any new css files in the `application.scss`
- Elements and modifiers should be nested under the block
- Magic numbers should be avoided
- Classes should have intentional-revealing names.

### Fixing Optics Violations
As CSS is created or modified, it's important to be looking for Optics violations. These would include:
- **Hard-coded colors**
  - `#fff`, `#FFFFFF`, `rgb(...)`, `hsl(...)`, `rgba(...)`, named colors like `white`
  - Gradients: `linear-gradient(...)` containing literals
- **Hard-coded spacing/sizing**
  - `px`, `rem`, `em`, `%` (sometimes), `vh/vw` (maybe allowed depending on policy)
  - `border-radius`, `gap`, `padding`, `margin`, `width/height` when used as spacing primitives
- **Hard-coded shadows/borders**
  - `box-shadow: 0 1px 3px rgba(...)`
  - `border: 1px solid #ddd`
- **"Almost token" mistakes**
  - `var(--op_color_primary...)` (bad separators)
  - `var(--op-color-primary-plus-one-on)` (segment order wrong)
  - Missed `--op-` prefix

When violations are found, refactor the CSS to use the appropriate Optics tokens from `skills/optics-context/assets/tokens.json`.

If no appropriate token exists, create a new token following the guidelines below.

### Creating New Optics Tokens
When creating new Optics tokens, follow these guidelines:
- Always ensure that new tokens align with the overall design system principles.
- Follow the established naming conventions for tokens.
- New tokens created within a project should use a namespace prefix related to the project to avoid conflicts. For example, a project called "Your App" might use the prefix `--ya-` for its tokens.
- Otherwise, use the standard token format as seen in the `skills/optics-context/assets/tokens.json` file.
- Occasionally, it may be helpful to create new global tokens to fit into the main Optics token set for your project. In such cases, ensure that the new token is broadly applicable and follows the established naming conventions. Usually, these tokens would be very general, such as new spacing sizes, color shades, or typography styles that could be reused across multiple parts of the application.

## Example CSS class
```css
.card {
  position: relative;
  border-radius: var(--_op-card-radius);
  background-color: var(--op-color-background);

  /* Modifiers */

  &.card--padded {
    padding: var(--op-space-medium);
  }


  /* Elements */
  .card__header,
  .card__body,
  .card__footer {
    padding: var(--op-space-medium);
  }

  .card__header {
    border-start-end-radius: var(--op-radius-medium);
    border-start-start-radius: var(--op-radius-medium);
  }

  .card__footer {
    border-end-end-radius: var(--op-radius-medium);
    border-end-start-radius: var(--op-radius-medium);
  }
}
```

## Creating Optics Components

To create a new CSS component, follow these steps:

1. Create a CSS file for the new component and import it
2. Start by defining a css `.{component-name}` selector for the component. This will serve as the base style for the component and all its variants.
3. Create modifiers for any all variants of the component you defined in the previous step. This ensures that the base style is shared consistently across all variations.
4. When creating variants of the component, use the following syntax: `.{component-name}--{variant}`. It can be helpful to nest these under the main class with a `&.{component-name}--{variant}` to ensure they only work with that component.
5. For stylistic tweaks that apply to all variants, use modifiers following the BEM (Block, Element, Modifier) syntax. The modifier class should be in the format: `.{component-name}--{modifier}` just like the other variants.

As a general policy, each CSS component should live in its own file unless very closely related.

To illustrate these concepts, let's consider an example of a button. You can use the following template as a guide:

```css
/* Define the main component */
.btn {
  /* Base styles for the button */

  /* Hover state */
  &:hover {
    /*
      Styles for the hovered button modifier
      ...
    */
  }

  /* Modifier: Large button */
  &.btn--large {
    /* Styles for the large button modifier */
  }

  /* Modifier: Disabled button */
  &.btn--disabled,
  &:disabled {
    /* Styles for the disabled button modifier */
  }
}

/* Variant: Primary button */
.btn.btn--primary {
  /*
    Specific styles for the primary button variant
    ...
  */
}
```
