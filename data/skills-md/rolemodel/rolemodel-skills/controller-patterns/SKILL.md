---
name: controller-patterns
description: Review and update existing Rails controllers and generate new controllers following professional patterns and best practices. Covers RESTful conventions, authorization patterns, proper error handling, and maintainable code organization.
---

# Controller Best Practices

## Purpose
This skill helps AI agents review existing Rails controllers and generate new controllers following professional patterns and best practices. It covers RESTful conventions, authorization patterns, proper error handling, and maintainable code organization that can be applied to any Rails application.

## Context
This skill covers:
- **Rails** with RESTful conventions
- **Authorization patterns** (Pundit or similar)
- **Strong parameters** for security
- **Proper HTTP status codes** and flash messages
- **Consistent naming conventions**
- **Error handling best practices**

## Best Practices

## 1. Authorization

Implement authorization checks for all actions that interact with resources. This example uses Pundit, but the pattern applies to any authorization framework (CanCanCan, ActionPolicy, etc.).

**Key Principles:**
- Authorize in all actions that interact with resources
- Use scoped queries for collection actions
- Authorize in both `set_*` methods and create actions

```ruby
# In index - scope collections to authorized records
def index
  @products = policy_scope(Product)
  # Or with CanCanCan: @products = Product.accessible_by(current_ability)
end

# In new/create - authorize new instances
def new
  @product = authorize Product.new
end

def create
  @product = authorize Product.new(product_params)
  # ...
end

# In set method - authorize before any operation
def set_product
  @product = authorize Product.find(params[:id])
  # Or with CanCanCan: @product = Product.find(params[:id]); authorize! :read, @product
end
```

**Why This Matters:**
- Prevents unauthorized access to resources
- Provides a single, consistent authorization point
- Makes security audits easier
- Fails fast if authorization rules aren't met

## 2. Before Actions

Use `before_action` to DRY up your controllers by extracting common setup logic.

```ruby
before_action :set_product, only: %i[show edit update destroy]
before_action :set_company, only: %i[show edit update destroy]
```

**Best Practices:**
- Always use `only:` or `except:` to be explicit about which actions are affected
- Name methods descriptively: `set_[resource]`, `require_admin`, `check_ownership`
- Order matters - list them in the order they should execute
- Keep before_action methods simple and focused

**Common Before Actions:**
```ruby
# Resource loading
before_action :set_product, only: %i[show edit update destroy]

# Authorization checks
before_action :require_admin, only: %i[destroy]
before_action :require_ownership, only: %i[edit update destroy]

# State validation checks
before_action :ensure_pending, only: %i[create]
before_action :ensure_stopped, only: %i[create]

# Parent resource loading (for nested resources)
before_action :set_company
before_action :set_employee, only: %i[show edit update destroy]
```

**State Validation Pattern:**

Extract state validation into before_actions to keep controller actions focused:

```ruby
private

def ensure_pending
  return if @time_entry.pending?

  redirect_to time_entries_path, alert: 'Only pending entries can be submitted.'
end

def ensure_stopped
  return unless @time_entry.running?

  redirect_to time_entries_path, alert: 'Cannot submit a running timer.'
end
```

## 3. RESTful Actions Structure

**Index:**
```ruby
def index
  @resources = policy_scope(Resource)
end
```

**Show:**
```ruby
def show
  # Set resource via before_action
  # Load any associated data needed for the view
  @related_items = policy_scope(@resource.related_items)
end
```

**New:**
```ruby
def new
  @resource = authorize Resource.new
end
```

**Create:**
```ruby
def create
  @resource = authorize Resource.new(resource_params)

  if @resource.save
    redirect_to @resource, notice: 'Successfully Created Resource'
  else
    render 'new', status: :unprocessable_content
  end
end
```

**Edit:**
```ruby
def edit
  # Set resource via before_action
end
```

**Update:**
```ruby
def update
  if @resource.update(resource_params)
    redirect_to @resource, notice: 'Successfully Updated Resource'
  else
    render 'edit', status: :unprocessable_content
  end
end
```

**Destroy:**
```ruby
def destroy
  @resource.destroy
  redirect_to resources_url, notice: 'Successfully Deleted Resource'
end
```

## 4. Private Methods

**Set Method:**
```ruby
private

def set_resource
  @resource = authorize Resource.find(params[:id])
end
```

**Strong Parameters:**
```ruby
def resource_params
  params.expect(resource: [
    :attribute_one,
    :attribute_two,
    { nested_attributes: %i[id attr1 attr2] },
    { array_attributes: [] },
  ])
end
```

## 5. HTTP Status Codes

Use semantic HTTP status codes to communicate the result of operations clearly.

**Common Status Codes:**
```ruby
# Success (2xx)
render :show, status: :ok                    # 200 - Standard success
render :show, status: :created               # 201 - Resource created (optional for create)
head :no_content                             # 204 - Success with no response body

# Client Errors (4xx)
render :new, status: :unprocessable_content  # 422 - Validation failed
render json: {error: "Not found"}, status: :not_found  # 404
head :forbidden                              # 403 - User lacks permission
head :unauthorized                           # 401 - Authentication required
```

**Best Practices:**
- Use `:unprocessable_content` (422) for validation errors on create/update
- Use standard redirects (302) for successful operations
- No explicit status needed for redirects (uses 302 by default)
- Turbo/Hotwire requires proper status codes for correct behavior

**Example:**
```ruby
def create
  @product = authorize Product.new(product_params)

  if @product.save
    redirect_to @product, notice: 'Successfully Created Product'  # 302 redirect
  else
    render :new, status: :unprocessable_content  # 422 for validation errors
  end
end
```

## 6. Flash Messages

Use consistent, user-friendly flash messages for user feedback.

**Message Patterns:**
```ruby
# Success messages (use notice:)
redirect_to @product, notice: 'Successfully Created Product'
redirect_to @product, notice: 'Successfully Updated Product'
redirect_to products_url, notice: 'Successfully Deleted Product'

# Error messages (use alert:)
redirect_to products_url, alert: 'Failed to delete product'
redirect_to @product, alert: 'Unable to process request'

# Info messages
redirect_to @product, notice: 'Email sent successfully'
```

**Best Practices:**
- Use `notice:` for success messages
- Use `alert:` for error/warning messages
- Keep messages concise and action-oriented
- Use consistent capitalization and phrasing
- Avoid technical jargon in user-facing messages

## 7. Naming Conventions

Follow Rails conventions for consistent, predictable code.

**Controller Naming:**
```ruby
# Controller inherits from ApplicationController
class ProductsController < ApplicationController
  # ...
end

# Nested namespaced controllers
class Admin::ProductsController < Admin::BaseController
  # ...
end
```

**Instance Variables:**
```ruby
# Singular for individual resources
@product, @user, @article, @order

# Plural for collections
@products, @users, @articles, @orders

# Related resources maintain context
@product_reviews, @user_orders
```

**Private Method Names:**
```ruby
# Resource loading
def set_product
def set_user

# Strong parameters
def product_params
def user_params

# Authorization checks
def require_admin
def require_ownership
```

## Examples

## Simple CRUD Controller
```ruby
class ProductsController < ApplicationController
  before_action :set_product, only: %i[show edit update destroy]

  def index
    @products = policy_scope(Product)
  end

  def show
  end

  def new
    @product = authorize Product.new
  end

  def create
    @product = authorize Product.new(product_params)

    if @product.save
      redirect_to @product, notice: 'Successfully Created Product'
    else
      render 'new', status: :unprocessable_content
    end
  end

  def edit
  end

  def update
    if @product.update(product_params)
      redirect_to @product, notice: 'Successfully Updated Product'
    else
      render 'edit', status: :unprocessable_content
    end
  end

  def destroy
    @product.destroy
    redirect_to products_url, notice: 'Successfully Deleted Product'
  end

  private

  def set_product
    @product = authorize Product.find(params[:id])
  end

  def product_params
    params.expect(product: %i[name description price])
  end
end
```

## Controller with Nested Resources
```ruby
class OrderItemsController < ApplicationController
  before_action :set_order
  before_action :set_order_item, only: %i[show edit update destroy]

  def index
    @order_items = policy_scope(@order.order_items)
  end

  def new
    @order_item = authorize @order.order_items.build
  end

  def create
    @order_item = authorize @order.order_items.build(order_item_params)

    if @order_item.save
      redirect_to [@order, @order_item], notice: 'Successfully Created Order Item'
    else
      render 'new', status: :unprocessable_content
    end
  end

  def update
    if @order_item.update(order_item_params)
      redirect_to [@order, @order_item], notice: 'Successfully Updated Order Item'
    else
      render 'edit', status: :unprocessable_content
    end
  end

  def destroy
    @order_item.destroy
    redirect_to order_order_items_url(@order), notice: 'Successfully Deleted Order Item'
  end

  private

  def set_order
    @order = authorize Order.find(params[:order_id])
  end

  def set_order_item
    @order_item = authorize @order.order_items.find(params[:id])
  end

  def order_item_params
    params.expect(order_item: %i[product_id quantity price])
  end
end
```

## Review Checklist

When reviewing or generating controllers, verify:

- [ ] Controller inherits from `ApplicationController`
- [ ] All resource interactions use `authorize` or `policy_scope`
- [ ] `before_action` is used appropriately with `only:` parameter
- [ ] All standard RESTful actions follow the pattern
- [ ] Strong parameters are properly defined in private method
- [ ] Nested attributes use proper symbols array syntax
- [ ] Array attributes use `[]` notation
- [ ] HTTP status `:unprocessable_content` is used for validation failures
- [ ] Flash messages are consistent and user-friendly
- [ ] Redirects use resource path helpers
- [ ] Instance variables use appropriate singular/plural naming
- [ ] Private methods are properly defined and ordered

## Anti-Patterns to Avoid

❌ **Don't skip authorization:**
```ruby
def create
  @product = Product.new(product_params)  # Missing authorize!
end
```

✅ **Always authorize:**
```ruby
def create
  @product = authorize Product.new(product_params)
end
```

❌ **Don't use incorrect status codes:**
```ruby
render :new, status: :unprocessable_entity  # Wrong status
```

✅ **Use correct status:**
```ruby
render :new, status: :unprocessable_content
```

❌ **Don't use inconsistent flash messages:**
```ruby
redirect_to @product, notice: 'Product created!'
redirect_to @product, notice: 'The product has been successfully created'
redirect_to @product, notice: 'Product was saved'
```

✅ **Be consistent:**
```ruby
redirect_to @product, notice: 'Successfully Created Product'
redirect_to @product, notice: 'Successfully Updated Product'
redirect_to @product, notice: 'Successfully Deleted Product'
```

❌ **Don't forget strong parameters:**
```ruby
def create
  @product = authorize Product.new(params[:product])  # Unsafe!
end
```

✅ **Always use strong parameters:**
```ruby
def create
  @product = authorize Product.new(product_params)
end

private

def product_params
  params.expect(product: %i[name description price])
end
```

## Advanced Patterns

## RESTful Namespaced Controllers

For related actions on a resource, use namespaced controllers with standard RESTful actions (`create` and `destroy`) instead of custom actions. Organize controllers in a namespace folder matching the parent resource.

**Anti-Pattern:**
```ruby
# ❌ Custom action on main controller
class TimeEntriesController < ApplicationController
  def submit
    @time_entry.update!(status: :submitted)
    redirect_to time_entries_path
  end
end

# ❌ Controller not namespaced properly
class UnsubmitTimeEntriesController < ApplicationController
  def create
    @time_entry.update!(status: :pending)
    redirect_to time_entries_path
  end
end

# routes.rb
resources :time_entries do
  resource :submit_time_entry, only: [:create]
  resource :unsubmit_time_entry, only: [:create]
end

# File structure
/controllers
  /time_entries_controller.rb
  /submit_time_entries_controller.rb
  /unsubmit_time_entries_controller.rb
```

**Better Pattern:**
```ruby
# ✅ Namespaced controller with create and destroy actions
class TimeEntries::SubmissionsController < ApplicationController
  before_action :set_time_entry
  before_action :ensure_pending, only: [:create]
  before_action :ensure_stopped, only: [:create]
  before_action :ensure_submitted, only: [:destroy]

  def create
    @time_entry.update!(status: :submitted, submitted_at: Time.current)
    redirect_to time_entries_path, notice: 'Time entry submitted for approval.'
  end

  def destroy
    @time_entry.update!(status: :pending, submitted_at: nil)
    redirect_to time_entries_path, notice: 'Time entry unsubmitted.'
  end

  private

  def set_time_entry
    @time_entry = current_user.time_entries.find(params[:time_entry_id])
  end

  def ensure_pending
    return if @time_entry.pending?

    redirect_to time_entries_path, alert: 'Only pending entries can be submitted.'
  end

  def ensure_stopped
    return unless @time_entry.running?

    redirect_to time_entries_path, alert: 'Cannot submit a running timer.'
  end

  def ensure_submitted
    return if @time_entry.submitted?

    redirect_to time_entries_path, alert: 'Only submitted entries can be unsubmitted.'
  end
end

# routes.rb
resources :time_entries do
  resource :submission, only: [:create, :destroy], module: :time_entries
end

# File structure
/controllers
  /time_entries_controller.rb
  /time_entries
    /submissions_controller.rb

# View usage
button_to time_entry_submission_path(@time_entry), method: :post    # submit
button_to time_entry_submission_path(@time_entry), method: :delete  # unsubmit
```

**When to Use:**
- Actions that represent creating or destroying a conceptual sub-resource (submissions, subscriptions, approvals)
- Related actions that operate on the same parent resource
- Actions that change a primary state of a resource
- When you want to keep controllers focused and single-purpose

**Benefits:**
- Follows RESTful conventions (using `create` and `destroy` actions)
- Groups related functionality under a clear namespace
- Cleaner file organization with namespace folders
- Easier to test and maintain
- Clear separation of concerns
- Standard routing patterns
- Single controller instead of multiple separate controllers
- Validation logic extracted to before_actions keeps controller actions focused
- Before_actions can be tested independently

## Bulk Operations as Namespaced RESTful Controllers

Handle bulk operations in namespaced controllers using the `create` action with validation in before_actions:

```ruby
class TimeEntries::BulkSubmissionsController < ApplicationController
  before_action :set_entries
  before_action :ensure_entries_present
  before_action :ensure_entries_valid

  def create
    @entries.update_all(status: TimeEntry.statuses[:submitted], submitted_at: Time.current)
    redirect_to time_entries_path, notice: "#{@entries.count} time #{'entry'.pluralize(@entries.count)} submitted for approval."
  end

  private

  def set_entries
    entry_ids = params[:time_entry_ids] || []
    @entries = current_user.time_entries.where(id: entry_ids)
  end

  def ensure_entries_present
    return if @entries.any?

    redirect_to time_entries_path, alert: 'No time entries selected.'
  end

  def ensure_entries_valid
    invalid_entries = @entries.reject { |e| e.pending? && e.stopped? }
    return if invalid_entries.empty?

    redirect_to time_entries_path, alert: 'Only stopped pending entries can be submitted.'
  end
end

# routes.rb
resource :bulk_submissions, only: [:create], module: :time_entries

# File structure
/controllers
  /time_entries_controller.rb
  /time_entries
    /submissions_controller.rb
    /bulk_submissions_controller.rb

# View usage
form_with url: bulk_submissions_path, method: :post do |f|
  # form fields
end
```

## Scoped Collections in Show Actions

When showing a resource with related collections, apply policy scopes:

```ruby
def show
  @active_projects = policy_scope(@company.projects.active)
  @archived_projects = policy_scope(@company.projects.archived)
end
```

## Multiple Nested Associations

Handle complex nested relationships:

```ruby
def show
  @reviews = policy_scope(@product.reviews)
  @related_products = policy_scope(@product.category.products.where.not(id: @product.id))
end
```

## Nested Attributes in Strong Parameters

```ruby
def product_params
  params.expect(product: [
    :name,
    :description,
    :price,
    { images_attributes: %i[id url alt_text _destroy] },
    { variants_attributes: %i[id sku price stock_count _destroy] },
    { tags: [] },
    { category_ids: [] },
  ])
end
```

**Key Points:**
- Include `:id` for updating existing nested records
- Include `_destroy` to allow deletion of nested records
- Use `[]` for simple array attributes
- Use `%i[...]` for nested attributes hashes

## Usage Instructions for AI Agents

When asked to **review a controller:**
1. Check against the review checklist
2. Identify any anti-patterns
3. Suggest specific fixes with code examples
4. Prioritize authorization and security issues

When asked to **generate a new controller:**
1. Ask for the resource name and attributes if not provided
2. Determine if it's a simple or nested resource
3. Follow the appropriate example pattern
4. Include all standard RESTful actions unless specified otherwise
5. Generate appropriate strong parameters based on attributes
6. Ensure all authorization calls are in place
