---
name: aws-finops
description: AWS FinOps cost optimization analysis for Opsy. Use when users ask to analyze AWS costs, find waste, optimize spending, identify idle/underutilized resources, review Reserved Instance or Savings Plans coverage, or generate cost optimization reports. Triggers on "reduce AWS costs", "find unused resources", "cost analysis", "optimize spend", "idle resources", "rightsizing", "savings opportunities", "why is my AWS bill high".
---

# AWS FinOps Skill for Opsy

## Step 1: Cost Explorer First

Start with Cost Explorer — one call covers all regions and services:

1. **Spend by service** — identifies top cost drivers
2. **Spend by region** — shows where resources live  
3. **Daily trend** — spots anomalies

Focus on services representing >5% of spend.

### If Credits Mask Costs ($0 spend)

Check if Resource Explorer is enabled:
```
aws resource-explorer-2 list-indexes --region us-east-1
```

If enabled, use it — one call gets ALL resources:
```
aws resource-explorer-2 search --query-string "*" --region us-east-1
```

If NOT enabled, use resourcegroupstaggingapi to find all tagged resources:
```
aws resourcegroupstaggingapi get-resources --region us-east-1
```

Then query each active region for core services: EC2, RDS, EBS, Lambda, S3, ECS, EKS, NAT Gateways, Load Balancers.

## Step 2: Deep Dive Each Resource

For every resource found, gather full details:

- **EC2**: Instance type, state, launch time, CloudWatch CPU/memory
- **RDS**: Instance class, connections (14d), storage, Multi-AZ, engine
- **EBS**: Attachment status, volume type, size, snapshots
- **S3**: Lifecycle policies, storage class, versioning
- **Lambda**: Invocations (30d), memory, runtime, provisioned concurrency
- **ECS/EKS**: Task definitions, service counts, cluster utilization
- **ECR**: Repositories, image count, lifecycle policies
- **Load Balancers**: Request count (14d), target groups
- **NAT Gateway**: Data processed
- **Elastic IPs**: Association status
- **CloudWatch Logs**: Retention settings
- **Secrets Manager**: Secret count

Check EVERY resource for optimization opportunities. Don't skip services.

## Step 3: Check Commitment Coverage

- Savings Plans utilization
- Reserved Instance coverage gaps
- Expiring commitments (next 30 days)

## Safety Guardrails

Report findings with evidence, suggest investigation — not direct actions:
- "Instance i-xxx averaged 3% CPU over 30 days — rightsizing candidate"
- "Volume vol-xxx unattached since [date] — verify before removing"
- "RDS db-xxx had 0 connections for 14 days — confirm if still needed"

**Thresholds:**
- **Idle**: ~0% utilization for 14+ days
- **Underutilized**: <10% average for 14+ days
- **Rightsizing candidate**: <30% average

## Smart Recommendation Rules

Only flag when action is possible:

| Situation | Action |
|-----------|--------|
| Minimum size + in use (db.t3.micro with connections) | Skip — already right-sized |
| Minimum size + idle (db.t3.micro, 0 connections) | Flag as idle |
| Larger size + low utilization | Flag for rightsizing with specific target |
| Tagged `FinOps:Skip=true` | Skip |
| Dev/staging with `Environment=dev` | Skip low utilization (expected) |

Before flagging, verify:
1. Is this the minimum size?
2. Is it actually in use? (connections/invocations/requests)
3. Is there a smaller option?

## Service Checklists

**EC2**: Utilization, stopped instances (EBS cost), previous-gen types, On-Demand 24/7 → SP/RI

**Lambda**: Zero invocations (30d), memory vs duration tradeoff, provisioned concurrency

**ECS/EKS**: Fargate vs EC2, resource requests vs usage, Spot for fault-tolerant

**ECR**: Lifecycle policies, image count, total size — old images accumulate

**RDS**: Connection count, Multi-AZ in dev, instance class utilization, storage, previous-gen

**DynamoDB**: Provisioned vs On-Demand fit, auto-scaling, TTL

**ElastiCache/OpenSearch**: Node utilization, reserved coverage

**S3**: Lifecycle policies, storage class, Intelligent-Tiering, incomplete multipart uploads

**EBS**: Unattached volumes, gp2→gp3, snapshot retention, IOPS necessity

**Networking**: Cross-AZ transfer, NAT Gateway → VPC endpoints, CloudFront caching

**Load Balancers**: Zero requests = orphaned, Classic→ALB/NLB

**Elastic IPs**: Unassociated = $3.60/month each

**CloudWatch**: Log retention (default infinite), high-res metrics necessity

**Secrets Manager**: $0.40/month vs free Parameter Store

**API Gateway**: HTTP API 70% cheaper than REST

## Output Requirements

### CSV (Required)

```
account_id,resource_name,status,recommendation_type,potential_savings_monthly,resource_id,region,resource_type,tags,description
123456789012,web-server-prod,Underutilized,Rightsizing to t3.small,45.00,i-0abc123def456,us-east-1,EC2 Instance,"Environment=prod,Team=platform","Avg CPU 8% over 30 days. Current: t3.large"
123456789012,,Unattached,Verify before removing,12.50,vol-0xyz789,us-east-1,EBS Volume,,"100GB gp2 volume unattached since 2024-12-01"
123456789012,raspberry,No-Lifecycle,Add ECR lifecycle policy,2.00,raspberry,us-east-1,ECR Repository,,"47 images totaling 12GB. No lifecycle policy configured"
```

| Column | Description |
|--------|-------------|
| `account_id` | AWS account ID |
| `resource_name` | Name tag value (empty if untagged) |
| `status` | `Idle`, `Underutilized`, `Oversized`, `Unattached`, `Previous-Gen`, `No-Lifecycle`, `Uncovered` |
| `recommendation_type` | Specific action: `Rightsizing to X`, `Verify before removing`, `Add ECR lifecycle policy`, `Switch to gp3`, `Consider SP/RI` |
| `potential_savings_monthly` | USD/month (conservative estimate) |
| `resource_id` | AWS resource ID |
| `region` | AWS region |
| `resource_type` | `EC2 Instance`, `EBS Volume`, `RDS Instance`, `ECR Repository`, `S3 Bucket`, etc. |
| `tags` | Resource tags as key=value pairs (from AWS tags, not Name) |
| `description` | Details: current state, metrics, why flagged, specific numbers |

### Summary (Markdown)

```markdown
## AWS FinOps Summary
**Account:** [id] | **Date:** [date]

### Spend Overview
- Monthly spend: $X,XXX
- Top spenders: [service1] (X%), [service2] (X%), [service3] (X%)

### Findings
- Total potential savings: $X,XXX/month
- Resources flagged: X

### Top 5 Opportunities
1. [resource] - [recommendation] - $X/month

### Next Steps
- [investigation recommendations]
```

Save as `finops-report-[account-id]-[date].csv`