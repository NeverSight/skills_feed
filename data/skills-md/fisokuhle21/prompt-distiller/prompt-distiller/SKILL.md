---
name: prompt-distiller
description: |
  Analyze multi-turn AI coding conversations to generate optimized one-shot prompts that capture the essence of iterative work. 
  Use when: (1) A conversation took multiple iterations to achieve the desired result, (2) You want to create a reusable prompt for similar future tasks, 
  (3) You need to understand what information was missing from the initial request, (4) Planning a complex task and want to generate clarifying questions upfront.
  Supports OpenCode, Claude Code, Gemini CLI, and Codex CLI session data.
---

# Prompt Distiller

Transform iterative conversations into optimized one-shot prompts. Learn from multi-turn exchanges to create prompts that succeed on the first try.

## Mode Selection

Determine which mode applies:

**Distilling a conversation?** User wants to create a one-shot prompt from a session.
- Follow: DISTILL Workflow below

**Planning a new task?** User wants to plan ahead with clarifying questions.
- Follow: PLAN Workflow below

**Listing sessions?** User wants to see available conversations.
- Follow: LIST Workflow below

## DISTILL Workflow

### Step 1: List Available Sessions

Run the session listing script to find conversations:

```bash
python scripts/list_sessions.py [--agent opencode|claude|gemini|codex|all] [--limit 20]
```

Present sessions to user with:
- Session ID/timestamp
- Initial prompt preview
- Message count
- Duration/turns

### Step 2: Load and Parse Session

Once user selects a session or provides a conversation file/URL:

```bash
# Parse OpenCode/Claude/Gemini/Codex session by ID
python scripts/parse_session.py <session-id-or-path> [--agent opencode|claude|gemini|codex]

# Parse external conversation files (.md, .txt)
python scripts/parse_session.py conversation.md
python scripts/parse_session.py chat_export.txt

# Parse from URL (automatically downloads large files)
python scripts/parse_session.py https://example.com/conversation.md
python scripts/parse_session.py https://gist.githubusercontent.com/.../chat.md --save-dir ~/downloads/
```

The script will:
- Detect agent type if not specified (supports `opencode`, `claude`, `gemini`, `codex`, `file`, or `url`)
- Download files from URLs if too large to read online (saved to `~/.cache/prompt-distiller/downloads/`)
- Parse external .md/.txt files with various conversation formats
- Extract all user messages and assistant responses
- Identify tool calls and their results
- Track file modifications and key decisions

**Supported External File Formats:**
- Markdown headers: `## User` / `## Assistant`
- Prefix format: `User:` / `Assistant:` 
- Human/AI format: `Human:` / `AI:`
- Numbered format: `1. User:` / `2. Assistant:`

### Step 3: Analyze the Conversation

Run the distillation analysis:

```bash
# Default: saves to ./distilled-prompts/
python scripts/distill_prompt.py <session-id-or-path>

# Custom output directory
python scripts/distill_prompt.py <session> --output ~/my-prompts/

# Custom output file path
python scripts/distill_prompt.py <session> --output ~/prompts/my-prompt.md

# Output to stdout
python scripts/distill_prompt.py <session> --stdout
```

The analyzer identifies:
1. **Initial Intent** - What the user originally wanted
2. **Missing Context** - Information that had to be clarified
3. **Corrections Made** - Where the assistant went wrong
4. **Key Decisions** - Important choices that shaped the outcome
5. **Final Solution** - What actually worked

### Step 4: Generate One-Shot Prompt

The script outputs a markdown file containing:

```markdown
# Distilled Prompt: [Task Summary]

## Original Context
- Session: [ID]
- Turns: [N]
- Duration: [Time]

## One-Shot Prompt

[The optimized prompt that includes all necessary context upfront]

## What Made This Work
- [Key insight 1]
- [Key insight 2]

## Anti-Patterns Avoided
- [What went wrong initially]

## Reusability Notes
- [When to use this prompt template]
- [Variables to customize]
```

**Output Format Options:**

```bash
# Get only the one-shot prompt (no metadata)
python scripts/distill_prompt.py <session> --prompt-only

# Get JSON output for programmatic use
python scripts/distill_prompt.py <session> --json

# Ready-to-use: display prompt + copy to clipboard
python scripts/distill_prompt.py <session> --use
```

The `--use` flag is particularly useful for immediately using the distilled prompt:
- Displays the optimized prompt
- Automatically copies to clipboard (xclip, xsel, or pbcopy)
- Provides instructions for starting a new session

### Step 5: Review and Refine

Present the distilled prompt to the user. Ask:
- Does this capture the essential requirements?
- Are there domain-specific details to add?
- Should any sections be expanded or condensed?

## PLAN Workflow

### Step 1: Gather Initial Request

Ask the user to describe their task. Listen for:
- Vague requirements
- Assumed context
- Implicit constraints
- Missing acceptance criteria

### Step 2: Generate Clarifying Questions

Run the planning question generator:

```bash
python scripts/generate_questions.py --task "<user's task description>"
```

The script generates questions across categories:
- **Scope**: What's in/out of bounds?
- **Context**: What existing code/patterns to follow?
- **Constraints**: Performance, compatibility, style requirements?
- **Acceptance**: How will success be measured?
- **Edge Cases**: What happens when things go wrong?

### Step 3: Conduct Planning Interview

Present questions to the user in batches of 3-5. Prioritize:
1. Blocking questions (can't proceed without answers)
2. Scope clarifications
3. Nice-to-have details

After each batch, assess if enough context has been gathered.

### Step 4: Synthesize One-Shot Prompt

Once sufficient context is gathered:

```bash
python scripts/synthesize_prompt.py --task "<task>" --answers "<qa-pairs>"
```

Generate a comprehensive prompt that:
- States the objective clearly
- Provides all necessary context
- Specifies constraints and preferences
- Defines acceptance criteria
- Anticipates edge cases

### Step 5: Validate the Prompt

Present the synthesized prompt and ask:
- Is anything missing?
- Are priorities correct?
- Should any constraints be relaxed?

## LIST Workflow

### List OpenCode Sessions

```bash
python scripts/list_sessions.py --agent opencode
```

Default location: `~/.local/share/opencode/storage/`

### List Claude Code Sessions

```bash
python scripts/list_sessions.py --agent claude
```

Default location: `~/.claude/projects/`

### List Gemini CLI Sessions

```bash
python scripts/list_sessions.py --agent gemini
```

Default location: `~/.gemini/tmp/<project_hash>/chats/`

### List Codex CLI Sessions

```bash
python scripts/list_sessions.py --agent codex
```

Default location: `~/.codex/sessions/`

### List All Agents

```bash
python scripts/list_sessions.py --agent all
```

## External Conversation Files

You can also distill prompts from exported conversations or manually created files:

```bash
# Parse and analyze a markdown conversation
python scripts/distill_prompt.py conversation.md --use

# Parse a text file export
python scripts/distill_prompt.py chat_export.txt --output ~/prompts/
```

**Supported Formats:**
- `## User` / `## Assistant` - Markdown headers
- `User:` / `Assistant:` - Colon-prefixed messages
- `Human:` / `AI:` - Alternative role names
- `1. User:` / `2. Assistant:` - Numbered messages
- `>>> User >>>` / `--- Assistant ---` - Block separators

If no format is detected, the entire file is treated as a single user message.

## URL Support

Distill prompts directly from conversations hosted online. Large files are automatically downloaded locally:

```bash
# Download and distill from URL
python scripts/distill_prompt.py https://example.com/conversation.md --use

# Download from GitHub Gist
python scripts/distill_prompt.py https://gist.githubusercontent.com/user/id/raw/chat.md

# Specify custom download directory
python scripts/distill_prompt.py https://example.com/large-chat.md --save-dir ~/downloads/

# Force re-download (bypass cache)
python scripts/distill_prompt.py https://example.com/chat.md --force

# Set maximum file size (default 50MB)
python scripts/distill_prompt.py https://example.com/huge-chat.md --max-size 100
```

**URL Features:**
- Automatic file type detection from URL
- Caches downloaded files in `~/.cache/prompt-distiller/downloads/`
- Respects `--force` flag to re-download
- Configurable max file size limit (default 50MB)
- Works with raw GitHub, Gists, Pastebin, and any direct file URL

## Session Data Locations

| Agent | Default Path | Format |
|-------|--------------|--------|
| OpenCode | `~/.local/share/opencode/storage/` | JSON |
| Claude Code | `~/.claude/projects/` | JSONL |
| Gemini CLI | `~/.gemini/tmp/<project_hash>/chats/` | JSON |
| Codex CLI | `~/.codex/sessions/` | JSON |

Override with environment variables:
- `OPENCODE_SESSIONS_PATH`
- `CLAUDE_SESSIONS_PATH`
- `GEMINI_SESSIONS_PATH`
- `CODEX_SESSIONS_PATH`

## Resources

### scripts/

| Script | Purpose |
|--------|---------|
| `list_sessions.py` | List available conversation sessions (OpenCode, Claude, Gemini, Codex) |
| `parse_session.py` | Parse session data (OpenCode, Claude, Gemini, Codex, files, or URLs) |
| `distill_prompt.py` | Analyze conversation and generate one-shot prompt |
| `generate_questions.py` | Generate planning questions for a task |
| `synthesize_prompt.py` | Create prompt from task + Q&A answers |

### distill_prompt.py Options

| Flag | Description |
|------|-------------|
| `--output PATH` | Custom output file or directory |
| `--stdout` | Print full output to stdout |
| `--prompt-only` | Output only the one-shot prompt (no metadata) |
| `--use` | Display prompt and copy to clipboard |
| `--json` | Output analysis as JSON |
| `--agent TYPE` | Force agent type: opencode, claude, gemini, codex, file, or url |
| `--save-dir PATH` | Directory for downloaded files (URLs) |
| `--force` | Force re-download even if cached |
| `--max-size MB` | Maximum download size in MB (default: 50) |

### parse_session.py Options

| Flag | Description |
|------|-------------|
| `--agent TYPE` | Force agent type: opencode, claude, gemini, codex, file, or url |
| `--output FILE` | Save parsed output to file |
| `--json` | Output as JSON instead of formatted text |
| `--save-dir PATH` | Directory for downloaded files (URLs) |
| `--force` | Force re-download even if cached |
| `--max-size MB` | Maximum download size in MB (default: 50) |

### references/

- [prompt-patterns.md](references/prompt-patterns.md) - Effective prompt structures and templates
- [analysis-criteria.md](references/analysis-criteria.md) - How conversations are analyzed
