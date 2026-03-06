---
name: graphql
description: Design GraphQL schemas, resolvers, and federation. Use for GraphQL API design or performance issues.
---

# GraphQL Development

Design efficient GraphQL APIs.

## When to Use

- Creating GraphQL schemas
- Resolver implementation
- N+1 query problems
- Federation/stitching
- Performance optimization

## Schema Design

```graphql
type Query {
  user(id: ID!): User
  users(filter: UserFilter, limit: Int = 10): UserConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
}

type User {
  id: ID!
  email: String!
  name: String!
  posts(first: Int, after: String): PostConnection!
  createdAt: DateTime!
}

input CreateUserInput {
  email: String!
  name: String!
}

type CreateUserPayload {
  user: User
  errors: [Error!]
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
  endCursor: String
}
```

## Resolvers

```javascript
const resolvers = {
  Query: {
    user: (_, { id }, { dataSources }) => dataSources.users.getById(id),

    users: async (_, { filter, limit }, { dataSources }) => {
      const users = await dataSources.users.find(filter, limit);
      return connectionFromArray(users);
    },
  },

  User: {
    // Field resolver with DataLoader for N+1
    posts: (user, args, { loaders }) => loaders.postsByUser.load(user.id),
  },

  Mutation: {
    createUser: async (_, { input }, { dataSources }) => {
      try {
        const user = await dataSources.users.create(input);
        return { user, errors: null };
      } catch (e) {
        return { user: null, errors: [{ message: e.message }] };
      }
    },
  },
};
```

## DataLoader (N+1 Solution)

```javascript
const DataLoader = require("dataloader");

const createLoaders = (dataSources) => ({
  userById: new DataLoader(async (ids) => {
    const users = await dataSources.users.getByIds(ids);
    const userMap = new Map(users.map((u) => [u.id, u]));
    return ids.map((id) => userMap.get(id) || null);
  }),

  postsByUser: new DataLoader(async (userIds) => {
    const posts = await dataSources.posts.findByUserIds(userIds);
    const grouped = groupBy(posts, "userId");
    return userIds.map((id) => grouped[id] || []);
  }),
});
```

## Performance Tips

- Use DataLoader for batching
- Implement query complexity limits
- Add depth limiting
- Cache with Redis/CDN
- Use persisted queries

## Best Practices

- Nullable by default, explicit `!` for required
- Use input types for mutations
- Return payload types with errors
- Implement cursor pagination
- Version via schema evolution

## Examples

**Input:** "Fix N+1 queries"
**Action:** Implement DataLoader, batch database queries

**Input:** "Design user management API"
**Action:** Create schema with types, queries, mutations, pagination
