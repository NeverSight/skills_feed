---
name: looker-studio
description: |
  Skill for creating dashboards and calculated fields in Google Looker Studio (formerly Data Studio).
  Use when the user:
  - Needs help with formulas or calculated fields in Looker Studio
  - Wants to connect Looker Studio to PostgreSQL/Supabase
  - Needs to create visualizations or dashboards
  - Asks about function syntax (CASE, IF, DATETIME, etc.)
  - Wants to convert timezones or format dates
  - Needs to blend data from multiple sources
---

# Looker Studio Skill

Complete guide for creating dashboards and calculated fields in Google Looker Studio.

## Main Workflow

1. **Identify the task type:**
   - Create calculated field → See function references
   - Connect database → See `postgresql-connection.md`
   - Create visualization → Follow best practices

2. **For calculated fields:**
   - Determine the function type needed (date, text, aggregation, logic)
   - Check the corresponding reference
   - Test the formula in Looker Studio

## Quick Syntax Reference

### Most Used Functions

```sql
-- Subtract time (e.g., convert UTC to local)
DATETIME_SUB(date_field, INTERVAL 5 HOUR)

-- Simple conditional
IF(condition, value_if_true, value_if_false)

-- Multiple conditions
CASE
  WHEN condition1 THEN result1
  WHEN condition2 THEN result2
  ELSE default_result
END

-- Default value if NULL
IFNULL(field, 'default_value')

-- Aggregations
SUM(field), AVG(field), MAX(field), MIN(field), COUNT(field)

-- Text
CONCAT(text1, text2), UPPER(text), LOWER(text)

-- Format date
FORMAT_DATETIME('%d/%m/%Y %H:%M', date_field)
```

### Common Timezones

| Timezone | Code |
|----------|------|
| US Eastern | `America/New_York` (UTC-5/-4) |
| US Pacific | `America/Los_Angeles` (UTC-8/-7) |
| UK | `Europe/London` (UTC+0/+1) |
| Central Europe | `Europe/Berlin` (UTC+1/+2) |
| Australia Sydney | `Australia/Sydney` (UTC+10/+11) |
| India | `Asia/Kolkata` (UTC+5:30) |
| Japan | `Asia/Tokyo` (UTC+9) |

### Timezone Conversion

```sql
-- Simple method: subtract/add hours
DATETIME_SUB(utc_field, INTERVAL 5 HOUR)

-- With FORMAT for display
FORMAT_DATETIME('%Y-%m-%d %H:%M', DATETIME_SUB(field, INTERVAL 5 HOUR))
```

## PostgreSQL/Supabase Connection

**Recommended configuration:**
- Host: `aws-X-REGION.pooler.supabase.com`
- Port: `5432` or `6543`
- Username: `user.PROJECT_REF`
- SSL: Disabled (if causing certificate issues)

**Limitations:**
- Maximum 150,000 rows per query
- Only `public` schema
- ASCII headers only

## Available References

- `date-functions.md` - DATETIME_ADD, DATETIME_SUB, EXTRACT, FORMAT_DATETIME
- `text-functions.md` - CONCAT, SUBSTR, REPLACE, REGEXP_EXTRACT
- `aggregation-functions.md` - SUM, AVG, COUNT, MAX, MIN, PERCENTILE
- `logic-functions.md` - CASE, IF, IFNULL, COALESCE, operators
- `conversion-functions.md` - CAST, data types
- `postgresql-connection.md` - PostgreSQL/Supabase configuration
- `resources.md` - Courses, tutorials, official documentation

## Best Practices

1. **Data source level calculated fields** for reusability
2. **Use IFNULL** to handle null values
3. **Avoid division by zero** with `NULLIF(divisor, 0)`
4. **Limit data** for better performance
5. **Use filters** before complex aggregations
