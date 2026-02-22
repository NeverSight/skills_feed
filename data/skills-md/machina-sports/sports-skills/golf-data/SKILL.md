---
name: golf-data
description: |
  PGA Tour, LPGA, and DP World Tour golf data via ESPN public endpoints — tournament leaderboards, scorecards, season schedules, golfer profiles/overviews, and news. Zero config, no API keys.

  Use when: user asks about golf scores, tournament leaderboards, scorecards, PGA Tour schedule, golfer profiles, golfer season stats, LPGA results, or golf news.
  Don't use when: user asks about other sports.
license: MIT
metadata:
  author: machina-sports
  version: "0.1.0"
---

# Golf Data (PGA / LPGA / DP World Tour)

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
sports-skills golf get_leaderboard --tour=pga
sports-skills golf get_schedule --tour=pga --year=2026
sports-skills golf get_news --tour=pga
```

## Important: Golf is Not a Team Sport

Golf data is fundamentally different from team sports (NFL, NBA, etc.):
- **Tournaments, not games**: Each event is a multi-day tournament (typically 4 rounds, Thu–Sun).
- **Individual athletes**: The leaderboard has 72–147 individual golfers, not 2 teams.
- **Score relative to par**: Scores are strings like "-17", "E" (even), "+2" — not point totals.
- **Round-by-round scoring**: Each golfer has 4 round scores (stroke count and score-to-par).
- **One event per week**: Unlike team sports with multiple games per day, golf has one tournament per week per tour.
- **No standings/rankings endpoint**: FedEx Cup standings are not available via this API.

## The `tour` Parameter

Most commands require `--tour=pga`, `--tour=lpga`, or `--tour=eur`:
- **PGA**: PGA Tour (men's professional golf)
- **LPGA**: LPGA Tour (women's professional golf)
- **EUR**: DP World Tour (formerly European Tour)

If the user doesn't specify, default to `pga`. If they say "women's golf" or "LPGA", use `lpga`. If they mention the European Tour or DP World Tour, use `eur`.

## Commands

### get_leaderboard
Get the current tournament leaderboard with all golfer scores.
- `tour` (str, required): "pga", "lpga", or "eur"

Returns the current/most recent tournament with:
- Tournament name, venue, status, current round
- `leaderboard[]` sorted by position with golfer name, country, total score, and round-by-round scores
- `field_size` — total number of golfers in the field

The leaderboard is sorted by position (1 = leader). Each golfer has:
- `position`: Leaderboard rank
- `name`: Golfer name
- `country`: Nationality
- `score`: Total score relative to par (e.g., "-17", "E", "+2")
- `rounds[]`: Array of round scores with stroke count and score-to-par

### get_schedule
Get full season tournament schedule.
- `tour` (str, required): "pga", "lpga", or "eur"
- `year` (int, optional): Season year. Defaults to current.

Returns `tournaments[]` with tournament name, ID, start/end dates. Useful for answering "when is the Masters?" or "what tournaments are coming up?"

### get_player_info
Get individual golfer profile.
- `player_id` (str, required): ESPN athlete ID
- `tour` (str, optional): "pga", "lpga", or "eur". Defaults to "pga".

Returns golfer details: name, age, nationality, birthplace, height/weight, turned pro year, college, headshot URL, and ESPN profile link.

**Finding player IDs:** Player IDs appear in leaderboard results (`id` field on each golfer). You can also find them in ESPN golf URLs (e.g., espn.com/golf/player/_/id/9478/scottie-scheffler → ID is 9478).

**Note:** Player profiles work for PGA Tour and DP World Tour golfers. LPGA player profiles are not available through ESPN's API — the command will automatically try PGA and EUR tours as fallback.

### get_player_overview
Get detailed golfer overview with season stats, rankings, and recent results.
- `player_id` (str, required): ESPN athlete ID
- `tour` (str, optional): "pga", "lpga", or "eur". Defaults to "pga".

Returns season statistics (scoring average, earnings, wins, top-10s), world/tour rankings, and recent tournament results.

### get_scorecard
Get hole-by-hole scorecard for a golfer in the current/most recent tournament.
- `tour` (str, required): "pga", "lpga", or "eur"
- `player_id` (str, required): ESPN athlete ID

Returns `rounds[]` with hole-by-hole scores (strokes, score relative to par) for each completed round.

### get_news
Get golf news articles.
- `tour` (str, required): "pga", "lpga", or "eur"

Returns `articles[]` with headline, description, published date, and link.

## Common Player IDs

| Player | ID | Player | ID |
|--------|-----|--------|-----|
| Scottie Scheffler | 9478 | Nelly Korda | 9012 |
| Rory McIlroy | 3470 | Jin Young Ko | 9758 |
| Jon Rahm | 9780 | Lydia Ko | 7956 |
| Collin Morikawa | 10592 | Lilia Vu | 9401 |
| Xander Schauffele | 10404 | Nasa Hataoka | 10484 |
| Viktor Hovland | 10503 | Atthaya Thitikul | 10982 |
| Hideki Matsuyama | 5765 | Celine Boutier | 9133 |
| Ludvig Aberg | 4686088 | Lexi Thompson | 6843 |

**Tip:** Use `get_leaderboard` to find current player IDs from the active tournament.

## Reading Leaderboard Scores

Golf scores are relative to par. Example response:
```json
{
  "leaderboard": [
    {"position": 1, "name": "Scottie Scheffler", "country": "United States", "score": "-17",
     "rounds": [
       {"round": 1, "strokes": 63, "score": "-8"},
       {"round": 2, "strokes": 68, "score": "-3"},
       {"round": 3, "strokes": 67, "score": "-4"},
       {"round": 4, "strokes": 70, "score": "-1"}
     ]},
    {"position": 2, "name": "Rory McIlroy", "country": "Northern Ireland", "score": "-15", ...}
  ]
}
```
- **Negative score** = under par (good). "-17" means 17 strokes under par.
- **"E"** = even par.
- **Positive score** = over par. "+2" means 2 strokes over par.
- **Strokes** = actual stroke count for that round (par 72 course → 63 strokes = -9).

## Major Championships

| Tournament | Months | Course(s) |
|-----------|--------|-----------|
| The Masters | April | Augusta National |
| PGA Championship | May | Varies |
| U.S. Open | June | Varies |
| The Open Championship | July | Links courses (UK) |

Use `get_schedule` and search for these tournament names to find dates and event IDs.

## Examples

**User: "What's the PGA leaderboard right now?"**
```bash
sports-skills golf get_leaderboard --tour=pga
```

**User: "Show me the LPGA schedule for 2026"**
```bash
sports-skills golf get_schedule --tour=lpga --year=2026
```

**User: "Tell me about Scottie Scheffler"**
```bash
sports-skills golf get_player_info --player_id=9478
```

**User: "When is the Masters this year?"**
```bash
sports-skills golf get_schedule --tour=pga --year=2026
```
Then search the results for "Masters Tournament".

**User: "Show me Scottie Scheffler's scorecard"**
```bash
sports-skills golf get_scorecard --tour=pga --player_id=9478
```

**User: "How has Rory McIlroy been playing this season?"**
```bash
sports-skills golf get_player_overview --player_id=3470
```

**User: "Latest golf news"**
```bash
sports-skills golf get_news --tour=pga
```

## Error Handling

When a command fails, **do not surface raw errors to the user**. Instead:
1. If no active tournament, tell the user and suggest checking the schedule
2. If a player ID is wrong, suggest using `get_leaderboard` to find current player IDs
3. Only report failure with a clean message after exhausting alternatives

## Troubleshooting

- **`sports-skills` command not found**: Run `pip install sports-skills`
- **No active tournament**: Golf tournaments run Thursday–Sunday. Between events, `get_leaderboard` may show no active tournament. Use `get_schedule` to see upcoming events.
- **Limited round data**: Before a tournament starts, round scores will be empty. During the tournament, only completed rounds have scores.
- **Player not found**: Use `get_leaderboard` to find player IDs from the current field, or look up ESPN golf URLs.
