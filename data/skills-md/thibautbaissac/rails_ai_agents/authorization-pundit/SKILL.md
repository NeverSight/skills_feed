---
name: authorization-pundit
description: Implements policy-based authorization with Pundit for resource access control. Use when adding authorization rules, checking permissions, restricting actions, role-based access, or when user mentions Pundit, policies, authorization, or permissions.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Authorization with Pundit for Rails 8

## Overview

Pundit provides policy-based authorization:
- Plain Ruby policy objects
- Convention over configuration
- Easy to test
- Scoped queries for collections
- Works with any authentication system

## Quick Start

```bash
# Add to Gemfile
bundle add pundit

# Generate base files
bin/rails generate pundit:install

# Generate policy for model
bin/rails generate pundit:policy Event
```

## Project Structure

```
app/
├── policies/
│   ├── application_policy.rb    # Base policy
│   ├── event_policy.rb
│   ├── vendor_policy.rb
│   └── user_policy.rb
spec/policies/
├── event_policy_spec.rb
├── vendor_policy_spec.rb
└── user_policy_spec.rb
```

## TDD Workflow

```
Authorization Progress:
- [ ] Step 1: Write policy spec (RED)
- [ ] Step 2: Run spec (fails)
- [ ] Step 3: Implement policy
- [ ] Step 4: Run spec (GREEN)
- [ ] Step 5: Add policy to controller
- [ ] Step 6: Test integration
```

## Base Policy

```ruby
# app/policies/application_policy.rb
class ApplicationPolicy
  attr_reader :user, :record

  def initialize(user, record)
    @user = user
    @record = record
  end

  # Default: deny all
  def index?
    false
  end

  def show?
    false
  end

  def create?
    false
  end

  def new?
    create?
  end

  def update?
    false
  end

  def edit?
    update?
  end

  def destroy?
    false
  end

  class Scope
    def initialize(user, scope)
      @user = user
      @scope = scope
    end

    def resolve
      raise NotImplementedError, "Define #resolve in #{self.class}"
    end

    private

    attr_reader :user, :scope
  end
end
```

## Policy Testing

### Policy Spec

```ruby
# spec/policies/event_policy_spec.rb
require 'rails_helper'

RSpec.describe EventPolicy, type: :policy do
  subject { described_class }

  let(:account) { create(:account) }
  let(:user) { create(:user, account: account) }
  let(:other_user) { create(:user) }  # Different account
  let(:event) { create(:event, account: account) }

  permissions :index? do
    it "permits any authenticated user" do
      expect(subject).to permit(user, Event)
    end
  end

  permissions :show? do
    it "permits user from same account" do
      expect(subject).to permit(user, event)
    end

    it "denies user from different account" do
      expect(subject).not_to permit(other_user, event)
    end
  end

  permissions :create? do
    it "permits user from same account" do
      expect(subject).to permit(user, Event.new(account: account))
    end
  end

  permissions :update?, :destroy? do
    it "permits user from same account" do
      expect(subject).to permit(user, event)
    end

    it "denies user from different account" do
      expect(subject).not_to permit(other_user, event)
    end
  end

  describe "Scope" do
    let!(:own_event) { create(:event, account: account) }
    let!(:other_event) { create(:event) }  # Different account

    it "returns events for user's account only" do
      scope = described_class::Scope.new(user, Event).resolve

      expect(scope).to include(own_event)
      expect(scope).not_to include(other_event)
    end
  end
end
```

### Using pundit-matchers Gem

```ruby
# Gemfile
gem 'pundit-matchers', group: :test

# spec/rails_helper.rb
require 'pundit/matchers'

# spec/policies/event_policy_spec.rb
RSpec.describe EventPolicy, type: :policy do
  subject { described_class.new(user, event) }

  let(:account) { create(:account) }
  let(:user) { create(:user, account: account) }
  let(:event) { create(:event, account: account) }

  context "user owns the event" do
    it { is_expected.to permit_actions([:show, :edit, :update, :destroy]) }
  end

  context "user from different account" do
    let(:user) { create(:user) }

    it { is_expected.to forbid_actions([:show, :edit, :update, :destroy]) }
  end
end
```

## Policy Implementation

### Basic Policy

```ruby
# app/policies/event_policy.rb
class EventPolicy < ApplicationPolicy
  def index?
    true  # Any authenticated user can list
  end

  def show?
    owner?
  end

  def create?
    true  # Any authenticated user can create
  end

  def update?
    owner?
  end

  def destroy?
    owner?
  end

  private

  def owner?
    record.account_id == user.account_id
  end

  class Scope < ApplicationPolicy::Scope
    def resolve
      scope.where(account_id: user.account_id)
    end
  end
end
```

### Role-Based Policy

```ruby
# app/policies/event_policy.rb
class EventPolicy < ApplicationPolicy
  def index?
    true
  end

  def show?
    owner? || admin?
  end

  def create?
    member_or_above?
  end

  def update?
    owner_or_admin?
  end

  def destroy?
    admin?
  end

  # Custom action
  def publish?
    owner_or_admin? && record.draft?
  end

  def duplicate?
    owner?
  end

  private

  def owner?
    record.account_id == user.account_id
  end

  def admin?
    user.admin?
  end

  def member_or_above?
    user.member? || user.admin?
  end

  def owner_or_admin?
    owner? || admin?
  end

  class Scope < ApplicationPolicy::Scope
    def resolve
      if user.admin?
        scope.all
      else
        scope.where(account_id: user.account_id)
      end
    end
  end
end
```

### Policy with Conditions

```ruby
# app/policies/event_policy.rb
class EventPolicy < ApplicationPolicy
  def update?
    owner? && !record.locked?
  end

  def destroy?
    owner? && record.destroyable?
  end

  def cancel?
    owner? && record.can_cancel?
  end

  def restore?
    owner? && record.cancelled?
  end
end
```

## Controller Integration

### Basic Usage

```ruby
# app/controllers/events_controller.rb
class EventsController < ApplicationController
  def index
    @events = policy_scope(Event)
  end

  def show
    @event = Event.find(params[:id])
    authorize @event
  end

  def new
    @event = current_account.events.build
    authorize @event
  end

  def create
    @event = current_account.events.build(event_params)
    authorize @event

    if @event.save
      redirect_to @event, notice: t(".success")
    else
      render :new, status: :unprocessable_entity
    end
  end

  def edit
    @event = Event.find(params[:id])
    authorize @event
  end

  def update
    @event = Event.find(params[:id])
    authorize @event

    if @event.update(event_params)
      redirect_to @event, notice: t(".success")
    else
      render :edit, status: :unprocessable_entity
    end
  end

  def destroy
    @event = Event.find(params[:id])
    authorize @event
    @event.destroy
    redirect_to events_path, notice: t(".success")
  end
end
```

### Custom Action Authorization

```ruby
class EventsController < ApplicationController
  def publish
    @event = Event.find(params[:id])
    authorize @event, :publish?

    if @event.publish!
      redirect_to @event, notice: t(".success")
    else
      redirect_to @event, alert: t(".failure")
    end
  end

  def duplicate
    @event = Event.find(params[:id])
    authorize @event, :duplicate?

    @new_event = @event.duplicate
    redirect_to edit_event_path(@new_event)
  end
end
```

### Ensuring Authorization

```ruby
# app/controllers/application_controller.rb
class ApplicationController < ActionController::Base
  include Pundit::Authorization

  after_action :verify_authorized, except: :index
  after_action :verify_policy_scoped, only: :index

  rescue_from Pundit::NotAuthorizedError, with: :user_not_authorized

  private

  def user_not_authorized
    flash[:alert] = t("pundit.not_authorized")
    redirect_back(fallback_location: root_path)
  end
end
```

### Skip Authorization

```ruby
class HomeController < ApplicationController
  skip_after_action :verify_authorized, only: [:index, :about]
  skip_after_action :verify_policy_scoped, only: [:index, :about]

  def index
    # Public page, no authorization needed
  end
end
```

## View Integration

### Conditional Display

```erb
<%# app/views/events/show.html.erb %>
<h1><%= @event.name %></h1>

<% if policy(@event).edit? %>
  <%= link_to t("common.edit"), edit_event_path(@event) %>
<% end %>

<% if policy(@event).destroy? %>
  <%= button_to t("common.delete"), @event, method: :delete,
                data: { confirm: t("common.confirm_delete") } %>
<% end %>

<% if policy(@event).publish? %>
  <%= button_to t(".publish"), publish_event_path(@event), method: :post %>
<% end %>
```

### In Components

```ruby
# app/components/event_actions_component.rb
class EventActionsComponent < ApplicationComponent
  include Pundit::Authorization

  def initialize(event:, user:)
    @event = event
    @user = user
  end

  def can_edit?
    policy.edit?
  end

  def can_delete?
    policy.destroy?
  end

  def can_publish?
    policy.publish?
  end

  private

  def policy
    @policy ||= EventPolicy.new(@user, @event)
  end
end
```

## Headless Policies

For actions not tied to a specific record:

```ruby
# app/policies/dashboard_policy.rb
class DashboardPolicy < ApplicationPolicy
  def initialize(user, _record = nil)
    @user = user
  end

  def show?
    true
  end

  def admin_panel?
    user.admin?
  end

  def export_data?
    user.admin? || user.manager?
  end
end
```

```ruby
# Controller
class DashboardController < ApplicationController
  def show
    authorize :dashboard, :show?
  end

  def admin_panel
    authorize :dashboard, :admin_panel?
  end
end
```

## Permitted Attributes

### In Policy

```ruby
# app/policies/event_policy.rb
class EventPolicy < ApplicationPolicy
  def permitted_attributes
    if user.admin?
      [:name, :event_date, :status, :budget_cents, :internal_notes]
    else
      [:name, :event_date, :status, :budget_cents]
    end
  end

  def permitted_attributes_for_create
    [:name, :event_date]
  end

  def permitted_attributes_for_update
    permitted_attributes
  end
end
```

### In Controller

```ruby
class EventsController < ApplicationController
  def create
    @event = current_account.events.build(permitted_attributes(@event))
    authorize @event
    # ...
  end

  def update
    @event = Event.find(params[:id])
    authorize @event

    if @event.update(permitted_attributes(@event))
      # ...
    end
  end
end
```

## Nested Resource Policies

```ruby
# app/policies/comment_policy.rb
class CommentPolicy < ApplicationPolicy
  def create?
    # User can comment on events they can view
    EventPolicy.new(user, record.event).show?
  end

  def destroy?
    owner? || event_owner?
  end

  private

  def owner?
    record.user_id == user.id
  end

  def event_owner?
    record.event.account_id == user.account_id
  end

  class Scope < ApplicationPolicy::Scope
    def resolve
      # Only comments on events user can see
      scope.joins(:event).where(events: { account_id: user.account_id })
    end
  end
end
```

## Testing Controller Authorization

```ruby
# spec/requests/events_spec.rb
RSpec.describe "Events", type: :request do
  let(:user) { create(:user) }
  let(:other_user) { create(:user) }
  let(:event) { create(:event, account: user.account) }
  let(:other_event) { create(:event, account: other_user.account) }

  before { sign_in user }

  describe "GET /events/:id" do
    it "allows access to own events" do
      get event_path(event)
      expect(response).to have_http_status(:ok)
    end

    it "denies access to other's events" do
      get event_path(other_event)
      expect(response).to redirect_to(root_path)
    end
  end

  describe "DELETE /events/:id" do
    it "allows deletion of own events" do
      delete event_path(event)
      expect(response).to redirect_to(events_path)
      expect(Event.exists?(event.id)).to be false
    end

    it "denies deletion of other's events" do
      delete event_path(other_event)
      expect(response).to redirect_to(root_path)
      expect(Event.exists?(other_event.id)).to be true
    end
  end
end
```

## Error Messages

```yaml
# config/locales/en.yml
en:
  pundit:
    not_authorized: You are not authorized to perform this action.
    event_policy:
      show?: You cannot view this event.
      update?: You cannot edit this event.
      destroy?: You cannot delete this event.
      publish?: This event cannot be published.
```

```ruby
# Custom error handling
rescue_from Pundit::NotAuthorizedError do |exception|
  policy_name = exception.policy.class.to_s.underscore
  message = t("#{policy_name}.#{exception.query}", scope: "pundit", default: :default)
  redirect_back(fallback_location: root_path, alert: message)
end
```

## Checklist

- [ ] Policy spec written first (RED)
- [ ] Policy inherits from ApplicationPolicy
- [ ] Scope defined for collections
- [ ] Controller uses `authorize` and `policy_scope`
- [ ] `verify_authorized` after_action enabled
- [ ] Views use `policy(@record).action?`
- [ ] Error handling configured
- [ ] Multi-tenancy enforced in Scope
- [ ] All specs GREEN
