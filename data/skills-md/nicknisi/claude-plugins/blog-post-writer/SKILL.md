---
name: blog-post-writer
description: Transform brain dumps into polished blog posts in Nick Nisi's voice. Use when the user says "write a blog post," "draft a post," "write about [topic]," "turn my notes into a blog post," or provides scattered ideas, talking points, or conclusions that need shaping into a cohesive narrative.
---

# Nick Nisi Blog Writer

Transform unstructured brain dumps into polished blog posts that sound like Nick Nisi.

## Process

### 1. Receive the Brain Dump

Accept whatever the user provides:

- Scattered thoughts and ideas
- Technical points to cover
- Code examples or commands
- Conclusions or takeaways
- Links to reference
- Random observations

Don't require organization. The mess is the input.

**Clarify constraints** (if not provided, ask about):

- Target length (see `references/post-template.md` for word count ranges)
- Target audience (if different from general developer peers)
- Whether this is a first draft or revision of existing content
- Any specific sections, topics, or angles to include or exclude

### 2. Read Voice and Tone

Load `references/voice-tone.md` as the baseline voice guide.

**Then calibrate against recent writing:**

1. Fetch `https://nicknisi.com/posts` to find the 2-3 most recent posts
2. Fetch and read those posts
3. Note any patterns that extend or differ from the static reference — new phrases, tone shifts, topic-specific voice adjustments

The static reference captures established patterns. The live fetch catches evolution. When they conflict, prefer the recent posts — voice is a living thing. If the site cannot be fetched, rely on the static voice guide alone.

Key characteristics (read the full reference for details and examples):

- Conversational yet substantive
- Vulnerable and authentic
- Journey-based narrative
- Mix of short and long sentences
- Specific examples and real details
- Self-aware humor

### 3. Choose a Narrative Framework

Match the content to the best framework. Read the corresponding reference file before writing.

| Framework | Reference | Best when... |
|---|---|---|
| **Story Circle** | `references/story-circle.md` | There's a personal journey or transformation |
| **SCQA** | `references/scqa.md` | Solving a technical problem analytically |
| **Progressive Disclosure** | `references/progressive-disclosure.md` | Teaching a concept or introducing a tool |
| **Compare & Contrast** | `references/compare-contrast.md` | Evaluating options or trade-offs |
| **Post-mortem** | `references/post-mortem.md` | Recounting an incident, migration, or failure |
| **PAS** | `references/problem-agitation-solution.md` | Short, punchy fix or optimization story |

**How to choose:**

- Is there a personal journey? → **Story Circle**
- Is the reader making a decision? → **Compare & Contrast**
- Is the goal to teach? → **Progressive Disclosure**
- Is it a bug fix or performance win? → **PAS** (short) or **SCQA** (detailed)
- Did something go wrong? → **Post-mortem**

Not every post maps cleanly to one framework. Hybrid approaches are fine — use a framework as a starting structure, not a straitjacket.

`voice-tone.md` and `post-template.md` are always loaded. Load only one framework reference in addition — do not preload all six.

### 4. Outline the Post

Apply the chosen framework to the brain dump material:

- Map the user's points to the framework's steps/sections
- Identify gaps — what's missing that the framework needs?
- Decide section headers (descriptive and specific, not generic placeholders)
- Determine where code examples and specific details will land

If the content doesn't fit the framework cleanly, adapt — the framework is scaffolding, not a cage.

### 5. Write in Nick's Voice

Apply voice characteristics:

**Opening:**

- Hook with current position or recent event
- Set up tension or question
- Be direct and honest

**Body:**

- Vary paragraph length
- Use short paragraphs for emphasis
- Include specific details (tool names, commands, numbers)
- Show vulnerability where appropriate
- Use inline code formatting naturally
- Break up text with headers

**Technical content:**

- Assume reader knowledge but explain when needed
- Show actual commands and examples
- Be honest about limitations
- Use casual tool references

**Tone modulation:**

- Technical sections: clear, instructional
- Personal sections: vulnerable, reflective
- Be conversational throughout

**Ending:**

- Tie back to opening
- Forward-looking perspective
- Actionable advice
- Optimistic or thought-provoking

### 6. Review and Refine

Check the post:

- Does it sound conversational?
- Is there a clear narrative arc?
- Are technical details specific and accurate?
- Does it show vulnerability appropriately?
- Are paragraphs varied in length?
- Is humor self-aware, not forced?
- Does it end with momentum?

**AI slop check:**

1. Load `references/ai-slop-checklist.md` for the curated guidance and Nick-specific nuances
2. Fetch the current "words to watch" from Wikipedia by calling:
   ```
   https://en.wikipedia.org/w/api.php?action=parse&page=Wikipedia:Signs_of_AI_writing&prop=wikitext&format=json
   ```
   Extract the `{{tmbox}}` "Words to watch" lists and the AI vocabulary word list from the response. These evolve as AI writing patterns change — newer models drop old tells and develop new ones.
3. Scan the draft for vocabulary clusters, formulaic transitions, superficial -ing phrases, and structural tells. One hit is normal; a pattern means the LLM was writing on autopilot instead of in Nick's voice.

If the API fetch fails, fall back to the static checklist alone.

Show the post to the user for feedback and iterate.

**Revision strategy:**

- Re-read `references/voice-tone.md` before revising to recalibrate
- Focus changes on the specific feedback — don't rewrite unrelated sections
- Preserve the overall narrative structure unless the user explicitly requests restructuring
- If feedback is vague ("make it better"), ask what specifically feels off

## Output Format

Format posts using `references/post-template.md` as the structural template. This defines the frontmatter schema and file format for Nick's site.

For detailed voice do's and don'ts, see `references/voice-tone.md`.

## Example Patterns

### Opening hooks:

```markdown
"AI is going to replace developers."

I must have heard that phrase a hundred times in the last year.
```

```markdown
I've been thinking a lot about how we use AI in our daily work.
```

### Emphasis through structure:

```markdown
Then something clicked.

I watched it use rg to search through codebases, just like I would.
```

### Vulnerability:

```markdown
I won't lie – joining Meta was intimidating.
```

### Technical details:

```markdown
I watched it use `rg` to search through codebases, just like I would.
It ran `npm test` to verify its changes weren't breaking anything.
```

### Conclusions:

```markdown
You're not being replaced; you're being amplified.
```

## Bundled Resources

### References

- `references/voice-tone.md` - Complete voice and tone guide. Read this first to capture Nick's style.
- `references/post-template.md` - Output format template with frontmatter schema and structural skeleton.
- `references/ai-slop-checklist.md` - AI writing tells to scan for during review. Adapted from Wikipedia's field guide.

**Narrative frameworks** (read the one that matches the content):

- `references/story-circle.md` - Journey/transformation narrative
- `references/scqa.md` - Situation-Complication-Question-Answer for analytical problem-solving posts
- `references/progressive-disclosure.md` - Simple-to-complex layering for teaching concepts
- `references/compare-contrast.md` - Structured evaluation of trade-offs between options
- `references/post-mortem.md` - Incident/migration retrospective with timeline and lessons
- `references/problem-agitation-solution.md` - Punchy three-act structure for fix/optimization stories

## Workflow Example

User provides brain dump:

```
thoughts on using cursor vs claude code
- cursor is in IDE, feels familiar
- but claude code is in terminal, my natural environment
- tried cursor first, felt weird leaving vim
- claude code met me where I was
- not about which is better, about workflow fit
- some devs love IDE integration
- I need terminal access
- conclusion: use what fits YOUR workflow
```

Process:

1. Read voice-tone.md
2. Choose framework — this is a personal journey, so **Compare & Contrast** with Story Circle elements
3. Outline: Current tools → Trying Cursor → Finding Claude Code → Realization
4. Write opening hook about tool debates
5. Show vulnerability about trying new things
6. Include specific terminal commands naturally
7. Conclude with "meet yourself where you are" message
8. Review for conversational tone and specific details

Sample output (opening paragraphs):

```markdown
"Which AI coding tool should I use?"

I must get asked that question weekly at this point. And honestly? I tried to answer it
the wrong way for months.

When Cursor started blowing up, I did what any curious developer would do — I installed
it and gave it a shot. It's impressive. The inline completions, the chat panel, the way
it weaves right into VS Code. I get why people love it.

But here's the thing: I'm not a VS Code person. I live in the terminal. Vim, tmux,
`rg` piped into `fzf` — that's my happy place. And every time I opened Cursor, I felt
like I was visiting someone else's apartment. Nice place, but not *mine*.

Then I found Claude Code.
```

Notice: conversational hook, specific tool names, vulnerability about trying something new, short paragraph for emphasis at the end.
