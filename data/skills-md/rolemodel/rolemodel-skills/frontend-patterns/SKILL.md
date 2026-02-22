---
name: frontend-patterns
description: Frontend patterns for Rails applications using Slim templates, Stimulus JavaScript framework, CSS with Optics utilities. Use when building views, adding interactivity, styling components, or when the user mentions Slim, Stimulus, JavaScript, CSS, or frontend development.
---

# Frontend Patterns

## Tech Stack
- **Slim** - HTML templating
- **Stimulus** - JavaScript interactions
- **CSS** - Styling
- **Optics** - CSS styling framework
- **Simple Form** - Form builder

## Slim Templates

### Conventions
- Use Ruby 3+ syntax (e.g., keyword arguments with `:`)
- Keep logic minimal in views
- Extract complex rendering to helpers or partials
- Use locals for partial data passing
- **Always prioritize DRY principles - extract repeated markup into partials**
- **Extract partials when logic or markup is repeated more than once**
- **Never use inline styles**

### When to Use Helpers vs Partials

**Use Helper Methods when:**
- Simple conditional logic that returns HTML with different text/classes
- Formatting data (dates, currency, durations)
- Generating single HTML elements with varying attributes
- Logic is stateless and doesn't need multiple elements
- Example: `status_badge(status)`, `format_duration(seconds)`

**Use Partials when:**
- Complex markup structure (multiple nested elements)
- Reusable UI components with layout
- Need to render collections
- Significant HTML that would clutter a helper
- Example: `_time_entry_row.html.slim`, `_timer_form.html.slim`

**Rule of thumb:** If it's primarily conditional text/classes in a single element, use a helper. If it's a structure/layout, use a partial.

### Partial Extraction Guidelines
- Extract forms on the `new` and `edit` pages into `_form` partials
- Extract repeated structures into component partials
- Use descriptive partial names: `_time_entry_row`, `_project_selector`, `_status_badge`
- Place partials in same directory as parent view or in `shared/` for cross-feature use
- Always use keyword arguments for partial locals: `render 'row', time_entry:, show_actions: true`

### Partial Organization
```
app/views/
  time_entries/
    edit.html.slim            # Edit view
    index.html.slim           # Main view
    new.html.slim             # New view
    show.html.slim            # Show view
    _time_entries.html.slim   # Table collection of rows
    _time_entry.html.slim     # Individual row
    _form.html.slim           # Time Entries form
  shared/
    _status_badge.html.slim   # Reusable badge
    _empty_state.html.slim    # Empty state pattern
```

### Conditional class names
Use the rails class_names helper to manage conditional class names in Slim templates.
```slim
button.btn class=class_names('btn--active': active) Click Me
```

### Example
```slim
-# locals: (user:, active: false)
.user-card class=('active' if active)
  h3 = user.name
  p = user.email
```

## Simple Form

### Overview
Always use Simple Form for forms. Never use `form_with`, `form_for`, or Rails form helpers directly.

### Basic Model Form
```slim
= simple_form_for @user do |f|
  = f.input :first_name
  = f.input :last_name
  = f.input :email, required: true

  .form__actions
    = link_to 'Cancel', :back, class: 'btn btn--outline'
    = f.submit 'Save', class: 'btn btn--primary'
```

### Non-Model Form (with URL)
For forms without a model (like bulk actions or search forms):

```slim
= simple_form_for :search, url: search_path, method: :get do |f|
  = f.input :query, label: 'Search'
  = f.submit 'Search', class: 'btn btn--primary'
```

**Important**: When using `simple_form_for :symbol`, params are nested under the symbol:
```ruby
# View: simple_form_for :time_entry
# Params received: { time_entry: { task_id: 1, description: "text" } }
# Access with: params.dig(:time_entry, :task_id)
```

### Form with HTML Options
```slim
= simple_form_for @record, html: { id: 'custom-form', class: 'special-form' } do |f|
  = f.input :name
```

### Form with Data Attributes (Turbo)
```slim
= simple_form_for @record, data: { turbo_frame: '_top' } do |f|
  = f.input :name
```

### Common Input Types
```slim
/ Text input
= f.input :name

/ Text area
= f.input :description, as: :text, input_html: { rows: 4 }

/ Select dropdown
= f.input :project_id, collection: @projects, prompt: 'Select a project...'

/ Boolean checkbox
= f.input :active, as: :boolean

/ Date picker
= f.input :start_date, as: :date

/ With placeholder
= f.input :email, placeholder: 'user@example.com'

/ With custom input attributes
= f.input :description, input_html: { rows: 3, required: true, data: { controller: 'auto-save' } }
```

### Collections and Associations
```slim
/ Simple collection
= f.input :category_id, collection: @categories

/ With custom text/value methods
= f.input :project_id, collection: @projects, label_method: :name, value_method: :id

/ Grouped collection
= f.input :task_id, as: :grouped_select, collection: @projects, group_method: :tasks

/ With prompt
= f.input :status, collection: ['pending', 'approved', 'rejected'], prompt: 'Select status...'
```

### Custom Labels and Hints
```slim
= f.input :email, label: 'Email Address', hint: 'We will never share your email'
= f.input :password, label: 'Password', placeholder: 'At least 8 characters'
```

### Disabled Inputs
```slim
= f.input :task_id, disabled: true, input_html: { data: { target: 'form.taskSelect' } }
```

### Hidden Fields
```slim
= f.hidden_field :organization_id, value: current_user.organization_id
```

### Submit Buttons
```slim
/ Standard submit
= f.submit 'Save', class: 'btn btn--primary'

/ With data attributes
= f.submit 'Save', class: 'btn btn--primary', data: { disable_with: 'Saving...' }

/ Associated with external form (for modal footers)
= f.submit 'Save', form: 'my-form-id', class: 'btn btn--primary'
```

### Form Actions Pattern
Standard pattern for form button groups:

```slim
.form__actions
  = link_to 'Cancel', :back, class: 'btn btn--outline'
  = f.submit 'Save', class: 'btn btn--primary'
```

### Bulk Action Forms
For forms that collect checkboxes without inputs:

```slim
= simple_form_for :bulk_action, url: bulk_approve_path, method: :post, html: { id: 'bulk-form' } do |f|
  / Form will collect checked checkboxes via form attribute

/ Checkboxes reference the form
= check_box_tag 'entry_ids[]', entry.id, false, form: 'bulk-form'
```

### Modal Forms
Forms that submit within modals and redirect to parent page:

```slim
= simple_form_for @record, html: { id: 'modal-form' }, data: { turbo_frame: '_top' } do |f|
  = f.input :reason, as: :text, input_html: { rows: 3, required: true }

-# In modal footer (outside form)
- content_for :modal_actions do
  = button_tag 'Submit', type: 'submit', form: 'modal-form', class: 'btn btn--primary'
```

### Best Practices
- Always use `simple_form_for`, never `form_with` or `form_for`
- Use `:symbol` for non-model forms with url parameter
- Use `@model` for model-based forms
- Leverage Simple Form's automatic label generation
- Use `input_html` for custom HTML attributes on the input element
- Use `html` option for attributes on the form element itself
- Keep forms accessible with proper labels
- Use `.form__actions` for button groups

## Stimulus Controllers

### Structure
- One controller per behavior
- Use data attributes for configuration
- Keep controllers focused and composable
- Follow naming conventions (kebab-case in HTML)

### Example
```javascript
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["output"]
  static values = { url: String }

  connect() {
    // Initialization
  }

  perform() {
    // Action logic
  }
}
```

## CSS & Optics

### Guidelines
- Use Optics utility classes where applicable
- Keep custom CSS minimal and scoped
- Follow BEM or similar naming for custom components
- Avoid inline styles

## Future Topics
- Turbo Frames and Streams patterns
- Form styling conventions
- Icon helper usage
- Responsive design patterns
- Animation and transition guidelines
