---
name: aws-profile-management
description: Use before any Terraform or AWS operation to verify correct credentials and profile are active. Prevents cross-environment accidents.
---

# AWS Profile Management

## Overview

Credential mistakes are one of the most common causes of infrastructure accidents. This skill ensures the correct AWS profile is active before any operation.

**Announce at start:** "I'm using the aws-profile-management skill to verify credentials."

## Pre-Operation Verification

### Step 1: Check Current Identity

```bash
# Get current identity
aws sts get-caller-identity
```

Expected output includes:
- **Account**: AWS account ID
- **Arn**: IAM user/role ARN
- **UserId**: User or assumed role ID

### Step 2: Match to Environment

| Environment | Expected Account | Expected Role Pattern |
|-------------|------------------|----------------------|
| dev | 123456789012 | *-dev-*, *-developer-* |
| staging | 234567890123 | *-staging-*, *-deploy-* |
| prod | 345678901234 | *-prod-*, *-admin-* |

**STOP** if account doesn't match expected environment.

### Step 3: Check Credential Expiry

For assumed roles:
```bash
# Check remaining session time
aws sts get-caller-identity 2>&1 | grep -i expir || echo "Credentials valid"
```

For SSO:
```bash
# Check SSO session
aws sso list-accounts 2>&1 || echo "Check SSO login status"
```

## Profile Switching

### Using Named Profiles

```bash
# List available profiles
aws configure list-profiles

# Set profile for session
export AWS_PROFILE=production

# Or use inline
AWS_PROFILE=production terraform plan
```

### Using AWS SSO

```bash
# Login to SSO
aws sso login --profile production

# Verify login
aws sts get-caller-identity --profile production
```

### Using Assume Role

```bash
# Assume role and export credentials
eval $(aws sts assume-role \
  --role-arn arn:aws:iam::ACCOUNT:role/ROLE_NAME \
  --role-session-name terraform-session \
  --query 'Credentials.[AccessKeyId,SecretAccessKey,SessionToken]' \
  --output text | \
  awk '{print "export AWS_ACCESS_KEY_ID="$1"\nexport AWS_SECRET_ACCESS_KEY="$2"\nexport AWS_SESSION_TOKEN="$3}')

# Verify
aws sts get-caller-identity
```

## Environment Detection

### From Directory Structure

```
environments/
├── dev/
├── staging/
└── prod/
```

```bash
# Detect environment from path
ENV=$(basename "$(pwd)")
echo "Detected environment: $ENV"
```

### From Terraform Backend

```bash
# Check backend configuration
grep -A 10 'backend' *.tf | grep -E 'bucket|key|workspace'
```

### From Workspace

```bash
# Check Terraform workspace
terraform workspace show
```

## Safety Checks

### Pre-Operation Checklist

Before any Terraform or AWS operation:

1. **Identity Verified**
   - [ ] Account ID matches environment
   - [ ] Role/user is appropriate
   - [ ] Credentials not expired

2. **Environment Confirmed**
   - [ ] Directory matches expected environment
   - [ ] Backend configuration is correct
   - [ ] No conflicting env vars set

3. **Permission Verified**
   - [ ] Role has required permissions
   - [ ] No unexpected permission errors expected

### Red Flags - STOP Immediately

| Condition | Action |
|-----------|--------|
| Account ID doesn't match environment | STOP - wrong account! |
| Role seems too permissive for task | Verify with user |
| Credentials expired | Re-authenticate |
| Multiple AWS_* env vars set | Clear and use profile |
| Unknown account ID | Verify before proceeding |

## Common Issues

### Wrong Account Active

**Symptoms:**
- Terraform can't find expected resources
- Plan shows creating resources that exist
- Permission denied for expected resources

**Solution:**
```bash
# Clear any env vars
unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN

# Set correct profile
export AWS_PROFILE=correct_profile

# Verify
aws sts get-caller-identity
```

### Expired Credentials

**Symptoms:**
- "ExpiredToken" errors
- "credentials have expired" messages

**Solution:**
```bash
# For SSO
aws sso login --profile your_profile

# For assumed role
# Re-run assume-role command
```

### Conflicting Configurations

**Symptoms:**
- Unexpected account appearing
- Operations in wrong region

**Solution:**
```bash
# Check all credential sources
echo "Profile: $AWS_PROFILE"
echo "Access Key set: ${AWS_ACCESS_KEY_ID:+yes}"
echo "Default region: $AWS_DEFAULT_REGION"
aws configure list
```

## Integration with Other Skills

This skill should be invoked **before**:
- terraform-plan-review
- terraform-drift-detection
- terraform-state-operations
- Any AWS CLI operations

The profile verification output should be included in analysis reports to confirm correct environment.
