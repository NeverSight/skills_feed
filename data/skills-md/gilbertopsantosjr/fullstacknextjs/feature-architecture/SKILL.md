---
name: feature-architecture
description: Guide for implementing features in a layered Next.js full-stack architecture. Use when planning new features, understanding the layer structure (Model, DAL, Service, Actions, Components, Pages), or deciding where code should live.
---

# Feature Architecture

## Layer Overview

```
┌─────────────────────────────────────────┐
│  Pages (src/app/)                       │  Route handlers, layouts
├─────────────────────────────────────────┤
│  Components (features/*/components/)    │  UI elements
├─────────────────────────────────────────┤
│  Server Actions (features/*/usecases/)  │  API layer
├─────────────────────────────────────────┤
│  Services (features/*/<name>-service)   │  Business logic
├─────────────────────────────────────────┤
│  DAL (features/*/dal/)                  │  Database access
├─────────────────────────────────────────┤
│  Model (features/*/model/)              │  Schemas, types
└─────────────────────────────────────────┘
```

## Implementation Order

**Always implement bottom-up:**

1. **Model** - Zod schemas, types, constants
2. **DAL** - Database operations
3. **Service** - Business logic
4. **Actions** - Server actions
5. **Components** - UI
6. **Pages** - Routes

## Feature Directory Structure

```
src/features/<feature>/
├── model/
│   ├── <feature>-schemas.ts     # Zod schemas + types
│   └── <feature>-constants.ts   # Constants
├── dal/
│   ├── create_<entity>.ts       # snake_case files
│   ├── find_<entity>_by_id.ts
│   ├── update_<entity>.ts
│   └── delete_<entity>.ts
├── <feature>-service.ts         # Business logic
├── usecases/
│   ├── create/actions/<action>.ts
│   ├── update/actions/<action>.ts
│   └── delete/actions/<action>.ts
├── components/
│   ├── <Component>.tsx
│   ├── <Component>-server.tsx
│   └── <Component>-client.tsx
└── utils/                       # Feature utilities
```

## Layer Responsibilities

### Model Layer
- Zod schemas for validation
- TypeScript types (inferred from Zod)
- Constants and enums
- **No logic**, only definitions

### DAL Layer
- Direct database operations
- One file per operation
- snake_case naming
- Returns `{ success, data?, error? }`
- Entity-to-model converters
- **No business logic**

### Service Layer
- Business logic and validation
- Orchestrates DAL calls
- Permission checks
- **Called by actions, not directly by UI**

### Actions Layer
- Server actions for client calls
- Authentication via `authedProcedure`
- Input validation with Zod
- Calls services, NOT DAL
- Cache revalidation

### Components Layer
- Server components (default)
- Client components (interactivity)
- Split pattern for hybrid needs

### Pages Layer
- Route definitions
- Layout composition
- Data fetching (server components)

## Naming Conventions

| Layer | Case | Example |
|-------|------|---------|
| Model files | kebab-case | `account-schemas.ts` |
| DAL files | snake_case | `create_account.ts` |
| Service files | kebab-case | `account-service.ts` |
| Action files | kebab-case | `create-account-action.ts` |
| Components | PascalCase | `AccountCard.tsx` |
| Directories | kebab-case | `user-profile/` |
| Constants | SCREAMING_SNAKE | `MAX_NAME_LENGTH` |

## Data Flow

```
User Action
    ↓
Component (client)
    ↓
Server Action (validates, authenticates)
    ↓
Service (business logic)
    ↓
DAL (database operation)
    ↓
DynamoDB
```

## Quick Reference

| Need to... | Go to... |
|------------|----------|
| Add validation | `model/<feature>-schemas.ts` |
| Add DB operation | `dal/` (new snake_case file) |
| Add business rule | `<feature>-service.ts` |
| Add API endpoint | `usecases/*/actions/` |
| Add UI element | `components/` |
| Add page route | `src/app/` |

## Environment Setup

```bash
# Install UV for Python tools
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
pnpm install

# Development
pnpm dev

# SST dev mode
npx sst dev --stage dev
```

## Related Skills

- **zod-validation** - Schema patterns
- **dynamodb-onetable** - Database patterns
- **nextjs-server-actions** - Action patterns
- **nextjs-web-client** - Component patterns
- **sst-infra** - Deployment patterns
