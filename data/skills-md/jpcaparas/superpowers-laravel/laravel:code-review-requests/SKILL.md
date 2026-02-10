---
name: laravel:code-review-requests
description: Request effective code reviews—specify focus areas, provide context, ask for architectural feedback, reference Laravel conventions
---

# Code Review Requests

Focused review requests get actionable feedback. Vague requests get generic advice.

## Specify Focus Areas

### Vague
"Review this code"

### Focused
"Review OrderService for security and performance:

**Focus on:**
- Authorization checks (are we verifying user owns the order?)
- SQL injection risks (any raw queries?)
- N+1 query problems (eager loading correct?)
- Transaction handling (atomic operations?)
- Error handling (graceful failures?)

**Code:**
```php
class OrderService
{
    public function createOrder(User $user, array $items): Order
    {
        $order = Order::create(['user_id' => $user->id]);
        
        foreach ($items as $item) {
            OrderItem::create([
                'order_id' => $order->id,
                'product_id' => $item['product_id'],
                'quantity' => $item['quantity'],
            ]);
        }
        
        return $order;
    }
}
```"

**Why it works:** Clear focus areas guide the review toward specific concerns.

## Provide Context

### Insufficient Context
"Is this controller okay?"

### Sufficient Context
"Review ProductController for our API:

**Context:**
- Public API used by mobile app and web frontend
- Handles 10k requests/day, needs to scale to 100k
- Products have categories (belongsTo) and reviews (hasMany)
- Using Laravel 11.x with Sanctum authentication
- Following repository pattern (ProductRepository exists)

**Concerns:**
- Is the response format consistent with our other API endpoints?
- Are we handling errors appropriately?
- Should we add rate limiting?

**Code:**
```php
class ProductController extends Controller
{
    public function index(Request $request)
    {
        $products = Product::with('category')
            ->paginate(20);
            
        return ProductResource::collection($products);
    }
}
```"

**Why it works:** Context about usage, scale, patterns, and specific concerns.

## Architectural Feedback

### Unclear
"Is the architecture good?"

### Clear
"Review the architecture of our payment processing:

**Current design:**
```
PaymentController
  → PaymentService
    → StripeGateway (direct Stripe API calls)
    → PaymentRepository (database)
```

**Concerns:**
1. PaymentService is tightly coupled to Stripe. What if we add PayPal?
2. No retry logic for failed payments
3. Webhook handling is in a separate controller, feels disconnected
4. No audit trail of payment attempts

**Questions:**
- Should we use a PaymentGatewayInterface for multiple providers?
- Where should retry logic live? Service or job?
- How to structure webhook handling?
- Best way to add audit logging?

**Current code:** [attach PaymentService.php]"

**Why it works:** Explains current design, identifies concerns, asks specific questions.

## Laravel-Specific Review

### Generic
"Check if this follows best practices"

### Laravel-Specific
"Review for Laravel conventions and best practices:

**Code:**
```php
class UserController extends Controller
{
    public function store(Request $request)
    {
        $validated = $request->validate([
            'email' => 'required|email|unique:users',
            'password' => 'required|min:8',
        ]);
        
        $user = new User();
        $user->email = $validated['email'];
        $user->password = Hash::make($validated['password']);
        $user->save();
        
        return response()->json($user, 201);
    }
}
```

**Check for:**
- Should validation be in a Form Request?
- Is mass assignment safer than manual assignment?
- Should we use a Resource for the response?
- Is password hashing handled correctly?
- Should user creation be in a service/action?
- Any missing authorization checks?
- Following Laravel 11.x conventions?"

**Why it works:** Asks about specific Laravel patterns and conventions.

## Specify Experience Level

### Unclear Depth
"Review my code"

### Clear Depth
"Review this authentication implementation:

**My experience:** Junior developer, 6 months with Laravel

**What I need:**
- Explain any security issues in detail (I'm still learning auth best practices)
- Point out Laravel conventions I'm missing
- Suggest improvements with examples
- If something is wrong, explain why and show the correct approach

**Code:**
```php
public function login(Request $request)
{
    $user = User::where('email', $request->email)->first();
    
    if ($user && Hash::check($request->password, $user->password)) {
        $token = $user->createToken('auth')->plainTextToken;
        return response()->json(['token' => $token]);
    }
    
    return response()->json(['error' => 'Invalid credentials'], 401);
}
```

**Questions:**
- Is this secure enough for production?
- What am I missing?
- How would a senior developer write this?"

**Why it works:** Sets expectations for depth and style of feedback.

## Review Request Templates

### Template: Security Review
```
**Focus:** Security vulnerabilities and best practices
**Code:** [attach code]
**Context:** [authentication method, data sensitivity, user roles]
**Specific concerns:**
- [ ] SQL injection risks
- [ ] XSS vulnerabilities  
- [ ] Authorization checks
- [ ] Data validation
- [ ] Sensitive data exposure
```

### Template: Performance Review
```
**Focus:** Performance and scalability
**Code:** [attach code]
**Current metrics:** [response times, query counts]
**Expected load:** [requests/day, concurrent users]
**Specific concerns:**
- [ ] N+1 queries
- [ ] Missing indexes
- [ ] Inefficient algorithms
- [ ] Caching opportunities
- [ ] Memory usage
```

### Template: Architecture Review
```
**Focus:** Design patterns and maintainability
**Code:** [attach code]
**Current architecture:** [describe structure]
**Team size:** [number of developers]
**Specific concerns:**
- [ ] Separation of concerns
- [ ] Testability
- [ ] Coupling between components
- [ ] Code duplication
- [ ] Complexity
```

### Template: Laravel Conventions
```
**Focus:** Laravel best practices and conventions
**Code:** [attach code]
**Laravel version:** [11.x or 12.x]
**Specific concerns:**
- [ ] Following framework conventions
- [ ] Using appropriate Laravel features
- [ ] Eloquent relationships correct
- [ ] Validation approach
- [ ] Resource/response formatting
```

## Quick Reference

Request effective reviews:
- **Specify focus** - Security, performance, architecture, conventions
- **Provide context** - Purpose, scale, patterns, constraints
- **Ask specific questions** - Don't just ask "is this good?"
- **Reference Laravel** - Ask about framework-specific patterns
- **Set depth** - Junior needs explanations, senior needs quick feedback

Focused requests = actionable feedback.
