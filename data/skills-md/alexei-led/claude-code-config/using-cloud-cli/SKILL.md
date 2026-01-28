---
name: using-cloud-cli
description: Cloud CLI patterns for GCP and AWS. Use when running bq queries, gcloud commands, aws commands, or making decisions about cloud services. Covers BigQuery cost optimization and operational best practices.
user-invocable: false
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
---

# Cloud CLI Patterns

Credentials are pre-configured. Use `--help` or Context7 for syntax.

## BigQuery

```bash
# Always estimate cost first
bq query --dry_run --use_legacy_sql=false 'SELECT ...'

# Run query
bq query --use_legacy_sql=false --format=json 'SELECT ...'

# List tables
bq ls project:dataset

# Get table schema
bq show --schema --format=json project:dataset.table
```

**Cost awareness**: Charged per bytes scanned. Use `--dry_run`, partition tables, specify columns.

## GCP (gcloud)

```bash
# List resources
gcloud compute instances list --format=json

# Describe resource
gcloud compute instances describe INSTANCE --zone=ZONE --format=json

# Create with explicit project
gcloud compute instances create NAME --project=PROJECT --zone=ZONE

# Use --quiet for automation
gcloud compute instances delete NAME --quiet
```

## AWS

```bash
# List resources
aws ec2 describe-instances --output json

# With JMESPath filtering
aws ec2 describe-instances --query 'Reservations[].Instances[].InstanceId' --output text

# Explicit region
aws s3 ls s3://bucket --region us-west-2

# Dry run where available
aws ec2 run-instances --dry-run ...
```

## Error Handling & Recovery

### Authentication Failures

**GCP auth issues:**

```bash
# Check current auth status
gcloud auth list

# Re-authenticate user
gcloud auth login

# Re-authenticate application default credentials
gcloud auth application-default login

# For service accounts
gcloud auth activate-service-account --key-file=key.json
```

**AWS auth issues:**

```bash
# Check current identity
aws sts get-caller-identity

# Verify credentials file
cat ~/.aws/credentials

# Use specific profile
aws s3 ls --profile production

# Refresh SSO credentials
aws sso login --profile my-sso-profile
```

**Common auth errors:**

| Error                  | Cause             | Fix                     |
| ---------------------- | ----------------- | ----------------------- |
| `UNAUTHENTICATED`      | No credentials    | Run `gcloud auth login` |
| `AccessDenied`         | Wrong permissions | Check IAM roles         |
| `ExpiredToken`         | Session expired   | Re-authenticate         |
| `InvalidClientTokenId` | Bad AWS key       | Verify credentials file |

### Rate Limiting

**Symptoms:**

- `429 Too Many Requests`
- `RESOURCE_EXHAUSTED`
- `Throttling` errors

**Mitigation:**

```bash
# Add delays between operations
for bucket in $(aws s3 ls | awk '{print $3}'); do
  aws s3 ls "s3://$bucket" --summarize
  sleep 1  # Prevent throttling
done

# Use pagination instead of large requests
aws ec2 describe-instances --max-items 100 --starting-token "$TOKEN"

# For BigQuery: Use batch queries, avoid rapid-fire
bq query --batch 'SELECT ...'  # Lower priority, less throttling
```

**API quotas:**

- Check quotas: `gcloud compute project-info describe --project=PROJECT`
- Request increase: Console → IAM → Quotas

### Common Error Patterns

**Resource not found:**

```bash
# Verify resource exists first
gcloud compute instances describe NAME --zone=ZONE 2>/dev/null || echo "Not found"

# List available resources
gcloud compute zones list --filter="region:us-central1"
```

**Permission denied:**

```bash
# Check your roles
gcloud projects get-iam-policy PROJECT --flatten="bindings[].members" \
  --filter="bindings.members:$(gcloud config get-value account)"

# For AWS
aws iam get-user
aws iam list-attached-user-policies --user-name USERNAME
```

**Region/zone mismatch:**

```bash
# Always specify explicitly
gcloud compute instances create NAME --zone=us-central1-a  # Not just region!
aws ec2 run-instances --region us-west-2 ...
```

### Retry Patterns

```bash
# Simple retry with backoff
retry_cmd() {
  local max_attempts=3
  local delay=2
  local attempt=1

  while [ $attempt -le $max_attempts ]; do
    if "$@"; then return 0; fi
    echo "Attempt $attempt failed, retrying in ${delay}s..."
    sleep $delay
    delay=$((delay * 2))
    attempt=$((attempt + 1))
  done
  return 1
}

retry_cmd gcloud compute instances start my-instance --zone=us-central1-a
```

## References

- [GCP.md](GCP.md) - GCP service patterns and common commands
- [AWS.md](AWS.md) - AWS service patterns and common commands
- [scripts/](scripts/) - Helper scripts for common operations
