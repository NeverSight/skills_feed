---
name: graphql-api-development
description: Comprehensive guide for building GraphQL APIs including schema design, queries, mutations, subscriptions, resolvers, type system, error handling, authentication, authorization, caching strategies, and production best practices
tags: [graphql, api, schema, queries, mutations, subscriptions, resolvers, javascript, typescript, web-development, backend]
tier: tier-1
---

# GraphQL API Development

A comprehensive skill for building production-ready GraphQL APIs using graphql-js. Master schema design, type systems, resolvers, queries, mutations, subscriptions, authentication, authorization, caching, testing, and deployment strategies.

## When to Use This Skill

Use this skill when:

- Building a new API that requires flexible data fetching for web or mobile clients
- Replacing or augmenting REST APIs with more efficient data access patterns
- Developing APIs for applications with complex, nested data relationships
- Creating APIs that serve multiple client types (web, mobile, desktop) with different data needs
- Building real-time applications requiring subscriptions and live updates
- Designing APIs where clients need to specify exactly what data they need
- Developing GraphQL servers with Node.js and Express
- Implementing type-safe APIs with strong schema validation
- Creating self-documenting APIs with built-in introspection
- Building microservices that need to be composed into a unified API

## When GraphQL Excels Over REST

### GraphQL Advantages

1. **Precise Data Fetching**: Clients request exactly what they need, no over/under-fetching
2. **Single Request**: Fetch multiple resources in one roundtrip instead of multiple REST endpoints
3. **Strongly Typed**: Schema defines exact types, enabling validation and tooling
4. **Introspection**: Self-documenting API with queryable schema
5. **Versioning Not Required**: Add new fields without breaking existing queries
6. **Real-time Updates**: Built-in subscription support for live data
7. **Nested Resources**: Naturally handle complex relationships without N+1 queries
8. **Client-Driven**: Clients control data shape, reducing backend changes

### When to Stick with REST

- Simple CRUD operations with standard resources
- File uploads/downloads (GraphQL requires multipart handling)
- HTTP caching is critical (GraphQL typically uses POST)
- Team unfamiliar with GraphQL (learning curve)
- Existing REST infrastructure works well

## Core Concepts

### The GraphQL Type System

GraphQL's type system is its foundation. Every GraphQL API defines:

1. **Scalar Types**: Basic data types (String, Int, Float, Boolean, ID)
2. **Object Types**: Complex types with fields
3. **Query Type**: Entry point for read operations
4. **Mutation Type**: Entry point for write operations
5. **Subscription Type**: Entry point for real-time updates
6. **Input Types**: Complex inputs for mutations
7. **Enums**: Fixed set of values
8. **Interfaces**: Abstract types that objects implement
9. **Unions**: Types that can be one of several types
10. **Non-Null Types**: Types that cannot be null
11. **List Types**: Arrays of types

### Schema Definition

Two approaches for defining GraphQL schemas:

**1. Schema Definition Language (SDL)** - Declarative, readable:

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
  posts: [Post!]!
}
```

**2. Programmatic API** - Type-safe, programmatic:

```javascript
const UserType = new GraphQLObjectType({
  name: 'User',
  fields: {
    id: { type: new GraphQLNonNull(GraphQLID) },
    name: { type: new GraphQLNonNull(GraphQLString) },
    email: { type: new GraphQLNonNull(GraphQLString) },
    posts: { type: new GraphQLList(new GraphQLNonNull(PostType)) }
  }
});
```

### Resolvers

Resolvers are functions that return data for schema fields. Every field can have a resolver:

```javascript
const resolvers = {
  Query: {
    user: (parent, args, context, info) => {
      return context.db.findUserById(args.id);
    }
  },
  User: {
    posts: (user, args, context) => {
      return context.db.findPostsByAuthorId(user.id);
    }
  }
};
```

**Resolver Function Signature**:
- `parent`: The result from the parent resolver
- `args`: Arguments passed to the field
- `context`: Shared context (database, auth, etc.)
- `info`: Field-specific metadata

### Queries

Queries fetch data from your API:

```graphql
query GetUser {
  user(id: "123") {
    id
    name
    email
    posts {
      title
      content
    }
  }
}
```

### Mutations

Mutations modify data:

```graphql
mutation CreatePost {
  createPost(input: {
    title: "GraphQL is awesome"
    content: "Here's why..."
    authorId: "123"
  }) {
    id
    title
    author {
      name
    }
  }
}
```

### Subscriptions

Subscriptions enable real-time updates:

```graphql
subscription OnPostCreated {
  postCreated {
    id
    title
    author {
      name
    }
  }
}
```

## Schema Design Patterns

### Pattern 1: Input Types for Mutations

Always use input types for complex mutation arguments:

```graphql
input CreateUserInput {
  name: String!
  email: String!
  age: Int
  bio: String
}

type Mutation {
  createUser(input: CreateUserInput!): User!
}
```

**Why**: Easier to extend, better organization, reusable across mutations.

### Pattern 2: Interfaces for Shared Fields

Use interfaces when multiple types share fields:

```graphql
interface Node {
  id: ID!
  createdAt: String!
  updatedAt: String!
}

type User implements Node {
  id: ID!
  createdAt: String!
  updatedAt: String!
  name: String!
  email: String!
}

type Post implements Node {
  id: ID!
  createdAt: String!
  updatedAt: String!
  title: String!
  content: String
}
```

### Pattern 3: Unions for Polymorphic Returns

Use unions when a field can return different types:

```graphql
union SearchResult = User | Post | Comment

type Query {
  search(query: String!): [SearchResult!]!
}
```

### Pattern 4: Pagination Patterns

**Offset-based pagination**:

```graphql
type Query {
  posts(offset: Int, limit: Int): PostConnection!
}

type PostConnection {
  items: [Post!]!
  total: Int!
  hasMore: Boolean!
}
```

**Cursor-based pagination (Relay-style)**:

```graphql
type Query {
  posts(first: Int, after: String): PostConnection!
}

type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
}

type PostEdge {
  node: Post!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  endCursor: String
}
```

### Pattern 5: Error Handling

**Field-level errors**:

```graphql
type MutationPayload {
  success: Boolean!
  message: String
  user: User
  errors: [Error!]
}

type Error {
  field: String!
  message: String!
}
```

**Union-based error handling**:

```graphql
union CreateUserResult = User | ValidationError | DatabaseError

type ValidationError {
  field: String!
  message: String!
}
```

### Pattern 6: Versioning with Directives

Deprecate fields instead of versioning:

```graphql
type User {
  name: String! @deprecated(reason: "Use firstName and lastName")
  firstName: String!
  lastName: String!
}
```

## Query Optimization and Performance

### The N+1 Problem

**Problem**: Fetching nested data causes multiple database queries:

```javascript
// BAD: N+1 queries
const UserType = new GraphQLObjectType({
  name: 'User',
  fields: {
    posts: {
      type: new GraphQLList(PostType),
      resolve: (user) => {
        // This runs once PER user!
        return db.getPostsByUserId(user.id);
      }
    }
  }
});

// Query for 100 users = 1 query for users + 100 queries for posts = 101 queries
```

### DataLoader Solution

DataLoader batches and caches requests:

```javascript
import DataLoader from 'dataloader';

// Create DataLoader
const postLoader = new DataLoader(async (userIds) => {
  // Single query for all user IDs
  const posts = await db.getPostsByUserIds(userIds);

  // Group posts by userId
  const postsByUserId = {};
  posts.forEach(post => {
    if (!postsByUserId[post.authorId]) {
      postsByUserId[post.authorId] = [];
    }
    postsByUserId[post.authorId].push(post);
  });

  // Return in same order as userIds
  return userIds.map(id => postsByUserId[id] || []);
});

// Use in resolver
const UserType = new GraphQLObjectType({
  name: 'User',
  fields: {
    posts: {
      type: new GraphQLList(PostType),
      resolve: (user, args, context) => {
        return context.loaders.postLoader.load(user.id);
      }
    }
  }
});

// Add to context
const context = {
  loaders: {
    postLoader: new DataLoader(batchLoadPosts)
  }
};
```

### Query Complexity Analysis

Limit expensive queries:

```javascript
import { getComplexity, simpleEstimator } from 'graphql-query-complexity';

const complexity = getComplexity({
  schema,
  query,
  estimators: [
    simpleEstimator({ defaultComplexity: 1 })
  ]
});

if (complexity > 1000) {
  throw new Error('Query too complex');
}
```

### Depth Limiting

Prevent deeply nested queries:

```javascript
import depthLimit from 'graphql-depth-limit';

const server = new ApolloServer({
  schema,
  validationRules: [depthLimit(5)]
});
```

## Mutations and Input Validation

### Mutation Design Pattern

```graphql
input CreatePostInput {
  title: String!
  content: String!
  authorId: ID!
  tags: [String!]
}

type CreatePostPayload {
  post: Post
  errors: [UserError!]
  success: Boolean!
}

type UserError {
  message: String!
  field: String
}

type Mutation {
  createPost(input: CreatePostInput!): CreatePostPayload!
}
```

### Input Validation

```javascript
const Mutation = new GraphQLObjectType({
  name: 'Mutation',
  fields: {
    createPost: {
      type: CreatePostPayload,
      args: {
        input: { type: new GraphQLNonNull(CreatePostInput) }
      },
      resolve: async (_, { input }, context) => {
        // Validate input
        const errors = [];

        if (input.title.length < 3) {
          errors.push({
            field: 'title',
            message: 'Title must be at least 3 characters'
          });
        }

        if (input.content.length < 10) {
          errors.push({
            field: 'content',
            message: 'Content must be at least 10 characters'
          });
        }

        if (errors.length > 0) {
          return { errors, success: false, post: null };
        }

        // Create post
        const post = await context.db.createPost(input);
        return { post, errors: [], success: true };
      }
    }
  }
});
```

## Subscriptions and Real-time Updates

### Setting Up Subscriptions

```javascript
import { GraphQLObjectType, GraphQLString } from 'graphql';
import { PubSub } from 'graphql-subscriptions';

const pubsub = new PubSub();

const Subscription = new GraphQLObjectType({
  name: 'Subscription',
  fields: {
    postCreated: {
      type: PostType,
      subscribe: () => pubsub.asyncIterator(['POST_CREATED'])
    },
    messageReceived: {
      type: MessageType,
      args: {
        channelId: { type: new GraphQLNonNull(GraphQLID) }
      },
      subscribe: (_, { channelId }) => {
        return pubsub.asyncIterator([`MESSAGE_${channelId}`]);
      }
    }
  }
});
```

### Publishing Events

```javascript
const Mutation = new GraphQLObjectType({
  name: 'Mutation',
  fields: {
    createPost: {
      type: PostType,
      args: {
        input: { type: new GraphQLNonNull(CreatePostInput) }
      },
      resolve: async (_, { input }, context) => {
        const post = await context.db.createPost(input);

        // Publish to subscribers
        pubsub.publish('POST_CREATED', { postCreated: post });

        return post;
      }
    }
  }
});
```

### WebSocket Server Setup

```javascript
import { createServer } from 'http';
import { WebSocketServer } from 'ws';
import { useServer } from 'graphql-ws/lib/use/ws';
import { execute, subscribe } from 'graphql';
import express from 'express';

const app = express();
const httpServer = createServer(app);

// WebSocket server for subscriptions
const wsServer = new WebSocketServer({
  server: httpServer,
  path: '/graphql'
});

useServer(
  {
    schema,
    execute,
    subscribe,
    context: (ctx) => {
      // Access connection params, headers
      return {
        userId: ctx.connectionParams?.userId,
        db: database
      };
    }
  },
  wsServer
);

httpServer.listen(4000);
```

## Authentication and Authorization

### Context-Based Authentication

```javascript
import jwt from 'jsonwebtoken';

// Middleware to extract user
const authMiddleware = async (req) => {
  const token = req.headers.authorization?.replace('Bearer ', '');

  if (!token) {
    return { user: null };
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    const user = await db.findUserById(decoded.userId);
    return { user };
  } catch (error) {
    return { user: null };
  }
};

// Add to GraphQL context
app.all('/graphql', async (req, res) => {
  const auth = await authMiddleware(req);

  createHandler({
    schema,
    context: {
      user: auth.user,
      db: database
    }
  })(req, res);
});
```

### Resolver-Level Authorization

```javascript
const Query = new GraphQLObjectType({
  name: 'Query',
  fields: {
    me: {
      type: UserType,
      resolve: (_, __, context) => {
        if (!context.user) {
          throw new Error('Authentication required');
        }
        return context.user;
      }
    },
    adminData: {
      type: GraphQLString,
      resolve: (_, __, context) => {
        if (!context.user) {
          throw new Error('Authentication required');
        }

        if (context.user.role !== 'admin') {
          throw new Error('Admin access required');
        }

        return 'Secret admin data';
      }
    }
  }
});
```

### Field-Level Authorization

```javascript
const PostType = new GraphQLObjectType({
  name: 'Post',
  fields: {
    title: { type: GraphQLString },
    content: { type: GraphQLString },
    draft: {
      type: GraphQLBoolean,
      resolve: (post, args, context) => {
        // Only author can see draft status
        if (post.authorId !== context.user?.id) {
          return null;
        }
        return post.draft;
      }
    }
  }
});
```

### Directive-Based Authorization

```graphql
directive @auth(requires: Role = USER) on FIELD_DEFINITION

enum Role {
  USER
  ADMIN
  MODERATOR
}

type Query {
  publicData: String
  userData: String @auth(requires: USER)
  adminData: String @auth(requires: ADMIN)
}
```

```javascript
import { mapSchema, getDirective, MapperKind } from '@graphql-tools/utils';

function authDirective(schema, directiveName) {
  return mapSchema(schema, {
    [MapperKind.OBJECT_FIELD]: (fieldConfig) => {
      const authDirective = getDirective(schema, fieldConfig, directiveName)?.[0];

      if (authDirective) {
        const { requires } = authDirective;
        const { resolve = defaultFieldResolver } = fieldConfig;

        fieldConfig.resolve = async (source, args, context, info) => {
          if (!context.user) {
            throw new Error('Authentication required');
          }

          if (context.user.role !== requires) {
            throw new Error(`${requires} role required`);
          }

          return resolve(source, args, context, info);
        };
      }

      return fieldConfig;
    }
  });
}
```

## Caching Strategies

### In-Memory Caching

```javascript
import { LRUCache } from 'lru-cache';

const cache = new LRUCache({
  max: 500,
  ttl: 1000 * 60 * 5 // 5 minutes
});

const Query = new GraphQLObjectType({
  name: 'Query',
  fields: {
    product: {
      type: ProductType,
      args: { id: { type: new GraphQLNonNull(GraphQLID) } },
      resolve: async (_, { id }, context) => {
        const cacheKey = `product:${id}`;
        const cached = cache.get(cacheKey);

        if (cached) {
          return cached;
        }

        const product = await context.db.findProductById(id);
        cache.set(cacheKey, product);
        return product;
      }
    }
  }
});
```

### Redis Caching

```javascript
import Redis from 'ioredis';

const redis = new Redis({
  host: process.env.REDIS_HOST,
  port: process.env.REDIS_PORT
});

const Query = new GraphQLObjectType({
  name: 'Query',
  fields: {
    user: {
      type: UserType,
      args: { id: { type: new GraphQLNonNull(GraphQLID) } },
      resolve: async (_, { id }, context) => {
        const cacheKey = `user:${id}`;

        // Check cache
        const cached = await redis.get(cacheKey);
        if (cached) {
          return JSON.parse(cached);
        }

        // Fetch from database
        const user = await context.db.findUserById(id);

        // Cache for 10 minutes
        await redis.setex(cacheKey, 600, JSON.stringify(user));

        return user;
      }
    }
  }
});
```

### Cache Invalidation

```javascript
const Mutation = new GraphQLObjectType({
  name: 'Mutation',
  fields: {
    updateUser: {
      type: UserType,
      args: {
        id: { type: new GraphQLNonNull(GraphQLID) },
        input: { type: new GraphQLNonNull(UpdateUserInput) }
      },
      resolve: async (_, { id, input }, context) => {
        const user = await context.db.updateUser(id, input);

        // Invalidate cache
        const cacheKey = `user:${id}`;
        await redis.del(cacheKey);

        // Also invalidate list caches
        await redis.del('users:all');

        return user;
      }
    }
  }
});
```

## Error Handling

### Custom Error Classes

```javascript
class AuthenticationError extends Error {
  constructor(message) {
    super(message);
    this.name = 'AuthenticationError';
    this.extensions = { code: 'UNAUTHENTICATED' };
  }
}

class ForbiddenError extends Error {
  constructor(message) {
    super(message);
    this.name = 'ForbiddenError';
    this.extensions = { code: 'FORBIDDEN' };
  }
}

class ValidationError extends Error {
  constructor(message, fields) {
    super(message);
    this.name = 'ValidationError';
    this.extensions = {
      code: 'BAD_USER_INPUT',
      fields
    };
  }
}
```

### Error Formatting

```javascript
import { formatError } from 'graphql';

const customFormatError = (error) => {
  // Log error for monitoring
  console.error('GraphQL Error:', {
    message: error.message,
    locations: error.locations,
    path: error.path,
    extensions: error.extensions
  });

  // Don't expose internal errors to clients
  if (error.message.startsWith('Database')) {
    return {
      message: 'Internal server error',
      extensions: { code: 'INTERNAL_SERVER_ERROR' }
    };
  }

  return formatError(error);
};

const server = new ApolloServer({
  schema,
  formatError: customFormatError
});
```

### Graceful Error Responses

```javascript
const Query = new GraphQLObjectType({
  name: 'Query',
  fields: {
    user: {
      type: UserType,
      args: { id: { type: new GraphQLNonNull(GraphQLID) } },
      resolve: async (_, { id }, context) => {
        try {
          const user = await context.db.findUserById(id);

          if (!user) {
            throw new Error(`User with ID ${id} not found`);
          }

          return user;
        } catch (error) {
          // Log error
          console.error('Error fetching user:', error);

          // Re-throw with user-friendly message
          if (error.code === 'ECONNREFUSED') {
            throw new Error('Unable to connect to database');
          }

          throw error;
        }
      }
    }
  }
});
```

## Testing GraphQL APIs

### Unit Testing Resolvers

```javascript
import { describe, it, expect, jest } from '@jest/globals';

describe('User resolver', () => {
  it('returns user by ID', async () => {
    const mockDb = {
      findUserById: jest.fn().mockResolvedValue({
        id: '1',
        name: 'Alice',
        email: 'alice@example.com'
      })
    };

    const context = { db: mockDb };
    const result = await userResolver.resolve(null, { id: '1' }, context);

    expect(mockDb.findUserById).toHaveBeenCalledWith('1');
    expect(result).toEqual({
      id: '1',
      name: 'Alice',
      email: 'alice@example.com'
    });
  });

  it('throws error for non-existent user', async () => {
    const mockDb = {
      findUserById: jest.fn().mockResolvedValue(null)
    };

    const context = { db: mockDb };

    await expect(
      userResolver.resolve(null, { id: '999' }, context)
    ).rejects.toThrow('User with ID 999 not found');
  });
});
```

### Integration Testing

```javascript
import { graphql } from 'graphql';
import { schema } from './schema';

describe('GraphQL Schema', () => {
  it('executes user query', async () => {
    const query = `
      query {
        user(id: "1") {
          id
          name
          email
        }
      }
    `;

    const result = await graphql({
      schema,
      source: query,
      contextValue: {
        db: mockDatabase,
        user: null
      }
    });

    expect(result.errors).toBeUndefined();
    expect(result.data?.user).toEqual({
      id: '1',
      name: 'Alice',
      email: 'alice@example.com'
    });
  });

  it('handles authentication errors', async () => {
    const query = `
      query {
        me {
          id
          name
        }
      }
    `;

    const result = await graphql({
      schema,
      source: query,
      contextValue: {
        db: mockDatabase,
        user: null
      }
    });

    expect(result.errors).toBeDefined();
    expect(result.errors[0].message).toBe('Authentication required');
  });
});
```

### Testing with Apollo Server

```javascript
import { ApolloServer } from '@apollo/server';

const testServer = new ApolloServer({
  schema,
});

describe('User queries', () => {
  it('fetches user successfully', async () => {
    const response = await testServer.executeOperation({
      query: `
        query GetUser($id: ID!) {
          user(id: $id) {
            id
            name
          }
        }
      `,
      variables: { id: '1' }
    });

    expect(response.body.singleResult.errors).toBeUndefined();
    expect(response.body.singleResult.data?.user).toMatchObject({
      id: '1',
      name: expect.any(String)
    });
  });
});
```

## Production Best Practices

### Schema Organization

```
src/
├── schema/
│   ├── index.js          # Combine all types
│   ├── types/
│   │   ├── user.js       # User type and resolvers
│   │   ├── post.js       # Post type and resolvers
│   │   └── comment.js    # Comment type and resolvers
│   ├── queries/
│   │   ├── user.js       # User queries
│   │   └── post.js       # Post queries
│   ├── mutations/
│   │   ├── user.js       # User mutations
│   │   └── post.js       # Post mutations
│   └── subscriptions/
│       └── post.js       # Post subscriptions
├── directives/
│   └── auth.js           # Authorization directive
├── utils/
│   ├── loaders.js        # DataLoader instances
│   └── context.js        # Context builder
└── server.js             # Server setup
```

### Monitoring and Logging

```javascript
import { ApolloServerPluginLandingPageGraphQLPlayground } from '@apollo/server-plugin-landing-page-graphql-playground';

const server = new ApolloServer({
  schema,
  plugins: [
    // Request logging
    {
      async requestDidStart(requestContext) {
        console.log('Request started:', requestContext.request.query);

        return {
          async didEncounterErrors(ctx) {
            console.error('Errors:', ctx.errors);
          },
          async willSendResponse(ctx) {
            console.log('Response sent');
          }
        };
      }
    },

    // Performance monitoring
    {
      async requestDidStart() {
        const start = Date.now();

        return {
          async willSendResponse() {
            const duration = Date.now() - start;
            console.log(`Request duration: ${duration}ms`);
          }
        };
      }
    }
  ]
});
```

### Rate Limiting

```javascript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per window
  message: 'Too many requests, please try again later'
});

app.use('/graphql', limiter);
```

### Query Whitelisting

```javascript
const allowedQueries = new Set([
  'query GetUser { user(id: $id) { id name email } }',
  'mutation CreatePost { createPost(input: $input) { id title } }'
]);

const validateQuery = (query) => {
  const normalized = query.replace(/\s+/g, ' ').trim();
  if (!allowedQueries.has(normalized)) {
    throw new Error('Query not whitelisted');
  }
};
```

### Security Headers

```javascript
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'"],
    }
  },
  crossOriginEmbedderPolicy: false
}));
```

## Advanced Patterns

### Federation (Microservices)

```javascript
import { buildSubgraphSchema } from '@apollo/subgraph';

// Users service
const userSchema = buildSubgraphSchema({
  typeDefs: `
    type User @key(fields: "id") {
      id: ID!
      name: String!
      email: String!
    }
  `,
  resolvers: {
    User: {
      __resolveReference(user) {
        return findUserById(user.id);
      }
    }
  }
});

// Posts service
const postSchema = buildSubgraphSchema({
  typeDefs: `
    type Post {
      id: ID!
      title: String!
      author: User!
    }

    extend type User @key(fields: "id") {
      id: ID! @external
      posts: [Post!]!
    }
  `,
  resolvers: {
    Post: {
      author(post) {
        return { __typename: 'User', id: post.authorId };
      }
    },
    User: {
      posts(user) {
        return findPostsByAuthorId(user.id);
      }
    }
  }
});
```

### Custom Scalars

```javascript
import { GraphQLScalarType, Kind } from 'graphql';

const DateTimeScalar = new GraphQLScalarType({
  name: 'DateTime',
  description: 'ISO-8601 DateTime string',

  serialize(value) {
    // Send to client
    return value instanceof Date ? value.toISOString() : null;
  },

  parseValue(value) {
    // From variables
    return new Date(value);
  },

  parseLiteral(ast) {
    // From query string
    if (ast.kind === Kind.STRING) {
      return new Date(ast.value);
    }
    return null;
  }
});

// Use in schema
const schema = new GraphQLSchema({
  types: [DateTimeScalar],
  query: new GraphQLObjectType({
    name: 'Query',
    fields: {
      now: {
        type: DateTimeScalar,
        resolve: () => new Date()
      }
    }
  })
});
```

### Batch Operations

```javascript
const Mutation = new GraphQLObjectType({
  name: 'Mutation',
  fields: {
    batchCreateUsers: {
      type: new GraphQLList(UserType),
      args: {
        inputs: {
          type: new GraphQLNonNull(
            new GraphQLList(new GraphQLNonNull(CreateUserInput))
          )
        }
      },
      resolve: async (_, { inputs }, context) => {
        const users = await Promise.all(
          inputs.map(input => context.db.createUser(input))
        );
        return users;
      }
    }
  }
});
```

## Common Patterns Summary

1. **Use Input Types**: For all mutations with multiple arguments
2. **Implement DataLoader**: Solve N+1 queries for nested data
3. **Add Pagination**: For list fields that can grow unbounded
4. **Handle Errors Gracefully**: Return user-friendly error messages
5. **Validate Inputs**: At resolver level before database operations
6. **Use Context for Shared State**: Database, authentication, loaders
7. **Implement Authorization**: At resolver or directive level
8. **Cache Aggressively**: Use Redis or in-memory for frequently accessed data
9. **Monitor Performance**: Track query complexity and execution time
10. **Version with @deprecated**: Never break existing queries
11. **Test Thoroughly**: Unit test resolvers, integration test queries
12. **Document Schema**: Use descriptions in SDL
13. **Use Non-Null Wisely**: Only for truly required fields
14. **Organize Schema**: Split into modules by domain
15. **Secure Production**: Rate limiting, query whitelisting, depth limiting

## Resources and Tools

### Essential Libraries

- **graphql-js**: Core GraphQL implementation
- **express**: Web server framework
- **graphql-http**: HTTP handler for GraphQL
- **dataloader**: Batching and caching
- **graphql-ws**: WebSocket server for subscriptions
- **graphql-scalars**: Common custom scalars
- **graphql-tools**: Schema manipulation utilities

### Development Tools

- **GraphiQL**: In-browser GraphQL IDE
- **GraphQL Playground**: Advanced GraphQL IDE
- **Apollo Studio**: Schema registry and monitoring
- **GraphQL Code Generator**: Generate TypeScript types
- **eslint-plugin-graphql**: Lint GraphQL queries

### Learning Resources

- GraphQL Official Documentation: https://graphql.org
- GraphQL.js Repository: https://github.com/graphql/graphql-js
- How to GraphQL: https://howtographql.com
- Apollo GraphQL: https://apollographql.com
- GraphQL Weekly Newsletter: https://graphqlweekly.com

---

**Skill Version**: 1.0.0
**Last Updated**: October 2025
**Skill Category**: API Development, Backend, GraphQL, Web Development
**Compatible With**: Node.js, Express, TypeScript, JavaScript
