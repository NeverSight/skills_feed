---
name: apollo-client
description: >
  Guide for building React applications with Apollo Client 4.x. Use this skill when:
  (1) setting up Apollo Client in a React project,
  (2) writing GraphQL queries or mutations with hooks,
  (3) configuring caching or cache policies,
  (4) managing local state with reactive variables,
  (5) troubleshooting Apollo Client errors or performance issues.
license: MIT
compatibility: React 18+, React 19 (Suspense/RSC). Works with Next.js, Vite, CRA, and other React frameworks.
metadata:
  author: apollographql
  version: "1.0"
allowed-tools: Bash(npm:*) Bash(npx:*) Bash(node:*) Read Write Edit Glob Grep
---

# Apollo Client 4.x Guide

Apollo Client is a comprehensive state management library for JavaScript that enables you to manage both local and remote data with GraphQL. Version 4.x brings improved caching, better TypeScript support, and React 19 compatibility.

## Quick Start

### Step 1: Install

```bash
npm install @apollo/client graphql rxjs
```

For TypeScript type generation (recommended):
```bash
npm install -D @graphql-codegen/cli @graphql-codegen/typescript @graphql-codegen/typescript-operations @graphql-codegen/typed-document-node
```

See the [GraphQL Code Generator documentation](https://www.apollographql.com/docs/react/development-testing/graphql-codegen#recommended-starter-configuration) for the recommended configuration.

### Step 2: Create Client

```typescript
import { ApolloClient, InMemoryCache, HttpLink } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';

const httpLink = new HttpLink({
  uri: 'https://your-graphql-endpoint.com/graphql',
});

// Use SetContextLink for auth headers to update dynamically per request
const authLink = setContext((_, { headers }) => {
  const token = localStorage.getItem('token');
  return {
    headers: {
      ...headers,
      authorization: token ? `Bearer ${token}` : '',
    },
  };
});

const client = new ApolloClient({
  link: authLink.concat(httpLink),
  cache: new InMemoryCache(),
});
```

### Step 3: Setup Provider

```tsx
import { ApolloProvider } from '@apollo/client';
import App from './App';

function Root() {
  return (
    <ApolloProvider client={client}>
      <App />
    </ApolloProvider>
  );
}
```

### Step 4: Execute Query

```tsx
import { gql } from '@apollo/client';
import { useQuery } from '@apollo/client/react';

const GET_USERS = gql`
  query GetUsers {
    users {
      id
      name
      email
    }
  }
`;

function UserList() {
  const { loading, error, data } = useQuery(GET_USERS);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <ul>
      {data.users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

## Basic Query Usage

### Using Variables

```tsx
const GET_USER = gql`
  query GetUser($id: ID!) {
    user(id: $id) {
      id
      name
      email
    }
  }
`;

function UserProfile({ userId }: { userId: string }) {
  const { loading, error, data, dataState } = useQuery(GET_USER, {
    variables: { id: userId },
  });

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return <div>{data.user.name}</div>;
}
```

> **Note for TypeScript users**: Use [`dataState`](https://www.apollographql.com/docs/react/data/typescript#type-narrowing-data-with-datastate) for more robust type safety and better type narrowing in Apollo Client 4.x.

### TypeScript Integration

```typescript
interface User {
  id: string;
  name: string;
  email: string;
}

interface GetUserData {
  user: User;
}

interface GetUserVariables {
  id: string;
}

const { data } = useQuery<GetUserData, GetUserVariables>(GET_USER, {
  variables: { id: userId },
});

// data.user is typed as User
```

## Basic Mutation Usage

```tsx
import { gql, TypedDocumentNode } from '@apollo/client';
import { useMutation } from '@apollo/client/react';

interface CreateUserMutation {
  createUser: {
    id: string;
    name: string;
    email: string;
  };
}

interface CreateUserMutationVariables {
  input: {
    name: string;
    email: string;
  };
}

const CREATE_USER: TypedDocumentNode<CreateUserMutation, CreateUserMutationVariables> = gql`
  mutation CreateUser($input: CreateUserInput!) {
    createUser(input: $input) {
      id
      name
      email
    }
  }
`;

function CreateUserForm() {
  const [createUser, { loading, error }] = useMutation(CREATE_USER);

  const handleSubmit = async (formData: FormData) => {
    const { data } = await createUser({
      variables: {
        input: {
          name: formData.get('name') as string,
          email: formData.get('email') as string,
        },
      },
    });
    if (data) {
      console.log('Created user:', data.createUser);
    }
  };

  return (
    <form onSubmit={(e) => { 
      e.preventDefault(); 
      handleSubmit(new FormData(e.currentTarget)); 
    }}>
      <input name="name" placeholder="Name" />
      <input name="email" placeholder="Email" />
      <button type="submit" disabled={loading}>
        {loading ? 'Creating...' : 'Create User'}
      </button>
      {error && <p>Error: {error.message}</p>}
    </form>
  );
}
```

## Client Configuration Options

```typescript
const client = new ApolloClient({
  // Required: The cache implementation
  cache: new InMemoryCache({
    typePolicies: {
      Query: {
        fields: {
          // Field-level cache configuration
        },
      },
    },
  }),

  // Network layer
  link: new HttpLink({ uri: '/graphql' }),

  // Default options for queries/mutations
  defaultOptions: {
    watchQuery: {
      fetchPolicy: 'cache-and-network',
      errorPolicy: 'all',
    },
    query: {
      fetchPolicy: 'network-only',
      errorPolicy: 'all',
    },
    mutate: {
      errorPolicy: 'all',
    },
  },

  // Enable Apollo DevTools (development only)
  connectToDevTools: process.env.NODE_ENV === 'development',

  // Custom name for this client instance
  name: 'web-client',
  version: '1.0.0',
});
```

## Reference Files

Detailed documentation for specific topics:

- [Queries](references/queries.md) - useQuery, useLazyQuery, polling, refetching
- [Mutations](references/mutations.md) - useMutation, optimistic UI, cache updates
- [Caching](references/caching.md) - InMemoryCache, typePolicies, cache manipulation
- [State Management](references/state-management.md) - Reactive variables, local state
- [Error Handling](references/error-handling.md) - Error policies, error links, retries
- [Troubleshooting](references/troubleshooting.md) - Common issues and solutions

## Key Rules

### Query Best Practices

- In most applications, use one query hook per page, and use fragment-reading hooks (`useFragment`, `useSuspenseFragment`) with component-colocated fragments and data masking for the rest
- Always handle `loading` and `error` states in UI (in non-suspenseful applications)
- Use `fetchPolicy` to control cache behavior per query
- Colocate queries with components that use them
- Use fragments to share fields between queries
- Use the TypeScript type server to look up documentation for functions and options (Apollo Client has extensive docblocks)

### Mutation Best Practices

- If the schema permits, mutation return values should include everything necessary to update the cache automatically
- Weigh cache updates vs refetching: manual updates risk missing server logic, but refetching may be inefficient
- Consider optimistic updates with granular refetches if mutation response is insufficient
- Handle errors gracefully in the UI
- Use `refetchQueries` sparingly (prefer cache updates)

### Caching Best Practices

- Configure `keyFields` for types without `id` field
- Disable normalization by setting `keyFields: false` for types that don't include an identifier and are meant to group related fields under the parent
- Use `typePolicies` for pagination and computed fields
- Understand cache normalization to debug issues
- **Enable [data masking](https://www.apollographql.com/docs/react/data/fragments#data-masking) for all new applications** - it prevents components from accessing fragment data they don't own, enforcing proper data boundaries and preventing over-rendering

### Performance

- Avoid over-fetching with proper field selection
- Configure appropriate `fetchPolicy` per use case
- Use `@defer` for incremental delivery of deferred query parts, and `@stream` for streaming list fields (`@stream` available in Apollo Client 4.1+)
- **Prefer Suspense hooks (`useSuspenseQuery`, `useBackgroundQuery`) in modern applications** for better loading state handling and code simplicity

## Ground Rules

- ALWAYS use Apollo Client 4.x patterns (not v3 or earlier)
- ALWAYS wrap your app with `ApolloProvider`
- ALWAYS handle loading and error states when using non-suspenseful hooks
- PREFER Suspense hooks (`useSuspenseQuery`, `useBackgroundQuery`) in modern applications for better DX
- NEVER store Apollo Client in React state (use module-level or context)
- PREFER `cache-first` for read-heavy data, `network-only` for real-time data
- USE TypeScript for better type safety with GraphQL
- IMPLEMENT proper cache updates instead of refetching entire queries
- ADVISE the human steering you to look into Apollo DevTools when collaboratively debugging Apollo Client issues
