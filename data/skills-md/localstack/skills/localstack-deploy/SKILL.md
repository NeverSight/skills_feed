---
name: localstack-deploy
description: Deploy infrastructure to LocalStack using IaC tools. Use when users want to deploy Terraform, CDK, CloudFormation, or Pulumi to LocalStack, or need help configuring tflocal, cdklocal, pulumilocal, or awslocal wrappers.
---

# Infrastructure as Code Deployment

Deploy AWS infrastructure to LocalStack using popular IaC tools including Terraform, AWS CDK, CloudFormation, and Pulumi.

## Capabilities

- Deploy Terraform configurations to LocalStack
- Run AWS CDK deployments locally
- Deploy CloudFormation stacks
- Execute Pulumi programs against LocalStack
- Validate infrastructure before deployment

## Terraform

### Using tflocal (Preferred)

The `tflocal` wrapper is the preferred way to deploy Terraform configurations to LocalStack. It automatically configures all AWS provider endpoints to point to LocalStack, requiring no changes to your Terraform files.

```bash
# Install tflocal wrapper
pip install terraform-local

# Use tflocal instead of terraform - no provider changes needed
tflocal init
tflocal plan
tflocal apply -auto-approve
tflocal destroy -auto-approve
```

### Manual Provider Configuration (Fallback)

Only use manual provider configuration if `tflocal` cannot be installed (e.g., Python/pip is not available in the environment). This approach requires modifying your Terraform files:

```hcl
# In your provider configuration:
provider "aws" {
  access_key                  = "test"
  secret_key                  = "test"
  region                      = "us-east-1"

  endpoints {
    s3       = "http://localhost:4566"
    dynamodb = "http://localhost:4566"
    lambda   = "http://localhost:4566"
    # Add other services as needed
  }

  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
}
```

Note: When using manual configuration, you must list endpoints for each AWS service used in your configuration.

## AWS CDK

### Setup

```bash
# Install cdklocal wrapper
npm install -g aws-cdk-local aws-cdk

# Bootstrap (first time only)
cdklocal bootstrap
```

### Deploy

```bash
# Deploy all stacks
cdklocal deploy --all --require-approval never

# Deploy specific stack
cdklocal deploy MyStack

# Destroy
cdklocal destroy --all --force
```

## CloudFormation

### Deploy with awslocal

```bash
# Create stack
awslocal cloudformation create-stack \
  --stack-name my-stack \
  --template-body file://template.yaml

# Update stack
awslocal cloudformation update-stack \
  --stack-name my-stack \
  --template-body file://template.yaml

# Delete stack
awslocal cloudformation delete-stack --stack-name my-stack

# Describe stack
awslocal cloudformation describe-stacks --stack-name my-stack
```

## Pulumi

### Using pulumilocal (Preferred)

The `pulumilocal` wrapper is the preferred way to deploy Pulumi programs to LocalStack. It automatically configures AWS endpoints, requiring no changes to your Pulumi configuration.

```bash
# Install pulumilocal wrapper
pip install pulumi-local

# Use pulumilocal instead of pulumi - no config changes needed
pulumilocal preview
pulumilocal up --yes
pulumilocal destroy --yes
```

### Manual Configuration (Fallback)

Only use manual configuration if `pulumilocal` cannot be installed (e.g., Python/pip is not available in the environment):

```bash
# Configure Pulumi for LocalStack
pulumi config set aws:accessKey test
pulumi config set aws:secretKey test
pulumi config set aws:region us-east-1
pulumi config set aws:endpoints '[{"s3":"http://localhost:4566"}]'
```

```bash
# Deploy with standard pulumi commands
pulumi preview
pulumi up --yes
pulumi destroy --yes
```

## Best Practices

- Use wrapper tools (`tflocal`, `cdklocal`, `awslocal`) for simplified configuration
- Test infrastructure changes locally before deploying to AWS
- Use `PERSISTENCE=1` to retain state across LocalStack restarts
- Leverage Cloud Pods to save/restore infrastructure state
