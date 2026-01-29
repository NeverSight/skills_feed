---
name: inertia-rails-performance
description: Optimize Inertia Rails application performance. Use when implementing code splitting, prefetching, deferred props, infinite scrolling, polling, or other performance optimizations.
license: MIT
metadata:
  author: community
  version: "1.0.0"
user-invocable: true
---

# Inertia Rails Performance Optimization

Comprehensive guide to optimizing Inertia Rails applications for speed and efficiency.

## Props Optimization

### Return Minimal Data

**Impact:** CRITICAL - Reduces payload size, improves security

```ruby
# Bad - sends entire model
render inertia: { users: User.all }

# Good - only required fields
render inertia: {
  users: User.all.as_json(only: [:id, :name, :email, :avatar_url])
}

# Better - use select to avoid loading unnecessary columns
render inertia: {
  users: User.select(:id, :name, :email, :avatar_url).as_json
}
```

### Lazy Evaluation with Lambdas

**Impact:** HIGH - Prevents unnecessary queries

```ruby
# Bad - evaluates even if not used
inertia_share do
  {
    recent_posts: Post.recent.limit(5).as_json,
    total_users: User.count
  }
end

# Good - only evaluates when accessed
inertia_share do
  {
    recent_posts: -> { Post.recent.limit(5).as_json },
    total_users: -> { User.count }
  }
end
```

## Deferred Props

Load non-critical data after initial page render:

```ruby
def dashboard
  render inertia: {
    # Critical data - loads immediately
    user: current_user.as_json(only: [:id, :name]),

    # Non-critical - loads after page renders
    analytics: InertiaRails.defer { Analytics.for_user(current_user) },

    # Group related deferred props (fetched in parallel)
    recommendations: InertiaRails.defer(group: 'suggestions') {
      Recommendations.for(current_user)
    },
    trending: InertiaRails.defer(group: 'suggestions') {
      Post.trending.limit(10).as_json
    },

    # Separate group - fetched in parallel with 'suggestions'
    notifications: InertiaRails.defer(group: 'alerts') {
      current_user.notifications.unread.as_json
    }
  }
end
```

### Frontend Handling

```vue
<script setup>
import { Deferred } from '@inertiajs/vue3'

defineProps(['user', 'analytics', 'recommendations'])
</script>

<template>
  <div>
    <!-- Immediate render -->
    <h1>Welcome, {{ user.name }}</h1>

    <!-- Shows loading state then content -->
    <Deferred data="analytics">
      <template #fallback>
        <AnalyticsSkeleton />
      </template>
      <AnalyticsChart :data="analytics" />
    </Deferred>

    <!-- Multiple deferred props -->
    <Deferred :data="['recommendations', 'trending']">
      <template #fallback>
        <RecommendationsSkeleton />
      </template>
      <RecommendationsList :items="recommendations" />
      <TrendingList :items="trending" />
    </Deferred>
  </div>
</template>
```

## Partial Reloads

Refresh only specific props without full page reload:

```javascript
import { router } from '@inertiajs/vue3'

// Reload only 'users' prop
router.reload({ only: ['users'] })

// Exclude specific props
router.reload({ except: ['analytics'] })

// With data parameters
router.reload({
  only: ['users'],
  data: { search: 'john', page: 2 }
})
```

### Server-Side Optimization

```ruby
def index
  render inertia: {
    # Standard prop - always included
    users: User.search(params[:search]).page(params[:page]).as_json,

    # Optional prop - only when explicitly requested
    statistics: InertiaRails.optional { compute_statistics },

    # Always prop - included even in partial reloads
    csrf_token: InertiaRails.always { form_authenticity_token }
  }
end
```

### Link with Partial Reload

```vue
<Link href="/users" :only="['users']">
  Refresh Users
</Link>

<Link href="/users?search=john" :only="['users']" preserve-state>
  Search John
</Link>
```

## Code Splitting

Split your bundle to load pages on demand:

### Vite (Recommended)

```javascript
// Lazy loading - loads pages on demand
const pages = import.meta.glob('../pages/**/*.vue')

createInertiaApp({
  resolve: (name) => {
    return pages[`../pages/${name}.vue`]()  // Note: returns Promise
  },
  // ...
})
```

### Eager Loading (Small Apps)

```javascript
// All pages in initial bundle - faster for small apps
const pages = import.meta.glob('../pages/**/*.vue', { eager: true })

createInertiaApp({
  resolve: (name) => pages[`../pages/${name}.vue`],
  // ...
})
```

### Hybrid Approach

```javascript
// Eager load critical pages, lazy load others
const criticalPages = import.meta.glob([
  '../pages/Home.vue',
  '../pages/Dashboard.vue',
], { eager: true })

const otherPages = import.meta.glob([
  '../pages/**/*.vue',
  '!../pages/Home.vue',
  '!../pages/Dashboard.vue',
])

createInertiaApp({
  resolve: (name) => {
    const page = criticalPages[`../pages/${name}.vue`]
    if (page) return page

    return otherPages[`../pages/${name}.vue`]()
  },
})
```

## Prefetching

Load pages before user navigates:

### Link Prefetching

```vue
<!-- Prefetch on hover (default: 75ms delay) -->
<Link href="/users" prefetch>Users</Link>

<!-- Prefetch immediately on mount -->
<Link href="/dashboard" prefetch="mount">Dashboard</Link>

<!-- Prefetch on mousedown -->
<Link href="/reports" prefetch="click">Reports</Link>

<!-- Multiple strategies -->
<Link href="/settings" :prefetch="['mount', 'hover']">Settings</Link>
```

### Cache Configuration

```vue
<!-- Cache for 1 minute -->
<Link href="/users" prefetch cache-for="1m">Users</Link>

<!-- Cache for 30 seconds, stale for 1 minute (stale-while-revalidate) -->
<Link href="/users" prefetch :cache-for="['30s', '1m']">Users</Link>
```

### Programmatic Prefetching

```javascript
import { router } from '@inertiajs/vue3'

// Prefetch a page
router.prefetch('/users')

// With options
router.prefetch('/users', {
  method: 'get',
  data: { page: 2 }
}, {
  cacheFor: '1m'
})
```

### Cache Tags for Invalidation

```vue
<Link href="/users" prefetch cache-tags="users">Users</Link>
<Link href="/users/active" prefetch cache-tags="users">Active Users</Link>

<!-- Form that invalidates user cache -->
<Form action="/users" method="post" invalidate-cache-tags="users">
  <!-- ... -->
</Form>
```

```javascript
// Manual invalidation
router.flushByCacheTags('users')

// Flush all prefetch cache
router.flushAll()
```

## Infinite Scrolling

Load more content without pagination:

### Server-Side

```ruby
def index
  posts = Post.order(created_at: :desc).page(params[:page]).per(20)

  render inertia: {
    posts: InertiaRails.merge { posts.as_json(only: [:id, :title, :excerpt]) },
    pagination: {
      current_page: posts.current_page,
      total_pages: posts.total_pages,
      has_more: !posts.last_page?
    }
  }
end
```

### Client-Side (Vue)

```vue
<script setup>
import { router } from '@inertiajs/vue3'
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps(['posts', 'pagination'])
const loading = ref(false)
const sentinel = ref(null)

function loadMore() {
  if (loading.value || !props.pagination.has_more) return

  loading.value = true
  router.reload({
    data: { page: props.pagination.current_page + 1 },
    only: ['posts', 'pagination'],
    preserveScroll: true,
    preserveState: true,
    onFinish: () => (loading.value = false),
  })
}

// Intersection Observer for automatic loading
let observer
onMounted(() => {
  observer = new IntersectionObserver(
    (entries) => {
      if (entries[0].isIntersecting) loadMore()
    },
    { rootMargin: '100px' }
  )
  if (sentinel.value) observer.observe(sentinel.value)
})

onUnmounted(() => observer?.disconnect())
</script>

<template>
  <div>
    <div v-for="post in posts" :key="post.id" class="post">
      <h2>{{ post.title }}</h2>
      <p>{{ post.excerpt }}</p>
    </div>

    <div ref="sentinel" class="h-4" />

    <div v-if="loading" class="text-center py-4">
      Loading more...
    </div>

    <div v-if="!pagination.has_more" class="text-center py-4 text-gray-500">
      No more posts
    </div>
  </div>
</template>
```

### Merge Options

```ruby
# Append to array (default)
InertiaRails.merge { items }

# Prepend to array
InertiaRails.merge(prepend: true) { items }

# Target specific key
InertiaRails.merge(append: 'data') { { data: items, meta: meta } }

# Update matching items instead of duplicating
InertiaRails.merge(match_on: 'id') { items }
```

## Polling

Real-time updates without WebSockets:

```vue
<script setup>
import { usePoll } from '@inertiajs/vue3'

// Poll every 5 seconds
usePoll(5000)

// With options
usePoll(5000, {
  only: ['notifications', 'messages'],
  onStart: () => console.log('Polling...'),
  onFinish: () => console.log('Poll complete'),
})

// Manual control
const { start, stop } = usePoll(5000, {}, { autoStart: false })

// Start polling when component becomes visible
const visible = usePageVisibility()
watch(visible, (isVisible) => {
  isVisible ? start() : stop()
})
</script>
```

### Throttling in Background

```javascript
// Default: 90% throttle in background tabs
usePoll(5000)

// Keep polling at full speed in background
usePoll(5000, {}, { keepAlive: true })
```

## Progress Indicators

### Default NProgress

```javascript
createInertiaApp({
  progress: {
    delay: 250,        // Show after 250ms (skip quick loads)
    color: '#29d',     // Progress bar color
    includeCSS: true,  // Include default styles
    showProgress: true // Show percentage
  },
})
```

### Disable for Specific Requests

```javascript
router.visit('/quick-action', {
  showProgress: false
})
```

### Async Requests

```javascript
// Background request without progress indicator
router.post('/analytics/track', { event: 'view' }, {
  async: true,
  showProgress: false
})

// Async with progress
router.post('/upload', formData, {
  async: true,
  showProgress: true
})
```

## Once Props

Data resolved once and remembered across navigations:

```ruby
inertia_share do
  {
    # Evaluated once per session, not on every navigation
    app_config: InertiaRails.once { AppConfig.to_json },
    feature_flags: InertiaRails.once { FeatureFlags.current }
  }
end
```

Combined with optional/deferred:

```ruby
render inertia: {
  # Optional + once: resolved only when requested, then remembered
  user_preferences: InertiaRails.optional(once: true) {
    current_user.preferences.as_json
  }
}
```

## Asset Versioning

Ensure users get fresh assets after deployment:

```ruby
# config/initializers/inertia_rails.rb
InertiaRails.configure do |config|
  # Using ViteRuby digest
  config.version = -> { ViteRuby.digest }

  # Or custom version
  config.version = -> { ENV['ASSET_VERSION'] || Rails.application.config.assets_version }
end
```

When version changes, Inertia triggers a full page reload instead of XHR.

## Database Query Optimization

### Eager Loading

```ruby
def index
  # Bad - N+1 queries
  users = User.all
  render inertia: {
    users: users.map { |u| u.as_json(include: :posts) }
  }

  # Good - eager load
  users = User.includes(:posts)
  render inertia: {
    users: users.as_json(include: { posts: { only: [:id, :title] } })
  }
end
```

### Selective Loading

```ruby
def index
  # Only select needed columns
  users = User
    .select(:id, :name, :email, :created_at)
    .includes(:profile)
    .order(created_at: :desc)
    .limit(50)

  render inertia: {
    users: users.as_json(
      only: [:id, :name, :email],
      include: { profile: { only: [:avatar_url] } }
    )
  }
end
```

## Caching Strategies

### Fragment Caching

```ruby
def index
  render inertia: {
    stats: Rails.cache.fetch('dashboard_stats', expires_in: 5.minutes) do
      compute_expensive_stats
    end
  }
end
```

### Response Caching with ETags

```ruby
def show
  user = User.find(params[:id])

  if stale?(user)
    render inertia: { user: user.as_json(only: [:id, :name]) }
  end
end
```

## Performance Monitoring

### Track Slow Requests

```ruby
# app/controllers/application_controller.rb
around_action :track_request_time

private

def track_request_time
  start = Time.current
  yield
  duration = Time.current - start

  if duration > 1.second
    Rails.logger.warn "Slow request: #{request.path} took #{duration.round(2)}s"
  end
end
```

### Client-Side Metrics

```javascript
router.on('start', (event) => {
  event.detail.visit.startTime = performance.now()
})

router.on('finish', (event) => {
  const duration = performance.now() - event.detail.visit.startTime
  if (duration > 1000) {
    console.warn(`Slow navigation to ${event.detail.visit.url}: ${duration}ms`)
  }
})
```

## WhenVisible - Lazy Load on Viewport Entry

Load data only when elements become visible using Intersection Observer:

### Basic Usage

```vue
<script setup>
import { WhenVisible } from '@inertiajs/vue3'

defineProps(['users', 'teams'])
</script>

<template>
  <div>
    <!-- Main content loads immediately -->
    <UserList :users="users" />

    <!-- Teams load when scrolled into view -->
    <WhenVisible data="teams">
      <template #fallback>
        <TeamsSkeleton />
      </template>
      <TeamList :teams="teams" />
    </WhenVisible>
  </div>
</template>
```

### Multiple Props

```vue
<WhenVisible :data="['teams', 'projects']">
  <template #fallback>
    <LoadingSpinner />
  </template>
  <Dashboard :teams="teams" :projects="projects" />
</WhenVisible>
```

### Configuration Options

```vue
<!-- Start loading 500px before element is visible -->
<WhenVisible data="comments" :buffer="500">
  <Comments :comments="comments" />
</WhenVisible>

<!-- Custom wrapper element -->
<WhenVisible data="stats" as="section">
  <Stats :stats="stats" />
</WhenVisible>

<!-- Reload every time element becomes visible (for infinite scroll) -->
<WhenVisible data="posts" always>
  <PostList :posts="posts" />
</WhenVisible>
```

### With Form Submissions

Prevent reloading WhenVisible props after form submission:

```javascript
form.post('/comments', {
  except: ['teams'],  // Don't reload teams managed by WhenVisible
})
```

## Scroll Management

### Scroll Preservation

```javascript
// Always preserve scroll position
router.visit('/users', { preserveScroll: true })

// Preserve only on validation errors
router.visit('/users', { preserveScroll: 'errors' })

// Conditional preservation
router.visit('/users', {
  preserveScroll: (page) => page.props.shouldPreserve
})
```

### Link with Scroll Control

```vue
<Link href="/users" preserve-scroll>Users</Link>
```

### Scroll Regions

For scrollable containers (not document body):

```vue
<template>
  <div class="h-screen flex">
    <!-- Sidebar with independent scroll -->
    <nav class="w-64 overflow-y-auto" scroll-region>
      <SidebarContent />
    </nav>

    <!-- Main content with independent scroll -->
    <main class="flex-1 overflow-y-auto" scroll-region>
      <slot />
    </main>
  </div>
</template>
```

Inertia tracks and restores scroll position for elements with `scroll-region` attribute.

### Reset Scroll Programmatically

```javascript
router.visit('/users', {
  preserveScroll: false,  // Reset to top (default)
})
```

## Best Practices Summary

1. **Props**: Return only necessary data, use lazy evaluation
2. **Deferred Props**: Move non-critical data to deferred loading
3. **Partial Reloads**: Refresh only changed data
4. **Code Splitting**: Lazy load pages for large applications
5. **Prefetching**: Preload likely next pages
6. **Infinite Scroll**: Use merge props for seamless pagination
7. **Polling**: Use sparingly with proper throttling
8. **Database**: Eager load associations, select only needed columns
9. **Caching**: Cache expensive computations
10. **Monitoring**: Track and optimize slow requests
11. **WhenVisible**: Lazy load below-the-fold content
12. **Scroll Regions**: Use for complex layouts with multiple scroll areas
