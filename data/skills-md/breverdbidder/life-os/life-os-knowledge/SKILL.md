---
name: life-os-knowledge
description: Personal knowledge base for Shapira family daily life. Use when querying or storing information about hotels, swim meet venues, travel logistics, restaurants, service providers, or any location-based preferences. Triggers on phrases like "remember this hotel", "where did we stay", "next time in [city]", "log this location", or references to past stays/visits.
---

# Life OS Knowledge Base

Personal knowledge system for the Shapira family. Stores hotels, venues, travel logistics, and location-based preferences.

## Data Storage

**Database:** Supabase mocerqjnksmhcjzxrewo.supabase.co  
**Table:** `insights` (using insight_type for categorization)

## Schema

Uses the existing `insights` table with these insight_types:
- `HOTEL` - Hotels and lodging
- `SWIM_VENUE` - Competition pools and swim facilities  
- `RESTAURANT` - Dining locations
- `SERVICE_PROVIDER` - Contractors, professionals
- `TRAVEL_ROUTE` - Common drives and logistics

### Key Fields
| Field | Usage |
|-------|-------|
| insight_type | Category: HOTEL, SWIM_VENUE, etc. |
| title | Location name |
| description | JSON with full details (address, city, state, notes) |
| confidence | Rating 1-5 |
| related_date | Last visited date |
| source | Always "life_os_knowledge" |

## Query Examples

### Find hotels in a city
```python
GET /rest/v1/insights?insight_type=eq.HOTEL&description=cs."Ocala"
```

### Find swim venues
```python
GET /rest/v1/insights?insight_type=eq.SWIM_VENUE&order=confidence.desc
```

## Insert New Location

```python
import httpx, json

data = {
    "insight_type": "HOTEL",
    "title": "Hotel Name",
    "description": json.dumps({
        "address": "123 Main St",
        "city": "City",
        "state": "FL",
        "context": "Why we use this",
        "room_type": "king suite",
        "amenities": ["pool", "breakfast"],
        "value": "excellent"
    }),
    "related_date": "2025-12-04",
    "priority": "medium",
    "status": "active",
    "source": "life_os_knowledge",
    "confidence": 5
}
r = client.post(f"{SUPABASE_URL}/rest/v1/insights", headers=headers, json=data)
```

## Reference Files

- `references/hotels.md` - Hotel reviews
- `references/swim-venues.md` - Swim venue details
- `references/travel.md` - Travel routes

## Current Data (Dec 2025)

### Hotels
- **Staybridge Suites Ocala** ⭐⭐⭐⭐⭐ - 4627 NW Blitchton Rd, Ocala FL
  - Context: Michael swim meets at Ocala Aquatic Center
  - Room: Studio with queen beds, full kitchen
  - Value: Excellent

### Swim Venues  
- **Ocala Aquatic Center** ⭐⭐⭐⭐⭐ - 2500 E Fort King St, Ocala FL
  - Pool: FAST, 50m outdoor
  - Drive from Satellite Beach: 2.5 hours (142 mi)
  - Preferred hotel: Staybridge Suites Ocala
