---
name: api-versioning
description: Use when designing or modifying APIs. Use when adding breaking changes. Use when clients depend on API stability.
---

# API Versioning

## Overview

**Version your APIs from day one. Never break existing clients.**

Breaking changes without versioning destroy client trust. Version APIs explicitly, support multiple versions gracefully, and deprecate with ample warning.

## When to Use

- Designing new API endpoints
- Adding or modifying existing endpoints
- Making changes that could break clients
- Planning API evolution strategy
- Reviewing API design decisions

## The Iron Rule

```
NEVER make breaking changes to a released API version.
```

**No exceptions:**
- Not for "it's a bug fix"
- Not for "nobody uses that field"
- Not for "we'll notify clients"
- Not for "it's just internal"
- Not for "the old way was wrong"

**Breaking changes require a new version. Always.**

## Detection: What's a Breaking Change?

| Change | Breaking? | Safe Alternative |
|--------|-----------|------------------|
| Removing a field | YES | Deprecate, keep returning |
| Renaming a field | YES | Add new, keep old |
| Changing field type | YES | Add new field |
| Changing response structure | YES | New version |
| Adding required parameter | YES | Make optional with default |
| Removing endpoint | YES | Deprecate, maintain |
| Changing error codes | YES | Add new codes, keep old |
| Adding optional field | NO | Safe to add |
| Adding new endpoint | NO | Safe to add |
| Adding optional parameter | NO | Safe to add |

## Versioning Strategies

### 1. URL Path Versioning (Recommended)

```typescript
// ✅ CORRECT: Version in URL path
// /api/v1/users
// /api/v2/users

app.get('/api/v1/users', handleUsersV1);
app.get('/api/v2/users', handleUsersV2);
```

**Pros:** Explicit, cacheable, easy to route
**Cons:** URL proliferation

### 2. Header Versioning

```typescript
// ✅ CORRECT: Version in Accept header
// Accept: application/vnd.api+json; version=1

app.get('/api/users', (req, res) => {
  const version = parseVersion(req.headers.accept);
  if (version === 1) return handleUsersV1(req, res);
  if (version === 2) return handleUsersV2(req, res);
  return res.status(406).json({ error: 'Unsupported version' });
});
```

**Pros:** Clean URLs
**Cons:** Hidden, harder to test, caching complexity

### 3. Query Parameter Versioning

```typescript
// ✅ ACCEPTABLE: Version as query param
// /api/users?version=1

app.get('/api/users', (req, res) => {
  const version = parseInt(req.query.version) || LATEST_VERSION;
  // ...
});
```

**Pros:** Simple
**Cons:** Optional parameter often forgotten

## Correct Version Evolution Pattern

```typescript
// Version 1: Original API
interface UserV1 {
  id: string;
  name: string;       // Full name
  email: string;
}

// Version 2: Split name into parts (BREAKING!)
interface UserV2 {
  id: string;
  firstName: string;  // New field
  lastName: string;   // New field
  email: string;
}

// ✅ CORRECT: Support both versions
class UserController {
  async getUserV1(id: string): Promise<UserV1> {
    const user = await this.userService.getUser(id);
    return {
      id: user.id,
      name: `${user.firstName} ${user.lastName}`,  // Compute for v1 clients
      email: user.email,
    };
  }

  async getUserV2(id: string): Promise<UserV2> {
    const user = await this.userService.getUser(id);
    return {
      id: user.id,
      firstName: user.firstName,
      lastName: user.lastName,
      email: user.email,
    };
  }
}

// ❌ WRONG: Silently change v1 response
// ❌ WRONG: Force all clients to update simultaneously
// ❌ WRONG: Remove v1 without deprecation period
```

## Deprecation Protocol

Never surprise clients. Follow this:

```typescript
// 1. Announce deprecation (headers + docs)
res.setHeader('Deprecation', 'true');
res.setHeader('Sunset', 'Sat, 01 Jan 2025 00:00:00 GMT');
res.setHeader('Link', '</api/v2/users>; rel="successor-version"');

// 2. Log usage to track migration
logger.info('Deprecated v1 endpoint called', { 
  endpoint: '/api/v1/users',
  clientId: req.clientId,
});

// 3. Maintain for deprecation period (minimum 6 months for external APIs)

// 4. Return 410 Gone after sunset date
if (isPastSunset('/api/v1/users')) {
  return res.status(410).json({
    error: 'This API version has been retired',
    migration: 'https://docs.api.com/migration-v1-to-v2',
    successor: '/api/v2/users',
  });
}
```

## Pressure Resistance Protocol

### 1. "Just Ship It, We'll Version Later"
**Pressure:** "We need to launch, versioning can wait"

**Response:** Adding versioning to an existing API is 10x harder than starting with it. Clients already depend on the unversioned endpoints.

**Action:** Add `/v1/` prefix now. Takes 5 minutes.

### 2. "It's Internal, We Control All Clients"
**Pressure:** "We can just update all our services"

**Response:** Internal APIs become external. Services can't update simultaneously. Deployments fail mid-rollout.

**Action:** Version internal APIs too. Your future self will thank you.

### 3. "It's a Bug Fix, Not a Breaking Change"
**Pressure:** "The old behavior was wrong"

**Response:** Clients may depend on the "wrong" behavior. A fix can break them.

**Action:** Fix in new version. Document the fix. Let clients opt-in.

### 4. "Nobody Uses That Field"
**Pressure:** "Analytics show it's unused"

**Response:** Analytics might be wrong. One client relying on it = breaking change.

**Action:** Deprecate with warning, keep returning the field, sunset after migration period.

### 5. "We'll Just Notify Clients"
**Pressure:** "We'll email everyone before the change"

**Response:** Emails get missed. Clients need deploy time. Surprise breaks cause outages.

**Action:** Deprecation headers + sunset period + new version.

## Red Flags - STOP and Reconsider

If you notice ANY of these, you're about to break clients:

- Removing or renaming fields without new version
- Changing response structure "to improve it"
- "Nobody will notice this change"
- No version in API path or headers
- Only one version supported
- Deprecating without sunset date
- Changing semantics (same field, different meaning)

**All of these mean: Create a new API version.**

## Version Lifecycle Management

```
┌─────────┐     ┌─────────────┐     ┌────────────┐     ┌───────┐
│  Alpha  │ ──► │  Released   │ ──► │ Deprecated │ ──► │ Sunset│
└─────────┘     └─────────────┘     └────────────┘     └───────┘
 Breaking OK     No breaking         Warn clients      410 Gone
                 Support 2-3 ver     6+ months         Remove code
```

| Phase | Breaking Changes | Client Action |
|-------|------------------|---------------|
| Alpha (v0.x) | Allowed with notice | Expect instability |
| Released (v1+) | Never | Rely on stability |
| Deprecated | None | Migrate to successor |
| Sunset | N/A | Endpoint returns 410 |

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "We'll add versioning later" | Later = breaking existing clients. |
| "It's internal only" | Internal becomes external. Version anyway. |
| "Small change, won't break anything" | Small changes break clients constantly. |
| "We'll coordinate the update" | Coordination fails. Services deploy independently. |
| "It's just a rename" | Renames break clients that parse responses. |
| "The docs explain the change" | Clients don't re-read docs. Code breaks. |
| "Analytics show no usage" | One client matters. Analytics miss things. |

## Quick Reference

| Scenario | Action |
|----------|--------|
| New API | Start with `/v1/` immediately |
| Adding field | Add to current version (non-breaking) |
| Removing field | New version + deprecate old |
| Renaming field | Add new name, keep old, deprecate old |
| Changing structure | New version |
| Bug that changes behavior | Fix in new version |
| Deprecating version | Announce + 6mo minimum + sunset date |

## The Bottom Line

**Version from day one. Never break released versions. Deprecate gracefully.**

When pressured to "just change it" or "version later": add versioning now, create new version for breaking changes, give clients time to migrate. API stability is a contract—don't break it.
