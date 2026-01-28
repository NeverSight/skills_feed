---
name: graphql-fundamentals
description: Master GraphQL core concepts - types, queries, mutations, and subscriptions
sasmp_version: "1.3.0"
bonded_agent: 01-graphql-fundamentals
bond_type: PRIMARY_BOND
version: "2.0.0"
complexity: beginner
estimated_time: "2-4 hours"
prerequisites: []
---

# GraphQL Fundamentals Skill

> Master the building blocks of GraphQL APIs

## Overview

This skill covers the essential GraphQL concepts every developer needs. From type definitions to query operations, you'll learn the foundation for building GraphQL APIs.

---

## Quick Reference

| Concept | Syntax | Example |
|---------|--------|---------|
| Scalar | `String`, `Int`, `Float`, `Boolean`, `ID` | `name: String!` |
| Object | `type Name { fields }` | `type User { id: ID! }` |
| Input | `input Name { fields }` | `input CreateUserInput { name: String! }` |
| Enum | `enum Name { VALUES }` | `enum Status { ACTIVE INACTIVE }` |
| List | `[Type]` or `[Type!]!` | `tags: [String!]!` |
| Non-null | `Type!` | `id: ID!` |

---

## Core Concepts

### 1. Type System

```graphql
# Scalar types (built-in)
type Example {
  id: ID!           # Unique identifier
  name: String!     # Text
  age: Int          # Integer (nullable)
  score: Float!     # Decimal
  active: Boolean!  # True/false
}

# Custom scalars
scalar DateTime
scalar JSON
scalar Upload

# Object types
type User {
  id: ID!
  email: String!
  profile: Profile    # Nested object
  posts: [Post!]!     # List of objects
}

type Profile {
  bio: String
  avatar: String
}

# Enums
enum UserRole {
  ADMIN
  EDITOR
  VIEWER
}

# Input types (for mutations)
input CreateUserInput {
  email: String!
  name: String!
  role: UserRole = VIEWER  # Default value
}

# Interfaces
interface Node {
  id: ID!
}

type User implements Node {
  id: ID!
  name: String!
}

# Unions
union SearchResult = User | Post | Comment
```

### 2. Queries

```graphql
# Schema definition
type Query {
  # Single item
  user(id: ID!): User

  # List with optional filter
  users(filter: UserFilter, limit: Int = 10): [User!]!

  # Search
  search(query: String!): [SearchResult!]!
}

# Client query examples
query GetUser {
  user(id: "123") {
    id
    name
    email
  }
}

query GetUsersWithFilter {
  users(filter: { role: ADMIN }, limit: 5) {
    id
    name
  }
}

# With variables
query GetUser($userId: ID!) {
  user(id: $userId) {
    id
    name
  }
}
# Variables: { "userId": "123" }

# With aliases
query GetTwoUsers {
  admin: user(id: "1") { name }
  editor: user(id: "2") { name }
}

# With fragments
fragment UserFields on User {
  id
  name
  email
}

query GetUsers {
  users {
    ...UserFields
  }
}
```

### 3. Mutations

```graphql
# Schema definition
type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): DeletePayload!
}

type CreateUserPayload {
  user: User
  errors: [Error!]!
}

# Client mutation
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    user {
      id
      name
    }
    errors {
      field
      message
    }
  }
}
# Variables: { "input": { "email": "test@example.com", "name": "Test" } }
```

### 4. Subscriptions

```graphql
# Schema definition
type Subscription {
  userCreated: User!
  messageReceived(channelId: ID!): Message!
}

# Client subscription
subscription OnUserCreated {
  userCreated {
    id
    name
    createdAt
  }
}

subscription OnMessage($channelId: ID!) {
  messageReceived(channelId: $channelId) {
    id
    content
    sender { name }
  }
}
```

---

## Common Patterns

### Nullability Cheat Sheet

```graphql
type Example {
  # Required field - never null
  id: ID!

  # Optional field - can be null
  nickname: String

  # Required list, optional items
  tags: [String]!        # [], ["a", null, "b"]

  # Required list, required items (most common)
  categories: [Category!]!  # [], [cat1, cat2]

  # Optional list (avoid - ambiguous)
  # items: [Item]  # null vs [] unclear
}
```

### Input Validation Pattern

```graphql
input CreateUserInput {
  email: String!      # Required
  name: String!       # Required
  age: Int            # Optional
  role: UserRole = VIEWER  # Optional with default
}
```

---

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `Cannot query field "x"` | Field not in schema | Check spelling, verify schema |
| `Variable "$x" not defined` | Missing variable declaration | Add to query signature |
| `Expected non-null, got null` | Resolver returned null for `!` field | Fix resolver or make nullable |
| `Unknown type "X"` | Type not defined | Add type definition |

### Debug Commands

```bash
# Validate schema
npx graphql-inspector validate schema.graphql

# Introspect remote schema
npx graphql-inspector introspect http://localhost:4000/graphql

# Check for breaking changes
npx graphql-inspector diff old.graphql new.graphql
```

---

## Usage

```
Skill("graphql-fundamentals")
```

## Related Skills
- `graphql-schema-design` - Advanced schema patterns
- `graphql-resolvers` - Implementing resolvers
- `graphql-codegen` - TypeScript type generation

## Related Agent
- `01-graphql-fundamentals` - For detailed guidance
