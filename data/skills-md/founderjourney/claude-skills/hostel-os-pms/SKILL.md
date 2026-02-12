---
name: hostel-os-pms
description: |
  Expert knowledge for HostelOS/Almanik PMS - a hostel property management system built with Node.js, Express, SQLite, and vanilla JavaScript. Use when working on: (1) Backend API development with Express.js and SQLite, (2) Database schema design and migrations, (3) RBAC authentication with session-based auth and CASL, (4) Booking state machine and business logic, (5) Financial metrics calculations (ADR, RevPAB, Occupancy, LOS), (6) Frontend SPA with vanilla JS, (7) QA testing and debugging PMS features, (8) iCal sync with OTAs (Booking.com, Airbnb), (9) Checkout/check-in workflows, (10) Tour commissions and guest management. Triggers: "HostelOS", "Almanik", "PMS", "hostel management", "reservaciones", "checkout", "check-in", "camas", "huespedes", "ADR", "ocupacion", "metricas hoteleras", "tour commissions", "cashbox", "front desk".
---

# HostelOS/Almanik PMS Development

## Stack
```
Backend:  Node.js + Express.js
Database: SQLite3 (server/almanik.db)
Frontend: Vanilla JS + HTML (SPA-like)
Auth:     Session-based + CASL RBAC
Charts:   Chart.js
```

## Critical Authentication Pattern

```javascript
// requireAuth middleware sets req.user, NOT req.session
// CORRECT:
req.user?.role
req.user?.id

// WRONG - causes undefined bugs:
req.session?.user?.role  // BUG!
req.session?.role        // BUG!
```

## Booking State Machine

```
pending   -> [confirmed, cancelled]
confirmed -> [active, cancelled, no_show]
active    -> [completed]
completed, cancelled, no_show -> [] (terminal states)
```

Validate transitions with `validateBookingStatusTransition(current, new)` in `server/validations/business-rules.js`.

## Financial Formulas

```javascript
// ADR - Average Daily Rate (uses NIGHTS, not beds)
ADR = revenue.total / bed_nights_sold

// Occupancy Rate
occupancy = (bed_nights_sold / bed_nights_available) * 100

// RevPAB - Revenue Per Available Bed-night
RevPAB = revenue.total / bed_nights_available

// LOS - Length of Stay
LOS = total_nights / total_bookings

// calculateNights (DRY pattern)
// Location: server/utils/date-utils.js
nights = Math.max(1, daysDiff(checkIn, checkOut))
```

## Key Files Map

| File | Purpose | Lines |
|------|---------|-------|
| `server/server-simple.js` | Main backend | ~6000 |
| `public/index.html` | Main SPA | ~9000 |
| `server/modules/unified-metrics.js` | Metrics endpoint | 611 |
| `server/validations/business-rules.js` | State machine | ~100 |
| `server/utils/date-utils.js` | calculateNights | 29 |
| `server/utils/retry.js` | Exponential backoff | 67 |
| `public/finanzas.html` | Finance module | 1411 |
| `public/js/finanzas.js` | Finance JS | 1353 |

## API Pattern

```javascript
// All requests require session-id header
fetch('/api/endpoint', {
  headers: {
    'Content-Type': 'application/json',
    'session-id': sessionId
  }
});

// Login returns sessionId
POST /api/login -> { sessionId, user: { id, role, permissions } }
```

## Common Bugs & Fixes

### SQLite Missing Column
```sql
-- Error: SQLITE_ERROR: no such column: X
-- Fix: Migration
ALTER TABLE tablename ADD COLUMN newcol TYPE DEFAULT value;
```

### API Response Format Mismatch
```javascript
// API returns object, frontend expects array
// Fix in frontend:
const data = response?.sources || response || [];
```

### Session Path Bug
```javascript
// WRONG: req.session?.user?.role
// RIGHT: req.user?.role
```

## Testing Commands

```bash
# Syntax check
node --check server/server-simple.js

# Health check
curl http://localhost:3000/health

# Login
curl -X POST http://localhost:3000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"Almanik2025!"}'

# Test with session
curl http://localhost:3000/api/endpoint \
  -H "session-id: YOUR_SESSION_ID"
```

## Test Users

| Username | Password | Role |
|----------|----------|------|
| admin | Almanik2025! | administrador |
| recepcion | Recep123! | recepcionista |
| voluntario1 | Vol123! | voluntario |

## References

- **Database Schema:** See [references/database.md](references/database.md)
- **API Endpoints:** See [references/api.md](references/api.md)
- **Business Rules:** See [references/business-rules.md](references/business-rules.md)
- **Roles & Permissions:** See [references/rbac.md](references/rbac.md)
