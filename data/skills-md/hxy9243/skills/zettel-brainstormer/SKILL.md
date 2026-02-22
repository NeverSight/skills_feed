---
name: zettel-brainstormer
description: It reads from your local zettelkasten notes, find a random idea, and find references by links or tags, then expand the idea with the references.
---

# Zettel Brainstormer 🧠

This skill formalizes the process of taking a rough idea or draft and enriching it with deep research, diverse perspectives, and structured brainstorming.

The configuration file is `config/models.json`, which can be edited manually or using the `setup.py` script.

## New 3-Stage Workflow

This skill now supports a 3-stage pipeline to balance cost and quality:

1) Find References (with `find_links.py`)

- Run `scripts/find_links.py` to identify relevant existing notes.
  - **Wikilinked documents** (follows [[wikilinks]] N levels deep, up to M total docs)
  - **Tag-similar documents** (finds notes with overlapping tags)
- Output: A JSON list of absolute file paths to relevant notes.

2) Subagent: Preprocess contents (with `preprocess_model`)

- The agent iterates through the list of files found in Stage 1.
- For each file:
  - Read the file content.
  - Apply `templates/preprocess.md` using the `preprocess_model`, pass the seed note keypoints and file content as context.
  - Extract: Relevance score, Summary, Key Points, and Quotes.
  - Output: A structured markdown summary of the note.

3) Draft & Humanize (with `pro_model`)

- Gather all preprocessed markdown outputs from Stage 2.
- Apply `templates/draft.md` using the `pro_model`.
- Synthesize points, add proper Obsidian properties, tags, and links.
- Uses the `obsidian` skill if available to match style.

## Files & Scripts

This skill includes the following resources under the skill folder:

- `scripts/find_links.py`  -- finds relevant note paths (linked + tag similar)
- `scripts/draft_prompt.py` -- (Deprecated) generate prompt for agent
- `scripts/obsidian_utils.py` -- shared utilities for wikilink extraction
- `templates/preprocess.md` -- Instructions for subagent to extract info from single note
- `templates/draft.md` -- Instructions for final draft generation
- `config/models.example.json`  -- example configuration file

## Configuration & Setup

**First Run Setup**:
Before using this skill, you must run the setup script to configure models and directories.

```bash
python scripts/setup.py
```

This will create `config/models.json` with your preferences. You can press ENTER to accept defaults.

**Configuration Fields**:
- `pro_model`: The model used for drafting (defaults to agent's current model)
- `preprocess_model`: Cheap model for extraction (defaults to agent's current model)
- `zettel_dir`: Path to your Zettelkasten notes
- `output_dir`: Path where drafts should be saved
- `search_skill`: Which search skill to use for web/X research (web_search, brave_search, or none)
- `link_depth`: How many levels deep to follow [[wikilinks]] (N levels, default: 2)
- `max_links`: Maximum total linked notes to include (M links, default: 10)

## Usage

- Trigger when user asks: "brainstorm X", "expand this draft", "research and add notes to <path>".
- Example workflow (pseudo):
  1. Pick a seed note.
  2. Find Links: `python scripts/find_links.py --input <seed_note> --output /tmp/paths.json`
  3. Preprocess Subagent Loop:
     - Load `/tmp/paths.json`.
     - For each path, read content.
     - Prompt `preprocess_model` with `templates/preprocess.md` + content.
     - Store result.
  4. Final Draft:
     - Concatenate seed note + all preprocess results.
     - Prompt `pro_model` with `templates/draft.md` + concatenated context.
  5. Save result to note.

## Notes for maintainers

- Keep preprocess outputs small (200-600 tokens) to save cost.
- Ensure all external links are included in the `References` section with full titles and URLs.
- When appending, always include a timestamp and short provenance line.
