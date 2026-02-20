---
name: ai-coding-agents
description: Comprehensive guide for using Codex CLI (OpenAI) and Claude Code CLI (Anthropic) - AI-powered coding agents. Use when orchestrating CLI commands, automating tasks, configuring agents, or troubleshooting issues.
---

# AI Coding Agents Skill

Expert knowledge for Codex CLI and Claude Code CLI — the two leading AI coding agents.

**Note:** This skill documents both tools for reference. VMark development primarily uses **Claude Code CLI**. The Codex CLI sections are retained for completeness and cross-tool workflows.

## When to Use

- Orchestrating complex coding tasks via CLI
- Configuring MCP servers for either tool
- Setting up automation pipelines (CI/CD)
- Troubleshooting authentication or sandbox issues
- Comparing capabilities between agents
- Custom agent/subagent configuration

## Quick Reference

### Starting Sessions

| Task | Codex CLI | Claude Code CLI |
|------|-----------|-----------------|
| Interactive session | `codex` | `claude` |
| With prompt | `codex "fix the bug"` | `claude "fix the bug"` |
| Non-interactive | `codex exec "task"` | `claude -p "task"` |
| Resume last | `codex resume --last` | `claude -c` |
| Resume by ID | `codex resume <id>` | `claude -r <id>` |

### Safety Modes

| Mode | Codex CLI | Claude Code CLI |
|------|-----------|-----------------|
| Read-only | `-s read-only` | `--permission-mode plan` |
| Workspace write | `-s workspace-write` | (default) |
| Full access | `-s danger-full-access` | `--dangerously-skip-permissions` |
| Auto mode | `--full-auto` | `--permission-mode default` |
| YOLO mode | `--yolo` | `--dangerously-skip-permissions` |

### Model Selection

| Task | Codex CLI | Claude Code CLI |
|------|-----------|-----------------|
| Select model | `-m gpt-5-codex` | `--model opus` |
| Use local OSS | `--oss` | N/A |
| Fallback model | N/A | `--fallback-model sonnet` |

---

## Codex CLI (OpenAI)

### Installation
```bash
npm i -g @openai/codex
# or
brew install --cask codex
```

### Authentication
```bash
codex login              # OAuth via ChatGPT
codex login --with-api-key   # Read API key from stdin
codex login status       # Check auth status
codex logout             # Remove credentials
```

### Core Commands

#### `codex` - Interactive Mode
```bash
codex                           # Start TUI
codex "fix all TypeScript errors"  # With initial prompt
codex -i screenshot.png "explain"  # With image
codex --full-auto "refactor"    # Low-friction mode
codex --search "find docs"      # Enable web search
```

#### `codex exec` - Non-Interactive
```bash
codex exec "write tests"        # Run and exit
codex e "task"                  # Short alias
echo "task" | codex exec -      # From stdin
codex exec --json "task"        # JSONL output
codex exec -o result.txt "task" # Save to file
codex exec --output-schema schema.json "task"  # Validate output
```

#### `codex resume` - Continue Sessions
```bash
codex resume                    # Interactive picker
codex resume --last             # Most recent
codex resume --all              # Show all (any directory)
codex resume <session-id>       # Specific session
codex resume <id> "continue with this"  # With prompt
```

#### `codex review` - Code Review
```bash
codex review                    # Review current branch vs main
codex review --uncommitted      # Review uncommitted changes
codex review --base develop     # Against specific branch
codex review --commit abc123    # Review specific commit
codex review "focus on security"  # Custom instructions
```

#### `codex apply` - Apply Cloud Task
```bash
codex apply <task-id>           # Apply diff from cloud task
```

#### `codex cloud` - Cloud Tasks (Experimental)
```bash
codex cloud                     # Browse cloud tasks
codex cloud exec "task" --env <env-id>  # Submit task
codex cloud status <task-id>    # Check status
codex cloud diff <task-id>      # Show diff
codex cloud apply <task-id>     # Apply changes
```

#### `codex mcp` - MCP Server Management
```bash
codex mcp list                  # List servers
codex mcp list --json           # JSON output
codex mcp get <name>            # Server details
codex mcp add <name> -- npx my-server   # Add stdio server
codex mcp add <name> --url https://... # Add HTTP server
codex mcp add <name> --env API_KEY=xxx -- cmd  # With env vars
codex mcp remove <name>         # Remove server
codex mcp login <name> --scopes read,write  # OAuth for HTTP
codex mcp logout <name>         # Remove OAuth
```

#### `codex sandbox` - Run Sandboxed Commands
```bash
# macOS
codex sandbox macos -- npm test
codex sandbox seatbelt --full-auto -- ./script.sh

# Linux
codex sandbox linux -- npm test
codex sandbox landlock -- ./script.sh
```

#### `codex completion` - Shell Completions
```bash
codex completion bash >> ~/.bashrc
codex completion zsh >> ~/.zshrc
codex completion fish > ~/.config/fish/completions/codex.fish
```

### Slash Commands (Interactive)

| Command | Purpose |
|---------|---------|
| `/model` | Switch model (gpt-5-codex, gpt-5, etc.) |
| `/approvals` | Change approval policy |
| `/compact` | Summarize conversation, free context |
| `/diff` | Show git diff |
| `/review` | Analyze working tree |
| `/status` | Show config and token usage |
| `/mcp` | List available MCP tools |
| `/mention` | Attach files |
| `/fork` | Branch conversation |
| `/resume` | Reopen previous session |
| `/new` | Fresh conversation |
| `/init` | Create AGENTS.md scaffold |
| `/feedback` | Submit logs/diagnostics |
| `/quit`, `/exit` | Exit CLI |

### Configuration (`~/.codex/config.toml`)
```toml
model = "gpt-5-codex"
approval_policy = "on-request"

[sandbox]
mode = "workspace-write"

[features]
web_search = true

[profiles.ci]
model = "gpt-4.1"
approval_policy = "never"
```

### Global Flags
```
-m, --model <MODEL>          Model selection
-s, --sandbox <MODE>         read-only|workspace-write|danger-full-access
-a, --ask-for-approval <P>   untrusted|on-failure|on-request|never
-c, --config <KEY=VALUE>     Override config
-C, --cd <DIR>               Working directory
-i, --image <FILE>           Attach image(s)
-p, --profile <NAME>         Config profile
--full-auto                  Low-friction mode
--yolo                       Bypass all safety (DANGEROUS)
--search                     Enable web search
--add-dir <DIR>              Grant additional write access
--enable <FEATURE>           Enable feature flag
--disable <FEATURE>          Disable feature flag
--oss                        Use local OSS model
```

---

## Claude Code CLI (Anthropic)

### Installation
```bash
npm install -g @anthropic-ai/claude-code
```

### Authentication
```bash
claude                      # First run prompts login
claude setup-token          # Set up long-lived token
# Requires Claude Pro/Max subscription OR API key
```

### Core Commands

#### `claude` - Interactive Mode
```bash
claude                          # Start REPL
claude "explain this project"   # With prompt
claude -c                       # Continue last conversation
claude -r "session-name"        # Resume by name/ID
claude --model opus             # Select model
claude --chrome                 # Enable Chrome integration
claude --ide                    # Auto-connect to IDE
```

#### `claude -p` - Print Mode (Non-Interactive)
```bash
claude -p "explain this function"   # Query and exit
cat file | claude -p "explain"      # Process piped input
claude -p --output-format json "q"  # JSON output
claude -p --output-format stream-json "q"  # Streaming JSON
claude -p --max-turns 3 "task"      # Limit agent turns
claude -p --max-budget-usd 5 "task" # Spending limit
claude -p --json-schema '{...}' "q" # Validate output schema
```

#### `claude mcp` - MCP Server Management
```bash
claude mcp list                 # List servers
claude mcp get <name>           # Server details
claude mcp add <name> <cmd>     # Add stdio server
claude mcp add -t http <name> <url>  # Add HTTP server
claude mcp add -e KEY=val <name> -- cmd  # With env vars
claude mcp add -H "Auth: Bearer x" <name> <url>  # With headers
claude mcp add -s project <name> <cmd>  # Project scope
claude mcp remove <name>        # Remove server
claude mcp serve                # Run as MCP server
claude mcp add-from-claude-desktop   # Import from desktop app
claude mcp reset-project-choices     # Reset approvals
```

#### `claude plugin` - Plugin Management
```bash
claude plugin list              # List plugins
claude plugin install <name>    # Install plugin
claude plugin install <name>@marketplace  # From specific marketplace
claude plugin uninstall <name>  # Remove plugin
claude plugin enable <name>     # Enable disabled plugin
claude plugin disable <name>    # Disable plugin
claude plugin update <name>     # Update plugin
claude plugin validate <path>   # Validate manifest
claude plugin marketplace       # Manage marketplaces
```

#### `claude update` - Self-Update
```bash
claude update                   # Check and install updates
```

#### `claude doctor` - Diagnostics
```bash
claude doctor                   # Check health/issues
```

#### `claude install` - Native Build
```bash
claude install                  # Install native build
claude install stable           # Specific version
claude install latest           # Latest version
```

### Slash Commands (Interactive)

| Command | Purpose |
|---------|---------|
| `/init` | Generate CLAUDE.md |
| `/clear` | Reset context |
| `/compact` | Summarize conversation |
| `/bug` | Report issues |
| `/doctor` | Run diagnostics |
| `/model` | Switch model |
| `/config` | View/edit settings |
| `/permissions` | Manage permissions |
| `/memory` | View/edit memory |
| `/project:<cmd>` | Project-specific commands |
| `/user:<cmd>` | User-specific commands |

### Custom Commands

Create `.claude/commands/fix-issue.md`:
```markdown
Fix GitHub issue #$ARGUMENTS

1. Read the issue details
2. Identify the problem
3. Implement the fix
4. Write tests
5. Create a commit
```

Usage: `/project:fix-issue 1234`

### Configuration

**User settings** (`~/.claude/settings.json`):
```json
{
  "model": "claude-sonnet-4-5-20250929",
  "verbose": false,
  "theme": "dark"
}
```

**Project settings** (`.claude/settings.json`):
```json
{
  "allowedTools": ["Bash(git:*)", "Read", "Edit"],
  "disallowedTools": ["Bash(rm:*)"]
}
```

### CLI Flags

#### Core
```
-p, --print                 Non-interactive mode
-c, --continue              Continue last conversation
-r, --resume <ID>           Resume specific session
-v, --version               Show version
```

#### Model & Config
```
--model <MODEL>             sonnet|opus|haiku or full name
--fallback-model <MODEL>    Fallback when overloaded
--settings <FILE>           Load settings JSON
--setting-sources <LIST>    user,project,local
--session-id <UUID>         Use specific session ID
```

#### System Prompt
```
--system-prompt <TEXT>      Replace default prompt
--append-system-prompt <T>  Append to default
--system-prompt-file <F>    Replace with file (print only)
--append-system-prompt-file Replace with file (print only)
```

#### Agent & Tools
```
--agent <NAME>              Specify agent
--agents <JSON>             Define custom subagents
--tools <LIST>              Restrict built-in tools
--allowedTools <LIST>       Auto-approve tools
--disallowedTools <LIST>    Remove tools from context
```

#### Permissions
```
--permission-mode <MODE>    acceptEdits|bypassPermissions|default|delegate|dontAsk|plan
--dangerously-skip-permissions  Skip all prompts (DANGEROUS)
--allow-dangerously-skip-permissions  Enable bypass option
```

#### Output
```
--output-format <FMT>       text|json|stream-json
--input-format <FMT>        text|stream-json
--include-partial-messages  Include streaming chunks
--verbose                   Verbose logging
--debug [FILTER]            Debug mode with filtering
```

#### Advanced
```
--max-turns <N>             Limit agent turns (print only)
--max-budget-usd <AMT>      Spending limit (print only)
--json-schema <SCHEMA>      Validate JSON output
--chrome / --no-chrome      Chrome integration
--ide                       IDE auto-connect
--fork-session              Create new session on resume
--no-session-persistence    Don't save session
--add-dir <DIRS>            Additional directories
--plugin-dir <DIRS>         Load plugins
--disable-slash-commands    Disable all skills
--mcp-config <FILES>        MCP server configs
--strict-mcp-config         Only use specified MCP
--betas <HEADERS>           Beta API headers
```

### Custom Subagents

```bash
claude --agents '{
  "reviewer": {
    "description": "Code reviewer. Use after changes.",
    "prompt": "You are a senior code reviewer...",
    "tools": ["Read", "Grep", "Glob"],
    "model": "sonnet"
  }
}'
```

---

## Common Patterns & Edge Cases

### CI/CD Integration

**Codex in GitHub Actions:**
```yaml
- name: Run Codex
  run: |
    echo "${{ secrets.OPENAI_API_KEY }}" | codex login --with-api-key
    codex exec --json -o result.txt "fix linting errors"
```

**Claude in CI:**
```yaml
- name: Run Claude
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  run: |
    claude -p --output-format json "review this PR" > review.json
```

### Handling Rate Limits

**Codex:** Automatic backoff built-in.

**Claude:** Use `--fallback-model`:
```bash
claude -p --fallback-model haiku "quick task"
```

### Working with Large Codebases

```bash
# Codex: Use /compact to free context
# In session: /compact

# Claude: Use /compact or start fresh
claude --no-session-persistence -p "analyze src/"
```

### Multi-Directory Access

```bash
# Codex
codex --add-dir ../shared-lib --add-dir ../config

# Claude
claude --add-dir ../shared-lib ../config
```

### Structured Output

**Codex:**
```bash
codex exec --output-schema schema.json "generate API spec"
```

**Claude:**
```bash
claude -p --json-schema '{"type":"object","properties":{"name":{"type":"string"}}}' "extract data"
```

### Image Input

**Codex:**
```bash
codex -i screenshot.png "explain this UI"
codex -i img1.png -i img2.png "compare these"
```

**Claude:**
```bash
# Via file reference in prompt
claude "analyze the image at ./screenshot.png"
```

### Session Forking

```bash
# Codex: /fork in session

# Claude
claude -r "session-id" --fork-session "try alternative approach"
```

### MCP Server Debugging

**Codex:**
```bash
codex mcp list --json | jq .
```

**Claude:**
```bash
claude --debug "mcp" --mcp-config ./mcp.json
```

---

## Troubleshooting

### Authentication Issues

| Problem | Codex | Claude |
|---------|-------|--------|
| Not logged in | `codex login status` | `claude doctor` |
| Token expired | `codex logout && codex login` | `claude setup-token` |
| API key issues | Check `OPENAI_API_KEY` | Check `ANTHROPIC_API_KEY` |

### Sandbox Issues

| Problem | Solution |
|---------|----------|
| Permission denied | Use `--add-dir` for specific directories |
| Can't run commands | Check sandbox mode, use `workspace-write` |
| Network blocked | Sandbox may block network; use `danger-full-access` carefully |

### MCP Server Issues

| Problem | Solution |
|---------|----------|
| Server not found | Check `mcp list`, verify installation |
| Connection failed | Check server logs, verify URL/command |
| Auth required | Use `mcp login` (Codex) or add headers (Claude) |

### Performance Issues

| Problem | Solution |
|---------|----------|
| Slow responses | Use lighter model (gpt-4.1-mini / haiku) |
| Context overflow | Use `/compact` to summarize |
| High costs | Set `--max-budget-usd` (Claude) |

---

## Best Practices

1. **Start with read-only** for exploration, escalate as needed
2. **Use sessions** - resume work instead of starting fresh
3. **Create AGENTS.md/CLAUDE.md** for project-specific instructions
4. **Leverage MCP servers** for external integrations
5. **Use structured output** in CI/CD for parsing
6. **Set spending limits** with `--max-budget-usd`
7. **Review diffs** before applying (`/diff`, `codex cloud diff`)
8. **Commit checkpoints** before major changes
