---
name: philosophy-repo
description: "Stoffy's philosophical knowledge repository - thinkers, thoughts, sources, and debates. Auto-activates for philosophical discussion, capturing reflections, exploring ideas, or referencing philosophers. Triggers: 'consciousness', 'free will', 'existence', 'meaning', 'knowledge', 'morality', 'I've been thinking', 'what if', 'philosophically', philosopher names (Friston, Nietzsche, Heidegger, Sartre, etc.), 'capture this thought', 'add to my reflections', 'what do I think about', 'explore the idea', 'philosophical sources'."
---

# Philosophy Repository Skill

Stoffy's personal philosophical knowledge system - a living repository of thinkers, thoughts, sources, and structured explorations across fundamental questions of consciousness, existence, free will, knowledge, and meaning.

## When This Skill Activates

### Automatic Triggers

**Topic Keywords**:
- Consciousness, mind, awareness, qualia, subjective experience, hard problem
- Free will, determinism, agency, choice, responsibility
- Existence, being, reality, metaphysics, ontology, nothingness
- Knowledge, epistemology, truth, belief, certainty, skepticism
- Meaning, purpose, fulfillment, value, the good life
- Morality, ethics, virtue, duty, obligation, right and wrong

**Philosopher Names** (52 thinkers in repository):
- Contemporary: Karl Friston, Anil Seth, Daniel Dennett, Thomas Metzinger, Andy Clark, Nick Chater, David Krakauer, Joscha Bach, Evan Thompson, Mark Solms
- Modern: Friedrich Nietzsche, Martin Heidegger, Jean-Paul Sartre, Simone de Beauvoir, Albert Camus, Hannah Arendt, Ludwig Wittgenstein, Michel Foucault
- Classical: Immanuel Kant, Georg Hegel, Baruch Spinoza, David Hume, John Locke, Rene Descartes
- Ancient: Plato, Aristotle, Socrates, Confucius, Laozi, Siddhartha Gautama (Buddha), Nagarjuna
- Medieval: Thomas Aquinas, Augustine, Maimonides

**Conversational Patterns**:
- "I've been thinking about..."
- "What if..."
- "Philosophically speaking..."
- "What does [philosopher] say about..."
- "Capture this thought..."
- "Add this to my reflections..."
- "What do I think about..."
- "Explore the idea of..."
- "Let me work through this..."
- "This connects to..."

## Repository Structure

```
knowledge/philosophy/
├── thinkers/           # 52 philosopher profiles
│   └── <name>/
│       ├── profile.md      # Core ideas, key concepts, tradition
│       ├── notes.md        # Ongoing engagement notes
│       ├── reflections.md  # Personal reflections on their ideas
│       └── references.md   # Cross-references to thoughts
│
├── thoughts/           # Philosophical explorations by theme
│   ├── consciousness/      # Mind, awareness, experience
│   ├── free_will/          # Agency, determinism, choice
│   ├── existence/          # Being, reality, metaphysics
│   ├── knowledge/          # Epistemology, truth, belief
│   ├── computational_philosophy/
│   └── CLAUDE.md           # Theme documentation
│
├── sources/            # Reference materials
│   ├── books/              # Book notes and summaries
│   ├── articles/           # Academic article notes
│   └── lectures/           # Lecture and presentation notes
│
└── debates/            # Structured philosophical debates
    └── YYYY-MM-DD_topic_agent1_vs_agent2.md
```

## Available Operations

### 1. READ: Access Philosophical Content

**Read a thinker profile**:
```
Read: knowledge/philosophy/thinkers/karl_friston/profile.md
Read: knowledge/philosophy/thinkers/friedrich_nietzsche/notes.md
Read: knowledge/philosophy/thinkers/immanuel_kant/reflections.md
```

**Read a thought exploration**:
```
Read: knowledge/philosophy/thoughts/consciousness/2025-12-26_fep_hard_problem/thought.md
Read: knowledge/philosophy/thoughts/free_will/2025-12-26_kompatibilismus_2_0/thought.md
Read: knowledge/philosophy/thoughts/existence/2025-12-26_wu_wei_free_energy.md
```

**Read a source summary**:
```
Read: knowledge/philosophy/sources/books/active_inference.md
Read: knowledge/philosophy/sources/books/being_and_time.md
```

**Read a debate transcript**:
```
Read: knowledge/philosophy/debates/2025-12-30_predictive_brain_karl_friston_vs_laozi.md
```

### 2. EXPLORE: Discover Content

**List all thinkers**:
```bash
ls knowledge/philosophy/thinkers/
```

**Find thoughts by theme**:
```bash
ls knowledge/philosophy/thoughts/consciousness/
ls knowledge/philosophy/thoughts/free_will/
ls knowledge/philosophy/thoughts/existence/
ls knowledge/philosophy/thoughts/knowledge/
```

**Search for specific topics**:
```bash
grep -r "Free Energy Principle" knowledge/philosophy/
grep -r "hard problem" knowledge/philosophy/thoughts/
```

### 3. WRITE: Capture New Content

**Create a new thought**:
1. Determine theme: consciousness, free_will, existence, knowledge, morality, life_meaning
2. Create folder: `knowledge/philosophy/thoughts/<theme>/YYYY-MM-DD_<slug>/`
3. Create `thought.md` with frontmatter and content
4. Update cross-references if connected to thinkers or other thoughts

**Thought template**:
```markdown
---
title: "<Thought Title>"
date: YYYY-MM-DD
status: seed | exploring | developing | crystallized | integrated
theme: <theme>
related_thinkers:
  - <thinker_folder_name>
related_thoughts:
  - <path_to_related_thought>
tags: []
---

# <Title>

## The Question

What question or insight sparked this exploration?

## Current Position

My current thinking on this matter...

## Arguments

### Supporting
- Argument 1
- Argument 2

### Challenges
- Objection 1
- Objection 2

## Connections

Links to related thinkers, thoughts, and sources.
```

**Add notes to a thinker**:
```
Edit: knowledge/philosophy/thinkers/<name>/notes.md
```

**Add personal reflections**:
```
Edit: knowledge/philosophy/thinkers/<name>/reflections.md
```

**Update references after thought creation**:
```
Edit: knowledge/philosophy/thinkers/<name>/references.md
```

### 4. CONNECT: Build Knowledge Graph

**Cross-reference thought to thinker**:
When creating a thought that engages with a thinker's ideas:
1. Add thinker to thought's `related_thinkers` frontmatter
2. Add thought to thinker's `references.md` file

**Cross-reference thoughts**:
When thoughts connect:
1. Add to `related_thoughts` in both thought frontmatter
2. Document the connection in each thought's Connections section

### 5. DEBATE: Orchestrate Philosophical Dialogues

Use the `/debate` command to stage structured debates:
```
/debate <agent1> <agent2> <rounds> <topic>
```

Debates are saved to `knowledge/philosophy/debates/` with full transcripts.

## Thought Lifecycle

```
SEED -> EXPLORING -> DEVELOPING -> CRYSTALLIZED -> INTEGRATED
                          |               |
                          v               v
                    CHALLENGED       ARCHIVED
```

| Stage | Description | Exit Criteria |
|-------|-------------|---------------|
| **Seed** | Initial spark or question | Thought is clearly articulated |
| **Exploring** | Actively thinking through | Core insight emerges |
| **Developing** | Building coherent position | Position articulated with arguments |
| **Crystallized** | Clear position formed | Can defend against objections |
| **Challenged** | Under reconsideration | Resolved or evolved |
| **Integrated** | Woven into worldview | Connected to other positions |
| **Archived** | No longer active | Documented for reference |

## Memory Files (Higher Weight)

Every file can have a companion `_memory.md` file that contains human corrections and key insights. Memory files have **HIGHER WEIGHT** than source files.

```
profile.md          -> profile_memory.md
notes.md            -> notes_memory.md
thought.md          -> thought_memory.md
```

When processing any file, **ALWAYS check for corresponding `_memory.md`** and apply its content first.

## Key Themes in Repository

### Consciousness
- Free Energy Principle and the hard problem
- Computational phenomenology
- Predictive processing and controlled hallucination
- Strange loops and self-reference
- Interoceptive embodied self

### Free Will
- Compatibilism 2.0 (inferential autonomy)
- The four humiliations of humankind
- Active inference and agency
- Friston's framework on choice

### Existence
- Existentielle Potentialitat (relational ontology)
- Wu Wei as free energy minimization
- Emergence and nothingness
- Sinnfeld und Potentialitat

### Knowledge
- Self-reference, computation, and truth
- Kantian roots of predictive processing
- Interface theory of reality
- Complexity and constructivism

## Featured Thinkers (with extensive profiles)

| Thinker | Domain | Key Contribution |
|---------|--------|------------------|
| **Karl Friston** | Neuroscience/Philosophy | Free Energy Principle, Active Inference |
| **Thomas Metzinger** | Philosophy of Mind | Phenomenal Self Model, Ego Tunnel |
| **Anil Seth** | Cognitive Science | Controlled Hallucination, Being You |
| **Daniel Dennett** | Philosophy | Heterophenomenology, Illusionism |
| **Andy Clark** | Philosophy | Extended Mind, Predictive Processing |
| **Nick Chater** | Cognitive Science | The Mind is Flat |
| **Douglas Hofstadter** | Cognitive Science | Strange Loops, GEB |
| **Martin Heidegger** | Phenomenology | Being and Time, Dasein |
| **Friedrich Nietzsche** | Existentialism | Will to Power, Eternal Return |
| **Baruch Spinoza** | Rationalism | Conatus, Substance Monism |

## Integration with Other Skills

**For academic research on philosophical topics**:
```
Skill(academic-research): "consciousness predictive processing"
```

**For philosophical method application**:
```
Skill(philosophy-of-mind): Apply consciousness analysis protocol
Skill(epistemology): Evaluate knowledge claims
Skill(ethics): Analyze moral dimensions
Skill(phenomenological-method): Apply phenomenological reduction
```

**For thought experiments**:
```
Skill(thought-experiments): Design or analyze thought experiments
```

## Example Usage Patterns

### Capture a spontaneous insight
User: "I've been thinking about how attention might not just reveal consciousness but actually constitute it..."

Response:
1. Engage with the idea philosophically
2. Connect to relevant thinkers (Friston on precision weighting, Seth on attention)
3. Offer to create a new thought entry if substantial
4. Reference existing related thoughts

### Research a philosophical question
User: "What does Friston say about free will?"

Response:
1. Read `knowledge/philosophy/thinkers/karl_friston/profile.md`
2. Search for free will content in thoughts
3. Synthesize and present with connections
4. Reference specific passages and sources

### Add to ongoing engagement
User: "Add this to my notes on Heidegger - his concept of thrownness connects to Friston's Markov blankets..."

Response:
1. Read current notes: `knowledge/philosophy/thinkers/martin_heidegger/notes.md`
2. Append new insight with date
3. Consider creating cross-reference in Friston's notes
4. Suggest related thought explorations

### Explore a theme
User: "Show me what I've explored about consciousness"

Response:
1. List all thoughts in `knowledge/philosophy/thoughts/consciousness/`
2. Summarize each thought's status and core insight
3. Identify connections between thoughts
4. Suggest unexplored areas or next explorations

## Invocation Guidance

This skill should be invoked when:
- Discussing any philosophical topic or question
- Referencing or asking about specific philosophers
- Wanting to capture, develop, or review personal philosophical thinking
- Exploring connections between ideas
- Researching philosophical sources
- Orchestrating philosophical debates
- Tracking the evolution of philosophical positions

## Python Utilities

The repository includes Python scripts in `scripts/philosophy/` for programmatic operations.

### PhilosophyRepo Class (Main Interface)

```python
from scripts.philosophy import PhilosophyRepo

repo = PhilosophyRepo()

# Read content
thought = repo.read_thought("consciousness/2025-12-26_fep_hard_problem")
thinker = repo.read_thinker("karl_friston")

# Write content
path = repo.write_thought(
    title="On Presence",
    theme="consciousness",
    content="Being fully here, in this moment..."
)

# Search
results = repo.search("free energy principle")

# Link thought to thinker
repo.link("consciousness/on-presence", "karl_friston", "strong", "Core FEP themes")
```

### Writer Module (`scripts/philosophy/writer.py`)

```python
from scripts.philosophy.writer import write_thought, write_thinker, write_source

# Create thought with full options
path = write_thought(
    title="Consciousness and Time",
    theme="consciousness",  # consciousness, free_will, existence, knowledge, morality, life_meaning
    initial_spark="What if time perception IS consciousness?",
    status="seed",  # seed, exploring, developing, crystallized, integrated
    related_thinkers=["karl_friston", "anil_seth"],
    use_folder=True,  # Creates folder structure vs single file
    auto_commit=True  # Auto-commits to git
)

# Create thinker profile
path = write_thinker(
    name="New Philosopher",
    thinker_type="philosopher",
    era="contemporary",
    traditions=["phenomenology", "cognitive science"],
    key_works=["Major Work"],
    core_ideas=["Core idea 1", "Core idea 2"]
)

# Create source entry
path = write_source(
    title="Being and Time",
    author="Martin Heidegger",
    source_type="book",  # book, article, lecture, essay, podcast
    year=1927,
    themes=["existence", "consciousness"]
)
```

### Linker Module (`scripts/philosophy/linker.py`)

```python
from scripts.philosophy.linker import (
    create_bidirectional_link,
    get_thinker_thoughts,
    get_thought_thinkers,
    validate_links,
    list_thinkers,
    list_thoughts
)

# Create bidirectional link
create_bidirectional_link(
    thought_path="consciousness/2025-12-26_fep_hard_problem",
    thinker_name="karl_friston",
    strength="strong",  # strong, moderate, weak
    reasoning="Core FEP themes directly addressed"
)

# Query links
thoughts = get_thinker_thoughts("karl_friston")
thinkers = get_thought_thinkers("consciousness/2025-12-26_fep_hard_problem")

# Validate all links (find orphaned references)
issues = validate_links()
```

### CLI Usage

```bash
# Link a thought to a thinker
python scripts/philosophy/linker.py link "consciousness/fep_hard_problem" "karl_friston" "strong" "Core FEP themes"

# List all thinkers
python scripts/philosophy/linker.py list-thinkers

# List all thoughts
python scripts/philosophy/linker.py list-thoughts

# Validate all bidirectional links
python scripts/philosophy/linker.py validate
```

### Additional Modules

| Module | Purpose |
|--------|---------|
| `repo.py` | GitHub API layer using `gh` CLI for remote operations |
| `templates.py` | Template rendering for new content |
| `content.py` | Content parsing and extraction |
| `indices.py` | Index management and search |
| `validator.py` | Content validation |
| `integration.py` | Full integration utilities |

## Quick Reference

| Action | Command/Path |
|--------|--------------|
| Read thinker | `knowledge/philosophy/thinkers/<name>/profile.md` |
| Read thought | `knowledge/philosophy/thoughts/<theme>/<date>_<slug>/thought.md` |
| List thinkers | `ls knowledge/philosophy/thinkers/` |
| List thoughts | `ls knowledge/philosophy/thoughts/<theme>/` |
| Search content | `grep -r "<term>" knowledge/philosophy/` |
| Create thought | New folder + thought.md in appropriate theme |
| Update notes | Edit `knowledge/philosophy/thinkers/<name>/notes.md` |
| Add reflection | Edit `knowledge/philosophy/thinkers/<name>/reflections.md` |
| Stage debate | `/debate <agent1> <agent2> <rounds> <topic>` |
| Python: Create thought | `write_thought(title, theme, initial_spark)` |
| Python: Link content | `create_bidirectional_link(thought, thinker, strength, reason)` |
| Python: Validate links | `python scripts/philosophy/linker.py validate` |
