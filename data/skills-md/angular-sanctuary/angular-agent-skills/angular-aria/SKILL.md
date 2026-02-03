---
name: angular-aria
description: Headless accessible UI primitives implementing WAI-ARIA patterns for Angular
metadata:
  author: Gerome Grignon
  version: "2026.2.2"
  source: Generated from https://github.com/angular/angular, scripts located at https://github.com/angular-sanctuary/angular-agent-skills
---

> The skill is based on Angular Aria (from Angular repository), generated at 2026-02-02.

Angular Aria is a collection of headless, accessible directives that implement common WAI-ARIA patterns. The directives handle keyboard interactions, ARIA attributes, focus management, and screen reader support—you provide the HTML structure, CSS styling, and business logic.

Install via `npm install @angular/aria`.

## When to Apply

Use this skill when:

- Building **custom accessible UI components** that need WAI-ARIA compliance
- Implementing **keyboard navigation** patterns (arrow keys, Enter, Escape, Tab)
- Adding **focus management** to interactive widgets
- Creating **headless/unstyled** UI primitives with custom styling
- Building **autocomplete**, **combobox**, **listbox**, **select**, or **multiselect** inputs
- Implementing **menus**, **menubars**, or **toolbars** with proper ARIA roles
- Creating **accordion**, **tabs**, **tree**, or **grid** patterns
- Needing **screen reader support** for custom components

Do NOT use this skill when:

- Using Angular Material components (they have built-in accessibility)
- Building simple forms with native HTML elements
- The WAI-ARIA pattern you need is not covered by Angular Aria

## Core

| Topic | Description | Reference |
|-------|-------------|-----------|
| Overview | Introduction to Angular Aria, when to use, what's included | [core-overview](references/core-overview.md) |

## Search and Selection

| Topic | Description | Reference |
|-------|-------------|-----------|
| Autocomplete | Text input with filtered suggestions as users type | [selection-autocomplete](references/selection-autocomplete.md) |
| Combobox | Primitive directive coordinating text input with popup | [selection-combobox](references/selection-combobox.md) |
| Listbox | Single or multi-select option lists with keyboard navigation | [selection-listbox](references/selection-listbox.md) |
| Select | Single-selection dropdown pattern | [selection-select](references/selection-select.md) |
| Multiselect | Multiple-selection dropdown with compact display | [selection-multiselect](references/selection-multiselect.md) |

## Navigation and Actions

| Topic | Description | Reference |
|-------|-------------|-----------|
| Menu | Dropdown menus with nested submenus and keyboard shortcuts | [navigation-menu](references/navigation-menu.md) |
| Menubar | Horizontal navigation bar for persistent application menus | [navigation-menubar](references/navigation-menubar.md) |
| Toolbar | Grouped sets of controls with logical keyboard navigation | [navigation-toolbar](references/navigation-toolbar.md) |

## Content Organization

| Topic | Description | Reference |
|-------|-------------|-----------|
| Accordion | Collapsible content panels with expand/collapse | [content-accordion](references/content-accordion.md) |
| Tabs | Tabbed interfaces with automatic or manual activation | [content-tabs](references/content-tabs.md) |
| Tree | Hierarchical lists with expand/collapse | [content-tree](references/content-tree.md) |
| Grid | Two-dimensional data with cell-by-cell keyboard navigation | [content-grid](references/content-grid.md) |
