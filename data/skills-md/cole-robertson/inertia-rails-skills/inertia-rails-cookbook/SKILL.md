---
name: inertia-rails-cookbook
description: Recipes and patterns for common Inertia Rails use cases. Includes modal dialogs, shadcn/ui integration, search with filters, wizard flows, and other advanced patterns.
license: MIT
metadata:
  author: community
  version: "1.0.0"
user-invocable: true
---

# Inertia Rails Cookbook

Practical recipes for common patterns and integrations in Inertia Rails applications.

## Working with the Official Starter Kits

The official starter kits provide a complete foundation. Here's how to customize them for your needs.

### Starter Kit Structure (React)

```
app/
├── controllers/
│   ├── application_controller.rb    # Shared data setup
│   ├── dashboard_controller.rb      # Example authenticated page
│   ├── home_controller.rb           # Public landing page
│   ├── sessions_controller.rb       # Login/logout
│   ├── users_controller.rb          # Registration
│   ├── identity/                    # Password reset
│   └── settings/                    # User settings
├── frontend/
│   ├── components/
│   │   ├── ui/                      # shadcn/ui components
│   │   ├── nav-main.tsx             # Main navigation
│   │   ├── app-sidebar.tsx          # Sidebar component
│   │   └── user-menu-content.tsx    # User dropdown
│   ├── hooks/
│   │   ├── use-flash.tsx            # Flash message hook
│   │   └── use-appearance.tsx       # Dark mode hook
│   ├── layouts/
│   │   ├── app-layout.tsx           # Main app layout
│   │   ├── auth-layout.tsx          # Auth pages layout
│   │   └── app/
│   │       ├── app-sidebar-layout.tsx
│   │       └── app-header-layout.tsx
│   ├── pages/
│   │   ├── dashboard/index.tsx      # Dashboard page
│   │   ├── home/index.tsx           # Landing page
│   │   ├── sessions/new.tsx         # Login page
│   │   ├── users/new.tsx            # Registration page
│   │   └── settings/                # Settings pages
│   └── types/
│       └── index.ts                 # Shared TypeScript types
```

### Adding a New Resource

**1. Generate the controller:**
```bash
bin/rails generate controller Products index show new create edit update destroy
```

**2. Create the page components:**

```tsx
// app/frontend/pages/products/index.tsx
import { Head, Link } from '@inertiajs/react'
import AppLayout from '@/layouts/app-layout'
import { Button } from '@/components/ui/button'
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow
} from '@/components/ui/table'

interface Product {
  id: number
  name: string
  price: number
}

interface Props {
  products: Product[]
}

export default function ProductsIndex({ products }: Props) {
  return (
    <AppLayout>
      <Head title="Products" />

      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Products</h1>
        <Button asChild>
          <Link href="/products/new">Add Product</Link>
        </Button>
      </div>

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Name</TableHead>
            <TableHead>Price</TableHead>
            <TableHead>Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {products.map((product) => (
            <TableRow key={product.id}>
              <TableCell>{product.name}</TableCell>
              <TableCell>${product.price}</TableCell>
              <TableCell>
                <Link href={`/products/${product.id}/edit`}>Edit</Link>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </AppLayout>
  )
}
```

**3. Update navigation:**

```tsx
// app/frontend/components/nav-main.tsx
const navItems = [
  { title: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { title: 'Products', href: '/products', icon: Package },  // Add this
  // ...
]
```

**4. Add route:**
```ruby
# config/routes.rb
resources :products
```

### Adding New shadcn/ui Components

The starter kit includes many components, but you can add more:

```bash
# Add a specific component
npx shadcn@latest add toast
npx shadcn@latest add calendar
npx shadcn@latest add data-table

# See all available components
npx shadcn@latest add
```

### Customizing the Layout

**Switch between sidebar and header layouts:**

```tsx
// app/frontend/layouts/app-layout.tsx
import AppSidebarLayout from '@/layouts/app/app-sidebar-layout'
import AppHeaderLayout from '@/layouts/app/app-header-layout'

// Use sidebar (default)
export default function AppLayout({ children }: Props) {
  return <AppSidebarLayout>{children}</AppSidebarLayout>
}

// Or use header layout
export default function AppLayout({ children }: Props) {
  return <AppHeaderLayout>{children}</AppHeaderLayout>
}
```

### Extending Types

```tsx
// app/frontend/types/index.ts
export interface User {
  id: number
  name: string
  email: string
  avatar_url: string | null
}

// Add your own types
export interface Product {
  id: number
  name: string
  description: string
  price: number
  created_at: string
}

export interface PageProps {
  auth: {
    user: User | null
  }
  flash: {
    success?: string
    error?: string
  }
}
```

### Using the Flash Hook

The starter kit includes a flash message system with Sonner toasts:

```tsx
// Already set up in the layout, just use flash in your controller
class ProductsController < ApplicationController
  def create
    @product = Product.create(product_params)
    redirect_to products_path, notice: 'Product created!'
  end
end
```

The `use-flash` hook automatically displays flash messages as toasts.

### Removing Features You Don't Need

**Remove settings pages:**
```bash
rm -rf app/frontend/pages/settings
rm -rf app/controllers/settings
# Remove routes in config/routes.rb
```

**Remove authentication (for internal tools):**
```bash
rm -rf app/frontend/pages/sessions
rm -rf app/frontend/pages/users
rm -rf app/frontend/pages/identity
rm app/controllers/sessions_controller.rb
rm app/controllers/users_controller.rb
rm -rf app/controllers/identity
# Update routes and ApplicationController
```

---

## Inertia Modal - Render Pages as Dialogs

The `inertia_rails-contrib` gem and `@inertiaui/modal` package let you render any Inertia page as a modal dialog.

### Installation

```bash
# Ruby gem (optional, for base_url helper)
bundle add inertia_rails-contrib

# NPM package (Vue)
npm install @inertiaui/modal-vue

# NPM package (React)
npm install @inertiaui/modal-react
```

### Setup (Vue)

```javascript
// app/frontend/entrypoints/application.js
import { createInertiaApp } from '@inertiajs/vue3'
import { renderApp } from '@inertiaui/modal-vue'
import { createSSRApp, h } from 'vue'

createInertiaApp({
  resolve: (name) => pages[`../pages/${name}.vue`],
  setup({ el, App, props, plugin }) {
    createSSRApp({
      render: () => renderApp(App, props),  // Use renderApp
    })
      .use(plugin)
      .mount(el)
  },
})
```

### Tailwind Configuration

```javascript
// tailwind.config.js (v3)
module.exports = {
  content: [
    // ... your content paths
    './node_modules/@inertiaui/modal-vue/src/**/*.vue',
  ],
}
```

```css
/* For Tailwind v4 */
@import "tailwindcss";
@source '../../../node_modules/@inertiaui/modal-vue';
```

### Basic Usage

**Open a page as modal:**
```vue
<script setup>
import { ModalLink } from '@inertiaui/modal-vue'
</script>

<template>
  <ModalLink href="/users/create">
    Create User
  </ModalLink>
</template>
```

**Wrap page content in Modal:**
```vue
<!-- pages/users/create.vue -->
<script setup>
import { Modal } from '@inertiaui/modal-vue'

defineProps(['roles'])
</script>

<template>
  <Modal>
    <h2>Create User</h2>
    <UserForm :roles="roles" />
  </Modal>
</template>
```

### Modal with Base URL

Enable URL updates and browser history:

**Controller:**
```ruby
class UsersController < ApplicationController
  def create
    render inertia_modal: {
      roles: Role.all.as_json
    }, base_url: users_path
  end
end
```

**Link with navigation:**
```vue
<ModalLink href="/users/create" navigate>
  Create User
</ModalLink>
```

Now the URL changes to `/users/create` when opened, supports browser back button, and can be bookmarked.

### Slideover Variant

```vue
<template>
  <Modal slideover>
    <h2>User Details</h2>
    <!-- Content slides in from the side -->
  </Modal>
</template>
```

### Nested Modals

```vue
<template>
  <Modal>
    <h2>Edit User</h2>
    <UserForm />

    <!-- Open another modal from within -->
    <ModalLink href="/roles/create">
      Add New Role
    </ModalLink>
  </Modal>
</template>
```

### Closing Modals

```vue
<script setup>
import { Modal } from '@inertiaui/modal-vue'

const emit = defineEmits(['close'])
</script>

<template>
  <Modal @close="emit('close')">
    <button @click="emit('close')">Cancel</button>
  </Modal>
</template>
```

---

## Integrating shadcn/ui

Use shadcn/ui components with Inertia Rails for a polished UI.

### Setup (Vue)

```bash
# Initialize shadcn/ui
npx shadcn-vue@latest init

# Add components
npx shadcn-vue@latest add button input card form
```

### Form with shadcn/ui

```vue
<script setup>
import { useForm } from '@inertiajs/vue3'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

const form = useForm({
  email: '',
  password: '',
})

function submit() {
  form.post('/login')
}
</script>

<template>
  <Card class="w-[400px]">
    <CardHeader>
      <CardTitle>Login</CardTitle>
    </CardHeader>
    <CardContent>
      <form @submit.prevent="submit" class="space-y-4">
        <div class="space-y-2">
          <Label for="email">Email</Label>
          <Input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="you@example.com"
          />
          <p v-if="form.errors.email" class="text-sm text-red-500">
            {{ form.errors.email }}
          </p>
        </div>

        <div class="space-y-2">
          <Label for="password">Password</Label>
          <Input
            id="password"
            v-model="form.password"
            type="password"
          />
        </div>

        <Button type="submit" :disabled="form.processing" class="w-full">
          {{ form.processing ? 'Signing in...' : 'Sign in' }}
        </Button>
      </form>
    </CardContent>
  </Card>
</template>
```

### Data Table with Sorting and Filtering

```vue
<script setup>
import { router } from '@inertiajs/vue3'
import { ref, watch } from 'vue'
import { useDebounceFn } from '@vueuse/core'
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow
} from '@/components/ui/table'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'

const props = defineProps(['users', 'filters'])

const search = ref(props.filters.search || '')
const sort = ref(props.filters.sort || 'name')
const direction = ref(props.filters.direction || 'asc')

const debouncedSearch = useDebounceFn(() => {
  router.get('/users', {
    search: search.value,
    sort: sort.value,
    direction: direction.value,
  }, {
    preserveState: true,
    replace: true,
  })
}, 300)

watch(search, debouncedSearch)

function toggleSort(column) {
  if (sort.value === column) {
    direction.value = direction.value === 'asc' ? 'desc' : 'asc'
  } else {
    sort.value = column
    direction.value = 'asc'
  }
  debouncedSearch()
}
</script>

<template>
  <div class="space-y-4">
    <Input
      v-model="search"
      placeholder="Search users..."
      class="max-w-sm"
    />

    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>
            <Button variant="ghost" @click="toggleSort('name')">
              Name
              <span v-if="sort === 'name'">{{ direction === 'asc' ? '↑' : '↓' }}</span>
            </Button>
          </TableHead>
          <TableHead>
            <Button variant="ghost" @click="toggleSort('email')">
              Email
              <span v-if="sort === 'email'">{{ direction === 'asc' ? '↑' : '↓' }}</span>
            </Button>
          </TableHead>
          <TableHead>Actions</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        <TableRow v-for="user in users" :key="user.id">
          <TableCell>{{ user.name }}</TableCell>
          <TableCell>{{ user.email }}</TableCell>
          <TableCell>
            <Link :href="`/users/${user.id}/edit`">Edit</Link>
          </TableCell>
        </TableRow>
      </TableBody>
    </Table>
  </div>
</template>
```

---

## Search with Filters

### Controller

```ruby
class UsersController < ApplicationController
  def index
    users = User.all

    # Apply search
    if params[:search].present?
      users = users.where('name ILIKE ? OR email ILIKE ?',
        "%#{params[:search]}%", "%#{params[:search]}%")
    end

    # Apply filters
    users = users.where(role: params[:role]) if params[:role].present?
    users = users.where(active: params[:active]) if params[:active].present?

    # Apply sorting
    sort_column = %w[name email created_at].include?(params[:sort]) ? params[:sort] : 'name'
    sort_direction = params[:direction] == 'desc' ? 'desc' : 'asc'
    users = users.order("#{sort_column} #{sort_direction}")

    # Paginate
    users = users.page(params[:page]).per(20)

    render inertia: {
      users: users.as_json(only: [:id, :name, :email, :role, :active]),
      filters: {
        search: params[:search],
        role: params[:role],
        active: params[:active],
        sort: sort_column,
        direction: sort_direction,
      },
      pagination: {
        current_page: users.current_page,
        total_pages: users.total_pages,
        total_count: users.total_count,
      }
    }
  end
end
```

### Frontend with URL Sync

```vue
<script setup>
import { router } from '@inertiajs/vue3'
import { ref, watch } from 'vue'
import { useDebounceFn } from '@vueuse/core'

const props = defineProps(['users', 'filters', 'pagination'])

const search = ref(props.filters.search || '')
const role = ref(props.filters.role || '')
const active = ref(props.filters.active || '')

function applyFilters() {
  router.get('/users', {
    search: search.value || undefined,
    role: role.value || undefined,
    active: active.value || undefined,
  }, {
    preserveState: true,
    replace: true,
  })
}

const debouncedSearch = useDebounceFn(applyFilters, 300)
watch(search, debouncedSearch)

function clearFilters() {
  search.value = ''
  role.value = ''
  active.value = ''
  applyFilters()
}
</script>

<template>
  <div class="space-y-4">
    <div class="flex gap-4">
      <input v-model="search" placeholder="Search..." class="input" />

      <select v-model="role" @change="applyFilters" class="select">
        <option value="">All Roles</option>
        <option value="admin">Admin</option>
        <option value="user">User</option>
      </select>

      <select v-model="active" @change="applyFilters" class="select">
        <option value="">All Status</option>
        <option value="true">Active</option>
        <option value="false">Inactive</option>
      </select>

      <button @click="clearFilters">Clear</button>
    </div>

    <UserTable :users="users" />

    <Pagination :pagination="pagination" />
  </div>
</template>
```

---

## Multi-Step Wizard

### Controller

```ruby
class OnboardingController < ApplicationController
  def show
    step = params[:step]&.to_i || 1

    render inertia: "onboarding/step#{step}", props: {
      step: step,
      total_steps: 4,
      data: session[:onboarding] || {}
    }
  end

  def update
    step = params[:step].to_i

    # Merge step data into session
    session[:onboarding] ||= {}
    session[:onboarding].merge!(step_params.to_h)

    if step < 4
      redirect_to onboarding_path(step: step + 1)
    else
      # Complete onboarding
      User.create!(session[:onboarding])
      session.delete(:onboarding)
      redirect_to dashboard_path, notice: 'Welcome!'
    end
  end

  private

  def step_params
    case params[:step].to_i
    when 1 then params.permit(:name, :email)
    when 2 then params.permit(:company, :role)
    when 3 then params.permit(:preferences)
    when 4 then params.permit(:terms_accepted)
    end
  end
end
```

### Wizard Component

```vue
<script setup>
import { useForm, router } from '@inertiajs/vue3'

const props = defineProps(['step', 'total_steps', 'data'])

const form = useForm({
  ...props.data
})

function next() {
  form.post(`/onboarding?step=${props.step}`)
}

function back() {
  router.get(`/onboarding?step=${props.step - 1}`)
}
</script>

<template>
  <div>
    <!-- Progress indicator -->
    <div class="flex gap-2 mb-8">
      <div
        v-for="i in total_steps"
        :key="i"
        :class="[
          'w-8 h-8 rounded-full flex items-center justify-center',
          i <= step ? 'bg-blue-500 text-white' : 'bg-gray-200'
        ]"
      >
        {{ i }}
      </div>
    </div>

    <form @submit.prevent="next">
      <!-- Step content via slot -->
      <slot :form="form" />

      <div class="flex gap-4 mt-8">
        <button v-if="step > 1" type="button" @click="back">
          Back
        </button>
        <button type="submit" :disabled="form.processing">
          {{ step === total_steps ? 'Complete' : 'Next' }}
        </button>
      </div>
    </form>
  </div>
</template>
```

---

## Flash Messages with Toast

### Shared Data Setup

```ruby
# app/controllers/application_controller.rb
class ApplicationController < ActionController::Base
  inertia_share flash: -> {
    {
      success: flash.notice,
      error: flash.alert,
      info: flash[:info],
      warning: flash[:warning]
    }.compact
  }
end
```

### Toast Component (Vue)

```vue
<!-- components/FlashMessages.vue -->
<script setup>
import { usePage } from '@inertiajs/vue3'
import { watch, ref } from 'vue'

const page = usePage()
const toasts = ref([])

watch(() => page.props.flash, (flash) => {
  Object.entries(flash).forEach(([type, message]) => {
    if (message) {
      const id = Date.now()
      toasts.value.push({ id, type, message })

      setTimeout(() => {
        toasts.value = toasts.value.filter(t => t.id !== id)
      }, 5000)
    }
  })
}, { immediate: true })
</script>

<template>
  <div class="fixed top-4 right-4 space-y-2 z-50">
    <TransitionGroup name="toast">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="[
          'px-4 py-3 rounded-lg shadow-lg',
          {
            'bg-green-500 text-white': toast.type === 'success',
            'bg-red-500 text-white': toast.type === 'error',
            'bg-blue-500 text-white': toast.type === 'info',
            'bg-yellow-500 text-black': toast.type === 'warning',
          }
        ]"
      >
        {{ toast.message }}
      </div>
    </TransitionGroup>
  </div>
</template>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}
.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>
```

### Usage in Layout

```vue
<!-- layouts/AppLayout.vue -->
<script setup>
import FlashMessages from '@/components/FlashMessages.vue'
</script>

<template>
  <div>
    <FlashMessages />
    <nav><!-- ... --></nav>
    <main>
      <slot />
    </main>
  </div>
</template>
```

---

## Confirmation Dialogs

### Reusable Confirm Component

```vue
<!-- components/ConfirmDialog.vue -->
<script setup>
import { ref } from 'vue'

const isOpen = ref(false)
const resolvePromise = ref(null)
const options = ref({})

function confirm(opts = {}) {
  options.value = {
    title: 'Are you sure?',
    message: 'This action cannot be undone.',
    confirmText: 'Confirm',
    cancelText: 'Cancel',
    destructive: false,
    ...opts
  }
  isOpen.value = true

  return new Promise((resolve) => {
    resolvePromise.value = resolve
  })
}

function handleConfirm() {
  isOpen.value = false
  resolvePromise.value?.(true)
}

function handleCancel() {
  isOpen.value = false
  resolvePromise.value?.(false)
}

defineExpose({ confirm })
</script>

<template>
  <Teleport to="body">
    <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center">
      <div class="absolute inset-0 bg-black/50" @click="handleCancel" />
      <div class="relative bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h3 class="text-lg font-semibold">{{ options.title }}</h3>
        <p class="mt-2 text-gray-600">{{ options.message }}</p>
        <div class="mt-6 flex gap-3 justify-end">
          <button @click="handleCancel" class="btn-secondary">
            {{ options.cancelText }}
          </button>
          <button
            @click="handleConfirm"
            :class="options.destructive ? 'btn-danger' : 'btn-primary'"
          >
            {{ options.confirmText }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>
```

### Usage

```vue
<script setup>
import { ref } from 'vue'
import { router } from '@inertiajs/vue3'
import ConfirmDialog from '@/components/ConfirmDialog.vue'

const confirmDialog = ref(null)

async function deleteUser(user) {
  const confirmed = await confirmDialog.value.confirm({
    title: 'Delete User',
    message: `Are you sure you want to delete ${user.name}?`,
    confirmText: 'Delete',
    destructive: true,
  })

  if (confirmed) {
    router.delete(`/users/${user.id}`)
  }
}
</script>

<template>
  <div>
    <button @click="deleteUser(user)">Delete</button>
    <ConfirmDialog ref="confirmDialog" />
  </div>
</template>
```

---

## Handling Rails Validation Error Types

Rails returns different error formats. Handle them consistently:

```ruby
# Controller helper
def format_errors(model)
  model.errors.to_hash.transform_values { |messages| messages.first }
end

# Usage
redirect_to edit_user_url(user), inertia: { errors: format_errors(user) }
```

```javascript
// Frontend - errors are now { field: 'message' } format
form.errors.email  // "can't be blank"
```

### Nested Model Errors

```ruby
# For nested attributes
def format_nested_errors(model)
  errors = {}

  model.errors.each do |error|
    key = error.attribute.to_s.gsub('.', '_')
    errors[key] = error.message
  end

  errors
end
```

---

## Real-Time Features with ActionCable

### Setup Turbo Streams Alternative

```javascript
// channels/notifications_channel.js
import { router } from '@inertiajs/vue3'
import consumer from './consumer'

consumer.subscriptions.create('NotificationsChannel', {
  received(data) {
    if (data.reload) {
      router.reload({ only: ['notifications'] })
    }
  }
})
```

### Controller Broadcast

```ruby
class NotificationsController < ApplicationController
  def create
    notification = current_user.notifications.create!(notification_params)

    ActionCable.server.broadcast(
      "notifications_#{current_user.id}",
      { reload: true }
    )

    redirect_to notifications_path
  end
end
```

---

## File Downloads

### Triggering Downloads

```ruby
def download
  report = Report.find(params[:id])

  # Return download URL as prop
  render inertia: {
    download_url: rails_blob_path(report.file, disposition: 'attachment')
  }
end
```

```javascript
// Trigger download without navigation
function downloadFile(url) {
  window.location.href = url
}

// Or use inertia_location for non-Inertia responses
router.visit(url, { method: 'get' })
```

### External Redirect for Downloads

```ruby
def export
  # Generate file...
  inertia_location export_download_path(token: token)
end
```
