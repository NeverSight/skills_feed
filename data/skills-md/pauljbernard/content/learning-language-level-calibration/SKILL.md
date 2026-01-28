---
name: learning-language-level-calibration
description: Assess content difficulty by language proficiency level, calibrate reading level for multilingual learners, adapt content for language proficiency, and design language scaffolding. Use when creating content for non-native speakers. Activates on "language level", "proficiency calibration", "readability", or "language learners".
---

# Learning Language Level Calibration

Calibrate educational content difficulty for language proficiency levels and multilingual learners.

## When to Use

- Creating content for English Language Learners (ELL/ESL)
- Adapting for multilingual classrooms
- Language-sensitive subject instruction
- Supporting non-native speakers
- International student programs

## Proficiency Frameworks

### CEFR Levels (Common European Framework)

- **A1** (Beginner): Basic phrases, simple interactions
- **A2** (Elementary): Routine tasks, simple descriptions
- **B1** (Intermediate): Main points of clear input, workplace basics
- **B2** (Upper Intermediate): Complex text, spontaneous interaction
- **C1** (Advanced): Implicit meaning, flexible language use
- **C2** (Proficient): Subtle distinctions, near-native fluency

### Other Frameworks

- ACTFL (American Council): Novice, Intermediate, Advanced, Superior, Distinguished
- ILR (Interagency Language Roundtable): 0-5 scale
- Cambridge English: KET, PET, FCE, CAE, CPE

## Calibration Factors

### Vocabulary Complexity

**Word Frequency**:
- A1-A2: Most frequent 1,000-2,000 words
- B1-B2: 3,000-5,000 words
- C1-C2: 8,000+ words, academic vocabulary

**Technical Terms**:
- Glossary support needed
- Visual aids
- Translations or explanations

### Sentence Structure

**Complexity by Level**:
- A1-A2: Simple sentences, present tense focus
- B1-B2: Compound sentences, various tenses
- C1-C2: Complex subordination, passive voice, conditionals

### Text Length

**Appropriate Length**:
- A1: 50-100 words per section
- B1: 200-300 words
- C1: 500+ words, longer paragraphs

### Cultural Load

**Background Knowledge**:
- Explicit cultural references
- Idioms and expressions
- Implicit meanings

## Adaptation Strategies

### Simplification

**Techniques**:
- Break long sentences
- Use active voice
- Replace rare words with common alternatives
- Add visual supports
- Provide glossaries

### Scaffolding

**Language Supports**:
- Sentence frames
- Word banks
- Graphic organizers
- Multilingual glossaries
- Translation aids (strategic, not crutches)

## CLI Interface

```bash
# Assess content level
/learning.language-level-calibration --content "lesson.md" --estimate-level

# Adapt to target level
/learning.language-level-calibration --content "advanced-text.md" --target-level "B1" --output simplified.md

# Create scaffolded versions
/learning.language-level-calibration --content "article.md" --levels "A2,B1,B2,C1" --output levels/

# Readability metrics
/learning.language-level-calibration --content "course/" --metrics "CEFR,Flesch-Kincaid,Lexile"
```

## Output

- Language proficiency level assessment
- Vocabulary analysis (frequency, academic word list)
- Sentence complexity metrics
- Adapted content at target levels
- Scaffolding recommendations

## Composition

**Input from**: `/curriculum.develop-content`, `/learning.translation`
**Works with**: `/learning.cefr-alignment`, `/curriculum.review-accessibility`
**Output to**: Language-calibrated learning materials

## Exit Codes

- **0**: Calibration complete
- **1**: Content too complex to simplify
- **2**: Target level incompatible with content
