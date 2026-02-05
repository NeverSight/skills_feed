---
name: terraform-drift-detection
description: Use when detecting infrastructure drift between Terraform state and actual AWS resources. Identifies out-of-band changes.
---

# Terraform Drift Detection

## Overview

Detect and categorize drift between Terraform-managed state and actual infrastructure. Drift indicates out-of-band changes that can cause problems during the next apply.

**Announce at start:** "I'm using the terraform-drift-detection skill to check for infrastructure drift."

## The Process

### Step 1: Verify Environment

```bash
# Verify AWS credentials and account
aws sts get-caller-identity

# Confirm we're in the right directory/environment
pwd
ls -la *.tf 2>/dev/null | head -5
```

### Step 2: Refresh State

```bash
# Initialize if needed
terraform init

# Refresh state to detect drift
terraform plan -refresh-only -out=drift.out

# Convert to JSON for analysis
terraform show -json drift.out > drift.json
```

### Step 3: Analyze Drift

Parse drift.json and categorize changes:

#### Drift Categories

| Category | Severity | Examples |
|----------|----------|----------|
| **Security Drift** | CRITICAL | Security groups, IAM, encryption |
| **Configuration Drift** | HIGH | Instance settings, networking |
| **Tag Drift** | LOW | Tags modified outside Terraform |
| **Metadata Drift** | INFO | AWS-managed fields that change |

### Step 4: Dispatch Analysis Agent

```
Task(drift-detector) → Categorize and assess drift impact
```

**Agent should:**
- Categorize each drifted resource
- Assess impact of accepting vs rejecting drift
- Identify potential causes (manual changes, AWS updates, etc.)

### Step 5: Present Findings

```markdown
## Drift Detection Report

### Summary
- Total drifted resources: X
- Critical drift: Y
- High drift: Z
- Low/Info drift: W

### Critical Drift (Requires Immediate Attention)
| Resource | Attribute | State Value | Actual Value |
|----------|-----------|-------------|--------------|
| ... | ... | ... | ... |

### Potential Causes
- Manual console changes: [list if detected]
- AWS service updates: [list if detected]
- Unknown origin: [list if detected]

### Recommended Actions
1. [Action for each drifted resource]
```

### Step 6: Resolution Options

Present user with options:

1. **Accept Drift**: Run `terraform apply -refresh-only` to update state to match actual
2. **Reject Drift**: Run `terraform apply` to revert actual infrastructure to match code
3. **Investigate**: Manual review needed before deciding
4. **Hybrid**: Accept some drift, reject other drift

**Never auto-resolve drift. Always get user approval.**

## Common Drift Sources

### Intentional (Usually Accept)
- AWS auto-scaling adjustments
- Managed service updates
- Emergency manual fixes (document these!)

### Unintentional (Usually Reject)
- Console click-ops mistakes
- Unapproved manual changes
- Conflicting automation

### Systemic (Fix Root Cause)
- Multiple tools managing same resources
- Missing Terraform coverage
- CI/CD race conditions

## Integration with Memory

Store detected drift patterns:
- Which resources commonly drift
- Common causes in this environment
- Resolution preferences

Query memory before analysis:
- Has this resource drifted before?
- What was the cause last time?
- What resolution was chosen?

## Verification Checklist

Before presenting:
- [ ] Refresh completed successfully
- [ ] All drift categorized by severity
- [ ] Root causes identified where possible
- [ ] Resolution options are clear
- [ ] No sensitive values exposed in output
