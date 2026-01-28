---
name: cloud-platforms
description: AWS, GCP, Azure data platforms, infrastructure as code, and cloud-native data solutions
sasmp_version: "1.3.0"
bonded_agent: 05-cloud-engineer
bond_type: PRIMARY_BOND
skill_version: "2.0.0"
last_updated: "2025-01"
complexity: intermediate
estimated_mastery_hours: 160
prerequisites: [python-programming, sql-databases]
unlocks: [containerization, big-data, data-warehousing]
---

# Cloud Platforms for Data Engineering

Production-grade cloud infrastructure for data pipelines, storage, and analytics on AWS, GCP, and Azure.

## Quick Start

```python
# AWS S3 + Lambda Data Pipeline
import boto3
import json

s3_client = boto3.client('s3')
glue_client = boto3.client('glue')

def lambda_handler(event, context):
    """Process S3 event and trigger Glue job."""
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Trigger Glue ETL job
    response = glue_client.start_job_run(
        JobName='etl-process-raw-data',
        Arguments={
            '--source_path': f's3://{bucket}/{key}',
            '--output_path': 's3://processed-bucket/output/'
        }
    )

    return {'statusCode': 200, 'jobRunId': response['JobRunId']}
```

## Core Concepts

### 1. AWS Data Stack

```python
# AWS Glue ETL Job (PySpark)
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'source_path', 'output_path'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read from S3
df = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [args['source_path']]},
    format="parquet"
)

# Transform
df_transformed = ApplyMapping.apply(
    frame=df,
    mappings=[
        ("id", "long", "id", "long"),
        ("name", "string", "customer_name", "string"),
        ("created_at", "string", "created_at", "timestamp")
    ]
)

# Write to S3 with partitioning
glueContext.write_dynamic_frame.from_options(
    frame=df_transformed,
    connection_type="s3",
    connection_options={
        "path": args['output_path'],
        "partitionKeys": ["year", "month"]
    },
    format="parquet"
)

job.commit()
```

### 2. GCP Data Stack

```python
# BigQuery + Cloud Functions
from google.cloud import bigquery
from google.cloud import storage

def process_gcs_file(event, context):
    """Cloud Function triggered by GCS upload."""
    bucket = event['bucket']
    name = event['name']

    client = bigquery.Client()

    # Load data from GCS to BigQuery
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )

    uri = f"gs://{bucket}/{name}"
    table_id = "project.dataset.events"

    load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
    load_job.result()  # Wait for completion

    return f"Loaded {load_job.output_rows} rows"
```

### 3. Terraform Infrastructure

```hcl
# AWS Data Lake Infrastructure
resource "aws_s3_bucket" "data_lake" {
  bucket = "company-data-lake-${var.environment}"

  tags = {
    Environment = var.environment
    Purpose     = "data-lake"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "data_lake_lifecycle" {
  bucket = aws_s3_bucket.data_lake.id

  rule {
    id     = "archive-old-data"
    status = "Enabled"

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }
  }
}

resource "aws_glue_catalog_database" "analytics" {
  name = "analytics_${var.environment}"
}

resource "aws_glue_crawler" "data_crawler" {
  database_name = aws_glue_catalog_database.analytics.name
  name          = "data-crawler"
  role          = aws_iam_role.glue_role.arn

  s3_target {
    path = "s3://${aws_s3_bucket.data_lake.bucket}/raw/"
  }

  schedule = "cron(0 6 * * ? *)"
}
```

### 4. Cost Optimization

```python
# AWS Cost monitoring
import boto3
from datetime import datetime, timedelta

def get_service_costs(days=30):
    """Get cost breakdown by service."""
    ce = boto3.client('ce')

    end = datetime.now().strftime('%Y-%m-%d')
    start = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

    response = ce.get_cost_and_usage(
        TimePeriod={'Start': start, 'End': end},
        Granularity='MONTHLY',
        Metrics=['UnblendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
    )

    for result in response['ResultsByTime']:
        for group in result['Groups']:
            service = group['Keys'][0]
            cost = float(group['Metrics']['UnblendedCost']['Amount'])
            print(f"{service}: ${cost:.2f}")

# S3 Intelligent Tiering
s3 = boto3.client('s3')
s3.put_bucket_intelligent_tiering_configuration(
    Bucket='data-lake',
    Id='AutoTiering',
    IntelligentTieringConfiguration={
        'Id': 'AutoTiering',
        'Status': 'Enabled',
        'Tierings': [
            {'Days': 90, 'AccessTier': 'ARCHIVE_ACCESS'},
            {'Days': 180, 'AccessTier': 'DEEP_ARCHIVE_ACCESS'}
        ]
    }
)
```

## Tools & Technologies

| Tool | Purpose | Version (2025) |
|------|---------|----------------|
| **AWS S3** | Object storage | Latest |
| **AWS Glue** | ETL service | 4.0 |
| **AWS EMR** | Managed Spark | 7.0+ |
| **BigQuery** | Analytics DW | Latest |
| **Cloud Dataflow** | Stream/batch | Latest |
| **Azure Data Factory** | ETL/ELT | Latest |
| **Terraform** | IaC | 1.6+ |
| **Pulumi** | IaC (Python) | 3.0+ |

## Troubleshooting Guide

| Issue | Symptoms | Root Cause | Fix |
|-------|----------|------------|-----|
| **Permission Denied** | AccessDenied error | IAM policy missing | Check IAM roles |
| **Timeout** | Lambda/Function timeout | Long-running process | Increase timeout, use Step Functions |
| **Cost Spike** | Unexpected charges | Unoptimized queries/storage | Enable cost alerts, lifecycle policies |
| **Cold Start** | Slow first invocation | Lambda cold start | Provisioned concurrency |

## Best Practices

```python
# ✅ DO: Use IAM roles, not access keys
session = boto3.Session()  # Uses instance role

# ✅ DO: Enable encryption at rest
s3.put_bucket_encryption(
    Bucket='my-bucket',
    ServerSideEncryptionConfiguration={...}
)

# ✅ DO: Use VPC endpoints for private access
# ✅ DO: Enable CloudWatch alarms for monitoring
# ✅ DO: Use tags for cost allocation

# ❌ DON'T: Hard-code credentials
# ❌ DON'T: Use root account for operations
# ❌ DON'T: Leave buckets public
```

## Resources

- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [GCP Data Engineering](https://cloud.google.com/learn/what-is-data-engineering)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest)

---

**Skill Certification Checklist:**
- [ ] Can design cloud data lake architecture
- [ ] Can implement ETL with Glue/Dataflow
- [ ] Can manage infrastructure with Terraform
- [ ] Can optimize cloud costs
- [ ] Can implement security best practices
