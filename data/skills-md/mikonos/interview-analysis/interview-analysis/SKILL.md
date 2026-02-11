---
name: interview-analysis
description: Deep interview analysis using dynamic expert routing. Automatically selects top domain thinkers based on role type to distinguish genuine capability from performance, identifying Battle Scars over Methodology Recitation. Applicable to any professional position including product management, engineering, design, operations, sales, and data science.
---

# Interview Analysis Skill

> **Core Mission**: Transform interview transcripts into deep insights.
> **Core Logic**: Don't listen to what candidates "say" (Methodology Recitation), observe what they've "done" (Battle Scars) and "how they think" (First Principles).

## 1. Dynamic Expert Activation (Expert Routing)

### Core Principle
Based on **role type** and **evaluation dimensions**, automatically select the **best minds** combination for that domain:

**Three-Step Expert Selection**:
1. **Identify core competency domain**: Product/Engineering/Operations/Design/Sales/Data Science/...
2. **Match top domain thinkers**: Recognized methodology masters or practitioners in the field
3. **Combine hiring experts**: Geoff Smart (fact-checking) + Lou Adler (competency validation)

### Common Role-Expert Mapping (Non-Exhaustive)

| Role Type | Domain Expert (Methodology) | Hiring Expert (Validation) | Rationale |
|-----------|---------------------------|---------------------------|-----------|
| **Product Manager** | Marty Cagan / Julie Zhuo | Geoff Smart | Product Sense + Fact Check |
| **Software Engineer** | Linus Torvalds / John Carmack | Lou Adler | Engineering Judgment + Results Validation |
| **Growth Hacker** | Sean Ellis / Brian Balfour | Geoff Smart | Growth Methodology + Metrics Verification |
| **UX Designer** | Don Norman / Jony Ive | Lou Adler | UX Principles + Portfolio Validation |
| **Data Scientist** | Andrew Ng / DJ Patil | Geoff Smart | Technical Depth + Project Verification |
| **Operations** | Sheryl Sandberg / Reid Hoffman | Lou Adler | Scale Operations + Results Focus |
| **Sales/BD** | Aaron Ross / Jill Konrath | Geoff Smart | Sales Methodology + Performance Verification |

> [!IMPORTANT]
> **Flexibility Principle**: The table above is for reference only. Flexibly select the most appropriate expert combination based on specific role and candidate background.
> 
> **Encourage Innovation**: If you believe a non-mainstream expert is better suited to evaluate this candidate, make that choice and explain your rationale.
> 
> **Core Question**: "Who can best identify imposters in this role? Whose framework best validates core competencies?"

## 2. Execution Workflow

### Step 1: Fact Reconstruction & Red Flag Scan
*   **Timeline Reconstruction**: Connect experiences scattered across multiple interview rounds, checking for logical gaps.
*   **Consistency Verification**: Compare different versions of the same story told to different interviewers (e.g., reasons for leaving, project failures).
*   **Red Flag Annotation**: Mark all vague titles (e.g., SPM), exaggerated data, and attribution fallacies ("it was all market/technology's fault").

### Step 2: Deep Decoding - STAR Episodes
*   **Tactic**: Select 1-2 core cases (e.g., startup project, most challenging project) for microscopic analysis.
*   **Truth Extraction**:
    *   **Methodology Check**: Is the candidate reciting SOPs (MECE, SWOT) or applying first principles?
    *   **Solution Bias Check**: Did they jump straight to "add features," or first conduct "value validation"?
    *   **Technical Boundary Check**: For technical challenges, did they "deflect blame" or "anticipate"?

### Step 3: Interviewer Meta-Analysis
*   **Subject**: Evaluate interviewer (you/colleagues) performance.
*   **Dimensions**:
    *   **Depth**: Did they probe at critical moments? Or let it pass?
    *   **Bias**: Did they draw conclusions too early or ask leading questions?
    *   **Bar**: Did they maintain A Player standards?

### Step 4: Card-based Output (Zettelkasten Output)
Generate Markdown cards using the following standard templates, saved to `people/{candidate_name}/analysis/`. Be sure to read template content before filling in analysis results.

*   **Profile (Comprehensive Portrait)**:
    *   Template path: `templates/profile_template.md`
    *   Purpose: Fact checking, red flag scanning, core competency assessment.
*   **Insight (Deep Analysis)**:
    *   Template path: `templates/insight_template.md`
    *   Purpose: Deep dive into specific domains (e.g., AI Capability, Product Strategy).
*   **Meta-Analysis (Interviewer Review)**:
    *   Template path: `templates/evaluation_template.md`
    *   Purpose: Evaluate interviewer performance and organizational recommendations.
*   **Structure Note (Hub Document)**:
    *   Template path: `templates/structure_note_template.md`
    *   Purpose: Serves as hub connecting all analysis cards above, forming decision closure.

## 3. Usage Examples

*   "Analyze Li Yashuang's three interview rounds, focusing on AI capabilities."
*   "Review this interview to see where we interviewers did well and where we missed opportunities."
*   "Use Marty Cagan's perspective to analyze this candidate's product thinking."
