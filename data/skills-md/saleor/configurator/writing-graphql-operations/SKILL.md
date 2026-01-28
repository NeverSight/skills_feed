---
name: writing-graphql-operations
description: "Creates GraphQL queries and mutations using gql.tada and urql. Implements repository pattern with type-safe operations and error handling. Triggers on: GraphQL query, GraphQL mutation, gql.tada, urql client, Saleor API, fragments, repository pattern, fetch-schema, MSW mocks."
allowed-tools: "Read, Grep, Glob, Write, Edit"
---

# GraphQL Operations Developer

## Purpose

Guide the creation and maintenance of GraphQL operations following project conventions for type safety, organization, error handling, and testing.

## When to Use

- Creating new GraphQL queries or mutations
- Integrating with Saleor API endpoints
- Updating schema after Saleor changes
- Working with urql client configuration
- Creating mocks for testing

## Table of Contents

- [Project GraphQL Stack](#project-graphql-stack)
- [File Organization](#file-organization)
- [Creating Operations with gql.tada](#creating-operations-with-gqltada)
- [Repository Pattern](#repository-pattern)
- [Error Handling](#error-handling)
- [Schema Management](#schema-management)
- [Testing GraphQL Operations](#testing-graphql-operations)
- [Client Configuration](#client-configuration)
- [Best Practices](#best-practices)
- [References](#references)

## Project GraphQL Stack

| Tool | Purpose |
|------|---------|
| **urql** | GraphQL client with caching |
| **gql.tada** | Type-safe GraphQL with TypeScript inference |
| **@urql/exchange-auth** | Authentication handling |
| **@urql/exchange-retry** | Rate limiting and retry logic |

## File Organization

```
src/lib/graphql/
├── client.ts              # urql client configuration
├── operations/            # GraphQL operation definitions
│   ├── products.ts
│   ├── categories.ts
│   └── ...
├── fragments/             # Reusable GraphQL fragments
│   └── ...
├── __mocks__/            # Test mocks
│   └── ...
└── schema.graphql        # Saleor schema (generated)

src/modules/<entity>/
├── repository.ts          # Uses GraphQL operations
└── ...
```

## Creating Operations with gql.tada

### Basic Query

```typescript
import { graphql } from 'gql.tada';

// gql.tada infers types from schema automatically
export const GetCategoriesQuery = graphql(`
  query GetCategories($first: Int!) {
    categories(first: $first) {
      edges {
        node {
          id
          name
          slug
          description
          parent {
            id
            slug
          }
        }
      }
    }
  }
`);

// Type is inferred automatically
type GetCategoriesResult = ResultOf<typeof GetCategoriesQuery>;
```

### Query with Variables

```typescript
export const GetCategoryBySlugQuery = graphql(`
  query GetCategoryBySlug($slug: String!) {
    category(slug: $slug) {
      id
      name
      slug
      description
      level
      parent {
        id
        slug
      }
      children(first: 100) {
        edges {
          node {
            id
            name
            slug
          }
        }
      }
    }
  }
`);
```

### Mutation

```typescript
export const CreateCategoryMutation = graphql(`
  mutation CreateCategory($input: CategoryInput!) {
    categoryCreate(input: $input) {
      category {
        id
        name
        slug
      }
      errors {
        field
        message
        code
      }
    }
  }
`);
```

### Using Fragments

```typescript
// Define reusable fragment
export const CategoryFieldsFragment = graphql(`
  fragment CategoryFields on Category {
    id
    name
    slug
    description
    level
  }
`);

// Use in query
export const GetCategoriesWithFragmentQuery = graphql(`
  query GetCategoriesWithFragment($first: Int!) {
    categories(first: $first) {
      edges {
        node {
          ...CategoryFields
        }
      }
    }
  }
`, [CategoryFieldsFragment]);
```

## Repository Pattern

### Standard Repository Structure

```typescript
// src/modules/category/repository.ts
import { Client } from '@urql/core';
import { graphql } from 'gql.tada';
import { GraphQLError } from '@/lib/errors';

const GetCategoriesQuery = graphql(`...`);
const CreateCategoryMutation = graphql(`...`);

export class CategoryRepository {
  constructor(private readonly client: Client) {}

  async findAll(): Promise<Category[]> {
    const result = await this.client.query(GetCategoriesQuery, { first: 100 });

    if (result.error) {
      throw GraphQLError.fromCombinedError(result.error, 'GetCategories');
    }

    return this.mapCategories(result.data?.categories);
  }

  async create(input: CategoryInput): Promise<Category> {
    const result = await this.client.mutation(CreateCategoryMutation, { input });

    if (result.error) {
      throw GraphQLError.fromCombinedError(result.error, 'CreateCategory');
    }

    if (result.data?.categoryCreate?.errors?.length) {
      throw new GraphQLError(
        'Category creation failed',
        result.data.categoryCreate.errors
      );
    }

    return this.mapCategory(result.data?.categoryCreate?.category);
  }

  // Map GraphQL response to domain model
  private mapCategory(gqlCategory: GqlCategory | null): Category {
    if (!gqlCategory) {
      throw new EntityNotFoundError('Category not found');
    }
    return {
      id: gqlCategory.id,
      name: gqlCategory.name,
      slug: gqlCategory.slug,
      description: gqlCategory.description ?? undefined,
    };
  }
}
```

## Error Handling

### Wrapping GraphQL Errors

```typescript
import { CombinedError } from '@urql/core';
import { GraphQLError } from '@/lib/errors';

// In repository methods
if (result.error) {
  throw GraphQLError.fromCombinedError(
    result.error,
    'OperationName',
    { entitySlug: input.slug }  // Additional context
  );
}

// Handle mutation-specific errors
if (result.data?.mutationName?.errors?.length) {
  const errors = result.data.mutationName.errors;
  throw new GraphQLError(
    `Operation failed: ${errors.map(e => e.message).join(', ')}`,
    errors
  );
}
```

### Common Error Scenarios

| Error Type | Cause | Handling |
|------------|-------|----------|
| `CombinedError` | Network/GraphQL errors | `GraphQLError.fromCombinedError()` |
| `errors` array | Mutation validation errors | Check `result.data?.mutation?.errors` |
| Rate limit (429) | Too many requests | Automatic retry via exchange |
| Auth error | Invalid/expired token | Re-authenticate |

## Schema Management

### Updating Schema

```bash
# Fetch latest schema from Saleor instance
pnpm fetch-schema

# This updates:
# - src/lib/graphql/schema.graphql
# - graphql-env.d.ts (type definitions)
```

### When to Update Schema

- New Saleor features needed
- After Saleor version upgrade
- When encountering schema drift errors
- Commit schema changes with feature implementation

## Testing GraphQL Operations

### Mock Setup with MSW

```typescript
// src/lib/graphql/__mocks__/category-mocks.ts
import { graphql, HttpResponse } from 'msw';

export const categoryHandlers = [
  graphql.query('GetCategories', () => {
    return HttpResponse.json({
      data: {
        categories: {
          edges: [
            {
              node: {
                id: 'cat-1',
                name: 'Electronics',
                slug: 'electronics',
              },
            },
          ],
        },
      },
    });
  }),

  graphql.mutation('CreateCategory', ({ variables }) => {
    return HttpResponse.json({
      data: {
        categoryCreate: {
          category: {
            id: 'new-cat',
            name: variables.input.name,
            slug: variables.input.slug,
          },
          errors: [],
        },
      },
    });
  }),
];
```

### Repository Test Pattern

```typescript
describe('CategoryRepository', () => {
  const server = setupServer(...categoryHandlers);

  beforeAll(() => server.listen());
  afterEach(() => server.resetHandlers());
  afterAll(() => server.close());

  it('should fetch all categories', async () => {
    const repository = new CategoryRepository(testClient);
    const categories = await repository.findAll();

    expect(categories).toHaveLength(1);
    expect(categories[0].slug).toBe('electronics');
  });
});
```

## Client Configuration

### urql Client Setup

```typescript
// src/lib/graphql/client.ts
import { Client, cacheExchange, fetchExchange } from '@urql/core';
import { authExchange } from '@urql/exchange-auth';
import { retryExchange } from '@urql/exchange-retry';

export const createClient = (url: string, token: string) => {
  return new Client({
    url,
    exchanges: [
      cacheExchange,
      authExchange(async utils => ({
        addAuthToOperation(operation) {
          return utils.appendHeaders(operation, {
            Authorization: `Bearer ${token}`,
          });
        },
      })),
      retryExchange({
        initialDelayMs: 1000,
        maxDelayMs: 15000,
        maxNumberAttempts: 5,
        retryIf: error => {
          // Retry on rate limits and network errors
          return error?.response?.status === 429 || !error?.response;
        },
      }),
      fetchExchange,
    ],
  });
};
```

## Best Practices

### Do's

- Use `gql.tada` for all operations (type inference)
- Keep operations close to their domain modules
- Map GraphQL responses to domain models
- Include operation name in error context
- Update mocks when schema changes

### Don'ts

- Don't use raw string queries (no type safety)
- Don't expose GraphQL types directly to services
- Don't skip error handling for any operation
- Don't hardcode pagination limits (use constants)

## Validation Checkpoints

| Phase | Validate | Command |
|-------|----------|---------|
| Schema fresh | No drift | `pnpm fetch-schema` |
| Operations typed | gql.tada inference | Check IDE types |
| Mocks match | MSW handlers | `pnpm test` |
| Error handling | All paths covered | Code review |

## Common Mistakes

| Mistake | Issue | Fix |
|---------|-------|-----|
| Not checking `errors` array | Silent failures | Always check `result.data?.mutation?.errors` |
| Exposing GraphQL types | Coupling | Map to domain types in repository |
| Missing error context | Hard to debug | Include operation name in errors |
| Stale schema | Type errors | Run `pnpm fetch-schema` after Saleor updates |
| Not using fragments | Code duplication | Extract shared fields to fragments |

## External Documentation

For up-to-date library docs, use Context7 MCP:
- urql: `mcp__context7__get-library-docs` with `/urql-graphql/urql`
- gql.tada: Use `mcp__context7__resolve-library-id` with "gql.tada"

## References

### Skill Reference Files
- **[Error Handling](references/error-handling.md)** - Error types, wrapping, and recovery patterns
- **[Fragment Patterns](references/fragment-patterns.md)** - Fragment composition and type inference

### Project Resources
- `{baseDir}/src/lib/graphql/client.ts` - Client configuration
- `{baseDir}/src/lib/graphql/operations/` - Existing operations
- `{baseDir}/docs/CODE_QUALITY.md#graphql--external-integrations` - Quality standards

## Related Skills

- **Complete entity workflow**: See `adding-entity-types` for full implementation including bulk mutations
- **Bulk operations**: See `adding-entity-types/references/bulk-mutations.md` for chunking patterns
- **Testing GraphQL**: See `analyzing-test-coverage` for MSW setup

## Quick Reference Rule

For a condensed quick reference, see `.claude/rules/graphql-patterns.md` (automatically loaded when editing GraphQL operations and repository files).
