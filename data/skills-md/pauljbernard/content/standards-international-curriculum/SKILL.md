---
name: standards-international-curriculum
description: Align to international education frameworks including IB (PYP/MYP/DP), Cambridge International (IGCSE/A-Levels), UK National Curriculum, Australian Curriculum, and European frameworks. Use for international school curriculum. Activates on "IB", "Cambridge", "UK curriculum", or "international standards".
---

# Standards: International Curriculum Alignment

Align educational content to major international curriculum frameworks and standards.

## When to Use

- International school curriculum development
- IB program implementation
- Cambridge qualification courses
- UK/Australian curriculum adaptation
- Global education programs

## Major International Frameworks

(See /learning.international-standards for detailed framework descriptions)

### Quick Reference

**IB (International Baccalaureate)**:
- PYP, MYP, DP, CP programs
- Learner Profile, ATL Skills, Concepts

**Cambridge International**:
- Primary, Lower Secondary, IGCSE, AS/A Levels
- Learning objectives, Assessment objectives

**UK National Curriculum**:
- Key Stages 1-5
- Programmes of Study, Attainment Targets

**Australian Curriculum**:
- F-10, Senior Secondary
- Content Descriptions, Achievement Standards

## CLI Interface

```bash
/standards.international-curriculum --content "math-unit/" --framework "IB-MYP" --level "Year3"
```

## Output

- International standards alignment
- Framework-specific requirements
- Assessment criteria mapping
- Grade/year level conversion

## Composition

**Works with**: `/learning.international-standards`, `/standards.crosswalk-mapper`

## Exit Codes

- **0**: Alignment complete
- **1**: Framework not supported
- **2**: Level mismatch
