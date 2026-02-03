---
name: angularfire
description: Angular wrapper for Firebase with dependency injection, RxJS observables, and Zone.js integration
metadata:
  author: Gerome Grignon
  version: "2026.2.1"
  source: Generated from https://github.com/angular/angularfire, scripts located at https://github.com/angular-sanctuary/angular-agent-skills
---

> The skill is based on AngularFire v18.0.1, generated at 2026-02-01.

AngularFire is the official Angular library for Firebase. It provides Angular-native wrappers around the Firebase JS SDK with:

- **Dependency Injection** - Firebase services as injectable Angular services
- **Zone.js Integration** - Automatic zone wrapping for change detection stability
- **RxJS Observables** - Real-time data streams as Observables
- **Lazy Loading** - Dynamic imports to reduce bundle size
- **SSR Support** - Compatible with Angular Universal/SSR
- **Router Guards** - Built-in auth guards for route protection

## When to Apply

Use this skill when:

- **Setting up Firebase** in an Angular application
- Implementing **Firebase Authentication** (sign-in, sign-out, auth guards)
- Working with **Cloud Firestore** (collections, documents, queries, real-time updates)
- Using **Realtime Database** for real-time data synchronization
- Managing **file uploads/downloads** with Cloud Storage
- Calling **Cloud Functions** from Angular
- Implementing **analytics**, **performance monitoring**, or **remote config**
- Setting up **push notifications** with Cloud Messaging
- Protecting routes with **auth guards**
- Configuring **Firebase emulators** for local development
- Building **server-side rendered** Angular apps with Firebase

Do NOT use this skill when:

- Using Firebase JS SDK directly without Angular wrappers
- Working with non-Firebase backends
- The Firebase product you need is not supported by AngularFire

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Setup & Configuration | Firebase app initialization and dependency injection | [core-setup](references/core-setup.md) |
| Zone Wrappers | Understanding zone integration for app stability | [core-zones](references/core-zones.md) |

## Firebase Products

### Database & Storage

| Topic | Description | Reference |
|-------|-------------|-----------|
| Cloud Firestore | Collections, documents, queries, real-time data | [product-firestore](references/product-firestore.md) |
| Realtime Database | Lists, objects, queries, and real-time sync | [product-realtime-database](references/product-realtime-database.md) |
| Cloud Storage | File uploads, downloads, and management | [product-storage](references/product-storage.md) |

### Authentication & Security

| Topic | Description | Reference |
|-------|-------------|-----------|
| Authentication | Auth state, observables, sign-in methods, SSR support | [product-auth](references/product-auth.md) |
| Auth Guards | Route protection with customizable pipes | [product-auth-guards](references/product-auth-guards.md) |
| App Check | Protecting backend resources from abuse | [product-app-check](references/product-app-check.md) |

### Backend & Functions

| Topic | Description | Reference |
|-------|-------------|-----------|
| Cloud Functions | Calling HTTPS callable functions | [product-functions](references/product-functions.md) |

### Analytics & Monitoring

| Topic | Description | Reference |
|-------|-------------|-----------|
| Analytics | Event tracking and user properties | [product-analytics](references/product-analytics.md) |
| Performance Monitoring | Custom traces and metrics | [product-performance](references/product-performance.md) |

### Configuration & Messaging

| Topic | Description | Reference |
|-------|-------------|-----------|
| Remote Config | Feature flags and dynamic configuration | [product-remote-config](references/product-remote-config.md) |
| Cloud Messaging | Push notifications with service workers | [product-messaging](references/product-messaging.md) |

### AI

| Topic | Description | Reference |
|-------|-------------|-----------|
| Vertex AI | Gemini generative AI models | [product-vertexai](references/product-vertexai.md) |

## Advanced Topics

| Topic | Description | Reference |
|-------|-------------|-----------|
| Firebase Hosting Deployment | Deploy to Firebase Hosting with CLI schematics | [advanced-deploy](references/advanced-deploy.md) |
| Server-Side Rendering | Angular Universal with Firebase | [advanced-ssr](references/advanced-ssr.md) |
| Emulator Suite | Local development with Firebase emulators | [advanced-emulators](references/advanced-emulators.md) |
