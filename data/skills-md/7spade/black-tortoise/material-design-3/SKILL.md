---
name: material-design-3
description: Material Design 3 (Material You) design system knowledge for modern web and Angular applications. Use when implementing Material Design 3 theming, components, typography, color systems, dynamic color, accessibility patterns, or migrating from Material Design 2. Covers design tokens, theming APIs, and Material You principles.
license: MIT
---

# Material Design 3 (Material You) Skill

## 🎯 Purpose
This skill provides comprehensive guidance on **Material Design 3** (also known as Material You), Google's latest design system that emphasizes personalization, accessibility, and modern UI patterns for Angular applications.

## 📦 What is Material Design 3?

Material Design 3 is Google's latest design language that introduces:
- **Dynamic Color**: Adaptive color palettes based on user preferences
- **Enhanced Accessibility**: WCAG 2.1 AA compliance by default
- **Flexible Theming**: Token-based theming system
- **Modern Components**: Updated component designs with better customization
- **Personalization**: User-centric design that adapts to preferences

## 🎨 When to Use This Skill

Use Material Design 3 guidance when:
- Implementing a new Angular application with Material Design
- Migrating from Material Design 2 to Material Design 3
- Creating custom themes using Material Design 3 tokens
- Implementing dynamic color theming
- Building accessible, modern UI components
- Following Material You design principles
- Working with Material Design 3 typography and spacing systems

## 🛠️ Core Concepts

### 1. Color System

Material Design 3 introduces a sophisticated color system:

**Color Roles:**
- **Primary**: Main brand color for prominent actions
- **Secondary**: Supporting color for less prominent actions
- **Tertiary**: Accent color for highlights and contrasts
- **Error**: Color for error states
- **Surface**: Background colors for components
- **On-colors**: Contrasting text/icon colors (on-primary, on-secondary, etc.)

**Color Variants:**
- Container colors (e.g., `primary-container`)
- On-container colors (e.g., `on-primary-container`)
- Surface variants (surface-dim, surface-bright, surface-container)

### 2. Dynamic Color

Material Design 3's signature feature:
- Generate color schemes from source colors
- Support both light and dark themes
- Automatic contrast adjustments
- System-level color extraction (from wallpaper on supported platforms)

### 3. Typography

Five typography scales:
- **Display**: Largest text (display-large, display-medium, display-small)
- **Headline**: Section headers (headline-large to headline-small)
- **Title**: Subsection titles (title-large to title-small)
- **Body**: Main content (body-large, body-medium, body-small)
- **Label**: UI labels (label-large to label-small)

### 4. Elevation

Three elevation strategies:
- **Shadow**: Traditional elevation with shadows
- **Overlay**: Tonal surface overlays
- **Combined**: Shadow + overlay for enhanced depth perception

### 5. Shape

Rounded corner system with four scales:
- **None**: 0dp (sharp corners)
- **Extra Small**: 4dp
- **Small**: 8dp
- **Medium**: 12dp
- **Large**: 16dp
- **Extra Large**: 28dp

## 📚 Implementation in Angular

### Setting Up Material Design 3 Theme

```scss
// Define your theme using M3 tokens
@use '@angular/material' as mat;

// Include core Material Design 3 styles
@include mat.core();

// Define your color palette
$my-primary: mat.define-palette(mat.$azure-palette);
$my-accent: mat.define-palette(mat.$blue-palette);
$my-warn: mat.define-palette(mat.$red-palette);

// Create the theme
$my-theme: mat.define-theme((
  color: (
    theme-type: light,
    primary: $my-primary,
    tertiary: $my-accent,
  ),
  typography: (
    brand-family: 'Roboto',
    bold-weight: 700
  ),
  density: (
    scale: 0
  )
));

// Apply the theme
@include mat.all-component-themes($my-theme);

// Dark theme variant
$my-dark-theme: mat.define-theme((
  color: (
    theme-type: dark,
    primary: $my-primary,
    tertiary: $my-accent,
  )
));

// Apply dark theme when needed
.dark-theme {
  @include mat.all-component-colors($my-dark-theme);
}
```

### Using Color Tokens

```scss
// Access theme colors in your components
.my-component {
  background-color: var(--mat-sys-primary);
  color: var(--mat-sys-on-primary);
  
  &:hover {
    background-color: var(--mat-sys-primary-container);
    color: var(--mat-sys-on-primary-container);
  }
}

// Surface variants
.surface {
  background-color: var(--mat-sys-surface);
  color: var(--mat-sys-on-surface);
}

.surface-container {
  background-color: var(--mat-sys-surface-container);
}
```

### Typography Usage

```scss
// Using typography tokens
.heading {
  font: var(--mat-sys-headline-large);
}

.body-text {
  font: var(--mat-sys-body-medium);
}

.label {
  font: var(--mat-sys-label-small);
}
```

### Elevation and Shadows

```scss
.elevated-card {
  // Level 1 elevation
  box-shadow: var(--mat-sys-level1);
  
  &:hover {
    // Level 2 elevation on hover
    box-shadow: var(--mat-sys-level2);
  }
}
```

## 🎯 Best Practices

### 1. Theme Consistency
- Use design tokens instead of hardcoded values
- Maintain consistent color usage across components
- Follow Material Design 3 color role guidelines

### 2. Accessibility
- Ensure minimum 4.5:1 contrast ratio for text
- Use semantic color roles (primary, secondary, error)
- Support both light and dark themes
- Provide sufficient touch target sizes (48x48dp minimum)

### 3. Responsive Design
- Use Material Design 3 breakpoints
- Adapt layouts for different screen sizes
- Test on mobile, tablet, and desktop viewports

### 4. Dynamic Theming
```typescript
// Example: Dynamic theme switching in Angular
export class ThemeService {
  private isDark = signal(false);
  
  toggleTheme() {
    this.isDark.update(dark => !dark);
    document.body.classList.toggle('dark-theme', this.isDark());
  }
  
  applyCustomColors(sourceColor: string) {
    // Generate M3 palette from source color
    const palette = this.generateM3Palette(sourceColor);
    this.applyCSSVariables(palette);
  }
}
```

## 🔧 Common Patterns

### Custom Component with M3 Tokens

```typescript
@Component({
  selector: 'app-custom-button',
  template: `
    <button class="m3-button" [class.filled]="variant === 'filled'">
      <ng-content></ng-content>
    </button>
  `,
  styles: [`
    .m3-button {
      padding: 10px 24px;
      border-radius: var(--mat-sys-corner-full);
      font: var(--mat-sys-label-large);
      border: none;
      cursor: pointer;
      
      &.filled {
        background-color: var(--mat-sys-primary);
        color: var(--mat-sys-on-primary);
        
        &:hover {
          background-color: var(--mat-sys-primary-container);
          color: var(--mat-sys-on-primary-container);
        }
      }
      
      &.outlined {
        background-color: transparent;
        border: 1px solid var(--mat-sys-outline);
        color: var(--mat-sys-primary);
      }
    }
  `]
})
export class CustomButtonComponent {
  @Input() variant: 'filled' | 'outlined' = 'filled';
}
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Colors not applying | Ensure `@include mat.core()` is called first |
| Theme tokens undefined | Check Angular Material version (requires v15+) |
| Dark theme not working | Verify `.dark-theme` class is applied to parent element |
| Custom colors not working | Use `define-palette()` with proper Material color palette |
| Typography not loading | Include Material Design fonts (Roboto) in index.html |
| Accessibility contrast issues | Use Material's built-in color roles instead of custom colors |

## 📖 References

- [Material Design 3 Official Guidelines](https://m3.material.io/)
- [Angular Material Theming Guide](https://material.angular.io/guide/theming)
- [Material Design Color System](https://m3.material.io/styles/color/system/overview)
- [Material Design Typography](https://m3.material.io/styles/typography/overview)
- [Accessibility Guidelines](https://m3.material.io/foundations/accessible-design/overview)

## 💡 Migration from Material Design 2

Key changes when migrating from M2 to M3:
1. Replace color palette with theme-type approach
2. Update component styles to use design tokens
3. Migrate custom themes to new theming API
4. Update typography from mat-typography-level to M3 tokens
5. Replace elevation mixins with CSS custom properties
6. Test accessibility with new contrast requirements

---

## 📂 Recommended Placement

**Project-level skill:**
```
/.github/skills/material-design-3/SKILL.md
```

**Personal global skill:**
```
~/.github/skills/material-design-3/SKILL.md
```

Copilot will automatically load this skill when Material Design 3 topics are mentioned.
