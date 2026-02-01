---
name: angular-fire
description: Best practices and code patterns for @angular/fire version 20+, integrating Firestore and Auth with Signals and DDD architecture.
---

# AngularFire & Firebase Patterns Skill

## 🎯 Purpose
This skill provides implementation patterns for using `@angular/fire` in a **Zoneless, Signal-first, and DDD-compliant** Angular 20 application.

## 🛠️ Core Patterns

### 1. Repository Implementation (Infrastructure)
How to implement a Domain Repository using Firestore and Signals.

```typescript
// src/app/integration/persistence/task-firestore.repository.ts
import { inject, Injectable } from '@angular/core';
import { Firestore, collection, collectionData, query, where, doc, setDoc } from '@angular/fire/firestore';
import { toSignal } from '@angular/core/rxjs-interop';
import { TaskRepository } from '@domain/repositories';
import { TaskEntity } from '@domain/entities';

@Injectable({ providedIn: 'root' })
export class TaskFirestoreRepository implements TaskRepository {
  private firestore = inject(Firestore);
  private collection = collection(this.firestore, 'tasks');

  // Return Observable (Infrastructure Standard)
  findByWorkspace(workspaceId: string): Observable<TaskEntity[]> {
    const q = query(this.collection, where('workspaceId', '==', workspaceId));
    return collectionData(q, { idField: 'id' }) as Observable<TaskEntity[]>;
  }

  async save(task: TaskEntity): Promise<void> {
    const docRef = doc(this.firestore, `tasks/${task.id}`);
    await setDoc(docRef, task);
  }
}
```

### 2. Signal-Based Auth State (Account Module)
Standard pattern for building an Auth Store.

```typescript
// src/app/account/application/stores/auth.store.ts
import { inject } from '@angular/core';
import { Auth, user } from '@angular/fire/auth';
import { toSignal } from '@angular/core/rxjs-interop';
import { signalStore, withState, withComputed } from '@ngrx/signals';

export const AuthStore = signalStore(
  { providedIn: 'root' },
  withComputed(() => {
    const auth = inject(Auth);
    // Transform Firebase User stream to Signal
    const currentUser = toSignal(user(auth));
    
    return {
      user: currentUser,
      isAuthenticated: computed(() => !!currentUser()),
      userId: computed(() => currentUser()?.uid ?? null)
    };
  })
);
```

### 3. Error Mapping
Firebase errors should not reach the Domain or UI directly.

```typescript
try {
  await signInWithEmailAndPassword(this.auth, email, password);
} catch (error: any) {
  // Map Firebase Auth Error to Domain Error
  if (error.code === 'auth/wrong-password') {
    throw new InvalidCredentialsError();
  }
  throw new InfrastructureError(error.message);
}
```

## 🔐 Security Rules Checklist

- [ ] `request.auth != null` for all workspace data.
- [ ] Users can only read `workspaces` they are members of.
- [ ] Use `get(/databases/(default)/documents/workspaces/$(workspaceId)).data.members` for permission checks.
- [ ] No `allow read, write: if true;` even in development.

## 🚀 Optimization Patterns

- **Zoneless Safety**: Ensure all Firestore interactions are wrapped in Angular Signals to avoid missing change detection.
- **Snapshot Transformation**: Always map `Timestamp` objects to `number` (milliseconds) when converting to Domain Entities.
- **Batching**: Use `writeBatch()` for multiple updates to maintain atomicity and save costs.
