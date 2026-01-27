---
name: angular-material
description: Angular Material component library expertise for Angular 20+ applications. Use when implementing Material Design components (buttons, forms, dialogs, tables, navigation), theming, accessibility, or building Angular UI with pre-built Material components. Covers all Material modules, component APIs, and best practices.
license: MIT
---

# Angular Material Component Library Skill

## Rules

### Setup and Configuration
- Must install `@angular/material`, `@angular/cdk`, `@angular/animations`
- Must configure `provideAnimations()` in `app.config.ts`
- Must import specific Material modules (e.g., `MatButtonModule`, `MatIconModule`)
- Must NOT import all Material modules with wildcard (`import * as Material`)

### Form Controls
- Must wrap all `matInput` in `<mat-form-field>` with `<mat-label>`
- Must use `appearance="outline"` or `appearance="fill"` for form fields
- Must use Reactive Forms with Material form controls
- Must provide validation error messages with `<mat-error>`
- Must use `MatDatepickerModule` with `MatNativeDateModule` for date pickers

### Navigation Components
- Must set explicit height on `<mat-sidenav-container>`
- Must use `mat-nav-list` for navigation lists with `@for` and `track`
- Must use `color` attribute for semantic styling (`primary`, `accent`, `warn`)

### Buttons and Icons
- Must use appropriate button variant: `mat-button`, `mat-raised-button`, `mat-flat-button`, `mat-stroked-button`, `mat-icon-button`, `mat-fab`, `mat-mini-fab`
- Must provide `aria-label` for icon-only buttons
- Must import Material Icons font in `index.html`

### Data Tables
- Must define `displayedColumns` for table columns
- Must use `matColumnDef`, `mat-header-cell`, `mat-cell` for column definition
- Must use `MatSort` directive with `mat-sort-header` for sorting
- Must set `dataSource.sort` and `dataSource.paginator` in `ngAfterViewInit()`
- Must use `MatPaginator` with `[pageSize]` and `[pageSizeOptions]`

### Dialogs and Popups
- Must inject `MatDialog` service to open dialogs
- Must use `<h2 mat-dialog-title>`, `<mat-dialog-content>`, `<mat-dialog-actions>` structure
- Must use `[mat-dialog-close]` for dialog action buttons
- Must configure dialog width in open options
- Must subscribe to `afterClosed()` for dialog results

### Theming
- Must use `@use '@angular/material' as mat` in SCSS
- Must define custom palettes with `mat.define-palette()`
- Must create theme with `mat.define-light-theme()` or `mat.define-dark-theme()`
- Must include `@include mat.all-component-themes($theme)`

### Accessibility
- Must provide labels for all form fields
- Must add ARIA attributes for icon-only buttons
- Must ensure keyboard navigation support
- Must use semantic color attributes (`primary`, `accent`, `warn`)

### Performance
- Must import only needed Material modules
- Must use `@defer` for lazy loading heavy components
- Must use virtual scrolling for large lists

---

## Context

### Summary
Angular Material is the official Material Design component library for Angular, providing 50+ production-ready components with built-in accessibility, theming, and TypeScript support.

### When to Use This Skill
- Building Angular applications with Material Design
- Implementing forms with Material form controls
- Creating data tables with sorting, pagination, and filtering
- Building navigation with Material sidenav and toolbars
- Implementing dialogs, snackbars, and bottom sheets
- Using Material icons and buttons
- Creating custom themes
- Ensuring accessibility compliance

### Installation

```bash
# Using Angular CLI (recommended)
ng add @angular/material

# Or using npm/pnpm
pnpm install @angular/material @angular/cdk @angular/animations
```

### Application Setup

```typescript
// app.config.ts (Angular 20+ standalone)
import { provideAnimations } from '@angular/platform-browser/animations';

export const appConfig: ApplicationConfig = {
  providers: [
    provideAnimations(),
    // ... other providers
  ]
};
```

### Component Import Example

```typescript
// In standalone component
import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatToolbarModule } from '@angular/material/toolbar';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [MatButtonModule, MatIconModule, MatToolbarModule],
  template: `
    <mat-toolbar color="primary">
      <span>My App</span>
      <span class="spacer"></span>
      <button mat-icon-button>
        <mat-icon>menu</mat-icon>
      </button>
    </mat-toolbar>
  `
})
export class HeaderComponent {}
```

## 📚 Core Component Categories

### 1. Form Controls

**Input & Text Fields:**
```typescript
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { FormControl, ReactiveFormsModule } from '@angular/forms';

@Component({
  standalone: true,
  imports: [MatFormFieldModule, MatInputModule, ReactiveFormsModule],
  template: `
    <mat-form-field appearance="outline">
      <mat-label>Email</mat-label>
      <input matInput [formControl]="email" placeholder="user@example.com">
      <mat-hint>Enter your email address</mat-hint>
      @if (email.hasError('email')) {
        <mat-error>Invalid email format</mat-error>
      }
    </mat-form-field>
  `
})
export class EmailInputComponent {
  email = new FormControl('', [Validators.required, Validators.email]);
}
```

**Select & Autocomplete:**
```typescript
import { MatSelectModule } from '@angular/material/select';
import { MatAutocompleteModule } from '@angular/material/autocomplete';

// Select example
<mat-form-field>
  <mat-label>Country</mat-label>
  <mat-select [formControl]="country">
    @for (country of countries; track country.code) {
      <mat-option [value]="country.code">{{ country.name }}</mat-option>
    }
  </mat-select>
</mat-form-field>

// Autocomplete example
<mat-form-field>
  <mat-label>Search</mat-label>
  <input matInput [formControl]="search" [matAutocomplete]="auto">
  <mat-autocomplete #auto="matAutocomplete">
    @for (option of filteredOptions(); track option) {
      <mat-option [value]="option">{{ option }}</mat-option>
    }
  </mat-autocomplete>
</mat-form-field>
```

**Checkboxes & Radio Buttons:**
```typescript
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatRadioModule } from '@angular/material/radio';

// Checkbox
<mat-checkbox [formControl]="agreeToTerms">
  I agree to terms and conditions
</mat-checkbox>

// Radio group
<mat-radio-group [formControl]="selectedOption">
  <mat-radio-button value="option1">Option 1</mat-radio-button>
  <mat-radio-button value="option2">Option 2</mat-radio-button>
</mat-radio-group>
```

**Date & Time Pickers:**
```typescript
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';

<mat-form-field>
  <mat-label>Choose a date</mat-label>
  <input matInput [matDatepicker]="picker" [formControl]="selectedDate">
  <mat-datepicker-toggle matIconSuffix [for]="picker"></mat-datepicker-toggle>
  <mat-datepicker #picker></mat-datepicker>
</mat-form-field>
```

### 2. Navigation Components

**Toolbar:**
```typescript
import { MatToolbarModule } from '@angular/material/toolbar';

<mat-toolbar color="primary">
  <button mat-icon-button>
    <mat-icon>menu</mat-icon>
  </button>
  <span>Application Title</span>
  <span class="spacer"></span>
  <button mat-icon-button>
    <mat-icon>account_circle</mat-icon>
  </button>
</mat-toolbar>
```

**Sidenav:**
```typescript
import { MatSidenavModule } from '@angular/material/sidenav';

<mat-sidenav-container class="sidenav-container">
  <mat-sidenav #sidenav mode="side" opened>
    <mat-nav-list>
      @for (item of navItems; track item.route) {
        <a mat-list-item [routerLink]="item.route">
          <mat-icon>{{ item.icon }}</mat-icon>
          {{ item.label }}
        </a>
      }
    </mat-nav-list>
  </mat-sidenav>
  
  <mat-sidenav-content>
    <router-outlet></router-outlet>
  </mat-sidenav-content>
</mat-sidenav-container>
```

**Tabs:**
```typescript
import { MatTabsModule } from '@angular/material/tabs';

<mat-tab-group>
  <mat-tab label="Overview">
    <div class="tab-content">Overview content</div>
  </mat-tab>
  <mat-tab label="Details">
    <div class="tab-content">Details content</div>
  </mat-tab>
  <mat-tab label="Settings">
    <div class="tab-content">Settings content</div>
  </mat-tab>
</mat-tab-group>
```

### 3. Layout Components

**Cards:**
```typescript
import { MatCardModule } from '@angular/material/card';

<mat-card>
  <mat-card-header>
    <mat-card-title>Card Title</mat-card-title>
    <mat-card-subtitle>Card Subtitle</mat-card-subtitle>
  </mat-card-header>
  
  <img mat-card-image src="image.jpg" alt="Photo">
  
  <mat-card-content>
    <p>Card content goes here</p>
  </mat-card-content>
  
  <mat-card-actions>
    <button mat-button>LIKE</button>
    <button mat-button>SHARE</button>
  </mat-card-actions>
</mat-card>
```

**Grid List:**
```typescript
import { MatGridListModule } from '@angular/material/grid-list';

<mat-grid-list cols="3" rowHeight="200px">
  @for (tile of tiles; track tile.id) {
    <mat-grid-tile [colspan]="tile.cols" [rowspan]="tile.rows">
      <img [src]="tile.image" [alt]="tile.title">
      <mat-grid-tile-footer>
        <h3>{{ tile.title }}</h3>
      </mat-grid-tile-footer>
    </mat-grid-tile>
  }
</mat-grid-list>
```

### 4. Buttons & Indicators

**Buttons:**
```typescript
import { MatButtonModule } from '@angular/material/button';

<!-- Different button types -->
<button mat-button>Basic</button>
<button mat-raised-button color="primary">Raised</button>
<button mat-flat-button color="accent">Flat</button>
<button mat-stroked-button>Stroked</button>
<button mat-icon-button><mat-icon>favorite</mat-icon></button>
<button mat-fab color="primary"><mat-icon>add</mat-icon></button>
<button mat-mini-fab color="accent"><mat-icon>edit</mat-icon></button>
```

**Progress Indicators:**
```typescript
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatProgressBarModule } from '@angular/material/progress-bar';

<!-- Spinner -->
<mat-spinner></mat-spinner>
<mat-spinner diameter="50"></mat-spinner>

<!-- Progress bar -->
<mat-progress-bar mode="indeterminate"></mat-progress-bar>
<mat-progress-bar mode="determinate" [value]="progressValue"></mat-progress-bar>
```

### 5. Popups & Modals

**Dialog:**
```typescript
import { MatDialogModule, MatDialog } from '@angular/material/dialog';

// Open dialog
openDialog() {
  const dialogRef = this.dialog.open(MyDialogComponent, {
    width: '600px',
    data: { name: 'User Name' }
  });
  
  dialogRef.afterClosed().subscribe(result => {
    console.log('Dialog result:', result);
  });
}

// Dialog component
@Component({
  template: `
    <h2 mat-dialog-title>Dialog Title</h2>
    <mat-dialog-content>
      <p>Dialog content</p>
    </mat-dialog-content>
    <mat-dialog-actions align="end">
      <button mat-button mat-dialog-close>Cancel</button>
      <button mat-raised-button color="primary" [mat-dialog-close]="true">
        Confirm
      </button>
    </mat-dialog-actions>
  `
})
export class MyDialogComponent {
  constructor(@Inject(MAT_DIALOG_DATA) public data: any) {}
}
```

**Snackbar:**
```typescript
import { MatSnackBarModule, MatSnackBar } from '@angular/material/snackbar';

showSnackbar() {
  this.snackBar.open('Message sent successfully!', 'Close', {
    duration: 3000,
    horizontalPosition: 'end',
    verticalPosition: 'top'
  });
}
```

**Bottom Sheet:**
```typescript
import { MatBottomSheetModule, MatBottomSheet } from '@angular/material/bottom-sheet';

openBottomSheet() {
  this.bottomSheet.open(BottomSheetComponent);
}
```

### 6. Data Tables

**Table with Sorting & Pagination:**
```typescript
import { MatTableModule } from '@angular/material/table';
import { MatSortModule, MatSort } from '@angular/material/sort';
import { MatPaginatorModule, MatPaginator } from '@angular/material/paginator';

@Component({
  template: `
    <table mat-table [dataSource]="dataSource" matSort>
      <ng-container matColumnDef="name">
        <th mat-header-cell *matHeaderCellDef mat-sort-header>Name</th>
        <td mat-cell *matCellDef="let element">{{ element.name }}</td>
      </ng-container>
      
      <ng-container matColumnDef="email">
        <th mat-header-cell *matHeaderCellDef mat-sort-header>Email</th>
        <td mat-cell *matCellDef="let element">{{ element.email }}</td>
      </ng-container>
      
      <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
      <tr mat-row *matRowDef="let row; columns: displayedColumns;"></tr>
    </table>
    
    <mat-paginator [pageSize]="10" [pageSizeOptions]="[5, 10, 25, 100]">
    </mat-paginator>
  `
})
export class TableComponent implements AfterViewInit {
  displayedColumns = ['name', 'email'];
  dataSource = new MatTableDataSource(this.data);
  
  @ViewChild(MatSort) sort!: MatSort;
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  
  ngAfterViewInit() {
    this.dataSource.sort = this.sort;
    this.dataSource.paginator = this.paginator;
  }
}
```

## 🎯 Best Practices

### 1. Import Only What You Need
```typescript
// ✅ Good - Import specific modules
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

// ❌ Bad - Don't import everything
import * as Material from '@angular/material';
```

### 2. Use Appearance Variants
```typescript
// Material form fields support different appearances
<mat-form-field appearance="fill">     <!-- Default -->
<mat-form-field appearance="outline">  <!-- Outlined -->
<mat-form-field appearance="legacy">   <!-- Deprecated -->
```

### 3. Leverage Color Themes
```typescript
// Use color attribute for semantic styling
<button mat-raised-button color="primary">Primary</button>
<button mat-raised-button color="accent">Accent</button>
<button mat-raised-button color="warn">Warn</button>
```

### 4. Accessibility
```typescript
// Always provide labels and ARIA attributes
<button mat-icon-button aria-label="Delete item">
  <mat-icon>delete</mat-icon>
</button>

<mat-form-field>
  <mat-label>Email</mat-label>  <!-- Always include labels -->
  <input matInput type="email">
</mat-form-field>
```

### 5. Responsive Design
```scss
// Use Material breakpoints
@use '@angular/material' as mat;

@media (max-width: mat.$small-breakpoint) {
  .sidenav {
    mode: 'over';
  }
}
```

## 🔧 Theming

### Custom Theme
```scss
@use '@angular/material' as mat;

$my-primary: mat.define-palette(mat.$indigo-palette);
$my-accent: mat.define-palette(mat.$pink-palette);
$my-warn: mat.define-palette(mat.$red-palette);

$my-theme: mat.define-light-theme((
  color: (
    primary: $my-primary,
    accent: $my-accent,
    warn: $my-warn,
  ),
  typography: mat.define-typography-config(),
  density: 0,
));

@include mat.all-component-themes($my-theme);
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Animations not working | Import `provideAnimations()` or `BrowserAnimationsModule` |
| Icons not showing | Import Material Icons font in index.html |
| Styles not applying | Import `@angular/material/prebuilt-themes` in styles.scss |
| Form field errors | Wrap input in `<mat-form-field>` with `<mat-label>` |
| Table not sorting | Add `MatSort` directive and set `dataSource.sort` |
| Dialog not opening | Inject `MatDialog` service and import `MatDialogModule` |

## 📖 References

- [Angular Material Official Docs](https://material.angular.io/)
- [Component API Reference](https://material.angular.io/components/categories)
- [Material Design Guidelines](https://m3.material.io/)
- [Angular Material GitHub](https://github.com/angular/components)

---

## 📂 Recommended Placement

**Project-level skill:**
```
/.github/skills/angular-material/SKILL.md
```

Copilot will load this when working with Angular Material components.
