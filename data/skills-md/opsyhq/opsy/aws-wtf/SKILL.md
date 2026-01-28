---
name: aws-wtf
description: AWS charge explainer for Opsy. Use when users ask "what am I paying for", "explain my AWS bill", "where is my money going", "break down AWS charges", "what is this charge for", "why am I being charged", "cost breakdown", or want to understand any AWS charge.
---

# AWS WTF Skill for Opsy

Explains every charge on your AWS bill — what it is, why you're paying, and what resource caused it.

## ⚠️ Mandatory Output

**You MUST automatically generate and save a CSV file at the end of every analysis.**
Do not wait for the user to ask. The analysis is incomplete until the CSV exists.

## Step 1: Cost Explorer (Two Queries Required)

Run BOTH queries to detect credit coverage:

```bash
# Query 1: Normal (shows $0 if credits cover costs)
aws ce get-cost-and-usage \
  --time-period Start=$(date -v-30d +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics "UnblendedCost" "UsageQuantity" \
  --group-by Type=DIMENSION,Key=SERVICE

# Query 2: Exclude credits (shows ACTUAL usage cost)
aws ce get-cost-and-usage \
  --time-period Start=$(date -v-30d +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics "UnblendedCost" "UsageQuantity" \
  --group-by Type=DIMENSION,Key=SERVICE \
  --filter '{"Not": {"Dimensions": {"Key": "RECORD_TYPE", "Values": ["Credit", "Refund"]}}}'
```

**Interpretation:**
- Query 1 = $0, Query 2 = $X → Credits covering $X actual usage
- Query 1 = Query 2 = $0 → Real free tier
- Query 1 = Query 2 = $X → Normal billing

**If credits detected, warn user:** "Your bill shows $0 but actual usage is $X/month. When credits run out, you WILL be charged."

## Step 2: Identify ALL Regions

```bash
aws ce get-cost-and-usage \
  --time-period Start=$(date -v-30d +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics "UnblendedCost" \
  --group-by Type=DIMENSION,Key=REGION \
  --filter '{"Not": {"Dimensions": {"Key": "RECORD_TYPE", "Values": ["Credit", "Refund"]}}}'
```

**You MUST enumerate resources in EVERY region showing charges > $0.01.**

## Step 3: Enumerate ALL Resources

For each region with charges, query ALL applicable services using `--region $REGION`:

- `aws ec2 describe-instances`
- `aws ec2 describe-volumes`
- `aws ec2 describe-snapshots --owner-ids self`
- `aws ec2 describe-addresses`
- `aws ec2 describe-nat-gateways`
- `aws rds describe-db-instances`
- `aws elbv2 describe-load-balancers`
- `aws ecs list-clusters` → `describe-clusters` → `list-services` → `list-tasks`
- `aws eks list-clusters` → `describe-cluster`
- `aws lambda list-functions`
- `aws s3api list-buckets` (global) → `get-bucket-location` per bucket
- `aws ecr describe-repositories`
- `aws secretsmanager list-secrets`
- `aws logs describe-log-groups`
- `aws kms list-keys`
- `aws route53 list-hosted-zones` (global)

### ARN Construction

For resources without ARN in response, construct: `arn:aws:{service}:{region}:{account}:{resource-type}/{id}`

Examples:
- EC2: `arn:aws:ec2:us-east-1:123456789012:instance/i-abc123`
- EBS: `arn:aws:ec2:us-east-1:123456789012:volume/vol-abc123`
- S3: `arn:aws:s3:::bucket-name`

## ⚠️ CRITICAL: Every Charge Must Have Identification

**Every row in the CSV MUST have a resource identifier (ARN + resource_id) UNLESS it is truly untraceable.**

### What CAN Be Traced (MUST have ARN)

ANY charge from these services MUST be traced to a specific resource:

| Service | Has ARN | Example |
|---------|---------|---------|
| EC2 | ✅ Always | Instance, Volume, Snapshot, EIP, NAT Gateway |
| S3 | ✅ Always | Bucket |
| RDS | ✅ Always | Instance |
| ECS/EKS | ✅ Always | Cluster, Service, Task |
| Lambda | ✅ Always | Function |
| ALB/NLB | ✅ Always | Load Balancer |
| CloudWatch Logs | ✅ Always | Log Group |
| Secrets Manager | ✅ Always | Secret |
| KMS | ✅ Always | Key |
| ECR | ✅ Always | Repository |
| Route 53 | ✅ Always | Hosted Zone |

**If Cost Explorer shows charges for these but you can't find the resource → it was deleted mid-period. Put ARN as `DELETED - {service}` and note in description.**

### What CANNOT Be Traced (N/A allowed)

Only these charges are truly untraceable to a single resource:

| Charge Type | Why Untraceable |
|-------------|-----------------|
| Data Transfer Out | Aggregated from multiple sources |
| Data Transfer Inter-Region | No single source |
| Data Transfer Inter-AZ | No single source |
| Support Plan | Account-level |
| Tax | Account-level |
| CloudWatch Custom Metrics (aggregated) | No single dimension |

**For these only:** use `arn: N/A - Service-level charge` or `N/A - Account-level charge`

### Verification Rule

Before marking ANY charge as N/A, ask: "Is there a specific AWS resource that caused this?"
- If YES → find it, get its ARN
- If NO (only data transfer, support, tax) → N/A is acceptable

### Elastic IP Verification

Check `AssociationId` before calling an IP "unattached":
- `AssociationId` present → attached (even if `InstanceId` is empty)
- `NetworkInterfaceOwnerId = "amazon-..."` → service-managed (ALB, RDS, NAT)

### Public IPv4 Charges

AWS charges $0.005/hr ($3.60/mo) per public IPv4. Find all sources:
- EC2 public IPs, Elastic IPs, internet-facing ALBs, NAT Gateways

## CSV Output (Mandatory)

**Filename:** `aws-wtf-{account-id}-{date}.csv`

```csv
account_id,resource_name,charge_category,charge_explanation,monthly_cost_usd,status,resource_id,arn,region,resource_type,tags,description
```

### Column Definitions

| Column | Description |
|--------|-------------|
| `account_id` | AWS account ID |
| `resource_name` | Name tag (empty if untagged) |
| `charge_category` | `Compute`, `Storage`, `Database`, `Networking`, `Container`, `Serverless`, `Monitoring`, `DNS`, `Security`, `Data Transfer`, `Support`, `Tax` |
| `charge_explanation` | What you're paying for: `EC2 t3.small`, `EBS gp3 20GB`, `ALB hourly` |
| `monthly_cost_usd` | Actual cost (not $0 even if credit-covered) |
| `status` | `Billed`, `Free-Tier`, `Credit-Offset` |
| `resource_id` | AWS resource ID or `N/A` for non-resource charges |
| `arn` | Full ARN or `N/A - Service-level charge` |
| `region` | AWS region or `global` |
| `resource_type` | `EC2`, `EBS`, `RDS`, `S3`, `Lambda`, etc. |
| `tags` | `key=value,key=value` |
| `description` | Cost breakdown: `720 hrs × $0.10/hr`, details |

### One Row Per Charge Type

A resource can have multiple rows:
- EC2: Compute hours + Public IPv4
- RDS: Instance hours + Storage
- ALB: Hourly + LCU + Public IPv4
- ECS Fargate: vCPU + Memory

### Example

```csv
account_id,resource_name,charge_category,charge_explanation,monthly_cost_usd,status,resource_id,arn,region,resource_type,tags,description
550435500798,api-server,Compute,EC2 t3.small,15.18,Credit-Offset,i-abc123,arn:aws:ec2:us-east-1:550435500798:instance/i-abc123,us-east-1,EC2,"Env=prod","720 hrs × $0.0211/hr"
550435500798,api-server,Networking,Public IPv4,3.60,Credit-Offset,i-abc123,arn:aws:ec2:us-east-1:550435500798:instance/i-abc123,us-east-1,EC2-IPv4,,"720 hrs × $0.005/hr"
550435500798,/aws/lambda/func,Monitoring,CloudWatch Logs,0.45,Credit-Offset,/aws/lambda/func,arn:aws:logs:us-east-1:550435500798:log-group:/aws/lambda/func,us-east-1,CloudWatch-Logs,,"15GB × $0.03/GB"
550435500798,,Data Transfer,Egress to Internet,12.00,Billed,N/A,N/A - Service-level charge,us-east-1,DataTransfer,,"133GB × $0.09/GB"
```

## Summary Report

```markdown
## AWS Bill Breakdown
**Account:** {id} | **Period:** {start} to {end}

### Cost Summary
| Metric | Amount |
|--------|--------|
| Actual Usage | $XXX |
| Credits Applied | -$XXX |
| **You Pay** | **$X.XX** |

### By Category
| Category | Amount | % |
|----------|--------|---|
| Compute | $XX | X% |
| Storage | $XX | X% |
...

### Top Charges
| Resource | Type | Cost | Description |
|----------|------|------|-------------|
| {name} | {type} | $XX | {explanation} |
```

## Completion Checklist

- [ ] Cost Explorer: both queries (with/without credits)
- [ ] All regions identified and enumerated
- [ ] All resources listed with ARNs
- [ ] CSV file saved
- [ ] Summary shown to user

**Analysis is INCOMPLETE until CSV file exists.**

