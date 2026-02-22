---
name: jest
description:
    Testing Roblox/Luau code with Jest Roblox. Use when writing tests, mocking
    functions, asserting values, or configuring test suites in Luau with Jest
    Roblox. NOT JavaScript Jest — uses .never instead of .not, jest.fn() returns
    two values, 0 is truthy.
metadata:
    author: Christopher Buss
    version: "2026.2.7"
    source:
        Generated from https://github.com/Roblox/jest-roblox, scripts located at
        https://github.com/christopher-buss/skills
---

> Based on Jest Roblox v3.x, generated 2026-02-07.

Jest Roblox is a Luau port of Jest for the Roblox platform. It closely follows
the upstream Jest API but has critical deviations due to Luau language
constraints.

**Critical deviations from JS Jest:**

- `.never` instead of `.not` (reserved keyword)
- `jest.fn()` returns **two values**: mock object + forwarding function
- `0`, `""`, `{}` are **truthy** in Luau (only `false` and `nil` are falsy)
- All globals (`describe`, `expect`, `jest`, etc.) must be explicitly imported
- `.each` uses table syntax, not tagged template literals
- Custom matchers take `self` as first parameter

Read [core-deviations](references/core-deviations.md) first when working with
this codebase.

## Core References

| Topic               | Description                                              | Reference                                                          |
| ------------------- | -------------------------------------------------------- | ------------------------------------------------------------------ |
| Deviations          | All Luau/Roblox differences from JS Jest                 | [core-deviations](references/core-deviations.md)                   |
| Test Structure      | describe, test/it, hooks, .each, .only/.skip             | [core-test-structure](references/core-test-structure.md)           |
| Matchers            | toBe, toEqual, toContain, toThrow, mock matchers         | [core-matchers](references/core-matchers.md)                       |
| Asymmetric Matchers | expect.anything/any/nothing/callable, .resolves/.rejects | [core-asymmetric-matchers](references/core-asymmetric-matchers.md) |
| Mocking             | jest.fn(), spyOn, mock.calls, return values              | [core-mocking](references/core-mocking.md)                         |
| Configuration       | jest.config.lua, runCLI, reporters, options              | [core-configuration](references/core-configuration.md)             |

## Features

### Testing Patterns

| Topic            | Description                                     | Reference                                                          |
| ---------------- | ----------------------------------------------- | ------------------------------------------------------------------ |
| Async Testing    | Promises, done callbacks, .resolves/.rejects    | [feature-async-testing](references/feature-async-testing.md)       |
| Custom Matchers  | expect.extend(), self parameter, isNever        | [feature-custom-matchers](references/feature-custom-matchers.md)   |
| Snapshot Testing | toMatchSnapshot, property matchers, serializers | [feature-snapshot-testing](references/feature-snapshot-testing.md) |
| Test Filtering   | testMatch, testPathPattern, testNamePattern     | [feature-test-filtering](references/feature-test-filtering.md)     |

### Mocking

| Topic          | Description                                   | Reference                                                      |
| -------------- | --------------------------------------------- | -------------------------------------------------------------- |
| Timer Mocks    | useFakeTimers, Roblox timers, engineFrameTime | [feature-timer-mocks](references/feature-timer-mocks.md)       |
| Global Mocks   | jest.globalEnv, spyOn globals, library mocks  | [feature-global-mocks](references/feature-global-mocks.md)     |
| Module Mocking | jest.mock(), isolateModules, resetModules     | [feature-module-mocking](references/feature-module-mocking.md) |

### Advanced

| Topic        | Description                                      | Reference                                                    |
| ------------ | ------------------------------------------------ | ------------------------------------------------------------ |
| Benchmarking | benchmark(), Reporter, Profiler, CustomReporters | [advanced-benchmarking](references/advanced-benchmarking.md) |
