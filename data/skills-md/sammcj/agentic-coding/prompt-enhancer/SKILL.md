---
name: prompt-enhancer
description: |
 Knowledge for transforming poor or overly simple user prompts with expert-level framing. Triggers include: user explicitly asking to improve/refine/rewrite their prompt or user requesting help framing a request for another AI system.
# model: inherit
# context: fork
# user-invocable: true
# allowed-tools: Read,Write,Bash,Grep,WebFetch,WebSearch
---

# Expert Prompt Enhancer

Transform prompts written by non-specialists into the form a domain expert would use to make the same request.
The intent is to give people the benefits of expert framing without requiring them to learn domain-specific language or problem structuring.

## Why This Matters

Research demonstrates that AI output quality correlates strongly with input sophistication. AI systems exhibit "parahuman" psychology - they respond to expertise signals, authority framing, and precise problem specification the same way humans do. A vaguely-worded request yields generic output; an expert-framed request yields expert-quality output. This skill bridges that gap without changing *what* someone asks for - only *how* it's expressed.

## Expert Communication Patterns

Expert requests differ from novice requests in predictable ways:

| Pattern           | Novice               | Expert                                        |
|-------------------|----------------------|-----------------------------------------------|
| **Precision**     | "make it faster"     | "optimise page load performance"              |
| **Decomposition** | Single vague request | Broken into logical components                |
| **Constraints**   | Unstated             | Explicit limits, trade-offs, success criteria |
| **Context**       | Missing              | System fit, standards, prior attempts         |
| **Role framing**  | None                 | "As a database architect, review this schema" |
| **Failure modes** | Ignored              | Anticipated and specified                     |

## What expert communication looks like

Expert requests differ from novice requests in predictable ways:

**They name things precisely.** Experts use domain-specific terminology because it's unambiguous. "Optimise page load performance" vs "make it faster". "Implement rate limiting" vs "stop people using it too much".

**They decompose problems.** Experts break requests into logical components, identify dependencies, and sequence appropriately. They know what sub-problems exist within a request.

**They specify constraints and success criteria.** Experts state what limits apply, what trade-offs are acceptable, and what "done" looks like in measurable terms.

**They establish context.** Experts situate problems: what system does this fit into, what standards apply, why does this matter, what's been tried before.

**They assign appropriate roles.** Experts often frame who should be doing the work: "As a database architect, review this schema" rather than "look at this database stuff".

**They anticipate failure modes.** Experts know what can go wrong and specify what to avoid or handle.

## Transformation Process

1. **Identify the domain** - Who would professionally handle this? What terminology and standards apply?
2. **Find core intent** - What does the user actually want beneath imprecise language?
3. **Surface ambiguity** - Fill obvious gaps with reasonable defaults. Only flag genuine ambiguities where guessing could go wrong.
4. **Apply expert patterns** - Precise terminology, decomposition, constraints, success criteria, role framing.
5. **Match complexity to task** - A simple question needs clarity, not PhD-level complexity.

## Examples

These illustrate the transformation from novice to expert framing:

---

**Original:** "My back hurts, what should I do?"

**Expert rewrite:** "Provide guidance on managing back pain. Cover: how to assess whether back pain warrants professional evaluation vs self-care, red flag symptoms that require urgent attention, evidence-based self-care approaches for common musculoskeletal back pain, activity modifications that help vs hurt recovery, and when to consider different types of practitioners (GP, physio, chiropractor, etc.). Focus on helping me make informed decisions rather than diagnosing."

**What changed:** Reframed from "tell me what to do" to "help me understand decision-making for this situation". Specified the information categories that would actually be useful. Acknowledged appropriate scope limitations.

---

**Original:** "Help me eat healthier"

**Expert rewrite:** "I want to improve my eating habits sustainably. Rather than a strict diet plan, give me: the highest-impact changes that nutrition research actually supports (not fads), practical strategies for implementation that account for real-world constraints like time and budget, how to think about trade-offs (e.g., when 'good enough' beats 'perfect'), and common pitfalls that derail people. I'm more interested in building lasting habits than optimising for rapid results."

**What changed:** Specified the type of advice wanted (sustainable habits vs strict plans), named the decision framework (high-impact, evidence-based), set the optimisation target (lasting change vs rapid results), anticipated failure modes.

---

**Original:** "Help me be more productive"

**Expert rewrite:** "I want to improve my personal productivity. Approach this as a diagnostic: what are the most common root causes of productivity problems (energy management, prioritisation, environment, systems, motivation), how do I identify which apply to me, and what interventions match each root cause? I'd rather understand the underlying principles than get a list of tips and apps. Include how to evaluate whether a change is actually working."

**What changed:** Reframed from "give me tips" to "help me diagnose and address root causes". Asked for principles over tactics. Included success criteria (how to evaluate).

---

**Original:** "My teenager won't listen to me"

**Expert rewrite:** "I'm experiencing communication difficulties with my teenager. Help me understand: what's developmentally normal in adolescent behaviour around authority and autonomy, communication patterns that typically backfire with teenagers (so I can check if I'm using them), evidence-based approaches that work with adolescent psychology rather than against it, and how to distinguish between normal boundary-testing and genuinely concerning behaviour. I want to improve the relationship, not just achieve compliance."

**What changed:** Reframed the goal from compliance to relationship quality. Asked for developmental context that explains the behaviour. Requested both what to avoid and what works. Set realistic expectations.

---

**Original:** "Write me a short story"

**Expert rewrite:** "Write a short story of around 2,000 words. Aim for literary fiction with a reflective tone - the kind of piece that might appear in a quality magazine. Focus on a small, specific moment that reveals something larger about a character or relationship. Prioritise voice and interiority over plot mechanics. End with resonance rather than resolution. Surprise me with the premise."

**What changed:** Specified length, genre positioning, and tone. Named craft priorities (voice, interiority, resonance). Gave clear aesthetic direction while leaving creative freedom on subject matter.

---

**Original:** "Help me negotiate my salary"

**Expert rewrite:** "I need to negotiate salary for a job offer. Walk me through: how to research and establish my market value, the psychology of negotiation (anchoring, framing, reciprocity) applied to compensation discussions, specific language and tactics that work in salary conversations, common mistakes that weaken negotiating position, and how to handle common employer responses (budget constraints, equity offers, delayed reviews). Include how to negotiate non-salary elements if base salary is genuinely fixed."

**What changed:** Decomposed "negotiate" into component skills. Named relevant psychological principles. Anticipated the specific scenarios that arise. Included fallback strategies.

---

**Original:** "Explain machine learning to me"

**Expert rewrite:** "Explain machine learning for someone with no technical background. Cover: the core insight of what makes ML different from traditional programming (learning patterns vs following rules), the main categories of ML problems (supervised, unsupervised, reinforcement) with one concrete real-world example each, and an honest assessment of what ML is genuinely good at vs where it struggles or gets overhyped. Use analogies rather than maths. Keep it under 800 words."

**What changed:** Set audience level explicitly, specified structure and scope, requested concrete examples, asked for honest limitations (not just capabilities), set format constraints.

---

**Original:** "Help me write a cover letter for a marketing job"

**Expert rewrite:** "Draft a cover letter for a marketing position. Structure: open with a hook that demonstrates strategic thinking about the company or market (not generic enthusiasm), move into 2-3 specific examples of marketing impact I've delivered (I'll provide details), close with a confident call to action. Tone should be professionally warm, commercially-minded, and specific rather than vague. 300 words maximum. Avoid clichés like 'passionate about marketing' or 'excited for this opportunity'."

**What changed:** Specified rhetorical structure that hiring managers respond to. Set tone parameters with examples of what to avoid. Length constraint. Indicated what input is needed without requiring the user to restructure anything.

---

**Original:** "Make my website faster"

**Expert rewrite:** "Analyse website performance and provide prioritised optimisation recommendations. Assess the main performance dimensions: server response time, render-blocking resources, asset optimisation (images, scripts, stylesheets), caching strategy, and third-party script impact. For each issue identified, explain the problem, the fix, and the expected impact. Prioritise by effort-to-impact ratio. I'll provide the URL or performance data."

**What changed:** Named the diagnostic framework (performance dimensions). Specified output format (problem/fix/impact). Set prioritisation criteria. Established this as analysis before action.

---

**Original:** "I need a Python script to clean up my data"

**Expert rewrite:** "Help me write a Python script for data cleaning. I'll share a sample of the data - from that, identify the data quality issues present (missing values, duplicates, inconsistent formats, outliers, encoding problems) and write cleaning code that handles each. Use pandas. Include validation that confirms the cleaning worked. Structure the code so each cleaning step is separate and commented, making it easy to modify for my specific needs."

**What changed:** Established a workflow (show sample → identify issues → write code). Specified the tool. Asked for validation and modular structure. This version can proceed once data is shared, without requiring the user to pre-diagnose their own data problems.

---

## Your transformation approach

When rewriting a prompt:

1. **Identify the domain and who would professionally handle this request.** This tells you what terminology, standards, and mental models apply.

2. **Find the core intent beneath imprecise language.** What does the user actually want to achieve or understand?

3. **Identify what's implicit or ambiguous.** What has the user not specified that would affect the outcome? Distinguish between:

    - Gaps you can fill with reasonable defaults (do this)
    - Genuine ambiguities where guessing could go badly wrong (flag these)
4. **Reframe using expert patterns:** precise terminology, appropriate decomposition, explicit constraints, success criteria, and role framing where helpful.

5. **Match complexity to the task.** A simple question needs professional-level clarity, not PhD-level complexity. Don't inflate.

## Constraints

- **Preserve intent absolutely.** You elevate how something is asked, never what is asked.
- **Don't invent requirements.** Fill obvious gaps with reasonable defaults; don't add things the user didn't imply.
- **Make reasonable assumptions rather than asking the user to specify everything.** The goal is to improve prompts without creating work for the user. Only surface ambiguity when guessing wrong would lead to a significantly worse outcome.
- **Use correct terminology, not impressive terminology.** Domain language should clarify, not obscure or intimidate.
- **Don't be precious about the output format.** For simple transformations, a straightforward rewrite is fine. Only add explanatory notes when the transformation involves non-obvious choices.

## Output

Provide the expert rewrite. If you made assumptions about ambiguous elements, or if there are meaningful alternative framings the user might prefer, note these briefly after the rewrite.
