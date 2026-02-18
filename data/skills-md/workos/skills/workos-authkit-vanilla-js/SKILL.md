---
name: workos-authkit-vanilla-js
description: Integrate WorkOS AuthKit with vanilla JavaScript applications. No framework required, browser-only. Use when project is plain HTML/JS, doesn't use React/Vue/etc, or mentions vanilla JavaScript authentication.
---

# WorkOS AuthKit for Vanilla JavaScript

## Decision Tree

### Step 1: Fetch README (BLOCKING)

WebFetch: `https://github.com/workos/authkit-js/blob/main/README.md`

**README is source of truth.** If this skill conflicts, follow README.

### Step 2: Detect Project Type

```
Has package.json with build tool (Vite, webpack, Parcel)?
  YES -> Bundled project (npm install)
  NO  -> CDN/Static project (script tag)
```

### Step 3: Follow README Installation

- **Bundled**: Use package manager install from README
- **CDN**: Use unpkg script tag from README

### Step 4: Implement Per README

Follow README examples for:

- Client initialization
- Sign in/out handlers
- User state management

## Critical API Quirk

`createClient()` is **async** - returns a Promise, not a client directly.

```javascript
// CORRECT
const authkit = await createClient(clientId);
```

## Verification Checklist

- [ ] README fetched and read before writing code
- [ ] Project type detected (bundled vs CDN)
- [ ] SDK installed/script added
- [ ] `createClient()` called with `await`
- [ ] Client ID provided (env var or hardcoded)
- [ ] Sign in called from user gesture (click handler)
- [ ] No console errors on page load
- [ ] Auth UI updates on sign in/out

## Environment Variables

**Bundled projects only:**

- Vite: `VITE_WORKOS_CLIENT_ID`
- Webpack: `REACT_APP_WORKOS_CLIENT_ID` or custom
- No `WORKOS_API_KEY` needed (client-side SDK)

## Error Recovery

| Error                            | Cause               | Fix                                                    |
| -------------------------------- | ------------------- | ------------------------------------------------------ |
| `WorkOS is not defined`          | CDN not loaded      | Add script to `<head>` before your code                |
| `createClient is not a function` | Wrong import        | npm: check import path; CDN: use `WorkOS.createClient` |
| `clientId is required`           | Undefined env var   | Check env prefix matches build tool                    |
| CORS errors                      | `file://` protocol  | Use local dev server (`npx serve`)                     |
| Popup blocked                    | Not user gesture    | Call `signIn()` only from click handler                |
| Auth state lost                  | Token not persisted | Check localStorage in dev tools                        |

## Task Flow

1. **preflight**: Fetch README, detect project type, verify env vars
2. **install**: Add SDK per project type
3. **callback**: SDK handles internally (no server route needed)
4. **provider**: Initialize client with `await createClient()`
5. **ui**: Add auth buttons and state display
6. **verify**: Build (if bundled), check console
