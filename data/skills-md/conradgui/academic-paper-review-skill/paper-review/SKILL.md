---
name: paper-review
description: Use when reviewing, proofreading, auditing, or authorially polishing scientific and technical manuscripts in Markdown, DOCX, PDF, LaTeX, or plain text; checking research logic, methods, evidence, citations, reference relevance or duplication, AI-trace candidates, text clarity, terminology, style consistency, or producing a structured review or protected revision.
---

# Paper Review

## Overview

Produce a concrete manuscript review across two parallel quality tracks:

1. **Scientific Review:** research questions, methods, evidence, variables, equations, figures/tables, citations, and conclusion boundaries.
2. **Text Quality Review:** clarity, terminology, redundancy, paragraph flow, register, and manuscript-style consistency.

Default to a Markdown review report unless the user requests another output format. Scientific validity remains the first priority; text-quality review must not weaken or replace it.

## Default Behavior

1. Read the full manuscript or all provided manuscript material before writing findings.
2. Preserve equations, symbols, citation keys, table/figure labels, and quoted snippets exactly when needed for accuracy.
3. Match the user's requested language; default to Simplified Chinese (简体中文) unless specified otherwise.
4. Create a new timestamped review file at `paper-reviews/review-YYYY-MM-DD-HHMMSS.md` when writing to disk, unless the user gives another path. Treat `paper-reviews/` and `paper-revisions/` as user-facing deliverable directories. Do not place plans, scratch notes, logs, or temporary files in them.
5. Do not modify the manuscript unless the user explicitly requests edits or a revision pass.
6. Do not require a fixed review template. Use the structure that best exposes actionable issues.
7. If the manuscript is incomplete, review what is available and state which checks are limited by missing files.
8. Run both review tracks by default. Keep the text-quality result concise unless material problems or an explicit request trigger detailed reporting.
9. Do not infer authorship or output an AI probability.

## Input Handling

Support Markdown, DOCX, PDF, LaTeX source, and plain text.

- **Markdown or plain text:** review structure, claims, citations, tables, formulas, and prose directly.
- **DOCX:** review extractable manuscript content only. Use headings or table text as content-location context when available, but do not assess, repair, preserve, or guarantee layout, styles, pagination, comments, tracked changes, text boxes, field codes, or equation/table rendering.
- **PDF:** review visible content; note that source-level comments, hidden metadata, and some cross-reference checks may be limited. Do not perform full-manuscript polishing from PDF alone.
- **LaTeX:** inspect source when available; for LaTeX-specific source, macro, cross-reference, and compileability concerns, prefer `$latex-paper-review` when installed.
- **Multi-file projects:** inspect the main file plus included chapters, bibliography, appendices, tables, figures/captions, and supporting notes when available.

## Manuscript Understanding Model

Before formulating any review findings, build a structured internal map covering:

- **Research Question Map**: Identify the core research questions, primary claims, and intended contributions.
- **Construct / Variable / Parameter Map**: Identify independent/dependent variables, mediators, moderators, control variables, mathematical parameters, system components, or theoretical constructs (as applicable to the manuscript type).
- **Relationship Map**: Identify hypothesized directions, causal links, logical dependencies, mathematical relationships, or system interactions.
- **Method Fit Assessment**: Evaluate whether the selected research design or method logically answers the research questions, whether the generated evidence supports the stated claims, and whether conclusion boundaries match the evidence.

Use this map to test whether the paper's claims, method, evidence, and wording align. Do not output this model in the final report unless it directly exposes an issue.

## Mode Router

Select one primary mode before loading conditional references or writing the report:

1. **Default Review:** use when the user asks for a manuscript review without selecting another mode. Run scientific review plus lightweight text-quality review. Apply the Core Manuscript Audit Protocol first, then read `references/text-quality-audit.md` for the language-agnostic lightweight audit and its AI-trace candidate scan. Read `references/ai-trace-candidate-audit.md` only when a material candidate appears or the user explicitly requests detailed AI-trace review. Load the Chinese and/or English deep-audit reference only after detailed reporting is triggered or the user explicitly requests language-focused review.
2. **Recheck / Delta Review:** use when the user provides a prior review or asks whether a revised manuscript resolved earlier findings. Apply the delta protocol and review only the requested scope plus changes needed to classify prior findings.
3. **Reference Audit:** use only when the user explicitly requests reference relevance, recency, duplication, version-overlap, or citation-redundancy review. Produce its independent report; do not silently turn it into a full manuscript review.
4. **Authorial Polishing:** use only when the user explicitly requests a finding-level edit, paragraph/section polish, revision pass, or full-manuscript polish. Do not edit during any review mode.

Default Review is the only mode that automatically runs both quality tracks. A user may explicitly narrow Default Review to scientific-only or text-quality-only scope. Do not expand into another mode unless the user explicitly requests it. If the user explicitly combines modes, perform them in the stated order and keep their deliverables separate.

Keep scientific and text-quality findings distinct. A vague causal claim belongs in Scientific Review even if the sentence is also awkward. A sustained register shift or redundant paragraph belongs in Text Quality Review unless it changes scientific meaning.

## Core Manuscript Audit Protocol

Every manuscript must receive a transparent core audit before optional type-specific checks. Apply these checks across manuscript types without forcing empirical-paper concepts onto non-empirical work:

1. **Research question audit:** identify the main question, contribution, and whether the paper's structure keeps returning to that question.
2. **Core concept / variable / symbol / construct audit:** identify the key units of analysis for this manuscript type and check whether they are defined, used consistently, and operational enough for readers to follow.
3. **Claim-evidence chain audit:** test whether each important claim is supported by the paper's method, data, figures, tables, derivations, citations, appendices, or explicit assumptions.
4. **Method-question fit audit:** check whether the selected method, model, experiment, proof, system evaluation, or review framework can answer the research question.
5. **Structural coherence audit:** check whether title, abstract, introduction, related work, method, results, discussion, conclusion, and appendices form a coherent path.
6. **Support-material audit:** check whether figures, tables, appendices, references, formulas, and supplementary material support rather than contradict the main text.
7. **Conclusion boundary audit:** check whether conclusion strength, limitations, causal wording, and practical implications match the actual evidence.
8. **Actionability audit:** convert the most important findings into the action plan table defined in `Output Contract`.

Interpret "variables" broadly:

- empirical papers: variables, indicators, controls, mediators, moderators
- theoretical papers: concepts, propositions, assumptions, definitions
- mathematical papers: symbols, parameters, functions, theorem conditions
- systems papers: modules, inputs/outputs, metrics, baselines
- review papers: taxonomy dimensions, concept boundaries, literature streams

## Review Workflow

1. Identify manuscript type: empirical, theoretical/mathematical, systems/technical, review/conceptual, or mixed.
2. Build the manuscript understanding model.
3. Apply the Core Manuscript Audit Protocol.
4. Trace the Evidence Chain for identified claims: Check the path `Claim` -> `Evidence` -> `Figure/Table` -> `Method` -> `Citation` -> `Appendix` (if applicable) for inconsistencies, missing links, or overreaching assertions.
5. If the manuscript has empirical-research features, read `references/empirical-paper-audit.md` and apply it as an enhancement module, not as a replacement for the core audit.
6. Read `references/claim-strength-calibration.md` when the manuscript contains causal, significance, robustness, novelty, policy, or contribution claims whose wording may be stronger than the evidence.
7. Audit the highest-risk content first: research question, method, variables/symbols, evidence, results, equations, figures/tables, appendices, and citations.
8. Re-check the scientific findings and classify them by severity and certainty.
9. Apply the text-quality route selected by Mode Router after scientific review when the selected mode includes text quality.
10. Run `scripts/proofing_scan.py` when code execution is available and the input is PDF, DOCX, Markdown, or text-like; otherwise do the manual proofing scan below.
11. Spot-check all script and style candidates in context before reporting them.
12. Write the review report with scientific findings prioritized and a separate text-quality section.

## Reference Audit Execution

After Mode Router selects Reference Audit, run this independent module. A normal manuscript review may flag a citation problem, but it must not silently expand into this separate audit.

1. Read `references/reference-audit.md`.
2. Use **Core References** mode by default: audit references attached to the research question, theoretical mechanism, methods or measures, key facts, main result interpretation, and contribution comparison.
3. Use **All Cited References** mode only when the user requests complete coverage. Report every cited source as audited, missing, unmatched, or unable to assess.
4. Check the complete bibliography for exact and probable version duplicates in either mode; limit claim-context relevance and functional-redundancy analysis to the selected mode.
5. Write an independent report to `paper-reviews/reference-audit-YYYY-MM-DD-HHMMSS.md`. Do not merge a large reference matrix into the default manuscript review unless the user requests that format.
6. Apply the existing external-research opt-in policy to recency, retraction, supersession, DOI, and publication-version checks. Never infer author intent or assign a composite reference-quality score.

## Recheck / Delta Review

After Mode Router selects Recheck / Delta Review, use this protocol.

In recheck mode:

1. Read the prior review and the current manuscript materials.
2. Preserve prior finding IDs when available and map findings to their current manuscript locations, accounting for section or wording changes. Do not replace a mapped prior ID with `D-*` or another new namespace.
3. Classify each prior finding with one exact status token:
   - **Resolved:** the issue is fixed.
   - **Still Open:** the issue remains materially unchanged.
   - **Downgraded:** the issue remains but has been narrowed, qualified, or partially addressed.
   - **Upgraded:** the issue became more serious or now affects a higher-priority claim.
   - **New:** a newly introduced or newly discovered issue.
   - **Needs External Verification:** the status depends on data, literature, code, or context not available in the manuscript.
4. Do not simply repeat the old review. Focus on status changes, remaining blockers, and new issues.
5. Include next action for each still-open, downgraded, upgraded, new, or verification-needed item.
6. Assign a new `S-*` or `T-*` ID only to a genuinely new issue, continuing after the highest existing ID in that track.
7. Include every unresolved delta item in the Action Plan Table and keep its mapped finding ID visible.

The status matrix is mandatory and must include every prior finding plus every new finding. Use the exact English status tokens above in the `状态` column; a Chinese explanation may follow in parentheses.

```markdown
| Finding ID | 原问题 | 当前位置 | 状态 | 下一步动作 |
|---|---|---|---|---|
```

## Review Lenses

Use these lenses as applicable:

- **Structure:** title, abstract, introduction, related work, method, results, discussion, conclusion, and appendices form a coherent path.
- **Evidence:** claims are supported by data, figures, tables, experiments, citations, derivations, or stated assumptions.
- **Method:** study design, variables, model, experiment, proof, or review method can answer the research question.
- **Expression:** terms, paragraphs, figures, tables, references, and formatting support reader comprehension.
- **Risk:** overclaiming, causal overreach, missing caveats, sample limits, external validity, unsupported novelty, or ambiguity.

## Manuscript-Type Checks

For each manuscript type, check specific methodological validity dimensions (if applicable):

- **Empirical papers**: Check variable definitions, measurement validity, model specification, table interpretation, robustness checks, causal language, causal boundary limits, selection bias, endogeneity, construct reliability, and conclusion boundaries.
- **Theoretical or mathematical papers**: Check definitions, assumptions, notation, boundary conditions, theorem/proposition statements, proof steps, dimensions, signs, branches, and symbol drift.
- **Systems or technical papers**: Check task framing, baseline fairness, evaluation metrics, implementation ambiguity, reproducibility, ablations, external validity, and claim-to-result alignment.
- **Review or conceptual papers**: Check taxonomy logic, concept boundaries, source representativeness, citation support, and whether synthesis goes beyond summary.

## Common Manuscript Failure Modes

Check these cross-disciplinary failure modes when applicable. Treat venue-specific requirements as `Needs External Verification` unless the user provides the guideline or authorizes a lookup.

- **Title, abstract, and keywords:** describe the same research question, method, evidence, population/system, and bounded conclusion as the main text.
- **Introduction:** distinguishes context, unresolved gap, research objective/question, and contribution without inflating novelty.
- **Related work or literature review:** synthesizes comparison, disagreement, trend, taxonomy, and the current gap instead of becoming a paper-by-paper inventory.
- **Methods or materials:** provides data or material provenance, inclusion/exclusion rules, preprocessing, procedural detail, and settings sufficient for evaluation or reproduction.
- **Ethics and governance:** includes approval, consent, conflicts, funding, data/code availability, or other required declarations when the study or venue requires them.
- **Results:** Results reports observation before interpretation and does not hide null, mixed, boundary, or uncertainty information relevant to the main claim.
- **Discussion:** Discussion distinguishes findings from interpretation, alternative explanations, prior literature, limitations, and implications.
- **Limitations:** identifies concrete threats and affected claim boundaries rather than using generic caveats contradicted elsewhere.
- **Conclusion:** answers the research question without introducing new evidence, mechanisms, populations, or stronger claims.
- **References and declarations:** every material citation supports the adjacent claim; cited and listed sources reconcile; required declarations are present when applicable.

## Technical And Evidence Audit

Always check for:

- unsupported or overstated claims
- conclusions that do not follow from reported results
- inconsistency between text, equations, figures, tables, captions, appendices, and conclusions
- undefined variables, constructs, terms, symbols, or abbreviations
- notation or terminology drift
- unit, dimensional, arithmetic, or quantitative inconsistencies
- sign errors, missing factors, normalization ambiguity, or missing case distinctions
- inverse-trig, branch, or quadrant ambiguity, such as `arctan(x/y)` where `atan2` or an explicit branch convention may be needed
- mismatch between definitions, formulas, appendix material, and implementation-facing expressions
- missing assumptions, qualifiers, limitations, or uncertainty that materially affect interpretation
- citation/reference mismatch or citation used to support a claim it does not actually establish

When a finding concerns claim strength, use `references/claim-strength-calibration.md` to identify an evidence-appropriate wording level and minimal phrase options. Do not draft a paste-ready replacement sentence unless the user explicitly requests polishing.

## Severity And Certainty Classification

For each finding, you must determine both its severity and certainty:

### Severity Levels
- **Critical Issues**: Factual, logical, or methodological issues that threaten the primary validity of the manuscript (e.g., unsupported core claims, missing identification strategy, undefined key variables, contradictory results).
- **Major Issues**: Significant problems that weaken confidence in the findings (e.g., measurement ambiguity, incomplete methodological justification, weak evidence chain).
- **Minor Issues**: Localized errors that affect clarity, consistency, or readability (e.g., terminology inconsistency, local figure-text mismatches, formatting problems).
- **Writing Suggestions**: Non-essential suggestions to improve flow, grammar, or phrasing.

### Certainty Labels
- **确定错误 (Definite Error)**: Contradicted directly by the manuscript's own contents, math, or established logic.
- **证据不足 (Unsupported Claim)**: Stated more strongly than the manuscript's data or references justify.
- **疑似问题 (Likely Issue)**: Highly probable issue that requires authors' attention but cannot be proven definitively from the text alone.
- **需核对/确认 (Requires Verification)**: Depends on external literature or context outside the manuscript.

## External Research Policy

Do not perform external web or literature searches by default. Do not search until the user explicitly authorizes it. If a finding cannot be assessed without external knowledge, label it `Needs External Verification`, explain what must be checked, and ask for permission before searching.

When searching, protect manuscript privacy by using anonymized queries (do not upload the title, author names, or sensitive draft text).

### Source Credibility Hierarchy
- **Tier 1 (Authoritative)**: Peer-reviewed original studies and reviews, official standards, standard textbooks, official statistics, regulatory or institutional primary sources, and official technical documentation.
- **Tier 2 (Supporting or discovery)**: Reputable preprints (including arXiv), university lecture notes, technical manuals, and academic indexes or databases such as OpenAlex and PubMed. Index records help locate sources but are not evidence by themselves.
- **Tier 3 (Non-authoritative)**: General forums (StackOverflow, Reddit), commercial/marketing blogs, AI summaries without sources.
*Rule: Tier 3 sources may only serve as search leads or prompts to check further, but MUST NEVER be cited as academic evidence, consensus, or proof of error.*

### Cross-Validation Rule
When a review conclusion depends on external academic consensus, cross-check multiple authoritative (Tier 1/2) sources whenever feasible. If evidence remains uncertain, label the issue as "requires verification" rather than asserting that the manuscript is incorrect.

## Text Quality Review

When the selected route includes text quality, include observable issues that affect meaning, technical clarity, manuscript-level style consistency, or professionalism:

- ambiguous phrasing that changes interpretation
- inconsistent terminology
- weak transitions that obscure argument logic
- unclear figure/table descriptions
- malformed equation-adjacent prose
- broken references, duplicated punctuation, malformed titles, or obvious citation-format glitches
- high-confidence grammar, spelling, or capitalization issues
- sustained register, person, tense, or terminology drift
- redundant restatement, template residue, chatbot framing, or unfilled placeholders

Avoid subjective line editing, word blacklists, or style fingerprinting. Do not force variation for its own sake.

Treat AI-trace review as a text-quality submodule, not a third review track. Surface patterns are candidates, not proof of authorship. Trace material candidates to specificity, evidence, citations, terminology, and section fit; report the underlying problem instead of claiming that text is AI-generated.

## Authorial Polishing

After Mode Router selects Authorial Polishing, use this execution protocol.

1. Read `references/authorial-polishing.md`.
2. Build the confirmed authorial, manuscript-consistent, or neutral style baseline defined by the reference, then build the immutable content ledger before editing. Do not call an inferred manuscript baseline the author's personal voice.
3. For an explicit full-manuscript request, read `references/external-polishing-routing.md`; check only local Skill availability and ask once before optional enhancement.
4. Generate the revision artifact allowed by the input format and a companion report. Never overwrite the source manuscript. For DOCX, generate structured content revision guidance and a companion report, not a DOCX copy.
5. Re-run scientific, terminology, and claim-boundary checks on the revised content.

Nature Polishing may provide constrained academic-expression candidates when installed and authorized. Humanizer variants may only provide audit candidates; they must not control full rewrites, output AI scores, or optimize perplexity/burstiness.

## Final Proofing Sweep

Run when useful:

```bash
python3 scripts/proofing_scan.py <path-to-pdf-or-text> --max-hits 80
```

Use hits as candidates and spot-check before including them. Chatbot residue, placeholder, and citation-markup hits are publication-artifact warnings, not authorship judgments.

If code execution is unavailable, manually scan for duplicated punctuation, malformed equation-adjacent prose, product/language capitalization, citation-format glitches, and branch/quad ambiguity patterns such as `arctan(x/y)`.

## Output Contract

Generate the default report in Simplified Chinese (简体中文) unless the user requests another language.

### Anti-Generic Feedback Rules
You must NOT output low-value, vague suggestions (e.g., "增强创新性", "扩展文献", "提升贡献") that lack precise local facts or actionable advice.
If no concrete issues are identified, output "未发现明显问题" directly. Do not invent minor issues just to fill space.

### Finding Format
For every scientific finding and every detailed text-quality finding, start the finding on its own Markdown heading line: `### S-01: concise title` for Scientific Review or `### T-01: concise title` for detailed Text Quality Review. The heading is the finding identifier used by the action plan and recheck matrix. Do not place the ID only in bold text, a table cell, or a severity-group heading.

Each detailed finding MUST then include:
1. **Finding ID:** the same ID shown in its heading: `S-01`, `S-02`, ... for Scientific Review; `T-01`, `T-02`, ... for detailed Text Quality Review.
2. **Location** (e.g., section number, page, line number, or equation/figure label).
3. **Evidence / 具体证据:** the specific local quote, number, formula, table/figure entry, or cross-section mismatch that supports the finding. Do not use a restatement of the finding as evidence.
4. **Problem** (factual explanation of the issue).
5. **Why it matters** (impact on manuscript validity or readability).
6. **Revision guidance / 修改指导** (the change objective, constraints to preserve, and concrete edit actions).
7. **Severity** (Critical, Major, Minor, or Writing Suggestion).
8. **Certainty** (确定错误, 证据不足, 疑似问题, or 需核对/确认).
*Note: Only output the Evidence Chain trace path if an issue or discrepancy in the chain is found.*

### DOCX Report Boundary
For every DOCX review, include this concise scope statement in the overall assessment or immediately before detailed findings, translated when the user requests a non-Chinese report:

`审阅边界：本报告仅审阅该 DOCX 的可提取论文内容；不评估、修复或保证 Word/DOCX 的布局、样式、分页、批注、修订、文本框、域代码或公式/表格渲染。`

Do not omit this statement even when no content finding is identified.

An isolated non-material text observation is not a detailed finding. Report it in one concise sentence without a `T-*` ID, detailed table, or action-plan row. Reserve `T-*` IDs for text-quality issues that satisfy the detailed-audit trigger.

By default, revision guidance must not contain a paste-ready replacement paragraph. Use structure, operations, evidence-appropriate wording levels, or short phrase alternatives. Generate complete replacement sentences or paragraphs only after the user explicitly requests authorial polishing for a named finding, location, section, or manuscript.

Default Markdown report structure:
- Concise overall assessment (整体评估)
- Detailed findings grouped by **Severity** (from Critical down to Minor/Suggestions)
- Text quality review (文本质量审阅): one-sentence result by default, detailed table only when triggered
- AI-trace candidate audit (AI 痕迹候选审阅): one-sentence result by default; detailed candidate matrix only when explicitly requested or materially triggered
- High-priority fixes (高优先级修改建议)
- Items needing external verification (需核对/确认事项)
- Action plan table (修改行动表)

When detailed text-quality reporting is triggered, use:

```markdown
| Finding ID | 位置 | 严重程度 | 判断确定性 | 文本问题 | 具体证据 | 影响 | 修改方向 |
|---|---|---|---|---|---|---|---|
```

### Action Plan Table

End the report with a concise action plan table when concrete fixes exist. Do not force rows when there are no actionable issues.

```markdown
| 优先级 | 问题 | 修改类型 | 建议修改位置 | 是否阻塞提交 |
|---|---|---|---|---|
```

Use:

- **优先级:** `P0`, `P1`, or `P2`
- **修改类型:** `主张强度校准`, `变量定义补充`, `表文一致性`, `方法说明补充`, `文献支撑补充`, `结构调整`, `表达澄清`, `文本清晰度`, `文风一致性`, `冗余压缩`, `作者化润色`, `格式/引用修正`, or `需外部核查`
- **是否阻塞提交:** `是`, `否`, or `取决于要求`

Prefix the `问题` cell with its finding ID when applicable, for example `[S-01]` or `[T-01]`. Do not use `P0/P1/P2` as finding IDs.

### Next-Step Routing

When actionable findings exist, end with one concise next-step example that matches the actual issue type. Do not show every route, and do not send a scientific finding to authorial polishing by default.

- **Scientific `S-*` finding:** `按 finding S-01 的修改指导修复相关科学性问题，保留数据、引用和结论边界。`
- **Text-quality `T-*` finding:** `按本文已确认的文风基线润色 finding T-01，仅修改相关位置。`
- **Reference Audit:** use a reference-specific action such as `补交原文、调整引用位置、合并条目或核查更新来源`.

Only generate an edited passage when the user explicitly requests Authorial Polishing for a named finding, location, section, or manuscript.
