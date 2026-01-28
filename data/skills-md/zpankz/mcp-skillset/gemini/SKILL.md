---
name: gemini
description: |
  Execute Google Gemini CLI for large-context code analysis, multimodal reasoning, and repository-scale reviews.
  Also use for delegating tasks requiring 1M token context windows or Gemini-specific capabilities.
tools:
  - Bash
  - Read
  - Grep
  - Glob
  - WebFetch
disallowedTools:
  - Write
  - Edit
  - TodoWrite
context: fork
model: opus
---

# Gemini Skill Guide

## When to Use This Skill

**Primary Use Cases**:

1. User explicitly requests `gemini` CLI execution (Mode 1: Direct CLI)
2. Large-context analysis requiring 1M token window (Mode 2: Gemini Delegation)
3. Repository-scale code reviews and architectural analysis
4. Multimodal analysis (code + images/diagrams)
5. Cross-module dependency tracking

**Do NOT use for**:

- Simple code explanations (use Claude directly)
- Small context tasks (<100K tokens)
- Tasks not requiring Gemini-specific capabilities

## Execution Modes

### Mode 1: Direct CLI Execution

**When**: User explicitly asks to run gemini CLI

**Workflow**:

1. Gather configuration using structured questions:
   - Model selection (gemini-3-pro-preview vs gemini-3-flash-preview)
   - Approval mode (default, auto_edit, yolo)
   - Output format (text, json, stream-json)

2. Execute:
   ```bash
   gemini "<PROMPT>" -m <MODEL> --approval-mode <MODE> --output-format <FORMAT>
   ```

3. Inform user: "You can resume with 'gemini --resume latest' anytime"

**Resuming**:
```bash
gemini "<CONTINUATION PROMPT>" --resume latest
```

### Mode 2: Gemini Delegation for Large Context

**When**: Task requires large context window (>100K tokens), multimodal input,
or repository-scale analysis

**Workflow**:

1. Analyze context and identify what Gemini analysis would help
2. Formulate comprehensive query with all relevant context:
   - Problem statement
   - Current findings
   - Code snippets or file references
   - Specific questions
3. Leverage Gemini's 1M token context for comprehensive analysis
4. Execute: `gemini "<DETAILED CONTEXT>" --output-format json`
5. Synthesize Gemini response into actionable insights
6. Report findings with:
   - Clear summary of Gemini's analysis
   - Specific recommendations or solutions
   - Additional considerations or caveats
   - Next steps if applicable

### Error Handling

- Verify gemini binary exists before execution: `which gemini`
- Stop immediately on non-zero exit codes and report to user
- Request direction before retrying failed commands
- Before using high-autonomy flags, confirm with user:
  - `--yolo` (auto-approve all actions)
  - `--approval-mode yolo`

### Context Management

- Gemini excels at large context (up to 1M tokens)
- For massive contexts (>500K tokens), consider module-by-module summaries
- Use `--include-directories` to add additional workspace paths
- Leverage session resume for iterative refinement

## Configuration Gathering Patterns

### Initial Configuration (Mode 1, Step 1)

At the start of Mode 1 execution, gather model, approval mode, and output format:

**Standard configuration question:**

```text
Select gemini configuration (model, approval mode, and output format):

1. "gemini-3-pro-preview / default / json (Recommended)" - High quality, safe mode
2. "gemini-3-pro-preview / auto_edit / json" - High quality, auto-approve edits
3. "gemini-3-flash-preview / default / json" - Fast, safe mode
4. "gemini-3-flash-preview / auto_edit / json" - Fast, auto-approve edits
5. "gemini-3-pro-preview / yolo / json" - High quality, fully autonomous
6. "gemini-3-flash-preview / yolo / json" - Fast, fully autonomous
7. "Custom" - User will specify model, approval, and format separately
```

### High-Impact Flags Confirmation

Before executing with --yolo or autonomous flags:

```text
Ready to execute with these flags: [LIST FLAGS]. Proceed?

1. "Execute now" - Run as configured
2. "Modify configuration" - Change settings
3. "Cancel" - Abort
```

### Post-Execution Follow-up

After gemini command completes:

```text
Gemini completed. [SUMMARY]. Next steps?

1. "Resume with additional prompt" - Continue session
2. "Analyze results" - Review output
3. "Complete" - Finished
4. "Retry with different config" - Adjust settings
```

### Error Recovery

When command fails or has warnings:

```text
Error: [SPECIFIC ERROR]. How to proceed?

1. "Resume with adjustments" - Fix and continue
2. "Retry with different config" - Change model/approval/format
3. "Accept partial results" - Use what worked
4. "Invoke heal-skill" - Fix outdated SKILL.md
```

## Running a Task

1. Gather configuration using the patterns above
2. Assemble the command with the appropriate options:
   - `-m, --model <MODEL>` (gemini-3-pro-preview or gemini-3-flash-preview)
   - `--approval-mode <MODE>` (default, auto_edit, yolo)
   - `-o, --output-format <FORMAT>` (text, json, stream-json)
   - `--include-directories <DIRS>` (additional workspace paths)
   - `-r, --resume <SESSION>` (latest or session index)
3. Run the command, capture output, and summarize for the user
4. **After Gemini completes**, inform the user: "You can resume this Gemini
   session at any time by saying 'gemini resume' or asking me to continue."

### Quick Reference

| Use case | Approval mode | Key flags |
| --- | --- | --- |
| Safe analysis | `default` | `--approval-mode default --output-format json` |
| Auto-approve edits | `auto_edit` | `--approval-mode auto_edit --output-format json` |
| Fully autonomous | `yolo` | `--yolo --output-format json` |
| Resume recent session | Inherited | `--resume latest` |
| Add workspace directories | Match task | `--include-directories <DIRS>` |
| Interactive continuation | default | `-i "<PROMPT>"` (stays interactive after) |

## Model Selection

| Model | Use Case | Context | Speed |
|-------|----------|---------|-------|
| `gemini-3-pro-preview` | Complex reasoning, architecture review | 1M tokens | Slower |
| `gemini-3-flash-preview` | Quick analysis, simple tasks | 1M tokens | Faster |

## Session Management

```bash
# List available sessions
gemini --list-sessions

# Resume most recent session
gemini --resume latest

# Resume specific session by index
gemini --resume 5

# Delete a session
gemini --delete-session 3
```

## MCP Server Integration

```bash
# List configured MCP servers
gemini mcp list

# Add an MCP server
gemini mcp add <name> <command> [args...]

# Remove an MCP server
gemini mcp remove <name>

# Limit to specific MCP servers
gemini "<PROMPT>" --allowed-mcp-server-names mcp-skillset
```

## Extension System

```bash
# List installed extensions
gemini extensions list

# Install extension from git or path
gemini extensions install <source> [--auto-update] [--pre-release]

# Update extensions
gemini extensions update [--all]

# Disable/enable extension
gemini extensions disable <name>
gemini extensions enable <name>
```

## Following Up

- After every `gemini` command, offer follow-up options
- When resuming, use: `gemini "<new prompt>" --resume latest`
- The resumed session automatically uses the same context from the original
- Restate the chosen model and approval mode when proposing follow-up actions

## Error Handling Guidelines

- Stop and report failures whenever `gemini --version` or a `gemini` command
  exits non-zero; request direction before retrying
- Confirm high-impact flags before execution
- When output includes warnings or partial results, offer error recovery options

## Comparison with Codex Skill

| Feature | Gemini | Codex |
|---------|--------|-------|
| Context window | 1M tokens | ~200K tokens |
| Primary models | gemini-3-pro/flash | gpt-5.2-codex |
| Approval modes | default/auto_edit/yolo | never/on-request/on-failure |
| Sandbox | Boolean (--sandbox) | read-only/workspace-write/danger-full-access |
| Resume | --resume latest/index | codex exec resume --last |
| Stderr handling | N/A | 2>/dev/null for thinking tokens |
| Output format | text/json/stream-json | json flag |

## Integration Patterns

### With Other CLI Agents

```bash
# Use gemini for large context, codex for GPT-specific
gemini "Analyze entire codebase architecture" --output-format json
codex exec "Implement specific feature based on analysis" --full-auto

# Chain with research CLI
research docs -t "framework API" --format json | gemini "Apply this to codebase"
```

### Multimodal Analysis

```bash
# Gemini can process images inline with code
gemini "Analyze this architecture diagram and compare with implementation" \
  --include-directories ./docs ./src
```

## Heal-Skill Integration

When gemini CLI API changes are detected (command failures, unexpected output formats, or deprecated flags):

1. **Detection**: Notice command failures or API mismatches during execution
2. **Trigger**: Flag skill for healing via `/heal-skill gemini`
3. **Analysis**: Healing agent analyzes current CLI with `gemini --help` and `gemini --version`
4. **Update**: Updates skill documentation to match current API
5. **Validation**: Re-validates agent configuration for compatibility
6. **Model Verification**: Ensures only gemini-3 models are referenced
7. **Context Window Verification**: Confirms 1M token context window specifications

**Common Changes to Monitor**:
- New or deprecated command flags
- Changes to approval modes or output formats
- Model availability updates (gemini-3 family)
- MCP server integration API changes
- Session management API modifications
- Extension system updates
- Context window specification changes
