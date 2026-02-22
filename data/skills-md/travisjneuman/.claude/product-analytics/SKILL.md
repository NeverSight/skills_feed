---
name: product-analytics
description: Event tracking architecture, funnels, cohorts, A/B testing, PostHog/Amplitude
---

# Product Analytics

## Overview

This skill covers designing and implementing product analytics systems that provide actionable insights into user behavior. It addresses event taxonomy design, analytics SDK integration with major platforms (PostHog, Amplitude, Mixpanel, Segment), funnel and cohort analysis, A/B testing and feature flags, user journey mapping, GDPR-compliant consent management, and custom metric definitions.

Use this skill when adding analytics to a new product, redesigning an event tracking system, setting up A/B testing infrastructure, implementing consent management, or building custom dashboards for product teams.

---

## Core Principles

1. **Design the taxonomy before writing code** - A well-designed event naming convention and property schema prevents the #1 analytics failure: inconsistent, unqueryable data. Agree on naming conventions first.
2. **Track actions, not pages** - Page views tell you where users went. Events with context tell you what users did and why. Focus on user actions: `project_created`, `file_uploaded`, `subscription_upgraded`.
3. **Identify before you track** - Every event needs a user identity. Anonymous events before signup should be linked to the authenticated identity once the user logs in (alias/merge).
4. **Consent is mandatory** - GDPR and CCPA require explicit user consent before tracking. Build consent management into the analytics layer, not as an afterthought.
5. **Less is more** - Tracking everything creates noise. Track the events that answer specific product questions. You can always add events later; removing noise from existing data is much harder.

---

## Key Patterns

### Pattern 1: Event Taxonomy Design

**When to use:** Before implementing any analytics tracking. This is the foundation everything else builds on.

**Implementation:**

```typescript
// Event taxonomy schema
// Convention: object_action (noun_verb in past tense)

// Core event types
type AnalyticsEvent =
  // Authentication
  | { event: "user_signed_up"; properties: { method: "email" | "google" | "github"; referralSource?: string } }
  | { event: "user_logged_in"; properties: { method: "email" | "google" | "github" } }
  | { event: "user_logged_out"; properties: Record<string, never> }

  // Onboarding
  | { event: "onboarding_started"; properties: { variant?: string } }
  | { event: "onboarding_step_completed"; properties: { step: number; stepName: string } }
  | { event: "onboarding_completed"; properties: { durationSeconds: number } }
  | { event: "onboarding_skipped"; properties: { lastStep: number } }

  // Core product actions
  | { event: "project_created"; properties: { template?: string; source: "dashboard" | "onboarding" | "api" } }
  | { event: "project_deleted"; properties: { projectAge: number; itemCount: number } }
  | { event: "file_uploaded"; properties: { fileType: string; fileSizeBytes: number; source: "drag_drop" | "file_picker" | "api" } }

  // Subscription
  | { event: "subscription_started"; properties: { plan: string; billingCycle: "monthly" | "annual"; amount: number } }
  | { event: "subscription_upgraded"; properties: { fromPlan: string; toPlan: string } }
  | { event: "subscription_cancelled"; properties: { reason?: string; plan: string; tenureDays: number } }

  // Feature engagement
  | { event: "feature_used"; properties: { feature: string; context: string } }
  | { event: "search_performed"; properties: { query: string; resultCount: number; source: string } }
  | { event: "export_completed"; properties: { format: "csv" | "pdf" | "json"; itemCount: number } };

// Type-safe tracking function
function track<T extends AnalyticsEvent>(
  event: T["event"],
  properties: T["properties"]
): void {
  // Implementation below
}

// Usage - fully typed, autocomplete works
track("project_created", {
  template: "blank",
  source: "dashboard",
});
```

**Why:** A typed event taxonomy prevents typos (`user_signedup` vs `user_signed_up`), ensures required properties are always present, and makes the tracking plan self-documenting. The `object_action` convention groups related events together in analytics dashboards.

---

### Pattern 2: Analytics Client with Consent Management

**When to use:** Every product that tracks user behavior, which is every product.

**Implementation:**

```typescript
// analytics.ts - Unified analytics client
import posthog from "posthog-js";

type ConsentStatus = "granted" | "denied" | "pending";

interface AnalyticsConfig {
  posthogKey: string;
  posthogHost?: string;
}

class Analytics {
  private initialized = false;
  private consent: ConsentStatus = "pending";
  private queuedEvents: Array<{ event: string; properties: Record<string, unknown> }> = [];

  init(config: AnalyticsConfig) {
    posthog.init(config.posthogKey, {
      api_host: config.posthogHost ?? "https://us.i.posthog.com",
      persistence: "localStorage+cookie",
      autocapture: false, // Explicit tracking only
      capture_pageview: false, // Manual pageview tracking
      capture_pageleave: true,
      // Respect Do Not Track
      respect_dnt: true,
      // Cookie-less mode until consent
      persistence: this.consent === "granted" ? "localStorage+cookie" : "memory",
    });
    this.initialized = true;
  }

  setConsent(status: ConsentStatus) {
    this.consent = status;

    if (status === "granted") {
      posthog.opt_in_capturing();
      // Flush queued events
      for (const event of this.queuedEvents) {
        this.trackInternal(event.event, event.properties);
      }
      this.queuedEvents = [];
    } else if (status === "denied") {
      posthog.opt_out_capturing();
      this.queuedEvents = [];
    }
  }

  identify(userId: string, traits?: Record<string, unknown>) {
    if (this.consent !== "granted") return;
    posthog.identify(userId, traits);
  }

  // Alias anonymous ID to authenticated ID (for signup flow)
  alias(newId: string) {
    if (this.consent !== "granted") return;
    posthog.alias(newId);
  }

  track(event: string, properties?: Record<string, unknown>) {
    if (this.consent === "denied") return;

    const enrichedProperties = {
      ...properties,
      timestamp: new Date().toISOString(),
      url: typeof window !== "undefined" ? window.location.href : undefined,
      referrer: typeof document !== "undefined" ? document.referrer : undefined,
    };

    if (this.consent === "pending") {
      this.queuedEvents.push({ event, properties: enrichedProperties });
      return;
    }

    this.trackInternal(event, enrichedProperties);
  }

  private trackInternal(event: string, properties: Record<string, unknown>) {
    if (!this.initialized) return;
    posthog.capture(event, properties);
  }

  page(name?: string, properties?: Record<string, unknown>) {
    this.track("$pageview", { pageName: name, ...properties });
  }

  reset() {
    posthog.reset();
  }
}

export const analytics = new Analytics();
```

```tsx
// React consent banner component
function ConsentBanner() {
  const [showBanner, setShowBanner] = useState(() => {
    return localStorage.getItem("analytics_consent") === null;
  });

  const handleConsent = (granted: boolean) => {
    const status = granted ? "granted" : "denied";
    localStorage.setItem("analytics_consent", status);
    analytics.setConsent(status);
    setShowBanner(false);
  };

  if (!showBanner) return null;

  return (
    <div role="dialog" aria-label="Cookie consent" className="consent-banner">
      <p>We use analytics to improve our product. No personal data is sold.</p>
      <div className="consent-actions">
        <button onClick={() => handleConsent(false)}>Decline</button>
        <button onClick={() => handleConsent(true)}>Accept</button>
      </div>
    </div>
  );
}
```

**Why:** Consent-first analytics is legally required (GDPR, CCPA) and builds user trust. The queue pattern ensures no events are lost if the user grants consent after performing actions. Explicit tracking (no autocapture) keeps data clean and intentional.

---

### Pattern 3: Funnel Analysis Implementation

**When to use:** Measuring conversion through multi-step flows (signup, onboarding, checkout).

**Implementation:**

```typescript
// Track each funnel step explicitly
const ONBOARDING_FUNNEL = [
  "onboarding_started",
  "onboarding_step_completed:profile",
  "onboarding_step_completed:workspace",
  "onboarding_step_completed:invite",
  "onboarding_completed",
] as const;

// Instrument each step
function OnboardingFlow() {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    analytics.track("onboarding_started", { variant: "v2" });
  }, []);

  const completeStep = (stepName: string) => {
    analytics.track("onboarding_step_completed", {
      step: currentStep,
      stepName,
      timeOnStepSeconds: getTimeOnStep(),
    });
    setCurrentStep((prev) => prev + 1);
  };

  const skip = () => {
    analytics.track("onboarding_skipped", {
      lastStep: currentStep,
      lastStepName: steps[currentStep].name,
    });
    router.push("/dashboard");
  };

  const complete = () => {
    analytics.track("onboarding_completed", {
      durationSeconds: getTotalDuration(),
      stepsCompleted: currentStep + 1,
      stepsSkipped: steps.length - currentStep - 1,
    });
    router.push("/dashboard");
  };

  // ...render steps
}

// Checkout funnel tracking
function useCheckoutFunnel() {
  const trackStep = (step: string, properties?: Record<string, unknown>) => {
    analytics.track(`checkout_${step}`, {
      ...properties,
      cartValue: getCartTotal(),
      itemCount: getCartItemCount(),
      timestamp: Date.now(),
    });
  };

  return {
    viewCart: () => trackStep("cart_viewed"),
    startCheckout: () => trackStep("started"),
    addShipping: (method: string) => trackStep("shipping_added", { method }),
    addPayment: (type: string) => trackStep("payment_added", { type }),
    complete: (orderId: string) => trackStep("completed", { orderId }),
    abandon: (step: string) => trackStep("abandoned", { lastStep: step }),
  };
}
```

**Why:** Funnel analysis reveals where users drop off. Tracking each step with context (time spent, variant, cart value) enables segmented analysis: "Users from Google Ads drop off at the shipping step 3x more than organic users." This insight drives targeted optimization.

---

### Pattern 4: Feature Flag-Driven A/B Testing

**When to use:** Testing product changes with statistical rigor before rolling out to all users.

**Implementation:**

```typescript
// PostHog feature flags for A/B testing
import posthog from "posthog-js";

// Check feature flag with typed variants
function useExperiment<T extends string>(
  flagKey: string,
  variants: T[]
): T | "control" | undefined {
  const [variant, setVariant] = useState<T | "control" | undefined>();

  useEffect(() => {
    posthog.onFeatureFlags(() => {
      const value = posthog.getFeatureFlag(flagKey);

      if (value === false || value === undefined) {
        setVariant("control");
      } else if (typeof value === "string" && variants.includes(value as T)) {
        setVariant(value as T);
      } else {
        setVariant("control");
      }

      // Track experiment exposure (for accurate analysis)
      analytics.track("$experiment_started", {
        experiment: flagKey,
        variant: value ?? "control",
      });
    });
  }, [flagKey]);

  return variant;
}

// Usage in component
function PricingPage() {
  const variant = useExperiment("pricing-page-redesign", ["new-layout", "social-proof"]);

  if (!variant) return <LoadingSkeleton />;

  switch (variant) {
    case "new-layout":
      return <PricingNewLayout />;
    case "social-proof":
      return <PricingSocialProof />;
    case "control":
    default:
      return <PricingControl />;
  }
}
```

**Why:** A/B testing removes opinion from product decisions. Feature flags enable gradual rollout, instant rollback, and segment-specific targeting. Tracking exposure events separately from conversion events ensures accurate statistical analysis (intent-to-treat analysis).

---

## Event Naming Convention Reference

| Convention | Example | When to Use |
|---|---|---|
| `object_action` | `project_created`, `file_uploaded` | Standard product events |
| `$system_event` | `$pageview`, `$identify` | System/platform events |
| `experiment_*` | `$experiment_started` | A/B test tracking |
| `feature_used` | `feature_used { feature: "export" }` | Generic feature engagement |

---

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Better Approach |
|---|---|---|
| Autocapture everything | Noisy data, hard to query, privacy risk | Explicit event tracking with defined taxonomy |
| Inconsistent event names | `userSignedUp` vs `user_signed_up` vs `signup` | Enforce naming convention with TypeScript types |
| Tracking without consent | GDPR/CCPA violation, fines up to 4% revenue | Consent banner with queue pattern |
| No user identification | Cannot do cohort analysis or retention | Identify users on login, alias on signup |
| Tracking PII in event properties | Privacy violation, data retention issues | Use user IDs, not emails/names in event properties |
| One massive "user_action" event | Cannot create meaningful funnels | Specific event per meaningful action |
| Not tracking negative outcomes | Only see what works, not what fails | Track errors, abandonment, rage clicks |

---

## Checklist

- [ ] Event taxonomy documented and typed (TypeScript interface)
- [ ] Naming convention enforced (`object_action` pattern)
- [ ] Analytics client initialized with consent management
- [ ] User identification on login, alias on signup
- [ ] Funnel steps tracked with contextual properties
- [ ] Feature flags set up for A/B testing
- [ ] Experiment exposure events tracked separately from conversions
- [ ] GDPR consent banner implemented with queue pattern
- [ ] No PII in event properties (emails, full names, IPs)
- [ ] Key funnels visualized in analytics dashboard
- [ ] Retention cohorts configured (Day 1, Day 7, Day 30)
- [ ] Analytics events validated in development (debug mode)

---

## Related Resources

- **Skills:** `growth-engineering` (A/B testing infrastructure), `authentication-patterns` (identify/alias flow)
- **Skills:** `accessibility-a11y` (accessible consent banners)
- **Rules:** `rules/stacks/react-typescript.md` (React hooks for analytics)
