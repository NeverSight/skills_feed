---
name: test
description: Run tests for Aenea project - unit tests, integration tests, coverage reports, watch mode
allowed-tools: Bash, Read, Grep, Glob
---

# Test

テスト実行とデバッグ。

## Commands

```bash
npm test                    # All tests
npm run test:watch          # Watch mode
npm run test:coverage       # Coverage
npm test -- path/to/test.ts # Specific file
```

## Key Test Files

- [tests/aenea/memory/memory-consolidator.test.ts](tests/aenea/memory/memory-consolidator.test.ts)
- [tests/utils/energy-management.test.ts](tests/utils/energy-management.test.ts)
- [tests/integration/database-persistence.test.ts](tests/integration/database-persistence.test.ts)

## Troubleshooting

```bash
# Database lock
pkill -f "aenea" && rm -f data/test_*.db
```

## Detailed Reference

Test philosophy, benchmarks, coverage areas: [reference.md](reference.md)
