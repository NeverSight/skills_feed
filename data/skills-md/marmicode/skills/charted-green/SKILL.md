---
name: charted-green
description: Progressively activates todo tests one at a time, updates implementation code until each passes (verified via Wallaby), then moves to the next—following the design doc as the single source of truth.
---

# Context

- designDocPath: $ARGUMENTS[0]
- testFilePath: $ARGUMENTS[1]

# Goal

Using the design doc at `${designDocPath}` as the single source of truth, progressively activate the tests in `${testFilePath}`.

# Steps

Categorize each test in `${testFilePath}` as:

- Implemented tests: tests that contain actual test code (not just empty or comments)
- Empty tests: tests that are empty or only contain comments - TOTALLY IGNORE THESE

For each implemented test, convert `it.todo(...)` into `it(...)`, but do it strictly one test at a time, then update the implementation just enough for that specific test to turn green — NOTHING MORE.

DO NOT IMPLEMENT ANYTHING THAT IS NOT DIRECTLY RELATED TO THE CURRENT TEST.

STOP when these tests are green.

# Rules

DO NOT IMPLEMENT EMPTY TESTS.

NEVER implement tests.

ONLY EDIT TESTS as a last resort after you have tried everything else.

Use the Wallaby MCP server to verify test results after each change. Only once the current test passes should you advance to the next one.
