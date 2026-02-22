---
name: routing-patterns
description: Review, generate, and update Rails routes following professional patterns and best practices. Covers RESTful resource routing, route concerns for code reusability, shallow nesting strategies, and advanced route configurations.
---

# Routes Best Practices

## Purpose
This skill helps AI agents review, generate, and update Rails routes following professional patterns and best practices. It covers RESTful resource routing, route concerns for code reusability, shallow nesting strategies, and advanced route configurations that can be applied to any Rails application.

## Context
This skill covers:
- **Rails routing** with RESTful conventions
- **Route concerns** for DRY (Don't Repeat Yourself) principle
- **Shallow nesting** to avoid overly long URLs
- **Custom parameters and metadata** for flexible routing
- **Custom route resolvers** for polymorphic paths
- **Constraint-based routing** for authorization
- **Organization patterns** for maintainable routes files

## Best Practices

## 1. Route Concerns for Reusable Behavior

Define concerns at the top of routes.rb for behaviors shared across multiple resources. This keeps your routes DRY and maintainable.

**Example: Commentable Resources**
```ruby
concern :commentable do
  resources :comments, commentable_type: parent_resource.name.classify
end
```

**Example: Duplicatable Resources**
```ruby
concern :duplicatable do
  resources :duplications, only: %i[create], resource_type: parent_resource.name.classify
end
```

**Example: Dynamic Form Updates (Turbo/AJAX)**
```ruby
concern :turbo_fetch do
  patch :turbo_fetch, on: :collection
end
```

**Key Points:**
- Concerns extract common nested resource patterns into reusable modules
- Use `parent_resource.name.classify` to dynamically pass the parent context type to controllers
- Specify `only:` or `except:` to limit actions when appropriate
- Custom parameters (like `commentable_type`, `resource_type`) are passed as metadata to controllers
- Controllers can access these via `params[:commentable_type]` or routing metadata

## 2. Applying Concerns to Resources

Apply concerns using the `concerns:` option with an array of symbols:

```ruby
resources :products, concerns: %i[duplicatable turbo_fetch]
resources :articles, concerns: %i[commentable duplicatable turbo_fetch]
```

**Benefits:**
- Eliminates repetitive nested resource definitions
- Changes to shared behavior only need to be updated in one place
- Makes it immediately clear which resources share common functionality

## 3. Shallow Nesting Strategy

Use `scope shallow: true` wrapper to enable shallow nesting for all nested resources. This prevents URLs from becoming unwieldy with deep nesting.

```ruby
scope shallow: true do
  resources :projects do
    resources :tasks do
      resources :comments
        # comments routes are shallow - only :index and :create are nested
        # show/edit/update/destroy use /comments/:id instead of /projects/:project_id/tasks/:task_id/comments/:id
      end
    end
  end
end
```

**Benefits:**
- Shorter, cleaner URLs for member actions (show, edit, update, destroy)
- Only collection actions (index, create) remain nested under parent
- Easier to bookmark and share individual resource URLs
- Can override with `shallow: false` when full nesting is needed

**Generated Routes:**
```
# Nested (collection routes)
GET    /projects/:project_id/tasks                tasks#index
POST   /projects/:project_id/tasks                tasks#create
GET    /projects/:project_id/tasks/new            tasks#new

# Shallow (member routes)
GET    /tasks/:id                                 tasks#show
GET    /tasks/:id/edit                            tasks#edit
PATCH  /tasks/:id                                 tasks#update
DELETE /tasks/:id                                 tasks#destroy
```

**Override Example:**
```ruby
concern :assembly do
  # Keep full nesting when parent context is always needed
  resources :assembly_items, only: %i[show], param: :kind, shallow: false
end
```

## 4. Limiting Actions with only: and except:

Always be explicit about which actions a resource provides. This improves security, performance, and code clarity.

```ruby
# Only specific actions
resources :webhooks, only: [], concerns: %i[turbo_fetch]  # No standard REST actions, only custom
resources :duplications, only: %i[create]                 # Only create action needed
resources :previews, only: %i[show update]                # Only show and update

# All except specific actions
resources :automations, except: %i[show]                  # All standard actions except show
resources :notes, except: %i[show]                        # Create/edit/destroy but no individual view
resources :widgets, except: %i[index show]                # No collection or individual views
```

**Why This Matters:**
- Prevents unused routes from cluttering `rails routes` output
- Blocks access to unimplemented controller actions
- Documents intent clearly for other developers
- Reduces attack surface by not exposing unnecessary endpoints

## 5. Nested Resources

For resources that belong to a parent, nest them appropriately:

```ruby
resources :companies do
  resources :employees, except: %i[index show]
end

resources :products do
  resources :reviews, except: %i[index]
  resources :variants, except: %i[index show]
end
```

**Common Pattern:**
- Parent resource gets full CRUD by default
- Nested resources often exclude `index` (displayed on parent's show page)
- Nested resources often exclude `show` (edited inline or from parent view)
- Nested create/update/destroy actions work within parent context

## 6. Singular Resources

Use `resource` (singular) for resources where there's only one per parent:

```ruby
resources :users do
  resource :profile, only: %i[show edit update]  # Only one profile per user
  resource :settings, only: %i[edit update]      # Only one settings per user
  resource :avatar, only: %i[show update]        # Only one avatar per user
end
```

**Key Points:**
- Singular resources don't have an `index` action
- URLs don't require an `:id` parameter (e.g., `/users/1/profile` not `/users/1/profiles/1`)
- Perfect for one-to-one relationships or singleton resources

## 7. Collection and Member Routes

Add custom routes using `on: :collection` or `on: :member`:

```ruby
resources :products do
  # Collection routes (no :id needed)
  get :search, on: :collection              # /products/search
  post :bulk_import, on: :collection        # /products/bulk_import

  # Member routes (requires :id)
  post :duplicate, on: :member              # /products/:id/duplicate
  patch :archive, on: :member               # /products/:id/archive
  get :preview, on: :member                 # /products/:id/preview
end

# In a concern
concern :archivable do
  patch :archive, on: :member
  patch :unarchive, on: :member
end
```

**Key Points:**
- **Collection routes** act on the entire collection (no `:id` parameter)
- **Member routes** act on a single resource (requires `:id` parameter)
- Use appropriate HTTP verbs (GET for reads, POST for creates, PATCH/PUT for updates, DELETE for removes)

## 8. Custom Parameters

Override default parameter names using `param:`:

```ruby
resources :products, param: :slug  # Uses :slug instead of :id

# In concerns
concern :categorizable do
  resources :categories, only: %i[show], param: :slug
end
```

**Results:**
- URLs become `/products/:slug` instead of `/products/:id`
- Controller receives `params[:slug]` instead of `params[:id]`
- Example: `/products/vintage-leather-jacket` instead of `/products/123`
- Useful for SEO-friendly URLs or when using non-numeric identifiers

## 9. Default Options

Set default options for a resource:

```ruby
resources :categories, defaults: { subcategory: false }
```

These defaults are available in `params[:subcategory]`.

## 10. Custom Route Resolvers

Define custom resolvers for polymorphic path helpers:

```ruby
resolve 'Bulk::Accessories' do |form|
  form.persisted? ? [form.accessory] : [form.tank, :accessories]
end

resolve 'AssemblyItem' do |item|
  [item.host, item]
end
```

**Usage:** These allow `url_for(@form_object)` or `link_to(@assembly_item)` to work correctly.

## 11. Session Routes

Use `controller` block with `scope` for related authentication actions:

```ruby
controller :sessions do
  get :login, action: :new
  delete :logout, action: :destroy

  scope :auth do
    get :failure
    match 'ADFS/callback', action: :create, via: %i[get post], as: :adfs_callback
  end
end
```

## 12. Mounting Engines with Constraints

Mount admin engines with authentication constraints:

```ruby
# Allow access only if user is logged in and is admin
mount PgHero::Engine, at: :pghero,
  constraints: -> env {
    env.session[:user_id].present? &&
    User.find_by(id: env.session[:user_id])&.admin?
  }

# Redirect to login if not authenticated
get :pghero, to: redirect('/login'), anchor: false,
  constraints: -> env { env.session[:user_id].blank? }
```

## 13. Health Check Routes

```ruby
# Production health check
mount Health::Check::Engine, at: 'health-check' if Rails.env.production?

# Rails 7.1+ health check
get :up, to: 'rails/health#show', as: :rails_health_check
```

## Complete Example Structure

Here's a well-organized routes file following all best practices:

```ruby
Rails.application.routes.draw do
  # 1. Define concerns first (reusable route patterns)
  concern :commentable do
    resources :comments, commentable_type: parent_resource.name.classify
  end

  concern :archivable do
    patch :archive, on: :member
    patch :unarchive, on: :member
  end

  concern :searchable do
    get :search, on: :collection
  end

  # 2. Main routes with shallow nesting
  scope shallow: true do
    # Top-level resources
    resources :users, except: %i[show] do
      resource :profile, only: %i[show edit update]
      resource :settings, only: %i[edit update]
    end

    resources :products, concerns: %i[commentable archivable searchable] do
      resources :reviews, except: %i[index]
      resources :variants, except: %i[index show]
    end

    # Nested resources
    resources :projects do
      resources :tasks, concerns: %i[commentable] do
        resource :assignment, only: %i[create destroy]
      end
    end
  end

  # 3. Session/authentication routes
  controller :sessions do
    get :login, action: :new
    post :login, action: :create
    delete :logout, action: :destroy
  end

  # 4. Admin routes with constraints
  namespace :admin do
    resources :users
    resources :settings, only: %i[index update]
  end

  # 5. Mounted engines (with constraints if needed)
  mount Sidekiq::Web, at: '/sidekiq', constraints: AdminConstraint.new

  # 6. Custom route resolvers (for polymorphic routing)
  resolve 'ProjectTask' do |task|
    [task.project, task]
  end

  # 7. Health checks
  get :up, to: 'rails/health#show', as: :rails_health_check

  # 8. Root route
  root 'dashboard#index'
end
```

## Review Checklist

When reviewing or generating routes, verify:

- [ ] Concerns are defined at the top of the file
- [ ] Concerns are DRY and reusable across multiple resources
- [ ] Custom parameters (like `commentable_type`) use `parent_resource.name.classify`
- [ ] Shallow nesting is enabled with `scope shallow: true`
- [ ] Resources explicitly use `only:` or `except:` to limit actions
- [ ] Nested resources follow the pattern (often no index/show)
- [ ] Singular resources use `resource` not `resources`
- [ ] Collection/member routes use `on:` parameter
- [ ] Custom parameter names use `param:` when needed
- [ ] Route resolvers are defined for form objects and polymorphic models
- [ ] Admin engines have authentication constraints
- [ ] Root route is defined
- [ ] Routes are organized logically (concerns → resources → custom → engines → resolvers → root)

## Anti-Patterns to Avoid

❌ **Don't repeat nested resource patterns:**
```ruby
resources :articles do
  resources :comments, commentable_type: 'Article'
end

resources :posts do
  resources :comments, commentable_type: 'Post'
end
```

✅ **Use concerns instead:**
```ruby
concern :commentable do
  resources :comments, commentable_type: parent_resource.name.classify
end

resources :articles, concerns: %i[commentable]
resources :posts, concerns: %i[commentable]
```

❌ **Don't use deep nesting without shallow:**
```ruby
resources :companies do
  resources :projects do
    resources :tasks do
      # Results in /companies/:company_id/projects/:project_id/tasks/:id/edit
    end
  end
end
```

✅ **Use shallow nesting:**
```ruby
scope shallow: true do
  resources :companies do
    resources :projects do
      resources :tasks  # edit becomes /tasks/:id/edit
    end
  end
end
```

❌ **Don't leave all actions when not needed:**
```ruby
resources :duplications  # Provides 7 REST actions but only need create
```

✅ **Be explicit:**
```ruby
resources :duplications, only: %i[create]
```

❌ **Don't use plural for singular resources:**
```ruby
resources :profiles, only: %i[show]  # There's only one profile per user
```

✅ **Use singular resource:**
```ruby
resource :profile, only: %i[show]
```

❌ **Don't hardcode context types:**
```ruby
concern :commentable do
  resources :comments, commentable_type: 'Article'  # Only works for articles
end
```

✅ **Use parent_resource:**
```ruby
concern :commentable do
  resources :comments, commentable_type: parent_resource.name.classify
end
```

## Advanced Patterns

## Concerns with Nested Concerns

Concerns can reference other concerns for highly reusable routing patterns:

```ruby
concern :searchable do
  get :search, on: :collection
  get :autocomplete, on: :collection
end

concern :taggable do
  resources :tags, only: %i[index create destroy],
    concerns: %i[searchable],
    taggable_type: parent_resource.name.classify
end

resources :articles, concerns: %i[taggable]
# Articles get tags with search and autocomplete functionality
```

## Multiple Custom Params

You can pass multiple custom parameters to concerns:

```ruby
concern :versioned do
  resources :versions,
    only: %i[index show],
    param: :version_number,
    shallow: false,
    versionable_type: parent_resource.name.classify
end
```

These custom parameters are available in the controller as routing metadata:
```ruby
# In controller
def index
  @versionable_type = request.path_parameters[:versionable_type] # => "Article"
end
```

## Context-Specific Route Additions

Add additional routes to specific resources after applying a concern:

```ruby
resources :articles, concerns: %i[commentable] do
  # Add article-specific routes beyond the concern
  get :preview, on: :member
  post :publish, on: :member
end
```

## Conditional Engine Mounting

Mount engines conditionally based on environment:

```ruby
if Rails.env.production?
  mount HealthCheck::Engine, at: 'health-check'
end

unless Rails.env.production?
  mount LetterOpenerWeb::Engine, at: '/letter_opener'
end
```

## Common Routing Patterns

These patterns appear frequently in Rails applications and can be implemented using concerns:

**Commentable Resources:**
- Pattern: Resources that can have comments
- Implementation: Nested comments resource with polymorphic association
- Applied to: Articles, blog posts, products, tasks, etc.

**Duplicatable Resources:**
- Pattern: Resources that can be cloned/duplicated
- Implementation: Create-only nested resource for duplication action
- Applied to: Templates, documents, configurations, etc.

**Archivable Resources:**
- Pattern: Resources that can be archived/unarchived
- Implementation: Member routes for archive state changes
- Applied to: Projects, documents, records, etc.

**Searchable Resources:**
- Pattern: Resources with search/filter functionality
- Implementation: Collection routes for search operations
- Applied to: Products, users, articles, etc.

**Versioned Resources:**
- Pattern: Resources with version history
- Implementation: Nested versions resource, often read-only
- Applied to: Documents, API resources, configurations, etc.

**Taggable Resources:**
- Pattern: Resources that can be tagged/categorized
- Implementation: Nested tags with create/destroy actions
- Applied to: Articles, images, bookmarks, etc.

## Usage Instructions for AI Agents

When asked to **review routes:**
1. Check routes are organized: concerns → resources → custom → engines → resolvers → root
2. Verify concerns are properly defined and reusable
3. Check for deep nesting that should use shallow
4. Ensure resources use `only:`/`except:` appropriately
5. Verify singular vs plural resource usage
6. Check for repeated patterns that should be concerns
7. Validate custom resolvers match model relationships

When asked to **generate new routes:**
1. Determine if the behavior is reusable → create/use a concern
2. Check if resource should be nested under a parent
3. Enable shallow nesting for nested resources (unless explicitly needed)
4. Specify `only:` or `except:` based on needed actions
5. Use `resource` (singular) if there's only one per parent
6. Add custom collection/member routes if needed
7. Create route resolver if it's a form object or polymorphic model
8. Follow existing concern patterns for similar functionality

When asked to **update routes:**
1. Maintain consistency with existing patterns
2. If adding similar functionality to multiple resources, refactor to use concerns
3. Update existing concerns rather than duplicating code
4. Preserve shallow nesting strategy
5. Keep routes organized in the established structure
6. Update custom resolvers if model relationships change

## Testing Routes

Always verify routes after changes:

```bash
# List all routes
rails routes

# Search for specific routes
rails routes | grep products

# Show routes for a specific controller
rails routes -c products

# Show routes with expanded format
rails routes --expanded

# Filter by HTTP verb
rails routes -g POST
```

---

*Last Updated: February 2026*
