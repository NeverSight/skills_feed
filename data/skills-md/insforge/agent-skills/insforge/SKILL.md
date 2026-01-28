---
name: insforge
description: |
  Build applications with InsForge Backend-as-a-Service. Use when developers need to:
  (1) Set up backend infrastructure (create tables, storage buckets, deploy functions, configure auth/AI)
  (2) Integrate InsForge SDK into frontend applications (database CRUD, auth flows, file uploads, AI operations, real-time messaging)
  (3) Deploy frontend applications to InsForge hosting

  IMPORTANT: Before any backend work, you MUST have the user's Project URL and API Key. If not provided, ask the user first.

  Key distinction: Backend configuration uses HTTP API calls to the InsForge project URL. Client integration uses the @insforge/sdk in application code.
license: MIT
metadata:
  author: insforge
  version: "1.0.0"
  organization: InsForge
  date: January 2026
---

# InsForge Agent Skill

## STOP: Check Credentials First

**You MUST have these before making ANY backend API calls:**

| Credential | Format | Required For |
|------------|--------|--------------|
| **Project URL** | `https://{project-id}.{region}.insforge.app` | All API calls |
| **API Key** | `ik_xxxx...` | Authorization header |

**Action:** If the user has not provided both credentials, **ASK NOW** before proceeding.

```
Do you have an InsForge project? I'll need:
1. Project URL (e.g., https://abc123.us-east-1.insforge.app)
2. API Key (starts with ik_)

You can find these in InsForge Dashboard → Project Settings.
```

---

## When to Use Which Documentation

### Use `sdk-integration.md` files when:
- Integrating InsForge services into the **user's frontend application**
- Implementing features that run in the browser or client app
- Writing code that uses `@insforge/sdk` methods
- Examples: User login flow, fetching data, uploading files, real-time subscriptions

### Use `backend-configuration.md` files when:
- **Configuring the InsForge backend** before the app can use a feature
- Creating database tables, storage buckets, or deploying serverless functions
- Setting up real-time channels or database triggers
- Managing auth settings, AI configurations, or deployments
- Examples: Creating a `posts` table, enabling OAuth providers, deploying an edge function

## Typical Workflow

1. **Backend Configuration** → Configure infrastructure via HTTP API
2. **SDK Integration** → Use SDK in application code

**Example: Adding file uploads**
1. First create a storage bucket → see [storage/backend-configuration.md](storage/backend-configuration.md)
2. Then implement upload in the app → see [storage/sdk-integration.md](storage/sdk-integration.md)

**Example: Adding user authentication**
1. First configure auth settings → see [auth/backend-configuration.md](auth/backend-configuration.md)
2. Then implement login/signup → see [auth/sdk-integration.md](auth/sdk-integration.md)

## First Step: Get Backend Metadata

**Always get the backend metadata first** before doing any work. This gives you the complete picture of the current project structure.

```
GET /api/metadata
Authorization: Bearer {admin-token-or-api-key}
```

This returns the full backend state including:
- **Database**: Tables, columns, relationships, indexes, RLS policies
- **Auth**: Configuration, OAuth providers, user stats
- **Storage**: Buckets and visibility settings
- **Functions**: Deployed functions and status
- **AI**: Configured models
- **Realtime**: Channel patterns

Understanding the existing backend structure before making changes prevents errors and helps you build on what's already there.

## Quick Setup

```bash
npm install @insforge/sdk@latest
```

```javascript
import { createClient } from '@insforge/sdk'

const insforge = createClient({
  baseUrl: 'https://your-project.region.insforge.app',
  anonKey: 'your-anon-key'
})
```

## Module Reference

| Module | SDK Integration | Backend Configuration |
|--------|-----------------|----------------------|
| **Database** | [database/sdk-integration.md](database/sdk-integration.md) | [database/backend-configuration.md](database/backend-configuration.md) |
| **Auth** | [auth/sdk-integration.md](auth/sdk-integration.md) | [auth/backend-configuration.md](auth/backend-configuration.md) |
| **Storage** | [storage/sdk-integration.md](storage/sdk-integration.md) | [storage/backend-configuration.md](storage/backend-configuration.md) |
| **Functions** | [functions/sdk-integration.md](functions/sdk-integration.md) | [functions/backend-configuration.md](functions/backend-configuration.md) |
| **AI** | [ai/sdk-integration.md](ai/sdk-integration.md) | [ai/backend-configuration.md](ai/backend-configuration.md) |
| **Real-time** | [realtime/sdk-integration.md](realtime/sdk-integration.md) | [realtime/backend-configuration.md](realtime/backend-configuration.md) |
| **Deployments** | — | [deployments/workflow.md](deployments/workflow.md) |
| **Logs** | — | [logs/debugging.md](logs/debugging.md) |

### What Each Module Covers

| Module | sdk-integration.md | backend-configuration.md |
|--------|-------------------|-------------------------|
| **Database** | CRUD operations, filters, pagination | Create tables, RLS policies, triggers, indexes |
| **Auth** | Sign up/in, OAuth, sessions, profiles | Auth config, user management, anon tokens |
| **Storage** | Upload, download, delete files | Create/manage buckets |
| **Functions** | Invoke functions | Deploy, update, delete functions |
| **AI** | Chat, images, embeddings | Models, credits, usage stats |
| **Real-time** | Connect, subscribe, publish events | Channel patterns, database triggers |
| **Deployments** | — | Deploy frontend apps |
| **Logs** | — | Fetch container logs for debugging |

## SDK Quick Reference

All SDK methods return `{ data, error }`.

| Module | Methods |
|--------|---------|
| `insforge.database` | `.from().select()`, `.insert()`, `.update()`, `.delete()`, `.rpc()` |
| `insforge.auth` | `.signUp()`, `.signInWithPassword()`, `.signInWithOAuth()`, `.signOut()`, `.getCurrentSession()` |
| `insforge.storage` | `.from().upload()`, `.uploadAuto()`, `.download()`, `.remove()` |
| `insforge.functions` | `.invoke()` |
| `insforge.ai` | `.chat.completions.create()`, `.images.generate()`, `.embeddings.create()` |
| `insforge.realtime` | `.connect()`, `.subscribe()`, `.publish()`, `.on()`, `.disconnect()` |

## Backend API Quick Reference

**Base URL**: `https://your-project.region.insforge.app`

**Authentication**: `Authorization: Bearer {admin-token-or-api-key}`

| Task | Endpoint |
|------|----------|
| Execute SQL | `POST /api/database/advance/rawsql` |
| Create bucket | `POST /api/storage/buckets` |
| Deploy function | `POST /api/functions` |
| Configure auth | `PUT /api/auth/config` |
| Get metadata | `GET /api/metadata` |
| Deploy frontend | `POST /api/deployments` |
| Get logs | `GET /api/logs/{source}` |

## Important Notes

- **Database inserts require array format**: `insert([{...}])` not `insert({...})`
- **Storage**: Save both `url` AND `key` to database for download/delete operations
- **Functions invoke URL**: `/functions/{slug}` (without `/api` prefix)
- **Use Tailwind CSS v3.4** (do not upgrade to v4)
