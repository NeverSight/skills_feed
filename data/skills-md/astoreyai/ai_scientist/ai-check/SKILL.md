---
name: ai-check
description: "Detect AI/LLM-generated text patterns in research writing. Use when: (1) Reviewing manuscript drafts before submission, (2) Pre-commit validation of documentation, (3) Quality assurance checks on research artifacts, (4) Ensuring natural academic writing style, (5) Tracking writing authenticity over time. Analyzes grammar perfection, sentence uniformity, paragraph structure, word frequency (AI-typical words like 'delve', 'leverage', 'robust'), punctuation patterns, and transition word overuse."
allowed-tools: Read, Grep, Bash
version: 1.0.0
---

# AI-Generated Text Detection Skill

## Purpose

Detect patterns typical of LLM-generated text to ensure natural, human-authored academic writing. This skill helps maintain authenticity in research publications, dissertations, and documentation.

## When to Use This Skill

### Primary Use Cases
1. **Pre-Commit Validation** - Automatically check manuscripts and documentation before git commits
2. **Manuscript Review** - Validate academic writing before submission to journals or committees  
3. **Quality Assurance** - Part of systematic QA workflow for research artifacts
4. **On-Demand Analysis** - Manual review of any text file for AI patterns
5. **Writing Evolution Tracking** - Monitor writing style changes over time

### Specific Scenarios
- Before submitting dissertation chapters to advisor
- Prior to journal article submission
- When reviewing team member contributions
- After making significant edits to documentation
- When suspicious patterns are noticed in writing
- During peer review or committee review preparation

## Detection Methodology

### 1. Grammar Pattern Analysis

**What We Check:**
- **Excessive Perfection**: Zero typos, missing commas, or minor errors throughout
- **Comma Placement**: Perfect comma usage in all complex sentences
- **Formal Register**: Consistent formal tone with no informal elements
- **Grammar Consistency**: No variations in grammatical choices

**Red Flags:**
- Absolutely no grammatical errors in 10+ pages
- Every semicolon and colon used perfectly
- No sentence fragments or run-ons even in appropriate contexts
- Overly formal language even in methods sections

**Human Writing Typically Has:**
- Occasional minor typos or comma splices
- Some inconsistency in formality
- Natural variations in grammar choices
- Context-appropriate informality

### 2. Sentence Structure Uniformity

**What We Check:**
- **Sentence Length Distribution**: Variation in sentence lengths
- **Structural Patterns**: Repetitive sentence structures
- **Complexity Variation**: Mix of simple, compound, complex sentences
- **Opening Patterns**: How sentences begin

**Red Flags:**
- Most sentences 15-25 words (AI sweet spot)
- Repetitive subject-verb-object patterns
- Every paragraph starts with topic sentence
- Excessive use of transition words at sentence starts
- Predictable sentence complexity patterns

**Human Writing Typically Has:**
- Wide variation (5-40+ word sentences)
- Unpredictable sentence structures
- Occasional fragments for emphasis
- Natural flow without forced transitions

### 3. Paragraph Structure Analysis

**What We Check:**
- **Paragraph Length**: Uniformity vs. natural variation
- **Structural Pattern**: Topic sentence + support + conclusion pattern
- **Information Flow**: Natural vs. algorithmic organization
- **Paragraph Transitions**: Connection between paragraphs

**Red Flags:**
- All paragraphs 4-6 sentences long
- Every paragraph follows same structure  
- Mechanical transitions between paragraphs
- Perfectly balanced paragraph lengths
- No single-sentence paragraphs

**Human Writing Typically Has:**
- Paragraph length variation (1-10+ sentences)
- Structural diversity based on content
- Natural transitions
- Strategic use of short/long paragraphs for emphasis

### 4. Word Frequency Analysis (AI-Typical Words)

**High-Risk AI Words** (overused by LLMs):

**Verbs:**
- "delve" (rarely used by humans)
- "leverage" (business jargon)
- "utilize" (instead of "use")
- "facilitate" (overly formal)
- "demonstrate" (overused)
- "implement" (in non-technical contexts)
- "enhance" (marketing language)

**Adjectives:**
- "robust" (technical overuse)
- "comprehensive" (vague intensifier)
- "innovative" (buzzword)
- "cutting-edge" (cliché)
- "significant" (statistical overuse)
- "substantial" (formal overuse)
- "considerable" (formal overuse)
- "crucial" (intensity overuse)

**Transition Words** (overused):
- "furthermore" (very formal)
- "moreover" (archaic feeling)
- "additionally" (redundant)
- "consequently" (overused)
- "subsequently" (temporal overuse)
- "nevertheless" (formal overuse)
- "nonetheless" (synonym overuse)

**Phrases:**
- "it is important to note that"
- "it should be emphasized that"
- "a comprehensive analysis of"
- "in the context of"
- "with respect to"
- "in terms of"
- "in order to" (instead of "to")

**Detection Criteria:**
- Count frequency per 1000 words
- Compare to human academic writing baselines
- Flag if 3+ high-risk words per 1000 words
- Weight by word rarity (delve = high weight)

### 5. Punctuation Patterns

**What We Check:**
- **Semicolon Usage**: Frequency and correctness
- **Colon Usage**: Perfect usage patterns
- **Em-Dash Usage**: Consistent stylistic choices
- **Comma Patterns**: Perfection vs. natural variation
- **Ellipsis/Exclamation**: Absence in informal contexts

**Red Flags:**
- Excessive semicolon use (2+ per paragraph)
- Perfect colon usage throughout
- Consistent em-dash formatting (—)
- No missing commas anywhere
- Zero informal punctuation

**Human Writing Typically Has:**
- Inconsistent punctuation choices
- Occasional missing/extra commas
- Variable dash formatting (- vs -- vs —)
- Some informal punctuation where appropriate

## Confidence Scoring System

### Scoring Formula

**Overall Confidence** = Weighted average of:
- Grammar perfection: 20%
- Sentence uniformity: 25%
- Paragraph structure: 20%
- AI-typical words: 25%
- Punctuation patterns: 10%

Each metric scored 0-100, then combined with weights.

### Confidence Levels

#### Low Confidence (0-30%): Likely Human Writing
**Characteristics:**
- Natural sentence length variation (5-40+ words)
- Occasional grammatical imperfections
- Authentic voice and natural flow
- Domain-specific terminology used naturally
- Structural variety in paragraphs
- Minimal AI-typical words (0-2 per 1000 words)

**Action:** ✅ Writing appears authentic, no changes needed

#### Medium Confidence (30-70%): Possible AI Assistance
**Characteristics:**
- Some uniformity in sentence structure
- Mix of AI-typical and natural patterns
- May be human-edited AI output
- Overly formal in places
- Some transition word overuse
- 3-5 AI-typical words per 1000 words

**Action:** ⚠️ Review flagged sections, apply suggestions selectively

**Examples of Mixed Writing:**
- AI-generated first draft with heavy human editing
- Human writing that mimics academic formality excessively
- Non-native English speakers using formal templates
- Multiple authors with different styles

#### High Confidence (70-100%): Likely AI-Generated
**Characteristics:**
- Excessive uniformity across all metrics
- Multiple AI-typical word clusters
- Perfect grammar and punctuation throughout
- Artificial transition patterns
- Mechanical paragraph structure
- 6+ AI-typical words per 1000 words

**Action:** 🚫 Significant revision needed, rewrite in authentic voice

## Output Format

When running AI-check analysis, generate a comprehensive report:

### 1. Executive Summary
```
Overall Confidence Score: 65%
Status: MEDIUM - Possible AI assistance detected
Files Analyzed: 1
Total Words: 3,456
Recommendation: Review flagged sections
```

### 2. Metric Breakdown
```
Grammar Perfection:     85% (High - suspiciously few errors)
Sentence Uniformity:    72% (High - repetitive structures)
Paragraph Structure:    68% (Medium - some variation)
AI-Typical Words:       58% (Medium - 4.2 per 1000 words)
Punctuation Patterns:   45% (Low - natural variation)
```

### 3. Flagged Sections
```
Lines 45-67 (Confidence: 82%)
  Pattern: Excessive transition words + uniform sentences
  AI Words: "moreover", "furthermore", "leverage", "robust"
  
Lines 112-134 (Confidence: 76%)
  Pattern: Perfect grammar + mechanical structure
  AI Words: "delve", "comprehensive", "facilitate"
```

### 4. Specific Issues Detected
```
High-Risk AI Words Found (per 1000 words):
  • "delve" (2 occurrences) - RARELY used by humans
  • "leverage" (3 occurrences) - Business jargon overuse
  • "robust" (4 occurrences) - Technical overuse
  • "furthermore" (6 occurrences) - Formal transition overuse

Sentence Uniformity Issues:
  • 67% of sentences are 15-25 words (AI sweet spot)
  • 82% of paragraphs start with transition words
  • Low variation in sentence complexity

Paragraph Structure Issues:
  • All paragraphs 4-6 sentences long
  • Mechanical topic-sentence pattern throughout
```

### 5. Word Frequency Report
```
Top AI-Typical Words:
1. "furthermore" - 6x (baseline: 0.5x per 1000 words)
2. "robust" - 4x (baseline: 0.8x per 1000 words)
3. "leverage" - 3x (baseline: 0.3x per 1000 words)
4. "comprehensive" - 3x (baseline: 1.2x per 1000 words)
5. "delve" - 2x (baseline: 0.1x per 1000 words)

Comparison to Human Academic Writing:
  Your text: 4.2 AI-typical words per 1000
  Human baseline: 1.5 AI-typical words per 1000
  Ratio: 2.8x higher than human baseline
```

## Improvement Suggestions

### For High Confidence (70-100%) Detections

**Sentence Structure:**
- ❌ "Furthermore, the results demonstrate a comprehensive analysis of the robust dataset."
- ✅ "The results show our analysis covered the full dataset."

**Why Better:** Simpler words, no transition word, more direct

**Word Choice:**
- ❌ "This study delves into the utilization of innovative methodologies."
- ✅ "We examine how researchers use new methods."

**Why Better:** Active voice, common words, clearer meaning

**Paragraph Variation:**
- ❌ All paragraphs 5 sentences, topic sentence + 3 support + conclusion
- ✅ Mix paragraph lengths: 2, 7, 4, 3, 6 sentences based on content needs

**Why Better:** Natural flow based on content, not formula

### Specific Suggestion Categories

#### 1. Vary Sentence Lengths
```
Current: 15-25 word sentences consistently
Suggestion: Mix short (5-10), medium (15-20), long (25-35) sentences
Example:
  - Short: "The effect was significant."
  - Medium: "We observed a 23% increase across all conditions."
  - Long: "This finding aligns with previous work showing that..."
```

#### 2. Replace AI-Typical Words
```
Replace → With
- "delve into" → "examine", "explore", "investigate"
- "leverage" → "use", "apply", "employ"
- "utilize" → "use"
- "robust" → "strong", "reliable", "thorough"
- "facilitate" → "enable", "help", "allow"
- "furthermore" → "also", "next", [or remove]
- "moreover" → "additionally", "also", [or use dash]
- "comprehensive" → "complete", "thorough", "full"
```

#### 3. Add Natural Imperfections (Where Appropriate)
```
- Use contractions in appropriate contexts ("it's", "we'll")
- Include domain-specific jargon naturally
- Allow informal phrasing in methods/procedures
- Use occasional sentence fragments for emphasis
- Add personal observations or interpretations
- Include field-specific colloquialisms
```

#### 4. Break Paragraph Uniformity
```
Current: All paragraphs follow topic-support-support-support-conclusion
Suggestion: Vary based on content
  - Use single-sentence paragraphs for emphasis
  - Combine related ideas into longer paragraphs
  - Don't force every paragraph to have 5 sentences
  - Let content determine structure, not formula
```

#### 5. Remove Mechanical Transitions
```
❌ "Furthermore, the results show... Moreover, the analysis reveals..."
✅ "The results show... The analysis also reveals..." [simpler transitions]
✅ "The results show... Looking closer, the analysis..." [natural bridges]
```

## Integration Points

### 1. Pre-Commit Hook Integration
**Automatic checking before git commits**

```bash
# Configured in .claude/settings.json
"gitPreCommit": {
  "command": "python3 hooks/pre-commit-ai-check.py",
  "enabled": true
}
```

**Behavior:**
- Runs on staged `.md`, `.tex`, `.rst` files
- Warns if confidence 30-70%
- Blocks commit if confidence >70%
- User can override with `git commit --no-verify`

**Exit Codes:**
- 0: Pass (confidence <30%)
- 1: Warning (confidence 30-70%, commit allowed)
- 2: Block (confidence >70%, commit blocked)

### 2. Quality Assurance Integration
**Part of comprehensive QA workflow**

Integrated into `code/quality_assurance/qa_manager.py`:
- Runs during manuscript phase QA validation
- Checks all deliverable documents
- Generates detailed QA report section
- Fails QA if confidence >40%

**Configuration** (`.ai-check-config.yaml`):
```yaml
qa_integration:
  enabled: true
  max_confidence_threshold: 0.40
  check_manuscripts: true
  check_documentation: true
  generate_detailed_reports: true
```

### 3. Manuscript Writer Agent Integration
**Real-time feedback during writing**

Agent checks writing incrementally:
- After drafting each section
- Before moving to next phase
- Applies suggestions automatically
- Re-checks until confidence <30%

**Agent Workflow:**
1. Draft section
2. Run ai-check skill
3. Review detection results
4. Apply improvement suggestions
5. Re-check until authentic
6. Proceed to next section

### 4. Standalone Skill Usage
**Manual invocation by user or agents**

**User Invocation:**
```
Please run ai-check on docs/manuscript/discussion.tex and provide detailed feedback.
```

**Agent Invocation:**
```
I'll use the ai-check skill to verify this text before proceeding.
```

**CLI Tool:**
```bash
python tools/ai_check.py path/to/file.md
python tools/ai_check.py --directory docs/
python tools/ai_check.py --format html --output report.html
```

## Tracking System

### Historical Tracking
Log all AI-check runs to database for evolution tracking:

**Database Schema** (PostgreSQL via research-database MCP):
```sql
CREATE TABLE ai_check_history (
  id SERIAL PRIMARY KEY,
  file_path TEXT NOT NULL,
  git_commit TEXT,
  timestamp TIMESTAMP DEFAULT NOW(),
  overall_confidence FLOAT,
  grammar_score FLOAT,
  sentence_score FLOAT,
  paragraph_score FLOAT,
  word_score FLOAT,
  punctuation_score FLOAT,
  ai_words_found JSONB,
  flagged_sections JSONB
);
```

### Trend Analysis
Track writing evolution:
```
File: docs/manuscript/discussion.tex

Version History:
2025-01-15: 78% confidence (HIGH - likely AI)
2025-01-18: 52% confidence (MEDIUM - revision 1)
2025-01-20: 34% confidence (LOW-MEDIUM - revision 2)
2025-01-22: 18% confidence (LOW - authentic writing)

Trend: ✅ Improving toward authentic writing
```

**Use Cases:**
- Monitor dissertation chapters over time
- Track improvements after applying suggestions
- Demonstrate writing authenticity to committee
- Identify sections needing more work

## Configuration

### Configuration File: `.ai-check-config.yaml`

```yaml
# AI-Check Skill Configuration

# Pre-Commit Hook Settings
pre_commit:
  enabled: true
  check_files: [".md", ".tex", ".rst", ".txt"]
  check_docstrings: true  # Check Python docstrings
  block_threshold: 0.70   # Block commit if >= 70%
  warn_threshold: 0.30    # Warn if >= 30%
  exclude_patterns:
    - "*/examples/*"
    - "*/tests/*"
    - "*/node_modules/*"
    - "*/.venv/*"

# Quality Assurance Integration
qa_integration:
  enabled: true
  max_confidence_threshold: 0.40  # Fail QA if >= 40%
  check_manuscripts: true
  check_documentation: true
  generate_detailed_reports: true
  track_history: true

# Detection Parameters
detection:
  # Weight each metric (must sum to 1.0)
  weights:
    grammar_perfection: 0.20
    sentence_uniformity: 0.25
    paragraph_structure: 0.20
    ai_word_frequency: 0.25
    punctuation_patterns: 0.10
  
  # AI-typical word lists
  ai_words:
    high_risk: ["delve", "leverage", "utilize"]
    medium_risk: ["robust", "comprehensive", "facilitate"]
    transitions: ["furthermore", "moreover", "additionally"]
  
  # Thresholds
  ai_words_per_1000_threshold: 3.0
  human_baseline_per_1000: 1.5
  
# Report Generation
reporting:
  default_format: "markdown"  # markdown, json, html
  include_suggestions: true
  include_word_frequency: true
  include_flagged_sections: true
  max_flagged_sections: 10

# Tracking
tracking:
  enabled: true
  database: "research-database-mcp"
  retention_days: 365
```

### Per-Project Overrides

Create `.ai-check.local.yaml` for project-specific settings:
```yaml
# Project-specific overrides
pre_commit:
  block_threshold: 0.60  # More lenient for early drafts
  
detection:
  ai_words:
    high_risk: ["delve"]  # Only flag worst offenders
```

## Examples

### Example 1: High Confidence Detection

**Input Text:**
```
Furthermore, this comprehensive study delves into the robust 
methodologies utilized to facilitate the implementation of innovative 
approaches. Moreover, the analysis demonstrates significant findings 
that leverage state-of-the-art techniques. Subsequently, the results 
indicate substantial improvements across all metrics. Nevertheless, 
additional research is crucial to fully comprehend the implications.
```

**AI-Check Report:**
```
Overall Confidence: 89% (HIGH - Likely AI-generated)

Issues Detected:
- 8 AI-typical words in 60 words (13.3 per 1000 words!)
- Every sentence starts with transition word
- Uniform sentence length (15-18 words each)
- Perfect grammar, zero natural imperfections
- Mechanical paragraph structure

AI Words Found:
- furthermore, comprehensive, delves, robust
- utilized, facilitate, innovative, leverage
- demonstrates, significant, subsequently, substantial
- nevertheless, crucial, comprehend

Recommendation: Complete rewrite recommended
```

**Suggested Revision:**
```
We examined the methods used in this approach. The analysis shows 
clear improvements across metrics. However, more research is needed 
to understand the full implications.

(23 words, 12% confidence - much more natural)
```

### Example 2: Medium Confidence Detection

**Input Text:**
```
The experimental design followed standard protocols established in 
previous work (Smith et al., 2023). We collected data from 150 
participants over six months. Statistical analysis used mixed-effects 
models to account for repeated measures. The results showed a 
significant main effect of condition (p < 0.001).
```

**AI-Check Report:**
```
Overall Confidence: 35% (MEDIUM - Possible minor AI assistance)

Issues Detected:
- Slightly uniform sentence length (11-15 words)
- One AI-typical word: "significant" (statistical context acceptable)
- Otherwise natural academic writing

Recommendation: Minor revisions optional, writing appears largely authentic
```

### Example 3: Low Confidence (Human Writing)

**Input Text:**
```
OK so here's what we found. The effect was huge - way bigger than 
expected. Participants in the experimental group scored 23% higher 
on average. This wasn't just statistically significant; it was 
practically meaningful.

We're still not sure why. Maybe it's the timing? Could be the 
instructions were clearer. Need to run follow-ups.
```

**AI-Check Report:**
```
Overall Confidence: 8% (LOW - Clearly human writing)

Human Writing Indicators:
- Natural sentence variation (4-19 words)
- Informal elements ("OK so", "way bigger")
- Incomplete thoughts and questions
- Natural uncertainty expressions
- Zero AI-typical words
- Authentic voice throughout

Recommendation: Writing is authentic, no changes needed
```

## Best Practices

### For PhD Students

1. **Run Before Advisor Meetings**
   - Check chapters before sending to advisor
   - Ensure authenticity before committee review
   - Track improvements over time

2. **Use During Drafting**
   - Check each section after writing
   - Apply suggestions immediately
   - Develop natural writing habits

3. **Pre-Submission Validation**
   - Run on complete manuscripts before journal submission
   - Check supplementary materials
   - Verify all documentation

### For Research Teams

1. **Establish Team Standards**
   - Set agreed-upon confidence thresholds
   - Define when to block vs. warn
   - Create team-specific word lists

2. **Code Review Integration**
   - Check documentation in pull requests
   - Validate README files and guides
   - Ensure authentic technical writing

3. **Track Team Writing**
   - Monitor trends across team members
   - Identify systematic issues
   - Share improvement strategies

### For Journal Submission

1. **Pre-Submission Checklist**
   - [ ] Overall confidence <30%
   - [ ] No flagged high-risk sections
   - [ ] AI-typical words <2 per 1000 words
   - [ ] Natural sentence variation present
   - [ ] Authentic academic voice throughout

2. **Demonstrating Authenticity**
   - Include AI-check reports in submission materials
   - Show writing evolution over time
   - Document revision process

## Limitations

### What This Skill Cannot Do

1. **Not 100% Accurate**
   - LLMs constantly improving
   - Patterns evolve over time
   - False positives possible (very formal human writing)
   - False negatives possible (heavily edited AI text)

2. **Cannot Detect All AI Usage**
   - Well-edited AI text may pass
   - Human writing in AI style may be flagged
   - Paraphrasing tools may evade detection
   - Future models may have different patterns

3. **Domain Limitations**
   - Trained primarily on academic writing
   - May not work well for creative writing
   - Technical jargon may affect scores
   - Non-English text not supported

### Use Alongside Human Judgment

**This skill is a tool, not a replacement for human judgment:**
- Use confidence scores as guidance, not absolute truth
- Consider context and field-specific norms
- Combine with plagiarism detection tools
- Maintain academic integrity standards
- Update word lists as AI patterns evolve

## Support

### Troubleshooting

**Problem:** False positive on authentic writing
**Solution:** Check if writing is overly formal. Consider field-specific norms. Adjust thresholds in config.

**Problem:** AI text passing with low confidence
**Solution:** Update AI-typical word lists. Check for heavily edited text. Report patterns for skill updates.

**Problem:** Pre-commit hook too slow
**Solution:** Reduce checked file types. Enable caching. Check only modified sections.

**Problem:** Disagreement with manual review
**Solution:** Generate detailed report. Review flagged sections specifically. Consider multiple metrics not just overall score.

### Getting Help

- **Documentation:** See `docs/skills/ai-check-reference.md`
- **Issues:** https://github.com/astoreyai/ai_scientist/issues
- **Updates:** Check for skill updates regularly as AI patterns evolve

---

**Last Updated:** 2025-11-09
**Version:** 1.0.0
**License:** MIT
