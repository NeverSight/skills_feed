---
name: "Deprecation Handler"
description: "Handles deprecated APIs, types, and modules by applying safe migration patterns. Use when encountering deprecation warnings, migrating from deprecated code, updating dependencies with breaking changes, or modernizing legacy code to use current APIs."
version: "1.1.0"
model: haiku
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(npx:*)
  - Bash(npm:*)
  - Bash(yarn:*)
---

# Deprecation Handler

This skill helps safely identify, assess, and migrate deprecated code to modern alternatives. It ensures systematic handling of deprecated APIs, types, functions, and modules.

## When to Use

Invoke this skill when:

- Encountering deprecation warnings in compiler/linter output
- Modifying files containing deprecated code
- Upgrading dependencies that introduce breaking changes
- Reviewing code that uses legacy APIs or patterns
- Planning refactoring work on older codebases
- Investigating build warnings or IDE strikethrough indicators

## Workflow

### Step 1: Detect Deprecations

**Automated Detection**:

```bash
# TypeScript compiler warnings
npx tsc --noEmit

# Dependency audit
npm outdated
yarn outdated

# Check for deprecated packages
npm deprecate-check
```

**Manual Detection**:

- Review IDE warnings (strikethrough text, warning indicators)
- Check console output in development environment
- Examine framework migration guides
- Review official changelogs for upgraded versions

**Output**: Create a catalog of all detected deprecations with:

- Location (file path, line number)
- Deprecated API/function/type name
- Deprecation message/reason
- Recommended replacement (if provided)

### Step 2: Assess Impact

**Classify by Priority**:

- **Immediate**: Security vulnerabilities, breaking changes in next version, performance-critical
- **High**: Simple replacements, touching file anyway, direct alternatives available
- **Medium**: Requires refactoring, architectural changes, distant sunset timeline
- **Low**: Monitor only, optional optimizations, style-only changes

**Analyze Scope**:

- Count total usages across codebase
- Identify affected modules/components
- Determine dependencies and coupling
- Estimate migration effort (hours/days)

**Risk Assessment**:

- Breaking change potential
- Test coverage of affected code
- API stability of replacement
- Migration path complexity

### Step 3: Plan Migration

**For Immediate/High Priority**:

1. Identify direct replacement from deprecation message
2. Check official migration guide
3. Verify replacement is stable and well-documented
4. Plan incremental changes (file-by-file or module-by-module)
5. Ensure test coverage exists or add tests

**For Medium/Low Priority**:

1. Document deprecation with inline comments
2. Create task/issue for future work
3. Note blockers preventing immediate fix
4. Link to migration guide or documentation
5. Set review timeline based on sunset date

**Output**: Migration plan with:

- Prioritized list of changes
- File-by-file or module-by-module strategy
- Required testing approach
- Rollback plan if needed

### Step 4: Execute Replacement

**Safe Migration Pattern**:

```typescript
// 1. Add new implementation alongside old
const newImplementation = modernApi.newMethod(params);

// 2. Validate equivalence in tests
expect(newImplementation).toEqual(oldImplementation);

// 3. Replace usage
// const result = legacyApi.deprecatedMethod(params); // DEPRECATED
const result = modernApi.newMethod(params);

// 4. Remove old code after validation
```

**Incremental Approach**:

- Fix one file/module at a time
- Run tests after each change
- Commit working changes incrementally
- Keep related changes together
- Document non-obvious replacements

**For Simple Cases** (same file):

```typescript
// Before
import { deprecatedFunc } from 'old-package';
deprecatedFunc(arg);

// After
import { newFunc } from 'new-package';
newFunc(arg);
```

**For Complex Cases** (separate commit/PR):

1. Create migration branch
2. Update implementation with new API
3. Add comprehensive tests
4. Document breaking changes
5. Review and merge separately

### Step 5: Validate Changes

**Automated Validation**:

```bash
# Type checking
npx tsc --noEmit

# Linting (should show fewer deprecation warnings)
npx eslint . --ext .ts,.tsx,.js,.jsx

# Run test suite
npm test
yarn test

# Build verification
npm run build
yarn build
```

**Manual Validation**:

- Review IDE for remaining deprecation warnings
- Check console for runtime warnings
- Verify functionality in development environment
- Test edge cases and error conditions
- Review diff for unintended changes

**Regression Prevention**:

- Ensure all tests pass
- Verify no new TypeScript errors
- Check that linting warnings decreased
- Confirm build succeeds
- Test affected features manually

## Common Migration Patterns

See `resources/migration-patterns.md` for detailed examples of:

- React lifecycle to hooks
- Class components to functional components
- Deprecated npm packages to modern alternatives
- Legacy API patterns to current best practices
- Framework-specific migration guides

## Documentation Requirements

### For Unfixed Deprecations

When deprecations cannot be immediately fixed:

```typescript
/**
 * TODO: Migrate to newApi.modernMethod() when v3 migration is complete
 *
 * Current usage of deprecatedMethod() due to:
 * - Dependency on legacy authentication system
 * - Breaking changes require coordinated update
 *
 * Migration guide: https://docs.example.com/v2-to-v3
 * Sunset date: 2026-Q2
 * Tracking issue: #1234
 */
legacyApi.deprecatedMethod(params);
```

**Required Elements**:

1. Replacement API/method name
2. Reason for delay (blocker, dependency, complexity)
3. Link to migration guide or documentation
4. Sunset date (if known)
5. Tracking issue/task reference

### For Completed Migrations

Update changelog or migration notes:

```markdown
## Deprecation Fixes

- Replaced `React.createClass` with functional components
- Migrated from `componentWillMount` to `useEffect` hooks
- Updated deprecated `request` package to `axios`
- Removed usage of deprecated `moment` in favor of `date-fns`
```

## Safety Checks

Before completing migration:

- [ ] All tests pass
- [ ] No new TypeScript errors introduced
- [ ] Linting warnings decreased (or explained)
- [ ] Build succeeds without new warnings
- [ ] Functionality verified in development
- [ ] Breaking changes documented
- [ ] Rollback plan identified
- [ ] Code review completed (if team project)

## Edge Cases

### Deprecated with No Replacement

```typescript
// Document why no replacement exists and alternative approach
// DEPRECATED: myLib.removedFeature() has no direct replacement
// Alternative: Implement custom logic using myLib.lowerLevelApi()
// See: https://github.com/mylib/issues/5678
const customImplementation = (params) => {
  // Custom logic using available APIs
};
```

### Conflicting Dependencies

```typescript
// When one dependency requires deprecated API from another:
// TODO: Blocked by outdated-package@2.x requiring deprecated API
// Cannot upgrade until outdated-package releases v3.x
// Tracking: https://github.com/outdated-package/issues/123
deprecatedApi.requiredByDependency();
```

### Partial Migration

```typescript
// When migrating incrementally across large codebase:
// MIGRATION IN PROGRESS: 45% complete (15/33 files migrated)
// See migration plan: docs/deprecation-migration-plan.md
// This file: Not yet migrated (scheduled for Sprint 5)
legacyPattern.stillInUse();
```

## Best Practices

1. **Fix on Touch**: Update deprecations when modifying a file, even if unrelated to main change
2. **Batch Similar Changes**: Group related deprecation fixes in focused commits
3. **Test First**: Ensure test coverage before migrating deprecated code
4. **Document Blockers**: Clearly explain why deprecations remain unfixed
5. **Monitor Sunset Dates**: Track deprecation timelines and plan accordingly
6. **Prefer Official Guides**: Use framework/library migration guides over custom solutions
7. **Validate Equivalence**: Ensure new code behaves identically to deprecated version
8. **Incremental Changes**: Don't mix deprecation fixes with feature work

## Resources

- [resources/standards.md](resources/standards.md) - Full deprecation handling rules and anti-patterns
- [resources/migration-patterns.md](resources/migration-patterns.md) - Common deprecation patterns and solutions
- [resources/framework-guides.md](resources/framework-guides.md) - Framework-specific migration guides
- [resources/testing-strategies.md](resources/testing-strategies.md) - Testing approaches for migration validation

## Related Standards

This skill implements patterns from:

- TypeScript rules - Type safety during migration
- Git standards - Commit practices for deprecation fixes
- React rules - Component migration patterns
