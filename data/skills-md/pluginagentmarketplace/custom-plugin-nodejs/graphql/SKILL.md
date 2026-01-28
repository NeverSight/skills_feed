---
name: graphql
description: Build GraphQL APIs with Node.js using Apollo Server, type definitions, resolvers, and real-time subscriptions
version: "2.1.0"
sasmp_version: "1.3.0"
bonded_agent: 02-express-framework
bond_type: PRIMARY_BOND
---

# GraphQL with Node.js Skill

Master building flexible, efficient GraphQL APIs using Node.js with Apollo Server, type-safe schemas, and real-time subscriptions.

## Quick Start

GraphQL API in 4 steps:
1. **Define Schema** - Types, queries, mutations
2. **Write Resolvers** - Data fetching logic
3. **Setup Server** - Apollo Server configuration
4. **Connect Data** - Database integration

## Core Concepts

### Schema Definition (SDL)
```graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
}

type Post {
  id: ID!
  title: String!
  content: String
  author: User!
}

type Query {
  user(id: ID!): User
  users(limit: Int, offset: Int): [User!]!
  post(id: ID!): Post
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User
  deleteUser(id: ID!): Boolean!
}

input CreateUserInput {
  name: String!
  email: String!
  password: String!
}

type Subscription {
  postCreated: Post!
}
```

### Apollo Server Setup
```javascript
const { ApolloServer } = require('@apollo/server');
const { expressMiddleware } = require('@apollo/server/express4');
const { readFileSync } = require('fs');

const typeDefs = readFileSync('./schema.graphql', 'utf-8');

const resolvers = {
  Query: {
    user: async (_, { id }, { dataSources }) => {
      return dataSources.userAPI.getUser(id);
    },
    users: async (_, { limit = 10, offset = 0 }, { dataSources }) => {
      return dataSources.userAPI.getUsers(limit, offset);
    }
  },
  Mutation: {
    createUser: async (_, { input }, { dataSources }) => {
      return dataSources.userAPI.createUser(input);
    }
  },
  User: {
    posts: async (parent, _, { dataSources }) => {
      return dataSources.postAPI.getPostsByAuthor(parent.id);
    }
  }
};

const server = new ApolloServer({ typeDefs, resolvers });
await server.start();

app.use('/graphql', express.json(), expressMiddleware(server, {
  context: async ({ req }) => ({
    user: req.user,
    dataSources: {
      userAPI: new UserAPI(),
      postAPI: new PostAPI()
    }
  })
}));
```

## Learning Path

### Beginner (2-3 weeks)
- ✅ Understand GraphQL concepts
- ✅ Define schemas with SDL
- ✅ Write basic resolvers
- ✅ Query and mutation basics

### Intermediate (4-6 weeks)
- ✅ Field resolvers and relationships
- ✅ Input validation
- ✅ Error handling
- ✅ DataLoader for N+1

### Advanced (8-10 weeks)
- ✅ Subscriptions (real-time)
- ✅ Authentication and authorization
- ✅ Federation for microservices
- ✅ Performance optimization

## DataLoader for N+1 Problem
```javascript
const DataLoader = require('dataloader');

const createUserLoader = () =>
  new DataLoader(async (userIds) => {
    const users = await User.find({ _id: { $in: userIds } });
    const userMap = new Map(users.map(u => [u.id, u]));
    return userIds.map(id => userMap.get(id));
  });

// Use in resolver
User: {
  posts: (parent, _, { loaders }) => {
    return loaders.userLoader.load(parent.authorId);
  }
}
```

## Authentication & Authorization
```javascript
const { shield, rule, allow } = require('graphql-shield');

const isAuthenticated = rule()((parent, args, { user }) => {
  return user !== null;
});

const isAdmin = rule()((parent, args, { user }) => {
  return user?.role === 'admin';
});

const permissions = shield({
  Query: { '*': allow, users: isAuthenticated },
  Mutation: {
    createPost: isAuthenticated,
    deleteUser: isAdmin
  }
});
```

## Error Handling
```javascript
const { ApolloError, UserInputError } = require('apollo-server-express');

class NotFoundError extends ApolloError {
  constructor(message) {
    super(message, 'NOT_FOUND');
  }
}

// In resolvers
const resolvers = {
  Query: {
    user: async (_, { id }) => {
      const user = await User.findById(id);
      if (!user) throw new NotFoundError(`User ${id} not found`);
      return user;
    }
  }
};
```

## Unit Test Template
```javascript
const { createTestClient } = require('apollo-server-testing');

describe('GraphQL API', () => {
  let query, mutate;

  beforeAll(() => {
    const server = new ApolloServer({ typeDefs, resolvers });
    const testClient = createTestClient(server);
    query = testClient.query;
    mutate = testClient.mutate;
  });

  it('should return users list', async () => {
    const GET_USERS = `query { users { id name } }`;
    const res = await query({ query: GET_USERS });

    expect(res.errors).toBeUndefined();
    expect(res.data.users).toBeDefined();
  });
});
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| N+1 query issue | Field resolvers | Use DataLoader |
| Slow queries | No caching | Implement Apollo Cache |
| Type errors | Schema mismatch | Validate with codegen |
| Auth bypass | Missing guards | Use graphql-shield |

## When to Use

Use GraphQL when:
- Clients need flexible data fetching
- Multiple clients with different data needs
- Avoiding over-fetching/under-fetching
- Real-time updates needed
- API evolution without versioning

## Related Skills

- Express REST API (alternative approach)
- Database Integration (data sources)
- JWT Authentication (securing API)

## Resources

- [Apollo Server Docs](https://www.apollographql.com/docs/apollo-server/)
- [GraphQL Specification](https://spec.graphql.org/)
- [DataLoader](https://github.com/graphql/dataloader)
