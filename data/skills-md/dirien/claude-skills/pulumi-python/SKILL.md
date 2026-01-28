---
name: pulumi-python
description: Pulumi infrastructure as code using Python with Pulumi Cloud and ESC integration. Use when working with Pulumi Python projects, ESC environments, dynamic secrets, OIDC credentials, or infrastructure automation with Python.
---

# Pulumi Python Skill

## Development Workflow

### 1. Project Setup

```bash
# Create new Python project
pulumi new python

# Or with a cloud-specific template
pulumi new aws-python
pulumi new azure-python
pulumi new gcp-python
```

**Project structure:**
```
my-project/
├── Pulumi.yaml
├── Pulumi.dev.yaml      # Stack config (use ESC instead)
├── __main__.py
├── requirements.txt     # or pyproject.toml
└── venv/                # Virtual environment
```

### 2. Pulumi ESC Integration

Instead of using `pulumi config set` or stack config files, use Pulumi ESC for centralized secrets and configuration.

**Link ESC environment to stack:**
```bash
# Create ESC environment
esc env init myorg/myproject-dev

# Edit environment
esc env edit myorg/myproject-dev

# Link to Pulumi stack
pulumi config env add myorg/myproject-dev
```

**ESC environment definition (YAML):**
```yaml
values:
  # Static configuration
  pulumiConfig:
    aws:region: us-west-2
    myapp:instanceType: t3.medium

  # Dynamic OIDC credentials for AWS
  aws:
    login:
      fn::open::aws-login:
        oidc:
          roleArn: arn:aws:iam::123456789:role/pulumi-oidc
          sessionName: pulumi-deploy

  # Pull secrets from AWS Secrets Manager
  secrets:
    fn::open::aws-secrets:
      region: us-west-2
      login: ${aws.login}
      get:
        dbPassword:
          secretId: prod/database/password

  # Expose to environment variables
  environmentVariables:
    AWS_ACCESS_KEY_ID: ${aws.login.accessKeyId}
    AWS_SECRET_ACCESS_KEY: ${aws.login.secretAccessKey}
    AWS_SESSION_TOKEN: ${aws.login.sessionToken}
```

### 3. Python Patterns

**Basic resource creation:**
```python
import pulumi
import pulumi_aws as aws

# Get configuration from ESC
config = pulumi.Config()
instance_type = config.require("instanceType")

# Create resources with proper tagging
bucket = aws.s3.Bucket(
    "my-bucket",
    versioning=aws.s3.BucketVersioningArgs(
        enabled=True,
    ),
    server_side_encryption_configuration=aws.s3.BucketServerSideEncryptionConfigurationArgs(
        rule=aws.s3.BucketServerSideEncryptionConfigurationRuleArgs(
            apply_server_side_encryption_by_default=aws.s3.BucketServerSideEncryptionConfigurationRuleApplyServerSideEncryptionByDefaultArgs(
                sse_algorithm="AES256",
            ),
        ),
    ),
    tags={
        "Environment": pulumi.get_stack(),
        "ManagedBy": "Pulumi",
    },
)

# Export outputs
pulumi.export("bucket_name", bucket.id)
pulumi.export("bucket_arn", bucket.arn)
```

**Using dictionary literals (concise alternative):**
```python
import pulumi
import pulumi_aws as aws

bucket = aws.s3.Bucket(
    "my-bucket",
    versioning={"enabled": True},
    server_side_encryption_configuration={
        "rule": {
            "apply_server_side_encryption_by_default": {
                "sse_algorithm": "AES256",
            },
        },
    },
    tags={
        "Environment": pulumi.get_stack(),
        "ManagedBy": "Pulumi",
    },
)
```

**Component resources for reusability:**
```python
import pulumi
from pulumi_aws import lb


class WebServiceArgs:
    def __init__(self, port: pulumi.Input[int], image_uri: pulumi.Input[str]):
        self.port = port
        self.image_uri = image_uri


class WebService(pulumi.ComponentResource):
    url: pulumi.Output[str]

    def __init__(self, name: str, args: WebServiceArgs, opts: pulumi.ResourceOptions = None):
        super().__init__("custom:app:WebService", name, {}, opts)

        # Create child resources with parent=self
        load_balancer = lb.LoadBalancer(
            f"{name}-lb",
            load_balancer_type="application",
            # ... configuration
            opts=pulumi.ResourceOptions(parent=self),
        )

        self.url = load_balancer.dns_name

        self.register_outputs({
            "url": self.url,
        })
```

**Stack references for cross-stack dependencies:**
```python
import pulumi

# Reference outputs from networking stack
networking_stack = pulumi.StackReference("myorg/networking/prod")
vpc_id = networking_stack.get_output("vpc_id")
subnet_ids = networking_stack.get_output("private_subnet_ids")
```

**Working with Outputs:**
```python
import pulumi

# Apply transformation
uppercase_name = bucket.id.apply(lambda id: id.upper())

# Combine multiple outputs
combined = pulumi.Output.all(bucket.id, bucket.arn).apply(
    lambda args: f"Bucket {args[0]} has ARN {args[1]}"
)

# Using Output.concat for string interpolation
message = pulumi.Output.concat("Bucket ARN: ", bucket.arn)

# Conditional resources
is_prod = pulumi.get_stack() == "prod"
if is_prod:
    alarm = aws.cloudwatch.MetricAlarm(
        "alarm",
        # ... configuration
    )
```

### 4. Using ESC with esc run

Run any command with ESC environment variables injected:

```bash
# Run pulumi commands with ESC credentials
esc run myorg/aws-dev -- pulumi up

# Run tests with secrets
esc run myorg/test-env -- pytest

# Open environment and export to shell
esc open myorg/myproject-dev --format shell
```

### 5. Async Patterns

```python
import pulumi
import asyncio

# Pulumi programs are single-threaded
# Use Output.from_input for async-like patterns

async def fetch_data():
    # Async operation
    return {"key": "value"}

# Convert async result to Output
data = pulumi.Output.from_input(asyncio.get_event_loop().run_until_complete(fetch_data()))
```

### 6. Multi-Language Components

Create components in Python that can be consumed from any Pulumi language (TypeScript, Go, C#, Java, YAML).

**Project structure for multi-language component:**
```
my-component/
├── PulumiPlugin.yaml      # Required for multi-language
├── pyproject.toml         # or requirements.txt
└── __main__.py            # Component + entry point
```

**PulumiPlugin.yaml:**
```yaml
runtime: python
```

**Component with proper Args class (__main__.py):**
```python
from typing import Optional
import pulumi
from pulumi import Input, Output, ResourceOptions
from pulumi.provider.experimental import component_provider_host
import pulumi_aws as aws


class SecureBucketArgs:
    """Args class - use Input types for all properties."""

    def __init__(
        self,
        bucket_name: Input[str],
        enable_versioning: Optional[Input[bool]] = None,
        tags: Optional[Input[dict]] = None,
    ):
        self.bucket_name = bucket_name
        self.enable_versioning = enable_versioning or True
        self.tags = tags


class SecureBucket(pulumi.ComponentResource):
    """A secure S3 bucket with encryption and versioning."""

    bucket_id: Output[str]
    bucket_arn: Output[str]

    # Constructor must have 'args' parameter with type annotation
    def __init__(
        self,
        name: str,
        args: SecureBucketArgs,
        opts: Optional[ResourceOptions] = None,
    ):
        super().__init__("myorg:storage:SecureBucket", name, {}, opts)

        bucket = aws.s3.Bucket(
            f"{name}-bucket",
            bucket=args.bucket_name,
            versioning={"enabled": args.enable_versioning},
            server_side_encryption_configuration={
                "rule": {
                    "apply_server_side_encryption_by_default": {
                        "sse_algorithm": "AES256",
                    },
                },
            },
            tags=args.tags,
            opts=ResourceOptions(parent=self),
        )

        self.bucket_id = bucket.id
        self.bucket_arn = bucket.arn

        self.register_outputs({
            "bucket_id": self.bucket_id,
            "bucket_arn": self.bucket_arn,
        })


# Entry point for multi-language support
if __name__ == "__main__":
    component_provider_host(
        name="python-components",
        components=[SecureBucket],
    )
```

**Publishing for multi-language consumption:**
```bash
# Consume from git repository
pulumi package add github.com/myorg/my-component

# With version tag
pulumi package add github.com/myorg/my-component@v1.0.0

# Local development
pulumi package add /path/to/local/my-component
```

**Multi-language Args requirements:**
- Use `pulumi.Input[T]` type hints for all properties
- Args class must have `__init__` with typed parameters
- Constructor must have `args` parameter with type annotation
- Use `Optional[Input[T]]` for optional properties

## Best Practices

### Security
- Use Pulumi ESC for all secrets - never commit secrets to stack config files
- Enable OIDC authentication instead of static credentials
- Use dynamic secrets with short TTLs when possible
- Apply least-privilege IAM policies

### Code Organization
- Use ComponentResources for reusable infrastructure patterns
- Leverage Python's type hints for better IDE support
- Keep stack-specific config in ESC environments
- Use stack references for cross-stack dependencies
- Prefer Args classes for type safety, or dict literals for brevity

### Deployment
- Always run `pulumi preview` before `pulumi up`
- Use ESC environment versioning and tags for releases
- Implement proper tagging strategy for all resources

### Virtual Environments
- Always use virtual environments (`venv`, `poetry`, or `uv`)
- Specify toolchain in Pulumi.yaml for consistency

## Common Commands

```bash
# ESC Commands
esc env init <org>/<project>/<env>    # Create environment
esc env edit <org>/<env>              # Edit environment
esc env get <org>/<env>               # View resolved values
esc run <org>/<env> -- <command>      # Run with env vars
esc env version tag <org>/<env> <tag> # Tag version

# Pulumi Commands
pulumi new python                      # New project
pulumi config env add <org>/<env>     # Link ESC environment
pulumi preview                         # Preview changes
pulumi up                              # Deploy
pulumi stack output                    # View outputs
pulumi destroy                         # Tear down

# Dependency Management
pip install -r requirements.txt        # Install deps (pip)
poetry add pulumi-aws                  # Add dep (poetry)
uv add pulumi-aws                      # Add dep (uv)
```

## Python-Specific Considerations

### Virtual Environment Setup

**Using pip (default):**
```yaml
# Pulumi.yaml
runtime:
  name: python
  options:
    toolchain: pip
    virtualenv: venv
```

**Using poetry:**
```yaml
# Pulumi.yaml
runtime:
  name: python
  options:
    toolchain: poetry
```

**Using uv:**
```yaml
# Pulumi.yaml
runtime:
  name: python
  options:
    toolchain: uv
    virtualenv: .venv
```

### Type Checking

```yaml
# Pulumi.yaml - Enable type checking
runtime:
  name: python
  options:
    typechecker: mypy  # or pyright
```

### Input Type Options

```python
# Using Args classes (type-safe)
bucket = aws.s3.Bucket(
    "bucket",
    versioning=aws.s3.BucketVersioningArgs(enabled=True),
)

# Using dict literals (concise)
bucket = aws.s3.Bucket(
    "bucket",
    versioning={"enabled": True},
)
```

## References

- [references/pulumi-esc.md](references/pulumi-esc.md) - ESC patterns and commands
- [references/pulumi-patterns.md](references/pulumi-patterns.md) - Common infrastructure patterns
- [references/pulumi-python.md](references/pulumi-python.md) - Python-specific guidance
- [references/pulumi-best-practices-aws.md](references/pulumi-best-practices-aws.md) - AWS best practices
- [references/pulumi-best-practices-azure.md](references/pulumi-best-practices-azure.md) - Azure best practices
- [references/pulumi-best-practices-gcp.md](references/pulumi-best-practices-gcp.md) - GCP best practices
