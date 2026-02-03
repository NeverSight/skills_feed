---
name: akka-streams
description: Scala reactive streaming with Akka Streams and Pekko Streams. Use for dataflow and reactive programming patterns, testing stream components, and understanding when NOT to use streams (prefer plain functions for transformations and I/O).
---

# Akka Streams and Pekko Streams (Scala)

## Quick start
- **Think twice before using Streams**: prefer plain functions, even for I/O.
- Test stream components using `TestSource`, `TestSink`, and `TestProbe` from `akka-stream-testkit`.
- Always define supervision strategies for error handling; default behavior tears down the entire stream.
- Read `references/akka-streams.md` for core concepts and patterns.
- Read `references/best-practices.md` for critical guidance on when NOT to use streams.
- Read `references/testing.md` for comprehensive testing examples.

## When NOT to use Streams
- Don't model plain data transformations as stream operators; use regular functions instead.
- Don't use streams for general I/O; prefer plain functions or other abstractions.

## Workflow
1. Verify that Streams are the right tool: do you need dataflow or reactive programming patterns?
2. Design `Source`, `Flow`, and `Sink` components as separate, testable units.
3. Define error handling with `recover`, `recoverWithRetries`, or supervision strategies.
4. Test each component with `TestSource`/`TestSink` or `TestProbe` before integration.
5. Compose the final graph and materialize with explicit error handling.

## Testing rules
- Write tests using `akka-stream-testkit` for custom stream components.
- Use `TestSource.probe` and `TestSink.probe` for fine-grained control over element flow.
- Test backpressure behavior explicitly using `request()` and `expectNoMessage()`.
- Test error scenarios with `expectError()` or supervision strategies.

## Pekko Streams
- Pekko Streams is a fork of Akka Streams with identical APIs (package names change from `akka.*` to `org.apache.pekko.*`).
- All guidance for Akka Streams applies equally to Pekko Streams.
- When working with Pekko, adjust imports but keep patterns and testing approaches identical.

## Output expectations
- Keep stream topologies simple and testable; break complex graphs into named components.
- Make error handling explicit via supervision or recovery operators.
- Prefer immutability; stream graphs are blueprints until materialized.

## References
- Load `references/akka-streams.md` for core concepts, operators, and materialization.
- Load `references/best-practices.md` for critical guidance on avoiding stream overuse.
- Load `references/testing.md` for testing patterns and complete examples.
