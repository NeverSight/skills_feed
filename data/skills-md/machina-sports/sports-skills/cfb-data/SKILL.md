---
name: cfb-data
description: |
  College Football (CFB) data via ESPN public endpoints — scores, standings, rosters, schedules, game summaries, play-by-play, rankings, injuries, futures, team/player stats, and news for NCAA Division I FBS. Zero config, no API keys.

  Use when: user asks about college football scores, standings, rankings, team rosters, schedules, game results, play-by-play, injuries, betting futures, team/player statistics, or CFB news.
  Don't use when: user asks about NFL (use nfl-data), college basketball (use cbb-data), or non-sports topics.
license: MIT
metadata:
  author: machina-sports
  version: "0.1.0"
---

# College Football Data (CFB)

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
sports-skills cfb get_scoreboard
sports-skills cfb get_rankings
sports-skills cfb get_standings --group=8
```

## Important: College vs. Pro Differences

College football has 750+ FBS teams (vs 32 NFL teams), organized by **conferences** rather than divisions:
- **Standings are per-conference** — use the `group` parameter to filter
- **Rankings replace leaders** — college uses AP Top 25 and Coaches Poll instead of league-wide stat leaders
- **Ranked teams** have a `rank` field (null = unranked) on scoreboard competitors
- **Week-based schedule** — like NFL, college football uses week numbers

## Conference IDs (group parameter)

Use the `--group` parameter for standings and scoreboard filtering:

| Conference | Group ID | Conference | Group ID |
|-----------|----------|-----------|----------|
| ACC | 1 | Big 12 | 4 |
| SEC | 8 | Big Ten | 9 |
| Pac-12 | 15 | American | 151 |
| Mountain West | 17 | Sun Belt | 37 |
| MAC | 15 | Conference USA | 12 |

**Tip:** Conference IDs may change across seasons. Use `get_standings` without a group to see all conferences and their current structure.

## Commands

### get_scoreboard
Get live/recent college football scores.
- `date` (str, optional): Date in YYYY-MM-DD format. Defaults to today.
- `week` (int, optional): CFB week number.
- `group` (int, optional): Conference group ID to filter.
- `limit` (int, optional): Max events to return.

### get_standings
Get college football standings by conference.
- `season` (int, optional): Season year. Defaults to current.
- `group` (int, optional): Conference ID to filter (see table above).

### get_teams
Get all FBS college football teams (750+ teams).
No parameters required.

### get_team_roster
Get full roster for a college football team.
- `team_id` (str, required): ESPN team ID.

### get_team_schedule
Get schedule for a specific college football team.
- `team_id` (str, required): ESPN team ID.
- `season` (int, optional): Season year. Defaults to current.

### get_game_summary
Get detailed game summary with box score, scoring plays, and leaders.
- `event_id` (str, required): ESPN event ID.

### get_rankings
Get college football rankings — AP Top 25, Coaches Poll, CFP rankings.
- `season` (int, optional): Season year. Defaults to current.
- `week` (int, optional): Week number for historical rankings.

Returns `polls[]` with poll name and `teams[]` containing rank, previous rank, record, points, and first-place votes.

### get_news
Get college football news articles.
- `team_id` (str, optional): ESPN team ID to filter news by team.

### get_play_by_play
Get full play-by-play data for a game.
- `event_id` (str, required): ESPN event ID

Returns `drives[]` with play-by-play detail including down, distance, yard line, play description, and scoring plays.

### get_schedule
Get college football schedule by week.
- `season` (int, optional): Season year. Defaults to current.
- `week` (int, optional): CFB week number.
- `group` (int, optional): Conference group ID to filter.

### get_injuries
Get current college football injury reports across all teams. No parameters.

Returns `teams[]` with per-team injury lists including player name, position, status, injury type, and detail.

### get_futures
Get college football futures/odds markets (National Championship, Heisman, etc.).
- `limit` (int, optional): Max entries per market. Defaults to 25.
- `season_year` (int, optional): Season year. Defaults to current.

Returns `futures[]` with market name and entries (team/player name + odds value).

### get_team_stats
Get full team statistical profile for a season.
- `team_id` (str, required): ESPN team ID
- `season_year` (int, optional): Season year. Defaults to current.
- `season_type` (int, optional): 2=regular (default), 3=postseason.

Returns `categories[]` with detailed stats including value, rank, and per-game averages.

### get_player_stats
Get full player statistical profile for a season.
- `player_id` (str, required): ESPN athlete ID
- `season_year` (int, optional): Season year. Defaults to current.
- `season_type` (int, optional): 2=regular (default), 3=postseason.

Returns `categories[]` with detailed stats including value, rank, and per-game averages.

## Common Team IDs

| Team | ID | Team | ID |
|------|-----|------|-----|
| Alabama | 333 | Ohio State | 194 |
| Georgia | 61 | Michigan | 130 |
| Texas | 251 | USC | 30 |
| Oregon | 2483 | Penn State | 213 |
| Clemson | 228 | LSU | 99 |
| Florida State | 52 | Oklahoma | 201 |
| Notre Dame | 87 | Tennessee | 2633 |
| Florida | 57 | Auburn | 2 |

**Tip:** Use `get_teams` to get all team IDs, or look up ESPN URLs (e.g., espn.com/college-football/team/_/id/333/alabama → ID is 333).

## Examples

**User: "What are the college football rankings?"**
```bash
sports-skills cfb get_rankings
```

**User: "Show me SEC football standings"**
```bash
sports-skills cfb get_standings --group=8
```

**User: "What's Alabama's schedule this season?"**
```bash
sports-skills cfb get_team_schedule --team_id=333
```

**User: "Show me this week's college football scores"**
```bash
sports-skills cfb get_scoreboard
```

**User: "Get the box score for game 401635800"**
```bash
sports-skills cfb get_game_summary --event_id=401635800
```

**User: "Who's the Heisman favorite?"**
```bash
sports-skills cfb get_futures --limit=10
```

**User: "Show me Alabama's team stats"**
```bash
sports-skills cfb get_team_stats --team_id=333
```

## Error Handling

When a command fails, **do not surface raw errors to the user**. Instead:
1. If no events found for a date, check if it's in the off-season (CFB runs September–January)
2. If standings are empty without a group filter, try with a specific conference group
3. Only report failure with a clean message after exhausting alternatives

## Season Structure

- **Regular Season**: Late August – early December (Weeks 1–15)
- **Conference Championships**: Early December
- **Bowl Season**: Mid-December – early January
- **College Football Playoff**: December – January

## Troubleshooting

- **`sports-skills` command not found**: Run `pip install sports-skills`
- **No games found**: CFB is seasonal (Aug–Jan). Off-season scoreboard will be empty. Use `get_rankings` or `get_news` year-round.
- **Too many teams**: `get_teams` returns 750+ teams. Help users narrow down by suggesting specific team IDs.
- **Rankings empty in off-season**: Rankings are only published during the season and early off-season.
