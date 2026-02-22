---
name: workos-authkit-react
description: Integrate WorkOS AuthKit with React single-page applications. Client-side only authentication. Use when the project is a React SPA without Next.js or React Router.
---

# WorkOS AuthKit for React (SPA)

## Decision Tree

```
START
  │
  ├─► Fetch README (BLOCKING)
  │   github.com/workos/authkit-react/blob/main/README.md
  │   README is source of truth. Stop if fetch fails.
  │
  ├─► Detect Build Tool
  │   ├─ vite.config.ts exists? → Vite
  │   └─ otherwise → Create React App
  │
  ├─► Set Env Var Prefix
  │   ├─ Vite → VITE_WORKOS_CLIENT_ID
  │   └─ CRA  → REACT_APP_WORKOS_CLIENT_ID
  │
  └─► Implement per README
```

## Critical: Build Tool Detection

| Marker File               | Build Tool | Env Prefix   | Access Pattern            |
| ------------------------- | ---------- | ------------ | ------------------------- |
| `vite.config.ts`          | Vite       | `VITE_`      | `import.meta.env.VITE_*`  |
| `craco.config.js` or none | CRA        | `REACT_APP_` | `process.env.REACT_APP_*` |

**Wrong prefix = undefined values at runtime.** This is the #1 integration failure.

## Key Clarification: No Callback Route

The React SDK handles OAuth callbacks **internally** via AuthKitProvider.

- No server-side callback route needed
- SDK intercepts redirect URI client-side
- Token exchange happens automatically

Just ensure redirect URI env var matches WorkOS Dashboard exactly.

## Required Environment Variables

```
{PREFIX}WORKOS_CLIENT_ID=client_...
{PREFIX}WORKOS_REDIRECT_URI=http://localhost:5173/callback
```

No `WORKOS_API_KEY` needed. Client-side only SDK.

## Verification Checklist

- [ ] README fetched and read
- [ ] Build tool detected correctly
- [ ] Env var prefix matches build tool
- [ ] `.env` or `.env.local` has required vars
- [ ] No `next` dependency (wrong skill)
- [ ] No `react-router` dependency (wrong skill)
- [ ] AuthKitProvider wraps app root
- [ ] `pnpm build` exits 0

## Error Recovery

### "clientId is required"

**Cause:** Env var inaccessible (wrong prefix)

Check: Does prefix match build tool? Vite needs `VITE_`, CRA needs `REACT_APP_`.

### Auth state lost on refresh

**Cause:** Token persistence issue

Check: Browser dev tools → Application → Local Storage. SDK stores tokens here automatically.

### useAuth returns undefined

**Cause:** Component outside provider tree

Check: Entry file (`main.tsx` or `index.tsx`) wraps `<App />` in `<AuthKitProvider>`.

### Callback redirect fails

**Cause:** URI mismatch

Check: Env var redirect URI exactly matches WorkOS Dashboard → Redirects configuration.
