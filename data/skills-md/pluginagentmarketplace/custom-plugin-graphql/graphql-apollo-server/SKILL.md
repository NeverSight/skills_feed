---
name: graphql-apollo-server
description: Build production GraphQL servers with Apollo Server, plugins, and federation
sasmp_version: "1.3.0"
bonded_agent: 04-graphql-apollo-server
bond_type: PRIMARY_BOND
version: "2.0.0"
complexity: intermediate
estimated_time: "4-6 hours"
prerequisites: ["graphql-fundamentals", "graphql-resolvers"]
---

# Apollo Server Skill

> Deploy production-ready GraphQL APIs

## Overview

Learn to build scalable GraphQL servers with Apollo Server 4, including middleware integration, custom plugins, federation, and production best practices.

---

## Quick Reference

| Feature | Package | Purpose |
|---------|---------|---------|
| Server | `@apollo/server` | Core server |
| Express | `@apollo/server/express4` | Express integration |
| Plugins | `@apollo/server/plugin/*` | Extensibility |
| Federation | `@apollo/subgraph` | Microservices |

---

## Core Setup

### 1. Basic Server (Express)

```typescript
import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@apollo/server/express4';
import { ApolloServerPluginDrainHttpServer } from '@apollo/server/plugin/drainHttpServer';
import express from 'express';
import http from 'http';
import cors from 'cors';

interface Context {
  user: User | null;
  dataSources: DataSources;
}

async function startServer() {
  const app = express();
  const httpServer = http.createServer(app);

  const server = new ApolloServer<Context>({
    typeDefs,
    resolvers,
    plugins: [
      // Graceful shutdown
      ApolloServerPluginDrainHttpServer({ httpServer }),
    ],
  });

  await server.start();

  app.use(
    '/graphql',
    cors({ origin: ['http://localhost:3000'], credentials: true }),
    express.json(),
    expressMiddleware(server, {
      context: async ({ req }) => ({
        user: await getUser(req),
        dataSources: createDataSources(),
      }),
    }),
  );

  httpServer.listen(4000, () => {
    console.log('Server ready at http://localhost:4000/graphql');
  });
}
```

### 2. Production Configuration

```typescript
const server = new ApolloServer<Context>({
  typeDefs,
  resolvers,

  // Error formatting
  formatError: (error) => {
    console.error('GraphQL Error:', error);

    // Hide internal errors in production
    if (process.env.NODE_ENV === 'production') {
      if (error.extensions?.code === 'INTERNAL_SERVER_ERROR') {
        return { message: 'Internal error', extensions: { code: 'INTERNAL_ERROR' } };
      }
    }
    return error;
  },

  // Disable introspection in production
  introspection: process.env.NODE_ENV !== 'production',

  plugins: [
    ApolloServerPluginDrainHttpServer({ httpServer }),
    loggingPlugin,
    complexityPlugin,
  ],
});
```

### 3. Custom Plugins

```typescript
import { ApolloServerPlugin } from '@apollo/server';

// Logging plugin
const loggingPlugin: ApolloServerPlugin<Context> = {
  async requestDidStart({ request, contextValue }) {
    const start = Date.now();
    console.log('Request:', request.operationName);

    return {
      async willSendResponse() {
        console.log(`Completed in ${Date.now() - start}ms`);
      },

      async didEncounterErrors({ errors }) {
        errors.forEach(e => console.error('Error:', e.message));
      },
    };
  },
};

// Query complexity plugin
import { getComplexity, simpleEstimator } from 'graphql-query-complexity';

const complexityPlugin: ApolloServerPlugin<Context> = {
  async requestDidStart() {
    return {
      async didResolveOperation({ schema, document, request }) {
        const complexity = getComplexity({
          schema,
          query: document,
          variables: request.variables,
          estimators: [simpleEstimator({ defaultComplexity: 1 })],
        });

        if (complexity > 1000) {
          throw new GraphQLError('Query too complex');
        }
      },
    };
  },
};
```

### 4. Federation (Subgraph)

```typescript
import { buildSubgraphSchema } from '@apollo/subgraph';
import { gql } from 'graphql-tag';

const typeDefs = gql`
  extend schema
    @link(url: "https://specs.apollo.dev/federation/v2.0",
          import: ["@key", "@shareable", "@external"])

  type Query {
    user(id: ID!): User
  }

  type User @key(fields: "id") {
    id: ID!
    name: String!
    email: String!
  }
`;

const resolvers = {
  Query: {
    user: (_, { id }) => users.find(u => u.id === id),
  },
  User: {
    __resolveReference: (user) => users.find(u => u.id === user.id),
  },
};

const server = new ApolloServer({
  schema: buildSubgraphSchema({ typeDefs, resolvers }),
});
```

### 5. Response Caching

```typescript
import responseCachePlugin from '@apollo/server-plugin-response-cache';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    responseCachePlugin({
      // Cache key includes user ID for personalized data
      sessionId: ({ contextValue }) => contextValue.user?.id || null,
    }),
  ],
});

// Schema hints
const typeDefs = gql`
  type Query {
    # Cache for 1 hour
    popularPosts: [Post!]! @cacheControl(maxAge: 3600)

    # Private, user-specific
    me: User @cacheControl(maxAge: 0, scope: PRIVATE)
  }
`;
```

### 6. Health Checks

```typescript
// Health endpoint
app.get('/health', async (req, res) => {
  const checks = {
    server: 'healthy',
    database: await checkDb(),
    redis: await checkRedis(),
  };

  const healthy = Object.values(checks).every(c => c === 'healthy');
  res.status(healthy ? 200 : 503).json(checks);
});

// Readiness endpoint
app.get('/ready', (req, res) => {
  res.status(serverReady ? 200 : 503).json({ ready: serverReady });
});
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| CORS errors | Missing middleware | Add cors() before expressMiddleware |
| 503 on shutdown | No drain | Add DrainHttpServer plugin |
| Memory leak | Global loaders | Create per-request |
| Slow startup | Large schema | Use schema caching |

### Debug Commands

```bash
# Test server
curl http://localhost:4000/health

# Test GraphQL
curl -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __typename }"}'

# Introspection
curl -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { types { name } } }"}'
```

---

## Usage

```
Skill("graphql-apollo-server")
```

## Related Skills
- `graphql-resolvers` - Resolver implementation
- `graphql-security` - Security configuration
- `graphql-codegen` - Type generation

## Related Agent
- `04-graphql-apollo-server` - For detailed guidance
