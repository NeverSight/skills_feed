---
name: graphql-schema-design
description: Design production-grade GraphQL schemas with best practices and patterns
sasmp_version: "1.3.0"
bonded_agent: 02-graphql-schema
bond_type: PRIMARY_BOND
version: "2.0.0"
complexity: intermediate
estimated_time: "3-5 hours"
prerequisites: ["graphql-fundamentals"]
---

# GraphQL Schema Design Skill

> Architect scalable, maintainable GraphQL APIs

## Overview

Learn industry-standard patterns for designing GraphQL schemas that scale. Covers naming conventions, pagination, error handling, and schema evolution.

---

## Quick Reference

| Pattern | When to Use | Example |
|---------|-------------|---------|
| Connection | Paginated lists | `users: UserConnection!` |
| Payload | Mutation results | `CreateUserPayload` |
| Input | Mutation args | `CreateUserInput` |
| Interface | Shared fields | `interface Node { id: ID! }` |
| Union | Multiple types | `SearchResult = User \| Post` |

---

## Core Patterns

### 1. Naming Conventions

```graphql
# Types: PascalCase
type User { }
type UserProfile { }

# Fields: camelCase
type User {
  firstName: String!
  lastName: String!
  createdAt: DateTime!
  isActive: Boolean!      # Boolean prefix: is, has, can
}

# Queries: noun (singular/plural)
type Query {
  user(id: ID!): User           # Singular
  users: UserConnection!         # Plural
}

# Mutations: verb + noun
type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
  deleteUser(id: ID!): DeleteUserPayload!

  # Actions
  sendEmail(input: SendEmailInput!): SendEmailPayload!
  publishPost(id: ID!): PublishPostPayload!
}

# Inputs: [Action][Type]Input
input CreateUserInput { }
input UpdateUserInput { }
input UserFilterInput { }

# Payloads: [Action][Type]Payload
type CreateUserPayload { }
type UpdateUserPayload { }
```

### 2. Relay-Style Pagination

```graphql
# Connection pattern
type Query {
  users(
    first: Int
    after: String
    last: Int
    before: String
    filter: UserFilter
  ): UserConnection!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

# Usage
query GetUsers {
  users(first: 10, after: "cursor123") {
    edges {
      node { id name }
      cursor
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

### 3. Error Handling

```graphql
# Payload pattern (recommended)
type CreateUserPayload {
  user: User
  errors: [UserError!]!
}

type UserError {
  field: String
  message: String!
  code: UserErrorCode!
}

enum UserErrorCode {
  INVALID_EMAIL
  DUPLICATE_EMAIL
  WEAK_PASSWORD
  NOT_FOUND
  UNAUTHORIZED
}

# Union pattern (type-safe)
union CreateUserResult =
  | CreateUserSuccess
  | ValidationError
  | NotAuthorizedError

type CreateUserSuccess {
  user: User!
}

type ValidationError {
  field: String!
  message: String!
}

type NotAuthorizedError {
  message: String!
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserResult!
}
```

### 4. Node Interface

```graphql
# Global object identification
interface Node {
  id: ID!
}

type Query {
  node(id: ID!): Node
  nodes(ids: [ID!]!): [Node]!
}

type User implements Node {
  id: ID!
  name: String!
}

type Post implements Node {
  id: ID!
  title: String!
}

# Enables refetching any object by ID
query RefetchUser {
  node(id: "User:123") {
    ... on User {
      name
      email
    }
  }
}
```

### 5. Schema Organization

```graphql
# schema.graphql (root)
type Query {
  # User domain
  user(id: ID!): User
  users(filter: UserFilter): UserConnection!

  # Product domain
  product(id: ID!): Product
  products(filter: ProductFilter): ProductConnection!
}

type Mutation {
  # User mutations
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!

  # Product mutations
  createProduct(input: CreateProductInput!): CreateProductPayload!
}

# types/user.graphql
type User implements Node {
  id: ID!
  email: String!
  name: String!
  createdAt: DateTime!
  orders: OrderConnection!
}

# types/product.graphql
type Product implements Node {
  id: ID!
  name: String!
  price: Money!
  inventory: Int!
}
```

---

## Design Decisions

### When to Use What

```
Returning a list?
├── Small fixed size (<20) → [Item!]!
└── Variable/large size → ItemConnection!

Mutation result?
├── Can have user errors → Payload pattern
└── System errors only → Direct return

Multiple possible types?
├── Completely different → Union
└── Share common fields → Interface

Nested data?
├── Always needed together → Embed
└── Sometimes needed → Separate + ID reference
```

### Nullability Strategy

```graphql
type User {
  # Always required
  id: ID!
  email: String!

  # Optional (user choice)
  nickname: String
  bio: String

  # Lists: require list, require items
  posts: [Post!]!     # Never null, items never null

  # Computed (may fail)
  avatar: String      # Nullable if generation can fail
}
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Breaking change | Removed field | Use @deprecated first |
| Over-fetching | No pagination | Add Connection pattern |
| N+1 queries | Direct relations | Use DataLoader |
| Type explosion | Too many types | Use interfaces/generics |

### Schema Health Check

```bash
# Validate
npx graphql-inspector validate schema.graphql

# Check breaking changes
npx graphql-inspector diff old.graphql new.graphql

# Coverage analysis
npx graphql-inspector coverage schema.graphql queries/*.graphql
```

---

## Usage

```
Skill("graphql-schema-design")
```

## Related Skills
- `graphql-fundamentals` - Basic types and syntax
- `graphql-resolvers` - Implementing the schema
- `graphql-security` - Auth-aware design

## Related Agent
- `02-graphql-schema` - For detailed guidance
