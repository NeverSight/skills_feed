---
name: insights
description: Analyzes AI coding assistant sessions and generates an HTML report with workflow insights. Use this skill when the user asks to analyze sessions, generate a report, view usage patterns, check statistics, or review their coding workflow. Trigger phrases include "analyze my sessions", "generate a report", "show my stats", "how have I been using you", "session insights", "세션 분석", "리포트 생성", "사용 패턴".
compatibility: Requires bash 4+, jq. Supports Claude Code 2.1+, OpenCode 1.1+, Codex. macOS and Linux.
---

# Insights Skill

## When to Use This Skill

**IMPORTANT: You MUST activate this skill** when you detect ANY of the following signals from the user. Do NOT ask for confirmation — just start executing the orchestration steps below.

### Trigger Phrases (any language)

Use this skill when the user:

- Asks to **analyze sessions**: "analyze my sessions", "세션 분석해줘", "look at my sessions"
- Asks for a **report**: "generate a report", "리포트 만들어줘", "give me a report"
- Asks about **usage patterns**: "how have I been using you?", "사용 패턴 보여줘", "what are my patterns?"
- Asks about **statistics**: "show my stats", "통계 보여줘", "how many sessions?"
- Mentions **workflow insights**: "insights on my workflow", "워크플로우 분석", "what's working well?"
- Asks about **productivity**: "am I productive?", "내 생산성은?", "how efficient am I?"
- Uses **keywords**: "insights", "인사이트", "analytics", "분석", "report", "리포트", "stats", "통계", "sessions", "세션"
- Asks vaguely about **history**: "what have we been doing?", "그동안 뭐했지?", "show me my history"

### What NOT to Trigger On

Do NOT use this skill when the user:
- Asks about a specific coding task (not session analysis)
- Wants to read a single session's content (use session tools directly)
- Asks about this skill's code itself (just read the files)

## Overview

The **insights** skill generates a comprehensive HTML report analyzing your AI coding assistant usage patterns. It automatically detects which CLI you're using (Claude Code, OpenCode, or Codex), collects session data, performs 8 categories of analysis, and produces a styled HTML report with actionable insights.

**What it produces:**
- HTML report with 8 analysis sections
- Quantitative statistics (sessions, messages, duration, tools used)
- Qualitative insights (workflow patterns, friction points, suggestions)
- CLI-specific recommendations
- Self-contained file:// URL (no external dependencies)

## Prerequisites

**Required:**
- bash 4+ (check: `bash --version`)
- jq (JSON processor)

**Supported CLIs:**
- Claude Code 2.1+
- OpenCode 1.1+
- Codex

**Verify dependencies:**
```bash
./scripts/check-deps.sh
```

If dependencies are missing, the script provides install instructions.

## Orchestration Steps

Follow these steps in order. Each step depends on the previous one.

### Step 1: Check Dependencies

**Run:** `scripts/check-deps.sh`

**Purpose:** Verify jq and bash 4+ are installed.

**Action:**
- If exit code 0: Continue to Step 2
- If exit code 1: Show user the install instructions from stderr, then abort

**Example:**
```bash
cd skills/insights
./scripts/check-deps.sh
```

### Step 2: Detect CLI Type

**Run:** `scripts/detect-cli.sh`

**Purpose:** Auto-detect which AI coding CLI the user is running.

**Output:** Single line: `claude-code`, `opencode`, `codex`, or `unknown`

**Action:**
- Capture the output as `$CLI_TYPE`
- If output is `unknown`: Ask user which CLI they're using, or abort
- Otherwise: Continue to Step 3

**Example:**
```bash
CLI_TYPE=$(./scripts/detect-cli.sh)
echo "Detected CLI: $CLI_TYPE"
```

**Override:** User can specify CLI manually:
```bash
CLI_TYPE=$(./scripts/detect-cli.sh --cli claude-code)
```

### Step 3: Collect Session Metadata

**Run:** `scripts/collect-sessions.sh --cli $CLI_TYPE`

**Purpose:** Collect session metadata from the CLI's storage directory.

**Output:** JSON array of session objects (stdout)

**Action:**
- Capture output as `$SESSIONS_JSON`
- Verify it's valid JSON: `echo "$SESSIONS_JSON" | jq . > /dev/null`
- If empty array `[]`: Inform user no sessions found, abort
- Otherwise: Continue to Step 4

**Example:**
```bash
SESSIONS_JSON=$(./scripts/collect-sessions.sh --cli "$CLI_TYPE" --days 30)
echo "$SESSIONS_JSON" | jq 'length'  # Show session count
```

**Options:**
- `--limit N`: Limit to N most recent sessions (default: unlimited, filtered by --days)
- `--days N`: Only include sessions from the last N days (default: 30)
- `--session-dir <path>`: Override default session directory

### Step 4: Aggregate Statistics

**Run:** `scripts/aggregate-stats.sh` (reads from stdin)

**Purpose:** Compute quantitative statistics from session metadata.

**Input:** Session metadata JSON array (from Step 3)

**Output:** Aggregated stats JSON object (stdout)

**Action:**
- Pipe `$SESSIONS_JSON` to aggregate-stats.sh
- Capture output as `$STATS_JSON`
- Verify valid JSON
- Continue to Step 5

**Example:**
```bash
STATS_JSON=$(echo "$SESSIONS_JSON" | ./scripts/aggregate-stats.sh)
echo "$STATS_JSON" | jq '.total_sessions, .total_messages'
```

**Stats included:**
- total_sessions, total_messages, total_duration_hours
- date_range (start, end)
- tool_counts, languages, projects
- git_commits, git_pushes
- days_active, messages_per_day
- message_hours (24-element array)

### Step 5: Extract Session Facets (Optional but Recommended)

**Purpose:** Extract qualitative facets from individual sessions for richer analysis.

**Limit:** Up to 20 sessions (to manage token cost)

**Prompt:** Use the facet extraction prompt from `references/facet-extraction.md`

**Action:**
1. Select up to 20 sessions from `$SESSIONS_JSON` (prioritize recent, diverse sessions)
2. For each session:
   - Read the full session data (messages, tool calls, outcomes)
   - Execute the facet extraction prompt with session context
   - Parse the JSON response
3. Aggregate facets into `$FACETS_JSON`

**Facet fields:**
- goal_categories (debugging, feature_implementation, refactoring, etc.)
- user_satisfaction_counts (happy, satisfied, frustrated, etc.)
- friction_counts (misunderstood_request, buggy_code, etc.)
- outcome_level (success, partial_success, blocked, abandoned)

**Cache:** Store extracted facets in `~/.agent-insights/cache/facets/<session-id>.json` to avoid re-extraction.

**Example:**
```bash
# Pseudo-code (agent executes this logic)
for session in (first 20 sessions):
  cache_file="~/.agent-insights/cache/facets/${session.session_id}.json"
  if cache_file exists:
    facet = read cache_file
  else:
    facet = execute_facet_extraction_prompt(session)
    write facet to cache_file
  facets.append(facet)
```

### Step 6: Run 8 Analysis Prompts

**Purpose:** Generate qualitative insights across 8 categories.

**Prompts:** All 8 prompts are in `references/analysis-prompts.md`

**Context:** Provide each prompt with:
- `$STATS_JSON` (aggregated statistics)
- `$FACETS_JSON` (extracted facets, if available)
- `$CLI_TYPE` (for CLI-specific suggestions)

**Prompts to execute:**
1. **project_areas** - What the user works on (4-5 areas)
2. **interaction_style** - How the user interacts (narrative + key_pattern)
3. **what_works** - Impressive workflows (3 items)
4. **friction_analysis** - Pain points (3 categories × 2 examples)
5. **suggestions** - CLI-agnostic + CLI-specific features (use `references/suggestions-by-cli.md`)
6. **on_the_horizon** - Future opportunities (3 items with copyable_prompt)
7. **fun_ending** - Memorable moment (headline + detail)
8. **at_a_glance** - Executive summary (4 fields: whats_working, whats_hindering, quick_wins, ambitious_workflows)

**Execution:**
- Run all 8 prompts **in parallel** if possible (faster)
- Each prompt returns a JSON object
- Combine all 8 responses into `$INSIGHTS_JSON`

**Example:**
```json
{
  "project_areas": {...},
  "interaction_style": {...},
  "what_works": {...},
  "friction_analysis": {...},
  "suggestions": {...},
  "on_the_horizon": {...},
  "fun_ending": {...},
  "at_a_glance": {...}
}
```

**Important:** Each prompt includes "RESPOND WITH ONLY A VALID JSON OBJECT" instruction. Parse responses carefully.

### Step 7: Generate HTML Report

**Run:** `scripts/generate-report.sh --stats <stats-file> --cli $CLI_TYPE --output <path>`

**Purpose:** Inject JSON data into HTML template and create final report.

**Input:**
- `$INSIGHTS_JSON` (from Step 6, via stdin)
- `$STATS_JSON` (from Step 4, via --stats file)
- `$CLI_TYPE` (via --cli flag)

**Output:** Path to generated HTML file (stdout)

**Action:**
1. Write `$STATS_JSON` to a temp file
2. Pipe `$INSIGHTS_JSON` to generate-report.sh
3. Capture output path as `$REPORT_PATH`
4. Continue to Step 8

**Example:**
```bash
STATS_FILE=$(mktemp)
echo "$STATS_JSON" > "$STATS_FILE"

REPORT_PATH=$(echo "$INSIGHTS_JSON" | ./scripts/generate-report.sh \
  --stats "$STATS_FILE" \
  --cli "$CLI_TYPE" \
  --language "${LANGUAGE:-en}" \
  --output ~/.agent-insights/reports/report-$(date +%Y-%m-%d).html)

echo "Report generated: $REPORT_PATH"
```

**Default output:** `./insights-report.html`

**Recommended output:** `~/.agent-insights/reports/report-YYYY-MM-DD.html`

### Step 8: Present to User

**Purpose:** Show summary and provide file:// URL.

**Action:**
1. Read key stats from `$STATS_JSON`:
   - total_sessions
   - total_messages
   - total_duration_hours
   - date_range
2. Read at-a-glance summary from `$INSIGHTS_JSON`
3. Present to user:

**Example output:**
```
✅ Insights Report Generated

📊 Summary:
- Sessions analyzed: 42
- Total messages: 1,247
- Time period: 2026-01-15 to 2026-02-06
- Total duration: 18.5 hours

🎯 At a Glance:
- What's working: You're effectively using Claude for rapid prototyping...
- What's hindering: Frequent context resets when switching between projects...
- Quick wins: Try using /compact to reduce token usage...
- Ambitious workflows: Explore multi-file refactoring with LSP tools...

📄 Full report: file://$REPORT_PATH

Open the report in your browser to see detailed insights across 8 categories.
```

## Output Format

The generated HTML report includes:

**Header:**
- Title: "Insights Report"
- CLI type badge
- Generation date
- Stats bar (sessions · messages · hours · commits)

**8 Sections:**
1. **At a Glance** - 4-item executive summary
2. **What You Work On** - Project areas with session counts
3. **Your Style** - Interaction style narrative
4. **What's Working Well** - Impressive workflows
5. **Friction Points** - Categorized pain points
6. **Suggestions** - Features and usage patterns to try
7. **On the Horizon** - Future opportunities with copyable prompts
8. **Fun Moment** - Memorable headline

**Features:**
- Self-contained (no external resources)
- Dark/light theme support (auto-detects via `prefers-color-scheme`)
- Responsive design (mobile-friendly)
- Print-friendly styles

## Reference Files

All supporting documentation is in `references/`:

- **analysis-prompts.md** - Complete text of all 8 analysis prompts with expected JSON schemas
- **facet-extraction.md** - Session facet extraction prompt and enums
- **schema.md** - JSON schemas for session metadata, stats, facets, and insights
- **cli-formats.md** - Detailed documentation of session storage formats for each CLI
- **suggestions-by-cli.md** - CLI-specific feature suggestions (MCP servers, custom skills, hooks, etc.)

## Troubleshooting

### "jq: command not found"

**Solution:** Install jq:
- macOS: `brew install jq`
- Linux: `apt install jq` or `yum install jq`

### "Bash version too old"

**Solution:** Upgrade to bash 4+:
- macOS: `brew install bash` (then restart terminal)
- Linux: Usually already 4+

### "No sessions found"

**Possible causes:**
1. CLI not detected correctly
   - Run: `./scripts/detect-cli.sh`
   - Override: `./scripts/detect-cli.sh --cli claude-code`
2. Session directory empty
   - Check: `ls ~/.claude/projects/` (Claude Code)
   - Check: `ls ~/.local/share/opencode/storage/session/` (OpenCode)
   - Check: `ls ~/.codex/sessions/` (Codex)
3. Sessions filtered out (<2 messages, <1 minute)
   - Review filtering logic in `scripts/collect-sessions.sh`

### "Report generation fails"

**Possible causes:**
1. Invalid JSON from analysis prompts
   - Verify: `echo "$INSIGHTS_JSON" | jq .`
   - Check: Each prompt response is valid JSON
2. Missing template file
   - Verify: `ls scripts/templates/report.html`
3. Python not available
   - generate-report.sh uses Python for JSON injection
   - Verify: `python3 --version`

### "Analysis prompts return non-JSON"

**Solution:** Ensure each prompt includes "RESPOND WITH ONLY A VALID JSON OBJECT" instruction. If the model returns markdown code blocks, strip them:

```bash
response=$(echo "$response" | sed 's/^```json//; s/^```//; s/```$//')
```

## Examples

### Basic Usage

```bash
cd skills/insights

# 1. Check dependencies
./scripts/check-deps.sh || exit 1

# 2. Detect CLI
CLI_TYPE=$(./scripts/detect-cli.sh)

# 3. Collect sessions
SESSIONS=$(./scripts/collect-sessions.sh --cli "$CLI_TYPE" --days 30)

# 4. Aggregate stats
STATS=$(echo "$SESSIONS" | ./scripts/aggregate-stats.sh)

# 5. Extract facets (agent logic, not shown)

# 6. Run analysis prompts (agent logic, not shown)

# 7. Generate report
STATS_FILE=$(mktemp)
echo "$STATS" > "$STATS_FILE"
REPORT=$(echo "$INSIGHTS" | ./scripts/generate-report.sh --stats "$STATS_FILE" --cli "$CLI_TYPE")

# 8. Present
echo "Report: file://$REPORT"
```

### Override CLI Detection

```bash
# Force Claude Code
CLI_TYPE=$(./scripts/detect-cli.sh --cli claude-code)
```

### Limit Sessions

```bash
# Analyze only last 10 sessions
SESSIONS=$(./scripts/collect-sessions.sh --cli "$CLI_TYPE" --limit 10)
```

### Custom Output Path

```bash
# Save to specific location
mkdir -p ~/reports
REPORT=$(echo "$INSIGHTS" | ./scripts/generate-report.sh \
  --stats stats.json \
  --cli claude-code \
  --output ~/reports/insights-$(date +%Y%m%d).html)
```

## Notes

- **Token cost:** Facet extraction (Step 5) and analysis prompts (Step 6) consume tokens. Limit facet extraction to 20 sessions.
- **Caching:** Cache extracted facets in `~/.agent-insights/cache/facets/` to avoid re-extraction on subsequent runs.
- **Parallelization:** Run the 8 analysis prompts in parallel for faster execution.
- **Privacy:** All data stays local. No external API calls. Report is self-contained HTML.
- **Extensibility:** To add a new CLI, create an adapter in `collect-sessions.sh` following the existing pattern.

## Language Support

The insights skill supports multi-language report generation.

### Supported Languages
- **Built-in**: English (`en`), Korean (`ko`)
- **Dynamic**: Any language via AI translation

### How to Specify Language
1. **CLI flag**: `--language <code>` (e.g., `--language ko`)
2. **Environment variable**: `LANG` or `LC_ALL` (e.g., `LANG=ko_KR.UTF-8`)
3. **Default**: English (`en`)

### What Gets Translated
- **HTML report UI strings**: Section titles, labels (26 strings)
- **Analysis content**: Insights JSON values (via prompt instruction)

### What Stays in English
- **JSON keys**: Always English for consistency
- **Shell script output**: Help messages, errors

## Version

This skill targets:
- Claude Code 2.1+
- OpenCode 1.1+
- Codex (latest)

For older versions, session formats may differ. Check `references/cli-formats.md` for compatibility notes.
