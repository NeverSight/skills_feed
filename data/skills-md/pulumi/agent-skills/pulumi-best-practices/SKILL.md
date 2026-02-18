---
name: pulumi-best-practices
version: 1.0.0
description: Best practices for writing reliable Pulumi programs. Covers Output handling, resource dependencies, component structure, secrets management, safe refactoring with aliases, and deployment workflows.
---

# Pulumi Best Practices

## When to Use This Skill

Invoke this skill when:

- Writing new Pulumi programs or components
- Reviewing Pulumi code for correctness
- Refactoring existing Pulumi infrastructure
- Debugging resource dependency issues
- Setting up configuration and secrets

## Practices

### 1. Never Create Resources Inside `apply()`

**Why**: Resources created inside `apply()` don't appear in `pulumi preview`, making changes unpredictable. Pulumi cannot properly track dependencies, leading to race conditions and deployment failures.

**Detection signals**:

- `new aws.` or other resource constructors inside `.apply()` callbacks
- Resource creation inside `pulumi.all([...]).apply()`
- Dynamic resource counts determined at runtime inside apply

**Wrong**:

```typescript
const bucket = new aws.s3.Bucket("bucket");

bucket.id.apply(bucketId => {
    // WRONG: This resource won't appear in preview
    new aws.s3.BucketObject("object", {
        bucket: bucketId,
        content: "hello",
    });
});
```

**Right**:

```typescript
const bucket = new aws.s3.Bucket("bucket");

// Pass the output directly - Pulumi handles the dependency
const object = new aws.s3.BucketObject("object", {
    bucket: bucket.id,  // Output<string> works here
    content: "hello",
});
```

**When apply is appropriate**:

- Transforming output values for use in tags, names, or computed strings
- Logging or debugging (not resource creation)
- Conditional logic that affects resource properties, not resource existence

**Reference**: https://www.pulumi.com/docs/concepts/inputs-outputs/

---

### 2. Pass Outputs Directly as Inputs

**Why**: Pulumi builds a directed acyclic graph (DAG) based on input/output relationships. Passing outputs directly ensures correct creation order. Unwrapping values manually breaks the dependency chain, causing resources to deploy in wrong order or reference values that don't exist yet.

**Detection signals**:

- Variables extracted from `.apply()` used later as resource inputs
- `await` on output values outside of apply
- String concatenation with outputs instead of `pulumi.interpolate`

**Wrong**:

```typescript
const vpc = new aws.ec2.Vpc("vpc", { cidrBlock: "10.0.0.0/16" });

// WRONG: Extracting the value breaks the dependency chain
let vpcId: string;
vpc.id.apply(id => { vpcId = id; });

const subnet = new aws.ec2.Subnet("subnet", {
    vpcId: vpcId,  // May be undefined, no tracked dependency
    cidrBlock: "10.0.1.0/24",
});
```

**Right**:

```typescript
const vpc = new aws.ec2.Vpc("vpc", { cidrBlock: "10.0.0.0/16" });

const subnet = new aws.ec2.Subnet("subnet", {
    vpcId: vpc.id,  // Pass the Output directly
    cidrBlock: "10.0.1.0/24",
});
```

**For string interpolation**:

```typescript
// WRONG
const name = bucket.id.apply(id => `prefix-${id}-suffix`);

// RIGHT - use pulumi.interpolate for template literals
const name = pulumi.interpolate`prefix-${bucket.id}-suffix`;

// RIGHT - use pulumi.concat for simple concatenation
const name = pulumi.concat("prefix-", bucket.id, "-suffix");
```

**Reference**: https://www.pulumi.com/docs/concepts/inputs-outputs/

---

### 3. Use Components for Related Resources

**Why**: ComponentResource classes group related resources into reusable, logical units. Without components, your resource graph is flat, making it hard to understand which resources belong together, reuse patterns across stacks, or reason about your infrastructure at a higher level.

**Detection signals**:

- Multiple related resources created at top level without grouping
- Repeated resource patterns across stacks that should be abstracted
- Hard to understand resource relationships from the Pulumi console

**Wrong**:

```typescript
// Flat structure - no logical grouping, hard to reuse
const bucket = new aws.s3.Bucket("app-bucket");
const bucketPolicy = new aws.s3.BucketPolicy("app-bucket-policy", {
    bucket: bucket.id,
    policy: policyDoc,
});
const originAccessIdentity = new aws.cloudfront.OriginAccessIdentity("app-oai");
const distribution = new aws.cloudfront.Distribution("app-cdn", { /* ... */ });
```

**Right**:

```typescript
interface StaticSiteArgs {
    domain: string;
    content: pulumi.asset.AssetArchive;
}

class StaticSite extends pulumi.ComponentResource {
    public readonly url: pulumi.Output<string>;

    constructor(name: string, args: StaticSiteArgs, opts?: pulumi.ComponentResourceOptions) {
        super("myorg:components:StaticSite", name, args, opts);

        // Resources created here - see practice 4 for parent setup
        const bucket = new aws.s3.Bucket(`${name}-bucket`, {}, { parent: this });
        // ...

        this.url = distribution.domainName;
        this.registerOutputs({ url: this.url });
    }
}

// Reusable across stacks
const site = new StaticSite("marketing", {
    domain: "marketing.example.com",
    content: new pulumi.asset.FileArchive("./dist"),
});
```

**Component best practices**:

- Use a consistent type URN pattern: `organization:module:ComponentName`
- Call `registerOutputs()` at the end of the constructor
- Expose outputs as class properties for consumers
- Accept `ComponentResourceOptions` to allow callers to set providers, aliases, etc.

For in-depth component authoring guidance (args design, multi-language support, testing, distribution), use skill `pulumi-component`.

**Reference**: https://www.pulumi.com/docs/concepts/resources/components/

---

### 4. Always Set `parent: this` in Components

**Why**: When you create resources inside a ComponentResource without setting `parent: this`, those resources appear at the root level of your stack's state. This breaks the logical hierarchy, makes the Pulumi console hard to navigate, and can cause issues with aliases and refactoring. The parent relationship is what makes the component actually group its children.

**Detection signals**:

- ComponentResource classes that don't pass `{ parent: this }` to child resources
- Resources inside a component appearing at root level in the console
- Unexpected behavior when adding aliases to components

**Wrong**:

```typescript
class MyComponent extends pulumi.ComponentResource {
    constructor(name: string, opts?: pulumi.ComponentResourceOptions) {
        super("myorg:components:MyComponent", name, {}, opts);

        // WRONG: No parent set - this bucket appears at root level
        const bucket = new aws.s3.Bucket(`${name}-bucket`);
    }
}
```

**Right**:

```typescript
class MyComponent extends pulumi.ComponentResource {
    constructor(name: string, opts?: pulumi.ComponentResourceOptions) {
        super("myorg:components:MyComponent", name, {}, opts);

        // RIGHT: Parent establishes hierarchy
        const bucket = new aws.s3.Bucket(`${name}-bucket`, {}, {
            parent: this
        });

        const policy = new aws.s3.BucketPolicy(`${name}-policy`, {
            bucket: bucket.id,
            policy: policyDoc,
        }, {
            parent: this
        });
    }
}
```

**What parent: this provides**:

- Resources appear nested under the component in Pulumi console
- Deleting the component deletes all children
- Aliases on the component automatically apply to children
- Clear ownership in state files

**Reference**: https://www.pulumi.com/docs/concepts/resources/components/

---

### 5. Encrypt Secrets from Day One

**Why**: Secrets marked with `--secret` are encrypted in state files, masked in CLI output, and tracked through transformations. Starting with plaintext config and converting later requires credential rotation, reference updates, and audit of leaked values in logs and state history.

**Detection signals**:

- Passwords, API keys, tokens stored as plain config
- Connection strings with embedded credentials
- Private keys or certificates in plaintext

**Wrong**:

```bash
# Plaintext - will be visible in state and logs
pulumi config set databasePassword hunter2
pulumi config set apiKey sk-1234567890
```

**Right**:

```bash
# Encrypted from the start
pulumi config set --secret databasePassword hunter2
pulumi config set --secret apiKey sk-1234567890
```

**In code**:

```typescript
const config = new pulumi.Config();

// This retrieves a secret - the value stays encrypted
const dbPassword = config.requireSecret("databasePassword");

// Creating outputs from secrets preserves secrecy
const connectionString = pulumi.interpolate`postgres://user:${dbPassword}@host/db`;
// connectionString is also a secret Output

// Explicitly mark values as secret
const computed = pulumi.secret(someValue);
```

**Use Pulumi ESC for centralized secrets**:

```yaml
# Pulumi.yaml
environment:
  - production-secrets  # Pull from ESC environment
```

```bash
# ESC manages secrets centrally across stacks
esc env set production-secrets db.password --secret "hunter2"
```

**What qualifies as a secret**:

- Passwords and passphrases
- API keys and tokens
- Private keys and certificates
- Connection strings with credentials
- OAuth client secrets
- Encryption keys

**References**:

- https://www.pulumi.com/docs/concepts/secrets/
- https://www.pulumi.com/docs/esc/

---

### 6. Use Aliases When Refactoring

**Why**: Renaming resources, moving them into components, or changing parents causes Pulumi to see them as new resources. Without aliases, refactoring destroys and recreates resources, potentially causing downtime or data loss. Aliases preserve resource identity through refactors.

**Detection signals**:

- Resource rename without alias
- Moving resource into or out of a ComponentResource
- Changing the parent of a resource
- Preview shows delete+create when update was intended

**Wrong**:

```typescript
// Before: resource named "my-bucket"
const bucket = new aws.s3.Bucket("my-bucket");

// After: renamed without alias - DESTROYS THE BUCKET
const bucket = new aws.s3.Bucket("application-bucket");
```

**Right**:

```typescript
// After: renamed with alias - preserves the existing bucket
const bucket = new aws.s3.Bucket("application-bucket", {}, {
    aliases: [{ name: "my-bucket" }],
});
```

**Moving into a component**:

```typescript
// Before: top-level resource
const bucket = new aws.s3.Bucket("my-bucket");

// After: inside a component - needs alias with old parent
class MyComponent extends pulumi.ComponentResource {
    constructor(name: string, opts?: pulumi.ComponentResourceOptions) {
        super("myorg:components:MyComponent", name, {}, opts);

        const bucket = new aws.s3.Bucket("bucket", {}, {
            parent: this,
            aliases: [{
                name: "my-bucket",
                parent: pulumi.rootStackResource,  // Was at root
            }],
        });
    }
}
```

**Alias types**:

```typescript
// Simple name change
aliases: [{ name: "old-name" }]

// Parent change
aliases: [{ name: "resource-name", parent: oldParent }]

// Full URN (when you know the exact previous URN)
aliases: ["urn:pulumi:stack::project::aws:s3/bucket:Bucket::old-name"]
```

**Lifecycle**:

1. Add alias during refactor
2. Run `pulumi up` on all stacks
3. Remove alias after all stacks updated (optional, but keeps code clean)

**Reference**: https://www.pulumi.com/docs/iac/concepts/resources/options/aliases/

---

### 7. Preview Before Every Deployment

**Why**: `pulumi preview` shows exactly what will be created, updated, or destroyed. Surprises in production come from skipping preview. A resource showing "replace" when you expected "update" means imminent destruction and recreation.

**Detection signals**:

- Running `pulumi up --yes` interactively without reviewing changes
- No preview step anywhere in the CI/CD workflow for a given change
- Preview output not reviewed before merge or deployment approval

**Wrong**:

```bash
# Deploying blind
pulumi up --yes
```

**Right**:

```bash
# Always preview first
pulumi preview

# Review the output, then deploy
pulumi up
```

**What to look for in preview**:

- `+ create` - New resource will be created
- `~ update` - Existing resource will be modified in place
- `- delete` - Resource will be destroyed
- `+-replace` - Resource will be destroyed and recreated (potential downtime)
- `~+-replace` - Resource will be updated, then replaced

**Warning signs**:

- Unexpected `replace` operations (check for immutable property changes)
- Resources being deleted that shouldn't be
- More changes than expected from your code diff

**CI/CD integration**:

```yaml
# GitHub Actions example
jobs:
  preview:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Pulumi Preview
        uses: pulumi/actions@v5
        with:
          command: preview
          stack-name: production
        env:
          PULUMI_ACCESS_TOKEN: ${{ secrets.PULUMI_ACCESS_TOKEN }}

  deploy:
    needs: preview
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Pulumi Up
        uses: pulumi/actions@v5
        with:
          command: up
          stack-name: production
```

**PR workflow**:

- Run preview on every PR
- Post preview output as PR comment
- Require preview review before merge
- Deploy only on merge to main

**References**:

- https://www.pulumi.com/docs/cli/commands/pulumi_preview/
- https://www.pulumi.com/docs/iac/packages-and-automation/continuous-delivery/github-actions/

---

## Quick Reference

| Practice | Key Signal | Fix |
|----------|-----------|-----|
| No resources in apply | `new Resource()` inside `.apply()` | Move resource outside, pass Output directly |
| Pass outputs directly | Extracted values used as inputs | Use Output objects, `pulumi.interpolate` |
| Use components | Flat structure, repeated patterns | Create ComponentResource classes |
| Set parent: this | Component children at root level | Pass `{ parent: this }` to all child resources |
| Secrets from day one | Plaintext passwords/keys in config | Use `--secret` flag, ESC |
| Aliases when refactoring | Delete+create in preview | Add alias with old name/parent |
| Preview before deploy | `pulumi up --yes` | Always run `pulumi preview` first |

## Validation Checklist

When reviewing Pulumi code, verify:

- [ ] No resource constructors inside `apply()` callbacks
- [ ] Outputs passed directly to dependent resources
- [ ] Related resources grouped in ComponentResource classes
- [ ] Child resources have `{ parent: this }`
- [ ] Sensitive values use `config.requireSecret()` or `--secret`
- [ ] Refactored resources have aliases preserving identity
- [ ] Deployment process includes preview step

## Related Skills

- **pulumi-component**: Deep guide to authoring ComponentResource classes, designing args interfaces, multi-language support, testing, and distribution. Use skill `pulumi-component`.
- **pulumi-automation-api**: Programmatic orchestration of multiple stacks. Use skill `pulumi-automation-api`.
- **pulumi-esc**: Centralized secrets and configuration management. Use skill `pulumi-esc`.
