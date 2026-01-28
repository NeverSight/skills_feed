---
name: pulumi-typescript
description: Pulumi infrastructure as code using TypeScript with Pulumi Cloud and ESC integration. Use when working with Pulumi TypeScript projects, ESC environments, dynamic secrets, OIDC credentials, or infrastructure automation with Node.js/TypeScript.
---

# Pulumi TypeScript Skill

## Development Workflow

### 1. Project Setup

```bash
# Create new TypeScript project
pulumi new typescript

# Or with a cloud-specific template
pulumi new aws-typescript
pulumi new azure-typescript
pulumi new gcp-typescript
```

**Project structure:**
```
my-project/
├── Pulumi.yaml
├── Pulumi.dev.yaml      # Stack config (use ESC instead)
├── package.json
├── tsconfig.json
└── index.ts
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

### 3. TypeScript Patterns

**Basic resource creation:**
```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

// Get configuration from ESC
const config = new pulumi.Config();
const instanceType = config.require("instanceType");

// Create resources with proper tagging
const bucket = new aws.s3.Bucket("my-bucket", {
    versioning: { enabled: true },
    serverSideEncryptionConfiguration: {
        rule: {
            applyServerSideEncryptionByDefault: {
                sseAlgorithm: "AES256",
            },
        },
    },
    tags: {
        Environment: pulumi.getStack(),
        ManagedBy: "Pulumi",
    },
});

// Export outputs
export const bucketName = bucket.id;
export const bucketArn = bucket.arn;
```

**Component resources for reusability:**
```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

interface WebServiceArgs {
    port: pulumi.Input<number>;
    imageUri: pulumi.Input<string>;
}

class WebService extends pulumi.ComponentResource {
    public readonly url: pulumi.Output<string>;

    constructor(name: string, args: WebServiceArgs, opts?: pulumi.ComponentResourceOptions) {
        super("custom:app:WebService", name, {}, opts);

        // Create child resources with { parent: this }
        const lb = new aws.lb.LoadBalancer(`${name}-lb`, {
            loadBalancerType: "application",
            // ... configuration
        }, { parent: this });

        this.url = lb.dnsName;
        this.registerOutputs({ url: this.url });
    }
}
```

**Stack references for cross-stack dependencies:**
```typescript
import * as pulumi from "@pulumi/pulumi";

// Reference outputs from networking stack
const networkingStack = new pulumi.StackReference("myorg/networking/prod");
const vpcId = networkingStack.getOutput("vpcId");
const subnetIds = networkingStack.getOutput("privateSubnetIds");
```

**Working with Outputs:**
```typescript
import * as pulumi from "@pulumi/pulumi";

// Use apply for transformations
const uppercaseName = bucket.id.apply(id => id.toUpperCase());

// Use pulumi.all for multiple outputs
const combined = pulumi.all([bucket.id, bucket.arn]).apply(
    ([id, arn]) => `Bucket ${id} has ARN ${arn}`
);

// Conditional resources
const isProd = pulumi.getStack() === "prod";
const monitoring = isProd ? new aws.cloudwatch.MetricAlarm("alarm", {
    // ... configuration
}) : undefined;
```

### 4. Using ESC with esc run

Run any command with ESC environment variables injected:

```bash
# Run pulumi commands with ESC credentials
esc run myorg/aws-dev -- pulumi up

# Run tests with secrets
esc run myorg/test-env -- npm test

# Open environment and export to shell
esc open myorg/myproject-dev --format shell
```

### 5. Async Patterns

```typescript
// Export async function for top-level await
export = async () => {
    const data = await fetchExternalData();

    const resource = new aws.s3.Bucket("bucket", {
        tags: { data: data.value },
    });

    return {
        bucketName: resource.id,
    };
};
```

### 6. Multi-Language Components

Create components in TypeScript that can be consumed from any Pulumi language (Python, Go, C#, Java, YAML).

**Project structure for multi-language component:**
```
my-component/
├── PulumiPlugin.yaml      # Required for multi-language
├── package.json
├── tsconfig.json
└── index.ts               # Component definition
```

**PulumiPlugin.yaml:**
```yaml
runtime: nodejs
```

**Component with proper Args interface:**
```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

// Args interface - use Input types for all properties
export interface SecureBucketArgs {
    // Wrap all scalar members in Input types
    bucketName: pulumi.Input<string>;
    enableVersioning?: pulumi.Input<boolean>;
    tags?: pulumi.Input<Record<string, pulumi.Input<string>>>;
}

export class SecureBucket extends pulumi.ComponentResource {
    public readonly bucketId: pulumi.Output<string>;
    public readonly bucketArn: pulumi.Output<string>;

    // Constructor must have 'args' parameter with type annotation
    constructor(name: string, args: SecureBucketArgs, opts?: pulumi.ComponentResourceOptions) {
        super("myorg:storage:SecureBucket", name, {}, opts);

        const bucket = new aws.s3.Bucket(`${name}-bucket`, {
            bucket: args.bucketName,
            versioning: { enabled: args.enableVersioning ?? true },
            serverSideEncryptionConfiguration: {
                rule: {
                    applyServerSideEncryptionByDefault: {
                        sseAlgorithm: "AES256",
                    },
                },
            },
            tags: args.tags,
        }, { parent: this });

        this.bucketId = bucket.id;
        this.bucketArn = bucket.arn;

        this.registerOutputs({
            bucketId: this.bucketId,
            bucketArn: this.bucketArn,
        });
    }
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
- Use `pulumi.Input<T>` for all scalar properties
- Avoid union types (`string | number`) - not supported
- Avoid functions/callbacks - not serializable
- Constructor must have `args` parameter with type declaration

## Best Practices

### Security
- Use Pulumi ESC for all secrets - never commit secrets to stack config files
- Enable OIDC authentication instead of static credentials
- Use dynamic secrets with short TTLs when possible
- Apply least-privilege IAM policies

### Code Organization
- Use ComponentResources for reusable infrastructure patterns
- Leverage TypeScript's type system for configuration validation
- Keep stack-specific config in ESC environments
- Use stack references for cross-stack dependencies

### Deployment
- Always run `pulumi preview` before `pulumi up`
- Use ESC environment versioning and tags for releases
- Implement proper tagging strategy for all resources

## Common Commands

```bash
# ESC Commands
esc env init <org>/<project>/<env>    # Create environment
esc env edit <org>/<env>              # Edit environment
esc env get <org>/<env>               # View resolved values
esc run <org>/<env> -- <command>      # Run with env vars
esc env version tag <org>/<env> <tag> # Tag version

# Pulumi Commands
pulumi new typescript                  # New project
pulumi config env add <org>/<env>     # Link ESC environment
pulumi preview                         # Preview changes
pulumi up                              # Deploy
pulumi stack output                    # View outputs
pulumi destroy                         # Tear down
```

## References

- [references/pulumi-esc.md](references/pulumi-esc.md) - ESC patterns and commands
- [references/pulumi-patterns.md](references/pulumi-patterns.md) - Common infrastructure patterns
- [references/pulumi-typescript.md](references/pulumi-typescript.md) - TypeScript-specific guidance
- [references/pulumi-best-practices-aws.md](references/pulumi-best-practices-aws.md) - AWS best practices
- [references/pulumi-best-practices-azure.md](references/pulumi-best-practices-azure.md) - Azure best practices
- [references/pulumi-best-practices-gcp.md](references/pulumi-best-practices-gcp.md) - GCP best practices
