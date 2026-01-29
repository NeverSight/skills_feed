---
name: wprdc
description: Query Pittsburgh's Western PA Regional Data Center (WPRDC) — 363+ datasets covering property assessments, air quality, 311 requests, jail census, overdose data, permits, violations, and more. Run SQL queries against live tables without downloading. Use when user asks about Pittsburgh/Allegheny County public data, property lookups, civic data, or regional statistics.
version: 1.1.0
homepage: https://data.wprdc.org
metadata:
  emoji: 📊
  tags:
    - pittsburgh
    - civic-data
    - wprdc
    - ckan
    - property
    - public-data
    - allegheny-county
---

# WPRDC - Pittsburgh Regional Data Center

Query 363+ datasets from the Western PA Regional Data Center. Property assessments, air quality, 311 requests, jail census, overdose data, parking, permits, violations — all queryable via SQL without downloading.

## Quick Start

```bash
# Search for datasets
<skill>/wprdc.py search "property sales"
<skill>/wprdc.py search "air quality" --org allegheny-county

# Get dataset info
<skill>/wprdc.py info property-assessments

# List resources (tables) in a dataset
<skill>/wprdc.py resources property-assessments

# See field schema
<skill>/wprdc.py fields assessments

# SQL query (the killer feature!)
<skill>/wprdc.py query 'SELECT "PARID", "PROPERTYADDRESS" FROM @assessments WHERE "PROPERTYCITY"='"'"'PITTSBURGH'"'"' LIMIT 5'

# Quick parcel lookup
<skill>/wprdc.py parcel 0028F00194000000

# Download a dataset
<skill>/wprdc.py download property-assessments --format csv
```

## Commands

### `search <query>`
Search for datasets by keyword.

Options:
- `--org <name>` — Filter by organization (e.g., `allegheny-county`, `city-of-pittsburgh`)
- `--group <name>` — Filter by topic group (e.g., `health`, `housing-properties`)
- `--limit <n>` — Max results (default: 10)
- `--json` — Raw JSON output

### `info <dataset>`
Get detailed information about a dataset, including description, resources, and metadata.

### `resources <dataset>`
List all resources (tables/files) in a dataset with their IDs and queryability status.

### `fields <resource>`
Show the field schema for a resource. Use shortcut names or resource IDs.

### `query <sql>`
Execute SQL queries against live data. **This is the power feature!**

**Important:** Column names must be double-quoted because PostgreSQL is case-sensitive:
```sql
SELECT "PARID", "PROPERTYADDRESS" FROM @assessments WHERE "PROPERTYCITY"='PITTSBURGH' LIMIT 5
```

Use `@shortcut` notation for common tables (see Shortcuts below).

Options:
- `--json` — Raw JSON output
- `--table` — Format as ASCII table

### `parcel <pin>`
Quick property lookup by parcel ID. Returns address, assessments, building info, and last sale.

```bash
<skill>/wprdc.py parcel 0028F00194000000
```

### `download <dataset>`
Download a resource to a file.

Options:
- `--resource <id|name>` — Specific resource
- `--format <csv|json|geojson>` — Preferred format
- `--output <path>` — Output filename

### `orgs`
List all organizations publishing data.

### `groups`
List all topic groups (categories).

### `shortcuts`
Show available query shortcuts.

## Query Shortcuts

Use `@shortcut` in SQL queries instead of long resource IDs:

| Shortcut | Dataset |
|----------|---------|
| `@assessments` | Property Assessments (584K parcels) |
| `@sales` | Property Sales |
| `@311` | 311 Service Requests |
| `@permits` | PLI Permits |
| `@violations` | PLI Violations |
| `@overdoses` | Fatal Accidental Overdoses |
| `@jail` | Jail Daily Census |
| `@air-quality` | Air Quality |
| `@fishfry` | Fish Fry Map |

Example:
```bash
<skill>/wprdc.py query 'SELECT * FROM @overdoses WHERE "death_year"=2024 LIMIT 10'
```

## Before Querying, Ask Yourself

1. **Scope**: Is this City of Pittsburgh only, or all of Allegheny County?
   - PLI violations, 311, permits → **City of Pittsburgh only** (90 neighborhoods)
   - Property assessments, overdoses, jail → **All of Allegheny County** (130 municipalities)

2. **Freshness**: When was this dataset last updated? Run `info <dataset>` first.

3. **Fields**: What columns exist? Run `fields <resource>` before writing SQL.

4. **Size**: How many records? Start with `LIMIT 10`, expand once you know it works.

## NEVER Do

- **NEVER use CAST(), ROUND(), AVG(), or other SQL functions** — WPRDC blocks them. You'll get "Access denied: Not authorized to call function". Do aggregation client-side.

- **NEVER query without LIMIT on large tables** — Assessments has 584K rows. Queries timeout. Always add `LIMIT`.

- **NEVER assume county-wide coverage for City datasets** — PLI violations, 311, permits are **City of Pittsburgh only**. Aspinwall, Fox Chapel, Mt. Lebanon = separate municipalities, not in the data.

- **NEVER trust "under maintenance" datasets** — County plumbing inspections, housing inspections, food facilities are currently broken. Check `info` first.

- **NEVER forget column quoting** — UPPERCASE columns need double quotes (`"PARID"`), lowercase don't (`case_year`). Wrong quoting = cryptic "column does not exist" errors.

- **NEVER use wildcards on unindexed text** — `LIKE '%something%'` on large tables will timeout. Be specific.

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `409 CONFLICT` + "column does not exist" | Unquoted uppercase column | Add quotes: `"PARID"` not `PARID` |
| `Access denied: Not authorized to call function` | Used CAST/ROUND/AVG | Remove function, process client-side |
| Timeout / no response | Query too large | Add `LIMIT`, narrow `WHERE` clause |
| Empty results | Filter mismatch | Check exact string values with a broad query first |
| "resource not found" | Wrong resource ID | Use `resources <dataset>` to get correct ID |

## SQL Tips

1. **Quote UPPERCASE column names** — PostgreSQL is case-sensitive:
   ```sql
   SELECT "PROPERTYADDRESS" FROM @assessments  -- ✓ uppercase needs quotes
   SELECT case_year FROM @overdoses            -- ✓ lowercase works without quotes
   ```

2. **GROUP BY works**, but not aggregate functions:
   ```sql
   SELECT "PROPERTYCITY", COUNT(*) as cnt 
   FROM @assessments 
   GROUP BY "PROPERTYCITY" 
   ORDER BY cnt DESC 
   LIMIT 10
   ```

3. **Check fields first** — Column names vary wildly between datasets

## Coverage Map (Critical!)

| Dataset | Coverage | Municipalities |
|---------|----------|----------------|
| Property Assessments | **All Allegheny County** | 130 municipalities |
| Property Sales | **All Allegheny County** | 130 municipalities |
| Fatal Overdoses | **All Allegheny County** | By zip code |
| Jail Census | **All Allegheny County** | County facility |
| 911 Dispatches | **Most of county** | 111 of 130 municipalities |
| Air Quality | **All Allegheny County** | Monitor locations |
| PLI Violations | **City of Pittsburgh ONLY** | 90 neighborhoods |
| PLI Permits | **City of Pittsburgh ONLY** | 90 neighborhoods |
| 311 Requests | **City of Pittsburgh ONLY** | 90 neighborhoods |

**If someone asks about Fox Chapel, Aspinwall, Mt. Lebanon, etc.** → Only county-wide datasets apply. No PLI/311 data for suburbs.

## Organizations & Topics

Use `orgs` and `groups` commands to explore. Major publishers:
- **allegheny-county** (143 datasets) — assessments, health, jail
- **city-of-pittsburgh** (126 datasets) — 311, permits, violations

## Example Queries

```bash
# Property lookup by parcel ID
<skill>/wprdc.py parcel 0028F00194000000

# Search by address (use SQL)
<skill>/wprdc.py query 'SELECT * FROM @assessments WHERE "PROPERTYHOUSENUM"='"'"'251'"'"' AND "PROPERTYADDRESS" LIKE '"'"'%PASADENA%'"'"''

# Overdose trends by year
<skill>/wprdc.py query 'SELECT case_year, COUNT(*) as deaths FROM @overdoses GROUP BY case_year ORDER BY case_year'

# Filter by neighborhood (City of Pittsburgh only)
<skill>/wprdc.py query 'SELECT "VIOLATION", COUNT(*) FROM @violations WHERE "NEIGHBORHOOD"='"'"'Hazelwood'"'"' GROUP BY "VIOLATION" ORDER BY COUNT(*) DESC LIMIT 10'

# Cross-tab query
<skill>/wprdc.py query 'SELECT combined_od1, race, COUNT(*) FROM @overdoses GROUP BY combined_od1, race ORDER BY COUNT(*) DESC LIMIT 20'
```

## Known Issues (as of Jan 2026)

- **311 Data** stopped updating Feb 2025 — new system transition
- **County Plumbing Inspections** — under maintenance
- **County Housing Inspections** — under maintenance  
- **County Food Facilities** — under maintenance

Always run `info <dataset>` to check last update date before relying on data.
