---
name: aws-cli
description: This skill should be used when users need to interact with AWS services via CLI. It covers all AWS services including EC2, ECS, EKS, Lambda, S3, RDS, DynamoDB, VPC, Route53, CloudFront, Bedrock, Support, Billing, and more. Supports querying, creating, modifying, deleting resources, monitoring, debugging, and cost analysis. Triggers on requests mentioning AWS, cloud resources, or specific AWS service names.
---

# AWS CLI Skill

This skill enables comprehensive AWS cloud infrastructure management using the AWS CLI tool.

## Environment

- **Default Region**: `us-east-1`
- **AWS CLI**: Pre-configured with full account permissions
- **Account**: SimplexAI AWS account (ID: 830101142436)

## Safety Protocol

### Dangerous Operations Requiring Confirmation

Before executing any of the following operations, explicitly confirm with the user:

- **Delete operations**: `delete-*`, `remove-*`, `terminate-*`, `deregister-*`
- **Destructive modifications**: `modify-*` on production resources, `update-*` that changes critical settings
- **State changes**: `stop-*`, `reboot-*` on production instances
- **Security changes**: IAM policy modifications, security group rule changes
- **Cost implications**: Creating expensive resources (large EC2 instances, NAT gateways, etc.)

### Confirmation Format

```
⚠️ 危险操作确认

操作: [具体操作描述]
影响: [潜在影响说明]
资源: [受影响的资源标识]

是否继续执行？
```

## Common Operations Reference

### Compute Services

#### EC2

```bash
# List instances
aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId,State.Name,InstanceType,Tags[?Key==`Name`].Value|[0]]' --output table

# Instance state management
aws ec2 start-instances --instance-ids <id>
aws ec2 stop-instances --instance-ids <id>
aws ec2 reboot-instances --instance-ids <id>
```

#### ECS

```bash
# List clusters and services
aws ecs list-clusters
aws ecs list-services --cluster <cluster-name>
aws ecs describe-services --cluster <cluster-name> --services <service-name>

# View running tasks
aws ecs list-tasks --cluster <cluster-name> --service-name <service-name>
aws ecs describe-tasks --cluster <cluster-name> --tasks <task-arn>

# Force new deployment
aws ecs update-service --cluster <cluster-name> --service <service-name> --force-new-deployment
```

#### EKS

```bash
# List clusters
aws eks list-clusters
aws eks describe-cluster --name <cluster-name>

# Update kubeconfig
aws eks update-kubeconfig --name <cluster-name> --region us-east-1
```

#### Lambda

```bash
# List functions
aws lambda list-functions --query 'Functions[].[FunctionName,Runtime,LastModified]' --output table

# Invoke function
aws lambda invoke --function-name <name> --payload '{}' response.json

# View logs
aws logs tail /aws/lambda/<function-name> --follow
```

### Storage Services

#### S3

```bash
# List buckets and objects
aws s3 ls
aws s3 ls s3://<bucket-name>/ --recursive --human-readable

# Copy and sync
aws s3 cp <local-file> s3://<bucket>/<key>
aws s3 sync <local-dir> s3://<bucket>/<prefix>

# Bucket info
aws s3api get-bucket-location --bucket <bucket-name>
aws s3api get-bucket-versioning --bucket <bucket-name>
```

#### ECR

```bash
# List repositories
aws ecr describe-repositories --query 'repositories[].[repositoryName,repositoryUri]' --output table

# List images in repository
aws ecr describe-images --repository-name simplexai/<service> --query 'imageDetails | sort_by(@, &imagePushedAt) | [-10:].[imageTags[0],imagePushedAt]' --output table

# Get login token
aws ecr get-login-password --region us-east-1
```

### Database Services

#### RDS

```bash
# List instances
aws rds describe-db-instances --query 'DBInstances[].[DBInstanceIdentifier,DBInstanceClass,Engine,DBInstanceStatus]' --output table

# Instance details
aws rds describe-db-instances --db-instance-identifier <id>

# Snapshots
aws rds describe-db-snapshots --db-instance-identifier <id>
```

#### DynamoDB

```bash
# List tables
aws dynamodb list-tables

# Table info
aws dynamodb describe-table --table-name <table>

# Query/scan
aws dynamodb scan --table-name <table> --limit 10
```

#### ElastiCache

```bash
# List clusters
aws elasticache describe-cache-clusters
aws elasticache describe-replication-groups
```

### Network Services

#### VPC

```bash
# List VPCs and subnets
aws ec2 describe-vpcs --query 'Vpcs[].[VpcId,CidrBlock,Tags[?Key==`Name`].Value|[0]]' --output table
aws ec2 describe-subnets --query 'Subnets[].[SubnetId,VpcId,CidrBlock,AvailabilityZone]' --output table

# Security groups
aws ec2 describe-security-groups --query 'SecurityGroups[].[GroupId,GroupName,VpcId]' --output table
```

#### Route53

```bash
# List hosted zones
aws route53 list-hosted-zones

# List records
aws route53 list-resource-record-sets --hosted-zone-id <zone-id>
```

#### CloudFront

```bash
# List distributions
aws cloudfront list-distributions --query 'DistributionList.Items[].[Id,DomainName,Status]' --output table

# Invalidate cache
aws cloudfront create-invalidation --distribution-id <id> --paths "/*"
```

### Monitoring & Logging

#### CloudWatch

```bash
# List log groups
aws logs describe-log-groups --query 'logGroups[].[logGroupName,storedBytes]' --output table

# Tail logs
aws logs tail <log-group-name> --follow --since 1h

# Get metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=<instance-id> \
  --start-time $(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 300 \
  --statistics Average
```

### Cost & Billing

```bash
# Get current month costs
aws ce get-cost-and-usage \
  --time-period Start=$(date +%Y-%m-01),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=DIMENSION,Key=SERVICE

# Cost by service
aws ce get-cost-and-usage \
  --time-period Start=$(date +%Y-%m-01),End=$(date +%Y-%m-%d) \
  --granularity DAILY \
  --metrics UnblendedCost \
  --group-by Type=DIMENSION,Key=SERVICE
```

### AI Services (Bedrock)

```bash
# List models
aws bedrock list-foundation-models --query 'modelSummaries[].[modelId,providerName]' --output table

# List custom models
aws bedrock list-custom-models
```

### Support

```bash
# Create support case
aws support create-case \
  --subject "Issue description" \
  --communication-body "Detailed description" \
  --service-code amazon-ec2 \
  --category-code general-info \
  --severity-code low

# List cases
aws support describe-cases
```

### IAM

```bash
# List users and roles
aws iam list-users --query 'Users[].[UserName,CreateDate]' --output table
aws iam list-roles --query 'Roles[].[RoleName,CreateDate]' --output table

# Get current identity
aws sts get-caller-identity
```

## Output Formatting Guidelines

### For Query Operations

- Use `--query` with JMESPath to filter relevant fields
- Use `--output table` for human-readable output
- Use `--output json` when detailed data is needed

### For Status Checks

Provide concise summaries:

```
✅ EC2 实例状态
┌─────────────────┬──────────┬────────────┐
│ 实例 ID         │ 状态     │ 类型       │
├─────────────────┼──────────┼────────────┤
│ i-0abc123...    │ running  │ t3.medium  │
└─────────────────┴──────────┴────────────┘
```

### For Modification Operations

Report the action taken and result:

```
✅ 操作完成
- 操作: 停止 EC2 实例
- 实例: i-0abc123def456
- 之前状态: running
- 当前状态: stopping
```

## Error Handling

When AWS CLI commands fail:

1. Parse the error message to identify the issue
2. Suggest possible solutions
3. Check IAM permissions if access denied
4. Verify resource exists and is in the correct region

## Integration with GitOps

This skill integrates with the SimplexAI GitOps workflow:

- **ECR Registry**: `830101142436.dkr.ecr.us-east-1.amazonaws.com/simplexai/*`
- **EKS Clusters**: Production and Staging in us-east-1
- **Namespaces**: `production` for prod, `staging` for staging

Reference `CLAUDE.md` for kubectl cluster aliases:
- `k1` - AWS Production (EKS)
- `k2` - AWS Staging (EKS)
