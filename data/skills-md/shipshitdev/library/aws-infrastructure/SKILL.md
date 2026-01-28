---
name: aws-infrastructure
description: Expert in AWS infrastructure setup including EC2, VPC, security groups, Application Load Balancers, Route53 DNS, and SSL/TLS certificates. Use this skill for AWS infrastructure configuration and deployment.
---

# AWS Infrastructure Expert

## Overview

This skill enables AI assistants to help set up and configure AWS infrastructure for micro startups, including EC2 instances, VPCs, security groups, load balancers, DNS, and SSL certificates.

## When to Use This Skill

This skill activates when users need:

- EC2 instance setup and configuration
- VPC and networking setup
- Security group configuration
- Application Load Balancer setup
- Route53 DNS configuration
- SSL/TLS certificate management (ACM)
- Auto-scaling groups
- CloudWatch monitoring

## EC2 Setup

### Instance Types

- **Development:** t3.medium (2 vCPU, 4GB RAM)
- **Production (small):** t3.large (2 vCPU, 8GB RAM)
- **Production (medium):** m5.large (2 vCPU, 8GB RAM)

### Storage

- Use gp3 SSD volumes
- Development: 20GB minimum
- Production: 100GB+ based on needs
- Enable EBS snapshots for backups

### Key Pairs

- Generate or import SSH key pairs
- Store private keys securely
- Use IAM roles instead of access keys when possible

## VPC Configuration

### Basic Setup

- Create VPC with CIDR block (e.g., 10.0.0.0/16)
- Create public and private subnets
- Set up Internet Gateway
- Configure route tables
- Set up NAT Gateway for private subnets (if needed)

### Subnets

- Public subnets: For load balancers, bastion hosts
- Private subnets: For application servers, databases
- Multi-AZ for high availability

## Security Groups

### Application Security Group

```
Inbound:
- HTTP (80) from ALB security group
- HTTPS (443) from ALB security group
- SSH (22) from bastion/your IP only

Outbound:
- All traffic (0.0.0.0/0)
```

### Database Security Group

```
Inbound:
- MongoDB (27017) from application security group only
- Redis (6379) from application security group only
- SSH (22) from bastion/your IP only

Outbound:
- All traffic (0.0.0.0/0)
```

### Load Balancer Security Group

```
Inbound:
- HTTP (80) from 0.0.0.0/0
- HTTPS (443) from 0.0.0.0/0

Outbound:
- HTTP (80) to application security group
- HTTPS (443) to application security group
```

## Application Load Balancer

### Setup

1. Create ALB in public subnets
2. Configure target groups (EC2 instances)
3. Set up health checks
4. Configure listeners (HTTP → HTTPS redirect)
5. Attach SSL certificate from ACM

### Health Checks

- Path: `/health` or `/api/health`
- Protocol: HTTP
- Port: 3001 (backend) or 3000 (frontend)
- Healthy threshold: 2
- Unhealthy threshold: 2
- Timeout: 5 seconds
- Interval: 30 seconds

## Route53 DNS

### Domain Setup

1. Create hosted zone for domain
2. Create A record (alias) pointing to ALB
3. Create CNAME for www subdomain
4. Update nameservers at domain registrar

### SSL/TLS (ACM)

1. Request certificate in ACM (us-east-1 for CloudFront/ALB)
2. Validate via DNS (add CNAME records)
3. Attach certificate to ALB listener
4. Certificate auto-renews

## CloudWatch Monitoring

### Metrics

- EC2: CPU, Memory, Disk, Network
- ALB: Request count, Target response time, HTTP errors
- Custom metrics for application-specific data

### Alarms

- High CPU utilization
- Low disk space
- Application errors (via CloudWatch Logs)
- Unhealthy target instances

## Best Practices

- Use IAM roles instead of access keys
- Enable CloudTrail for audit logging
- Use VPC endpoints for AWS service access
- Implement least privilege security groups
- Use private subnets for databases
- Enable encryption at rest for EBS volumes
- Set up automated backups (EBS snapshots)
- Monitor costs with AWS Cost Explorer

## Integration

This skill integrates with `/db-setup` for MongoDB on EC2 and `/deploy` for deployment workflows.
