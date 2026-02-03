---
name: account-identity
description: Identity and account patterns for src/app/account, including AngularFire Auth integration, signal-first auth state, route guards, and security boundaries; use when touching auth, user/session state, or account UI flows.
---

# Account / Identity

## Intent
Keep authentication and identity state correct, observable, and isolated from other bounded contexts.

## Boundaries
- Treat identity as a separate context: other modules depend on identity signals/tokens, not on Firebase Auth types.
- Do not leak platform objects (Firebase User, JWT claims) into Domain models.

## Signal-First Auth State
- Represent the current session as signals (user, isAuthenticated, userId, claims).
- Convert Observable streams to signals at the store/facade boundary.
- Ensure cleanup is automatic (use Angular signal interop helpers and lifecycle-aware patterns).

## Authorization
- Prefer explicit permissions signals (e.g., canReadWorkspace, canManageMembers) derived from claims/membership.
- Keep permission rules centralized (one store/service), not duplicated across components.

## Routing
- Use functional guards and `inject()`.
- Guard by signals (not by async subscribe-in-guard side effects).

## Error Handling
- Map provider errors (Firebase/HTTP) to app-level error types before exposing to UI.
- UI should render stable error states; avoid throwing raw platform errors.

## Security Checklist
- Never rely on the client for authorization.
- Treat security rules / server checks as the enforcement mechanism.
- Avoid persisting secrets in source code; use environment configuration.
