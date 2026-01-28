---
name: graphql
description: GraphQL API development including schema design, resolvers, queries, mutations, subscriptions, and integration with Node.js, Apollo, and other frameworks. Use when building GraphQL APIs, designing GraphQL schemas, implementing resolvers, or debugging GraphQL issues.
---

# GraphQL Development

GraphQL API design, implementation, and best practices.

## Schema Design

### Type Definitions

```graphql
# Scalar types
type User {
    id: ID!
    email: String!
    name: String
    age: Int
    balance: Float
    isActive: Boolean!
    createdAt: DateTime!  # Custom scalar
}

# Enum types
enum UserRole {
    ADMIN
    EDITOR
    USER
}

enum OrderStatus {
    PENDING
    PROCESSING
    SHIPPED
    DELIVERED
    CANCELLED
}

# Input types (for mutations)
input CreateUserInput {
    email: String!
    name: String!
    password: String!
    role: UserRole = USER
}

input UpdateUserInput {
    name: String
    email: String
}

# Interface
interface Node {
    id: ID!
}

type User implements Node {
    id: ID!
    email: String!
}

# Union types
union SearchResult = User | Post | Comment
```

### Relationships

```graphql
type User {
    id: ID!
    email: String!
    posts: [Post!]!                    # One-to-many
    profile: Profile                   # One-to-one (nullable)
    followers: [User!]!                # Self-referential
    following: [User!]!
}

type Post {
    id: ID!
    title: String!
    content: String!
    author: User!                      # Many-to-one
    tags: [Tag!]!                      # Many-to-many
    comments(first: Int, after: String): CommentConnection!
}

# Connection pattern for pagination
type CommentConnection {
    edges: [CommentEdge!]!
    pageInfo: PageInfo!
    totalCount: Int!
}

type CommentEdge {
    cursor: String!
    node: Comment!
}

type PageInfo {
    hasNextPage: Boolean!
    hasPreviousPage: Boolean!
    startCursor: String
    endCursor: String
}
```

## Queries & Mutations

### Query Types

```graphql
type Query {
    # Single item
    user(id: ID!): User
    userByEmail(email: String!): User

    # Lists with filtering
    users(
        filter: UserFilter
        orderBy: UserOrderBy
        first: Int
        after: String
    ): UserConnection!

    # Search
    search(query: String!, types: [SearchType!]): [SearchResult!]!

    # Current user
    me: User
}

input UserFilter {
    role: UserRole
    isActive: Boolean
    createdAfter: DateTime
}

input UserOrderBy {
    field: UserSortField!
    direction: SortDirection!
}

enum UserSortField {
    CREATED_AT
    NAME
    EMAIL
}

enum SortDirection {
    ASC
    DESC
}
```

### Mutation Types

```graphql
type Mutation {
    # Create
    createUser(input: CreateUserInput!): CreateUserPayload!

    # Update
    updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!

    # Delete
    deleteUser(id: ID!): DeleteUserPayload!

    # Authentication
    login(email: String!, password: String!): AuthPayload!
    logout: Boolean!
    refreshToken(token: String!): AuthPayload!
}

# Payload pattern (recommended)
type CreateUserPayload {
    user: User
    errors: [Error!]
}

type Error {
    field: String
    message: String!
    code: ErrorCode!
}

enum ErrorCode {
    VALIDATION_ERROR
    NOT_FOUND
    UNAUTHORIZED
    FORBIDDEN
}
```

### Subscriptions

```graphql
type Subscription {
    # Real-time updates
    postCreated: Post!
    commentAdded(postId: ID!): Comment!
    userStatusChanged(userId: ID!): User!

    # With filtering
    messageReceived(roomId: ID!): Message!
}
```

## Apollo Server (Node.js)

### Setup

```javascript
import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@apollo/server/express4';
import express from 'express';

const typeDefs = `#graphql
    type Query {
        users: [User!]!
        user(id: ID!): User
    }

    type User {
        id: ID!
        email: String!
        posts: [Post!]!
    }
`;

const resolvers = {
    Query: {
        users: async (_, __, { dataSources }) => {
            return dataSources.userAPI.getUsers();
        },
        user: async (_, { id }, { dataSources }) => {
            return dataSources.userAPI.getUser(id);
        },
    },
    User: {
        posts: async (parent, _, { dataSources }) => {
            return dataSources.postAPI.getPostsByAuthor(parent.id);
        },
    },
};

const server = new ApolloServer({
    typeDefs,
    resolvers,
});

const app = express();
await server.start();

app.use(
    '/graphql',
    express.json(),
    expressMiddleware(server, {
        context: async ({ req }) => ({
            token: req.headers.authorization,
            dataSources: {
                userAPI: new UserAPI(),
                postAPI: new PostAPI(),
            },
        }),
    })
);
```

### Resolvers

```javascript
const resolvers = {
    Query: {
        // Arguments: parent, args, context, info
        user: async (_, { id }, { dataSources, user }) => {
            return dataSources.userAPI.getUser(id);
        },

        users: async (_, { filter, first, after }, { dataSources }) => {
            const users = await dataSources.userAPI.getUsers({
                filter,
                limit: first,
                cursor: after,
            });
            return formatConnection(users);
        },
    },

    Mutation: {
        createUser: async (_, { input }, { dataSources }) => {
            try {
                const user = await dataSources.userAPI.create(input);
                return { user, errors: null };
            } catch (error) {
                return {
                    user: null,
                    errors: [{ message: error.message, code: 'VALIDATION_ERROR' }],
                };
            }
        },
    },

    // Field-level resolvers
    User: {
        fullName: (parent) => `${parent.firstName} ${parent.lastName}`,
        posts: async (parent, { first }, { dataSources }) => {
            return dataSources.postAPI.getByAuthor(parent.id, { limit: first });
        },
    },

    // Custom scalars
    DateTime: new GraphQLScalarType({
        name: 'DateTime',
        parseValue: (value) => new Date(value),
        serialize: (value) => value.toISOString(),
    }),
};
```

### DataLoader (N+1 Prevention)

```javascript
import DataLoader from 'dataloader';

// Create loader
const userLoader = new DataLoader(async (userIds) => {
    const users = await db.users.findMany({
        where: { id: { in: userIds } },
    });
    // Return in same order as input
    return userIds.map((id) => users.find((u) => u.id === id));
});

// In resolver
const resolvers = {
    Post: {
        author: (parent, _, { loaders }) => {
            return loaders.userLoader.load(parent.authorId);
        },
    },
};

// Context setup
const context = ({ req }) => ({
    loaders: {
        userLoader: new DataLoader(batchUsers),
    },
});
```

## Authentication & Authorization

### Context-based Auth

```javascript
const server = new ApolloServer({
    typeDefs,
    resolvers,
    context: async ({ req }) => {
        const token = req.headers.authorization?.replace('Bearer ', '');
        let user = null;

        if (token) {
            try {
                user = await verifyToken(token);
            } catch (e) {
                // Invalid token, user stays null
            }
        }

        return { user };
    },
});

// In resolver
const resolvers = {
    Query: {
        me: (_, __, { user }) => {
            if (!user) throw new AuthenticationError('Not authenticated');
            return user;
        },
    },
};
```

### Directive-based Auth

```graphql
directive @auth(requires: Role = USER) on FIELD_DEFINITION

type Query {
    publicPosts: [Post!]!
    myPosts: [Post!]! @auth
    allUsers: [User!]! @auth(requires: ADMIN)
}
```

```javascript
import { mapSchema, getDirective, MapperKind } from '@graphql-tools/utils';

function authDirective(directiveName) {
    return {
        authDirectiveTransformer: (schema) =>
            mapSchema(schema, {
                [MapperKind.OBJECT_FIELD]: (fieldConfig) => {
                    const directive = getDirective(schema, fieldConfig, directiveName)?.[0];
                    if (directive) {
                        const { resolve = defaultFieldResolver } = fieldConfig;
                        fieldConfig.resolve = async function (source, args, context, info) {
                            if (!context.user) {
                                throw new AuthenticationError('Not authenticated');
                            }
                            const requiredRole = directive.requires;
                            if (requiredRole && context.user.role !== requiredRole) {
                                throw new ForbiddenError('Not authorized');
                            }
                            return resolve(source, args, context, info);
                        };
                    }
                    return fieldConfig;
                },
            }),
    };
}
```

## Error Handling

```javascript
import { GraphQLError } from 'graphql';

// Custom errors
class NotFoundError extends GraphQLError {
    constructor(message) {
        super(message, {
            extensions: {
                code: 'NOT_FOUND',
                http: { status: 404 },
            },
        });
    }
}

class ValidationError extends GraphQLError {
    constructor(errors) {
        super('Validation failed', {
            extensions: {
                code: 'VALIDATION_ERROR',
                validationErrors: errors,
                http: { status: 400 },
            },
        });
    }
}

// Usage in resolver
const resolvers = {
    Query: {
        user: async (_, { id }) => {
            const user = await db.users.findUnique({ where: { id } });
            if (!user) {
                throw new NotFoundError(`User ${id} not found`);
            }
            return user;
        },
    },
};
```

## Performance

### Query Complexity

```javascript
import { createComplexityLimitRule } from 'graphql-validation-complexity';

const server = new ApolloServer({
    typeDefs,
    resolvers,
    validationRules: [
        createComplexityLimitRule(1000, {
            scalarCost: 1,
            objectCost: 10,
            listFactor: 20,
        }),
    ],
});
```

### Depth Limiting

```javascript
import depthLimit from 'graphql-depth-limit';

const server = new ApolloServer({
    typeDefs,
    resolvers,
    validationRules: [depthLimit(10)],
});
```

### Caching

```graphql
type Query {
    user(id: ID!): User @cacheControl(maxAge: 60)
    posts: [Post!]! @cacheControl(maxAge: 30, scope: PUBLIC)
}

type User @cacheControl(maxAge: 120) {
    id: ID!
    email: String! @cacheControl(maxAge: 0, scope: PRIVATE)
}
```

## Testing

```javascript
import { ApolloServer } from '@apollo/server';

describe('User Queries', () => {
    let server;

    beforeAll(() => {
        server = new ApolloServer({
            typeDefs,
            resolvers,
        });
    });

    it('should return user by id', async () => {
        const response = await server.executeOperation({
            query: `
                query GetUser($id: ID!) {
                    user(id: $id) {
                        id
                        email
                    }
                }
            `,
            variables: { id: '1' },
        });

        expect(response.body.singleResult.errors).toBeUndefined();
        expect(response.body.singleResult.data?.user).toEqual({
            id: '1',
            email: 'test@example.com',
        });
    });
});
```
