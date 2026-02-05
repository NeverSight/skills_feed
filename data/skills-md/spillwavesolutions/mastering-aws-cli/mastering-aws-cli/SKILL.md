---
name: mastering-aws-cli
description: |
  AWS CLI v2 quick-reference for experienced developers. Covers compute (Lambda, ECS, EKS), storage (S3, DynamoDB, Aurora), networking (VPC, SSM tunneling), security (IAM, Secrets Manager), and GitHub Actions CI/CD. Use when asked to "write aws commands", "debug aws access", "set up cross-account roles", "configure aws cli", "assume role", "S3 bucket operations", or "deploy to ECS".
triggers:
  - aws cli
  - aws command line
  - aws commands
  - ec2
  - s3
  - lambda
  - iam
  - eks
  - ecs
  - ecr
  - dynamodb
  - rds
  - aurora
  - glue
  - msk
  - kinesis
  - ssm
  - secrets manager
  - parameter store
  - vpc
  - cloudwatch
  - sts
  - assume role
  - aws configure
  - aws sso
  - github actions aws
  - oidc aws
  - bastion
  - ssm tunnel
  - kubectl eks
category: cloud-infrastructure
license: MIT
allowed-tools:
  - Read
  - Bash
  - WebFetch
metadata:
  version: 2.1.0
  author: Spillwave
---

# AWS CLI v2 Quick Reference

A unified tool to manage AWS services from the terminal. This guide focuses on CLI v2 features, practical examples, and advanced patterns for experienced developers.

## Quick Start

```bash
# Verify installation and version
aws --version

# Interactive configuration
aws configure                    # Access keys + region + output format
aws configure sso               # IAM Identity Center (SSO) - recommended

# Verify identity
aws sts get-caller-identity     # Shows Account, UserId, ARN

# Enable auto-prompt for command discovery
aws dynamodb --cli-auto-prompt
```

## Power User Tips

```bash
# See all waiter commands for a service
aws ec2 wait help

# Generate command skeleton (fill in the blanks)
aws lambda create-function --generate-cli-skeleton > create-fn.json

# Create CLI alias for common commands
aws configure set cli_alias.whoami "sts get-caller-identity"
aws whoami  # Now works!

# Disable pager for scripting
export AWS_PAGER=""
```

See [Advanced Patterns](references/advanced-patterns.md) for JMESPath mastery and automation tricks.

## Global Options

| Flag | Description |
|:-----|:------------|
| `--profile NAME` | Use named profile from `~/.aws/credentials` |
| `--region REGION` | Override default region (e.g., `us-east-1`) |
| `--output FORMAT` | Output: `json` (default), `text`, `table`, `yaml`, `yaml-stream` |
| `--query EXPR` | Filter output using JMESPath expressions |
| `--no-paginate` | Disable auto-pagination (first page only) |
| `--dry-run` | Check permissions without executing (EC2, etc.) |
| `--debug` | Verbose HTTP/API debug logging |
| `--cli-auto-prompt` | Interactive parameter completion |
| `--no-cli-pager` | Disable output paging |

## Decision Trees

### Compute & Containers
```
Need compute?
├── Serverless functions ────────────► Lambda (references/lambda.md)
├── Docker containers
│   ├── Managed orchestration ───────► ECS (references/ecs.md)
│   ├── Kubernetes ──────────────────► EKS (references/eks.md)
│   └── Container registry ──────────► ECR (references/ecr.md)
└── Virtual machines ────────────────► EC2 (use aws ec2 commands)
```

### Data & Storage
```
Need data storage?
├── Object/blob storage ─────────────► S3 (references/s3.md)
├── NoSQL (key-value/document) ──────► DynamoDB (references/dynamodb.md)
├── Relational SQL ──────────────────► Aurora/RDS (references/aurora.md)
├── Data catalog & ETL ──────────────► Glue (references/glue.md)
└── Data warehouse ──────────────────► Redshift (aws redshift commands)
```

### Streaming & Messaging
```
Need streaming/messaging?
├── Kafka-compatible ────────────────► MSK (references/msk.md)
├── Real-time streams ───────────────► Kinesis (references/kinesis.md)
├── Message queues ──────────────────► SQS (aws sqs commands)
└── Pub/Sub notifications ───────────► SNS (aws sns commands)
```

### Security & Access
```
Need security/access management?
├── Users, roles, policies ──────────► IAM (references/iam-security.md)
├── Secrets & credentials ───────────► Secrets Manager/SSM (references/private-parameters.md)
├── Private network access ──────────► VPC (references/vpc-networking.md)
└── Secure tunneling ────────────────► SSM/Bastion (references/bastion-tunneling.md)
```

## Reference File Navigation

| Reference | Description | Key Triggers |
|:----------|:------------|:-------------|
| [Setup](references/setup.md) | Installation, configuration, profiles, SSO | `install`, `configure`, `sso`, `profile` |
| [IAM & Security](references/iam-security.md) | Roles, policies, STS, MFA, cross-account | `iam`, `role`, `policy`, `sts`, `assume-role` |
| [Lambda](references/lambda.md) | Functions, layers, aliases, URLs, events | `lambda`, `serverless`, `function` |
| [ECS](references/ecs.md) | Clusters, tasks, services, Fargate | `ecs`, `fargate`, `task`, `container` |
| [EKS](references/eks.md) | Clusters, node groups, kubeconfig, IRSA | `eks`, `kubernetes`, `kubectl`, `k8s` |
| [ECR](references/ecr.md) | Repositories, auth, scanning, lifecycle | `ecr`, `docker`, `registry`, `image` |
| [S3](references/s3.md) | Buckets, objects, sync, presign, lifecycle | `s3`, `bucket`, `upload`, `sync` |
| [DynamoDB](references/dynamodb.md) | Tables, items, queries, streams, backups | `dynamodb`, `ddb`, `nosql` |
| [Aurora/RDS](references/aurora.md) | Clusters, serverless v2, cloning, blue-green | `rds`, `aurora`, `mysql`, `postgresql` |
| [Glue](references/glue.md) | Catalog, crawlers, ETL jobs, workflows | `glue`, `etl`, `catalog`, `crawler` |
| [MSK](references/msk.md) | Kafka clusters, serverless, configuration | `msk`, `kafka`, `streaming` |
| [Kinesis](references/kinesis.md) | Data streams, Firehose, consumers | `kinesis`, `stream`, `firehose` |
| [Secrets & Params](references/private-parameters.md) | Parameter Store, Secrets Manager, rotation | `ssm`, `secrets`, `parameter`, `rotation` |
| [VPC & Networking](references/vpc-networking.md) | VPCs, subnets, security groups, endpoints | `vpc`, `subnet`, `security-group`, `endpoint` |
| [Bastion & Tunneling](references/bastion-tunneling.md) | SSM Session Manager, port forwarding | `bastion`, `tunnel`, `ssm`, `ssh` |
| [GitHub CI/CD](references/github-cicd.md) | OIDC, GitHub Actions, CodeBuild | `github`, `actions`, `oidc`, `cicd` |
| [Advanced Patterns](references/advanced-patterns.md) | JMESPath, waiters, skeletons, aliases | `jmespath`, `query`, `waiter`, `alias` |

## Environment Variables

| Variable | Purpose | Example |
|:---------|:--------|:--------|
| `AWS_ACCESS_KEY_ID` | Access key for authentication | `AKIAIOSFODNN7EXAMPLE` |
| `AWS_SECRET_ACCESS_KEY` | Secret key for authentication | `wJalrXUtnFEMI/...` |
| `AWS_SESSION_TOKEN` | Session token (temporary credentials) | For STS assume-role |
| `AWS_PROFILE` | Named profile to use | `production` |
| `AWS_REGION` | AWS region for requests | `us-west-2` |
| `AWS_DEFAULT_OUTPUT` | Default output format | `json`, `text`, `table` |
| `AWS_PAGER` | Pager program (empty to disable) | `""` |
| `AWS_CONFIG_FILE` | Custom config file path | `~/.aws/config` |
| `AWS_SHARED_CREDENTIALS_FILE` | Custom credentials file path | `~/.aws/credentials` |
| `AWS_CA_BUNDLE` | Custom CA certificate bundle | `/path/to/cert.pem` |
| `AWS_RETRY_MODE` | Retry mode | `standard`, `adaptive` |

## Credential Precedence

The CLI resolves credentials in this order (first match wins):

1. **Command-line options** (`--profile`, explicit credentials)
2. **Environment variables** (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
3. **Web identity token** (EKS IRSA, OIDC)
4. **SSO credentials** (IAM Identity Center)
5. **Credentials file** (`~/.aws/credentials`)
6. **Config file** (`~/.aws/config` with `credential_process`)
7. **Container credentials** (ECS task role)
8. **Instance metadata** (EC2 instance profile, IMDSv2)

## Common Patterns

### Profile Switching
```bash
# Use specific profile for one command
aws s3 ls --profile production

# Set default profile for session
export AWS_PROFILE=production

# List configured profiles
aws configure list-profiles
```

### Output Filtering with JMESPath
```bash
# Get specific fields
aws ec2 describe-instances \
    --query 'Reservations[*].Instances[*].[InstanceId,State.Name]' \
    --output table

# Filter running instances
aws ec2 describe-instances \
    --query 'Reservations[*].Instances[?State.Name==`running`].InstanceId' \
    --output text
```

### Wait for Resource State
```bash
# Wait for instance to be running
aws ec2 wait instance-running --instance-ids i-1234567890abcdef0

# Wait for Lambda function update
aws lambda wait function-updated --function-name my-function
```

## Best Practices

| Category | Recommendation |
|:---------|:---------------|
| **Security** | Use `aws configure sso` over long-lived access keys |
| **Security** | Use IAM roles for compute (EC2/Lambda/ECS) instead of embedded keys |
| **Security** | Enable MFA for sensitive operations |
| **Scripting** | Use `--output json` or `--output text` for parsing |
| **Scripting** | Use `--query` to filter data and reduce output |
| **Safety** | Use `--dry-run` before destructive operations |
| **Performance** | Use `--page-size` to control memory on large lists |
| **Regions** | Explicitly set region in scripts to avoid surprises |
| **Cost** | Use lifecycle policies (S3/ECR) for automatic cleanup |
| **Debugging** | Use `--debug` to see raw HTTP requests/responses |

## Common Errors Quick Reference

| Error | Cause | Fix |
|:------|:------|:----|
| `ExpiredToken` | Session credentials expired | Run `aws sso login` or `aws sts get-session-token` |
| `AccessDenied` | Missing IAM permissions | Check IAM policy; use `--debug` to see required action |
| `InvalidClientTokenId` | Invalid access key | Verify `AWS_ACCESS_KEY_ID` or run `aws configure` |
| `UnauthorizedAccess` | Wrong region or account | Check `--region` flag and `aws sts get-caller-identity` |
| `ThrottlingException` | API rate limit exceeded | Add retry logic with exponential backoff |
| `NoCredentialProviders` | No credentials found | Check credential chain; run `aws configure list` |

For detailed troubleshooting, see [Setup](references/setup.md#troubleshooting).

## When Not to Use

- **AWS SDK code** — For boto3, AWS SDK for JavaScript, etc., use programming documentation
- **CloudFormation/Terraform** — This skill covers CLI commands, not IaC templates
- **Console UI steps** — CLI-focused; use AWS documentation for console walkthroughs
- **Pricing/billing** — Use AWS pricing calculator or Cost Explorer documentation

## Quick Command Reference

```bash
# Identity & Access
aws sts get-caller-identity
# → {"Account": "123456789012", "UserId": "AIDAEXAMPLE", "Arn": "arn:aws:iam::123456789012:user/dev"}

aws sts assume-role --role-arn arn:aws:iam::123456789012:role/Admin --role-session-name mysession
# → {"Credentials": {"AccessKeyId": "ASIA...", "SecretAccessKey": "...", "SessionToken": "..."}}

# S3
aws s3 ls
# → 2024-01-15 bucket-name-1
# → 2024-02-20 bucket-name-2

aws s3 sync ./local s3://bucket/prefix --delete

# Lambda
aws lambda invoke --function-name fn response.json
# → {"StatusCode": 200, "ExecutedVersion": "$LATEST"}

aws lambda update-function-code --function-name fn --zip-file fileb://code.zip
# → {"FunctionName": "fn", "LastModified": "2024-12-28T...", "State": "Active"}

# ECS
aws ecs list-clusters
# → {"clusterArns": ["arn:aws:ecs:us-east-1:123456789012:cluster/prod"]}

aws ecs update-service --cluster prod --service api --force-new-deployment

# EKS
aws eks update-kubeconfig --name my-cluster
# → Added new context arn:aws:eks:us-east-1:123456789012:cluster/my-cluster

aws eks list-clusters
# → {"clusters": ["my-cluster", "dev-cluster"]}

# Secrets
aws secretsmanager get-secret-value --secret-id prod/api/key --query SecretString --output text
# → sk_live_xxxxxxxxxxxxx

aws ssm get-parameter --name /app/prod/db/host --with-decryption --query Parameter.Value --output text
# → db.example.com

# Debugging
aws ssm start-session --target i-0123456789abcdef0
# → Starting session with SessionId: user-0a1b2c3d4e5f67890
```
