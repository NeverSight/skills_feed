---
name: error-boundaries
description: Use when deciding where to catch errors. Use when errors propagate too far or not far enough. Use when designing component/service isolation.
---

# Error Boundaries

## Overview

**Catch errors at logical boundaries, not random points in the call stack.**

Error boundaries are strategic catch points that prevent cascading failures while enabling graceful degradation. Place them at architectural boundaries—not scattered throughout business logic.

## When to Use

- Designing application architecture
- Deciding where try/catch belongs
- Preventing one failure from crashing everything
- Implementing graceful degradation
- Isolating components from each other

## The Iron Rule

```
NEVER scatter try/catch randomly. Place catches at ARCHITECTURAL BOUNDARIES only.
```

**No exceptions:**
- Not for "defensive programming"
- Not for "safety wrapper"
- Not for "just in case"
- Not for "the function might throw"

**Boundaries are intentional. Random catches hide bugs.**

## What Is a Boundary?

Boundaries are points where context changes:

```
┌─────────────────────────────────────────────────────────────┐
│                         ENTRY BOUNDARIES                     │
│  HTTP Request → [BOUNDARY] → Application                    │
│  Message Queue → [BOUNDARY] → Handler                       │
│  CLI Command → [BOUNDARY] → Execution                       │
│  Cron Job → [BOUNDARY] → Task                               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                       INTERNAL BOUNDARIES                    │
│  Application → [BOUNDARY] → External API                    │
│  Business Logic → [BOUNDARY] → Database                     │
│  Core → [BOUNDARY] → Third-party Library                    │
│  Parent Component → [BOUNDARY] → Child Component            │
└─────────────────────────────────────────────────────────────┘
```

## Strategic Boundary Placement

### Entry Boundary: HTTP Controller

```typescript
// ✅ CORRECT: Top-level error middleware
app.use(errorMiddleware);

function errorMiddleware(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  // This is THE boundary between HTTP and application
  
  if (error instanceof ValidationError) {
    return res.status(400).json({ error: error.message, fields: error.fields });
  }
  
  if (error instanceof NotFoundError) {
    return res.status(404).json({ error: error.message });
  }
  
  if (error instanceof UnauthorizedError) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  
  // Log unknown errors, return generic response
  logger.error('Unhandled error', { error, request: req.path });
  return res.status(500).json({ error: 'Internal server error' });
}

// ❌ WRONG: try/catch in every controller
async function getUser(req: Request, res: Response) {
  try {
    const user = await userService.findById(req.params.id);
    res.json(user);
  } catch (error) {
    // Scattered catch - duplicated across all controllers
    res.status(500).json({ error: 'Failed' });
  }
}

// ✅ CORRECT: Let errors propagate to middleware
async function getUser(req: Request, res: Response) {
  const user = await userService.findById(req.params.id);
  res.json(user);
  // Errors propagate to errorMiddleware
}
```

### Internal Boundary: External Service Adapter

```typescript
// ✅ CORRECT: Boundary between your code and external service
class PaymentGatewayAdapter {
  async charge(amount: number, token: string): Promise<ChargeResult> {
    try {
      // External call - this is a boundary
      const response = await this.stripeClient.charges.create({
        amount,
        source: token,
      });
      return this.mapToChargeResult(response);
    } catch (error) {
      // Translate external error to domain error
      if (error instanceof Stripe.CardError) {
        throw new PaymentDeclinedError(error.message, error.code);
      }
      if (error instanceof Stripe.RateLimitError) {
        throw new PaymentServiceUnavailableError('Rate limited');
      }
      if (error instanceof Stripe.APIConnectionError) {
        throw new PaymentServiceUnavailableError('Connection failed');
      }
      throw new PaymentError('Unexpected payment error', { cause: error });
    }
  }
}

// ❌ WRONG: Let Stripe errors leak into business logic
// ❌ WRONG: Catch in OrderService instead of adapter
```

### UI Boundary: React Error Boundary

```tsx
// ✅ CORRECT: Component-level error isolation
class ErrorBoundary extends React.Component<Props, State> {
  state = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    // Log to monitoring service
    errorService.report(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || <DefaultErrorUI />;
    }
    return this.props.children;
  }
}

// Usage: Isolate features from each other
function App() {
  return (
    <Layout>
      <ErrorBoundary fallback={<DashboardError />}>
        <Dashboard />
      </ErrorBoundary>
      
      <ErrorBoundary fallback={<SidebarError />}>
        <Sidebar />
      </ErrorBoundary>
      
      {/* Sidebar error doesn't crash Dashboard */}
    </Layout>
  );
}
```

## The Boundary Checklist

Before adding try/catch, verify:

| Question | If No... |
|----------|----------|
| Is this a context transition point? | Don't catch here |
| Would catching prevent meaningful propagation? | Don't catch here |
| Can I translate to a meaningful domain error? | Don't catch here |
| Is there a specific recovery action? | Don't catch here |
| Does the boundary change ownership? | Don't catch here |

## Correct Propagation Pattern

Let errors propagate through business logic:

```typescript
// ✅ CORRECT: No random catches in service layer
class OrderService {
  async createOrder(data: OrderData): Promise<Order> {
    // Validate (may throw ValidationError)
    this.validator.validate(data);
    
    // Get user (may throw NotFoundError)
    const user = await this.userRepo.findById(data.userId);
    
    // Check business rules (may throw BusinessRuleError)
    this.rules.assertCanCreateOrder(user, data);
    
    // Process payment (may throw PaymentError from adapter)
    const payment = await this.paymentAdapter.charge(data.amount, user.paymentToken);
    
    // Create order (may throw DatabaseError from repo)
    const order = await this.orderRepo.create({
      ...data,
      paymentId: payment.id,
    });
    
    return order;
    // ALL errors propagate to controller boundary
  }
}

// ❌ WRONG: Defensive try/catch in service
class OrderService {
  async createOrder(data: OrderData): Promise<Order | null> {
    try {
      // ... same logic ...
      return order;
    } catch (error) {
      logger.error('Order creation failed', error);
      return null;  // Lost context, hidden failure
    }
  }
}
```

## Graceful Degradation at Boundaries

Boundaries can provide fallbacks:

```typescript
// ✅ CORRECT: Graceful degradation at recommendation boundary
class ProductPage {
  async load(productId: string) {
    // Core data - must succeed
    const product = await this.productService.getById(productId);
    
    // Recommendations - can fail gracefully
    let recommendations: Product[] = [];
    try {
      recommendations = await this.recommendationService.getFor(productId);
    } catch (error) {
      // Log but don't fail the page
      logger.warn('Recommendations unavailable', { productId, error });
      // Empty recommendations is acceptable fallback
    }
    
    return { product, recommendations };
  }
}
```

**Key distinction:** This is a boundary between "required" and "optional" features.
It's NOT random defensive programming—it's intentional graceful degradation.

## Pressure Resistance Protocol

### 1. "Wrap Everything in Try/Catch for Safety"
**Pressure:** "Be defensive, catch all errors"

**Response:** Scattered catches hide bugs and prevent proper handling at boundaries. Errors propagate for a reason.

**Action:** Remove interior catches. Handle at boundaries only.

### 2. "The Function Might Throw"
**Pressure:** "I should catch just in case"

**Response:** That's what boundaries are for. Business logic shouldn't know about error handling.

**Action:** Let it throw. Boundary will catch.

### 3. "I Want to Add Context to Errors"
**Pressure:** "Catch, add info, re-throw"

**Response:** Only if you're adding genuinely useful context. Most catch-and-rethrow just adds noise.

**Action:** Only wrap if context is truly lost otherwise. Usually it isn't.

### 4. "Each Component Should Handle Its Errors"
**Pressure:** "Encapsulation means local handling"

**Response:** Components should THROW appropriate errors. CATCHING is for boundaries.

**Action:** Component throws. Boundary catches. Separation of concerns.

## Red Flags - STOP and Reconsider

If you notice ANY of these, remove the catch:

- try/catch in pure business logic functions
- Catching and re-throwing without translation
- try/catch that just logs and continues
- Empty catch blocks
- Catch in every method of a class
- try/catch for "defensive programming"
- Catching errors you can't meaningfully handle

**All of these mean: Let the error propagate to a real boundary.**

## Boundary Inventory

Map your application's boundaries:

```typescript
// Document where boundaries exist
const BOUNDARIES = {
  // Entry points
  HTTP: 'errorMiddleware in app.ts',
  GraphQL: 'formatError in apollo.ts',
  MessageQueue: 'errorHandler in consumer.ts',
  CronJobs: 'wrapWithErrorHandling in scheduler.ts',
  
  // Internal boundaries
  ExternalAPIs: [
    'PaymentGatewayAdapter',
    'EmailServiceAdapter',
    'SearchServiceAdapter',
  ],
  
  // UI boundaries
  React: 'ErrorBoundary components per feature',
  
  // Optional/degradable features
  Degradable: [
    'RecommendationService (fallback: empty)',
    'AnalyticsService (fallback: skip)',
  ],
};
```

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "Defensive programming is good" | Defensive = validate inputs. Not = scatter catches. |
| "Catch errors where they occur" | Catch at boundaries. Throw where they occur. |
| "Add context with catch-rethrow" | Usually adds noise. Boundaries have context. |
| "Prevent cascading failures" | Boundaries prevent cascades. Random catches hide bugs. |
| "Component independence" | Components throw. Boundaries catch. Still independent. |
| "Safety wrapper" | Wrappers hide failures. Fail fast instead. |

## Quick Reference

| Location | Action |
|----------|--------|
| HTTP middleware | ✅ Catch and translate to responses |
| Message handler | ✅ Catch, ack/nack, log |
| External adapter | ✅ Catch and translate to domain errors |
| React error boundary | ✅ Catch and show fallback UI |
| Service method | ❌ Let errors propagate |
| Repository method | ❌ Let errors propagate (unless wrapping DB errors) |
| Utility function | ❌ Let errors propagate |
| Pure business logic | ❌ Let errors propagate |

## The Bottom Line

**Boundaries are architectural. Catches are strategic.**

Place try/catch at context transitions: HTTP entry, external adapters, UI component isolation, optional feature degradation. Never in business logic. Let errors propagate to boundaries where they can be translated, logged, and handled appropriately.
