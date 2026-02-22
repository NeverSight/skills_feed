---
name: stimulus-controllers
description: Create and register Stimulus controllers for interactive JavaScript features. Use when adding client-side interactivity, dynamic UI updates, or when the user mentions Stimulus controllers or JavaScript behavior.
---

# Stimulus Controllers

## Overview
Stimulus controllers provide modular JavaScript functionality connected to HTML via data attributes. After creating a new controller, you must register it in the index.js file.

## Creating a New Controller

### 1. Create the Controller File
Create a new controller in `app/javascript/controllers/`:

```javascript
// app/javascript/controllers/example_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["element"]
  static values = { name: String }

  connect() {
    // Called when controller is connected to DOM
  }

  disconnect() {
    // Called when controller is disconnected from DOM
  }

  // Action methods
  handleClick(event) {
    event.preventDefault()
    // Your logic here
  }
}
```

### 2. Register the Controller
**CRITICAL**: After creating a new controller, run:

```bash
bin/rails stimulus:manifest:update
```

This automatically updates `app/javascript/controllers/index.js` to register your controller.

**Manual Registration** (if needed):
```javascript
import ExampleController from "./example_controller"
application.register("example", ExampleController)
```

Controller name in HTML uses kebab-case: `data-controller="example"`

### 3. Use in HTML
Connect the controller to HTML elements:

```slim
.container data-controller="example" data-example-name-value="test"
  button data-action="click->example#handleClick" Click Me
  div data-example-target="element" Target Element
```

## Naming Conventions

- **File**: `example_controller.js` (snake_case)
- **Class**: `export default class extends Controller`
- **Registration**: `"example"` (kebab-case)
- **HTML**: `data-controller="example"` (kebab-case)
- **Multi-word**: `bulk_submit_controller.js` → `"bulk-submit"`

## Key Concepts

### Targets
Reference specific DOM elements:

```javascript
static targets = ["input", "output"]

// Access in methods:
this.inputTarget        // First matching element
this.inputTargets       // All matching elements
this.hasInputTarget     // Boolean check
```

### Values
Type-safe data attributes:

```javascript
static values = {
  url: String,
  count: Number,
  active: Boolean,
  items: Array,
  config: Object
}

// Access in methods:
this.urlValue
this.countValue

// Watch for changes:
urlValueChanged(newUrl, oldUrl) {
  // Called when value changes
}
```

### Actions
Connect events to methods:

```html
<!-- Basic action -->
data-action="click->example#save"

<!-- Multiple actions -->
data-action="click->example#save submit->example#submit"

<!-- Custom events -->
data-action="example:refresh->example#reload"

<!-- Event modifiers -->
data-action="submit->example#save:prevent"
```

### Classes
Manage CSS classes:

```javascript
static classes = ["active", "hidden"]

// Use in methods:
this.element.classList.add(this.activeClass)
this.element.classList.remove(this.hiddenClass)
```

## Common Patterns

### Form Validation
```javascript
export default class extends Controller {
  static targets = ["form", "submit"]

  validate() {
    const isValid = this.formTarget.checkValidity()
    this.submitTarget.disabled = !isValid
  }
}
```

### Toggle Visibility
```javascript
export default class extends Controller {
  static targets = ["content"]
  static classes = ["hidden"]

  toggle() {
    this.contentTarget.classList.toggle(this.hiddenClass)
  }
}
```

### AJAX Updates
```javascript
export default class extends Controller {
  static values = { url: String }

  async refresh() {
    const response = await fetch(this.urlValue)
    const html = await response.text()
    this.element.innerHTML = html
  }
}
```

## Testing

Test Stimulus controllers in system specs:

```ruby
it 'handles interaction', :js do
  visit page_path

  click_button 'Toggle'

  expect(page).to have_css('[data-controller="example"]')
end
```

## Troubleshooting

**Controller not working?**
1. Verify controller is registered in `index.js`
2. Run `bin/rails stimulus:manifest:update`
3. Check browser console for errors
4. Verify data attribute spelling (kebab-case)
5. Ensure JavaScript is enabled in tests (`:js` tag)

**Targets not found?**
- Check target name in `static targets` matches HTML
- Use `hasXxxTarget` to verify existence before accessing
- Ensure target element is in controller scope

## Related Skills
- [frontend-patterns](../frontend-patterns/SKILL.md) - HTML and CSS patterns
- [turbo-fetch](../turbo-fetch/SKILL.md) - Dynamic form updates
- [testing-patterns](../testing-patterns/SKILL.md) - Testing JavaScript features
