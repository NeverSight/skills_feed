---
name: dotnet-best-practices
description: Comprehensive .NET development guidelines covering error handling, async patterns, type design, database performance, API design, DI, architecture, serialization, performance optimization, logging, and testing. Contains 100+ rules prioritized by impact to guide code reviews and automated refactoring.
license: MIT
metadata:
  author: akires47
  version: "1.0.0"
---

# .NET Best Practices

Comprehensive development guide for modern .NET applications with C# 12+. Contains 100+ rules across 11 categories, prioritized by impact to guide code generation, refactoring, and reviews.

## When to Apply

Reference these guidelines when:
- Writing new C# code or refactoring existing code
- Designing APIs, services, or domain models
- Implementing data access layers or async operations
- Reviewing code for performance, correctness, or maintainability
- Setting up dependency injection, configuration, or logging
- Writing tests (unit, integration, snapshot)
- Building distributed systems or microservices

## Rule Categories by Priority

| Priority | Category | Impact | Prefix | Rules |
|----------|----------|--------|--------|-------|
| 1 | Error Handling | CRITICAL | `error-` | 8 |
| 2 | Async Patterns | CRITICAL | `async-` | 9 |
| 3 | Type Design | HIGH | `type-` | 10 |
| 4 | Database Performance | HIGH | `db-` | 12 |
| 5 | API Design | MEDIUM-HIGH | `api-` | 8 |
| 6 | Dependency Injection | MEDIUM | `di-` | 7 |
| 7 | Architecture | MEDIUM | `arch-` | 8 |
| 8 | Serialization | MEDIUM | `serial-` | 6 |
| 9 | Performance | LOW-MEDIUM | `perf-` | 12 |
| 10 | Logging | LOW-MEDIUM | `log-` | 6 |
| 11 | Testing | LOW | `test-` | 8 |

**Total: 94 Rules**

## Quick Reference

### 1. Error Handling (CRITICAL)

- `error-result-pattern` - Return Result<T> for expected errors, not exceptions
- `error-validation-boundaries` - Validate at handler entry points, fail fast
- `error-guard-clauses` - Use guard clauses for null/range checks
- `error-exception-filters` - Use `catch when` for selective exception handling
- `error-global-handlers` - Implement middleware for unhandled exceptions
- `error-never-catch-all` - Avoid catching all exceptions without rethrowing
- `error-custom-exceptions` - Use built-in exceptions, avoid custom ones
- `error-exception-properties` - Add context to exceptions via Data property

### 2. Async Patterns (CRITICAL)

- `async-cancellation-token` - Always accept CancellationToken in async methods
- `async-all-the-way` - Never block on async code with .Result or .Wait()
- `async-valuetask` - Use ValueTask for hot paths with synchronous completions
- `async-iasyncenumerable` - Use IAsyncEnumerable for streaming data
- `async-parallel-foreach` - Use Parallel.ForEachAsync for bounded concurrency
- `async-channel` - Use System.Threading.Channels for producer-consumer
- `async-semaphore` - Use SemaphoreSlim for rate limiting
- `async-configureawait` - Use ConfigureAwait(false) in library code
- `async-avoid-async-void` - Never use async void except for event handlers

### 3. Type Design (HIGH)

- `type-records-for-dtos` - Use records for immutable DTOs
- `type-readonly-record-struct` - Use readonly record struct for value objects
- `type-seal-classes` - Seal classes by default unless designed for inheritance
- `type-composition-over-inheritance` - Prefer composition over inheritance
- `type-nullable-reference-types` - Enable nullable reference types, handle nulls explicitly
- `type-pattern-matching` - Use switch expressions and pattern matching
- `type-primary-constructors` - Use primary constructors for simple classes
- `type-immutability-default` - Design types to be immutable by default
- `type-explicit-conversions` - Avoid implicit conversions for value objects
- `type-no-public-setters` - Use init or constructor, not public setters

### 4. Database Performance (HIGH)

- `db-read-write-separation` - Separate read models from write models
- `db-notracking-default` - Configure NoTracking by default in EF Core
- `db-row-limits` - Always apply row limits to queries
- `db-n-plus-one` - Avoid N+1 queries with Include or batch fetching
- `db-cartesian-explosion` - Use AsSplitQuery to prevent Cartesian products
- `db-compiled-queries` - Use EF.CompileAsyncQuery for hot paths
- `db-connection-pooling` - Use NpgsqlDataSource for connection pooling
- `db-optimistic-concurrency` - Use RowVersion for concurrent updates
- `db-projections-over-entities` - Use Select projections, not full entities
- `db-no-application-joins` - Do joins in SQL, never in application code
- `db-bulk-operations` - Use ExecuteUpdate/Delete for bulk modifications
- `db-no-generic-repositories` - Use purpose-built stores, not generic repositories

### 5. API Design (MEDIUM-HIGH)

- `api-accept-abstractions` - Accept IEnumerable/IReadOnlyCollection in parameters
- `api-return-specific-types` - Return IReadOnlyList/IReadOnlyCollection from methods
- `api-readonly-collections` - Return immutable collections from public APIs
- `api-method-overloads` - Use overloads for common scenarios, not optionals
- `api-extension-methods` - Use extension methods for fluent APIs
- `api-fluent-builders` - Use builder pattern for complex object construction
- `api-async-suffix` - Suffix async methods with Async
- `api-avoid-out-params` - Return tuples or records instead of out parameters

### 6. Dependency Injection (MEDIUM)

- `di-extension-methods` - Group service registrations in extension methods
- `di-lifetime-management` - Understand Singleton, Scoped, Transient lifetimes
- `di-options-pattern` - Use IOptions<T> for configuration
- `di-validate-on-start` - Call ValidateOnStart() for configuration validation
- `di-keyed-services` - Use keyed services for multiple implementations
- `di-avoid-service-locator` - Never inject IServiceProvider as service locator
- `di-no-scoped-in-singleton` - Never inject Scoped services into Singleton

### 7. Architecture (MEDIUM)

- `arch-vertical-slice` - Organize by feature (vertical slices), not layers
- `arch-feature-organization` - One feature per file with all related code
- `arch-static-handlers` - Use static handler methods in features
- `arch-module-boundaries` - Use InternalsVisibleTo for module boundaries
- `arch-feature-flags` - Implement runtime feature toggling
- `arch-background-services` - Use IHostedService for background work
- `arch-minimal-apis` - Prefer minimal APIs over controller-based APIs
- `arch-map-endpoints-per-feature` - Each feature maps its own endpoints

### 8. Serialization (MEDIUM)

- `serial-system-text-json` - Use System.Text.Json, not Newtonsoft.Json
- `serial-source-generators` - Use JsonSerializerContext source generators
- `serial-protobuf` - Use Protobuf for actor systems and event sourcing
- `serial-messagepack` - Use MessagePack for high-performance scenarios
- `serial-wire-compatibility` - Design for forward/backward compatibility
- `serial-no-type-names` - Never embed type names in wire format

### 9. Performance (LOW-MEDIUM)

- `perf-span-and-memory` - Use Span<T>/Memory<T> for buffer operations
- `perf-defer-enumeration` - Don't materialize IEnumerable until necessary
- `perf-frozen-collections` - Use FrozenDictionary/FrozenSet for static data
- `perf-string-interpolation` - Use string interpolation, not concatenation
- `perf-list-capacity` - Initialize List with capacity when size is known
- `perf-dictionary-trygetvalue` - Use TryGetValue instead of ContainsKey + indexer
- `perf-array-pool` - Use ArrayPool for temporary large buffers
- `perf-object-pool` - Use ObjectPool for expensive-to-create objects
- `perf-compiled-regex` - Use GeneratedRegex source generator
- `perf-static-pure-functions` - Prefer static methods for pure functions
- `perf-stackalloc` - Use stackalloc for small temporary buffers
- `perf-avoid-closure-allocations` - Cache delegates to avoid closure allocations

### 10. Logging (LOW-MEDIUM)

- `log-structured-logging` - Use structured logging with named parameters
- `log-logger-message-define` - Use LoggerMessage.Define for high-performance logging
- `log-correlation-ids` - Implement request correlation via Activity.Current
- `log-activity-tracing` - Use System.Diagnostics.Activity for distributed tracing
- `log-log-levels` - Use appropriate log levels (Trace/Debug/Info/Warning/Error/Critical)
- `log-avoid-string-interpolation` - Pass message template, not interpolated strings

### 11. Testing (LOW)

- `test-testcontainers` - Use TestContainers for integration tests, not mocks
- `test-snapshot-testing` - Use Verify for snapshot testing APIs and outputs
- `test-arrange-act-assert` - Follow AAA pattern for test structure
- `test-fakes-vs-mocks` - Prefer hand-written fakes over mocking libraries
- `test-data-builders` - Use builder pattern for complex test data
- `test-integration-webappfactory` - Use WebApplicationFactory for API integration tests
- `test-one-assertion-per-test` - Focus each test on a single assertion
- `test-descriptive-names` - Use descriptive test names that explain the scenario

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/error-result-pattern.md
rules/async-cancellation-token.md
rules/db-notracking-default.md
```

Each rule file contains:
- Brief explanation of why it matters
- ❌ Incorrect code example with explanation
- ✅ Correct code example with explanation
- Additional context and references

## Full Compiled Document

For the complete guide with all rules expanded inline: `AGENTS.md`

This document is optimized for LLM context loading and contains all rules with full code examples.

## Anti-Patterns Summary

Common mistakes to avoid:

| Anti-Pattern | Rule |
|--------------|------|
| Throwing exceptions for business logic | `error-result-pattern` |
| Blocking on async code with .Result | `async-all-the-way` |
| Mutable DTOs with public setters | `type-records-for-dtos` |
| Queries without row limits | `db-row-limits` |
| N+1 query problems | `db-n-plus-one` |
| Returning List<T> from APIs | `api-readonly-collections` |
| Massive Program.cs with 200+ DI registrations | `di-extension-methods` |
| Organizing by technical layers | `arch-vertical-slice` |
| Using Newtonsoft.Json | `serial-system-text-json` |
| String concatenation in loops | `perf-string-interpolation` |
| Mocking databases in tests | `test-testcontainers` |

## Resources

- **.NET Documentation**: https://learn.microsoft.com/en-us/dotnet/
- **C# Language Reference**: https://learn.microsoft.com/en-us/dotnet/csharp/
- **EF Core Performance**: https://learn.microsoft.com/en-us/ef/core/performance/
- **ASP.NET Core**: https://learn.microsoft.com/en-us/aspnet/core/
- **Performance Best Practices**: https://learn.microsoft.com/en-us/dotnet/standard/performance/
