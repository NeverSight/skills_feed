---
name: fastf1
description: |
  Formula 1 data — race schedules, results, lap timing, driver and team info. Powered by the FastF1 library. Covers F1 sessions, qualifying, practice, race results, sector times, tire strategy.

  Use when: user asks about F1 race results, qualifying, lap times, driver stats, team info, the F1 calendar, or Formula 1 data.
  Don't use when: user asks about other motorsports (MotoGP, NASCAR, IndyCar, WEC, Formula E). Don't use for F1 betting odds or predictions — use kalshi or polymarket instead. Don't use for F1 news articles — use sports-news instead.
license: MIT
compatibility: Requires Python 3.10+ with fastf1 and pandas (pip install sports-skills[f1])
metadata:
  author: machina-sports
  version: "0.1.0"
---

# FastF1 — Formula 1 Data

## Setup

F1 requires extra dependencies (fastf1 + pandas). Install with:
```bash
which sports-skills || pip install sports-skills[f1]
```
If already installed without F1 support, add the extra:
```bash
pip install sports-skills[f1]
```
If `pip install` fails with a Python version error, the package requires Python 3.10+. Find a compatible Python:
```bash
python3 --version  # check version
# If < 3.10, try: python3.12 -m pip install sports-skills[f1]
# On macOS with Homebrew: /opt/homebrew/bin/python3.12 -m pip install sports-skills[f1]
```
No API keys required.

## Quick Start

Prefer the CLI — it avoids Python import path issues:
```bash
sports-skills f1 get_race_schedule --year=2025
sports-skills f1 get_race_results --year=2025 --event=Monza
```

Python SDK (alternative):
```python
from sports_skills import f1

schedule = f1.get_race_schedule(year=2025)
results = f1.get_race_results(year=2025, event="Monza")
```

## Choosing the Year

Derive the current year from the system prompt's date (e.g., `currentDate: 2026-02-16` → current year is 2026).

- **If the user specifies a year**, use it as-is.
- **If the user says "latest", "recent", "last season", or doesn't specify a year**: The F1 season runs roughly March–December. If the current month is January or February (i.e., before the new season starts), use `year = current_year - 1` since that's the most recent completed season. From March onward, use the current year — races will have started or be imminent.
- **Never hardcode a year.** Always derive it from the system date.

## Commands

### get_race_schedule
Get race schedule for a season.
- `year` (int, required): Season year

### get_race_results
Get race results (positions, times, points).
- `year` (int, required): Season year
- `event` (str, required): Event name (e.g., "Monza", "Silverstone")

### get_session_data
Get detailed session data (qualifying, race, practice).
- `session_year` (int, required): Year
- `session_name` (str, required): Event name
- `session_type` (str, optional): "Q" (qualifying), "R" (race), "FP1", etc. Default: "Q"

### get_driver_info
Get driver information for a season.
- `year` (int, required): Season year
- `driver` (str, optional): Driver code or name. Omit for all drivers.

### get_team_info
Get team information for a season.
- `year` (int, required): Season year
- `team` (str, optional): Team name. Omit for all teams.

### get_lap_data
Get lap-by-lap timing data.
- `year` (int, required): Season year
- `event` (str, required): Event name
- `session_type` (str, optional): Session type. Default: "R"
- `driver` (str, optional): Driver code. Omit for all drivers.

### get_pit_stops
Get pit stop durations (PitIn → PitOut) for a race or full season.
- `year` (int, required): Season year
- `event` (str, optional): Event name. Omit for full season.
- `driver` (str, optional): Driver code. Omit for all drivers.

### get_speed_data
Get speed trap and intermediate speed data for a race or full season.
- `year` (int, required): Season year
- `event` (str, optional): Event name. Omit for full season.
- `driver` (str, optional): Driver code. Omit for all drivers.

### get_championship_standings
Get driver and constructor championship standings aggregated from all race results.
- `year` (int, required): Season year

### get_season_stats
Get aggregated season stats: fastest laps, top speeds, points, wins, podiums per driver/team.
- `year` (int, required): Season year

### get_team_comparison
Compare two teams head-to-head: qualifying, race pace, sectors, points.
- `year` (int, required): Season year
- `team1` (str, required): First team name (e.g., "Red Bull")
- `team2` (str, required): Second team name (e.g., "McLaren")
- `event` (str, optional): Event name. Omit for full season.

### get_teammate_comparison
Compare teammates within the same team: qualifying H2H, race H2H, pace delta.
- `year` (int, required): Season year
- `team` (str, required): Team name (e.g., "McLaren")
- `event` (str, optional): Event name. Omit for full season.

### get_tire_analysis
Tire strategy and degradation analysis: compound usage, stint lengths, degradation rates.
- `year` (int, required): Season year
- `event` (str, optional): Event name. Omit for full season.
- `driver` (str, optional): Driver code. Omit for all drivers.

## Examples

In these examples, `{year}` means the year derived using the rules in "Choosing the Year" above.

User: "Show me the F1 calendar"
1. Call `get_race_schedule(year={year})`
2. Present schedule with event names, dates, and circuits

User: "How did Verstappen do at Monza?"
1. Derive the year (if unspecified, use the latest completed season per the rules above)
2. Call `get_race_results(year={year}, event="Monza")` for final classification
3. Call `get_lap_data(year={year}, event="Monza", session_type="R", driver="VER")` for lap times
4. Present finishing position, gap to leader, fastest lap, and tire strategy

User: "Compare qualifying times at Silverstone"
1. Derive the year
2. Call `get_session_data(session_year={year}, session_name="Silverstone", session_type="Q")`
3. Call `get_lap_data(year={year}, event="Silverstone", session_type="Q")` for all drivers
4. Present Q1/Q2/Q3 times sorted by position

User: "What were the latest F1 results?" (asked in February 2026)
1. Current month is February → season hasn't started → use `year = 2025`
2. Call `get_race_schedule(year=2025)` to find the last event of that season
3. Call `get_race_results(year=2025, event=<last_event>)` for the final race results
4. Present the results

## Error Handling

When a command fails (wrong event name, no data for that session, network error, etc.), **do not surface the raw error to the user**. Instead:

1. **Catch it silently** — treat the failure as an exploratory miss, not a fatal error.
2. **Try alternatives** — e.g., if an event name doesn't match, call `get_race_schedule()` first to find the correct name, then retry. If a session type has no data, try a different session type.
3. **Only report failure after exhausting alternatives** — and when you do, give a clean human-readable message (e.g., "No qualifying data is available for that event yet"), not a traceback or raw CLI output.

This is especially important when the agent is responding through messaging platforms (Telegram, Slack, etc.) where raw exec failures look broken.

## Common Mistakes

**These are the ONLY valid commands.** Do not invent or guess command names:
- `get_race_schedule`
- `get_race_results`
- `get_session_data`
- `get_driver_info`
- `get_team_info`
- `get_lap_data`
- `get_pit_stops`
- `get_speed_data`
- `get_championship_standings`
- `get_season_stats`
- `get_team_comparison`
- `get_teammate_comparison`
- `get_tire_analysis`

**Commands that DO NOT exist** (commonly hallucinated):
- ~~`get_driver_results`~~ — use `get_race_results` and filter by driver, or use `get_lap_data` with the `driver` parameter.
- ~~`get_standings`~~ — use `get_championship_standings`.
- ~~`get_fastest_laps`~~ — use `get_lap_data` and find the minimum `lap_time`, or use `get_season_stats` for season-wide fastest laps.
- ~~`get_tire_strategy`~~ — use `get_tire_analysis` for full tire strategy and degradation data.
- ~~`get_circuit_info`~~ — circuit details are included in `get_race_schedule` output.

If you're unsure whether a command exists, check this list. Do not try commands that aren't listed above.

## Troubleshooting

- **`sports-skills` command not found**: Package not installed. Run `pip install sports-skills[f1]`. If pip fails with a Python version error, you need Python 3.10+ — see Setup section.
- **`ModuleNotFoundError: No module named 'sports_skills'`**: Same as above — install the package. Prefer the CLI over Python imports to avoid path issues.
- **ImportError on `from sports_skills import f1`**: F1 module requires extra dependencies beyond the base package. Run `pip install sports-skills[f1]` to add fastf1 + pandas.
- **No data for future events**: FastF1 only returns data for completed sessions. Future races appear in the schedule but have no session data.
- **Slow first request**: FastF1 downloads and caches session data locally. First call for a given session may take 10-30 seconds. Subsequent calls are fast.
- **Event name not found**: Use the exact event name from `get_race_schedule()`. Common circuit names like "Monza" or "Silverstone" usually work as aliases.
- **`fastest_lap` false / `fastest_lap_time` empty in race results**: FastF1 doesn't always populate these fields. To find the actual fastest lap, use `get_lap_data()` and find the minimum `lap_time` across all drivers.
