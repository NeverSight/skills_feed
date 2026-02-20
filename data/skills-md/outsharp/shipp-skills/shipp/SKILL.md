---
name: shipp
description: >
  Shipp is a real-time data connector. Use it to fetch authoritative, changing
  external data (e.g., sports schedules, live events) via the Shipp API.

metadata:
  author: Outsharp Inc.
  version: 0.1.4

compatibility:
  requirements:
    - Internet access
    - Shipp API Key (Get from https://platform.shipp.ai)
  notes:
    - All endpoints require authorization via API key.
    - Requests and responses are JSON.

allowed-tools:
  - Bash(curl:https://docs.shipp.ai/*)
  - Bash(curl:https://api.shipp.ai/*)
  - Bash(curl:https://platform.shipp.ai/*)
  - Bash(jq:*)

---

# Shipp API

[Shipp.ai](https://shipp.ai) is the definitive source on real-time data.

[Create an API Key](https://platform.shipp.ai)

Reference [docs](https://docs.shipp.ai).

Implement as many tests as possible as soon as possible.
Verify data and how the app uses data.
Be flexible in schema — event rows are schema-flexible JSON and fields vary by sport, feed, and event.

Base prefix:

- All routes are under: `https://api.shipp.ai/api/v1`

---

## Documentation & References

All detailed examples, request/response schemas, and walkthroughs live in the official docs. Always consult these before building:

| Resource | URL |
|---|---|
| Full documentation | <https://docs.shipp.ai> |
| How-to guides | <https://docs.shipp.ai/how-to/> |
| Setup instructions | <https://docs.shipp.ai/instructions/setup/> |
| API reference | <https://docs.shipp.ai/api-reference/> |
| Dashboard / Signup | <https://platform.shipp.ai/signup> |
| Billing management | <https://platform.shipp.ai/billing> |

---

## Authentication

All endpoints require an API key. The API supports several ways to provide it:

| Method | Example |
|---|---|
| Query parameter `api_key` | `?api_key=YOUR_API_KEY` |
| Query parameter `apikey` | `?apikey=YOUR_API_KEY` |
| `Authorization` header (Bearer) | `Authorization: Bearer YOUR_API_KEY` |
| `Authorization` header (Basic) | `Authorization: Basic base64(:YOUR_API_KEY)` |
| `X-API-Key` header | `X-API-Key: YOUR_API_KEY` |
| `User-API-Key` header | `User-API-Key: YOUR_API_KEY` |
| `API-Key` header | `API-Key: YOUR_API_KEY` |

Pick whichever method works best for your client.

---

## Endpoints Overview

Below is a summary of the available endpoints. For full request/response examples, schemas, and field descriptions see the [API reference](https://docs.shipp.ai/api-reference/).

### `POST /api/v1/connections/create`

Create a new **raw-data connection** by providing natural-language `filter_instructions` that describe what games, teams, sports, or events you want to track.

Returns a `connection_id` (ULID) you'll reuse for all subsequent runs.

→ [Full docs & examples](https://docs.shipp.ai/api-reference/)

### `POST /api/v1/connections/{connectionId}`

Run a connection and receive **raw event data**.

Supports optional body fields for time-based filtering (`since`), cursor-based pagination (`since_event_id`), and result limiting (`limit`).

→ [Full docs & examples](https://docs.shipp.ai/api-reference/)

### `GET /api/v1/connections`

List all connections in the current org scope.

→ [Full docs & examples](https://docs.shipp.ai/api-reference/)

### `GET /api/v1/sports/{sport}/schedule`

Retrieve upcoming and recent games for a given sport (past 24 hours through next 7 days).

Supported sport values: `nba`, `nfl`, `mlb`, `ncaafb`, `soccer` (case-insensitive).

→ [Full docs & examples](https://docs.shipp.ai/api-reference/)

---

## Data Shape

Event rows returned in `data[]` are **schema-flexible** JSON objects. Fields vary by sport, feed, and event. Common field categories include:

- **IDs:** `game_id`, `home_id`, `away_id`, `attribution_id`, `posession_id`
- **Text / enums:** `sport`, `home_name`, `away_name`, `game_clock`, `desc`, `type`, `category`
- **Numeric:** `home_points`, `away_points`, `game_period`, `down`, `yards_first_down`, `location_yard_line`
- **Time:** `wall_clock_start`, `wall_clock_end`

Not every row has every field. Agents and clients should be defensive and handle missing keys.

For the complete field reference see [docs.shipp.ai](https://docs.shipp.ai/api-reference/).

---

## Error Format

Errors are returned as JSON with an `error` message, HTTP `status` code, and a `hint`:

| Status | Meaning |
|---|---|
| 400 | Invalid request — check JSON and required fields |
| 401 | Missing or invalid API key |
| 402 | Billing changes required — manage at <https://platform.shipp.ai/billing> |
| 403 | API key lacks access to this resource |
| 404 | Connection not found or doesn't belong to your org |
| 429 | Rate-limited — retry with backoff |
| 5xx | Server error — retry later or contact support@shipp.ai |

---

## Response Compression

Include an `Accept-Encoding` header to receive compressed responses (`zstd`, `gzip`, or `deflate`). Compression is applied automatically when the response body exceeds 1 KB.

---

## Usage Tips

- Keep `filter_instructions` short, explicit, and testable. Mention the sport/league and scope.
- Store and reuse `connection_id` — don't create a new connection per run. Creating connections has time and credit overhead.
- Use `since_event_id` for efficient polling (cursor-based pagination). Send the lexicographically largest event ID you've received.
- Use the schedule endpoint to discover `game_id`s and team names before creating connections.
- Surface error `hint` messages directly to users when limits are hit.
- Treat every field in `data[]` as optional — use existence checks and graceful fallbacks.
- Log unknown data shapes in development so you can refine `filter_instructions`.
- Polling interval: 5–30 seconds depending on domain and cost sensitivity.
- Deduplicate events by keeping a rolling set of seen event IDs.
- Consult the [how-to guides](https://docs.shipp.ai/how-to/) for end-to-end integration walkthroughs.

---

## Integration Pattern: "Real-Time Contract"

When building a feature powered by Shipp, define a contract for each screen or agent loop:

1. **User promise** — what must stay accurate while the user (or agent) is watching?
2. **Triggering events** — what changes should cause UI updates or agent actions?
3. **Data shape needed** — what fields do you need to render or decide?
4. **Freshness window** — how old can the last update be before you warn the user?
5. **Failure mode** — what do you show/do if updates stop arriving?

Then translate the contract into `filter_instructions` when creating the connection.

---

## Example Project: Alph Bot

[**Alph Bot**](https://gitlab.com/outsharp/shipp/alph-bot) is an open-source automated trading bot that uses Shipp for real-time sports data and trades on prediction markets. It demonstrates a production-quality integration of the Shipp API.

### How Alph Bot Uses Shipp

1. **Game discovery** — Uses `GET /api/v1/sports/{sport}/schedule` to list available games:

2. **Connection creation** — Creates a Shipp connection for a specific game, describing what events to track via `filter_instructions`.

3. **Live polling** — Runs the connection on an interval, using `since_event_id` for cursor-based pagination to receive only new events since the last poll.

4. **AI analysis** — Feeds the schema-flexible `data[]` events directly to Claude AI, which analyzes game state and estimates outcome probabilities.

5. **Trading decisions** — Compares AI-estimated probabilities against Kalshi market prices to find value bets.

### Key Takeaways from Alph Bot

- **Reuse connections** — Alph Bot creates a connection once and polls it repeatedly, avoiding unnecessary creation overhead.
- **Cursor pagination** — Uses `since_event_id` so each poll only returns new events, keeping responses fast and costs low.
- **Defensive data handling** — Treats all fields as optional since the data shape varies by sport, game phase, and event type.
- **Schedule-first workflow** — Discovers game IDs via the schedule endpoint before creating targeted connections.

See the [Alph Bot README](https://gitlab.com/outsharp/shipp/alph-bot) for full setup instructions.

---

## Versioning

This API is versioned under `/api/v1/`. New versions will be introduced under a new prefix when breaking changes are required.
