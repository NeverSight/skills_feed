---
name: inertia-rails-pages
description: >-
  Page components, persistent layouts, Link/router navigation, Head, Deferred, WhenVisible, InfiniteScroll,
  and URL-driven state for Inertia Rails. React examples inline; Vue and Svelte equivalents in references.
  Use when building pages, adding navigation, implementing persistent layouts, infinite scroll, lazy-loaded
  sections, or working with client-side Inertia APIs (router.reload, router.replaceProp, prefetching).
---

# Inertia Rails Pages

Page components, layouts, navigation, and client-side APIs.

**Before building a page, ask:**
- **Does this page need a layout?** → Use persistent layout (React: `Page.layout = ...`; Vue: `defineOptions({ layout })`; Svelte: module script export) — wrapping in JSX/template remounts on every navigation, losing scroll position, audio playback, and component state
- **Does UI state come from the URL?** → Change BOTH controller (read `params`, pass as prop) AND component (derive from prop, no `useState`/`useEffect`) — use `router.get` to update URL
- **Need to refresh data without navigation?** → `router.reload({ only: [...] })` — never `useEffect` + `fetch`
- **Need to update a prop without server round-trip?** → `router.replaceProp` — no fetch, no reload

**NEVER:**
- Parse `window.location.search` or use `useSearchParams` — derive URL state from controller props
- Use `useState`/`useEffect` to sync URL ↔ React state — the controller passes URL-derived data as props; the component just reads them
- Pass arguments to `<Deferred>` render function — `{(data) => ...}` does NOT work; child reads via `usePage()`
- Access `usePage().props.flash` — flash is top-level: `usePage().flash`
- Wrap layout in JSX return for persistence — use `Page.layout = ...` or global layout inside createInertiaApp's resolve callback

## Page Component Structure

Pages are default exports receiving controller props as function arguments.
Use `type Props = { ... }` (not `interface` — causes TS2344 in React). Vue uses `defineProps<T>()`, Svelte uses `let { ... } = $props()`.

```tsx
type Props = {
  posts: Post[]
}

export default function Index({ posts }: Props) {
  return <PostList posts={posts} />
}
```

## Persistent Layouts

Layouts persist across navigations — no remounting, preserving scroll, audio, etc.

```tsx
import { AppLayout } from '@/layouts/app-layout'

export default function Show({ course }: Props) {
  return <CourseContent course={course} />
}

// Single layout
Show.layout = (page: React.ReactNode) => <AppLayout>{page}</AppLayout>
```

Default layout in entrypoint:
```tsx
// app/frontend/entrypoints/inertia.tsx
resolve: async (name) => {
  const page = await pages[`../pages/${name}.tsx`]()
  page.default.layout ??= (page: React.ReactNode) => <AppLayout>{page}</AppLayout> // default if not set
  return page
}
```

## Navigation

### `<Link>` and `router`

Use `<Link href="...">` for internal navigation (not `<a>`) and `router.get/post/patch/delete`
for programmatic navigation. Key non-obvious features:

```tsx
// Prefetching — preloads page data on hover
<Link href="/users" prefetch>Users</Link>
<Link href="/users" prefetch cacheFor="30s">Users</Link>

// Prefetch with cache tags — invalidate after mutations
<Link href="/users" prefetch cacheTags="users">Users</Link>

// Programmatic prefetch (e.g., likely next destination)
router.prefetch('/settings', {}, { cacheFor: '1m' })

// Partial reload — refresh specific props without navigation
router.reload({ only: ['users'] })
```

Full `router` API, visit options, and event callbacks are in
`references/navigation.md` — see loading trigger below.

### Client-Side Prop Helpers

Update props without a server round-trip:

```tsx
// Replace a single prop (dot notation supported)
router.replaceProp('show_modal', false)
router.replaceProp('user.name', 'Jane Smith')

// With callback (receives current value + all props)
router.replaceProp('count', (current) => current + 1)

// Append/prepend to array props
router.appendToProp('messages', { id: 4, text: 'New' })
router.prependToProp('notifications', (current, props) => ({
  id: Date.now(),
  message: `Hello ${props.auth.user.name}`,
}))
```

These are shortcuts to `router.replace()` with `preserveScroll` and
`preserveState` automatically set to `true`.

**`router.replaceProp` vs `router.reload`:** Use `router.replaceProp` for client-only state changes
(toggling a modal, incrementing a counter) — no server round-trip. Use `router.reload`
when you need fresh data from the server (updated records, recalculated stats).

## URL-Driven State (Dialogs, Tabs, Filters)

URL state = server state = props. **ALWAYS implement both sides:**

1. **Controller** — read `params` and pass as a prop
2. **Component** — derive UI state from that prop (no `useState`, no `useEffect`)
3. **Update** — `router.get` with query params to change URL (triggers server round-trip, new props arrive)

**NEVER** use `useState` + `useEffect` to sync URL ↔ dialog/tab/filter state.
The server is the single source of truth — the component just reads props.

```ruby
# Step 1: Controller reads params, passes as prop
def index
  render inertia: {
    users: User.all,
    selected_user_id: params[:user_id]&.to_i
  }
end
```

```tsx
// Step 2+3: Derive state from props, router.get to update URL

type Props = {
  users: User[]
  selected_user_id: number | null  // from controller
}

export default function Index({ users, selected_user_id }: Props) {
  // Derive — no useState, no useEffect, no window.location parsing
  const selectedUser = selected_user_id
    ? users.find(u => u.id === selected_user_id)
    : null

  const openDialog = (id: number) =>
    router.get('/users', { user_id: id }, {
      preserveState: true,
      preserveScroll: true,
    })

  const closeDialog = () =>
    router.get('/users', {}, {
      preserveState: true,
      preserveScroll: true,
    })

  return (
    <Dialog open={!!selectedUser} onOpenChange={(open) => !open && closeDialog()}>
      <DialogContent>{/* ... */}</DialogContent>
    </Dialog>
  )
}
```

**Why not useEffect?** When `router.get('/users', { user_id: 5 })` fires, Inertia
makes a request to the server → controller runs with `params[:user_id] = 5` →
returns new props with `selected_user_id: 5` → component re-renders with the
dialog open. The cycle is: URL → server → props → render. Parsing
`window.location` client-side duplicates what the server already does.

## Shared Props

Shared props (auth, flash) are typed globally via InertiaConfig (see `inertia-rails-typescript` skill) — page components only type their OWN props:

```tsx
type Props = {
  users: User[]         // page-specific only
  // auth is NOT here — typed globally via InertiaConfig
}

export default function Index({ users }: Props) {
  const { props, flash } = usePage()
  // props.auth typed via InertiaConfig, flash.notice typed via InertiaConfig
  return <UserList users={users} />
}
```

## Flash Access

**Flash is top-level on the page object, NOT inside props** — this is the #1
flash mistake. Flash config is in `inertia-rails-controllers`; toast UI is in `shadcn-inertia`.

```tsx
// BAD:  usePage().props.flash   ← WRONG, flash is not in props
// GOOD: usePage().flash         ← flash.notice, flash.alert
```

## `<Deferred>` Component

Renders fallback until deferred props arrive. Children can be plain `ReactNode`
or `() => ReactNode` render function. Either way, the child reads the deferred
prop from page props via `usePage()` — the render function receives **no arguments**.

```tsx
import { Deferred } from '@inertiajs/react'

export default function Dashboard({ basic_stats }: Props) {
  return (
    <>
      <QuickStats data={basic_stats} />
      <Deferred data="detailed_stats" fallback={<Spinner />}>
        <DetailedStats />
      </Deferred>
    </>
  )
}

// Also valid — render function (no args, child still reads from usePage):
// <Deferred data="stats" fallback={<Spinner />}>
//   {() => <Stats />}
// </Deferred>

// BAD — render function does NOT receive data as argument:
// <Deferred data="stats">{(data) => <Stats data={data} />}</Deferred>
```

## `<InfiniteScroll>` Component

Automatic infinite scroll — loads next pages as user scrolls down. Pairs with
`InertiaRails.scroll` on the server (see `inertia-rails-controllers`):

```tsx
import { InfiniteScroll } from '@inertiajs/react'

export default function Index({ posts }: Props) {
  return (
    <InfiniteScroll data="posts" loading={() => <Spinner />}>
      {posts.map(post => <PostCard key={post.id} post={post} />)}
    </InfiniteScroll>
  )
}
```

Props: `data` (prop name), `loading` (fallback), `manual` (button instead of auto),
`manualAfter={3}` (auto for first 3 pages, then button), `preserveUrl` (don't update URL).

## `<WhenVisible>` Component

Loads data when element enters viewport. Use for **lazy sections** (comments,
related items), NOT for infinite scroll (use `<InfiniteScroll>` above):

```tsx
import { WhenVisible } from '@inertiajs/react'

<WhenVisible data="comments" fallback={<Spinner />}>
  <CommentsList />
</WhenVisible>
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Layout remounts on every navigation | Wrapping layout in JSX return instead of `Page.layout` | Use persistent layout |
| `Deferred` children never render | Render function expects args `{(data) => ...}` | Render function receives NO arguments — use `{() => <Child />}` or plain `<Child />`. Child reads prop via `usePage()` |
| Flash is `undefined` | Accessing `usePage().props.flash` | Flash is top-level: `usePage().flash`, not inside `props` |
| URL state lost on navigation | Parsing `window.location` in useEffect | Derive from props — controller reads `params` and passes as prop |
| `WhenVisible` never triggers | Element not in viewport or prop name wrong | `data` must match a prop name the controller provides on partial reload |
| Component state resets on `router.get` | Missing `preserveState: true` | Add `preserveState: true` to visit options for filter/sort/tab changes |
| Scroll jumps to top after form submit | Missing `preserveScroll` | Add `preserveScroll: true` to the visit or form options |

## Related Skills
- **Flash config** → `inertia-rails-controllers` (flash_keys)
- **Flash toast UI** → `shadcn-inertia` (Sonner + useFlash)
- **Shared props typing** → `inertia-rails-typescript` (InertiaConfig)
- **Deferred server-side** → `inertia-rails-controllers` (InertiaRails.defer)
- **URL-driven dialogs** → `shadcn-inertia` (Dialog component)

## Vue / Svelte

All examples above use React syntax. For Vue 3 or Svelte equivalents:

- **Vue 3**: [`references/vue.md`](references/vue.md) — `defineProps`, `usePage()` composable, scoped slots for `<Deferred>`/`<WhenVisible>`/`<InfiniteScroll>`, `defineOptions({ layout })` for persistent layouts
- **Svelte**: [`references/svelte.md`](references/svelte.md) — `$props()`, `$page` store, `{#snippet}` syntax for `<Deferred>`/`<WhenVisible>`/`<InfiniteScroll>`, `<svelte:head>` instead of `<Head>`, module script layout export

**MANDATORY — READ THE MATCHING FILE** when the project uses Vue or Svelte. The concepts and NEVER rules above apply to all frameworks, but code syntax differs.

## References

**MANDATORY — READ ENTIRE FILE** when implementing event callbacks (`onBefore`,
`onStart`, `onProgress`, `onFinish`, `onCancel`), client-side flash, or scroll
management:
[`references/navigation.md`](references/navigation.md) (~200 lines) — full callback
API, `router.flash()`, scroll regions, and history encryption.

**MANDATORY — READ ENTIRE FILE** when implementing nested layouts, conditional
layouts, or layout-level data sharing:
[`references/layouts.md`](references/layouts.md) (~180 lines) — nested layout patterns,
layout props, and default layout configuration.

**Do NOT load** references for basic `<Link>`, `router.visit`, or single-level
layout usage — the examples above are sufficient.
