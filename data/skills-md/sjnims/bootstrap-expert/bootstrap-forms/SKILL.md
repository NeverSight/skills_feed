---
name: bootstrap-forms
description: This skill should be used when the user asks about Bootstrap forms, Bootstrap form controls, Bootstrap input fields, Bootstrap select, Bootstrap checkboxes, Bootstrap radio buttons, Bootstrap switches, Bootstrap range inputs, Bootstrap input groups, Bootstrap floating labels, Bootstrap form validation, Bootstrap form layout, how to create Bootstrap forms, needs help with form styling and validation in Bootstrap, wants to create a form, add form validation, style form inputs, make an inline form, add floating labels to inputs, create a login form, build a registration form, or validate user input.
---

# Bootstrap 5.3 Forms

Bootstrap provides comprehensive form styling including controls, layouts, validation states, and input groups.

## Form Controls

### Text Inputs

```html
<div class="mb-3">
  <label for="email" class="form-label">Email address</label>
  <input type="email" class="form-control" id="email" placeholder="name@example.com">
</div>

<div class="mb-3">
  <label for="password" class="form-label">Password</label>
  <input type="password" class="form-control" id="password">
</div>
```

### Sizing

To match input size with surrounding elements or emphasize important fields, use sizing classes. Use `.form-control-lg` for hero sections or primary CTAs. Use `.form-control-sm` for compact UIs like toolbars or inline forms.

```html
<input class="form-control form-control-lg" type="text" placeholder="Large input">
<input class="form-control" type="text" placeholder="Default input">
<input class="form-control form-control-sm" type="text" placeholder="Small input">
```

### Disabled and Readonly

Use `disabled` for fields users cannot interact with at all. Use `readonly` when values should be visible and selectable but not editable. Use `.form-control-plaintext` with `readonly` to display values without form styling.

```html
<input class="form-control" type="text" disabled value="Disabled input">
<input class="form-control" type="text" readonly value="Readonly input">
<input class="form-control-plaintext" type="text" readonly value="Readonly plain text">
```

### File Input

```html
<div class="mb-3">
  <label for="file" class="form-label">Upload file</label>
  <input class="form-control" type="file" id="file">
</div>

<!-- Multiple files -->
<input class="form-control" type="file" multiple>
```

### Color Picker

```html
<div class="mb-3">
  <label for="color" class="form-label">Color picker</label>
  <input type="color" class="form-control form-control-color" id="color" value="#0d6efd">
</div>
```

### Textarea

```html
<div class="mb-3">
  <label for="textarea" class="form-label">Comments</label>
  <textarea class="form-control" id="textarea" rows="3"></textarea>
</div>
```

### Help Text

Use `.form-text` for supplemental instructions. Connect help text to inputs with `aria-describedby` so screen readers announce it when the input is focused:

```html
<div class="mb-3">
  <label for="password" class="form-label">Password</label>
  <input type="password" class="form-control" id="password" aria-describedby="passwordHelp">
  <div id="passwordHelp" class="form-text">Must be 8+ characters with one uppercase letter.</div>
</div>
```

When an input has both help text and validation feedback, reference both in `aria-describedby`:

```html
<div class="mb-3">
  <label for="email" class="form-label">Email</label>
  <input type="email" class="form-control is-invalid" id="email"
         aria-describedby="emailHelp emailError" aria-invalid="true">
  <div id="emailHelp" class="form-text">We'll never share your email.</div>
  <div id="emailError" class="invalid-feedback">Please enter a valid email address.</div>
</div>
```

## Select

```html
<select class="form-select">
  <option selected>Choose an option</option>
  <option value="1">Option One</option>
  <option value="2">Option Two</option>
  <option value="3">Option Three</option>
</select>

<!-- Multiple select -->
<select class="form-select" multiple>
  <option value="1">One</option>
  <option value="2">Two</option>
  <option value="3">Three</option>
</select>

<!-- Sizing -->
<select class="form-select form-select-lg">...</select>
<select class="form-select form-select-sm">...</select>

<!-- Visible options with size attribute -->
<select class="form-select" size="3">
  <option value="1">One</option>
  <option value="2">Two</option>
  <option value="3">Three</option>
  <option value="4">Four</option>
</select>
```

The `size` attribute displays multiple options without requiring `multiple` selection. Unlike `.form-select-lg` which changes visual scale, `size` controls how many options are visible at once. Use it for small option lists where showing all choices improves usability.

## Datalists

Datalists provide autocomplete suggestions for text inputs. They combine the flexibility of free-text input with the convenience of predefined options.

```html
<label for="browser" class="form-label">Choose a browser</label>
<input class="form-control" list="browsers" id="browser" placeholder="Type to search...">
<datalist id="browsers">
  <option value="Chrome">
  <option value="Firefox">
  <option value="Safari">
  <option value="Edge">
  <option value="Opera">
</datalist>
```

Connect the input to the datalist using the `list` attribute matching the datalist's `id`. Users can type freely or select from suggestions. Datalist styling is browser-native and varies across browsers—Bootstrap's `.form-control` styles the input, but the dropdown appearance is not customizable.

## Checkboxes and Radios

### Checkboxes

```html
<div class="form-check">
  <input class="form-check-input" type="checkbox" id="check1">
  <label class="form-check-label" for="check1">Default checkbox</label>
</div>
<div class="form-check">
  <input class="form-check-input" type="checkbox" id="check2" checked>
  <label class="form-check-label" for="check2">Checked checkbox</label>
</div>
```

### Indeterminate Checkboxes

Use the indeterminate state for checkboxes representing a "partially checked" condition. This is useful for "select all" patterns where some but not all child items are checked. The state must be set via JavaScript—there is no HTML attribute for it.

```html
<div class="form-check">
  <input class="form-check-input" type="checkbox" id="checkIndeterminate">
  <label class="form-check-label" for="checkIndeterminate">Select all items</label>
</div>

<script>
  document.getElementById('checkIndeterminate').indeterminate = true;
</script>
```

### Radios

```html
<div class="form-check">
  <input class="form-check-input" type="radio" name="radios" id="radio1" checked>
  <label class="form-check-label" for="radio1">First radio</label>
</div>
<div class="form-check">
  <input class="form-check-input" type="radio" name="radios" id="radio2">
  <label class="form-check-label" for="radio2">Second radio</label>
</div>
```

### Switches

Prefer switches over checkboxes for on/off settings that take effect immediately, like enabling notifications or toggling dark mode. Use checkboxes for multi-select options or when changes require a submit action.

```html
<div class="form-check form-switch">
  <input class="form-check-input" type="checkbox" role="switch" id="switch1">
  <label class="form-check-label" for="switch1">Default switch</label>
</div>
<div class="form-check form-switch">
  <input class="form-check-input" type="checkbox" role="switch" id="switch2" checked>
  <label class="form-check-label" for="switch2">Checked switch</label>
</div>
```

For iOS 17.4+ Safari, add the `switch` attribute to enable native haptic feedback:

```html
<div class="form-check form-switch">
  <input class="form-check-input" type="checkbox" role="switch" id="nativeSwitch" switch>
  <label class="form-check-label" for="nativeSwitch">Native haptics (iOS 17.4+)</label>
</div>
```

### Inline

```html
<div class="form-check form-check-inline">
  <input class="form-check-input" type="checkbox" id="inline1">
  <label class="form-check-label" for="inline1">1</label>
</div>
<div class="form-check form-check-inline">
  <input class="form-check-input" type="checkbox" id="inline2">
  <label class="form-check-label" for="inline2">2</label>
</div>
```

### Reverse Layout

Use `.form-check-reverse` to position the input on the opposite side—label first, checkbox/radio second. This creates a right-aligned input style useful for settings interfaces or RTL layouts.

```html
<div class="form-check form-check-reverse">
  <input class="form-check-input" type="checkbox" id="reverseCheck">
  <label class="form-check-label" for="reverseCheck">Reverse checkbox</label>
</div>

<div class="form-check form-check-reverse">
  <input class="form-check-input" type="radio" name="reverseRadios" id="reverseRadio1">
  <label class="form-check-label" for="reverseRadio1">First reverse radio</label>
</div>
```

## Toggle Buttons

Use `.btn-check` to create button-styled checkboxes and radios. Unlike standard form checks, toggle buttons use `.btn` classes on the label for a button appearance while maintaining checkbox/radio semantics. Use them for segmented controls, filter toggles, and option selectors.

### Checkbox Toggle

```html
<input type="checkbox" class="btn-check" id="btn-check" autocomplete="off">
<label class="btn btn-primary" for="btn-check">Single toggle</label>

<input type="checkbox" class="btn-check" id="btn-check-2" checked autocomplete="off">
<label class="btn btn-primary" for="btn-check-2">Checked</label>

<input type="checkbox" class="btn-check" id="btn-check-3" disabled autocomplete="off">
<label class="btn btn-primary" for="btn-check-3">Disabled</label>
```

### Radio Toggle

Group radio toggles with the `name` attribute for single-select behavior:

```html
<input type="radio" class="btn-check" name="options" id="option1" autocomplete="off" checked>
<label class="btn btn-secondary" for="option1">Checked</label>

<input type="radio" class="btn-check" name="options" id="option2" autocomplete="off">
<label class="btn btn-secondary" for="option2">Radio</label>

<input type="radio" class="btn-check" name="options" id="option3" autocomplete="off">
<label class="btn btn-secondary" for="option3">Radio</label>
```

### Outlined Styles

Use `.btn-outline-*` for a lighter, bordered appearance:

```html
<input type="checkbox" class="btn-check" id="btn-outlined" autocomplete="off">
<label class="btn btn-outline-primary" for="btn-outlined">Toggle</label>

<input type="radio" class="btn-check" name="opts" id="success" autocomplete="off" checked>
<label class="btn btn-outline-success" for="success">Success</label>

<input type="radio" class="btn-check" name="opts" id="danger" autocomplete="off">
<label class="btn btn-outline-danger" for="danger">Danger</label>
```

### Accessibility

Toggle buttons are announced by screen readers as "checked"/"not checked" since they are fundamentally checkboxes or radios. This differs from button plugin toggles announced as "button"/"button pressed". Choose based on semantics—use toggle buttons when the control represents a true on/off or selection state.

## Range

Range inputs provide a slider control. Use `.form-range` for consistent styling across browsers.

```html
<label for="range" class="form-label">Range slider</label>
<input type="range" class="form-range" id="range">

<!-- With min, max, step -->
<input type="range" class="form-range" min="0" max="100" step="5">
```

### Displaying the Current Value

Use the `<output>` element with JavaScript to show the current range value in real-time:

```html
<label for="volumeRange" class="form-label">
  Volume: <output id="volumeValue">50</output>
</label>
<input type="range" class="form-range" id="volumeRange"
       min="0" max="100" value="50"
       oninput="document.getElementById('volumeValue').textContent = this.value">
```

The `oninput` event fires as the slider moves, providing immediate feedback. Place the `<output>` element in the label or nearby for clear association. For more complex scenarios, use a separate event listener instead of inline handlers.

## Input Groups

Use input groups to visually attach related elements to form controls. Common patterns include currency symbols, units of measurement, or action buttons alongside inputs.

### Basic

```html
<div class="input-group mb-3">
  <span class="input-group-text">@</span>
  <input type="text" class="form-control" placeholder="Username">
</div>

<div class="input-group mb-3">
  <input type="text" class="form-control" placeholder="Email">
  <span class="input-group-text">@example.com</span>
</div>

<div class="input-group mb-3">
  <span class="input-group-text">$</span>
  <input type="text" class="form-control" placeholder="Amount">
  <span class="input-group-text">.00</span>
</div>
```

### With Buttons

```html
<div class="input-group mb-3">
  <input type="text" class="form-control" placeholder="Search...">
  <button class="btn btn-outline-secondary" type="button">Search</button>
</div>

<div class="input-group mb-3">
  <button class="btn btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
    Dropdown
  </button>
  <ul class="dropdown-menu">
    <li><a class="dropdown-item" href="#">Action</a></li>
  </ul>
  <input type="text" class="form-control">
</div>
```

### Sizing

```html
<div class="input-group input-group-sm">...</div>
<div class="input-group">...</div>
<div class="input-group input-group-lg">...</div>
```

### Wrapping Behavior

Input groups wrap by default via `flex-wrap: wrap`. To keep all elements on a single line regardless of content width, add `.flex-nowrap`:

```html
<div class="input-group flex-nowrap">
  <span class="input-group-text">@</span>
  <input type="text" class="form-control" placeholder="Username">
</div>
```

### Border Radius Limitations

Hidden elements (using `.d-none` or `display: none`) in the first or last position break border-radius styling on adjacent elements. This is a known Bootstrap limitation. Workaround: move hidden elements outside the input group or use visibility utilities instead when the element needs to remain in the DOM.

### Segmented Dropdown Buttons

Use `.dropdown-toggle-split` for split button dropdowns within input groups. This creates a separate dropdown trigger alongside a main action button:

```html
<div class="input-group">
  <button type="button" class="btn btn-outline-secondary">Action</button>
  <button type="button" class="btn btn-outline-secondary dropdown-toggle dropdown-toggle-split"
          data-bs-toggle="dropdown" aria-expanded="false">
    <span class="visually-hidden">Toggle Dropdown</span>
  </button>
  <ul class="dropdown-menu dropdown-menu-end">
    <li><a class="dropdown-item" href="#">Option 1</a></li>
    <li><a class="dropdown-item" href="#">Option 2</a></li>
  </ul>
  <input type="text" class="form-control" placeholder="Enter value">
</div>
```

## Floating Labels

Use floating labels for a cleaner, more compact form design where labels animate into the input on focus. They work best in simple forms like login or signup. Avoid them when you need help text or complex validation messages alongside inputs.

```html
<div class="form-floating mb-3">
  <input type="email" class="form-control" id="floatingEmail" placeholder="name@example.com">
  <label for="floatingEmail">Email address</label>
</div>

<div class="form-floating mb-3">
  <input type="password" class="form-control" id="floatingPassword" placeholder="Password">
  <label for="floatingPassword">Password</label>
</div>

<div class="form-floating">
  <textarea class="form-control" placeholder="Leave a comment" id="floatingTextarea"></textarea>
  <label for="floatingTextarea">Comments</label>
</div>
```

### Input Groups with Floating Labels and Validation

When combining floating labels with input groups and validation, special structure is required. Place `.form-floating` inside `.input-group`, add `.has-validation` to the input group, and place validation feedback outside `.form-floating` but inside `.input-group`:

```html
<div class="input-group has-validation">
  <span class="input-group-text">@</span>
  <div class="form-floating is-invalid">
    <input type="text" class="form-control is-invalid" id="floatingUsername"
           placeholder="Username" required>
    <label for="floatingUsername">Username</label>
  </div>
  <div class="invalid-feedback">Please choose a username.</div>
</div>
```

The `.has-validation` class ensures proper border-radius styling when validation feedback is present. Without it, the input group's visual appearance may break with validation states.

## Form Layout

Choose your layout based on form complexity and available space.

### Vertical (Default)

Use vertical layout for most forms—it's the simplest and works well on mobile. Labels stack above inputs for easy scanning.

```html
<form>
  <div class="mb-3">
    <label for="email" class="form-label">Email</label>
    <input type="email" class="form-control" id="email">
  </div>
  <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

### Horizontal

Use horizontal layout when you have ample width and want a more compact appearance. Best for settings pages or admin panels with many short fields.

```html
<form>
  <div class="row mb-3">
    <label for="email" class="col-sm-2 col-form-label">Email</label>
    <div class="col-sm-10">
      <input type="email" class="form-control" id="email">
    </div>
  </div>
  <div class="row">
    <div class="col-sm-10 offset-sm-2">
      <button type="submit" class="btn btn-primary">Submit</button>
    </div>
  </div>
</form>
```

### Inline

```html
<form class="row row-cols-lg-auto g-3 align-items-center">
  <div class="col-12">
    <input type="text" class="form-control" placeholder="Username">
  </div>
  <div class="col-12">
    <select class="form-select">
      <option selected>Choose...</option>
    </select>
  </div>
  <div class="col-12">
    <button type="submit" class="btn btn-primary">Submit</button>
  </div>
</form>
```

### Grid Layout

```html
<form>
  <div class="row g-3">
    <div class="col-md-6">
      <label for="firstName" class="form-label">First name</label>
      <input type="text" class="form-control" id="firstName">
    </div>
    <div class="col-md-6">
      <label for="lastName" class="form-label">Last name</label>
      <input type="text" class="form-control" id="lastName">
    </div>
    <div class="col-12">
      <label for="address" class="form-label">Address</label>
      <input type="text" class="form-control" id="address">
    </div>
    <div class="col-md-6">
      <label for="city" class="form-label">City</label>
      <input type="text" class="form-control" id="city">
    </div>
    <div class="col-md-4">
      <label for="state" class="form-label">State</label>
      <select id="state" class="form-select">
        <option selected>Choose...</option>
      </select>
    </div>
    <div class="col-md-2">
      <label for="zip" class="form-label">Zip</label>
      <input type="text" class="form-control" id="zip">
    </div>
    <div class="col-12">
      <button type="submit" class="btn btn-primary">Submit</button>
    </div>
  </div>
</form>
```

## Accessibility Essentials

Forms require proper accessibility attributes for screen reader support and WCAG compliance.

### Labels

Always associate labels with inputs using `for` and `id` attributes:

```html
<label for="email" class="form-label">Email address</label>
<input type="email" class="form-control" id="email">
```

For visually hidden labels, use `.visually-hidden`:

```html
<label for="search" class="visually-hidden">Search</label>
<input type="search" class="form-control" id="search" placeholder="Search...">
```

### Help Text

Connect help text to inputs with `aria-describedby`:

```html
<input type="password" class="form-control" id="password" aria-describedby="passwordHelp">
<div id="passwordHelp" class="form-text">Must be 8+ characters.</div>
```

### Validation States

Mark invalid fields for assistive technology:

```html
<input type="email" class="form-control is-invalid" aria-invalid="true" aria-describedby="emailError">
<div id="emailError" class="invalid-feedback">Please enter a valid email.</div>
```

### Required Fields

```html
<input type="text" class="form-control" required aria-required="true">
```

## Validation

### Browser Default

```html
<form class="row g-3 needs-validation" novalidate>
  <div class="col-md-6">
    <label for="validationCustom01" class="form-label">First name</label>
    <input type="text" class="form-control" id="validationCustom01" required>
    <div class="valid-feedback">Looks good!</div>
    <div class="invalid-feedback">Please provide a first name.</div>
  </div>
  <div class="col-12">
    <button class="btn btn-primary" type="submit">Submit form</button>
  </div>
</form>

<script>
// JavaScript for validation
(function () {
  'use strict'
  var forms = document.querySelectorAll('.needs-validation')
  Array.prototype.slice.call(forms).forEach(function (form) {
    form.addEventListener('submit', function (event) {
      if (!form.checkValidity()) {
        event.preventDefault()
        event.stopPropagation()
      }
      form.classList.add('was-validated')
    }, false)
  })
})()
</script>
```

### Validation States

```html
<!-- Valid -->
<input type="text" class="form-control is-valid">
<div class="valid-feedback">Looks good!</div>

<!-- Invalid -->
<input type="text" class="form-control is-invalid">
<div class="invalid-feedback">Please provide a valid value.</div>
```

### Validation Tooltips

Use `.valid-tooltip` and `.invalid-tooltip` as alternatives to feedback messages when you want positioned tooltip-style validation. Tooltips appear as floating messages positioned absolutely, requiring the parent element to have `position: relative`:

```html
<div class="col-md-4 position-relative">
  <label for="city" class="form-label">City</label>
  <input type="text" class="form-control is-invalid" id="city" required>
  <div class="valid-tooltip">Looks good!</div>
  <div class="invalid-tooltip">Please provide a valid city.</div>
</div>
```

Tooltips are useful when feedback messages would disrupt form layout or when you want a more prominent visual indicator. Use them consistently within a form—avoid mixing tooltips and feedback messages.

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Using placeholder as label | Not accessible, disappears on input | Always use `<label>` elements |
| Missing `novalidate` with custom validation | Browser shows default + custom feedback | Add `novalidate` to `<form>` |
| Forgetting `.has-validation` on input groups | Border radius breaks with validation | Add `.has-validation` to `.input-group` |
| Labels without `for` attribute | Screen readers can't associate label | Match `for` with input `id` |
| Missing `aria-describedby` for help text | Help text not announced | Connect with `aria-describedby` |
| Omitting `aria-invalid="true"` | Screen readers miss error state | Add `aria-invalid` with `.is-invalid` |
| Using `display: none` on first/last input group item | Border radius breaks on adjacent elements | Use `.visually-hidden` or move outside group |

See `references/validation-approaches.md` for validation method comparison and `references/accessibility-checklist.md` for complete accessibility requirements.

## Additional Resources

### Reference Files

- `references/form-reference.md` - Complete form class reference
- `references/validation-approaches.md` - Browser vs custom vs server-side validation comparison
- `references/accessibility-checklist.md` - Required attributes and testing procedures

### Example Files

- `examples/validation-form.html` - Form validation patterns
- `examples/floating-labels-form.html` - Signup and login forms with floating labels
- `examples/horizontal-form.html` - Horizontal layouts, sizing, radios, readonly display
- `examples/inline-search-form.html` - Navbar search, filters, toolbars, newsletter forms
- `examples/toggle-buttons.html` - Checkbox and radio toggle buttons, outlined styles
- `examples/accessibility-patterns.html` - Accessible forms with ARIA attributes
