---
name: paper-writing
description: Expert guidance for writing high-quality academic and research papers. Use when the user wants to write, structure, revise, or improve academic papers, research articles, conference papers, or technical reports. Provides comprehensive support for all stages from planning to final polish.
license: MIT
compatibility: Works with any text editor or document format. Optimized for academic writing in LaTeX, Markdown, Word, or plain text.
metadata:
  category: writing
  version: 1.0.0
  author: Claude Code Community
---

# Academic Paper Writing Skill

This skill provides comprehensive guidance for writing excellent academic and research papers across all disciplines. It covers structure, style, argumentation, and best practices from initial planning through final revision.

## When to Use This Skill

Use this skill when working on:
- Research papers and journal articles
- Conference papers and proceedings
- Technical reports and white papers
- Thesis chapters and dissertations
- Literature reviews and survey papers
- Position papers and perspectives

## Quick Start

For immediate guidance, see the task-specific workflows below. For comprehensive reference material, consult:
- `references/REFERENCE.md` - Complete writing guidelines and best practices
- `references/STRUCTURE.md` - Detailed templates for different paper types
- `references/STYLE.md` - Writing style and clarity guidelines
- `assets/` - Ready-to-use paper templates

## Core Workflow

### 1. Planning Phase

**Understand the Requirements**
- Identify target venue (journal, conference, report)
- Check formatting requirements (APA, IEEE, ACM, Chicago, etc.)
- Note page limits, section requirements, and citation style
- Clarify submission deadlines and review process

**Define the Research Question**
- Formulate a clear, focused research question or hypothesis
- Ensure the question is specific, measurable, and answerable
- Identify the gap in existing knowledge or practice
- State the contribution your work will make

**Create an Outline**
- Draft section headings based on paper type (see Structure section)
- Allocate approximate space to each section
- Identify key points for each section
- Map evidence and references to sections

### 2. Writing Phase

**Follow the Structured Approach**

Work section-by-section, not necessarily in order. Many authors write in this sequence:
1. Methods (clearest, most concrete)
2. Results (present findings)
3. Introduction (frame the problem)
4. Discussion (interpret results)
5. Conclusion (summarize contributions)
6. Abstract (last, summarizes everything)

**Section-Specific Guidance**

**Abstract (150-300 words)**
- State the problem and motivation (1-2 sentences)
- Describe your approach/method (1-2 sentences)
- Summarize key results (2-3 sentences)
- State conclusions and implications (1-2 sentences)
- Make it self-contained (no citations, no undefined acronyms)

**Introduction**
- Hook: Why should anyone care? (1 paragraph)
- Context: What's the broader problem space? (1-2 paragraphs)
- Gap: What's missing in current solutions? (1 paragraph)
- Your contribution: What does this paper do? (1 paragraph)
- Paper organization: Brief roadmap (optional, 1 paragraph)

**Related Work / Literature Review**
- Group work thematically, not chronologically
- Compare and contrast approaches
- Identify limitations of existing work
- Position your work clearly vs. alternatives
- Be fair and accurate (don't strawman competitors)

**Methodology / Approach**
- Describe methods with enough detail for replication
- Justify design choices
- Define metrics and evaluation criteria
- Explain data collection and analysis procedures
- Include diagrams for complex processes

**Results**
- Present findings objectively without interpretation
- Use tables and figures effectively (see Visualization section)
- Report statistical significance where applicable
- Address both positive and negative results
- Organize by research question or hypothesis

**Discussion**
- Interpret results in context of research questions
- Compare with related work
- Explain unexpected findings
- Acknowledge limitations honestly
- Discuss implications for theory and practice

**Conclusion**
- Restate key contributions (1 paragraph)
- Summarize main findings (1 paragraph)
- Discuss broader implications (1 paragraph)
- Suggest future work (1 paragraph)
- End with a strong closing statement

### 3. Refinement Phase

**First Revision: Structure and Argument**
- Does each section serve its purpose?
- Is the argument logical and complete?
- Are transitions between sections smooth?
- Does evidence support all claims?
- Are counterarguments addressed?

**Second Revision: Clarity and Style**
- Remove jargon and define technical terms
- Eliminate redundancy and wordiness
- Use active voice for clarity (prefer "We analyzed" over "Analysis was performed")
- Ensure parallel structure in lists
- Check paragraph length (aim for 4-8 sentences)

**Third Revision: Polish**
- Check grammar, spelling, punctuation
- Verify all citations are formatted correctly
- Ensure figures/tables are referenced in text
- Number sections, equations, figures consistently
- Proofread carefully (reading aloud helps)

## Visualization Best Practices

**Tables**
- Use for precise numerical comparisons
- Keep simple and readable (avoid excessive gridlines)
- Include clear column headers and units
- Caption goes above the table
- Reference in text before the table appears

**Figures**
- Use for trends, patterns, relationships
- Ensure axes are labeled with units
- Use readable fonts (at least 10pt in final size)
- Caption goes below the figure
- Make interpretable in grayscale (avoid color-only distinctions)

**General Rules**
- Every table/figure must be referenced in the text
- Each should be self-explanatory with its caption
- Number consecutively (Figure 1, Figure 2, etc.)
- Place close to first reference when possible

## Common Pitfalls to Avoid

**Structural Issues**
- ❌ Burying the contribution in the middle
- ✅ State contribution clearly in introduction
- ❌ Results section that interprets rather than presents
- ✅ Keep results objective, interpret in discussion
- ❌ Conclusion that introduces new information
- ✅ Conclusion only synthesizes existing content

**Writing Issues**
- ❌ Passive constructions: "It was found that..."
- ✅ Active voice: "We found that..."
- ❌ Hedging excessively: "It seems to possibly suggest..."
- ✅ Be direct: "The results indicate..."
- ❌ Undefined acronyms and jargon
- ✅ Define terms on first use

**Citation Issues**
- ❌ Missing citations for claims
- ✅ Every factual claim needs a source
- ❌ Over-citing obvious facts
- ✅ Common knowledge doesn't need citation
- ❌ Citing without reading (citation padding)
- ✅ Cite only what you've actually read and verified

## Discipline-Specific Considerations

**Computer Science / Engineering**
- Emphasize reproducibility and implementation details
- Include complexity analysis where relevant
- Provide algorithm pseudocode or code snippets
- Compare against state-of-the-art baselines
- Make code/data available when possible

**Natural Sciences**
- Follow strict IMRAD structure (Intro, Methods, Results, Discussion)
- Report statistical power and effect sizes
- Include detailed experimental protocols
- Address confounding variables
- Report null results honestly

**Social Sciences**
- Contextualize within theoretical frameworks
- Justify sampling and participant selection
- Report demographic information
- Address potential biases
- Discuss generalizability limitations

**Humanities**
- Develop clear thesis statement
- Support arguments with textual evidence
- Engage with scholarly debates
- Use close reading and analysis
- Contextualize within historical/cultural frameworks

## Conversation-First Approach

When helping users write papers, prioritize natural conversation over rapid-fire questions:

1. **Start simple**: Ask ONE opening question to understand their situation
   - "What's your paper about?" (topic/working title)
   - OR "What stage are you at?" (if they're already focused)

2. **Listen and follow up**: Based on their answer, ask the next most relevant question
   - If they're starting: Ask about target venue or research gap
   - If they're revising: Ask which section needs work
   - If they're stuck: Ask what specific challenge they're facing

3. **Build context progressively**: Let information emerge naturally through dialogue

4. **Provide targeted help**: Focus on their immediate need, not all possible topics

5. **Maintain author voice**: Edit to improve, not to rewrite in a different style

6. **Explain recommendations**: Help them understand why changes strengthen their paper

7. **Load references as needed**: Use reference documents for deeper guidance only when relevant

## Using Reference Materials

This skill includes detailed reference materials for deeper guidance:

- **Load `references/REFERENCE.md`** for comprehensive writing guidelines, style guides, and detailed best practices
- **Load `references/STRUCTURE.md`** for complete templates for different paper types (journal article, conference paper, thesis, etc.)
- **Load `references/STYLE.md`** for in-depth guidance on academic writing style, word choice, and clarity
- **Check `assets/`** for ready-to-use templates in various formats

Only load these materials when needed to conserve context. For most tasks, the guidance above is sufficient.

## Progressive Enhancement

**Basic use**: Follow the Core Workflow for writing or revising papers

**Intermediate use**: Consult reference materials for specific sections or challenges

**Advanced use**: Use templates from assets/ and customize for specific venues

## Quality Checklist

Before considering a paper complete, verify:

- [ ] Clear research question or contribution stated in introduction
- [ ] All claims supported by evidence or citations
- [ ] Logical flow from section to section
- [ ] Methods sufficiently detailed for replication
- [ ] Results presented objectively
- [ ] Discussion interprets results and addresses limitations
- [ ] All figures/tables referenced in text and have clear captions
- [ ] Citations formatted consistently
- [ ] Abstract accurately summarizes the paper
- [ ] No typos or grammatical errors
- [ ] Meets venue requirements (format, length, style)

## Examples

**Example 1: Progressive discovery—starting fresh**

```
User: Help me write a research paper.

Claude: What's your paper about? (topic, working title, or research question)

User: It's about federated learning for edge devices.

Claude: Got it—that's a focused topic. Are you at the stage of having completed
research and needing to write it up, or are you still planning the work?

User: I've done the research and have preliminary results. I just don't know
where to start.

Claude: Perfect—let me help you structure this. What's your target venue?
(e.g., a specific conference, journal, or is this a thesis chapter?)
```

Notice: One question asked, then the next, building naturally from their answers.

---

**Example 2: Targeted revision (existing draft)**

```
User: My introduction feels weak and I'm not sure why.

Claude: I'd like to take a look. Can you share what you have, or tell me
what the main challenge is? (e.g., doesn't grab attention, doesn't explain
why this work matters, etc.)

User: I think I'm not making the research gap clear enough. Here's what I wrote...

Claude: [Reads their draft]

Looking at your introduction, I see you've identified the problem nicely,
but you're right—the gap (what's missing in current solutions) isn't
explicit. Here's what I'd suggest...
```

Notice: Start with curiosity about their specific challenge, then provide
targeted feedback on the actual content.

---

**Example 3: Stuck in the middle**

```
User: I have my methods section written, but I'm stuck on results.

Claude: What's tripping you up about the results section specifically?
(e.g., how to organize findings, whether to include raw data, interpretation
vs. presentation, etc.)

User: I have a lot of data. I don't know what to include and how to present it
so it's not overwhelming.

Claude: That's a common challenge. Let me help you think through data selection
and visualization...
```

Notice: Rather than lecturing about results sections in general, we drill down
into their specific problem first.

## Tips for Success

**Writing Process**
- Write regularly in focused sessions (2-3 hours)
- Don't edit while drafting (separate creation from refinement)
- Get feedback early and often
- Read papers in your target venue for style/structure

**Revision Strategy**
- Take breaks between revision passes
- Read paper aloud to catch awkward phrasing
- Get fresh eyes (colleagues, advisors)
- Use revision checklist systematically

**Time Management**
- Allocate 40% planning, 30% writing, 30% revision
- Build in buffer time before deadlines
- Start with rough drafts, refine iteratively
- Don't aim for perfection in first draft

Remember: All good papers go through multiple revisions. Writing is rewriting.

## Sources and Credits

This skill is based on authoritative academic writing resources:

- **Thatcher, Jason Bennett** (2024). "Rules for Writing Elite Information Systems Papers." Available at SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5993034 or http://dx.doi.org/10.2139/ssrn.5993034
- **APA Publication Manual** (7th Edition)
- **IEEE Editorial Style Manual**
- Academic writing best practices from Ohio University, Duke University, MIT, USC, and UCSD
