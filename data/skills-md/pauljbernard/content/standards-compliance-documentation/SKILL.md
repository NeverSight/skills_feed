---
name: standards-compliance-documentation
description: Generate professional standards alignment documentation for board presentations, curriculum reviews, accreditation reports, grant proposals, and administrator reviews. Use for stakeholder communication. Activates on "compliance documentation", "board report", or "standards report".
---

# Standards: Compliance Documentation

Generate professional documentation demonstrating standards compliance for various stakeholders and purposes.

## When to Use

- Board of education presentations
- Curriculum adoption reviews
- Accreditation self-studies
- Grant proposal applications
- State reporting requirements
- Parent/community communication
- Administrator reviews

## Documentation Types

### 1. Board Presentations

**Audience**: School board members, community

**Format**: Slide deck (PowerPoint/PDF)

**Content**:
- Executive summary (1 slide)
- Standards coverage overview with visuals
- Comparison to peer districts
- Assessment alignment summary
- Budget implications (if relevant)
- Recommendation and next steps

**Length**: 10-15 slides, 15-20 minute presentation

**Style**: High-level, visual, non-technical

### 2. Curriculum Review Documents

**Audience**: Curriculum committees, administrators

**Format**: Detailed report (Word/PDF)

**Content**:
- Program overview
- Standards crosswalk (detailed table)
- Scope and sequence
- Assessment blueprint
- Instructional materials list
- Professional development needs
- Implementation timeline

**Length**: 20-50 pages

**Style**: Comprehensive, technical, evidenced-based

### 3. Accreditation Reports

**Audience**: Accreditation bodies (regional, state)

**Format**: Formal report with appendices

**Content**:
- Standards alignment evidence
- Assessment data and analysis
- Curriculum maps
- Sample assessments with rubrics
- Teacher qualification documentation
- Professional development records
- Continuous improvement plans

**Length**: 50-100+ pages

**Style**: Formal, compliance-focused, evidence-heavy

### 4. Grant Proposals

**Audience**: Funders (federal, state, foundation)

**Format**: Proposal with attachments

**Content**:
- Needs statement (standards gaps)
- Proposed solution (how grant addresses gaps)
- Standards alignment of new program
- Expected outcomes with metrics
- Budget narrative tied to standards
- Evaluation plan

**Length**: 10-30 pages + appendices

**Style**: Persuasive, data-driven, outcome-focused

### 5. State Reporting

**Audience**: State education department

**Format**: Required templates/forms

**Content**:
- Standards coverage certification
- Textbook/materials list with ISBN
- Teacher qualifications
- Assessment results by standard
- Instructional minutes by subject

**Length**: Varies by state

**Style**: Compliance-focused, template-driven

### 6. Parent/Community Communication

**Audience**: Parents, community members

**Format**: One-page summary, FAQ, website content

**Content**:
- "What are [state] standards?"
- "How does our curriculum align?"
- "How will we know students are learning?"
- "What support is available?"
- "How can parents help?"

**Length**: 1-4 pages

**Style**: Accessible, non-technical, reassuring

## Documentation Components

### Standard Elements

**Include in Most Reports**:
1. **Cover page**: Title, date, authors, organization
2. **Executive summary**: Key findings, 1-2 pages
3. **Introduction**: Purpose, scope, methodology
4. **Standards overview**: Which frameworks, why these standards
5. **Alignment evidence**: Tables, matrices, examples
6. **Data/outcomes**: Assessment results, success metrics
7. **Recommendations**: Next steps, improvements
8. **Appendices**: Detailed crosswalks, sample materials

### Visual Elements

**Effective Visualizations**:
- **Coverage charts**: Pie charts, bar graphs showing % by strand
- **Timeline/Gantt charts**: Implementation schedule
- **Comparison tables**: Program A vs. B, before vs. after
- **Heat maps**: Coverage intensity by standard
- **Flowcharts**: Curriculum sequence, decision trees

### Evidence Examples

**Strengthen Documentation**:
- **Sample lessons** with standards tags
- **Assessment items** mapped to standards
- **Student work samples** demonstrating proficiency
- **Teacher surveys** on implementation
- **Student performance data** by standard

## Quality Criteria

### Professional Standards

**Formatting**:
- Consistent fonts, headers, footers
- Page numbers
- Table of contents for long documents
- Clear section headings
- White space for readability

**Writing**:
- Clear, concise language
- Active voice
- Defined acronyms
- Consistent terminology
- Proofread (no errors)

**Data Integrity**:
- Accurate alignment claims
- Current data
- Cited sources
- Verifiable evidence

## Templates by Purpose

### Board Presentation Outline

1. Title slide
2. Purpose and overview
3. Standards landscape (state/national context)
4. Current state assessment
5. Coverage analysis (visual)
6. Depth and rigor summary
7. Assessment alignment
8. Comparison data (if available)
9. Strengths
10. Areas for improvement
11. Budget considerations
12. Recommendations
13. Implementation timeline
14. Questions/discussion

### Grant Proposal Outline

1. Abstract
2. Needs statement (standards gaps)
3. Project description (how addressing gaps)
4. Standards alignment table
5. Goals and objectives (SMART)
6. Methods and activities
7. Evaluation plan
8. Dissemination
9. Budget and justification
10. Organizational capacity
11. Appendices (letters of support, CVs, etc.)

## CLI Interface

```bash
# Board presentation
/standards.compliance-documentation --curriculum "district-math/" --standards "CCSS-Math-K-8" --format "board-presentation" --output board-deck.pptx

# Curriculum review
/standards.compliance-documentation --program "science-curriculum/" --standards "NGSS" --format "curriculum-review" --output review-document.pdf

# Accreditation report
/standards.compliance-documentation --all-programs "k-12-curricula/" --accreditation "AdvancED" --comprehensive-report --output accreditation-package/

# Grant proposal
/standards.compliance-documentation --need "math-intervention" --standards "State-Math-3-5" --format "grant-proposal" --funder "State-Ed-Grant" --output grant-proposal.docx

# State reporting
/standards.compliance-documentation --curriculum "ela-6-8/" --format "state-report" --state "Texas" --template "TEA-curriculum-cert.xlsx"

# Parent communication
/standards.compliance-documentation --curriculum "elementary-math/" --format "parent-guide" --output parent-standards-guide.pdf --simple-language
```

## Output

- Professional formatted documents
- Slide decks with visuals
- Detailed crosswalks and tables
- Evidence appendices
- Compliance certifications
- Stakeholder-appropriate summaries

## Composition

**Input from**: `/standards.coverage-validator`, `/standards.us-state-mapper`, `/curriculum.analyze-outcomes`
**Final step** after: All standards validation complete
**Output to**: Stakeholders, accreditation bodies, funders

## Exit Codes

- **0**: Documentation generated successfully
- **1**: Insufficient data for requested format
- **2**: Template not available
- **3**: Validation must pass before documentation
