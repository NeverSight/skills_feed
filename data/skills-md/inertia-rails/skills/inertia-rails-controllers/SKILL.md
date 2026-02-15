---
name: inertia-rails-controllers
description: >-
  ALWAYS `render inertia: { key: data }` to pass data as props — instance variables are NOT auto-passed
  (only alba-inertia does that). Rails controller patterns for Inertia.js: render inertia, prop types
  (defer, optional, merge, scroll), shared data, flash, PRG redirects, validation errors. Use when
  writing controllers that load data, display records, or serve Inertia responses. CRITICAL: external
  URLs (Stripe/OAuth) MUST use inertia_location, NEVER redirect_to.
---

# Inertia Rails Controllers

Server-side patterns for Rails controllers serving Inertia responses.

**Before adding a prop, ask:**
- **Needed on every page?** → `inertia_share` in a base controller (`InertiaController`), not a per-action prop
- **Expensive to compute?** → `InertiaRails.defer` — page loads fast, data streams in after
- **Only needed on partial reload?** → `InertiaRails.optional` — skipped on initial load
- **Reference data that rarely changes?** → `InertiaRails.once` — cached across navigations

**NEVER:**
- Use `redirect_to` for external URLs (Stripe, OAuth, SSO) — it returns 302 but the Inertia client tries to parse the response as JSON, causing a broken redirect. Use `inertia_location` (returns 409 + `X-Inertia-Location` header).
- Use `errors.full_messages` for validation errors — it produces flat strings without field keys, so errors can't be mapped to the corresponding input fields on the frontend. Use `errors.to_hash(true)`.
- Use `inertia.defer`, `Inertia.defer`, or `inertia_rails.defer` — the correct syntax is `InertiaRails.defer { ... }`. All prop helpers are module methods on the `InertiaRails` constant.
- Assume instance variables are auto-passed as props — they are NOT (unless `alba-inertia` gem is configured). Every action that passes props to the frontend MUST call `render inertia: { key: data }`.
- Use `success`/`error` as flash keys without updating `config.flash_keys` — Rails defaults to `notice`/`alert`. Custom keys must be added to both the initializer config and the `FlashData` TypeScript type.

## Render Syntax

> **`default_render: true` TRAP:** This setting only auto-infers the component
> name from controller/action — it does **NOT** auto-pass instance variables as
> props. Writing `@posts = Post.all` in an action with `default_render: true`
> renders the correct component but sends **zero data** to the frontend.
> Instance variables are only auto-serialized as props when `alba-inertia` gem
> is configured — check `Gemfile` before relying on this. Without it, you MUST
> use `render inertia: { posts: data }` to pass any data to the page.
>
> Empty actions (`def index; end`) are correct ONLY for pages that need no data
> (e.g., a static dashboard page, a login form). If the action queries the
> database, it MUST call `render inertia:` with data.

| Situation | Syntax | Component path |
|-----------|--------|----------------|
| Action loads data | `render inertia: { users: data }` | Inferred from controller/action |
| Action loads NO data (static page) | Empty action or `render inertia: {}` | Inferred from controller/action |
| Rendering a different page | `render inertia: 'errors/show', props: { error: e }` | Explicit path |

**Rule of thumb:** If your action touches the database, it MUST call `render inertia:` with data.
If the action body is empty, the page receives only shared props (from `inertia_share`).

```ruby
# CORRECT — data passed as props
def index
  render inertia: { users: users_data, stats: InertiaRails.defer { ExpensiveQuery.run } }
end

# CORRECT — static page, no data needed
def index; end

# WRONG — @posts is NEVER sent to the frontend (without alba-inertia)
def index
  @posts = Post.all
end
```

> **Note:** If the project uses the `alba-inertia` gem (check `Gemfile`), instance
> variables are auto-serialized as props and explicit `render inertia:` is not needed.
> See the `alba-inertia` skill for that convention.

## Prop Types

**`InertiaRails.defer`** — NOT `inertia.defer`, NOT `Inertia.defer`. All prop helpers are module methods on `InertiaRails`.

| Type | Syntax | Behavior |
|------|--------|----------|
| Regular | `{ key: value }` | Always evaluated, always included |
| Lazy | `-> { expensive_value }` | Included on initial page render, lazily evaluated on partial reloads |
| Optional | `InertiaRails.optional { ... }` | Only evaluated on partial reload requesting it |
| Defer | `InertiaRails.defer { ... }` | Loaded after initial page render |
| Defer (grouped) | `InertiaRails.defer(group: 'name') { ... }` | Grouped deferred — fetched in parallel |
| Once | `InertiaRails.once { ... }` | Resolved once, remembered across navigations |
| Merge | `InertiaRails.merge { ... }` | Appended to existing array (infinite scroll) |
| Deep merge | `InertiaRails.deep_merge { ... }` | Deep merged into existing object |
| Always | `InertiaRails.always { ... }` | Included even in partial reloads |
| Scroll | `InertiaRails.scroll { ... }` | Scroll-aware prop for infinite scroll |

```ruby
def index
  render inertia: {
    filters: filter_params,
    messages: -> { messages_scope.as_json },
    stats: InertiaRails.defer { Dashboard.stats },
    chart: InertiaRails.defer(group: 'analytics') { Dashboard.chart },
    countries: InertiaRails.once { Country.pluck(:name, :code) },
    posts: InertiaRails.merge { @posts.as_json },
    csrf: InertiaRails.always { form_authenticity_token },
  }
end
```

### Deferred Props — Full Stack Example

Server defers slow data, client shows fallback then swaps in content:

```ruby
# Controller
def show
  render inertia: {
    basic_stats: Stats.quick_summary,
    analytics: InertiaRails.defer { Analytics.compute_slow },
  }
end
```

```tsx
// Page component — child reads deferred prop from page props
import { Deferred, usePage } from '@inertiajs/react'

export default function Dashboard({ basic_stats }: Props) {
  return (
    <>
      <QuickStats data={basic_stats} />
      <Deferred data="analytics" fallback={<div>Loading analytics...</div>}>
        <AnalyticsPanel />
      </Deferred>
    </>
  )
}

function AnalyticsPanel() {
  const { analytics } = usePage<{ analytics: Analytics }>().props
  return <div>{analytics.revenue}</div>
}
```

## Shared Data

Use `inertia_share` in controllers — it needs controller context (`current_user`,
request). The initializer only handles `config.*` settings (version, flash_keys).

```ruby
class ApplicationController < ActionController::Base
  # Static
  inertia_share app_name: 'MyApp'

  # Using lambdas (most common)
  inertia_share auth: -> { { user: current_user&.as_json(only: [:id, :name, :email, :role]) } }

  # Conditional
  inertia_share if: :user_signed_in? do
    { notifications: -> { current_user.unread_notifications_count } }
  end
end
```

Lambda and action-scoped variants are in [`references/configuration.md`](references/configuration.md).

**Evaluation order:** Multiple `inertia_share` calls merge top-down. If a child
controller shares the same key as a parent, the child's value wins. Block and lambda
shares are lazily evaluated per-request — they don't run for non-Inertia requests.

## Flash Messages

Flash is automatic. Configure exposed keys if needed:

```ruby
# config/initializers/inertia_rails.rb
InertiaRails.configure do |config|
  config.flash_keys = %i[notice alert toast] # default: %i[notice alert]
end
```

Use standard Rails flash in controllers:
```ruby
redirect_to users_path, notice: "User created!"
# or
flash.alert = "Something went wrong"
redirect_to users_path
```

## Redirects & Validation Errors

After create/update/delete, always redirect (Post-Redirect-Get). Standard Rails
`redirect_to` works. The Inertia-specific part is validation error handling:

```ruby
def create
  @user = User.new(user_params)
  if @user.save
    redirect_to users_path, notice: "Created!"
  else
    redirect_back_or_to new_user_path, inertia: { errors: @user.errors.to_hash(true) }
  end
end
```

**`to_hash` vs `to_hash(true)`:** `to_hash` gives `{ name: ["can't be blank"] }`,
`to_hash(true)` gives `{ name: ["Name can't be blank"] }`. Keys must match input
`name` attributes — mismatched keys mean errors won't display next to the right field.

**NEVER use `errors.full_messages`** — it produces flat strings without field keys,
so errors can't be mapped to the corresponding input fields on the frontend.

## Authorization as Props

Pass permissions as per-resource `can` hash — frontend controls visibility,
server enforces access. See `inertia-rails-controllers` + `inertia-rails-pages` skills.

**MANDATORY — READ ENTIRE FILE** when implementing authorization props:
[`references/authorization.md`](references/authorization.md) (~40 lines) — full-stack
`can` pattern with Action Policy/Pundit/CanCanCan examples.

**Do NOT load** if not passing permission data to the frontend.

## External Redirects (`inertia_location`)

**CRITICAL:** `redirect_to` for external URLs breaks Inertia — the client
receives a 302 but tries to handle it as an Inertia response (JSON), not a
full page redirect. `inertia_location` returns 409 with `X-Inertia-Location`
header, which tells the client to do `window.location = url`.

```ruby
# Stripe checkout — MUST use inertia_location, not redirect_to
def create
  checkout_session = Current.user.payment_processor.checkout(
    mode: "payment",
    line_items: "price_xxx",
    success_url: enrollments_url,
    cancel_url: course_url(@course),
  )
  inertia_location checkout_session.url
end
```

Use `inertia_location` for any URL outside the Inertia app: payment
providers, OAuth, external services.

## History Encryption

Encrypts page data in browser history state — `config.encrypt_history = Rails.env.production?`.
Use `redirect_to path, inertia: { clear_history: true }` on logout/role change.
Full setup with server-side and client-side examples is in
[`references/configuration.md`](references/configuration.md).

## Configuration

See [`references/configuration.md`](references/configuration.md) for all
`InertiaRails.configure` options (version, encrypt_history, flash_keys, etc.).

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| 302 loop on Stripe/OAuth redirect | `redirect_to` for external URL | Use `inertia_location` — it returns 409 + `X-Inertia-Location` header |
| Errors don't display next to fields | Error keys don't match input `name` | `to_hash` keys must match input `name` attributes exactly |
| TS2305: `postsPath` not found in `@/routes` | js-routes not regenerated after adding routes | Run `rails js_routes:generate` after changing `config/routes.rb` |

## Related Skills
- **Form error display** → `inertia-rails-forms`
- **Flash toast UI** → `inertia-rails-pages` (access) + `shadcn-inertia` (Sonner)
- **Deferred on client** → `inertia-rails-pages` (`<Deferred>` component)
- **Type-safe props** → `inertia-rails-typescript` or `alba-inertia` (serializers)
- **Testing** → `inertia-rails-testing`

## References

**MANDATORY — READ ENTIRE FILE** when using advanced prop types (`merge`,
`scroll`, `deep_merge`) or combining multiple prop options:
[`references/prop-types.md`](references/prop-types.md) (~180 lines) — detailed behavior,
edge cases, and combination rules for all prop types.

**Do NOT load** `prop-types.md` for basic `defer`, `optional`, `once`, or `always`
usage — the table above is sufficient.

Load [`references/configuration.md`](references/configuration.md) (~180 lines) only when
setting up `InertiaRails.configure` for the first time or debugging configuration
issues. **Do NOT load** for routine controller work.
