---
name: test-driven-development
description: Use when implementing any feature or bugfix, before writing implementation code
---

# Test-Driven Development (TDD) for Laravel

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

**Violating the letter of the rules is violating the spirit of the rules.**

## When to Use

**Always:**

- New features
- Bug fixes
- Refactoring
- Behavior changes

**Exceptions (ask your human partner):**

- Throwaway prototypes
- Generated code (migrations, factories)
- Configuration files

Thinking "skip TDD just this once"? Stop. That's rationalization.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over.

**No exceptions:**

- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

Implement fresh from tests. Period.

## Red-Green-Refactor

### RED - Write Failing Test

Write one minimal test showing what should happen.

**Good:**

```php
test('retries failed operations 3 times', function () {
    $attempts = 0;

    $operation = function () use (&$attempts) {
        $attempts++;
        if ($attempts < 3) {
            throw new Exception('fail');
        }
        return 'success';
    };

    $result = retryOperation($operation);

    expect($result)->toBe('success');
    expect($attempts)->toBe(3);
});
```

Clear name, tests real behavior, one thing

**Bad:**

```php
test('retry works', function () {
    $mock = Mockery::mock(SomeService::class);
    $mock->shouldReceive('call')
        ->times(3)
        ->andThrow(new Exception(), new Exception())
        ->andReturn('success');

    retryOperation(fn () => $mock->call());

    // Only verifies mock was called, not actual behavior
});
```

Vague name, tests mock not code

**Requirements:**

- One behavior
- Clear name
- Real code (no mocks unless unavoidable)

### Verify RED - Watch It Fail

**MANDATORY. Never skip.**

```bash
php artisan test --filter="retries failed operations"
```

Confirm:

- Test fails (not errors)
- Failure message is expected
- Fails because feature missing (not typos)

**Test passes?** You're testing existing behavior. Fix test.

**Test errors?** Fix error, re-run until it fails correctly.

### GREEN - Minimal Code

Write simplest code to pass the test.

**Good:**

```php
function retryOperation(callable $fn, int $maxRetries = 3): mixed
{
    for ($i = 0; $i < $maxRetries; $i++) {
        try {
            return $fn();
        } catch (Exception $e) {
            if ($i === $maxRetries - 1) {
                throw $e;
            }
        }
    }
}
```

Just enough to pass

**Bad:**

```php
function retryOperation(
    callable $fn,
    int $maxRetries = 3,
    string $backoff = 'exponential',
    ?callable $onRetry = null,
    ?LoggerInterface $logger = null,
): mixed {
    // YAGNI - You Aren't Gonna Need It
}
```

Over-engineered

Don't add features, refactor other code, or "improve" beyond the test.

### Verify GREEN - Watch It Pass

**MANDATORY.**

```bash
php artisan test --filter="retries failed operations"
```

Confirm:

- Test passes
- Other tests still pass
- Output pristine (no errors, warnings, deprecations)

**Test fails?** Fix code, not test.

**Other tests fail?** Fix now.

### REFACTOR - Clean Up

After green only:

- Remove duplication
- Improve names
- Extract to Actions, Services, or helpers

Keep tests green. Don't add behavior.

### Repeat

Next failing test for next feature.

## Good Tests

| Quality          | Good                                | Bad                                                 |
| ---------------- | ----------------------------------- | --------------------------------------------------- |
| **Minimal**      | One thing. "and" in name? Split it. | `test('validates email and domain and whitespace')` |
| **Clear**        | Name describes behavior             | `test('test1')`                                     |
| **Shows intent** | Demonstrates desired API            | Obscures what code should do                        |

## Why Order Matters

**"I'll write tests after to verify it works"**

Tests written after code pass immediately. Passing immediately proves nothing:

- Might test wrong thing
- Might test implementation, not behavior
- Might miss edge cases you forgot
- You never saw it catch the bug

Test-first forces you to see the test fail, proving it actually tests something.

**"I already manually tested all the edge cases"**

Manual testing is ad-hoc. You think you tested everything but:

- No record of what you tested
- Can't re-run when code changes
- Easy to forget cases under pressure
- "It worked when I tried it" ≠ comprehensive

Automated tests are systematic. They run the same way every time.

**"Deleting X hours of work is wasteful"**

Sunk cost fallacy. The time is already gone. Your choice now:

- Delete and rewrite with TDD (X more hours, high confidence)
- Keep it and add tests after (30 min, low confidence, likely bugs)

The "waste" is keeping code you can't trust. Working code without real tests is technical debt.

**"TDD is dogmatic, being pragmatic means adapting"**

TDD IS pragmatic:

- Finds bugs before commit (faster than debugging after)
- Prevents regressions (tests catch breaks immediately)
- Documents behavior (tests show how to use code)
- Enables refactoring (change freely, tests catch breaks)

"Pragmatic" shortcuts = debugging in production = slower.

**"Tests after achieve the same goals - it's spirit not ritual"**

No. Tests-after answer "What does this do?" Tests-first answer "What should this do?"

Tests-after are biased by your implementation. You test what you built, not what's required. You verify remembered edge cases, not discovered ones.

Tests-first force edge case discovery before implementing. Tests-after verify you remembered everything (you didn't).

30 minutes of tests after ≠ TDD. You get coverage, lose proof tests work.

## Common Rationalizations

| Excuse                                 | Reality                                                                 |
| -------------------------------------- | ----------------------------------------------------------------------- |
| "Too simple to test"                   | Simple code breaks. Test takes 30 seconds.                              |
| "I'll test after"                      | Tests passing immediately prove nothing.                                |
| "Tests after achieve same goals"       | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Already manually tested"              | Ad-hoc ≠ systematic. No record, can't re-run.                           |
| "Deleting X hours is wasteful"         | Sunk cost fallacy. Keeping unverified code is technical debt.           |
| "Keep as reference, write tests first" | You'll adapt it. That's testing after. Delete means delete.             |
| "Need to explore first"                | Fine. Throw away exploration, start with TDD.                           |
| "Test hard = design unclear"           | Listen to test. Hard to test = hard to use.                             |
| "TDD will slow me down"                | TDD faster than debugging. Pragmatic = test-first.                      |
| "Manual test faster"                   | Manual doesn't prove edge cases. You'll re-test every change.           |
| "Existing code has no tests"           | You're improving it. Add tests for existing code.                       |

## Red Flags - STOP and Start Over

- Code before test
- Test after implementation
- Test passes immediately
- Can't explain why test failed
- Tests added "later"
- Rationalizing "just this once"
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit not ritual"
- "Keep as reference" or "adapt existing code"
- "Already spent X hours, deleting is wasteful"
- "TDD is dogmatic, I'm being pragmatic"
- "This is different because..."

**All of these mean: Delete code. Start over with TDD.**

## Laravel-Specific Examples

### Example: Bug Fix with Form Request

**Bug:** Empty email accepted

**RED**

```php
test('rejects empty email', function () {
    $response = $this->postJson('/api/users', [
        'email' => '',
        'name' => 'Test User',
    ]);

    $response->assertStatus(422)
        ->assertJsonValidationErrors(['email']);
});
```

**Verify RED**

```bash
$ php artisan test --filter="rejects empty email"
FAIL: Expected status 422, got 200
```

**GREEN**

```php
// app/Http/Requests/StoreUserRequest.php
class StoreUserRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'email' => ['required', 'email'],
            'name' => ['required', 'string'],
        ];
    }
}
```

**Verify GREEN**

```bash
$ php artisan test --filter="rejects empty email"
PASS
```

### Example: Action Class

**RED**

```php
test('calculate order total includes tax', function () {
    $order = Order::factory()->create([
        'subtotal' => 10000, // $100.00 in cents
    ]);

    $action = new CalculateOrderTotalAction();
    $result = $action->execute($order, taxRate: 0.08);

    expect($result->total)->toBe(10800);
    expect($result->tax)->toBe(800);
});
```

**Verify RED**

```bash
$ php artisan test --filter="calculate order total"
FAIL: Class CalculateOrderTotalAction not found
```

**GREEN**

```php
// app/Actions/CalculateOrderTotalAction.php
class CalculateOrderTotalAction
{
    public function execute(Order $order, float $taxRate): OrderTotal
    {
        $tax = (int) round($order->subtotal * $taxRate);

        return new OrderTotal(
            subtotal: $order->subtotal,
            tax: $tax,
            total: $order->subtotal + $tax,
        );
    }
}
```

**Verify GREEN**

```bash
$ php artisan test --filter="calculate order total"
PASS
```

### Example: Policy/Gate Authorization

**RED**

```php
test('users can only view their own orders', function () {
    $user = User::factory()->create();
    $otherUser = User::factory()->create();
    $order = Order::factory()->for($otherUser)->create();

    $this->actingAs($user);

    expect($user->can('view', $order))->toBeFalse();
});

test('users can view their own orders', function () {
    $user = User::factory()->create();
    $order = Order::factory()->for($user)->create();

    $this->actingAs($user);

    expect($user->can('view', $order))->toBeTrue();
});
```

**GREEN**

```php
// app/Policies/OrderPolicy.php
class OrderPolicy
{
    public function view(User $user, Order $order): bool
    {
        return $user->id === $order->user_id;
    }
}
```

### Example: Eloquent Scope

**RED**

```php
test('active scope returns only active users', function () {
    User::factory()->count(3)->create(['active' => true]);
    User::factory()->count(2)->create(['active' => false]);

    $activeUsers = User::active()->get();

    expect($activeUsers)->toHaveCount(3);
    expect($activeUsers->pluck('active')->unique()->all())->toBe([true]);
});
```

**GREEN**

```php
// app/Models/User.php
public function scopeActive(Builder $query): Builder
{
    return $query->where('active', true);
}
```

### Example: Job/Queue

**RED**

```php
use Illuminate\Support\Facades\Queue;

test('order completion dispatches notification job', function () {
    Queue::fake();

    $order = Order::factory()->create();
    $action = new CompleteOrderAction();

    $action->execute($order);

    Queue::assertPushed(SendOrderCompletionNotification::class, function ($job) use ($order) {
        return $job->order->id === $order->id;
    });
});
```

**GREEN**

```php
class CompleteOrderAction
{
    public function execute(Order $order): void
    {
        $order->update(['status' => 'completed']);

        SendOrderCompletionNotification::dispatch($order);
    }
}
```

### Example: Event Listener

**RED**

```php
use Illuminate\Support\Facades\Event;

test('user registration fires UserRegistered event', function () {
    Event::fake([UserRegistered::class]);

    $action = new RegisterUserAction();
    $user = $action->execute([
        'email' => 'test@example.com',
        'password' => 'password',
    ]);

    Event::assertDispatched(UserRegistered::class, function ($event) use ($user) {
        return $event->user->id === $user->id;
    });
});
```

**GREEN**

```php
class RegisterUserAction
{
    public function execute(array $data): User
    {
        $user = User::create([
            'email' => $data['email'],
            'password' => Hash::make($data['password']),
        ]);

        event(new UserRegistered($user));

        return $user;
    }
}
```

## Pest-Specific Features

### Use `describe` for Grouping Related Tests

```php
describe('OrderPolicy', function () {
    test('owners can view their orders', function () {
        // ...
    });

    test('owners can cancel pending orders', function () {
        // ...
    });

    test('owners cannot cancel shipped orders', function () {
        // ...
    });
});
```

### Use `beforeEach` for Common Setup

```php
beforeEach(function () {
    $this->user = User::factory()->create();
    $this->actingAs($this->user);
});

test('can create order', function () {
    // $this->user is available
});
```

### Use Datasets for Parameterized Tests

```php
dataset('invalid_emails', [
    'empty string' => [''],
    'missing @' => ['invalidemail.com'],
    'missing domain' => ['test@'],
    'spaces' => ['test @example.com'],
]);

test('rejects invalid email formats', function (string $email) {
    $response = $this->postJson('/api/users', [
        'email' => $email,
        'name' => 'Test',
    ]);

    $response->assertJsonValidationErrors(['email']);
})->with('invalid_emails');
```

### Use Higher-Order Tests for Simple Cases

```php
test('homepage loads successfully')
    ->get('/')
    ->assertOk();

test('guests cannot access dashboard')
    ->get('/dashboard')
    ->assertRedirect('/login');
```

## Verification Checklist

Before marking work complete:

- [ ] Every new Action/Service/Model method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass: `php artisan test`
- [ ] Output pristine (no errors, warnings, deprecations)
- [ ] Tests use real code (fakes only for external services)
- [ ] Edge cases and errors covered

Can't check all boxes? You skipped TDD. Start over.

## Useful Commands

```bash
# Run all tests
php artisan test

# Run specific test by name
php artisan test --filter="rejects empty email"

# Run specific test file
php artisan test tests/Feature/OrderTest.php

# Run tests in parallel
php artisan test --parallel

# Run with coverage
php artisan test --coverage

# Run and stop on first failure
php artisan test --stop-on-failure

# Run only dirty tests (changed files)
php artisan test --dirty
```

## When Stuck

| Problem                | Solution                                                             |
| ---------------------- | -------------------------------------------------------------------- |
| Don't know how to test | Write wished-for API. Write assertion first. Ask your human partner. |
| Test too complicated   | Design too complicated. Simplify interface.                          |
| Must mock everything   | Code too coupled. Use dependency injection.                          |
| Test setup huge        | Use factories, traits, helpers. Still complex? Simplify design.      |
| Database slow          | Use `RefreshDatabase` or `LazilyRefreshDatabase` trait.              |

## Debugging Integration

Bug found? Write failing test reproducing it. Follow TDD cycle. Test proves fix and prevents regression.

Never fix bugs without a test.

## Final Rule

```
Production code → test exists and failed first
Otherwise → not TDD
```

No exceptions without your human partner's permission.
