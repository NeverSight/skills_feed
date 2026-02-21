---
name: nhl-data
description: |
  NHL data via ESPN public endpoints — scores, standings, rosters, schedules, game summaries, statistical leaders, and news. Zero config, no API keys.

  Use when: user asks about NHL scores, standings, team rosters, schedules, game stats, box scores, or NHL news.
  Don't use when: user asks about other hockey leagues (AHL, KHL, college hockey), or other sports. Don't use for live play-by-play — data updates post-play.
license: MIT
metadata:
  author: machina-sports
  version: "0.1.0"
---

# NHL Data

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
sports-skills nhl get_scoreboard
sports-skills nhl get_standings --season=2025
sports-skills nhl get_teams
```

## Choosing the Season

Derive the current year from the system prompt's date (e.g., `currentDate: 2026-02-18` → current year is 2026).

- **If the user specifies a season**, use it as-is.
- **If the user says "current", "this season", or doesn't specify**: The NHL season runs October–June. If the current month is October–December, the active season year matches the current year. If January–June, the active season started the previous calendar year (use that year as the season).
- **Example:** Current date is February 2026 → active season started October 2025 → use season `2025`.
- **Never hardcode a season.** Always derive it from the system date.

## Commands

### get_scoreboard
Get live/recent NHL scores.
- `date` (str, optional): Date in YYYY-MM-DD format. Defaults to today.

Returns `events[]` with game info, scores, status, and competitors.

### get_standings
Get NHL standings by conference and division.
- `season` (int, optional): Season year

Returns `groups[]` with Eastern/Western conferences and division standings including W-L-OTL, points, regulation wins, goals for/against, and streak.

### get_teams
Get all NHL teams. No parameters.

Returns `teams[]` with id, name, abbreviation, logo, and location.

### get_team_roster
Get full roster for a team.
- `team_id` (str, required): ESPN team ID (e.g., "21" for Maple Leafs)

Returns `athletes[]` with name, position, jersey number, height, weight, experience, birthplace, and shoots/catches.

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
Get NHL statistical leaders (goals, assists, points, etc.).
- `season` (int, optional): Season year

Returns `categories[]` with leader rankings per stat category.

### get_news
Get NHL news articles.
- `team_id` (str, optional): Filter by team

Returns `articles[]` with headline, description, published date, and link.

### get_schedule
Get NHL schedule for a specific date or season.
- `date` (str, optional): Date in YYYY-MM-DD format
- `season` (int, optional): Season year (used only if no date provided)

Returns `events[]` for the specified date.

## Team IDs (Common)

| Team | ID | Team | ID |
|------|-----|------|-----|
| Anaheim Ducks | 25 | Nashville Predators | 27 |
| Boston Bruins | 1 | New Jersey Devils | 11 |
| Buffalo Sabres | 2 | New York Islanders | 12 |
| Calgary Flames | 3 | New York Rangers | 13 |
| Carolina Hurricanes | 7 | Ottawa Senators | 14 |
| Chicago Blackhawks | 4 | Philadelphia Flyers | 15 |
| Colorado Avalanche | 17 | Pittsburgh Penguins | 16 |
| Columbus Blue Jackets | 29 | San Jose Sharks | 18 |
| Dallas Stars | 9 | Seattle Kraken | 124292 |
| Detroit Red Wings | 5 | St. Louis Blues | 19 |
| Edmonton Oilers | 6 | Tampa Bay Lightning | 20 |
| Florida Panthers | 26 | Toronto Maple Leafs | 21 |
| Los Angeles Kings | 8 | Utah Mammoth | 129764 |
| Minnesota Wild | 30 | Vancouver Canucks | 22 |
| Montreal Canadiens | 10 | Vegas Golden Knights | 37 |
| | | Washington Capitals | 23 |
| | | Winnipeg Jets | 28 |

**Tip:** Use `get_teams` to get the full, accurate list of team IDs.

## Examples

**User: "What are today's NHL scores?"**
```bash
sports-skills nhl get_scoreboard
```

**User: "Show me the Eastern Conference standings"**
```bash
sports-skills nhl get_standings --season=2025
```
Then filter results for Eastern Conference.

**User: "Who's on the Maple Leafs roster?"**
```bash
sports-skills nhl get_team_roster --team_id=21
```

**User: "Show me the full box score for last night's Bruins game"**
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
