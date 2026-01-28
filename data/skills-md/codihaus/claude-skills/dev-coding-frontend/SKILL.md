---
name: dev-coding-frontend
description: Frontend implementation patterns and workflows
version: 1.1.0
---

# /dev-coding-frontend - Frontend Implementation

> **Skill Awareness**: See `skills/_registry.md` for all available skills.
> - **Loaded by**: `/dev-coding` when UI work needed
> - **References**: Load tech-specific from `references/` (nextjs.md, vue.md, etc.)
> - **Before**: Backend API contract should be documented

Frontend-specific patterns for UI components, pages, and client-side logic.

## When Loaded

This skill is loaded by `/dev-coding` when:
- Spec requires UI components
- Spec requires pages/routes
- Spec requires client-side logic

## Workflow

### Step 1: Understand Frontend Requirements

From the UC spec, extract:

```markdown
## Frontend Requirements Checklist

[ ] Pages/Routes needed?
    - Path
    - Layout
    - Auth required?

[ ] Components needed?
    - New components
    - Modify existing
    - Shared vs feature-specific

[ ] State management?
    - Local state
    - Global state
    - Server state (API data)

[ ] Forms?
    - Fields
    - Validation rules
    - Submit handling

[ ] API integration?
    - Endpoints to call
    - Request/response handling
    - Loading/error states
```

### Step 2: Review API Contract

If backend was just implemented (or exists), review:

```markdown
## Available API

From backend implementation notes:

### POST /api/auth/login
- Request: `{ email, password }`
- Response: `{ token, user }`
- Errors: 400 (validation), 401 (credentials)
```

Know this BEFORE building UI to match shapes.

### Step 3: Component Architecture

**Decide component structure:**

```
Feature component structure:
src/
├── components/
│   ├── ui/              # Shared/base components
│   │   ├── Button.tsx
│   │   └── Input.tsx
│   └── features/
│       └── auth/        # Feature-specific
│           ├── LoginForm.tsx
│           └── SignupForm.tsx
├── app/ (or pages/)
│   └── login/
│       └── page.tsx     # Page that uses LoginForm
```

**Follow project conventions** (from scout):
- Where components live
- Naming pattern
- Export style

### Step 4: Build Components

**Order:** Base components → Feature components → Pages

```
1. Check if base components exist (Button, Input, etc.)
2. Create feature components
3. Create/modify pages
4. Wire up routing
```

**Component Pattern:**

```tsx
// Follow project conventions
// This is a common pattern, adapt to project

interface LoginFormProps {
  onSuccess?: (user: User) => void;
  redirectTo?: string;
}

export function LoginForm({ onSuccess, redirectTo = '/' }: LoginFormProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const result = await login(formData);
      onSuccess?.(result.user);
      router.push(redirectTo);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {error && <Alert variant="error">{error}</Alert>}
      {/* Form fields */}
      <Button type="submit" disabled={isLoading}>
        {isLoading ? 'Loading...' : 'Login'}
      </Button>
    </form>
  );
}
```

### Step 5: API Integration

**Create API client functions:**

```typescript
// lib/api/auth.ts
export async function login(credentials: LoginCredentials) {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Login failed');
  }

  return response.json();
}
```

**Handle states:**

```tsx
// Loading state
{isLoading && <Spinner />}

// Error state
{error && <Alert variant="error">{error}</Alert>}

// Empty state
{items.length === 0 && <EmptyState message="No items found" />}

// Success state
{items.map(item => <ItemCard key={item.id} item={item} />)}
```

### Step 6: Form Handling

**Validation Pattern:**

```tsx
// Client-side validation
const validateForm = (data: FormData) => {
  const errors: Record<string, string> = {};

  if (!data.email) {
    errors.email = 'Email is required';
  } else if (!isValidEmail(data.email)) {
    errors.email = 'Invalid email format';
  }

  if (!data.password) {
    errors.password = 'Password is required';
  } else if (data.password.length < 8) {
    errors.password = 'Password must be at least 8 characters';
  }

  return errors;
};

// Show errors
{errors.email && <span className="error">{errors.email}</span>}
```

**Form Libraries** (use if project has them):
- react-hook-form
- formik
- native form handling

### Step 7: Verification

**Visual verification:**

```typescript
// Option 1: Playwright screenshot
await mcp__playwright__browser_navigate({ url: 'http://localhost:3000/login' });
await mcp__playwright__browser_snapshot({});

// Option 2: Manual check
// Navigate to page in browser, verify appearance
```

**Interaction verification:**

```typescript
// Fill and submit form
await mcp__playwright__browser_type({
  element: 'email input',
  ref: 'email-input-ref',
  text: 'test@test.com'
});

await mcp__playwright__browser_click({
  element: 'submit button',
  ref: 'submit-btn-ref'
});

// Verify result
await mcp__playwright__browser_snapshot({});
```

**Verification checklist:**
```
[ ] Page renders without errors
[ ] Components display correctly
[ ] Forms validate input
[ ] Submit calls correct API
[ ] Loading states show
[ ] Errors display properly
[ ] Success redirects/updates correctly
[ ] Mobile responsive (if required)
```

## Common Patterns

### Conditional Rendering

```tsx
// Auth guard
{isAuthenticated ? <Dashboard /> : <Redirect to="/login" />}

// Loading
{isLoading ? <Spinner /> : <Content />}

// Permission
{user.canEdit && <EditButton />}
```

### Data Fetching

```tsx
// Server component (Next.js App Router)
async function PostsPage() {
  const posts = await getPosts(); // Fetches on server
  return <PostList posts={posts} />;
}

// Client component with useEffect
function PostsPage() {
  const [posts, setPosts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    getPosts().then(setPosts).finally(() => setIsLoading(false));
  }, []);

  if (isLoading) return <Spinner />;
  return <PostList posts={posts} />;
}

// With SWR/React Query
function PostsPage() {
  const { data: posts, error, isLoading } = useSWR('/api/posts', fetcher);

  if (isLoading) return <Spinner />;
  if (error) return <Error message={error.message} />;
  return <PostList posts={posts} />;
}
```

### Navigation

```tsx
// Next.js
import { useRouter } from 'next/navigation';
const router = useRouter();
router.push('/dashboard');

// React Router
import { useNavigate } from 'react-router-dom';
const navigate = useNavigate();
navigate('/dashboard');
```

### Toast/Notifications

```tsx
// Success feedback
toast.success('Saved successfully');

// Error feedback
toast.error('Failed to save. Please try again.');

// Use project's toast library (sonner, react-hot-toast, etc.)
```

## Accessibility Checklist

```
[ ] Images have alt text
[ ] Form inputs have labels
[ ] Buttons have accessible names
[ ] Color contrast sufficient
[ ] Keyboard navigation works
[ ] Focus states visible
[ ] Screen reader tested (if critical)
```

## Responsive Checklist

```
[ ] Mobile layout (< 768px)
[ ] Tablet layout (768px - 1024px)
[ ] Desktop layout (> 1024px)
[ ] Touch targets large enough (44px minimum)
[ ] No horizontal scroll on mobile
```

## Debugging

### Component Not Rendering

```bash
# Check console for errors
# Browser DevTools → Console

# Check if component imported correctly
# Check if props passed correctly
# Check conditional rendering logic
```

### API Call Failing

```bash
# Check Network tab in DevTools
# Verify URL, method, headers
# Check CORS if cross-origin
# Verify backend is running
```

### Styling Issues

```bash
# Check if styles imported
# Check class names (typos)
# Check CSS specificity
# Check for conflicting styles
# Use DevTools Elements panel
```

### Using Playwright for Debug

```typescript
// Take screenshot of current state
await mcp__playwright__browser_take_screenshot({
  filename: 'debug-screenshot.png'
});

// Check console messages
await mcp__playwright__browser_console_messages({
  level: 'error'
});

// Check network requests
await mcp__playwright__browser_network_requests({});
```

## Tech-Specific References

Load additional patterns based on detected tech:

| Tech | Reference File |
|------|---------------|
| Next.js | `references/nextjs.md` |
| Vue | `references/vue.md` |
| React | `references/react.md` |
| shadcn/ui | `references/shadcn.md` |
| Tailwind | `references/tailwind.md` |

These files contain tech-specific patterns, gotchas, and best practices. Add them as your projects use different stacks.
