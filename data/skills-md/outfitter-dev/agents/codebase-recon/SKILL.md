---
name: codebase-recon
description: This skill should be used when analyzing codebases, understanding architecture, or when "analyze", "investigate", "explore code", or "understand architecture" are mentioned.
metadata:
  version: "1.0.0"
---

# Codebase Analysis

Evidence-based investigation → findings → confidence-tracked conclusions.

## Steps

1. Gather evidence from multiple sources (code, docs, tests, history)
2. Track confidence level as investigation progresses
3. Based on findings:
   - If pattern analysis needed → load the `outfitter:patterns` skill
   - If root cause investigation → load the `outfitter:find-root-causes` skill
   - If ready to report → load the `outfitter:report-findings` skill
4. Deliver findings with confidence level and caveats

<when_to_use>

- Codebase exploration and understanding
- Architecture analysis and mapping
- Pattern extraction and recognition
- Technical research within code
- Performance or security analysis

NOT for: wild guessing, assumptions without evidence, conclusions before investigation

</when_to_use>

<confidence>

| Bar | Lvl | Name | Action |
|-----|-----|------|--------|
| `░░░░░` | 0 | Gathering | Collect initial evidence |
| `▓░░░░` | 1 | Surveying | Broad scan, surface patterns |
| `▓▓░░░` | 2 | Investigating | Deep dive, verify patterns |
| `▓▓▓░░` | 3 | Analyzing | Cross-reference, fill gaps |
| `▓▓▓▓░` | 4 | Synthesizing | Connect findings, high confidence |
| `▓▓▓▓▓` | 5 | Concluded | Deliver findings |

*Calibration: 0=0–19%, 1=20–39%, 2=40–59%, 3=60–74%, 4=75–89%, 5=90–100%*

Start honest. Clear codebase + focused question → level 2–3. Vague or complex → level 0–1.

At level 4: "High confidence in findings. One more angle would reach full certainty. Continue or deliver now?"

Below level 5: include `△ Caveats` section.

</confidence>

<principles>

## Core Methodology

**Evidence over assumption** — investigate when you can, guess only when you must.

**Multi-source gathering** — code, docs, tests, history, web research, runtime behavior.

**Multiple angles** — examine from different perspectives before concluding.

**Document gaps** — flag uncertainty with △, track what's unknown.

**Show your work** — findings include supporting evidence, not just conclusions.

**Calibrate confidence** — distinguish fact from inference from assumption.

</principles>

<evidence_gathering>

## Source Priority

1. **Direct observation** — read code, run searches, examine files
2. **Documentation** — official docs, inline comments, ADRs
3. **Tests** — reveal intended behavior and edge cases
4. **History** — git log, commit messages, PR discussions
5. **External research** — library docs, Stack Overflow, RFCs
6. **Inference** — logical deduction from available evidence
7. **Assumption** — clearly flagged when other sources unavailable

## Investigation Patterns

**Start broad, then narrow:**
- File tree → identify relevant areas
- Search patterns → locate specific code
- Code structure → understand without full content
- Read targeted files → examine implementation
- Cross-reference → verify understanding

**Layer evidence:**
- What does the code do? (direct observation)
- Why was it written this way? (history, comments)
- How does it fit the system? (architecture, dependencies)
- What are the edge cases? (tests, error handling)

**Follow the trail:**
- Function calls → trace execution paths
- Imports/exports → map dependencies
- Test files → understand usage patterns
- Error messages → reveal assumptions
- Comments → capture historical context

</evidence_gathering>

<output_format>

## During Investigation

After each evidence-gathering step emit:

- **Confidence:** {BAR} {NAME}
- **Found:** { key discoveries }
- **Patterns:** { emerging themes }
- **Gaps:** { what's still unclear }
- **Next:** { investigation direction }

## At Delivery (Level 5)

### Findings

{ numbered list of discoveries with supporting evidence }

1. {FINDING} — evidence: {SOURCE}
2. {FINDING} — evidence: {SOURCE}

### Patterns

{ recurring themes or structures identified }

### Implications

{ what findings mean for the question at hand }

### Confidence Assessment

Overall: {BAR} {PERCENTAGE}%

High confidence areas:
- {AREA} — {REASON}

Lower confidence areas:
- {AREA} — {REASON}

### Supporting Evidence

- Code: { file paths and line ranges }
- Docs: { references }
- Tests: { relevant test files }
- History: { commit SHAs if relevant }
- External: { URLs if applicable }

## Below Level 5

### △ Caveats

**Assumptions:**
- {ASSUMPTION} — { why necessary, impact if wrong }

**Gaps:**
- {GAP} — { what's missing, how to fill }

**Unknowns:**
- {UNKNOWN} — { noted for future investigation }

</output_format>

<specialized_techniques>

Load skills for specialized analysis (see Steps section):

- **Pattern analysis** → `outfitter:patterns`
- **Root cause investigation** → `outfitter:find-root-causes`
- **Research synthesis** → `outfitter:report-findings`
- **Architecture analysis** → see [architecture-analysis.md](references/architecture-analysis.md)

</specialized_techniques>

<workflow>

Loop: Gather → Analyze → Update Confidence → Next step

1. **Calibrate starting confidence** — what do we already know?
2. **Identify evidence sources** — where can we look?
3. **Gather systematically** — collect from multiple angles
4. **Cross-reference findings** — verify patterns hold
5. **Flag uncertainties** — mark gaps with △
6. **Synthesize conclusions** — connect evidence to insights
7. **Deliver with confidence level** — clear about certainty

At each step:
- Document what you found (evidence)
- Note what it means (interpretation)
- Track what's still unclear (gaps)
- Update confidence bar

</workflow>

<validation>

Before concluding (level 4+):

**Check evidence quality:**
- ✓ Multiple sources confirm pattern?
- ✓ Direct observation vs inference clearly marked?
- ✓ Assumptions explicitly flagged?
- ✓ Counter-examples considered?

**Check completeness:**
- ✓ Original question fully addressed?
- ✓ Edge cases explored?
- ✓ Alternative explanations ruled out?
- ✓ Known unknowns documented?

**Check deliverable:**
- ✓ Findings supported by evidence?
- ✓ Confidence calibrated honestly?
- ✓ Caveats section included if <100%?
- ✓ Next steps clear if incomplete?

</validation>

<rules>

ALWAYS:
- Investigate before concluding
- Cite evidence sources with file paths/URLs
- Use confidence bars to track certainty
- Flag assumptions and gaps with △
- Cross-reference from multiple angles
- Document investigation trail
- Distinguish fact from inference
- Include caveats below level 5

NEVER:
- Guess when you can investigate
- State assumptions as facts
- Conclude from single source
- Hide uncertainty or gaps
- Skip validation checks
- Deliver without confidence assessment
- Conflate evidence with interpretation

</rules>

<references>

Core methodology:
- [confidence.md](../pathfinding/references/confidence.md) — confidence calibration (shared with pathfinding)

Micro-skills (load as needed):
- `outfitter:patterns` — extracting and validating patterns
- `outfitter:find-root-causes` — systematic problem diagnosis
- `outfitter:report-findings` — multi-source research synthesis

Local references:
- [architecture-analysis.md](references/architecture-analysis.md) — system structure mapping

Related skills:
- `outfitter:pathfinding` — clarifying requirements before analysis
- `outfitter:debugging` — structured bug investigation

</references>
