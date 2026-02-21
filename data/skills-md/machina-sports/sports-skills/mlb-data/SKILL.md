---
name: mlb-data
description: |
  MLB data via ESPN public endpoints — scores, standings, rosters, schedules, game summaries, statistical leaders, and news. Zero config, no API keys.

  Use when: user asks about MLB scores, standings, team rosters, schedules, game stats, box scores, or MLB news.
  Don't use when: user asks about minor league baseball, college baseball, international baseball, or other sports. Don't use for live play-by-play — data updates post-play.
license: MIT
metadata:
  author: machina-sports
  version: "0.1.0"
---

# MLB Data

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
sports-skills mlb get_scoreboard
sports-skills mlb get_standings --season=2025
sports-skills mlb get_teams
```

## Choosing the Season

Derive the active season from the system prompt's date — not just the calendar year.

- **If the user specifies a season**, use it as-is.
- **If the user says "current", "this season", or doesn't specify**: The MLB season runs late March/April through October. If the current month is January–March, the last completed season was the prior calendar year. From April onward, use the current calendar year.
- **Example:** Current date is February 2026 → MLB is in offseason → use season `2025`.
- **Example:** Current date is June 2026 → MLB season is active → use season `2026`.
- **Never hardcode a season.** Always derive it from the system date.

## Commands

### get_scoreboard
Get live/recent MLB scores.
- `date` (str, optional): Date in YYYY-MM-DD format. Defaults to today.

Returns `events[]` with game info, scores (by inning), status, and competitors.

### get_standings
Get MLB standings by league and division.
- `season` (int, optional): Season year

Returns `groups[]` with AL/NL leagues and East/Central/West division standings including W-L, PCT, GB, runs scored/allowed, run differential, and streak.

### get_teams
Get all 30 MLB teams. No parameters.

Returns `teams[]` with id, name, abbreviation, logo, and location.

### get_team_roster
Get full roster for a team.
- `team_id` (str, required): ESPN team ID (e.g., "10" for Yankees)

Returns `athletes[]` with name, position, jersey number, height, weight, experience, bats/throws, and birthplace.

### get_team_schedule
Get schedule for a specific team.
- `team_id` (str, required): ESPN team ID
- `season` (int, optional): Season year

Returns `events[]` with opponent, date, score (if played), and venue.

### get_game_summary
Get detailed box score and scoring plays.
- `event_id` (str, required): ESPN event ID

Returns `game_info`, `competitors`, `boxscore` (batting/pitching stats per player), `scoring_plays`, and `leaders`.

### get_leaders
Get MLB statistical leaders (batting avg, home runs, ERA, etc.).
- `season` (int, optional): Season year

Returns `categories[]` with leader rankings per stat category.

### get_news
Get MLB news articles.
- `team_id` (str, optional): Filter by team

Returns `articles[]` with headline, description, published date, and link.

### get_schedule
Get MLB schedule for a specific date or season.
- `date` (str, optional): Date in YYYY-MM-DD format
- `season` (int, optional): Season year (used only if no date provided)

Returns `events[]` for the specified date.

## Team IDs (Common)

| Team | ID | Team | ID |
|------|-----|------|-----|
| Arizona Diamondbacks | 29 | Milwaukee Brewers | 8 |
| Atlanta Braves | 15 | Minnesota Twins | 9 |
| Baltimore Orioles | 1 | New York Mets | 21 |
| Boston Red Sox | 2 | New York Yankees | 10 |
| Chicago Cubs | 16 | Oakland Athletics | 11 |
| Chicago White Sox | 4 | Philadelphia Phillies | 22 |
| Cincinnati Reds | 17 | Pittsburgh Pirates | 23 |
| Cleveland Guardians | 5 | San Diego Padres | 25 |
| Colorado Rockies | 27 | San Francisco Giants | 26 |
| Detroit Tigers | 6 | Seattle Mariners | 12 |
| Houston Astros | 18 | St. Louis Cardinals | 24 |
| Kansas City Royals | 7 | Tampa Bay Rays | 30 |
| Los Angeles Angels | 3 | Texas Rangers | 13 |
| Los Angeles Dodgers | 19 | Toronto Blue Jays | 14 |
| Miami Marlins | 28 | Washington Nationals | 20 |

**Tip:** Use `get_teams` to get the full, accurate list of team IDs.

## Examples

**User: "What are today's MLB scores?"**
```bash
sports-skills mlb get_scoreboard
```

**User: "Show me the AL East standings"**
```bash
sports-skills mlb get_standings --season=2025
```
Then filter results for American League East.

**User: "Who's on the Yankees roster?"**
```bash
sports-skills mlb get_team_roster --team_id=10
```

**User: "Show me the full box score for last night's Dodgers game"**
1. Find the event_id from `get_scoreboard --date=YYYY-MM-DD`
2. Call `get_game_summary --event_id=<id>` for full box score

## Error Handling

When a command fails, **do not surface raw errors to the user**. Instead:
1. Catch silently and try alternatives
2. If team name given instead of ID, use `get_teams` to find the ID first
3. Only report failure with a clean message after exhausting alternatives

## Troubleshooting

- **`sports-skills` command not found**: Run `pip install sports-skills`
- **Team not found**: Use `get_teams` to list all teams and find the correct ID
- **No data for future games**: ESPN only returns data for completed or in-progress games
- **Offseason**: `get_scoreboard` returns 0 events — expected. Use `get_standings` or `get_news` instead.
