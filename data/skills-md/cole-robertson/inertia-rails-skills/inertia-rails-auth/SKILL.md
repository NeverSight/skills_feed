---
name: inertia-rails-auth
description: Implement authentication and authorization in Inertia Rails applications. Use when setting up login, sessions, permissions, and access control with Devise, has_secure_password, or other auth solutions.
license: MIT
metadata:
  author: community
  version: "1.0.0"
user-invocable: true
---

# Inertia Rails Authentication & Authorization

Guide to implementing authentication and authorization in Inertia Rails applications.

## Key Principle

Inertia uses your existing Rails authentication infrastructure. No special OAuth or token-based auth required. Since your frontend and backend share the same domain, session-based auth works seamlessly.

## Authentication with Devise

### Setup

```ruby
# Gemfile
gem 'devise'
```

```bash
bundle install
rails generate devise:install
rails generate devise User
rails db:migrate
```

### Share Authentication State

```ruby
# app/controllers/application_controller.rb
class ApplicationController < ActionController::Base
  inertia_share do
    {
      auth: {
        user: current_user&.as_json(only: [:id, :name, :email, :avatar_url]),
        signed_in: user_signed_in?
      }
    }
  end
end
```

### Create Login Page

```ruby
# app/controllers/sessions_controller.rb
class SessionsController < Devise::SessionsController
  def new
    render inertia: {}
  end

  def create
    self.resource = warden.authenticate(auth_options)

    if resource
      sign_in(resource_name, resource)
      redirect_to after_sign_in_path_for(resource), notice: 'Signed in successfully!'
    else
      redirect_to new_session_path(resource_name), inertia: {
        errors: { email: 'Invalid email or password' }
      }
    end
  end

  def destroy
    sign_out(resource_name)
    redirect_to root_path, notice: 'Signed out successfully!'
  end
end
```

### Login Component (Vue)

```vue
<!-- app/frontend/pages/sessions/new.vue -->
<script setup>
import { useForm, Link } from '@inertiajs/vue3'

const form = useForm({
  email: '',
  password: '',
  remember: false,
})

function submit() {
  form.post('/users/sign_in', {
    onSuccess: () => form.reset('password'),
  })
}
</script>

<template>
  <form @submit.prevent="submit">
    <h1>Sign In</h1>

    <div>
      <label>Email</label>
      <input v-model="form.email" type="email" autofocus />
      <span v-if="form.errors.email" class="error">{{ form.errors.email }}</span>
    </div>

    <div>
      <label>Password</label>
      <input v-model="form.password" type="password" />
    </div>

    <div>
      <label>
        <input v-model="form.remember" type="checkbox" />
        Remember me
      </label>
    </div>

    <button type="submit" :disabled="form.processing">
      {{ form.processing ? 'Signing in...' : 'Sign In' }}
    </button>

    <p>
      <Link href="/users/sign_up">Create an account</Link>
      <Link href="/users/password/new">Forgot password?</Link>
    </p>
  </form>
</template>
```

### Login Component (React)

```jsx
// app/frontend/pages/sessions/new.jsx
import { useForm, Link } from '@inertiajs/react'

export default function Login() {
  const { data, setData, post, processing, errors, reset } = useForm({
    email: '',
    password: '',
    remember: false,
  })

  function submit(e) {
    e.preventDefault()
    post('/users/sign_in', {
      onSuccess: () => reset('password'),
    })
  }

  return (
    <form onSubmit={submit}>
      <h1>Sign In</h1>

      <div>
        <label>Email</label>
        <input
          type="email"
          value={data.email}
          onChange={(e) => setData('email', e.target.value)}
          autoFocus
        />
        {errors.email && <span className="error">{errors.email}</span>}
      </div>

      <div>
        <label>Password</label>
        <input
          type="password"
          value={data.password}
          onChange={(e) => setData('password', e.target.value)}
        />
      </div>

      <div>
        <label>
          <input
            type="checkbox"
            checked={data.remember}
            onChange={(e) => setData('remember', e.target.checked)}
          />
          Remember me
        </label>
      </div>

      <button type="submit" disabled={processing}>
        {processing ? 'Signing in...' : 'Sign In'}
      </button>

      <p>
        <Link href="/users/sign_up">Create an account</Link>
        <Link href="/users/password/new">Forgot password?</Link>
      </p>
    </form>
  )
}
```

## Authentication with has_secure_password

### User Model

```ruby
# app/models/user.rb
class User < ApplicationRecord
  has_secure_password

  validates :email, presence: true, uniqueness: true
  validates :password, length: { minimum: 8 }, allow_nil: true
end
```

### Sessions Controller

```ruby
# app/controllers/sessions_controller.rb
class SessionsController < ApplicationController
  skip_before_action :authenticate!, only: [:new, :create]

  def new
    render inertia: {}
  end

  def create
    user = User.find_by(email: params[:email])

    if user&.authenticate(params[:password])
      session[:user_id] = user.id
      redirect_to dashboard_path, notice: 'Welcome back!'
    else
      redirect_to login_path, inertia: {
        errors: { email: 'Invalid email or password' }
      }
    end
  end

  def destroy
    session.delete(:user_id)
    redirect_to root_path, notice: 'Signed out successfully!'
  end
end

# Routes
# config/routes.rb
get 'login', to: 'sessions#new'
post 'login', to: 'sessions#create'
delete 'logout', to: 'sessions#destroy'
```

### Application Controller Helper

```ruby
# app/controllers/application_controller.rb
class ApplicationController < ActionController::Base
  before_action :authenticate!
  helper_method :current_user, :user_signed_in?

  inertia_share do
    {
      auth: {
        user: current_user&.as_json(only: [:id, :name, :email]),
        signed_in: user_signed_in?
      }
    }
  end

  private

  def current_user
    @current_user ||= User.find_by(id: session[:user_id])
  end

  def user_signed_in?
    current_user.present?
  end

  def authenticate!
    unless user_signed_in?
      redirect_to login_path, alert: 'Please sign in to continue'
    end
  end
end
```

## Authorization

### Passing Permissions as Props

Since frontend components can't access server-side authorization helpers, pass permission results as props:

```ruby
# app/controllers/users_controller.rb
class UsersController < ApplicationController
  def index
    render inertia: {
      can: {
        create_user: policy(User).create?
      },
      users: User.all.map do |user|
        serialize_user(user)
      end
    }
  end

  def show
    user = User.find(params[:id])

    render inertia: {
      user: serialize_user(user),
      can: {
        edit: policy(user).edit?,
        delete: policy(user).destroy?
      }
    }
  end

  private

  def serialize_user(user)
    user.as_json(only: [:id, :name, :email]).merge(
      can: {
        edit: policy(user).edit?,
        delete: policy(user).destroy?
      }
    )
  end
end
```

### Using Pundit

```ruby
# Gemfile
gem 'pundit'

# app/controllers/application_controller.rb
class ApplicationController < ActionController::Base
  include Pundit::Authorization

  rescue_from Pundit::NotAuthorizedError, with: :user_not_authorized

  private

  def user_not_authorized
    redirect_to root_path, alert: 'You are not authorized to perform this action'
  end
end

# app/policies/user_policy.rb
class UserPolicy < ApplicationPolicy
  def index?
    true
  end

  def show?
    true
  end

  def create?
    user.admin?
  end

  def update?
    user.admin? || record == user
  end

  def destroy?
    user.admin? && record != user
  end
end
```

### Using Action Policy

```ruby
# Gemfile
gem 'action_policy'

# app/controllers/users_controller.rb
class UsersController < ApplicationController
  def index
    render inertia: {
      can: {
        create_user: allowed_to?(:create?, User)
      },
      users: User.all.map do |user|
        user.as_json(only: [:id, :name]).merge(
          can: {
            edit: allowed_to?(:edit?, user),
            delete: allowed_to?(:destroy?, user)
          }
        )
      end
    }
  end
end
```

### Frontend Permission Checks (Vue)

```vue
<script setup>
import { Link, usePage } from '@inertiajs/vue3'

const props = defineProps(['users', 'can'])
const { auth } = usePage().props
</script>

<template>
  <div>
    <h1>Users</h1>

    <!-- Global permission -->
    <Link v-if="can.create_user" href="/users/new" class="btn">
      Create User
    </Link>

    <ul>
      <li v-for="user in users" :key="user.id">
        {{ user.name }}

        <!-- Per-record permissions -->
        <Link v-if="user.can.edit" :href="`/users/${user.id}/edit`">
          Edit
        </Link>

        <Link
          v-if="user.can.delete"
          :href="`/users/${user.id}`"
          method="delete"
          as="button"
        >
          Delete
        </Link>
      </li>
    </ul>
  </div>
</template>
```

### Frontend Permission Checks (React)

```jsx
import { Link, usePage } from '@inertiajs/react'

export default function UsersIndex({ users, can }) {
  const { auth } = usePage().props

  return (
    <div>
      <h1>Users</h1>

      {can.create_user && (
        <Link href="/users/new" className="btn">
          Create User
        </Link>
      )}

      <ul>
        {users.map((user) => (
          <li key={user.id}>
            {user.name}

            {user.can.edit && (
              <Link href={`/users/${user.id}/edit`}>Edit</Link>
            )}

            {user.can.delete && (
              <Link
                href={`/users/${user.id}`}
                method="delete"
                as="button"
              >
                Delete
              </Link>
            )}
          </li>
        ))}
      </ul>
    </div>
  )
}
```

## History Encryption

Prevent sensitive data exposure via browser back button after logout:

```ruby
# config/initializers/inertia_rails.rb
InertiaRails.configure do |config|
  # Enable globally
  config.encrypt_history = true
end

# Or per-controller for sensitive areas
class Admin::BaseController < ApplicationController
  inertia_config(encrypt_history: true)
end

# Or per-request
def show
  render inertia: { secret_data: data }, encrypt_history: true
end
```

### Clear History on Logout

```ruby
def destroy
  sign_out(current_user)

  # Clear encrypted history (rotates encryption key)
  redirect_to root_path, inertia: { clear_history: true }
end
```

Client-side:

```javascript
import { router } from '@inertiajs/vue3'

function logout() {
  router.clearHistory()
  router.post('/logout')
}
```

## Protected Routes

### Middleware Approach

```ruby
# app/controllers/application_controller.rb
class ApplicationController < ActionController::Base
  before_action :authenticate!

  private

  def authenticate!
    unless user_signed_in?
      redirect_to login_path, alert: 'Please sign in'
    end
  end
end

# Skip for public controllers
class PagesController < ApplicationController
  skip_before_action :authenticate!, only: [:home, :about]
end
```

### Role-Based Access

```ruby
class Admin::BaseController < ApplicationController
  before_action :require_admin!

  private

  def require_admin!
    unless current_user&.admin?
      redirect_to root_path, alert: 'Admin access required'
    end
  end
end
```

## CSRF Protection

Inertia handles CSRF automatically. Ensure Rails is configured:

```ruby
# app/controllers/application_controller.rb
class ApplicationController < ActionController::Base
  protect_from_forgery with: :exception
end
```

Axios (used by Inertia) automatically:
1. Reads `XSRF-TOKEN` cookie set by Rails
2. Sends `X-XSRF-TOKEN` header with requests

## Registration Flow

```ruby
# app/controllers/registrations_controller.rb
class RegistrationsController < ApplicationController
  skip_before_action :authenticate!

  def new
    render inertia: {}
  end

  def create
    user = User.new(user_params)

    if user.save
      session[:user_id] = user.id
      redirect_to dashboard_path, notice: 'Welcome!'
    else
      redirect_to register_path, inertia: { errors: user.errors }
    end
  end

  private

  def user_params
    params.require(:user).permit(:name, :email, :password, :password_confirmation)
  end
end
```

## Password Reset Flow

```ruby
# app/controllers/password_resets_controller.rb
class PasswordResetsController < ApplicationController
  skip_before_action :authenticate!

  def new
    render inertia: {}
  end

  def create
    user = User.find_by(email: params[:email])
    user&.send_password_reset_email

    # Always show success to prevent email enumeration
    redirect_to login_path, notice: 'Check your email for reset instructions'
  end

  def edit
    user = User.find_by(password_reset_token: params[:token])

    if user&.password_reset_valid?
      render inertia: { token: params[:token] }
    else
      redirect_to login_path, alert: 'Invalid or expired reset link'
    end
  end

  def update
    user = User.find_by(password_reset_token: params[:token])

    if user&.password_reset_valid? && user.update(password_params)
      user.clear_password_reset!
      session[:user_id] = user.id
      redirect_to dashboard_path, notice: 'Password updated!'
    else
      redirect_to edit_password_reset_path(token: params[:token]),
        inertia: { errors: user&.errors || { token: 'Invalid token' } }
    end
  end

  private

  def password_params
    params.permit(:password, :password_confirmation)
  end
end
```

## Best Practices

### 1. Never Trust Client-Side Auth Checks

Always verify permissions server-side:

```ruby
def destroy
  user = User.find(params[:id])
  authorize user  # Pundit/ActionPolicy check

  user.destroy
  redirect_to users_path
end
```

### 2. Minimize Exposed User Data

```ruby
# Bad
inertia_share auth: { user: current_user }

# Good
inertia_share auth: {
  user: current_user&.as_json(only: [:id, :name, :email])
}
```

### 3. Use Secure Session Configuration

```ruby
# config/initializers/session_store.rb
Rails.application.config.session_store :cookie_store,
  key: '_myapp_session',
  secure: Rails.env.production?,
  httponly: true,
  same_site: :lax
```

### 4. Handle Session Expiry Gracefully

```javascript
// Check auth state on each navigation
router.on('navigate', () => {
  const { auth } = usePage().props
  if (!auth.signed_in && requiresAuth(page.component)) {
    router.visit('/login')
  }
})
```

### 5. Implement Rate Limiting

```ruby
# Gemfile
gem 'rack-attack'

# config/initializers/rack_attack.rb
Rack::Attack.throttle('login attempts', limit: 5, period: 60) do |req|
  req.ip if req.path == '/login' && req.post?
end
```
