---
name: test-generator
description: Generates test code from specifications, components, and API endpoints. Creates unit tests, integration tests, and E2E tests following project testing patterns and conventions.
version: 1.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Glob, Grep]
best_practices:
  - Analyze existing test patterns
  - Follow project testing conventions
  - Generate comprehensive test coverage
  - Include edge cases and error scenarios
  - Use appropriate testing framework
error_handling: graceful
streaming: supported
templates: [unit-test, integration-test, e2e-test, api-test]
---

<identity>
Test Generator Skill - Generates test code from specifications, components, and API endpoints following project testing patterns and conventions.
</identity>

<capabilities>
- Generating tests for new components
- Creating tests for API endpoints
- Generating E2E tests for user flows
- Creating integration tests
- Adding test coverage for existing code
</capabilities>

<instructions>
<execution_process>

### Step 1: Identify Test Type

Determine what type of test is needed:

- **Unit Test**: Component/function testing
- **Integration Test**: Service/API integration
- **E2E Test**: Full user flow testing
- **API Test**: Endpoint testing

### Step 2: Analyze Target Code

Examine code to test (Use Parallel Read/Grep/Glob):

- Read component/function code
- Identify test cases
- Understand dependencies
- Note edge cases

### Step 3: Analyze Test Patterns

Review existing tests:

- Read similar test files
- Identify testing patterns
- Note testing framework usage
- Understand mocking strategies

### Step 4: Generate Test Code

Create test following patterns:

- Use appropriate testing framework
- Follow project conventions
- Include comprehensive coverage
- Add edge cases and error scenarios

### Step 5: Coverage Analysis

After generating tests, analyze coverage:

1. **Check that generated tests cover all requirements**:
   - Verify all functions/methods are tested
   - Check all branches are covered (if/else, switch, etc.)
   - Ensure all edge cases are tested
   - Validate error scenarios are covered

2. **Validate tests are runnable**:
   - Check test syntax is valid
   - Verify imports are correct
   - Ensure test framework is properly configured
   - Validate test setup/teardown is correct

3. **Report coverage percentage**:
   - Calculate line coverage (if possible)
   - Calculate branch coverage (if possible)
   - Report uncovered code paths
   - Suggest additional tests for uncovered areas

4. **Coverage Validation Checklist**:
   - [ ] All public functions/methods have tests
   - [ ] All error paths are tested
   - [ ] All edge cases are covered
   - [ ] Tests are syntactically valid
   - [ ] Tests can be executed successfully
   - [ ] Coverage meets project thresholds (if defined)
         </execution_process>
         </instructions>

<examples>
<code_example>
**Unit Test (React Component)**

```typescript
import { render, screen, waitFor } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import { UserProfile } from './user-profile'

describe('UserProfile', () => {
  it('renders user information', async () => {
    const mockUser = { id: '1', name: 'John', email: 'john@example.com' }

    render(<UserProfile user={mockUser} />)

    await waitFor(() => {
      expect(screen.getByText('John')).toBeInTheDocument()
      expect(screen.getByText('john@example.com')).toBeInTheDocument()
    })
  })

  it('handles loading state', () => {
    render(<UserProfile user={null} loading />)
    expect(screen.getByTestId('loading')).toBeInTheDocument()
  })

  it('handles error state', () => {
    render(<UserProfile user={null} error="Failed to load" />)
    expect(screen.getByText('Failed to load')).toBeInTheDocument()
  })
})
```

</code_example>

<code_example>
**Integration Test (API)**

```typescript
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { createTestClient } from './test-client';

describe('Users API', () => {
  let client: TestClient;

  beforeAll(() => {
    client = createTestClient();
  });

  afterAll(async () => {
    await client.cleanup();
  });

  it('creates a user', async () => {
    const response = await client.post('/api/users', {
      email: 'test@example.com',
      name: 'Test User',
    });

    expect(response.status).toBe(201);
    expect(response.data).toHaveProperty('id');
    expect(response.data.email).toBe('test@example.com');
  });

  it('validates required fields', async () => {
    const response = await client.post('/api/users', {});

    expect(response.status).toBe(400);
    expect(response.data).toHaveProperty('errors');
  });
});
```

</code_example>

<code_example>
**E2E Test (Cypress)**

```typescript
describe('User Authentication Flow', () => {
  beforeEach(() => {
    cy.visit('/login');
  });

  it('allows user to login', () => {
    cy.get('[data-testid="email-input"]').type('user@example.com');
    cy.get('[data-testid="password-input"]').type('password123');
    cy.get('[data-testid="login-button"]').click();

    cy.url().should('include', '/dashboard');
    cy.get('[data-testid="user-menu"]').should('be.visible');
  });

  it('shows error for invalid credentials', () => {
    cy.get('[data-testid="email-input"]').type('invalid@example.com');
    cy.get('[data-testid="password-input"]').type('wrong');
    cy.get('[data-testid="login-button"]').click();

    cy.get('[data-testid="error-message"]')
      .should('be.visible')
      .and('contain', 'Invalid credentials');
  });
});
```

</code_example>
</examples>

<instructions>
<integration>
**Integration with Developer Agent**:
- Generates tests during development
- Ensures test coverage
- Validates implementation

**Integration with QA Agent**:

- Creates comprehensive test suites
- Generates test plans
- Validates test quality
  </integration>

<best_practices>

1. **Follow Patterns**: Match existing test structure
2. **Comprehensive Coverage**: Test happy paths and edge cases
3. **Clear Test Names**: Descriptive test descriptions
4. **Isolate Tests**: Each test should be independent
5. **Mock Dependencies**: Use appropriate mocking strategies
   </best_practices>
   </instructions>

<examples>
<usage_example>
**Example Commands**:

```bash
# Generate tests for a file
node .claude/tools/test-generator/generate.mjs src/components/UserProfile.tsx

# The tool will analyze the file and generate appropriate tests
```

</usage_example>
</examples>

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
