---
name: form-auto-save
description: Automatic form submission after user input changes using a debounce mechanism to prevent excessive server requests. Creates a seamless auto-save experience for forms with rich text editors or multiple fields.
---

# Form Auto Save Skill

## Overview
The Form Auto Save pattern provides automatic form submission after user input changes, using a debounce mechanism to prevent excessive server requests. This creates a seamless "auto-save" experience for users editing forms.

## When to Use
- Long-form editing interfaces where users expect automatic saving
- Forms with rich text editors or multiple fields
- Edit pages where users might navigate away and expect changes to persist
- Forms that benefit from progressive saving without explicit "Save" button clicks

## Implementation

### 1. Stimulus Controller
The pattern uses a Stimulus controller (`form-auto-save`) that handles the auto-save logic.

**Controller Location:** `app/javascript/controllers/form_auto_save_controller.js`

**Key Features:**
- Debounce time of 8 seconds (configurable via `static DEBOUNCE_TIME`)
- Listens to both `change` and `lexxy:change` events (for custom components)
- Uses passive event listeners for better performance
- Provides `cancel()` and `submit()` methods for programmatic control

**Controller Code Pattern:**
```javascript
import { Controller } from '@hotwired/stimulus'

export default class extends Controller {
  static DEBOUNCE_TIME = 8000

  connect() {
    this.element.addEventListener('change', this.#debounceSubmit.bind(this), { passive: true })
    this.element.addEventListener('lexxy:change', this.#debounceSubmit.bind(this), { passive: true })
  }

  cancel() {
    clearTimeout(this.debounceTimer)
  }

  submit() {
    this.element.requestSubmit()
  }

  #debounceSubmit() {
    this.#debounce(this.submit.bind(this))
  }

  #debounce(callback) {
    clearTimeout(this.debounceTimer)
    this.debounceTimer = setTimeout(callback, this.constructor.DEBOUNCE_TIME)
  }
}
```

### 2. View Integration
Attach the controller to the form element using Stimulus data attributes.

**Required Attributes:**
- `data: { controller: 'form-auto-save' }` - Attaches the Stimulus controller
- `data: { turbo_permanent: true }` - Optional but recommended to preserve form state during Turbo navigation

**Example (Slim):**
```slim
= simple_form_for resource, html: { data: { controller: 'form-auto-save', turbo_permanent: true } } do |f|
  = f.input :field_name
  = f.rich_text_area :content
```

## Important Considerations

### Debounce Time
- Default: 8 seconds (8000ms)
- Adjust via `static DEBOUNCE_TIME` in the controller if needed
- Consider user experience: too short = excessive requests, too long = lost changes

### Event Listeners
- Listens to `change` events (standard HTML input changes)
- Listens to `lexxy:change` events (custom component events, like rich text editors)
- Uses passive listeners for better scroll performance

### Turbo Permanent
- `turbo_permanent: true` keeps the form element across Turbo navigation
- Prevents loss of unsaved changes when user navigates
- Critical for forms with auto-save to maintain debounce timers

### Form Validation
- Ensure backend validation handles partial saves gracefully
- Consider whether all fields should be required or allow partial completion
- Provide clear error feedback if auto-save fails

## Testing

For testing auto-save functionality, use the `turbo-fetch` controller alongside `form-auto-save` to track request completion without relying on sleep timers.

### Turbo Fetch Controller
Add this controller to your JavaScript controllers:

**File:** `app/javascript/controllers/turbo_fetch_controller.js`
```javascript
import { Controller } from '@hotwired/stimulus'
import { patch } from '@rails/request.js'

export default class extends Controller {
  static values = {
    url: String,
    count: Number,
    isRunning: { type: Boolean, default: false }
  }

  async perform({ params: { url: urlParam, query: queryParams } }) {
    this.isRunningValue = true
    const body = new FormData(this.element)

    if (queryParams) Object.keys(queryParams).forEach(key => body.append(key, queryParams[key]))

    const response = await patch(urlParam || this.urlValue, { body, responseKind: 'turbo-stream' })
    this.isRunningValue = false
    if (response.ok) this.countValue += 1
  }
}
```

### Turbo Fetch Helper
Add this helper to your RSpec support files:

**File:** `spec/support/helpers/turbo_fetch_helper.rb`
```ruby
module TurboFetchHelper
  def expect_turbo_fetch_request
    count_value = find("[data-controller='turbo-fetch']")['data-turbo-fetch-count-value'] || 0
    yield
    expect(page).to have_selector("[data-turbo-fetch-count-value='#{count_value.to_i + 1}']")
  end
end
```

### View Integration for Testing
Add the `turbo-fetch` controller alongside `form-auto-save`:

```slim
= simple_form_for resource, html: { data: { controller: 'form-auto-save turbo-fetch', turbo_permanent: true } } do |f|
  = f.input :field_name
  = f.rich_text_area :content
```

### System Spec Example
```ruby
require 'rails_helper'

RSpec.describe 'Form Auto Save', :js do
  it 'automatically saves form after changes' do
    resource = create(:resource)
    visit edit_resource_path(resource)

    expect_turbo_fetch_request do
      fill_in 'Field name', with: 'Updated value'
    end

    expect(resource.reload.field_name).to eq('Updated value')
  end

  it 'debounces multiple rapid changes' do
    resource = create(:resource)
    visit edit_resource_path(resource)

    expect_turbo_fetch_request do
      fill_in 'Field name', with: 'First'
      fill_in 'Field name', with: 'Second'
      fill_in 'Field name', with: 'Final'
    end

    # Should only save once with final value
    expect(resource.reload.field_name).to eq('Final')
  end
end
```

## Common Issues

### Issue: Form doesn't auto-save
**Check:**
- Controller properly attached: `data: { controller: 'form-auto-save' }`
- Form fields trigger `change` events (text inputs may need blur)
- Network requests in browser DevTools

### Issue: Too many requests
**Solutions:**
- Increase `DEBOUNCE_TIME`
- Check for unnecessary event triggers
- Verify debounce logic is working

### Issue: Lost changes on navigation
**Solutions:**
- Add `turbo_permanent: true` to form
- Ensure form has stable `id` attribute
- Consider adding "unsaved changes" warning

## Related Patterns
- **Turbo Streams:** For more complex form updates and partial page replacements
- **Stimulus Values:** If you need per-instance debounce times
- **Form Validation:** Consider inline validation with auto-save

## References
- Stimulus Controller API: https://stimulus.hotwired.dev/
- Turbo Permanent: https://turbo.hotwired.dev/handbook/building#persisting-elements-across-page-loads
