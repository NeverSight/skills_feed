---
name: bug-fix
description: "Systematic workflow for verifying bug fixes to ensure quality and prevent regres..."
version: 1.0.0
tags: []
progressive_disclosure:
  entry_point:
    summary: "Systematic workflow for verifying bug fixes to ensure quality and prevent regres..."
    when_to_use: "When working with bug-fix or related functionality."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
---
# Bug Fix Verification

Systematic workflow for verifying bug fixes to ensure quality and prevent regressions.

## When to Use This Skill

Use this skill when:
- Fixing a reported bug
- Creating PR for bug fix
- Need to document bug fix verification
- Want to ensure fix doesn't introduce regressions
- Need structured approach to bug resolution

## Why Bug Fix Verification Matters

### Problems It Solves
- ❌ Fixing symptoms instead of root cause
- ❌ Introducing new bugs while fixing old ones
- ❌ Incomplete testing of edge cases
- ❌ No proof that bug is actually fixed
- ❌ Poor documentation of fix reasoning

### Benefits
- ✅ Confirms bug is truly fixed (not masked)
- ✅ Documents root cause analysis
- ✅ Prevents regression with tests
- ✅ Provides clear evidence for stakeholders
- ✅ Improves team knowledge of codebase

## Bug Fix Workflow

### Step 1: Reproduce Before Fix

**Critical**: Never fix a bug without first reproducing it.

#### Reproduction Checklist
- [ ] Document exact steps to reproduce
- [ ] Capture error message/behavior with screenshots
- [ ] Note frequency (100% reproducible, intermittent, etc.)
- [ ] Video recording if UI-related or complex interaction
- [ ] Identify affected versions/environments
- [ ] Note any workarounds users have found
- [ ] Verify bug exists in clean environment (not just local)

#### Reproduction Documentation Template
```markdown
## Bug Reproduction

### Steps to Reproduce
1. Navigate to `/dashboard`
2. Click "Export Data" button
3. Select date range: Jan 1 - Dec 31
4. Click "Generate Report"

### Expected Behavior
- Report downloads as CSV file
- File contains all transactions for date range
- Download completes in < 5 seconds

### Actual Behavior
- Error appears: "Failed to generate report"
- Console error: `TypeError: Cannot read property 'map' of undefined`
- No file downloads
- Issue occurs 100% of the time

### Environment
- Browser: Chrome 120.0.6099.109
- OS: macOS 14.2
- User Role: Admin
- Data Size: ~10,000 transactions

### Screenshots
![Error message](screenshots/export-error.png)
![Console error](screenshots/console-error.png)
```

### Step 2: Root Cause Analysis

Investigate WHY the bug occurs, not just WHAT happens.

#### Investigation Steps
1. **Review Error Logs**: Check server logs, browser console, error tracking
2. **Trace Code Path**: Follow execution from trigger point to error
3. **Identify Breaking Point**: Find exact line/function where bug occurs
4. **Understand Context**: Why does code behave this way?
5. **Check Recent Changes**: Did recent commit introduce this?
6. **Review Related Code**: Are there similar patterns elsewhere?

#### Root Cause Documentation
```markdown
## Root Cause Analysis

### Investigation
- Error occurs in `generateReport()` function at line 45
- Function assumes `transactions` array always exists
- When date range returns no results, backend returns `null`
- Frontend doesn't handle `null` case, tries to call `.map()` on `null`

### Root Cause
- Missing null check before array operations
- Backend API doesn't return consistent data structure (sometimes `[]`, sometimes `null`)
- No validation of API response shape

### Why This Wasn't Caught
- Unit tests only covered happy path (data exists)
- Integration tests didn't test empty result scenario
- Backend inconsistency not documented in API contract
```

### Step 3: Implement Fix

Fix the root cause, not the symptom.

#### Fix Guidelines
- **Minimal Change**: Fix only what's necessary
- **Defensive Coding**: Add validation/guards
- **Consistent Patterns**: Follow existing error handling patterns
- **Type Safety**: Use types to prevent similar bugs
- **Documentation**: Comment non-obvious fixes

#### Example Fix
```typescript
// BEFORE (Bug)
function generateReport(transactions) {
  return transactions.map(t => ({
    date: t.date,
    amount: t.amount,
  }));
}

// AFTER (Fixed)
function generateReport(transactions) {
  // Guard against null/undefined from backend
  if (!transactions || !Array.isArray(transactions)) {
    console.warn('No transactions to export');
    return [];
  }

  return transactions.map(t => ({
    date: t.date,
    amount: t.amount,
  }));
}
```

### Step 4: Verify Fix

Prove the bug is fixed through systematic testing.

#### Verification Checklist
- [ ] Follow same reproduction steps
- [ ] Confirm bug no longer occurs
- [ ] Test edge cases around the fix
- [ ] Verify no new errors introduced
- [ ] Check fix works across environments (dev, staging)
- [ ] Validate fix matches expected behavior

#### Verification Documentation
```markdown
## Fix Verification

### Testing Performed
1. ✅ Followed original reproduction steps - bug no longer occurs
2. ✅ Tested with empty date range - shows "No data to export" message
3. ✅ Tested with valid date range - exports successfully
4. ✅ Tested with large dataset (50k+ transactions) - works correctly
5. ✅ Tested in Chrome, Firefox, Safari - all working
6. ✅ Tested on staging environment - fix confirmed

### Edge Cases Tested
- Empty result set → Shows appropriate message
- Null response from API → Handled gracefully
- Single transaction → Exports correctly
- Malformed transaction data → Logs error, doesn't crash

### No New Issues
- ✅ No console errors
- ✅ No memory leaks
- ✅ No performance degradation
- ✅ Other export features still work
```

### Step 5: Add Tests to Prevent Regression

**Critical**: Every bug fix must include tests.

#### Test Requirements
- [ ] Test that reproduces original bug (should pass after fix)
- [ ] Tests for edge cases discovered during investigation
- [ ] Integration test if bug involved multiple components
- [ ] Update existing tests if they need to handle new scenarios

#### Example Tests
```typescript
describe('generateReport', () => {
  // Test that reproduces original bug
  it('should handle null transactions gracefully', () => {
    const result = generateReport(null);
    expect(result).toEqual([]);
    expect(console.warn).toHaveBeenCalledWith('No transactions to export');
  });

  // Edge cases
  it('should handle undefined transactions', () => {
    const result = generateReport(undefined);
    expect(result).toEqual([]);
  });

  it('should handle empty array', () => {
    const result = generateReport([]);
    expect(result).toEqual([]);
  });

  it('should handle single transaction', () => {
    const transactions = [{ date: '2025-01-01', amount: 100 }];
    const result = generateReport(transactions);
    expect(result).toHaveLength(1);
    expect(result[0]).toEqual({ date: '2025-01-01', amount: 100 });
  });

  // Original happy path (should still work)
  it('should transform multiple transactions correctly', () => {
    const transactions = [
      { date: '2025-01-01', amount: 100 },
      { date: '2025-01-02', amount: 200 },
    ];
    const result = generateReport(transactions);
    expect(result).toHaveLength(2);
  });
});
```

### Step 6: Document in PR

Comprehensive PR description for bug fixes.

#### PR Template for Bug Fixes
```markdown
## Bug Fix: [Brief Description]

**Ticket**: #123 / ENG-456 / JIRA-789

### Problem
[Clear description of the bug]

### Reproduction Steps (Before Fix)
1. [Step 1]
2. [Step 2]
3. [Error occurs]

**Expected**: [What should happen]
**Actual**: [What happened instead]

### Root Cause
[Detailed explanation of why bug occurred]

- Where: `src/utils/report.ts`, line 45
- Why: Null check missing before array operation
- Impact: Affects all users trying to export with empty date ranges

### Solution
[Explanation of how fix works]

- Added null/undefined check before array operations
- Return empty array instead of crashing
- Added user-facing warning message
- Updated API response handling to be more defensive

### Fix Verification (After)
1. ✅ Followed reproduction steps - bug no longer occurs
2. ✅ Tested edge cases (null, undefined, empty array)
3. ✅ Tested across browsers (Chrome, Firefox, Safari)
4. ✅ Verified on staging environment
5. ✅ No new console errors or warnings

### Test Coverage
- Added unit tests for null/undefined handling
- Added tests for empty array edge case
- Updated integration tests for export feature
- All existing tests still passing

**Coverage**: +15 lines covered, 0 lines uncovered

### Regression Prevention
- [x] Tests added that would catch this bug if reintroduced
- [x] Similar patterns checked in codebase (found 2, fixed in this PR)
- [x] Documentation updated to note API response inconsistency

### Screenshots/Evidence
**Before (Bug)**:
![Error state](screenshots/before-error.png)

**After (Fixed)**:
![Success state](screenshots/after-success.png)
![Empty state](screenshots/after-empty.png)

### Deployment Notes
- No migrations required
- No environment variable changes
- Safe to deploy immediately
- Rollback: Revert this commit

### Related Issues
- Closes #123
- Related to #456 (similar null handling issue)
```

## Common Pitfalls to Avoid

### During Investigation
- ❌ Assuming you know the cause without verifying
- ❌ Fixing symptoms instead of root cause
- ❌ Not checking if similar bugs exist elsewhere
- ❌ Skipping reproduction in clean environment

### During Implementation
- ❌ Making changes beyond fixing the bug
- ❌ Refactoring unrelated code in bug fix PR
- ❌ Adding features while fixing bugs
- ❌ Not handling all edge cases discovered

### During Verification
- ❌ Only testing happy path after fix
- ❌ Not testing in multiple environments
- ❌ Skipping regression testing
- ❌ Not documenting what was tested

### During Documentation
- ❌ Vague PR descriptions ("Fixed bug")
- ❌ Not explaining root cause
- ❌ Missing before/after evidence
- ❌ Not linking to original bug report

## Bug Fix Quality Standards

### Minimum Requirements
- ✅ Root cause identified and documented
- ✅ Fix is minimal and targeted
- ✅ Tests added to prevent regression
- ✅ Verification documented with evidence
- ✅ No new bugs introduced
- ✅ Works across all supported environments

### Excellence Indicators
- ✅ Similar patterns checked and fixed
- ✅ Multiple edge cases tested
- ✅ Performance impact measured
- ✅ Team knowledge shared (wiki/docs updated)
- ✅ Preventive measures suggested

## Automation Support

### Bug Fix PR Template

Create `.github/PULL_REQUEST_TEMPLATE/bug_fix.md`:
```markdown
## Bug Fix

**Ticket**: [Ticket number/link]

### Problem
[Description of bug]

### Reproduction Steps (Before Fix)
1.
2.
3.

**Expected**:
**Actual**:

### Root Cause
[Explanation of why bug occurred]

### Solution
[How fix works]

### Verification (After)
- [ ] Original reproduction steps no longer trigger bug
- [ ] Edge cases tested
- [ ] Tested in multiple browsers/environments
- [ ] No new errors or warnings

### Test Coverage
- [ ] Tests added for bug scenario
- [ ] Tests added for edge cases
- [ ] All existing tests passing

### Screenshots
**Before**: [Screenshot]
**After**: [Screenshot]
```

### GitHub Actions for Bug Fix PRs

```yaml
name: Bug Fix Verification
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  verify-bug-fix:
    if: contains(github.event.pull_request.labels.*.name, 'bug')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check PR description
        run: |
          PR_BODY="${{ github.event.pull_request.body }}"
          if [[ ! "$PR_BODY" =~ "Root Cause" ]]; then
            echo "::error::Bug fix PR must document root cause"
            exit 1
          fi
          if [[ ! "$PR_BODY" =~ "Verification" ]]; then
            echo "::error::Bug fix PR must document verification steps"
            exit 1
          fi

      - name: Run tests
        run: npm test

      - name: Check test coverage
        run: |
          COVERAGE=$(npm test -- --coverage --json | jq '.total.lines.pct')
          if (( $(echo "$COVERAGE < 90" | bc -l) )); then
            echo "::warning::Test coverage is below 90%"
          fi
```

## Success Criteria

### Bug Fix is Complete When
- ✅ Bug can no longer be reproduced
- ✅ Root cause is understood and documented
- ✅ Fix is minimal and targeted
- ✅ Tests prevent regression
- ✅ Edge cases are handled
- ✅ Works in all environments
- ✅ PR documentation is comprehensive
- ✅ No new issues introduced

## Related Skills

- `universal-verification-pre-merge` - Pre-merge verification checklist
- `universal-verification-screenshot` - Visual verification for UI bugs
- `universal-debugging-systematic-debugging` - Systematic debugging methodology
- `universal-debugging-root-cause-tracing` - Root cause analysis techniques
- `universal-testing-testing-anti-patterns` - Testing patterns to avoid
