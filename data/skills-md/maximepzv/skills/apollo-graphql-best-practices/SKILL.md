---
name: apollo-graphql-best-practices
description: Best practices for Apollo GraphQL development including Apollo Client (React hooks, caching, error handling) and Apollo Server (schema design, resolvers, context, plugins). Use when writing, reviewing, or refactoring GraphQL code with Apollo, setting up Apollo Client/Server, implementing queries/mutations, configuring cache policies, or handling GraphQL errors.
---

# Apollo GraphQL Best Practices

## When to Apply

Use this skill when:
- Setting up a new Apollo Client or Apollo Server project
- Writing GraphQL queries, mutations, or subscriptions
- Implementing React components with `useQuery`, `useMutation`, or `useLazyQuery`
- Configuring cache policies, type policies, or pagination
- Designing GraphQL schemas or writing resolvers
- Handling GraphQL or network errors
- Optimizing GraphQL performance (N+1 queries, caching, batching)
- Reviewing or refactoring existing Apollo GraphQL code

---

## Apollo Client

### Client Setup

Configure `ApolloClient` with `InMemoryCache` and appropriate type policies:

```typescript
import { ApolloClient, InMemoryCache, HttpLink } from "@apollo/client";

const client = new ApolloClient({
  link: new HttpLink({ uri: "/graphql" }),
  cache: new InMemoryCache({
    typePolicies: {
      Query: {
        fields: {
          // Define field policies for pagination, merging, etc.
        },
      },
      // Custom key fields for entity identification
      User: {
        keyFields: ["email"], // Use email instead of id
      },
    },
  }),
});
```

### Queries with useQuery

```typescript
import { useQuery, gql } from "@apollo/client";

const GET_DATA = gql`
  query GetData($id: ID!) {
    item(id: $id) {
      id
      name
    }
  }
`;

function Component({ id }: { id: string }) {
  const { data, loading, error } = useQuery(GET_DATA, {
    variables: { id },
    fetchPolicy: "cache-first", // Default, use cache when available
  });

  if (loading) return <Loading />;
  if (error) return <Error message={error.message} />;
  return <Display data={data} />;
}
```

### Mutations with useMutation

Update cache after mutations using `update` callback:

```typescript
import { useMutation, gql } from "@apollo/client";

const ADD_ITEM = gql`
  mutation AddItem($input: ItemInput!) {
    addItem(input: $input) {
      id
      name
    }
  }
`;

function AddItemForm() {
  const [addItem, { loading }] = useMutation(ADD_ITEM, {
    update(cache, { data: { addItem } }) {
      cache.modify({
        fields: {
          items(existingItems = []) {
            const newItemRef = cache.writeFragment({
              data: addItem,
              fragment: gql`
                fragment NewItem on Item {
                  id
                  name
                }
              `,
            });
            return [...existingItems, newItemRef];
          },
        },
      });
    },
    // Or use refetchQueries for simpler cases
    // refetchQueries: [{ query: GET_ITEMS }],
  });

  return (
    <form onSubmit={(e) => {
      e.preventDefault();
      addItem({ variables: { input: { name: "New Item" } } });
    }}>
      <button type="submit" disabled={loading}>Add</button>
    </form>
  );
}
```

### Error Handling

GraphQL can return partial data with errors (unlike REST where a single error fails the entire request). Use `errorPolicy` to control this behavior:

| Policy | Behavior |
|--------|----------|
| `none` | Treat any GraphQL error as a network error, discard data (default) |
| `ignore` | Ignore GraphQL errors, return only data |
| `all` | Return both data and errors, enabling partial data rendering |

```typescript
import { useQuery } from "@apollo/client";

function Component() {
  const { data, error } = useQuery(QUERY, {
    errorPolicy: "all" // Receive partial data with errors
  });

  if (error) {
    // Check if we have partial data to display
    if (data) {
      // Render partial data with error notification
      return (
        <div>
          <ErrorBanner message={error.message} />
          <Display data={data} />
        </div>
      );
    }
    // No data at all - show full error
    if (error.networkError) {
      return <div>Network error: {error.message}</div>;
    }
    return <div>Error: {error.graphQLErrors[0]?.message}</div>;
  }

  return <div>{data?.field}</div>;
}
```

### Cache Type Policies

Configure cache normalization, custom identifiers, and field merging:

```typescript
const cache = new InMemoryCache({
  typePolicies: {
    Query: {
      fields: {
        // Offset-based pagination with proper merging
        items: {
          keyArgs: ["filter"], // Cache separately per filter value
          merge(existing = [], incoming, { args }) {
            const offset = args?.offset ?? 0;
            const merged = existing.slice(0);
            for (let i = 0; i < incoming.length; i++) {
              merged[offset + i] = incoming[i];
            }
            return merged;
          },
        },
      },
    },
    // Custom cache key using different field than 'id'
    User: {
      keyFields: ["email"], // Use email as unique identifier
    },
    // Entities without id field
    Token: {
      keyFields: false, // Treat as singleton (no normalization)
    },
    // Composite key for join tables
    OrderItem: {
      keyFields: ["orderId", "productId"],
    },
  },
});
```

**Key concepts:**
- **Cache normalization**: Apollo stores objects in a flat lookup table using `__typename:id` as the cache key
- **keyFields**: Customize which fields identify an entity (default is `id` or `_id`)
- **keyArgs**: Control which arguments create separate cache entries
- **merge**: Define how to combine existing and incoming data (essential for pagination)

### Fetch Policies

| Policy | Behavior |
|--------|----------|
| `cache-first` | Read cache, fetch if missing (default) |
| `cache-only` | Only read cache, never fetch |
| `network-only` | Always fetch, update cache |
| `no-cache` | Always fetch, don't cache |
| `cache-and-network` | Return cache immediately, then fetch |

---

## Apollo Server

### Server Setup

```typescript
import { ApolloServer } from "@apollo/server";
import { startStandaloneServer } from "@apollo/server/standalone";

interface Context {
  user?: User;
  db: Database;
}

const server = new ApolloServer<Context>({
  typeDefs,
  resolvers,
});

const { url } = await startStandaloneServer(server, {
  context: async ({ req }) => ({
    user: await getUserFromToken(req.headers.authorization),
    db: await getDatabase(),
  }),
  listen: { port: 4000 },
});
```

### Schema Design Principles

1. **Use non-nullable by default** - Add `!` unless field can legitimately be null
2. **Prefer specific types** - Use `ID!` for identifiers, custom scalars for dates
3. **Design for the client** - Structure schema around UI needs, not database schema
4. **Use input types for mutations** - Group related arguments

```graphql
type Query {
  user(id: ID!): User
  users(filter: UserFilter, pagination: Pagination): UserConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
}

input CreateUserInput {
  email: String!
  name: String!
}

type CreateUserPayload {
  user: User
  errors: [Error!]
}
```

### Resolvers

```typescript
const resolvers = {
  Query: {
    user: async (_, { id }, context) => {
      return context.db.users.findById(id);
    },
  },
  Mutation: {
    createUser: async (_, { input }, context) => {
      if (!context.user) {
        throw new GraphQLError("Not authenticated", {
          extensions: { code: "UNAUTHENTICATED" },
        });
      }
      const user = await context.db.users.create(input);
      return { user, errors: [] };
    },
  },
  // Field resolvers for computed/related data
  User: {
    posts: (parent, _, context) => {
      return context.db.posts.findByUserId(parent.id);
    },
  },
};
```

### Error Handling

Throw `GraphQLError` with descriptive codes:

```typescript
import { GraphQLError } from "graphql";

// In resolver
if (!user) {
  throw new GraphQLError("User not found", {
    extensions: {
      code: "NOT_FOUND",
      argumentName: "id",
    },
  });
}

// In context for auth errors
context: async ({ req }) => {
  const user = await getUser(req);
  if (!user) {
    throw new GraphQLError("Authentication required", {
      extensions: {
        code: "UNAUTHENTICATED",
        http: { status: 401 },
      },
    });
  }
  return { user };
};
```

### Standard Error Codes

| Code | Use Case |
|------|----------|
| `UNAUTHENTICATED` | Missing or invalid authentication |
| `FORBIDDEN` | Authenticated but not authorized |
| `BAD_USER_INPUT` | Invalid argument values |
| `NOT_FOUND` | Requested resource doesn't exist |
| `INTERNAL_SERVER_ERROR` | Unexpected server errors |

---

## Performance Tips

1. **Use DataLoader** - Batch and cache database calls to avoid N+1 queries
2. **Implement pagination** - Never return unbounded lists
3. **Use persisted queries** - Reduce request size in production
4. **Enable APM** - Use Apollo Studio for query performance monitoring
5. **Lazy load fragments** - Split large queries with `@defer` directive
6. **Configure cache TTL** - Set appropriate `maxAge` for cached responses
7. **Limit query depth** - Prevent deeply nested queries that can cause performance issues
8. **Set query complexity limits** - Assign costs to fields and reject overly complex queries

---

## Security Best Practices

1. **Query depth limiting** - Prevent malicious deeply nested queries
2. **Query complexity analysis** - Assign costs to fields, reject queries exceeding threshold
3. **Rate limiting** - Throttle requests per client/IP
4. **Disable introspection in production** - Hide schema from unauthorized users
5. **Input validation** - Validate all user inputs in resolvers
6. **Field-level authorization** - Check permissions in field resolvers, not just at query level

```typescript
// Example: formatError to hide internal errors in production
const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: process.env.NODE_ENV !== "production",
  formatError: (error) => {
    // Log full error internally
    console.error(error);

    // Don't expose internal errors to clients
    if (error.extensions?.code === "INTERNAL_SERVER_ERROR") {
      return new GraphQLError("Internal server error", {
        extensions: { code: "INTERNAL_SERVER_ERROR" },
      });
    }
    return error;
  },
});
```

---

## Relay-Style Patterns

### Global IDs

Use base64-encoded `type:uuid` format for globally unique identifiers. This follows the [Relay Global Object Identification Specification](https://relay.dev/graphql/objectidentification.htm).

**Benefits:**
- Enables efficient client-side caching and data refetching
- Allows `node(id: ID!)` query to fetch any entity by ID
- Type information embedded in ID prevents accidental cross-type queries
- Libraries like Relay can automatically generate pagination and refetch queries

```typescript
// utils/globalId.ts
export type GlobalIdType = "user" | "request" | "classified" | "purchase";

export function encodeGlobalId(type: GlobalIdType, uuid: string): string {
  return Buffer.from(`${type}:${uuid}`).toString("base64");
}

export function decodeGlobalId(globalId: string): { type: string; uuid: string } {
  const decoded = Buffer.from(globalId, "base64").toString("utf-8");
  const [type, uuid] = decoded.split(":");

  if (!type || !uuid) {
    throw new Error("Invalid global ID format");
  }

  return { type, uuid };
}

// Examples
encodeGlobalId("request", "abc-123"); // -> "cmVxdWVzdDphYmMtMTIz"
decodeGlobalId("cmVxdWVzdDphYmMtMTIz"); // -> { type: 'request', uuid: 'abc-123' }
```

### Node Interface

Implement the Node interface for unified entity fetching. This is a core pattern from the [Relay specification](https://relay.dev/graphql/objectidentification.htm) that provides:

- A standard way to refetch any object by its ID
- Efficient cache management for client libraries
- Type-safe polymorphic queries

```graphql
# schema/node.graphql
interface Node {
  id: ID!
}

extend type Query {
  """
  Fetch any entity by its global ID.
  Returns null if the ID is invalid or the entity doesn't exist.
  """
  node(id: ID!): Node
}
```

```typescript
// resolvers/node.ts
export const nodeResolvers = {
  Query: {
    async node(parent: any, { id }: { id: string }, context: GraphQLContext) {
      try {
        const { type, uuid } = decodeGlobalId(id);

        switch (type) {
          case "request":
            return context.loaders.request.load(uuid);
          case "classified":
            return context.loaders.classified.load(uuid);
          case "purchase":
            return context.loaders.purchase.load(uuid);
          default:
            return null;
        }
      } catch (error) {
        return null; // Silent failure for invalid IDs
      }
    },
  },

  Node: {
    __resolveType(obj: any) {
      // Detect type based on unique fields or __typename
      if (obj.__typename) return obj.__typename;
      if ("condition" in obj && "priceMinimum" in obj) return "Request";
      if ("platformConfigId" in obj && "visibilityStatus" in obj) return "Classified";
      if ("buyerEmail" in obj || "shippingAddress" in obj) return "Purchase";
      return null;
    },
  },
};
```

### Entity Type with Global ID

```graphql
type Request implements Node {
  id: ID!  # Global ID (base64 encoded)
  title: String!
  description: String!
  # ... other fields
}
```

```typescript
// resolvers/request.ts
Request: {
  // Encode database UUID to global ID
  id(request: any) {
    return encodeGlobalId("request", request.id);
  },
}
```

### DataLoaders for Batching

Essential for efficient Node queries and avoiding N+1 problems. The N+1 problem occurs when fetching a list of items (1 query), then fetching related data for each item individually (N queries).

**Key DataLoader principles:**
- Create fresh DataLoaders per request (never share across requests)
- Always return results in the same order as input keys
- Use caching within a single request to deduplicate identical fetches
- Set `maxBatchSize` to prevent overly large queries

```typescript
// dataloaders/request.loader.ts
import DataLoader from "dataloader";

export function createRequestLoader(db: Database) {
  return new DataLoader<string, any>(
    async (uuids) => {
      // Batch fetch all requested entities in a single query
      // e.g., SELECT * FROM requests WHERE id IN (uuid1, uuid2, ...)
      const results = await db.requests.findByIds([...uuids]);

      // CRITICAL: Return results in same order as input uuids
      // DataLoader requires 1:1 mapping between keys and results
      const resultMap = new Map(results.map((r) => [r.id, r]));
      return uuids.map((uuid) => resultMap.get(uuid) ?? null);
    },
    {
      cache: true,        // Cache within this request
      maxBatchSize: 100,  // Limit batch size for DB query performance
    }
  );
}
```

```typescript
// dataloaders/index.ts
export interface Loaders {
  request: DataLoader<string, any>;
  classified: DataLoader<string, any>;
  purchase: DataLoader<string, any>;
}

export function createLoaders(db: Database): Loaders {
  return {
    request: createRequestLoader(db),
    classified: createClassifiedLoader(db),
    purchase: createPurchaseLoader(db),
  };
}
```

### Context with DataLoaders

Create fresh DataLoaders per request:

```typescript
// server.ts
export interface GraphQLContext {
  user: User | null;
  permissions: Permissions;
  db: Database;
  loaders: Loaders;
}

app.use(
  "/graphql",
  expressMiddleware(apolloServer, {
    context: async ({ req }): Promise<GraphQLContext> => ({
      user: (req as any).connectedUser ?? null,
      permissions: (req as any).connectedUserPermissions,
      db: database,
      loaders: createLoaders(database), // Fresh loaders per request
    }),
  })
);
```

### Offset-Based Pagination (Connection Pattern)

```graphql
# schema/common.graphql
type PageInfo {
  total: Int!
  offset: Int!
  limit: Int!
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
}

input PaginationInput {
  offset: Int = 0
  limit: Int = 50
}

type RequestConnection {
  items: [Request!]!
  pageInfo: PageInfo!
}

extend type Query {
  requests(pagination: PaginationInput): RequestConnection!
}
```

```typescript
// resolvers/request.ts
async requests(
  parent: any,
  { pagination = {} }: { pagination?: { offset?: number; limit?: number } },
  context: GraphQLContext
) {
  const { offset = 0, limit = 50 } = pagination;

  const [items, total] = await Promise.all([
    context.db.requests.findMany({
      where: { deletedAt: null },
      skip: offset,
      take: limit,
      orderBy: { createdAt: "asc" },
    }),
    context.db.requests.count({ where: { deletedAt: null } }),
  ]);

  return {
    items,
    pageInfo: {
      total,
      offset,
      limit,
      hasNextPage: offset + limit < total,
      hasPreviousPage: offset > 0,
    },
  };
}
```

### Silent Permission Handling (Queries)

For queries, return `null` instead of throwing errors:

```typescript
async request(parent: any, { id }: { id: string }, context: GraphQLContext) {
  try {
    const { type, uuid } = decodeGlobalId(id);

    // Wrong type - return null silently
    if (type !== "request") {
      return null;
    }

    // No permission - return null silently
    if (!context.permissions?.canViewRequest?.(uuid)) {
      return null;
    }

    const request = await context.loaders.request.load(uuid);
    return request ?? null;
  } catch (error) {
    console.error("Error fetching request:", error);
    return null;
  }
}
```

### Query Examples

```graphql
# Fetch single entity by global ID
query GetRequest {
  request(id: "cmVxdWVzdDphYmMxMjM=") {
    id
    title
    description
  }
}

# Using node query for any entity
query GetNode {
  node(id: "cmVxdWVzdDphYmMxMjM=") {
    id
    ... on Request {
      title
      price
    }
    ... on Classified {
      status
      url
    }
  }
}

# Paginated list
query ListRequests {
  requests(pagination: { offset: 0, limit: 10 }) {
    items {
      id
      title
    }
    pageInfo {
      total
      hasNextPage
    }
  }
}
```
