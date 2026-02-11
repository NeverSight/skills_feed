---
name: nodejs-best-practices
description: Node.js and Fastify performance, security, and best practices from Nearform. This skill should be used when writing, reviewing, or refactoring Node.js/Fastify code to ensure optimal performance, security, and maintainability. Triggers on tasks involving Node.js APIs, Fastify routes, database operations, error handling, or backend optimization.
license: MIT
metadata:
  author: nearform
  version: "1.0.0"
---

# Node.js Best Practices

Comprehensive guide for Node.js and Fastify applications, maintained by Nearform. Contains 48 rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Writing new Node.js APIs or Fastify routes
- Implementing database operations
- Reviewing code for performance or security issues
- Refactoring existing Node.js/Fastify code
- Optimizing API response times
- Handling errors and logging
- Setting up monitoring and observability

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Performance & Security | CRITICAL | `perf-` |
| 2 | API Design & Database | CRITICAL | `api-` |
| 3 | Error Handling & Logging | HIGH | `error-` |
| 4 | Fastify Optimization | MEDIUM-HIGH | `fastify-` |
| 5 | Async Patterns | MEDIUM | `async-` |
| 6 | Caching & State | MEDIUM | `cache-` |
| 7 | Code Organization | LOW-MEDIUM | `code-` |
| 8 | Monitoring & Diagnostics | LOW | `monitor-` |

## Quick Reference

### 1. Performance & Security (CRITICAL)

- `perf-block-event-loop` - Detect and prevent event loop blocking
- `perf-security-headers` - Implement essential security headers
- `perf-input-validation` - Validate and sanitize all inputs
- `perf-streaming` - Use streams for large payloads
- `perf-memory-leaks` - Prevent memory leaks
- `perf-compression` - Implement compression strategies

### 2. API Design & Database (CRITICAL)

- `api-rest-design` - Follow RESTful design principles
- `api-pagination` - Implement efficient pagination
- `api-connection-pooling` - Use connection pooling
- `api-query-optimization` - Optimize database queries
- `api-n-plus-one` - Prevent N+1 query problems
- `api-transactions` - Handle transactions properly

### 3. Error Handling & Logging (HIGH)

- `error-middleware` - Centralize error handling
- `error-structured-logging` - Use structured logging (Pino)
- `error-async-errors` - Handle async errors properly
- `error-sensitive-data` - Don't leak sensitive data in errors
- `error-unhandled-rejection` - Handle unhandled rejections
- `error-request-logging` - Log requests efficiently

### 4. Fastify Optimization (MEDIUM-HIGH)

- `fastify-schema-validation` - Use JSON schema validation
- `fastify-hooks` - Optimize hook usage
- `fastify-plugins` - Design reusable plugins
- `fastify-decorators` - Use decorators effectively
- `fastify-serialization` - Optimize JSON serialization
- `fastify-content-type` - Handle content types properly

### 5. Async Patterns (MEDIUM)

- `async-parallel` - Parallelize independent operations
- `async-error-handling` - Handle async errors gracefully
- `async-backpressure` - Handle backpressure in streams
- `async-rate-limiting` - Implement rate limiting
- `async-queue-management` - Use queues for background jobs
- `async-timeout` - Set timeouts for operations

### 6. Caching & State (MEDIUM)

- `cache-lru` - Use in-memory LRU caching
- `cache-redis` - Implement Redis caching
- `cache-http-headers` - Use HTTP caching headers
- `cache-invalidation` - Implement cache invalidation
- `cache-stale-revalidate` - Use stale-while-revalidate pattern
- `cache-database` - Cache database queries

### 7. Code Organization (LOW-MEDIUM)

- `code-module-structure` - Organize code by feature
- `code-dependency-injection` - Use dependency injection
- `code-config-management` - Manage configuration properly
- `code-env-variables` - Handle environment variables
- `code-testing` - Write testable code
- `code-typescript` - Use TypeScript effectively

### 8. Monitoring & Diagnostics (LOW)

- `monitor-health-check` - Implement health check endpoints
- `monitor-metrics` - Collect application metrics
- `monitor-apm` - Integrate APM tools
- `monitor-memory` - Monitor memory usage
- `monitor-cpu` - Profile CPU usage
- `monitor-distributed-tracing` - Implement distributed tracing

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/perf-block-event-loop.md
rules/api-n-plus-one.md
rules/_sections.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
