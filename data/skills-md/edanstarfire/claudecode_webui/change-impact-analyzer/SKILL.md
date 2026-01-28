---
name: change-impact-analyzer
description: Determine what needs modification and identify potential side effects of changes. Use before implementing changes to understand full scope and prevent breaking existing functionality.
---

# Change Impact Analyzer

## Instructions

### When to Invoke This Skill
- Before implementing feature or fix
- Planning refactoring work
- Assessing risk of changes
- Estimating scope of work
- Identifying test requirements
- Preventing regression bugs

### Analysis Framework

#### 1. Direct Impact
**What is directly changed?**
- Files being modified
- Functions being changed
- Classes being updated
- Data structures being altered

#### 2. Ripple Impact
**What depends on direct changes?**
- Callers of modified functions
- Users of modified classes
- Consumers of changed data
- Components using modified APIs

#### 3. Side Effects
**What might break?**
- Existing functionality
- Tests that check old behavior
- Documentation that's now outdated
- Assumptions in other code

#### 4. Integration Points
**What external systems are affected?**
- API contracts
- Database schema
- Frontend-backend interface
- External services
- Configuration files

### Analysis Workflow

#### Step 1: Identify Change Scope

**Questions to Answer:**
1. What files will be modified?
2. What functions/classes will change?
3. What's the nature of change? (add/modify/delete)
4. Is this breaking or non-breaking?

**Tools to Use:**
- `Grep` to find related code
- `Glob` to find related files
- `Read` to understand current implementation

#### Step 2: Find Direct Dependencies

**For Functions:**
```bash
# Find who calls this function
grep "<function_name>(" **/*.py
```

**For Classes:**
```bash
# Find who instantiates this class
grep "<ClassName>(" **/*.py

# Find who inherits from this class
grep "class .*(.*<ClassName>" **/*.py
```

**For Data Structures:**
```bash
# Find who accesses this field
grep "\.<field_name>" **/*.py
grep '\["<field_name>"\]' **/*.py
```

**For API Endpoints:**
```bash
# Find frontend code that calls this endpoint
grep "/api/<endpoint>" frontend/**/*.js
grep "/api/<endpoint>" frontend/**/*.vue
```

#### Step 3: Trace Indirect Dependencies

**Follow the Chain:**
1. Find what depends on your change
2. Find what depends on those dependencies
3. Continue until no new dependencies
4. Identify critical paths

**Example:**
```
Change: Modify SessionInfo dataclass
  ↓
Direct: SessionManager uses SessionInfo
  ↓
Indirect: SessionCoordinator uses SessionManager
  ↓
Indirect: WebServer calls SessionCoordinator
  ↓
Indirect: Frontend expects certain SessionInfo structure
```

#### Step 4: Identify Breaking Changes

**Breaking Changes Are:**
- Removing public methods/functions
- Changing function signatures
- Modifying API response structure
- Changing data types
- Removing fields from data structures
- Altering behavior that others rely on

**Non-Breaking Changes Are:**
- Adding new optional parameters (with defaults)
- Adding new methods
- Adding new API endpoints
- Adding optional fields to data structures
- Internal refactoring without interface changes

#### Step 5: Assess Test Impact

**What Tests Need Updates?**
```bash
# Find tests for the area
grep -r "<component_name>" **/test_*.py
grep -r "<function_name>" **/test_*.py
```

**Test Categories:**
- **Update Required**: Tests checking old behavior
- **New Tests Needed**: Tests for new functionality
- **Regression Tests**: Prevent breaking existing features
- **Integration Tests**: Verify components still work together

#### Step 6: Check Documentation Impact

**What Docs Need Updates?**
- README files
- API documentation
- Code comments
- CLAUDE.md (project instructions)
- User guides

**Find Relevant Docs:**
```bash
**/*.md
**/*README*
docs/**/*
```

### Risk Assessment Matrix

| Factor | Low Risk | Medium Risk | High Risk |
|--------|----------|-------------|-----------|
| **Scope** | Single file | Multiple files | Cross-cutting |
| **Usage** | Internal only | Within module | Public API |
| **Callers** | 1-2 places | 3-10 places | 10+ places |
| **Tests** | Full coverage | Partial coverage | No tests |
| **Complexity** | Simple logic | Moderate logic | Complex logic |
| **Breaking** | Non-breaking | Breaking with migration | Breaking without migration |

### Impact Analysis Template

```markdown
## Impact Analysis: <Change Description>

### Direct Changes
**Files Modified:**
- `path/to/file.py` - <what's changing>
- `path/to/other.js` - <what's changing>

**Functions/Classes Modified:**
- `function_name()` - <how it changes>
- `ClassName` - <how it changes>

**Nature of Change:**
- [ ] Addition (new functionality)
- [ ] Modification (change existing)
- [ ] Deletion (remove functionality)
- [ ] Refactoring (no behavior change)

**Breaking Change:**
- [ ] Yes - Requires updates elsewhere
- [ ] No - Backward compatible

### Ripple Effects

**Direct Dependencies:** (code that calls modified code)
- `component_a.py:123` - Calls `modified_function()`
- `component_b.vue:45` - Uses modified API endpoint

**Indirect Dependencies:** (code that depends on direct dependencies)
- `coordinator.py` - Orchestrates component_a
- `App.vue` - Contains component_b

**Integration Points:**
- [ ] API contracts - <affected endpoints>
- [ ] Database schema - <affected tables>
- [ ] Frontend-backend interface - <affected messages>
- [ ] Configuration - <affected settings>

### Side Effects

**Potential Issues:**
- <What might break?>
- <What assumptions are invalidated?>
- <What edge cases emerge?>

**Mitigation:**
- <How to prevent each issue?>

### Test Impact

**Tests Requiring Updates:**
- `test_component.py::test_old_behavior` - Now invalid
- `test_integration.py::test_api` - Response format changed

**New Tests Needed:**
- Test new functionality
- Test edge cases
- Regression tests for side effects

**Test Coverage:**
- Current: <percentage or assessment>
- After Change: <expected coverage>

### Documentation Impact

**Docs Requiring Updates:**
- [ ] README.md - <what section>
- [ ] API documentation - <what endpoints>
- [ ] CLAUDE.md - <what instructions>
- [ ] Code comments - <where>

### Risk Assessment

**Overall Risk:** [Low / Medium / High]

**Risk Factors:**
- Scope: <single file / multiple files / cross-cutting>
- Usage: <internal / module / public API>
- Callers: <count>
- Tests: <coverage level>
- Complexity: <simple / moderate / complex>

**Rollback Plan:**
- <How to undo if issues arise>

### Implementation Strategy

**Recommended Approach:**
1. <Step-by-step plan considering impact>
2. <Testing at each step>
3. <Validation before proceeding>

**Alternative Approach (if high risk):**
- <Feature flag approach?>
- <Incremental rollout?>
- <Parallel implementation?>
```

## Examples

### Example 1: Low-risk change
```
Change: Add new optional parameter to create_session()

Impact Analysis:
- Direct: session_coordinator.py, session_manager.py
- Dependencies: web_server.py calls create_session()
- Breaking: NO - parameter has default value
- Tests: Add test for new parameter
- Risk: LOW - backward compatible, single code path

Recommendation: Safe to proceed, minimal impact
```

### Example 2: Medium-risk change
```
Change: Modify SessionInfo dataclass (add new required field)

Impact Analysis:
- Direct: session_manager.py defines SessionInfo
- Dependencies:
  * session_coordinator.py uses SessionInfo
  * web_server.py serializes SessionInfo
  * data_storage.py persists SessionInfo
  * Frontend expects SessionInfo structure
- Breaking: YES - requires default value or migration
- Tests: Update all tests creating SessionInfo
- Risk: MEDIUM - multiple callers, needs coordination

Recommendation:
1. Add field with default value (backward compatible)
2. Update all creation sites to provide value
3. Remove default after migration complete
```

### Example 3: High-risk change
```
Change: Refactor message processing (extract handlers)

Impact Analysis:
- Direct: message_parser.py (complete rewrite)
- Dependencies:
  * session_coordinator.py processes all messages
  * claude_sdk.py calls message processor
  * data_storage.py expects certain format
  * Frontend displays processed messages
- Breaking: NO - interface stays same, internals change
- Tests: Comprehensive test coverage required
- Risk: HIGH - central component, many dependencies

Recommendation:
1. Add full test coverage FIRST
2. Refactor with tests passing at each step
3. No behavior changes
4. Manual testing of all message types
```

### Example 4: API endpoint change
```
Change: Modify /api/sessions/<id>/start response format

Impact Analysis:
- Direct: web_server.py endpoint
- Dependencies:
  * Frontend SessionView component
  * Any external API consumers
- Breaking: YES - response structure changes
- Integration: Frontend-backend contract
- Tests: Update API tests, frontend tests
- Risk: HIGH - public API, breaking change

Recommendation:
1. Version the API (/api/v2/sessions/...)
2. Deprecate old endpoint
3. Update frontend to use new endpoint
4. Eventually remove old endpoint
OR
1. Make change backward compatible (include both formats)
2. Update frontend
3. Remove old format
```

### Example 5: Database schema change
```
Change: Add new column to sessions table

Impact Analysis:
- Direct: Database schema, session_manager.py
- Dependencies:
  * data_storage.py reads/writes sessions
  * All session operations
- Breaking: Depends on implementation
- Migration: Required for existing databases
- Tests: Test with new column, test migration
- Risk: MEDIUM-HIGH - data integrity critical

Recommendation:
1. Create migration script (add column with default)
2. Update code to populate new column
3. Test migration on test database
4. Verify all existing operations still work
5. Document rollback procedure
```
