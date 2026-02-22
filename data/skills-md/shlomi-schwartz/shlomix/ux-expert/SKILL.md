---
name: ux-expert
description: Always-on UX advisor that surfaces relevant Laws of UX when building or modifying UI components. Proactively activates when creating, editing, or reviewing any user interface — components, layouts, navigation, forms, interactions, or visual design. Covers 30 laws across decision-making, cognition, visual organization, memory, engagement, and design principles.
---

# UX Expert

Indexes 30 Laws of UX from lawsofux.com and proactively advises during UI/UX development. Searches the law index below, reads relevant law files, follows relationship links when warranted, and fetches external resources for deeper context.

## When to Activate

Trigger this skill when:
- Creating or modifying UI components, pages, or layouts
- Adding options, choices, dropdowns, menus, or navigation items
- Changing layouts, spacing, visual grouping, or element positioning
- Modifying navigation flows, forms, or interactive elements
- Reviewing or discussing UI/UX design decisions
- Working on response time, loading states, or perceived performance
- Handling touch targets, click areas, or element sizing
- Any user-facing interface work where UX quality matters

## Law Index

### Decision & Choice
- **Choice Overload** (`choice-overload.md`) — Users get overwhelmed with too many options; reduce, categorize, or add filtering
- **Hick's Law** (`hicks-law.md`) — Decision time increases with number and complexity of choices; minimize options when speed matters
- **Tesler's Law** (`teslers-law.md`) — Every system has irreducible complexity; absorb it in design so users don't have to
- **Postel's Law** (`postels-law.md`) — Be liberal in what you accept from users, conservative in what you output

### Cognitive Capacity
- **Cognitive Load** (`cognitive-load.md`) — Total mental resources needed to use an interface; minimize extraneous load
- **Miller's Law** (`millers-law.md`) — Working memory holds ~7 (plus/minus 2) items; chunk information into groups
- **Chunking** (`chunking.md`) — Break information into meaningful groups to aid comprehension and recall
- **Working Memory** (`working-memory.md`) — Temporary cognitive storage for active tasks; don't force users to remember across steps
- **Selective Attention** (`selective-attention.md`) — Users focus on goal-relevant stimuli and miss the rest; design for what matters

### Visual Organization (Gestalt)
- **Law of Proximity** (`law-of-proximity.md`) — Near elements are perceived as grouped; use spacing to signal relationships
- **Law of Similarity** (`law-of-similarity.md`) — Similar-looking elements are perceived as related; use consistent styling for groups
- **Law of Common Region** (`law-of-common-region.md`) — Elements sharing a bounded area are perceived as grouped
- **Law of Uniform Connectedness** (`law-of-uniform-connectedness.md`) — Visually connected elements are perceived as more related
- **Law of Pragnanz** (`law-of-pragnanz.md`) — Users interpret complex visuals in the simplest form possible; favor clarity

### Memory & Perception
- **Serial Position Effect** (`serial-position-effect.md`) — Users best remember first and last items in a series; place key actions there
- **Von Restorff Effect** (`von-restorff-effect.md`) — The distinct item among similar ones is most remembered; use for CTAs
- **Peak-End Rule** (`peak-end-rule.md`) — Experiences are judged by their peak moment and ending, not the average
- **Zeigarnik Effect** (`zeigarnik-effect.md`) — Incomplete tasks are remembered better; use progress indicators to drive completion
- **Cognitive Bias** (`cognitive-bias.md`) — Systematic thinking errors that shape perception and decisions

### Engagement & Motivation
- **Flow** (`flow.md`) — State of deep immersion; balance challenge and skill, remove friction
- **Goal-Gradient Effect** (`goal-gradient-effect.md`) — Effort increases as users approach a goal; show progress to motivate
- **Paradox of the Active User** (`paradox-of-the-active-user.md`) — Users skip instructions and learn by doing; design for exploration
- **Parkinson's Law** (`parkinsons-law.md`) — Tasks expand to fill available time; use constraints and deadlines

### Design Principles
- **Jakob's Law** (`jakobs-law.md`) — Users expect your site to work like others they know; leverage existing mental models
- **Aesthetic-Usability Effect** (`aesthetic-usability-effect.md`) — Beautiful interfaces are perceived as more usable and forgive minor issues
- **Doherty Threshold** (`doherty-threshold.md`) — Keep response times under 400ms to maintain user engagement and flow
- **Fitts's Law** (`fittss-law.md`) — Target acquisition time depends on distance and size; make key elements large and close
- **Mental Model** (`mental-model.md`) — Users' internal representation of how a system works; align design with expectations
- **Occam's Razor** (`occams-razor.md`) — Prefer the simplest solution that meets requirements; remove unnecessary elements
- **Pareto Principle** (`pareto-principle.md`) — ~80% of effects come from ~20% of causes; focus effort on high-impact elements

> **Slug notes**: Fitts's Law = `fittss-law.md`, Hick's Law = `hicks-law.md`, Jakob's Law = `jakobs-law.md`, Miller's Law = `millers-law.md`, Tesler's Law = `teslers-law.md`, Postel's Law = `postels-law.md`, Law of Pragnanz = `law-of-pragnanz.md`

## Search & Retrieval Process

1. Extract context keywords from the current UI/UX work (component type, interaction pattern, design concern)
2. Scan the law index above — match keywords, categories, and descriptions to the task
3. Read 1-3 most relevant law files from `references/laws/`
4. Check the `## Related` section of each law read
5. Decide whether to read related laws (see traversal rules below)
6. When a law's `## Further Reading` links are directly relevant, fetch them for deeper context (see deep dive rules below)
7. Synthesize findings into actionable, specific advice

## Relationship Traversal — When to Read Deeper

After reading a primary law, examine its `## Related` section. Related laws use format `[Law Name](/slug/)` — map the slug to `references/laws/{slug}.md`.

**Read a related law when:**
- The related law's topic directly applies to the current UI context
- The primary law's takeaways reference concepts covered by the related law
- The user's change touches multiple UX dimensions that span both laws

**Skip a related law when:**
- It covers a UX dimension not relevant to the current task
- The primary law already provides sufficient guidance
- Reading more would delay actionable advice without adding value

**Limits:** Max 1 level of related-law traversal (never follow related-of-related). Max 4-5 total laws read per context (primary + related).

## Deep Dive — When to Fetch Further Reading

Each law file has a `## Further Reading` section with external links (Nielsen Norman Group, Smashing Magazine, etc.). These contain detailed research, examples, and case studies.

**Fetch a Further Reading link when:**
- The user is making a significant design decision and needs evidence-based justification
- The law's key takeaways alone are insufficient — the user needs implementation specifics or real-world examples
- Multiple laws conflict or create tension and external context would help resolve the tradeoff
- The user explicitly asks for deeper rationale or research backing

**Skip fetching when:**
- The key takeaways in the law file are sufficient for the advice needed
- The task is a minor UI tweak where general guidance is enough
- Fetching would slow down time-sensitive advice without meaningful benefit

**Limits:** Max 2-3 external fetches per context. Prefer Nielsen Norman Group and Interaction Design Foundation links (highest signal-to-noise).

## Output Format

- Lead with the specific recommendation: what to do or what to change
- Name the supporting law(s) — e.g., "Hick's Law suggests..."
- Quote the most relevant key takeaway(s) from the law file
- If multiple laws converge, note the pattern: "Both Hick's Law and Choice Overload point to..."
- If a Further Reading source was fetched, briefly cite the key insight from it
- Keep it concise: 3-6 sentences, not an essay
- Only advise when a law is clearly relevant or being violated — never force-fit
