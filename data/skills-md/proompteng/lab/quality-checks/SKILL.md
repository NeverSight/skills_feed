---
name: quality-checks
description: Run formatting, lint, typecheck, and tests for this repo; use when validating changes or investigating CI failures.
---

# Quality Checks

## Overview

Run the smallest set of checks for touched code. Use workspace filters and targeted test commands.

## JS/TS

```bash
bun run format
bun run --filter @proompteng/bumba lint
bun run --filter @proompteng/bumba tsc
bunx biome check services/bumba
```

## Go

```bash
go test ./services/prt
go build ./services/prt
```

## Kotlin

```bash
./gradlew test --tests "pkg.ClassTest"
```

## Rails

```bash
bundle exec rails test test/models/user_test.rb:42
```

## Python

```bash
pytest alchimie_tests/test_file.py -k "pattern"
```

## Resources

- Reference: `references/quality-matrix.md`
- Helper script: `scripts/run-quality.sh`
- Checklist: `assets/quality-checklist.md`
