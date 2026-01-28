---
name: bullet-tracer
description: Implement features using tracer bullet approach - build minimal end-to-end vertical slice first, then expand.
triggers:
  - bullet tracer
  - tracer bullet
---

# Bullet Tracer Skill

From The Pragmatic Programmer: "Use Tracer Bullets to Find the Target" — build a minimal end-to-end vertical slice that touches all layers first, then expand.

## Compatibility Note

Not all tickets/features are fully compatible with the tracer bullet approach (e.g., pure refactors, config changes, single-layer fixes). Be smart: apply tracer bullet concepts to compatible parts, use general best practices for the rest.

## Philosophy

- **Tracer bullet != prototype**: You keep the code, it becomes the foundation
- **Vertical slice**: Touch ALL layers (UI → API → logic → DB → tests) in one thin path
- **Fast feedback**: Validate architecture and integration points early
- **Hardcoded is OK**: Initial tracer can use minimal/fake data

## Workflow

### Phase 1: Tracer Bullet (MUST DO FIRST)

1. **Identify all layers** the feature touches (e.g., frontend, API, service, DB, config)
2. **Implement the thinnest possible path** through ALL layers:
   - One happy path only
   - Hardcoded values acceptable
   - Skip edge cases, validation, error handling
   - Must be runnable/testable end-to-end
3. **Write one integration test** that exercises the full path
4. **Verify it works** — run the test, manually test if needed

### Phase 2: Expand

Only after tracer works, expand systematically:

1. **Replace hardcoded values** with real implementations
2. **Add validation** and error handling
3. **Add edge cases** and additional paths
4. **Add unit tests** for individual components
5. **Refactor** for production quality

## Example

Feature: "User can save favorite items"

### Tracer (Phase 1):
```
- Frontend: Add button that calls POST /api/favorites with hardcoded itemId
- API: Endpoint that inserts into favorites table
- DB: Create favorites table with user_id, item_id
- Test: Integration test that clicks button, verifies DB row exists
```

### Expand (Phase 2):
- Real item selection UI
- Validation (item exists, not already favorited)
- Error handling and user feedback
- Unfavorite functionality
- List favorites page
- Unit tests for each layer

## Rules

1. **NEVER skip the tracer phase** — always build e2e first
2. **NEVER expand before tracer works** — resist the urge to "do it properly"
3. **Keep tracer minimal** — if you're adding "nice to haves", stop
4. **Tracer must touch ALL layers** — if it doesn't, it's not a tracer
5. **Tracer must be testable** — if you can't verify it works, add a test

## Anti-patterns

❌ Building the perfect DB schema before any code  
❌ Implementing full validation before happy path works  
❌ Writing all unit tests before integration test  
❌ Building frontend in isolation from backend  
❌ "I'll connect it later"  

## Checklist

Before moving to Phase 2, verify:

- [ ] Code touches every layer the feature needs
- [ ] Can run/test the feature end-to-end
- [ ] At least one integration test passes
