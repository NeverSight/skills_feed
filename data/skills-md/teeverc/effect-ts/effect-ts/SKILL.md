---
name: effect-ts
description: "Effect-TS (Effect) guidance for TypeScript: designing and implementing Effect-based code, modeling expected errors vs defects, managing dependencies with Context/Layer/Effect.Service, handling resource lifecycles with Scope, running effects at the program edge, using Effect.gen, validating data with Effect Schema, and testing time with TestClock. Use when asked to build, refactor, review, or explain Effect code or when converting Promise/async code to Effect."
---

# Effect-TS

## Overview

Provide workflows, patterns, and best practices for building Effect-based TypeScript programs, with focused references for errors, dependencies, resources, runtime execution, generators, schema, and testing.

For the most up-to-date documentation, see https://effect.website/docs and https://effect.website/docs/platform. For internal lookups, the effect-docs MCP can be used to search and fetch API references (https://github.com/tim-smart/effect-mcp).

## Quick Triage

- If it needs core Effect data types or combinators, open `references/core-usage.md`.
- If the task is about error modeling or typed failures, open `references/error-management.md`.
- If it needs error tooling (sandboxing, Cause, error-channel transforms), open `references/error-tooling.md`.
- If it involves services/dependencies, open `references/dependency-management.md`.
- If it involves layer construction or test wiring, open `references/layer-patterns.md`.
- If it involves resource lifecycles, open `references/resource-management.md`.
- If it involves running effects or runtime choice, open `references/runtime-execution.md`.
- If it involves fibers or concurrency primitives, open `references/concurrency.md`.
- If it involves interruption, supervision, or fiber refs, open `references/concurrency-advanced.md`.
- If it involves schedules or repetition, open `references/scheduling.md`.
- If it involves retries/backoff or schedule composition, open `references/scheduling-retry.md`.
- If it involves streams, queues, pubsub, or STM, open `references/streams-queues-stm.md`.
- If it involves HTTP clients or external APIs, open `references/http-client.md`.
- If it involves HTTP servers or API definitions, open `references/http-server.md`.
- If it involves request batching or data loaders, open `references/request-resolver.md`.
- If it involves caching or memoization, open `references/caching.md`.
- If it involves configuration or config providers, open `references/configuration.md`.
- If it involves advanced config or redaction, open `references/configuration-advanced.md`.
- If it involves logs, metrics, or tracing, open `references/observability.md`.
- If it needs concrete logger/metrics/tracing setups or exporters, open `references/observability-examples.md`.
- If it needs wiring of log/metric/trace layers, open `references/observability-wiring.md`.
- If it needs sequential/branching readability, open `references/generators.md`.
- If it needs runtime validation/decoding, open `references/schema.md`.
- If it needs deterministic time in tests, open `references/testing.md`.
- If it needs broader testing services, open `references/testing-stack.md`.
- If it involves migrating from Promise/async, open `references/migration-async.md`.
- If it needs versioning or signature changes, open `references/versioning.md`.
- If it hits common pitfalls or runtime errors, open `references/troubleshooting.md`.
- If it needs result inspection or debugging, open `references/exit-cause.md`.

## Core Workflow

1. Clarify boundaries and IO; keep core logic as `Effect` values.
2. Choose style: use pipelines for simple composition; use `Effect.gen` for sequential logic.
3. Model errors explicitly: type expected errors; treat defects as unexpected failures.
4. Model dependencies with services, tags, and layers; keep interfaces clean of construction concerns.
5. Manage resource lifecycles with `Scope` when opening/closing resources.
6. Provide the environment via layers and run effects only at the program edge.

## Output Standards

- Show imports and minimal runnable examples.
- Keep dependency graphs explicit (services, layers, context tags).
- Include error channel types and call out expected vs defect errors.
- Avoid running effects inside libraries; show runtime usage in entrypoints or tests.

## References

- `references/core-usage.md` - core data types and common combinators.
- `references/error-management.md` - expected vs unexpected errors and error-channel guidance.
- `references/error-tooling.md` - sandboxing, Cause handling, and error-channel transforms.
- `references/exit-cause.md` - Exit/Cause usage and result handling.
- `references/dependency-management.md` - services, tags, contexts, layers, and Effect.Service patterns.
- `references/layer-patterns.md` - layer construction, composition, and test wiring.
- `references/resource-management.md` - Scope and finalizers.
- `references/runtime-execution.md` - run\* functions and edge execution.
- `references/concurrency.md` - fibers, forking, and lifetime strategies.
- `references/concurrency-advanced.md` - interruption, supervision, and fiber refs.
- `references/scheduling.md` - schedules, repetition, and timing.
- `references/scheduling-retry.md` - retry policies, backoff, and schedule composition.
- `references/streams-queues-stm.md` - Stream, Queue, PubSub, and STM touchpoints.
- `references/http-client.md` - HTTP client patterns and external API calls.
- `references/http-server.md` - HTTP server and HttpApi patterns.
- `references/request-resolver.md` - Request/RequestResolver batching patterns.
- `references/caching.md` - caching and memoization utilities.
- `references/configuration.md` - Config, ConfigProvider, and runtime configuration.
- `references/configuration-advanced.md` - nested config, redaction, and test providers.
- `references/observability.md` - logging, metrics, and tracing overview.
- `references/observability-examples.md` - concrete logger/metrics/tracing configs and exporters.
- `references/observability-wiring.md` - how to provide observability layers in apps.
- `references/generators.md` - Effect.gen patterns.
- `references/schema.md` - Effect Schema overview and requirements.
- `references/testing.md` - TestClock guidance.
- `references/testing-stack.md` - test services, layers, and config in tests.
- `references/migration-async.md` - guidance for Promise/async migration.
- `references/versioning.md` - version and signature change notes.
- `references/troubleshooting.md` - common errors and fixes.
