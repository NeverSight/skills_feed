---
name: garmin-connect
description: Query Garmin Connect fitness and health data including activities, athlete stats, sleep, heart rate, stress, and body battery. Use when the user asks about Garmin data, workouts, training, or health metrics.
---

# Garmin Connect CLI Skill

Query and manage Garmin Connect data via the `garmin-connect` CLI.

## Prerequisites

- Install CLI: `curl -fsSL https://raw.githubusercontent.com/eddmann/garmin-connect-cli/main/install.sh | sh`
- Authenticate: `garmin-connect auth login` (email/password, supports MFA)

## Quick Context

Get aggregated data in one call:

```bash
garmin-connect context                      # Full context: profile, stats, health, activities
garmin-connect context --activities 10      # More recent activities
garmin-connect context --focus stats,health # Specific sections only
```

## Commands

Run `garmin-connect --help` or `garmin-connect <command> --help` to discover all options.

### Activities

```bash
garmin-connect activities list [--after DATE] [--before DATE] [--limit N] [--type TYPE]
garmin-connect activities get <ID> [--details]
garmin-connect activities splits <ID>
garmin-connect activities download <ID> [--format TCX|GPX|FIT] [-o FILE]
garmin-connect activities upload <FILE>
garmin-connect activities delete <ID> [--force]
```

### Athlete

```bash
garmin-connect athlete              # Profile
garmin-connect athlete stats        # Daily statistics
garmin-connect athlete summary      # Comprehensive stats + body metrics
```

### Health

```bash
garmin-connect health sleep [--date DATE]
garmin-connect health heart-rate [--date DATE]
garmin-connect health steps [--date DATE]
garmin-connect health stress [--date DATE]
garmin-connect health body-battery [--date DATE]
garmin-connect health rhr [--date DATE]
```

### Training

```bash
garmin-connect training status [--date DATE]     # Productive, Peaking, etc.
garmin-connect training readiness [--date DATE]  # Readiness score (0-100)
garmin-connect training vo2max [--date DATE]
garmin-connect training hrv [--date DATE]
garmin-connect training fitness-age
```

### Weight

```bash
garmin-connect weight list [--start DATE] [--end DATE]
garmin-connect weight get [--date DATE]
garmin-connect weight log <WEIGHT_KG> [--date DATE]
```

## Data Units

| Field                     | Unit    |
| ------------------------- | ------- |
| distance                  | meters  |
| duration, movingTime      | seconds |
| averageSpeed, maxSpeed    | m/s     |
| elevation                 | meters  |
| dates                     | ISO8601 |

## Common Patterns

```bash
# Recent activities
garmin-connect activities list --limit 10

# This month's activities
garmin-connect activities list --after 2025-12-01

# Filter with jq
garmin-connect activities list | jq '[.[] | select(.activityType.typeKey=="running")]'

# Total distance
garmin-connect activities list | jq '[.[].distance] | add'
```

## Auth Status

```bash
garmin-connect auth status    # Check if authenticated
garmin-connect auth login     # Login with email/password (supports MFA)
garmin-connect auth logout    # Clear stored tokens
```

## Activity Types

running, cycling, swimming, walking, hiking, trail_running, open_water_swimming, indoor_cycling, virtual_cycling, strength_training, cardio, yoga, pilates, elliptical, indoor_rowing, other

## Exit Codes

- 0 = Success
- 1 = General error
- 2 = Auth error (run `garmin-connect auth login`)
