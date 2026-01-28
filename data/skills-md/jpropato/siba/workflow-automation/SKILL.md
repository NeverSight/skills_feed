---
name: workflow-automation
description: "Design and implement automated workflows combining visual logic with custom code. Create multi-step automations, integrate APIs, and build AI-native pipelines. Use when designing automation flows, integrating APIs, building event-driven systems, or creating LangChain-style AI workflows."
---

# 🔄 Workflow Automation

> Patterns for building robust automated workflows, inspired by [n8n](https://github.com/n8n-io/n8n) and modern automation platforms.

## When to Use This Skill

Use this skill when:

- Designing multi-step automation workflows
- Integrating multiple APIs and services
- Building event-driven systems
- Creating AI-augmented pipelines
- Handling errors in complex flows

---

## 1. Workflow Design Principles

### 1.1 Core Concepts

```
┌─────────────────────────────────────────────────────────────┐
│                      WORKFLOW                                │
│  ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐      │
│  │Trigger │───▶│  Node  │───▶│  Node  │───▶│ Action │      │
│  └────────┘    └────────┘    └────────┘    └────────┘      │
│       │              │              │              │        │
│       ▼              ▼              ▼              ▼        │
│  [Webhook]    [Transform]    [Condition]    [Send Email]   │
└─────────────────────────────────────────────────────────────┘
```

**Key Components**:

- **Trigger**: What starts the workflow
- **Node**: Individual processing step
- **Edge**: Connection between nodes
- **Action**: External effect (API call, email, etc.)

### 1.2 Trigger Types

```javascript
const TRIGGER_TYPES = {
  // Event-based
  webhook: {
    description: "HTTP request triggers workflow",
    use_case: "External integrations, form submissions",
    example: "POST /webhook/order-created",
  },

  // Time-based
  cron: {
    description: "Scheduled execution",
    use_case: "Reports, cleanup, sync jobs",
    example: "0 9 * * *", // Daily at 9 AM
  },

  // Change-based
  polling: {
    description: "Check for changes periodically",
    use_case: "Monitor RSS, check file changes",
    example: "Every 5 minutes check for new items",
  },

  // Message-based
  queue: {
    description: "Process from message queue",
    use_case: "Async processing, decoupling",
    example: "SQS, RabbitMQ, Redis Streams",
  },

  // Manual
  manual: {
    description: "User-initiated execution",
    use_case: "Testing, on-demand tasks",
    example: "Run workflow button",
  },
};
```

### 1.3 Node Types

```javascript
const NODE_TYPES = {
  // Data transformation
  transform: {
    description: "Modify data shape or values",
    operations: ["map", "filter", "merge", "split"],
  },

  // Flow control
  condition: {
    description: "Branch based on logic",
    operations: ["if/else", "switch", "filter"],
  },

  // External actions
  action: {
    description: "Interact with external services",
    operations: ["HTTP request", "database", "email", "API"],
  },

  // Sub-workflows
  subworkflow: {
    description: "Call another workflow",
    operations: ["invoke", "wait", "parallel"],
  },

  // Error handling
  errorHandler: {
    description: "Handle failures gracefully",
    operations: ["retry", "fallback", "notify"],
  },
};
```

---

## 2. Common Workflow Patterns

### 2.1 Sequential Pipeline

```javascript
// Simple A → B → C flow
const sequentialWorkflow = {
  trigger: { type: "webhook", path: "/process" },
  nodes: [
    {
      id: "fetch",
      type: "http",
      config: {
        method: "GET",
        url: "{{trigger.data.api_url}}",
      },
    },
    {
      id: "transform",
      type: "code",
      config: {
        code: `
          return items.map(item => ({
            id: item.id,
            name: item.name.toUpperCase(),
            processed: true
          }));
        `,
      },
    },
    {
      id: "save",
      type: "database",
      config: {
        operation: "insert",
        table: "processed_items",
        data: "{{transform.output}}",
      },
    },
  ],
};
```

### 2.2 Parallel Execution

```javascript
// Fan-out: Execute multiple nodes in parallel
const parallelWorkflow = {
  trigger: { type: "cron", schedule: "0 * * * *" },
  nodes: [
    {
      id: "parallel_group",
      type: "parallel",
      nodes: [
        {
          id: "fetch_users",
          type: "http",
          config: { url: "/api/users" },
        },
        {
          id: "fetch_orders",
          type: "http",
          config: { url: "/api/orders" },
        },
        {
          id: "fetch_products",
          type: "http",
          config: { url: "/api/products" },
        },
      ],
    },
    {
      id: "merge",
      type: "merge",
      config: {
        method: "append", // or "combine", "zip"
        inputs: ["fetch_users", "fetch_orders", "fetch_products"],
      },
    },
  ],
};
```

### 2.3 Conditional Branching

```javascript
const conditionalWorkflow = {
  trigger: { type: "webhook", path: "/order" },
  nodes: [
    {
      id: "check_value",
      type: "switch",
      config: {
        property: "{{trigger.data.total}}",
        rules: [
          { operator: "gte", value: 1000, output: "high_value" },
          { operator: "gte", value: 100, output: "medium_value" },
          { operator: "lt", value: 100, output: "low_value" },
        ],
      },
    },
    {
      id: "high_value",
      type: "action",
      onlyIf: "{{check_value.output}} === 'high_value'",
      config: {
        action: "notify_sales_team",
      },
    },
    {
      id: "medium_value",
      type: "action",
      onlyIf: "{{check_value.output}} === 'medium_value'",
      config: {
        action: "send_thank_you_email",
      },
    },
    {
      id: "low_value",
      type: "action",
      onlyIf: "{{check_value.output}} === 'low_value'",
      config: {
        action: "add_to_newsletter",
      },
    },
  ],
};
```

### 2.4 Loop/Iterator Pattern

```javascript
const loopWorkflow = {
  trigger: { type: "manual" },
  nodes: [
    {
      id: "fetch_items",
      type: "http",
      config: { url: "/api/items" },
    },
    {
      id: "process_each",
      type: "loop",
      config: {
        items: "{{fetch_items.data}}",
        batchSize: 10, // Process 10 at a time
        continueOnError: true,
      },
      nodes: [
        {
          id: "enrich",
          type: "http",
          config: {
            url: "/api/enrich/{{item.id}}",
          },
        },
        {
          id: "save",
          type: "database",
          config: {
            operation: "update",
            id: "{{item.id}}",
            data: "{{enrich.output}}",
          },
        },
      ],
    },
  ],
};
```

### 2.5 Wait/Delay Pattern

```javascript
const waitWorkflow = {
  trigger: { type: "webhook", path: "/signup" },
  nodes: [
    {
      id: "send_welcome",
      type: "email",
      config: {
        to: "{{trigger.data.email}}",
        template: "welcome",
      },
    },
    {
      id: "wait_24h",
      type: "wait",
      config: {
        duration: "24h",
        // Or: resumeAt: "{{trigger.data.preferred_time}}"
      },
    },
    {
      id: "send_onboarding",
      type: "email",
      config: {
        to: "{{trigger.data.email}}",
        template: "onboarding_tips",
      },
    },
  ],
};
```

---

## 3. Error Handling Patterns

### 3.1 Retry with Backoff

```javascript
const retryConfig = {
  retries: 3,
  backoff: "exponential", // linear, exponential, fixed
  initialDelay: 1000, // ms
  maxDelay: 30000, // ms
  retryOn: ["ECONNRESET", "ETIMEDOUT", "HTTP_5XX"],
};

const nodeWithRetry = {
  id: "api_call",
  type: "http",
  config: { url: "/api/external" },
  errorHandling: {
    retry: retryConfig,
    onMaxRetries: {
      action: "continue", // or "fail", "branch"
      fallbackValue: { data: [] },
    },
  },
};
```

### 3.2 Dead Letter Queue

```javascript
const workflowWithDLQ = {
  config: {
    onError: {
      action: "send_to_dlq",
      queue: "failed_workflows",
      includeContext: true, // Include full workflow state
    },
  },
  nodes: [
    /* ... */
  ],
};

// Separate workflow to process failed items
const dlqProcessor = {
  trigger: {
    type: "queue",
    queue: "failed_workflows",
  },
  nodes: [
    {
      id: "analyze",
      type: "code",
      config: {
        code: `
          const error = $input.error;
          const context = $input.context;
          
          // Classify error
          if (error.type === 'VALIDATION') {
            return { action: 'discard', reason: 'Bad data' };
          }
          if (error.type === 'RATE_LIMIT') {
            return { action: 'retry', delay: '1h' };
          }
          return { action: 'manual_review' };
        `,
      },
    },
  ],
};
```

### 3.3 Compensation/Rollback

```javascript
const sagaWorkflow = {
  name: "order_saga",
  nodes: [
    {
      id: "reserve_inventory",
      type: "api",
      compensate: {
        id: "release_inventory",
        type: "api",
        config: { method: "POST", url: "/inventory/release" },
      },
    },
    {
      id: "charge_payment",
      type: "api",
      compensate: {
        id: "refund_payment",
        type: "api",
        config: { method: "POST", url: "/payments/refund" },
      },
    },
    {
      id: "create_shipment",
      type: "api",
      compensate: {
        id: "cancel_shipment",
        type: "api",
        config: { method: "POST", url: "/shipments/cancel" },
      },
    },
  ],
  onError: {
    strategy: "compensate_all", // Run all compensations in reverse order
  },
};
```

---

## 4. Integration Patterns

### 4.1 API Integration Template

```javascript
const apiIntegration = {
  name: "github_integration",
  baseUrl: "https://api.github.com",
  auth: {
    type: "bearer",
    token: "{{secrets.GITHUB_TOKEN}}",
  },
  operations: {
    listRepos: {
      method: "GET",
      path: "/user/repos",
      params: {
        per_page: 100,
        sort: "updated",
      },
    },
    createIssue: {
      method: "POST",
      path: "/repos/{{owner}}/{{repo}}/issues",
      body: {
        title: "{{title}}",
        body: "{{body}}",
        labels: "{{labels}}",
      },
    },
  },
  rateLimiting: {
    requests: 5000,
    period: "1h",
    strategy: "queue", // queue, reject, throttle
  },
};
```

### 4.2 Webhook Handler

```javascript
const webhookHandler = {
  trigger: {
    type: "webhook",
    path: "/webhooks/stripe",
    method: "POST",
    authentication: {
      type: "signature",
      header: "stripe-signature",
      secret: "{{secrets.STRIPE_WEBHOOK_SECRET}}",
      algorithm: "sha256",
    },
  },
  nodes: [
    {
      id: "validate",
      type: "code",
      config: {
        code: `
          const event = $input.body;
          if (!['checkout.session.completed', 
                'payment_intent.succeeded'].includes(event.type)) {
            return { skip: true };
          }
          return event;
        `,
      },
    },
    {
      id: "route",
      type: "switch",
      config: {
        property: "{{validate.type}}",
        routes: {
          "checkout.session.completed": "handle_checkout",
          "payment_intent.succeeded": "handle_payment",
        },
      },
    },
  ],
};
```

---

## 5. AI-Native Workflows

### 5.1 LLM in Pipeline

```javascript
const aiWorkflow = {
  trigger: { type: "webhook", path: "/analyze" },
  nodes: [
    {
      id: "extract_text",
      type: "code",
      config: {
        code: "return { text: $input.document.content }",
      },
    },
    {
      id: "analyze_sentiment",
      type: "llm",
      config: {
        model: "gpt-4",
        prompt: `
          Analyze the sentiment of the following text.
          Return JSON: {"sentiment": "positive|negative|neutral", "confidence": 0-1}
          
          Text: {{extract_text.text}}
        `,
        responseFormat: "json",
      },
    },
    {
      id: "route_by_sentiment",
      type: "switch",
      config: {
        property: "{{analyze_sentiment.sentiment}}",
        routes: {
          negative: "escalate_to_support",
          positive: "send_thank_you",
          neutral: "archive",
        },
      },
    },
  ],
};
```

### 5.2 Agent Workflow

```javascript
const agentWorkflow = {
  trigger: { type: "webhook", path: "/research" },
  nodes: [
    {
      id: "research_agent",
      type: "agent",
      config: {
        model: "gpt-4",
        tools: ["web_search", "calculator", "code_interpreter"],
        maxIterations: 10,
        prompt: `
          Research the following topic and provide a comprehensive summary:
          {{trigger.topic}}
          
          Use the tools available to gather accurate, up-to-date information.
        `,
      },
    },
    {
      id: "format_report",
      type: "llm",
      config: {
        model: "gpt-4",
        prompt: `
          Format this research into a professional report with sections:
          - Executive Summary
          - Key Findings
          - Recommendations
          
          Research: {{research_agent.output}}
        `,
      },
    },
    {
      id: "send_report",
      type: "email",
      config: {
        to: "{{trigger.email}}",
        subject: "Research Report: {{trigger.topic}}",
        body: "{{format_report.output}}",
      },
    },
  ],
};
```

---

## 6. Workflow Best Practices

### 6.1 Design Checklist

- [ ] **Idempotency**: Can workflow run multiple times safely?
- [ ] **Error handling**: What happens when nodes fail?
- [ ] **Timeouts**: Are there appropriate timeouts?
- [ ] **Logging**: Is there enough observability?
- [ ] **Rate limits**: Are external APIs rate-limited?
- [ ] **Secrets**: Are credentials stored securely?
- [ ] **Testing**: Can workflow be tested in isolation?

### 6.2 Naming Conventions

```javascript
// Workflows: verb_noun or noun_verb
"sync_customers";
"process_orders";
"daily_report_generator";

// Nodes: action_target
"fetch_user_data";
"transform_to_csv";
"send_notification_email";

// Variables: lowercase_snake_case
"order_total";
"customer_email";
"processing_date";
```

### 6.3 Testing Workflows

```javascript
const workflowTest = {
  name: "order_processing_test",
  workflow: "process_order",
  testCases: [
    {
      name: "valid_order",
      input: {
        order_id: "test-123",
        items: [{ sku: "A1", qty: 2 }],
      },
      expectedOutput: {
        status: "processed",
      },
      mocks: {
        inventory_check: { available: true },
        payment_process: { success: true },
      },
    },
    {
      name: "out_of_stock",
      input: {
        order_id: "test-456",
        items: [{ sku: "B2", qty: 100 }],
      },
      expectedOutput: {
        status: "failed",
        reason: "insufficient_inventory",
      },
      mocks: {
        inventory_check: { available: false },
      },
    },
  ],
};
```

---

## Resource Links

- [n8n Documentation](https://docs.n8n.io/)
- [Temporal Workflows](https://temporal.io/)
- [Apache Airflow](https://airflow.apache.org/)
- [Zapier Automation Patterns](https://zapier.com/blog/automation-patterns/)
