---
name: graphql-security
description: Secure GraphQL APIs - authentication, authorization, rate limiting, and validation
sasmp_version: "1.3.0"
bonded_agent: 06-graphql-security
bond_type: PRIMARY_BOND
version: "2.0.0"
complexity: advanced
estimated_time: "5-7 hours"
prerequisites: ["graphql-fundamentals", "graphql-resolvers", "graphql-apollo-server"]
---

# GraphQL Security Skill

> Protect your GraphQL APIs from attacks

## Overview

Learn essential security patterns for GraphQL: JWT authentication, role-based authorization, rate limiting, query complexity limits, and input validation.

---

## Security Checklist

| Check | Priority | Implementation |
|-------|----------|----------------|
| Authentication | Critical | JWT with refresh tokens |
| Authorization | Critical | Field-level with graphql-shield |
| Rate Limiting | Critical | Per-user/IP with Redis |
| Query Depth | High | graphql-depth-limit |
| Query Complexity | High | graphql-query-complexity |
| Introspection | High | Disable in production |
| Input Validation | High | Validate all inputs |
| Error Masking | Medium | Hide internal errors |

---

## Core Patterns

### 1. JWT Authentication

```typescript
import jwt from 'jsonwebtoken';

// Token creation
function createTokens(user) {
  const accessToken = jwt.sign(
    { userId: user.id, roles: user.roles },
    process.env.JWT_SECRET,
    { expiresIn: '15m' }
  );

  const refreshToken = jwt.sign(
    { userId: user.id },
    process.env.JWT_REFRESH_SECRET,
    { expiresIn: '7d' }
  );

  return { accessToken, refreshToken };
}

// Context setup
const context = async ({ req }) => {
  const token = req.headers.authorization?.replace('Bearer ', '');

  let user = null;
  if (token) {
    try {
      const payload = jwt.verify(token, process.env.JWT_SECRET);
      user = await db.users.findById(payload.userId);
    } catch (e) {
      // Token invalid or expired
    }
  }

  return { user };
};

// Login resolver
const resolvers = {
  Mutation: {
    login: async (_, { email, password }) => {
      const user = await db.users.findByEmail(email);

      if (!user || !await bcrypt.compare(password, user.passwordHash)) {
        throw new GraphQLError('Invalid credentials', {
          extensions: { code: 'UNAUTHORIZED' }
        });
      }

      return { ...createTokens(user), user };
    },
  },
};
```

### 2. Authorization with graphql-shield

```typescript
import { rule, shield, and, or } from 'graphql-shield';

// Rules
const isAuthenticated = rule()((_, __, { user }) => user !== null);

const isAdmin = rule()((_, __, { user }) =>
  user?.roles?.includes('ADMIN')
);

const isOwner = rule()(async (_, { id }, { user, dataSources }) => {
  const resource = await dataSources.findById(id);
  return resource?.userId === user?.id;
});

// Permissions
const permissions = shield({
  Query: {
    me: isAuthenticated,
    users: and(isAuthenticated, isAdmin),
    user: and(isAuthenticated, or(isOwner, isAdmin)),
  },
  Mutation: {
    updateUser: and(isAuthenticated, or(isOwner, isAdmin)),
    deleteUser: and(isAuthenticated, isAdmin),
  },
  User: {
    email: or(isOwner, isAdmin),
    privateField: isOwner,
  },
}, {
  fallbackError: new GraphQLError('Not authorized'),
});

// Apply
import { applyMiddleware } from 'graphql-middleware';
const protectedSchema = applyMiddleware(schema, permissions);
```

### 3. Rate Limiting

```typescript
// Express-level (basic)
import rateLimit from 'express-rate-limit';

app.use('/graphql', rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,
  keyGenerator: (req) => req.user?.id || req.ip,
}));

// GraphQL-level (granular)
const typeDefs = gql`
  directive @rateLimit(max: Int!, window: String!) on FIELD_DEFINITION

  type Mutation {
    login(email: String!, password: String!): AuthPayload!
      @rateLimit(max: 5, window: "15m")

    sendEmail(input: SendEmailInput!): Boolean!
      @rateLimit(max: 10, window: "1h")
  }
`;
```

### 4. Query Limits

```typescript
import depthLimit from 'graphql-depth-limit';
import { createComplexityLimitRule } from 'graphql-validation-complexity';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    // Max depth of 10
    depthLimit(10),

    // Max complexity of 1000
    createComplexityLimitRule(1000, {
      scalarCost: 1,
      objectCost: 2,
      listFactor: 10,
    }),
  ],

  // Disable introspection in production
  introspection: process.env.NODE_ENV !== 'production',
});
```

### 5. Input Validation

```typescript
import validator from 'validator';
import xss from 'xss';

const validate = {
  email: (v) => {
    if (!validator.isEmail(v)) throw new Error('Invalid email');
    return validator.normalizeEmail(v);
  },

  password: (v) => {
    if (v.length < 8) throw new Error('Password too short');
    if (!/[A-Z]/.test(v)) throw new Error('Need uppercase');
    if (!/[0-9]/.test(v)) throw new Error('Need number');
    return v;
  },

  html: (v) => xss(v),
};

const resolvers = {
  Mutation: {
    createUser: async (_, { input }) => {
      const clean = {
        email: validate.email(input.email),
        password: validate.password(input.password),
        bio: input.bio ? validate.html(input.bio) : null,
      };
      return db.users.create(clean);
    },
  },
};
```

### 6. Error Masking

```typescript
const server = new ApolloServer({
  formatError: (error) => {
    // Log full error
    console.error(error);

    // In production, hide internal errors
    if (process.env.NODE_ENV === 'production') {
      if (error.extensions?.code === 'INTERNAL_SERVER_ERROR') {
        return { message: 'Internal error', extensions: { code: 'INTERNAL_ERROR' } };
      }
    }

    return error;
  },
});
```

---

## Security Headers

```typescript
import helmet from 'helmet';
import cors from 'cors';

app.use(helmet());
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(','),
  credentials: true,
}));
app.use(express.json({ limit: '100kb' }));
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Token always invalid | Clock skew | Add grace period |
| Rate limit bypass | Wrong key | Use user ID when authenticated |
| Auth not working | Context async | Await context setup |
| Introspection exposed | Wrong env check | Verify NODE_ENV |

### Security Testing

```bash
# Test introspection (should fail in prod)
curl -X POST $API \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { types { name } } }"}'

# Test rate limit
for i in {1..20}; do
  curl -X POST $API \
    -d '{"query":"mutation { login(email:\"x\",password:\"y\") { token } }"}'
done

# Test depth limit (should fail)
curl -X POST $API \
  -d '{"query":"{ user { posts { author { posts { author { id } } } } } }"}'
```

---

## Usage

```
Skill("graphql-security")
```

## Related Skills
- `graphql-apollo-server` - Server configuration
- `graphql-resolvers` - Auth in resolvers
- `graphql-schema-design` - Auth-aware schema

## Related Agent
- `06-graphql-security` - For detailed guidance
