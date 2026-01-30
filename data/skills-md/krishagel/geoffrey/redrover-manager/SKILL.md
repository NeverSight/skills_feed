---
name: redrover-manager
description: Access Red Rover absence management data for PSD staff attendance tracking and reporting
triggers:
  - "redrover"
  - "red rover"
  - "absences"
  - "staff attendance"
  - "teacher absences"
  - "substitute"
  - "sub coverage"
  - "unfilled positions"
allowed-tools: Read, Bash
version: 0.1.0
---

# Red Rover Manager Skill

## Overview

Red Rover is an absence management system used by PSD to track staff absences and substitute coverage. This skill provides access to absence data for reporting and analysis.

## Configuration

- **Base URL**: `https://connect.redroverk12.com/`
- **Org ID**: 1305 (Peninsula School District)
- **Authentication**: HTTP Basic Auth + API Key header
- **Credentials**: Stored in 1Password as "RedRover"
- **Rate Limit**: 100 requests/minute

## Authentication

All requests require both:
1. `Authorization: Basic [base64(username:password)]` header
2. `apiKey: [key]` header (obtained from organization endpoint)

The organization endpoint returns a dynamic API key that should be used for subsequent requests.

## Scripts

All scripts are in `skills/redrover-manager/scripts/`. Run with `bun`:

### get_organization.js
Fetch organization info and validate credentials.

```bash
bun get_organization.js
```

Returns: Organization ID, name, and API key.

### get_absences.js
Fetch raw absence/vacancy data for a date range.

```bash
bun get_absences.js <start_date> <end_date> [filled|unfilled|all]
```

Examples:
```bash
bun get_absences.js 2026-01-20 2026-01-27
bun get_absences.js 2026-01-27 2026-01-27 unfilled
```

**Note:** Max date range is 31 days.

### get_daily_summary.js
Get daily absence summary (all staff) with counts by school, reason, and fill status.

```bash
bun get_daily_summary.js [date]
```

Date options:
- `today` (default)
- `yesterday`
- Day names: `monday`, `tuesday`, etc.
- `last wednesday`, `last friday`
- Specific date: `2026-01-27`

### get_certificated_summary.js
Get daily absence summary for **certificated staff only** (Teachers, ESA, CTE).

```bash
bun get_certificated_summary.js [date]
```

Same date options as above. This is the most commonly requested report - focuses on classroom coverage.

### get_weekly_summary.js
Get weekly trends and patterns.

```bash
bun get_weekly_summary.js [weeks_ago]
```

Options:
- `0` = this week (default)
- `1` = last week
- `2` = two weeks ago

## API Endpoints Used

### Organization
```
GET /api/v1/organization
Security: Basic Auth
Returns: Array with org info including dynamic apiKey
```

### Vacancy Details (Primary data endpoint)
```
GET /api/v1/{orgId}/Vacancy/details
Security: Basic Auth + apiKey header
Query Params:
  - fromDate: datetime (required)
  - toDate: datetime (required)
  - filled: boolean (optional - filter filled/unfilled)
  - pageSize: int (default 10, max 100)
  - page: int (default 1)
Returns: Paginated vacancy/absence data
```

## Common Workflows

### "How many absences yesterday?"
```bash
bun get_daily_summary.js yesterday
```

### "Show unfilled positions for today"
```bash
bun get_daily_summary.js today
# Look at unfilled_positions array in output
```

### "Weekly absence trends"
```bash
bun get_weekly_summary.js
```

### "Last week's summary"
```bash
bun get_weekly_summary.js 1
```

## Output Format

### Daily Summary
```json
{
  "date": "yesterday",
  "date_iso": "2026-01-26",
  "total_absences": 110,
  "filled": 75,
  "unfilled": 35,
  "fill_rate": 68,
  "by_school": {
    "PENINSULA HIGH SCHOOL": 13,
    "GIG HARBOR HIGH SCHOOL": 10
  },
  "by_reason": {
    "SICK LV > 1 SICK": 54,
    "OTH PAID LV > PERSONAL": 15
  },
  "by_position_type": {
    "Teacher": 55,
    "Paraprofessional": 36
  },
  "unfilled_positions": [
    {
      "school": "PENINSULA HIGH SCHOOL",
      "position": "MATH",
      "employee": "JANE DOE",
      "start": "2026-01-26T07:00:00",
      "end": "2026-01-26T14:30:00"
    }
  ]
}
```

### Weekly Summary
```json
{
  "week": "Jan 20-24, 2026",
  "week_label": "this week",
  "total_absences": 450,
  "daily_average": 90,
  "filled": 380,
  "unfilled": 70,
  "fill_rate": 84,
  "peak_day": { "day": "Monday", "count": 120 },
  "slow_day": { "day": "Friday", "count": 65 },
  "by_day": {
    "Monday": 120,
    "Tuesday": 95,
    "Wednesday": 90,
    "Thursday": 80,
    "Friday": 65
  },
  "trends": [
    { "type": "info", "message": "Monday had 120 absences (50%+ above average)" }
  ]
}
```

## Data Fields

Key fields in vacancy data:
- `absenceDetail.employee` - Employee who is absent
- `absenceDetail.reasons[0].name` - Reason category (SICK, PERSONAL, etc.)
- `location.name` - School name
- `position.title` - Position title
- `position.positionType.name` - Position category (Teacher, Paraprofessional, etc.)
- `substitute` - If present, position is filled
- `start` / `end` - Absence time range
- `needsReplacement` - Whether sub is required

## Schools in PSD

Common school names in data:
- PENINSULA HIGH SCHOOL
- GIG HARBOR HIGH SCHOOL
- HENDERSON BAY HIGH SCHOOL
- GOODMAN MIDDLE SCHOOL
- HARBOR RIDGE MIDDLE SCHOOL
- KEY PENINSULA MIDDLE SCHOOL
- KOPACHUCK MIDDLE SCHOOL
- ARTONDALE ELEMENTARY SCHOOL
- DISCOVERY ELEMENTARY SCHOOL
- EVERGREEN ELEMENTARY SCHOOL
- HARBOR HEIGHTS ELEMENTARY SCHOOL
- MINTER CREEK ELEMENTARY SCHOOL
- PIONEER ELEMENTARY SCHOOL
- PURDY ELEMENTARY SCHOOL
- SWIFT WATER ELEMENTARY SCHOOL
- VAUGHN ELEMENTARY SCHOOL
- VOYAGER ELEMENTARY SCHOOL
