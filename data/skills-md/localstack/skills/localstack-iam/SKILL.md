---
name: localstack-iam
description: Analyze and enforce IAM policies in LocalStack. Use when users want to enable IAM enforcement, detect permission violations, auto-generate least-privilege policies, or test IAM policies locally before deploying to AWS.
---

# IAM Policy Analyzer

Analyze IAM policies, detect permission violations, and automatically generate least-privilege policies based on actual usage.

## Capabilities

- Enforce IAM policies locally
- Detect permission violations
- Auto-generate policies from access patterns
- Analyze existing policies for issues
- Test policies before deploying to AWS

## Prerequisites

IAM enforcement requires LocalStack Pro:

```bash
export LOCALSTACK_AUTH_TOKEN=<your-token>
```

## IAM Enforcement Modes

### Enable Enforcement

```bash
# Soft mode - logs violations but allows requests
ENFORCE_IAM=soft localstack start -d

# Enforced mode - denies unauthorized requests
ENFORCE_IAM=1 localstack start -d
```

### Configuration

| Mode | Behavior |
|------|----------|
| Disabled (default) | No IAM checks |
| `soft` | Logs violations, allows requests |
| `1` / `enforced` | Full enforcement, denies unauthorized |

## Creating IAM Resources

### Create a User with Policy

```bash
# Create user
awslocal iam create-user --user-name dev-user

# Create access key
awslocal iam create-access-key --user-name dev-user

# Attach policy
awslocal iam attach-user-policy \
  --user-name dev-user \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
```

### Create Custom Policy

```bash
# Create policy from JSON file
awslocal iam create-policy \
  --policy-name my-custom-policy \
  --policy-document file://policy.json

# Example policy.json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::my-bucket/*"
    }
  ]
}
```

## Policy Analysis

### Detect Violations

1. Enable soft enforcement mode
2. Run your application
3. Check logs for access denied messages

```bash
# View IAM-related log entries
localstack logs | grep -i "access denied"
localstack logs | grep -i "iam"
```

### Auto-Generate Policies

Based on access patterns observed in soft mode, create least-privilege policies:

1. Run application with `ENFORCE_IAM=soft`
2. Collect all accessed resources and actions from logs
3. Generate minimal policy covering observed access

## Testing Policies

### Simulate Policy

```bash
# Test if action would be allowed
awslocal iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::000000000000:user/dev-user \
  --action-names s3:GetObject \
  --resource-arns arn:aws:s3:::my-bucket/file.txt
```

### Validate Policy

```bash
# Check policy syntax
awslocal accessanalyzer validate-policy \
  --policy-document file://policy.json \
  --policy-type IDENTITY_POLICY
```

## Best Practices

- Start with soft enforcement to discover required permissions
- Use least-privilege principles when creating policies
- Test policies locally before deploying to AWS
- Regularly audit and refine policies based on actual usage
- Use IAM roles instead of users where possible
