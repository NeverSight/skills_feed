---
name: vitest
description: Comprehensive Vitest testing framework guide with strong emphasis on Jest-to-Vitest migration. Covers automated migration using codemods, configuration setup, API differences, best practices, and troubleshooting. Use when migrating from Jest, setting up Vitest, writing tests, configuring test environments, or resolving migration issues. Primary focus is seamless Jest migration with minimal code changes.
---

<objective>
Expert guidance for migrating from Jest to Vitest and working with the Vitest testing framework. This skill focuses primarily on **automated migration from Jest** while covering setup, configuration, and best practices.

**Key benefits of Vitest over Jest:**

- 2-10x faster test startup (built on Vite and esbuild)
- Native TypeScript support without ts-jest
- Hot Module Replacement for instant re-runs
- Jest-compatible API requiring minimal code changes
- Modern ESM-first architecture
</objective>

<quick_start>
<automated_migration>
**RECOMMENDED APPROACH**: Use automated codemods for fastest migration.

**Option 1: vitest-codemod** (recommended)

```bash
# Install globally
npm install -g @vitest-codemod/jest

# Run migration on test files
vitest-codemod jest path/to/tests/**/*.test.js

# Or use npx (no installation)
npx @vitest-codemod/jest path/to/tests
```

**Option 2: Codemod.com Platform**

```bash
# Using VS Code extension
# Install "Codemod" extension from marketplace
# Right-click project → "Run Codemod" → "Jest to Vitest"

# Using CLI
npx codemod jest/vitest
```

**What codemods handle automatically:**

- ✓ Convert `jest.mock()` → `vi.mock()`
- ✓ Convert `jest.fn()` → `vi.fn()`
- ✓ Convert `jest.spyOn()` → `vi.spyOn()`
- ✓ Convert `jest.setTimeout()` → `vi.setConfig({ testTimeout })`
- ✓ Update global matchers and timer mocks
- ✓ Transform `jest.requireActual()` → `vi.importActual()`
- ✓ Update mock resets/clears/restores
</automated_migration>

<manual_migration>
**For users who need manual control or want to understand changes:**

**1. Install Vitest**

```bash
# Remove Jest
npm uninstall jest @types/jest ts-jest jest-environment-jsdom

# Install Vitest
npm install -D vitest @vitest/ui happy-dom
```

**2. Create vitest.config.ts**

```typescript
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    globals: true,              // Enable globals for Jest compatibility
    environment: 'happy-dom',   // Faster than jsdom
    setupFiles: ['./vitest.setup.ts'],
    clearMocks: true,
    restoreMocks: true,
  },
})
```

**3. Update package.json**

```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage"
  }
}
```

**4. Update TypeScript config**

```json
{
  "compilerOptions": {
    "types": ["vitest/globals"]
  }
}
```

**5. Update mock syntax**

```typescript
// Replace in all test files:
jest.fn → vi.fn
jest.spyOn → vi.spyOn
jest.mock → vi.mock
jest.useFakeTimers → vi.useFakeTimers
jest.clearAllMocks → vi.clearAllMocks
```

</manual_migration>

<automated_scripts>
**For comprehensive migrations with validation and rollback:**

Ready-to-run migration scripts available in `scripts/` directory:

- `quick-migrate.sh` - Fast 30-second migration for simple projects
- `comprehensive-migrate.sh` - Full-featured migration with project detection, backups, and validation

See [references/MIGRATION_SCRIPT.md](references/MIGRATION_SCRIPT.md) for usage instructions.
</automated_scripts>
</quick_start>

<critical_differences>
<module_mocking>
**Jest**: Auto-returns default export

```typescript
jest.mock('./module', () => 'hello')
```

**Vitest**: Must specify exports explicitly

```typescript
vi.mock('./module', () => ({
  default: 'hello'  // Explicit default export required
}))
```

</module_mocking>

<mock_reset_behavior>
**Jest**: `mockReset()` replaces with empty function returning `undefined`

**Vitest**: `mockReset()` resets to original implementation

To match Jest behavior in Vitest:

```typescript
mockFn.mockReset()
mockFn.mockImplementation(() => undefined)
```

</mock_reset_behavior>

<globals_configuration>
**Jest**: Globals enabled by default

**Vitest**: Must explicitly enable:

```typescript
export default defineConfig({
  test: {
    globals: true  // Enable for Jest compatibility
  }
})
```

Then add to `tsconfig.json`:

```json
{
  "compilerOptions": {
    "types": ["vitest/globals"]
  }
}
```

</globals_configuration>

<auto_mocking>
**Jest**: Files in `__mocks__/` auto-load

**Vitest**: Must call `vi.mock()` explicitly, or add to `setupFiles`:

```typescript
// vitest.setup.ts
vi.mock('./path/to/module')
```

</auto_mocking>

<async_tests>
**Jest**: Supports callback style with `done()`

**Vitest**: Use async/await or Promises

```typescript
// Before (Jest)
test('async test', (done) => {
  setTimeout(() => {
    expect(true).toBe(true)
    done()
  }, 100)
})

// After (Vitest)
test('async test', async () => {
  await new Promise(resolve => {
    setTimeout(() => {
      expect(true).toBe(true)
      resolve()
    }, 100)
  })
})
```

</async_tests>
</critical_differences>

<common_issues>
<testing_library_cleanup>
**Problem**: Auto-cleanup doesn't run when `globals: false`

**Solution**: Manually import cleanup in setup file

```typescript
// vitest.setup.ts
import { cleanup } from '@testing-library/react'
import { afterEach } from 'vitest'

afterEach(() => {
  cleanup()
})
```

</testing_library_cleanup>

<path_aliases>
**Problem**: Jest's `moduleNameMapper` not working

**Solution**: Configure in `vitest.config.ts`

```typescript
import { defineConfig } from 'vitest/config'
import path from 'path'

export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
    }
  }
})
```

</path_aliases>

<coverage_differences>
**Problem**: Coverage numbers don't match Jest

**Solution**: Vitest uses V8 by default. For Istanbul (Jest's provider):

```bash
npm install -D @vitest/coverage-istanbul
```

```typescript
export default defineConfig({
  test: {
    coverage: {
      provider: 'istanbul'
    }
  }
})
```

</coverage_differences>

<snapshot_names>
**Problem**: Test names in snapshots use `>` separator instead of spaces

```
Jest:  "describe title test title"
Vitest: "describe title > test title"
```

**Solution**: Regenerate snapshots with `npm run test -u`
</snapshot_names>
</common_issues>

<best_practices>

1. **Use `happy-dom` over `jsdom`** - 2-3x faster for most use cases
2. **Enable globals for easier migration** - Set `globals: true` in config
3. **Use watch mode during development** - `npm run test` (default behavior)
4. **Leverage UI mode for debugging** - `npm run test:ui` opens browser interface
5. **Configure auto-cleanup** - Set `clearMocks: true` and `restoreMocks: true`
6. **Use workspace configuration for monorepos** - See [CONFIG.md](references/CONFIG.md)
</best_practices>

<performance_optimization>

```typescript
export default defineConfig({
  test: {
    environment: 'node', // or 'happy-dom' instead of 'jsdom'
    maxWorkers: 4,       // Increase for parallel execution
    fileParallelism: true,
    testTimeout: 5000,
    isolate: false,      // Faster but use with caution
    pool: 'threads',     // or 'forks' for better isolation
  }
})
```

**Pool options:**

- `threads` (default) - Fast, CPU-intensive tests
- `forks` - Better isolation, more memory
- `vmThreads` - Best for TypeScript performance
</performance_optimization>

<migration_workflow>
**Recommended migration process:**

1. **Prepare**
   - Ensure all Jest tests passing
   - Commit working state
   - Create migration branch

2. **Install dependencies**

   ```bash
   npm install -D vitest @vitest/ui happy-dom
   ```

3. **Run automated codemod**

   ```bash
   npx @vitest-codemod/jest src/**/*.test.ts
   ```

4. **Create configuration**
   - Add `vitest.config.ts` with `globals: true`
   - Update `package.json` scripts
   - Update `tsconfig.json` types

5. **Run tests and fix issues**

   ```bash
   npm run test
   ```

   - Address failures one by one
   - Check [MIGRATION.md](references/MIGRATION.md) for solutions

6. **Update CI/CD**
   - Replace Jest commands with Vitest
   - Update coverage paths if needed

7. **Cleanup**

   ```bash
   npm uninstall jest @types/jest ts-jest
   rm jest.config.js
   ```

</migration_workflow>

<common_commands>

```bash
npm run test                    # Watch mode
npm run test:run                # Run once (CI mode)
npm run test:coverage           # With coverage
npm run test:ui                 # Visual UI
npm run test path/to/file.test.ts  # Specific file
npm run test -t "pattern"       # Matching pattern
npm run test --environment jsdom   # Specific environment
npm run test -u                 # Update snapshots
```

</common_commands>

<detailed_references>
For comprehensive information:

- **[MIGRATION.md](references/MIGRATION.md)** - Complete Jest→Vitest API mapping, troubleshooting, framework-specific guides
- **[CONFIG.md](references/CONFIG.md)** - Full configuration reference with examples for React, Vue, TypeScript, Node.js, monorepos
- **[MIGRATION_SCRIPT.md](references/MIGRATION_SCRIPT.md)** - Automated migration script usage and customization
- **Official Vitest docs**: <https://vitest.dev>
- **Vitest migration guide**: <https://vitest.dev/guide/migration>
- **vitest-codemod tool**: <https://github.com/trivikr/vitest-codemod>
- **Codemod platform**: <https://codemod.com/migrations/jest-to-vitest>
</detailed_references>

<success_criteria>
Migration is successful when:

- All tests passing with `npm run test:run`
- Coverage reports generate correctly
- CI/CD pipeline runs tests successfully
- No `jest` references remain in codebase
- TypeScript types resolve without errors
- Test execution is noticeably faster (2-10x improvement)
</success_criteria>

<when_successful>
After successful migration, you should observe:

- **5x faster cold start** - Initial test run (10s → 2s typical)
- **5x faster watch mode** - Hot reload (5s → <1s typical)
- **2x faster execution** - Overall test suite runtime
- **10x faster TypeScript tests** - No ts-jest compilation overhead
- **Better DX** - Instant feedback, visual UI, better error messages
</when_successful>
