---
name: refine
description: Improve Obsidian daily notes — polish writing, add missing wikilinks, extract long sections into dedicated notes, and suggest new vault entities. Use when the user types /refine or asks to clean up daily notes.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(echo $*), Bash(bash skills/transcribe-meeting/*), Bash(ffmpeg *), Bash(ffprobe *), Bash(curl *), Bash(gdown *), Bash(rclone *), Bash(op read*), Bash(whisper* *), Bash(jq *), Bash(file *), Bash(stat *), Bash(ls /tmp/meeting*), Bash(ls /run/media/*), Bash(youtubeuploader *), Bash(ls ~/Videos/*), Bash(ls ~/Pictures/*), Bash(bc *), ToolSearch
---

# Refine Daily Notes

Improve an Obsidian daily note by polishing prose, adding missing wikilinks to maintain a rich knowledge graph, extracting long sections into dedicated notes, and suggesting new vault entities.

## Workflow

### Phase 0: Setup

1. Run `echo $OBSIDIAN_VAULT_PATH` to get the vault root. If empty, ask the user for the path.
2. Determine the target date: use the argument if provided (e.g., `/refine 2026-02-14`), otherwise use today.
3. Read the daily note at `$VAULT/📅 Daily Notes/{date}.md`. Error if missing.

### Phase 1: Transcribe Meeting Recordings

Detect meeting recordings and transcribe them into meeting notes. Two sub-phases run in order: SD card auto-detect (primary), then Google Drive URL scan (fallback).

#### Phase 1a: Recording Detection & Matching (Primary)

1. **Discover screen recordings**:
   ```bash
   bash skills/transcribe-meeting/scripts/find-screenrecordings.sh "{date}"
   ```
   Save JSON output to `/tmp/screenrecs-{date}.json`. If no screen recordings found, use empty array `[]`.

2. **Discover Rodecaster recordings**:
   ```bash
   bash skills/transcribe-meeting/scripts/find-recordings.sh "{date}"
   ```
   Save JSON output to `/tmp/rodecaster-{date}.json`. If SD card not mounted or no recordings found, use empty array `[]`.

3. **Match recordings** by time overlap:
   ```bash
   bash skills/transcribe-meeting/scripts/match-recordings.sh /tmp/screenrecs-{date}.json /tmp/rodecaster-{date}.json
   ```
   This produces groups with `mode`, `video`, `audio`, and `transcribe_from` fields.

   If both arrays are empty, skip to Phase 1b silently.

4. **Check idempotency**: For each group, search for existing meeting notes by **both** `recording:` and `video_file:` fields:
   ```
   grep -rl 'recording: "{folder}"' "$VAULT/🎙️ Meetings/"
   grep -rl 'video_file: "{filename}"' "$VAULT/🎙️ Meetings/"
   ```
   Skip any group that already has a meeting note (matched by either field).

5. **Match to time entries**: For each new group, scan the daily note time entries for meeting-like entries. Use the recording start time and duration to correlate. Present to the user with mode info:
   > Found 2 recording groups:
   > 1. **omarchy-only**: screen recording from 09:36 (30 min) — no Rodecaster match. Match to `[[EWG]] - team standup - 0.5`?
   > 2. **omarchy+rodecaster**: screen recording from 11:02 + Rodecaster 10 (51 min). Match to `[[Khov]] - sync with Don - 1`?

6. **Extract context** from the matched time entry:
   - **Project**: The wikilinked project name (e.g., `[[Khov]]`)
   - **Description**: The task/meeting description (e.g., "sync with Don")
   - **Participants**: Any names mentioned in the line or surrounding context

7. **Determine audio source** for transcription:
   - `omarchy+rodecaster` → audio = Rodecaster WAV (`audio.path`)
   - `omarchy-only` → extract audio from screen recording:
     ```bash
     bash skills/transcribe-meeting/scripts/extract-audio.sh "{video.path}"
     ```
   - `rodecaster-only` → audio = Rodecaster WAV (`audio.path`)

8. **Transcribe inline** (do NOT use Task/sub-agents — they lack bash permissions). For each new group:

   a. Determine the engine: `echo $OBSIDIAN_WHISPER_ENGINE` (defaults to `openai` if unset).
   b. Run transcription directly:
      ```bash
      bash skills/transcribe-meeting/scripts/transcribe.sh "{wav_path}" "{engine}"
      ```
   c. Capture the JSON output (array of `{start, end, text}` segments).
   d. Generate a meeting note following the format in `skills/transcribe-meeting/SKILL.md` Phase 3:
      - Title, Summary, Decisions, Action Items, Open Questions, Transcript
      - Use context from the matched time entry (project, description, participants)
   e. **Present the summary to the user for approval** before writing.
   f. Create the meeting note at `$VAULT/🎙️ Meetings/{date} {Title}.md` with frontmatter:
      - `recording: "{folder}"` (if Rodecaster audio exists)
      - `audio_url: "{wav_path}"`
      - `video_file: "{video_filename}"` (if screen recording exists)
      - `recording_mode: "{mode}"`

   **Phase 3.5: Extract Key Screenshots** (only when video recording exists):

   **Step 1 — Find user screenshots taken during the meeting**:
   ```bash
   bash skills/transcribe-meeting/scripts/find-screenshots.sh "{date}" "{start_time}" "{duration_secs}"
   ```
   This returns a JSON array of screenshots from `~/Pictures/` (or `$OMARCHY_SCREENSHOT_DIR` / `$XDG_PICTURES_DIR`) taken during the meeting timeframe (±5 min buffer). Each entry has `path`, `timestamp`, and `offset_secs`.

   **Step 2 — Copy and embed user screenshots**:
   For each found screenshot:
   - Copy to `$VAULT/🗜️Attachments/{meeting-name}-user-{HH-MM-SS}.png`
   - Place in the meeting note at the transcript position closest to its `offset_secs`
   - Embed using `![[filename.png]]`

   **Step 3 — Supplement with ffmpeg-extracted frames**:
   - If fewer than 3 user screenshots were found, scan the transcript for visual moments (screen sharing, demos, "as you can see", "look at this", code references, topic transitions) and extract additional frames to reach 3-8 total:
     ```bash
     ffmpeg -ss {secs} -i "{video}" -frames:v 1 -q:v 2 -y "$VAULT/🗜️Attachments/{name}-{MM-SS}.png"
     ```
   - If 3+ user screenshots were found, skip ffmpeg extraction entirely.
   - If no user screenshots at all, fall back entirely to existing ffmpeg extraction behavior (select 3-8 key timestamps).

   Embed all screenshots at corresponding transcript positions using `![[filename.png]]`.

9. **Post-process & upload**: After transcription completes for each group:

   a. **Compress WAV → MP3** and **upload to Google Drive**:
      ```bash
      bash skills/transcribe-meeting/scripts/compress.sh "{wav_path}"
      bash skills/transcribe-meeting/scripts/upload-gdrive.sh "/tmp/meeting-archive/{filename}.mp3"
      ```
      Capture the Google Drive URL. Update `audio_url` in the meeting note.

   b. **Merge video + audio** (omarchy+rodecaster only):
      ```bash
      bash skills/transcribe-meeting/scripts/merge-av.sh "{video.path}" "{audio.path}"
      ```

   c. **Upload to YouTube** (omarchy+rodecaster and omarchy-only):
      ```bash
      bash skills/transcribe-meeting/scripts/upload-youtube.sh "{video_file}" "{meeting_title}" "{summary}" "{date}"
      ```
      - For `omarchy+rodecaster`: upload the **merged** MP4
      - For `omarchy-only`: upload the **original** screen recording MP4
      - Capture the YouTube URL. Update `video_url` in the meeting note.

10. **Update daily note**: Append a wikilink to the matched time entry line:
    ```
    - [[Khov]] - sync with Don - 1 - [[2026-02-18 Khov Sync with Don]]
    ```

11. **Update project note**: If the project has a note in `$VAULT/🗂️ Projects/`, add a `## Meetings` section (or append to existing) with a wikilink to the meeting note.

**Present the transcription summary to the user for confirmation before writing the meeting note** (consistent with refine's preview-before-applying pattern).

#### Phase 1b: Google Drive URL Detection (Fallback)

Scan the daily note for Google Drive audio links and transcribe them into meeting notes.

1. **Scan for audio URLs**: Look for lines containing `drive.google.com/file/d/` in the daily note text.
2. **Check for existing transcriptions**: For each URL found, search `$VAULT/🎙️ Meetings/` for a note with matching `audio_url` in frontmatter:
   ```
   grep -rl "audio_url:.*{file-id}" "$VAULT/🎙️ Meetings/"
   ```
   If a meeting note already exists for this URL, skip it (idempotent).
3. **Extract context**: From the daily note line containing the URL, infer:
   - **Project**: The wikilinked project name (e.g., `[[Khov]]`)
   - **Description**: The task/meeting description (e.g., "sync with Don")
   - **Participants**: Any names mentioned in the line or surrounding context
4. **Transcribe inline** (do NOT use Task/sub-agents). For each new recording:

   a. Download the audio:
      ```bash
      bash skills/transcribe-meeting/scripts/download-gdrive.sh "{url}"
      ```
   b. Determine the engine: `echo $OBSIDIAN_WHISPER_ENGINE` (defaults to `openai` if unset).
   c. Run transcription directly:
      ```bash
      bash skills/transcribe-meeting/scripts/transcribe.sh "{local_audio_path}" "{engine}"
      ```
   d. Capture the JSON output (array of `{start, end, text}` segments).
   e. Generate a meeting note following the format in `skills/transcribe-meeting/SKILL.md` Phase 3.
   f. **Present the summary to the user for approval** before writing.
   g. Create the meeting note at `$VAULT/🎙️ Meetings/{date} {Title}.md`.

5. **Update daily note**: Replace the Google Drive link in the daily note line:
   ```
   - [[Project]] - description - hours - [recording](https://drive.google.com/...)
   ```
   To:
   ```
   - [[Project]] - description - hours - [[{date} {Title}]]
   ```
6. **Update project note**: If the project has a note in `$VAULT/🗂️ Projects/`, add a `## Meetings` section (or append to existing) with a wikilink to the meeting note.

**Present the transcription summary to the user for confirmation before writing the meeting note** (consistent with refine's preview-before-applying pattern).

If no recordings are found from either source, skip this phase silently.

#### Phase 1c: Meeting Action Items → Daily Todos

After all meeting notes are created (from Phase 1a and 1b), extract action items and propose them as daily todos.

1. **Collect action items**: For each newly created meeting note, read its `## Action Items` section.
2. **Filter for Olivier's items**: Extract items assigned to Olivier (look for `@Olivier`, `Olivier:`, or unattributed items from 1:1 meetings where Olivier is a participant).
3. **Map to projects**: Use the meeting frontmatter `project:` field to determine which project section each item belongs to.
4. **Check for duplicates**: Fuzzy-match each proposed todo against existing todos in the daily note. Skip items that are already present (even if worded slightly differently).
5. **Present proposed insertions** grouped by project:
   > From [[2026-02-20 EXSQ Sol 1-1 Sync]]:
   > - [ ] [[EXSQ]] - Set up Claude Code access for Sol
   > - [ ] [[EXSQ]] - Explore Figma + GitHub integration feasibility
6. **If approved**, insert under the matching project heading in the daily note's todos section. If no matching heading exists, create one using `### [[Project]]` format.
7. **Format**: `- [ ] [[Project]] - task description (from [[Meeting Note]])` with nested sub-items if the action item has sub-tasks.

If no new meeting notes were created or no action items found, skip this phase silently.

### Phase 2: Discover Vault Entities

Build a catalog of all known entities so you can match them against the daily note text.

1. **Projects**: List files recursively in `$VAULT/🗂️ Projects/` — extract project names from filenames
2. **People**: List files in `$VAULT/👤 Persons/` — read each file to extract `aliases` from frontmatter
3. **Topics**: List files in `$VAULT/📚 Topics/` — extract topic names from filenames
4. **Coding sessions**: List files in `$VAULT/💻 Coding/` — for cross-reference awareness
5. **Meetings**: List files in `$VAULT/🎙️ Meetings/` — for cross-reference awareness and to avoid duplicate transcription

This gives you the full entity catalog to match against the daily note.

### Phase 2b: Slack Activity Scan (Optional)

**This phase is optional** — skip gracefully if Slack MCP tools are unavailable.

1. **Load Slack tools**: Use `ToolSearch` to search for `slack` tools. If no Slack MCP tools are available, skip this phase entirely with no error.
2. **Search for user's messages** on the target date using `slack_search_public_and_private`:
   - Query: `from:<@U07J89FDWPJ> on:{date}`
3. **Group messages** by channel and 30-minute time windows.
4. **Build a time coverage map** from existing daily note time entries (start times, durations, projects).
5. **Identify gaps**: time windows with 3+ Slack messages but no matching time entry.
6. **Detect huddles**: For each DM or group DM channel found in step 2, read messages around the activity window using `slack_read_channel` with `oldest`/`latest` timestamps. Look for messages from Slackbot containing `"A huddle started"`.
   - Slack's search API does **not** index huddle system messages — they can only be found by reading the channel directly.
   - When a huddle is found, record:
     - **Start time**: the Slackbot message timestamp
     - **Participants**: inferred from the DM/group DM members (the channel context)
     - **Estimated duration**: gap between the huddle start and the next human message in the channel (rough estimate — Slack does not expose huddle duration via API)
   - Huddles should **always** have a corresponding time entry. Flag any huddle that doesn't match an existing entry.
7. **Infer channel→project mapping** from channel names and existing time entries:
   - Check cached mappings in `$VAULT/.claude/intervals-cache/slack-mappings.md`
   - If a new channel→project mapping is discovered, append it to the cache file
8. **Present findings**:
   > Slack activity not covered by time entries:
   > - **#technomic-dev** (2:30-3:15pm, 8 messages): discussed vector search PR issues → [[Technomic]]?
   > - **#exsq-general** (4:00-4:20pm, 4 messages): coordinated with team on AI Upskill → [[EXSQ]]?
   > Add time entries for these?
   >
   > Huddles detected:
   > - **DM with [[Sol Parrot|Sol]]** (12:16pm, ~1h54m): matches `[[EXSQ]] - 1:1 sync with Sol - 2` ✓
   > - **DM with [[Adam Herrneckar|Adam]]** (3:05pm, ~25m): no matching time entry — add one?
9. **If approved**, suggest time entry lines but do **NOT** auto-insert into time entries — present them for the user to manually add (time entries are sacred structured data).

### Phase 3: Analyze & Improve Writing

Review each section of the daily note:

- **Skip time entries** — the bullet list at the top (lines like `- [[Project]] - task - duration`) is structured data for the intervals skill. Never modify these.
- **Improve prose** — fix grammar, improve clarity, tighten wording. Keep it concise.
- **Fix formatting** — consistent heading levels, list styles, spacing.
- **Preserve todos** — don't reorder, rewrite, or change checkbox state. Only improve prose around them.
- **Author's voice** — improve clarity without rewriting the user's natural style. Don't make it sound like AI wrote it.

### Phase 4: Add Missing Wikilinks

Scan all text (outside time entries) for mentions of known entities:

- **Projects**: Add `[[Project Name]]` links where project names appear unlinked
- **People**: Add `[[Full Name]]` or `[[Full Name|Alias]]` when a short name or alias is used
- **Topics**: Add `[[Topic]]` links where topic names appear unlinked
- **Heading style**: Use `### [[Project]]` for project section headings consistently

**Rules:**
- Don't double-link — skip text already inside `[[...]]`
- Don't link inside time entry lines
- Link known entities freely without asking the user

### Phase 5: Extract Long Sections

Identify sections that are >~20 lines or contain substantial standalone content worth its own note.

For each extractable section:

1. **Determine destination**: `🗂️ Projects/` subtree or `📚 Topics/` based on content
2. **Create the new note** with proper format:
   ```markdown
   # {Title}

   {Extracted content}

   ## Related
   - [[📅 Daily Notes/{date}]]
   ```
3. **Replace the section** in the daily note with a brief summary + `[[wikilink]]` to the new note

**Present all proposed extractions to the user for approval before executing.** Show what would be extracted, where it would go, and what the replacement summary would look like.

### Phase 5b: Suggest New Entities

Identify mentions of people, projects, or topics that don't match any existing vault note.

Present these as candidates:
```
It looks like **Jane Smith** and **ProjectX** are mentioned but don't have vault pages yet.
Want me to create them?
```

For each confirmed new entity, create the note following vault conventions:

- **Person**: `$VAULT/👤 Persons/{Name}.md`
  ```markdown
  ---
  aliases:
    - {short name}
  ---
  # {Full Name}

  **Role**: {if known}
  **Projects**: {if known}

  ## Notes
  ```

- **Project**: `$VAULT/🗂️ Projects/{Name}.md` (or appropriate subdirectory)
  ```markdown
  # {Project Name}

  {Brief description if known}

  ## Related
  ```

- **Topic**: `$VAULT/📚 Topics/{Name}.md`
  ```markdown
  # {Topic Name}

  {Brief definition if known}

  ## Related

  ## Notes
  ```

After creating new entities:
- Add them to the respective MOC file (e.g., Persons MOC, Topics MOC) if one exists
- Link them in the daily note (they now exist as vault pages)

### Phase 5c: Suggest Todo Completions

Scan unchecked todos against today's content to suggest completions with high confidence.

1. **Collect unchecked todos** from the daily note (lines matching `- [ ]`).
2. **Build an evidence corpus** from:
   - Meeting note `## Decisions` and `## Action Items` sections (items marked complete)
   - Coding session summaries and files changed (from `💻 Coding/` notes for this date)
   - PR review verdicts (merged PRs mentioned in notes)
   - Daily note prose sections
3. **Match todos to evidence** — for each unchecked todo, check for HIGH confidence matches only:
   - Strong keyword overlap between todo text and evidence
   - Explicit completion signals ("merged PR #X", "completed", "done", "shipped", "deployed")
4. **Present suggestions with evidence**:
   > These todos appear done based on today's work:
   > - `review PRs` — Evidence: wrote detailed reviews for PRs #650, #636, #571, #469
   > - `fix vector search` — Evidence: coding session [[2026-02-20--TechnomicIgnite--fix-vector-search]] shows fixes deployed
   > Mark as complete? (✅ 2026-02-20)
5. **If approved**, check off the todos: change `- [ ]` to `- [x]` and append completion date ` (✅ {date})`.

**Rules:**
- Never suggest more than 5 completions at once
- Skip anything below ~80% confidence — better to miss one than suggest a false positive
- Never auto-complete without user approval
- If no high-confidence matches found, skip this phase silently

### Phase 6: Apply & Confirm

1. **Show a summary** of all proposed changes before writing:
   - Prose improvements (brief description)
   - Wikilinks added (list them)
   - Sections extracted (destination paths)
   - New entities created (paths)
2. **Get user approval** before applying
3. **Apply changes**: edit the daily note, create any extracted/new entity notes
4. **Report**: what was changed, what was linked, what was extracted, what was created

### Phase 7: Update Project Recent Activity

After all daily note changes are applied, update each referenced project's note with a summary of today's activity.

1. **Identify projects** from today's time entries in the daily note.
2. **For each project** with a note in `$VAULT/🗂️ Projects/`:
   - Read the existing `## Recent Activity` section (or prepare to create it)
   - Build today's entry: `- **{date}**: {hours}h — {brief summary} (meetings: [[links]], coding: [[links]])`
   - Prune entries older than 7 days from the section
   - Insert the `## Recent Activity` section before `## Key Features` or at the end of the note if no logical insertion point
3. **Check idempotency**: If an entry for today's date already exists, update it rather than duplicating.
4. **Present all proposed project note updates** for approval before applying.
5. **Apply changes** if approved.

### Phase 7b: Update Person Interaction History

Update person notes for anyone who appeared in today's meetings.

1. **Collect participants** from all newly created meeting notes (from frontmatter `participants:` field).
2. **For each person** with a note in `$VAULT/👤 Persons/`:
   - Read the existing `## Recent Interactions` section (or prepare to create it)
   - Build entry: `- **{date}**: [[Meeting Note]] — {topics discussed, action items for/from them}`
   - Prune entries older than 30 days from the section
   - Insert the `## Recent Interactions` section before `## Notes` or at the end of the note
3. **Check idempotency**: If an entry for today's date + same meeting already exists, skip it.
4. **Present all proposed person note updates** for approval before applying.
5. **Apply changes** if approved.

If no new meeting notes were created or no participants have vault pages, skip this phase silently.

## Key Rules

- **Never modify time entries** — the bullet list at the top is structured data
- **Preserve todos** — only improve prose around them
- **Link known entities freely** — no need to ask for entities that already exist
- **Offer to create unknown entities** — ask before creating new vault pages
- **Author's voice** — improve clarity without rewriting style
- **Idempotent** — running twice shouldn't cause issues (don't re-extract already-extracted sections, don't double-link)
- **Show before applying** — always preview changes for user approval
