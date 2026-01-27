---
name: angular-cdk
description: Angular Component Dev Kit (CDK) expertise for building custom components with accessibility, overlays, drag-and-drop, virtual scrolling, and layout utilities. Use when creating custom UI components, implementing accessibility features, building overlays/dialogs, virtual scrolling for large lists, or using CDK utilities for responsive layouts.
license: MIT
---

# Angular CDK (Component Dev Kit) Skill

## Rules

### Lifecycle & Resource Management
- **Must** create `FocusTrap` in `ngOnInit()` using `focusTrapFactory.create()`
- **Must** call `focusTrap.focusInitialElement()` after creating focus trap
- **Must** destroy `FocusTrap` in `ngOnDestroy()` using `focusTrap.destroy()`
- **Must** stop monitoring focus in `ngOnDestroy()` using `focusMonitor.stopMonitoring()`
- **Must** destroy `keyManager` in `ngOnDestroy()` using `keyManager.destroy()`
- **Must** dispose `overlayRef` in cleanup using `overlayRef.dispose()`
- **Must** explicitly release all CDK resources in `ngOnDestroy()`
- **Must** clean up: `focusTrap`, `overlayRef`, `focusMonitor`, `keyManager`
- **Shall Not** leave CDK resources without cleanup (causes memory leaks)

### Accessibility
- **Must** use `LiveAnnouncer` for screen reader announcements of dynamic content
- **Must** use `FocusKeyManager` for keyboard navigation in lists

### Overlay Positioning
- **Must** use `flexibleConnectedTo()` with at least two fallback position strategies
- **Must** configure explicit `scrollStrategy` for overlay
- **Must** configure explicit `hasBackdrop` property for overlay
- **Must** attach portal to overlay using `overlayRef.attach(portal)`

### Portal Usage
- **Must** use `ComponentPortal` for dynamic component rendering
- **Must** use `TemplatePortal` for template content projection
- **Must** detach portal when no longer needed to prevent memory leaks

### Drag & Drop
- **Must** use `cdkDropList` container with `(cdkDropListDropped)` event handler
- **Must** use `cdkDrag` directive on draggable items
- **Must** use `track` expressions in `@for` loops with drag items
- **Must** use `moveItemInArray()` for single-list reordering
- **Must** use `transferArrayItem()` for cross-list transfers
- **Must** connect drop lists using `[cdkDropListConnectedTo]` for cross-list drag

### Virtual Scrolling
- **Only** use `CdkVirtualScrollViewport` for lists with more than 100 items
- **Must** set explicit `itemSize` property
- **Must** configure `minBufferPx` and `maxBufferPx` for smooth scrolling
- **Must** set fixed height on viewport container
- **Must Not** use auto-height virtual scroll viewports

### Breakpoint Observer
- **Must** use `BreakpointObserver` for responsive layout detection
- **Must** use `toSignal()` when converting breakpoint observables to signals
- **Must** provide `initialValue` when using `toSignal()` with breakpoints
- **Must Not** use direct `window.innerWidth` or manual resize listeners
- **Must Not** use direct `window.matchMedia()` calls

---

## Context

### 🎯 Purpose
This skill provides comprehensive guidance on the **Angular Component Dev Kit (CDK)**, a set of behavior primitives for building accessible, high-quality Angular components without Material Design styling.

### 📦 What is Angular CDK?

The Angular CDK is a library of unstyled UI component behaviors:
- **Accessibility (A11y)**: Screen reader support, keyboard navigation, focus management
- **Overlay**: Positioning, backdrop, and overlay management
- **Portal**: Dynamic component rendering
- **Drag & Drop**: Sortable lists and drag-and-drop interactions
- **Virtual Scrolling**: Efficient rendering of large lists
- **Layout**: Responsive layout utilities and breakpoint observers
- **Table**: Data table functionality without styling
- **Tree**: Hierarchical tree structures

### 🎨 When to Use This Skill

Use Angular CDK guidance when:
- Building custom UI components from scratch
- Implementing accessible components (ARIA, focus management)
- Creating overlays, modals, or tooltips
- Building drag-and-drop functionality
- Implementing virtual scrolling for performance
- Working with responsive layouts and breakpoints
- Creating custom data tables or tree views
- Managing focus trapping and keyboard navigation

### 📚 Core CDK Modules

#### 1. Accessibility (A11y)

**Focus Management:**
```typescript
import { FocusTrapFactory, FocusMonitor } from '@angular/cdk/a11y';

export class DialogComponent implements OnInit, OnDestroy {
  private focusTrap: FocusTrap;
  
  constructor(
    private focusTrapFactory: FocusTrapFactory,
    private focusMonitor: FocusMonitor,
    private elementRef: ElementRef
  ) {}
  
  ngOnInit() {
    // Create focus trap to keep focus within dialog
    this.focusTrap = this.focusTrapFactory.create(
      this.elementRef.nativeElement
    );
    this.focusTrap.focusInitialElement();
    
    // Monitor focus changes
    this.focusMonitor.monitor(this.elementRef, true).subscribe(origin => {
      console.log('Focus origin:', origin);
    });
  }
  
  ngOnDestroy() {
    this.focusTrap.destroy();
    this.focusMonitor.stopMonitoring(this.elementRef);
  }
}
```

**Live Announcer (Screen Readers):**
```typescript
import { LiveAnnouncer } from '@angular/cdk/a11y';

export class NotificationComponent {
  constructor(private liveAnnouncer: LiveAnnouncer) {}
  
  announce(message: string) {
    // Announce to screen readers
    this.liveAnnouncer.announce(message, 'polite');
  }
  
  announceUrgent(message: string) {
    this.liveAnnouncer.announce(message, 'assertive');
  }
}
```

**List Key Manager (Keyboard Navigation):**
```typescript
import { FocusKeyManager } from '@angular/cdk/a11y';
import { QueryList, ViewChildren, AfterViewInit } from '@angular/core';

export class MenuComponent implements AfterViewInit {
  @ViewChildren(MenuItem) menuItems: QueryList<MenuItem>;
  private keyManager: FocusKeyManager<MenuItem>;
  
  ngAfterViewInit() {
    this.keyManager = new FocusKeyManager(this.menuItems)
      .withWrap()
      .withVerticalOrientation();
  }
  
  onKeydown(event: KeyboardEvent) {
    this.keyManager.onKeydown(event);
  }
}
```

#### 2. Overlay

**Creating Overlays:**
```typescript
import { Overlay, OverlayConfig, OverlayRef } from '@angular/cdk/overlay';
import { ComponentPortal } from '@angular/cdk/portal';

export class TooltipDirective {
  private overlayRef: OverlayRef | null = null;
  
  constructor(
    private overlay: Overlay,
    private elementRef: ElementRef
  ) {}
  
  show() {
    // Create overlay configuration
    const config = new OverlayConfig({
      positionStrategy: this.overlay.position()
        .flexibleConnectedTo(this.elementRef)
        .withPositions([
          {
            originX: 'center',
            originY: 'bottom',
            overlayX: 'center',
            overlayY: 'top',
            offsetY: 8
          }
        ]),
      hasBackdrop: false,
      scrollStrategy: this.overlay.scrollStrategies.reposition()
    });
    
    // Create overlay
    this.overlayRef = this.overlay.create(config);
    
    // Attach component to overlay
    const portal = new ComponentPortal(TooltipComponent);
    this.overlayRef.attach(portal);
  }
  
  hide() {
    if (this.overlayRef) {
      this.overlayRef.dispose();
      this.overlayRef = null;
    }
  }
}
```

**Global Position Strategy:**
```typescript
const config = new OverlayConfig({
  positionStrategy: this.overlay.position()
    .global()
    .centerHorizontally()
    .centerVertically(),
  hasBackdrop: true,
  backdropClass: 'dark-backdrop'
});
```

#### 3. Portal

**Template Portals:**
```typescript
import { TemplatePortal } from '@angular/cdk/portal';
import { TemplateRef, ViewContainerRef } from '@angular/core';

export class PortalExample {
  @ViewChild('templatePortalContent') templateRef: TemplateRef<any>;
  selectedPortal: TemplatePortal<any>;
  
  constructor(private viewContainerRef: ViewContainerRef) {}
  
  createTemplatePortal() {
    this.selectedPortal = new TemplatePortal(
      this.templateRef,
      this.viewContainerRef
    );
  }
}
```

```html
<ng-template #templatePortalContent>
  <p>This content will be rendered in a portal</p>
</ng-template>

<div cdkPortalOutlet [cdkPortalOutlet]="selectedPortal"></div>
```

**Component Portals:**
```typescript
import { ComponentPortal } from '@angular/cdk/portal';

createComponentPortal() {
  const portal = new ComponentPortal(
    MyComponent,
    null, // ViewContainerRef (optional)
    this.injector, // Custom injector (optional)
    this.componentFactoryResolver // (optional)
  );
  
  // Attach to overlay or portal outlet
  const ref = this.overlayRef.attach(portal);
  ref.instance.data = 'Custom data';
}
```

#### 4. Drag & Drop

**Sortable List:**
```typescript
import { CdkDragDrop, moveItemInArray } from '@angular/cdk/drag-drop';

@Component({
  template: `
    <div cdkDropList (cdkDropListDropped)="drop($event)">
      @for (item of items; track item) {
        <div cdkDrag>
          <div class="drag-handle" cdkDragHandle>⋮⋮</div>
          {{ item }}
        </div>
      }
    </div>
  `
})
export class SortableListComponent {
  items = ['Item 1', 'Item 2', 'Item 3'];
  
  drop(event: CdkDragDrop<string[]>) {
    moveItemInArray(this.items, event.previousIndex, event.currentIndex);
  }
}
```

**Drag Between Lists:**
```typescript
import { CdkDragDrop, transferArrayItem } from '@angular/cdk/drag-drop';

@Component({
  template: `
    <div class="lists-container">
      <div cdkDropList #todoList="cdkDropList"
           [cdkDropListData]="todo"
           [cdkDropListConnectedTo]="[doneList]"
           (cdkDropListDropped)="drop($event)">
        @for (item of todo; track item) {
          <div cdkDrag>{{ item }}</div>
        }
      </div>
      
      <div cdkDropList #doneList="cdkDropList"
           [cdkDropListData]="done"
           [cdkDropListConnectedTo]="[todoList]"
           (cdkDropListDropped)="drop($event)">
        @for (item of done; track item) {
          <div cdkDrag>{{ item }}</div>
        }
      </div>
    </div>
  `
})
export class TaskBoardComponent {
  todo = ['Task 1', 'Task 2'];
  done = ['Task 3'];
  
  drop(event: CdkDragDrop<string[]>) {
    if (event.previousContainer === event.container) {
      moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
    } else {
      transferArrayItem(
        event.previousContainer.data,
        event.container.data,
        event.previousIndex,
        event.currentIndex
      );
    }
  }
}
```

#### 5. Virtual Scrolling

**Virtual Scroll for Large Lists:**
```typescript
import { CdkVirtualScrollViewport } from '@angular/cdk/scrolling';

@Component({
  template: `
    <cdk-virtual-scroll-viewport itemSize="50" class="viewport">
      @for (item of items; track item) {
        <div class="item">{{ item }}</div>
      }
    </cdk-virtual-scroll-viewport>
  `,
  styles: [`
    .viewport {
      height: 400px;
      width: 100%;
    }
    
    .item {
      height: 50px;
      display: flex;
      align-items: center;
    }
  `]
})
export class VirtualScrollComponent {
  items = Array.from({ length: 10000 }, (_, i) => `Item #${i}`);
}
```

**Dynamic Item Sizes:**
```typescript
@Component({
  template: `
    <cdk-virtual-scroll-viewport 
      [itemSize]="50" 
      minBufferPx="200" 
      maxBufferPx="400">
      @for (item of items; track item.id) {
        <div class="item" [style.height.px]="item.height">
          {{ item.content }}
        </div>
      }
    </cdk-virtual-scroll-viewport>
  `
})
export class DynamicVirtualScrollComponent {
  items = Array.from({ length: 1000 }, (_, i) => ({
    id: i,
    content: `Item ${i}`,
    height: 40 + (i % 3) * 20 // Variable heights
  }));
}
```

#### 6. Layout & Breakpoints

**Breakpoint Observer:**
```typescript
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';

export class ResponsiveComponent {
  isHandset$ = this.breakpointObserver.observe(Breakpoints.Handset)
    .pipe(map(result => result.matches));
  
  constructor(private breakpointObserver: BreakpointObserver) {
    // Observe multiple breakpoints
    this.breakpointObserver.observe([
      Breakpoints.XSmall,
      Breakpoints.Small,
      Breakpoints.Medium,
      Breakpoints.Large,
      Breakpoints.XLarge
    ]).subscribe(result => {
      if (result.breakpoints[Breakpoints.XSmall]) {
        this.columns = 1;
      } else if (result.breakpoints[Breakpoints.Small]) {
        this.columns = 2;
      } else {
        this.columns = 4;
      }
    });
  }
}
```

**Custom Breakpoints:**
```typescript
const customBreakpoints = {
  mobile: '(max-width: 599px)',
  tablet: '(min-width: 600px) and (max-width: 959px)',
  desktop: '(min-width: 960px)'
};

this.breakpointObserver.observe([customBreakpoints.mobile])
  .subscribe(result => {
    this.isMobile = result.matches;
  });
```

#### 7. Table

**CDK Table (Unstyled):**
```typescript
import { DataSource } from '@angular/cdk/collections';

@Component({
  template: `
    <cdk-table [dataSource]="dataSource">
      <ng-container cdkColumnDef="name">
        <cdk-header-cell *cdkHeaderCellDef>Name</cdk-header-cell>
        <cdk-cell *cdkCellDef="let row">{{ row.name }}</cdk-cell>
      </ng-container>
      
      <ng-container cdkColumnDef="email">
        <cdk-header-cell *cdkHeaderCellDef>Email</cdk-header-cell>
        <cdk-cell *cdkCellDef="let row">{{ row.email }}</cdk-cell>
      </ng-container>
      
      <cdk-header-row *cdkHeaderRowDef="displayedColumns"></cdk-header-row>
      <cdk-row *cdkRowDef="let row; columns: displayedColumns;"></cdk-row>
    </cdk-table>
  `
})
export class TableComponent {
  displayedColumns = ['name', 'email'];
  dataSource = new MyDataSource();
}
```

#### 8. Tree

**Nested Tree:**
```typescript
import { NestedTreeControl } from '@angular/cdk/tree';
import { ArrayDataSource } from '@angular/cdk/collections';

interface FileNode {
  name: string;
  children?: FileNode[];
}

@Component({
  template: `
    <cdk-tree [dataSource]="dataSource" [treeControl]="treeControl">
      <cdk-nested-tree-node *cdkTreeNodeDef="let node">
        {{ node.name }}
      </cdk-nested-tree-node>
      
      <cdk-nested-tree-node *cdkTreeNodeDef="let node; when: hasChild">
        <button (click)="treeControl.toggle(node)">
          {{ treeControl.isExpanded(node) ? '▼' : '▶' }}
        </button>
        {{ node.name }}
        
        <div *ngIf="treeControl.isExpanded(node)">
          <ng-container cdkTreeNodeOutlet></ng-container>
        </div>
      </cdk-nested-tree-node>
    </cdk-tree>
  `
})
export class TreeComponent {
  treeControl = new NestedTreeControl<FileNode>(node => node.children);
  dataSource = new ArrayDataSource(TREE_DATA);
  
  hasChild = (_: number, node: FileNode) => !!node.children && node.children.length > 0;
}
```

### 🎯 Best Practices

#### 1. Accessibility First
```typescript
// Always use CDK a11y utilities for custom components
import { FocusTrap, LiveAnnouncer } from '@angular/cdk/a11y';

// Trap focus in modals
// Announce dynamic content changes
// Implement keyboard navigation
```

#### 2. Overlay Positioning
```typescript
// Use flexible positioning for better UX
const positionStrategy = this.overlay.position()
  .flexibleConnectedTo(this.elementRef)
  .withPositions([
    // Primary position
    { originX: 'start', originY: 'bottom', overlayX: 'start', overlayY: 'top' },
    // Fallback positions
    { originX: 'start', originY: 'top', overlayX: 'start', overlayY: 'bottom' },
    { originX: 'end', originY: 'bottom', overlayX: 'end', overlayY: 'top' }
  ]);
```

#### 3. Virtual Scrolling Performance
```typescript
// Configure buffer sizes for smooth scrolling
<cdk-virtual-scroll-viewport 
  itemSize="50"
  minBufferPx="400"   // Render extra items above
  maxBufferPx="800">  // Render extra items below
```

#### 4. Drag & Drop Constraints
```typescript
// Constrain drag movement
<div cdkDrag [cdkDragBoundary]="'.boundary-element'">
  Constrained drag
</div>

// Custom drag preview
<div cdkDrag>
  <div *cdkDragPreview>Custom preview</div>
  <div *cdkDragPlaceholder>Placeholder</div>
  Content
</div>
```

### 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Overlay not positioning correctly | Check scroll strategy and position preferences |
| Virtual scroll not rendering | Ensure `itemSize` matches actual item height |
| Drag & drop not working | Import `DragDropModule` and use correct directives |
| Focus trap not working | Ensure element has focusable children |
| Breakpoint observer not triggering | Check for correct breakpoint strings |
| Tree not expanding | Implement `hasChild` function and tree control |

### 📖 References

- [Angular CDK Official Docs](https://material.angular.io/cdk/categories)
- [CDK API Reference](https://material.angular.io/cdk/api)
- [Accessibility Guide](https://www.w3.org/WAI/ARIA/apg/)
- [CDK GitHub Repository](https://github.com/angular/components)

### 💡 Common Use Cases

1. **Custom Dropdown**: Use Overlay + Portal
2. **Accessible Dialog**: Use Overlay + Focus Trap + Live Announcer
3. **Infinite Scroll**: Use Virtual Scroll Viewport
4. **Sortable Table**: Use CDK Table + Drag Drop
5. **Responsive Sidebar**: Use Breakpoint Observer + Layout
6. **File Tree**: Use CDK Tree
7. **Custom Tooltip**: Use Overlay + Positioning Strategy

### 📂 Recommended Placement

**Project-level skill:**
```
/.github/skills/angular-cdk/SKILL.md
```

Copilot will load this when working with Angular CDK features.
