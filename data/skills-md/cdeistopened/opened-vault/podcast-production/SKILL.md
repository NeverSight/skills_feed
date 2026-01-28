---
name: podcast-production
description: Complete workflow for producing podcast episodes from raw transcript to publishable YouTube and social media assets. Four-checkpoint system for strategic decision-making plus final polished assets.
---

# Podcast Production Skill

## Overview

Transform a raw podcast transcript into polished, multi-platform content assets through four strategic checkpoints. Each checkpoint delivers decision-ready analysis in a markdown file for your feedback before proceeding. You'll provide feedback directly in the checkpoint documents, then we'll iterate before moving to the next phase. Final outputs include publication-ready YouTube strategy and a narrative-driven blog post.

**Workflow Structure:**
- Start with `[Guest]_Source_Material.md` (raw transcript + notes)
- Create `Checkpoint_1_Comprehensive_Analysis.md` (your feedback here)
- Create `Checkpoint_2_Cold_Opens_and_Clips.md` (your feedback here)
- Create `Checkpoint_3_YouTube_Strategy.md` (your feedback here)
- Create `Checkpoint_4_Polished_Transcript_and_Blog.md` (final deliverable)

---

## Execution Model: Subagents for Context Preservation

**CRITICAL**: Each checkpoint should be executed by a dedicated subagent (using the Task tool) to preserve context window in the main conversation. The workflow is:

1. **Main agent** reads source material, confirms approach with user
2. **Subagent 1** executes Checkpoint 1, writes file, reports back summary
3. **User reviews**, provides feedback on Big Idea selection
4. **Subagent 2** executes Checkpoint 2 (reads Checkpoint 1 + source), writes file, reports back
5. **User reviews**, approves cold open and clips
6. **Subagent 3** executes Checkpoint 3 (reads prior checkpoints), writes file, reports back
7. **User reviews**, approves YouTube strategy
8. **Subagent 4** executes Checkpoint 4 (reads all prior work), writes final deliverables

**Subagent prompt template:**
```
You are executing [Checkpoint N] of the podcast production workflow.

Episode: [Guest Name]
Working directory: [path to episode folder]

Read the following files:
- SOURCE.MD (raw transcript)
- [Any prior checkpoint files]

Create: Checkpoint_[N]_[Name].md following the podcast-production skill format.

[Specific checkpoint instructions from skill]

Write the checkpoint file and report back with:
1. Key decisions/recommendations
2. Questions for user feedback
```

This preserves context by having each subagent start fresh with only the necessary files, rather than accumulating the entire conversation history.

## When to Use This Skill

- You have a raw podcast transcript and need to identify the strongest marketing angle
- You want to create a cold open that hooks listeners immediately
- You need YouTube titles and thumbnail strategies
- You're creating social clips from podcast material
- You want to create SEO-optimized blog content from the episode
- You want all assets aligned with OpenEd brand identity

---

## Session Startup

At the start of each podcast production session, sync the content database:

```bash
cd "Content/Misc. Utilities/seomachine" && python3 -c "
from dotenv import load_dotenv
load_dotenv('data_sources/config/.env')
from data_sources.modules.webflow import sync_content_database
sync_content_database()
"
```

This pulls latest content from Webflow to `Content/Master Content Database/` for internal linking and context.

---

## THE FOUR CHECKPOINTS

### Checkpoint 1: Comprehensive Analysis (90-120 min)

**Goal**: Understand the episode, identify strongest themes, and inventory building blocks for all downstream content (social clips, long-form clips, blog posts, newsletters).

**Your deliverable**: `Checkpoint_1_Comprehensive_Analysis.md`

**Document Structure** (in this order):
1. **Episode Metadata** (guest, host, duration, credentials)
2. **The TED Talk Version** (2-3 orthogonal angles that capture what the episode delivers - emphasize salience over clickability)
3. **5 Big Ideas** (potential marketing angles for different assets)
4. **Chapter Outline** (timestamped)
5. **Snippet Inventory** (25-30 short quotable moments, 5-30 sec each, labeled S1-S29)
6. **Guest Voice Inventory** (sticky phrases, syntax patterns, named concepts)
7. **Quote Bank** (organized by theme)
8. **Surprising Points** (contradictions with common belief)
9. **Top Recommendation** (with reasoning)

**Snippet Inventory Format** - Each snippet MUST include:
- Label (S1, S2, etc.)
- Category (Counterintuitive, Memorable Quotes, Relatable/Funny, Practical/Actionable, Emotional, Origin Story)
- Timestamp range
- **Speaker attribution** (JOSHUA, ISAAC, ELA, etc.)
- Verbatim quote

Example:
```
**[S1] "No Shoulds, Only Coulds" (18:21-18:52) - JOSHUA**
> "There are no shoulds, there are only coulds..."
```

**The TED Talk Version** - Provide 2-3 somewhat orthogonal angles:
- What is this episode *actually* about? (salience)
- What's the surprising/counterintuitive framing? (interest)
- What's the practical takeaway? (utility)

**User decision point**: Which Big Idea/angle to pursue for primary assets?

**IMPORTANT**: Balance clickability with salience. Lean toward what the episode actually delivers rather than what might get the most clicks but misrepresent the content.

**Reference**: See `references/checkpoint-1-example.md` for detailed example

---

### Checkpoint 2: Cold Opens & Clips (120-150 min)

**Prerequisites**: Checkpoint 1 complete + Big Idea selected

**Goal**: Create one approved cold open script and identify 3-5 approved social clips with on-screen hooks.

**Your deliverable**: `Checkpoint_2_Cold_Opens_and_Clips.md`

**Process** (two-step):
1. **First: Arrange snippets into cold open options** — Using the Snippet Inventory from Checkpoint 1, combine snippets (by label: S1, S2, etc.) into 3-5 cold open arrangements. Use [SWOOSH] to indicate transitions between unrelated moments.
2. **Then: Expand selected snippets into full clips** — Build out the best snippets into complete 45-90 second clips with full verbatim transcripts and edit markup.

**What it contains**:
- 3-5 cold open options (montages of snippets with [SWOOSH] transitions)
- One selected cold open script (22-35 seconds)
- On-screen text hooks (2-4 words each for social media captions)
- 3-5 approved social clips (45-90 sec each, full verbatim transcripts with edit markup)
- Each clip includes: timestamp range, on-screen hook, full transcript with ~~strikethrough~~ for cuts and *italics* for minor edits

**Output format**:
- Cold open: Montage structure using [SWOOSH] between unrelated moments, not linear narrative extracts
- Clips: Verbatim with edit markup (~~cuts~~, *changes*), timestamps throughout
- Hooks: 2-4 words maximum for mobile readability
- All clips ready for editor handoff

**Skills used**:
- **video-caption-creation**: For on-screen text hooks and short-form video captions (generates 3-5 hook options per clip)
- **cold-open-creator**: For cold open methodology (optional reference)

**Clip Types** (create a mix):

| Type | Duration | Structure | Best For |
|------|----------|-----------|----------|
| **Single Topic** | 45-90 sec | One complete idea with setup → tension → payoff | Actionable tips, counterintuitive insights, emotional moments |
| **Supercut / Montage** | 45-60 sec | Quick cuts with [SWOOSH] between unrelated moments | "Day in the life," personality showcase, vibe/energy clips |

**Supercut Template:**
```
**On-screen hook options:**
- "[Caption option 1]"
- "[Caption option 2]"

**Format:** Quick cuts, [SWOOSH] between each moment. ~45-60 seconds total.

---

**SPEAKER (timestamp):** [Short moment - 5-10 sec]

[SWOOSH]

**SPEAKER (timestamp):** [Short moment - 5-10 sec]

[SWOOSH]

(continue for 5-8 moments, end on emotional or memorable beat)
```

**User decision point**: Approve cold open and social clips for Checkpoint 3

**Reference**: See `references/checkpoint-2-example.md` for detailed example

---

### Checkpoint 3: YouTube Strategy (90-120 min)

**Prerequisites**: Checkpoint 2 complete + Cold open selected

**Goal**: Define YouTube title, thumbnail, description, and chapter timestamps.

**Your deliverable**: `Checkpoint_3_YouTube_Strategy.md`

**What it contains**:
- Final YouTube title (with guest name for authority)
- Thumbnail specification (2-4 words max, minimal design)
- YouTube description (opening hook sentence + full description + resources + chapters)
- Cold open script (verbatim clips)
- All 3 approved social clips with on-screen hooks
- Chapter breakdown (5-10 words per chapter title, keyword-rich)

**Skills used**:
- **youtube-title-creator**: For YouTube title strategy
- **opened-identity**: For brand alignment verification

**Output format**:
- Clean, streamlined specifications (no technical jargon)
- Chapter titles follow "My First Million" style (compelling, descriptive)
- Format: `(MM:SS) - Descriptive Chapter Title` (5-10 words max)
- Description: Opening hook + full description + resources + chapters
- Thumbnail: Simple visual + minimal text (2-4 words only)
- All clips ready to copy/paste

**User decision point**: Approve final specifications and move to Checkpoint 4

**Reference**: See `references/checkpoint-3-example.md` for detailed example

---

### Checkpoint 4: Polished Transcript & Blog Post (120-180 min)

**Prerequisites**: Checkpoint 3 complete + All selections locked

**Goal**: Create publication-ready transcript and SEO-optimized blog post.

**Your deliverables**:
- `[Guest]_YouTube_and_Show_Notes.md` (refined from Checkpoint 3)
- `[Guest]_Polished_Transcript.md` (new, contains transcript + blog)

**What it contains**:
- Full polished transcript (cleaned for readability)
- Embedded blog post (~1,000 words) focused on core insight
- Guest bio and resource links
- SEO headers and structure

**Skills used**:
- **transcript-polisher**: For transcript cleanup and formatting
- **podcast-blog-post-creator**: For narrative-driven blog post creation in Ela's voice

**Output structure**:
1. `[Guest]_YouTube_and_Show_Notes.md` — Handoff file for video production (title, thumbnail, cold open, show notes, timestamps)
2. `[Guest]_Polished_Transcript.md` — Publication-ready transcript with embedded blog post

**Reference**: See `references/checkpoint-4-example.md` for detailed example

---

## WORKFLOW TIMELINE & FILE STRUCTURE

| Phase | Duration | Input | Output File | Your Action |
|-------|----------|-------|------|---|
| **Setup** | 10 min | Raw materials | `[Guest]_Source_Material.md` | Provide feedback on context/notes |
| **Checkpoint 1** | 90-120 min | Source material | `Checkpoint_1_Comprehensive_Analysis.md` | Select Big Idea to pursue |
| **Checkpoint 2** | 120-150 min | Checkpoint 1 approved | `Checkpoint_2_Cold_Opens_and_Clips.md` | Approve cold open & clips |
| **Checkpoint 3** | 90-120 min | Checkpoint 2 approved | `Checkpoint_3_YouTube_Strategy.md` | Approve title/thumbnail/chapters |
| **Checkpoint 4** | 120-180 min | Checkpoint 3 approved | `Checkpoint_4_Polished_Transcript_and_Blog.md` | Review & publish |
| **TOTAL** | **6-8 hours** | Raw transcript | All publication-ready assets | 5 decision points |

---

## KEY PRINCIPLES

### Verbatim Only
All quoted transcript must be exactly as spoken. You can cut/rearrange, never paraphrase.

### Mine the Entire Transcript
Don't limit analysis to one section. The strongest angle might be anywhere.

### Bold Over Safe
Surprising, contrarian moments beat safe, obvious observations.

### Story Over Summary
Create narrative momentum. Clips should have complete arcs, not just be "good quotes."

### Simple Over Complex
- Thumbnails: 3 elements max
- Titles: One clear idea
- Clips: Clear beginning, middle, end

### Brand Aligned
All outputs reflect OpenEd visual and tonal guidelines. Homeschool parents should see themselves.

---

## SKILL DEPENDENCIES

| Checkpoint | Required Skills | Optional Skills |
|------------|-----------------|-----------------|
| **1** | None (pure analysis) | — |
| **2** | `cold-open-creator`, `video-caption-creation` | — |
| **3** | `youtube-title-creator`, `opened-identity` | — |
| **4** | `transcript-polisher`, `podcast-blog-post-creator` | `day-in-the-life`, `verified-review` |

**Optional skill triggers:**
- `day-in-the-life`: When guest describes daily/weekly homeschool structure. Use Guest Voice Inventory to preserve their voice.
- `verified-review`: When guest mentions specific curricula/tools. Creates 300-500 word reviews with real parent attribution.

---

## QUALITY GATES

| Transition | Key Checks |
|------------|------------|
| **1→2** | 5 distinct Big Ideas? One obvious choice? Entire transcript mined? |
| **2→3** | Cold open passes 4/5 tests (Stranger, Itch, Stakes, Tease, Emotion)? Ends on cliffhanger? 22-35 sec? All verbatim? |
| **3→4** | Title clear + includes guest? Thumbnail simple (2-4 words)? Chapter titles keyword-rich? Brand aligned? |
| **4→Publish** | Transcript clean? Blog ~1,000 words? Conversational tone? All assets ready? |

---

## COMMON MISTAKES

❌ Mining only part of transcript | ❌ Paraphrasing (all quotes verbatim) | ❌ Complex thumbnails (3 elements max) | ❌ Safe over surprising | ❌ Cold open too long (25-35s max) | ❌ Resolving cliffhanger | ❌ Skipping quality gates | ❌ Blog too formal (write like Ela)

---

## REFERENCES

For detailed instructions and examples, see:
- `references/checkpoint-1-example.md` — Complete Checkpoint 1 example
- `references/checkpoint-2-example.md` — Complete Checkpoint 2 example
- `references/checkpoint-3-example.md` — Complete Checkpoint 3 example (YouTube specifications format)
- `references/checkpoint-4-example.md` — Complete Checkpoint 4 example (Polished transcript + blog post)

---

## RELATED SKILLS

`cold-open-creator` | `video-caption-creation` | `youtube-title-creator` | `podcast-blog-post-creator` | `transcript-polisher` | `opened-identity` | `day-in-the-life` | `verified-review`

---

## SUCCESS METRICS

| Platform | Key Metrics |
|----------|-------------|
| **YouTube** | CTR >6%, retention in first 5 sec, viewers finish |
| **Blog** | SEO ranking, engagement to guest bio, shareability |
| **Social** | Clips standalone, text works without audio, platform fit |
| **Overall** | Theme alignment, brand consistency, team handoff ready |
