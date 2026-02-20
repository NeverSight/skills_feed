---
name: gplay-reports-download
description: Financial and statistics report listing and downloading from Google Play Console via GCS. Use when asked to view, list, or download financial earnings, sales, payouts, or app statistics (installs, ratings, crashes).
---

# Google Play Reports Download

Use this skill when you need to list or download financial reports (earnings, sales, payouts) or statistics reports (installs, ratings, crashes, store performance, subscriptions) from Google Play Console.

## How reports work

Google Play Console reports are **not available via the REST API**. They are stored as CSV/ZIP files in Google Cloud Storage (GCS) buckets:

- **Bucket name**: `pubsite_prod_rev_<developer_id>`
- **Financial reports**: `earnings/`, `sales/`, `payouts/` prefixes
- **Statistics reports**: `stats/installs/`, `stats/ratings/`, `stats/crashes/`, `stats/store_performance/`, `stats/subscriptions/` prefixes

The service account must have access to the GCS bucket (this access is granted automatically when the service account is added to Play Console with appropriate permissions).

## Prerequisites

- A service account configured via `gplay auth login`
- The GCS developer ID (see below — this is **not** the same as the Play Console URL ID)
- For financial reports: `VIEW_FINANCIAL_DATA` permission (service account must be added to Play Console with "View financial data" access)
- For stats reports: `VIEW_APP_INFORMATION` permission (service account must be added to Play Console with "View app information" access)

## Finding your developer ID

> **Important:** The developer ID for reports is **not** the numeric ID in your Play Console URL. The URL ID and the GCS bucket ID are different.

To find the correct developer ID:

1. Go to **Google Play Console** > **Download reports** (in the left sidebar under "Download reports")
2. Look for the **Cloud Storage URI** shown on that page, e.g.:
   ```
   gs://pubsite_prod_rev_12110000881713004121/
   ```
3. The number after `pubsite_prod_rev_` is your developer ID: `12110000881713004121`

Alternatively, use the Google Cloud Console to find the bucket name associated with your Play Console account.

**Common mistake:** Using the developer ID from the Play Console URL (`https://play.google.com/console/developers/<this_id>/...`) will result in a `404 Not Found` error because the GCS bucket uses a different internal ID.

## Financial reports

### List available financial reports

```bash
# List all financial reports
gplay reports financial list --developer <id>

# Filter by type
gplay reports financial list --developer <id> --type earnings
gplay reports financial list --developer <id> --type sales
gplay reports financial list --developer <id> --type payouts

# Filter by date range
gplay reports financial list --developer <id> --from 2026-01 --to 2026-06

# Combine filters
gplay reports financial list --developer <id> --type earnings --from 2026-01 --to 2026-03
```

### Download financial reports

```bash
# Download earnings for a specific month
gplay reports financial download --developer <id> --from 2026-01 --type earnings

# Download to a specific directory
gplay reports financial download --developer <id> --from 2026-01 --type earnings --dir ./reports

# Download a range of months
gplay reports financial download --developer <id> --from 2026-01 --to 2026-06 --type sales
```

### Financial report types

| Type | Description | Filename pattern |
|------|-------------|-----------------|
| `earnings` | Revenue and earnings data | `earnings/earnings_YYYYMM_<id>.zip` |
| `sales` | Sales transaction reports | `sales/salesreport_YYYYMM.zip` |
| `payouts` | Payment disbursement reports | `payouts/payout_YYYYMM.csv` |

## Statistics reports

### List available statistics reports

```bash
# List all stats reports for a developer
gplay reports stats list --developer <id>

# Filter by package name
gplay reports stats list --developer <id> --package com.example.app

# Filter by type
gplay reports stats list --developer <id> --type installs

# Filter by date range and package
gplay reports stats list --developer <id> --package com.example.app --type installs --from 2026-01 --to 2026-06
```

### Download statistics reports

```bash
# Download installs report
gplay reports stats download --developer <id> --package com.example.app --from 2026-01 --type installs

# Download to a specific directory
gplay reports stats download --developer <id> --package com.example.app --from 2026-01 --type crashes --dir ./reports

# Download a range of months
gplay reports stats download --developer <id> --package com.example.app --from 2026-01 --to 2026-06 --type ratings
```

### Statistics report types

| Type | Description | Filename pattern |
|------|-------------|-----------------|
| `installs` | Install/uninstall data | `stats/installs/installs_<pkg>_YYYYMM_overview.csv` |
| `ratings` | Rating distribution | `stats/ratings/ratings_<pkg>_YYYYMM_overview.csv` |
| `crashes` | Crash occurrence data | `stats/crashes/crashes_<pkg>_YYYYMM_overview.csv` |
| `store_performance` | Store listing performance | `stats/store_performance/...` |
| `subscriptions` | Subscription metrics | `stats/subscriptions/...` |

## Flags reference

### Financial commands

| Flag | Required | Description |
|------|----------|-------------|
| `--developer` | Yes | Developer ID |
| `--type` | No (list: default `all`) / Yes (download) | Report type: `earnings`, `sales`, `payouts`, `all` |
| `--from` | No (list) / Yes (download) | Start month `YYYY-MM` |
| `--to` | No | End month `YYYY-MM` (defaults to `--from`) |
| `--dir` | No | Output directory (default `.`) |
| `--output` | No | Output format: `json`, `table`, `markdown` |
| `--pretty` | No | Pretty-print JSON output |

### Stats commands

| Flag | Required | Description |
|------|----------|-------------|
| `--developer` | Yes | Developer ID |
| `--package` | No (list) / Yes (download) | Package name filter |
| `--type` | No (list: default `all`) / Yes (download) | Stats type: `installs`, `ratings`, `crashes`, `store_performance`, `subscriptions`, `all` |
| `--from` | No (list) / Yes (download) | Start month `YYYY-MM` |
| `--to` | No | End month `YYYY-MM` (defaults to `--from`) |
| `--dir` | No | Output directory (default `.`) |
| `--output` | No | Output format: `json`, `table`, `markdown` |
| `--pretty` | No | Pretty-print JSON output |

## Output format

### List output

```json
{
  "developer": "12345",
  "bucket": "pubsite_prod_rev_12345",
  "reports": [
    {"name": "earnings/earnings_202601_12345.zip", "size": 1234, "updated": "2026-02-01T00:00:00Z"}
  ]
}
```

### Download output

```json
{
  "developer": "12345",
  "type": "earnings",
  "from": "2026-01",
  "to": "2026-01",
  "dir": "./reports",
  "files": [
    {"name": "earnings/earnings_202601_12345.zip", "path": "reports/earnings_202601_12345.zip", "size": 1234}
  ]
}
```

## Common workflows

### Monthly financial review

```bash
# List last month's earnings
gplay reports financial list --developer <id> --type earnings --from 2026-01 --output table

# Download all financial reports for Q1
gplay reports financial download --developer <id> --from 2026-01 --to 2026-03 --type earnings --dir ./q1-reports
```

### App performance monitoring

```bash
# Check install trends
gplay reports stats list --developer <id> --package com.example.app --type installs --from 2026-01

# Download crash data for analysis
gplay reports stats download --developer <id> --package com.example.app --from 2026-01 --type crashes --dir ./crash-data
```

### CI/CD automated report collection

```bash
# Download all report types for archival
for type in earnings sales payouts; do
  gplay reports financial download --developer $DEV_ID --from $(date -d "last month" +%Y-%m) --type $type --dir ./monthly-reports
done
```

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `authentication failed` | Service account not configured | Run `gplay auth login --service-account <path>` |
| `403 Forbidden` | No GCS bucket access | Ensure service account is invited in Play Console with appropriate permissions |
| `404 Not Found` | Wrong developer ID or no reports | Use the GCS developer ID from Play Console > Download reports > Cloud Storage URI (not the URL developer ID) |
| Empty reports list | No reports for the date range | Check `--from`/`--to` range; reports may not exist for all months |
