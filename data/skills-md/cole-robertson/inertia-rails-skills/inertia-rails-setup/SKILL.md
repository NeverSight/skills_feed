---
name: inertia-rails-setup
description: Set up a new Inertia Rails project or add Inertia to an existing Rails application. Use when creating new projects, configuring Inertia, or setting up the development environment with React, Vue, or Svelte.
license: MIT
metadata:
  author: community
  version: "1.0.0"
user-invocable: true
argument-hint: "[react|vue|svelte] [--typescript] [--tailwind]"
---

# Inertia Rails Setup

This skill helps you set up Inertia.js in a Ruby on Rails application with your choice of frontend framework.

## Recommended: Official Starter Kits

For new projects, the fastest way to get started is cloning an official starter kit. These include authentication, shadcn/ui components, TypeScript, and optional SSR support out of the box.

### React Starter Kit (Recommended)

```bash
git clone https://github.com/inertia-rails/react-starter-kit myapp
cd myapp
bin/setup
```

**Includes:**
- React 19 + TypeScript
- shadcn/ui component library (20+ components)
- User authentication (login, register, password reset)
- Settings pages (profile, password, email, sessions, appearance)
- Multiple layouts (sidebar, header, auth variants)
- Dark mode support
- Kamal deployment config
- Optional SSR support
- Flash messages with Sonner toasts

### Vue Starter Kit

```bash
git clone https://github.com/inertia-rails/vue-starter-kit myapp
cd myapp
bin/setup
```

### Svelte Starter Kit

```bash
git clone https://github.com/inertia-rails/svelte-starter-kit myapp
cd myapp
bin/setup
```

### Customizing the Starter Kit

After cloning:

1. **Rename the app:**
   ```bash
   # Update config/application.rb
   module YourAppName
     class Application < Rails::Application
   ```

2. **Update database config:**
   ```bash
   # Edit config/database.yml with your settings
   ```

3. **Remove example pages you don't need:**
   ```bash
   # Delete from app/frontend/pages/ and corresponding controllers
   ```

4. **Add your own pages:**
   ```bash
   bin/rails generate controller Products index show
   # Create app/frontend/pages/products/index.tsx
   ```

5. **Customize the layout:**
   - Edit `app/frontend/layouts/app-layout.tsx` for main app
   - Edit `app/frontend/components/nav-main.tsx` for navigation

---

## Alternative: Generator Setup

If you prefer starting from scratch or adding Inertia to an existing Rails app:

### Quick Setup

```bash
# Create new Rails app (if needed)
rails new myapp --skip-javascript

# Add inertia_rails gem
bundle add inertia_rails

# Run the generator
bin/rails generate inertia:install
```

The generator will prompt you to select:
- Frontend framework (React, Vue, or Svelte)
- TypeScript support
- Tailwind CSS integration

## Manual Setup Steps

### 1. Add the Gem

```ruby
# Gemfile
gem 'inertia_rails'
```

```bash
bundle install
```

### 2. Install Vite Rails (if not present)

```bash
bundle add vite_rails
bundle exec vite install
```

### 3. Configure the Root Layout

Create or update `app/views/layouts/application.html.erb`:

```erb
<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <%= csp_meta_tag %>
    <%= inertia_ssr_head %>
    <%= vite_client_tag %>
    <%= vite_javascript_tag 'application' %>
  </head>
  <body>
    <%= yield %>
  </body>
</html>
```

### 4. Install Frontend Dependencies

**For React:**
```bash
npm install @inertiajs/react react react-dom
```

**For Vue 3:**
```bash
npm install @inertiajs/vue3 vue
```

**For Svelte:**
```bash
npm install @inertiajs/svelte svelte
```

### 5. Configure the Frontend Entry Point

Create `app/frontend/entrypoints/application.js`:

**React:**
```javascript
import { createInertiaApp } from '@inertiajs/react'
import { createRoot } from 'react-dom/client'

createInertiaApp({
  resolve: (name) => {
    const pages = import.meta.glob('../pages/**/*.jsx', { eager: true })
    return pages[`../pages/${name}.jsx`]
  },
  setup({ el, App, props }) {
    createRoot(el).render(<App {...props} />)
  },
})
```

**Vue 3:**
```javascript
import { createApp, h } from 'vue'
import { createInertiaApp } from '@inertiajs/vue3'

createInertiaApp({
  resolve: (name) => {
    const pages = import.meta.glob('../pages/**/*.vue', { eager: true })
    return pages[`../pages/${name}.vue`]
  },
  setup({ el, App, props, plugin }) {
    createApp({ render: () => h(App, props) })
      .use(plugin)
      .mount(el)
  },
})
```

**Svelte:**
```javascript
import { createInertiaApp } from '@inertiajs/svelte'

createInertiaApp({
  resolve: (name) => {
    const pages = import.meta.glob('../pages/**/*.svelte', { eager: true })
    return pages[`../pages/${name}.svelte`]
  },
  setup({ el, App }) {
    new App({ target: el })
  },
})
```

### 6. Create the Pages Directory

```bash
mkdir -p app/frontend/pages
```

### 7. Configure the Initializer

Create `config/initializers/inertia_rails.rb`:

```ruby
# frozen_string_literal: true

InertiaRails.configure do |config|
  # Asset versioning - triggers full reload when assets change
  config.version = -> { ViteRuby.digest }

  # Flash keys exposed to frontend
  config.flash_keys = %i[notice alert]

  # Deep merge shared data with page props
  # config.deep_merge_shared_data = true

  # Encrypt history for sensitive data (requires HTTPS)
  # config.encrypt_history = Rails.env.production?
end
```

### 8. Set Up Shared Data

In `app/controllers/application_controller.rb`:

```ruby
class ApplicationController < ActionController::Base
  inertia_share do
    {
      flash: {
        notice: flash.notice,
        alert: flash.alert
      },
      auth: {
        user: current_user&.as_json(only: [:id, :name, :email])
      }
    }
  end
end
```

### 9. Create Your First Page

**Controller:**
```ruby
# app/controllers/home_controller.rb
class HomeController < ApplicationController
  def index
    render inertia: { message: 'Welcome to Inertia Rails!' }
  end
end
```

**Route:**
```ruby
# config/routes.rb
Rails.application.routes.draw do
  root 'home#index'
end
```

**Page Component (React):**
```jsx
// app/frontend/pages/home/index.jsx
export default function Home({ message }) {
  return (
    <div>
      <h1>{message}</h1>
    </div>
  )
}
```

**Page Component (Vue):**
```vue
<!-- app/frontend/pages/home/index.vue -->
<script setup>
defineProps(['message'])
</script>

<template>
  <div>
    <h1>{{ message }}</h1>
  </div>
</template>
```

### 10. Start the Development Servers

```bash
# Terminal 1: Rails server
bin/rails server

# Terminal 2: Vite dev server
bin/vite dev
```

## Configuration Options Reference

| Option | Default | Description |
|--------|---------|-------------|
| `version` | `nil` | Asset version for cache busting |
| `layout` | `'application'` | Default layout template |
| `flash_keys` | `[:notice, :alert]` | Flash keys to share |
| `deep_merge_shared_data` | `false` | Deep merge props |
| `encrypt_history` | `false` | Encrypt browser history |
| `ssr_enabled` | `false` | Enable SSR |
| `ssr_url` | `'http://localhost:13714'` | SSR server URL |
| `default_render` | `false` | Auto-render Inertia |
| `root_dom_id` | `'app'` | Root element ID |

## Environment Variables

All config options can be set via `INERTIA_` prefixed env vars:

```bash
INERTIA_SSR_ENABLED=true
INERTIA_ENCRYPT_HISTORY=true
```

## Troubleshooting

### "Cannot find module '@inertiajs/react'"
Run `npm install` to install dependencies.

### Blank page with no errors
Check browser console for JavaScript errors. Ensure Vite dev server is running.

### Props not updating
Ensure you're using `render inertia:` not `render json:`.

### CSRF token errors
Inertia handles CSRF automatically via Axios. Ensure `protect_from_forgery` is enabled.
