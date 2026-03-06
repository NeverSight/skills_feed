---
name: meta-manuscript-assembly
description: Assemble publication-ready meta-analysis manuscripts with tables, figures, and references. Use when completing systematic review/meta-analysis manuscripts for journal submission.
context: fork
agent: general-purpose
---

# Meta-Analysis Manuscript Assembly

Complete systematic review and meta-analysis manuscripts for journal submission by creating publication-ready tables, figures, and references.

## When to Use

- Completing meta-analysis manuscript after analyses are done
- Creating tables from meta-analysis results
- Assembling multi-panel figures from forest/funnel plots
- Generating BibTeX references for systematic reviews
- Formatting manuscripts for high-impact journals (Lancet, JAMA, NEJM)

## Prerequisites

Before using this skill, ensure you have:

- Completed meta-analyses with results tables (CSV format)
- Generated individual figures (PNG at 300 DPI)
- Manuscript text sections written (Abstract, Introduction, Methods, Results, Discussion)
- List of all citations needed

## Workflow

### Phase 1: Tables Creation

Create comprehensive tables from analysis results:

#### Main Text Tables

1. **Table 1: Trial Characteristics**
   - Extract from extraction.csv or similar
   - Include: NCT number, first author, year, design, sample sizes, intervention details, follow-up
   - Format as markdown with abbreviations section

2. **Table 2: Efficacy Outcomes Summary**
   - Combine results from all meta-analyses (pCR, survival outcomes)
   - Include: effect estimates, 95% CI, p-values, I², absolute benefits, NNT
   - Add GRADE certainty ratings

3. **Table 3: Safety Outcomes Summary**
   - From safety meta-analysis results
   - Include: adverse events, rates, RR/OR, NNH
   - Add clinical management guidance

#### Supplementary Tables

4. **Risk of Bias Assessment**
   - Use RoB 2 or ROBINS-I tool format
   - Domain-by-domain assessment for each trial
   - Overall risk rating with justifications

5. **GRADE Evidence Profile**
   - Summary of Findings table format
   - All outcomes with certainty ratings
   - Domain-specific justifications (bias, inconsistency, indirectness, imprecision)

6. **Detailed Results Tables**
   - Individual trial results
   - Subgroup analyses
   - Sensitivity analyses

### Phase 2: Figure Assembly

Create multi-panel publication-ready figures:

#### Tool: Python Script with PIL/Pillow

```python
# Create assemble_figures.py
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def add_panel_label(img, label, position='top-left', font_size=80, offset=(40, 40)):
    """Add A, B, C labels to panels"""
    draw = ImageDraw.Draw(img)

    # Try to use system font
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        font = ImageFont.load_default()

    x, y = offset

    # Draw white background box for visibility
    bbox = draw.textbbox((x, y), label, font=font)
    padding = 10
    draw.rectangle(
        [bbox[0] - padding, bbox[1] - padding,
         bbox[2] + padding, bbox[3] + padding],
        fill='white',
        outline='black',
        width=2
    )

    draw.text((x, y), label, fill='black', font=font)
    return img

def create_multi_panel_figure(images_list, output_path, labels=['A', 'B', 'C'], spacing=40):
    """Combine multiple images vertically with labels"""
    # Add labels to images
    labeled_images = [add_panel_label(img, label) for img, label in zip(images_list, labels)]

    # Calculate dimensions
    max_width = max(img.width for img in labeled_images)
    total_height = sum(img.height for img in labeled_images) + spacing * (len(labeled_images) - 1)

    # Create combined image
    combined = Image.new('RGB', (max_width, total_height), 'white')

    # Paste images
    y_offset = 0
    for img in labeled_images:
        combined.paste(img, (0, y_offset))
        y_offset += img.height + spacing

    # Save at 300 DPI
    combined.save(output_path, dpi=(300, 300))
    return output_path
```

#### Typical Figure Structure

**Main Text:**

- Figure 1: Multi-panel efficacy (pCR, EFS, OS forest plots)
- Figure 2: Subgroup analysis (e.g., by biomarker status)
- Figure 3: Safety + Publication bias (SAE forest plot, funnel plot)

**Supplementary:**

- Supp Figure 1: Sensitivity analyses (leave-one-out plots)
- Supp Figure 2: Publication bias (funnel plots for all outcomes)

### Phase 3: References Management

Create comprehensive BibTeX file:

#### Steps:

1. **Extract all citations** from manuscript using grep

   ```bash
   grep -E "¹|²|³|⁴|⁵|⁶|⁷|⁸|⁹|⁰|\[\d+\]" manuscript_sections.md
   ```

2. **Create BibTeX entries** for each reference
   - Include DOI for all entries
   - Use standardized journal abbreviations (Index Medicus)
   - Format author names correctly

3. **Create mapping document**
   - Map superscripts (¹, ², ³) to BibTeX keys
   - Document citation locations in manuscript

4. **Create usage guide**
   - Pandoc conversion instructions
   - Zotero import instructions
   - Manual formatting examples (Lancet, JAMA style)

### Phase 4: Figure Legends

Write comprehensive legends for all figures:

#### Legend Structure:

```markdown
**Panel A. Outcome Name**
Description of what the panel shows. Forest plot showing [effect measure] for [outcome]
across [N] trials ([total participants]). [Statistical method used]. [Key result].
Horizontal lines represent 95% confidence intervals; diamond represents pooled effect.
Vertical line at [null value] indicates no treatment effect.

**Abbreviations**: List all abbreviations used.
```

Include:

- Statistical methods (random-effects, Hartung-Knapp adjustment)
- Heterogeneity measures (I², Cochran's Q)
- Clinical interpretations
- Abbreviations definitions

### Phase 5: Quality Assurance

Before submission, verify:

#### Tables

- [ ] All data matches analysis results exactly
- [ ] Abbreviations defined
- [ ] Footnotes explain all symbols
- [ ] Column/row headers clear
- [ ] Statistical notation consistent

#### Figures

- [ ] All figures at 300 DPI minimum
- [ ] Panel labels (A, B, C) visible and not obscuring data
- [ ] Legends match figures exactly
- [ ] Font sizes readable (≥8pt for final print size)
- [ ] Color schemes work in grayscale

#### References

- [ ] All citations have corresponding references
- [ ] Reference numbers sequential
- [ ] DOIs correct and working
- [ ] Journal abbreviations standardized
- [ ] Author names match original publications

## Output Structure

```
07_manuscript/
├── tables/
│   ├── Table1_Trial_Characteristics.md
│   ├── Table2_Efficacy_Summary.md
│   ├── Table3_Safety_Summary.md
│   ├── SupplementaryTable1_RiskOfBias.md
│   ├── SupplementaryTable2_GRADE_Profile.md
│   └── ...
├── figures/
│   ├── Figure1_Efficacy.png (300 DPI)
│   ├── Figure2_Subgroup.png (300 DPI)
│   ├── Figure3_Safety.png (300 DPI)
│   ├── SupplementaryFigure1_Sensitivity.png
│   └── ...
├── references.bib
├── FIGURE_LEGENDS.md
├── CITATION_MAPPING.md
└── REFERENCES_USAGE_GUIDE.md
```

## Time Estimates

- Tables creation: 2-3 hours
- Figure assembly: 1-2 hours
- References: 1-2 hours
- Legends: 1 hour
- QA: 1 hour
- **Total: 6-9 hours**

## Journal-Specific Formatting

### Lancet Oncology

- Word limit: 4000-5000 words
- Tables: 3-4 main text, unlimited supplementary
- Figures: 3-4 main text, unlimited supplementary
- References: Vancouver style, 30-40 typical
- Resolution: 300 DPI minimum

### JAMA

- Word limit: 3500 words
- Tables: 4 max
- Figures: 4 max
- References: 40 max
- Resolution: 300-600 DPI

### New England Journal of Medicine

- Word limit: 3000 words
- Tables: 3 max
- Figures: 3 max
- References: 40 max
- Resolution: 300 DPI minimum

## Common Pitfalls to Avoid

1. **Tables**: Don't mix effect measures (RR vs OR vs HR) without clear labeling
2. **Figures**: Don't compress below 300 DPI
3. **References**: Don't use auto-generated citations without verification
4. **Legends**: Don't omit statistical methods or abbreviations
5. **Overall**: Don't submit without independent verification of all numbers

## Related Skills

- `/meta-analysis` - Perform the statistical analyses
- `/prisma-flow` - Create PRISMA flow diagram
- `/grade-assessment` - Complete GRADE evidence profiles
- `/risk-of-bias` - Assess trial quality with RoB 2 tool

## Example Invocation

```
/meta-manuscript-assembly
```

Or with specific phase:

```
/meta-manuscript-assembly tables
/meta-manuscript-assembly figures
/meta-manuscript-assembly references
```

## Success Criteria

- ✅ All tables publication-ready with comprehensive notes
- ✅ All figures 300 DPI with professional panel labels
- ✅ Complete BibTeX file with all 30-40 references
- ✅ Comprehensive figure legends
- ✅ All numbers verified against original analyses
- ✅ Manuscript follows target journal guidelines
- ✅ Ready for co-author review and submission
