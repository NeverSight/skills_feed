---
name: translation-reframing-audience-shift
description: Use when content must be translated between audiences with different expertise, context, or goals while preserving accuracy but adapting presentation. Invoke when technical content needs business framing (engineering decisions → executive summary), strategic vision needs tactical translation (board presentation → team OKRs), expert knowledge needs simplification (academic paper → blog post, medical diagnosis → patient explanation), formal content needs casual tone (annual report → social media post), long-form needs summarization (50-page doc → 1-page brief), internal content needs external framing (roadmap → public updates, bug tracking → known issues), cross-cultural adaptation (US idioms → international clarity, Gen Z → Boomer messaging), medium shifts (written report → presentation script, detailed spec → action checklist), or when user mentions "explain to", "reframe for", "translate this for [audience]", "make this more [accessible/formal/technical]", "adapt for [executives/engineers/customers]", "simplify without losing accuracy", or "same content, different audience". Apply to technical communication (code → business value), organizational translation (strategy → execution), education (expert → novice), customer communication (internal → external), cross-cultural messaging, and anywhere same core message needs different presentation for different stakeholders while maintaining correctness.
---
# Translation, Reframing & Audience Shift

## Purpose

Adapt content for different audiences while preserving core accuracy—changing tone, depth, emphasis, and framing to match audience expertise, goals, and context.

## When to Use

**Invoke this skill when:**
- Same information needs to reach audiences with different expertise (technical → business, expert → novice)
- Content tone/formality needs changing (formal report → casual email, academic → conversational)
- Strategic content needs tactical translation (vision → action items, why → how)
- Internal content goes external (company docs → customer-facing, jargon → plain language)
- Long-form needs compression without losing key points (detailed → summary, comprehensive → highlights)
- Medium changes (written → spoken, document → presentation, email → social media)
- Cross-cultural or demographic shifts (US → international, industry → industry, generation → generation)
- Emphasis needs shifting (highlight different aspects for different stakeholders)

**Don't use when:**
- Content is already appropriate for target audience (no translation needed)
- Creating entirely new content (not adapting existing)
- Simple copy-editing (grammar, spelling) without audience shift
- Translating between human languages (use language translation, not this skill)

## What Is It?

**Translation/reframing** adapts content between audiences by preserving semantic accuracy (what is true) while changing presentation (how it's communicated). **Four fidelity types:**

**1. Semantic fidelity (MUST preserve):** Core facts, relationships, constraints, implications remain accurate
**2. Tonal fidelity (adapt):** Formality, emotion, register change to match audience expectations
**3. Emphasis fidelity (adapt):** What's highlighted vs. backgrounded shifts based on audience priorities
**4. Medium fidelity (adapt):** Structure, length, format change for different channels/contexts

**Example:** Technical incident postmortem → Customer status update

**Original (Engineers):** "Root cause: race condition in distributed lock manager under high concurrency (>5000 req/s). Null pointer dereference when lock timeout occurred before callback registration. Fix: added CAS operation with retry logic, deployed canary to 5% traffic, monitored for 2 hours before full rollout."

**Translated (Customers):** "What happened: Service slowdown on Jan 15, 2-3pm affecting checkout for some users. Root cause: Timing issue in our system under high traffic. Status: Fixed, monitored, and fully deployed. Prevention: Added safeguards to prevent similar timing issues."

**What changed:** Technical detail reduced, jargon removed, impact/status emphasized, customer concerns prioritized (what happened, is it fixed, will it happen again). **What preserved:** Timing, affected functionality, root cause category, resolution status.

## Workflow

Copy this checklist and track your progress:

```
Translation & Reframing Progress:
- [ ] Step 1: Analyze source and target audiences
- [ ] Step 2: Identify translation type and constraints
- [ ] Step 3: Apply translation strategy
- [ ] Step 4: Validate fidelity and appropriateness
- [ ] Step 5: Refine and deliver
```

**Step 1: Analyze source and target audiences**

Characterize both audiences using [Audience Analysis](#audience-analysis) framework (expertise, goals, context, constraints). Identify gap between source and target.

**Step 2: Identify translation type and constraints**

Classify as: technical↔business, strategic↔tactical, expert↔novice, formal↔informal, long↔short, internal↔external, or cross-cultural. See [Common Translation Types](#common-translation-types) for patterns.

**Step 3: Apply translation strategy**

For simple cases → Use [resources/template.md](resources/template.md) for structured translation. For complex cases (multiple audiences, high stakes, nuanced reframing) → Study [resources/methodology.md](resources/methodology.md) for advanced techniques.

**Step 4: Validate fidelity and appropriateness**

Self-assess using [resources/evaluators/rubric_translation_reframing_audience_shift.json](resources/evaluators/rubric_translation_reframing_audience_shift.json). Check: semantic accuracy preserved? tone appropriate? emphasis aligned with audience priorities? See [Validation](#validation) section.

**Step 5: Refine and deliver**

Create `translation-reframing-audience-shift.md` with source, target audience, translated content, and translation rationale. See [Delivery Format](#delivery-format).

---

## Audience Analysis

Before translating, characterize source and target:

**1. Expertise Level**
- **Expert**: Domain fluent, comfortable with jargon, wants depth and nuance
- **Intermediate**: Familiar with basics, needs some context, appreciates balance
- **Novice**: No background assumed, needs analogies and plain language, wants practical takeaways

**2. Primary Goals**
- **Decision-makers**: Want options, trade-offs, recommendations, risks, timelines
- **Implementers**: Want specifics, how-to, constraints, success criteria
- **Learners**: Want understanding, context, mental models, examples
- **Stakeholders**: Want impact, status, next steps, how it affects them

**3. Context & Constraints**
- **Time**: Busy executives (1-page), deep dives (comprehensive), quick updates (bullets)
- **Medium**: Email (skimmable), presentation (visual + verbal), document (reference)
- **Familiarity**: Internal (shared context) vs. external (assume nothing)
- **Sensitivity**: Public (carefully worded) vs. private (candid)

**4. Cultural/Demographic**
- **Language**: Native vs. non-native speakers (idiomatic vs. literal)
- **Generation**: Communication norms (emoji use, formality expectations)
- **Industry**: Tech vs. traditional (pacing, references, assumptions)
- **Geography**: US vs. international (date formats, measurement units, cultural references)

**Mapping exercise:** Source audience is [expertise/goals/context] → Target audience is [expertise/goals/context] → Gap requires [translation strategy].

---

## Common Translation Types

### Technical ↔ Business

**Technical → Business:**
- **Remove**: Implementation details, jargon, code, algorithms
- **Add**: Business value, customer impact, cost/benefit, competitive advantage
- **Shift emphasis**: How it works → Why it matters, Metrics → Outcomes
- **Example**: "Reduced p95 latency from 450ms to 120ms via query optimization" → "Pages load 3x faster, improving customer satisfaction and conversion"

**Business → Technical:**
- **Remove**: Marketing language, vague goals, buzzwords
- **Add**: Requirements, constraints, acceptance criteria, technical implications
- **Shift emphasis**: Vision → Implementation details, Outcomes → Metrics
- **Example**: "Delight customers with seamless experience" → "Reduce checkout flow to 2 steps, target 95% completion rate, maintain PCI compliance"

### Strategic ↔ Tactical

**Strategic → Tactical:**
- **Remove**: High-level vision, market trends, abstract goals
- **Add**: Specific actions, timelines, owners, dependencies, success metrics
- **Shift emphasis**: Why → What and how, 3-year vision → This quarter's plan
- **Example**: "Become data-driven organization" → "Q1: Instrument 10 key user flows. Q2: Train PMs on analytics. Q3: Establish weekly metrics review."

**Tactical → Strategic:**
- **Remove**: Granular tasks, individual tickets, daily activities
- **Add**: Themes, rationale, business alignment, cumulative impact
- **Shift emphasis**: Individual work → Portfolio narrative, Tasks → Outcomes
- **Example**: "Fixed 47 bugs, added 12 features, refactored auth" → "Improved product stability and security foundation to support enterprise customers"

### Expert ↔ Novice

**Expert → Novice:**
- **Remove**: Jargon, assumptions of prior knowledge, complex terminology
- **Add**: Analogies, definitions, examples, "why this matters"
- **Shift emphasis**: Nuance → Core concepts, Edge cases → Happy path
- **Example (Medical)**: "Idiopathic hypertension, prescribe ACE inhibitor, monitor renal function" → "High blood pressure without clear cause. Medication helps blood vessels relax. Regular kidney checks needed."

**Novice → Expert:**
- **Remove**: Over-explanations, analogies, hand-holding
- **Add**: Precision, technical terms, caveats, edge cases
- **Shift emphasis**: Simplified model → Accurate complexity
- **Example**: "Make the button easier to click" → "Increase touch target to 44×44pt per iOS HIG, add 8pt padding, ensure 3:1 contrast ratio"

### Formal ↔ Informal

**Formal → Informal:**
- **Tone**: Third person → First person, Passive → Active, Complex → Simple
- **Structure**: Rigid sections → Conversational flow, Citations → Casual mentions
- **Language**: "Furthermore, it is evident" → "Also, you can see"
- **Example**: "The organization has determined that remote work arrangements shall be permitted" → "We're allowing remote work"

**Informal → Formal:**
- **Tone**: Contractions → Full words ("we're" → "we are"), Casual → Professional
- **Structure**: Loose → Structured sections with clear headers
- **Language**: "Stuff's broken" → "System experiencing degradation"
- **Example**: "Just shipped this cool feature!" → "Released enhanced functionality for improved user experience"

### Long-form ↔ Summary

**Long → Summary:**
- **Structure**: Inverted pyramid (most important first), bullet points, highlight key decisions/actions
- **Remove**: Supporting details, full context, exhaustive examples
- **Preserve**: Core findings, recommendations, next steps, critical caveats
- **Ratios**: 50 pages → 1 page (50:1), 1 hour → 5 min (12:1), Comprehensive → Highlights

**Summary → Long-form:**
- **Add**: Context, methodology, supporting evidence, alternative perspectives
- **Structure**: Introduction → Body → Conclusion, Multiple sections with subheadings
- **Preserve**: Original key points as outline, Expand each with detail

---

## Validation

Before finalizing, check:

**Semantic Fidelity (CRITICAL):**
- [ ] Core facts accurate? (No distortions or omissions that change meaning)
- [ ] Relationships preserved? (Cause-effect, dependencies, constraints intact)
- [ ] Caveats included? (Limitations, uncertainties, edge cases mentioned when relevant)
- [ ] Implications correct? (What this means for audience is accurate)
- [ ] Verifiable? (Expert in source domain would confirm translation is accurate)

**Audience Appropriateness:**
- [ ] Expertise match? (Not too technical or too dumbed-down for target)
- [ ] Jargon level right? (Explained when needed, used when understood)
- [ ] Goals addressed? (Decision-makers get options, implementers get how-to, learners get why)
- [ ] Tone appropriate? (Formality, emotion, register match audience expectations)
- [ ] Length appropriate? (Respects audience time constraints)

**Emphasis Alignment:**
- [ ] Priorities match audience? (Highlight what they care about)
- [ ] Details at right level? (Enough for understanding, not overwhelming)
- [ ] Actionability? (If audience needs to act, next steps are clear)
- [ ] Framing effective? (Positive/negative/neutral matches context and goal)

**Medium & Format:**
- [ ] Structure fits medium? (Email = skimmable, presentation = visual, document = reference)
- [ ] Formatting helps comprehension? (Headers, bullets, bold for key points)
- [ ] Accessibility? (Clear for non-native speakers if needed, links/references provided)

**Cultural/Demographic:**
- [ ] Idioms/references work? (Avoided US-centric idioms if international audience)
- [ ] Examples relatable? (Audience can connect to scenarios)
- [ ] Assumptions explicit? (Don't rely on shared context that target lacks)

**Minimum Standard:** Use rubric (resources/evaluators/rubric_translation_reframing_audience_shift.json). Average score ≥ 3.5/5 before delivering.

---

## Delivery Format

Create `translation-reframing-audience-shift.md` with:

**1. Source Analysis**
- Original audience: [Expertise, goals, context]
- Original content: [Brief excerpt or summary]
- Original tone/emphasis: [What was highlighted, how it was framed]

**2. Target Analysis**
- Target audience: [Expertise, goals, context]
- Translation type: [Technical→Business, Strategic→Tactical, etc.]
- Key constraints: [Length, medium, sensitivity]

**3. Translated Content**
- [Full translated version]
- [Formatted for target medium—bullets for emails, sections for docs, etc.]

**4. Translation Rationale**
- **What changed:** [Jargon removed, emphasis shifted to X, details reduced, analogies added]
- **What preserved:** [Core facts, key implications, critical caveats]
- **Why:** [Audience expertise gap, time constraints, medium requirements, cultural adaptation]

**5. Validation Notes**
- Semantic fidelity: ✓ Core facts accurate
- Audience match: ✓ Tone and depth appropriate for [target]
- Emphasis: ✓ Highlights [audience priorities]
- Limitations: [Any unavoidable compromises, e.g., "Some nuance lost for brevity"]

---

## Common Translation Patterns

**"So What?" Test (Technical → Business):** Every technical detail answers "so what?" - "Migrated to Kubernetes" → "Auto-scale during traffic spikes, 30% cost reduction" | "OAuth 2.0" → "Enterprise SSO, removes adoption barrier"

**"How?" Test (Strategic → Tactical):** Every goal answers "how?" - "Improve satisfaction" → "Response <2hr, add help center, NPS survey" | "AI-first company" → "Train PMs (Q1), hire 3 ML engineers (Q2), pilot feature (Q3)"

**Analogy Bridge (Expert → Novice):** Familiar → Unfamiliar - "Git branching" = essay draft versions | "Microservices" = food trucks not one restaurant | "API rate limiting" = nightclub capacity

**Inverted Pyramid (Long → Summary):** Most important first - Lede (1-2 sentences) → Key details (2-3 bullets) → Supporting (optional depth)

**Code-Switching (Cross-Cultural):** Replace cultural references - "Home run" (US) → "Big success" (neutral) | "Fire hose" idiom → "Overwhelming info" (literal) | MM/DD/YYYY → YYYY-MM-DD (ISO)

---

## Quick Reference

**Resources:**
- [resources/template.md](resources/template.md) - Structured translation workflow
- [resources/methodology.md](resources/methodology.md) - Advanced techniques for complex/nuanced translation
- [resources/evaluators/rubric_translation_reframing_audience_shift.json](resources/evaluators/rubric_translation_reframing_audience_shift.json) - Quality criteria

**Key Principles:**
- **Preserve semantic accuracy** - Facts, relationships, implications must remain true
- **Adapt presentation** - Tone, depth, emphasis change for audience
- **Match audience needs** - Expertise level, goals, context, constraints
- **Test with "would expert confirm?"** - Source domain expert validates translation accuracy
- **Test with "can target act on it?"** - Target audience can understand and use it

**Red Flags:**
- Semantic drift (facts become inaccurate through simplification)
- Talking down (condescending tone to novices)
- Jargon mismatch (too technical or too vague for audience)
- Missing "so what?" (technical details without business impact)
- Missing "how?" (strategic vision without tactical translation)
- Lost nuance (critical caveats omitted for brevity)
- Cultural assumptions (idioms, references that exclude target)
- Wrong emphasis (highlighting what you find interesting vs. what audience needs)
