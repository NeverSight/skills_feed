---
name: pulumi-component
version: 1.0.0
description: Guide for authoring Pulumi ComponentResource classes. Use when creating reusable infrastructure components, designing component interfaces, setting up multi-language support, or distributing component packages.
---

# Authoring Pulumi Components

A ComponentResource groups related infrastructure resources into a reusable, logical unit. Components make infrastructure easier to understand, reuse, and maintain. Components appear as a single node with children nested underneath in `pulumi preview`/`pulumi up` output and in the Pulumi Cloud console.

This skill covers the full component authoring lifecycle. For general Pulumi coding patterns (Output handling, secrets, aliases, preview workflows), use the `pulumi-best-practices` skill instead.

## When to Use This Skill

Invoke this skill when:

- Creating a new ComponentResource class
- Designing the args interface for a component
- Making a component consumable from multiple Pulumi languages
- Publishing or distributing a component package
- Refactoring inline resources into a reusable component
- Debugging component behavior (missing outputs, stuck creating, children at wrong level)

## Component Anatomy

Every component has four required elements:

1. **Extend ComponentResource** and call `super()` with a type URN
2. **Accept standard parameters**: name, args, and `ComponentResourceOptions`
3. **Set `parent: this`** on all child resources
4. **Call `registerOutputs()`** at the end of the constructor

### TypeScript

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

interface StaticSiteArgs {
    indexDocument?: pulumi.Input<string>;
    errorDocument?: pulumi.Input<string>;
}

class StaticSite extends pulumi.ComponentResource {
    public readonly bucketName: pulumi.Output<string>;
    public readonly websiteUrl: pulumi.Output<string>;

    constructor(name: string, args: StaticSiteArgs, opts?: pulumi.ComponentResourceOptions) {
        // 1. Call super with type URN: <package>:<module>:<type>
        super("myorg:index:StaticSite", name, {}, opts);

        // 2. Create child resources with parent: this
        const bucket = new aws.s3.Bucket(`${name}-bucket`, {}, { parent: this });

        const website = new aws.s3.BucketWebsiteConfigurationV2(`${name}-website`, {
            bucket: bucket.id,
            indexDocument: { suffix: args.indexDocument ?? "index.html" },
            errorDocument: { key: args.errorDocument ?? "error.html" },
        }, { parent: this });

        // 3. Expose outputs as class properties
        this.bucketName = bucket.id;
        this.websiteUrl = website.websiteEndpoint;

        // 4. Register outputs -- always the last line
        this.registerOutputs({
            bucketName: this.bucketName,
            websiteUrl: this.websiteUrl,
        });
    }
}

// Usage
const site = new StaticSite("marketing", {
    indexDocument: "index.html",
});
export const url = site.websiteUrl;
```

### Python

```python
import pulumi
import pulumi_aws as aws

class StaticSiteArgs:
    def __init__(self,
                 index_document: pulumi.Input[str] = "index.html",
                 error_document: pulumi.Input[str] = "error.html"):
        self.index_document = index_document
        self.error_document = error_document

class StaticSite(pulumi.ComponentResource):
    bucket_name: pulumi.Output[str]
    website_url: pulumi.Output[str]

    def __init__(self, name: str, args: StaticSiteArgs,
                 opts: pulumi.ResourceOptions = None):
        super().__init__("myorg:index:StaticSite", name, None, opts)

        bucket = aws.s3.Bucket(f"{name}-bucket",
            opts=pulumi.ResourceOptions(parent=self))

        website = aws.s3.BucketWebsiteConfigurationV2(f"{name}-website",
            bucket=bucket.id,
            index_document=aws.s3.BucketWebsiteConfigurationV2IndexDocumentArgs(
                suffix=args.index_document,
            ),
            error_document=aws.s3.BucketWebsiteConfigurationV2ErrorDocumentArgs(
                key=args.error_document,
            ),
            opts=pulumi.ResourceOptions(parent=self))

        self.bucket_name = bucket.id
        self.website_url = website.website_endpoint

        self.register_outputs({
            "bucket_name": self.bucket_name,
            "website_url": self.website_url,
        })

site = StaticSite("marketing", StaticSiteArgs())
pulumi.export("url", site.website_url)
```

### Type URN Format

The first argument to `super()` is the type URN: `<package>:<module>:<type>`.

| Segment | Convention | Example |
|---------|-----------|---------|
| package | Organization or package name | `myorg`, `acme`, `pkg` |
| module  | Usually `index` | `index` |
| type    | PascalCase class name | `StaticSite`, `VpcNetwork` |

Full examples: `myorg:index:StaticSite`, `acme:index:KubernetesCluster`

### registerOutputs Is Required

**Why**: Without `registerOutputs()`, the component appears stuck in a "creating" state in the Pulumi console and outputs are not persisted to state.

**Wrong**:

```typescript
class MyComponent extends pulumi.ComponentResource {
    public readonly url: pulumi.Output<string>;

    constructor(name: string, args: MyArgs, opts?: pulumi.ComponentResourceOptions) {
        super("myorg:index:MyComponent", name, {}, opts);
        const bucket = new aws.s3.Bucket(`${name}-bucket`, {}, { parent: this });
        this.url = bucket.bucketRegionalDomainName;
        // Missing registerOutputs -- component stuck "creating"
    }
}
```

**Right**:

```typescript
class MyComponent extends pulumi.ComponentResource {
    public readonly url: pulumi.Output<string>;

    constructor(name: string, args: MyArgs, opts?: pulumi.ComponentResourceOptions) {
        super("myorg:index:MyComponent", name, {}, opts);
        const bucket = new aws.s3.Bucket(`${name}-bucket`, {}, { parent: this });
        this.url = bucket.bucketRegionalDomainName;

        this.registerOutputs({ url: this.url });
    }
}
```

### Derive Child Names from the Component Name

**Why**: Hardcoded child names cause collisions when the component is instantiated multiple times.

**Wrong**:

```typescript
// Collides if two instances of this component exist
const bucket = new aws.s3.Bucket("my-bucket", {}, { parent: this });
```

**Right**:

```typescript
// Unique per component instance
const bucket = new aws.s3.Bucket(`${name}-bucket`, {}, { parent: this });
```

---

## Designing the Args Interface

The args interface is the most impactful design decision. It defines what consumers can configure and how composable the component is.

### Wrap Properties in Input<T>

**Why**: `Input<T>` accepts both plain values and `Output<T>` from other resources. Without it, consumers must unwrap outputs manually with `.apply()`.

**Wrong**:

```typescript
interface WebServiceArgs {
    port: number;            // Forces consumers to unwrap Outputs
    vpcId: string;           // Cannot accept vpc.id directly
}
```

**Right**:

```typescript
interface WebServiceArgs {
    port: pulumi.Input<number>;     // Accepts 8080 or someOutput
    vpcId: pulumi.Input<string>;    // Accepts "vpc-123" or vpc.id
}
```

### Keep Structures Flat

Avoid deeply nested arg objects. Flat interfaces are easier to use and evolve.

```typescript
// Prefer flat
interface DatabaseArgs {
    instanceClass: pulumi.Input<string>;
    storageGb: pulumi.Input<number>;
    enableBackups?: pulumi.Input<boolean>;
    backupRetentionDays?: pulumi.Input<number>;
}

// Avoid deep nesting
interface DatabaseArgs {
    instance: {
        compute: { class: pulumi.Input<string> };
        storage: { sizeGb: pulumi.Input<number> };
    };
    backup: {
        config: { enabled: pulumi.Input<boolean>; retention: pulumi.Input<number> };
    };
}
```

### No Union Types

Union types break multi-language SDK generation. Python, Go, and C# cannot represent `string | number`.

**Wrong**:

```typescript
interface MyArgs {
    port: pulumi.Input<string | number>;  // Fails in Python, Go, C#
}
```

**Right**:

```typescript
interface MyArgs {
    port: pulumi.Input<number>;  // Single type, works everywhere
}
```

If you need to accept multiple forms, use separate optional properties:

```typescript
interface StorageArgs {
    sizeGb?: pulumi.Input<number>;      // Specify size in GB
    sizeMb?: pulumi.Input<number>;      // Or specify size in MB
}
```

### No Functions or Callbacks

Functions cannot be serialized across language boundaries.

**Wrong**:

```typescript
interface MyArgs {
    nameTransform: (name: string) => string;  // Cannot serialize
}
```

**Right**:

```typescript
interface MyArgs {
    namePrefix?: pulumi.Input<string>;   // Configuration instead of callback
    nameSuffix?: pulumi.Input<string>;
}
```

### Use Defaults for Optional Properties

Set sensible defaults inside the constructor so consumers only configure what they need:

```typescript
interface SecureBucketArgs {
    enableVersioning?: pulumi.Input<boolean>;   // Defaults to true
    enableEncryption?: pulumi.Input<boolean>;   // Defaults to true
    blockPublicAccess?: pulumi.Input<boolean>;  // Defaults to true
}

class SecureBucket extends pulumi.ComponentResource {
    constructor(name: string, args: SecureBucketArgs, opts?: pulumi.ComponentResourceOptions) {
        super("myorg:index:SecureBucket", name, {}, opts);

        const enableVersioning = args.enableVersioning ?? true;
        const enableEncryption = args.enableEncryption ?? true;
        const blockPublicAccess = args.blockPublicAccess ?? true;

        // Apply defaults...
    }
}

// Consumer only overrides what they need
const bucket = new SecureBucket("data", { enableVersioning: false });
```

---

## Exposing Outputs

### Expose Only What Consumers Need

Components often create many internal resources. Expose only the values consumers need, not every internal resource.

**Wrong**:

```typescript
class Database extends pulumi.ComponentResource {
    // Exposes everything -- consumers see implementation details
    public readonly cluster: aws.rds.Cluster;
    public readonly primaryInstance: aws.rds.ClusterInstance;
    public readonly replicaInstance: aws.rds.ClusterInstance;
    public readonly subnetGroup: aws.rds.SubnetGroup;
    public readonly securityGroup: aws.ec2.SecurityGroup;
    public readonly parameterGroup: aws.rds.ClusterParameterGroup;
    // ...
}
```

**Right**:

```typescript
class Database extends pulumi.ComponentResource {
    // Exposes only what consumers need
    public readonly endpoint: pulumi.Output<string>;
    public readonly port: pulumi.Output<number>;
    public readonly securityGroupId: pulumi.Output<string>;

    constructor(name: string, args: DatabaseArgs, opts?: pulumi.ComponentResourceOptions) {
        super("myorg:index:Database", name, {}, opts);

        const sg = new aws.ec2.SecurityGroup(`${name}-sg`, { /* ... */ }, { parent: this });
        const cluster = new aws.rds.Cluster(`${name}-cluster`, { /* ... */ }, { parent: this });

        this.endpoint = cluster.endpoint;
        this.port = cluster.port;
        this.securityGroupId = sg.id;

        this.registerOutputs({
            endpoint: this.endpoint,
            port: this.port,
            securityGroupId: this.securityGroupId,
        });
    }
}
```

### Derive Composite Outputs

Use `pulumi.interpolate` or `pulumi.concat` to build derived values:

```typescript
this.connectionString = pulumi.interpolate`postgresql://${args.username}:${args.password}@${cluster.endpoint}:${cluster.port}/${args.databaseName}`;

this.registerOutputs({ connectionString: this.connectionString });
```

---

## Component Design Patterns

### Sensible Defaults with Override

Encode best practices as defaults. Allow consumers to override when they have specific requirements.

```typescript
interface SecureBucketArgs {
    enableVersioning?: pulumi.Input<boolean>;
    enableEncryption?: pulumi.Input<boolean>;
    blockPublicAccess?: pulumi.Input<boolean>;
    tags?: pulumi.Input<Record<string, pulumi.Input<string>>>;
}

class SecureBucket extends pulumi.ComponentResource {
    public readonly bucketId: pulumi.Output<string>;
    public readonly arn: pulumi.Output<string>;

    constructor(name: string, args: SecureBucketArgs = {}, opts?: pulumi.ComponentResourceOptions) {
        super("myorg:index:SecureBucket", name, {}, opts);

        const bucket = new aws.s3.Bucket(`${name}-bucket`, {
            tags: args.tags,
        }, { parent: this });

        // Versioning on by default
        if (args.enableVersioning !== false) {
            new aws.s3.BucketVersioningV2(`${name}-versioning`, {
                bucket: bucket.id,
                versioningConfiguration: { status: "Enabled" },
            }, { parent: this });
        }

        // Encryption on by default
        if (args.enableEncryption !== false) {
            new aws.s3.BucketServerSideEncryptionConfigurationV2(`${name}-encryption`, {
                bucket: bucket.id,
                rules: [{ applyServerSideEncryptionByDefault: { sseAlgorithm: "AES256" } }],
            }, { parent: this });
        }

        // Public access blocked by default
        if (args.blockPublicAccess !== false) {
            new aws.s3.BucketPublicAccessBlock(`${name}-public-access`, {
                bucket: bucket.id,
                blockPublicAcls: true,
                blockPublicPolicy: true,
                ignorePublicAcls: true,
                restrictPublicBuckets: true,
            }, { parent: this });
        }

        this.bucketId = bucket.id;
        this.arn = bucket.arn;
        this.registerOutputs({ bucketId: this.bucketId, arn: this.arn });
    }
}
```

### Conditional Resource Creation

Use optional args to gate creation of sub-resources:

```typescript
interface WebServiceArgs {
    image: pulumi.Input<string>;
    port: pulumi.Input<number>;
    enableMonitoring?: pulumi.Input<boolean>;
    alarmEmail?: pulumi.Input<string>;
}

class WebService extends pulumi.ComponentResource {
    constructor(name: string, args: WebServiceArgs, opts?: pulumi.ComponentResourceOptions) {
        super("myorg:index:WebService", name, {}, opts);

        const service = new aws.ecs.Service(`${name}-service`, {
            // ...service config...
        }, { parent: this });

        // Only create alarm infrastructure when monitoring is enabled
        if (args.enableMonitoring) {
            const topic = new aws.sns.Topic(`${name}-alerts`, {}, { parent: this });

            if (args.alarmEmail) {
                new aws.sns.TopicSubscription(`${name}-alert-email`, {
                    topic: topic.arn,
                    protocol: "email",
                    endpoint: args.alarmEmail,
                }, { parent: this });
            }

            new aws.cloudwatch.MetricAlarm(`${name}-cpu-alarm`, {
                // ...alarm config referencing service...
                alarmActions: [topic.arn],
            }, { parent: this });
        }

        this.registerOutputs({});
    }
}
```

### Composition

Build higher-level components from lower-level ones. Each level manages a single concern.

```typescript
// Lower-level component
class VpcNetwork extends pulumi.ComponentResource {
    public readonly vpcId: pulumi.Output<string>;
    public readonly publicSubnetIds: pulumi.Output<string>[];
    public readonly privateSubnetIds: pulumi.Output<string>[];

    constructor(name: string, args: VpcNetworkArgs, opts?: pulumi.ComponentResourceOptions) {
        super("myorg:index:VpcNetwork", name, {}, opts);
        // ...create VPC, subnets, route tables...
        this.registerOutputs({ vpcId: this.vpcId });
    }
}

// Higher-level component that uses VpcNetwork
class Platform extends pulumi.ComponentResource {
    public readonly kubeconfig: pulumi.Output<string>;

    constructor(name: string, args: PlatformArgs, opts?: pulumi.ComponentResourceOptions) {
        super("myorg:index:Platform", name, {}, opts);

        // Compose lower-level components
        const network = new VpcNetwork(`${name}-network`, {
            cidrBlock: args.cidrBlock,
        }, { parent: this });

        const cluster = new aws.eks.Cluster(`${name}-cluster`, {
            vpcConfig: {
                subnetIds: network.privateSubnetIds,
            },
        }, { parent: this });

        this.kubeconfig = cluster.kubeconfig;
        this.registerOutputs({ kubeconfig: this.kubeconfig });
    }
}
```

### Provider Passthrough

Accept explicit providers for multi-region or multi-account deployments. `ComponentResourceOptions` carries provider configuration to children automatically:

```typescript
// Consumer passes a provider for a different region
const usWest = new aws.Provider("us-west", { region: "us-west-2" });
const site = new StaticSite("west-site", { indexDocument: "index.html" }, {
    providers: [usWest],
});
```

Children with `{ parent: this }` automatically inherit the provider. No extra code is needed inside the component.

---

## Multi-Language Components

If your component will be consumed from multiple Pulumi languages (TypeScript, Python, Go, C#, Java, YAML), package it as a multi-language component.

### Do You Need Multi-Language?

Ask: "Will anyone consume this component from a different language than it was authored in?"

**Single-language component** (no packaging needed):

- Your team uses one language and the component stays within that codebase
- The component is internal to a single project or monorepo
- No `PulumiPlugin.yaml` needed -- just import the class directly

**Multi-language component** (packaging required):

- Other teams consume your component in different languages
- Platform teams building abstractions for developers who choose their own language
- YAML consumers need access -- even if you author in TypeScript, YAML programs require multi-language packaging to use your component
- Building a shared component library for your organization
- Publishing to the Pulumi private registry or public registry is a common reason, but not required for multi-language support

**Common mistake**: A TypeScript platform team builds components only their TypeScript users can consume. If application developers use Python or YAML, those components are invisible to them without multi-language packaging.

### Setup

Create a `PulumiPlugin.yaml` in the component directory to declare the runtime:

```yaml
runtime: nodejs
```

Or for Python:

```yaml
runtime: python
```

### Serialization Constraints

For multi-language compatibility, args must be serializable. These constraints apply regardless of the authoring language:

| Allowed | Not Allowed |
|---------|-------------|
| `string`, `number`, `boolean` | Union types (`string \| number`) |
| `Input<T>` wrappers | Functions and callbacks |
| Arrays and maps of primitives | Complex nested generics |
| Enums | Platform-specific types |

### Consuming Multi-Language Components

Consumers install the component with `pulumi package add`, which automatically downloads the provider plugin, generates a local SDK in the consumer's language, and updates `Pulumi.yaml`:

```bash
# From a Git repository
pulumi package add <git-repo-url>

# From a specific version tag
pulumi package add <git-repo-url>@v1.0.0
```

For fresh checkouts or CI environments, run `pulumi install` to ensure all package dependencies are available. The consumer does not need to manually generate SDKs.

Authors who publish SDKs to package managers (npm, PyPI, etc.) can optionally use `pulumi package gen-sdk` to generate language-specific SDKs for publishing. Most component authors do not need this -- `pulumi package add` handles SDK generation on the consumer side.

### Entry Points

Published multi-language components require an entry point that hosts the component provider process. The entry point pattern differs by language.

**TypeScript** (`runtime: nodejs`):

Export component classes from `index.ts`. No separate entry point file is needed. Pulumi introspects exported classes automatically.

```typescript
// index.ts -- exports are the entry point
export { StaticSite, StaticSiteArgs } from "./staticSite";
export { SecureBucket, SecureBucketArgs } from "./secureBucket";
```

**Python** (`runtime: python`):

Create a `__main__.py` that calls `component_provider_host` with all component classes:

```python
from pulumi.provider.experimental import component_provider_host
from static_site import StaticSite
from secure_bucket import SecureBucket

if __name__ == "__main__":
    component_provider_host(
        name="my-components",
        components=[StaticSite, SecureBucket],
    )
```

**Go** (`runtime: go`):

Create a `main.go` that builds and runs the provider:

```go
package main

import (
    "context"
    "fmt"
    "os"

    "github.com/pulumi/pulumi-go-provider/infer"
)

func main() {
    p, err := infer.NewProviderBuilder().
        WithComponents(
            infer.ComponentF(NewStaticSite),
            infer.ComponentF(NewSecureBucket),
        ).
        Build()
    if err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }
    if err := p.Run(context.Background(), "my-components", "0.1.0"); err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }
}
```

**C#** (`runtime: dotnet`):

Create a `Program.cs` that serves the component provider host:

```csharp
using System.Threading.Tasks;

class Program
{
    public static Task Main(string[] args) =>
        Pulumi.Experimental.Provider.ComponentProviderHost.Serve(args);
}
```

For a complete working example across all languages, see https://github.com/mikhailshilkov/comp-as-comp.

**Reference**: https://www.pulumi.com/docs/iac/using-pulumi/pulumi-packages/

---

## Distribution

Choose a distribution method based on your audience:

| Audience | Method | How |
|----------|--------|-----|
| Same project | Direct import | Standard language import |
| Same organization | Private registry | `pulumi package publish` to Pulumi Cloud |
| Same organization | Git repository | `pulumi package add <repo>` with version tags |
| Language ecosystem | Package manager | Publish to npm, PyPI, NuGet, or Maven |
| Public community | Pulumi Registry | Submit via pulumi/registry GitHub repo |

### Pulumi Private Registry

The private registry is the centralized catalog for your organization's components. It provides automatic API documentation, version management, and discoverability for all teams.

Publish a component to the private registry:

```bash
pulumi package publish https://github.com/myorg/my-component --publisher myorg
```

Version components using git tags with a `v` prefix:

```bash
git tag v1.0.0
git push origin v1.0.0
```

A README file is required when publishing. Pulumi uses it as the component's documentation page in the registry.

Automate publishing from GitHub Actions using OIDC authentication:

```yaml
name: Publish Component
on:
  push:
    tags:
      - "v*"

permissions:
  id-token: write
  contents: read

jobs:
  publish:
    runs-on: ubuntu-latest
    env:
      PULUMI_ORG: myorg
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: pulumi/auth-actions@v1
        with:
          organization: ${{ env.PULUMI_ORG }}
          requested-token-type: urn:pulumi:token-type:access_token:organization
      - run: pulumi package publish https://github.com/${{ github.repository }} --publisher ${{ env.PULUMI_ORG }}
```

**Prerequisites**: Configure GitHub OIDC integration with Pulumi Cloud before using this workflow.

The registry supports private GitHub and GitLab repositories. For non-OIDC setups, authenticate with `GITHUB_TOKEN` or `GITLAB_TOKEN` environment variables.

The private registry automatically generates SDK documentation for each published component. Enrich the generated docs by adding type annotations to your component's inputs and outputs (JSDoc in TypeScript, docstrings in Python, `Annotate()` methods in Go).

**Reference**: https://www.pulumi.com/docs/idp/get-started/private-registry/

### Git Repository Distribution

Tag releases for consumers to pin versions:

```bash
git tag v1.0.0
git push origin v1.0.0
```

Consumers install with:

```bash
pulumi package add https://github.com/myorg/my-component@v1.0.0
```

### Package Manager Distribution

Publish language-specific packages for native dependency management:

- **npm**: `npm publish` for TypeScript/JavaScript
- **PyPI**: `twine upload` for Python
- **NuGet**: `dotnet nuget push` for .NET
- **Maven Central**: Standard Maven publishing for Java

**Reference**: https://www.pulumi.com/docs/iac/using-pulumi/pulumi-packages/

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Resources inside `apply()` | Not visible in `pulumi preview` | Move resource creation outside apply (see `pulumi-best-practices` practice 1) |
| Missing `registerOutputs()` | Component stuck "creating" | Always call as last line of constructor |
| Missing `parent: this` | Children appear at root level | Pass `{ parent: this }` to all child resources |
| Union types in args | Breaks Python, Go, C# SDKs | Use single types; separate properties for variants |
| Functions in args | Cannot serialize across languages | Use configuration properties instead |
| Hardcoded child names | Collisions with multiple instances | Derive names from `${name}-suffix` |
| Over-exposed outputs | Leaks implementation details | Export only what consumers need |
| Single-use component | Unnecessary abstraction overhead | Use inline resources until a pattern repeats |
| Deeply nested args | Hard to use and evolve | Keep interfaces flat with optional properties |

---

## Quick Reference

| Topic | Key Point |
|-------|-----------|
| Type URN | `<package>:<module>:<type>`, module usually `index` |
| Constructor | `super(type, name, {}, opts)` then children then `registerOutputs()` |
| Child resources | Always `{ parent: this }`, derive name from `${name}-suffix` |
| Args interface | Wrap in `Input<T>`, no unions, no functions, flat structure |
| Outputs | Public readonly `Output<T>` properties, expose only essentials |
| Defaults | Use `??` operator to apply sensible defaults in constructor |
| Composition | Lower-level components composed into higher-level ones |
| Multi-language | `PulumiPlugin.yaml` + entry point; consumers use `pulumi package add` |
| Distribution | Private registry, git tags, package managers, or public Pulumi Registry |

## Related Skills

- **pulumi-best-practices**: General Pulumi patterns including Output handling, secrets, and aliases
- **pulumi-automation-api**: Programmatic orchestration for integration testing and multi-stack workflows
- **pulumi-esc**: Centralized secrets and configuration for component deployments

## References

- https://www.pulumi.com/docs/iac/concepts/resources/components/
- https://www.pulumi.com/docs/iac/using-pulumi/pulumi-packages/
- https://www.pulumi.com/docs/idp/get-started/private-registry/
- https://www.pulumi.com/docs/iac/concepts/inputs-outputs/
- https://www.pulumi.com/docs/iac/concepts/resources/options/aliases/
