---
name: separation-of-concerns
description: Use when component does too many things. Use when mixing data fetching, logic, and presentation. Use when code is hard to test.
---

# Separation of Concerns

## Overview

**Each piece of code should do one thing. Data, logic, and presentation should be separate.**

Mixed concerns create untestable, unreusable, unmaintainable code. Separation enables testing, reuse, and clarity.

## When to Use

- Component fetches, transforms, and displays data
- Business logic mixed with UI code
- Database queries in controllers
- Hard to test a piece of code in isolation

## The Iron Rule

```
NEVER mix data fetching, business logic, and presentation in one place.
```

**No exceptions:**
- Not for "it's a small component"
- Not for "it's simpler this way"
- Not for "only used once"
- Not for "it works"

## Detection: Mixed Concerns Smell

If one file does fetch + transform + display, STOP:

```typescript
// ❌ VIOLATION: Component does everything
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    // Data fetching
    fetch(`/api/users/${userId}`)
      .then(res => res.json())
      .then(data => {
        // Business logic / transformation
        const fullName = `${data.firstName} ${data.lastName}`;
        const memberSince = new Date(data.createdAt).toLocaleDateString();
        const isVIP = data.orderCount > 100;
        
        setUser({ ...data, fullName, memberSince, isVIP });
        setLoading(false);
      });
  }, [userId]);
  
  // Presentation
  if (loading) return <div>Loading...</div>;
  
  return (
    <div className="user-profile">
      <h1>{user.fullName}</h1>
      {user.isVIP && <span className="vip-badge">VIP</span>}
      <p>Member since: {user.memberSince}</p>
    </div>
  );
}
```

Problems:
- Can't test formatting without fetching
- Can't reuse fetch logic
- Can't reuse presentation
- Component does 3 jobs

## The Correct Pattern: Separated Layers

```typescript
// ✅ CORRECT: Separated concerns

// 1. Data fetching (hook)
// hooks/useUser.ts
function useUser(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  
  useEffect(() => {
    setLoading(true);
    fetch(`/api/users/${userId}`)
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch');
        return res.json();
      })
      .then(setUser)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [userId]);
  
  return { user, loading, error };
}

// 2. Business logic (pure functions)
// utils/userFormatters.ts
interface FormattedUser {
  fullName: string;
  memberSince: string;
  isVIP: boolean;
}

function formatUser(user: User): FormattedUser {
  return {
    fullName: `${user.firstName} ${user.lastName}`,
    memberSince: new Date(user.createdAt).toLocaleDateString(),
    isVIP: user.orderCount > 100,
  };
}

// 3. Presentation (dumb component)
// components/UserCard.tsx
interface UserCardProps {
  fullName: string;
  memberSince: string;
  isVIP: boolean;
}

function UserCard({ fullName, memberSince, isVIP }: UserCardProps) {
  return (
    <div className="user-profile">
      <h1>{fullName}</h1>
      {isVIP && <span className="vip-badge">VIP</span>}
      <p>Member since: {memberSince}</p>
    </div>
  );
}

// 4. Composition (container component)
// pages/UserProfile.tsx
function UserProfile({ userId }) {
  const { user, loading, error } = useUser(userId);
  
  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;
  if (!user) return <NotFound />;
  
  const formatted = formatUser(user);
  
  return <UserCard {...formatted} />;
}
```

## Benefits of Separation

| Mixed | Separated |
|-------|-----------|
| Can't test formatting | `formatUser()` tested in isolation |
| Can't reuse fetch | `useUser()` reusable anywhere |
| Can't reuse UI | `UserCard` reusable with any data |
| 1 complex component | 4 simple pieces |

## The Layers

### 1. Data Layer (Hooks, Services)
- Fetching data
- API calls
- State management
- No business logic

### 2. Logic Layer (Pure Functions)
- Transformations
- Calculations
- Validations
- Business rules

### 3. Presentation Layer (Components)
- Rendering UI
- Styling
- User interactions
- No data fetching

### 4. Composition Layer (Containers)
- Connects layers
- Handles loading/error states
- Passes data down

## Pressure Resistance Protocol

### 1. "It's a Small Component"
**Pressure:** "For simple cases, separation is overkill"

**Response:** Small becomes large. Start clean, stay clean.

**Action:** Separate even for small components. It costs little.

### 2. "It's Simpler This Way"
**Pressure:** "Everything in one place is easier to understand"

**Response:** Mixed concerns seem simple but are hard to test, debug, and modify.

**Action:** Separation is simpler in the long run.

### 3. "Only Used Once"
**Pressure:** "This component is unique, won't be reused"

**Response:** Testability matters even for unique components.

**Action:** Separate for testability, not just reuse.

## Red Flags - STOP and Reconsider

- `useEffect` with fetch + transform + setState
- Business logic in render functions
- Database queries in route handlers
- API calls in utility functions
- Components with 100+ lines

**All of these mean: Separate the concerns.**

## Quick Reference

| Concern | Where It Belongs |
|---------|------------------|
| API calls | Hooks / Services |
| Data transformation | Pure functions |
| Business rules | Pure functions |
| UI rendering | Presentation components |
| Connecting pieces | Container components |

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "Small component" | Small grows. Separate now. |
| "Simpler together" | Separated is simpler to test/modify. |
| "Only used once" | Testability matters. |
| "It works" | Working ≠ maintainable. |
| "Over-engineering" | This is just engineering. |

## The Bottom Line

**Data fetching in hooks. Logic in pure functions. UI in components.**

Separation enables testing, reuse, and maintainability. A component should either fetch data, transform it, or display it - never all three.
