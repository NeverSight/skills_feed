---
name: implement-feature
description: High-level orchestrator skill for implementing and validating new features end-to-end in the Fake Survey Generator. This skill guides the agent through the complete workflow of analyzing requirements, implementing changes, building, testing, starting the application, and validating features work correctly.
---

# Implement Feature Skill

Use this skill to implement a new feature end-to-end with complete validation from code changes through interactive E2E testing.

## What This Skill Does

This is an orchestrator skill that sequences the following steps:

1. **Analyze Requirements** - Understand the feature request and identify affected components
2. **Implement Changes** - Generate code changes across backend/frontend as needed
3. **Build Backend** - Compile .NET backend projects
4. **Build Frontend** - Compile TypeScript/React frontend
5. **Run Tests** - Execute unit and integration tests to validate logic
6. **Start Aspire Runtime** - Spin up the complete application environment
7. **Validate E2E** - Execute feature-specific happy-path validation in running UI
8. **Report Results** - Document validation outcomes (success/failure)

This orchestrator halts at the first failure and reports details to the user for remediation.

## When to Use

Use this skill when:
- Implementing a new feature from requirements to completion
- Need end-to-end validation that feature works correctly
- Want a guided, checkpoint-based development workflow
- Need to track progress through multiple validation stages

## How the Agent Should Use This Skill

### Phase 1: Requirements Analysis

**Input**: Feature requirement or story from the user

**Agent Task**:
1. Analyze the feature request to understand:
   - What user-facing behavior is expected?
   - What components need changes (Frontend, API, Application logic)?
   - What data/models are involved?
   - What happy-path user journey should be validated?
   
2. Document your understanding:
   - Affected backend services (Api, Application, Worker)
   - Frontend components to modify (React components, pages)
   - Database changes needed (new entities, migrations)
   - API endpoints to create or modify
   - Happy-path validation flow (e.g., "user clicks button → form displays → data saved → list updated")

3. **Checkpoint**: Confirm understanding with user before proceeding to implementation

**Example Analysis**:
```
Feature: Change survey creation button to purple
Analysis:
- Frontend Component: `src/client/frontend/src/components/SurveyList.tsx` (button styling)
- Backend Changes: None required
- Happy-Path: Navigate to survey list → verify button is purple
```

### Phase 2: Implementation

**Agent Task**:
1. Implement backend changes (if any):
   - Create/modify API endpoints in `src/server/FakeSurveyGenerator.Api/`
   - Create/modify business logic in `src/server/FakeSurveyGenerator.Application/`
   - Create/modify domain models as needed
   - Add/update database migrations if schema changes

2. Implement frontend changes (if any):
   - Modify React components in `src/client/frontend/src/`
   - Update types/interfaces for new API contracts
   - Update UI styling/layout as needed
   - Handle new validation/error scenarios

3. Add/Update Tests:
   - Unit tests in `src/server/FakeSurveyGenerator.Application.Tests/`
   - Integration tests in `src/server/FakeSurveyGenerator.Api.Tests.Integration/`
   - Aim for coverage of happy-path and edge cases

4. **Checkpoint**: Review changes are complete before proceeding to validation

**Implementation Checklist**:
- [ ] Backend logic implemented (if needed)
- [ ] Frontend UI updated (if needed)
- [ ] Tests written for new logic
- [ ] No syntax errors in code
- [ ] Dependencies updated if needed (NuGet, npm)

### Phase 3: Build Validation

**Agent Task**: Invoke Build Backend Skill
```
Invoke: build-backend skill
Expected: Exit code 0, no compilation errors
On Failure: Report compilation errors to user, stop
```

**Agent Task**: Invoke Build Frontend Skill
```
Invoke: build-frontend skill
Expected: Exit code 0, no TypeScript errors
On Failure: Report build errors to user, stop
```

### Phase 4: Test Validation

**Agent Task**: Invoke Test Backend Units Skill
```
Invoke: test-backend-units skill
Expected: All tests pass, exit code 0
On Failure: Report failed test names and assertions, stop
```

**Checkpoint**: All tests must pass before proceeding to E2E

### Phase 5: Runtime Validation

**Agent Task**: Invoke Validate Aspire Runtime Skill
```
Invoke: validate-aspire-runtime skill
Expected: All resources healthy, UI endpoint discovered
Steps:
1. Run `aspire run` command in a terminal
2. Use Aspire MCP list_resources tool to monitor health
3. Wait for all resources (sql, cache, api, worker, ui) to be healthy
4. Extract UI endpoint URL (typically https://localhost:3000)
5. Report endpoint to next skill

On Failure: Report which resource failed to start, stop
```

**Important**: Leave Aspire running after this step; it's needed for E2E validation

### Phase 6: E2E Validation

**Agent Task**: Invoke Validate E2E Skill
```
Invoke: validate-e2e skill
Context Provided to E2E Skill:
- UI endpoint URL from Aspire runtime
- Feature requirements/happy-path flow from Phase 1

E2E Skill Execution:
1. Use Playwright MCP to navigate UI
2. Execute feature-specific validation steps
3. Verify expected state changes and behavior
4. Report pass/fail with evidence

Expected: All validations pass
On Failure: Report specific validation failures, stop
```

### Phase 7: Results & Cleanup

**Success Path** ✅:
1. Report to user: "Feature implementation validated successfully!"
2. Provide summary:
   - Builds: Passed ✅
   - Tests: N tests passed ✅
   - E2E Validation: Feature working as expected ✅
3. User can stop Aspire (Ctrl+C) when ready

**Failure Path** ❌:
1. Report to user: "Validation failed at [specific stage]"
2. Provide details:
   - Stage: [Build/Test/Runtime/E2E]
   - Error: [specific error details]
   - Recommendation: [fix guidance if applicable]
3. User must fix issues and re-run validation from failing stage

## Checkpoint & Halt Strategy

The orchestrator uses the following halt behavior:

| Stage                 | Halt Condition                | Action                           |
| --------------------- | ----------------------------- | -------------------------------- |
| Requirements Analysis | N/A                           | Confirm understanding            |
| Implementation        | User indicates incomplete     | Halt, ask for completion         |
| Backend Build         | Exit code ≠ 0                 | Halt, report compilation errors  |
| Frontend Build        | Exit code ≠ 0                 | Halt, report build errors        |
| Backend Tests         | Any test fails                | Halt, report test failures       |
| Aspire Runtime        | Resources don't reach healthy | Halt, report startup error       |
| E2E Validation        | Assertions fail               | Halt, report validation failures |
| Success               | All stages pass               | Complete ✅                       |

## Typical Feature Implementation Timeline

1. **Analysis** - 5-10 minutes
2. **Implementation** - 15-60 minutes (depends on feature complexity)
3. **Builds** - 1-2 minutes
4. **Tests** - 1-3 minutes
5. **Aspire Startup** - 2-5 minutes (first run slower)
6. **E2E Validation** - 2-10 minutes
7. **Total** - 30-90 minutes end-to-end

## Common Feature Types & Implementation Patterns

### Type: New API Endpoint
- **Backend Changes**: Create DTO, handler, controller action
- **Frontend Changes**: Create API client call, UI components
- **Tests**: Unit test handler logic, integration test endpoint

### Type: Frontend UI Component Change
- **Backend Changes**: Usually none
- **Frontend Changes**: Modify React component, styles
- **Tests**: Snapshot tests, interaction tests in acceptance tests

### Type: Database Feature (e.g., new entity)
- **Backend Changes**: Create entity, update DbContext, add migration
- **Frontend Changes**: Add UI for new entity (if user-facing)
- **Tests**: Repository/handler tests with real database (Testcontainers)

### Type: Cross-Cutting (spans frontend + backend + database)
- **All layers**: Implement complete flow end-to-end
- **Tests**: Full integration test from API to database
- **E2E**: Happy-path user journey through complete workflow

## Reference: Available Skills

Each phase invokes a specific skill:

| Phase          | Skill Name              | Standalone Skill Location                 |
| -------------- | ----------------------- | ----------------------------------------- |
| Build Backend  | build-backend           | `.github/skills/build-backend/`           |
| Build Frontend | build-frontend          | `.github/skills/build-frontend/`          |
| Run Tests      | test-backend-units      | `.github/skills/test-backend-units/`      |
| Start Runtime  | validate-aspire-runtime | `.github/skills/validate-aspire-runtime/` |
| E2E Validation | validate-e2e            | `.github/skills/validate-e2e/`            |

For more details on each skill, see their individual SKILL.md files.

## Foundation Knowledge

Reference: **fake-survey-gen-foundation** skill for detailed project architecture, service topology, and patterns.

## Example: Complete Feature Implementation

**Scenario**: "Add ability to search surveys by title"

**Phase 1: Analysis**
```
Feature: Search surveys by title
Changes Needed:
- Backend: Add search parameter to GetSurveys API endpoint
- Frontend: Add search input box to survey list page
- Happy-Path: List surveys → type search term → verify filtered results
```

**Phase 2-4: Implement & Build**
```
- Add `searchTerm` parameter to Application service method
- Add filtering logic (e.g., LINQ .Where(s => s.Title.Contains(searchTerm)))
- Add React input field with onChange handler
- Call API with search parameter
- Write unit tests for search logic
- Write integration test for endpoint with search
- Builds pass ✅
- Tests pass ✅
```

**Phase 5: Runtime**
```
- Start aspire run
- Resources reach healthy ✅
- UI endpoint: https://localhost:3000
```

**Phase 6: E2E Validation**
```
- Navigate to https://localhost:3000
- See survey list with multiple surveys
- Type "test" in search box
- Verify only surveys with "test" in title remain
- Clear search, verify full list returns
- Validation passes ✅
```

**Result**: Feature implemented, tested, and validated end-to-end ✅
