---
name: cbb-data
description: |
  College Basketball (CBB) data via ESPN public endpoints — scores, standings, rosters, schedules, game summaries, play-by-play, win probability, rankings, futures, team/player stats, and news for NCAA Division I men's basketball. Zero config, no API keys.

  Use when: user asks about college basketball scores, March Madness, NCAA tournament, standings, rankings, team rosters, schedules, play-by-play, betting futures, team/player statistics, or CBB news.
  Don't use when: user asks about NBA/WNBA (use nba-data/wnba-data), college football (use cfb-data), or non-sports topics.
license: MIT
metadata:
  author: machina-sports
  version: "0.1.0"
---

# College Basketball Data (CBB)

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
sports-skills cbb get_scoreboard
sports-skills cbb get_rankings
sports-skills cbb get_standings --group=23
```

## Important: College vs. Pro Differences

College basketball has 360+ D1 teams (vs 30 NBA teams), organized by **conferences**:
- **Standings are per-conference** — use the `group` parameter to filter
- **Rankings replace leaders** — college uses AP Top 25 and Coaches Poll instead of league-wide stat leaders
- **Ranked teams** have a `rank` field (null = unranked) on scoreboard competitors
- **Many games per day** — during the season, 50+ games can be scheduled daily
- **March Madness** — the NCAA Tournament runs in March/April with 68 teams

## Conference IDs (group parameter)

Use the `--group` parameter for standings and scoreboard filtering:

| Conference | Group ID | Conference | Group ID |
|-----------|----------|-----------|----------|
| ACC | 2 | Big 12 | 8 |
| SEC | 23 | Big Ten | 7 |
| Big East | 4 | Pac-12 | 21 |
| American | 62 | Mountain West | 44 |
| Atlantic 10 | 3 | West Coast | 26 |
| Missouri Valley | 18 | Colonial | 10 |

**Tip:** Conference IDs are different from CFB. Use `get_standings` without a group to see all conferences.

## Commands

### get_scoreboard
Get live/recent college basketball scores.
- `date` (str, optional): Date in YYYY-MM-DD format. Defaults to today.
- `group` (int, optional): Conference group ID to filter.
- `limit` (int, optional): Max events to return.

### get_standings
Get college basketball standings by conference.
- `season` (int, optional): Season year. Defaults to current.
- `group` (int, optional): Conference ID to filter (see table above).

### get_teams
Get all D1 men's college basketball teams (360+ teams).
No parameters required.

### get_team_roster
Get full roster for a college basketball team.
- `team_id` (str, required): ESPN team ID.

### get_team_schedule
Get schedule for a specific college basketball team.
- `team_id` (str, required): ESPN team ID.
- `season` (int, optional): Season year. Defaults to current.

### get_game_summary
Get detailed game summary with box score and player stats.
- `event_id` (str, required): ESPN event ID.

### get_rankings
Get college basketball rankings — AP Top 25, Coaches Poll.
- `season` (int, optional): Season year. Defaults to current.
- `week` (int, optional): Week number for historical rankings.

Returns `polls[]` with poll name and `teams[]` containing rank, previous rank, record, points, and first-place votes.

### get_news
Get college basketball news articles.
- `team_id` (str, optional): ESPN team ID to filter news by team.

### get_play_by_play
Get full play-by-play data for a game.
- `event_id` (str, required): ESPN event ID

Returns play-by-play detail including period, clock, team, play description, and scoring plays.

### get_win_probability
Get win probability chart data for a game.
- `event_id` (str, required): ESPN event ID

Returns timestamped home/away win probability percentages throughout the game.

### get_schedule
Get college basketball schedule.
- `date` (str, optional): Date in YYYY-MM-DD format.
- `season` (int, optional): Season year. Defaults to current.
- `group` (int, optional): Conference group ID to filter.

### get_futures
Get college basketball futures/odds markets (National Championship, Player of the Year, etc.).
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
| Duke | 150 | Kansas | 2305 |
| Kentucky | 96 | North Carolina | 153 |
| UConn | 41 | Gonzaga | 2250 |
| Villanova | 222 | UCLA | 26 |
| Michigan State | 127 | Arizona | 12 |
| Purdue | 2509 | Houston | 248 |
| Tennessee | 2633 | Auburn | 2 |
| Baylor | 239 | Creighton | 156 |

**Tip:** Use `get_teams` to get all team IDs, or look up ESPN URLs (e.g., espn.com/mens-college-basketball/team/_/id/150/duke → ID is 150).

## Examples

**User: "What are the college basketball rankings?"**
```bash
sports-skills cbb get_rankings
```

**User: "Show me SEC basketball standings"**
```bash
sports-skills cbb get_standings --group=23
```

**User: "What are today's college basketball scores?"**
```bash
sports-skills cbb get_scoreboard
```

**User: "Show me Duke's roster"**
```bash
sports-skills cbb get_team_roster --team_id=150
```

**User: "Get the box score for game 401638574"**
```bash
sports-skills cbb get_game_summary --event_id=401638574
```

**User: "What's Kansas's schedule this season?"**
```bash
sports-skills cbb get_team_schedule --team_id=2305
```

**User: "Who's favored to win March Madness?"**
```bash
sports-skills cbb get_futures --limit=10
```

**User: "Show me Duke's team stats"**
```bash
sports-skills cbb get_team_stats --team_id=150
```

## Error Handling

When a command fails, **do not surface raw errors to the user**. Instead:
1. If no events found, check if it's the off-season (CBB runs November–April)
2. If standings are empty without a group filter, try a specific conference
3. During March Madness, the scoreboard will have tournament games
4. Only report failure with a clean message after exhausting alternatives

## Season Structure

- **Non-Conference Season**: November – December
- **Conference Play**: January – early March
- **Conference Tournaments**: Early–mid March
- **NCAA Tournament (March Madness)**: Mid-March – early April
  - First Four, First/Second Round, Sweet 16, Elite 8, Final Four, Championship

## Troubleshooting

- **`sports-skills` command not found**: Run `pip install sports-skills`
- **No games found**: CBB is seasonal (Nov–Apr). Off-season scoreboard will be empty.
- **Too many games**: During the season, 50+ games per day. Use `--group` to filter by conference or `--limit` to cap results.
- **Rankings empty in off-season**: Rankings are published weekly during the season (November–March).
- **Roster format differs from NBA**: College rosters may be a flat list instead of positional groups.
