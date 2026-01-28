---
name: graphql-resolvers
description: Write efficient resolvers with DataLoader, batching, and N+1 prevention
sasmp_version: "1.3.0"
bonded_agent: 03-graphql-resolvers
bond_type: PRIMARY_BOND
version: "2.0.0"
complexity: intermediate
estimated_time: "4-6 hours"
prerequisites: ["graphql-fundamentals", "graphql-schema-design"]
---

# GraphQL Resolvers Skill

> Build performant data fetching with proper patterns

## Overview

Master resolver implementation including the critical DataLoader pattern for preventing N+1 queries, context design, and error handling strategies.

---

## Quick Reference

| Pattern | Purpose | When to Use |
|---------|---------|-------------|
| DataLoader | Batch + cache | Any relationship field |
| Context | Request-scoped data | Auth, loaders, datasources |
| Field resolver | Computed fields | Derived data |
| Root resolver | Entry points | Query/Mutation fields |

---

## Core Patterns

### 1. Resolver Signature

```javascript
// (parent, args, context, info) => result

const resolvers = {
  Query: {
    // Root resolver - parent is undefined
    user: async (_, { id }, { dataSources }) => {
      return dataSources.users.findById(id);
    },
  },

  User: {
    // Field resolver - parent is User object
    posts: async (user, { first = 10 }, { loaders }) => {
      return loaders.postsByAuthor.load(user.id);
    },

    // Computed field - sync is fine
    fullName: (user) => `${user.firstName} ${user.lastName}`,

    // Default resolver (implicit)
    // email: (user) => user.email,
  },
};
```

### 2. DataLoader Pattern

```javascript
const DataLoader = require('dataloader');

// N+1 Problem:
// Query: { users { posts { title } } }
// Without DataLoader: 1 + N queries

// Solution: Batch loading
const createLoaders = () => ({
  // Batch by foreign key
  postsByAuthor: new DataLoader(async (authorIds) => {
    // 1. Single query for all authors
    const posts = await db.posts.findAll({
      where: { authorId: { [Op.in]: authorIds } }
    });

    // 2. Group by author
    const postsByAuthor = {};
    posts.forEach(post => {
      if (!postsByAuthor[post.authorId]) {
        postsByAuthor[post.authorId] = [];
      }
      postsByAuthor[post.authorId].push(post);
    });

    // 3. Return in same order as input
    return authorIds.map(id => postsByAuthor[id] || []);
  }),

  // Batch by primary key
  userById: new DataLoader(async (ids) => {
    const users = await db.users.findAll({
      where: { id: { [Op.in]: ids } }
    });
    const userMap = new Map(users.map(u => [u.id, u]));
    return ids.map(id => userMap.get(id) || null);
  }),
});

// Usage in resolvers
const resolvers = {
  Post: {
    author: (post, _, { loaders }) => {
      return loaders.userById.load(post.authorId);
    },
  },
  User: {
    posts: (user, _, { loaders }) => {
      return loaders.postsByAuthor.load(user.id);
    },
  },
};
```

### 3. Context Setup

```javascript
const createContext = async ({ req, res }) => {
  // 1. Parse auth token
  const token = req.headers.authorization?.replace('Bearer ', '');
  const user = token ? await verifyToken(token) : null;

  // 2. Create request-scoped loaders (IMPORTANT!)
  const loaders = createLoaders();

  // 3. Initialize data sources
  const dataSources = {
    users: new UserDataSource(db),
    posts: new PostDataSource(db),
  };

  // 4. Request metadata
  const requestId = req.headers['x-request-id'] || crypto.randomUUID();

  return {
    user,
    loaders,
    dataSources,
    requestId,
  };
};

// Apollo Server setup
const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: createContext,
});
```

### 4. Error Handling

```javascript
import { GraphQLError } from 'graphql';

const resolvers = {
  Mutation: {
    createUser: async (_, { input }, { dataSources, user }) => {
      // 1. Auth check
      if (!user) {
        throw new GraphQLError('Not authenticated', {
          extensions: { code: 'UNAUTHENTICATED' }
        });
      }

      // 2. Validation (return errors, don't throw)
      const validationErrors = validateInput(input);
      if (validationErrors.length > 0) {
        return { user: null, errors: validationErrors };
      }

      // 3. Business logic
      try {
        const newUser = await dataSources.users.create(input);
        return { user: newUser, errors: [] };
      } catch (error) {
        // Known error
        if (error.code === 'DUPLICATE_EMAIL') {
          return {
            user: null,
            errors: [{ field: 'email', message: 'Already exists' }]
          };
        }
        // Unknown error - throw
        throw new GraphQLError('Internal error', {
          extensions: { code: 'INTERNAL_ERROR' }
        });
      }
    },
  },
};
```

### 5. Subscription Resolvers

```javascript
import { PubSub, withFilter } from 'graphql-subscriptions';

const pubsub = new PubSub();

const resolvers = {
  Mutation: {
    sendMessage: async (_, { input }, { dataSources }) => {
      const message = await dataSources.messages.create(input);

      // Publish event
      pubsub.publish('MESSAGE_SENT', {
        messageSent: message,
        channelId: input.channelId,
      });

      return message;
    },
  },

  Subscription: {
    // Simple subscription
    userCreated: {
      subscribe: () => pubsub.asyncIterator(['USER_CREATED']),
    },

    // Filtered subscription
    messageSent: {
      subscribe: withFilter(
        () => pubsub.asyncIterator(['MESSAGE_SENT']),
        (payload, variables) => {
          return payload.channelId === variables.channelId;
        }
      ),
    },
  },
};
```

---

## Performance Targets

| Resolver Type | Target | Action if Exceeded |
|---------------|--------|-------------------|
| Simple field | < 10ms | Check DB indexes |
| DataLoader batch | < 50ms | Optimize query |
| Complex computation | < 200ms | Consider caching |
| Total request | < 500ms | Profile and optimize |

---

## Troubleshooting

| Issue | Symptom | Solution |
|-------|---------|----------|
| N+1 queries | Slow, many DB calls | Use DataLoader |
| Memory leak | Growing memory | Create loaders per request |
| Stale data | Wrong results | Clear DataLoader cache |
| Race condition | Intermittent errors | Don't mutate context |

### Debug Techniques

```javascript
// 1. Log DataLoader batches
const loader = new DataLoader(async (keys) => {
  console.log(`Batching ${keys.length} keys`);
  // ...
});

// 2. Time resolvers
const withTiming = (resolver) => async (...args) => {
  const start = Date.now();
  const result = await resolver(...args);
  console.log(`Took ${Date.now() - start}ms`);
  return result;
};

// 3. Request logging plugin
const loggingPlugin = {
  requestDidStart() {
    const start = Date.now();
    return {
      willSendResponse() {
        console.log(`Request took ${Date.now() - start}ms`);
      },
    };
  },
};
```

---

## Usage

```
Skill("graphql-resolvers")
```

## Related Skills
- `graphql-schema-design` - Schema that resolvers implement
- `graphql-apollo-server` - Server configuration
- `graphql-security` - Auth in resolvers

## Related Agent
- `03-graphql-resolvers` - For detailed guidance
