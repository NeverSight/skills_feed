---
name: prisma-diagram
description: "Generate PRISMA 2020 flow diagrams for systematic reviews. Use when: (1) Conducting systematic literature reviews, (2) Documenting screening process, (3) Reporting study selection for publications, (4) Demonstrating PRISMA compliance, (5) Creating transparent review methodology documentation."
allowed-tools: Read, Write
version: 1.0.0
---

# PRISMA Flow Diagram Skill

## Purpose

Create PRISMA 2020-compliant flow diagrams showing the study selection process in systematic reviews.

## PRISMA 2020 Flow Diagram Structure

```
┌─────────────────────────────────────────┐
│  Identification                         │
├─────────────────────────────────────────┤
│  Records identified from:               │
│  • Databases (n = X)                    │
│  • Registers (n = X)                    │
│  • Other sources (n = X)                │
│                                         │
│  Records removed before screening:      │
│  • Duplicate records (n = X)            │
│  • Records marked ineligible (n = X)    │
│  • Records removed for other reasons    │
│    (n = X)                              │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│  Screening                              │
├─────────────────────────────────────────┤
│  Records screened (n = X)               │
│  Records excluded (n = X)               │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│  Reports sought for retrieval (n = X)   │
│  Reports not retrieved (n = X)          │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│  Reports assessed for eligibility       │
│  (n = X)                                │
│                                         │
│  Reports excluded: (n = X)              │
│  • Reason 1 (n = X)                     │
│  • Reason 2 (n = X)                     │
│  • Reason 3 (n = X)                     │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│  Included                               │
├─────────────────────────────────────────┤
│  Studies included in review (n = X)     │
│  Reports of included studies (n = X)    │
└─────────────────────────────────────────┘
```

## Required Data Points

1. **Identification:**
   - Records from each database
   - Duplicates removed
   - Records marked ineligible

2. **Screening:**
   - Total records screened
   - Records excluded at title/abstract

3. **Eligibility:**
   - Full-text articles assessed
   - Exclusion reasons with counts

4. **Included:**
   - Final number of studies
   - Final number of reports

## Usage

Provide counts from your literature search and screening process. The skill generates a properly formatted PRISMA 2020 flow diagram in markdown or visual format.

## Integration

Use with literature-reviewer agent and research-database MCP server to automatically populate counts from screening data.

---

**Version:** 1.0.0
