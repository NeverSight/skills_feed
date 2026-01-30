---
name: writing-plans
description: Use when creating implementation plans. Mandates exact file paths, complete code samples, and expected output. No vague language allowed.
version: 1.0.0
---

# Writing Plans Skill

> **Core Principle**: Exact code in plan, not descriptions of code.

## Plan Structure

Every plan MUST follow this format:

### Header (Required)

```markdown
# Feature: [Name]

> Execute with: `orchestration` skill → `executor` subagent

**Goal**: [Single sentence describing what will be built]

**Architecture**: [2-3 sentences on how it fits into existing system]

**Stack**: [Technologies/frameworks involved]
```

---

## Task Format (Required)

Each task MUST include ALL of:

### 1. File References (Exact Paths)

```markdown
## Task N: [Descriptive Name]

**Files**:
- Create: `src/components/LoginForm.tsx`
- Modify: `src/pages/auth.tsx`
- Test: `tests/LoginForm.test.tsx`
```

### 2. Steps with Complete Code

```markdown
**Steps**:

1. Write failing test:
   ```typescript
   import { render, screen } from '@testing-library/react';
   import { LoginForm } from '../src/components/LoginForm';

   test('renders email input', () => {
     render(<LoginForm />);
     expect(screen.getByLabelText('Email')).toBeInTheDocument();
   });
   ```

2. Run test:
   ```bash
   npm test -- LoginForm.test.tsx
   ```
   Expected output:
   ```
   FAIL  tests/LoginForm.test.tsx
   ✕ renders email input
   Cannot find module '../src/components/LoginForm'
   ```

3. Implement:
   ```typescript
   export function LoginForm() {
     return (
       <form>
         <label htmlFor="email">Email</label>
         <input id="email" type="email" />
       </form>
     );
   }
   ```

4. Run test:
   ```bash
   npm test -- LoginForm.test.tsx
   ```
   Expected output:
   ```
   PASS  tests/LoginForm.test.tsx
   ✓ renders email input (42ms)
   ```

5. Commit:
   ```bash
   git add src/components/LoginForm.tsx tests/LoginForm.test.tsx
   git commit -m "feat(auth): add LoginForm component with email input"
   ```
```

---

## Forbidden Language

These phrases are NOT ALLOWED in plans:

| Forbidden | Why | Write Instead |
|-----------|-----|---------------|
| "Add validation" | Vague | Show exact validation code |
| "Update the file" | Vague | Show exact changes |
| "Handle errors" | Vague | Show error handling code |
| "Should pass" | Uncertain | Show exact expected output |
| "Similar to X" | Vague | Show actual code |
| "As needed" | Vague | Specify exactly what's needed |
| "etc." | Vague | List all items |

---

## Verification Checklist

Before finalizing a plan, verify:

- [ ] Every file has exact path
- [ ] Every code block is complete (not `// ...`)
- [ ] Every test shows expected failure message
- [ ] Every test shows expected pass message
- [ ] Every command shows expected output
- [ ] No forbidden language used

---

## Example: Good vs Bad

### Bad Plan Task
```markdown
## Task 1: Add Login Form

Create a login form component with email and password fields.
Add validation and error handling as needed.
Write tests for the component.
```

### Good Plan Task
```markdown
## Task 1: Add Login Form

**Files**:
- Create: `src/components/LoginForm.tsx`
- Test: `tests/LoginForm.test.tsx`

**Steps**:

1. Write failing test:
   ```typescript
   import { render, screen, fireEvent } from '@testing-library/react';
   import { LoginForm } from '../src/components/LoginForm';

   test('shows error when email is empty', () => {
     render(<LoginForm onSubmit={jest.fn()} />);
     fireEvent.click(screen.getByRole('button', { name: 'Login' }));
     expect(screen.getByText('Email is required')).toBeInTheDocument();
   });
   ```

2. Run test:
   ```bash
   npm test -- LoginForm.test.tsx
   ```
   Expected: FAIL - "Cannot find module"

[... continue with complete implementation ...]
```

---

## Integration with Orchestration

Plans created with this skill feed directly into:

| Downstream | How |
|------------|-----|
| `orchestration` | Tasks already decomposed |
| `executor` | Exact code provided |
| `tdd` | Tests specified first |
| `verification` | Expected output defined |

Chain: `writing-plans` → `orchestration` → `executor` → `verification`

---

## File Location

Save plans to: `docs/plans/YYYY-MM-DD-<feature-name>.md`

Example: `docs/plans/2025-01-20-login-form.md`
