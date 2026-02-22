---
name: data-engineering-storage-authentication
description: "Cloud storage authentication patterns: AWS, GCP, Azure credentials, IAM roles, service principals, secret management, and secure credential handling for data pipelines."
dependsOn: []
---

# Cloud Storage Authentication

Secure authentication patterns for accessing cloud storage (S3, GCS, Azure Blob) and cloud services in data pipelines. Covers IAM roles, service principals, secret managers, and best practices for credential management.

## Quick Reference

| Provider | Recommended Auth | Alternative |
|----------|----------------|-------------|
| **AWS** | IAM roles (EC2/ECS/Lambda) | Environment variables, Secrets Manager |
| **GCP** | Workload Identity / ADC | Service account keys (discouraged) |
| **Azure** | Managed Identity | Service principal with certificate |
| **Local Dev** | `.env` files + local credentials | Static keys (temporary only) |

## Core Principles

1. **Least Privilege**: Grant only necessary permissions (read-only, specific bucket)
2. **Short-lived credentials**: Use STS tokens, OIDC, not long-term keys
3. **Automatic rotation**: Prefer managed identities that rotate automatically
4. **Secret management**: Never commit credentials; use secret managers
5. **Audit everything**: Enable CloudTrail/Azure Audit Logs/GCP Audit Logs
6. **Separate environments**: Different credentials for dev/staging/prod

## When to Use What?

- **Production on cloud VMs**: Use IAM roles/Managed Identities (no credentials in code)
- **CI/CD pipelines**: Use workload identity federation (OIDC) or short-lived tokens
- **Local development**: `.env` files with user credentials from `aws configure`, `gcloud auth`, `az login`
- **Third-party integrations**: Service principals with scoped permissions
- **Cross-account access**: Role assumption (AWS), workload identity (GCP), service principal (Azure)

## Skill Dependencies

This skill is foundational for:
- `@data-engineering-storage-remote-access` - All cloud storage backends
- `@data-engineering-storage-lakehouse` - Delta Lake/Iceberg with cloud catalogs
- `@data-engineering-streaming` - Kafka connectors with cloud auth
- `@data-engineering-ai-ml` - OpenAI, vector DBs with cloud storage
- `@data-engineering-orchestration` - dbt, Prefect, Dagster cloud connectors

---

## Detailed Guides

### AWS Authentication
See: `aws.md`

- IAM roles (EC2 instance profiles, ECS task roles, Lambda execution roles)
- IAM users with access keys (discouraged for production)
- STS temporary credentials (AssumeRole, GetSessionToken)
- S3 presigned URLs for temporary file access
- Cross-account access patterns
- AWS Secrets Manager integration
- Environment variable resolution (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`)

### Google Cloud Platform
See: `gcp.md`

- Service accounts (JSON keys)
- Workload Identity Federation (no keys needed!)
- Application Default Credentials (ADC)
- Cloud Storage signed URLs
- Secret Manager integration
- Environment variables (`GOOGLE_APPLICATION_CREDENTIALS`)
- GCP workload identity for GKE, Cloud Run, Compute Engine

### Azure
See: `azure.md`

- Managed Identities (system-assigned, user-assigned)
- Service Principals (client secret, certificate)
- SAS tokens for Blob Storage
- Azure Key Vault integration
- Environment variables (`AZURE_STORAGE_ACCOUNT`, `AZURE_STORAGE_KEY`)
- Azure AD workload identity for AKS, App Service, VMs

### Patterns & Best Practices
See: `patterns.md`

- Secret rotation automation
- Multi-environment credential management
- Local development setup without production keys
- CI/CD pipeline authentication (GitHub Actions, GitLab CI, Jenkins)
- Testing with mock credentials (Moto, google-cloud-testutils)
- Credential leakage prevention (.gitignore, pre-commit hooks)

### Testing Strategies
See: `testing.md`

- Mocking cloud services for unit tests
- Using local emulators (MinIO, Azurite, LocalStack)
- Test credential patterns with placeholders
- Integration test setup with temporary credentials

---

## Quick Examples

### AWS IAM Role (Production)
```python
# No credentials in code - automatically from EC2/ECS/Lambda
import boto3
s3 = boto3.client('s3')  # Uses instance metadata
```

### GCP Workload Identity (Production)
```bash
# Enable workload identity on GKE/Cloud Run
# Then in Python:
import google.auth
credentials, project = google.auth.default()
# No env vars needed!
```

### Azure Managed Identity (Production)
```python
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

credential = DefaultAzureCredential()  # Auto-detects managed identity
client = BlobServiceClient(account_url="...", credential=credential)
```

### Local Development
```bash
# AWS
aws configure  # Enter keys from IAM user (dev only)

# GCP
gcloud auth application-default login

# Azure
az login
```

---

## Common Pitfalls

❌ **Hardcoding credentials** - Committing to git → rotate immediately
❌ **Using root/admin accounts** - Create scoped users/service principals
❌ **Long-lived keys** - Rotate every 90 days or less
❌ **Over-permissive roles** - Grant `s3:GetObject` not `s3:*`
❌ **Missing environment separation** - Dev credentials in prod
❌ **Disabling TLS verification** - Except for local MinIO testing only

---

## References

- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [GCP Workload Identity](https://cloud.google.com/iam/docs/workload-identity-federation)
- [Azure Managed Identities](https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview)
- [HashiCorp Vault](https://developer.hashicorp.com/vault/docs)
- Legacy `@data-engineering-storage-remote-access` auth notes are deprecated; use this skill as the source of truth.
