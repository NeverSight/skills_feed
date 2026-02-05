---
name: running-tests
description: Use ANY TIME running tests (npm test, node --test, pytest, etc.) to capture output and prevent context overflow.
---

# Running Tests

Test suites can sometimes take a very long time to run, consume lots of system
resources, and generate lots of output. To save time and preserve your context,
follow this simple guide.

## When to Use This Skill

✅ Use if:
- Running any test command (npm test, node --test, pytest, etc.)
- Expecting more than 5 lines of output
- Want to preserve context tokens for further analysis

❌ Don't use if:
- Running a single quick test file (< 1 second)
- Already redirecting output manually

## Guidelines

- Always redirect test output to a file!

```bash
npm test > /tmp/test-output.txt 2>&1
```

- Analyze that file as needed after the run is finished

```bash
tail -n20 /tmp/test-output.txt

wc -l /tmp/test-output.txt

grep 'fail' /tmp/test-output.txt
```

## Default Pattern

Every test run should follow this pattern:

```bash
npm test > /tmp/test-output.txt 2>&1
tail -20 /tmp/test-output.txt
```

