---
name: charted-red
description: Writes the next failing test based on provided design doc and existing todo tests
---

# Context

- designDocPath: $ARGUMENTS[0]
- testFilePath: $ARGUMENTS[1]

# Task

Based on the design doc at ${designDocPath} (if present), implement the body of the next todo test in ${testFilePath} without enabling it (i.e. keep "it.todo").

- Remove the step-by-step comment instructions from the test body and replace them with actual code.
- Remember that you love TDD and you want to write tests first.
- Implement the test only, do not implement the feature.

## Example

### Before

```ts
it.todo("compute sum", () => {
  // Inject calculator
  // Call calculator.sum(1, 2)
  // Assert that the result is 3
});
```

### After

```ts
it.todo("compute sum", () => {
  const calculator = t.inject(Calculator);
  const result = calculator.sum(1, 2);
  expect(result).toBe(3);
});
```
