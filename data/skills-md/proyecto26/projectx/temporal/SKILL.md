---
name: temporal
description: Temporal workflow orchestration. Use when working with durable workflows, activities, or the order processing pipeline in packages/workflows.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Temporal Workflow Development

## Package Location

Temporal workflows and activities are in `packages/workflows/`.

```
packages/workflows/
├── src/
│   ├── workflows/        # Workflow definitions
│   ├── activities/       # Activity implementations
│   ├── worker.ts         # Worker configuration
│   └── client.ts         # Temporal client
└── package.json
```

## Workflow Basics

Workflows are deterministic functions that orchestrate activities.

### Defining a Workflow

```typescript
// packages/workflows/src/workflows/order.workflow.ts
import {
  proxyActivities,
  sleep,
  defineSignal,
  setHandler,
  condition,
} from '@temporalio/workflow';
import type * as activities from '../activities';

const { processPayment, sendOrderConfirmation, updateInventory, notifyShipping } =
  proxyActivities<typeof activities>({
    startToCloseTimeout: '5 minutes',
    retry: {
      maximumAttempts: 3,
      initialInterval: '1 second',
      backoffCoefficient: 2,
    },
  });

export const cancelOrderSignal = defineSignal('cancelOrder');

export interface OrderWorkflowInput {
  orderId: string;
  customerId: string;
  items: Array<{ productId: string; quantity: number }>;
  total: number;
}

export async function orderWorkflow(input: OrderWorkflowInput): Promise<string> {
  let cancelled = false;

  setHandler(cancelOrderSignal, () => {
    cancelled = true;
  });

  // Step 1: Process payment
  const paymentResult = await processPayment({
    orderId: input.orderId,
    amount: input.total,
    customerId: input.customerId,
  });

  if (!paymentResult.success) {
    return 'PAYMENT_FAILED';
  }

  // Check for cancellation
  if (cancelled) {
    // Refund payment
    await refundPayment({ paymentId: paymentResult.paymentId });
    return 'CANCELLED';
  }

  // Step 2: Update inventory
  await updateInventory(input.items);

  // Step 3: Send confirmation email
  await sendOrderConfirmation({
    orderId: input.orderId,
    customerId: input.customerId,
  });

  // Step 4: Wait for shipping (with timeout)
  await sleep('1 hour');
  await notifyShipping({ orderId: input.orderId });

  return 'COMPLETED';
}
```

## Activities

Activities are the building blocks that perform actual work.

### Defining Activities

```typescript
// packages/workflows/src/activities/payment.activities.ts
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export interface ProcessPaymentInput {
  orderId: string;
  amount: number;
  customerId: string;
}

export interface ProcessPaymentResult {
  success: boolean;
  paymentId?: string;
  error?: string;
}

export async function processPayment(
  input: ProcessPaymentInput
): Promise<ProcessPaymentResult> {
  try {
    const paymentIntent = await stripe.paymentIntents.create({
      amount: Math.round(input.amount * 100),
      currency: 'usd',
      metadata: {
        orderId: input.orderId,
        customerId: input.customerId,
      },
    });

    return {
      success: true,
      paymentId: paymentIntent.id,
    };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Payment failed',
    };
  }
}

export async function refundPayment(input: { paymentId: string }): Promise<void> {
  await stripe.refunds.create({
    payment_intent: input.paymentId,
  });
}
```

## Worker Setup

```typescript
// packages/workflows/src/worker.ts
import { Worker } from '@temporalio/worker';
import * as activities from './activities';

async function run() {
  const worker = await Worker.create({
    workflowsPath: require.resolve('./workflows'),
    activities,
    taskQueue: 'order-processing',
    connection: {
      address: process.env.TEMPORAL_ADDRESS || 'localhost:7233',
    },
  });

  await worker.run();
}

run().catch(console.error);
```

## Client Usage in NestJS

```typescript
// apps/order/src/order/order.service.ts
import { Injectable } from '@nestjs/common';
import { Client, Connection } from '@temporalio/client';
import { orderWorkflow, cancelOrderSignal } from '@projectx/workflows';

@Injectable()
export class OrderService {
  private client: Client;

  async onModuleInit() {
    const connection = await Connection.connect({
      address: process.env.TEMPORAL_ADDRESS || 'localhost:7233',
    });
    this.client = new Client({ connection });
  }

  async createOrder(orderData: CreateOrderDto): Promise<string> {
    const orderId = generateOrderId();

    // Start workflow
    const handle = await this.client.workflow.start(orderWorkflow, {
      taskQueue: 'order-processing',
      workflowId: `order-${orderId}`,
      args: [{
        orderId,
        customerId: orderData.customerId,
        items: orderData.items,
        total: orderData.total,
      }],
    });

    return orderId;
  }

  async cancelOrder(orderId: string): Promise<void> {
    const handle = this.client.workflow.getHandle(`order-${orderId}`);
    await handle.signal(cancelOrderSignal);
  }

  async getOrderStatus(orderId: string): Promise<string> {
    const handle = this.client.workflow.getHandle(`order-${orderId}`);
    const description = await handle.describe();
    return description.status.name;
  }
}
```

## Query Workflow State

```typescript
// In workflow
import { defineQuery, setHandler } from '@temporalio/workflow';

export const getOrderStatusQuery = defineQuery<string>('getOrderStatus');

export async function orderWorkflow(input: OrderWorkflowInput): Promise<string> {
  let status = 'PENDING';

  setHandler(getOrderStatusQuery, () => status);

  status = 'PROCESSING_PAYMENT';
  await processPayment(/* ... */);

  status = 'UPDATING_INVENTORY';
  await updateInventory(/* ... */);

  // ...
}

// In client
const handle = client.workflow.getHandle(workflowId);
const status = await handle.query(getOrderStatusQuery);
```

## Docker Setup

The project includes Temporal in docker-compose.yml:

```bash
# Start Temporal server + UI
docker-compose up -d temporal temporal-ui

# Access Temporal UI
open http://localhost:8080
```

## Best Practices

1. **Keep workflows deterministic** - No direct I/O, random, or time-dependent operations
2. **Use activities for side effects** - All external calls go in activities
3. **Set appropriate timeouts** - Configure startToCloseTimeout for activities
4. **Handle signals gracefully** - Check for signals at appropriate points
5. **Use queries for state** - Don't expose internal state directly
6. **Version workflows** - Use workflow versioning for updates
7. **Test workflows** - Use Temporal's testing framework
