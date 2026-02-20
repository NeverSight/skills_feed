---
name: bcn-transport
description: Expert in Barcelona's transportation geography (El Prat Airport, Sants Station) and taxi sector operational patterns.
---

# Barcelona Transportation Context Skill

This skill provides the assistant with specific domain knowledge about the taxi sector in Barcelona and its key transportation hubs.

## Knowledge Areas

### 1. El Prat Airport (BCN) Geography
- **Terminal 1 (T1):** Knowledge of "Parrilla" (taxi queue), departures, arrivals, and Puente Aéreo zones.
- **Terminal 2 (T2):** Differences between T2A, T2B, and T2C (EasyJet).
- **Geofence Coordinates:** Accurate polygon definitions for these zones.

### 2. Sants Train Station
- **Arrivals/Departures:** Understanding the flow of AVE and regional trains.
- **Taxi Zones:** Specifics of the Sants taxi queue and surrounding traffic flow.

### 3. Taxi Sector Operations
- **IMET Regulations:** General knowledge of the Metropolitan Institute of Taxi (IMET) rules (shifts, pricing, holidays).
- **Market Dynamics:** Understanding when and where demand peaks happen (e.g., Fira Barcelona events, night leisure zones).

### 4. Recommendation Logic (`useWhereNext`)
- **Arrival Correlation:** Correlating `vuelos.json` and `trenes.json` with taxi demand.
- **Travel Times:** Knowledge of typical travel times between key points in Barcelona to refine "Where Next" scores.

## Guidelines for Responses
- Use **local terminology** (Parrilla, Born, Eixample, etc.) where appropriate.
- When suggesting geofence changes, reference the **physical layout** of terminals.
- Help refine the `useWhereNext` scoring algorithm based on **local peak hours**.
