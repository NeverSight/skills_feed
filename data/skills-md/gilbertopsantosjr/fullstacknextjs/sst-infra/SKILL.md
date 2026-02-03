---
name: sst-infra
description: Guide for AWS serverless infrastructure using SST v3 (Serverless Stack). Use when configuring deployment, creating stacks, managing secrets, setting up CI/CD, or deploying Next.js applications to AWS Lambda with DynamoDB.
---

# SST v3 Infrastructure

## Project Structure

```
project/
├── sst.config.ts          # Main SST config
├── stacks/
│   ├── dynamodb.ts        # Database stack
│   ├── nextjs.ts          # Next.js deployment
│   └── environment.ts     # Environment config
└── open-next.config.ts    # Lambda streaming config
```

## Main Config

```typescript
// sst.config.ts
export default $config({
  app(input) {
    return {
      name: 'my-app',
      removal: input?.stage === 'prod' ? 'retain' : 'remove',
      protect: ['prod'].includes(input?.stage ?? ''),
      home: 'aws',
      providers: { aws: { region: 'us-east-1' } },
    }
  },
  async run() {
    const { table } = await import('./stacks/dynamodb')
    const { site } = await import('./stacks/nextjs')
    return { url: site.url, tableName: table.name }
  },
})
```

## DynamoDB Stack

```typescript
// stacks/dynamodb.ts
export const table = new sst.aws.Dynamo('Table', {
  fields: {
    pk: 'string', sk: 'string',
    gsi1pk: 'string', gsi1sk: 'string',
  },
  primaryIndex: { hashKey: 'pk', rangeKey: 'sk' },
  globalIndexes: {
    gsi1: { hashKey: 'gsi1pk', rangeKey: 'gsi1sk' },
  },
  transform: {
    table: (args) => { args.billingMode = 'PAY_PER_REQUEST' },
  },
})
```

## Next.js Stack

```typescript
// stacks/nextjs.ts
import { table } from './dynamodb'

export const site = new sst.aws.Nextjs('Site', {
  path: 'apps/web',
  link: [table],
  environment: {
    TABLE_NAME: table.name,
  },
  domain: {
    name: `${$app.stage === 'prod' ? '' : `${$app.stage}.`}myapp.com`,
    dns: sst.aws.dns({ zone: 'myapp.com' }),
  },
})
```

## OpenNext Config

```typescript
// open-next.config.ts
import type { OpenNextConfig } from 'open-next/types/open-next'

const config: OpenNextConfig = {
  default: {
    override: { wrapper: 'aws-lambda-streaming' },
  },
}
export default config
```

## Commands

```bash
# Development (local Lambda)
npx sst dev --stage dev

# Deploy
npx sst deploy --stage dev
npx sst deploy --stage prod

# Remove
npx sst remove --stage dev

# Outputs
npx sst outputs --stage dev

# Secrets
npx sst secret set AUTH_SECRET "value" --stage dev
npx sst secret list --stage dev
```

## Environment Stages

| Stage | Domain | Protection | Removal |
|-------|--------|------------|---------|
| dev | dev.app.com | No | Remove |
| test | test.app.com | No | Remove |
| prod | app.com | Yes | Retain |

## CI/CD (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  workflow_dispatch:
    inputs:
      stage:
        type: choice
        options: [dev, test, prod]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
      - uses: actions/setup-node@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1
      - run: pnpm install --frozen-lockfile
      - run: npx sst deploy --stage ${{ inputs.stage }}
```



## Local Development

```bash
# DynamoDB Local
docker run -p 8000:8000 amazon/dynamodb-local

# Environment
TABLE_NAME=dev-Table
DYNAMODB_LOCAL=true
```
