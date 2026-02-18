---
name: cloudformation-to-pulumi
description: Convert an AWS CloudFormation stack or template to Pulumi. This skill MUST be loaded whenever a user requests migration or conversion of CloudFormation to Pulumi.
---

## IMPORTANT: PLAN ADJUSTMENT REQUIRED

**If you have already generated a migration plan before loading this skill, you MUST:**
1. Review your existing plan against the workflows and requirements in this skill
2. Identify any gaps, missing steps, or incorrect assumptions
3. Update and revise your plan to align with this skill's guidance
4. Communicate the adjusted plan to the user before proceeding

## CRITICAL SUCCESS REQUIREMENTS

The migration output MUST meet all of the following:

1. **Complete Resource Coverage**
   - Every CloudFormation resource MUST be represented in the Pulumi program OR explicitly justified in the final report.

2. **CloudFormation Logical ID as Resource Name**
   - **CRITICAL**: Every Pulumi resource MUST use the CloudFormation Logical ID as its resource name.
   - This enables the `cdk-importer` tool to automatically find import IDs.
   - DO NOT rename resources. Automated import will FAIL if you change the logical IDs.

3. **Successful Deployment**
   - The produced Pulumi program must be structurally valid and capable of a successful `pulumi preview` (assuming proper config).

4. **Zero-Diff Import Validation** (if importing existing resources)
   - After import, `pulumi preview` must show NO updates, replaces, creates, or deletes.

5. **Final Migration Report**
   - Always output a formal migration report suitable for a Pull Request.

## WHEN INFORMATION IS MISSING

If the user has not provided a CloudFormation template, you MUST fetch it from AWS using the stack name.

## MIGRATION WORKFLOW

Follow this workflow **exactly** and in this order:

### 1. INFORMATION GATHERING

#### 1.1 Verify AWS Credentials (ESC)

Running AWS commands requires credentials loaded via Pulumi ESC.

- If the user has already provided an ESC environment, use it.
- If no ESC environment is specified, **ask the user which ESC environment to use** before proceeding.

**For detailed ESC information:** Use skill `pulumi-esc`.

You MUST confirm the AWS region with the user.

#### 1.2 Get the CloudFormation Template

**If user provided a template file**: Read the template directly.

**If user only provided a stack name**: Fetch the template from AWS:

```bash
aws cloudformation get-template \
  --region <region> \
  --stack-name <stack-name> \
  --query 'TemplateBody' \
  --output json > template.json
```

#### 1.3 Build Resource Inventory

List all resources in the stack:

```bash
aws cloudformation list-stack-resources \
  --region <region> \
  --stack-name <stack-name> \
  --output json
```

This provides:
- `LogicalResourceId` - **Use this as the Pulumi resource name**
- `PhysicalResourceId` - The actual AWS resource ID
- `ResourceType` - The CloudFormation resource type

#### 1.4 Analyze Template Structure

Extract from the template:
- Parameters and their defaults
- Mappings
- Conditions
- Outputs
- Resource dependencies (Ref, GetAtt, DependsOn)

### 2. CODE CONVERSION (CloudFormation → Pulumi)

**IMPORTANT:** There is NO automated conversion tool for CloudFormation. You MUST convert each resource manually.

#### 2.1 Resource Name Convention (CRITICAL)

**Every Pulumi resource MUST use the CloudFormation Logical ID as its name.**

```typescript
// CloudFormation:
// "MyAppBucketABC123": { "Type": "AWS::S3::Bucket", ... }

// Pulumi - CORRECT:
const myAppBucket = new aws.s3.Bucket("MyAppBucketABC123", { ... });

// Pulumi - WRONG (DO NOT do this - import will fail):
const myAppBucket = new aws.s3.Bucket("my-app-bucket", { ... });
```

This naming convention is REQUIRED because the `cdk-importer` tool matches resources by name.

#### 2.2 Provider Strategy

**⚠️ CRITICAL: ALWAYS USE aws-native BY DEFAULT ⚠️**

- Use `aws-native` for all resources unless there's a specific reason to use `aws`.
- CloudFormation types map directly to aws-native (e.g., `AWS::S3::Bucket` → `aws-native.s3.Bucket`).
- Only use `aws` (classic) when aws-native doesn't support a required feature.

**This is MANDATORY for successful imports with cdk-importer.** The cdk-importer works by matching CloudFormation resources to Pulumi resources, and CloudFormation maps 1:1 to aws-native. Using the classic `aws` provider will cause import failures.

#### 2.3 CloudFormation Intrinsic Functions

Map CloudFormation intrinsic functions to Pulumi equivalents:

| CloudFormation | Pulumi Equivalent |
|----------------|-------------------|
| `!Ref` (resource) | Resource output (e.g., `bucket.id`) |
| `!Ref` (parameter) | Pulumi config |
| `!GetAtt Resource.Attr` | Resource property output |
| `!Sub "..."` | `pulumi.interpolate` |
| `!Join [delim, [...]]` | `pulumi.interpolate` or `.apply()` |
| `!If [cond, true, false]` | Ternary operator |
| `!Equals [a, b]` | `===` comparison |
| `!Select [idx, list]` | Array indexing with `.apply()` |
| `!Split [delim, str]` | `.apply(v => v.split(...))` |
| `Fn::ImportValue` | Stack references or config |

##### Example: !Sub

```typescript
// CloudFormation: !Sub "arn:aws:s3:::${MyBucket}/*"
// Pulumi:
const bucketArn = pulumi.interpolate`arn:aws:s3:::${myBucket.bucket}/*`;
```

##### Example: !GetAtt

```typescript
// CloudFormation: !GetAtt MyFunction.Arn
// Pulumi:
const functionArn = myFunction.arn;
```

#### 2.4 CloudFormation Conditions

Convert CloudFormation conditions to TypeScript logic:

```typescript
// CloudFormation:
// "Conditions": {
//   "CreateProdResources": { "Fn::Equals": [{ "Ref": "Environment" }, "prod"] }
// }

// Pulumi:
const config = new pulumi.Config();
const environment = config.require("environment");
const createProdResources = environment === "prod";

if (createProdResources) {
  // Create production-only resources
}
```

#### 2.5 CloudFormation Parameters

Convert parameters to Pulumi config:

```typescript
// CloudFormation:
// "Parameters": {
//   "InstanceType": { "Type": "String", "Default": "t3.micro" }
// }

// Pulumi:
const config = new pulumi.Config();
const instanceType = config.get("instanceType") || "t3.micro";
```

#### 2.6 CloudFormation Mappings

Convert mappings to TypeScript objects:

```typescript
// CloudFormation:
// "Mappings": {
//   "RegionMap": {
//     "us-east-1": { "AMI": "ami-12345" },
//     "us-west-2": { "AMI": "ami-67890" }
//   }
// }

// Pulumi:
const regionMap: Record<string, { ami: string }> = {
  "us-east-1": { ami: "ami-12345" },
  "us-west-2": { ami: "ami-67890" },
};
const ami = regionMap[aws.config.region!].ami;
```

#### 2.7 Custom Resources

CloudFormation Custom Resources (`AWS::CloudFormation::CustomResource` or `Custom::*`) require special handling:

1. **Identify the purpose**: Read the Lambda function code to understand what it does
2. **Find native replacement**: Check if Pulumi has a native resource that provides the same functionality
3. **If no replacement**: Document in the migration report that manual implementation is needed

#### 2.8 TypeScript Output Handling

aws-native outputs often include undefined. Avoid `!` non-null assertions. Always safely unwrap with `.apply()`:

```typescript
// WRONG
functionName: lambdaFunction.functionName!,

// CORRECT
functionName: lambdaFunction.functionName.apply(name => name || ""),
```

### 3. RESOURCE IMPORT

After conversion, import existing resources to be managed by Pulumi.

#### 3.0 Pre-Import Validation (REQUIRED)

**Before proceeding with import, verify your code:**

1. **Check Provider Usage**: Scan your code to ensure all resources use `aws-native`
2. **Document Exceptions**: Any use of `aws` (classic) provider must be justified
3. **Verify Resource Names**: Confirm all resources use CloudFormation Logical IDs as names

#### 3.1 Automated Import with cdk-importer

Because you used CloudFormation Logical IDs as resource names, you can use the `cdk-importer` tool to automatically import resources.

Follow [cfn-importer.md](cfn-importer.md) for detailed import procedures.

#### 3.2 Manual Import for Failed Resources

For resources that fail automatic import:

1. Follow [cloudformation-id-lookup.md](cloudformation-id-lookup.md) to find the import ID format
2. Use `pulumi import`:

```bash
pulumi import <pulumi-resource-type> <logical-id> <import-id>
```

#### 3.3 Running Preview After Import

After import, run `pulumi preview`. There must be:
- NO updates
- NO replaces
- NO creates
- NO deletes

If there are changes, investigate and update the program until preview is clean.

## OUTPUT FORMAT (REQUIRED)

When performing a migration, always produce:

1. **Overview** (high-level description)
2. **Migration Plan Summary**
3. **Pulumi Code Outputs** (TypeScript; organized by file)
4. **Resource Mapping Table**:

| CloudFormation Logical ID | CFN Type | Pulumi Type | Provider |
|---------------------------|----------|-------------|----------|
| `MyAppBucketABC123` | `AWS::S3::Bucket` | `aws-native.s3.Bucket` | aws-native |
| `MyLambdaFunction456` | `AWS::Lambda::Function` | `aws-native.lambda.Function` | aws-native |

5. **Custom Resources Summary** (if any)
6. **Final Migration Report** (PR-ready)
7. **Next Steps** (import instructions)

## FOR DETAILED DOCUMENTATION

Fetch content from official Pulumi documentation:
- https://www.pulumi.com/docs/iac/adopting-pulumi/migrating-to-pulumi/from-aws/
