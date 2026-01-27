---
name: firebase-data-connect
description: Firebase Data Connect integration for GraphQL-based data access with PostgreSQL. Use when building GraphQL schemas, queries, mutations, or integrating Firebase Data Connect with Angular applications. Supports type-safe generated SDKs, real-time subscriptions, and server-side data validation.
license: Complete terms in LICENSE.txt
---

# Firebase Data Connect

Expert guidance for integrating Firebase Data Connect with Angular applications, providing type-safe GraphQL operations backed by PostgreSQL.

## When to Use This Skill

Activate this skill when you need to:
- Define GraphQL schemas for Firebase Data Connect
- Create queries and mutations for data operations
- Integrate Data Connect with Angular services
- Generate type-safe TypeScript SDKs
- Implement real-time data subscriptions
- Configure Data Connect connectors and services
- Migrate from Firestore to Data Connect
- Optimize GraphQL query performance

## What is Firebase Data Connect?

Firebase Data Connect is a relational database service that provides:
- **GraphQL API** for type-safe data access
- **PostgreSQL** backend for relational data
- **Generated SDKs** for TypeScript/JavaScript
- **Real-time subscriptions** for live data
- **Server-side validation** and security rules
- **Local emulator** for development and testing

## Prerequisites

### Required Tools
- Firebase CLI (`npm install -g firebase-tools`)
- Node.js 18+ and npm/pnpm
- Angular 20+ project
- Firebase project with Data Connect enabled

### Installation

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login to Firebase
firebase login

# Initialize Data Connect in your project
firebase init dataconnect

# Install Angular Fire (if not already installed)
npm install @angular/fire
```

## Project Structure

```
dataconnect/
├── dataconnect.yaml          # Connector configuration
├── schema/
│   ├── schema.gql            # GraphQL schema definitions
│   └── types.gql             # Custom types and enums
├── queries/
│   ├── users.gql             # User queries
│   └── workspace.gql         # Workspace queries
├── mutations/
│   ├── createUser.gql        # User mutations
│   └── updateWorkspace.gql   # Workspace mutations
└── seed_data.gql             # Development seed data

src/dataconnect-generated/    # Generated TypeScript SDK
└── index.ts                  # Auto-generated type-safe operations
```

## Schema Definition

### Basic Schema Example

```graphql
# dataconnect/schema/schema.gql

type User @table {
  id: UUID! @default(expr: "uuidV4()")
  email: String! @unique
  displayName: String!
  photoURL: String
  createdAt: Timestamp! @default(expr: "request.time")
  updatedAt: Timestamp! @default(expr: "request.time")
  
  # Relationships
  workspaces: [WorkspaceMember!]! @relationFrom(field: "user")
}

type Workspace @table {
  id: UUID! @default(expr: "uuidV4()")
  name: String!
  description: String
  ownerId: UUID!
  createdAt: Timestamp! @default(expr: "request.time")
  
  # Relationships
  owner: User! @relation(fields: "ownerId")
  members: [WorkspaceMember!]! @relationFrom(field: "workspace")
}

type WorkspaceMember @table {
  id: UUID! @default(expr: "uuidV4()")
  userId: UUID!
  workspaceId: UUID!
  role: MemberRole!
  joinedAt: Timestamp! @default(expr: "request.time")
  
  # Relationships
  user: User! @relation(fields: "userId")
  workspace: Workspace! @relation(fields: "workspaceId")
  
  # Composite unique constraint
  @unique(fields: ["userId", "workspaceId"])
}

enum MemberRole {
  OWNER
  ADMIN
  MEMBER
  VIEWER
}
```

## Queries

### Query Definition

```graphql
# dataconnect/queries/users.gql

query GetUser($userId: UUID!) @auth(level: USER) {
  user(id: $userId) {
    id
    email
    displayName
    photoURL
    createdAt
  }
}

query ListUserWorkspaces($userId: UUID!) @auth(level: USER) {
  workspaceMembers(where: { userId: { eq: $userId } }) {
    workspace {
      id
      name
      description
      owner {
        id
        displayName
      }
    }
    role
    joinedAt
  }
}

query SearchWorkspaces($searchTerm: String!) @auth(level: USER) {
  workspaces(
    where: { 
      name: { contains: $searchTerm } 
    }
    orderBy: { createdAt: DESC }
    limit: 20
  ) {
    id
    name
    description
    owner {
      displayName
    }
    createdAt
  }
}
```

## Mutations

### Mutation Definition

```graphql
# dataconnect/mutations/workspace.gql

mutation CreateWorkspace(
  $name: String!
  $description: String
  $ownerId: UUID!
) @auth(level: USER) {
  workspace_insert(data: {
    name: $name
    description: $description
    ownerId: $ownerId
  }) {
    id
    name
    description
    createdAt
  }
}

mutation AddWorkspaceMember(
  $workspaceId: UUID!
  $userId: UUID!
  $role: MemberRole!
) @auth(level: USER) {
  workspaceMember_insert(data: {
    workspaceId: $workspaceId
    userId: $userId
    role: $role
  }) {
    id
    user {
      displayName
      email
    }
    role
    joinedAt
  }
}

mutation UpdateWorkspace(
  $id: UUID!
  $name: String
  $description: String
) @auth(level: USER) {
  workspace_update(
    id: $id
    data: {
      name: $name
      description: $description
    }
  ) {
    id
    name
    description
    updatedAt
  }
}
```

## Angular Integration

### Generated SDK Usage

```typescript
// src/app/infrastructure/firebase/data-connect.service.ts
import { Injectable, inject } from '@angular/core';
import { ConnectorConfig, getDataConnect } from '@angular/fire/data-connect';
import { 
  getUser, 
  listUserWorkspaces,
  createWorkspace,
  addWorkspaceMember 
} from '@/dataconnect-generated';

@Injectable({ providedIn: 'root' })
export class DataConnectService {
  private dataConnect = getDataConnect();
  
  // Execute query
  async getUserById(userId: string) {
    const result = await getUser(this.dataConnect, { userId });
    return result.data.user;
  }
  
  // Execute query with variables
  async getUserWorkspaces(userId: string) {
    const result = await listUserWorkspaces(this.dataConnect, { userId });
    return result.data.workspaceMembers;
  }
  
  // Execute mutation
  async createNewWorkspace(name: string, description: string, ownerId: string) {
    const result = await createWorkspace(this.dataConnect, {
      name,
      description,
      ownerId
    });
    return result.data.workspace_insert;
  }
}
```

### Repository Pattern

```typescript
// src/app/infrastructure/persistence/workspace-dataconnect.repository.ts
import { Injectable } from '@angular/core';
import { Observable, from } from 'rxjs';
import { map } from 'rxjs/operators';
import { DataConnectService } from '../firebase/data-connect.service';
import { IWorkspaceRepository } from '@domain/repositories/workspace.repository';
import { Workspace } from '@domain/workspace/workspace.entity';

@Injectable({ providedIn: 'root' })
export class WorkspaceDataConnectRepository implements IWorkspaceRepository {
  constructor(private dataConnect: DataConnectService) {}
  
  findById(id: string): Observable<Workspace | null> {
    return from(this.dataConnect.getWorkspaceById(id)).pipe(
      map(data => data ? this.toDomain(data) : null)
    );
  }
  
  findByOwnerId(ownerId: string): Observable<Workspace[]> {
    return from(this.dataConnect.getUserWorkspaces(ownerId)).pipe(
      map(members => members.map(m => this.toDomain(m.workspace)))
    );
  }
  
  save(workspace: Workspace): Observable<Workspace> {
    return from(this.dataConnect.createNewWorkspace(
      workspace.name,
      workspace.description,
      workspace.ownerId
    )).pipe(
      map(data => this.toDomain(data))
    );
  }
  
  private toDomain(data: any): Workspace {
    // Map Data Connect response to domain entity
    return new Workspace({
      id: data.id,
      name: data.name,
      description: data.description,
      ownerId: data.ownerId,
      createdAt: new Date(data.createdAt)
    });
  }
}
```

### NgRx Signals Integration

```typescript
// src/app/application/store/workspace.store.ts
import { signalStore, withState, withMethods } from '@ngrx/signals';
import { rxMethod } from '@ngrx/signals/rxjs-interop';
import { pipe, switchMap, tap } from 'rxjs';
import { tapResponse } from '@ngrx/operators';
import { inject } from '@angular/core';
import { patchState } from '@ngrx/signals';
import { DataConnectService } from '@infrastructure/firebase/data-connect.service';

export const WorkspaceStore = signalStore(
  { providedIn: 'root' },
  withState({
    workspaces: [] as Workspace[],
    selectedWorkspace: null as Workspace | null,
    loading: false,
    error: null as string | null
  }),
  withMethods((store, dataConnect = inject(DataConnectService)) => ({
    loadUserWorkspaces: rxMethod<string>(
      pipe(
        tap(() => patchState(store, { loading: true, error: null })),
        switchMap((userId) => dataConnect.getUserWorkspaces(userId)),
        tapResponse({
          next: (workspaces) => patchState(store, { 
            workspaces, 
            loading: false 
          }),
          error: (error: Error) => patchState(store, { 
            error: error.message, 
            loading: false 
          })
        })
      )
    ),
    
    createWorkspace: rxMethod<{ name: string; description: string; ownerId: string }>(
      pipe(
        tap(() => patchState(store, { loading: true })),
        switchMap(({ name, description, ownerId }) => 
          dataConnect.createNewWorkspace(name, description, ownerId)
        ),
        tapResponse({
          next: (workspace) => patchState(store, (state) => ({
            workspaces: [...state.workspaces, workspace],
            loading: false
          })),
          error: (error: Error) => patchState(store, { 
            error: error.message, 
            loading: false 
          })
        })
      )
    )
  }))
);
```

## Configuration

### dataconnect.yaml

```yaml
# dataconnect/dataconnect.yaml
connectorId: my-connector
cloudSql:
  instanceId: my-instance
  database: my-database
schema:
  source: ./schema
  datasource:
    postgresql: {}
queries:
  source: ./queries
mutations:
  source: ./mutations
```

### Angular Fire Configuration

```typescript
// src/app/app.config.ts
import { ApplicationConfig } from '@angular/core';
import { provideFirebaseApp, initializeApp } from '@angular/fire/app';
import { provideDataConnect, getDataConnect } from '@angular/fire/data-connect';
import { environment } from './environments/environment';

export const appConfig: ApplicationConfig = {
  providers: [
    provideFirebaseApp(() => initializeApp(environment.firebase)),
    provideDataConnect(() => getDataConnect({
      connector: 'my-connector',
      location: 'us-central1'
    })),
  ]
};
```

## Local Development

### Start Emulator

```bash
# Start Data Connect emulator
firebase emulators:start --only dataconnect

# Run with seed data
firebase emulators:start --only dataconnect --import=./seed-data

# Generate TypeScript SDK
firebase dataconnect:sdk:generate --output=src/dataconnect-generated
```

### Seed Data

```graphql
# dataconnect/seed_data.gql
mutation SeedUsers {
  user1: user_insert(data: {
    email: "admin@example.com"
    displayName: "Admin User"
  }) { id }
  
  user2: user_insert(data: {
    email: "member@example.com"
    displayName: "Member User"
  }) { id }
}

mutation SeedWorkspaces {
  workspace1: workspace_insert(data: {
    name: "Default Workspace"
    description: "Main workspace"
    ownerId: "USER_ID_HERE"
  }) { id }
}
```

## Best Practices

### Schema Design

```typescript
// ✅ Good - Use proper relationships
type Post @table {
  authorId: UUID!
  author: User! @relation(fields: "authorId")
}

// ❌ Bad - Duplicating data
type Post @table {
  authorEmail: String
  authorName: String
}
```

### Query Optimization

```graphql
# ✅ Good - Request only needed fields
query GetWorkspace($id: UUID!) {
  workspace(id: $id) {
    id
    name
    owner { displayName }
  }
}

# ❌ Bad - Over-fetching
query GetWorkspace($id: UUID!) {
  workspace(id: $id) {
    id
    name
    description
    owner {
      id
      email
      displayName
      photoURL
      createdAt
      updatedAt
    }
    members {
      user {
        id
        email
        displayName
      }
    }
  }
}
```

### Error Handling

```typescript
// ✅ Good - Handle errors properly
async loadWorkspace(id: string) {
  try {
    const result = await getWorkspace(this.dataConnect, { id });
    if (result.errors) {
      throw new Error(result.errors[0].message);
    }
    return result.data.workspace;
  } catch (error) {
    console.error('Failed to load workspace:', error);
    throw error;
  }
}

// ❌ Bad - Ignore errors
async loadWorkspace(id: string) {
  const result = await getWorkspace(this.dataConnect, { id });
  return result.data.workspace;
}
```

## Security

### Authentication Rules

```graphql
# Require authentication
query GetUser($id: UUID!) @auth(level: USER) {
  user(id: $id) { ... }
}

# Require specific role
mutation DeleteWorkspace($id: UUID!) @auth(level: USER, expr: "auth.uid == resource.ownerId") {
  workspace_delete(id: $id) { id }
}
```

### Input Validation

```graphql
# Use constraints
type User @table {
  email: String! @unique
  displayName: String! @check(expr: "length(this) >= 3")
  age: Int @check(expr: "this >= 18")
}
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| SDK generation fails | Schema syntax errors | Run `firebase dataconnect:validate` |
| Query returns null | Missing @auth directive | Add proper authentication |
| Relationship error | Incorrect field references | Check @relation fields match column names |
| Emulator won't start | Port already in use | Change port in firebase.json or kill process |
| Type mismatch | Stale generated code | Re-run `firebase dataconnect:sdk:generate` |

## Migration from Firestore

```typescript
// Before (Firestore)
const docRef = doc(firestore, 'workspaces', id);
const docSnap = await getDoc(docRef);
const data = docSnap.data();

// After (Data Connect)
const result = await getWorkspace(dataConnect, { id });
const data = result.data.workspace;
```

## References

- [Firebase Data Connect Documentation](https://firebase.google.com/docs/data-connect)
- [GraphQL Schema Reference](https://firebase.google.com/docs/data-connect/schema)
- [AngularFire Data Connect](https://github.com/angular/angularfire/blob/main/docs/data-connect.md)
- [PostgreSQL Data Types](https://www.postgresql.org/docs/current/datatype.html)
