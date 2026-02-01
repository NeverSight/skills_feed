---
name: rails-graphql-patterns
description: GraphQL patterns for Rails applications using graphql-ruby gem. Automatically invoked when working with GraphQL schemas, types, resolvers, mutations, subscriptions, or the app/graphql directory. Triggers on "GraphQL", "schema", "resolver", "mutation", "query type", "subscription", "graphql-ruby", "field", "argument", "N+1 graphql", "dataloader".
allowed-tools: Read, Grep, Glob
---

# Rails GraphQL Patterns

Patterns for building GraphQL APIs in Rails applications using graphql-ruby.

## When This Skill Applies

- Designing GraphQL schemas and types
- Implementing resolvers and mutations
- Optimizing queries and preventing N+1 problems
- Handling authentication/authorization in GraphQL
- Implementing subscriptions for real-time updates
- Structuring the app/graphql directory

## Quick Reference

| Component | Purpose | Location |
|-----------|---------|----------|
| Types | Define object shapes | `app/graphql/types/` |
| Queries | Read operations | `app/graphql/types/query_type.rb` |
| Mutations | Write operations | `app/graphql/mutations/` |
| Resolvers | Query logic | `app/graphql/resolvers/` |
| Sources | DataLoader batching | `app/graphql/sources/` |

## Detailed Documentation

- [patterns.md](patterns.md) - Complete GraphQL patterns with examples

## Type Definition Basics

```ruby
# app/graphql/types/user_type.rb
module Types
  class UserType < Types::BaseObject
    field :id, ID, null: false
    field :email, String, null: false
    field :name, String
    field :created_at, GraphQL::Types::ISO8601DateTime, null: false

    field :posts, [Types::PostType], null: true
    field :posts_count, Integer, null: false

    def posts_count
      object.posts.size  # Use size for counter cache
    end
  end
end
```

## Mutation Basics

```ruby
# app/graphql/mutations/create_post.rb
module Mutations
  class CreatePost < BaseMutation
    argument :title, String, required: true
    argument :content, String, required: true

    field :post, Types::PostType
    field :errors, [String], null: false

    def resolve(title:, content:)
      post = context[:current_user].posts.build(title: title, content: content)

      if post.save
        { post: post, errors: [] }
      else
        { post: nil, errors: post.errors.full_messages }
      end
    end
  end
end
```

## N+1 Prevention with DataLoader

```ruby
# app/graphql/sources/record_loader.rb
class Sources::RecordLoader < GraphQL::Dataloader::Source
  def initialize(model_class)
    @model_class = model_class
  end

  def fetch(ids)
    records = @model_class.where(id: ids).index_by(&:id)
    ids.map { |id| records[id] }
  end
end

# Usage in type
def author
  dataloader.with(Sources::RecordLoader, User).load(object.user_id)
end
```

## Key Principles

- **Type Safety**: Define explicit types for all fields
- **Null Handling**: Be intentional about `null: true/false`
- **Batch Loading**: Use DataLoader to prevent N+1 queries
- **Authorization**: Check permissions at field level
- **Error Handling**: Return structured errors, not exceptions
