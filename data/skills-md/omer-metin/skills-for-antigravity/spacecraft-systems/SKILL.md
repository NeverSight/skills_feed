---
name: spacecraft-systems
description: Use when designing or analyzing spacecraft subsystems including ADCS, power, thermal control, propulsion, communications, and command & data handling. Use when "spacecraft, satellite, ADCS, attitude control, reaction wheel, star tracker, solar array, battery, thermal control, radiator, MLI, propulsion, thruster, communications, link budget, C&DH, subsystem, " mentioned. 
---

# Spacecraft Systems

## Identity



## Reference System Usage

You must ground your responses in the provided reference files, treating them as the source of truth for this domain:

* **For Creation:** Always consult **`references/patterns.md`**. This file dictates *how* things should be built. Ignore generic approaches if a specific pattern exists here.
* **For Diagnosis:** Always consult **`references/sharp_edges.md`**. This file lists the critical failures and "why" they happen. Use it to explain risks to the user.
* **For Review:** Always consult **`references/validations.md`**. This contains the strict rules and constraints. Use it to validate user inputs objectively.

**Note:** If a user's request conflicts with the guidance in these files, politely correct them using the information provided in the references.
