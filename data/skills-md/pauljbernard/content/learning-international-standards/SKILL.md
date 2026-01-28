---
name: learning-international-standards
description: Map learning objectives to international educational standards and frameworks including IB, Cambridge International, UK National Curriculum, Australian Curriculum, and regional systems. Use when aligning to non-US standards. Activates on "international standards", "IB curriculum", "Cambridge", or "global frameworks".
---

# Learning International Standards Alignment

Map curriculum to international educational standards and frameworks beyond US systems.

## When to Use

- International school curriculum development
- Cross-border educational programs
- IB, Cambridge, or other international frameworks
- Aligning to foreign national curricula
- Supporting expatriate or global learners

## Key Standards Frameworks

### 1. International Baccalaureate (IB)

**Programs**:
- **PYP** (Primary Years Programme): Ages 3-12
- **MYP** (Middle Years Programme): Ages 11-16
- **DP** (Diploma Programme): Ages 16-19
- **CP** (Career-related Programme): Ages 16-19

**Key Elements**:
- Learner Profile attributes
- Approaches to Learning (ATL) skills
- Concepts-based curriculum
- Action and service components

### 2. Cambridge International

**Qualifications**:
- Cambridge Primary (5-11 years)
- Cambridge Lower Secondary (11-14 years)
- Cambridge IGCSE (14-16 years)
- Cambridge International AS & A Levels (16-19 years)

**Standards**:
- Subject-specific learning objectives
- Assessment objectives
- Scheme of work guidance

### 3. UK National Curriculum

**Key Stages**:
- KS1: Years 1-2 (ages 5-7)
- KS2: Years 3-6 (ages 7-11)
- KS3: Years 7-9 (ages 11-14)
- KS4: Years 10-11 (ages 14-16)
- KS5: Years 12-13 (ages 16-18)

**Components**:
- Programmes of study
- Attainment targets
- National tests/GCSEs/A-Levels

### 4. Australian Curriculum

**Learning Areas**:
- 8 learning areas
- F-10 (Foundation to Year 10)
- Senior secondary (Years 11-12)

**Structure**:
- Content descriptions
- Achievement standards
- General capabilities
- Cross-curriculum priorities

### 5. Other Regional Frameworks

- **Ontario Curriculum** (Canada)
- **New Zealand Curriculum**
- **Singapore Syllabus**
- **European Baccalaureate**
- **French Baccalauréat**

## Grade Level Conversion

**US ↔ International Mapping**:
| US Grade | UK Year | IB | Australian Year | Age |
|----------|---------|-----|-----------------|-----|
| K | Reception | PYP | Foundation | 5 |
| 1 | Year 1 | PYP | Year 1 | 6 |
| 5 | Year 6 | PYP | Year 6 | 10-11 |
| 6 | Year 7 | MYP 1 | Year 7 | 11-12 |
| 10 | Year 11 | MYP 5 | Year 10 | 15-16 |
| 11-12 | Years 12-13 | DP | Years 11-12 | 16-18 |

## CLI Interface

```bash
# Align to IB framework
/learning.international-standards --content "unit-plan.md" --framework "IB-MYP" --level "Year 3"

# Map to UK National Curriculum
/learning.international-standards --objectives "learning-objectives.json" --framework "UK-NC" --key-stage "KS3"

# Cambridge alignment
/learning.international-standards --content "science-course/" --framework "Cambridge-IGCSE" --subject "Biology"

# Multiple frameworks
/learning.international-standards --content "math-unit/" --frameworks "IB-DP,Cambridge-AS,Australian" --level "Year 12"

# Grade conversion
/learning.international-standards --convert-grade "US Grade 7" --to "UK,IB,Australian"
```

## Output

- Standards alignment map with framework codes
- Grade level conversion table
- Framework-specific requirements
- Assessment alignment
- Curriculum gap analysis

## Composition

**Input from**: `/curriculum.research`, `/curriculum.design`
**Works with**: `/standards.crosswalk-mapper`, `/learning.cultural-adaptation`
**Output to**: Internationally-aligned curriculum

## Exit Codes

- **0**: Standards alignment complete
- **1**: Framework not supported
- **2**: Insufficient content for alignment
- **3**: Grade level mismatch
