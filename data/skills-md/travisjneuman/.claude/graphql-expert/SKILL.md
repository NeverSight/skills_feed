---
name: graphql-expert
description: GraphQL API design and implementation. Use when building GraphQL APIs, designing schemas, implementing resolvers, or optimizing GraphQL performance.
---

# GraphQL Expert

Comprehensive guide for designing and implementing GraphQL APIs.

## GraphQL Fundamentals

### What is GraphQL?

```
GraphQL is a query language for APIs that:
✓ Lets clients request exactly what they need
✓ Gets multiple resources in one request
✓ Uses a type system to describe data
✓ Provides introspection (self-documenting)

GraphQL vs REST:
┌─────────────────────────────────────────┐
│ REST: Multiple endpoints, fixed shapes  │
│ GET /users/1                            │
│ GET /users/1/posts                      │
│ GET /users/1/followers                  │
├─────────────────────────────────────────┤
│ GraphQL: Single endpoint, flexible      │
│ POST /graphql                           │
│ query { user(id: 1) {                   │
│   name                                  │
│   posts { title }                       │
│   followers { name }                    │
│ }}                                      │
└─────────────────────────────────────────┘
```

---

## Schema Design

### Type System

```graphql
# Scalar Types (built-in)
String, Int, Float, Boolean, ID

# Custom Scalar
scalar DateTime
scalar JSON

# Object Type
type User {
  id: ID!
  email: String!
  name: String
  createdAt: DateTime!
  posts: [Post!]!
}

# Enum
enum Role {
  ADMIN
  USER
  GUEST
}

# Interface
interface Node {
  id: ID!
}

type User implements Node {
  id: ID!
  # ... other fields
}

# Union
union SearchResult = User | Post | Comment

# Input Type (for mutations)
input CreateUserInput {
  email: String!
  name: String!
  role: Role = USER
}
```

### Nullability

```graphql
# Field modifiers:
String      # Nullable string
String!     # Non-null string
[String]    # Nullable list of nullable strings
[String!]   # Nullable list of non-null strings
[String]!   # Non-null list of nullable strings
[String!]!  # Non-null list of non-null strings

# Best practice:
# - Make fields nullable by default
# - Use ! only when guaranteed non-null
# - Lists should usually be non-null: [Item!]!
```

### Schema Structure

```graphql
# Root Types
type Query {
  # Read operations
  user(id: ID!): User
  users(limit: Int, offset: Int): [User!]!
  me: User
}

type Mutation {
  # Write operations
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): Boolean!
}

type Subscription {
  # Real-time updates
  userCreated: User!
  messageReceived(roomId: ID!): Message!
}
```

---

## Query Design

### Basic Queries

```graphql
# Simple query
query GetUser {
  user(id: "1") {
    name
    email
  }
}

# With variables
query GetUser($id: ID!) {
  user(id: $id) {
    name
    email
  }
}

# Multiple queries
query Dashboard {
  me {
    name
    notifications {
      count
    }
  }
  recentPosts(limit: 5) {
    title
    createdAt
  }
}
```

### Pagination

```graphql
# Offset-based (simple, but has issues)
type Query {
  users(limit: Int!, offset: Int!): [User!]!
}

# Cursor-based (recommended)
type Query {
  users(first: Int, after: String): UserConnection!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  cursor: String!
  node: User!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

# Usage
query {
  users(first: 10, after: "cursor123") {
    edges {
      cursor
      node {
        name
        email
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

### Filtering & Sorting

```graphql
input UserFilter {
  name: StringFilter
  email: StringFilter
  role: Role
  createdAt: DateFilter
}

input StringFilter {
  equals: String
  contains: String
  startsWith: String
}

input DateFilter {
  before: DateTime
  after: DateTime
}

enum UserSortField {
  NAME
  EMAIL
  CREATED_AT
}

input UserSort {
  field: UserSortField!
  direction: SortDirection!
}

enum SortDirection {
  ASC
  DESC
}

type Query {
  users(
    filter: UserFilter
    sort: UserSort
    first: Int
    after: String
  ): UserConnection!
}
```

---

## Mutations

### Mutation Design

```graphql
# Input types for mutations
input CreatePostInput {
  title: String!
  content: String!
  published: Boolean = false
  categoryIds: [ID!]
}

input UpdatePostInput {
  title: String
  content: String
  published: Boolean
}

# Mutation payloads (recommended)
type CreatePostPayload {
  post: Post
  errors: [Error!]!
}

type Error {
  field: String
  message: String!
}

type Mutation {
  createPost(input: CreatePostInput!): CreatePostPayload!
  updatePost(id: ID!, input: UpdatePostInput!): UpdatePostPayload!
  deletePost(id: ID!): DeletePostPayload!
}

# Usage
mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    post {
      id
      title
    }
    errors {
      field
      message
    }
  }
}
```

### Batch Mutations

```graphql
# For multiple operations
type Mutation {
  bulkDeletePosts(ids: [ID!]!): BulkDeletePayload!
  bulkUpdatePosts(updates: [PostUpdate!]!): BulkUpdatePayload!
}

input PostUpdate {
  id: ID!
  input: UpdatePostInput!
}
```

---

## Resolvers

### Basic Resolvers

```typescript
// TypeScript resolver implementation
const resolvers = {
  Query: {
    user: async (_, { id }, context) => {
      return context.dataSources.users.findById(id);
    },

    users: async (_, { filter, sort, first, after }, context) => {
      return context.dataSources.users.findMany({
        filter,
        sort,
        first,
        after,
      });
    },
  },

  Mutation: {
    createUser: async (_, { input }, context) => {
      // Validate
      const errors = validateCreateUser(input);
      if (errors.length) {
        return { user: null, errors };
      }

      // Create
      const user = await context.dataSources.users.create(input);
      return { user, errors: [] };
    },
  },

  // Field resolvers
  User: {
    posts: async (user, _, context) => {
      return context.dataSources.posts.findByUserId(user.id);
    },

    fullName: (user) => {
      return `${user.firstName} ${user.lastName}`;
    },
  },
};
```

### Resolver Context

```typescript
// Context setup
interface Context {
  user: User | null;
  dataSources: {
    users: UserDataSource;
    posts: PostDataSource;
  };
  loaders: {
    userLoader: DataLoader<string, User>;
    postLoader: DataLoader<string, Post>;
  };
}

// In server setup
const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: async ({ req }) => ({
    user: await getUserFromToken(req.headers.authorization),
    dataSources: {
      users: new UserDataSource(db),
      posts: new PostDataSource(db),
    },
    loaders: createLoaders(),
  }),
});
```

---

## Performance Optimization

### DataLoader (N+1 Solution)

```typescript
import DataLoader from "dataloader";

// Create loader
const userLoader = new DataLoader<string, User>(async (ids) => {
  const users = await db.users.findMany({
    where: { id: { in: ids } },
  });

  // Return in same order as input ids
  const userMap = new Map(users.map((u) => [u.id, u]));
  return ids.map((id) => userMap.get(id) || null);
});

// Use in resolver
const resolvers = {
  Post: {
    author: (post, _, context) => {
      return context.loaders.userLoader.load(post.authorId);
    },
  },
};
```

### Query Complexity

```typescript
import { createComplexityLimitRule } from "graphql-validation-complexity";

// Limit query complexity
const complexityLimitRule = createComplexityLimitRule(1000, {
  scalarCost: 1,
  objectCost: 10,
  listFactor: 10,
});

// Or field-level costs
const typeDefs = gql`
  type Query {
    users: [User!]! @complexity(value: 10, multipliers: ["first"])
    user(id: ID!): User @complexity(value: 1)
  }
`;
```

### Query Depth Limiting

```typescript
import depthLimit from "graphql-depth-limit";

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [depthLimit(10)],
});
```

### Persisted Queries

```typescript
// Client sends hash instead of full query
// Reduces bandwidth, enables whitelisting

// Apollo Client setup
import { createPersistedQueryLink } from "@apollo/client/link/persisted-queries";

const link = createPersistedQueryLink({ sha256 }).concat(httpLink);

// Server validates against known queries
const server = new ApolloServer({
  typeDefs,
  resolvers,
  persistedQueries: {
    cache: new RedisCache(),
  },
});
```

---

## Authentication & Authorization

### Context-Based Auth

```typescript
// Add user to context
const context = async ({ req }) => {
  const token = req.headers.authorization?.replace("Bearer ", "");
  const user = token ? await verifyToken(token) : null;
  return { user };
};

// Check in resolvers
const resolvers = {
  Query: {
    me: (_, __, context) => {
      if (!context.user) {
        throw new AuthenticationError("Not authenticated");
      }
      return context.user;
    },
  },
};
```

### Directive-Based Auth

```graphql
directive @auth(requires: Role = USER) on FIELD_DEFINITION

type Query {
  publicPosts: [Post!]!
  me: User @auth
  adminDashboard: Dashboard @auth(requires: ADMIN)
}
```

```typescript
// Directive implementation
class AuthDirective extends SchemaDirectiveVisitor {
  visitFieldDefinition(field) {
    const { resolve = defaultFieldResolver } = field;
    const requiredRole = this.args.requires;

    field.resolve = async function (...args) {
      const context = args[2];

      if (!context.user) {
        throw new AuthenticationError("Not authenticated");
      }

      if (requiredRole && context.user.role !== requiredRole) {
        throw new ForbiddenError("Not authorized");
      }

      return resolve.apply(this, args);
    };
  }
}
```

---

## Error Handling

### Error Types

```typescript
import {
  ApolloError,
  AuthenticationError,
  ForbiddenError,
  UserInputError,
} from "apollo-server";

// Validation errors
throw new UserInputError("Invalid email format", {
  field: "email",
});

// Auth errors
throw new AuthenticationError("Must be logged in");
throw new ForbiddenError("Not authorized to view this resource");

// Custom errors
class NotFoundError extends ApolloError {
  constructor(resource: string) {
    super(`${resource} not found`, "NOT_FOUND");
  }
}
```

### Error Formatting

```typescript
const server = new ApolloServer({
  formatError: (error) => {
    // Log internal errors
    if (error.extensions?.code === "INTERNAL_SERVER_ERROR") {
      console.error(error);
      return new Error("Internal server error");
    }

    // Mask sensitive info
    if (error.message.includes("password")) {
      return new Error("An error occurred");
    }

    return error;
  },
});
```

---

## Subscriptions

### Setup

```graphql
type Subscription {
  messageCreated(roomId: ID!): Message!
  userStatusChanged(userId: ID!): UserStatus!
}
```

```typescript
import { PubSub } from "graphql-subscriptions";

const pubsub = new PubSub();

const resolvers = {
  Mutation: {
    sendMessage: async (_, { input }, context) => {
      const message = await createMessage(input);

      pubsub.publish(`MESSAGE_CREATED_${input.roomId}`, {
        messageCreated: message,
      });

      return message;
    },
  },

  Subscription: {
    messageCreated: {
      subscribe: (_, { roomId }) => {
        return pubsub.asyncIterator(`MESSAGE_CREATED_${roomId}`);
      },
    },
  },
};
```

### With Filtering

```typescript
import { withFilter } from "graphql-subscriptions";

const resolvers = {
  Subscription: {
    messageCreated: {
      subscribe: withFilter(
        () => pubsub.asyncIterator("MESSAGE_CREATED"),
        (payload, variables, context) => {
          // Only send to users in the room
          return (
            payload.messageCreated.roomId === variables.roomId &&
            context.user.rooms.includes(variables.roomId)
          );
        },
      ),
    },
  },
};
```

---

## Client Integration

### Apollo Client Setup

```typescript
import { ApolloClient, InMemoryCache, createHttpLink } from "@apollo/client";
import { setContext } from "@apollo/client/link/context";

const httpLink = createHttpLink({
  uri: "/graphql",
});

const authLink = setContext((_, { headers }) => {
  const token = localStorage.getItem("token");
  return {
    headers: {
      ...headers,
      authorization: token ? `Bearer ${token}` : "",
    },
  };
});

const client = new ApolloClient({
  link: authLink.concat(httpLink),
  cache: new InMemoryCache(),
});
```

### React Hooks

```typescript
import { useQuery, useMutation, gql } from '@apollo/client';

const GET_USER = gql`
  query GetUser($id: ID!) {
    user(id: $id) {
      id
      name
      email
    }
  }
`;

function UserProfile({ userId }) {
  const { loading, error, data } = useQuery(GET_USER, {
    variables: { id: userId },
  });

  if (loading) return <Spinner />;
  if (error) return <Error message={error.message} />;

  return <div>{data.user.name}</div>;
}

// Mutation
const CREATE_POST = gql`
  mutation CreatePost($input: CreatePostInput!) {
    createPost(input: $input) {
      post { id title }
      errors { field message }
    }
  }
`;

function CreatePostForm() {
  const [createPost, { loading }] = useMutation(CREATE_POST, {
    update(cache, { data }) {
      // Update cache after mutation
    },
  });

  const handleSubmit = async (input) => {
    const { data } = await createPost({ variables: { input } });
    if (data.createPost.errors.length) {
      // Handle errors
    }
  };
}
```

---

## Best Practices

### DO:

- Design schema from client perspective
- Use input types for mutations
- Return payloads with errors from mutations
- Implement DataLoader for N+1 prevention
- Use cursor-based pagination
- Add query complexity limits
- Version schemas carefully

### DON'T:

- Expose database schema directly
- Create deeply nested types unnecessarily
- Forget about authorization
- Allow unbounded queries
- Skip error handling
- Ignore caching strategies
- Mutate data in queries

---

## Schema Checklist

- [ ] Types named descriptively (singular, PascalCase)
- [ ] Consistent nullability patterns
- [ ] Input types for all mutations
- [ ] Payload types with error handling
- [ ] Pagination for all lists
- [ ] Authentication/authorization considered
- [ ] Performance optimizations in place
