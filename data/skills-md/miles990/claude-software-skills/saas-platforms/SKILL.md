---
name: saas-platforms
description: SaaS architecture, multi-tenancy, and subscription management
domain: domain-applications
version: 1.0.0
tags: [saas, multi-tenancy, subscriptions, billing, onboarding]
triggers:
  keywords:
    primary: [saas, multi-tenant, subscription, billing, tenant]
    secondary: [onboarding, feature flag, usage billing, plan, pricing tier]
  context_boost: [platform, b2b, enterprise, organization]
  context_penalty: [mobile, game, desktop]
  priority: high
---

# SaaS Platform Development

## Overview

Building Software-as-a-Service applications with multi-tenancy, subscription billing, and user management.

---

## Multi-Tenancy

### Database Strategies

```typescript
// Strategy 1: Shared database with tenant_id column
interface TenantEntity {
  tenantId: string;
  // ... other fields
}

// Middleware to inject tenant context
function tenantMiddleware(req: Request, res: Response, next: NextFunction) {
  const tenantId = req.headers['x-tenant-id'] || req.user?.tenantId;

  if (!tenantId) {
    return res.status(400).json({ error: 'Tenant ID required' });
  }

  req.tenantId = tenantId;
  next();
}

// Prisma middleware for automatic tenant filtering
prisma.$use(async (params, next) => {
  const tenantId = getCurrentTenantId();

  if (params.model && hasTenantId(params.model)) {
    // Add tenant filter to queries
    if (params.action === 'findMany' || params.action === 'findFirst') {
      params.args.where = {
        ...params.args.where,
        tenantId,
      };
    }

    // Add tenant ID to creates
    if (params.action === 'create') {
      params.args.data.tenantId = tenantId;
    }
  }

  return next(params);
});

// Strategy 2: Schema per tenant (PostgreSQL)
async function createTenantSchema(tenantId: string) {
  await prisma.$executeRaw`CREATE SCHEMA IF NOT EXISTS ${tenantId}`;

  // Run migrations for new schema
  await runMigrations(tenantId);
}

function getTenantConnection(tenantId: string) {
  return new PrismaClient({
    datasources: {
      db: {
        url: `${process.env.DATABASE_URL}?schema=${tenantId}`,
      },
    },
  });
}

// Strategy 3: Database per tenant
async function createTenantDatabase(tenantId: string) {
  const dbName = `tenant_${tenantId}`;
  await adminDb.$executeRaw`CREATE DATABASE ${dbName}`;

  return new PrismaClient({
    datasources: {
      db: {
        url: `postgresql://user:pass@host:5432/${dbName}`,
      },
    },
  });
}
```

### Tenant Isolation

```typescript
// Row-level security with Prisma
const prisma = new PrismaClient().$extends({
  query: {
    $allModels: {
      async findMany({ model, operation, args, query }) {
        const tenantId = getCurrentTenantId();
        args.where = { ...args.where, tenantId };
        return query(args);
      },
      async create({ model, operation, args, query }) {
        const tenantId = getCurrentTenantId();
        args.data = { ...args.data, tenantId };
        return query(args);
      },
    },
  },
});

// PostgreSQL Row Level Security
/*
CREATE POLICY tenant_isolation ON projects
    USING (tenant_id = current_setting('app.tenant_id')::uuid);

ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
*/

// Set tenant context for RLS
async function withTenantContext<T>(
  tenantId: string,
  fn: () => Promise<T>
): Promise<T> {
  await prisma.$executeRaw`SET app.tenant_id = ${tenantId}`;
  try {
    return await fn();
  } finally {
    await prisma.$executeRaw`RESET app.tenant_id`;
  }
}
```

---

## Subscription Management

### Stripe Subscriptions

```typescript
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

// Create subscription
async function createSubscription(
  customerId: string,
  priceId: string,
  trialDays?: number
) {
  const subscription = await stripe.subscriptions.create({
    customer: customerId,
    items: [{ price: priceId }],
    trial_period_days: trialDays,
    payment_behavior: 'default_incomplete',
    payment_settings: { save_default_payment_method: 'on_subscription' },
    expand: ['latest_invoice.payment_intent'],
  });

  return subscription;
}

// Update subscription
async function updateSubscription(subscriptionId: string, newPriceId: string) {
  const subscription = await stripe.subscriptions.retrieve(subscriptionId);

  return stripe.subscriptions.update(subscriptionId, {
    items: [
      {
        id: subscription.items.data[0].id,
        price: newPriceId,
      },
    ],
    proration_behavior: 'create_prorations',
  });
}

// Cancel subscription
async function cancelSubscription(subscriptionId: string, immediate = false) {
  if (immediate) {
    return stripe.subscriptions.cancel(subscriptionId);
  }

  return stripe.subscriptions.update(subscriptionId, {
    cancel_at_period_end: true,
  });
}

// Handle subscription webhooks
async function handleSubscriptionWebhook(event: Stripe.Event) {
  switch (event.type) {
    case 'customer.subscription.created':
    case 'customer.subscription.updated': {
      const subscription = event.data.object as Stripe.Subscription;
      await syncSubscription(subscription);
      break;
    }

    case 'customer.subscription.deleted': {
      const subscription = event.data.object as Stripe.Subscription;
      await deactivateSubscription(subscription.id);
      break;
    }

    case 'invoice.payment_succeeded': {
      const invoice = event.data.object as Stripe.Invoice;
      await recordPayment(invoice);
      break;
    }

    case 'invoice.payment_failed': {
      const invoice = event.data.object as Stripe.Invoice;
      await handleFailedPayment(invoice);
      break;
    }
  }
}

// Sync subscription to database
async function syncSubscription(subscription: Stripe.Subscription) {
  const planMapping: Record<string, string> = {
    price_starter: 'starter',
    price_pro: 'pro',
    price_enterprise: 'enterprise',
  };

  await prisma.organization.update({
    where: { stripeCustomerId: subscription.customer as string },
    data: {
      subscriptionId: subscription.id,
      subscriptionStatus: subscription.status,
      plan: planMapping[subscription.items.data[0].price.id] || 'free',
      currentPeriodEnd: new Date(subscription.current_period_end * 1000),
    },
  });
}
```

### Usage-Based Billing

```typescript
// Track usage
async function recordUsage(
  subscriptionItemId: string,
  quantity: number,
  timestamp?: number
) {
  await stripe.subscriptionItems.createUsageRecord(subscriptionItemId, {
    quantity,
    timestamp: timestamp || Math.floor(Date.now() / 1000),
    action: 'increment',
  });
}

// Usage tracking service
class UsageTracker {
  private buffer: Map<string, number> = new Map();
  private flushInterval: NodeJS.Timeout;

  constructor(private flushIntervalMs = 60000) {
    this.flushInterval = setInterval(() => this.flush(), flushIntervalMs);
  }

  track(orgId: string, metric: string, amount = 1) {
    const key = `${orgId}:${metric}`;
    this.buffer.set(key, (this.buffer.get(key) || 0) + amount);
  }

  async flush() {
    const entries = Array.from(this.buffer.entries());
    this.buffer.clear();

    for (const [key, amount] of entries) {
      const [orgId, metric] = key.split(':');

      // Record to database
      await prisma.usageRecord.create({
        data: {
          organizationId: orgId,
          metric,
          amount,
          timestamp: new Date(),
        },
      });

      // Report to Stripe (for metered billing)
      const org = await prisma.organization.findUnique({
        where: { id: orgId },
        select: { subscriptionItemId: true },
      });

      if (org?.subscriptionItemId) {
        await recordUsage(org.subscriptionItemId, amount);
      }
    }
  }
}
```

---

## Feature Flags & Entitlements

```typescript
interface Plan {
  id: string;
  name: string;
  features: {
    [key: string]: boolean | number;
  };
  limits: {
    [key: string]: number;
  };
}

const plans: Record<string, Plan> = {
  free: {
    id: 'free',
    name: 'Free',
    features: {
      basicAnalytics: true,
      advancedAnalytics: false,
      apiAccess: false,
      customBranding: false,
    },
    limits: {
      projects: 3,
      teamMembers: 1,
      storage: 100, // MB
      apiCalls: 1000,
    },
  },
  pro: {
    id: 'pro',
    name: 'Pro',
    features: {
      basicAnalytics: true,
      advancedAnalytics: true,
      apiAccess: true,
      customBranding: false,
    },
    limits: {
      projects: 20,
      teamMembers: 10,
      storage: 10000, // MB
      apiCalls: 100000,
    },
  },
  enterprise: {
    id: 'enterprise',
    name: 'Enterprise',
    features: {
      basicAnalytics: true,
      advancedAnalytics: true,
      apiAccess: true,
      customBranding: true,
    },
    limits: {
      projects: -1, // Unlimited
      teamMembers: -1,
      storage: -1,
      apiCalls: -1,
    },
  },
};

// Check feature access
function hasFeature(org: Organization, feature: string): boolean {
  const plan = plans[org.plan];
  return plan?.features[feature] ?? false;
}

// Check limit
function checkLimit(org: Organization, resource: string, current: number): boolean {
  const plan = plans[org.plan];
  const limit = plan?.limits[resource] ?? 0;
  return limit === -1 || current < limit;
}

// Middleware for feature gating
function requireFeature(feature: string) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const org = await getOrganization(req.tenantId);

    if (!hasFeature(org, feature)) {
      return res.status(403).json({
        error: 'Feature not available',
        upgrade: true,
        requiredPlan: getMinimumPlanForFeature(feature),
      });
    }

    next();
  };
}
```

---

## User Onboarding

```typescript
interface OnboardingStep {
  id: string;
  title: string;
  completed: boolean;
  skippable: boolean;
}

async function getOnboardingProgress(userId: string) {
  const user = await prisma.user.findUnique({
    where: { id: userId },
    include: { organization: true },
  });

  const steps: OnboardingStep[] = [
    {
      id: 'profile',
      title: 'Complete your profile',
      completed: !!user.name && !!user.avatar,
      skippable: true,
    },
    {
      id: 'invite_team',
      title: 'Invite team members',
      completed: user.organization.memberCount > 1,
      skippable: true,
    },
    {
      id: 'create_project',
      title: 'Create your first project',
      completed: user.organization.projectCount > 0,
      skippable: false,
    },
    {
      id: 'connect_integration',
      title: 'Connect an integration',
      completed: user.organization.integrationCount > 0,
      skippable: true,
    },
  ];

  const completedCount = steps.filter((s) => s.completed).length;

  return {
    steps,
    progress: Math.round((completedCount / steps.length) * 100),
    isComplete: steps.every((s) => s.completed || s.skippable),
  };
}
```

---

## Related Skills

- [[system-design]] - SaaS architecture
- [[security-practices]] - Multi-tenant security
- [[database]] - Tenant data isolation

