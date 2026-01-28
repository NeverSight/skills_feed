---
name: e2e-test-runner
description: |
  Run and debug end-to-end tests for web, iOS, and Android platforms.
  Use when running e2e tests, demonstrating features to leadership,
  debugging test failures, checking test status, or when user mentions
  testing, e2e, Playwright, Maestro, demo, demonstration, or test automation.
---

# E2E Test Runner Skill

This skill helps you run and debug end-to-end tests for the Happy/VibeBox project.

> **Note:** All commands in this document assume you are running from the project root directory.

## Platforms Supported

- **Web**: Playwright-based OAuth authentication tests
- **iOS**: Maestro tests (future)
- **Android**: Maestro tests (future)

## When to Use This Skill

Automatically activates when:
- User asks to run e2e tests
- User wants to demonstrate features (especially to leadership)
- User mentions test failures or debugging
- User talks about OAuth, authentication testing
- User mentions Playwright or Maestro
- User asks about test status or running tests

## Core Workflow

### Step 1: Check Prerequisites

Before running tests, ALWAYS verify:

1. **Docker services** (Postgres + Logto) are running
2. **Next.js server** is running on correct port with correct env
3. **Expo web client** is running with correct configuration
4. **Happy Server** configuration is correct

Use the `check-services.sh` script or manually verify:

```bash
# Check Docker
docker ps | grep -E "postgres|logto"

# Check Next.js server (should be on 3003)
lsof -ti:3003

# Check Expo web (should be on 8081)
lsof -ti:8081

# Verify server env
grep HAPPY_SERVER_URL server/.env.local
```

**Expected configuration:**
- Docker: localhost:3001 (Logto), localhost:3002 (Postgres)
- Next.js: localhost:3003 with `HAPPY_SERVER_URL=https://api.cluster-fluster.com`
- Expo web: localhost:8081 with `EXPO_PUBLIC_API_URL=http://localhost:3003`
- Happy Server: https://api.cluster-fluster.com (default, DON'T override)

### Step 2: Start Missing Services

If services are not running, start them in correct order:

```bash
# 1. Start Docker (if needed)
cd docker
docker compose up -d

# 2. Start Next.js server (if needed)
cd server
yarn dev

# 3. Start Expo web with correct env (if needed)
cd client
EXPO_PUBLIC_API_URL=http://localhost:3003 yarn web
```

**CRITICAL**:
- NEVER set `EXPO_PUBLIC_HAPPY_SERVER_URL` - let it use the default official URL
- ALWAYS set `EXPO_PUBLIC_API_URL=http://localhost:3003` for local testing

### Step 3: Run the Test

For web OAuth tests:

```bash
cd client/tests/e2e/web
EXPO_PUBLIC_API_URL=http://localhost:3003 node oauth-authentication.test.js
```

The test will:
- Open a browser window
- Navigate to VibeBox at http://localhost:8081
- Click "Sign In with Logto"
- Create a new user account automatically
- Complete the full OAuth flow
- Verify authentication state
- Take screenshots at each step
- Display success/failure clearly

### Step 4: Interpret Results

**Success indicators:**
- ✅ All steps show green checkmarks
- ✅ Final URL is `http://localhost:8081/` (NOT `/callback`)
- ✅ localStorage contains ID token
- ✅ Authentication state shows `isAuthenticated=true`
- ✅ No 404 or 500 errors in the logs

**Common issues:**
- If final URL is `/callback` → Check env configuration
- If 404 errors on `/api/*` → Check `EXPO_PUBLIC_API_URL`
- If CORS errors on `/v1/*` → Check Happy Server URL (should NOT be localhost)
- If test hangs → Check all services are running

See `TROUBLESHOOTING.md` for detailed error resolution.

## Key Files and Locations

- Test file: `client/tests/e2e/web/oauth-authentication.test.js`
- Test docs: `client/tests/e2e/web/README.md`
- Screenshots: `client/tests/e2e/web/tmp/oauth-redirect/`
- Server config: `server/.env.local`
- API client: `client/sources/services/api.ts`
- Happy Server config: `client/sources/sync/serverConfig.ts`

## Environment Variables Reference

### Client (Expo)
- `EXPO_PUBLIC_API_URL` - VibeBox Platform API (set to `http://localhost:3003` for local dev)
- `EXPO_PUBLIC_HAPPY_SERVER_URL` - Happy Server API (DON'T set, use default `https://api.cluster-fluster.com`)

### Server (Next.js)
- `HAPPY_SERVER_URL` - Happy Server API (set to `https://api.cluster-fluster.com` in `.env.local`)

## Best Practices

1. **Always check prerequisites first** - Don't assume services are running
2. **Use correct environment variables** - Wrong config causes 90% of issues
3. **Read the full test output** - Don't just look at the final status
4. **Check for 404/500 errors** - Success status doesn't mean no errors
5. **Verify final URL** - Should be `/` not `/callback`
6. **Take screenshots** - Tests save screenshots automatically for debugging

## Demonstration Mode

When user asks to "demonstrate to leadership" or similar:
1. Ensure all services are running perfectly
2. Run the test with full output visible
3. Highlight key success indicators
4. Show screenshots if needed
5. Emphasize the complete OAuth flow (no popups, full redirect)

## Related Documentation

- Prerequisites: See `PREREQUISITES.md`
- Troubleshooting: See `TROUBLESHOOTING.md`
- Service check script: `scripts/check-services.sh`
