---
name: aws-skills
description: AWS development with CDK best practices, serverless patterns, cost optimization, and event-driven architecture. Use when deploying to AWS, writing Lambda functions, configuring API Gateway, working with DynamoDB, S3, or any AWS service.
---

# AWS Development Skills

## AWS CDK Best Practices

### Project Structure
```
infrastructure/
├── bin/
│   └── app.ts              # CDK app entry point
├── lib/
│   ├── stacks/
│   │   ├── api-stack.ts
│   │   ├── database-stack.ts
│   │   └── storage-stack.ts
│   ├── constructs/
│   │   ├── lambda-function.ts
│   │   └── api-gateway.ts
│   └── config/
│       └── environment.ts
├── lambda/
│   └── handlers/
├── cdk.json
└── package.json
```

### Stack Definition
```typescript
import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import { Construct } from 'constructs';

interface ApiStackProps extends cdk.StackProps {
  environment: string;
  domainName?: string;
}

export class ApiStack extends cdk.Stack {
  public readonly api: apigateway.RestApi;

  constructor(scope: Construct, id: string, props: ApiStackProps) {
    super(scope, id, props);

    const handler = new lambda.Function(this, 'ApiHandler', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'index.handler',
      code: lambda.Code.fromAsset('lambda/handlers'),
      environment: { NODE_ENV: props.environment },
      memorySize: 256,
      timeout: cdk.Duration.seconds(30),
    });

    this.api = new apigateway.RestApi(this, 'Api', {
      restApiName: `${props.environment}-api`,
      deployOptions: {
        stageName: props.environment,
        throttlingRateLimit: 1000,
        throttlingBurstLimit: 500,
      },
    });

    const integration = new apigateway.LambdaIntegration(handler);
    this.api.root.addMethod('GET', integration);
  }
}
```

## Serverless Patterns

### Lambda Best Practices
```typescript
import { APIGatewayProxyHandler } from 'aws-lambda';

// Initialize outside handler for connection reuse
const dynamodb = new DynamoDB.DocumentClient();

export const handler: APIGatewayProxyHandler = async (event) => {
  try {
    const body = JSON.parse(event.body || '{}');
    const result = await processRequest(body);
    return response(200, result);
  } catch (error) {
    console.error('Error:', error);
    return response(500, { error: 'Internal server error' });
  }
};

function response(statusCode: number, body: any) {
  return {
    statusCode,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
    },
    body: JSON.stringify(body),
  };
}
```

### DynamoDB Single-Table Design
```typescript
const table = new dynamodb.Table(this, 'Table', {
  partitionKey: { name: 'PK', type: dynamodb.AttributeType.STRING },
  sortKey: { name: 'SK', type: dynamodb.AttributeType.STRING },
  billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
});

// Access patterns
// User by ID:      PK=USER#123, SK=PROFILE
// User's orders:   PK=USER#123, SK=ORDER#timestamp
// Order by ID:     GSI1PK=ORDER#456, GSI1SK=ORDER#456
```

### Event-Driven with EventBridge
```typescript
const rule = new events.Rule(this, 'OrderCreatedRule', {
  eventPattern: {
    source: ['orders'],
    detailType: ['OrderCreated'],
  },
});

rule.addTarget(new targets.LambdaFunction(processOrderHandler));
rule.addTarget(new targets.SqsQueue(notificationQueue));
```

### SQS + Lambda Pattern
```typescript
const dlq = new sqs.Queue(this, 'DeadLetterQueue');

const queue = new sqs.Queue(this, 'ProcessingQueue', {
  visibilityTimeout: cdk.Duration.seconds(300),
  deadLetterQueue: { queue: dlq, maxReceiveCount: 3 },
});

processor.addEventSource(new SqsEventSource(queue, {
  batchSize: 10,
  maxBatchingWindow: cdk.Duration.seconds(5),
}));
```

## Cost Optimization

### Lambda Optimization
```typescript
const handler = new lambda.Function(this, 'Handler', {
  memorySize: 256,
  timeout: cdk.Duration.seconds(10),
  architecture: lambda.Architecture.ARM_64, // Cost savings
});
```

### S3 Lifecycle Rules
```typescript
const bucket = new s3.Bucket(this, 'Bucket', {
  lifecycleRules: [{
    transitions: [
      { storageClass: s3.StorageClass.INFREQUENT_ACCESS, transitionAfter: cdk.Duration.days(30) },
      { storageClass: s3.StorageClass.GLACIER, transitionAfter: cdk.Duration.days(90) },
    ],
    expiration: cdk.Duration.days(365),
  }],
});
```

## Security Best Practices

### IAM Least Privilege
```typescript
// Grant methods (preferred)
table.grantReadWriteData(handler);
bucket.grantRead(handler);
```

### Secrets Management
```typescript
const secret = secretsmanager.Secret.fromSecretNameV2(this, 'DbSecret', 'prod/db/credentials');
secret.grantRead(handler);
```

## Monitoring

### CloudWatch Alarms
```typescript
new cloudwatch.Alarm(this, 'LambdaErrors', {
  metric: handler.metricErrors(),
  threshold: 1,
  evaluationPeriods: 1,
});
```

### X-Ray Tracing
```typescript
const handler = new lambda.Function(this, 'Handler', {
  tracing: lambda.Tracing.ACTIVE,
});
```
