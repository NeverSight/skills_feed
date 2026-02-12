---
name: better-stimulus
description: Apply Better Stimulus best practices for writing maintainable, reusable StimulusJS controllers following SOLID principles
---

# Better Stimulus

Apply opinionated best practices from [betterstimulus.com](https://betterstimulus.com/) when writing or refactoring Stimulus controllers. These patterns emphasize code reusability, proper separation of concerns, and SOLID design principles.

## When to Use This Skill

Invoke this skill when:
- Writing new Stimulus controllers
- Refactoring existing Stimulus code
- Reviewing Stimulus controller architecture
- Debugging inter-controller communication
- Integrating third-party JavaScript libraries
- Implementing form submission logic
- Managing controller state
- Setting up Turbo integration

## Core Principles

### 1. Make Controllers Configurable

**Externalize hardcoded values into data attributes** rather than embedding them in controller logic.

Bad:
```javascript
toggle() {
  this.element.classList.toggle("active")
}
```

Good:
```javascript
static classes = ["active"]
toggle() {
  this.element.classList.toggle(this.activeClass)
}
```
```html
<div data-controller="toggle" data-toggle-active-class="active"></div>
```

### 2. Use Values API for State

**Store controller state in Stimulus values**, not instance properties, to leverage reactivity and DOM persistence.

Bad:
```javascript
connect() {
  this.count = 0
}
```

Good:
```javascript
static values = { count: Number }
countValueChanged(count) {
  this.updateDisplay()
}
```

### 3. Keep Controllers Focused (Single Responsibility)

**Each controller should have one reason to change.** Split controllers that mix concerns.

Ask: "What would cause this controller to change?" If multiple unrelated reasons, split it.

### 4. Don't Overuse connect()

Use `connect()` for:
- Instantiating third-party plugins (Swiper, Chart.js, etc.)
- Feature detection/browser capabilities

Don't use `connect()` for:
- Setting up state (use Values API)
- Adding event listeners (use `data-action`)

### 5. Register Events Declaratively

**Use `data-action` attributes** instead of `addEventListener()` to let Stimulus manage lifecycle.

Bad:
```javascript
connect() {
  document.addEventListener("click", this.handler.bind(this))
}
```

Good:
```html
<div data-action="click@document->controller#handler"></div>
```

## Key Patterns

### Architecture

- **Configurable Controllers**: Inject dependencies via data attributes
- **Application Controller**: Base class for shared functionality
- **Mixins**: Share behavior via "acts as" relationships
- **Targetless Controllers**: Separate element vs. target manipulation
- **Namespaced Attributes**: Handle arbitrary parameter sets

See: `references/architecture.md`

### State Management

- Use Values API for nearly all state
- Leverage change callbacks (`[name]ValueChanged`)
- Keep values serializable
- Provide sensible defaults

See: `references/state-management.md`

### Lifecycle

- Use `connect()` for third-party library initialization
- Pair `connect()` with `disconnect()` for cleanup
- Avoid overloading `connect()` with state setup
- Implement `teardown()` for Turbo-specific cleanup

See: `references/lifecycle.md`

### Controller Communication

Three approaches:

1. **Custom Events**: Loose coupling, broadcast pattern
2. **Outlets**: Direct controller references, structured layouts
3. **Callbacks**: Request state from other controllers

Choose based on relationship:
- Unknown receivers → Custom events
- Known hierarchy → Outlets
- Data sharing → Callbacks

See: `references/events-and-interaction.md`

### SOLID Principles

- **Single Responsibility**: One reason to change
- **Open-Closed**: Extend via inheritance, not modification
- **Dependency Inversion**: Depend on abstractions, inject via config

See: `references/solid-principles.md`

### DOM & Turbo

- Use `<template>` to restore DOM state
- Use `requestSubmit()` not `submit()` for forms
- Implement global teardown for Turbo caching
- Handle Turbo events declaratively

See: `references/dom-and-turbo.md`

### Error Handling

- Create ApplicationController with `handleError()` method
- Integrate with error tracking (Sentry, Honeybadger)
- Provide user-friendly messages
- Use try-catch for async operations

See: `references/error-handling.md`

## Quick Reference

### Value Types
```javascript
static values = {
  url: String,
  count: Number,
  enabled: Boolean,
  items: Array,
  config: Object
}
```

### Event Actions
```html
<!-- Element events -->
<div data-action="click->controller#method">

<!-- Global events -->
<div data-action="resize@window->controller#layout">
<div data-action="keydown@document->controller#handleKey">

<!-- Multiple actions -->
<div data-action="click->ctrl1#method1 click->ctrl2#method2">
```

### Custom Events
```javascript
// Dispatch
const event = new CustomEvent('name:action', {
  bubbles: true,
  detail: { key: 'value' }
})
this.element.dispatchEvent(event)

// Listen
data-action="name:action->controller#handler"
```

### Outlets
```html
<div data-controller="parent"
     data-parent-child-outlet=".child">
  <div class="child" data-controller="child"></div>
</div>
```

```javascript
static outlets = ['child']
this.childOutlets.forEach(outlet => outlet.method())
```

### Lifecycle Hooks
```javascript
connect()           // Element connected to DOM
disconnect()        // Element removed from DOM
[name]TargetConnected(element)      // Target added
[name]TargetDisconnected(element)   // Target removed
[name]ValueChanged(value, oldValue) // Value changed
[name]OutletConnected(outlet)       // Outlet connected
[name]OutletDisconnected(outlet)    // Outlet disconnected
```

## Implementation Workflow

When writing a new controller:

1. **Identify responsibility** - What single purpose does this serve?
2. **Choose state approach** - Use Values API unless non-serializable
3. **Declare static properties** - values, targets, classes, outlets
4. **Implement change callbacks** - React to value changes
5. **Keep connect() minimal** - Only for third-party setup
6. **Use declarative actions** - Avoid addEventListener
7. **Handle errors gracefully** - Wrap risky operations in try-catch
8. **Test lifecycle** - Verify connect/disconnect behavior

When refactoring:

1. **Check Single Responsibility** - Split if multiple concerns
2. **Extract configuration** - Move hardcoded values to data attributes
3. **Convert to Values API** - Replace instance properties with values
4. **Simplify connect()** - Move state and listeners out
5. **Use inheritance/mixins** - Share common behavior properly
6. **Decouple controllers** - Use events/outlets for communication
7. **Add error handling** - Implement handleError from ApplicationController

## Common Mistakes to Avoid

- ❌ Hardcoding CSS classes, selectors, or IDs in controllers
- ❌ Using instance properties for state instead of values
- ❌ Overloading `connect()` with state setup and event listeners
- ❌ Creating "page controllers" that handle multiple concerns
- ❌ Using `addEventListener()` without proper cleanup
- ❌ Calling `.bind()` separately in connect and disconnect
- ❌ Using `submit()` instead of `requestSubmit()`
- ❌ Modifying base classes instead of extending them
- ❌ Tight coupling between controllers
- ❌ Swallowing errors without logging or reporting

## Resources

All patterns in this skill come from [betterstimulus.com](https://betterstimulus.com/), an opinionated collection of StimulusJS best practices.

For detailed explanations and examples, see:
- `references/architecture.md` - Controller design patterns
- `references/state-management.md` - Values API usage
- `references/lifecycle.md` - Lifecycle best practices
- `references/events-and-interaction.md` - Communication patterns
- `references/solid-principles.md` - SOLID design principles
- `references/dom-and-turbo.md` - DOM manipulation and Turbo
- `references/error-handling.md` - Error management
