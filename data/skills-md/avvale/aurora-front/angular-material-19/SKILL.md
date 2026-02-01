---
name: angular-material-19
description: >
    Angular Material 19 components, Material 3 theming, CDK with 2D drag-drop,
    timepicker, custom form controls, and dark mode. Trigger: When using
    Material components, creating custom controls, working with CDK, or theming.
license: MIT
metadata:
    author: aurora
    version: '3.0'
    material_version: '19.x'
    auto_invoke:
        'Material components, CDK, ControlValueAccessor, MatFormFieldControl,
        dialogs, tables, theming, timepicker'
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## When to Use

- Using Angular Material 19 components
- Creating custom form controls with signal-based patterns
- Implementing Material 3 theming with CSS variables
- Setting up dark/light mode switching
- Using CDK features (2D Drag & Drop, Overlay, A11y)
- Working with the new timepicker component

**Reference files** (loaded on demand):

- [timepicker.md](timepicker.md) — Timepicker usage, intervals, validation
- [theming.md](theming.md) — M3 theming, dark mode, override mixins, theme service
- [cdk-patterns.md](cdk-patterns.md) — 2D drag-drop, tab reorder, overlay, selection
- [custom-controls.md](custom-controls.md) — ControlValueAccessor, MatFormFieldControl with signals

---

## Angular Material 19 Key Changes

### Material 3 (M3) is Stable

Material 3 is now the default design system. Key features:

- **Design tokens as CSS variables** — All styling via `--mat-*` variables
- **`light-dark()` function** — Native CSS for theme switching
- **Component override mixins** — Granular customization without specificity wars
- **New "Styling" tab** — Each component's docs now shows override API

### New Components in v19

- **Timepicker** (`mat-timepicker`) — Native time selection → see [timepicker.md](timepicker.md)
- **2D Drag & Drop** — Mixed orientation support in CDK → see [cdk-patterns.md](cdk-patterns.md)
- **Tab reordering** — Draggable tabs with CDK

---

## Quick Reference: Common Imports

```typescript
// Forms
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatTimepickerModule } from '@angular/material/timepicker'; // NEW v19
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';

// Buttons & Icons
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

// Layout
import { MatCardModule } from '@angular/material/card';
import { MatTabsModule } from '@angular/material/tabs';
import { MatExpansionModule } from '@angular/material/expansion';

// Data Display
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatSortModule } from '@angular/material/sort';
import { MatChipsModule } from '@angular/material/chips';
import { MatTooltipModule } from '@angular/material/tooltip';

// Feedback
import { MatDialogModule } from '@angular/material/dialog';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

// CDK
import { DragDropModule } from '@angular/cdk/drag-drop';
import { OverlayModule } from '@angular/cdk/overlay';
```

---

## Material Dialog Pattern

```typescript
import { Component, inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef, MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';

@Component({
    selector: 'confirm-dialog',
    imports: [MatDialogModule, MatButtonModule],
    template: `
        <h2 mat-dialog-title>{{ data.title }}</h2>
        <mat-dialog-content>
            <p>{{ data.message }}</p>
        </mat-dialog-content>
        <mat-dialog-actions align="end">
            <button mat-button mat-dialog-close>Cancel</button>
            <button mat-flat-button color="warn" [mat-dialog-close]="true">
                {{ data.confirmText ?? 'Confirm' }}
            </button>
        </mat-dialog-actions>
    `,
})
export class ConfirmDialogComponent
{
    readonly data = inject<{ title: string; message: string; confirmText?: string }>(MAT_DIALOG_DATA);
}
```

---

## Material Table with Signals

```typescript
import { Component, signal, computed, viewChild } from '@angular/core';
import { MatTableModule } from '@angular/material/table';
import { MatSortModule, MatSort, Sort } from '@angular/material/sort';
import { MatPaginatorModule, MatPaginator, PageEvent } from '@angular/material/paginator';

@Component({
    selector: 'app-data-table',
    imports: [MatTableModule, MatSortModule, MatPaginatorModule],
    template: `
        <table [dataSource]="dataSource()" mat-table matSort
               (matSortChange)="onSortChange($event)">
            <!-- columns -->
            <tr *matHeaderRowDef="displayedColumns" mat-header-row></tr>
            <tr *matRowDef="let row; columns: displayedColumns" mat-row></tr>
        </table>
        <mat-paginator [length]="totalItems()" [pageSize]="pageSize()"
                       [pageSizeOptions]="[10, 25, 50]"
                       (page)="onPageChange($event)"></mat-paginator>
    `,
})
export class DataTableComponent {
    data = signal<any[]>([]);
    totalItems = signal(0);
    pageSize = signal(10);
    sort = viewChild(MatSort);
    paginator = viewChild(MatPaginator);
    displayedColumns = ['name', 'email', 'actions'];
    dataSource = computed(() => this.data());

    onSortChange(sort: Sort): void { /* update & reload */ }
    onPageChange(event: PageEvent): void { /* update & reload */ }
}
```

---

## Anti-Patterns

| Avoid                                         | Do Instead                                    |
| --------------------------------------------- | --------------------------------------------- |
| `@ViewChild(MatSort)` decorator               | `viewChild(MatSort)` signal query             |
| Manual `stateChanges.next()` calls everywhere | Use `effect()` to auto-emit on signal changes |
| Importing entire Material module              | Import only needed component modules          |
| Using `any` for dialog data                   | Create typed interfaces                       |
| Hardcoded colors in components                | Use `--mat-sys-*` CSS variables               |
| `@media (prefers-color-scheme)` manually      | Use `light-dark()` function in theme          |
| Custom dark mode class logic                  | Set `color-scheme: light dark` on html        |
| Using third-party timepicker                  | Use native `mat-timepicker` (v19+)            |

---

## Migration Checklist

- [ ] Replace third-party timepicker with `mat-timepicker`
- [ ] Convert `@ViewChild` queries to signal queries
- [ ] Update theming to use M3 `mat.theme()` mixin
- [ ] Implement dark mode with `light-dark()` function
- [ ] Use component override mixins instead of deep CSS selectors
- [ ] Convert custom controls to use signals internally

---

## Related Skills

| Skill        | When to Use Together                       |
| ------------ | ------------------------------------------ |
| `angular-19` | Angular 19 patterns, signals, resource API |
| `tailwind`   | Combined Tailwind + Material styling       |
| `typescript` | TypeScript patterns for typed components   |

---

## Resources

- [Angular Material Docs](https://material.angular.dev/)
- [Material 3 Theming Guide](https://material.angular.dev/guide/theming)
- [Timepicker Component](https://material.angular.dev/components/timepicker)
- [CDK Drag & Drop](https://material.angular.dev/cdk/drag-drop)
