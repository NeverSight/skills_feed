---
name: flight-search
description: Search Google Flights for prices, times, and airlines. No API key required.
homepage: https://github.com/Olafs-World/flight-search
metadata:
  {
    "openclaw":
      {
        "emoji": "✈️",
        "requires": { "bins": ["uvx"] },
        "install":
          [
            {
              "id": "uv",
              "kind": "pip",
              "package": "uv",
              "bins": ["uvx"],
              "label": "Install uv (for uvx)",
            },
          ],
      },
  }
---

# Flight Search

Search Google Flights from the command line. Get prices, times, and airlines - no API key needed.

Built on [fast-flights](https://github.com/AWeirdDev/flights).

## Quick Start

```bash
# one-off search (no install needed)
uvx flight-search DEN LAX --date 2026-03-01

# or install globally
uv tool install flight-search
flight-search JFK LHR --date 2026-06-15 --return 2026-06-22
```

## Options

```
positional arguments:
  origin                Origin airport code (e.g., DEN, LAX, JFK)
  destination           Destination airport code

options:
  --date, -d            Departure date (YYYY-MM-DD) [required]
  --return, -r          Return date for round trips (YYYY-MM-DD)
  --adults, -a          Number of adults (default: 1)
  --children, -c        Number of children (default: 0)
  --class, -C           Seat class: economy, premium-economy, business, first
  --limit, -l           Max results (default: 10)
  --output, -o          Output format: text or json (default: text)
```

## Examples

```bash
# One-way flight
flight-search DEN LAX --date 2026-03-01

# Round trip with passengers
flight-search JFK LHR --date 2026-06-15 --return 2026-06-22 --adults 2

# Business class
flight-search SFO NRT --date 2026-04-01 --class business

# JSON output for parsing
flight-search ORD CDG --date 2026-05-01 --output json
```

## Example Output

```
✈️  DEN → LAX
   One way · 2026-03-01
   Prices are currently: typical

──────────────────────────────────────────────────
   Frontier ⭐ BEST
   🕐 10:43 PM → 12:30 AM +1
   ⏱️  2 hr 47 min
   ✅ Nonstop
   💰 $84

──────────────────────────────────────────────────
   United ⭐ BEST
   🕐 5:33 PM → 7:13 PM
   ⏱️  2 hr 40 min
   ✅ Nonstop
   💰 $139
```

## JSON Output

Returns structured data:

```json
{
  "origin": "DEN",
  "destination": "LAX",
  "date": "2026-03-01",
  "current_price": "typical",
  "flights": [
    {
      "airline": "Frontier",
      "departure_time": "10:43 PM",
      "arrival_time": "12:30 AM",
      "duration": "2 hr 47 min",
      "stops": 0,
      "price": 84,
      "is_best": true
    }
  ]
}
```

## Links

- [PyPI](https://pypi.org/project/flight-search/)
- [GitHub](https://github.com/Olafs-World/flight-search)
