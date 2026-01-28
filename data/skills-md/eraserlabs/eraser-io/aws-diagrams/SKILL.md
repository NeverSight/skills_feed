---
name: aws-diagrams
description: 'Visualizes AWS infrastructure from CLI output, CloudFormation, or descriptions. Use when user has AWS resources to diagram.'
license: MIT
compatibility: Requires network access to call Eraser API
allowed-tools: Read Write Bash(curl:*)
metadata:
  version: "1.0.0"
  author: Eraser Labs
  tags: aws, diagram, cloudformation, ec2, vpc, s3, rds, lambda, infrastructure
---

# AWS Diagram Generator

Generates architecture diagrams for AWS infrastructure from CloudFormation templates, AWS CLI output, or natural language descriptions.

## When to Use

Activate this skill when:

- User has AWS CloudFormation templates (YAML/JSON)
- User provides AWS CLI output (e.g., `aws ec2 describe-instances`)
- User wants to visualize AWS resources
- User mentions AWS services (EC2, S3, RDS, Lambda, VPC, etc.)
- User asks to "diagram my AWS infrastructure"

## How It Works

This skill generates AWS-specific diagrams by parsing AWS resources and calling the Eraser API directly:

1. **Parse AWS Resources**: Extract resources from CloudFormation, CLI output, or descriptions
2. **Map AWS Relationships**: Identify VPCs, subnets, security groups, IAM roles
3. **Generate Eraser DSL**: Create Eraser DSL code from AWS resources
4. **Call Eraser API**: Use `/api/render/elements` with `diagramType: "cloud-architecture-diagram"`

## Instructions

When the user provides AWS infrastructure information:

1. **Parse the Source**

   - **CloudFormation**: Extract `Resources` section, identify types (AWS::EC2::Instance, etc.)
   - **CLI Output**: Parse JSON output from `aws` commands
   - **Description**: Identify AWS service names and relationships

2. **Identify AWS Components**

   - **Networking**: VPCs, Subnets, Internet Gateways, NAT Gateways, Route Tables
   - **Compute**: EC2 Instances, Auto Scaling Groups, Lambda Functions, ECS Services
   - **Storage**: S3 Buckets, EBS Volumes, EFS File Systems
   - **Databases**: RDS Instances, DynamoDB Tables, ElastiCache Clusters
   - **Security**: Security Groups, IAM Roles, IAM Policies, NACLs
   - **Load Balancing**: ALB, NLB, CLB
   - **Other**: SQS Queues, SNS Topics, API Gateway, CloudFront

3. **Map Relationships**

   - EC2 instances in subnets
   - Subnets in VPCs
   - Security groups attached to instances
   - IAM roles attached to services
   - Load balancers targeting instances
   - Databases accessed by applications

4. **Generate Eraser DSL** Convert AWS resources to Eraser DSL:

   - **CRITICAL: Label Formatting Rules**
     - Labels MUST be on a single line - NEVER use newlines inside label attributes
     - Keep labels simple and readable - prefer separate labels over concatenating too much metadata
     - Format DSL with proper line breaks (one node/group per line, but labels stay on single lines)
     - If including metadata like CIDR blocks or instance types, include them in the same quoted label string: `[label: "VPC 10.0.0.0/16"]`

   Example:

   ```
   main-vpc [label: "VPC 10.0.0.0/16"] {
     public-subnet [label: "Public Subnet"] {
       web-server [icon: aws-ec2, label: "Web Server"]
       load-balancer [icon: aws-elb]
     }
     private-subnet [label: "Private Subnet"] {
       database [icon: aws-rds]
       cache [icon: aws-elasticache]
     }
   }
   data-bucket [icon: aws-s3]
   function [icon: aws-lambda]
   load-balancer -> web-server
   web-server -> database
   ```

5. **Make the HTTP Request**

   **IMPORTANT**: You MUST execute this curl command after generating the DSL. Never stop after generating DSL without making the API call.

   **CRITICAL**: In the `X-Skill-Source` header below, you MUST replace the value with your AI agent name:
   - If you are Claude (Anthropic), use: `claude`
   - If you are running in Cursor, use: `cursor`
   - If you are ChatGPT (OpenAI), use: `chatgpt`
   - If you are Gemini (Google), use: `gemini`
   - Otherwise, use your model/agent name in lowercase

   ```bash
   curl -X POST https://app.eraser.io/api/render/elements \
     -H "Content-Type: application/json" \
     -H "X-Skill-Source: eraser-skill" \
     -H "Authorization: Bearer ${ERASER_API_KEY}" \
     -d '{
       "elements": [{
         "type": "diagram",
         "id": "diagram-1",
         "code": "<your generated DSL>",
         "diagramType": "cloud-architecture-diagram"
       }],
       "scale": 2,
        "theme": "${ERASER_THEME:-dark}",
       "background": true
     }'
   ```

6. **Track Sources During Analysis**

   As you analyze files and resources to generate the diagram, track:

   - **Internal files**: Record each file path you read and what information was extracted (e.g., `infra/main.tf` - VPC and subnet definitions)
   - **External references**: Note any documentation, examples, or URLs consulted (e.g., AWS VPC best practices documentation)
   - **Annotations**: For each source, note what it contributed to the diagram

7. **Handle the Response**

   **CRITICAL: Minimal Output Format**

   Your response MUST always include these elements with clear headers:

   1. **Diagram Preview**: Display with a header
      ```
      ## Diagram
      ![{Title}]({imageUrl})
      ```
      Use the ACTUAL `imageUrl` from the API response.

   2. **Editor Link**: Display with a header
      ```
      ## Open in Eraser
      [Edit this diagram in the Eraser editor]({createEraserFileUrl})
      ```
      Use the ACTUAL URL from the API response.

   3. **Sources section**: Brief list of files/resources analyzed (if applicable)
      ```
      ## Sources
      - `path/to/file` - What was extracted
      ```

   4. **Diagram Code section**: The Eraser DSL in a code block with `eraser` language tag
      ```
      ## Diagram Code
      ```eraser
      {DSL code here}
      ```
      ```

   5. **Learn More link**: `You can learn more about Eraser at https://docs.eraser.io`

   **Additional content rules:**
   - If the user ONLY asked for a diagram, include NOTHING beyond the 5 elements above
   - If the user explicitly asked for more (e.g., "explain the architecture", "suggest improvements"), you may include that additional content
   - Never add unrequested sections like Overview, Security Considerations, Testing, etc.

   The default output should be SHORT. The diagram image speaks for itself.

## AWS-Specific Tips

- **Show Regions and AZs**: Include availability zones for multi-AZ deployments
- **VPC as Container**: Always show VPCs containing subnets and resources
- **Security Groups**: Include security group rules and attachments
- **IAM Roles**: Show IAM roles attached to services
- **Data Flow**: Show traffic flow (Internet → ALB → EC2 → RDS)
- **Use AWS Icons**: Request AWS-specific styling in the description

## Example: CloudFormation with Multiple AWS Services

### User Input

```yaml
Resources:
  MyVPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16

  PublicSubnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref MyVPC
      CidrBlock: 10.0.1.0/24

  WebServer:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: t3.micro
      SubnetId: !Ref PublicSubnet

  MyBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-app-bucket

  MyFunction:
    Type: AWS::Lambda::Function
    Properties:
      Runtime: python3.9
      Handler: index.handler

  MyDatabase:
    Type: AWS::RDS::DBInstance
    Properties:
      Engine: postgres
      DBInstanceClass: db.t3.micro
```

### Expected Behavior

1. Parses CloudFormation:

   - **Networking**: VPC, Subnet
   - **Compute**: EC2 instance, Lambda function
   - **Storage**: S3 bucket
   - **Database**: RDS PostgreSQL instance

2. Generates DSL showing AWS service diversity:

   ```
   MyVPC [label: "VPC 10.0.0.0/16"] {
     PublicSubnet [label: "Public Subnet 10.0.1.0/24"] {
       WebServer [icon: aws-ec2, label: "EC2 t3.micro"]
     }
   }

   MyBucket [icon: aws-s3, label: "S3 my-app-bucket"]
   MyFunction [icon: aws-lambda, label: "Lambda python3.9"]
   MyDatabase [icon: aws-rds, label: "RDS PostgreSQL db.t3.micro"]

   WebServer -> MyBucket
   MyFunction -> MyDatabase
   WebServer -> MyDatabase
   ```

   **Important**: All label text must be on a single line within quotes. AWS-specific: Include service icons, show data flows between services, group by VPC when applicable.

3. Calls `/api/render/elements` with `diagramType: "cloud-architecture-diagram"`

## Example: AWS CLI Output

### User Input

```
User runs: aws ec2 describe-instances
Provides JSON output
```

### Expected Behavior

1. Parses JSON to extract:

   - Instance IDs, types, states
   - Subnet IDs, VPC IDs
   - Security groups
   - Tags

2. Formats and calls API
