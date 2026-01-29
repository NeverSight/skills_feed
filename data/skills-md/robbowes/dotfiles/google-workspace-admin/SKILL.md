---
name: google-workspace-admin
description: Google Workspace administration via terminal using GAM7 CLI. Use when user wants to manage users, groups, organizational units, Drive files, labels, permissions, Chrome devices, Gmail settings, or any Google Workspace admin task from command line. Covers GAM7 installation, common workflows, bulk operations, data classification labels, and security best practices. Beginner-friendly with guidance toward standard approaches.
---

# Google Workspace Admin CLI (GAM7)

GAM7 is the standard CLI tool for Google Workspace administration. Before executing commands, ask clarifying questions to ensure standard approaches.

## Beginner Guidance Philosophy

**Always ask before acting:**
- "What's the business reason for this change?"
- "Is this a one-off or recurring need?"
- "Have you checked if this can be done in Admin Console instead?"
- "Should we test on a single user first?"

**Guide toward standard practices:**
- Bulk operations should use CSV files, not loops
- Changes to permissions should be audited
- User provisioning should follow established OU structure

## Installation

```bash
# Linux/macOS/Cloud Shell
bash <(curl -s -S -L https://git.io/gam-install) -l

# Verify
gam version
gam info domain
```

Setup requires: Google Workspace paid/Edu/Nonprofit edition, super admin access.

## Core Command Patterns

```bash
gam <action> <entity> [options]
gam <entity> <selector> <action> [options]
gam csv <file> gam <action> ~column_name
```

## User Management

```bash
# List all users
gam print users allfields todrive

# Create user
gam create user john.doe@domain.com firstname John lastname Doe password 'TempPass123!' changepassword on org /Staff

# Create from CSV (users.csv: email,firstname,lastname,password,org)
gam csv users.csv gam create user ~email firstname ~firstname lastname ~lastname password ~password org ~org changepassword on

# Update user
gam update user john.doe@domain.com suspended off

# Bulk suspend (suspended_users.csv: email)
gam csv suspended_users.csv gam update user ~email suspended on

# Delete user
gam delete user john.doe@domain.com

# Get user info
gam info user john.doe@domain.com

# Reset password
gam update user john.doe@domain.com password 'NewTemp123!' changepassword on
```

⚠️ **Before bulk user operations:** Always preview with `gam csv file.csv gam info user ~email` first.

## Group Management

```bash
# List groups
gam print groups allfields members todrive

# Create group
gam create group engineering@domain.com name "Engineering Team" description "Engineering department"

# Add members
gam update group engineering@domain.com add member user@domain.com
gam update group engineering@domain.com add owner manager@domain.com

# Bulk add (members.csv: group,email,role)
gam csv members.csv gam update group ~group add ~role ~email

# Remove member
gam update group engineering@domain.com delete member user@domain.com

# Group settings
gam update group engineering@domain.com who_can_join invited_can_join who_can_post_message all_members_can_post
```

## Organizational Units

```bash
# List OUs
gam print orgs allfields

# Create OU
gam create org "/Staff/Engineering" description "Engineering department"

# Move user to OU
gam update user john.doe@domain.com org "/Staff/Engineering"

# Bulk move (moves.csv: email,org)
gam csv moves.csv gam update user ~email org ~org
```

## Drive & Labels

```bash
# List user's files
gam user john.doe@domain.com print filelist todrive

# Find externally shared files
gam user john.doe@domain.com print filelist query "visibility='anyoneWithLink' or visibility='anyoneCanFind'" todrive

# Transfer ownership
gam user departing@domain.com transfer drive newowner@domain.com

# Shared drives
gam print shareddrives todrive
gam create shareddrive name "Project Alpha"
```

### Data Classification Labels

See [references/labels.md](references/labels.md) for full label management.

```bash
# List available labels
gam print drivelabels todrive

# Show label details
gam info drivelabel labels/<label_id>

# Apply label to file
gam user user@domain.com update drivefile id:<file_id> addlabel labels/<label_id> field.<field_id> selection <choice_id>

# Find files by label
gam user user@domain.com print filelist query "labels/<label_id>" todrive

# Bulk apply labels (files.csv: user,file_id,label_id,field_id,choice_id)
gam csv files.csv gam user ~user update drivefile id:~file_id addlabel labels/~label_id field.~field_id selection ~choice_id
```

⚠️ **Label creation must be done in Admin Console** (Security > Data classification > Label Manager). GAM can apply/query labels but not create them.

## Security & Audit

```bash
# 2-Step Verification status
gam print users fields primaryEmail,isEnrolledIn2Sv,isEnforcedIn2Sv todrive

# Find users without 2SV
gam print users query "isEnrolledIn2Sv=false" todrive

# Admin audit log
gam report admin start -30d todrive

# Login audit
gam report login start -7d todrive

# Drive activity
gam report drive start -7d todrive

# Token (OAuth app) audit
gam all users print tokens todrive
```

## Chrome & Devices

```bash
# List Chrome devices
gam print cros allfields todrive

# Disable device
gam update cros query:serial:ABC123 action disable

# Mobile devices
gam print mobile todrive

# Wipe mobile device
gam update mobile <resource_id> action admin_remote_wipe
```

## Gmail Settings

```bash
# Set vacation responder
gam user user@domain.com vacation on subject "Out of Office" message "I'm away until Monday"

# Set signature
gam user user@domain.com signature file signature.html

# Bulk signature (users.csv: email)
gam csv users.csv gam user ~email signature file signature.html

# Add delegate
gam user executive@domain.com delegate to assistant@domain.com

# List filters
gam user user@domain.com print filters
```

## Bulk Operations Pattern

**Always follow this pattern:**
1. Create CSV with required columns
2. Preview: `gam csv file.csv gam info user ~email`
3. Execute: `gam csv file.csv gam <actual command>`
4. Verify: Re-run info/print command

```bash
# CSV template for user creation
# users.csv:
# email,firstname,lastname,password,org,phone
# john.doe@domain.com,John,Doe,TempPass123!,/Staff,+1555123456

gam csv users.csv gam create user ~email firstname ~firstname lastname ~lastname password ~password org ~org phone ~phone changepassword on
```

## Troubleshooting

```bash
# Re-authenticate
gam oauth create

# Check service account
gam user admin@domain.com check serviceaccount

# Debug mode
gam config debug true <command>

# API quota errors: wait and retry, or request quota increase in GCP Console
```

## Security Best Practices

See [references/security.md](references/security.md) for comprehensive checklist.

**Critical settings to verify:**
1. MFA enforced for all users, especially admins
2. 2-5 super admins only (not 1, not >5)
3. Separate admin accounts from daily-use accounts
4. External sharing restricted or monitored
5. Less secure apps disabled
6. OAuth app whitelisting enabled
7. Alert center configured

**Questions to ask before any admin change:**
- "Is there an audit trail requirement?"
- "Who approved this change?"
- "Should we test in a sandbox OU first?"
- "What's the rollback plan?"

## Resources

- [GAM7 Wiki](https://github.com/GAM-team/GAM/wiki)
- [GAM Discussion Group](https://groups.google.com/g/google-apps-manager)
- [Google Workspace Admin Help](https://support.google.com/a/)
- [Admin SDK API Reference](https://developers.google.com/admin-sdk)
