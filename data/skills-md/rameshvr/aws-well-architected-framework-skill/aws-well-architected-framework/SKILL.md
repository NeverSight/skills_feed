---
name: aws-well-architected-framework
description: Use when reviewing AWS architecture, designing cloud systems, addressing operational issues, security concerns, reliability problems, performance bottlenecks, cost overruns, or sustainability goals
---

# AWS Well-Architected Framework

Expert guidance for designing, reviewing, and improving AWS architectures using the six pillars of the Well-Architected Framework.

## When to Use

Use this skill when:

- Reviewing existing AWS architecture for best practices
- Designing new cloud systems or applications
- Troubleshooting operational issues, security vulnerabilities, or reliability problems
- Optimizing costs or improving performance
- Preparing for architecture reviews or audits
- Migrating workloads to AWS
- Addressing compliance or sustainability requirements
- User asks "is my architecture good?" or "how can I improve my AWS setup?"

## Core Principle

**Systematic architecture evaluation across 6 pillars ensures balanced, well-designed systems that meet business objectives.**

The AWS Well-Architected Framework provides a consistent approach for evaluating cloud architectures and implementing scalable designs.

## The Six Pillars

| Pillar | Focus | Key Question |
|--------|-------|--------------|
| **Operational Excellence** | Run and monitor systems | How do we operate effectively? |
| **Security** | Protect information and systems | How do we protect data and resources? |
| **Reliability** | Recover from failures | How do we ensure workload availability? |
| **Performance Efficiency** | Use resources effectively | How do we meet performance requirements? |
| **Cost Optimization** | Avoid unnecessary costs | How do we achieve cost-effective outcomes? |
| **Sustainability** | Minimize environmental impact | How do we reduce carbon footprint? |

## Architecture Review Workflow

**CRITICAL: You MUST review ALL 6 pillars systematically. Never skip a pillar because it "seems not applicable" - every workload has considerations across all pillars.**

```dot
digraph review_flow {
    "Architecture review needed" [shape=doublecircle];
    "Identify workload scope" [shape=box];
    "Review each pillar systematically" [shape=box];
    "Document findings per pillar" [shape=box];
    "Prioritize improvements" [shape=box];
    "Create action plan" [shape=box];
    "All pillars reviewed?" [shape=diamond];
    "Complete" [shape=doublecircle];

    "Architecture review needed" -> "Identify workload scope";
    "Identify workload scope" -> "Review each pillar systematically";
    "Review each pillar systematically" -> "Document findings per pillar";
    "Document findings per pillar" -> "All pillars reviewed?";
    "All pillars reviewed?" -> "Review each pillar systematically" [label="no"];
    "All pillars reviewed?" -> "Prioritize improvements" [label="yes"];
    "Prioritize improvements" -> "Create action plan";
    "Create action plan" -> "Complete";
}
```

**Red Flags - You're Skipping the Framework:**
- "This pillar doesn't apply to this workload" - WRONG, every pillar applies
- Jumping straight to recommendations without documenting current state
- Only reviewing 3-4 pillars instead of all 6
- Providing generic advice instead of workload-specific assessment

## Pillar 1: Operational Excellence

**Goal:** Support development and run workloads effectively, gain insight into operations, and continuously improve processes.

### Design Principles

- Perform operations as code (IaC)
- Make frequent, small, reversible changes
- Refine operations procedures frequently
- Anticipate failure
- Learn from operational events and failures

### Key Areas

**Organization:**
- How do teams share architecture knowledge?
- Are there clear ownership and accountability models?

**Prepare:**
- How do you design workloads for observability?
- Infrastructure as code implementation?
- Deployment practices (CI/CD)?

**Operate:**
- What's the runbook for common operations?
- How do you understand workload health?
- How do you respond to events?

**Evolve:**
- How do you learn from operational events?
- Process for continuous improvement?

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Manual deployments | Implement CI/CD with CloudFormation/CDK/Terraform |
| No visibility into system health | Add CloudWatch dashboards, metrics, alarms |
| Operational procedures outdated | Regular runbook reviews, post-incident learning |
| Slow incident response | Create automated remediation with Lambda/Systems Manager |

### Quick Implementation Checklist

- [ ] Infrastructure defined as code (CloudFormation/CDK/Terraform)
- [ ] CI/CD pipeline implemented
- [ ] CloudWatch dashboards for key metrics
- [ ] Alarms for critical thresholds
- [ ] Runbooks documented and accessible
- [ ] Regular game days to test procedures
- [ ] Post-incident review process

## Pillar 2: Security

**Goal:** Protect data, systems, and assets through cloud security practices.

### Design Principles

- Implement strong identity foundation
- Enable traceability
- Apply security at all layers
- Automate security best practices
- Protect data in transit and at rest
- Keep people away from data
- Prepare for security events

### Key Areas

**Security Foundations:**
- How do you manage credentials and authentication?
- IAM roles and policies following least privilege?

**Identity and Access Management:**
- How do you manage identities for people and machines?
- MFA enabled for all human access?

**Detection:**
- How do you detect and investigate security events?
- CloudTrail, GuardDuty, Security Hub configured?

**Infrastructure Protection:**
- How do you protect networks and compute?
- VPC configuration, security groups, NACLs?

**Data Protection:**
- How do you classify and protect data?
- Encryption at rest and in transit?

**Incident Response:**
- How do you respond to security incidents?
- Incident response plan tested?

### Critical Security Patterns

**Never Do:**
```typescript
// ❌ DANGEROUS: Hardcoded credentials
const AWS = require('aws-sdk');
const s3 = new AWS.S3({
  accessKeyId: 'AKIAIOSFODNN7EXAMPLE',
  secretAccessKey: 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
});
```

**Always Do:**
```typescript
// ✅ CORRECT: Use IAM roles
const AWS = require('aws-sdk');
const s3 = new AWS.S3(); // Credentials from IAM role

// Lambda function with IAM role
const lambda = new lambda.Function(this, 'MyFunction', {
  // IAM role with least privilege
  role: myRole,
  // ...
});
```

### Security Checklist

- [ ] No hardcoded credentials anywhere (check git history!)
- [ ] IAM roles follow least privilege principle
- [ ] MFA enabled for root and privileged accounts
- [ ] CloudTrail enabled in all regions
- [ ] VPC with proper public/private subnet architecture
- [ ] Security groups with minimal inbound rules
- [ ] Encryption at rest for all data stores
- [ ] HTTPS/TLS for all data in transit
- [ ] Secrets Manager or Parameter Store for secrets
- [ ] Regular security patching process
- [ ] AWS Config for compliance monitoring
- [ ] GuardDuty for threat detection

## Pillar 3: Reliability

**Goal:** Ensure workload performs its intended function correctly and consistently.

### Design Principles

- Automatically recover from failure
- Test recovery procedures
- Scale horizontally
- Stop guessing capacity
- Manage change through automation

### Key Areas

**Foundations:**
- How do you manage service quotas and constraints?
- Network topology designed for HA?

**Workload Architecture:**
- How do you design workload service architecture?
- Microservices vs monolith considerations?

**Change Management:**
- How do you monitor workload resources?
- How are changes deployed safely?

**Failure Management:**
- How do you back up data?
- How do you design for resilience?
- DR plan and RTO/RPO defined?

### High Availability Patterns

**Multi-AZ Deployment:**
```
Region
├── AZ-1: Application + Database
├── AZ-2: Application + Database (standby)
└── AZ-3: Application + Database (standby)
```

**Multi-Region Deployment:**
```
Primary Region          Secondary Region
├── Active workload    ├── Standby/Active
├── Database (primary) ├── Database (replica)
└── Route 53 health check monitoring
```

### Backup Strategy

| Data Type | Solution | RPO | RTO |
|-----------|----------|-----|-----|
| **RDS** | Automated backups + snapshots | < 5 min | < 30 min |
| **DynamoDB** | Point-in-time recovery | Seconds | Minutes |
| **S3** | Versioning + cross-region replication | Real-time | Immediate |
| **EBS** | Snapshots via AWS Backup | Hours | Hours |

### Reliability Checklist

- [ ] Multi-AZ deployment for critical components
- [ ] Health checks configured (ELB, Route 53)
- [ ] Auto Scaling groups with proper sizing
- [ ] RDS automated backups enabled
- [ ] DynamoDB point-in-time recovery enabled
- [ ] S3 versioning for critical buckets
- [ ] Disaster recovery plan documented and tested
- [ ] Chaos engineering tests (failure injection)
- [ ] Graceful degradation strategies
- [ ] Circuit breaker patterns implemented

## Pillar 4: Performance Efficiency

**Goal:** Use computing resources efficiently to meet requirements and maintain efficiency as demand changes.

### Design Principles

- Democratize advanced technologies
- Go global in minutes
- Use serverless architectures
- Experiment more often
- Consider mechanical sympathy

### Key Areas

**Selection:**
- How do you select appropriate resource types and sizes?
- Compute: EC2, Lambda, Fargate, ECS, EKS?
- Database: RDS, DynamoDB, Aurora, ElastiCache?
- Storage: S3, EFS, EBS, Glacier?

**Review:**
- How do you evolve workload to use new resources?
- Regular review of AWS new features?

**Monitoring:**
- How do you monitor resources?
- CloudWatch, X-Ray for distributed tracing?

**Trade-offs:**
- How do you use trade-offs to improve performance?
- Caching, consistency models, compression?

### Performance Patterns

**Caching Strategy:**
```
Client → CloudFront (edge cache)
  → API Gateway
    → Lambda
      → ElastiCache (data cache)
        → DynamoDB/RDS
```

**Database Selection:**

| Use Case | Recommended Service |
|----------|-------------------|
| Relational, complex queries | RDS (PostgreSQL/MySQL) |
| High throughput, simple queries | DynamoDB |
| Graph relationships | Neptune |
| Search and analytics | OpenSearch |
| Time-series data | Timestream |
| In-memory cache | ElastiCache (Redis/Memcached) |

### Performance Checklist

- [ ] Right-sized compute instances (not over-provisioned)
- [ ] Content delivery through CloudFront
- [ ] Database read replicas for read-heavy workloads
- [ ] Caching layer (ElastiCache, DAX, CloudFront)
- [ ] Asynchronous processing with SQS/SNS/EventBridge
- [ ] Auto Scaling configured appropriately
- [ ] Database indexes optimized
- [ ] Monitoring with CloudWatch and X-Ray
- [ ] Regular performance testing under load

## Pillar 5: Cost Optimization

**Goal:** Run systems to deliver business value at lowest price point.

### Design Principles

- Implement cloud financial management
- Adopt consumption model
- Measure overall efficiency
- Stop spending on undifferentiated heavy lifting
- Analyze and attribute expenditure

### Key Areas

**Practice Cloud Financial Management:**
- Cost allocation tags implemented?
- Budgets and alerts configured?

**Expenditure and Usage Awareness:**
- How do you govern usage?
- Cost Explorer and AWS Budgets configured?

**Cost-Effective Resources:**
- How do you evaluate cost when selecting services?
- Reserved Instances or Savings Plans for predictable workloads?

**Manage Demand:**
- How do you manage demand and supply resources?
- Throttling, caching to reduce demand?

**Optimize Over Time:**
- How do you evaluate new services?
- Regular review of cost optimization opportunities?

### Cost Optimization Strategies

| Strategy | Implementation | Potential Savings |
|----------|---------------|-------------------|
| **Right-sizing** | Use Compute Optimizer recommendations | 20-40% |
| **Reserved Instances** | 1-year or 3-year commitments | 30-75% |
| **Savings Plans** | Flexible compute commitments | 30-70% |
| **Spot Instances** | Fault-tolerant workloads | 50-90% |
| **S3 Intelligent-Tiering** | Automatic storage class optimization | 40-60% |
| **Auto Scaling** | Scale resources with demand | 30-50% |
| **Lambda instead of EC2** | For appropriate workloads | Varies |

### Cost Monitoring

```typescript
// CDK Example: Set up budget alerts
import * as budgets from 'aws-cdk-lib/aws-budgets';

new budgets.CfnBudget(this, 'MonthlyBudget', {
  budget: {
    budgetType: 'COST',
    timeUnit: 'MONTHLY',
    budgetLimit: {
      amount: 1000,
      unit: 'USD',
    },
  },
  notificationsWithSubscribers: [{
    notification: {
      notificationType: 'ACTUAL',
      comparisonOperator: 'GREATER_THAN',
      threshold: 80, // Alert at 80%
    },
    subscribers: [{
      subscriptionType: 'EMAIL',
      address: 'team@example.com',
    }],
  }],
});
```

### Cost Optimization Checklist

- [ ] Cost allocation tags applied consistently
- [ ] AWS Budgets configured with alerts
- [ ] Cost Explorer reviewed monthly
- [ ] Reserved Instances or Savings Plans for stable workloads
- [ ] Spot Instances for fault-tolerant workloads
- [ ] Unused resources identified and terminated
- [ ] S3 lifecycle policies for data management
- [ ] Right-sized instances (not over-provisioned)
- [ ] Lambda memory optimization
- [ ] DynamoDB on-demand vs provisioned analysis
- [ ] Data transfer costs analyzed and optimized

## Pillar 6: Sustainability

**Goal:** Minimize environmental impact of running cloud workloads.

### Design Principles

- Understand your impact
- Establish sustainability goals
- Maximize utilization
- Anticipate and adopt new, more efficient offerings
- Use managed services
- Reduce downstream impact

### Key Areas

**Region Selection:**
- Choose regions with renewable energy
- AWS regions with lower carbon intensity

**User Behavior Patterns:**
- Scale resources with demand
- Remove unused resources

**Software and Architecture:**
- Optimize code for efficiency
- Use appropriate services (serverless over provisioned)

**Data Patterns:**
- Minimize data movement
- Use data compression
- Implement lifecycle policies

**Hardware Patterns:**
- Use minimum necessary hardware
- Use instance types with best performance per watt

**Development Process:**
- Test sustainability improvements
- Measure and report carbon footprint

### Sustainability Checklist

- [ ] Workloads in regions with renewable energy
- [ ] Auto Scaling to match demand (no idle resources)
- [ ] Unused resources regularly cleaned up
- [ ] Graviton processors considered for better efficiency
- [ ] Managed services used where appropriate
- [ ] Data lifecycle policies to reduce storage
- [ ] Efficient code (async processing, optimized queries)
- [ ] Monitoring resource utilization
- [ ] Carbon footprint tracked (AWS Customer Carbon Footprint Tool)

## Review Process

### 1. Scoping Phase

**Questions to ask:**
- What is the workload scope? (entire system vs specific component)
- What are the business objectives?
- What are the compliance requirements?
- What are the current pain points?

### 2. Review Each Pillar

For each pillar, use this template:

**Current State:**
- Document what exists today

**Gaps:**
- What's missing or needs improvement?

**Risks:**
- What are the high/medium/low priority risks?

**Recommendations:**
- Specific, actionable improvements

### 3. Prioritization Matrix

| Priority | Criteria |
|----------|----------|
| **High** | Security vulnerabilities, critical availability risks, major cost waste |
| **Medium** | Performance issues, moderate cost optimization, operational improvements |
| **Low** | Nice-to-haves, future considerations, minor optimizations |

### 4. Action Plan Template

```markdown
## Pillar: [Name]

### Issue: [Description]
- **Risk Level:** High/Medium/Low
- **Impact:** [Business impact]
- **Effort:** Low/Medium/High

### Recommendation:
[Specific actions]

### Implementation Steps:
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Success Criteria:
- [Measurable outcome 1]
- [Measurable outcome 2]

### Resources:
- [AWS documentation links]
- [Blog posts or examples]
```

## Common Anti-Patterns

| Anti-Pattern | Issue | Better Approach |
|--------------|-------|-----------------|
| **Single AZ deployment** | No fault tolerance | Multi-AZ architecture |
| **No IaC** | Manual config, drift | CloudFormation/CDK/Terraform |
| **Hardcoded secrets** | Security vulnerability | Secrets Manager/Parameter Store |
| **No monitoring** | Blind operation | CloudWatch dashboards + alarms |
| **No backups** | Data loss risk | Automated backup strategy |
| **Over-provisioning** | Cost waste | Right-sizing + Auto Scaling |
| **No cost tracking** | Budget overruns | Tags + Budgets + Cost Explorer |
| **Monolithic architecture** | Hard to scale | Microservices or serverless |

## Real-World Example

**Scenario:** Serverless API with authentication

**Architecture Review:**

**Operational Excellence:**
- ✅ Lambda functions deployed via CDK
- ✅ CloudWatch logs enabled
- ❌ Missing: Distributed tracing (X-Ray), dashboards

**Security:**
- ❌ CRITICAL: Hardcoded API keys in Lambda environment variables
- ✅ API Gateway with IAM authorization
- ❌ Missing: Secrets Manager, encryption at rest

**Reliability:**
- ✅ Multi-AZ DynamoDB table
- ❌ Single region deployment
- ❌ Missing: Backup strategy, DR plan

**Performance:**
- ✅ CloudFront for static assets
- ❌ No caching for API responses
- ❌ Lambda cold starts not optimized

**Cost:**
- ❌ DynamoDB provisioned capacity, but traffic is spiky
- ✅ Lambda usage-based pricing
- ❌ Missing: Budget alerts, cost allocation tags

**Sustainability:**
- ✅ Serverless architecture (good utilization)
- ❌ Unused dev/test resources running 24/7

**Priority Actions:**
1. **HIGH**: Move API keys to Secrets Manager (Security)
2. **HIGH**: Implement DynamoDB backups (Reliability)
3. **MEDIUM**: Add X-Ray tracing (Operational Excellence)
4. **MEDIUM**: Switch DynamoDB to on-demand (Cost)
5. **LOW**: Add API Gateway caching (Performance)

## Resources

- [AWS Well-Architected Framework Whitepaper](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [AWS Well-Architected Tool](https://console.aws.amazon.com/wellarchitected) (Interactive reviews)
- [Well-Architected Labs](https://wellarchitectedlabs.com/)
- [AWS Architecture Center](https://aws.amazon.com/architecture/)
- [Sustainability Pillar Whitepaper](https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/sustainability-pillar.html)

## Common Mistakes When Using This Framework

| Mistake | Why It's Wrong | Correct Approach |
|---------|---------------|------------------|
| "Sustainability doesn't apply to this workload" | Every workload consumes resources and energy | Review all 6 pillars, even if findings are minimal |
| Skipping current state documentation | Can't measure improvement without baseline | Always document "Current State" before recommendations |
| Generic recommendations | Not actionable or specific to this workload | Provide specific AWS services, code examples, priorities |
| No prioritization | Everything seems equally important | Use HIGH/MEDIUM/LOW risk levels, create phased plan |
| Forgetting about trade-offs | Optimizing one pillar at expense of others | Explicitly call out trade-offs (e.g., multi-region cost vs reliability) |

## Using This Skill

When conducting architecture reviews:

1. **Start with context** - understand business objectives and constraints
2. **Review systematically** - go through all 6 pillars, don't skip ANY
3. **Document findings** - use consistent format per pillar (Current State → Gaps → Recommendations)
4. **Prioritize ruthlessly** - security and availability issues first
5. **Be specific** - actionable recommendations with examples and AWS service names
6. **Provide resources** - link to AWS docs and examples
7. **Create action plan** - clear next steps with success criteria and effort estimates
8. **Call out trade-offs** - be explicit about costs and benefits of each recommendation

**Remember:** Architecture is about trade-offs. A perfect architecture doesn't exist - aim for a well-balanced one that meets business needs.

**No exceptions to reviewing all 6 pillars** - even if a pillar seems "not applicable", document why and what the current state is.
