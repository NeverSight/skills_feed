---
name: angular-material-v20
description: Angular Material v20 UI component library for Angular 20+ applications. Use when implementing Material Design components, theming, forms, tables, dialogs, navigation, or building Material-based UI. Covers component APIs, accessibility, and best practices for Material 20.
license: MIT
---

# Angular Material v20 Skill

## Rules

### Installation
- Use `ng add @angular/material` for automatic setup
- Must install `@angular/material@~20.0.0` and `@angular/cdk@~20.0.0` together

### Component Imports
- Import specific component modules (e.g., `MatDialogModule`, `MatFormFieldModule`)
- Use standalone components with explicit imports array
- NEVER import entire Material library

### Theming
- Use `@use '@angular/material' as mat;` syntax
- Include `mat.core()` before theme definitions
- Define theme with `mat.define-light-theme()` or `mat.define-dark-theme()`
- Include `mat.all-component-themes($theme)` to apply theme

### Form Fields
- Wrap `matInput` elements in `<mat-form-field>`
- Use `appearance` attribute: `outline`, `fill`, or `standard`
- Include `<mat-label>` for accessibility
- Show errors with `<mat-error>` when field is invalid and touched

### Dialog Usage
- Inject `MatDialog` service
- Use `dialog.open(Component, config)` to open dialogs
- Configure dialog with `width`, `data`, and other options
- Access dialog data via `MAT_DIALOG_DATA` injection token

### Accessibility
- Follow ARIA guidelines for all components
- Include aria-labels where text content is not visible
- Ensure keyboard navigation works for all interactive elements

### Change Detection
- Use `OnPush` change detection strategy
- Leverage signals for reactive state management

### Performance
- Lazy load Material modules when possible
- Import only required component modules
- Use virtual scrolling for large lists with `cdk-virtual-scroll-viewport`

---

## Context

### Summary
Angular Material v20 is the official Material Design component library for Angular 20+ applications, providing pre-built UI components with theming support and accessibility features.

### When to Use This Skill

Activate this skill when you need to:
- Implement Material Design components in Angular applications
- Set up or customize Material theming
- Work with form controls (inputs, selects, checkboxes, datepickers)
- Create navigation components (toolbar, sidenav, menu, tabs)
- Build layouts with cards, expansion panels, steppers
- Display data in tables with sorting and pagination
- Show dialogs, snackbars, tooltips, or bottom sheets
- Ensure WCAG accessibility compliance
- Optimize Material component performance

### Core Components

#### Form Controls
- MatInput - Text input fields
- MatSelect - Dropdown selection
- MatCheckbox - Checkbox inputs
- MatRadioButton - Radio button groups
- MatSlideToggle - Toggle switches
- MatSlider - Slider inputs
- MatDatepicker - Date selection

#### Navigation
- MatToolbar - Top navigation bar
- MatSidenav - Side navigation drawer
- MatMenu - Dropdown menus
- MatTabs - Tabbed navigation

#### Layout
- MatCard - Card containers
- MatDivider - Visual separators
- MatExpansionPanel - Collapsible panels
- MatGridList - Grid layouts
- MatList - List displays
- MatStepper - Step-by-step workflows

#### Buttons & Indicators
- MatButton - Button variants
- MatButtonToggle - Toggle button groups
- MatBadge - Notification badges
- MatChip - Chip elements
- MatIcon - Icon display
- MatProgressBar - Linear progress
- MatProgressSpinner - Circular progress

#### Popups & Modals
- MatDialog - Modal dialogs
- MatSnackBar - Toast notifications
- MatTooltip - Hover tooltips
- MatBottomSheet - Bottom sheet modals

#### Data Tables
- MatTable - Data table display
- MatSort - Column sorting
- MatPaginator - Table pagination

### Theming Example

```typescript
// styles.scss
@use '@angular/material' as mat;

@include mat.core();

$my-primary: mat.define-palette(mat.$indigo-palette);
$my-accent: mat.define-palette(mat.$pink-palette);
$my-warn: mat.define-palette(mat.$red-palette);

$my-theme: mat.define-light-theme((
  color: (
    primary: $my-primary,
    accent: $my-accent,
    warn: $my-warn,
  )
));

@include mat.all-component-themes($my-theme);
```

### Dialog Example

```typescript
import { Component, inject } from '@angular/core';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';

@Component({
  selector: 'app-example',
  standalone: true,
  imports: [MatDialogModule],
  template: `
    <button mat-raised-button (click)="openDialog()">
      Open Dialog
    </button>
  `
})
export class ExampleComponent {
  dialog = inject(MatDialog);
  
  openDialog() {
    this.dialog.open(MyDialogComponent, {
      width: '400px',
      data: { name: 'Example' }
    });
  }
}
```

### Form Field Example

```typescript
import { Component } from '@angular/core';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-form',
  standalone: true,
  imports: [MatFormFieldModule, MatInputModule, ReactiveFormsModule],
  template: `
    <mat-form-field appearance="outline">
      <mat-label>Email</mat-label>
      <input matInput [formControl]="email" />
      <mat-error *ngIf="email.hasError('required')">
        Email is required
      </mat-error>
    </mat-form-field>
  `
})
export class FormComponent {
  email = new FormControl('', Validators.required);
}
```

### Best Practices

1. **Import modules** - Import specific component modules for better tree-shaking
2. **Use theming** - Leverage Material's theming system for consistent styling
3. **Accessibility** - Follow ARIA guidelines and ensure keyboard navigation
4. **OnPush** - Use OnPush change detection with signals for better performance
5. **Lazy loading** - Lazy load Material modules where possible to reduce initial bundle size

### References

- [Material Design Guidelines](https://material.io/design)
- [Angular Material Docs](https://material.angular.io)
- [Component API](https://material.angular.io/components/categories)
