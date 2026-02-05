---
name: synthesis-matrix
description: "Create evidence synthesis matrices for systematic reviews. Use when: (1) Organizing extracted data, (2) Comparing study characteristics, (3) Identifying patterns across studies, (4) Preparing synthesis for manuscripts."
allowed-tools: Read, Write
version: 1.0.0
---

# Evidence Synthesis Matrix Skill

## Purpose
Organize and synthesize evidence across multiple studies using structured matrices.

## Matrix Structure

| Study | Population | Design | Intervention | Outcome | Effect Size | Quality |
|-------|-----------|---------|--------------|---------|------------|---------|
| Smith 2023 | N=120, Adults | RCT | CBT vs WL | Depression | d=0.65 | Low RoB |
| Jones 2022 | N=85, Adolescents | RCT | CBT vs TAU | Depression | d=0.42 | Some concerns |

## Key Elements

**Study Characteristics:**
- Author, year
- Sample size
- Population details

**Methods:**
- Study design
- Intervention details
- Comparison group
- Follow-up duration

**Results:**
- Primary outcomes
- Effect sizes with CI
- Statistical significance

**Quality:**
- Risk of bias assessment
- GRADE rating
- Limitations

## Integration with Agents

Use with literature-reviewer agent to automatically populate matrices from extracted data.

---
**Version:** 1.0.0
