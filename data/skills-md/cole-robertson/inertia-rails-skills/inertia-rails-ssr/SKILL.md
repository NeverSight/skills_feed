---
name: inertia-rails-ssr
description: Set up Server-Side Rendering (SSR) for Inertia Rails applications. Use when you need SEO optimization, faster initial page loads, or support for users with JavaScript disabled.
license: MIT
metadata:
  author: community
  version: "1.0.0"
user-invocable: true
---

# Inertia Rails Server-Side Rendering (SSR)

Server-Side Rendering pre-renders JavaScript pages on the server, delivering fully rendered HTML to visitors. This improves SEO, enables faster initial page loads, and allows basic navigation even with JavaScript disabled.

## When to Use SSR

- **SEO-critical pages** - Landing pages, blog posts, product pages
- **Social sharing** - Pages that need proper Open Graph meta tags
- **Slow connections** - Users see content before JavaScript loads
- **Accessibility** - Basic functionality without JavaScript

## Requirements

- **Node.js** must be available on your server
- **Vue 3.2.13+** (or install `@vue/server-renderer` separately for older versions)
- **Vite Ruby** for build configuration

## Setup Steps

### 1. Create SSR Entry Point

Create `app/frontend/ssr/ssr.js`:

**Vue 3:**
```javascript
import { createInertiaApp } from '@inertiajs/vue3'
import createServer from '@inertiajs/vue3/server'
import { renderToString } from '@vue/server-renderer'
import { createSSRApp, h } from 'vue'

const pages = import.meta.glob('../pages/**/*.vue', { eager: true })

createServer((page) =>
  createInertiaApp({
    page,
    render: renderToString,
    resolve: (name) => {
      const page = pages[`../pages/${name}.vue`]
      if (!page) {
        throw new Error(`Page not found: ${name}`)
      }
      return page
    },
    setup({ App, props, plugin }) {
      return createSSRApp({
        render: () => h(App, props),
      }).use(plugin)
    },
  })
)
```

**React:**
```javascript
import { createInertiaApp } from '@inertiajs/react'
import createServer from '@inertiajs/react/server'
import ReactDOMServer from 'react-dom/server'

const pages = import.meta.glob('../pages/**/*.jsx', { eager: true })

createServer((page) =>
  createInertiaApp({
    page,
    render: ReactDOMServer.renderToString,
    resolve: (name) => {
      const page = pages[`../pages/${name}.jsx`]
      if (!page) {
        throw new Error(`Page not found: ${name}`)
      }
      return page
    },
    setup: ({ App, props }) => <App {...props} />,
  })
)
```

### 2. Configure Vite Ruby

Update `config/vite.json`:

```json
{
  "all": {
    "sourceCodeDir": "app/frontend",
    "entrypointsDir": "entrypoints"
  },
  "development": {
    "autoBuild": true
  },
  "production": {
    "ssrBuildEnabled": true
  }
}
```

### 3. Enable SSR in Rails

Update `config/initializers/inertia_rails.rb`:

```ruby
InertiaRails.configure do |config|
  # Enable SSR only when Vite is configured for it
  config.ssr_enabled = ViteRuby.config.ssr_build_enabled

  # SSR server URL (default)
  config.ssr_url = 'http://localhost:13714'
end
```

### 4. Update Client Entry Point

Modify `app/frontend/entrypoints/application.js` for hydration:

**Vue 3:**
```javascript
import { createInertiaApp } from '@inertiajs/vue3'
import { createSSRApp, h } from 'vue'

const pages = import.meta.glob('../pages/**/*.vue', { eager: true })

createInertiaApp({
  resolve: (name) => pages[`../pages/${name}.vue`],
  setup({ el, App, props, plugin }) {
    // Use createSSRApp instead of createApp for hydration
    createSSRApp({
      render: () => h(App, props),
    })
      .use(plugin)
      .mount(el)
  },
})
```

**React:**
```javascript
import { createInertiaApp } from '@inertiajs/react'
import { hydrateRoot } from 'react-dom/client'

const pages = import.meta.glob('../pages/**/*.jsx', { eager: true })

createInertiaApp({
  resolve: (name) => pages[`../pages/${name}.jsx`],
  setup({ el, App, props }) {
    // Use hydrateRoot instead of createRoot for SSR
    hydrateRoot(el, <App {...props} />)
  },
})
```

### 5. Update Layout for SSR Head

Add SSR head injection to your layout:

```erb
<!-- app/views/layouts/application.html.erb -->
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
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

### 6. Build and Run

```bash
# Build both client and SSR bundles
bin/vite build
bin/vite build --ssr

# Start the SSR server
bin/vite ssr
```

## Production Deployment

### Process Manager (systemd)

Create `/etc/systemd/system/inertia-ssr.service`:

```ini
[Unit]
Description=Inertia SSR Server
After=network.target

[Service]
Type=simple
User=deploy
WorkingDirectory=/var/www/myapp/current
ExecStart=/usr/bin/node public/vite-ssr/ssr.js
Restart=on-failure
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable inertia-ssr
sudo systemctl start inertia-ssr
```

### Process Manager (PM2)

```bash
pm2 start public/vite-ssr/ssr.js --name inertia-ssr
pm2 save
```

### Docker

```dockerfile
# Run SSR server alongside Rails
CMD ["sh", "-c", "node public/vite-ssr/ssr.js & bundle exec puma"]
```

## Advanced Configuration

### Clustering

For better performance on multi-core systems (requires `@inertiajs/core` v2.0.7+):

```javascript
// ssr/ssr.js
createServer(
  (page) => createInertiaApp({ /* ... */ }),
  { cluster: true }  // Enable clustering
)
```

This runs multiple Node.js processes on a single port using round-robin request handling.

### Custom Port

```javascript
createServer(
  (page) => createInertiaApp({ /* ... */ }),
  { port: 13715 }  // Custom port
)
```

Update Rails config to match:

```ruby
config.ssr_url = 'http://localhost:13715'
```

### Conditional SSR

Enable SSR only for specific routes:

```ruby
class ApplicationController < ActionController::Base
  # Disable SSR for admin pages
  inertia_config(ssr_enabled: false)
end

class PagesController < ApplicationController
  # Enable SSR for public pages
  inertia_config(ssr_enabled: Rails.env.production?)
end
```

## Title and Meta Tags

### Server-Side Meta Tags

Set meta tags in your controller:

```ruby
class PostsController < ApplicationController
  def show
    post = Post.find(params[:id])

    render inertia: {
      post: post.as_json(only: [:id, :title, :content])
    }, meta: {
      title: post.title,
      description: post.excerpt,
      og_image: post.cover_image_url
    }
  end
end
```

### Using Head Component

**Vue 3:**
```vue
<script setup>
import { Head } from '@inertiajs/vue3'

defineProps(['post'])
</script>

<template>
  <Head>
    <title>{{ post.title }}</title>
    <meta name="description" :content="post.excerpt" />
    <meta property="og:title" :content="post.title" />
    <meta property="og:image" :content="post.coverImageUrl" />
  </Head>

  <article>
    <h1>{{ post.title }}</h1>
    <!-- ... -->
  </article>
</template>
```

**React:**
```jsx
import { Head } from '@inertiajs/react'

export default function Show({ post }) {
  return (
    <>
      <Head>
        <title>{post.title}</title>
        <meta name="description" content={post.excerpt} />
        <meta property="og:title" content={post.title} />
      </Head>

      <article>
        <h1>{post.title}</h1>
        {/* ... */}
      </article>
    </>
  )
}
```

### Default Title Template

```javascript
createInertiaApp({
  title: (title) => title ? `${title} - My App` : 'My App',
  // ...
})
```

## Troubleshooting

### SSR Server Not Responding

1. Check if the SSR server is running: `curl http://localhost:13714`
2. Check logs: `journalctl -u inertia-ssr -f`
3. Verify the port matches your Rails config

### Hydration Mismatch Errors

1. Ensure client and server render the same content
2. Avoid browser-only APIs in initial render (use `onMounted`)
3. Check for date/time formatting differences

```javascript
// Bad - different on server vs client
const time = new Date().toLocaleTimeString()

// Good - render after mount
const time = ref(null)
onMounted(() => {
  time.value = new Date().toLocaleTimeString()
})
```

### Memory Leaks

1. Avoid global state mutations in SSR
2. Use request-scoped state only
3. Monitor Node.js memory usage

### Missing Styles on Initial Load

Ensure CSS is included in the SSR bundle or use critical CSS extraction.

## Performance Tips

1. **Keep SSR lightweight** - Defer heavy computations to client
2. **Use streaming** (when supported) for faster TTFB
3. **Cache SSR responses** for static pages
4. **Monitor SSR latency** - Add observability

```ruby
# Log slow SSR renders
around_action :track_ssr_time, if: -> { request.inertia? }

def track_ssr_time
  start = Time.current
  yield
  duration = Time.current - start
  Rails.logger.info "SSR render: #{duration.round(3)}s" if duration > 0.1
end
```
