---
name: you-aint-gonna-need-it
description: Use when tempted to add features "for later". Use when building "production-ready" systems before needed. Use when adding flexibility that isn't required yet.
---

# YAGNI (You Ain't Gonna Need It)

## Overview

**Don't implement something until you actually need it.**

Every feature has a cost: code to write, tests to maintain, complexity to manage. Speculative features often go unused while creating real burden.

## When to Use

- Adding features "users might want later"
- Building "production-ready" infrastructure upfront
- Adding flexibility "in case requirements change"
- Implementing patterns "because best practices"
- Creating abstractions for hypothetical use cases

## The Iron Rule

```
NEVER build features until they're actually required.
```

**No exceptions:**
- Not for "users will probably want this"
- Not for "it's easy to add now"
- Not for "production systems need this"
- Not for "best practices say include this"

## Detection: The "Might Need" Smell

If your justification includes "might", "probably", "eventually", or "in case", STOP:

```typescript
// ❌ VIOLATION: Asked for 3 endpoints, built 15
// Request: GET/POST/DELETE todos
// Built: pagination, filtering, sorting, soft delete, restore,
//        rate limiting, health checks, metrics, audit logs,
//        batch operations, search, tags, priorities, due dates...

// ✅ CORRECT: Build exactly what was asked
app.get('/todos', (req, res) => { /* list todos */ });
app.post('/todos', (req, res) => { /* create todo */ });
app.delete('/todos/:id', (req, res) => { /* delete todo */ });
```

## The Cost of Speculative Features

Every unneeded feature costs:

| Cost Type | Impact |
|-----------|--------|
| **Development time** | Hours building unused code |
| **Testing burden** | Tests for features nobody uses |
| **Maintenance** | Updates, security patches, dependency management |
| **Complexity** | More code = more bugs, harder onboarding |
| **Cognitive load** | Developers must understand unused systems |
| **Technical debt** | Speculative abstractions often wrong |

## Correct Pattern: Minimal First

Build the minimum that solves the actual problem:

```typescript
// ❌ YAGNI VIOLATION: "Production-ready" todo API
// - Zod validation with inference
// - Pagination with cursors
// - Full-text search
// - Soft delete + restore
// - Rate limiting
// - Request tracing
// - Health endpoints
// - Graceful shutdown
// - Structured logging
// ... for a simple todo list

// ✅ CORRECT: What was actually requested
interface Todo {
  id: string;
  title: string;
  completed: boolean;
}

const todos: Todo[] = [];

app.get('/todos', (req, res) => res.json(todos));

app.post('/todos', (req, res) => {
  const todo = { id: crypto.randomUUID(), title: req.body.title, completed: false };
  todos.push(todo);
  res.status(201).json(todo);
});

app.delete('/todos/:id', (req, res) => {
  const index = todos.findIndex(t => t.id === req.params.id);
  if (index === -1) return res.status(404).json({ error: 'Not found' });
  todos.splice(index, 1);
  res.status(204).send();
});

// Add pagination WHEN users have enough todos to need it
// Add search WHEN users ask for search
// Add rate limiting WHEN there's abuse
```

## Pressure Resistance Protocol

### 1. "Production Systems Need This"
**Pressure:** "Real production apps have logging, monitoring, health checks..."

**Response:** Add production features when going to production. Not during prototyping.

**Action:** Build MVP first. Add infrastructure when deploying for real.

### 2. "It's Easy to Add Now"
**Pressure:** "While I'm here, might as well add sorting and filtering"

**Response:** Easy to add now = easy to add later. Don't pay the maintenance cost until needed.

**Action:** Add it when someone actually needs it.

### 3. "Best Practices Say..."
**Pressure:** "Best practices recommend pagination, rate limiting, etc."

**Response:** Best practices are for problems you have. Don't solve problems you don't have.

**Action:** Follow best practices for your actual requirements.

### 4. "Users Will Want This"
**Pressure:** "Users will probably want to filter by date"

**Response:** "Probably" is not a requirement. Wait for actual user requests.

**Action:** Ship without it. Add when users actually ask.

## Red Flags - STOP and Reconsider

If you notice ANY of these, you're violating YAGNI:

- "While I'm at it, I'll also add..."
- "Users might want to..."
- "In case we need to..."
- "Let's make it production-ready"
- "Best practices recommend..."
- Building abstractions for single use cases
- Adding configuration for things that won't change

**All of these mean: Stop. Build only what's required.**

## What YAGNI Is NOT

YAGNI doesn't mean:
- Write bad code (quality is always needed)
- Skip error handling (that's required)
- Ignore security (that's required from day 1)
- Avoid good structure (clean code is required)

YAGNI means: Don't add **features** and **capabilities** until they're needed.

## Quick Reference

| Speculative | Wait Until |
|-------------|------------|
| Pagination | List exceeds reasonable size |
| Rate limiting | Actual abuse occurs |
| Soft delete | Users request undo capability |
| Full-text search | Users request search |
| Audit logging | Compliance requires it |
| Multi-tenancy | Second tenant exists |
| Caching | Performance problems measured |

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "Production systems need this" | Add when going to production. |
| "It's easy to add now" | Then it's easy to add later too. |
| "Users will probably want it" | Wait until they actually do. |
| "Best practices say..." | For problems you have, not might have. |
| "It'll be harder later" | Usually false. Context will be clearer later. |
| "We'll need it eventually" | Eventually isn't now. |

## The Bottom Line

**Build what's needed. Nothing more.**

When tempted to add "just one more feature": stop, check if it's required NOW, ship without it. The best code is code you didn't have to write.
