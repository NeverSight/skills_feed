---
name: json-typed-attributes
description: Define typed attributes backed by JSON fields in Rails models. Use when models need flexible data storage with type casting, validations, and form integration. Supports integer, decimal, string, text, boolean, date, and array types.
---

# JSON Typed Attributes

This skill helps you work with JSON-backed attributes in Rails models using the `StoreJsonAttributes` concern. It provides type casting, validation support, and seamless form integration.

## When to Use

- You need flexible data storage without creating separate database columns
- You want to store structured data (like configuration, metadata, or dynamic fields) in a JSON column
- You need proper type casting for JSON attributes (numbers, dates, booleans, arrays)
- You want to validate JSON-backed attributes like regular ActiveRecord attributes
- You need JSON attributes to work seamlessly with Rails forms

## Setup

### 1. Ensure JSON Column Exists

Your model must have a JSON column to store the attributes. Common names are `data`, `metadata`, or `settings`:

```ruby
# In migration
add_column :table_name, :data, :jsonb, default: {}
```

### 2. Include the Concern

```ruby
class YourModel < ApplicationRecord
  include StoreJsonAttributes
end
```

### 3. Define Typed Attributes

Use `store_typed_attributes` to define attributes with automatic type casting:

```ruby
store_typed_attributes [:attribute_name], type: :type_name, field: :json_column_name
```

## Supported Types

### String

```ruby
store_typed_attributes %i[timeline status], type: :string, field: :data
```

- Casts values to strings
- Returns `nil` for blank values
- Example usage:
  ```ruby
  record.timeline = "30 Days"
  record.timeline # => "30 Days"
  ```

### Integer

```ruby
store_typed_attributes %i[age count quantity], type: :integer, field: :data
```

- Casts values to integers
- Automatically strips commas and spaces from input ("1,000" → 1000)
- Returns `nil` for invalid values
- Example usage:
  ```ruby
  record.quantity = "1,500"
  record.quantity # => 1500
  ```

### Decimal

```ruby
store_typed_attributes %i[price revenue percentage], type: :decimal, field: :data
```

- Casts values to BigDecimal
- Automatically strips commas and spaces from input
- Preserves precision
- Example usage:
  ```ruby
  record.price = "1,234.56"
  record.price # => BigDecimal("1234.56")
  ```

### Boolean

```ruby
store_typed_attributes %i[active enabled verified], type: :boolean, field: :data
```

- Creates predicate methods (ending in `?`)
- Casts truthy/falsy values correctly
- Example usage:
  ```ruby
  record.active = "1"
  record.active? # => true

  record.active = "0"
  record.active? # => false
  ```

### Date

```ruby
store_typed_attributes %i[started_at completed_at], type: :date, field: :data
```

- Casts strings to Date objects
- Handles various date formats
- Example usage:
  ```ruby
  record.started_at = "2026-02-04"
  record.started_at # => Date object
  record.started_at.strftime("%B %d, %Y") # => "February 04, 2026"
  ```

### Array

```ruby
store_typed_attributes %i[categories tags], type: :array, field: :data
```

- Always returns an array (empty array if nil)
- Automatically removes blank values with `compact_blank`
- Example usage:
  ```ruby
  record.categories = ["Revenue Generation", "Operations Management"]
  record.categories # => ["Revenue Generation", "Operations Management"]

  record.categories = ["", "Valid", nil, "Another"]
  record.categories # => ["Valid", "Another"]
  ```

### Text

```ruby
store_typed_attributes %i[notes description], type: :text, field: :data
```

- Similar to string but intended for longer content
- Creates predicate method (ending in `?`)
- Example usage:
  ```ruby
  record.notes = "Long text content..."
  record.notes? # => true (if present)
  ```

## Complete Example

```ruby
# frozen_string_literal: true

class CBPComponents::KeyQuestion < CoreBusinessPresentationComponent
  CATEGORIES = [
    'Revenue Generation',
    'Operations Management',
    'Organizational Development',
    'Financial Management',
    'Ministry',
    'Personal Issue',
  ].freeze

  TIMELINES = ['30 Days', '90 Days', '180 Days', '1 Year', 'More than 1 Year'].freeze

  # Define JSON-backed typed attributes
  store_typed_attributes %i[timeline], type: :string, field: :data
  store_typed_attributes %i[categories], type: :array, field: :data

  # Add validations like any other attribute
  validates :timeline, inclusion: { in: TIMELINES, allow_blank: true }
  validates :categories, inclusion: { in: CATEGORIES }, allow_blank: true

  # Use in strong parameters
  private

  def base_params
    super.concat([:timeline, :summary, categories: []])
  end
end
```

## Working with Forms

JSON-backed attributes work seamlessly with Rails form helpers:

### Simple Fields

```slim
= form.text_field :timeline
= form.number_field :quantity
= form.check_box :active
```

### Array Fields (Checkboxes)

```slim
- CATEGORIES.each do |category|
  = form.check_box :categories,
    { multiple: true, checked: form.object.categories.include?(category) },
    category,
    nil
  = category
```

### Select Fields

```slim
= form.select :timeline,
  options_for_select(TIMELINES, form.object.timeline),
  { include_blank: "Select timeline" }
```

## Adding Validations

Validate JSON-backed attributes like regular attributes:

```ruby
# Presence
validates :timeline, presence: true

# Inclusion
validates :timeline, inclusion: { in: TIMELINES }

# Length
validates :categories, length: { minimum: 1, message: "must select at least one" }

# Custom validation
validate :categories_must_be_valid

private

def categories_must_be_valid
  invalid_categories = categories - CATEGORIES
  if invalid_categories.any?
    errors.add(:categories, "contains invalid categories: #{invalid_categories.join(', ')}")
  end
end

# Numericality
validates :quantity, numericality: { greater_than: 0, allow_nil: true }

# Format
validates :status, format: { with: /\A[A-Z][a-z]+\z/, allow_blank: true }
```

## Strong Parameters

Always include JSON-backed attributes in your strong parameters:

```ruby
# For simple types (string, integer, decimal, boolean, date)
params.require(:model).permit(:timeline, :quantity, :active, :started_at)

# For arrays, use array syntax
params.require(:model).permit(:timeline, categories: [])
```

## Multiple JSON Fields

You can use different JSON fields for different concerns:

```ruby
class Product < ApplicationRecord
  # Pricing data
  store_typed_attributes %i[base_price discount_percentage], type: :decimal, field: :pricing_data

  # Inventory data
  store_typed_attributes %i[quantity threshold], type: :integer, field: :inventory_data

  # Feature flags
  store_typed_attributes %i[featured new_arrival on_sale], type: :boolean, field: :flags
end
```

## Common Patterns

### Constants for Validation

Define constants for valid values:

```ruby
STATUSES = %w[pending approved rejected].freeze
PRIORITIES = %w[low medium high urgent].freeze

store_typed_attributes %i[status], type: :string, field: :data
store_typed_attributes %i[priority], type: :string, field: :data

validates :status, inclusion: { in: STATUSES, allow_blank: true }
validates :priority, inclusion: { in: PRIORITIES, allow_blank: true }
```

### Default Values

Set defaults in initializer or after_initialize:

```ruby
after_initialize :set_defaults, if: :new_record?

private

def set_defaults
  self.categories ||= []
  self.timeline ||= '90 Days'
  self.active = true if active.nil?
end
```

### Scopes and Queries

Query JSON attributes using PostgreSQL JSON operators:

```ruby
# Find records with specific value
scope :with_timeline, ->(timeline) {
  where("data->>'timeline' = ?", timeline)
}

# Find records where array contains value
scope :with_category, ->(category) {
  where("data->'categories' ? :category", category: category)
}

# Find records with any of multiple values
scope :with_any_category, ->(categories) {
  where("data->'categories' ?| array[:categories]", categories: categories)
}
```

## Best Practices

1. **Always specify the field name** - Makes it clear where data is stored
   ```ruby
   store_typed_attributes %i[timeline], type: :string, field: :data
   ```

2. **Use arrays for multi-select data** - Automatically handles blank values
   ```ruby
   store_typed_attributes %i[categories], type: :array, field: :data
   ```

3. **Define constants for valid values** - Makes validations and forms easier
   ```ruby
   TIMELINES = ['30 Days', '90 Days', '180 Days'].freeze
   validates :timeline, inclusion: { in: TIMELINES, allow_blank: true }
   ```

4. **Add validations** - JSON attributes should be validated like any other attribute
   ```ruby
   validates :quantity, numericality: { greater_than: 0, allow_nil: true }
   ```

5. **Use appropriate types** - Choose the type that matches your data
   - Use `:decimal` for money/percentages (not `:integer`)
   - Use `:array` for multi-select (automatically removes blanks)
   - Use `:boolean` for flags (creates predicate methods)

6. **Include in strong parameters** - Don't forget array syntax for array types
   ```ruby
   params.require(:model).permit(:timeline, categories: [])
   ```

7. **Consider indexing** - For frequently queried JSON attributes, add GIN indexes
   ```ruby
   add_index :table_name, :data, using: :gin
   ```

## Troubleshooting

### Attribute not persisting
- Ensure the JSON column exists in the database
- Check that the field name matches: `field: :data`
- Verify strong parameters include the attribute

### Type casting not working
- Verify the type is spelled correctly: `:integer`, `:decimal`, `:string`, etc.
- For arrays, ensure you're setting an array value
- For booleans, use the predicate method: `record.active?`

### Form not displaying correct values
- For arrays, check that you're using `multiple: true` and checking inclusion
- For selects, use `options_for_select` with the current value
- Ensure the getter method returns the expected type

### Validation failing
- Check that the attribute is included in strong parameters
- Verify constants match the expected values exactly
- For arrays, remember blank values are automatically removed
