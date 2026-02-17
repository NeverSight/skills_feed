---
name: skill-creator-v2
description: Create high-quality agent skills using a principle-driven approach. Use this when you need to create a new skill or improve an existing one, focusing on expertise transfer rather than mechanical instructions. This skill emphasizes research, synthesis, critique, and the four core truths of skill design.
---

# Skill Creator v2: Principle-Driven Skill Design

This skill guides you through creating skills that **transfer expertise**, not just list instructions.

## The 4 Core Truths

Every skill you create must embody these principles:

| Truth | What It Means | In Practice |
|-------|---------------|-------------|
| **Expertise Transfer, Not Instructions** | Make Claude think like an expert, not follow steps | Teach mental models and decision frameworks, not checklists |
| **Flow, Not Friction** | Produce output, not intermediate documents | Go straight to deliverables - no "now write a plan" steps |
| **Voice Matches Domain** | Sound like a practitioner, not documentation | Use domain language naturally, avoid meta-commentary |
| **Focused Beats Comprehensive** | Constrain ruthlessly | Every section must justify its token cost |

## When to Use This Skill

Use this skill when:
- Creating a new skill from scratch
- A skill isn't performing well and needs rethinking
- You want to understand *why* certain patterns work
- You need to make tough trade-offs about what to include

**Don't use this for:**
- Quick iterations on working skills (use the standard skill-creator)
- Just packaging an existing skill (use packaging scripts directly)

## The 10-Step Process

```
UNDERSTAND the problem
    ↓
EXPLORE Claude's failures  
    ↓
RESEARCH domain expertise
    ↓
SYNTHESIZE principles
    ↓
DRAFT the skill
    ↓
SELF-CRITIQUE rigorously
    ↓
ITERATE on feedback
    ↓
TEST on real scenarios
    ↓
FINALIZE structure
    ↓
PACKAGE for distribution
```

### 1. UNDERSTAND → What skill? What problem?

Start by crystallizing the core need:
- **What specific capability gap exists?** (Not "documentation" but "Claude rewrites the same 50-line parsing script every time")
- **What does success look like?** (Concrete examples of before/after)
- **Who benefits and how?** (Time saved? Quality improved? Consistency achieved?)

**Good examples:**
- "Engineers spend 20 minutes each time formatting API responses to match our schema"
- "Claude generates valid SQL but doesn't know our table relationships"
- "We need Claude to follow our 47-point brand guidelines without a wall of text"

**Bad examples:**
- "Make Claude better at X" (too vague)
- "Help with documents" (too broad)

**Output:** A crisp problem statement you could explain in 30 seconds.

### 2. EXPLORE → See where Claude fails without guidance

**Critical step - don't skip this.** You need to *observe* the failure mode, not imagine it.

Try the task without the skill:
1. Give Claude a representative request
2. Note where it struggles, hesitates, or produces suboptimal output
3. Try 3-5 variations to see if it's consistent

**Document:**
- What did Claude do wrong?
- What knowledge was it missing?
- What did it waste time on?
- When did it ask for clarification vs. guess?

**Example observations:**
- "Claude generated working code but used pandas when our stack is polars"
- "Claude wrote a 200-line form instead of using our 10-line template"
- "Claude asked what format we wanted - it should know we always use ISO 8601"

**Why this matters:** You're designing for *actual* failure modes, not theoretical ones. This prevents over-specifying (wasting tokens) or under-specifying (skill doesn't help).

### 3. RESEARCH → Go deep on the domain

Now that you know *what* fails, understand *why* success looks like and what experts know.

**For technical domains:**
- What mental models do experts use?
- What are the key decision points?
- What patterns repeat across scenarios?
- What's stable vs. what varies?

**For workflow domains:**
- What's the expert's internal checklist?
- What do they check for quality?
- What shortcuts do they know?
- What mistakes do novices make?

**Research sources:**
- Interview domain experts
- Review high-quality examples
- Read practitioner documentation (not beginner tutorials)
- Analyze your own expert behavior

**Output:** A list of insights that would make Claude competent, not just capable.

### 4. SYNTHESIZE → Extract principles from research

Transform observations into teachable principles.

**Pattern recognition:**
- What do all good examples have in common?
- What varies based on context?
- What rules have exceptions? (Document both)
- What can be expressed as "if X then Y"?

**Compression:**
- Can 5 bullet points become 1 principle?
- Can 3 examples show a pattern?
- Can a decision tree replace prose?

**Example synthesis:**
```
Raw research:
- Example 1 uses indentation for hierarchy
- Example 2 uses bullet points for parallel items
- Example 3 uses numbered lists for sequences
- Example 4 combines all three appropriately

Synthesized principle:
"Match structure to meaning: indent for hierarchy, bullets for parallelism, numbers for sequence."
```

**Output:** Distilled principles that transfer expertise, not just information.

### 5. DRAFT → Write initial skill

Now you can draft. Structure using **progressive disclosure**:

```
skill-name/
├── SKILL.md          # Core workflow + principles (<500 lines)
│   ├── YAML frontmatter (name, description)
│   └── Essential instructions
├── references/       # Deep knowledge (loaded as needed)
│   ├── patterns.md
│   └── examples.md
├── scripts/          # Executable code
│   └── helper.py
└── assets/           # Templates, not documentation
    └── template.json
```

**Frontmatter:**
```yaml
---
name: skill-name
description: >
  What the skill does + when to trigger it. Be specific about use cases.
  Good: "Process medical transcripts following HIPAA guidelines, including
  de-identification and structured output formatting."
  Bad: "Help with medical documents."
---
```

**SKILL.md structure:**

```markdown
# Skill Name

[One paragraph: what problem this solves]

## Core Approach

[The mental model - how an expert thinks about this domain]

## When [Most Common Scenario]

[Direct instructions using imperative form]
[Include only essential decision points]
[Reference detailed guides in references/ as needed]

## When [Second Most Common Scenario]

[...]

## Quality Checks

[What good output looks like - help Claude self-evaluate]
```

**Key drafting principles:**

1. **Imperative mood**: "Extract text" not "You should extract text"
2. **Example over explanation**: Show one good example > describe in prose
3. **Decision points explicit**: "If X then Y, otherwise Z"
4. **Offload detail**: "See references/advanced.md" not "here's 500 words"
5. **Quality criteria**: Help Claude know when it's done

### 6. SELF-CRITIQUE → Review against quality criteria

Now be ruthlessly critical. For each section, ask:

**Expertise Transfer Test:**
- [ ] Does this make Claude *think* like an expert or just *act* like one?
- [ ] Would a domain expert recognize this approach?
- [ ] Are we teaching patterns or prescribing steps?

**Flow Test:**
- [ ] Can Claude go straight to output?
- [ ] Do we force intermediate artifacts Claude doesn't need?
- [ ] Would an expert work this way?

**Voice Test:**
- [ ] Does this sound like domain documentation or AI instructions?
- [ ] Would a practitioner say "execute step 3" or just do it?
- [ ] Are we narrating process or enabling work?

**Focus Test:**
- [ ] Can we delete this section and still succeed? (If yes, delete it)
- [ ] Is this addressing observed failure modes? (If no, question it)
- [ ] Could this be a one-line reference instead?

**Token Efficiency Test:**
- [ ] Would this information surprise Claude? (If no, cut it)
- [ ] Is this stable knowledge vs. variable context?
- [ ] Should this be in SKILL.md or references/?

**Progressive Disclosure Test:**
- [ ] Do we force-load information Claude might not need?
- [ ] Can variations go in separate reference files?
- [ ] Are scripts documented or just executable?

**Red flags:**
- Phrases like "you should", "make sure to", "don't forget"
- Apologetic language: "This might seem complex but..."
- Meta-commentary: "The next step is to..."
- Over-specification: Dictating every detail when heuristics suffice
- Under-specification: Vague guidance on fragile operations

### 7. ITERATE → Fix gaps, get feedback, improve

**Testing approaches:**

1. **Yourself:** Use the skill on real scenarios - note friction
2. **Others:** Have someone else try it - watch where they struggle  
3. **Claude:** Have Claude use it - monitor for confusion or errors

**Feedback loop:**
```
Use skill → Note issue → Hypothesis on why → Update skill → Test again
```

**Common improvements:**
- **Too much guidance:** Claude over-thinks → Trust Claude more, delete text
- **Too little guidance:** Claude guesses wrong → Add decision framework
- **Wrong abstraction:** Scenarios don't map cleanly → Reorganize around real patterns
- **Missing context:** Claude lacks key info → Move knowledge from your head to references/

**Iteration triggers:**
- Claude asks questions that the skill should answer
- Output quality varies unexpectedly
- Claude ignores parts of the skill
- You find yourself adding ad-hoc instructions in chat

### 8. TEST → Use skill on a real scenario

Final validation with a realistic task:

1. **Pick a task** that's representative but not used during design
2. **Use the skill** as if you're a new user
3. **Document:**
   - Did it work on first try?
   - Where did Claude hesitate?
   - What did you need to clarify?
   - Was anything missing?
   - Was anything unused?

**Success criteria:**
- Claude produces quality output without ad-hoc guidance
- The skill handles expected variations naturally
- Token usage is reasonable (<2000 tokens loaded typically)
- Claude doesn't ask questions the skill should answer

### 9. FINALIZE → Codify into optimal structure

Polish for production:

**SKILL.md:**
- Remove TODOs and draft artifacts
- Verify all references exist and are linked
- Ensure imperative mood throughout
- Trim any remaining cruft

**References:**
- Organize by use case (not by type)
- Add grep-able patterns for large files
- Include only what Claude might need

**Scripts:**
- Test thoroughly
- Include docstrings (Claude might read them)
- Consider: should this be a reference instead?

**Assets:**
- Only include files that are used in output
- Remove examples/samples unless they're templates

**Validation:**
```bash
# Use the packaging script - it validates automatically
scripts/package_skill.py /path/to/skill-folder
```

### 10. PACKAGE → Share the skill

Once validated:

```bash
# Creates skill-name.skill file
scripts/package_skill.py /path/to/skill-folder /output/directory
```

The .skill file is a zip with a .skill extension containing your complete skill structure.

## Common Skill Patterns

### High-Level Guide with Deep References

**When:** Complex domain with many variations

**SKILL.md:**
```markdown
## Core workflow

[Essential steps + decision points]

For detailed guidance:
- **Pattern library:** See references/patterns.md
- **Full examples:** See references/examples.md  
- **API reference:** See references/api.md
```

**Benefit:** SKILL.md stays focused; Claude loads depth only when needed

### Script-Heavy with Minimal Instructions

**When:** Fragile operations requiring exact execution

**SKILL.md:**
```markdown
## Rotating PDFs

Use scripts/rotate_pdf.py:

\`\`\`bash
python scripts/rotate_pdf.py input.pdf --angle 90 --output rotated.pdf
\`\`\`

The script handles edge cases and validation.
```

**Benefit:** Deterministic, token-efficient, no "reinventing the wheel"

### Template-Based with Examples

**When:** Output follows a strict format

**SKILL.md:**
```markdown
## Report format

ALWAYS use this structure:

# [Title]

## Executive Summary
[One paragraph]

## Key Findings  
- Finding 1 [with data]
- Finding 2 [with data]

## Recommendations
1. Specific action
2. Specific action
```

**Benefit:** Claude produces consistent output without guessing

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | Fix |
|--------------|--------------|-----|
| **Novel-length SKILL.md** | Wastes tokens, hard to maintain | Split into references/ |
| **Step-by-step recipes** | Makes Claude mechanical, not thoughtful | Teach principles |
| **Generic advice** | Claude already knows this | Only include novel info |
| **Assuming incompetence** | Over-explains, wastes tokens | Trust Claude's base knowledge |
| **README/CHANGELOG/etc** | AI doesn't need meta-documentation | Delete these files |
| **Loading everything upfront** | Wastes context | Use progressive disclosure |
| **Vague triggering** | Skill loaded when not needed | Be specific in description |

## Degrees of Freedom Framework

Match instruction specificity to task fragility:

**High Freedom (General Guidance)**
- Use when: Multiple valid approaches exist
- Format: Principles + examples
- Example: "Write engaging product copy"

**Medium Freedom (Preferred Patterns)**
- Use when: Best practices exist but context varies
- Format: Decision framework + examples
- Example: "Structure SQL queries for readability"

**Low Freedom (Exact Execution)**
- Use when: Operations are fragile or compliance-critical
- Format: Scripts or strict templates
- Example: "Fill IRS tax forms"

## Working with Existing Skills

**To improve a skill:**

1. Use it on real tasks - note where it fails
2. Check: Is this a skill problem or wrong use case?
3. Run through EXPLORE phase again
4. Apply targeted fixes (resist full rewrites)
5. Test that fixes don't break existing use cases

**To merge skills:**

Only if they share 80%+ overlap. Otherwise keep separate - Claude can use multiple skills.

**To split a skill:**

When SKILL.md exceeds 500 lines or covers truly distinct workflows. Split at natural boundaries, update descriptions.

## Quick Reference: Skill Creation Checklist

- [ ] Problem clearly defined with concrete examples
- [ ] Observed Claude's actual failure modes (not assumed)
- [ ] Researched domain to extract expert mental models
- [ ] Synthesized principles, not just collected facts
- [ ] SKILL.md under 500 lines
- [ ] Description is specific about when to trigger
- [ ] Imperative mood throughout
- [ ] Progressive disclosure: SKILL.md → references → scripts
- [ ] Every section justified by observed need
- [ ] Tested on realistic scenarios
- [ ] No README, CHANGELOG, or meta-docs
- [ ] Packaged and validated

## References

For detailed patterns:
- **Workflow patterns:** See the standard skill-creator's references/workflows.md
- **Output patterns:** See the standard skill-creator's references/output-patterns.md

## Tools

Use the standard skill-creator scripts:
- `scripts/init_skill.py` - Initialize skill structure
- `scripts/package_skill.py` - Validate and package
- `scripts/quick_validate.py` - Check structure only

## Final Wisdom

**The best skill is the one that disappears.** When Claude uses it, it should feel like Claude "just knows" how to do the task - not like it's following a manual.

If your skill makes Claude sound like it's reading instructions, you've created friction. If Claude sounds like a domain expert who happens to have expertise in this area, you've transferred expertise.

That's the difference.