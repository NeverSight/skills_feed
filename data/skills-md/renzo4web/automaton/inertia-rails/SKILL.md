---
name: inertia-rails
description: Building full-stack applications with Inertia.js in Rails using React. Use when working with Inertia responses, forms, props, redirects, React page components, or Rails controllers in an Inertia project.
---

# Inertia Rails

## What is Inertia Rails

Inertia Rails is a hybrid approach that combines Rails server-side routing with React client-side views. It's not a traditional SPA (no client-side routing) and not traditional SSR (no server-side rendering).

**How it works:**

- Rails handles routing, controllers, authentication, data fetching
- React components replace ERB templates as the view layer
- Inertia intercepts link clicks and makes XHR requests
- Server returns JSON with component name and props instead of HTML
- Client dynamically swaps components without full page reload

**Component location:** `app/frontend/pages/ControllerName/ActionName.jsx`

---

## Responses & Props

### Basic Inertia Response

```ruby
# Automatic component resolution: users/show.jsx
def show
  user = User.find(params[:id])
  render inertia: { user: }
end
```

### Explicit Component Names

```ruby
def my_event
  event = Event.find(params[:id])
  render inertia: 'events/show', props: { event: }
end
```

### View Data for ERB Templates

```ruby
def show
  event = Event.find(params[:id])
  render inertia: { event: }, view_data: { meta: event.meta }
end
```

**⚠️ Security Warning:** All props are visible client-side. Never include sensitive data in props.

---

## Redirects

Always redirect after form submissions. Inertia automatically handles 303 responses.

```ruby
def create
  user = User.new(user_params)
  
  if user.save
    redirect_to users_url
  else
    redirect_to new_user_url, inertia: { errors: user.errors }
  end
end
```

### External Redirects

Use `inertia_location` for external URLs or non-Inertia endpoints:

```ruby
inertia_location external_service_url
```

---

## Forms

### Form Component

Use `<Form>` for simple forms that behave like HTML forms:

```jsx
import { Form } from '@inertiajs/react'

<Form action="/users" method="post">
  <input type="text" name="name" />
  <input type="email" name="email" />
  <button type="submit">Create User</button>
</Form>
```

**Key props:**

- `action`, `method`: Form endpoint
- `resetOnSuccess`: Reset form after successful submission
- `transform`: Modify data before submission
- `onSuccess`, `onError`: Event callbacks

**Slot props for state:**

```jsx
<Form action="/users" method="post">
  {({ errors, processing, wasSuccessful }) => (
    <>
      <input type="text" name="name" />
      {errors.name && <div>{errors.name}</div>}
      <button type="submit" disabled={processing}>
        {processing ? 'Creating...' : 'Create User'}
      </button>
      {wasSuccessful && <div>User created!</div>}
    </>
  )}
</Form>
```

### useForm Helper

Use `useForm` for programmatic control and complex forms:

```jsx
import { useForm } from '@inertiajs/react'

const { data, setData, post, processing, errors, reset } = useForm({
  name: '',
  email: '',
})

function submit(e) {
  e.preventDefault()
  post('/users', {
    onSuccess: () => reset('password'),
  })
}

return (
  <form onSubmit={submit}>
    <input
      value={data.name}
      onChange={(e) => setData('name', e.target.value)}
    />
    {errors.name && <div>{errors.name}</div>}
    <button type="submit" disabled={processing}>Submit</button>
  </form>
)
```

**Key methods:**

- `get`, `post`, `put`, `patch`, `delete`: Submit form
- `setData`: Update form data
- `reset`: Reset to default values
- `clearErrors`: Clear validation errors
- `setError`: Manually set errors

### Validation Errors

Rails automatically populates errors when validation fails:

```ruby
# Controller - errors automatically available in frontend
def create
  user = User.new(user_params)
  if user.save
    redirect_to users_url
  else
    redirect_to new_user_url, inertia: { errors: user.errors }
  end
end
```

---

## Deferred & Lazy Props

### Server-side Deferred Props

Use `InertiaRails.defer` for data that loads after initial render:

```ruby
def index
  render inertia: {
    users: -> { User.all },
    permissions: InertiaRails.defer { Permission.all },
  }
end
```

### Client-side Deferred Component

```jsx
import { Deferred } from '@inertiajs/react'

<Deferred data="permissions" fallback={<div>Loading...</div>}>
  <PermissionsComponent />
</Deferred>
```

### WhenVisible for Lazy Loading

```jsx
import { WhenVisible } from '@inertiajs/react'

<WhenVisible data="permissions" fallback={<div>Loading...</div>}>
  <PermissionsComponent />
</WhenVisible>
```

---

## Navigation

### Link Component

Replace `<a>` with `<Link>` for Inertia navigation:

```jsx
import { Link } from '@inertiajs/react'

<Link href="/users">Users</Link>
<Link href="/users/new" method="post" as="button">New User</Link>
```

### Programmatic Navigation

```jsx
import { router } from '@inertiajs/react'

router.visit('/users')
router.post('/users', data)
router.visit('/users', { only: ['users'] }) // Partial reload
```

---

## Flash Messages

### Setting Flash Messages

```ruby
def create
  user = User.new(user_params)
  if user.save
    redirect_to users_url, notice: 'User created successfully!'
  else
    redirect_to new_user_url, inertia: { 
      errors: user.errors,
      alert: 'Failed to create user'
    }
  end
end
```

### Accessing Flash Messages

Flash messages are automatically available as props:

```jsx
// In your layout or page component
export default function Layout({ children, flash }) {
  return (
    <div>
      {flash.notice && <div className="notice">{flash.notice}</div>}
      {flash.alert && <div className="alert">{flash.alert}</div>}
      {children}
    </div>
  )
}
```

---

## Routes

### Shorthand Routes

Route directly to components without controllers:

```ruby
# config/routes.rb
inertia 'dashboard' => 'Dashboard'
inertia :settings  # Maps to Settings component

namespace :admin do
  inertia 'dashboard' => 'Admin/Dashboard'
end

resources :users do
  inertia :activity, on: :member
end
```

### URL Generation

Generate URLs server-side and include as props:

```ruby
def index
  render inertia: {
    users: User.all.map { |user| 
      user.as_json(only: [:id, :name]).merge(edit_url: edit_user_path(user))
    },
    create_url: new_user_path
  }
end
```

---
