---
name: datetime-info
description: Shows current date and time in multiple formats. Use when you need timestamps, day of week, or formatted dates.
---

# Datetime Info

Displays current date and time in various formats.

## Usage

```bash
python ~/.copilot/skills/datetime-info/datetime_info.py [options]
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--format` | Output format: iso, timestamp, human, all | all |
| `--timezone` | Timezone (e.g., UTC, America/New_York) | local |

## Output

JSON with:
- `iso`: ISO 8601 format (2024-01-15T10:30:00)
- `timestamp`: Unix timestamp
- `human`: Human readable (Monday, January 15, 2024)
- `day_of_week`: Day name
- `time`: Current time HH:MM:SS

## Examples

### Get All Formats
```bash
python ~/.copilot/skills/datetime-info/datetime_info.py
```

### ISO Format Only
```bash
python ~/.copilot/skills/datetime-info/datetime_info.py --format iso
```
