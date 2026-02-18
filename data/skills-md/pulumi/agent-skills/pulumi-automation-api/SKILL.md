---
name: pulumi-automation-api
version: 1.0.0
description: Best practices for using Pulumi Automation API to programmatically orchestrate infrastructure operations. Covers multi-stack orchestration, embedding Pulumi in applications, architecture choices, and common patterns.
---

# Pulumi Automation API

## When to Use This Skill

Invoke this skill when:

- Orchestrating deployments across multiple Pulumi stacks
- Embedding Pulumi operations in custom applications
- Building self-service infrastructure platforms
- Replacing fragile Bash/Makefile orchestration scripts
- Creating custom CLIs for infrastructure management
- Building web applications that provision infrastructure

## What is Automation API

Automation API provides programmatic access to Pulumi operations. Instead of running `pulumi up` from the CLI, you call functions in your code that perform the same operations.

```typescript
import * as automation from "@pulumi/pulumi/automation";

// Create or select a stack
const stack = await automation.LocalWorkspace.createOrSelectStack({
    stackName: "dev",
    projectName: "my-project",
    program: async () => {
        // Your Pulumi program here
    },
});

// Run pulumi up programmatically
const upResult = await stack.up({ onOutput: console.log });
console.log(`Update summary: ${JSON.stringify(upResult.summary)}`);
```

## When to Use Automation API

### Good Use Cases

**Multi-stack orchestration:**

When you split infrastructure into multiple focused projects, Automation API helps offset the added complexity by orchestrating operations across stacks:

```text
infrastructure → platform → application
     ↓              ↓            ↓
   (VPC)      (Kubernetes)   (Services)
```

Automation API ensures correct sequencing without manual intervention.

**Self-service platforms:**

Build internal tools where developers request infrastructure without learning Pulumi:

- Web portals for environment provisioning
- Slack bots that create/destroy resources
- Custom CLIs tailored to your organization

**Embedded infrastructure:**

Applications that provision their own infrastructure:

- SaaS platforms creating per-tenant resources
- Testing frameworks spinning up test environments
- CI/CD systems with dynamic infrastructure needs

**Replacing fragile scripts:**

If you have Bash scripts or Makefiles stitching together multiple `pulumi` commands, Automation API provides:

- Proper error handling
- Type safety
- Programmatic access to outputs

### When NOT to Use

- Single project with standard deployment needs
- When you don't need programmatic control over operations

## Architecture Choices

### Local Source vs Inline Source

**Local Source** - Pulumi program in separate files:

```typescript
const stack = await automation.LocalWorkspace.createOrSelectStack({
    stackName: "dev",
    workDir: "./infrastructure",  // Points to existing Pulumi project
});
```

**When to use:**

- Different teams maintain orchestrator vs Pulumi programs
- Pulumi programs already exist
- Want independent version control and release cycles
- Platform team orchestrating application team's infrastructure

**Inline Source** - Pulumi program embedded in orchestrator:

```typescript
import * as aws from "@pulumi/aws";

const stack = await automation.LocalWorkspace.createOrSelectStack({
    stackName: "dev",
    projectName: "my-project",
    program: async () => {
        const bucket = new aws.s3.Bucket("my-bucket");
        return { bucketName: bucket.id };
    },
});
```

**When to use:**

- Single team owns everything
- Tight coupling between orchestration and infrastructure is desired
- Distributing as compiled binary (no source files needed)
- Simpler deployment artifact

### Language Independence

The Automation API program can use a different language than the Pulumi programs it orchestrates:

```text
Orchestrator (Go) → manages → Pulumi Program (TypeScript)
```

This enables platform teams to use their preferred language while application teams use theirs.

## Common Patterns

### Multi-Stack Orchestration

Deploy multiple stacks in dependency order:

```typescript
import * as automation from "@pulumi/pulumi/automation";

async function deploy() {
    const stacks = [
        { name: "infrastructure", dir: "./infra" },
        { name: "platform", dir: "./platform" },
        { name: "application", dir: "./app" },
    ];

    for (const stackInfo of stacks) {
        console.log(`Deploying ${stackInfo.name}...`);

        const stack = await automation.LocalWorkspace.createOrSelectStack({
            stackName: "prod",
            workDir: stackInfo.dir,
        });

        await stack.up({ onOutput: console.log });
        console.log(`${stackInfo.name} deployed successfully`);
    }
}

async function destroy() {
    // Destroy in reverse order
    const stacks = [
        { name: "application", dir: "./app" },
        { name: "platform", dir: "./platform" },
        { name: "infrastructure", dir: "./infra" },
    ];

    for (const stackInfo of stacks) {
        console.log(`Destroying ${stackInfo.name}...`);

        const stack = await automation.LocalWorkspace.selectStack({
            stackName: "prod",
            workDir: stackInfo.dir,
        });

        await stack.destroy({ onOutput: console.log });
    }
}
```

### Passing Configuration

Set stack configuration programmatically:

```typescript
const stack = await automation.LocalWorkspace.createOrSelectStack({
    stackName: "dev",
    workDir: "./infrastructure",
});

// Set configuration values
await stack.setConfig("aws:region", { value: "us-west-2" });
await stack.setConfig("dbPassword", { value: "secret", secret: true });

// Then deploy
await stack.up();
```

### Reading Outputs

Access stack outputs after deployment:

```typescript
const upResult = await stack.up();

// Get all outputs
const outputs = await stack.outputs();
console.log(`VPC ID: ${outputs["vpcId"].value}`);

// Or from the up result
console.log(`Outputs: ${JSON.stringify(upResult.outputs)}`);
```

### Error Handling

Handle deployment failures gracefully:

```typescript
try {
    const result = await stack.up({ onOutput: console.log });

    if (result.summary.result === "failed") {
        console.error("Deployment failed");
        process.exit(1);
    }
} catch (error) {
    console.error(`Deployment error: ${error}`);
    throw error;
}
```

### Parallel Stack Operations

When stacks are independent, deploy in parallel:

```typescript
const independentStacks = [
    { name: "service-a", dir: "./service-a" },
    { name: "service-b", dir: "./service-b" },
    { name: "service-c", dir: "./service-c" },
];

await Promise.all(independentStacks.map(async (stackInfo) => {
    const stack = await automation.LocalWorkspace.createOrSelectStack({
        stackName: "prod",
        workDir: stackInfo.dir,
    });
    return stack.up({ onOutput: (msg) => console.log(`[${stackInfo.name}] ${msg}`) });
}));
```

## Best Practices

### Separate Configuration from Code

Externalize configuration into files or environment variables:

```typescript
import * as fs from "fs";

interface DeployConfig {
    stacks: Array<{ name: string; dir: string; }>;
    environment: string;
}

const config: DeployConfig = JSON.parse(
    fs.readFileSync("./deploy-config.json", "utf-8")
);

for (const stackInfo of config.stacks) {
    const stack = await automation.LocalWorkspace.createOrSelectStack({
        stackName: config.environment,
        workDir: stackInfo.dir,
    });
    await stack.up();
}
```

This enables distributing compiled binaries without exposing source code.

### Stream Output for Long Operations

Use `onOutput` callback for real-time feedback:

```typescript
await stack.up({
    onOutput: (message) => {
        process.stdout.write(message);
        // Or send to logging system, websocket, etc.
    },
});
```

## Quick Reference

| Scenario | Approach |
| --- | --- |
| Existing Pulumi projects | Local source with workDir |
| New embedded infrastructure | Inline source with program function |
| Different teams | Local source for independence |
| Compiled binary distribution | Inline source or bundled local |
| Multi-stack dependencies | Sequential deployment in order |
| Independent stacks | Parallel deployment with Promise.all |

## Related Skills

- **pulumi-best-practices**: Code-level patterns for Pulumi programs

## References

- https://www.pulumi.com/docs/using-pulumi/automation-api/
- https://www.pulumi.com/docs/using-pulumi/automation-api/concepts-terminology/
- https://www.pulumi.com/blog/iac-recommended-practices-using-automation-api/
