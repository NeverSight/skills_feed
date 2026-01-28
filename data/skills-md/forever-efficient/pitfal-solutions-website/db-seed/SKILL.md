---
name: db-seed
description: Seed the DynamoDB database with sample data for development and testing. Populates galleries, inquiries, and admin tables. Use when setting up local dev environment or resetting test data. WARNING - never run in production.
---

# Seed Database

Populate DynamoDB tables with sample data for development/testing.

## WARNING
This skill modifies database data. ALWAYS verify the environment before proceeding.

## Pre-checks
1. Verify environment (NEVER run in production!):
   ```bash
   echo "Current AWS Profile: $AWS_PROFILE"
   aws sts get-caller-identity --profile pitfal
   ```

2. Confirm with user before proceeding

## Seed Commands

### Seed All Tables (Recommended Order)
```bash
# 1. Seed admin users and settings first
aws dynamodb batch-write-item \
  --request-items file://scripts/seed-admin.json \
  --profile pitfal

# 2. Seed galleries and images
aws dynamodb batch-write-item \
  --request-items file://scripts/seed-galleries.json \
  --profile pitfal

# 3. Seed sample inquiries
aws dynamodb batch-write-item \
  --request-items file://scripts/seed-inquiries.json \
  --profile pitfal
```

### Seed Individual Tables

#### Admin Users & Settings
```bash
aws dynamodb batch-write-item \
  --request-items file://scripts/seed-admin.json \
  --profile pitfal
```

#### Galleries & Images
```bash
aws dynamodb batch-write-item \
  --request-items file://scripts/seed-galleries.json \
  --profile pitfal
```

#### Inquiries
```bash
aws dynamodb batch-write-item \
  --request-items file://scripts/seed-inquiries.json \
  --profile pitfal
```

## Verify Seeding
```bash
# Count items in galleries table
aws dynamodb scan \
  --table-name pitfal-galleries \
  --select COUNT \
  --profile pitfal

# Count items in inquiries table
aws dynamodb scan \
  --table-name pitfal-inquiries \
  --select COUNT \
  --profile pitfal

# Count items in admin table
aws dynamodb scan \
  --table-name pitfal-admin \
  --select COUNT \
  --profile pitfal
```

## Seed Data Contents

| File | Contents |
|------|----------|
| `seed-admin.json` | Admin user, site settings, services, testimonials, FAQs |
| `seed-galleries.json` | Sample galleries (brand, portrait, event) with images |
| `seed-inquiries.json` | Sample booking inquiries in various statuses |

## Default Admin Credentials
- Username: `admin`
- Password: `admin123` (change immediately in production!)
- Note: Password hash in seed file is bcrypt with cost factor 12

## Clear Data (Development Only)
To remove all seed data:
```bash
# This is destructive - confirm before running
aws dynamodb delete-table --table-name pitfal-galleries --profile pitfal
aws dynamodb delete-table --table-name pitfal-inquiries --profile pitfal
aws dynamodb delete-table --table-name pitfal-admin --profile pitfal
# Then re-run terraform apply to recreate tables
```
