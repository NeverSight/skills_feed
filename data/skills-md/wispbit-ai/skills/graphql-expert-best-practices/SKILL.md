---
name: graphql-expert-best-practices
description: GraphQL performance optimization and best practices for building scalable APIs. This skill should be used when writing, reviewing, or refactoring GraphQL schemas, resolvers, or query execution code. Triggers on tasks involving GraphQL APIs, resolver optimization, query performance, or data fetching patterns.
license: MIT
metadata:
  author: wispbit
  version: "1.0.0"
---

# GraphQL Expert Best Practices

Comprehensive performance optimization and best practices guide for GraphQL APIs. Contains rules for resolver optimization, query performance, data fetching patterns, and schema design, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Writing GraphQL schemas, resolvers, or type definitions
- Implementing data fetching and resolver logic
- Reviewing GraphQL code for performance issues
- Refactoring existing GraphQL APIs
- Optimizing query execution or resolver performance
- Designing GraphQL server architecture

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Query Optimization | CRITICAL | `dataloader-` |
| 2 | Schema Design | CRITICAL-HIGH | `schema-` |
| 3 | Mutation Design | CRITICAL-HIGH | `mutation-` |
| 4 | Pagination | HIGH | `pagination-` |
| 5 | Security | CRITICAL-MEDIUM | `security-` |
| 6 | Operations | MEDIUM | `operations-` |

## Quick Reference

- `dataloader-n-plus-one` - Use DataLoader to batch queries and prevent N+1 performance issues
- `query-unique-identifiers` - Use unique identifiers over composite parameters to simplify API surface
- `schema-no-json-filters` - Ban arbitrary JSON filter scalars to prevent NoSQL injection vulnerabilities
- `schema-no-binary-data` - Avoid large binary data in schema to prevent payload bloat and memory issues
- `schema-stable-identifiers` - Use globally stable opaque identifiers to prevent information leakage and enumeration attacks
- `schema-structured-types` - Use structured types over unstructured String/JSON fields to improve type safety
- `schema-split-types-by-role` - Split types by role to prevent privacy field leakage and eliminate runtime authorization
- `schema-prefer-deprecation` - Prefer deprecation over versioning to enable continuous API evolution
- `schema-field-overload` - Avoid field overloads for viewer vs user to prevent security issues and improve API clarity
- `schema-minimize-nullable-args` - Minimize nullable arguments to improve API clarity and type safety
- `schema-no-duplicate-fields` - Prevent duplicate fields accessible through nested objects to maintain single source of truth
- `mutation-no-file-uploads` - Avoid file uploads through GraphQL to prevent memory exhaustion and security vulnerabilities
- `mutation-single-input-object` - Use single input object argument instead of multiple scalars to improve API evolvability
- `mutation-union-result-types` - Return union types with dedicated success and specific error types for type-safe error handling
- `mutation-explicit-actions` - Design mutations around explicit actions rather than generic update patterns
- `mutation-separate-input-types` - Separate input types for create and update to improve type safety
- `mutation-avoid-validation-scalars` - Avoid custom validation scalars to prevent multi-request error loops
- `pagination-no-default-totalcount` - Avoid default totalCount in connections to prevent performance degradation
- `security-complexity-limits` - Require complexity and query node limits to prevent resource exhaustion attacks
- `security-disable-introspection` - Disable introspection in production to prevent schema disclosure
- `operations-require-client-headers` - Require client identification headers for debugging and monitoring

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/dataloader-n-plus-one.md
rules/query-unique-identifiers.md
rules/schema-no-json-filters.md
rules/schema-no-binary-data.md
rules/schema-stable-identifiers.md
rules/schema-structured-types.md
rules/schema-split-types-by-role.md
rules/schema-prefer-deprecation.md
rules/schema-field-overload.md
rules/schema-minimize-nullable-args.md
rules/schema-no-duplicate-fields.md
rules/mutation-no-file-uploads.md
rules/mutation-single-input-object.md
rules/mutation-union-result-types.md
rules/mutation-explicit-actions.md
rules/mutation-separate-input-types.md
rules/mutation-avoid-validation-scalars.md
rules/pagination-no-default-totalcount.md
rules/security-complexity-limits.md
rules/security-disable-introspection.md
rules/operations-require-client-headers.md
```

Each rule file contains:
- Brief explanation of why it matters
- When to use and when not to use the pattern
- Implementation requirements
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references