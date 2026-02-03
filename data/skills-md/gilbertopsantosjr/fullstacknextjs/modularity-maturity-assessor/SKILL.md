---
name: modularity-maturity-assessor
description: Architecture maturity specialist that assesses modular architecture compliance and maturity levels against the 10 modular principles, with enhanced focus on state isolation, service layer patterns, runtime independence, and explicit communication. Adapted for Next.js 15+, DynamoDB, ZSA, and Vitest.
---

# Modularity Maturity Assessor (Next.js + DynamoDB)

Expert in evaluating modular architecture compliance and maturity levels based on the 10 foundational principles, with enhanced detection for modern patterns like service layer design, runtime-agnostic code, and explicit communication contracts.

## Technology Stack Context

| Component | Technology |
|-----------|------------|
| Framework | Next.js 15+ / React 19+ |
| Database | DynamoDB (single-table design) |
| ORM | OneTable |
| Server Actions | ZSA (Zod Server Actions) |
| Validation | Zod schemas |
| Testing | Vitest |
| Deployment | SST (Serverless Stack) |

## Critical Principles (Highest Weight)

These principles have the highest impact on architecture maturity:

| Rank | Principle | Weight | Why Critical |
|------|-----------|--------|--------------|
| 1 | **State Isolation (P8)** | 1.5x | Most frequently violated, causes data integrity issues |
| 2 | **Well-Defined Boundaries (P1)** | 1.2x | Foundation for all other principles |
| 3 | **Explicit Communication (P5)** | 1.2x | Prevents coupling via service layer enforcement |
| 4 | **Deployment Independence (P7)** | 1.0x | Enables runtime flexibility (Next.js + Lambda) |

## When to Use This Skill

- User asks for architecture assessment, compliance check, or maturity evaluation
- User mentions "modularity", "architecture quality", or "principle compliance"
- User requests verification of feature boundaries or design patterns
- Proactively after major refactoring or feature creation to verify compliance
- **Before production deployments** to catch compliance regressions
- **After adding cross-feature dependencies** to verify proper communication patterns

## Assessment Process

### Phase 1: Load Documentation Context

Load documents in this order as needed:

1. **Always start with**: `docs/ARCHITECTURE-OVERVIEW.md` (navigation hub)
2. **For state isolation checks**: `docs/STATE-ISOLATION.md` (most critical violations)
3. **For feature structure**: `docs/MODULAR-PRINCIPLES.md` (principles 1-7)
4. **For implementation patterns**: `docs/CODING-PATTERNS.md`
5. **For DynamoDB patterns**: `docs/DYNAMODB-DESIGN.md`

### Phase 2: Run Detection Commands

**Critical - State Isolation (Principle 8)**: HIGHEST PRIORITY

```bash
# Cross-feature DAL imports (MOST CRITICAL)
echo "=== Cross-Feature DAL Imports (P0) ==="
grep -r "from '@/features/[^']*dal'" src/features/ | \
  awk -F: '{
    match($1, /features\/([^/]+)/, feat);
    match($2, /features\/([^/]+)\/dal/, imported);
    if (feat[1] != imported[1] && imported[1] != "") {
      print "VIOLATION: " $1 " imports from " imported[1] "/dal"
    }
  }'

# DynamoDB key patterns without feature prefix
echo "=== DynamoDB Key Patterns ==="
grep -E "(pk|sk):" src/features/database/db-schema.ts
```

**Deployment Independence (Principle 7) - Runtime Agnostic**:

```bash
# Check for 'server-only' in DAL files (P0 - breaks Lambda)
echo "=== 'server-only' in DAL (P0) ==="
grep -l "server-only" src/features/*/dal/*.ts 2>/dev/null

# Check for Next.js-specific imports in DAL/service (P1)
echo "=== Next.js imports in DAL/Service (P1) ==="
grep -r "from 'next" src/features/*/dal/ src/features/*/service/ 2>/dev/null
```

**Explicit Communication (Principle 5) - Service Layer**:

```bash
# Check for missing service layers when features are accessed externally
echo "=== Features Without Service Layer (P1) ==="
for dir in src/features/*/; do
  name=$(basename $dir)
  external_imports=$(grep -r "from '@/features/$name'" src/features/ 2>/dev/null | grep -v "src/features/$name" | wc -l)
  if [ "$external_imports" -gt 0 ]; then
    if [ ! -d "$dir/service" ]; then
      echo "WARNING: $name has $external_imports external imports but no service layer"
    fi
  fi
done

# Check for DAL exports in index.ts (violation)
echo "=== DAL Exports in index.ts (P1) ==="
grep -l "from.*dal" src/features/*/index.ts 2>/dev/null
```

**Well-Defined Boundaries (Principle 1)**:

```bash
# Check what's exported from each feature
echo "=== Feature Exports ==="
for dir in src/features/*/; do
  name=$(basename $dir)
  if [ -f "$dir/index.ts" ]; then
    echo "=== $name ==="
    grep "export" $dir/index.ts
  fi
done
```

**RepositoryResult Pattern**:

```bash
# DAL files without RepositoryResult (P1)
echo "=== DAL Without RepositoryResult (P1) ==="
grep -L "RepositoryResult" src/features/*/dal/*.ts 2>/dev/null | grep -v test | grep -v index
```

**Lean Server Actions**:

```bash
# Check action file sizes (should be <50 lines)
echo "=== Action File Sizes ==="
find src/features/*/actions -name "*.ts" ! -name "index.ts" -exec wc -l {} \; 2>/dev/null | \
  awk '$1 > 50 {print "WARNING: " $2 " has " $1 " lines (>50)"}'

# Check for ZSA pattern usage
echo "=== ZSA Pattern Usage ==="
grep -l "authedProcedure\|publicProcedure" src/features/*/actions/*.ts 2>/dev/null | wc -l
```

**Testing (Vitest)**:

```bash
# Check for test files
echo "=== Test Coverage ==="
for dir in src/features/*/dal/; do
  feature=$(echo $dir | sed 's|src/features/||' | sed 's|/dal/||')
  dal_count=$(ls $dir/*.ts 2>/dev/null | grep -v test | grep -v index | wc -l)
  test_count=$(ls $dir/*.test.ts 2>/dev/null | wc -l)
  echo "$feature: $test_count tests for $dal_count DAL files"
done

# Check for cross-feature DAL imports in tests (violation)
echo "=== Cross-Feature DAL in Tests (P0) ==="
grep -r "from '@/features/[^']*dal'" src/features/**/*.test.ts 2>/dev/null | \
  awk -F: '{
    match($1, /features\/([^/]+)/, feat);
    match($2, /features\/([^/]+)\/dal/, imported);
    if (feat[1] != imported[1] && imported[1] != "") {
      print "VIOLATION: " $1 " imports from " imported[1] "/dal"
    }
  }'
```

## Maturity Scoring

| Principle                  | Score | Weight | Weighted Score | Notes                    |
| -------------------------- | ----- | ------ | -------------- | ------------------------ |
| 1. Boundaries              | X/10  | 1.2    | X              | [Brief note]             |
| 2. Composability           | X/10  | 0.8    | X              | [Brief note]             |
| 3. Independence            | X/10  | 1.0    | X              | [Brief note]             |
| 4. Individual Scale        | X/10  | 0.6    | X              | [Brief note]             |
| 5. Explicit Communication  | X/10  | 1.2    | X              | [Brief note]             |
| 6. Replaceability          | X/10  | 0.8    | X              | [Brief note]             |
| 7. Deployment Independence | X/10  | 1.0    | X              | [Brief note]             |
| 8. State Isolation         | X/10  | 1.5    | X              | [Brief note] CRITICAL    |
| 9. Observability           | X/10  | 0.9    | X              | [Brief note]             |
| 10. Fail Independence      | X/10  | 0.9    | X              | [Brief note]             |
| **TOTAL**                  |       | 10.0   | **X/100**      |                          |

### Scoring Guidelines

**10/10 - Excellent**: Full compliance, best practices followed, service layers where needed
**8-9/10 - Good**: Strong compliance, minor improvements possible
**6-7/10 - Acceptable**: Partial compliance, some violations, missing service layers
**4-5/10 - Needs Improvement**: Multiple violations, cross-feature DAL access detected
**1-3/10 - Critical**: Major violations, state isolation broken, immediate action required

### Automatic Fail Conditions

The following violations automatically cap the overall score:

| Violation | Max Score | Reason |
|-----------|-----------|--------|
| Cross-feature DAL imports | 40/100 | Independence completely broken |
| `'server-only'` in DAL | 50/100 | Deployment independence broken |
| Cross-feature DAL in tests | 55/100 | Test isolation broken |
| Missing service layer (when needed) | 65/100 | Explicit communication violated |
| DAL exports in index.ts | 70/100 | Boundaries not well-defined |
| DAL without RepositoryResult | 75/100 | Error handling pattern missing |

## Common Pitfalls to Check

### P0 - Critical (Block Deployment)

1. **Cross-Feature DAL Imports** - MOST CRITICAL
2. **`'server-only'` in DAL** - Breaks Lambda deployment
3. **Cross-Feature DAL in Tests** - Test isolation violation
4. **DynamoDB Keys Without Feature Prefix** - Data isolation risk

### P1 - High (Fix in Current Sprint)

5. **Missing Service Layer** (when other features access)
6. **DAL Without RepositoryResult** - Inconsistent error handling
7. **Fat Server Actions (>50 lines)** - Business logic leaking
8. **DAL Exports in index.ts** - Boundaries violated
9. **Next.js Imports in DAL/Service** - Runtime coupling

### P2 - Medium (Fix Soon)

10. **Missing Tests for DAL** - Coverage gaps
11. **Services Without JSDoc** - Documentation gaps
12. **Inconsistent Naming** (snake_case DAL, kebab-case actions)
13. **Missing Zod Schemas** - Validation gaps

### P3 - Low (Nice to Have)

14. **Missing Logging in DAL** - Observability gaps
15. **No Error Codes** - Debugging harder
16. **Missing Type Exports** - Consumer experience

## Detection Commands Summary

### Run All Critical Checks

```bash
#!/bin/bash
# architecture-check.sh

echo "========================================"
echo "Architecture Compliance Check"
echo "========================================"

FAILED=0

# P0: Cross-feature DAL imports
echo -e "\n[P0] Cross-Feature DAL Imports..."
VIOLATIONS=$(grep -r "from '@/features/" src/features/ 2>/dev/null | \
  grep "/dal'" | \
  awk -F: '{
    match($1, /features\/([^/]+)/, feat);
    match($2, /features\/([^/]+)\/dal/, imported);
    if (feat[1] != imported[1] && imported[1] != "") {
      print "  " $1
    }
  }')
if [ ! -z "$VIOLATIONS" ]; then
  echo "FAIL: Cross-feature DAL imports found:"
  echo "$VIOLATIONS"
  FAILED=1
else
  echo "PASS"
fi

# P0: 'server-only' in DAL
echo -e "\n[P0] 'server-only' in DAL..."
SERVER_ONLY=$(grep -l "server-only" src/features/*/dal/*.ts 2>/dev/null)
if [ ! -z "$SERVER_ONLY" ]; then
  echo "FAIL: 'server-only' found in DAL:"
  echo "$SERVER_ONLY"
  FAILED=1
else
  echo "PASS"
fi

# P0: Cross-feature DAL in tests
echo -e "\n[P0] Cross-Feature DAL in Tests..."
TEST_VIOLATIONS=$(grep -r "from '@/features/" src/features/**/*.test.ts 2>/dev/null | \
  grep "/dal'" | \
  awk -F: '{
    match($1, /features\/([^/]+)/, feat);
    match($2, /features\/([^/]+)\/dal/, imported);
    if (feat[1] != imported[1] && imported[1] != "") {
      print "  " $1
    }
  }')
if [ ! -z "$TEST_VIOLATIONS" ]; then
  echo "FAIL: Cross-feature DAL imports in tests:"
  echo "$TEST_VIOLATIONS"
  FAILED=1
else
  echo "PASS"
fi

# P1: DAL exports in index.ts
echo -e "\n[P1] DAL Exports in index.ts..."
DAL_EXPORTS=$(grep -l "from.*dal" src/features/*/index.ts 2>/dev/null)
if [ ! -z "$DAL_EXPORTS" ]; then
  echo "WARNING: DAL exported in index.ts:"
  echo "$DAL_EXPORTS"
else
  echo "PASS"
fi

# P1: RepositoryResult pattern
echo -e "\n[P1] RepositoryResult Pattern..."
NO_RESULT=$(grep -L "RepositoryResult" src/features/*/dal/*.ts 2>/dev/null | grep -v test | grep -v index)
if [ ! -z "$NO_RESULT" ]; then
  echo "WARNING: DAL files without RepositoryResult:"
  echo "$NO_RESULT"
else
  echo "PASS"
fi

# P1: Service layer check
echo -e "\n[P1] Service Layer Coverage..."
for dir in src/features/*/; do
  name=$(basename $dir)
  external_imports=$(grep -r "from '@/features/$name'" src/features/ 2>/dev/null | grep -v "src/features/$name" | wc -l | tr -d ' ')
  if [ "$external_imports" -gt 0 ]; then
    if [ ! -d "${dir}service" ]; then
      echo "WARNING: $name has $external_imports external imports but no service layer"
    fi
  fi
done
echo "DONE"

# Summary
echo -e "\n========================================"
if [ $FAILED -eq 1 ]; then
  echo "RESULT: FAILED - Critical violations found"
  exit 1
else
  echo "RESULT: PASSED - No critical violations"
  exit 0
fi
```

## CI/CD Integration

### GitHub Actions Workflow

```yaml
name: Architecture Compliance

on: [push, pull_request]

jobs:
  compliance-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: P0 - Cross-Feature DAL Imports
        run: |
          VIOLATIONS=$(grep -r "from '@/features/" src/features/ 2>/dev/null | \
            grep "/dal'" | \
            awk -F: '{
              match($1, /features\/([^/]+)/, feat);
              match($2, /features\/([^/]+)\/dal/, imported);
              if (feat[1] != imported[1] && imported[1] != "") {
                print $1
              }
            }')
          if [ ! -z "$VIOLATIONS" ]; then
            echo "Cross-feature DAL imports found:"
            echo "$VIOLATIONS"
            exit 1
          fi
          echo "No cross-feature DAL imports"

      - name: P0 - server-only in DAL
        run: |
          SERVER_ONLY=$(grep -l "server-only" src/features/*/dal/*.ts 2>/dev/null || true)
          if [ ! -z "$SERVER_ONLY" ]; then
            echo "'server-only' found in DAL:"
            echo "$SERVER_ONLY"
            exit 1
          fi
          echo "No 'server-only' in DAL"

      - name: P0 - Cross-Feature DAL in Tests
        run: |
          VIOLATIONS=$(grep -r "from '@/features/" src/features/**/*.test.ts 2>/dev/null | \
            grep "/dal'" | \
            awk -F: '{
              match($1, /features\/([^/]+)/, feat);
              match($2, /features\/([^/]+)\/dal/, imported);
              if (feat[1] != imported[1] && imported[1] != "") {
                print $1
              }
            }' || true)
          if [ ! -z "$VIOLATIONS" ]; then
            echo "Cross-feature DAL in tests:"
            echo "$VIOLATIONS"
            exit 1
          fi
          echo "No cross-feature DAL in tests"

      - name: P1 - RepositoryResult Pattern
        run: |
          NO_RESULT=$(grep -L "RepositoryResult" src/features/*/dal/*.ts 2>/dev/null | grep -v test | grep -v index || true)
          if [ ! -z "$NO_RESULT" ]; then
            echo "DAL files without RepositoryResult:"
            echo "$NO_RESULT"
            echo "::warning::Some DAL files missing RepositoryResult pattern"
          fi

      - name: Run Tests
        run: npx vitest run
```

### Pre-Commit Hook

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
set -e

echo "Running Architecture Compliance Checks..."

# P0: Cross-feature DAL imports
VIOLATIONS=$(grep -r "from '@/features/" src/features/ 2>/dev/null | \
  grep "/dal'" | \
  awk -F: '{
    match($1, /features\/([^/]+)/, feat);
    match($2, /features\/([^/]+)\/dal/, imported);
    if (feat[1] != imported[1] && imported[1] != "") { print $1 }
  }')
if [ ! -z "$VIOLATIONS" ]; then
  echo "BLOCKED: Cross-feature DAL imports found"
  echo "$VIOLATIONS"
  exit 1
fi

# P0: 'server-only' in DAL
SERVER_ONLY=$(grep -l "server-only" src/features/*/dal/*.ts 2>/dev/null || true)
if [ ! -z "$SERVER_ONLY" ]; then
  echo "BLOCKED: 'server-only' in DAL"
  echo "$SERVER_ONLY"
  exit 1
fi

echo "Architecture checks passed"
```

## Maturity Level Definitions

### Immature (0-40/100)
- Critical principle violations
- Cross-feature DAL imports
- No service layers
- `'server-only'` in DAL
- Multiple P0 issues

### Developing (41-65/100)
- Some boundaries defined
- Partial service layer coverage
- Some DAL functions missing RepositoryResult
- Can deploy with monitoring

### Mature (66-85/100)
- Strong boundaries
- Service layers where needed
- RepositoryResult throughout
- Runtime-agnostic DAL
- Good test coverage

### Advanced (86-100/100)
- Excellent compliance
- Best practices throughout
- Zero critical violations
- Full test coverage
- Only optimization opportunities

## Best Practices

1. **Be Thorough**: Check every feature, don't skip any
2. **Be Specific**: Always provide file paths for violations
3. **Be Actionable**: Every violation needs a clear fix
4. **Be Evidence-Based**: Back claims with detection command output
5. **Prioritize Correctly**: P0 violations are always blockers
6. **Reference Documentation**: Link to specific doc sections for each finding
7. **Run All Commands**: Don't skip detection commands

## Notes

- Always prioritize State Isolation (Principle 8) as it's the most critical
- Detection commands are mandatory, not optional
- Every finding must reference specific documentation
- Be constructive: show both the problem AND the solution
- Consider running this assessment after major refactoring or before production releases
- Cross-feature DAL imports are the #1 violation to catch

## Sample Assessment Output

```markdown
# Architecture Maturity Assessment

**Date**: 2025-01-15
**Scope**: All features in src/features/

## Executive Summary

**Overall Score**: 72/100 (Mature)
**Critical Violations**: 0
**High Priority Issues**: 3
**Medium Priority Issues**: 5

## Findings

### P0 - Critical (None)
No critical violations found.

### P1 - High Priority

1. **Missing Service Layer in `billing` feature**
   - Location: `src/features/billing/`
   - Issue: `accounts` feature imports from `billing` but no service layer exists
   - Fix: Create `src/features/billing/service/billing-service.ts`

2. **DAL Without RepositoryResult**
   - Location: `src/features/notifications/dal/send_email.ts`
   - Issue: Function throws instead of returning RepositoryResult
   - Fix: Wrap in try/catch, return RepositoryResult<void>

3. **Fat Server Action**
   - Location: `src/features/accounts/actions/create-account.ts` (78 lines)
   - Issue: Business logic in action handler
   - Fix: Extract to DAL function

### P2 - Medium Priority

1. Missing tests for `billing` DAL (0/5 coverage)
2. Missing JSDoc on `accountsService` methods
3. Inconsistent naming in `notifications/dal/SendEmail.ts` (should be snake_case)
4. Missing Zod schema for `UpdateBillingInput`
5. No error codes in `notifications` DAL errors

## Recommendations

1. **Immediate**: Create billing service layer (blocks next deployment)
2. **This Sprint**: Add RepositoryResult to notifications DAL
3. **This Sprint**: Refactor fat create-account action
4. **Next Sprint**: Add billing DAL tests
5. **Backlog**: Standardize naming conventions
```

## References

- Architecture Overview: `docs/ARCHITECTURE-OVERVIEW.md`
- State Isolation: `docs/STATE-ISOLATION.md`
- Coding Patterns: `docs/CODING-PATTERNS.md`
- DynamoDB Design: `docs/DYNAMODB-DESIGN.md`
- Testing Patterns: `docs/TESTING-PATTERNS.md`
