---
name: optimizely-experimentation
description: Optimizely Experimentation Full Stack SDK patterns
---

# Optimizely Experimentation SDK

## Overview

This skill covers Optimizely Full Stack SDK patterns for feature flags, A/B testing, and event tracking.

## SDK Initialization

### Basic Setup

```typescript
import { createInstance } from '@optimizely/optimizely-sdk';

const optimizelyClient = createInstance({
  sdkKey: process.env.NEXT_PUBLIC_OPTIMIZELY_SDK_KEY,
  datafileOptions: {
    autoUpdate: true,
    updateInterval: 60000, // 1 minute
  },
  eventBatchSize: 10,
  eventFlushInterval: 1000,
});

export default optimizelyClient;
```

### React Provider Setup

```tsx
import { OptimizelyProvider, createInstance } from '@optimizely/react-sdk';

const optimizely = createInstance({
  sdkKey: process.env.NEXT_PUBLIC_OPTIMIZELY_SDK_KEY,
});

function App() {
  return (
    <OptimizelyProvider
      optimizely={optimizely}
      user={{
        id: getUserId(),
        attributes: getUserAttributes(),
      }}
      timeout={500}
    >
      <YourApp />
    </OptimizelyProvider>
  );
}
```

## Feature Flags

### Using useDecision Hook

```tsx
import { useDecision } from '@optimizely/react-sdk';

function FeatureComponent() {
  const [decision, clientReady] = useDecision('feature_key');

  if (!clientReady) {
    return <Skeleton />;
  }

  if (!decision.enabled) {
    return null;
  }

  return <NewFeature variables={decision.variables} />;
}
```

### Typed Feature Variables

```typescript
interface PricingVariables {
  discount: number;
  currency: string;
  showBadge: boolean;
}

function usePricingFeature() {
  const [decision, clientReady] = useDecision('pricing_feature');

  return {
    isReady: clientReady,
    isEnabled: decision.enabled,
    discount: decision.variables.discount as number,
    currency: decision.variables.currency as string,
    showBadge: decision.variables.showBadge as boolean,
  };
}
```

## A/B Testing

### Experiment with Variations

```tsx
function CheckoutExperiment() {
  const [decision, clientReady] = useDecision('checkout_experiment');

  if (!clientReady) {
    return <CheckoutSkeleton />;
  }

  switch (decision.variationKey) {
    case 'single_page':
      return <SinglePageCheckout />;
    case 'express':
      return <ExpressCheckout />;
    default:
      return <StandardCheckout />;
  }
}
```

### Server-Side Experiment

```typescript
// pages/api/checkout.ts or app/api/checkout/route.ts
export async function getServerSideProps({ req }) {
  const userId = getUserId(req);
  const decision = optimizelyClient.decide('checkout_experiment', userId);

  return {
    props: {
      variation: decision.variationKey,
      userId,
    },
  };
}
```

## Event Tracking

### Basic Event

```typescript
const userContext = optimizelyClient.createUserContext(userId, {
  membershipTier: user.tier,
  country: user.country,
});

userContext.trackEvent('purchase_completed', {
  revenue: 9900, // In cents
  currency: 'USD',
  itemCount: 3,
});
```

### With React Hook

```tsx
import { useTrackEvent } from '@optimizely/react-sdk';

function PurchaseButton({ amount }: { amount: number }) {
  const track = useTrackEvent();

  const handlePurchase = async () => {
    const result = await processPayment();

    if (result.success) {
      track('purchase_completed', {
        revenue: amount * 100,
        currency: 'USD',
      });
    }
  };

  return <button onClick={handlePurchase}>Purchase</button>;
}
```

## Best Practices

1. **Use timeout** in OptimizelyProvider for anti-flicker
2. **Check clientReady** before rendering variations
3. **Use typed variables** for type safety
4. **Track after success** not before actions
5. **Never include PII** in events or attributes
6. **Use environment variables** for SDK keys
