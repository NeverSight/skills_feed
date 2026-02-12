---
name: google-flights
description: Search Google Flights for flight prices and schedules using browser automation. Use when user asks to search flights, find airfare, compare prices, check flight availability, or look up routes. Triggers include "search flights", "find flights", "how much is a flight", "flights from X to Y", "cheapest flight", "flight prices", "airfare", "flight schedule", "nonstop flights", "when should I fly".
allowed-tools: Bash(agent-browser:*)
---

# Google Flights Search

Search Google Flights via agent-browser to find flight prices, schedules, and availability.

## When to Use

- User asks to search/find/compare flights or airfare
- User wants to know flight prices between cities
- User asks about flight schedules or availability
- User wants to find the cheapest flight for specific dates

## When NOT to Use

- **Booking flights**: This skill searches only. Do not attempt to complete a purchase.
- **Hotels/rental cars**: Use other tools for non-flight travel searches.
- **Historical price data**: Google Flights shows current prices, not historical.

## Session Convention

Always use `--session flights` for isolation.

## Fast Path: URL-Based Search (Preferred)

Construct a URL with a natural language `?q=` parameter. Loads results directly — **3 commands total**.

### URL Template

```
https://www.google.com/travel/flights?q=Flights+from+{ORIGIN}+to+{DEST}+on+{DATE}[+returning+{DATE}][+one+way][+business+class][+N+passengers]
```

### Default: Economy + Business Comparison

**Always run two parallel sessions** — economy and business — to show the price delta. This adds no extra time since both load concurrently.

```bash
# Launch both in parallel (background the first)
agent-browser --session econ open "https://www.google.com/travel/flights?q=Flights+from+BKK+to+NRT+on+2026-03-20+returning+2026-03-27" &
agent-browser --session biz open "https://www.google.com/travel/flights?q=Flights+from+BKK+to+NRT+on+2026-03-20+returning+2026-03-27+business+class" &
wait

# Wait for both to load
agent-browser --session econ wait --load networkidle &
agent-browser --session biz wait --load networkidle &
wait

# Snapshot both
agent-browser --session econ snapshot -i
agent-browser --session biz snapshot -i

# Close both
agent-browser --session econ close &
agent-browser --session biz close &
wait
```

Then present results with a **business class delta column**:

| # | Airline | Route | Duration | Stops | Economy | Business | Delta |
|---|---------|-------|----------|-------|---------|----------|-------|
| 1 | JAL | BKK-NRT | 5h 55m | Nonstop | THB 23,255 | THB 65,915 | +THB 42,660 (+183%) |
| 2 | ANA | BKK-NRT | 5h 55m | Nonstop | THB 35,255 | — | N/A |
| 3 | THAI | BKK-NRT | 5h 50m | Nonstop | THB 28,165 | — | N/A |

**Matching logic**: Match flights by airline name and departure time. Not all economy flights have a business equivalent (budget carriers like ZIPAIR, Air Japan don't offer business). Show "—" when no business match exists.

**Tip**: When an airline appears in business results but not economy (e.g., Philippine Airlines), it may operate business-only pricing on that route. Include it in the table with "—" for economy.

### One Way with Business Delta

Same pattern — just add `+one+way` to both URLs:

```bash
agent-browser --session econ open "https://www.google.com/travel/flights?q=Flights+from+LAX+to+LHR+on+2026-04-15+one+way" &
agent-browser --session biz open "https://www.google.com/travel/flights?q=Flights+from+LAX+to+LHR+on+2026-04-15+one+way+business+class" &
wait
```

### When User Asks for Business Only

If the user specifically asks for business class (not a comparison), run just the business session:

```bash
agent-browser --session flights open "https://www.google.com/travel/flights?q=Flights+from+JFK+to+CDG+on+2026-06-01+returning+2026-06-15+business+class"
agent-browser --session flights wait --load networkidle
agent-browser --session flights snapshot -i
agent-browser --session flights close
```

### First Class / Multiple Passengers

```bash
agent-browser --session flights open "https://www.google.com/travel/flights?q=Flights+from+JFK+to+CDG+on+2026-06-01+returning+2026-06-15+first+class+2+adults+1+child"
agent-browser --session flights wait --load networkidle
agent-browser --session flights snapshot -i
agent-browser --session flights close
```

### What Works via URL

| Feature | URL syntax | Status |
|---------|-----------|--------|
| Round trip | `+returning+YYYY-MM-DD` | Works |
| One way | `+one+way` | Works |
| Business class | `+business+class` | Works |
| First class | `+first+class` | Works |
| N passengers (adults) | `+N+passengers` | Works |
| Adults + children | `+2+adults+1+child` | Works |
| IATA codes | `BKK`, `NRT`, `LAX` | Works |
| City names | `Bangkok`, `Tokyo` | Works |
| Dates as YYYY-MM-DD | `2026-03-20` | Works (best) |
| Natural dates | `March+20` | Works |
| **Premium economy** | `+premium+economy` | **Fails** |
| **Multi-city** | N/A | **Fails** |

### What Requires Interactive Fallback

- **Premium economy** cabin class
- **Multi-city** trips (3+ legs)
- **Infant passengers** (seat vs lap distinction)
- **URL didn't load results** (consent banner, CAPTCHA, locale issue)

### Reading Results from Snapshot

Each flight appears as a `link` element with a full description:

```
link "From 20508 Thai baht round trip total. Nonstop flight with Air Japan.
     Leaves Suvarnabhumi Airport at 12:10 AM on Friday, March 20 and arrives
     at Narita International Airport at 8:15 AM on Friday, March 20.
     Total duration 6 hr 5 min. Select flight"
```

Parse economy + business snapshots into a **combined table with delta**:

| # | Airline | Dep | Arr | Duration | Stops | Economy | Business | Biz Delta |
|---|---------|-----|-----|----------|-------|---------|----------|-----------|
| 1 | JAL | 8:05 AM | 4:00 PM | 5h 55m | Nonstop | THB 23,255 | THB 65,915 | +THB 42,660 (+183%) |
| 2 | THAI | 10:30 PM | 6:20 AM+1 | 5h 50m | Nonstop | THB 28,165 | THB 75,000 | +THB 46,835 (+166%) |
| 3 | Air Japan | 12:10 AM | 8:15 AM | 6h 05m | Nonstop | THB 20,515 | — | — |
| 4 | ZIPAIR | 11:45 PM | 7:30 AM+1 | 5h 45m | Nonstop | THB 21,425 | — | — |

**Matching**: Pair economy and business results by airline + departure time. Budget carriers without business class show "—". Include "Best"/"Cheapest" labels from Google when present.

## Interactive Workflow (Fallback)

Use for multi-city, premium economy, or when the URL path fails.

### Open and Snapshot

```bash
agent-browser --session flights open "https://www.google.com/travel/flights"
agent-browser --session flights wait 3000
agent-browser --session flights snapshot -i
```

If a consent banner appears, click "Accept all" or "Reject all" first.

### Set Trip Type (if not Round Trip)

```bash
agent-browser --session flights click @eN   # Trip type combobox ("Round trip")
agent-browser --session flights snapshot -i
agent-browser --session flights click @eN   # "One way" or "Multi-city"
agent-browser --session flights wait 1000
agent-browser --session flights snapshot -i
```

### Set Cabin Class / Passengers (if non-default)

**Cabin class:**
```bash
agent-browser --session flights click @eN   # Cabin class combobox
agent-browser --session flights snapshot -i
agent-browser --session flights click @eN   # Select class
agent-browser --session flights wait 1000
agent-browser --session flights snapshot -i
```

**Passengers:**
```bash
agent-browser --session flights click @eN   # Passengers button
agent-browser --session flights snapshot -i
agent-browser --session flights click @eN   # "+" for Adults/Children/Infants
agent-browser --session flights snapshot -i
agent-browser --session flights click @eN   # "Done"
agent-browser --session flights wait 1000
agent-browser --session flights snapshot -i
```

### Enter Airport (Origin or Destination)

```bash
agent-browser --session flights click @eN   # Combobox field
agent-browser --session flights wait 1000
agent-browser --session flights snapshot -i
agent-browser --session flights fill @eN "BKK"
agent-browser --session flights wait 2000   # CRITICAL: wait for autocomplete
agent-browser --session flights snapshot -i
agent-browser --session flights click @eN   # Click suggestion (NEVER press Enter)
agent-browser --session flights wait 1000
agent-browser --session flights snapshot -i
```

### Set Dates

```bash
agent-browser --session flights click @eN   # Date textbox
agent-browser --session flights wait 1000
agent-browser --session flights snapshot -i
# Calendar shows dates as buttons: "Friday, March 20, 2026"
agent-browser --session flights click @eN   # Click target date
agent-browser --session flights wait 500
agent-browser --session flights snapshot -i
# Click "Done" to close calendar
agent-browser --session flights click @eN   # "Done" button
agent-browser --session flights wait 1000
agent-browser --session flights snapshot -i
```

### Search

**"Done" only closes the calendar. You MUST click "Search" separately.**

```bash
agent-browser --session flights click @eN   # "Search" button
agent-browser --session flights wait --load networkidle
agent-browser --session flights snapshot -i
agent-browser --session flights close
```

### Multi-City Specifics

After selecting "Multi-city" trip type, the form shows one row per leg:

- Each leg has: origin combobox, destination combobox, departure date textbox
- **Origins auto-fill** from the previous leg's destination
- Click "Add flight" to add more legs (default: 2 legs shown)
- Click "Remove flight from X to Y" buttons to remove legs
- Results show flights for the **first leg**, with prices reflecting the **total multi-city cost**

Fill each leg's destination + date in order, then click "Search".

## Key Rules

| Rule | Why |
|------|-----|
| Prefer URL fast path | 3 commands vs 15+ interactive |
| `wait --load networkidle` | Smarter than fixed `wait 5000` — returns when network settles |
| Use `fill` not `type` for airports | Clears existing text first |
| Wait 2s after typing airport codes | Autocomplete needs API roundtrip |
| Always CLICK suggestions, never Enter | Enter is unreliable for autocomplete |
| Re-snapshot after every interaction | DOM changes invalidate refs |
| "Done" ≠ Search | Calendar Done only closes picker |

## Troubleshooting

**Consent popups**: Click "Accept all" or "Reject all" in the snapshot.

**URL fast path didn't work**: Fall back to interactive. Some regions/locales handle `?q=` differently.

**No results**: Verify airports (check combobox labels), dates in the future, or wait longer.

**Bot detection / CAPTCHA**: Inform user. Do NOT solve CAPTCHAs. Retry after a short wait.

## Deep-Dive Reference

See [references/interaction-patterns.md](references/interaction-patterns.md) for:
- Full annotated walkthrough (every command + expected output)
- Airport autocomplete failure modes and recovery
- Date picker calendar navigation
- Multi-city searches
- Scrolling for more results
