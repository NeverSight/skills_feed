---
name: travel-companion
description: Plan trips, search flights/hotels on Expedia, discover destinations via TikTok, Instagram, and Google Maps, check weather, and email itineraries. Uses the OpenClaw-managed browser. Use when users want travel planning help, destination recommendations, flight/hotel searches, or trip itineraries.
metadata:
  tags: travel, trip, itinerary, flights, hotels, planning
---

# Travel Companion

Assist users with travel planning, destination research, and itinerary management.

## Quick Start

1. **Clarify the request** - Confirm destination, dates, budget, and interests
2. **Research** - Use browser with `profile: "openclaw"` to search:
   - TikTok for trending local tips
   - Instagram for events and spots
   - Eventbrite for specific dates
   - Google Maps for attractions
   - Expedia for flights/hotels
3. **Take snapshots** - Read pages with `snapshotFormat: "ai"`
4. **Compile** - Create summary with activities, weather, costs
5. **Offer to email** - Send itinerary via AgentMail

## Browser Usage

**Always use `profile: "openclaw"`:**

```json
{
  "action": "navigate",
  "targetUrl": "https://www.tiktok.com/search?q=fun%20things%20to%20do%20in%20tokyo",
  "profile": "openclaw"
}
```

**No extension needed** - OpenClaw manages the browser directly.

## Search URLs

**TikTok (trending tips):**
`https://www.tiktok.com/search?q={query}`

**Instagram (events):**
`https://www.instagram.com/explore/search/keyword/?q={query}`

**Eventbrite (specific dates):**
`https://www.eventbrite.com/d/{city}/events-{date}/`

**Google Maps (attractions):**
`https://www.google.com/maps/search/best+attractions+{city}`

**Expedia (flights):**
`https://www.expedia.com/Flights-Search?trip=roundtrip&from={from}&to={to}&dates={date1},{date2}`

## Workflow

1. Navigate to URL with `action: "navigate"`
2. Wait for load with `action: "act", request: { kind: "wait", timeMs: 5000 }`
3. Read page with `action: "snapshot", snapshotFormat: "ai"`
4. Extract relevant info from snapshot text

## Email Itinerary

Use AgentMail with `AGENTMAIL_API_KEY` - see [references/agentmail.md](references/agentmail.md)

## Response Format

Keep concise with emojis for visual appeal:
- Weather summary
- TikTok/Instagram highlights
- Eventbrite events
- Attractions with addresses
- Cost estimates

End with: "More details or email this itinerary?"

## Troubleshooting

**"Can't reach browser"** - User runs: `openclaw browser start`

**Instagram blocks access** - Use TikTok and Eventbrite instead

**Page won't load** - Increase wait time to 5000ms+, try alternate URLs

## Examples

**Day trip:**
```
User: What's fun in DC on Friday?

Search TikTok for trending DC tips, Instagram for events,
Eventbrite for Friday activities. Snapshot each page.
Summarize top 3-5 options with addresses and costs.
```

**Full trip:**
```
User: Plan a weekend in Miami under $500

Research Expedia for flights/hotels, Instagram for beach spots,
TikTok for food tips. Create 2-day itinerary. Offer to email.
```
