---
name: angularfire
description: AngularFire library for integrating Firebase services (Authentication, Firestore, Storage, Functions, Analytics) with Angular applications. Use when building Angular apps with Firebase backend, implementing authentication, real-time database, cloud storage, serverless functions, or Firebase analytics. Covers v20+ with standalone components.
license: MIT
---

# AngularFire Integration Skill

Master Firebase integration with Angular 20+ using AngularFire v20+. This skill covers authentication, Firestore database, cloud storage, cloud functions, and best practices for reactive state management with Signals.

## 📋 Rules

### Core Integration
- **MUST** use `provideFirebaseApp()` + `initializeApp()` in `app.config.ts` providers
- **MUST** use modular API imports: `provideAuth(() => getAuth())`, `provideFirestore(() => getFirestore())`
- **MUST NOT** use compatibility API (`@angular/fire/compat/*`)
- **MUST** store Firebase config in environment files
- **MUST NOT** hardcode API keys or secrets in version control

### Authentication
- **MUST** use `inject(Auth)` for authentication service
- **MUST** use `toSignal()` to convert `authState()` observable to Signal
- **MUST** provide `initialValue: null` when converting auth state
- **MUST** manage auth state in NgRx Signals store
- **MUST NOT** use manual subscriptions for auth state

### Firestore Database
- **MUST** use `inject(Firestore)` for database service
- **MUST** convert Firestore observables (`collectionData()`, `docData()`) to Signals using `toSignal()`
- **MUST** use query constraints (`where()`, `orderBy()`, `limit()`) for filtered reads
- **MUST** validate user input BEFORE database operations
- **MUST NOT** fetch entire collections without constraints
- **MUST** use `rxMethod()` with `tapResponse()` for async operations in stores
- **MUST** define security rules in `firestore.rules`
- **MUST NOT** use `allow read, write: if true` in production

### Cloud Storage
- **MUST** use `inject(Storage)` for storage service
- **MUST** validate file size and type BEFORE upload
- **MUST** define security rules in `storage.rules`
- **MUST** handle upload errors with user feedback
- **MUST NOT** expose file URLs without validation

### Cloud Functions
- **MUST** use `inject(Functions)` for functions service
- **MUST** use `httpsCallable()` with proper TypeScript typing
- **MUST** configure timeout for functions
- **MUST** handle function errors explicitly

### Error Handling
- **MUST** handle specific Firebase error codes (`auth/*`, `storage/*`, `functions/*`)
- **MUST** provide user-friendly error messages
- **MUST NOT** expose internal error details to users
- **MUST NOT** silently swallow errors

### Repository Pattern
- **MUST** encapsulate Firebase operations in repository layer (infrastructure)
- **MUST** convert Firestore documents to domain entities in repository
- **MUST NOT** expose Firestore types in domain layer
- **MUST NOT** place Firebase operations in components or application layer

### Security Rules
- **MUST** implement authentication checks in Firestore rules (`request.auth != null`)
- **MUST** implement user-specific access control (`resource.data.userId == request.auth.uid`)
- **MUST** test security rules with Firebase emulator
- **MUST NOT** deploy rules without testing

## 📖 Context

### When to Use This Skill

Activate this skill when:
- Setting up Firebase in Angular applications
- Implementing authentication flows (email/password, OAuth providers)
- Working with Firestore real-time database
- Handling file uploads to Firebase Storage
- Calling Firebase Cloud Functions
- Managing offline persistence
- Configuring security rules
- Integrating Firebase with NgRx Signals stores

### What is AngularFire?

AngularFire is the official Angular library for Firebase:
- **Firebase Authentication**: User authentication and authorization
- **Cloud Firestore**: NoSQL real-time database
- **Realtime Database**: Legacy real-time database
- **Cloud Storage**: File storage and serving
- **Cloud Functions**: Serverless backend functions
- **Analytics**: User analytics and tracking
- **RxJS Integration**: Observable-based APIs
- **Angular Standalone Support**: Full support for standalone components

### Prerequisites

**Required:**
- Angular 20+ project with standalone components
- Firebase project (create at https://console.firebase.google.com)
- AngularFire v20+ installed
- @ngrx/signals for state management

**Installation:**
```bash
# Install AngularFire and Firebase SDK
pnpm install @angular/fire firebase

# Or using Angular CLI
ng add @angular/fire
```

### Step-by-Step Workflows

#### 1. Initial Setup

**Firebase Configuration:**
```typescript
// src/environments/environment.ts
export const environment = {
  production: false,
  firebase: {
    apiKey: "YOUR_API_KEY",
    authDomain: "your-app.firebaseapp.com",
    projectId: "your-project-id",
    storageBucket: "your-app.appspot.com",
    messagingSenderId: "123456789",
    appId: "1:123456789:web:abcdef",
    measurementId: "G-XXXXXXXXXX"
  }
};
```

**App Configuration (Standalone):**
```typescript
// app.config.ts
import { ApplicationConfig } from '@angular/core';
import { provideFirebaseApp, initializeApp } from '@angular/fire/app';
import { provideAuth, getAuth } from '@angular/fire/auth';
import { provideFirestore, getFirestore } from '@angular/fire/firestore';
import { provideStorage, getStorage } from '@angular/fire/storage';
import { provideFunctions, getFunctions } from '@angular/fire/functions';
import { provideAnalytics, getAnalytics } from '@angular/fire/analytics';
import { environment } from './environments/environment';

export const appConfig: ApplicationConfig = {
  providers: [
    provideFirebaseApp(() => initializeApp(environment.firebase)),
    provideAuth(() => getAuth()),
    provideFirestore(() => getFirestore()),
    provideStorage(() => getStorage()),
    provideFunctions(() => getFunctions()),
    provideAnalytics(() => getAnalytics()),
  ]
};
```

#### 2. Authentication Implementation

**Auth Service:**
```typescript
import { Auth, signInWithEmailAndPassword, createUserWithEmailAndPassword, 
         signOut, user, User } from '@angular/fire/auth';
import { inject } from '@angular/core';
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private auth = inject(Auth);
  
  // Observable of current user
  user$ = user(this.auth);
  
  async signIn(email: string, password: string) {
    return signInWithEmailAndPassword(this.auth, email, password);
  }
  
  async signUp(email: string, password: string) {
    return createUserWithEmailAndPassword(this.auth, email, password);
  }
  
  async signOut() {
    return signOut(this.auth);
  }
}
```

**Auth Store with Signals:**
```typescript
import { signalStore, withState, withMethods } from '@ngrx/signals';
import { rxMethod } from '@ngrx/signals/rxjs-interop';
import { inject } from '@angular/core';
import { Auth, user, User } from '@angular/fire/auth';
import { pipe, switchMap, tap } from 'rxjs';
import { toSignal } from '@angular/core/rxjs-interop';

interface AuthState {
  user: User | null;
  loading: boolean;
}

export const AuthStore = signalStore(
  { providedIn: 'root' },
  withState<AuthState>({ user: null, loading: false }),
  withMethods((store, auth = inject(Auth)) => {
    const user$ = user(auth);
    const userSignal = toSignal(user$, { initialValue: null });
    
    return {
      user: userSignal,
      // Additional methods for sign in, sign out, etc.
    };
  })
);
```

#### 3. Firestore Database Operations

**Firestore Repository (Infrastructure):**
```typescript
import { Firestore, collection, collectionData, doc, docData, 
         addDoc, updateDoc, deleteDoc, query, where } from '@angular/fire/firestore';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

export interface Task {
  id?: string;
  title: string;
  completed: boolean;
  userId: string;
}

@Injectable({ providedIn: 'root' })
export class TaskRepository {
  private firestore = inject(Firestore);
  private tasksCollection = collection(this.firestore, 'tasks');
  
  // Get all tasks for a user
  getUserTasks(userId: string): Observable<Task[]> {
    const q = query(this.tasksCollection, where('userId', '==', userId));
    return collectionData(q, { idField: 'id' });
  }
  
  // Get single task
  getTask(id: string): Observable<Task> {
    const taskDoc = doc(this.firestore, `tasks/${id}`);
    return docData(taskDoc, { idField: 'id' });
  }
  
  // Create task
  async createTask(task: Omit<Task, 'id'>): Promise<string> {
    const docRef = await addDoc(this.tasksCollection, task);
    return docRef.id;
  }
  
  // Update task
  async updateTask(id: string, changes: Partial<Task>): Promise<void> {
    const taskDoc = doc(this.firestore, `tasks/${id}`);
    return updateDoc(taskDoc, changes);
  }
  
  // Delete task
  async deleteTask(id: string): Promise<void> {
    const taskDoc = doc(this.firestore, `tasks/${id}`);
    return deleteDoc(taskDoc);
  }
}
```

**Firestore Store Integration:**
```typescript
import { signalStore, withState, withMethods } from '@ngrx/signals';
import { rxMethod } from '@ngrx/signals/rxjs-interop';
import { inject } from '@angular/core';
import { TaskRepository, Task } from './task.repository';
import { pipe, switchMap, tap } from 'rxjs';
import { tapResponse } from '@ngrx/operators';

interface TaskState {
  tasks: Task[];
  loading: boolean;
  error: string | null;
}

export const TaskStore = signalStore(
  { providedIn: 'root' },
  withState<TaskState>({ tasks: [], loading: false, error: null }),
  withMethods((store, repo = inject(TaskRepository)) => ({
    loadUserTasks: rxMethod<string>(
      pipe(
        tap(() => patchState(store, { loading: true })),
        switchMap((userId) => repo.getUserTasks(userId)),
        tapResponse({
          next: (tasks) => patchState(store, { tasks, loading: false }),
          error: (error) => patchState(store, { 
            error: error.message, 
            loading: false 
          })
        })
      )
    ),
    
    async addTask(task: Omit<Task, 'id'>) {
      try {
        await repo.createTask(task);
      } catch (error) {
        patchState(store, { error: error.message });
      }
    }
  }))
);
```

#### 4. Cloud Storage Operations

**Storage Service:**
```typescript
import { Storage, ref, uploadBytesResumable, getDownloadURL, 
         deleteObject } from '@angular/fire/storage';
import { inject, Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class StorageService {
  private storage = inject(Storage);
  
  // Upload file with progress tracking
  uploadFile(path: string, file: File) {
    const storageRef = ref(this.storage, path);
    return uploadBytesResumable(storageRef, file);
  }
  
  // Get download URL
  async getDownloadURL(path: string): Promise<string> {
    const storageRef = ref(this.storage, path);
    return getDownloadURL(storageRef);
  }
  
  // Delete file
  async deleteFile(path: string): Promise<void> {
    const storageRef = ref(this.storage, path);
    return deleteObject(storageRef);
  }
}
```

#### 5. Cloud Functions

**Functions Service:**
```typescript
import { Functions, httpsCallable } from '@angular/fire/functions';
import { inject, Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class FunctionsService {
  private functions = inject(Functions);
  
  // Call a cloud function
  async sendEmail(to: string, subject: string, body: string) {
    const callable = httpsCallable(this.functions, 'sendEmail');
    return callable({ to, subject, body });
  }
}
```

### Security Rules Examples

**Firestore Rules:**
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can only read/write their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Tasks belong to users
    match /tasks/{taskId} {
      allow read, write: if request.auth != null && 
                           resource.data.userId == request.auth.uid;
    }
  }
}
```

**Storage Rules:**
```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // Users can only upload to their own folder
    match /users/{userId}/{allPaths=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

### Offline Persistence

```typescript
// Enable offline persistence
import { enableIndexedDbPersistence } from '@angular/fire/firestore';

provideFirebaseApp(() => {
  const app = initializeApp(environment.firebase);
  const firestore = getFirestore(app);
  enableIndexedDbPersistence(firestore);
  return app;
});
```

### Error Handling Patterns

**Auth Errors:**
```typescript
try {
  await signIn(email, password);
} catch (error: any) {
  switch (error.code) {
    case 'auth/user-not-found':
      return 'User not found';
    case 'auth/wrong-password':
      return 'Invalid password';
    case 'auth/too-many-requests':
      return 'Too many attempts, try again later';
    default:
      return 'Authentication failed';
  }
}
```

**Firestore Errors:**
```typescript
try {
  await updateTask(id, changes);
} catch (error: any) {
  switch (error.code) {
    case 'permission-denied':
      return 'Access denied';
    case 'not-found':
      return 'Task not found';
    case 'unavailable':
      return 'Service temporarily unavailable';
    default:
      return 'Operation failed';
  }
}
```

### 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Firebase not initialized | Check `provideFirebaseApp()` in app.config.ts |
| Auth errors | Verify Firebase config and enable auth methods in console |
| Firestore permission denied | Check security rules and user authentication |
| Storage upload fails | Verify storage rules and file size limits |
| Functions timeout | Increase timeout or optimize function code |
| Analytics not tracking | Check analytics is enabled in Firebase console |

### 📖 References

- [AngularFire Documentation](https://github.com/angular/angularfire)
- [Firebase Documentation](https://firebase.google.com/docs)
- [Firestore Guide](https://firebase.google.com/docs/firestore)
- [Firebase Auth Guide](https://firebase.google.com/docs/auth)
- [Cloud Storage Guide](https://firebase.google.com/docs/storage)

---

## 📂 Recommended Placement

**Project-level skill:**
```
/.github/skills/angularfire/SKILL.md
```

Copilot will load this when working with Firebase in Angular applications.
