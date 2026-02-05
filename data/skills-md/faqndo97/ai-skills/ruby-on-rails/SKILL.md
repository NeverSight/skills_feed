---
name: ruby-on-rails
description: Build Ruby on Rails features from scratch through production. Full lifecycle - build, debug, test, optimize, refactor. Follows Vanilla Rails philosophy (37signals/DHH), SOLID principles, and Rails 8 patterns.
---

<essential_principles>
## Vanilla Rails Philosophy

**"No one paradigm"** - Pragmatism over purity. Rails provides everything needed without complex architectural patterns.

### 1. Rich Domain Models Over Service Objects

Business logic lives in models. Use nested operation classes for complex workflows:

```ruby
# Model method delegates to nested class
class Quote < ApplicationRecord
  def create_purchase_order
    PurchaseOrderCreation.new(self).call
  end
end

# app/models/quote/purchase_order_creation.rb
class Quote::PurchaseOrderCreation
  def initialize(quote) = @quote = quote

  def call
    ApplicationRecord.transaction do
      po = create_purchase_order
      update_quote_status
      po
    end
  end
end
```

### 2. Concerns for Cohesive Traits

Concerns represent domain concepts, not junk drawers:

```ruby
module Closable
  extend ActiveSupport::Concern

  included do
    scope :open, -> { where(closed_at: nil) }
    scope :closed, -> { where.not(closed_at: nil) }
  end

  def close! = update!(closed_at: Time.current)
  def closed? = closed_at.present?
  def open? = !closed?
end
```

### 3. Thin Controllers, Fat Models

Controllers coordinate; models contain logic. Use filter chaining:

```ruby
def index
  resources = Resource.all
    .then(&method(:apply_scoping))
    .then(&method(:filter_by_status))
    .then(&method(:apply_ordering))

  render json: ResourceBlueprint.render(resources)
end
```

### 4. Current Pattern for Request Context

Use `Current` for cross-cutting concerns:

```ruby
class Current < ActiveSupport::CurrentAttributes
  attribute :user, :organization
end

# Set once in controller, use anywhere
Current.organization
```
</essential_principles>

<intake>
**What would you like to do?**

1. Build a new feature/endpoint
2. Debug an existing issue
3. Write/run tests
4. Optimize performance
5. Refactor code
6. Something else

**Then read the matching workflow from `workflows/` and follow it.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "new", "create", "build", "feature", "endpoint", "api" | `workflows/build-feature.md` |
| 2, "broken", "fix", "debug", "crash", "bug", "error" | `workflows/debug.md` |
| 3, "test", "tests", "spec", "coverage" | `workflows/write-tests.md` |
| 4, "slow", "optimize", "performance", "fast", "n+1" | `workflows/optimize-performance.md` |
| 5, "refactor", "clean", "improve", "restructure" | `workflows/refactor.md` |
| 6, other | Clarify, then select workflow or references |
</routing>

<verification_loop>
## After Every Change

```bash
# 1. Syntax check
ruby -c app/models/changed_file.rb

# 2. Run tests
bin/rails test test/models/changed_file_test.rb

# 3. Lint
bundle exec rubocop app/models/changed_file.rb -a
```

Report: "Syntax: OK | Tests: X pass | Lint: clean"
</verification_loop>

<reference_index>
## Domain Knowledge

All in `references/`:

**Architecture:** architecture.md
**Models:** models.md
**Controllers:** controllers.md
**Serialization:** blueprints.md
**Validations:** validations-callbacks.md
**Background Jobs:** background-jobs.md
**Performance:** performance.md
**Testing:** testing.md
**Multi-Tenant:** multi-tenant.md
**Anti-Patterns:** anti-patterns.md
</reference_index>

<workflows_index>
## Workflows

All in `workflows/`:

| File | Purpose |
|------|---------|
| build-feature.md | Create new feature/endpoint from scratch |
| debug.md | Find and fix bugs |
| write-tests.md | Write and run tests |
| optimize-performance.md | Profile and speed up |
| refactor.md | Restructure code following patterns |
</workflows_index>
