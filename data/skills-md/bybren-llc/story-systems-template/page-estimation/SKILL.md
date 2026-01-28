---
name: page-estimation
wtfbId: wtfb:page-estimation
description: |
  This skill provides screenplay page count and runtime estimation formulas.
  Covers the page-to-screen rule (1 page = 1 minute), genre adjustments,
  target lengths for features vs shorts, and element-based calculations.

  Use when: estimating screenplay length, calculating runtime, tracking
  page count, or validating target length for submission requirements.
---

# Page Estimation Skill

## Invocation Triggers
Apply this skill when:
- Estimating screenplay length
- Calculating runtime
- Tracking page count
- Validating target length

## The Page-to-Screen Rule

### Standard Formula
```
1 page of screenplay ≈ 1 minute of screen time
```

### Genre Adjustments
| Genre | Adjustment | Typical Length |
|-------|------------|----------------|
| Action | 0.8-0.9 min/page | 95-115 pages |
| Comedy | 1.0 min/page | 90-110 pages |
| Drama | 1.0-1.1 min/page | 100-120 pages |
| Thriller | 0.9-1.0 min/page | 100-115 pages |
| Horror | 0.9-1.0 min/page | 85-100 pages |
| Animation | 0.7-0.8 min/page | 75-95 pages |

### Why It Varies
- **Action-heavy scripts:** More white space, faster pace → shorter pages
- **Dialogue-heavy scripts:** Dense pages → longer runtime per page
- **Visual storytelling:** Less text, more subtext → varies

## Estimation Methods

### Method 1: Element Count
Rough estimate based on script elements:

```markdown
Scenes: 60 scenes × 1.5 pages avg = 90 pages
Adjustment for dialogue density: +10%
Estimated: ~99 pages
```

### Method 2: Word Count
```markdown
Total words: 20,000
Average screenplay: 180-200 words/page
Estimated: 20,000 ÷ 190 = 105 pages
```

### Method 3: Structural Estimate
```markdown
Act One (Setup): 25 pages
Act Two (Confrontation): 55 pages
Act Three (Resolution): 25 pages
Total: 105 pages
```

### Method 4: Scene-by-Scene
Most accurate:
```markdown
| Scene | Est. Pages |
|-------|-----------|
| 1 | 2 |
| 2 | 1.5 |
| 3 | 3 |
| ... | ... |
| Total | X |
```

## Fountain Page Count

### Title Page
- Always counts as page 1
- Not numbered in output
- Adds ~1 page to total

### Scene Headings
- Each scene heading takes ~2 lines
- 55-60 lines per page standard
- Many short scenes = more page overhead

### Dialogue vs. Action
- Dialogue: ~35-40 lines per page (narrower column)
- Action: ~55-60 lines per page (full width)
- Heavy dialogue = fewer scenes per page

### Elements That Add Length
- Dual dialogue (takes more vertical space)
- Parentheticals (extra lines)
- Transitions (blank lines before/after)
- Page breaks (forced `===`)

## Target Lengths

### Feature Films
| Market | Target | Range |
|--------|--------|-------|
| Studio | 110 | 100-120 |
| Indie | 95 | 85-110 |
| Spec | 105 | 95-115 |
| Comedy | 100 | 90-110 |

### Television
| Format | Target | Range |
|--------|--------|-------|
| Half-hour (single cam) | 30 | 25-35 |
| Half-hour (multi-cam) | 50 | 45-55 |
| One-hour drama | 55 | 50-65 |
| Limited series (episode) | 60 | 55-70 |

### Short Films
| Duration | Pages |
|----------|-------|
| 5 min | 5 |
| 10 min | 10 |
| 15 min | 15 |
| 20 min | 20 |

## Tracking Template

### Page Count Log
```markdown
## Page Tracking: [TITLE]

### Current Status
- **Total Pages:** [X]
- **Target:** [Y]
- **Variance:** [+/- Z]

### By Act
| Act | Pages | Target | Status |
|-----|-------|--------|--------|
| One | X | 25 | [over/under/ok] |
| Two | X | 55 | [over/under/ok] |
| Three | X | 25 | [over/under/ok] |

### Historical
| Date | Pages | Change | Note |
|------|-------|--------|------|
| 2025-12-20 | 85 | -- | First draft start |
| 2025-12-25 | 102 | +17 | First draft complete |
| 2025-12-27 | 98 | -4 | Trim pass |
```

## Runtime Calculation

### Formula
```
Runtime (minutes) = Pages × Genre Factor
```

### Calculator
```markdown
Pages: 105
Genre: Thriller (0.95)
Estimated Runtime: 105 × 0.95 = 99.75 minutes
Formatted: 1h 40m
```

### By Scene
```markdown
| Scene | Pages | Runtime |
|-------|-------|---------|
| 1 | 2 | 2 min |
| 2 | 3 | 3 min |
| ... | ... | ... |
| Total | 105 | 105 min |
```

## Adjusting Length

### Too Long
1. **Cut scenes:** Remove non-essential scenes
2. **Combine scenes:** Merge scenes with similar purpose
3. **Trim dialogue:** Reduce line count
4. **Tighten action:** Cut verbose descriptions
5. **Enter later/leave earlier:** Trim scene edges

### Too Short
1. **Add character moments:** Deepen relationships
2. **Expand key scenes:** Give weight to important moments
3. **Add B-story:** Strengthen subplots
4. **Develop obstacles:** More complications
5. **Add breathing room:** Moments of reflection

### Red Flags
- Feature spec over 120 pages: Instant rejection risk
- Feature spec under 90 pages: Feels slight
- TV spec off by more than 5 pages: Format unfamiliarity

## Quick Reference

### Scene Page Estimates
| Scene Type | Typical Length |
|------------|---------------|
| Short dialogue | 1/2 - 1 page |
| Standard dialogue | 2 - 3 pages |
| Action sequence | 3 - 5 pages |
| Major confrontation | 4 - 6 pages |
| Montage | 1 - 2 pages |
| Establishing | 1/4 - 1/2 page |

### Structural Landmarks (110-page feature)
| Beat | Target Page |
|------|-------------|
| Catalyst | 10-12 |
| Break Into Two | 25 |
| Midpoint | 55 |
| All Is Lost | 75 |
| Break Into Three | 85 |
| Climax | 100-105 |
| Resolution | 105-110 |

## Validation Checklist
- [ ] Total pages within target range
- [ ] Acts properly proportioned
- [ ] No single act dominates
- [ ] Pacing feels appropriate
- [ ] Runtime estimate matches target
