---
name: cloud-platforms
description: AWS, GCP, Azure services and cloud-native development
domain: development-stacks
version: 1.0.0
tags: [aws, gcp, azure, serverless, lambda, s3, cloudflare]
triggers:
  keywords:
    primary: [aws, gcp, azure, cloud, serverless, lambda, s3]
    secondary: [ec2, cloudflare, vercel, netlify, dynamodb, cloud function]
  context_boost: [deploy, infrastructure, scale, hosting]
  context_penalty: [frontend, ui, design]
  priority: high
---

# Cloud Platforms

## Overview

Cloud services, serverless architectures, and cloud-native development patterns for AWS, GCP, and Azure.

---

## AWS

### Lambda Functions

```typescript
// lambda/handler.ts
import { APIGatewayProxyHandler, APIGatewayProxyResult } from 'aws-lambda';

export const handler: APIGatewayProxyHandler = async (event) => {
  try {
    const body = JSON.parse(event.body || '{}');

    // Business logic
    const result = await processRequest(body);

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify(result),
    };
  } catch (error) {
    console.error('Handler error:', error);

    return {
      statusCode: error.statusCode || 500,
      body: JSON.stringify({
        error: error.message || 'Internal server error',
      }),
    };
  }
};

// With middleware (middy)
import middy from '@middy/core';
import jsonBodyParser from '@middy/http-json-body-parser';
import httpErrorHandler from '@middy/http-error-handler';
import cors from '@middy/http-cors';

const baseHandler = async (event) => {
  // event.body is already parsed
  return {
    statusCode: 200,
    body: JSON.stringify({ data: event.body }),
  };
};

export const handler = middy(baseHandler)
  .use(jsonBodyParser())
  .use(httpErrorHandler())
  .use(cors());
```

### S3 Operations

```typescript
import { S3Client, PutObjectCommand, GetObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';

const s3 = new S3Client({ region: process.env.AWS_REGION });

// Upload file
async function uploadFile(key: string, body: Buffer, contentType: string) {
  await s3.send(new PutObjectCommand({
    Bucket: process.env.S3_BUCKET,
    Key: key,
    Body: body,
    ContentType: contentType,
  }));

  return `https://${process.env.S3_BUCKET}.s3.amazonaws.com/${key}`;
}

// Generate presigned upload URL
async function getUploadUrl(key: string, contentType: string, expiresIn = 3600) {
  const command = new PutObjectCommand({
    Bucket: process.env.S3_BUCKET,
    Key: key,
    ContentType: contentType,
  });

  return getSignedUrl(s3, command, { expiresIn });
}

// Generate presigned download URL
async function getDownloadUrl(key: string, expiresIn = 3600) {
  const command = new GetObjectCommand({
    Bucket: process.env.S3_BUCKET,
    Key: key,
  });

  return getSignedUrl(s3, command, { expiresIn });
}
```

### DynamoDB

```typescript
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import {
  DynamoDBDocumentClient,
  PutCommand,
  GetCommand,
  QueryCommand,
  UpdateCommand,
} from '@aws-sdk/lib-dynamodb';

const client = new DynamoDBClient({ region: process.env.AWS_REGION });
const docClient = DynamoDBDocumentClient.from(client);

// Single table design patterns
const TABLE_NAME = process.env.DYNAMODB_TABLE;

// Put item
async function createUser(user: User) {
  await docClient.send(new PutCommand({
    TableName: TABLE_NAME,
    Item: {
      PK: `USER#${user.id}`,
      SK: `PROFILE#${user.id}`,
      GSI1PK: `EMAIL#${user.email}`,
      GSI1SK: `USER#${user.id}`,
      ...user,
      createdAt: new Date().toISOString(),
    },
    ConditionExpression: 'attribute_not_exists(PK)',
  }));
}

// Get item
async function getUser(userId: string) {
  const result = await docClient.send(new GetCommand({
    TableName: TABLE_NAME,
    Key: {
      PK: `USER#${userId}`,
      SK: `PROFILE#${userId}`,
    },
  }));

  return result.Item;
}

// Query with GSI
async function getUserByEmail(email: string) {
  const result = await docClient.send(new QueryCommand({
    TableName: TABLE_NAME,
    IndexName: 'GSI1',
    KeyConditionExpression: 'GSI1PK = :pk',
    ExpressionAttributeValues: {
      ':pk': `EMAIL#${email}`,
    },
  }));

  return result.Items?.[0];
}

// Update with conditions
async function updateUserStatus(userId: string, status: string) {
  await docClient.send(new UpdateCommand({
    TableName: TABLE_NAME,
    Key: {
      PK: `USER#${userId}`,
      SK: `PROFILE#${userId}`,
    },
    UpdateExpression: 'SET #status = :status, updatedAt = :now',
    ConditionExpression: 'attribute_exists(PK)',
    ExpressionAttributeNames: {
      '#status': 'status',
    },
    ExpressionAttributeValues: {
      ':status': status,
      ':now': new Date().toISOString(),
    },
  }));
}
```

### SQS & SNS

```typescript
import { SQSClient, SendMessageCommand, ReceiveMessageCommand } from '@aws-sdk/client-sqs';
import { SNSClient, PublishCommand } from '@aws-sdk/client-sns';

const sqs = new SQSClient({ region: process.env.AWS_REGION });
const sns = new SNSClient({ region: process.env.AWS_REGION });

// Send to SQS
async function queueJob(job: Job) {
  await sqs.send(new SendMessageCommand({
    QueueUrl: process.env.SQS_QUEUE_URL,
    MessageBody: JSON.stringify(job),
    MessageAttributes: {
      type: {
        DataType: 'String',
        StringValue: job.type,
      },
    },
  }));
}

// Publish to SNS
async function publishEvent(topic: string, event: Event) {
  await sns.send(new PublishCommand({
    TopicArn: `arn:aws:sns:${process.env.AWS_REGION}:${process.env.AWS_ACCOUNT}:${topic}`,
    Message: JSON.stringify(event),
    MessageAttributes: {
      eventType: {
        DataType: 'String',
        StringValue: event.type,
      },
    },
  }));
}

// Lambda SQS handler
export const sqsHandler = async (event: SQSEvent) => {
  for (const record of event.Records) {
    const job = JSON.parse(record.body);
    await processJob(job);
  }
};
```

---

## Google Cloud Platform

### Cloud Functions

```typescript
import { HttpFunction, CloudEvent } from '@google-cloud/functions-framework';

// HTTP function
export const httpHandler: HttpFunction = async (req, res) => {
  res.set('Access-Control-Allow-Origin', '*');

  if (req.method === 'OPTIONS') {
    res.status(204).send('');
    return;
  }

  try {
    const result = await processRequest(req.body);
    res.json(result);
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Internal error' });
  }
};

// Pub/Sub triggered function
export const pubsubHandler = async (event: CloudEvent<{ message: { data: string } }>) => {
  const data = JSON.parse(
    Buffer.from(event.data.message.data, 'base64').toString()
  );

  await processMessage(data);
};

// Cloud Storage triggered
export const storageHandler = async (event: CloudEvent<StorageObjectData>) => {
  const file = event.data;
  console.log(`Processing file: ${file.bucket}/${file.name}`);

  await processFile(file.bucket, file.name);
};
```

### Firestore

```typescript
import { Firestore, FieldValue } from '@google-cloud/firestore';

const db = new Firestore();

// Create document
async function createUser(user: User) {
  const docRef = db.collection('users').doc(user.id);
  await docRef.set({
    ...user,
    createdAt: FieldValue.serverTimestamp(),
  });
}

// Query with filters
async function getActiveUsers(limit = 10) {
  const snapshot = await db.collection('users')
    .where('status', '==', 'active')
    .orderBy('createdAt', 'desc')
    .limit(limit)
    .get();

  return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
}

// Transaction
async function transferCredits(fromId: string, toId: string, amount: number) {
  await db.runTransaction(async (t) => {
    const fromRef = db.collection('accounts').doc(fromId);
    const toRef = db.collection('accounts').doc(toId);

    const fromDoc = await t.get(fromRef);
    const fromBalance = fromDoc.data()?.balance || 0;

    if (fromBalance < amount) {
      throw new Error('Insufficient balance');
    }

    t.update(fromRef, { balance: FieldValue.increment(-amount) });
    t.update(toRef, { balance: FieldValue.increment(amount) });
  });
}

// Real-time listener
function subscribeToUser(userId: string, callback: (user: User) => void) {
  return db.collection('users').doc(userId).onSnapshot((doc) => {
    if (doc.exists) {
      callback({ id: doc.id, ...doc.data() } as User);
    }
  });
}
```

---

## Serverless Framework

### serverless.yml

```yaml
service: my-api

provider:
  name: aws
  runtime: nodejs18.x
  region: ${opt:region, 'us-east-1'}
  stage: ${opt:stage, 'dev'}
  environment:
    TABLE_NAME: ${self:service}-${self:provider.stage}
    BUCKET_NAME: ${self:service}-uploads-${self:provider.stage}
  iam:
    role:
      statements:
        - Effect: Allow
          Action:
            - dynamodb:Query
            - dynamodb:Scan
            - dynamodb:GetItem
            - dynamodb:PutItem
            - dynamodb:UpdateItem
            - dynamodb:DeleteItem
          Resource:
            - !GetAtt DynamoDBTable.Arn
            - !Join ['/', [!GetAtt DynamoDBTable.Arn, 'index/*']]
        - Effect: Allow
          Action:
            - s3:PutObject
            - s3:GetObject
          Resource:
            - !Join ['/', [!GetAtt S3Bucket.Arn, '*']]

functions:
  api:
    handler: src/handlers/api.handler
    events:
      - http:
          path: /{proxy+}
          method: ANY
          cors: true

  processQueue:
    handler: src/handlers/queue.handler
    events:
      - sqs:
          arn: !GetAtt Queue.Arn
          batchSize: 10

  scheduledTask:
    handler: src/handlers/scheduled.handler
    events:
      - schedule: rate(1 hour)

resources:
  Resources:
    DynamoDBTable:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: ${self:provider.environment.TABLE_NAME}
        BillingMode: PAY_PER_REQUEST
        AttributeDefinitions:
          - AttributeName: PK
            AttributeType: S
          - AttributeName: SK
            AttributeType: S
          - AttributeName: GSI1PK
            AttributeType: S
          - AttributeName: GSI1SK
            AttributeType: S
        KeySchema:
          - AttributeName: PK
            KeyType: HASH
          - AttributeName: SK
            KeyType: RANGE
        GlobalSecondaryIndexes:
          - IndexName: GSI1
            KeySchema:
              - AttributeName: GSI1PK
                KeyType: HASH
              - AttributeName: GSI1SK
                KeyType: RANGE
            Projection:
              ProjectionType: ALL

    S3Bucket:
      Type: AWS::S3::Bucket
      Properties:
        BucketName: ${self:provider.environment.BUCKET_NAME}

    Queue:
      Type: AWS::SQS::Queue
      Properties:
        QueueName: ${self:service}-${self:provider.stage}-queue

plugins:
  - serverless-esbuild
  - serverless-offline
```

---

## Cloudflare Workers

```typescript
// worker.ts
export interface Env {
  KV: KVNamespace;
  DB: D1Database;
  BUCKET: R2Bucket;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext) {
    const url = new URL(request.url);

    // Router
    if (url.pathname.startsWith('/api/')) {
      return handleAPI(request, env);
    }

    // Static assets from R2
    if (url.pathname.startsWith('/assets/')) {
      const key = url.pathname.slice(8);
      const object = await env.BUCKET.get(key);

      if (!object) {
        return new Response('Not found', { status: 404 });
      }

      return new Response(object.body, {
        headers: {
          'Content-Type': object.httpMetadata?.contentType || 'application/octet-stream',
          'Cache-Control': 'public, max-age=31536000',
        },
      });
    }

    return new Response('Not found', { status: 404 });
  },
};

async function handleAPI(request: Request, env: Env) {
  const url = new URL(request.url);

  // KV operations
  if (url.pathname === '/api/cache') {
    const key = url.searchParams.get('key');

    if (request.method === 'GET') {
      const value = await env.KV.get(key);
      return Response.json({ value });
    }

    if (request.method === 'PUT') {
      const { value, ttl } = await request.json();
      await env.KV.put(key, value, { expirationTtl: ttl });
      return Response.json({ success: true });
    }
  }

  // D1 (SQLite) operations
  if (url.pathname === '/api/users') {
    if (request.method === 'GET') {
      const { results } = await env.DB.prepare(
        'SELECT * FROM users ORDER BY created_at DESC LIMIT 10'
      ).all();

      return Response.json(results);
    }

    if (request.method === 'POST') {
      const { name, email } = await request.json();

      const result = await env.DB.prepare(
        'INSERT INTO users (name, email) VALUES (?, ?) RETURNING *'
      ).bind(name, email).first();

      return Response.json(result, { status: 201 });
    }
  }

  return new Response('Not found', { status: 404 });
}
```

---

## Related Skills

- [[devops-cicd]] - Cloud deployments
- [[system-design]] - Cloud architecture
- [[reliability-engineering]] - Cloud reliability

