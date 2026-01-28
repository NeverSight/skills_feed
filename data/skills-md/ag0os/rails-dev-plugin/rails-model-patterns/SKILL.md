---
name: rails-model-patterns
description: ActiveRecord model patterns and conventions for Rails. Automatically invoked when working with models, associations, validations, scopes, callbacks, or database schema design. Triggers on "model", "ActiveRecord", "association", "has_many", "belongs_to", "validation", "validates", "scope", "callback", "migration", "schema", "index", "foreign key".
allowed-tools: Read, Grep, Glob
---

# Rails Model Patterns

Patterns for building well-structured ActiveRecord models in Rails applications.

## When This Skill Applies

- Designing models with proper associations
- Implementing validations and callbacks
- Creating efficient scopes and queries
- Writing safe database migrations
- Optimizing database performance

## Quick Reference

| Pattern | Use When |
|---------|----------|
| `belongs_to` | Child references parent |
| `has_many` | Parent has multiple children |
| `has_one` | Parent has single child |
| `has_many :through` | Many-to-many via join model |
| `has_and_belongs_to_many` | Simple many-to-many (no join model attributes) |

## Detailed Documentation

- [associations.md](associations.md) - Association patterns and options
- [validations.md](validations.md) - Validation patterns
- [migrations.md](migrations.md) - Safe migration practices

## Model Structure Best Practice

```ruby
class User < ApplicationRecord
  # 1. Constants
  ROLES = %w[admin member guest].freeze

  # 2. Associations
  belongs_to :organization
  has_many :posts, dependent: :destroy
  has_many :comments, through: :posts

  # 3. Validations
  validates :email, presence: true, uniqueness: { case_sensitive: false }
  validates :name, presence: true, length: { maximum: 100 }
  validates :role, inclusion: { in: ROLES }

  # 4. Scopes
  scope :active, -> { where(active: true) }
  scope :recent, -> { order(created_at: :desc) }
  scope :admins, -> { where(role: 'admin') }

  # 5. Callbacks (use sparingly)
  before_save :normalize_email

  # 6. Class methods
  def self.find_by_email(email)
    find_by(email: email.downcase.strip)
  end

  # 7. Instance methods
  def admin?
    role == 'admin'
  end

  private

  def normalize_email
    self.email = email.downcase.strip
  end
end
```

## Key Principles

### Validations
- Use built-in validators when possible
- Add database constraints for critical validations
- Custom validators for complex business rules

### Associations
- Always specify `:dependent` option
- Use `:inverse_of` for bidirectional associations
- Consider counter caches for counts

### Scopes
- Prefer scopes over class methods for queries
- Chain scopes for complex queries
- Use `merge` to combine scopes from different models

### Callbacks
- Use sparingly - prefer service objects
- Keep callbacks focused and simple
- Avoid callbacks that trigger external services
