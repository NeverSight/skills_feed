---
name: angular-material
description: Angular Material UI component library based on Material Design 3
metadata:
  author: Gerome Grignon
  version: "2026.1.31"
  source: Generated from https://github.com/angular/components, scripts located at https://github.com/angular-sanctuary/angular-agent-skills
---

> The skill is based on Angular Material v21.x (v21.2.0-next.2), generated at 2026-01-31.

Angular Material is the official UI component library for Angular, implementing Material Design 3 (M3). It provides a comprehensive set of pre-built, accessible components along with the Component Dev Kit (CDK) for building custom components.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Theming | M3 theming system with color palettes, typography, density, and CSS variables | [core-theming](references/core-theming.md) |
| Schematics | Angular CLI schematics for scaffolding components and generating themes | [core-schematics](references/core-schematics.md) |
| Component Harnesses | Test harnesses for reliable, maintainable component testing | [core-harnesses](references/core-harnesses.md) |

## Components

### Buttons & Indicators

| Topic | Description | Reference |
|-------|-------------|-----------|
| Buttons | Text, filled, FAB, icon buttons, and button toggles | [component-buttons](references/components/component-buttons.md) |
| Badge | Small status descriptors attached to elements | [component-badge](references/components/component-badge.md) |
| Icon | Vector icon display with font and SVG support | [component-icon](references/components/component-icon.md) |
| Progress | Progress bar and spinner indicators | [component-progress](references/components/component-progress.md) |

### Form Controls

| Topic | Description | Reference |
|-------|-------------|-----------|
| Form Field | Form field wrapper with labels, hints, errors | [component-form-field](references/components/component-form-field.md) |
| Input | Native input and textarea with mat-form-field | [component-input](references/components/component-input.md) |
| Select | Dropdown select with single and multiple selection | [component-select](references/components/component-select.md) |
| Autocomplete | Text input with dropdown suggestions | [component-autocomplete](references/components/component-autocomplete.md) |
| Chips | Chips for selection, filtering, and tag input | [component-chips](references/components/component-chips.md) |
| Form Controls | Checkbox, radio, slide toggle, slider | [component-form-controls](references/components/component-form-controls.md) |
| Datepicker | Date and date range pickers | [component-datepicker](references/components/component-datepicker.md) |
| Timepicker | Time selection with dropdown options | [component-timepicker](references/components/component-timepicker.md) |

### Layout

| Topic | Description | Reference |
|-------|-------------|-----------|
| Card | Content containers for text, images, actions | [component-card](references/components/component-card.md) |
| Divider | Line separator for visual content separation | [component-divider](references/components/component-divider.md) |
| Expansion | Expandable panels and accordion | [component-expansion](references/components/component-expansion.md) |
| Grid List | Two-dimensional grid layout for tiles | [component-grid-list](references/components/component-grid-list.md) |
| List | Lists for items, navigation, actions, selection | [component-list](references/components/component-list.md) |
| Tree | Hierarchical data display with flat/nested trees | [component-tree](references/components/component-tree.md) |

### Navigation

| Topic | Description | Reference |
|-------|-------------|-----------|
| Navigation | Sidenav, menu, toolbar, and tabs | [component-navigation](references/components/component-navigation.md) |
| Stepper | Wizard-like workflows with steps | [component-stepper](references/components/component-stepper.md) |

### Tables

| Topic | Description | Reference |
|-------|-------------|-----------|
| Table | Material Design data table with features | [component-table](references/components/component-table.md) |
| Sort | Sortable column headers | [component-sort](references/components/component-sort.md) |
| Paginator | Pagination controls for paged data | [component-paginator](references/components/component-paginator.md) |

### Popups & Modals

| Topic | Description | Reference |
|-------|-------------|-----------|
| Dialog | Modal dialogs with data sharing | [component-dialog](references/components/component-dialog.md) |
| Bottom Sheet | Modal panels from the bottom | [component-bottom-sheet](references/components/component-bottom-sheet.md) |
| Snackbar | Brief notification messages | [component-snackbar](references/components/component-snackbar.md) |
| Tooltip | Text labels on hover/focus | [component-tooltip](references/components/component-tooltip.md) |

## CDK (Component Development Kit)

### Overlays & Positioning

| Topic | Description | Reference |
|-------|-------------|-----------|
| Overlay | Floating panels with positioning strategies | [cdk-overlay](references/cdk/cdk-overlay.md) |
| Portal | Dynamic content rendering | [cdk-portal](references/cdk/cdk-portal.md) |
| Dialog | Unstyled modal dialog foundation | [cdk-dialog](references/cdk/cdk-dialog.md) |

### Accessibility

| Topic | Description | Reference |
|-------|-------------|-----------|
| Accessibility | Focus management, keyboard navigation, live announcer | [cdk-a11y](references/cdk/cdk-a11y.md) |

### Data & Collections

| Topic | Description | Reference |
|-------|-------------|-----------|
| Table | Foundational data table with DataSource pattern | [cdk-table](references/cdk/cdk-table.md) |
| Tree | Foundation for hierarchical tree display | [cdk-tree](references/cdk/cdk-tree.md) |
| Collections | SelectionModel for managing selection state | [cdk-collections](references/cdk/cdk-collections.md) |
| Virtual Scrolling | Performant rendering of large lists | [cdk-scrolling](references/cdk/cdk-scrolling.md) |

### Layout & Responsiveness

| Topic | Description | Reference |
|-------|-------------|-----------|
| Layout | BreakpointObserver and MediaMatcher | [cdk-layout](references/cdk/cdk-layout.md) |
| Bidi | Bidirectionality (LTR/RTL) handling | [cdk-bidi](references/cdk/cdk-bidi.md) |

### Interaction

| Topic | Description | Reference |
|-------|-------------|-----------|
| Drag and Drop | Reordering lists and transferring items | [cdk-drag-drop](references/cdk/cdk-drag-drop.md) |
| Clipboard | Copy text to system clipboard | [cdk-clipboard](references/cdk/cdk-clipboard.md) |
| Listbox | Accessible custom listbox controls | [cdk-listbox](references/cdk/cdk-listbox.md) |
| Menu | Accessible custom menus and menu bars | [cdk-menu](references/cdk/cdk-menu.md) |

### Component Foundations

| Topic | Description | Reference |
|-------|-------------|-----------|
| Accordion | Foundation for expandable panel groups | [cdk-accordion](references/cdk/cdk-accordion.md) |
| Stepper | Foundation for wizard-like workflows | [cdk-stepper](references/cdk/cdk-stepper.md) |

### Utilities

| Topic | Description | Reference |
|-------|-------------|-----------|
| Text Field | Auto-resize textarea and autofill detection | [cdk-text-field](references/cdk/cdk-text-field.md) |
| Platform | Browser and platform detection | [cdk-platform](references/cdk/cdk-platform.md) |
| Observers | Content mutation observation | [cdk-observers](references/cdk/cdk-observers.md) |
| Coercion | Input type coercion utilities | [cdk-coercion](references/cdk/cdk-coercion.md) |
| Keycodes | Keyboard key code constants | [cdk-keycodes](references/cdk/cdk-keycodes.md) |

## Advanced

| Topic | Description | Reference |
|-------|-------------|-----------|
| Custom Form Field Control | Creating custom mat-form-field controls | [advanced-custom-form-field](references/advanced-custom-form-field.md) |
| Theme Customization | CSS variables and utility classes in custom components | [advanced-theme-customization](references/advanced-theme-customization.md) |
