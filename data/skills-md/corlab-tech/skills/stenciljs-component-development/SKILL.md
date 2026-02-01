---
name: stenciljs-component-development
description: Use when creating or modifying Stencil.js web components. Ensures components follow Stencil best practices, proper decorator usage, lifecycle methods, and TypeScript conventions.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Stencil.js - Component Development

Build scalable, enterprise-ready web components using Stencil.js with TypeScript and Web Component standards. Stencil components are framework-agnostic and can be distributed to React, Angular, Vue, and traditional web applications.

## Key Concepts

### Component Structure

A Stencil component is a TypeScript class decorated with `@Component()`:

```typescript
import { Component, Prop, State, Event, EventEmitter, Watch, h } from '@stencil/core';

@Component({
  tag: 'my-component',
  styleUrl: 'my-component.css',
  shadow: true,
})
export class MyComponent {
  @Prop() name: string;
  @State() isActive: boolean = false;
  
  render() {
    return (
      <div>
        <p>Hello, {this.name}!</p>
      </div>
    );
  }
}
```

### Component Decorator Options

```typescript
@Component({
  tag: 'my-component',              // Required: Custom element tag name (must contain hyphen)
  styleUrl: 'my-component.css',     // Single stylesheet
  styleUrls: {                      // Multiple stylesheets for different modes
    ios: 'my-component.ios.css',
    md: 'my-component.md.css'
  },
  shadow: true,                     // Use Shadow DOM (recommended)
  scoped: false,                    // Scoped CSS without Shadow DOM
  assetsDirs: ['assets'],           // Asset directories to copy
  formAssociated: false,            // Form-associated custom element
})
```

## Decorators

### @Prop() - Component Properties

Public properties exposed as attributes:

```typescript
// Basic prop
@Prop() name: string;

// With default value
@Prop() size: 'small' | 'medium' | 'large' = 'medium';

// Mutable prop (can be changed internally)
@Prop({ mutable: true }) value: string;

// Reflect to attribute (sync prop changes to DOM attribute)
@Prop({ reflect: true }) active: boolean;

// Attribute name different from property name
@Prop({ attribute: 'data-id' }) dataId: string;
```

**Best Practices:**
- Always type your props
- Use JSDoc comments for public API documentation
- Set sensible defaults when appropriate
- Use `reflect: true` sparingly (performance cost)

### @State() - Internal State

Private state that triggers re-renders when changed:

```typescript
@State() isOpen: boolean = false;
@State() items: string[] = [];

// Updating state triggers re-render
this.isOpen = true;
```

**Important:**
- State is internal only, not exposed as attributes
- Mutating arrays/objects directly won't trigger re-render
- Use immutable patterns for complex state

### @Watch() - Property Change Handlers

Watch for prop or state changes:

```typescript
@Prop() value: string;

@Watch('value')
valueChanged(newValue: string, oldValue: string) {
  console.log(`Value changed from ${oldValue} to ${newValue}`);
  this.validateValue(newValue);
}

// Place @Watch() immediately after the prop it watches
@Prop() swipeEnabled: boolean = true;

@Watch('swipeEnabled')
swipeEnabledChanged(newSwipeEnabled: boolean, oldSwipeEnabled: boolean) {
  this.updateState();
}
```

### @Event() - Custom Events

Emit custom events:

```typescript
@Event() itemSelected: EventEmitter<string>;
@Event() formSubmit: EventEmitter<{value: string}>;

handleClick() {
  this.itemSelected.emit('item-1');
}
```

**Best Practices:**
- Use descriptive event names
- Type the event payload
- Document event details with JSDoc

### @Listen() - Event Listeners

Listen to DOM events:

```typescript
@Listen('click')
handleClick(event: MouseEvent) {
  console.log('Component clicked', event);
}

@Listen('scroll', { target: 'window' })
handleScroll(event: Event) {
  console.log('Window scrolled');
}

@Listen('resize', { target: 'window', passive: true })
handleResize() {
  this.updateDimensions();
}
```

### @Element() - Host Element Reference

Reference to the host element:

```typescript
@Element() el: HTMLElement;

componentDidLoad() {
  console.log('Host element:', this.el);
  this.el.classList.add('loaded');
}
```

### @Method() - Public Methods

Expose public async methods:

```typescript
@Method()
async open(): Promise<void> {
  this.isOpen = true;
}

@Method()
async getValue(): Promise<string> {
  return this.value;
}
```

**Important:**
- All public methods must be async
- Document with JSDoc for public API

## Lifecycle Methods

Lifecycle methods in order of execution:

```typescript
export class MyComponent {
  // 1. Called when component is connected to DOM (can be called multiple times)
  connectedCallback() {
    console.log('Component connected to DOM');
  }

  // 2. Called once before first render (good for async data loading)
  componentWillLoad() {
    console.log('Component will load');
    // Can return Promise to delay first render
  }

  // 3. Called once after first render
  componentDidLoad() {
    console.log('Component loaded');
  }

  // 4. Called before every render (after first)
  componentWillRender() {
    console.log('Component will render');
  }

  // 5. Called after every render (after first)
  componentDidRender() {
    console.log('Component rendered');
  }

  // 6. Called when component will update (not on first render)
  componentWillUpdate() {
    console.log('Component will update');
  }

  // 7. Called after component updates (not on first render)
  componentDidUpdate() {
    console.log('Component updated');
  }

  // 8. Determine if component should re-render
  componentShouldUpdate(newVal: any, oldVal: any, propName: string): boolean {
    return newVal !== oldVal;
  }

  // 9. Called when disconnected from DOM (can be called multiple times)
  disconnectedCallback() {
    console.log('Component disconnected');
  }
}
```

**Lifecycle Best Practices:**
- Use `componentWillLoad()` for async data fetching
- Use `componentDidLoad()` for DOM manipulation
- Use `connectedCallback()` for logic that runs every time element is attached
- Clean up in `disconnectedCallback()` (remove listeners, clear timers)

## JSX and Rendering

### render() Method

The `render()` method returns JSX:

```typescript
import { h } from '@stencil/core';

render() {
  return (
    <div class="container">
      <h1>Hello, {this.name}!</h1>
      {this.isActive && <p>Active!</p>}
      <button onClick={() => this.handleClick()}>
        Click me
      </button>
    </div>
  );
}
```

### Host Element

Use `<Host>` to set attributes on the host element:

```typescript
import { Host } from '@stencil/core';

render() {
  return (
    <Host
      class={{
        'is-active': this.isActive,
        'is-disabled': this.disabled
      }}
      aria-label={this.label}
    >
      <slot></slot>
    </Host>
  );
}
```

### Slots

Use slots for content projection:

```typescript
render() {
  return (
    <div>
      <header>
        <slot name="header"></slot>
      </header>
      <main>
        <slot></slot>  {/* Default slot */}
      </main>
      <footer>
        <slot name="footer"></slot>
      </footer>
    </div>
  );
}
```

### Conditional Rendering

```typescript
render() {
  return (
    <div>
      {this.loading ? (
        <div class="spinner">Loading...</div>
      ) : (
        <div class="content">{this.content}</div>
      )}
      
      {this.error && <div class="error">{this.error}</div>}
    </div>
  );
}
```

### Lists

```typescript
render() {
  return (
    <ul>
      {this.items.map(item => (
        <li key={item.id}>
          {item.name}
        </li>
      ))}
    </ul>
  );
}
```

## File Structure & Naming

### Directory Structure

One component per directory:

```
src/
├── components/
│   ├── my-button/
│   │   ├── my-button.tsx          # Component implementation
│   │   ├── my-button.css          # Styles
│   │   ├── my-button.spec.ts      # Unit tests
│   │   ├── my-button.e2e.ts       # E2E tests
│   │   └── readme.md              # Component documentation
│   ├── my-card/
│   │   ├── my-card.tsx
│   │   ├── my-card.ios.css        # iOS-specific styles
│   │   ├── my-card.md.css         # Material Design styles
│   │   └── my-card.css            # Base styles
```

### Naming Conventions

- **Tag names**: kebab-case with hyphen (required): `my-component`, `app-header`
- **Component class**: PascalCase: `MyComponent`, `AppHeader`
- **File names**: Match tag name: `my-component.tsx`
- **Props**: camelCase: `firstName`, `isActive`
- **Events**: camelCase: `itemSelected`, `formSubmit`
- **CSS classes**: kebab-case: `button-primary`, `is-active`

## Code Organization

Follow this order in component class:

```typescript
@Component({
  tag: 'my-component',
  styleUrl: 'my-component.css',
  shadow: true,
})
export class MyComponent {
  // 1. Own Properties (private, not decorated)
  private internalValue: number;
  someText = 'default';

  // 2. Reference to host element
  @Element() el: HTMLElement;

  // 3. State() variables (alphabetical)
  @State() isValidated: boolean;
  @State() status = 0;

  // 4. Public Property API - @Prop() (alphabetical)
  @Prop() content: string;
  @Prop() enabled: boolean;
  @Prop() type = 'default';

  // 5. Prop lifecycle events (@Watch) - immediately after related @Prop
  @Prop() value: string;
  
  @Watch('value')
  valueChanged(newValue: string, oldValue: string) {
    this.validate(newValue);
  }

  // 6. Events section (alphabetical)
  @Event() itemSelected: EventEmitter<string>;
  @Event() statusChanged: EventEmitter<number>;

  // 7. Component lifecycle events (in natural order)
  connectedCallback() {}
  disconnectedCallback() {}
  componentWillLoad() {}
  componentDidLoad() {}
  componentShouldUpdate() {}
  componentWillRender() {}
  componentDidRender() {}
  componentWillUpdate() {}
  componentDidUpdate() {}

  // 8. Listeners
  @Listen('click')
  onClick(event: MouseEvent) {
    console.log('Clicked');
  }

  // 9. Public methods API (alphabetical)
  @Method()
  async open(): Promise<void> {
    this.isOpen = true;
  }

  @Method()
  async close(): Promise<void> {
    this.isOpen = false;
  }

  // 10. Local methods (private business logic)
  private validate(value: string): boolean {
    return value.length > 0;
  }

  private updateState() {
    // Internal logic
  }

  // 11. render() function (always last)
  render() {
    return (
      <Host>
        <div class="container">
          <slot></slot>
        </div>
      </Host>
    );
  }
}
```

## Best Practices

### 1. Use TypeScript Strictly

```typescript
// Good - Fully typed
@Prop() items: Array<{id: string; name: string}>;
@State() count: number = 0;

// Bad - Any types
@Prop() items: any;
@State() count;
```

### 2. Immutable State Updates

```typescript
// Bad - Direct mutation won't trigger re-render
this.items.push(newItem);

// Good - Create new array
this.items = [...this.items, newItem];

// Bad - Direct object mutation
this.user.name = 'New Name';

// Good - Create new object
this.user = { ...this.user, name: 'New Name' };
```

### 3. Use Shadow DOM When Possible

```typescript
@Component({
  tag: 'my-component',
  styleUrl: 'my-component.css',
  shadow: true,  // Encapsulation and style isolation
})
```

### 4. Document Public API

```typescript
/**
 * The button component for user interactions
 */
@Component({
  tag: 'my-button',
})
export class MyButton {
  /**
   * The button label text
   */
  @Prop() label: string;

  /**
   * Emitted when the button is clicked
   */
  @Event() buttonClick: EventEmitter<void>;

  /**
   * Opens the button's associated menu
   */
  @Method()
  async openMenu(): Promise<void> {
    // ...
  }
}
```

### 5. Handle Async Operations Properly

```typescript
async componentWillLoad() {
  try {
    this.data = await this.fetchData();
  } catch (error) {
    console.error('Failed to load data:', error);
    this.error = 'Failed to load';
  }
}
```

### 6. Clean Up Resources

```typescript
private intervalId: number;

componentDidLoad() {
  this.intervalId = window.setInterval(() => {
    this.updateTime();
  }, 1000);
}

disconnectedCallback() {
  if (this.intervalId) {
    clearInterval(this.intervalId);
  }
}
```

### 7. Use Functional Components for Simple Cases

```typescript
import { h, FunctionalComponent } from '@stencil/core';

interface IconProps {
  name: string;
  size?: number;
}

export const Icon: FunctionalComponent<IconProps> = ({ name, size = 24 }) => (
  <svg width={size} height={size}>
    <use xlinkHref={`#icon-${name}`} />
  </svg>
);
```

## Anti-Patterns

### ❌ Don't Mutate Props

```typescript
// Bad
@Prop() value: string;

handleChange() {
  this.value = 'new value';  // Error if not mutable
}

// Good
@Prop({ mutable: true }) value: string;
// Or better: emit event and let parent handle
@Event() valueChange: EventEmitter<string>;

handleChange() {
  this.valueChange.emit('new value');
}
```

### ❌ Don't Use Constructor for Initialization

```typescript
// Bad
constructor() {
  this.data = this.fetchData();  // Won't work properly
}

// Good
async componentWillLoad() {
  this.data = await this.fetchData();
}
```

### ❌ Don't Access DOM in render()

```typescript
// Bad
render() {
  const width = this.el.offsetWidth;  // Can cause issues
  return <div style={{ width: `${width}px` }}></div>;
}

// Good
componentDidLoad() {
  this.width = this.el.offsetWidth;
}

render() {
  return <div style={{ width: `${this.width}px` }}></div>;
}
```

### ❌ Don't Forget Keys in Lists

```typescript
// Bad
render() {
  return (
    <ul>
      {this.items.map(item => <li>{item.name}</li>)}
    </ul>
  );
}

// Good
render() {
  return (
    <ul>
      {this.items.map(item => <li key={item.id}>{item.name}</li>)}
    </ul>
  );
}
```

### ❌ Don't Use Arrow Functions in render() for Handlers

```typescript
// Bad - Creates new function on every render
render() {
  return <button onClick={() => this.handleClick()}>Click</button>;
}

// Good - Bind in class or use arrow function property
private handleClick = () => {
  console.log('Clicked');
}

render() {
  return <button onClick={this.handleClick}>Click</button>;
}
```

## Testing

### Unit Tests

```typescript
import { newSpecPage } from '@stencil/core/testing';
import { MyComponent } from './my-component';

describe('my-component', () => {
  it('renders', async () => {
    const page = await newSpecPage({
      components: [MyComponent],
      html: `<my-component></my-component>`,
    });
    expect(page.root).toEqualHtml(`
      <my-component>
        <mock:shadow-root>
          <div>
            Hello, World!
          </div>
        </mock:shadow-root>
      </my-component>
    `);
  });

  it('renders with props', async () => {
    const page = await newSpecPage({
      components: [MyComponent],
      html: `<my-component name="Stencil"></my-component>`,
    });
    expect(page.root).toEqualHtml(`
      <my-component name="Stencil">
        <mock:shadow-root>
          <div>
            Hello, Stencil!
          </div>
        </mock:shadow-root>
      </my-component>
    `);
  });
});
```

### E2E Tests

```typescript
import { newE2EPage } from '@stencil/core/testing';

describe('my-component', () => {
  it('renders', async () => {
    const page = await newE2EPage();
    await page.setContent('<my-component></my-component>');
    
    const element = await page.find('my-component');
    expect(element).toHaveClass('hydrated');
  });

  it('emits event on click', async () => {
    const page = await newE2EPage();
    await page.setContent('<my-component></my-component>');
    
    const itemSelected = await page.spyOnEvent('itemSelected');
    const button = await page.find('my-component >>> button');
    await button.click();
    
    expect(itemSelected).toHaveReceivedEvent();
  });
});
```

## Common Patterns

### Form-Associated Components

```typescript
@Component({
  tag: 'my-input',
  formAssociated: true,
})
export class MyInput {
  @Element() el: HTMLElement;
  
  private internals: ElementInternals;

  componentWillLoad() {
    this.internals = (this.el as any).attachInternals();
  }

  @Prop() value: string = '';
  
  @Watch('value')
  valueChanged(newValue: string) {
    this.internals.setFormValue(newValue);
  }
}
```

### Loading States

```typescript
@State() loading: boolean = false;
@State() error: string | null = null;
@State() data: any = null;

async componentWillLoad() {
  await this.loadData();
}

private async loadData() {
  this.loading = true;
  this.error = null;
  
  try {
    this.data = await fetch('/api/data').then(r => r.json());
  } catch (e) {
    this.error = 'Failed to load data';
  } finally {
    this.loading = false;
  }
}

render() {
  if (this.loading) return <div>Loading...</div>;
  if (this.error) return <div class="error">{this.error}</div>;
  return <div>{JSON.stringify(this.data)}</div>;
}
```

### Controlled vs Uncontrolled

```typescript
// Controlled - value managed by parent
@Prop() value: string;
@Event() valueChange: EventEmitter<string>;

handleInput(event: Event) {
  const value = (event.target as HTMLInputElement).value;
  this.valueChange.emit(value);
}

render() {
  return <input value={this.value} onInput={e => this.handleInput(e)} />;
}

// Uncontrolled - internal state
@State() internalValue: string = '';

handleInput(event: Event) {
  this.internalValue = (event.target as HTMLInputElement).value;
}

render() {
  return <input value={this.internalValue} onInput={e => this.handleInput(e)} />;
}
```

## Performance Tips

1. **Use `componentShouldUpdate()` to prevent unnecessary renders**
2. **Avoid complex computations in render()**
3. **Use `memoize` for expensive calculations**
4. **Lazy load components with `import()`**
5. **Use Shadow DOM for style encapsulation**
6. **Minimize prop changes from parent**
7. **Use event delegation for lists**

## Related Resources

- [Stencil.js Official Documentation](https://stenciljs.com/docs/introduction)
- [Stencil Component API](https://stenciljs.com/docs/api)
- [Stencil Style Guide](https://stenciljs.com/docs/style-guide)
- [Web Components Standards](https://developer.mozilla.org/en-US/docs/Web/Web_Components)
