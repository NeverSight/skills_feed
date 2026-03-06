---
name: cloud
description: Design AWS/Azure/GCP infrastructure, implement IaC, and optimize costs. Use for cloud architecture, cost optimization, or migration.
---

# Cloud Architecture

Design and manage cloud infrastructure.

## When to Use

- Cloud architecture decisions
- Cost optimization
- Multi-region deployments
- Cloud migrations
- Infrastructure automation

## AWS Patterns

### Compute

```yaml
# ECS Service
Resources:
  Service:
    Type: AWS::ECS::Service
    Properties:
      Cluster: !Ref Cluster
      DesiredCount: 2
      LaunchType: FARGATE
      NetworkConfiguration:
        AwsvpcConfiguration:
          Subnets: !Ref PrivateSubnets
          SecurityGroups: [!Ref SecurityGroup]
```

### Serverless

```yaml
# Lambda with API Gateway
functions:
  api:
    handler: src/handler.main
    events:
      - http:
          path: /users
          method: get
    environment:
      TABLE_NAME: !Ref UsersTable
```

### Database

```hcl
# RDS with read replica
resource "aws_db_instance" "primary" {
  identifier     = "app-primary"
  engine         = "postgres"
  engine_version = "15"
  instance_class = "db.r6g.large"
  multi_az       = true
}

resource "aws_db_instance" "replica" {
  identifier          = "app-replica"
  replicate_source_db = aws_db_instance.primary.identifier
  instance_class      = "db.r6g.large"
}
```

## Cost Optimization

### Compute

- Use Spot/Preemptible for fault-tolerant workloads (70% savings)
- Right-size instances based on actual usage
- Reserved instances for steady-state workloads (40% savings)
- Auto-scaling based on demand

### Storage

- S3 lifecycle policies for infrequent access
- EBS volume type selection (gp3 vs io2)
- Delete unused snapshots and volumes

### Network

- Use VPC endpoints to avoid NAT costs
- CloudFront for static content
- Compress and cache responses

## Multi-Region

```
┌─────────────────┐     ┌─────────────────┐
│   us-east-1     │     │   eu-west-1     │
│ ┌─────────────┐ │     │ ┌─────────────┐ │
│ │ Application │ │     │ │ Application │ │
│ └──────┬──────┘ │     │ └──────┬──────┘ │
│        │        │     │        │        │
│ ┌──────┴──────┐ │     │ ┌──────┴──────┐ │
│ │  Database   │◄├─────┼►│   Replica   │ │
│ └─────────────┘ │     │ └─────────────┘ │
└─────────────────┘     └─────────────────┘
         │                       │
         └───────────┬───────────┘
                     │
              ┌──────┴──────┐
              │ Route 53    │
              │ (failover)  │
              └─────────────┘
```

## Security Baseline

- [ ] VPC with private subnets
- [ ] Security groups (least privilege)
- [ ] IAM roles (not keys)
- [ ] Encryption at rest and transit
- [ ] CloudTrail logging
- [ ] GuardDuty enabled

## Examples

**Input:** "Design HA architecture"
**Action:** Multi-AZ setup, load balancing, database replication, failover

**Input:** "Reduce cloud costs"
**Action:** Analyze usage, identify waste, recommend reserved/spot, optimize storage
