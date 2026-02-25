---
name: refactoring
description: "Load PROACTIVELY when task involves improving code structure without changing behavior. Use when user says \"refactor this\", \"clean up this code\", \"remove dead code\", \"reduce duplication\", \"reorganize the files\", or \"extract this into a function\". Covers extract function/component, rename symbol, simplify conditionals, improve type safety, dependency inversion, dead code removal, circular dependency resolution, and database query refactoring with automated safety validation (typecheck, tests) at each step."
metadata:
  version: 1.0.0
  category: quality
  tags: [refactoring, code-quality, maintainability, type-safety, architecture, design-patterns]
---

## Resources
```
scripts/
  validate-refactoring.sh
references/
  refactoring-patterns.md
```

# Refactoring Quality Skill

This skill teaches you how to perform safe, systematic code refactoring using GoodVibes precision tools. Refactoring improves code structure and maintainability without changing external behavior, making future development faster and reducing bugs.

## When to Use This Skill

Load this skill when:
- Code duplication needs to be eliminated
- Functions or components have grown too large
- Type safety needs improvement (reducing `any` usage)
- Conditional logic has become complex and hard to follow
- File and folder structure needs reorganization
- Dependencies are tightly coupled and need inversion
- Database schema or queries need optimization
- Code smells are making development slower

Trigger phrases: "refactor this code", "reduce duplication", "extract function", "simplify conditionals", "improve types", "reorganize", "clean up code".

## Core Workflow

### Phase 1: Analyze - Understand Current State

Before refactoring, map the current code structure and identify refactoring opportunities.

#### Step 1.1: Identify Code Smells

Use `discover` to find common code smells that need refactoring.

```yaml
discover:
  queries:
    # Large files (> 300 lines)
    - id: large_files
      type: glob
      patterns: ["src/**/*.{ts,tsx,js,jsx}"]
    # Code duplication
    - id: duplicate_patterns
      type: grep
      pattern: "(function|const|class)\\s+\\w+"
      glob: "**/*.{ts,tsx,js,jsx}"
    # Type safety issues
    - id: any_usage
      type: grep
      pattern: ":\\s*any(\\s|;|,|\\))"
      glob: "**/*.{ts,tsx}"
    # Complex conditionals
    - id: nested_conditions
      type: grep
      pattern: "if\\s*\\(.*if\\s*\\("
      glob: "**/*.{ts,tsx,js,jsx}"
  verbosity: files_only
```

**What this reveals:**
- Files that need splitting
- Repeated code patterns
- Type safety gaps
- Complex conditional logic

#### Step 1.2: Understand Dependencies

Use `precision_grep` to map how code is used across the codebase.

```yaml
precision_grep:
  queries:
    - id: function_usage
      pattern: "importFunctionName\\("
      glob: "**/*.{ts,tsx,js,jsx}"
  output:
    format: locations
  verbosity: standard
```

**Why this matters:**
- Refactoring requires updating all call sites
- Breaking changes must be identified upfront
- Unused code can be safely removed

#### Step 1.3: Ensure Tests Exist

Refactoring is only safe when tests validate behavior preservation.

```yaml
discover:
  queries:
    - id: test_files
      type: glob
      patterns: ["**/*.test.{ts,tsx}", "**/*.spec.{ts,tsx}"]
    - id: source_files
      type: glob
      patterns: ["src/**/*.{ts,tsx}"]
  verbosity: files_only
```

**Critical rule:**
- If tests don't exist, write them BEFORE refactoring
- Tests act as a safety net to ensure behavior is preserved
- Run tests before and after refactoring

### Phase 2: Extract Function/Component

Large functions and components are hard to test and maintain. Extract reusable pieces.

#### Step 2.1: Identify Extraction Opportunities

Look for repeated logic or code blocks that do one thing.

```yaml
precision_read:
  files:
    - path: "src/components/UserProfile.tsx"
      extract: symbols
  verbosity: standard
```

**Extraction candidates:**
- Code blocks that do one specific task
- Logic repeated in multiple places
- Functions longer than 50 lines
- React components with multiple responsibilities

#### Step 2.2: Extract the Function

**Before (duplicated validation logic):**

```typescript
// In user-routes.ts
export async function POST(request: Request) {
  const body = await request.json();
  if (!body.email || !body.email.includes('@')) {
    return Response.json({ error: 'Invalid email' }, { status: 400 });
  }
  // ... rest of logic
}

// In profile-routes.ts
export async function PUT(request: Request) {
  const body = await request.json();
  if (!body.email || !body.email.includes('@')) {
    return Response.json({ error: 'Invalid email' }, { status: 400 });
  }
  // ... rest of logic
}
```

**After (extracted validation):**

```typescript
// lib/validation.ts
import { z } from 'zod';

export const emailSchema = z.string().email();

export function validateEmail(email: unknown): { valid: true; email: string } | { valid: false; error: string } {
  const result = emailSchema.safeParse(email);
  if (!result.success) {
    return { valid: false, error: 'Invalid email format' };
  }
  return { valid: true, email: result.data };
}

// user-routes.ts
import { validateEmail } from '@/lib/validation';

export async function POST(request: Request) {
  const body = await request.json();
  const emailResult = validateEmail(body.email);
  if (!emailResult.valid) {
    return Response.json({ error: emailResult.error }, { status: 400 });
  }
  // ... rest of logic using emailResult.email
}
```

**Use `precision_edit` to perform the extraction:**

```yaml
precision_edit:
  operations:
    - action: replace
      path: "src/api/user-routes.ts"
      old_text: |
        const body = await request.json();
        if (!body.email || !body.email.includes('@')) {
          return Response.json({ error: 'Invalid email' }, { status: 400 });
        }
      new_text: |
        const body = await request.json();
        const emailResult = validateEmail(body.email);
        if (!emailResult.valid) {
          return Response.json({ error: emailResult.error }, { status: 400 });
        }
  verbosity: minimal
```

#### Step 2.3: Extract React Components

**Before (large component with multiple responsibilities):**

```typescript
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);
  const [posts, setPosts] = useState<Post[]>([]);
  const [followers, setFollowers] = useState<User[]>([]);

  useEffect(() => {
    fetch(`/api/users/${userId}`).then(r => r.json()).then(setUser);
    fetch(`/api/users/${userId}/posts`).then(r => r.json()).then(setPosts);
    fetch(`/api/users/${userId}/followers`).then(r => r.json()).then(setFollowers);
  }, [userId]);

  if (!user) return <div>Loading...</div>;

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.bio}</p>
      
      <div>
        <h2>Posts</h2>
        {posts.map(post => (
          <div key={post.id}>
            <h3>{post.title}</h3>
            <p>{post.content}</p>
          </div>
        ))}
      </div>
      
      <div>
        <h2>Followers</h2>
        {followers.map(follower => (
          <div key={follower.id}>
            <img src={follower.avatar} alt="" />
            <span>{follower.name}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
```

**After (extracted components and hooks):**

```typescript
// hooks/useUser.ts
export function useUser(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(r => r.json())
      .then(data => {
        setUser(data);
        setLoading(false);
      });
  }, [userId]);

  return { user, loading };
}

// components/UserPosts.tsx
export function UserPosts({ userId }: { userId: string }) {
  const [posts, setPosts] = useState<Post[]>([]);

  useEffect(() => {
    fetch(`/api/users/${userId}/posts`).then(r => r.json()).then(setPosts);
  }, [userId]);

  return (
    <div>
      <h2>Posts</h2>
      {posts.map(post => (
        <PostCard key={post.id} post={post} />
      ))}
    </div>
  );
}

// components/UserFollowers.tsx
export function UserFollowers({ userId }: { userId: string }) {
  const [followers, setFollowers] = useState<User[]>([]);

  useEffect(() => {
    fetch(`/api/users/${userId}/followers`).then(r => r.json()).then(setFollowers);
  }, [userId]);

  return (
    <div>
      <h2>Followers</h2>
      {followers.map(follower => (
        <FollowerCard key={follower.id} user={follower} />
      ))}
    </div>
  );
}

// components/UserProfile.tsx
function UserProfile({ userId }: { userId: string }) {
  const { user, loading } = useUser(userId);

  if (loading || !user) return <div>Loading...</div>;

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.bio}</p>
      <UserPosts userId={userId} />
      <UserFollowers userId={userId} />
    </div>
  );
}
```

**Benefits:**
- Each component has a single responsibility
- Easier to test in isolation
- Reusable across the application
- Better performance (can memoize individual pieces)

### Phase 3: Rename and Reorganize

Poor naming and file organization slow development.

#### Step 3.1: Improve Naming

Rename variables, functions, and files to be descriptive.

**Bad naming:**

```typescript
function getData(id: string) { ... }  // Too generic
const x = getUserById(userId);  // Unclear abbreviation
let flag = true;  // What does this flag represent?
```

**Good naming:**

```typescript
function getUserProfile(userId: string) { ... }  // Specific, clear intent
const userProfile = getUserById(userId);  // Descriptive
let isEmailVerified = true;  // Boolean naming convention
```

**Use `precision_edit` with `replace_all` for renaming:**

```yaml
precision_edit:
  operations:
    - action: replace
      path: "src/lib/user.ts"
      old_text: "function getData"
      new_text: "function getUserProfile"
      replace_all: true
  verbosity: minimal
```

#### Step 3.2: Reorganize File Structure

Group related files together using feature-based or layer-based structure.

**Before (flat structure):**

```
src/
  user-routes.ts
  user-service.ts
  user-repository.ts
  post-routes.ts
  post-service.ts
  post-repository.ts
```

**After (feature-based structure):**

```
src/
  features/
    users/
      api/
        routes.ts
      services/
        user-service.ts
      repositories/
        user-repository.ts
      types/
        user.types.ts
      index.ts  # Barrel export
    posts/
      api/
        routes.ts
      services/
        post-service.ts
      repositories/
        post-repository.ts
      types/
        post.types.ts
      index.ts
```

**Benefits:**
- Related code is colocated
- Easier to find files
- Clear feature boundaries
- Barrel exports simplify imports

**Use `precision_write` to create barrel exports:**

```yaml
precision_write:
  files:
    - path: "src/features/users/index.ts"
      content: |
        export * from './types/user.types';
        export * from './services/user-service';
        export * from './repositories/user-repository';
  verbosity: minimal
```

### Phase 4: Simplify Conditionals

Nested conditionals and complex boolean logic are error-prone.

#### Step 4.1: Use Guard Clauses

**Before (nested conditionals):**

```typescript
function processOrder(order: Order) {
  if (order.status === 'pending') {
    if (order.items.length > 0) {
      if (order.paymentConfirmed) {
        // Process order
        return processPayment(order);
      } else {
        throw new Error('Payment not confirmed');
      }
    } else {
      throw new Error('Order has no items');
    }
  } else {
    throw new Error('Order is not pending');
  }
}
```

**After (guard clauses):**

```typescript
function processOrder(order: Order) {
  if (order.status !== 'pending') {
    throw new Error('Order is not pending');
  }

  if (order.items.length === 0) {
    throw new Error('Order has no items');
  }

  if (!order.paymentConfirmed) {
    throw new Error('Payment not confirmed');
  }

  return processPayment(order);
}
```

**Benefits:**
- Flat structure, easier to read
- Error conditions checked first
- Happy path is at the end

#### Step 4.2: Extract Conditionals into Named Functions

**Before (complex boolean logic):**

```typescript
if (user.role === 'admin' || (user.role === 'moderator' && user.permissions.includes('delete')) || user.id === post.authorId) {
  deletePost(post.id);
}
```

**After (named function):**

```typescript
function canDeletePost(user: User, post: Post): boolean {
  if (user.role === 'admin') return true;
  if (user.role === 'moderator' && user.permissions.includes('delete')) return true;
  if (user.id === post.authorId) return true;
  return false;
}

if (canDeletePost(user, post)) {
  deletePost(post.id);
}
```

**Benefits:**
- Self-documenting code
- Reusable logic
- Easier to test

#### Step 4.3: Use Strategy Pattern for Complex Conditionals

**Before (long switch statement):**

```typescript
function calculateShipping(order: Order): number {
  switch (order.shippingMethod) {
    case 'standard':
      return order.weight * 0.5;
    case 'express':
      return order.weight * 1.5 + 10;
    case 'overnight':
      return order.weight * 3 + 25;
    case 'international':
      return order.weight * 5 + 50;
    default:
      throw new Error('Unknown shipping method');
  }
}
```

**After (strategy pattern):**

```typescript
interface ShippingStrategy {
  calculate(weight: number): number;
}

class StandardShipping implements ShippingStrategy {
  calculate(weight: number): number {
    return weight * 0.5;
  }
}

class ExpressShipping implements ShippingStrategy {
  calculate(weight: number): number {
    return weight * 1.5 + 10;
  }
}

class OvernightShipping implements ShippingStrategy {
  calculate(weight: number): number {
    return weight * 3 + 25;
  }
}

class InternationalShipping implements ShippingStrategy {
  calculate(weight: number): number {
    return weight * 5 + 50;
  }
}

const shippingStrategies: Record<string, ShippingStrategy> = {
  standard: new StandardShipping(),
  express: new ExpressShipping(),
  overnight: new OvernightShipping(),
  international: new InternationalShipping(),
};

function calculateShipping(order: Order): number {
  const strategy = shippingStrategies[order.shippingMethod];
  if (!strategy) {
    throw new Error('Unknown shipping method');
  }
  return strategy.calculate(order.weight);
}
```

**Benefits:**
- Open/closed principle (easy to add new strategies)
- Each strategy is independently testable
- Eliminates long switch statements

### Phase 5: Type Improvements

Strong typing catches bugs at compile time.

#### Step 5.1: Eliminate `any` Types

**Find all `any` usage:**

```yaml
precision_grep:
  queries:
    - id: any_usage
      pattern: ":\\s*any(\\s|;|,|\\))"
      glob: "**/*.{ts,tsx}"
  output:
    format: locations
  verbosity: standard
```

**Before (unsafe):**

```typescript
function processData(data: any) {
  return data.value.toUpperCase();  // Runtime error if value is not a string
}
```

**After (type-safe):**

```typescript
interface DataWithValue {
  value: string;
}

function processData(data: DataWithValue): string {
  return data.value.toUpperCase();
}
```

#### Step 5.2: Use Discriminated Unions

**Before (weak typing):**

```typescript
interface ApiResponse {
  success: boolean;
  data?: User;
  error?: string;
}

function handleResponse(response: ApiResponse) {
  if (response.success) {
    console.log(response.data.name);  // TypeScript can't guarantee data exists
  }
}
```

**After (discriminated union):**

```typescript
type ApiResponse =
  | { success: true; data: User }
  | { success: false; error: string };

function handleResponse(response: ApiResponse) {
  if (response.success) {
    console.log(response.data.name);  // TypeScript knows data exists here
  } else {
    console.error(response.error);  // TypeScript knows error exists here
  }
}
```

**Benefits:**
- Exhaustive type checking
- Impossible states are impossible to represent
- Better IntelliSense

#### Step 5.3: Add Generic Constraints

**Before (too generic):**

```typescript
function getProperty<T>(obj: T, key: string) {
  return obj[key];  // Type error: no index signature
}
```

**After (proper constraints):**

```typescript
function getProperty<T extends Record<string, unknown>, K extends keyof T>(
  obj: T,
  key: K
): T[K] {
  return obj[key];
}

const user = { name: 'Alice', age: 30 };
const name = getProperty(user, 'name');  // Type is string
const age = getProperty(user, 'age');    // Type is number
```

**Benefits:**
- Type inference works correctly
- Catches invalid key access at compile time

### Phase 6: Dependency Inversion

Decouple code by depending on abstractions, not implementations.

#### Step 6.1: Extract Interfaces

**Before (tight coupling):**

```typescript
import { PrismaClient } from '@prisma/client';

class UserService {
  private prisma = new PrismaClient();

  async getUser(id: string) {
    return this.prisma.user.findUnique({ where: { id } });
  }
}
```

**After (dependency injection):**

```typescript
interface UserRepository {
  findById(id: string): Promise<User | null>;
  create(data: CreateUserInput): Promise<User>;
  update(id: string, data: UpdateUserInput): Promise<User>;
}

class PrismaUserRepository implements UserRepository {
  constructor(private prisma: PrismaClient) {}

  async findById(id: string): Promise<User | null> {
    return this.prisma.user.findUnique({ where: { id } });
  }

  async create(data: CreateUserInput): Promise<User> {
    return this.prisma.user.create({ data });
  }

  async update(id: string, data: UpdateUserInput): Promise<User> {
    return this.prisma.user.update({ where: { id }, data });
  }
}

class UserService {
  constructor(private userRepo: UserRepository) {}

  async getUser(id: string) {
    return this.userRepo.findById(id);
  }
}

// Usage
const prisma = new PrismaClient();
const userRepo = new PrismaUserRepository(prisma);
const userService = new UserService(userRepo);
```

**Benefits:**
- Easy to mock in tests (inject fake repository)
- Can swap Prisma for another ORM without changing UserService
- Clear separation of concerns

#### Step 6.2: Use Factory Pattern

**Before (hard to test):**

```typescript
function sendEmail(to: string, subject: string, body: string) {
  const client = new SendGridClient(process.env.SENDGRID_API_KEY!);  // BAD: Non-null assertion bypasses runtime validation
  client.send({ to, subject, body });
}
```

**After (factory injection):**

```typescript
interface EmailClient {
  send(email: { to: string; subject: string; body: string }): Promise<void>;
}

class SendGridEmailClient implements EmailClient {
  constructor(private apiKey: string) {}

  async send(email: { to: string; subject: string; body: string }) {
    // SendGrid implementation
  }
}

class MockEmailClient implements EmailClient {
  async send(email: { to: string; subject: string; body: string }) {
    console.log('Mock email sent:', email);
  }
}

function createEmailClient(): EmailClient {
  if (process.env.NODE_ENV === 'test') {
    return new MockEmailClient();
  }
  const apiKey = process.env.SENDGRID_API_KEY;
  if (!apiKey) {
    throw new Error('SENDGRID_API_KEY environment variable is required');
  }
  return new SendGridEmailClient(apiKey);
}

function sendEmail(client: EmailClient, to: string, subject: string, body: string) {
  return client.send({ to, subject, body });
}
```

**Benefits:**
- Tests don't send real emails
- Easy to swap email providers
- Environment-specific behavior

### Phase 7: Database Refactoring

Database schemas and queries need careful refactoring.

#### Step 7.1: Add Indexes for Performance

**Check existing schema:**

```yaml
precision_read:
  files:
    - path: "prisma/schema.prisma"
      extract: content
  verbosity: standard
```

**Before (missing indexes):**

```prisma
model Post {
  id        String   @id @default(cuid())
  title     String
  published Boolean  @default(false)
  authorId  String
  createdAt DateTime @default(now())
}
```

**After (with indexes):**

```prisma
model Post {
  id        String   @id @default(cuid())
  title     String
  published Boolean  @default(false)
  authorId  String
  createdAt DateTime @default(now())

  @@index([authorId])
  @@index([published, createdAt])
}
```

**When to add indexes:**
- Foreign keys (authorId, userId)
- Fields in WHERE clauses (published, status)
- Fields in ORDER BY (createdAt, updatedAt)
- Compound indexes for multi-column queries

#### Step 7.2: Normalize Database Schema

**Before (denormalized):**

```prisma
model Order {
  id            String @id
  customerName  String
  customerEmail String
  customerPhone String
}
```

**After (normalized):**

```prisma
model Customer {
  id     String @id
  name   String
  email  String @unique
  phone  String
  orders Order[]
}

model Order {
  id         String   @id
  customerId String
  customer   Customer @relation(fields: [customerId], references: [id])

  @@index([customerId])
}
```

**Benefits:**
- No data duplication
- Update customer info in one place
- Referential integrity

#### Step 7.3: Optimize Queries

**Before (N+1 query):**

```typescript
const posts = await prisma.post.findMany();
for (const post of posts) {
  const author = await prisma.user.findUnique({ where: { id: post.authorId } });
  console.log(`${post.title} by ${author.name}`);  // Note: Use structured logger in production
}
```

**After (eager loading):**

```typescript
const posts = await prisma.post.findMany({
  include: {
    author: true,
  },
});
for (const post of posts) {
  console.log(`${post.title} by ${post.author.name}`);  // Note: Use structured logger in production
}
```

**Use `discover` to find N+1 patterns:**

```yaml
discover:
  queries:
    - id: n_plus_one
      type: grep
      pattern: "(for|forEach|map).*await.*(prisma|db|query|find)"
      glob: "**/*.{ts,tsx,js,jsx}"
  verbosity: locations
```

### Phase 8: Validation and Testing

Refactoring is only safe when validated by tests.

#### Step 8.1: Run Tests Before Refactoring

Establish baseline: tests must pass before you start.

```yaml
precision_exec:
  commands:
    - cmd: "npm run test"
  verbosity: standard
```

**If tests fail, fix them first.**

#### Step 8.2: Refactor Incrementally

Make small changes and validate after each step.

**Workflow:**
1. Run tests (establish baseline)
2. Make one refactoring change
3. Run tests again
4. If tests pass, commit and continue
5. If tests fail, revert and investigate

**Use `precision_exec` to validate:**

```yaml
precision_exec:
  commands:
    - cmd: "npm run typecheck"
    - cmd: "npm run lint"
    - cmd: "npm run test"
  verbosity: standard
```

#### Step 8.3: Add Tests for Refactored Code

If coverage drops, add tests.

```yaml
precision_exec:
  commands:
    - cmd: "npm run test -- --coverage"
  verbosity: standard
```

**Check coverage:**
- Functions should be 80%+ covered
- Critical paths should be 100% covered
- Edge cases should have explicit tests

### Phase 9: Update Documentation

Refactored code needs updated documentation.

#### Step 9.1: Update JSDoc Comments

**Before (outdated):**

```typescript
/**
 * Gets user data from the database
 */
function getData(id: string) { ... }  // Function was renamed
```

**After (current):**

```typescript
/**
 * Retrieves a user profile by ID including related posts and followers
 * @param userId - The unique identifier for the user
 * @returns User profile with posts and followers, or null if not found
 */
function getUserProfile(userId: string): Promise<UserProfile | null> { ... }
```

#### Step 9.2: Update README and Architecture Docs

If file structure changed, update documentation.

**Example updates:**
- Update file tree in README
- Update import examples
- Update architecture diagrams
- Update contribution guidelines

### Phase 10: Automated Validation

Run the validation script to ensure refactoring quality.

```bash
./scripts/validate-refactoring.sh /path/to/project
```

**The script validates:**
- Tests pass before and after
- Code duplication is reduced
- Type safety improved (no new `any` types)
- Functions are within size limits
- Import cycles eliminated
- Test coverage maintained or improved

## Common Refactoring Patterns

See `references/refactoring-patterns.md` for detailed before/after examples.

**Quick reference:**

### Extract Method

**When:** Function is too long or does multiple things  
**Fix:** Extract logical blocks into separate functions

### Rename Variable/Function

**When:** Name is unclear or misleading  
**Fix:** Rename to be descriptive and follow conventions

### Replace Conditional with Polymorphism

**When:** Switch statement based on type  
**Fix:** Use strategy pattern or class hierarchy

### Introduce Parameter Object

**When:** Function has too many parameters  
**Fix:** Group related parameters into an object

### Replace Magic Numbers

**When:** Hardcoded numbers without context  
**Fix:** Extract to named constants

### Consolidate Duplicate Conditional Fragments

**When:** Same code in all branches  
**Fix:** Move common code outside conditional

## Precision Tools for Refactoring

### Discover Tool

Find refactoring candidates across the codebase.

**Example: Find duplication**

```yaml
discover:
  queries:
    - id: validation_patterns
      type: grep
      pattern: "if.*!.*email.*includes"
      glob: "**/*.{ts,tsx}"
    - id: large_functions
      type: symbols
      query: "function"
  verbosity: locations
```

### Precision Edit

Perform safe, atomic refactoring edits.

**Example: Extract function**

```yaml
precision_edit:
  operations:
    - action: replace
      path: "src/api/user.ts"
      old_text: |
        if (!email || !email.includes('@')) {
          return { error: 'Invalid email' };
        }
      new_text: |
        const emailValidation = validateEmail(email);
        if (!emailValidation.valid) {
          return { error: emailValidation.error };
        }
  verbosity: minimal
```

### Precision Exec

Validate refactoring doesn't break anything.

```yaml
precision_exec:
  commands:
    - cmd: "npm run typecheck"
    - cmd: "npm run lint -- --fix"
    - cmd: "npm run test"
  verbosity: standard
```

## Validation Script

Use `scripts/validate-refactoring.sh` to validate refactoring quality.

```bash
./scripts/validate-refactoring.sh /path/to/project
```

**The script checks:**
- Tests passing before and after changes
- Code duplication metrics
- Type safety (no new `any` types)
- Function size limits
- Import cycles
- Test coverage maintained

## Quick Reference

### Refactoring Checklist

**Before refactoring:**
- [ ] Tests exist and pass
- [ ] Understand current code structure
- [ ] Identify refactoring goal (extract, rename, reorganize)
- [ ] Map all usage sites

**During refactoring:**
- [ ] Make small, incremental changes
- [ ] Run tests after each change
- [ ] Keep commits focused and atomic
- [ ] Update imports and references

**After refactoring:**
- [ ] All tests pass
- [ ] Type checking passes
- [ ] Linting passes
- [ ] Test coverage maintained or improved
- [ ] Documentation updated
- [ ] Run validation script

### When to Refactor

**Good times to refactor:**
- Before adding a new feature (clean up first)
- When fixing a bug (improve structure while fixing)
- During code review (suggest improvements)
- When code smells are noticed (duplication, complexity)

**Bad times to refactor:**
- While debugging an urgent issue (fix first, refactor later)
- Without tests (unsafe, can break behavior)
- Near a deadline (risk introducing bugs)
- When requirements are changing rapidly

### Refactoring Safety Rules

1. **Tests are mandatory** - Never refactor without tests
2. **One change at a time** - Don't mix refactoring with feature work
3. **Validate frequently** - Run tests after every change
4. **Commit atomically** - Each commit should be a complete, working state
5. **Preserve behavior** - Refactoring should not change functionality

## Advanced Techniques

### Automated Refactoring with Precision Tools

Use `discover` to find patterns, then `precision_edit` to fix them.

```yaml
# Step 1: Find all console.log statements
discover:
  queries:
    - id: console_logs
      type: grep
      pattern: "console\\.log\\("
      glob: "src/**/*.{ts,tsx}"
  verbosity: locations

# Step 2: Replace with proper logger
precision_edit:
  operations:
    - action: replace
      path: "src/file1.ts"
      old_text: "console.log("
      new_text: "logger.info("
      replace_all: true
  verbosity: minimal
```

### Parallel Refactoring

Refactor multiple files simultaneously using batch operations.

```yaml
precision_edit:
  operations:
    - action: replace
      path: "src/api/user.ts"
      old_text: "getData"
      new_text: "getUserProfile"
      replace_all: true
    - action: replace
      path: "src/api/post.ts"
      old_text: "getData"
      new_text: "getPostDetails"
      replace_all: true
  verbosity: minimal
```

### Refactoring Metrics

Track improvement over time.

**Measure before refactoring:**

```yaml
precision_exec:
  commands:
    - cmd: "find src -not -path '*/node_modules/*' -not -path '*/dist/*' -name '*.ts' -exec wc -l {} + | tail -1"
    - cmd: "grep -r --include='*.ts' --exclude-dir=node_modules --exclude-dir=dist --exclude-dir=.git --exclude-dir=.next -- 'any' src | wc -l"
  verbosity: standard
```

**Measure after refactoring and compare:**
- Lines of code (should decrease if duplication removed)
- `any` usage count (should decrease)
- Number of files (may increase if splitting large files)
- Test coverage (should maintain or increase)

## Integration with Other Skills

- Use **code-review** to identify refactoring needs
- Use **type-safety** skill for type improvement patterns
- Use **error-handling** skill when refactoring error logic
- Use **testing-strategy** to ensure adequate test coverage
- Use **component-architecture** when refactoring UI components
- Use **database-layer** when refactoring database queries

## Resources

- `references/refactoring-patterns.md` - Common refactoring patterns with examples
- `scripts/validate-refactoring.sh` - Automated refactoring validation
- Martin Fowler's Refactoring Catalog - https://refactoring.com/catalog/
- Clean Code by Robert C. Martin
- Refactoring: Improving the Design of Existing Code by Martin Fowler
