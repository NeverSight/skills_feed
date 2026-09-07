---
name: implement-graphql
type: atomic
license: MIT
description: >
  Use when building or reviewing a graphql-ruby schema, resolver, or mutation.
  Trigger words: GraphQL, graphql-ruby, resolver, mutation, dataloader, schema.
metadata:
  version: 1.0.0
  user-invocable: "true"
---

# Implement GraphQL

Use this skill when **designing, implementing, or reviewing GraphQL APIs** in a Rails application with the `graphql-ruby` gem.

## Core Process

**DO NOT proceed to step 3 before step 1 is written and failing.**

1. **SPEC:** Write failing spec (happy path + auth + validation error case) — see [TESTING.md](./TESTING.md). Use `AppSchema.execute` in `spec/graphql/`. Never use HTTP controller dispatch for GraphQL specs.

2. **TYPE:** Define arguments and return types. Use `connection_type` for pagination shapes. Do not leak internal model names.

3. **IMPLEMENT:** Create resolver/mutation class delegating to a service object. Use dedicated classes instead of inline field blocks.

4. **N+1 CHECK:** Use dataloader on every association load. For list resolvers, prime the dataloader with the records returned by the relation before fields resolve associated objects. Use `bullet` and `db-query-matchers` in specs.
   ```ruby
   # ✅ batches loads across all records
   def buyer
     dataloader.with(Sources::RecordById, Buyer).load(object.buyer_id)
   end
   ```

5. **AUTH CHECK:** Apply field-level guards where data is sensitive using Pundit or custom context guards.
   ```ruby
   field :internal_notes, String, null: true do
     guard -> (_obj, _args, ctx) { ctx[:current_user]&.admin? }
   end
   ```

6. **FINAL CHECK:** Verify every item in the HARD-GATE checklist below. Ensure mutations return `{ result, errors }` shapes on failure.
   ```ruby
   rescue ActiveRecord::RecordInvalid => e
     { order: nil, errors: e.record.errors.full_messages }
   ```

7. **RUN:** Ensure the full test suite is green before PR.

## HARD-GATE Checklist

Before shipping a resolver/mutation slice, ALL of the following must be confirmed:

- [ ] **Specs** — covers happy path, unauthenticated, unauthorized, validation errors, N+1 counts, and schema limits.
- [ ] **N+1 Prevention** — `dataloader.with(Source, Model).load(id)` on every association; never `object.association`.
- [ ] **Dataloader Priming** — collection resolvers prime records before association fields resolve.
- [ ] **Authorization** — sensitive fields have field-level guards (not type-level alone).
- [ ] **Type Conventions** — paginated collections use `Types::*Type.connection_type`, not plain arrays.
- [ ] **Schema Safeguards** — introspection disabled in production; `max_depth` and `max_complexity` set.
- [ ] **Error Handling** — mutations return `{ result, errors }` with rescue blocks; no unhandled exceptions.
- [ ] **Documentation** — `description:` on every field in every type.
- [ ] **Resolver Structure** — dedicated resolver classes, not inline field blocks.

## Extended Resources (Progressive Disclosure)

Load these files only when their specific content is needed:

- **[TESTING.md](./TESTING.md)** — For the spec template, paths, and checklist.
- **[EXAMPLES.md](EXAMPLES.md)** — For detailed code examples of dataloaders, mutations, and types.

## Integration

| Skill | When to chain |
|-------|---------------|
| **define-domain-language** | Type and field naming must match business language |
| **plan-tests** | Choose first failing spec (mutation vs query vs resolver unit) |
| **write-tests** | Full TDD cycle for resolvers and mutations |
| **security-check** | Auth, introspection disable, query depth/complexity limits |
