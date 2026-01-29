---
name: openjung-api
description: |
  Guide for integrating with the OpenJung (OEJTS) personality test API - a free, open-source alternative to MBTI.
  Use when building applications that need personality assessment, integrating MBTI-style tests, or working with
  the OpenMBTI API endpoints. Covers: (1) Fetching test questions, (2) Submitting answers and calculating results,
  (3) Understanding the scoring system, (4) Recording test sessions, (5) Retrieving aggregate statistics.
---

# OpenJung API Integration

OpenJung is an open-source personality test based on OEJTS (Open Extended Jungian Type Scales) - a validated 32-question assessment that determines MBTI-compatible personality types.

**Base URL**: `https://openmbti.org`

## Quick Start

### Minimal Integration (3 Steps)

```javascript
// 1. Fetch questions
const { questions } = await fetch('https://openmbti.org/api/questions').then(r => r.json());

// 2. Collect user answers (32 questions, values 1-5)
const answers = { "1": 3, "2": 5, /* ... all 32 */ "32": 4 };

// 3. Calculate result
const { result } = await fetch('https://openmbti.org/api/calculate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ answers })
}).then(r => r.json());

console.log(result.type); // "ENFP"
```

## API Endpoints

### GET /api/questions

Fetch all 32 test questions.

```
GET /api/questions?locale=en
```

**Response:**
```json
{
  "totalQuestions": 32,
  "questions": [
    {
      "id": 1,
      "dimension": "JP",
      "leftTrait": "Makes lists",
      "rightTrait": "Relies on memory"
    }
  ]
}
```

### POST /api/calculate

Calculate personality type from answers.

```javascript
POST /api/calculate
{
  "answers": { "1": 3, "2": 5, ... "32": 4 },
  "locale": "en",    // optional
  "save": true       // optional - saves to database
}
```

**Response:**
```json
{
  "result": {
    "type": "ENFP",
    "scores": { "EI": 18, "SN": 28, "TF": 22, "JP": 32 },
    "percentages": { "E": 75, "I": 25, "S": 12, "N": 88, "T": 31, "F": 69, "J": 0, "P": 100 },
    "typeInfo": {
      "name": "Campaigner",
      "description": "...",
      "strengths": ["..."],
      "weaknesses": ["..."]
    },
    "shareUrl": "https://openmbti.org/type/enfp?ei=18&sn=28&tf=22&jp=32"
  },
  "recordId": "uuid"
}
```

### POST /api/record

Record a completed test result (fire-and-forget).

```javascript
POST /api/record
{
  "answers": { ... },
  "result": { "type": "ENFP", "scores": {...}, "percentages": {...} }
}
```

### GET /api/stats

Get aggregate test statistics.

```json
{
  "totalTests": 15234,
  "typeDistribution": [{ "type": "INFP", "count": 2341 }],
  "localeDistribution": [{ "locale": "en", "count": 8234 }]
}
```

## Scoring System

**Scale**: 1-5 Likert (1 = strongly left trait, 5 = strongly right trait)

**Dimensions** (8 questions each):
- **EI**: Extroversion (E) ↔ Introversion (I)
- **SN**: Sensing (S) ↔ Intuition (N)
- **TF**: Thinking (T) ↔ Feeling (F)
- **JP**: Judging (J) ↔ Perceiving (P)

**Score Range**: 8-40 per dimension (8 questions × 1-5 scale)

**Threshold**: 24 (midpoint)
- Score ≤ 24 → left preference (E, S, F, J)
- Score > 24 → right preference (I, N, T, P)

**Note**: TF dimension is inverted - low score = F (Feeling), high = T (Thinking)

## Question Mapping

| Dimension | Question IDs |
|-----------|--------------|
| JP | 1, 5, 9, 13, 17, 21, 25, 29 |
| TF | 2, 6, 10, 14, 18, 22, 26, 30 |
| EI | 3, 7, 11, 15, 19, 23, 27, 31 |
| SN | 4, 8, 12, 16, 20, 24, 28, 32 |

## Localization

44 languages supported. Pass `locale` parameter to endpoints:
- `en` (English), `zh` (Simplified Chinese), `ja` (Japanese), `ko` (Korean)
- `es` (Spanish), `fr` (French), `de` (German), `pt` (Portuguese)
- And 36 more...

## Error Handling

| Error Code | Description |
|------------|-------------|
| `INVALID_BODY` | Malformed JSON |
| `INVALID_PARAMS` | Missing/wrong answers format |
| `INCOMPLETE_ANSWERS` | Not all 32 questions answered |
| `CALCULATION_FAILED` | Server error |

## Resources

For detailed API specifications and TypeScript types, see [references/api_reference.md](references/api_reference.md).
