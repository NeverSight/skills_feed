---
name: inertia-rails-testing
description: >-
  Testing Inertia Rails responses with RSpec and Minitest: component assertions, prop matching, flash verification,
  deferred props, and partial reload helpers. Use when writing controller specs, request specs, or integration tests
  for Inertia pages. ALWAYS use matchers (render_component, have_props, have_flash), NOT direct access
  (inertia.component, inertia.props). CRITICAL: after POST/PATCH/DELETE with redirect, MUST call follow_redirect!
  before asserting flash or props — without it you're asserting against the 302, not the Inertia page.
  Setup: require 'inertia_rails/rspec'.
---

# Inertia Rails Testing

Testing patterns for Inertia responses with RSpec and Minitest.

**For each controller action, verify:**
- **Correct component** → `render_component('users/index')`
- **Expected props** → `have_props(users: satisfy { ... })`
- **No leaked data** → `have_no_prop(:secret)`
- **Flash messages** → `follow_redirect!` then `have_flash(notice: '...')`
- **Deferred props** → `have_deferred_props(:analytics)`

**Common mistake:** Forgetting `follow_redirect!` after PRG — without it, you're
asserting against the 302 redirect response, not the Inertia page that follows.

## Setup

```ruby
# spec/rails_helper.rb
require 'inertia_rails/rspec'
```

## RSpec Matchers

| Matcher | Purpose |
|---------|---------|
| `be_inertia_response` | Verify response is Inertia format |
| `render_component('path')` | Check rendered component name |
| `have_props(key: value)` | Partial props match |
| `have_exact_props(key: value)` | Exact props match |
| `have_no_prop(:key)` | Assert prop absent |
| `have_flash(key: value)` | Partial flash match |
| `have_exact_flash(key: value)` | Exact flash match |
| `have_no_flash(:key)` | Assert flash absent |
| `have_deferred_props(:key)` | Check deferred props exist |
| `have_view_data(key: value)` | Partial view_data match |

## RSpec Examples

**ALWAYS use matchers** (`render_component`, `have_props`, `have_flash`) instead of
direct property access (`inertia.component`, `inertia.props[:key]`):

```ruby
# BAD — direct property access:
# expect(inertia.component).to eq('users/index')
# expect(inertia.props[:users].length).to eq(3)

# GOOD — use matchers:
expect(inertia).to render_component('users/index')
expect(inertia).to have_props(users: satisfy { |u| u.length == 3 })
```

```ruby
# Key pattern: follow_redirect! after POST/PATCH/DELETE before asserting
it 'redirects with flash on success' do
  post users_path, params: { user: valid_params }

  expect(response).to redirect_to(users_path)
  follow_redirect!
  expect(inertia).to have_flash(notice: 'User created!')
end

it 'returns validation errors on failure' do
  post users_path, params: { user: { name: '' } }

  follow_redirect!
  expect(inertia).to have_props(errors: hash_including('name' => anything))
end
```

### Test Shared Props

Shared props from `inertia_share` are included in `inertia.props`. The `inertia`
helper is available in `type: :request` specs after requiring `inertia_rails/rspec`:

```ruby
it 'includes shared auth data' do
  sign_in(user)
  get dashboard_path

  expect(inertia).to have_props(
    auth: hash_including(user: hash_including(id: user.id))
  )
end
```

```ruby
it 'excludes auth data for unauthenticated users' do
  get dashboard_path

  expect(inertia).to have_props(auth: hash_including(user: nil))
end
```

### Test Deferred Props

```ruby
it 'defers expensive analytics data' do
  get dashboard_path

  expect(inertia).to have_deferred_props(:analytics, :statistics)
  expect(inertia).to have_deferred_props(:slow_data, group: :slow)
end
```

### Partial Reload Helpers

```ruby
it 'supports partial reload' do
  get users_path

  # Simulate partial reload — only fetch specific props
  inertia_reload_only(:users, :pagination)

  # Or exclude specific props
  inertia_reload_except(:expensive_stats)

  # Load deferred props
  inertia_load_deferred_props(:default)
  inertia_load_deferred_props # loads all groups
end
```

### Test External Redirects (inertia_location)

```ruby
it 'redirects to Stripe via inertia_location' do
  post checkout_path

  # inertia_location returns 409 with X-Inertia-Location header
  expect(response).to have_http_status(:conflict)
  expect(response.headers['X-Inertia-Location']).to match(/stripe\.com/)
end
```

### NEVER Test These

- **Inertia framework behavior** — don't test that `<Form>` sends CSRF tokens or that `router.visit` works. Test YOUR controller logic.
- **Exact prop structure** — use `have_props(users: satisfy { ... })`, not deep equality on full JSON. Brittle tests break when you add a column.
- **Flash without `follow_redirect!`** — after POST/PATCH/DELETE with redirect, you MUST `follow_redirect!` before asserting flash or props. Without it you're asserting against the 302, not the page.
- **Deferred prop values on initial load** — deferred props are `nil` in the initial response because they're fetched in a separate request after page render. Use `have_deferred_props(:key)` to verify they're registered, or `inertia_load_deferred_props` to resolve them in tests.
- **Mocked Inertia responses** — use `type: :request` specs that exercise the full stack. `type: :controller` specs with `assigns` don't work because Inertia uses a custom render pipeline that only executes in the full request cycle.

### Direct Access (use matchers above when possible)

```ruby
inertia.component       # => 'users/index'
inertia.props           # => { users: [...] }
inertia.props[:users]   # direct prop access
inertia.flash           # => { notice: 'Created!' }
inertia.deferred_props  # => { default: [:analytics], slow: [:report] }
```

## Related Skills
- **Controller patterns** → `inertia-rails-controllers` (prop types, flash, PRG)
- **Form flows** → `inertia-rails-forms` (submission, validation)
- **Deferred/shared props** → `inertia-rails-pages` (Deferred, usePage)

## References

**MANDATORY — READ ENTIRE FILE** when writing Minitest tests (not RSpec):
[`references/minitest.md`](references/minitest.md) (~40 lines) — Minitest assertions
equivalent to the RSpec matchers above.

**Do NOT load** `minitest.md` for RSpec projects — the matchers above are all
you need.
