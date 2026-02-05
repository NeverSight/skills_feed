---
name: terraform-state-operations
description: Use when performing Terraform state surgery - state mv, import, rm operations. Requires extra safety measures.
---

# Terraform State Operations

## Overview

State operations modify Terraform's understanding of infrastructure without changing actual resources. These are dangerous because mistakes can orphan resources or cause Terraform to recreate existing infrastructure.

**Announce at start:** "I'm using the terraform-state-operations skill for safe state surgery."

## CRITICAL: Pre-Operation Safety

### 1. Create State Backup

**ALWAYS create a backup before ANY state operation:**

```bash
# Create timestamped backup
BACKUP_NAME="state-backup-$(date +%Y%m%d-%H%M%S).tfstate"

# For local state
cp terraform.tfstate "$BACKUP_NAME"

# For remote state (S3 example)
terraform state pull > "$BACKUP_NAME"

echo "Backup created: $BACKUP_NAME"
```

### 2. Document the Operation

Before proceeding, create a record:

```markdown
## State Operation Record

**Date:** [timestamp]
**Environment:** [env name]
**Operator:** [user]
**Reason:** [why this operation is needed]

### Planned Operations
1. [operation 1]
2. [operation 2]

### Backup Location
- Local: [path]
- Remote: [if applicable]

### Rollback Plan
[How to restore if something goes wrong]
```

### 3. Get User Approval

Present the plan and **require explicit approval** before executing.

## State Operations Guide

### terraform state mv

**Use case:** Rename resources, reorganize modules, refactor code

```bash
# List current resources
terraform state list

# Move/rename a resource
terraform state mv aws_instance.old_name aws_instance.new_name

# Move into a module
terraform state mv aws_instance.web module.web.aws_instance.this

# Move between modules
terraform state mv module.old.aws_instance.web module.new.aws_instance.web
```

**Verification after mv:**
```bash
# Should show no changes
terraform plan
```

### terraform state rm

**Use case:** Remove from state without destroying actual resource (adopting externally-managed resources)

```bash
# Remove single resource
terraform state rm aws_instance.legacy

# Remove module
terraform state rm module.legacy
```

**WARNING:** The actual resource continues to exist but is no longer managed by Terraform.

**Verification after rm:**
```bash
# Resource should appear as "new" if still in code
# Remove from code if intentionally unmanaging
terraform plan
```

### terraform import

**Use case:** Bring existing infrastructure under Terraform management

```bash
# Import existing resource
terraform import aws_instance.web i-1234567890abcdef0

# Import with module path
terraform import module.web.aws_instance.this i-1234567890abcdef0
```

**Before import:**
1. Write the resource configuration in code
2. Ensure configuration matches actual resource
3. Import
4. Run plan to verify no changes

**Verification after import:**
```bash
# Should show no changes (or only acceptable differences)
terraform plan
```

### terraform state pull/push

**Use case:** Backup, migrate, or restore state

```bash
# Pull current state
terraform state pull > state.json

# Push state (DANGEROUS - can overwrite!)
# terraform state push state.json  # BLOCKED by hook
```

## Recovery Procedures

### If State Becomes Corrupted

```bash
# Restore from backup
cp "$BACKUP_NAME" terraform.tfstate

# For remote state - may need to disable locking temporarily
# Consult your backend documentation
```

### If Resources Are Orphaned

1. Identify orphaned resources in AWS console
2. Either:
   - Import them back: `terraform import ...`
   - Delete them manually if no longer needed

### If Wrong Resources Removed

```bash
# Restore backup
cp "$BACKUP_NAME" terraform.tfstate

# Re-initialize to sync with backend
terraform init -reconfigure
```

## Approval Workflow

### For state mv (Low Risk)
1. Show planned move
2. Explain impact
3. Request approval
4. Execute with verification

### For state rm (Medium Risk)
1. Show what will be unmanaged
2. Explain orphan implications
3. Confirm resource won't be deleted
4. Request explicit approval
5. Execute with verification

### For state push (High Risk)
**Hook blocks this command.** If genuinely needed:
1. Explain why state push is necessary
2. Show state diff
3. Request explicit approval with acknowledgment of risks
4. User must disable hook manually

## Verification Checklist

Before any state operation:
- [ ] Backup created and verified
- [ ] Operation documented
- [ ] Impact explained to user
- [ ] User explicitly approved
- [ ] Rollback plan established

After operation:
- [ ] terraform plan shows expected result
- [ ] No unintended changes detected
- [ ] Backup retained for rollback window
- [ ] Operation logged to memory
