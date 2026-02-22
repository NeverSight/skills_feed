---
name: testing-patterns
description: Write automated tests using RSpec, Capybara, and FactoryBot for Rails applications. Use when implementing features, fixing bugs, or when the user mentions testing, specs, RSpec, Capybara, or test data. Avoid using rails console or server for testing.
---

# Testing Patterns

## Overview
Write automated tests using RSpec and Capybara. Avoid using the Rails console or starting a Rails server for testing.

## Test Command
```bash
bundle exec rspec
```

## Tech Stack
- **RSpec** - Testing framework
- **Capybara** - System/integration testing
- **FactoryBot** - Test data generation

## Best Practices

### General Guidelines
- Write tests first or alongside implementation
- Avoid manual testing via console
- Use factories for test data creation
- Keep tests focused and readable

### RSpec Conventions
- Use descriptive context and describe blocks
- Follow the arrange-act-assert pattern
- Use let for test data setup
- Prefer `let` over instance variables

### let vs let! (Lazy vs Eager Evaluation)

**Use `let` (lazy evaluation) when:**
- The variable is explicitly referenced in the test
- You want to avoid unnecessary database writes
- The record creation has side effects you want to control

**Use `let!` (eager evaluation) when:**
- Records must exist in the database before the test runs
- The variable is not directly referenced but its existence is required
- Testing queries that search for records (e.g., index pages, search functionality)
- Setting up background data that other records depend on

**Example - System Tests:**
```ruby
RSpec.describe 'Job Management', type: :system do
  # Use let! - these records must exist in DB for dropdowns and queries
  let!(:location) { create(:location, name: 'Downtown Site') }
  let!(:superintendent) { create(:user, :superintendent) }

  # Use let - only created when explicitly referenced in a test
  let(:job) { create(:job, name: 'Test Job', location:, superintendent:) }

  it 'shows location in dropdown' do
    visit new_job_path
    # location must exist in DB for dropdown to display it
    expect(page).to have_select('Location', with_options: [location.name])
  end

  it 'can delete a job' do
    visit job_path(job)  # job created here when first referenced
    click_button 'Delete'
  end
end
```

**Common Pitfall:**
```ruby
# ❌ WRONG - Test will fail because job2 doesn't exist in DB yet
let(:job1) { create(:job, name: 'Job 1') }
let(:job2) { create(:job, name: 'Job 2') }

it 'lists all jobs' do
  visit jobs_path
  expect(page).to have_content('Job 1')  # job1 created when referenced
  expect(page).to have_content('Job 2')  # FAIL - job2 never referenced, not in DB
end

# ✅ CORRECT - Both jobs exist before test runs
let!(:job1) { create(:job, name: 'Job 1') }
let!(:job2) { create(:job, name: 'Job 2') }

it 'lists all jobs' do
  visit jobs_path
  expect(page).to have_content('Job 1')  # Both jobs already in DB
  expect(page).to have_content('Job 2')  # Test passes
end
```

**Key Insight:**
If you expect to see data without explicitly interacting with the object variable (like viewing a list or selecting from a dropdown), use `let!` to ensure the record exists in the database.

### Validation Testing Pattern
Test validations explicitly using `build` with invalid data, then verify the model is invalid and check error messages:

```ruby
describe 'validations' do
  it 'must have a start date' do
    membership = build(:membership, start_date: nil)

    expect(membership).not_to be_valid
    expect(membership.errors.full_messages).to contain_exactly "Start date can't be blank"
  end

  it 'enforces end date must follow start date' do
    membership = build(:membership, start_date: 1.year.ago, end_date: 2.years.ago)

    expect(membership).not_to be_valid
    expect(membership.errors.full_messages).to contain_exactly 'End date must follow start date'
  end

  it 'permits empty end date' do
    membership = build(:membership, start_date: 1.year.ago, end_date: nil)

    expect(membership).to be_valid
  end
end
```

Key points:
- Use `build` instead of `create` to avoid database writes
- Test both invalid and valid scenarios
- Verify exact error messages with `full_messages`
- Use descriptive test names that explain the business rule
- Don't test associations or enums

### Capybara System Tests
- Test user-facing functionality
- Use `data-testid` attributes with `dom_id` for reliable element selection
- Test happy paths and edge cases
- Ensure tests are deterministic
- Avoid sleep statements; use Capybara's waiting mechanisms such as native expectations of elements to appear
- Use `:js` (e.g. `it 'does something', :js do`) for specs that run javascript such as stimulus controllers

### Element Selection with data-testid
Use `data-testid` attributes with `dom_id` for stable, reliable element selection that's resistant to UI changes:

**View:**
```slim
tbody
  - @entries.each do |entry|
    tr data-testid=dom_id(entry)
      td= entry.name
```

**Spec:**
```ruby
within(data_test(entry1)) do
  click_button 'Submit'
end
```

**Benefits:**
- Resilient to text changes (descriptions, labels, etc.)
- Works with dynamic content
- Self-documenting test intent
- Easier to refactor views

**Avoid:**
- Text-based lookups: `within('tr', text: 'Entry 1')`
- CSS class selectors that may change during styling
- Overly specific DOM traversal

### Scoping with within Blocks
When elements are ambiguous (multiple buttons/links with same text), use `within` blocks to scope interactions:

**Best Practice:**
Always use `within` blocks when:
1. Multiple elements share the same text/label
2. Interacting with modals, panels, or overlays
3. Working with repeating elements (table rows, cards)
4. Tests fail with "Ambiguous match" errors

### Turbo Confirm Dialogs
When testing actions that trigger Turbo confirm dialogs (e.g., delete buttons with `data: { turbo_confirm: 'message' }`), use the provided helper methods.

**Setup:**

Create the helper file:
```ruby
# spec/support/turbo_confirm_helper.rb
module TurboConfirmHelper
  def accept_turbo_confirm
    yield
    expect(page).to have_css '.confirm-dialog-wrapper--active', wait: 5
    sleep(0.5)
    within '.confirm-dialog-wrapper--active' do
      find('#confirm-accept').click
    end
    expect(page).to_not have_css '.confirm-dialog-wrapper--active', wait: 5
  end

  def deny_turbo_confirm
    yield
    expect(page).to have_css '.confirm-dialog-wrapper--active', wait: 5
    sleep(0.5)
    within '.confirm-dialog-wrapper--active' do
      find('#confirm-cancel').click
    end
    expect(page).to_not have_css '.confirm-dialog-wrapper--active', wait: 5
  end
end
```

Include in RSpec configuration:
```ruby
# spec/support/helpers.rb
RSpec.configure do |c|
  # ...existing code...
  c.include TurboConfirmHelper, type: :system
end
```

**Usage in Tests:**
```ruby
accept_turbo_confirm do
  click_button 'Delete'
end

deny_turbo_confirm do
  click_button 'Delete'
end
```

**Key Points:**
- Always use `:js` tag for tests involving Turbo confirm dialogs
- Pass the action that triggers the confirm as a block to the helper
- The helper automatically waits for the dialog to appear and disappear
- Use `accept_turbo_confirm` to click "Yes, I'm Sure"
- Use `deny_turbo_confirm` to click "Cancel"
- Helpers include proper wait times and scoping for reliability

### FactoryBot
- Define factories for all models
- Use traits for variations
- Keep factories minimal
- Override attributes in tests as needed
- Always use `build` or `create` instead of direct model instantiation
- Use `build` for validation tests to avoid database writes
- Use `create` when you need persisted records

## Future Topics
- Mocking and stubbing patterns
- Test organization strategies
- Performance testing
- CI/CD integration
