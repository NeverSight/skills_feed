---
name: blueprint-gem
description: Work with Blueprinter gem for JSON serialization in Ruby. Covers fields, views, associations, transformers, extractors, and configuration. Use when creating, modifying, or debugging blueprints.
---

<essential_principles>

<principle name="blueprints-are-presenters">
Blueprints are JSON object presenters - they transform Ruby objects into simple hashes for JSON serialization. They are NOT models, NOT decorators. Keep them focused on presentation logic only.
</principle>

<principle name="views-for-context">
Use views to provide different serialization contexts for the same blueprint. Don't create separate blueprint classes when views suffice. Views can include other views and exclude fields.
</principle>

<principle name="fields-shorthand">
Use `fields` (plural) for multiple simple attributes. Use `field` (singular) only when you need a block, renaming, or options. This keeps blueprints concise.

```ruby
# Good - concise
fields :id, :name, :email, :created_at

# Only use singular when needed
field :full_name do |user|
  "#{user.first_name} #{user.last_name}"
end
```
</principle>

<principle name="identifier-always-renders">
`identifier` fields always render in every view (they have their own implicit `:identifier` view). Use for primary keys and unique identifiers only.
</principle>

</essential_principles>

<quick_reference>

<pattern name="basic-blueprint">
```ruby
class UserBlueprint < Blueprinter::Base
  identifier :id

  fields :email, :name, :created_at
end

# Usage
UserBlueprint.render(user)           # JSON string
UserBlueprint.render_as_hash(user)   # Ruby Hash
```
</pattern>

<pattern name="computed-field">
```ruby
field :full_name do |user|
  "#{user.first_name} #{user.last_name}"
end

# With options access
field :display_name do |user, options|
  options[:admin] ? user.admin_name : user.public_name
end
```
</pattern>

<pattern name="association">
```ruby
association :company, blueprint: CompanyBlueprint
association :posts, blueprint: PostBlueprint, view: :summary
```
</pattern>

<pattern name="view">
```ruby
view :extended do
  fields :phone, :address
  association :orders, blueprint: OrderBlueprint
end

# Usage
UserBlueprint.render(user, view: :extended)
```
</pattern>

<pattern name="conditional-field">
```ruby
field :salary, if: ->(field_name, user, options) { options[:show_salary] }
field :age, unless: ->(field_name, user, options) { user.hide_age? }
```
</pattern>

</quick_reference>

<intake>
What do you need help with?

1. Create a new blueprint
2. Understand a specific concept (views, associations, transformers, etc.)
3. Debug a blueprint issue
4. Something else

**For option 2, specify the concept and I'll load the relevant reference.**
</intake>

<routing>
| Response | Action |
|----------|--------|
| 1, "create", "new" | Read `workflows/create-blueprint.md` |
| 2, "fields", "identifier" | Read `references/fields-and-identifiers.md` |
| 2, "views", "view" | Read `references/views.md` |
| 2, "association", "nested" | Read `references/associations.md` |
| 2, "config", "configure", "setup" | Read `references/configuration.md` |
| 2, "transformer", "extractor" | Read `references/transformers-and-extractors.md` |
| 2, "conditional", "default", "if", "unless" | Read `references/conditionals-and-defaults.md` |
| 3, "debug", "issue", "problem" | Read `references/anti-patterns.md` first |
| 4, other | Clarify need, then select appropriate reference |

**After reading, apply the knowledge to the user's specific situation.**
</routing>

<reference_index>

**Core Concepts:**
- fields-and-identifiers.md - Fields, identifiers, computed fields, field options
- views.md - Views, include/exclude, view inheritance
- associations.md - Nested blueprints, polymorphic associations

**Advanced:**
- configuration.md - Global config, JSON generators, field sorting
- transformers-and-extractors.md - Custom transformers and extractors
- conditionals-and-defaults.md - Conditional fields, defaults, nil handling

**Troubleshooting:**
- anti-patterns.md - Common mistakes and how to fix them

</reference_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| create-blueprint.md | Create a new blueprint with proper structure |
</workflows_index>
