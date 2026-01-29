---
name: inertia-rails-forms
description: Build forms in Inertia Rails applications with proper validation, file uploads, and error handling. Use when implementing forms, handling validation errors, or working with file uploads in Inertia.js with Rails.
license: MIT
metadata:
  author: community
  version: "1.0.0"
user-invocable: true
---

# Inertia Rails Forms

Comprehensive guide to building forms in Inertia Rails applications with React, Vue, or Svelte.

## The useForm Helper

The `useForm` helper provides reactive form state management with built-in features for validation, file uploads, and submission handling.

### React

```jsx
import { useForm } from '@inertiajs/react'

export default function CreateUser() {
  const { data, setData, post, processing, errors, reset } = useForm({
    name: '',
    email: '',
    password: '',
    avatar: null,
  })

  function submit(e) {
    e.preventDefault()
    post('/users', {
      onSuccess: () => reset('password'),
      preserveScroll: true,
    })
  }

  return (
    <form onSubmit={submit}>
      <div>
        <label>Name</label>
        <input
          type="text"
          value={data.name}
          onChange={(e) => setData('name', e.target.value)}
        />
        {errors.name && <span className="error">{errors.name}</span>}
      </div>

      <div>
        <label>Email</label>
        <input
          type="email"
          value={data.email}
          onChange={(e) => setData('email', e.target.value)}
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
        {errors.password && <span className="error">{errors.password}</span>}
      </div>

      <div>
        <label>Avatar</label>
        <input
          type="file"
          onChange={(e) => setData('avatar', e.target.files[0])}
        />
      </div>

      <button type="submit" disabled={processing}>
        {processing ? 'Creating...' : 'Create User'}
      </button>
    </form>
  )
}
```

### Vue 3

```vue
<script setup>
import { useForm } from '@inertiajs/vue3'

const form = useForm({
  name: '',
  email: '',
  password: '',
  avatar: null,
})

function submit() {
  form.post('/users', {
    onSuccess: () => form.reset('password'),
    preserveScroll: true,
  })
}
</script>

<template>
  <form @submit.prevent="submit">
    <div>
      <label>Name</label>
      <input v-model="form.name" type="text" />
      <span v-if="form.errors.name" class="error">{{ form.errors.name }}</span>
    </div>

    <div>
      <label>Email</label>
      <input v-model="form.email" type="email" />
      <span v-if="form.errors.email" class="error">{{ form.errors.email }}</span>
    </div>

    <div>
      <label>Password</label>
      <input v-model="form.password" type="password" />
      <span v-if="form.errors.password" class="error">{{ form.errors.password }}</span>
    </div>

    <div>
      <label>Avatar</label>
      <input type="file" @change="form.avatar = $event.target.files[0]" />
      <progress v-if="form.progress" :value="form.progress.percentage" max="100" />
    </div>

    <button type="submit" :disabled="form.processing">
      {{ form.processing ? 'Creating...' : 'Create User' }}
    </button>
  </form>
</template>
```

### Svelte

```svelte
<script>
import { useForm } from '@inertiajs/svelte'

let form = useForm({
  name: '',
  email: '',
  password: '',
  avatar: null,
})

function submit() {
  $form.post('/users', {
    onSuccess: () => $form.reset('password'),
    preserveScroll: true,
  })
}
</script>

<form on:submit|preventDefault={submit}>
  <div>
    <label>Name</label>
    <input type="text" bind:value={$form.name} />
    {#if $form.errors.name}
      <span class="error">{$form.errors.name}</span>
    {/if}
  </div>

  <div>
    <label>Email</label>
    <input type="email" bind:value={$form.email} />
    {#if $form.errors.email}
      <span class="error">{$form.errors.email}</span>
    {/if}
  </div>

  <div>
    <label>Password</label>
    <input type="password" bind:value={$form.password} />
  </div>

  <div>
    <label>Avatar</label>
    <input type="file" on:change={(e) => ($form.avatar = e.target.files[0])} />
  </div>

  <button type="submit" disabled={$form.processing}>
    {$form.processing ? 'Creating...' : 'Create User'}
  </button>
</form>
```

## Rails Controller Pattern

The standard pattern for handling form submissions:

```ruby
class UsersController < ApplicationController
  def new
    render inertia: {}
  end

  def create
    user = User.new(user_params)

    if user.save
      redirect_to users_url, notice: 'User created successfully!'
    else
      redirect_to new_user_url, inertia: { errors: user.errors }
    end
  end

  def edit
    user = User.find(params[:id])
    render inertia: { user: user.as_json(only: [:id, :name, :email]) }
  end

  def update
    user = User.find(params[:id])

    if user.update(user_params)
      redirect_to user_url(user), notice: 'User updated successfully!'
    else
      redirect_to edit_user_url(user), inertia: { errors: user.errors }
    end
  end

  private

  def user_params
    params.require(:user).permit(:name, :email, :password, :password_confirmation, :avatar)
  end
end
```

## useForm Properties and Methods

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `data` | Object | Current form data |
| `errors` | Object | Validation errors from server |
| `hasErrors` | Boolean | Whether errors exist |
| `processing` | Boolean | Whether form is submitting |
| `progress` | Object | File upload progress |
| `wasSuccessful` | Boolean | True after successful submission |
| `recentlySuccessful` | Boolean | True for 2 seconds after success |
| `isDirty` | Boolean | Whether form data has changed |

### Methods

| Method | Description |
|--------|-------------|
| `setData(key, value)` | Set a single field value |
| `setData(values)` | Set multiple field values |
| `reset()` | Reset all fields to initial values |
| `reset(...fields)` | Reset specific fields |
| `clearErrors()` | Clear all validation errors |
| `clearErrors(...fields)` | Clear specific field errors |
| `setError(field, message)` | Set a custom error |
| `setError(errors)` | Set multiple errors |
| `transform(callback)` | Transform data before submission |
| `defaults()` | Update default values for reset |
| `get(url, options)` | Submit GET request |
| `post(url, options)` | Submit POST request |
| `put(url, options)` | Submit PUT request |
| `patch(url, options)` | Submit PATCH request |
| `delete(url, options)` | Submit DELETE request |

### Submission Options

```javascript
form.post('/users', {
  // Preserve component state on validation errors
  preserveState: true,       // or 'errors' to preserve only on errors

  // Preserve scroll position
  preserveScroll: true,      // or 'errors' to preserve only on errors

  // Custom headers
  headers: { 'X-Custom': 'value' },

  // Force FormData even without files
  forceFormData: true,

  // Error bag for multiple forms on same page
  errorBag: 'createUser',

  // Event callbacks
  onBefore: (visit) => confirm('Submit form?'),
  onStart: (visit) => {},
  onProgress: (progress) => {},
  onSuccess: (page) => form.reset(),
  onError: (errors) => console.log(errors),
  onCancel: () => {},
  onFinish: () => {},
})
```

## File Uploads

Inertia automatically converts forms with files to `FormData`:

```javascript
const form = useForm({
  name: '',
  avatar: null,
  documents: [],  // Multiple files
})

// Single file
<input type="file" onChange={(e) => setData('avatar', e.target.files[0])} />

// Multiple files
<input
  type="file"
  multiple
  onChange={(e) => setData('documents', Array.from(e.target.files))}
/>
```

### Upload Progress

```vue
<template>
  <div v-if="form.progress">
    <progress :value="form.progress.percentage" max="100" />
    <span>{{ form.progress.percentage }}%</span>
  </div>
</template>
```

### File Uploads with PUT/PATCH

Some servers don't support multipart PUT/PATCH. Use method spoofing:

```javascript
// Instead of form.put()
form.post(`/users/${user.id}`, {
  _method: 'put',  // Rails recognizes this
})
```

## Nested Data

Use bracket notation for nested attributes:

```javascript
const form = useForm({
  user: {
    name: '',
    profile: {
      bio: '',
    },
  },
})

// Access errors
form.errors['user.name']
form.errors['user.profile.bio']
```

Or with Rails-style params:

```vue
<input name="user[name]" v-model="form.user.name" />
<input name="user[profile][bio]" v-model="form.user.profile.bio" />
```

## Multiple Forms on Same Page

Use error bags to isolate validation errors:

```javascript
// Login form
const loginForm = useForm({ email: '', password: '' })
loginForm.post('/login', { errorBag: 'login' })

// Register form
const registerForm = useForm({ name: '', email: '', password: '' })
registerForm.post('/register', { errorBag: 'register' })
```

Server-side:

```ruby
def create
  # ...
  redirect_to root_url, inertia: {
    errors: { login: { email: 'Invalid credentials' } }
  }
end
```

Access errors: `page.props.errors.login.email`

## Form Transforms

Transform data before submission:

```javascript
const form = useForm({
  first_name: 'John',
  last_name: 'Doe',
})

form
  .transform((data) => ({
    ...data,
    full_name: `${data.first_name} ${data.last_name}`,
  }))
  .post('/users')
```

## The Form Component (Declarative)

For simpler forms, use the Form component:

### Vue

```vue
<script setup>
import { Form } from '@inertiajs/vue3'
</script>

<template>
  <Form action="/users" method="post" v-slot="{ errors, processing }">
    <input type="text" name="name" />
    <span v-if="errors.name">{{ errors.name }}</span>

    <input type="email" name="email" />
    <span v-if="errors.email">{{ errors.email }}</span>

    <button type="submit" :disabled="processing">
      Submit
    </button>
  </Form>
</template>
```

### React

```jsx
import { Form } from '@inertiajs/react'

export default function CreateUser() {
  return (
    <Form action="/users" method="post">
      {({ errors, processing }) => (
        <>
          <input type="text" name="name" />
          {errors.name && <span>{errors.name}</span>}

          <input type="email" name="email" />
          {errors.email && <span>{errors.email}</span>}

          <button type="submit" disabled={processing}>
            Submit
          </button>
        </>
      )}
    </Form>
  )
}
```

## Remembering Form State

Preserve form data across browser history navigation using `useRemember`.

### The useRemember Hook

```javascript
import { useRemember } from '@inertiajs/vue3'

// Form state persists across back/forward navigation
const form = useRemember({
  name: '',
  email: '',
  message: '',
})
```

### Multiple Components on Same Page

Provide a unique key when multiple components use remember:

```javascript
// Contact form
const contactForm = useRemember({
  email: '',
  message: '',
}, 'ContactForm')

// Newsletter form
const newsletterForm = useRemember({
  email: '',
}, 'NewsletterForm')
```

### With useForm Helper

The form helper has built-in remember support:

```javascript
// Pass a unique key as first argument
const form = useForm('CreateUser', {
  name: '',
  email: '',
  password: '',
})

// For edit forms, include the ID for uniqueness
const form = useForm(`EditUser:${props.user.id}`, {
  name: props.user.name,
  email: props.user.email,
})
```

### Manual State Management

```javascript
import { router } from '@inertiajs/vue3'

// Save state manually
router.remember({ step: 2, selections: ['a', 'b'] }, 'wizard-state')

// Restore state
const savedState = router.restore('wizard-state')
if (savedState) {
  // Restore component state from savedState
}
```

### React Example

```jsx
import { useRemember } from '@inertiajs/react'

export default function ContactForm() {
  const [form, setForm] = useRemember({
    name: '',
    email: '',
    message: '',
  }, 'ContactForm')

  return (
    <form>
      <input
        value={form.name}
        onChange={(e) => setForm({ ...form, name: e.target.value })}
      />
      {/* ... */}
    </form>
  )
}
```

## Best Practices

### 1. Always Use the PRG Pattern

```ruby
# Incorrect - renders on POST
def create
  @user = User.create(user_params)
  render inertia: { user: @user }
end

# Correct - redirect after action
def create
  user = User.create(user_params)
  redirect_to user_url(user)
end
```

### 2. Return Minimal Error Data

```ruby
# Only include field errors, not full model
redirect_to new_user_url, inertia: { errors: user.errors.to_hash }
```

### 3. Handle Validation on Client and Server

```javascript
// Client-side for UX
const validateEmail = (email) => {
  if (!email.includes('@')) {
    form.setError('email', 'Invalid email format')
    return false
  }
  return true
}

function submit() {
  if (validateEmail(form.email)) {
    form.post('/users')  // Server validates too
  }
}
```

### 4. Preserve Scroll on Errors

```javascript
form.post('/users', {
  preserveScroll: 'errors',  // Only preserve on validation errors
})
```

### 5. Reset Sensitive Fields on Success

```javascript
form.post('/users', {
  onSuccess: () => form.reset('password', 'password_confirmation'),
})
```

### 6. Show Loading State

```vue
<button type="submit" :disabled="form.processing">
  <span v-if="form.processing">
    <Spinner /> Saving...
  </span>
  <span v-else>Save</span>
</button>
```

### 7. Confirm Destructive Actions

```javascript
function deleteUser() {
  if (confirm('Are you sure?')) {
    router.delete(`/users/${user.id}`)
  }
}
```
