---
name: workos-authkit-base
description: Architectural reference for WorkOS AuthKit integrations. Fetch README first for implementation details.
---

# WorkOS AuthKit Base Template

## First Action: Fetch README

Before any implementation, fetch the framework-specific README:

```
WebFetch: {sdk-package-name} README from npmjs.com or GitHub
```

README is the source of truth for: install commands, imports, API usage, code patterns.

## Task Structure (Required)

| Phase | Task      | Blocked By         | Purpose                           |
| ----- | --------- | ------------------ | --------------------------------- |
| 1     | preflight | -                  | Verify env vars, detect framework |
| 2     | install   | preflight          | Install SDK package               |
| 3     | callback  | install            | Create OAuth callback route       |
| 4     | provider  | install            | Setup auth context/middleware     |
| 5     | ui        | callback, provider | Add sign-in/out UI                |
| 6     | verify    | ui                 | Build confirmation                |

## Decision Trees

### Package Manager Detection

```
pnpm-lock.yaml? → pnpm
yarn.lock? → yarn
bun.lockb? → bun
else → npm
```

### Provider vs Middleware

```
Client-side framework? → AuthKitProvider wraps app
Server-side framework? → Middleware handles sessions
Hybrid (Next.js)? → Both may be needed
```

### Callback Route Location

Extract path from `WORKOS_REDIRECT_URI` → create route at that exact path.

## Environment Variables

| Variable                 | Purpose                        | When Required |
| ------------------------ | ------------------------------ | ------------- |
| `WORKOS_API_KEY`         | Server authentication          | Server SDKs   |
| `WORKOS_CLIENT_ID`       | Client identification          | All SDKs      |
| `WORKOS_REDIRECT_URI`    | OAuth callback URL             | Server SDKs   |
| `WORKOS_COOKIE_PASSWORD` | Session encryption (32+ chars) | Server SDKs   |

Note: Some frameworks use prefixed variants (e.g., `NEXT_PUBLIC_*`). Check README.

## Verification Checklists

### After Install

- [ ] SDK package installed in node_modules
- [ ] No install errors in output

### After Callback Route

- [ ] Route file exists at path matching `WORKOS_REDIRECT_URI`
- [ ] Imports SDK callback handler (not custom OAuth)

### After Provider/Middleware

- [ ] Provider wraps entire app (client-side)
- [ ] Middleware configured in correct location (server-side)

### After UI

- [ ] Home page shows conditional auth state
- [ ] Uses SDK functions for sign-in/out URLs

### Final Verification

- [ ] Build completes with exit code 0
- [ ] No import resolution errors

## Error Recovery

### Module not found

- [ ] Verify install completed successfully
- [ ] Verify SDK exists in node_modules
- [ ] Re-run install if missing

### Build import errors

- [ ] Delete `node_modules`, reinstall
- [ ] Verify package.json has SDK dependency

### Invalid redirect URI

- [ ] Compare route path to `WORKOS_REDIRECT_URI`
- [ ] Paths must match exactly

### Cookie password error

- [ ] Verify `WORKOS_COOKIE_PASSWORD` is 32+ characters
- [ ] Generate new: `openssl rand -base64 32`

### Auth state not persisting

- [ ] Verify provider wraps entire app
- [ ] Check middleware is in correct location

## Critical Rules

1. **Install SDK before writing imports** - never create import statements for uninstalled packages
2. **Use SDK functions** - never construct OAuth URLs manually
3. **Follow README patterns** - SDK APIs change between versions
4. **Extract callback path from env** - don't hardcode `/auth/callback`
