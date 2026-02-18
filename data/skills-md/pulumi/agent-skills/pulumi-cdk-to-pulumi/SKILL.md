---
name: pulumi-cdk-to-pulumi
description: Convert an AWS CDK application to Pulumi. This skill MUST be loaded whenever a user requests migration or conversion of a CDK application to Pulumi.
---

# CRITICAL SUCCESS REQUIREMENTS

The migration output MUST meet all of the following:

1. **Complete Resource Coverage**
   - Every CloudFormation resource synthesized by CDK MUST:
     - Be represented in the Pulumi program **OR**
     - Be explicitly justified in the final report.

2. **Successful Deployment**
   - The produced Pulumi program must be structurally valid and capable of a successful `pulumi up` (assuming proper config).

3. **Final Migration Report**
   - Always output a formal migration report suitable for a Pull Request.
   - Include:
     - CDK → Pulumi resource mapping
     - Provider decisions (aws-native vs aws)
     - Behavioral differences
     - Missing or manually required steps
     - Validation instructions

## WHEN INFORMATION IS MISSING

If a user-provided CDK project is incomplete, ambiguous, or missing artifacts (such as `cdk.out`), ask **targeted questions** before generating Pulumi code.

## MIGRATION WORKFLOW

Follow this workflow **exactly** and in this order:

### 1. INFORMATION GATHERING

#### 1.1 Verify AWS Credentials (ESC)

Running AWS commands (e.g., `aws cloudformation list-stack-resources`) and CDK commands (e.g. `cdk synth`) requires credentials loaded via Pulumi ESC.

- If the user has already provided an ESC environment, use it.
- If no ESC environment is specified, **ask the user which ESC environment to use** before proceeding with AWS commands.

You MUST confirm the AWS region with the user. The `cdk synth` results may be incorrect if ran with the wrong AWS Region.

#### 1.2 Synthesize CDK

Run/inspect:

```bash
npx cdk synth --quiet
```

- ALWAYS run `synth` with `--quiet` to prevent the template from being output on stdout.

If failing, inspect `cdk.json` or `package.json` for custom synth behavior.

#### 1.3 Identify CDK Stacks & Environments

Read `cdk.out/manifest.json`:

```bash
jq '.artifacts | to_entries | map(select(.value.type == "aws:cloudformation:stack") | {displayName: .key, environment: .value.environment}) | .[]' cdk.out/manifest.json
```

Example output:

```json
{
  "displayName": "DataStack-dev",
  "environment": "aws://616138583583/us-east-2"
}
{
  "displayName": "AppStack-dev",
  "environment": "aws://616138583583/us-east-2"
}
```

In the Pulumi stack you create you MUST set both the `aws:region` and `aws-native:region` config variables. For example:

```bash
pulumi config set aws-native:region us-east-2 --stack dev
pulumi config set aws:region us-east-2 --stack dev
```

#### 1.4 Build Resource Inventory

For each stack:

```bash
aws cloudformation list-stack-resources \
  --region <region> \
  --stack-name <stack> \
  --output json
```

#### 1.5 Analyze CDK Structure

Extract:

- Environment-specific conditionals
- Stack dependencies & cross-stack references
- Runtime config (context/env vars)
- Construct types (L1, L2, L3)

### 2. CODE CONVERSION (CDK → PULUMI)

- Perform the initial conversion using the `cdk2pulumi` tool. Follow [cdk-convert.md](cdk-convert.md) to perform the conversion.
- Read the conversion report and fill in any gaps. For example, if the conversion fails to convert a resource you have to convert it manually yourself.

#### 2.1 Custom Resources Handling

CDK uses Lambda-backed Custom Resources for functionality not available in CloudFormation. In synthesized CloudFormation, these appear as:

- Resource type: `AWS::CloudFormation::CustomResource` or `Custom::<name>`
- Metadata contains `aws:cdk:path` with the handler name (e.g., `aws-s3/auto-delete-objects-handler`)

**Default behavior**: `cdk2pulumi` rewrites custom resources to `aws-native:cloudformation:CustomResourceEmulator`, which invokes the original Lambda. This works but has tradeoffs (Lambda dependency, cold starts, eventual consistency).

**Migration strategies by handler type:**

| Handler | Strategy |
|---------|----------|
| `aws-certificatemanager/dns-validated-certificate-handler` | Replace with `aws.acm.Certificate`, `aws.route53.Record`, and `aws.acm.CertificateValidation` |
| `aws-ec2/restrict-default-security-group-handler` | Replace with `aws.ec2.DefaultSecurityGroup` resource with empty ingress/egress rules |
| `aws-ecr/auto-delete-images-handler` | Replace `aws-native:ecr:Repository` with `aws.ecr.Repository` with `forceDelete: true` |
| `aws-s3/auto-delete-objects-handler` | Replace `aws-native:s3:Bucket` with `aws.s3.Bucket` with `forceDestroy: true` |
| `aws-s3/notifications-resource-handler` | Replace with `aws.s3.BucketNotification` |
| `aws-logs/log-retention-handler` | Replace with `aws.cloudwatch.LogGroup` with explicit `retentionInDays` |
| `aws-iam/oidc-handler` | Replace with `aws.iam.OpenIdConnectProvider` |
| `aws-route53/delete-existing-record-set-handler` | Replace with `aws.route53.Record` with `allowOverwrite: true` |
| `aws-dynamodb/replica-handler` | Replace with `aws.dynamodb.TableReplica` |

**Cross-account/region handlers:**

- `aws-cloudfront/edge-function` → Use `aws.lambda.Function` with `region: "us-east-1"`
- `aws-route53/cross-account-zone-delegation-handler` → Use separate aws provider with cross-account role assumption

**Graceful degradation for unknown handlers:**

1. Keep the `CustomResourceEmulator` (default behavior)
2. Document the custom resource in the migration report with:
   - Original handler name and purpose (if discernible from CDK path)
   - Note that it uses Lambda invocation at runtime
   - Recommend user review for potential native replacement

#### 2.2 Provider Strategy

- **Default**: Use `aws-native` whenever the resource type is available.
- **Fallback**: Use `aws` when aws-native does not support equivalent features.

#### 2.3 Assets & Bundling

CDK uses Assets and Bundling to handle deployment artifacts. These are processed by the CDK CLI before CloudFormation deployment and appear in the `cdk.out` directory alongside `*.assets.json` metadata files. CloudFormation templates contain hard-coded references to asset locations (S3 bucket/key or ECR repo/tag).

```bash
# Inspect asset definitions
jq '.files, .dockerImages' cdk.out/*.assets.json
```

**Migration strategies by asset type:**

| Asset Type | Detection | Pulumi Migration |
|------------|-----------|------------------|
| **Docker Image** | `dockerImages` in assets.json | Use `docker-build.Image` to build and push. Replace hard-coded ECR URI with image output. |
| **File with build command** | `files` with `executable` field | **Flag to user** - build command needs setup in Pulumi |
| **Static file** | `files` without `executable`, no bundling in CDK source | Use `pulumi.FileArchive` or `pulumi.FileAsset` |
| **Bundled file** | `files` without `executable`, but CDK source uses bundling | **Flag to user** - bundling needs setup in Pulumi |

**Detecting Bundling in CDK Source:**

Check the CDK source code for bundling constructs (`NodejsFunction`, `PythonFunction`, `GoFunction`, or resources using the `bundling` option). If bundling is used, the build step needs to be replicated in Pulumi for ongoing development - otherwise source changes would require manually re-running `cdk synth`.

**When bundling is detected, inform the user:**

> **Build Step Detected**: This CDK application uses <BUNDLING_TYPE> which builds deployable artifacts during synthesis. This build step needs to be replicated in Pulumi for ongoing development.
>
> **Options:**
>
> 1. **CI/CD Pipeline** (Recommended): Move the build step to your CI pipeline and reference the pre-built artifact in Pulumi
> 2. **Pulumi Command Provider**: Use `command.local.Command` to run the build command during `pulumi up`
> 3. **Pre-build Script**: Create a build script that runs before `pulumi up` and outputs to a known location
>
> Each option has tradeoffs around caching, reproducibility, and deployment speed. For production workloads, option 1 is typically preferred.

#### 2.4 TypeScript Handling for aws-native

aws-native outputs often include undefined. Avoid `!` non-null assertions. Always safely unwrap with `.apply()`:

```ts
// ❌ WRONG - Will cause TypeScript errors
functionName: lambdaFunction.functionName!,

// ✅ CORRECT - Handle undefined safely
functionName: lambdaFunction.functionName.apply(name => name || ""),
```

#### 2.5 Environment Logic Preservation

Carry forward all conditional behaviors:

```ts
if (currentEnv.createVpc) {
  // create resources
} else {
  const vpcId = pulumi.output(currentEnv.vpcId);
}
```

### 3. Resource Import (optional)

After conversion you can optionally import the existing resources to now be managed by Pulumi. If the user does not request this you should suggest this as a follow up step to conversion.

- Always start with automated import using the `cdk-importer` tool. Follow [cdk-importer.md](cdk-importer.md) to perform the automated import.
- For any resources that fail to import with the automated tool, import them manually.

If you need to manually import resources:

- Follow [cloudformation-id-lookup.md](cloudformation-id-lookup.md) to look up CloudFormation import identifiers.
- Use the web-fetch tool to get content from the official Pulumi documentation.

- **Finding AWS import IDs** -> <https://www.pulumi.com/docs/iac/guides/migration/aws-import-ids/>
- **Manual migration approaches** -> <https://www.pulumi.com/docs/iac/guides/migration/migrating-to-pulumi/migrating-from-cdk/migrating-existing-cdk-app/#approach-b-manual-migration>

#### 3.1 Running preview after import

After performing an import you need to run `pulumi preview` to ensure there are no changes. No changes means:

- NO updates
- NO replaces
- NO creates
- NO deletes

If there are changes you must investigate and update the program until there are no changes.

## Working with the User

If the user asks for help planning or performing a CDK to Pulumi migration use the information above to guide the user towards the automated migration approach.

## For Detailed Documentation

When the user wants to deviate from the recommended path detailed above, use the web-fetch tool to get content from the official Pulumi documentation -> <https://www.pulumi.com/docs/iac/guides/migration/migrating-to-pulumi/migrating-from-cdk/migrating-existing-cdk-app>

This documentation covers topics:

- Migration Strategy
  - Convert vs. Rewrite
  - Import vs. Rehydrate
  - Best Practices
- Handling Multiple CDK Stacks
- Handling CDK Stages
- Code organization
- Converting CDK Constructs
- Execution Strategies
  - Automated Migration (recommended)
  - Manual Migration

## OUTPUT FORMAT (REQUIRED)

When performing a migration, always produce:

1. **Overview** (high-level description)
2. **Migration Plan Summary**
3. **Pulumi Code Outputs** (TypeScript; structured by file)
4. **Resource Mapping Table** (CDK → Pulumi)
5. **Custom Resources Summary** (if any):
   - Handlers migrated to native Pulumi resources
   - Handlers kept as `CustomResourceEmulator` with rationale
   - Any handlers requiring user attention
6. **Assets & Bundling Summary** (if any):
   - **Migrated**: Assets successfully converted (e.g., Docker images → `docker-build.Image`, static files → `pulumi.FileArchive`)
   - **Requires attention**: Assets with bundling steps, options presented, and decision if made
7. **Final Migration Report** (PR-ready)
8. **Next Steps** (optional refactors)

Keep code syntactically valid and clearly separated by files.
