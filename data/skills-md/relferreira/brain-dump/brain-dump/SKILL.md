---
name: brain-dump
description: Capture URLs, text, and images into personal knowledge base. Use when user says /brain-dump, "save this URL", "dump this", "capture this", "brain dump", "remember this", or wants to search or learn from saved content.
argument-hint: "[url | text | search <query> | learn [random|today]]"
allowed-tools: Bash, Read, Write, Glob, Grep, WebFetch
---

# Brain Dump Skill

Capture URLs, text, and images into a personal knowledge base stored as Markdown files in `~/.brain-dump/`.

## Commands

```
/brain-dump                    → List recent dumps
/brain-dump search <query>     → Search titles and content
/brain-dump learn              → Learn from smart selection (default: random)
/brain-dump learn random       → Learn from random dumps
/brain-dump learn today        → Learn from today's dumps
/brain-dump <url>              → Fetch, summarize, save URL
/brain-dump <image-path>       → Describe and save image
/brain-dump <text>             → Summarize (if long) and save text
```

## Instructions

### Step 1: Detect Input Type

Parse the arguments after `/brain-dump`:

1. **No arguments** → List mode
2. **Starts with `search `** → Search mode (query is everything after "search ")
3. **Starts with `learn`** → Learn mode (check for subcommand: `random`, `today`, or default to smart selection)
4. **Starts with `http://` or `https://`** → URL mode
5. **File path ending in `.png/.jpg/.jpeg/.gif/.webp/.svg` (and file exists)** → Image mode
6. **Anything else** → Text mode

### Step 2: Get Home Directory and Ensure Directory Exists

First, get the home directory path and create directories if needed:
```bash
echo $HOME && mkdir -p ~/.brain-dump/assets
```

**IMPORTANT**: For all Glob, Read, and Write operations, use the full expanded path (e.g., `/Users/username/.brain-dump/`) not `~`. The `~` only works in Bash commands.

### Step 3: Process Based on Mode

---

#### LIST MODE (no arguments)

1. First, get the home directory using Bash: `echo $HOME`
   - This returns the full path like `/Users/relferreira`
2. Use Glob with:
   - `pattern`: `*.md`
   - `path`: The home directory + `/.brain-dump` (e.g., `/Users/relferreira/.brain-dump`)
   - NEVER use `~` in path - it won't expand. Always use the full path from step 1.
3. For each file found (up to 10 most recent):
   - Read the frontmatter to extract date, tags, type
   - Extract the title (first `# ` heading)
4. Display a formatted list:
   ```
   Recent dumps:

   1. [2024-01-28] Article Title (url) #tag1 #tag2
   2. [2024-01-27] Quick Note (text) #notes
   ...
   ```
5. If no files found, say: "No dumps yet. Use `/brain-dump <url>`, `/brain-dump <text>`, or `/brain-dump <image-path>` to get started."

---

#### SEARCH MODE (starts with "search ")

1. Extract the query (everything after "search ")
2. Get the home directory using Bash: `echo $HOME`
3. Use Grep to search for the query:
   - `pattern`: the search query (case insensitive with `-i: true`)
   - `path`: The home directory + `/.brain-dump` (e.g., `/Users/relferreira/.brain-dump`)
   - `glob`: `*.md`
   - `output_mode`: `files_with_matches`
4. For each matching file:
   - Read the file to extract title, date, tags, and type from frontmatter
   - Show a snippet of the matching content (the line with the match)
5. Display results:
   ```
   Search results for "query":

   1. [2024-01-28] Article Title (url) #tag1 #tag2
      ...matching text snippet...

   2. [2024-01-27] Another Article (note) #notes
      ...matching text snippet...
   ```
6. If no matches found, say: "No dumps found matching 'query'."

---

#### LEARN MODE (starts with "learn")

Learn mode teaches you content from your dumps and then quizzes you.

**Step 1: Parse subcommand**
- `learn` or `learn random` → Smart/random selection
- `learn today` → Today's dumps only

**Step 2: Get home directory and load history**
```bash
echo $HOME
```
Then read `$HOME/.brain-dump/learn-history.json` if it exists.

**Step 3: Select dumps based on mode**

For `today`:
- Get all dumps where frontmatter `date` matches today's date (YYYY-MM-DD)
- If no dumps today, say: "No dumps from today. Try `/brain-dump learn random` instead."

For `random` (default - smart selection):
- Get all dump files using Glob
- Select 3-5 dumps using this priority:
  1. **2 new dumps** - files never seen in learn history
  2. **1 weak dump** - file with lowest score ratio from history (if any)
  3. **1-2 random dumps** - any files for reinforcement
- If fewer than 3 total dumps exist, use all of them

**Step 4: Teach Phase**
1. Read all selected dump files
2. Generate a cohesive lesson that:
   - Introduces the topics covered
   - Highlights key concepts from each dump
   - Makes connections between related ideas
3. Present the lesson:
   ```
   📚 Today's Lesson (3 dumps)

   You've been learning about [topics]...

   Key concepts:
   • [Concept 1 from dump 1]
   • [Concept 2 from dump 2]
   • [Concept 3 from dump 3]

   [2-3 paragraphs synthesizing the content]
   ```

**Step 5: Quiz Phase**
1. Generate 3-5 questions based on the lesson content
2. Mix question types:
   - Multiple choice (A/B/C/D)
   - True/False
   - Short answer
3. Ask questions one at a time:
   ```
   Question 1 of 4:

   What is the main benefit of [concept]?

   A) Option 1
   B) Option 2
   C) Option 3
   D) Option 4
   ```
4. Wait for user's answer
5. Respond with correct/incorrect and brief explanation
6. Continue to next question

**Step 6: Results and Save History**
1. Calculate score
2. Display results:
   ```
   📊 Results: 4/5 correct (80%)

   ✓ Question 1 - Correct
   ✓ Question 2 - Correct
   ✗ Question 3 - Incorrect (review: thinking-in-react.md)
   ✓ Question 4 - Correct
   ✓ Question 5 - Correct

   Great job! Consider reviewing the dumps you missed.
   ```
3. Save session to history file

**History File Format: `~/.brain-dump/learn-history.json`**
```json
{
  "sessions": [
    {
      "date": "2024-01-28T10:30:00Z",
      "mode": "random",
      "dumps": [
        {
          "file": "thinking-in-react.md",
          "correct": 2,
          "total": 2
        },
        {
          "file": "hooks-note.md",
          "correct": 1,
          "total": 2
        }
      ],
      "score": 4,
      "total": 5
    }
  ]
}
```

**Smart Selection Algorithm:**
When selecting dumps for `random` mode:
1. Parse history to calculate per-file stats:
   - `timesStudied`: how many sessions included this file
   - `correctRatio`: total correct / total questions for this file
2. Categorize files:
   - **New**: `timesStudied === 0`
   - **Weak**: `correctRatio < 0.7` and `timesStudied > 0`
   - **Strong**: `correctRatio >= 0.7`
3. Select in order:
   - Pick up to 2 from New (random)
   - Pick 1 from Weak (lowest ratio first)
   - Fill remaining (up to 5 total) from Strong or any available

---

#### URL MODE (starts with http:// or https://)

1. **Fetch content** using WebFetch with prompt:
   ```
   Extract the main content of this page. Provide:
   1. A clear, descriptive title (not the site name)
   2. A 2-4 sentence summary of the key points
   3. 2-3 relevant tags as a comma-separated list (lowercase, single words)

   Format your response as:
   TITLE: [title]
   SUMMARY: [summary]
   TAGS: [tag1, tag2, tag3]
   ```

2. **Parse the response** to extract title, summary, and tags

3. **Generate filename**:
   - Take the title
   - Convert to lowercase
   - Replace spaces and special chars with hyphens
   - Remove consecutive hyphens
   - Truncate to 50 characters max
   - Add `.md` extension
   - If file exists, append date: `filename-20240128.md`
   - If still exists, append counter: `filename-20240128-2.md`

4. **Create markdown file**:
   ```markdown
   ---
   date: YYYY-MM-DD
   source: [original URL]
   tags: [tag1, tag2, tag3]
   type: url
   ---

   # [Title]

   [Summary]

   ---
   Source: [original URL]
   ```

5. **Write file** to `~/.brain-dump/[filename].md`

6. **Confirm to user**:
   ```
   Saved: [title]
   File: ~/.brain-dump/[filename].md
   Tags: #tag1 #tag2 #tag3
   ```

**Error handling**: If WebFetch fails, offer to save as a simple bookmark:
```markdown
---
date: YYYY-MM-DD
source: [URL]
tags: [bookmark]
type: bookmark
---

# Bookmark: [URL domain]

URL saved for later review.

---
Source: [URL]
```

---

#### IMAGE MODE (image file path)

1. **Validate file exists** using Bash `test -f`

2. **Generate unique asset filename**:
   - Use format: `YYYYMMDD-HHMMSS-[original-filename]`
   - Copy to `~/.brain-dump/assets/`

3. **Read and describe image** using the Read tool (which handles images)

4. **Generate content** based on the image:
   - Create a descriptive title
   - Write a 2-4 sentence description
   - Extract 2-3 relevant tags

5. **Generate markdown filename** from the description (same rules as URL mode)

6. **Create markdown file**:
   ```markdown
   ---
   date: YYYY-MM-DD
   source: [original file path]
   tags: [tag1, tag2, tag3]
   type: image
   ---

   # [Descriptive Title]

   ![image](assets/[asset-filename])

   [Description of the image]

   ---
   Original: [original file path]
   ```

7. **Write file** and **confirm to user**

**Error handling**: If file doesn't exist, ask user to verify the path.

---

#### TEXT MODE (anything else)

1. **Analyze the text**:
   - If less than 500 characters: save as-is, generate title and tags
   - If 500+ characters: generate a 2-4 sentence summary

2. **Generate title**:
   - If text has a clear subject, use it
   - Otherwise, extract key phrase or use first few words

3. **Generate 2-3 tags** relevant to the content

4. **Generate filename** (same rules as URL mode)

5. **Create markdown file**:

   For short text (< 500 chars):
   ```markdown
   ---
   date: YYYY-MM-DD
   tags: [tag1, tag2, tag3]
   type: note
   ---

   # [Title]

   [Original text]
   ```

   For long text (>= 500 chars):
   ```markdown
   ---
   date: YYYY-MM-DD
   tags: [tag1, tag2, tag3]
   type: note
   ---

   # [Title]

   [Summary]

   ---

   ## Original Content

   [Full original text]
   ```

6. **Write file** and **confirm to user**

---

### Filename Generation Helper

To generate a valid filename:

1. Take the source string (title, description, or first words)
2. Convert to lowercase
3. Replace any character that isn't a-z, 0-9, or hyphen with a hyphen
4. Replace multiple consecutive hyphens with a single hyphen
5. Remove leading/trailing hyphens
6. Truncate to 50 characters (don't cut mid-word if possible)
7. Check if file exists in `~/.brain-dump/`:
   - If yes, append today's date: `name-20240128.md`
   - If that exists too, append counter: `name-20240128-2.md`, `name-20240128-3.md`, etc.

### Response Format

Always be concise. After successful save:
```
Saved: [title]
File: ~/.brain-dump/[filename].md
Tags: #tag1 #tag2 #tag3
```

For list mode, show a clean formatted list. For errors, be helpful and suggest fixes.
