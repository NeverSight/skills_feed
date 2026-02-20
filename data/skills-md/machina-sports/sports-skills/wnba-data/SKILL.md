---
name: wnba-data
description: |
  WNBA data via ESPN public endpoints — scores, standings, rosters, schedules, game summaries, statistical leaders, and news. Zero config, no API keys.

  Use when: user asks about WNBA scores, standings, team rosters, schedules, game stats, box scores, or WNBA news.
  Don't use when: user asks about NBA (use nba-data), men's basketball, college basketball, or other sports. Don't use for live play-by-play — data updates post-play.
license: MIT
metadata:
  author: machina-sports
  version: "0.1.0"
---

# WNBA Data

## Setup

Before first use, check if the CLI is available:
```bash
which sports-skills || pip install sports-skills
```
If `pip install` fails with a Python version error, the package requires Python 3.10+. Find a compatible Python:
```bash
python3 --version  # check version
# If < 3.10, try: python3.12 -m pip install sports-skills
# On macOS with Homebrew: /opt/homebrew/bin/python3.12 -m pip install sports-skills
```
No API keys required.

## Quick Start

Prefer the CLI — it avoids Python import path issues:
```bash
sports-skills wnba get_scoreboard
sports-skills wnba get_standings --season=2025
sports-skills wnba get_teams
```

## Choosing the Season

Derive the current year from the system prompt's date (e.g., `currentDate: 2026-02-18` → current year is 2026).

- **If the user specifies a season**, use it as-is.
- **If the user says "current", "this season", or doesn't specify**: The WNBA season runs May–October. If the current month is May–October, use `season = current_year`. If November–April (offseason), use `season = current_year - 1` (most recently completed season).
- **Never hardcode a season.** Always derive it from the system date.

## Commands

### get_scoreboard
Get live/recent WNBA scores.
- `date` (str, optional): Date in YYYY-MM-DD format. Defaults to today.

Returns `events[]` with game info, scores, status, and competitors.

### get_standings
Get WNBA standings by conference.
- `season` (int, optional): Season year

Returns `groups[]` with Eastern/Western conferences and team standings including W-L, PCT, GB, and streak.

### get_teams
Get all WNBA teams. No parameters.

Returns `teams[]` with id, name, abbreviation, logo, and location.

### get_team_roster
Get full roster for a team.
- `team_id` (str, required): ESPN team ID (e.g., "5" for Las Vegas Aces)

Returns `athletes[]` with name, position, jersey number, height, weight, experience.

### get_team_schedule
Get schedule for a specific team.
- `team_id` (str, required): ESPN team ID
- `season` (int, optional): Season year

Returns `events[]` with opponent, date, score (if played), and venue.

### get_game_summary
Get detailed box score and scoring plays.
- `event_id` (str, required): ESPN event ID

Returns `game_info`, `competitors`, `boxscore` (stats per player), `scoring_plays`, and `leaders`.

### get_leaders
Get WNBA statistical leaders (points, rebounds, assists, etc.).
- `season` (int, optional): Season year. Defaults to most recently completed season.

Returns `categories[]` with leader rankings per stat category.

### get_news
Get WNBA news articles.
- `team_id` (str, optional): Filter by team

Returns `articles[]` with headline, description, published date, and link.

### get_schedule
Get WNBA schedule for a specific date or season.
- `date` (str, optional): Date in YYYY-MM-DD format
- `season` (int, optional): Season year (used only if no date provided)

Returns `events[]` for the specified date.

## Team IDs (Common)

| Team | ID |
|------|----|
| Atlanta Dream | 3 |
| Chicago Sky | 4 |
| Connecticut Sun | 6 |
| Dallas Wings | 8 |
| Indiana Fever | 5 |
| Las Vegas Aces | 9 |
| Los Angeles Sparks | 14 |
| Minnesota Lynx | 16 |
| New York Liberty | 17 |
| Phoenix Mercury | 21 |
| Seattle Storm | 26 |
| Washington Mystics | 30 |

## Examples

**User: "What are today's WNBA scores?"**
```bash
sports-skills wnba get_scoreboard
```

**User: "Show me the WNBA standings"**
```bash
sports-skills wnba get_standings --season=2025
```

**User: "Who's on the Indiana Fever roster?"**
```bash
sports-skills wnba get_team_roster --team_id=5
```

**User: "Show me WNBA statistical leaders"**
```bash
sports-skills wnba get_leaders --season=2025
```

## Error Handling

When a command fails, **do not surface raw errors to the user**. Instead:
1. Catch silently and try alternatives
2. If team name given instead of ID, use `get_teams` to find the ID first
3. Only report failure with a clean message after exhausting alternatives

## Troubleshooting

- **`sports-skills` command not found**: Run `pip install sports-skills`
- **Team not found**: Use `get_teams` to list all teams and find the correct ID
- **No data for future games**: ESPN only returns data for completed or in-progress games
- **Offseason (Nov–Apr)**: `get_scoreboard` returns 0 events — expected. Use `get_standings --season=2025` or `get_news` instead.
