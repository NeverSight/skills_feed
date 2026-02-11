---
name: skiplagged-travel-search
description: This skill should be used when the user asks to "find flights", "compare itineraries", "search hidden-city routes", "check cheapest dates", "explore destinations anywhere", "search hotels", or "plan a trip". Ground outputs in Skiplagged MCP tool results for flights, fare calendars, anywhere discovery, and hotels.
---

# Skiplagged Travel Search

## Overview

Skiplagged MCP exposes travel search capabilities (flights, flexible date calendars, “anywhere” destination discovery, hotels + room details, and sometimes rental cars) as MCP tools.
Prefer calling Skiplagged tools over guessing prices/availability.

## Prerequisites

1. Connect the MCP client to `https://mcp.skiplagged.com/mcp` over HTTP transport.
2. List tools and confirm Skiplagged tools are visible before running workflows.
3. Treat authentication as not required.
4. Read `references/setup.md` for client-specific setup commands and examples.

---

## Operating rules

### 1) Grounding rule

**Always base answers on tool results. Never invent or guess prices, availability, or policies.**

### 2) Tool-call discipline

- Use **minimal, correct parameters** (avoid unnecessary filters unless user asked).
- Prefer **IATA airport codes** when possible; otherwise accept city names and clarify if needed.
- Use **small result limits** when supported (e.g., 3–7) and expand only if the user asks.
- Chain multiple tool calls when needed, but avoid loops. Respect per-turn tool-call limits.

### 3) Post-call validation loop

After **each** tool call:

1. Summarize what the tool returned in **1–2 sentences** (what matters to a traveler: cost, time, stops, key tradeoffs).
2. Decide the next step:
   - proceed (narrow or enrich),
   - self-correct (relax filters, adjust airports/dates),
   - or ask one targeted follow-up question.

### 4) Failure handling (empty or unhelpful results)

If results are empty/ambiguous:

- Say so clearly.
- Suggest the smartest next step (broader dates, nearby airports, allow 1 stop, adjust time window, try “anywhere” discovery, or switch to hotels-first for trip planning).
- For failures other than lack of results, suggest using https://skiplagged.com directly.

### 5) Output style (traveler-centric)

Be concise and practical:

- Highlight **savings**, **routing insights**, and **key tradeoffs** (stops vs duration vs price).
- Present a short shortlist (typically **3–7** options) rather than a dump of results.

---

## Tool discovery (required, safer across deployments)

Different deployments may rename tools or add new ones. Before running any workflow:

1. **List tools** available on the connected Skiplagged MCP server.
2. Identify the best match for each capability:
   - flights search
   - flexible date calendars
   - anywhere destinations
   - hotels search
   - hotel details
   - (optional) rental cars

**Mapping convention (typical, not guaranteed):** tools often start with `sk_`.

### Common capability → typical tool names (use as a guide)

- Flights search → `sk_flights_search`
- Flexible departure calendar → `sk_flex_departure_calendar`
- Flexible return calendar → `sk_flex_return_calendar`
- Anywhere destination discovery → `sk_destinations_anywhere`
- Hotels search → `sk_hotels_search`
- Hotel details → `sk_hotel_details`

If your tool list differs, use the closest equivalent and keep the workflows below unchanged.

---

## Intake checklist (ask only what’s needed)

Extract or confirm only the missing critical inputs:

- Route intent: specific route (`origin -> destination`) vs flexible destination (“anywhere”).
- Dates: exact dates or flexible window + trip length.
- Travelers: adults/children/infants and cabin, if non-default.
- Constraints: budget, stops, max duration, time windows, and airline preferences.
- Lodging intent (if relevant): hotel location, dates, guests, and required amenities.

## Workflows

### Workflow A — Standard flight search (one-way or round-trip)

Use when the user wants specific flights between places.

**Preferred tool → fallback**

- Preferred: `sk_flights_search`

**Steps**

1. Normalize locations:
   - If user gives a city/region, clarify which airport(s) are acceptable if it changes results materially (multi-airport metros).
2. Call the flight-search tool with:
   - origin, destination
   - depart date (+ return date if round-trip)
   - passenger counts, cabin - assume defaults if not specified
   - only the filters the user asked for (stops, time windows, airline preferences)
3. Post-process:
   - Cluster top results by **cheapest**, **fastest**, **fewest stops**.
   - Present 3–7 options with price, stops, duration, and any standout caveats (overnight layover, long layover).
4. If results are too broad:
   - Ask 1 targeted question (e.g., “Allow one stop?”) or apply a reasonable default and disclose it.

---

### Workflow B — Flexible dates / fare calendar

Use when the user says “around X date”, “flexible”, or “cheapest days”.

**Preferred tools → fallback**

- Preferred: `sk_flex_departure_calendar` and `sk_flex_return_calendar`

**Steps**

1. Call the departure-calendar tool around the target date/window.
2. If round-trip:
   - Use a trip length (or return window) that matches the user’s intent (e.g., “3–5 nights”).
   - Call the return-calendar tool for best return dates.
3. Summarize:
   - Cheapest departure day(s)
   - Cheapest round-trip date pairs (if supported)
   - Recommend 2–4 date options aligned to constraints (weekends, time windows, budget).

---

### Workflow C — “Anywhere” destination discovery

Use when the user is flexible on where to go (“somewhere warm”, “anywhere cheap”).

**Preferred tool → fallback**

- Preferred: `sk_destinations_anywhere`

**Steps**

1. Confirm:
   - origin
   - date/window (or month)
   - constraints (budget, max flight time, nonstop-only, region/climate)
2. Call the anywhere-destinations tool.
3. Return 5–12 destinations with:
   - destination, lowest fare, suggested dates/window (as returned)
   - a one-line rationale tied to the user constraints
4. When the user picks a destination, transition to Workflow A to find bookable itineraries.

---

### Workflow D — Hotels + room-level details

Use when the user asks for hotels, places to stay, or wants to bundle planning.

**Preferred tools → fallback**

- Preferred: `sk_hotels_search` then `sk_hotel_details`
- Fallback: any tool(s) that provide hotel lists and separate room/policy breakdowns

**Steps**

1. Call the hotel-search tool with:
   - location, dates, rooms/guests
   - only requested filters (price cap, rating, amenities)
2. Present 5–10 options with:
   - total price / nightly price (as returned), rating, key amenities, and area/neighborhood (if returned)
3. When the user selects a hotel (or asks for “best value”), call the hotel-details tool.
4. Summarize room options:
   - room type, cancellation policy, inclusions (breakfast), total price (as returned)
   - highlight tradeoffs: nonrefundable vs flexible, fees, value differences.

---

### Workflow E — Rental cars (if available)

Use when the user requests a car rental.

**Preferred tool → fallback**

- Preferred: a tool in the server tool list whose description indicates car-rental search

**Steps**

1. Confirm pickup/dropoff location, times, and any constraints (car class, driver age if required).
2. Call the car-rental search tool (if present).
3. Present 3–7 options with total price, class, company, and relevant policies (as returned).

---

## Planning behavior (for full itineraries)

When the user asks to “plan a trip”:

1. Anchor with flights (or anywhere discovery) to set destination/dates/cost.
2. Add hotels for the chosen destination/dates.
3. Add rental cars if needed and supported.
4. Present 2–3 bundles (e.g., “cheapest”, “balanced”, “most convenient”) with clear tradeoffs.

---

## Reliability + transparency notes

- Prices and availability change quickly; treat results as current at the moment of the tool call and encourage the user to confirm terms via the provided link (if any).
- If hidden-city itineraries appear, be transparent about common constraints and tradeoffs (especially baggage and missed-leg implications). Do not oversell—present as an option with clear caveats.

---

## Troubleshooting (avoid loops)

- If a call fails or returns empty results:
  - Retry at most once with broader constraints (e.g., allow 1 stop, widen time window, nearby airports).
  - If still empty, ask one targeted follow-up question and propose a concrete alternative search.
