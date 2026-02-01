---
name: stencil-atomic-design-system
description: Use when building a Stencil.js design system with Atomic Design methodology, design tokens, theming support, and slot-based components. Implements a multi-client architecture with standardized patterns for atoms, molecules, organisms, and templates.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Stencil.js Atomic Design System

Build a scalable, themeable design system using Stencil.js with Atomic Design principles, design tokens, and slot-based composition patterns for multi-client deployments.

## Project Structure

```
design-respec/
├── src/
│   ├── components/
│   │   # Atoms - Basic building blocks
│   │   ├── cor-button/
│   │   │   ├── cor-button.tsx
│   │   │   ├── cor-button.css
│   │   │   ├── cor-button.constants.ts
│   │   │   ├── cor-button.enums.ts
│   │   │   ├── cor-button.stories.ts
│   │   │   ├── readme.md
│   │   │   └── test/
│   │   │       └── cor-button.spec.tsx
│   │   ├── cor-icon/
│   │   ├── cor-typography/
│   │   ├── cor-separator/
│   │   # Molecules - Combined components
│   │   ├── cor-input-field/
│   │   ├── cor-toggle/
│   │   ├── cor-search-bar/
│   │   # Organisms - Complex UI structures
│   │   ├── cor-card/
│   │   ├── cor-navbar/
│   │   ├── cor-form/
│   │   # Templates - Page structures
│   │   ├── cor-page-layout/
│   │   └── cor-grid/
│   ├── assets/
│   │   └── css/
│   │       ├── index.css       # Main CSS imports
│   │       ├── base/           # Base HTML styles
│   │       └── utilities/      # Utility classes
│   └── utils/
│       └── theme-utils.ts
├── tokens/
│   ├── core/                   # Core design tokens
│   │   ├── color.tokens.json
│   │   ├── font.tokens.json
│   │   ├── space.tokens.json
│   │   ├── radius.tokens.json
│   │   ├── shadow.tokens.json
│   │   ├── border.tokens.json
│   │   ├── components/         # Component-specific tokens
│   │   └── style-dictionary.config.json
│   ├── respec/                 # RESPEC-specific tokens
│   │   └── [theme files]
│   ├── [client-name]/          # Client-specific tokens
│   │   └── [theme overrides]
│   └── generated/              # Auto-generated CSS
│       └── *.css
├── stencil.config.ts
└── package.json
```

## 1. Atomic Design Implementation

### Atoms - Foundational Elements

```typescript
// src/components/cor-button/cor-button.tsx
import { Component, Prop, h, Host } from '@stencil/core';

@Component({
  tag: 'cor-button',
  styleUrl: 'cor-button.css',
  shadow: true,
})
export class CorButton {
  /**
   * Button variant - defines the visual style
   */
  @Prop() variant: 'primary' | 'secondary' | 'tertiary' = 'primary';

  /**
   * Button size
   */
  @Prop() size: 'small' | 'medium' | 'large' = 'medium';

  /**
   * Disabled state
   */
  @Prop() disabled: boolean = false;

  render() {
    return (
      <Host
        class={{
          [`button--${this.variant}`]: true,
          [`button--${this.size}`]: true,
          'button--disabled': this.disabled,
        }}
      >
        <button disabled={this.disabled} class="button">
          <slot name="icon-left"></slot>
          <span class="button__content">
            <slot></slot>
          </span>
          <slot name="icon-right"></slot>
        </button>
      </Host>
    );
  }
}
```

```css
/* cor-button.css - Component-scoped tokens */
:host {
  /* Component-level tokens */
  --button-padding-small: var(--spacing-xs) var(--spacing-sm);
  --button-padding-medium: var(--spacing-sm) var(--spacing-md);
  --button-padding-large: var(--spacing-md) var(--spacing-lg);
  
  display: inline-block;
}

.button {
  /* Use semantic tokens from generated CSS */
  font-family: var(--font-family-pro-display);
  border-radius: var(--radius-md);
  transition: 250ms ease;
  cursor: pointer;
  border: none;
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
}

/* Size variants */
:host(.button--small) .button {
  padding: var(--button-padding-small);
  font-size: var(--font-size-sm);
}

:host(.button--medium) .button {
  padding: var(--button-padding-medium);
  font-size: var(--font-size-md);
}

:host(.button--large) .button {
  padding: var(--button-padding-large);
  font-size: var(--font-size-lg);
}

/* Variant styles using semantic tokens */
:host(.button--primary) .button {
  background: var(--color-primary-background-default);
  color: var(--color-primary-text-default);
  border: var(--spacing-px) solid var(--color-primary-border-default);
}

:host(.button--primary) .button:hover {
  background: var(--color-primary-background-hover);
  border-color: var(--color-primary-border-hover);
}

:host(.button--secondary) .button {
  background: var(--color-secondary-background-default);
  color: var(--color-secondary-text-default);
  border: var(--spacing-px) solid var(--color-secondary-border-default);
}

:host(.button--disabled) .button {
  opacity: 0.38;
  cursor: not-allowed;
}
```

### Molecules - Combined Elements

```typescript
// src/components/cor-input-field/cor-input-field.tsx
import { Component, Prop, State, Event, EventEmitter, h, Host } from '@stencil/core';

@Component({
  tag: 'cor-input-field',
  styleUrl: 'cor-input-field.css',
  shadow: true,
})
export class CorInputField {
  @Prop() label: string;
  @Prop() value: string = '';
  @Prop() error: string;
  @Prop() helperText: string;
  @Prop() required: boolean = false;
  @Prop() disabled: boolean = false;
  
  @State() focused: boolean = false;
  
  @Event() valueChange: EventEmitter<string>;

  private handleInput = (event: Event) => {
    const value = (event.target as HTMLInputElement).value;
    this.valueChange.emit(value);
  };

  render() {
    return (
      <Host
        class={{
          'input-field--focused': this.focused,
          'input-field--error': !!this.error,
          'input-field--disabled': this.disabled,
        }}
      >
        <div class="input-field">
          {this.label && (
            <label class="input-field__label">
              {this.label}
              {this.required && <span class="input-field__required">*</span>}
            </label>
          )}
          
          <div class="input-field__wrapper">
            <slot name="prefix"></slot>
            <input
              class="input-field__input"
              value={this.value}
              onInput={this.handleInput}
              onFocus={() => this.focused = true}
              onBlur={() => this.focused = false}
              disabled={this.disabled}
            />
            <slot name="suffix"></slot>
          </div>
          
          {(this.error || this.helperText) && (
            <div class="input-field__message">
              {this.error ? this.error : this.helperText}
            </div>
          )}
        </div>
      </Host>
    );
  }
}
```

### Organisms - Complex Structures

```typescript
// src/components/cor-card/cor-card.tsx
import { Component, Prop, h, Host } from '@stencil/core';

@Component({
  tag: 'cor-card',
  styleUrl: 'cor-card.css',
  shadow: true,
})
export class CorCard {
  @Prop() elevated: boolean = false;
  @Prop() interactive: boolean = false;

  render() {
    return (
      <Host
        class={{
          'card--elevated': this.elevated,
          'card--interactive': this.interactive,
        }}
      >
        <article class="card">
          <slot name="header"></slot>
          <div class="card__body">
            <slot></slot>
          </div>
          <slot name="footer"></slot>
        </article>
      </Host>
    );
  }
}
```

### Templates - Page Structures

```typescript
// src/components/cor-page-layout/cor-page-layout.tsx
import { Component, Prop, h, Host } from '@stencil/core';

@Component({
  tag: 'cor-page-layout',
  styleUrl: 'cor-page-layout.css',
  shadow: true,
})
export class CorPageLayout {
  @Prop() sidebarPosition: 'left' | 'right' = 'left';
  @Prop() hasHeader: boolean = true;
  @Prop() hasFooter: boolean = false;

  render() {
    return (
      <Host class={`layout--sidebar-${this.sidebarPosition}`}>
        <div class="layout">
          {this.hasHeader && (
            <header class="layout__header">
              <slot name="header"></slot>
            </header>
          )}
          
          <div class="layout__container">
            <aside class="layout__sidebar">
              <slot name="sidebar"></slot>
            </aside>
            
            <main class="layout__main">
              <slot></slot>
            </main>
          </div>
          
          {this.hasFooter && (
            <footer class="layout__footer">
              <slot name="footer"></slot>
            </footer>
          )}
        </div>
      </Host>
    );
  }
}
```

## 2. Design Tokens Framework

### Three-Tier Token Hierarchy

Tokens are defined in JSON format and processed by Style Dictionary to generate CSS variables.

#### Core Tokens (Foundation)
```json
/* tokens/core/color.tokens.json */
{
  "color": {
    "palette": {
      "blue": {
        "50": { "value": "#e3f2fd" },
        "100": { "value": "#bbdefb" },
        "200": { "value": "#90caf9" },
        "300": { "value": "#64b5f6" },
        "400": { "value": "#42a5f5" },
        "500": { "value": "#2196f3" },
        "600": { "value": "#1e88e5" },
        "700": { "value": "#1976d2" },
        "800": { "value": "#1565c0" },
        "900": { "value": "#0d47a1" }
      },
      "neutral": {
        "50": { "value": "#fafafa" },
        "100": { "value": "#f5f5f5" },
        "200": { "value": "#eeeeee" },
        "300": { "value": "#e0e0e0" },
        "400": { "value": "#bdbdbd" },
        "500": { "value": "#9e9e9e" },
        "600": { "value": "#757575" },
        "700": { "value": "#616161" },
        "800": { "value": "#424242" },
        "900": { "value": "#212121" }
      }
    }
  }
}
```

```json
/* tokens/core/font.tokens.json */
{
  "font": {
    "family": {
      "pro-display": {
        "value": "SF Pro Display, -apple-system, BlinkMacSystemFont, sans-serif"
      },
      "pro-text": {
        "value": "SF Pro Text, -apple-system, BlinkMacSystemFont, sans-serif"
      },
      "mono": {
        "value": "SF Mono, Monaco, monospace"
      }
    },
    "size": {
      "xs": { "value": "0.75rem" },
      "sm": { "value": "0.875rem" },
      "md": { "value": "1rem" },
      "lg": { "value": "1.125rem" },
      "xl": { "value": "1.25rem" },
      "2xl": { "value": "1.5rem" },
      "3xl": { "value": "1.875rem" },
      "4xl": { "value": "2.25rem" }
    },
    "weight": {
      "light": { "value": "300" },
      "regular": { "value": "400" },
      "medium": { "value": "500" },
      "semi-bold": { "value": "600" },
      "bold": { "value": "700" }
    }
  },
  "lineHeight": {
    "tight": { "value": "1.25" },
    "base": { "value": "1.5" },
    "relaxed": { "value": "1.75" }
  }
}
```

```json
/* tokens/core/space.tokens.json */
{
  "space": {
    "px": { "value": "1px" },
    "2xs": { "value": "0.125rem" },
    "xs": { "value": "0.25rem" },
    "sm": { "value": "0.5rem" },
    "md": { "value": "0.75rem" },
    "lg": { "value": "1rem" },
    "xl": { "value": "1.5rem" },
    "2xl": { "value": "2rem" },
    "3xl": { "value": "2.5rem" },
    "4xl": { "value": "3rem" },
    "5xl": { "value": "4rem" },
    "6xl": { "value": "5rem" },
    "7xl": { "value": "6rem" }
  }
}

/* tokens/core/radius.tokens.json */
{
  "radius": {
    "none": { "value": "0" },
    "sm": { "value": "0.25rem" },
    "md": { "value": "0.5rem" },
    "lg": { "value": "0.75rem" },
    "xl": { "value": "1rem" },
    "2xl": { "value": "1.5rem" },
    "3xl": { "value": "2rem" },
    "full": { "value": "9999px" }
  }
}
```

#### Component Tokens
```json
/* tokens/core/components/button.tokens.json */
{
  "button": {
    "primary": {
      "background": {
        "default": { "value": "{color.palette.blue.600}" },
        "hover": { "value": "{color.palette.blue.700}" },
        "active": { "value": "{color.palette.blue.800}" },
        "disabled": { "value": "{color.palette.blue.200}" }
      },
      "text": {
        "default": { "value": "#ffffff" },
        "disabled": { "value": "{color.palette.neutral.400}" }
      },
      "border": {
        "default": { "value": "{color.palette.blue.600}" },
        "hover": { "value": "{color.palette.blue.700}" }
      }
    },
    "secondary": {
      "background": {
        "default": { "value": "transparent" },
        "hover": { "value": "{color.palette.neutral.100}" },
        "active": { "value": "{color.palette.neutral.200}" }
      },
      "text": {
        "default": { "value": "{color.palette.neutral.900}" },
        "disabled": { "value": "{color.palette.neutral.400}" }
      },
      "border": {
        "default": { "value": "{color.palette.neutral.300}" },
        "hover": { "value": "{color.palette.neutral.400}" }
      }
    }
  }
}
```

#### Theme Support
```css
/* src/tokens/semantic/themes.css */
/* Light theme (default) */
:root,
[data-theme="light"] {
  --ds-color-background: white;
  --ds-color-surface: white;
  --ds-color-text-primary: var(--ds-color-gray-900);
  --ds-color-text-secondary: var(--ds-color-gray-600);
}

/* Dark theme */
[data-theme="dark"] {
  --ds-color-background: var(--ds-color-gray-900);
  --ds-color-surface: var(--ds-color-gray-800);
  --ds-color-text-primary: white;
  --ds-color-text-secondary: var(--ds-color-gray-300);
  --ds-border-color: var(--ds-color-gray-700);
}
```

### Global CSS Setup
```css
/* src/assets/css/index.css */
@import 'base/html.css';
@import 'utilities/scrollbars.css';
@import 'utilities/overlays.css';

/* Import generated tokens - these are auto-generated from JSON */
/* Tokens will be available as CSS variables like:
   --color-primary-background-default
   --font-family-pro-display
   --spacing-md
   --radius-lg
   etc.
*/
```

### Token Processing with Style Dictionary

```json
/* tokens/core/style-dictionary.config.json */
{
  "source": ["tokens/core/**/*.json"],
  "platforms": {
    "css": {
      "transformGroup": "css",
      "buildPath": "../generated/",
      "files": [
        {
          "destination": "core.css",
          "format": "css/variables"
        }
      ]
    }
  }
}
```

## 3. Slot-Based Component Architecture

### Why Slots Over Props

Slots provide better flexibility, composability, and performance for content projection:

```typescript
// ❌ Prop-based (avoid)
@Component({ tag: 'ds-button-bad' })
export class BadButton {
  @Prop() label: string;
  @Prop() iconLeft: string;
  @Prop() iconRight: string;
  
  render() {
    return (
      <button>
        {this.iconLeft && <ds-icon name={this.iconLeft} />}
        {this.label}
        {this.iconRight && <ds-icon name={this.iconRight} />}
      </button>
    );
  }
}

// ✅ Slot-based (preferred)
@Component({ tag: 'ds-button' })
export class Button {
  render() {
    return (
      <button>
        <slot name="icon-left"></slot>
        <slot></slot>
        <slot name="icon-right"></slot>
      </button>
    );
  }
}
```

### Slot Patterns

#### Default and Named Slots
```typescript
@Component({ tag: 'ds-modal' })
export class Modal {
  render() {
    return (
      <div class="modal">
        <div class="modal__header">
          <slot name="header"></slot>
        </div>
        <div class="modal__body">
          <slot></slot> {/* Default slot */}
        </div>
        <div class="modal__footer">
          <slot name="footer"></slot>
        </div>
      </div>
    );
  }
}
```

Usage:
```html
<ds-modal>
  <h2 slot="header">Modal Title</h2>
  <p>This is the body content in the default slot</p>
  <div slot="footer">
    <ds-button>Cancel</ds-button>
    <ds-button variant="primary">Confirm</ds-button>
  </div>
</ds-modal>
```

#### Conditional Slot Rendering
```typescript
@Component({ tag: 'ds-alert' })
export class Alert {
  @Element() el: HTMLElement;
  @State() hasIcon: boolean = false;
  
  componentWillLoad() {
    // Check if slot has content
    this.hasIcon = !!this.el.querySelector('[slot="icon"]');
  }
  
  render() {
    return (
      <div class={{ 'alert': true, 'alert--has-icon': this.hasIcon }}>
        {this.hasIcon && (
          <div class="alert__icon">
            <slot name="icon"></slot>
          </div>
        )}
        <div class="alert__content">
          <slot></slot>
        </div>
      </div>
    );
  }
}
```

#### Slot Fallback Content
```typescript
@Component({ tag: 'ds-avatar' })
export class Avatar {
  @Prop() name: string;
  
  render() {
    const initials = this.name
      ?.split(' ')
      .map(word => word[0])
      .join('')
      .toUpperCase();
    
    return (
      <div class="avatar">
        <slot>
          {/* Fallback content when slot is empty */}
          <span class="avatar__initials">{initials}</span>
        </slot>
      </div>
    );
  }
}
```

## 4. Multi-Client Theming Architecture

### Theme Structure

```
tokens/
├── core/                   # Base design tokens
├── respec/                # RESPEC-specific overrides
├── [client-name]/         # Client-specific tokens
└── generated/             # Auto-generated CSS from Style Dictionary
    ├── core.css
    ├── respec.css
    └── [client-name].css
```

### Build Configuration

```typescript
// stencil.config.ts
import { Config } from '@stencil/core';
import { reactOutputTarget as react } from '@stencil/react-output-target';
import { postcss } from '@stencil/postcss';
import postcssNested from 'postcss-nested';

export const config: Config = {
  namespace: 'design-system',
  srcDir: 'src',
  globalStyle: 'src/assets/css/index.css',
  outputTargets: [
    {
      type: 'dist',
      esmLoaderPath: '../loader',
      copy: [
        {
          src: '../tokens/generated/*.css',
          dest: 'tokens',
          warn: false,
        },
      ],
    },
    {
      type: 'dist-custom-elements',
      copy: [
        {
          src: '**/*.{jpg,png}',
          dest: 'dist/components/assets',
          warn: true,
        },
      ],
    },
    {
      type: 'docs-readme',
    },
    {
      type: 'www',
      serviceWorker: null,
    },
    // Conditional React output
    react({
      outDir: '../react-design-system/src/components/stencil-generated/',
    }),
  ],
  plugins: [
    postcss({
      plugins: [postcssNested()],
    }),
  ],
};
```

### Build Scripts

```json
// package.json
{
  "scripts": {
    "build": "npm run tokens:build && stencil build",
    "build:react": "npm run tokens:build && stencil build --react",
    "start": "stencil build --dev --watch --serve",
    "test": "stencil test --spec --e2e",
    "test:watch": "stencil test --spec --e2e --watchAll",
    "tokens:build": "style-dictionary build --config ./tokens/core/style-dictionary.config.json",
    "storybook": "storybook dev -p 6006",
    "build-storybook": "storybook build"
  }
}
```

## 5. Component File Structure

Each component follows this structure:

```
src/components/cor-[component-name]/
├── cor-[component-name].tsx           # Component implementation
├── cor-[component-name].css           # Component styles
├── cor-[component-name].enums.ts      # Enums for props
├── cor-[component-name].constants.ts  # Constants
├── cor-[component-name].stories.ts    # Storybook stories
├── readme.md                          # Auto-generated docs
└── test/
    ├── cor-[component-name].spec.tsx  # Unit tests
    └── cor-[component-name].e2e.ts   # E2E tests
```

## 6. CSS Variable Naming Convention

The project uses flat CSS variable naming without prefixes:

```css
/* Generated from tokens */
--color-primary-background-default
--color-primary-background-hover
--font-family-pro-display
--font-size-md
--spacing-lg
--radius-md
--shadow-sm
--line-height-base
--font-weight-semi-bold
```

## 7. Best Practices

### Component Development
1. **Use cor- prefix** for all components
2. **Slot-based composition** over props for content
3. **Enums for prop values** in separate .enums.ts files
4. **Constants** in separate .constants.ts files
5. **TypeScript strict mode** for type safety
6. **CSS variables** for all design tokens
7. **PostCSS with nested syntax** for styles

### Token Management
1. **JSON format** for token definitions
2. **Style Dictionary** for token processing
3. **Three-tier hierarchy**: Core → Theme → Component
4. **Reference tokens** using `{token.path}` syntax
5. **Auto-generate CSS** from JSON tokens

### Testing
1. **Unit tests** with `@stencil/core/testing`
2. **E2E tests** for user interactions
3. **Storybook stories** for visual testing
4. **Test file naming**: `*.spec.tsx` for unit, `*.e2e.ts` for E2E

### Documentation
1. **JSDoc comments** for public APIs
2. **Auto-generated readme** from component metadata
3. **Storybook** for interactive documentation
4. **Component stories** showing all variations
