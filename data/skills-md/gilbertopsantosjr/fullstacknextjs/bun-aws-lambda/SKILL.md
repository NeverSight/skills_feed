---
name: bun-aws-lambda
description: Bun AWS Lambda expert for creating, deploying, and optimizing Lambda functions using Bun runtime. Use when building Lambda handlers with Bun, setting up custom runtimes, creating container images for Lambda, configuring deployment artifacts, or converting Node.js Lambda handlers to Bun. Triggers on requests involving Bun + Lambda, serverless functions with Bun, Lambda event handling (API Gateway, SQS, SNS, EventBridge, S3, DynamoDB Streams), cold start optimization, or Lambda deployment patterns.
---

# Bun AWS Lambda Expert

Expert guidance for AWS Lambda functions using Bun runtime. Covers handler creation, deployment patterns, and Node.js migration.

## Handler Template

```typescript
import type { APIGatewayProxyEventV2, APIGatewayProxyResultV2 } from 'aws-lambda'

export async function handler(event: APIGatewayProxyEventV2): Promise<APIGatewayProxyResultV2> {
  try {
    const { pathParameters, body, queryStringParameters } = event
    const payload = body ? JSON.parse(body) : undefined

    // Business logic here

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ success: true }),
    }
  } catch (error) {
    console.error('Handler error:', error)
    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ error: 'Internal server error' }),
    }
  }
}
```

## Event Source Decision

```
Which event source?
├── HTTP API (API Gateway v2) → APIGatewayProxyEventV2
├── REST API (API Gateway v1) → APIGatewayProxyEvent
├── ALB → ALBEvent
├── SQS → SQSEvent (with SQSBatchResponse for partial failures)
├── SNS → SNSEvent
├── EventBridge → EventBridgeEvent<DetailType>
├── S3 → S3Event
├── DynamoDB Streams → DynamoDBStreamEvent
└── Scheduled (Cron) → ScheduledEvent
```

## Deployment Decision

```
How to deploy Bun Lambda?
├── Container Image (Recommended)
│   ├── Simplest setup
│   ├── Full control over runtime
│   └── Cold start: ~300-500ms
├── Custom Runtime Layer
│   ├── Smaller package size
│   ├── Faster cold starts (~100-200ms)
│   └── More complex setup
└── Node.js Runtime + Bun Build
    ├── Simplest if code is Node-compatible
    └── Use Bun only as bundler
```

## Container Image Quick Start

### Dockerfile

```dockerfile
FROM oven/bun:1 AS builder
WORKDIR /app
COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile --production
COPY src/ ./src/
RUN bun build src/handler.ts --outdir=dist --target=bun --minify

FROM public.ecr.aws/lambda/provided:al2023
RUN curl -fsSL https://bun.sh/install | bash
ENV PATH="/root/.bun/bin:${PATH}"
WORKDIR ${LAMBDA_TASK_ROOT}
COPY --from=builder /app/dist/ ./
COPY bootstrap ${LAMBDA_RUNTIME_DIR}/bootstrap
RUN chmod +x ${LAMBDA_RUNTIME_DIR}/bootstrap
CMD ["handler.handler"]
```

### Bootstrap (TypeScript)

```typescript
// bootstrap.ts
const RUNTIME_API = `http://${Bun.env.AWS_LAMBDA_RUNTIME_API}/2018-06-01/runtime`

const [moduleName, functionName] = (Bun.env._HANDLER ?? 'handler.handler').split('.')
const handlerModule = await import(`./${moduleName}.js`)
const handler = handlerModule[functionName]

while (true) {
  const next = await fetch(`${RUNTIME_API}/invocation/next`)
  const requestId = next.headers.get('Lambda-Runtime-Aws-Request-Id')!
  const event = await next.json()

  try {
    const result = await handler(event, { awsRequestId: requestId })
    await fetch(`${RUNTIME_API}/invocation/${requestId}/response`, {
      method: 'POST',
      body: JSON.stringify(result),
    })
  } catch (error) {
    await fetch(`${RUNTIME_API}/invocation/${requestId}/error`, {
      method: 'POST',
      body: JSON.stringify({ errorMessage: String(error) }),
    })
  }
}
```

## Bun-Specific Patterns

### Environment Variables

```typescript
const config = {
  dbUrl: Bun.env.DATABASE_URL!,
  apiKey: Bun.env.API_KEY!,
  stage: Bun.env.STAGE ?? 'dev',
}
```

### File Operations

```typescript
// Read JSON config
const config = await Bun.file('config.json').json()

// Write to /tmp
await Bun.write('/tmp/output.json', JSON.stringify(data))
```

### Native Fetch

```typescript
const response = await fetch('https://api.example.com/data', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(payload),
})
const data = await response.json()
```

### Hashing

```typescript
const hash = Bun.hash(content, 'sha256').toString(16)
```

## Cold Start Optimization

1. **Bundle with Bun**: Single file, tree-shaken
2. **Lazy initialization**: Load heavy deps on first request
3. **Use AWS SDK v3**: Modular imports
4. **Minimize dependencies**: Native fetch, no axios
5. **Consider provisioned concurrency**: For latency-critical

```typescript
// Lazy initialization pattern
let db: DatabaseClient | null = null

async function getDb() {
  if (!db) {
    const { DatabaseClient } = await import('./db')
    db = new DatabaseClient(Bun.env.DATABASE_URL!)
  }
  return db
}
```

## Best Practices

1. **Types**: Always use `aws-lambda` types for event/response
2. **Error Handling**: Catch all errors, return proper HTTP status
3. **Logging**: Use `console.error` for errors (CloudWatch compatible)
4. **Validation**: Validate input early, fail fast
5. **Idempotency**: Design for retries on async event sources
6. **Timeouts**: Set appropriate Lambda timeout for use case

## References

Detailed patterns and examples:

- **[event-sources.md](references/event-sources.md)**: Event structures for API Gateway, SQS, SNS, EventBridge, S3, DynamoDB Streams
- **[deployment-patterns.md](references/deployment-patterns.md)**: Container images, custom runtime layers, IaC templates (CDK, SAM, Terraform, SST)
- **[nodejs-migration.md](references/nodejs-migration.md)**: Converting Node.js handlers to Bun, API compatibility

## Skill Interface

When using this skill, provide:

```json
{
  "lambdaDescription": "What the function does, inputs, outputs, event source",
  "bunConstraints": "Bun version, ESM/CJS, HTTP framework preferences",
  "deploymentContext": "Container image, Lambda layer, API Gateway, SQS trigger, etc.",
  "existingCode": "(optional) Node.js code to convert",
  "nonFunctionalRequirements": "(optional) Latency, cold start, observability needs"
}
```

Response includes:
- **handlerCode**: Complete Bun Lambda handler code
- **runtimeNotes**: Bun-specific considerations and choices
- **deploymentHints**: IaC integration advice
- **nextSteps**: Testing, hardening, observability suggestions
