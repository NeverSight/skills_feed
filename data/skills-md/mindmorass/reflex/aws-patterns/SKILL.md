---
name: aws-patterns
description: AWS cloud infrastructure patterns and best practices. Use when designing AWS architectures, creating Lambda functions, configuring S3 buckets, setting up EC2 instances, designing VPCs, or implementing any AWS services.
---

# AWS Patterns

Best practices for AWS cloud infrastructure design and implementation.

## Core Services Patterns

### Lambda Functions

```python
# Best practice Lambda handler structure
import json
import logging
from typing import Any

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event: dict, context: Any) -> dict:
    """Lambda handler with proper error handling and logging."""
    try:
        logger.info(f"Event: {json.dumps(event)}")

        # Process event
        result = process_event(event)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(result)
        }
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return {"statusCode": 400, "body": json.dumps({"error": str(e)})}
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return {"statusCode": 500, "body": json.dumps({"error": "Internal server error"})}
```

### S3 Bucket Configuration

```yaml
# Secure S3 bucket with versioning and encryption
Resources:
  SecureBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "${AWS::StackName}-data"
      VersioningConfiguration:
        Status: Enabled
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      LoggingConfiguration:
        DestinationBucketName: !Ref LoggingBucket
        LogFilePrefix: s3-access-logs/
```

### VPC Design

```yaml
# Three-tier VPC architecture
Resources:
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      EnableDnsSupport: true

  # Public subnets (load balancers, NAT gateways)
  PublicSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.1.0/24
      AvailabilityZone: !Select [0, !GetAZs ""]
      MapPublicIpOnLaunch: true

  # Private subnets (application tier)
  PrivateSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.10.0/24
      AvailabilityZone: !Select [0, !GetAZs ""]

  # Data subnets (databases, caches)
  DataSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.20.0/24
      AvailabilityZone: !Select [0, !GetAZs ""]
```

## IAM Best Practices

### Least Privilege Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowSpecificS3Actions",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::my-bucket/prefix/*",
      "Condition": {
        "StringEquals": {
          "s3:x-amz-acl": "private"
        }
      }
    }
  ]
}
```

### Service Role Pattern

```yaml
LambdaExecutionRole:
  Type: AWS::IAM::Role
  Properties:
    AssumeRolePolicyDocument:
      Version: "2012-10-17"
      Statement:
        - Effect: Allow
          Principal:
            Service: lambda.amazonaws.com
          Action: sts:AssumeRole
    ManagedPolicyArns:
      - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
    Policies:
      - PolicyName: CustomPolicy
        PolicyDocument:
          Version: "2012-10-17"
          Statement:
            - Effect: Allow
              Action:
                - dynamodb:GetItem
                - dynamodb:PutItem
              Resource: !GetAtt Table.Arn
```

## Cost Optimization

### Resource Tagging Strategy

```yaml
Tags:
  - Key: Environment
    Value: !Ref Environment
  - Key: Project
    Value: !Ref ProjectName
  - Key: CostCenter
    Value: !Ref CostCenter
  - Key: Owner
    Value: !Ref OwnerEmail
  - Key: AutoShutdown
    Value: "true"  # For non-prod resources
```

### Spot Instances for Non-Critical Workloads

```yaml
SpotFleet:
  Type: AWS::EC2::SpotFleet
  Properties:
    SpotFleetRequestConfigData:
      IamFleetRole: !GetAtt SpotFleetRole.Arn
      TargetCapacity: 10
      AllocationStrategy: lowestPrice
      LaunchSpecifications:
        - InstanceType: m5.large
          SpotPrice: "0.05"
          SubnetId: !Ref PrivateSubnet1
```

## High Availability Patterns

### Multi-AZ Deployment

- Deploy across minimum 2 AZs, prefer 3
- Use Auto Scaling Groups with AZ-aware placement
- Configure cross-AZ load balancing
- Enable Multi-AZ for RDS and ElastiCache

### Circuit Breaker with Step Functions

```yaml
StateMachine:
  Type: AWS::StepFunctions::StateMachine
  Properties:
    DefinitionString: |
      {
        "StartAt": "CallService",
        "States": {
          "CallService": {
            "Type": "Task",
            "Resource": "${LambdaArn}",
            "Retry": [
              {
                "ErrorEquals": ["States.TaskFailed"],
                "IntervalSeconds": 2,
                "MaxAttempts": 3,
                "BackoffRate": 2
              }
            ],
            "Catch": [
              {
                "ErrorEquals": ["States.ALL"],
                "Next": "Fallback"
              }
            ],
            "End": true
          },
          "Fallback": {
            "Type": "Pass",
            "Result": {"status": "degraded"},
            "End": true
          }
        }
      }
```

## Security Patterns

### Secrets Manager Integration

```python
import boto3
from botocore.exceptions import ClientError
import json

def get_secret(secret_name: str, region: str = "us-east-1") -> dict:
    """Retrieve secret from AWS Secrets Manager."""
    client = boto3.client("secretsmanager", region_name=region)

    try:
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response["SecretString"])
    except ClientError as e:
        raise RuntimeError(f"Failed to retrieve secret: {e}")
```

### KMS Encryption

```yaml
KMSKey:
  Type: AWS::KMS::Key
  Properties:
    Description: Customer managed key for data encryption
    EnableKeyRotation: true
    KeyPolicy:
      Version: "2012-10-17"
      Statement:
        - Sid: Enable IAM User Permissions
          Effect: Allow
          Principal:
            AWS: !Sub "arn:aws:iam::${AWS::AccountId}:root"
          Action: kms:*
          Resource: "*"
```

## References

- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Security Best Practices](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/)
- [AWS Cost Optimization](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/)
