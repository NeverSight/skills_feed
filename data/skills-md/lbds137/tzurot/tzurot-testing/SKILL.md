---
name: tzurot-testing
description: 'Testing procedures. Invoke with /tzurot-testing for test execution, coverage audits, and debugging test failures.'
lastUpdated: '2026-02-13'
---

# Testing Procedures

**Invoke with /tzurot-testing** for test-related procedures.

**Testing patterns are in `.claude/rules/02-code-standards.md`** - they apply automatically.

## Running Tests

```bash
# Run all tests
pnpm test

# Run specific service
pnpm --filter @tzurot/ai-worker test

# Run specific file
pnpm test -- MyService.test.ts

# Run with coverage
pnpm test:coverage

# Run only changed packages
pnpm focus:test
```

## Coverage Audit Procedure

```bash
# Run unified audit (CI does this automatically)
pnpm ops test:audit

# Filter by category
pnpm ops test:audit --category=services
pnpm ops test:audit --category=contracts

# Update baseline (after closing gaps)
pnpm ops test:audit --update

# Strict mode (fails on ANY gap)
pnpm ops test:audit --strict
```

**Unified Baseline**: `test-coverage-baseline.json` (project root)

## Test File Types

| Type        | Pattern            | Location              | Infrastructure |
| ----------- | ------------------ | --------------------- | -------------- |
| Unit        | `*.test.ts`        | Next to source        | Fully mocked   |
| Integration | `*.int.test.ts`    | Next to source        | PGLite         |
| Schema      | `*.schema.test.ts` | `common-types/types/` | Zod only       |

## Debugging Test Failures

### 1. Run Specific Test

```bash
pnpm test -- MyService.test.ts --reporter=verbose
```

### 2. Check for Fake Timer Issues

```typescript
// ❌ WRONG - Promise rejection warning
const promise = asyncFunction();
await vi.runAllTimersAsync(); // Rejection happens here!
await expect(promise).rejects.toThrow(); // Too late

// ✅ CORRECT - Attach handler BEFORE advancing
const promise = asyncFunction();
const assertion = expect(promise).rejects.toThrow('Error');
await vi.runAllTimersAsync();
await assertion;
```

### 3. Reset Mock State

```typescript
beforeEach(() => {
  vi.clearAllMocks(); // Clear call history, keep impl
});
afterEach(() => {
  vi.restoreAllMocks(); // Restore originals (spies only)
});
```

## Creating Mock Factories

```typescript
// Use async factory for vi.mock hoisting
vi.mock('./MyService.js', async () => {
  const { mockMyService } = await import('../test/mocks/MyService.mock.js');
  return mockMyService;
});

// Import accessors after vi.mock
import { getMyServiceMock } from '../test/mocks/index.js';

it('should call service', () => {
  expect(getMyServiceMock().someMethod).toHaveBeenCalled();
});
```

## Integration Tests with PGLite

```typescript
describe('UserService', () => {
  let pglite: PGlite;
  let prisma: PrismaClient;

  beforeAll(async () => {
    pglite = new PGlite({ extensions: { vector } });
    await pglite.exec(loadPGliteSchema());
    prisma = new PrismaClient({ adapter: new PrismaPGlite(pglite) });
  });

  it('should create user', async () => {
    const service = new UserService(prisma);
    const userId = await service.getOrCreateUser('123', 'testuser');
    expect(userId).toBeDefined();
  });
});
```

**⚠️ ALWAYS use `loadPGliteSchema()`** - NEVER create tables manually!

## Integration Test Triggers

Integration tests (`*.int.test.ts`) run separately from unit tests and are **not** included in `pnpm test` or pre-push hooks.

**Always run `pnpm test:int` after:**

| Change                           | Why                                                                   |
| -------------------------------- | --------------------------------------------------------------------- |
| Add/remove slash command options | `CommandHandler.int.test.ts` snapshots capture full command structure |
| Add/remove subcommands           | Same snapshot tests                                                   |
| Restructure command directories  | `getCommandFiles()` discovery changes affect command loading          |
| Change component prefix routing  | Integration tests verify button/select menu routing                   |

**Update snapshots with:** `pnpm vitest run --config vitest.int.config.ts <file> --update`

## Definition of Done

- [ ] New service files have `.int.test.ts`
- [ ] New API schemas have `.schema.test.ts`
- [ ] Coverage doesn't drop (Codecov enforces 80%)
- [ ] Run `pnpm ops test:audit` to verify no new gaps

## References

- Full testing guide: `docs/reference/guides/TESTING.md`
- Mock factories: `services/*/src/test/mocks/`
- PGLite setup: `docs/reference/testing/PGLITE_SETUP.md`
- Coverage audit: `docs/reference/testing/COVERAGE_AUDIT_SYSTEM.md`
- Rules: `.claude/rules/02-code-standards.md`
