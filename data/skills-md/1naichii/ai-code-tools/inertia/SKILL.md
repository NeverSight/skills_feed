---
name: inertia
description: "Build modern monolith applications with Inertia.js - combining server-side frameworks (Laravel, Rails, etc.) with React/Vue/Svelte frontends without building APIs. Use when creating Inertia pages and layouts, working with Link component for navigation, building forms with Form component or useForm hook, handling validation and errors, managing shared data and props, implementing authentication and authorization, using manual visits with router, working with partial reloads, setting up persistent layouts, or configuring client-side setup."
---

# Inertia.js

Modern monolith framework for building SPAs without APIs. Combine server-side framework power with React/Vue/Svelte frontends.

## Core Concept

Inertia replaces your view layer - controllers return JavaScript page components instead of server-side templates. The `<Link>` component intercepts clicks for XHR visits, providing SPA experience without full page reloads.

## Quick Reference

### Basic Page Structure

```vue
<script setup>
import Layout from './Layout'
import { Head } from '@inertiajs/vue3'
defineProps({ user: Object })
</script>

<template>
    <Layout>
        <Head title="Welcome" />
        <h1>Welcome {{ user.name }}</h1>
    </Layout>
</template>
```

### Navigation

```vue
<Link href="/users">Users</Link>
<Link href="/logout" method="post" as="button">Logout</Link>
<Link href="/search" :data="{ query }" preserve-state>Search</Link>
```

### Form Submission

```vue
<!-- Simple Form Component -->
<Form action="/users" method="post">
    <input type="text" name="name" />
    <button type="submit">Create</button>
</Form>

<!-- useForm Hook -->
<script setup>
import { useForm } from '@inertiajs/vue3'
const form = useForm({ name: '', email: '' })
function submit() { form.post('/users') }
</script>
```

## Documentation by Topic

| Topic | Reference File | Description |
|-------|---------------|-------------|
| **Forms** | [forms.md](references/forms.md) | Form component, useForm helper, validation, error handling |
| **Links & Navigation** | [links.md](references/links.md) | Link component, manual visits, active states |
| **Validation** | [validation.md](references/validation.md) | Server-side validation, error bags, error display |
| **Pages & Layouts** | [pages-layouts.md](references/pages-layouts.md) | Page components, persistent layouts, default layouts |
| **Data & Props** | [data-props.md](references/data-props.md) | Shared data, partial reloads, deferred props |
| **Authentication** | [authentication.md](references/authentication.md) | Auth patterns, CSRF protection, authorization |
| **Setup** | [setup.md](references/setup.md) | Client-side initialization, server-side setup |
| **Advanced** | [advanced.md](references/advanced.md) | Events, error handling, scroll management, SSR |

## Common Patterns

### Displaying Validation Errors

```vue
<div v-if="errors.email">{{ errors.email }}</div>
```

### Accessing Shared Data

```vue
<script setup>
import { usePage } from '@inertiajs/vue3'
const page = usePage()
const user = computed(() => page.props.auth?.user)
</script>
```

### Preserving State/Scroll

```vue
<Link href="/form" preserve-state preserve-scroll>Edit</Link>
```

### Partial Reloads

```vue
<Link :only="['users']">Refresh Users</Link>
router.visit('/users', { only: ['users'] })
```

## Framework Support

- **Client:** Vue 3 (`@inertiajs/vue3`), React (`@inertiajs/react`), Svelte (`@inertiajs/svelte`)
- **Server:** Laravel (official), Rails, Phoenix, Symfony (community adapters)
