---
name: alba-inertia
description: >-
  Alba serializers + Typelizer for type-safe Inertia Rails props with auto-generated TypeScript types. Use when
  serializing models for Inertia responses, setting up Alba resources, generating TypeScript types from Ruby, or
  using Inertia prop options (defer, once, merge, scroll) with Alba attributes. Replaces as_json with structured,
  auto-typed ApplicationResource, page resources, and shared props resources. When active, OVERRIDES the
  `render inertia: { ... }` pattern from other skills — use convention-based instance variable rendering instead.
---

# Alba + Typelizer for Inertia Rails

Requires: `alba`, `typelizer`, `alba-inertia` gems in Gemfile.

Alba serializers for Inertia props with auto-generated TypeScript types.
Replaces `as_json(only: [...])` with structured, type-safe resources.

**Before creating a resource, ask:**
- **Reusable data shape (user, course)?** → Entity resource (`UserResource`) — shared across pages
- **Page-specific props bundle?** → Page resource (`UsersIndexResource`) — one per controller action
- **Global data (auth, notifications)?** → Shared props resource (`SharedPropsResource`)

**NEVER:**
- Use `as_json` when Alba is set up — it bypasses type generation and creates untyped props
- Skip `typelize_from` when resource name differs from model — Typelizer can't infer column types and generates `unknown`
- Put `declare module` augmentations in `serializers/index.ts` — Typelizer-generated types go in `serializers/index.ts`, manual InertiaConfig goes in `globals.d.ts`

## Setup

### ApplicationResource (all resources inherit from this)

```ruby
# app/resources/application_resource.rb
class ApplicationResource
  include Alba::Resource

  helper Typelizer::DSL          # enables typelize, typelize_from
  helper Alba::Inertia::Resource # enables inertia: option on attributes

  include Rails.application.routes.url_helpers
end
```

### Controller Integration

```ruby
# app/controllers/inertia_controller.rb
class InertiaController < ApplicationController
  include Alba::Inertia::Controller

  inertia_share { SharedPropsResource.new(self).to_inertia }
end
```

## Resource Types

### Entity Resource (reusable data shape)

```ruby
# app/resources/user_resource.rb
class UserResource < ApplicationResource
  typelize_from User  # needed when resource name doesn't match model

  attributes :id, :name, :email

  typelize :string?
  attribute :avatar_url do |user|
    user.avatar.attached? ? rails_blob_path(user.avatar, only_path: true) : nil
  end
end
```

### Page Resource (page-specific props)

```ruby
# app/resources/users/index_resource.rb
# Naming convention: {Controller}{Action}Resource
class UsersIndexResource < ApplicationResource
  has_many :users, resource: UserResource

  typelize :string
  attribute :search do |obj, _|
    obj.params.dig(:filters, :search)
  end
end
```

### Shared Props Resource

Requires Rails `Current` attributes (e.g., `Current.user`) to be configured —
see [CurrentAttributes](https://api.rubyonrails.org/classes/ActiveSupport/CurrentAttributes.html).

```ruby
# app/resources/shared_props_resource.rb
class SharedPropsResource < ApplicationResource
  one :auth, source: proc { Current }

  attribute :unread_messages_count, inertia: { always: true } do
    Current.user&.unread_count || 0
  end

  has_many :live_now, resource: LiveSessionsResource,
    inertia: { once: { expires_in: 5.minutes } }
end
```

## Convention-Based Rendering

With `Alba::Inertia::Controller`, instance variables auto-serialize:

```ruby
class UsersController < InertiaController
  def index
    @users = User.all        # auto-serialized via UserResource
    @filters = filter_params  # plain data passed through
    # Auto-detects UsersIndexResource
  end

  def show
    @user = User.find(params[:id])
    # Auto-detects UsersShowResource
  end
end
```

## Typelizer + Type Generation

`typelize_from` tells Typelizer which model to infer column types from — needed when
resource name doesn't match model. For computed attributes, declare types explicitly:

```ruby
class AuthorResource < ApplicationResource
  typelize_from User

  attributes :id, :name, :email

  typelize :string?                                  # next attribute is string | undefined
  attribute :avatar_url do |user|
    rails_storage_proxy_path(user.avatar) if user.avatar.attached?
  end

  typelize filters: "{category: number}"            # inline TS type
end
```

Types auto-generate when Rails server runs. Manual: `bin/rake typelizer:generate`.

## Inertia Prop Options in Alba

The `inertia:` option on attributes/associations maps to `InertiaRails` prop types:

```ruby
attribute :stats, inertia: :defer           # InertiaRails.defer
has_many :users, inertia: :optional         # InertiaRails.optional
has_many :countries, inertia: :once         # InertiaRails.once
has_many :items, inertia: { merge: true }   # InertiaRails.merge
attribute :csrf, inertia: { always: true }  # InertiaRails.always
```

**MANDATORY — READ ENTIRE FILE** when using grouped defer, merge with `match_on`,
scroll props, or combining multiple options:
[`references/prop-options.md`](references/prop-options.md) (~60 lines) — full syntax
for all `inertia:` option variants and `inertia_prop` alternative syntax.

**Do NOT load** for basic `inertia: :defer`, `inertia: :optional`, or
`inertia: :once` — the shorthand above is sufficient.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| TypeScript type is all `unknown` | Missing `typelize_from` | Add `typelize_from ModelName` when resource name doesn't match model |
| `inertia:` option has no effect | Missing helper | Ensure `helper Alba::Inertia::Resource` is in `ApplicationResource` |
| Types not regenerating | Server not running | Typelizer watches files in dev only. Run `bin/rake typelizer:generate` manually |
| `NoMethodError` for `typelize` | Missing helper | Ensure `helper Typelizer::DSL` is in `ApplicationResource` |
| Convention-based rendering picks wrong resource | Naming mismatch | Resource must be `{Controller}{Action}Resource` (e.g., `UsersIndexResource` for `UsersController#index`) |
| `to_inertia` undefined | Missing include | Controller needs `include Alba::Inertia::Controller` |

## Related Skills
- **Prop types** → `inertia-rails-controllers` (defer, once, merge, scroll)
- **TypeScript config** → `inertia-rails-typescript` (InertiaConfig in globals.d.ts)
