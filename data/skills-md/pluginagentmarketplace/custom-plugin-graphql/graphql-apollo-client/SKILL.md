---
name: graphql-apollo-client
description: Build React apps with Apollo Client - queries, mutations, cache, and subscriptions
sasmp_version: "1.3.0"
bonded_agent: 05-graphql-apollo-client
bond_type: PRIMARY_BOND
version: "2.0.0"
complexity: intermediate
estimated_time: "4-6 hours"
prerequisites: ["graphql-fundamentals"]
---

# Apollo Client Skill

> Master GraphQL in React applications

## Overview

Learn to integrate Apollo Client with React, including hooks, cache management, optimistic updates, and real-time subscriptions.

---

## Quick Reference

| Hook | Purpose | Returns |
|------|---------|---------|
| `useQuery` | Fetch data | `{ data, loading, error, refetch }` |
| `useMutation` | Modify data | `[mutate, { data, loading, error }]` |
| `useSubscription` | Real-time | `{ data, loading, error }` |
| `useLazyQuery` | On-demand fetch | `[execute, { data, loading }]` |

---

## Core Patterns

### 1. Client Setup

```typescript
import {
  ApolloClient,
  InMemoryCache,
  ApolloProvider,
  createHttpLink,
  from
} from '@apollo/client';
import { setContext } from '@apollo/client/link/context';
import { onError } from '@apollo/client/link/error';

// HTTP connection
const httpLink = createHttpLink({
  uri: 'http://localhost:4000/graphql',
  credentials: 'include',
});

// Auth header
const authLink = setContext((_, { headers }) => ({
  headers: {
    ...headers,
    authorization: localStorage.getItem('token')
      ? `Bearer ${localStorage.getItem('token')}`
      : '',
  },
}));

// Error handling
const errorLink = onError(({ graphQLErrors, networkError }) => {
  if (graphQLErrors) {
    graphQLErrors.forEach(({ message, extensions }) => {
      if (extensions?.code === 'UNAUTHENTICATED') {
        window.location.href = '/login';
      }
    });
  }
});

// Cache with type policies
const cache = new InMemoryCache({
  typePolicies: {
    User: { keyFields: ['id'] },
    Query: {
      fields: {
        users: {
          keyArgs: ['filter'],
          merge(existing, incoming, { args }) {
            if (!args?.after) return incoming;
            return {
              ...incoming,
              edges: [...(existing?.edges || []), ...incoming.edges],
            };
          },
        },
      },
    },
  },
});

// Client
const client = new ApolloClient({
  link: from([errorLink, authLink, httpLink]),
  cache,
});

// Provider
function App() {
  return (
    <ApolloProvider client={client}>
      <Router />
    </ApolloProvider>
  );
}
```

### 2. Queries

```typescript
import { gql, useQuery } from '@apollo/client';

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
  const { data, loading, error, refetch } = useQuery(GET_USER, {
    variables: { id: userId },
    // Options
    fetchPolicy: 'cache-and-network',
    pollInterval: 60000, // Refetch every minute
    skip: !userId,       // Skip if no userId
  });

  if (loading) return <Spinner />;
  if (error) return <Error onRetry={refetch} />;

  return <div>{data.user.name}</div>;
}

// Pagination
function UserList() {
  const { data, fetchMore, networkStatus } = useQuery(GET_USERS, {
    variables: { first: 10 },
    notifyOnNetworkStatusChange: true,
  });

  const loadMore = () => {
    fetchMore({
      variables: { after: data.users.pageInfo.endCursor },
    });
  };

  return (
    <>
      {data?.users.edges.map(({ node }) => (
        <UserCard key={node.id} user={node} />
      ))}
      {data?.users.pageInfo.hasNextPage && (
        <button onClick={loadMore}>Load More</button>
      )}
    </>
  );
}
```

### 3. Mutations

```typescript
const CREATE_USER = gql`
  mutation CreateUser($input: CreateUserInput!) {
    createUser(input: $input) {
      user { id name email }
      errors { field message }
    }
  }
`;

function CreateUserForm() {
  const [createUser, { loading }] = useMutation(CREATE_USER, {
    // Update cache after success
    update(cache, { data }) {
      if (!data?.createUser.user) return;

      cache.modify({
        fields: {
          users(existing = { edges: [] }) {
            const newRef = cache.writeFragment({
              data: data.createUser.user,
              fragment: gql`fragment NewUser on User { id name email }`,
            });
            return {
              ...existing,
              edges: [{ node: newRef }, ...existing.edges],
            };
          },
        },
      });
    },

    // Optimistic response
    optimisticResponse: (vars) => ({
      createUser: {
        __typename: 'CreateUserPayload',
        user: {
          __typename: 'User',
          id: 'temp-' + Date.now(),
          ...vars.input,
        },
        errors: [],
      },
    }),
  });

  const handleSubmit = async (input) => {
    const { data } = await createUser({ variables: { input } });
    if (data?.createUser.errors.length) {
      // Handle validation errors
    }
  };

  return <Form onSubmit={handleSubmit} loading={loading} />;
}
```

### 4. Optimistic Updates

```typescript
// Delete
const [deleteUser] = useMutation(DELETE_USER, {
  optimisticResponse: {
    deleteUser: { success: true, id: userId },
  },
  update(cache, { data }) {
    cache.evict({ id: cache.identify({ __typename: 'User', id: userId }) });
    cache.gc();
  },
});

// Toggle
const [toggleLike] = useMutation(TOGGLE_LIKE, {
  optimisticResponse: {
    toggleLike: {
      __typename: 'Post',
      id: post.id,
      isLiked: !post.isLiked,
      likeCount: post.isLiked ? post.likeCount - 1 : post.likeCount + 1,
    },
  },
});
```

### 5. Subscriptions

```typescript
import { useSubscription } from '@apollo/client';
import { GraphQLWsLink } from '@apollo/client/link/subscriptions';
import { createClient } from 'graphql-ws';
import { split } from '@apollo/client';
import { getMainDefinition } from '@apollo/client/utilities';

// WebSocket link
const wsLink = new GraphQLWsLink(
  createClient({
    url: 'ws://localhost:4000/graphql',
    connectionParams: () => ({
      authToken: localStorage.getItem('token'),
    }),
  })
);

// Split between HTTP and WS
const splitLink = split(
  ({ query }) => {
    const def = getMainDefinition(query);
    return def.kind === 'OperationDefinition' && def.operation === 'subscription';
  },
  wsLink,
  httpLink,
);

// Usage
const MESSAGE_SUB = gql`
  subscription OnMessage($channelId: ID!) {
    messageSent(channelId: $channelId) {
      id
      content
      sender { name }
    }
  }
`;

function Chat({ channelId }) {
  const { data } = useSubscription(MESSAGE_SUB, {
    variables: { channelId },
  });

  // New message in data?.messageSent
}
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Stale data | Cache not updated | Add update function |
| Duplicates | Missing keyFields | Configure typePolicies |
| Refetch loop | Variables object recreated | useMemo variables |
| No subscription | Missing split link | Add wsLink |

### Debug

```typescript
// Cache inspection
console.log(client.cache.extract());

// Apollo DevTools
// Install browser extension

// Logging link
import { ApolloLink } from '@apollo/client';

const logLink = new ApolloLink((operation, forward) => {
  console.log('Request:', operation.operationName);
  return forward(operation);
});
```

---

## Usage

```
Skill("graphql-apollo-client")
```

## Related Skills
- `graphql-fundamentals` - Query syntax
- `graphql-apollo-server` - Server integration
- `graphql-codegen` - Type generation

## Related Agent
- `05-graphql-apollo-client` - For detailed guidance
