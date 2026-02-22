---
name: lecture-alchemist
description: "Transform raw lecture transcripts (Zoom, YouTube, etc.) into structured, retention-optimized study notes. Use when the user provides a lecture transcript, class recording text, or asks to process/convert lecture notes. Handles WebDev, AI/ML, Web3, DSA, and general tech domains. Produces hierarchical topic breakdowns, cleaned code artifacts, intuition builders, flashcards, spaced repetition plans, and actionable study materials. Trigger phrases: 'process this transcript', 'convert lecture to notes', 'lecture notes', 'transcript to study material', 'Lecture Alchemist'."
---

# Lecture Alchemist - Technical Learning Transformer

Transform messy lecture transcripts into comprehensive, retention-optimized study materials.

## Three Roles

1. **Meticulous Transcriber** - Extract and organize every topic without loss
2. **Expert Tutor** - Enhance weak explanations with better intuition
3. **Study Architect** - Create revision-ready materials and action items

## Critical Rules

### Zero Topic Loss
Every technical concept, term, tool, command, code snippet, or teaching point in the transcript MUST appear in the output. Reorganize and enhance, but never skip or merge distinct concepts. Before finalizing, scan the transcript for any technical term not covered.

### Enhance, Don't Replace
When the instructor's explanation was weak:
- First present what they said
- Then provide enhanced explanation marked as `[ENHANCED]`
- Never pretend the enhanced version was in the lecture

### Domain Awareness

| Domain | Key Focus |
|--------|-----------|
| WebDev | Code patterns, framework idioms, deployment, debugging |
| AI/ML | Mathematical intuition, hyperparameters, model selection |
| Web3 | Security, gas optimization, common vulnerabilities |
| DSA | Complexity analysis, patterns, edge cases, interview relevance |

### Code Fidelity
- Extract ALL code from transcript
- Clean up transcription errors, preserve original structure
- Add explanatory comments, flag incomplete code

### Clean Markdown Only
- NO unicode box-drawing characters
- Use `---` for separators, not unicode lines
- Math in inline code (`y = wx + b`), not LaTeX
- All tables must have closing pipes
- Code blocks must specify language

## Transcript Handling

| Challenge | Action |
|-----------|--------|
| Filler words | Remove |
| Tangents | Separate into "Aside" if valuable, omit if not |
| Q&A mixed in | Extract to dedicated Q&A section |
| Incomplete sentences | Interpret intelligently, flag uncertainty |
| Code dictation | Reconstruct carefully, verify syntax |
| Screen sharing refs | Note as "[Visual reference in class]" |

## Output Structure

Follow the template in `references/output-template.md` exactly. The output contains these sections in order:

1. **Header** - Course, session, date, instructor, domain
2. **Session Overview** - One-liner, key takeaways, difficulty, balance, prerequisites
3. **Topic Hierarchy** - Complete taxonomy as indented markdown lists
4. **Detailed Concept Breakdown** - Each topic with: what was taught, core concept, intuition builder, code example, real-world application
5. **Code Artifacts** - All code cleaned, commented, with purpose and context
6. **Intuition Deep Dives** - For difficult concepts: how taught, the gap, better mental model `[ENHANCED]`
7. **Technical Analysis** - Domain-specific tables (math foundations, hyperparameters, complexity, when-to-use)
8. **Connections Map** - Prerequisites, leads-to, related concepts
9. **Knowledge Gaps** - What was assumed, why it matters, quick fill, resource
10. **Q&A from Session** - Questions and answers with extra context
11. **Action Items** - Homework, practice exercises, code to implement, topics to research
12. **Flashcards** - Key terms, concepts, syntax/commands tables
13. **Spaced Repetition Plan** - Tomorrow, 1 week, hands-on practice
14. **Summaries** - Tweet (<280 chars), paragraph (3-5 sentences), detailed (comprehensive)
15. **Processing Stats** - Word counts, topics extracted, code blocks, gaps, completeness

## Initialization

When a transcript is provided, respond:

```
Got it! Processing your **[Domain]** lecture transcript.

I'll extract:
- Complete topic hierarchy
- All code snippets (cleaned & commented)
- Intuition builders for tricky concepts
- Domain-specific technical analysis
- Actionable study materials

---
```

Then immediately proceed to full output.

## Topic Inventory Verification (Anti-Loss System)

If a Topic Inventory was provided from Stage 1 (transcribe-refiner), perform mandatory cross-verification:

1. **Check every concept** from the inventory against the Topic Hierarchy -- each must appear
2. **Check every technical term** -- each must be defined or explained somewhere
3. **Check every code/command** -- each must appear in Code Artifacts
4. **Check every Q&A item** -- each must appear in the Q&A section
5. **Report coverage** in Processing Stats:

```markdown
## Inventory Verification
- Concepts from inventory: [N] / [N] covered (100%)
- Technical terms: [N] / [N] covered
- Code references: [N] / [N] covered
- Q&A items: [N] / [N] covered
- **MISSING:** [list any items not covered, or "None"]
```

If ANY item is missing, add it before finalizing.

## Enhanced Sections (Best-in-Class Features)

### Difficulty Scoring Per Concept
Rate each concept in the detailed breakdown:
- **Difficulty:** [1-5 stars] | **Importance:** [Core / Supporting / Nice-to-know]

### Interview/Exam Angle
For each major concept, include:
> **If asked in an interview:** [How to explain this in 30 seconds]

### Common Misconceptions
For tricky concepts:
> **People often think:** [misconception]
> **Actually:** [correction]

### Cross-Lecture Links
When a concept connects to other sessions:
> **Previously covered:** [Topic] in [Session X]
> **Coming up next:** [Topic] in future sessions

### Learning Dependency Graph
At the end, include a text-based dependency list:
```
Concept A (prerequisite for B, C)
├── Concept B (prerequisite for D)
│   └── Concept D
└── Concept C
```

## Special Cases

- **Long transcripts (2+ hours):** Break into logical segments with intermediate summaries
- **Heavy Q&A sessions:** Separate Q&A section, note common confusions
- **Live coding sessions:** Document code evolution step-by-step, note debugging
- **Multiple instructors:** Attribute teachings when distinguishable
- **With Topic Inventory:** Always verify 100% coverage before output

## Quality Checklist

Before output, verify:
- Every topic from transcript is in the hierarchy
- Topic Inventory (if provided) shows 100% coverage
- All code extracted and cleaned with language specified
- All tables properly formatted with closing pipes
- No unicode box-drawing characters or LaTeX
- Difficult concepts have intuition builders
- Each concept has difficulty score and interview angle
- Technical analysis matches the domain
- Action items are concrete and actionable
- All three summary levels exist
- Cross-lecture links added where applicable

## Tutorial Bar-Raiser Handoff (Mandatory)

When this skill output is consumed by downstream packaging, enforce:

1. Learner-facing tutorial format:
   - emoji-led section headings
   - Mermaid diagrams
   - HOTS + FAQ + practice roadmap
   - intuition-first explanations before formalism
2. Naming convention in final published note:
   - `<Domain> Class <NN> [DD/MM/YYYY] - <Topic>`
3. Learner-facing sanitization:
   - remove inline `[source: ...]` tags from final tutorial note
   - keep traceability in sidecar artifacts (coverage matrix + segment ledger)
4. Publish an explicit learner filename:
   - `<DomainFile> Class <NN> [DD-MM-YYYY] - <Topic>.md`

## Pipeline Position

This skill is **Stage 2** in the lecture processing pipeline:
1. **transcribe-refiner** → clean transcript + Topic Inventory
2. **lecture-alchemist** (this) → structured study notes (verifies against inventory)
3. **concept-cartographer** → visual diagrams
4. **obsidian-markdown** → Obsidian vault formatting

## Reference Files

- `references/output-template.md` - Full output structure template
- `references/example-output.md` - Complete example (Neural Networks lecture)
