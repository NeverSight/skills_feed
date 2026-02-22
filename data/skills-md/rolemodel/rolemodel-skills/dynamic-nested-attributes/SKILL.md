---
name: dynamic-nested-attributes
description: Implement Rails nested attributes with dynamic add/remove functionality using Turbo Streams and Simple Form. Use when building forms where users need to manage multiple child records (has_many associations), add/remove nested items without page refresh, or create bulk records inline.
---

# Dynamic Nested Attributes

## Overview
Implement Rails nested attributes with dynamic add/remove functionality using Turbo Streams and Simple Form. This pattern allows users to add and remove associated records inline within a parent form.

## When to Use
- Building forms where users need to manage multiple child records (has_many associations)
- Adding/removing nested items without page refresh
- Bulk creation or editing of associated records
- Forms requiring progressive disclosure of additional fields

## Key Components

### 1. Form Object or Model
- Accepts nested attributes for the association
- Use `accepts_nested_attributes_for :association_name` in the model or form object

### 2. Main Form View
Create a form that includes:
- `simple_fields_for` for rendering existing nested items
- A container element with an ID for appending new items (e.g., `#accessories`)
- A link to add new items that triggers a Turbo Stream request

**Example:**
```slim
= simple_form_for resource do |f|
  = f.simple_fields_for :items do |ff|
    = render 'item_fields', f: ff, resource:

= render 'add_button', index: resource.items.size
```

**Add Button Partial (`_add_button.html.slim`):**
```slim
-# locals: (index:)
= link_to icon('add'), new_parent_item_path(index: index),
  id: 'add_button', class: 'btn', data: { turbo_stream: true }
```

### 3. Nested Fields Partial
Create a partial (e.g., `_item_fields.html.slim`) that:
- Wraps fields in a unique container with an ID based on index
- Includes a data controller for remove functionality
- Shows a delete button for all records
- Includes all form inputs for the nested item

**Example:**
```slim
fieldset id="item_#{f.index}" controller='destroy-nested-attributes'
  = f.hidden_field :_destroy, data: { destroy_nested_attributes_target: 'input' }
  = f.input :name
  = f.input :quantity
  .form-row__actions
    = button_tag icon('delete'), type: 'button', class: 'btn btn-delete',
      data: { action: 'destroy-nested-attributes#perform' }
```

### 4. Controller Actions
Implement a `new` action that:
- Builds a new nested item
- Accepts `index` parameter for tracking position

**Example:**
```ruby
def new
  @item = Item.new
end
```

### 5. Turbo Stream Response
Create a `new.turbo_stream.slim` view that:
- Updates the "add" button with incremented index
- Appends the new nested fields to the container
- Uses `index` parameter to ensure unique field names
- Works with non-persisted parents by using a symbol and empty URL

**Example:**
```slim
= turbo_stream.replace 'add_button', partial: 'add_button', locals: { index: params[:index].to_i + 1 }

= simple_form_for :parent, url: '' do |f|
  = f.simple_fields_for :items_attributes, @item, index: params[:index] do |ff|
    = turbo_stream.append 'items', partial: 'item_fields', locals: { f: ff }
```

### 6. Remove Stimulus Controller
Create a Stimulus controller to handle client-side removal:

**Example JavaScript:**
```javascript
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ['input']
  static classes = ['destroyed']

  connect() {
    if (!this.hasDestroyedClass) {
      this.element.setAttribute(`data-${this.identifier}-destroyed-class`, 'is-hidden')
    }
  }

  perform() {
    this.inputTarget.value = '1'
    this.element.classList.add(this.destroyedClass)
  }
}
```

## Implementation Checklist

- [ ] Add `accepts_nested_attributes_for` to model/form object
- [ ] Create main form with `simple_fields_for` and container element
- [ ] Create nested fields partial with remove functionality
- [ ] Implement controller `new` action with index support
- [ ] Create turbo_stream response view
- [ ] Add Stimulus controller for client-side removal
- [ ] Update routes to support nested resource creation
- [ ] Update strong parameters to permit nested attributes
- [ ] Add policy authorization if using Pundit

## Common Patterns

### Dynamic Collections Based on Parent Selection
Pass filtered collections to nested partials:
```slim
= render 'item_fields', f: ff, resource:, collection: resource.items
```

## Routes Example
If there is not an existing new route in use, use the following pattern
```ruby
resources :items, only: [:new]
```

If one does exist, create a new namespaced controller
```ruby
namespace :parent do
  resources :items, only: [:new]
end
```

## Strong Parameters Example
```ruby
def item_params
  params.require(:parent).permit(
    :category,
    :subcategory,
    items_attributes: %i[
      name
      quantity
      part_id
      optional
      hidden
    ]
  )
end
```

## Related Patterns
- Turbo Frame inline editing
- Stimulus data controller integration
- Form object pattern for bulk operations
- Policy-scoped collections for associations
