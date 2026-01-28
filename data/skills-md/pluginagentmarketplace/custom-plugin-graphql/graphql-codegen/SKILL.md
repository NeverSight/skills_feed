---
name: graphql-codegen
description: Generate TypeScript types and React hooks from GraphQL schemas
sasmp_version: "1.3.0"
bonded_agent: 07-graphql-codegen
bond_type: PRIMARY_BOND
version: "2.0.0"
complexity: intermediate
estimated_time: "2-4 hours"
prerequisites: ["graphql-fundamentals"]
---

# GraphQL Code Generator Skill

> Type-safe GraphQL with automatic code generation

## Overview

Learn to use GraphQL Code Generator to automatically generate TypeScript types, React hooks, and more from your GraphQL schema and operations.

---

## Quick Reference

| Plugin | Generates | Use Case |
|--------|-----------|----------|
| `typescript` | Base types | All projects |
| `typescript-operations` | Query/mutation types | All projects |
| `typescript-react-apollo` | React hooks | React + Apollo |
| `typescript-urql` | URQL hooks | React + URQL |
| `introspection` | Schema JSON | Apollo Client |

---

## Setup

### 1. Installation

```bash
npm install -D @graphql-codegen/cli \
  @graphql-codegen/typescript \
  @graphql-codegen/typescript-operations \
  @graphql-codegen/typescript-react-apollo \
  @parcel/watcher
```

### 2. Configuration

```typescript
// codegen.ts
import type { CodegenConfig } from '@graphql-codegen/cli';

const config: CodegenConfig = {
  // Schema source
  schema: 'http://localhost:4000/graphql',

  // Operations to generate from
  documents: ['src/**/*.graphql', 'src/**/*.tsx'],

  // Output
  generates: {
    './src/generated/graphql.ts': {
      plugins: [
        'typescript',
        'typescript-operations',
        'typescript-react-apollo',
      ],
      config: {
        // Custom scalars
        scalars: {
          DateTime: 'string',
          JSON: 'Record<string, unknown>',
        },
        // Generate hooks
        withHooks: true,
        // Use enums as types
        enumsAsTypes: true,
      },
    },
  },
};

export default config;
```

### 3. Scripts

```json
{
  "scripts": {
    "codegen": "graphql-codegen --config codegen.ts",
    "codegen:watch": "graphql-codegen --config codegen.ts --watch"
  }
}
```

---

## Usage Examples

### 1. Define Operations

```graphql
# src/graphql/queries.graphql
query GetUser($id: ID!) {
  user(id: $id) {
    id
    name
    email
  }
}

query GetUsers($first: Int!, $after: String) {
  users(first: $first, after: $after) {
    edges {
      node {
        ...UserFields
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}

fragment UserFields on User {
  id
  name
  email
  avatar
}

# src/graphql/mutations.graphql
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    user {
      ...UserFields
    }
    errors {
      field
      message
    }
  }
}
```

### 2. Use Generated Code

```tsx
// Types and hooks are generated
import {
  useGetUserQuery,
  useGetUsersQuery,
  useCreateUserMutation,
  UserFieldsFragment,
  GetUserQuery,
} from '../generated/graphql';

// Query with full type safety
function UserProfile({ userId }: { userId: string }) {
  const { data, loading, error } = useGetUserQuery({
    variables: { id: userId }, // Type-checked!
  });

  if (loading) return <Spinner />;
  if (error) return <Error />;

  // data.user is fully typed
  return <div>{data?.user?.name}</div>;
}

// Mutation with type safety
function CreateUser() {
  const [createUser] = useCreateUserMutation({
    update(cache, { data }) {
      // data is typed
      if (data?.createUser.user) {
        // ...
      }
    },
  });

  const handleSubmit = (input: CreateUserInput) => {
    createUser({ variables: { input } }); // Type-checked!
  };
}

// Fragment type
function UserCard({ user }: { user: UserFieldsFragment }) {
  return <div>{user.name}</div>; // Typed fields
}
```

---

## Advanced Config

### Multiple Outputs

```typescript
const config: CodegenConfig = {
  schema: 'http://localhost:4000/graphql',
  documents: 'src/**/*.graphql',

  generates: {
    // Types only
    './src/types.ts': {
      plugins: ['typescript'],
    },

    // Operations with type imports
    './src/operations.ts': {
      preset: 'import-types',
      presetConfig: { typesPath: './types' },
      plugins: ['typescript-operations'],
    },

    // Hooks
    './src/hooks.ts': {
      preset: 'import-types',
      presetConfig: { typesPath: './types' },
      plugins: ['typescript-react-apollo'],
    },

    // Near-operation files
    './src/': {
      preset: 'near-operation-file',
      presetConfig: {
        extension: '.generated.tsx',
        baseTypesPath: 'types.ts',
      },
      plugins: ['typescript-operations', 'typescript-react-apollo'],
    },
  },
};
```

### Client Preset (Recommended)

```typescript
const config: CodegenConfig = {
  schema: 'http://localhost:4000/graphql',
  documents: 'src/**/*.tsx',

  generates: {
    './src/gql/': {
      preset: 'client',
      config: {
        fragmentMasking: { unmaskFunctionName: 'getFragmentData' },
      },
    },
  },
};

// Usage
import { gql, getFragmentData } from '../gql';

const UserQuery = gql(`
  query GetUser($id: ID!) {
    user(id: $id) {
      ...UserAvatar
    }
  }
`);

const UserAvatarFragment = gql(`
  fragment UserAvatar on User {
    avatar
  }
`);

function Profile({ userId }) {
  const { data } = useQuery(UserQuery, { variables: { id: userId } });
  const avatar = getFragmentData(UserAvatarFragment, data?.user);
}
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Types not updating | Stale cache | Delete generated folder |
| Schema fetch fails | Auth required | Add headers to config |
| Duplicate types | Multiple outputs | Use import-types preset |
| Watch not working | Missing watcher | Install @parcel/watcher |

### Debug

```bash
# Validate schema access
curl http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { types { name } } }"}'

# Verbose codegen
npx graphql-codegen --verbose

# Check config
npx graphql-codegen --check
```

---

## Usage

```
Skill("graphql-codegen")
```

## Related Skills
- `graphql-fundamentals` - Schema syntax
- `graphql-apollo-client` - Using generated hooks
- `graphql-schema-design` - Better types

## Related Agent
- `07-graphql-codegen` - For detailed guidance
