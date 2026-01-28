---
name: pulumi-go
description: Pulumi infrastructure as code using Go with Pulumi Cloud and ESC integration. Use when working with Pulumi Go projects, ESC environments, dynamic secrets, OIDC credentials, or infrastructure automation with Golang.
---

# Pulumi Go Skill

## Development Workflow

### 1. Project Setup

```bash
# Create new Go project
pulumi new go

# Or with a cloud-specific template
pulumi new aws-go
pulumi new azure-go
pulumi new gcp-go
```

**Project structure:**
```
my-project/
├── Pulumi.yaml
├── Pulumi.dev.yaml      # Stack config (use ESC instead)
├── go.mod
├── go.sum
└── main.go
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

### 3. Go Patterns

**Basic resource creation:**
```go
package main

import (
    "github.com/pulumi/pulumi-aws/sdk/v6/go/aws/s3"
    "github.com/pulumi/pulumi/sdk/v3/go/pulumi"
    "github.com/pulumi/pulumi/sdk/v3/go/pulumi/config"
)

func main() {
    pulumi.Run(func(ctx *pulumi.Context) error {
        // Get configuration from ESC
        cfg := config.New(ctx, "")
        instanceType := cfg.Require("instanceType")

        // Create resources with proper tagging
        bucket, err := s3.NewBucket(ctx, "my-bucket", &s3.BucketArgs{
            Versioning: &s3.BucketVersioningArgs{
                Enabled: pulumi.Bool(true),
            },
            ServerSideEncryptionConfiguration: &s3.BucketServerSideEncryptionConfigurationArgs{
                Rule: &s3.BucketServerSideEncryptionConfigurationRuleArgs{
                    ApplyServerSideEncryptionByDefault: &s3.BucketServerSideEncryptionConfigurationRuleApplyServerSideEncryptionByDefaultArgs{
                        SseAlgorithm: pulumi.String("AES256"),
                    },
                },
            },
            Tags: pulumi.StringMap{
                "Environment": pulumi.String(ctx.Stack()),
                "ManagedBy":   pulumi.String("Pulumi"),
            },
        })
        if err != nil {
            return err
        }

        // Export outputs
        ctx.Export("bucketName", bucket.ID())
        ctx.Export("bucketArn", bucket.Arn)

        return nil
    })
}
```

**Component resources for reusability:**
```go
package main

import (
    "github.com/pulumi/pulumi-aws/sdk/v6/go/aws/lb"
    "github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

type WebServiceArgs struct {
    Port     pulumi.IntInput
    ImageUri pulumi.StringInput
}

type WebService struct {
    pulumi.ResourceState

    URL pulumi.StringOutput `pulumi:"url"`
}

func NewWebService(ctx *pulumi.Context, name string, args *WebServiceArgs, opts ...pulumi.ResourceOption) (*WebService, error) {
    component := &WebService{}
    err := ctx.RegisterComponentResource("custom:app:WebService", name, component, opts...)
    if err != nil {
        return nil, err
    }

    // Create child resources with pulumi.Parent(component)
    loadBalancer, err := lb.NewLoadBalancer(ctx, name+"-lb", &lb.LoadBalancerArgs{
        LoadBalancerType: pulumi.String("application"),
        // ... configuration
    }, pulumi.Parent(component))
    if err != nil {
        return nil, err
    }

    component.URL = loadBalancer.DnsName

    ctx.RegisterResourceOutputs(component, pulumi.Map{
        "url": component.URL,
    })

    return component, nil
}
```

**Stack references for cross-stack dependencies:**
```go
package main

import (
    "fmt"

    "github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

func main() {
    pulumi.Run(func(ctx *pulumi.Context) error {
        // Reference outputs from networking stack
        networkingStack, err := pulumi.NewStackReference(ctx, "myorg/networking/prod", nil)
        if err != nil {
            return err
        }

        vpcId := networkingStack.GetStringOutput(pulumi.String("vpcId"))
        subnetIds := networkingStack.GetOutput(pulumi.String("privateSubnetIds"))

        // Use in resource creation
        ctx.Export("vpcId", vpcId)

        return nil
    })
}
```

**Working with Outputs:**
```go
package main

import (
    "github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

func main() {
    pulumi.Run(func(ctx *pulumi.Context) error {
        // Apply transformation
        uppercaseName := bucket.ID().ApplyT(func(id string) string {
            return strings.ToUpper(id)
        }).(pulumi.StringOutput)

        // Combine multiple outputs
        combined := pulumi.All(bucket.ID(), bucket.Arn).ApplyT(
            func(args []interface{}) string {
                id := args[0].(string)
                arn := args[1].(string)
                return fmt.Sprintf("Bucket %s has ARN %s", id, arn)
            },
        ).(pulumi.StringOutput)

        // Conditional resources
        if ctx.Stack() == "prod" {
            _, err := cloudwatch.NewMetricAlarm(ctx, "alarm", &cloudwatch.MetricAlarmArgs{
                // ... configuration
            })
            if err != nil {
                return err
            }
        }

        return nil
    })
}
```

### 4. Using ESC with esc run

Run any command with ESC environment variables injected:

```bash
# Run pulumi commands with ESC credentials
esc run myorg/aws-dev -- pulumi up

# Run tests with secrets
esc run myorg/test-env -- go test ./...

# Open environment and export to shell
esc open myorg/myproject-dev --format shell
```

### 5. Error Handling Patterns

```go
func main() {
    pulumi.Run(func(ctx *pulumi.Context) error {
        // Always check errors
        bucket, err := s3.NewBucket(ctx, "bucket", &s3.BucketArgs{})
        if err != nil {
            return fmt.Errorf("failed to create bucket: %w", err)
        }

        // Chain operations with error handling
        policy, err := s3.NewBucketPolicy(ctx, "policy", &s3.BucketPolicyArgs{
            Bucket: bucket.ID(),
            Policy: bucket.Arn.ApplyT(func(arn string) string {
                return fmt.Sprintf(`{"Version":"2012-10-17",...}`, arn)
            }).(pulumi.StringOutput),
        })
        if err != nil {
            return fmt.Errorf("failed to create bucket policy: %w", err)
        }

        return nil
    })
}
```

### 6. Multi-Language Components

Create components in Go that can be consumed from any Pulumi language (TypeScript, Python, C#, Java, YAML).

**Project structure for multi-language component:**
```
my-component/
├── PulumiPlugin.yaml      # Required for multi-language
├── go.mod
├── go.sum
└── main.go                # Component + entry point
```

**PulumiPlugin.yaml:**
```yaml
runtime: go
```

**Component with proper Args struct (main.go):**
```go
package main

import (
    "context"
    "log"

    "github.com/pulumi/pulumi-aws/sdk/v6/go/aws/s3"
    "github.com/pulumi/pulumi-go-provider/infer"
    "github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

// Args struct - use Input types for all properties
type SecureBucketArgs struct {
    BucketName       pulumi.StringInput `pulumi:"bucketName"`
    EnableVersioning pulumi.BoolInput   `pulumi:"enableVersioning,optional"`
    Tags             pulumi.StringMapInput `pulumi:"tags,optional"`
}

type SecureBucket struct {
    pulumi.ResourceState

    BucketId  pulumi.StringOutput `pulumi:"bucketId"`
    BucketArn pulumi.StringOutput `pulumi:"bucketArn"`
}

func NewSecureBucket(ctx *pulumi.Context, name string, args *SecureBucketArgs, opts ...pulumi.ResourceOption) (*SecureBucket, error) {
    component := &SecureBucket{}
    err := ctx.RegisterComponentResource("myorg:storage:SecureBucket", name, component, opts...)
    if err != nil {
        return nil, err
    }

    bucket, err := s3.NewBucket(ctx, name+"-bucket", &s3.BucketArgs{
        Bucket: args.BucketName,
        Versioning: &s3.BucketVersioningArgs{
            Enabled: args.EnableVersioning,
        },
        ServerSideEncryptionConfiguration: &s3.BucketServerSideEncryptionConfigurationArgs{
            Rule: &s3.BucketServerSideEncryptionConfigurationRuleArgs{
                ApplyServerSideEncryptionByDefault: &s3.BucketServerSideEncryptionConfigurationRuleApplyServerSideEncryptionByDefaultArgs{
                    SseAlgorithm: pulumi.String("AES256"),
                },
            },
        },
        Tags: args.Tags,
    }, pulumi.Parent(component))
    if err != nil {
        return nil, err
    }

    component.BucketId = bucket.ID().ToStringOutput()
    component.BucketArn = bucket.Arn

    ctx.RegisterResourceOutputs(component, pulumi.Map{
        "bucketId":  component.BucketId,
        "bucketArn": component.BucketArn,
    })

    return component, nil
}

// Entry point for multi-language support
func main() {
    prov, err := infer.NewProviderBuilder().
        WithNamespace("myorg").
        WithComponents(
            infer.ComponentF(NewSecureBucket),
        ).
        Build()
    if err != nil {
        log.Fatal(err.Error())
    }
    _ = prov.Run(context.Background(), "go-components", "v0.0.1")
}
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
- Use `pulumi.*Input` types for all properties
- Use `pulumi:"fieldName"` struct tags
- Add `,optional` tag suffix for optional fields
- Avoid interface{} or unsupported types

## Best Practices

### Security
- Use Pulumi ESC for all secrets - never commit secrets to stack config files
- Enable OIDC authentication instead of static credentials
- Use dynamic secrets with short TTLs when possible
- Apply least-privilege IAM policies

### Code Organization
- Use Component Resources for reusable infrastructure patterns
- Leverage Go's type system for configuration validation
- Keep stack-specific config in ESC environments
- Use stack references for cross-stack dependencies
- Handle all errors explicitly

### Deployment
- Always run `pulumi preview` before `pulumi up`
- Use ESC environment versioning and tags for releases
- Implement proper tagging strategy for all resources
- Build your Go program before running Pulumi: `go build -o $(basename $(pwd))`

## Common Commands

```bash
# ESC Commands
esc env init <org>/<project>/<env>    # Create environment
esc env edit <org>/<env>              # Edit environment
esc env get <org>/<env>               # View resolved values
esc run <org>/<env> -- <command>      # Run with env vars
esc env version tag <org>/<env> <tag> # Tag version

# Pulumi Commands
pulumi new go                          # New project
pulumi config env add <org>/<env>     # Link ESC environment
go build -o $(basename $(pwd))         # Build Go binary
pulumi preview                         # Preview changes
pulumi up                              # Deploy
pulumi stack output                    # View outputs
pulumi destroy                         # Tear down
```

## Go-Specific Considerations

### Module Management

```bash
# Initialize Go modules
go mod init myproject

# Add Pulumi dependencies
go get github.com/pulumi/pulumi/sdk/v3
go get github.com/pulumi/pulumi-aws/sdk/v6

# Update dependencies
go mod tidy
```

### Building

```bash
# Build before running Pulumi
go build -o $(basename $(pwd))

# Or let Pulumi build automatically (slower)
pulumi up
```

## References

- [references/pulumi-esc.md](references/pulumi-esc.md) - ESC patterns and commands
- [references/pulumi-patterns.md](references/pulumi-patterns.md) - Common infrastructure patterns
- [references/pulumi-go.md](references/pulumi-go.md) - Go-specific guidance
- [references/pulumi-best-practices-aws.md](references/pulumi-best-practices-aws.md) - AWS best practices
- [references/pulumi-best-practices-azure.md](references/pulumi-best-practices-azure.md) - Azure best practices
- [references/pulumi-best-practices-gcp.md](references/pulumi-best-practices-gcp.md) - GCP best practices
