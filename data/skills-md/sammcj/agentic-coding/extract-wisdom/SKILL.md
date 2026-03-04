---
name: extract-wisdom
description: Extract wisdom, insights, and actionable takeaways from YouTube videos, blog posts, articles, or text files. Use when asked to analyse, summarise, or extract key insights from a given content source. Downloads YouTube transcripts, fetches web articles, reads local files, performs analysis, and saves structured markdown.
compatibility: Requires Bash Prettier Pandoc & WeasyPrint
allowed-tools: Read Write Edit Glob Grep Task WebFetch WebSearch Bash(bash ~/.claude/skills/extract-wisdom/scripts/download_transcript.sh *) Bash(bash scripts/download_transcript.sh *) Bash(bash ~/.claude/skills/extract-wisdom/scripts/format.sh *) Bash(bash scripts/format.sh *) Bash(bash ~/.claude/skills/extract-wisdom/scripts/render_pdf.sh *) Bash(bash scripts/render_pdf.sh *) Bash(mv *) Bash(mkdir *) Bash(mmdc *) Bash(mermaid-check *) Bash(npx @mermaid-js/mermaid-cli *) Bash(npx -y @mermaid-js/mermaid-cli *) Bash(* --help *)
---

# Wisdom Extraction

Script paths below use `<skill-dir>` to refer to this skill's directory.
Default location: `~/.claude/skills/extract-wisdom/`

## Workflow

### Step 1: Ask User Preferences

Use the `AskUserQuestion` tool to ask the user what level of detail they want (unless they've already stated this in the ask). Use multi-choice with options: "Detailed", "Concise". **Do not call any other tools in the same turn as this question. Wait for the user's response before proceeding to Step 2.** If `AskUserQuestion` is unavailable, default to "Detailed".

### Step 2: Identify Source and Acquire Content

Once you know the level of detail, determine the source type and acquire content accordingly:

#### **YouTube URL** (contains youtube.com or youtu.be)

Execute the download script to fetch only the transcript (no video file):

```bash
bash <skill-dir>/scripts/download_transcript.sh <youtube-url>
```

The script will:

- Auto-detect your environment
- Download English subtitles or auto-generated transcripts
- Output the transcript path and next steps

**Cookie handling:** The script first attempts to download using browser cookies (for access-restricted videos). If no browser is found or cookies fail, it automatically falls back to trying cookie-less download.

After downloading, execute the rename command the script provides:

```bash
mv <OUTPUT_DIR> <OUTPUT_DIR>/../YYYY-MM-DD-<concise-description>
```

- Keep the description short (1-6 words), use hyphens instead of spaces
- Take the video content and title into consideration
- Example: Video "My Interview With Demis Hassabis" becomes `2026-02-05-Demis-Hassabis-Interview`

Then read the transcript file from `TRANSCRIPT_PATH`. Transcripts are cleaned and formatted as continuous text with minimal whitespace.

**Note:** The download script uses `--restrict-filenames` to sanitise special characters in filenames for safer handling.

#### **Web URL or Document Path** (blog posts, articles, any non-YouTube URL)

Use WebFetch to extract content, for example:

```
WebFetch with prompt: "Extract the main article content"
```

WebFetch returns cleaned markdown-formatted content ready for analysis.

Note: Ensure the Webfetch tool does not truncate the content that we likely want to keep! If you have problems with Webfetch you can always use the Fetch tool (or similar).

**Local file path** (.txt, .md, or other text formats):

Use your standard file reading tool (e.g. `Read`) to load the full content directly.

If the content clearly indicates there was an image that is highly likely to contain important information that would not be captured or inferred from the text alone (e.g. a diagram of a complex concept, but NOT things like a photo the author, memes, product logos, screenshots etc...) and if you have the link to the image URL, you may wish to:

- Fetch the image to a temporary location
- Read the image to understand the content
- Validate if the content of the image adds value beyond what is already captured in the text or not
- If it does you could add a concise written description of what the image is trying to convey (but only if the content doesn't already convey this!), - OR if it's a diagram, use Mermaid within the Markdown wisdom document you're creating.

### Step 3: Analyse and Extract Wisdom

IMPORTANT: Avoid signal dilution, context collapse, quality degradation and degraded reasoning for future understanding of the content. Keep the signal-to-noise ratio high. Preserve domain insights while excluding filler or fluff.

Perform analysis on the content, extracting:

#### 1. Key Insights & Takeaways

- Identify the main ideas, core concepts, and central arguments
- Extract fundamental learnings and important revelations
- Highlight expert advice, best practices, or recommendations
- Note any surprising or counterintuitive information

#### 2. Notable Quotes

- Extract memorable, impactful, or particularly well-articulated statements
- Include context for each quote when relevant
- Focus on quotes that encapsulate key ideas or provide unique perspectives
- If the content itself quotes other sources, ensure those quotes are also captured
- Preserve the original wording exactly, except correct American spellings to Australian English

#### 3. Structured Summary

- Create hierarchical organisation of content
- Break down into logical sections or themes
- Provide clear section headings that reflect content structure
- Include high-level overview followed by detailed breakdowns
- Note any important examples, case studies, or demonstrations

#### 4. Actionable Takeaways

- List specific, concrete actions the audience can implement with examples (if applicable)
- Do not add your own advice, input or recommendations outside of what is in the content unless the user has asked you to do so
- Frame as clear, executable steps
- Prioritise practical advice over theoretical concepts
- Include any tools, resources, or techniques mentioned
- Distinguish between immediate actions and longer-term strategies

#### 5. Your Own Insights On The Content

Do this in a separate step, only after you've added the content from the source.

- Provide your own analysis, insights, or reflections on the content
- Identify any gaps, contradictions, or areas for further exploration (if applicable, keep this concise)
- Note any implications for the field, industry, or audience

### Step 4: Write Analysis to Markdown File

Determine the output directory:

**YouTube sources:** The renamed directory from Step 1.

**Web and text sources:** Run the following to determine the base output directory, then use it as described below:

```bash
bash <skill-dir>/scripts/download_transcript.sh --output-dir
```

If the command fails or is unavailable, fall back to `~/Downloads/text-wisdom/`.

Save to `<base-output-dir>/YYYY-MM-DD-<concise-description>/`:

- Create the directory if it doesn't exist
- Use the same date-prefixed naming convention as YouTube sources

**File name:** `<source-title> - analysis.md`

Format the analysis using this structure:

```markdown
# Analysis: [Title]

**Source**: [YouTube URL, web URL, or file path]

**Analysis Date**: [YYYY-MM-DD]

## Summary

[Brief 2-3 sentence overview of the main topic and purpose]

### Simplified Explanation

[Explain It Like I'm 10: A simple 1-2 sentence explanation of the core concept in a way a 10-year-old could understand]

### Key Takeaways

- [Concise takeaway 1]
- [Concise takeaway 2]
- [Concise takeaway 3]

## Key Insights

- [Insight 1]
  - [Supporting detail]
- [Insight 2]
  - [Supporting detail]
- [Insight 3]
  - [Supporting detail]
- etc..

## Notable Quotes (Only include if there are notable quotes)

> "[Quote 1]"

Context: [Brief context if needed]

> "[Quote 2]"

Context: [Brief context if needed]

## Structured Breakdown

### [Section 1 Title]

[Content summary]

### [Section 2 Title]

[Content summary]

## Actionable Takeaways

1. [Specific action item 1]
2. [Specific action item 2]
3. [Specific action item 3]

## Insights & Commentary

[Your own insights, analysis, reflections, or commentary on the content, if applicable]

## Additional Resources

[Any tools, links, or references mentioned in the content]

_Wisdom Extraction: [Current date in YYYY-MM-DD]_
```

After writing the analysis file, inform the user of the location.

### Step 5: Critical Self-Review

Conduct a critical self-review of your summarisation and analysis.

Create tasks to track the following (mechanical checks first, then content quality):

- [ ] No American English spelling - check and fix (e.g. judgment->judgement, practicing->practising, organize->organise)
- [ ] No em-dashes, smart quotes, or non-standard typography
- [ ] Proper markdown formatting
- [ ] Accuracy & faithfulness to the original content
- [ ] Completeness
- [ ] Concise, clear content with no fluff, marketing speak, filler, or padding (high signal-to-noise ratio)
- [ ] Logical organisation & structure

Re-read the analysis file, verify each item, fix any issues found, then mark tasks completed.

After completing your review and edits, format the markdown:

```bash
bash <skill-dir>/scripts/format.sh "path/to/file.md"
```

### Step 7: PDF Export

After all content is created and reviewed, render the markdown analysis to a styled PDF for easier sharing with the following command:

```bash
bash <skill-dir>/scripts/render_pdf.sh "<path-to-analysis.md>"
```

The PDF is saved alongside the markdown file with a `.pdf` extension. Use `--open` to open it after rendering, or `--css <file>` to provide an alternative stylesheet.

The script will check for required dependencies (`pandoc`, `weasyprint`) and tell you what to do if they're missing.

### Step 6: Provide A Short Summary For Sharing

After writing the analysis, generate a concise 1-3 sentence summary suitable for sharing the source on Slack.
Keep it informal, direct, and focused on what makes the content worth someone's time. Include the core concept and why it matters.
Format: plain text, no markdown formatting, no bullet points.

Then stop unless further instructions are given.

---

## Tips

- Don't add new lines between items in a list
- Avoid marketing speak, fluff or other unnecessary verbiage such as "comprehensive", "cutting-edge", "state-of-the-art", "enterprise-grade" etc.
- Always use Australian English spelling
- Do not use em-dashes or smart quotes
- Only use **bold** where emphasis is truly needed
- Ensure clarity and conciseness in summaries and takeaways
- Always ask yourself if the sentence adds value - if not, remove it
- If the source mentions a specific tool, resource or website, task a sub-agent to look it up and provide a brief summary, then include it in the Additional Resources section
- You can consider creating mermaid diagrams to explain complex concepts, relationships, or workflows found in the content
- When reading the content - it **must be read in FULL**, avoid using external plugins such as context-mode, serena etc that may alter the content or that require the use of indexing + search which could lead to loss of content or context.

### Multiple Source Analysis

When analysing multiple sources:

- Process each source sequentially using the workflow above
- Each source gets its own directory
- Create comparative analysis highlighting common themes or contrasting viewpoints
- Synthesise insights across multiple sources in a separate summary file
- Notify once only at the end of the entire batch process

### Topic-Specific Focus

When user requests focused analysis on specific topics:

- Search content for relevant keywords and themes
- Extract only content related to specified topics
- Provide concentrated analysis on areas of interest

### Time-Stamped Analysis (YouTube only)

If timestamps are needed:

- Note that basic transcripts don't preserve timestamps
- Can reference general flow (beginning, middle, end) of content
- For precise timestamps, may need to cross-reference with the actual video

## Resources

### scripts/

- `download_transcript.sh`: Downloads YouTube transcripts (no video files) using yt-dlp. Auto-detects environment (Claude Code/Claw) and OS, outputs paths and next steps.
- `format.sh`: Formats markdown files with prettier. Auto-detects bunx/npx, handles sandbox workarounds, silent on success.
- `render_pdf.sh`: Converts analysis markdown to a styled PDF using pandoc + weasyprint.

### styles/

- `wisdom-pdf.css`: CSS stylesheet for PDF rendering. Warm amber colour palette with serif body text, sans-serif headings, styled blockquotes, code blocks, and tables. Customisable or replaceable via `--css` flag.

---
