---
name: writers-room
wtfbId: wtfb:writers-room
description: |
  This skill convenes a 6-agent collaborative pre-production session.
  Story Architect, Dialogue Writer, Scene Writer, Research Specialist,
  Standards Reviewer, and Continuity Editor pitch their creative visions
  before writing begins.

  Use when: starting a new screenplay, planning major rewrites,
  reimagining existing material, or seeking diverse expert perspectives.
---

# Writer's Room Skill

## Purpose

A collaborative pre-production workflow where multiple specialized agents pitch their creative visions before any writing begins. This creates diverse perspectives, healthy creative tension, and a synthesized approach that draws from the best ideas.

## When to Use

- Before starting a new screenplay or major rewrite
- When reimagining existing material
- When the creative direction is uncertain
- When you want multiple expert perspectives before committing

## Participants

The Writer's Room convenes 6 specialized agents, each with a distinct role:

### Story Architect
**Focus:** Structure and form
- Alternative three-act structures
- Non-linear possibilities
- Scene sequence options
- Climax variations
- Pacing strategies

### Story Analyst
**Focus:** Character and meaning
- Character arc potential
- Thematic depth opportunities
- Aristotle's Six Components evaluation
- What the story is *really* about
- Theophrastus archetype analysis

### Dialogue Writer
**Focus:** Voice and tone
- Character voice distinctions
- Comedic/dramatic rhythm
- Language approach (profanity, dialect, period)
- Signature lines and moments
- Subtext opportunities

### Scene Writer
**Focus:** Visual storytelling
- Key visual setpieces
- Physical comedy/action beats
- Power dynamics per scene
- Compression opportunities
- "Show don't tell" moments

### Standards Reviewer
**Focus:** Quality and originality
- What makes each proposed element A-grade?
- Weak points to avoid
- Cliche identification
- Fresh vs. derivative analysis
- Genre boundary awareness

### Research Specialist
**Focus:** Authenticity and grounding
- Setting accuracy requirements
- Technical/professional accuracy
- Historical or cultural considerations
- Real-world logic checks
- Reference material needs

## Process

### Step 1: Brief the Room
Provide all participants with:
- The core premise/logline
- Any existing material (V1 script, source material, notes)
- Target tone and audience
- Constraints (runtime, budget considerations, rating)
- What's "sacred" vs. open for reimagining

### Step 2: Individual Pitches
Each agent prepares their perspective:
- What excites them about the material
- Their proposed approach
- Specific recommendations
- Potential concerns or warnings

### Step 3: Synthesis
Combine the best elements from all pitches into:
- A unified creative direction
- Key scenes that must exist
- Tone and voice guidelines
- What's explicitly off-limits
- The "North Star" for the project

## Output Format

```markdown
# Writer's Room Creative Direction

## Project: [Title]
## Date: [Session Date]
## Participants: Story Architect, Story Analyst, Dialogue Writer, Scene Writer, Standards Reviewer, Research Specialist

---

## The Pitch (From Story Architect)
[Structure and form recommendations]

## The Heart (From Story Analyst)
[Character and thematic core]

## The Voice (From Dialogue Writer)
[Tone and language approach]

## The Spectacle (From Scene Writer)
[Visual setpieces and key moments]

## The Standard (From Standards Reviewer)
[Quality benchmarks and originality notes]

## The Foundation (From Research Specialist)
[Authenticity requirements]

---

## Synthesized Creative Direction

### Core Approach
[Unified vision statement]

### Must-Have Scenes
1. [Scene description]
2. [Scene description]
3. [Scene description]

### Tone Guidelines
- [Guideline]
- [Guideline]

### Off-Limits
- [What to avoid]

### North Star
[Single guiding principle for all creative decisions]
```

## Benefits

1. **Diverse Perspectives:** No single creative blind spot
2. **Quality Bar:** Standards Reviewer prevents lazy choices
3. **Grounded Creativity:** Research Specialist prevents plausibility errors
4. **Unified Vision:** Synthesis creates alignment before writing begins
5. **Reusable Asset:** Creative Direction document guides entire production

## Integration

The Writer's Room output feeds directly into:
- `/theme-discovery` - Validates thematic direction
- `/character-interview` - Guides character development priorities
- `/story-check` - Establishes success criteria
- `/scene-writer` agent - Provides visual direction
- `/dialogue-writer` agent - Sets voice parameters

## Example Invocation

```
/writers-room

Project: Racoon Rescue V2
Premise: A drunk Navy petty officer uses an unconscious raccoon to bypass his breathalyzer interlock.
Existing: V1 screenplay (15 min short, dark comedy)
Target: Smart R (Fargo-level), complete reimagining
Sacred: Core premise only - everything else open
Constraints: Keep at ~15 min, sophisticated adult humor
```
