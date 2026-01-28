---
name: gcp-cli-gotchas
description: Use when encountering gcloud or bq CLI formatting errors, quote escaping issues, command substitution problems, or when debugging CLI commands. Provides solutions for backtick usage, heredoc syntax, timestamp filters, parameter escaping, and multiline command formatting.
---

# GCP CLI Formatting Gotchas & Escaping Solutions

Use this skill when you encounter CLI errors, need to debug command formatting, or want to avoid common escaping pitfalls with gcloud and bq commands.

## Common Issues and Solutions

### 1. Command Substitution Breaking

**Problem:** Nested command substitutions with pipes fail
```bash
# ❌ This fails with parse error
bq show PROJECT:DATASET.$(bq ls | tail -n 1 | cut -d',' -f1)
```

**Solution:** Break into steps
```bash
# ✅ Store intermediate result
TABLE=$(bq ls --format=csv PROJECT:DATASET | tail -n 1 | cut -d',' -f1)
bq show --schema PROJECT:DATASET.$TABLE
```

### 2. Quote Escaping in Filters

#### gcloud logging Timestamp Filters

**Must escape quotes:**
```bash
gcloud logging read \
  "timestamp>=\"2024-01-01T00:00:00Z\" AND
   timestamp<=\"2024-01-31T23:59:59Z\""
```

**Or use single quotes (recommended):**
```bash
gcloud logging read \
  'timestamp>="2024-01-01T00:00:00Z" AND
   timestamp<="2024-01-31T23:59:59Z"'
```

**For JSON payloads:**
```bash
# Single quotes outside, double quotes inside
gcloud logging read \
  'resource.type=gce_instance AND
   jsonPayload.message="Error occurred"'
```

### 3. BigQuery Query Formatting

#### Single-line queries (simple)
```bash
bq query --use_legacy_sql=false 'SELECT COUNT(*) FROM `project.dataset.table`'
```

**Quote rules:**
- Use **single quotes** for outer query wrapper
- Use **backticks** for table names with special chars
- Avoids escaping double quotes in SQL

#### Multi-line queries (recommended)

**Use heredoc for complex queries:**
```bash
bq query --use_legacy_sql=false <<'EOF'
SELECT
  customer_id,
  SUM(amount) as total
FROM `project.dataset.orders`
WHERE date >= '2024-01-01'
GROUP BY customer_id
ORDER BY total DESC
LIMIT 10
EOF
```

**Benefits:**
- No quote escaping needed
- Readable multi-line format
- `<<'EOF'` prevents variable expansion

### 4. Table/Dataset Name Formatting

**Three ways to specify:**
```bash
# 1. Fully qualified (safest, works everywhere)
PROJECT_ID:DATASET.TABLE

# 2. With backticks in SQL (required for special chars)
`project-with-dashes.dataset_name.table_name`

# 3. Default project (only when project is set in config)
DATASET.TABLE
```

**When to use backticks:**
- Project ID has dashes: `project-name`
- Dataset/table has special characters
- Inside SQL queries (always safer)

**When NOT to use backticks:**
- In bq CLI arguments: `bq show PROJECT:DATASET.TABLE` (no backticks)

### 5. Parameterized Queries (Avoid Escaping)

```bash
bq query \
  --use_legacy_sql=false \
  --parameter=start_date:DATE:2024-01-01 \
  --parameter=min_amount:FLOAT64:100.0 \
  'SELECT * FROM `table` WHERE date >= @start_date AND amount >= @min_amount'
```

**Benefits:**
- No injection risks
- No complex string escaping
- Clear parameter types

### 6. Multiline Flags

**Correct backslash placement:**
```bash
gcloud run deploy my-function \
  --source . \
  --function myEntryPoint \
  --base-image python313 \
  --region us-central1 \
  --allow-unauthenticated
```

**Rules:**
- Backslash must be LAST character on line
- No spaces after backslash
- Indentation on next line doesn't matter

### 7. Multiple Flags

**Works (can repeat):**
```bash
bq query \
  --parameter=name1:TYPE:value1 \
  --parameter=name2:TYPE:value2 \
  --parameter=name3:TYPE:value3 \
  'SELECT...'
```

**Doesn't work (single value only):**
```bash
# ❌ Second --role is ignored
gcloud projects add-iam-policy-binding PROJECT \
  --member=user:email \
  --role=roles/viewer \
  --role=roles/editor

# ✅ Run multiple commands
gcloud projects add-iam-policy-binding PROJECT --member=user:email --role=roles/viewer
gcloud projects add-iam-policy-binding PROJECT --member=user:email --role=roles/editor
```

### 8. Format Flag Usage

**Supported formats:**
```bash
# JSON output (most commands)
gcloud projects list --format=json

# Pretty JSON (bq)
bq show --format=prettyjson PROJECT:DATASET.TABLE

# CSV (some commands)
bq ls --format=csv PROJECT:DATASET

# Value extraction (gcloud)
gcloud config get-value project
```

**Gotcha:** Not all commands support all formats. Check `--help` first.

### 9. Debugging Commands

**Verbose output:**
```bash
# See detailed execution
gcloud --verbosity=debug COMMAND

# See API calls
gcloud --log-http COMMAND
```

**Dry run (bq only):**
```bash
# Validate without executing
bq query --dry_run 'SELECT...'
bq load --dry_run ...
```

**Test incrementally:**
```bash
# Start simple
bq query 'SELECT 1'

# Add complexity
bq query 'SELECT * FROM `project.dataset.table` LIMIT 1'

# Add filters
bq query 'SELECT * FROM `project.dataset.table` WHERE condition LIMIT 1'
```

### 10. Special Cases

**Transfer config needs location:**
```bash
# ❌ Fails - needs location
bq ls --transfer_config --project_id=PROJECT

# ✅ Works
bq ls --transfer_config --project_id=PROJECT --transfer_location=us
```

**CSV with newlines:**
```bash
bq load \
  --source_format=CSV \
  --allow_quoted_newlines \
  --skip_leading_rows=1 \
  dataset.table \
  gs://bucket/file.csv
```

## Quick Reference: Best Practices

1. **Use single quotes for outer query wrappers** (less escaping)
2. **Use backticks for table references in SQL**
3. **Use heredoc for complex multi-line queries**
4. **Break complex command substitutions into steps**
5. **Test with --dry_run when available**
6. **Use --format flags to get parseable output**
7. **Check --help for command-specific gotchas**
8. **Start simple, add complexity incrementally**
9. **Save complex commands as scripts**
10. **Use variables for reusable values** (PROJECT_ID, DATASET, etc.)

## When Dependencies Fail

If a command requires a flag you don't have, read the error message carefully. Many commands have dependency flags that must be set together:
- `--transfer_config` requires `--transfer_location`
- Some `--format` options only work with specific commands
- Region/zone flags may be required based on resource type
