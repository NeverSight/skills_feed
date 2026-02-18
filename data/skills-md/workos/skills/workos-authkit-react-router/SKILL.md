---
name: workos-authkit-react-router
description: Integrate WorkOS AuthKit with React Router applications. Supports v6 and v7 (Framework, Data, Declarative modes). Use when project uses react-router, react-router-dom, or mentions React Router authentication.
---

# WorkOS AuthKit for React Router

## Decision Tree

```
1. Fetch README (BLOCKING)
2. Detect router mode
3. Follow README for that mode
4. Verify with checklist below
```

## Phase 1: Fetch SDK Documentation (BLOCKING)

**STOP - Do not write any code until this completes.**

WebFetch: `https://github.com/workos/authkit-react-router/blob/main/README.md`

The README is the source of truth. If this skill conflicts with README, **follow the README**.

## Phase 2: Detect Router Mode

| Mode           | Detection Signal                | Key Indicator             |
| -------------- | ------------------------------- | ------------------------- |
| v7 Framework   | `react-router.config.ts` exists | Routes in `app/routes/`   |
| v7 Data        | `createBrowserRouter` in source | Loaders in route config   |
| v7 Declarative | `<BrowserRouter>` component     | Routes as JSX, no loaders |
| v6             | package.json version `"6.x"`    | Similar to v7 Declarative |

**Detection order:**

1. Check for `react-router.config.ts` (Framework mode)
2. Grep for `createBrowserRouter` (Data mode)
3. Check package.json version (v6 vs v7)
4. Default to Declarative if v7 with `<BrowserRouter>`

## Phase 3: Follow README

Based on detected mode, apply the corresponding README section. The README contains current API signatures and code patterns.

## Critical Distinctions

### authLoader vs authkitLoader

| Function        | Purpose                   | Where to use           |
| --------------- | ------------------------- | ---------------------- |
| `authLoader`    | OAuth callback handler    | Callback route ONLY    |
| `authkitLoader` | Fetch user data in routes | Any route needing auth |

**Common mistake:** Using `authkitLoader` for callback route. Use `authLoader()`.

### Root Route Requirement

Auth loader MUST be on root route for child routes to access auth context.

**Wrong:** Auth loader only on `/dashboard`
**Right:** Auth loader on `/` (root), children inherit context

## Environment Variables

Required in `.env` or `.env.local`:

- `WORKOS_API_KEY` - starts with `sk_`
- `WORKOS_CLIENT_ID` - starts with `client_`
- `WORKOS_REDIRECT_URI` - full URL (e.g., `http://localhost:3000/auth/callback`)
- `WORKOS_COOKIE_PASSWORD` - 32+ chars (server modes only)

## Verification Checklist

After implementation, verify:

- [ ] SDK installed in node_modules (package name from README)
- [ ] Callback route path matches `WORKOS_REDIRECT_URI` path segment
- [ ] Auth loader/provider on root route (not just child routes)
- [ ] Build succeeds: `npm run build` exits 0
- [ ] Correct mode pattern applied (loaders vs hooks)

## Error Recovery

### "loader is not a function"

**Cause:** Using loader pattern in Declarative/v6 mode
**Fix:** Declarative/v6 modes use `AuthKitProvider` + `useAuth` hook, not loaders

### Auth state not available in child routes

**Cause:** Auth loader missing from root route
**Fix:** Add `authkitLoader` (or `AuthKitProvider`) to root route so children inherit context

### useAuth returns undefined

**Cause:** Missing `AuthKitProvider` wrapper
**Fix:** Wrap app with `AuthKitProvider` (required for Declarative/v6 modes)

### Callback route 404

**Cause:** Route path mismatch with `WORKOS_REDIRECT_URI`
**Fix:** Extract exact path from env var, create route at that path

### "Module not found" for SDK

**Cause:** SDK not installed
**Fix:** Install SDK, wait for completion, verify `node_modules` before writing imports
