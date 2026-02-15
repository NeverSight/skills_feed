---
name: aws-cost-explorer
description: This skill should be used when users need to query AWS cost and usage details for a specific date. It supports querying costs at service level (e.g., EC2, S3, RDS) and drilling down to usage type level (e.g., instance types, storage classes, data transfer). Triggers on requests mentioning AWS costs, billing, spending, cost breakdown, or fee analysis.
---

# AWS Cost Explorer

Query AWS costs and usage details with flexible granularity - from service-level overview to detailed usage type breakdown.

## Capabilities

- Query daily AWS costs by service (e.g., EC2, S3, OpenSearch, DocumentDB)
- Drill down to usage type details for specific services (e.g., instance types, storage, data transfer)
- Filter results by minimum cost threshold
- Support both relative dates (days ago) and absolute dates (YYYY-MM-DD)
- Output in human-readable table or JSON format

## Usage

### Quick Commands

To query costs, use the bundled script at `scripts/cost_query.py`:

```bash
# Query costs from 2 days ago (default) by service
python3 <skill-path>/scripts/cost_query.py

# Query yesterday's costs, show items > $5
python3 <skill-path>/scripts/cost_query.py --days-ago 1 --min-cost 5

# Query specific date
python3 <skill-path>/scripts/cost_query.py --date 2026-01-15

# Query specific service's usage breakdown
python3 <skill-path>/scripts/cost_query.py --service "Amazon OpenSearch Service" --min-cost 1

# Query all services with usage type details
python3 <skill-path>/scripts/cost_query.py --detailed --min-cost 5

# Output as JSON
python3 <skill-path>/scripts/cost_query.py --json --min-cost 5
```

### Script Options

| Option | Short | Description |
|--------|-------|-------------|
| `--days-ago` | `-d` | Query N days ago (default: 2, i.e., day before yesterday) |
| `--date` | | Query specific date (YYYY-MM-DD format) |
| `--min-cost` | `-m` | Minimum cost threshold to display (default: 0) |
| `--service` | `-s` | Query usage type breakdown for a specific service |
| `--detailed` | | Show all services with usage type breakdown |
| `--json` | `-j` | Output in JSON format |

## Common Service Names

When using `--service`, use the exact AWS service names:

| Common Name | AWS Service Name |
|-------------|------------------|
| OpenSearch | `Amazon OpenSearch Service` |
| DocumentDB/MongoDB | `Amazon DocumentDB (with MongoDB compatibility)` |
| EC2 Compute | `Amazon Elastic Compute Cloud - Compute` |
| EC2 Other (EBS, NAT) | `EC2 - Other` |
| EFS | `Amazon Elastic File System` |
| S3 | `Amazon Simple Storage Service` |
| RDS | `Amazon Relational Database Service` |
| EKS | `Amazon Elastic Container Service for Kubernetes` |
| VPC | `Amazon Virtual Private Cloud` |
| Bedrock | `Amazon Bedrock` |
| Lambda | `AWS Lambda` |
| CloudWatch | `AmazonCloudWatch` |

## Understanding Usage Types

Common usage type patterns:

| Pattern | Meaning |
|---------|---------|
| `BoxUsage:*` | EC2 instance hours (e.g., `BoxUsage:m7i.large`) |
| `ESInstance:*` | OpenSearch instance hours |
| `EBS:VolumeUsage.*` | EBS storage (e.g., `EBS:VolumeUsage.gp3`) |
| `TimedStorage-ByteHrs` | S3/EFS storage capacity |
| `DataTransfer-*` | Data transfer costs |
| `NatGateway-*` | NAT Gateway costs |
| `VpcEndpoint-*` | VPC Endpoint costs |
| `*-input-tokens` / `*-output-tokens` | Bedrock token usage |
| `Elastic*Usage` | DocumentDB Elastic costs |

## Prerequisites

- AWS CLI configured with appropriate credentials
- IAM permissions for `ce:GetCostAndUsage`

## Example Workflow

1. First, get service-level overview:
   ```bash
   python3 <skill-path>/scripts/cost_query.py --min-cost 5
   ```

2. Identify high-cost services, then drill down:
   ```bash
   python3 <skill-path>/scripts/cost_query.py --service "Amazon OpenSearch Service" --min-cost 1
   ```

3. For comprehensive analysis, use detailed mode:
   ```bash
   python3 <skill-path>/scripts/cost_query.py --detailed --min-cost 5
   ```
