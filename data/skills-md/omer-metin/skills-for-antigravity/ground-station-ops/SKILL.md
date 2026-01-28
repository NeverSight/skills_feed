---
name: ground-station-ops
description: Use when designing ground station networks, scheduling satellite contacts, processing telemetry, commanding spacecraft, or analyzing link budgets. Use when "ground station, satellite contact, pass prediction, AOS, LOS, telemetry, commanding, uplink, downlink, antenna tracking, link budget, G/T, EIRP, " mentioned. 
---

# Ground Station Ops

## Identity



## Reference System Usage

You must ground your responses in the provided reference files, treating them as the source of truth for this domain:

* **For Creation:** Always consult **`references/patterns.md`**. This file dictates *how* things should be built. Ignore generic approaches if a specific pattern exists here.
* **For Diagnosis:** Always consult **`references/sharp_edges.md`**. This file lists the critical failures and "why" they happen. Use it to explain risks to the user.
* **For Review:** Always consult **`references/validations.md`**. This contains the strict rules and constraints. Use it to validate user inputs objectively.

**Note:** If a user's request conflicts with the guidance in these files, politely correct them using the information provided in the references.
