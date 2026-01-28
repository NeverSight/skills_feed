---
name: cdk-infrastructure
description: AWS CDK infrastructure development with TypeScript. Use when creating or modifying CDK stacks, constructs, DynamoDB tables, ECS/Fargate services, Lambda functions, S3 buckets, networking, IAM roles, or any CloudFormation resources. Covers configuration patterns, cross-stack references via SSM, naming conventions, and Bedrock AgentCore integration.
---

# AWS CDK Infrastructure Best Practices

## TypeScript

- Use strict type checking
- Import from `aws-cdk-lib` and `constructs`
- Use L2 constructs when available, L1 (Cfn*) when necessary

## Stack Organization

```
infrastructure/
├── bin/infrastructure.ts          # App entrypoint
├── lib/
│   ├── config.ts                  # Configuration loader
│   ├── infrastructure-stack.ts    # Network resources (deploy first)
│   ├── app-api-stack.ts           # Backend services
│   └── my-new-stack.ts            # New stacks go here
└── cdk.context.json               # Configuration
```

**Deployment Order:**
1. `InfrastructureStack` - VPC, ALB, ECS Cluster (always first)
2. Other stacks import network resources via SSM

## Configuration

Use the centralized config system:

```typescript
import { loadConfig, getResourceName, getStackEnv, applyStandardTags } from './config';

export class MyStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    const config = loadConfig(scope);
    super(scope, id, {
      ...props,
      env: getStackEnv(config),
      stackName: getResourceName(config, 'my-stack'),
    });
    applyStandardTags(this, config);
  }
}
```

For configuration patterns, see [references/configuration.md](references/configuration.md).

## Naming Conventions

**Resource Names:** Use `getResourceName()`:
```typescript
getResourceName(config, 'user-quotas')  // "bsu-agentcore-user-quotas"
```

**SSM Parameters:** Hierarchical naming:
```
/{projectPrefix}/{category}/{resource-type}
```

Categories: `/network/`, `/quota/`, `/cost-tracking/`, `/auth/`, `/frontend/`, `/gateway/`

## Cross-Stack References

**Export:**
```typescript
new ssm.StringParameter(this, 'VpcIdParam', {
  parameterName: `/${config.projectPrefix}/network/vpc-id`,
  stringValue: vpc.vpcId,
});
```

**Import:**
```typescript
const vpcId = ssm.StringParameter.valueForStringParameter(
  this,
  `/${config.projectPrefix}/network/vpc-id`
);
```

## DynamoDB Tables

- Always use PK + SK for flexibility
- Use `PAY_PER_REQUEST` billing
- Enable point-in-time recovery
- Environment-based removal policy

For table patterns, see [references/dynamodb.md](references/dynamodb.md).

## ECS/Fargate

- Import cluster from SSM
- Health checks mandatory
- Auto-scaling with CPU/memory targets
- Circuit breaker for rollback

For service patterns, see [references/ecs-fargate.md](references/ecs-fargate.md).

## Lambda

- Use ARM64 architecture (cost optimization)
- Role with least privilege
- Secrets Manager access requires wildcard suffix

For Lambda patterns, see [references/lambda.md](references/lambda.md).

## S3 Buckets

- Block public access
- Enable versioning
- Lifecycle rules for cost optimization
- Include account ID for global uniqueness

For bucket patterns, see [references/s3.md](references/s3.md).

## Security

- Separate security groups for ALB and ECS
- Private subnets for services
- IAM roles with SIDs for clarity
- Never hardcode secrets

For IAM patterns, see [references/iam.md](references/iam.md).

## Important Constraints

**AgentCore Names:** Use underscores, not hyphens:
```typescript
name: getResourceName(config, 'memory').replace(/-/g, '_')
```

**Secrets Manager ARN:** Include wildcard for random suffix:
```typescript
resources: [`${secret.secretArn}*`]
```

**Environment Removal Policy:**
```typescript
removalPolicy: config.environment === 'prod'
  ? cdk.RemovalPolicy.RETAIN
  : cdk.RemovalPolicy.DESTROY
```

## CDK Commands

```bash
cd infrastructure
npm install           # Install dependencies
npx cdk synth         # Synthesize CloudFormation
npx cdk deploy --all  # Deploy all stacks
npx cdk diff          # Preview changes
```
