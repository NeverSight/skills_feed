---
name: inertia-rails-testing
description: Test Inertia Rails applications with RSpec or Minitest. Use when writing tests for Inertia responses, components, props, flash messages, and partial reloads.
license: MIT
metadata:
  author: community
  version: "1.0.0"
user-invocable: true
---

# Inertia Rails Testing

Comprehensive guide to testing Inertia Rails applications with RSpec and Minitest.

## Testing Approaches

1. **Endpoint tests** - Verify server-side Inertia responses
2. **Client-side unit tests** - Test components with Vitest/Jest
3. **End-to-end tests** - Full browser testing with Capybara

## RSpec Setup

Add to `spec/rails_helper.rb`:

```ruby
require 'inertia_rails/rspec'
```

## RSpec Matchers Reference

### `be_inertia_response`

Verifies the response is an Inertia response:

```ruby
it 'returns an Inertia response' do
  get users_path
  expect(inertia).to be_inertia_response
end
```

### `render_component`

Checks the rendered component name:

```ruby
it 'renders the correct component' do
  get users_path
  expect(inertia).to render_component('users/index')

  # Case-insensitive matching
  expect(inertia).to render_component('Users/Index')
end
```

### `have_props`

Partial matching of props:

```ruby
it 'includes expected props' do
  get user_path(user)

  expect(inertia).to have_props(
    user: hash_including(
      id: user.id,
      name: 'John'
    )
  )
end

# With RSpec matchers
it 'has users array' do
  get users_path
  expect(inertia).to have_props(
    users: be_an(Array),
    total: be > 0
  )
end

# Check for specific keys
it 'includes required keys' do
  get dashboard_path
  expect(inertia).to have_props(:user, :stats, :notifications)
end
```

### `have_exact_props`

Exact matching of all props:

```ruby
it 'has exactly these props' do
  get simple_page_path

  expect(inertia).to have_exact_props(
    title: 'Simple Page',
    content: 'Hello'
  )
end
```

### `have_flash`

Check flash messages:

```ruby
it 'shows success message' do
  post users_path, params: { user: valid_attributes }
  follow_redirect!

  expect(inertia).to have_flash(notice: 'User created!')
end

it 'shows error message' do
  delete user_path(admin_user)
  follow_redirect!

  expect(inertia).to have_flash(alert: 'Cannot delete admin')
end
```

### `have_deferred_props`

Verify deferred props:

```ruby
it 'defers analytics data' do
  get dashboard_path

  expect(inertia).to have_deferred_props(:analytics)
  expect(inertia).to have_deferred_props(analytics: 'stats')  # with group
end
```

## Complete RSpec Examples

### Basic Request Specs

```ruby
# spec/requests/users_spec.rb
require 'rails_helper'

RSpec.describe '/users', type: :request do
  let(:user) { create(:user) }
  let(:valid_attributes) { { name: 'John', email: 'john@example.com' } }
  let(:invalid_attributes) { { name: '', email: 'invalid' } }

  describe 'GET /users' do
    before { create_list(:user, 3) }

    it 'renders the index component with users' do
      get users_path

      expect(inertia).to be_inertia_response
      expect(inertia).to render_component('users/index')
      expect(inertia).to have_props(
        users: have_attributes(size: 3)
      )
    end
  end

  describe 'GET /users/:id' do
    it 'renders the show component' do
      get user_path(user)

      expect(inertia).to render_component('users/show')
      expect(inertia).to have_props(
        user: hash_including(
          id: user.id,
          name: user.name,
          email: user.email
        )
      )
    end

    it 'does not expose sensitive data' do
      get user_path(user)

      user_props = inertia.props[:user]
      expect(user_props).not_to have_key(:password_digest)
      expect(user_props).not_to have_key(:remember_token)
    end
  end

  describe 'GET /users/new' do
    it 'renders the new component' do
      get new_user_path

      expect(inertia).to render_component('users/new')
    end
  end

  describe 'POST /users' do
    context 'with valid parameters' do
      it 'creates a new user and redirects' do
        expect {
          post users_path, params: { user: valid_attributes }
        }.to change(User, :count).by(1)

        expect(response).to redirect_to(users_url)
      end

      it 'shows success flash' do
        post users_path, params: { user: valid_attributes }
        follow_redirect!

        expect(inertia).to have_flash(notice: /created/i)
      end
    end

    context 'with invalid parameters' do
      it 'does not create a user' do
        expect {
          post users_path, params: { user: invalid_attributes }
        }.not_to change(User, :count)
      end

      it 'returns validation errors' do
        post users_path, params: { user: invalid_attributes }
        follow_redirect!

        expect(inertia).to have_props(
          errors: hash_including(:name, :email)
        )
      end
    end
  end

  describe 'PATCH /users/:id' do
    context 'with valid parameters' do
      it 'updates the user' do
        patch user_path(user), params: { user: { name: 'Updated' } }

        expect(user.reload.name).to eq('Updated')
        expect(response).to redirect_to(user_url(user))
      end
    end

    context 'with invalid parameters' do
      it 'returns validation errors' do
        patch user_path(user), params: { user: { email: 'invalid' } }
        follow_redirect!

        expect(inertia).to have_props(errors: hash_including(:email))
      end
    end
  end

  describe 'DELETE /users/:id' do
    it 'destroys the user' do
      user # create the user

      expect {
        delete user_path(user)
      }.to change(User, :count).by(-1)

      expect(response).to redirect_to(users_url)
    end
  end
end
```

### Testing Shared Data

```ruby
# spec/requests/shared_data_spec.rb
RSpec.describe 'Shared data', type: :request do
  describe 'authentication data' do
    context 'when logged in' do
      before { sign_in(user) }

      it 'includes current user' do
        get root_path

        expect(inertia).to have_props(
          auth: hash_including(
            user: hash_including(id: user.id)
          )
        )
      end
    end

    context 'when logged out' do
      it 'has null user' do
        get root_path

        expect(inertia).to have_props(
          auth: hash_including(user: nil)
        )
      end
    end
  end
end
```

### Testing Partial Reloads

```ruby
# spec/requests/partial_reloads_spec.rb
RSpec.describe 'Partial reloads', type: :request do
  it 'supports partial reload of specific props' do
    get dashboard_path
    expect(inertia).to have_props(:users, :stats, :notifications)

    # Simulate partial reload
    inertia_reload_only(:users)

    expect(inertia).to have_props(:users)
    expect(inertia.props.keys).to eq([:users])
  end

  it 'supports excluding props' do
    get dashboard_path

    inertia_reload_except(:notifications)

    expect(inertia).to have_props(:users, :stats)
    expect(inertia).not_to have_props(:notifications)
  end
end
```

### Testing Deferred Props

```ruby
# spec/requests/deferred_props_spec.rb
RSpec.describe 'Deferred props', type: :request do
  it 'initially defers expensive data' do
    get dashboard_path

    expect(inertia).to have_deferred_props(:analytics)
    expect(inertia.props).not_to have_key(:analytics)
  end

  it 'loads deferred props on request' do
    get dashboard_path
    inertia_load_deferred_props

    expect(inertia).to have_props(
      analytics: be_present
    )
  end
end
```

## Minitest Setup

Add to `test/test_helper.rb`:

```ruby
require 'inertia_rails/minitest'
```

## Minitest Assertions Reference

| RSpec Matcher | Minitest Assertion |
|---------------|-------------------|
| `be_inertia_response` | `assert_inertia_response` |
| `render_component` | `assert_inertia_component` |
| `have_props` | `assert_inertia_props` |
| `have_exact_props` | `assert_inertia_props_equal` |
| `have_flash` | `assert_inertia_flash` |
| `have_deferred_props` | `assert_inertia_deferred_props` |

Negation: `refute_*` variants available.

## Complete Minitest Examples

```ruby
# test/integration/users_test.rb
require 'test_helper'

class UsersTest < ActionDispatch::IntegrationTest
  def setup
    @user = users(:one)
  end

  test 'index renders users list' do
    get users_path

    assert_inertia_response
    assert_inertia_component 'users/index'
    assert_inertia_props users: ->(users) { users.is_a?(Array) }
  end

  test 'show renders user details' do
    get user_path(@user)

    assert_inertia_component 'users/show'
    assert_inertia_props(
      user: {
        id: @user.id,
        name: @user.name
      }
    )
  end

  test 'create with valid params redirects' do
    assert_difference 'User.count', 1 do
      post users_path, params: {
        user: { name: 'New User', email: 'new@example.com' }
      }
    end

    assert_redirected_to users_url
  end

  test 'create with invalid params shows errors' do
    post users_path, params: { user: { name: '' } }
    follow_redirect!

    assert_inertia_props errors: { name: ["can't be blank"] }
  end

  test 'shows flash after successful create' do
    post users_path, params: {
      user: { name: 'Test', email: 'test@example.com' }
    }
    follow_redirect!

    assert_inertia_flash notice: 'User created!'
  end

  test 'deferred props are loaded separately' do
    get dashboard_path

    assert_inertia_deferred_props :analytics

    inertia_load_deferred_props
    assert_inertia_props analytics: ->(data) { data.present? }
  end
end
```

## End-to-End Testing with Capybara

```ruby
# spec/system/users_spec.rb
require 'rails_helper'

RSpec.describe 'Users', type: :system do
  before do
    driven_by(:selenium_chrome_headless)
  end

  it 'creates a new user' do
    visit new_user_path

    fill_in 'Name', with: 'John Doe'
    fill_in 'Email', with: 'john@example.com'
    fill_in 'Password', with: 'password123'
    click_button 'Create User'

    expect(page).to have_content('User created successfully')
    expect(page).to have_content('John Doe')
  end

  it 'shows validation errors' do
    visit new_user_path

    fill_in 'Name', with: ''
    click_button 'Create User'

    expect(page).to have_content("Name can't be blank")
  end

  it 'navigates without full page reload' do
    visit users_path

    # Capture initial page load marker
    page.execute_script("window.initialPageLoad = true")

    click_link 'New User'

    # Still on same page load (SPA navigation)
    expect(page.evaluate_script("window.initialPageLoad")).to be true
    expect(page).to have_current_path(new_user_path)
  end
end
```

## Client-Side Component Testing

### Vitest/Jest Setup for Vue

```javascript
// vitest.config.js
import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  test: {
    environment: 'jsdom',
    globals: true,
  },
})
```

### Testing Vue Components

```javascript
// tests/pages/users/index.test.js
import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import UsersIndex from '@/pages/users/index.vue'

describe('UsersIndex', () => {
  it('renders users list', () => {
    const wrapper = mount(UsersIndex, {
      props: {
        users: [
          { id: 1, name: 'John' },
          { id: 2, name: 'Jane' },
        ],
      },
    })

    expect(wrapper.text()).toContain('John')
    expect(wrapper.text()).toContain('Jane')
  })

  it('shows empty state when no users', () => {
    const wrapper = mount(UsersIndex, {
      props: { users: [] },
    })

    expect(wrapper.text()).toContain('No users found')
  })
})
```

### Testing React Components

```javascript
// tests/pages/users/index.test.jsx
import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import UsersIndex from '@/pages/users/index'

describe('UsersIndex', () => {
  it('renders users list', () => {
    render(
      <UsersIndex
        users={[
          { id: 1, name: 'John' },
          { id: 2, name: 'Jane' },
        ]}
      />
    )

    expect(screen.getByText('John')).toBeInTheDocument()
    expect(screen.getByText('Jane')).toBeInTheDocument()
  })
})
```

## Testing Best Practices

### 1. Test Response Structure, Not Implementation

```ruby
# Good - tests the contract
expect(inertia).to have_props(
  user: hash_including(:id, :name, :email)
)

# Avoid - too coupled to implementation
expect(inertia.props[:user]).to eq(user.as_json)
```

### 2. Use Factories for Test Data

```ruby
# spec/factories/users.rb
FactoryBot.define do
  factory :user do
    name { Faker::Name.name }
    email { Faker::Internet.email }
    password { 'password123' }
  end
end
```

### 3. Test Authorization Results

```ruby
it 'includes permission data' do
  get users_path

  expect(inertia).to have_props(
    can: hash_including(
      create_user: be_in([true, false])
    )
  )
end
```

### 4. Test Error States

```ruby
it 'handles not found' do
  get user_path(id: 'nonexistent')

  expect(response).to have_http_status(:not_found)
end
```

### 5. Use Shared Examples for Common Patterns

```ruby
RSpec.shared_examples 'requires authentication' do
  it 'redirects to login' do
    expect(response).to redirect_to(login_url)
  end
end

describe 'GET /admin/users' do
  context 'when not logged in' do
    before { get admin_users_path }
    it_behaves_like 'requires authentication'
  end
end
```
