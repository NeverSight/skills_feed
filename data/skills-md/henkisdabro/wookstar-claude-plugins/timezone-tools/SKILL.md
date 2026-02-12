---
name: timezone-tools
description: Get current time in any timezone and convert times between timezones. Use when working with time, dates, timezones, scheduling across regions, or when user mentions specific cities/regions for time queries. Supports IANA timezone names.
---

# Timezone Tools

Get current time in any timezone and convert times between different timezones using IANA timezone database.

## Quick Start

### Get current time in a timezone

```bash
python scripts/get_time.py" "America/New_York"
```

### Convert time between timezones

```bash
python scripts/convert_time.py" "America/New_York" "14:30" "Australia/Perth"
```

### Search for timezone names

```bash
python scripts/list_timezones.py" "perth"
```

## Instructions

When the user asks about time or timezones:

1. **For current time queries** (e.g., "What time is it in Tokyo?"):
   - Use `scripts/get_time.py` with IANA timezone name
   - If unsure of timezone name, search first with `list_timezones.py`
   - Script outputs: timezone, datetime, day of week, DST status

2. **For time conversions** (e.g., "What's 2pm EST in Perth time?"):
   - Use `scripts/convert_time.py` with source timezone, time (HH:MM 24-hour), target timezone
   - Script shows source time, target time, and time difference
   - Automatically handles DST changes

3. **For timezone searches**:
   - Use `scripts/list_timezones.py` with city/country name
   - Returns matching IANA timezone names

## Common Timezones Reference

For quick reference, see [data/common_timezones.json](data/common_timezones.json) which includes major cities worldwide, with Perth prominently featured.

**User's local timezone**: The scripts automatically detect your local timezone using `tzlocal`.

## Examples

### Example 1: Current time query

User: "What time is it in Perth?"

```bash
python scripts/list_timezones.py" "perth"
# Output: Australia/Perth

python scripts/get_time.py" "Australia/Perth"
# Output:
# Timezone: Australia/Perth
# Current time: 2025-11-07T15:30:45
# Day: Thursday
# DST: No
```

### Example 2: Time conversion

User: "I have a meeting at 2pm New York time, what time is that in Perth?"

```bash
python scripts/convert_time.py" "America/New_York" "14:00" "Australia/Perth"
# Output:
# Source: America/New_York - 2025-11-07T14:00:00 (Thursday, DST: No)
# Target: Australia/Perth - 2025-11-08T03:00:00 (Friday, DST: No)
# Time difference: +13.0h
```

### Example 3: Multiple timezone search

User: "What are the timezone codes for London, Tokyo, and Sydney?"

```bash
python scripts/list_timezones.py" "london"
python scripts/list_timezones.py" "tokyo"
python scripts/list_timezones.py" "sydney"
# Outputs:
# Europe/London
# Asia/Tokyo
# Australia/Sydney
```

## Time Format

- All times use **24-hour format** (HH:MM): `14:30` not `2:30 PM`
- ISO 8601 datetime format for output: `2025-11-07T14:30:45`
- IANA timezone names (e.g., `America/New_York`, not `EST`)

## Troubleshooting

### "Invalid timezone" error

- Use IANA timezone names: `America/New_York` not `EST` or `Eastern`
- Search with `list_timezones.py` if unsure
- Check [data/common_timezones.json](data/common_timezones.json) for reference

### "Invalid time format" error

- Use 24-hour format: `14:30` not `2:30 PM`
- Format must be `HH:MM` with colon separator

### Missing dependencies

Install required Python packages:

```bash
pip install tzlocal
```

## Dependencies

- Python 3.9+
- `tzlocal>=5.0` - for local timezone detection
- `zoneinfo` - built-in Python 3.9+ (IANA timezone database)

## Notes

- Scripts automatically handle Daylight Saving Time (DST)
- Local timezone is auto-detected from system
- All timezone data uses IANA Time Zone Database
- Perth, Australia timezone: `Australia/Perth` (UTC+8, no DST)
