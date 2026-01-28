---
name: ai-code-reviewer
description: Automated AI-powered code review that runs on git hooks with progressive disclosure design. Use when setting up automated code review for a project, installing git hooks for code review, creating or modifying review rules, or configuring review behavior. Triggers on requests like "set up AI code review", "install review hooks", "create review rules", or "configure code reviewer".
---

# AI Code Reviewer

Automated AI-powered code review that runs on git hooks with progressive disclosure design. Reviews staged changes against project-specific rules using Claude AI, blocking or warning about violations before commits.

## Key Features

- **Progressive Disclosure**: Loads rule metadata first for fast matching, full details only for applicable rules
- **Git Hook Integration**: Automatically runs on pre-commit or pre-push
- **Project-Level Rules**: Each project maintains its own review rules in `.ai-reviewer/rules/`
- **Smart Matching**: Matches rules by keywords and file patterns before full AI review
- **Flexible Configuration**: Block/warn modes, Claude API or CLI backend
- **Token Efficient**: Minimizes context usage by loading only relevant rules

## Quick Start

1. **Initialize project structure** (if not exists):
   ```bash
   mkdir -p .ai-reviewer/{rules,hooks}
   cp <skill-path>/assets/config.yaml .ai-reviewer/
   cp <skill-path>/assets/rules/*.md .ai-reviewer/rules/
   cp <skill-path>/assets/hooks/*.template .ai-reviewer/hooks/
   ```

2. **Install git hook**:
   ```bash
   python3 <skill-path>/scripts/install_hook.py install --hook-type pre-commit
   ```

3. **Configure AI backend** in `.ai-reviewer/config.yaml`:
   - Set `ai_backend: claude-api` and provide `claude_api_key`, OR
   - Set `ai_backend: claude-cli` (requires Claude CLI installed)

4. **Test the review**:
   ```bash
   # Stage some changes
   git add .

   # Run review manually to test
   python3 <skill-path>/scripts/run_review.py --project-root .

   # If review passes, commit will proceed normally
   git commit -m "test commit"
   ```

5. **Skip review** when needed:
   ```bash
   git commit --no-verify -m "message"
   ```

## Workflow Decision Tree

```
User wants to:
│
├─ "Set up AI code review"
│  └─ Go to Initial Setup
│
├─ "Add review rules"
│  └─ Go to Creating Rules
│
├─ "Configure review behavior"
│  └─ Go to Configuration
│
├─ "Install/uninstall hooks"
│  └─ Go to Managing Git Hooks
│
├─ "Debug review issues"
│  └─ Go to Troubleshooting
│
└─ "Review staged changes manually"
   └─ Run: python3 <skill-path>/scripts/run_review.py --project-root .
```

## Initial Setup

### Step 1: Create Project Structure

The reviewer requires this structure:

```
project-root/
└── .ai-reviewer/
    ├── config.yaml          # Configuration
    ├── rules/               # Review rules
    │   ├── rule1.md
    │   └── rule2.md
    └── hooks/               # Git hook templates
        ├── pre-commit.template
        └── pre-push.template
```

**Copy from skill assets:**
```bash
# Create directories
mkdir -p .ai-reviewer/{rules,hooks}

# Copy example config
cp <skill-path>/assets/config.yaml .ai-reviewer/

# Copy example rules
cp <skill-path>/assets/rules/*.md .ai-reviewer/rules/

# Copy hook templates
cp <skill-path>/assets/hooks/*.template .ai-reviewer/hooks/
```

### Step 2: Configure Reviewer

Edit `.ai-reviewer/config.yaml`:

**For Claude API** (recommended):
```yaml
review_mode: block
ai_backend: claude-api
claude_api_key: "sk-ant-api03-..."  # Or use ANTHROPIC_API_KEY env var
model: claude-sonnet-4-5-20250929
```

**For Claude CLI**:
```yaml
review_mode: block
ai_backend: claude-cli
```

See [Configuration Reference](#configuration-reference) for all options.

### Step 3: Install Git Hooks

```bash
python3 <skill-path>/scripts/install_hook.py install --hook-type pre-commit
```

Or for pre-push:
```bash
python3 <skill-path>/scripts/install_hook.py install --hook-type pre-push
```

### Step 4: Verify Installation

```bash
# Run manual review
python3 <skill-path>/scripts/run_review.py --project-root .

# If successful, try a commit
git add .
git commit -m "test commit"
```

## Creating Rules

### Rule File Format

Rules are Markdown files with YAML frontmatter. See `references/rule_format.md` for complete specification.

**Basic structure:**
```yaml
---
id: unique-rule-id
keywords: ["keyword1", "keyword2"]
file_patterns: ["*.py", "src/**/*.js"]
priority: high | medium | low
description: Brief one-line description
---
# Rule Title

## Specification

Detailed explanation...

## Checklist

- Check item 1
- Check item 2

## Positive Examples

```python
# Good code
```

## Negative Examples

```python
# Bad code
```
```

### Rule Matching Logic

A rule triggers if **either** condition is met:

1. **File pattern match**: Changed file matches a pattern in `file_patterns`
2. **Keyword match**: Keyword appears in diff content

Both use OR logic - either triggers the rule.

### Creating a New Rule

1. Create `.ai-reviewer/rules/your-rule.md`
2. Add frontmatter with `id`, `keywords`, `file_patterns`, `priority`, `description`
3. Add sections: `Specification`, `Checklist`
4. Optionally add: `Positive Examples`, `Negative Examples`
5. Test by running review on sample code

**Example:**
```yaml
---
id: no-todo-comments
keywords: ["TODO", "FIXME", "HACK"]
file_patterns: ["*.py", "*.js", "*.ts"]
priority: medium
description: No TODO comments in production code
---
# No TODO Comments

## Specification

TODO comments should not be committed. Fix the issue or create a ticket.

## Checklist

- No TODO comments present
- No FIXME comments present
- No HACK comments present

## Negative Examples

```python
# TODO: Refactor this later
def bad_example():
    pass
```
```

## Configuration

### Review Modes

**Block mode** (strict):
```yaml
review_mode: block
```
Blocks commit if violations found. Use `--no-verify` to bypass.

**Warn mode** (permissive):
```yaml
review_mode: warn
```
Shows warnings but allows commit.

**Advisory mode** (informational):
```yaml
review_mode: advisory
```
Runs review but never blocks.

### AI Backend

**Claude API** (recommended, faster):
```yaml
ai_backend: claude-api
claude_api_key: "sk-ant-api03-..."
model: claude-sonnet-4-5-20250929
max_tokens: 4096
```

Requires API key. Set via config or `ANTHROPIC_API_KEY` env var.

**Claude CLI** (slower, no API key needed):
```yaml
ai_backend: claude-cli
```

Requires: `npm install -g @anthropic-ai/claude-cli`

### Skip Patterns

Exclude generated/vendor files:
```yaml
skip_patterns:
  - "*.min.js"
  - "vendor/**"
  - "node_modules/**"
  - "*.pb.go"
```

See `references/config_format.md` for complete configuration reference.

## Managing Git Hooks

### Install Hook

```bash
python3 <skill-path>/scripts/install_hook.py install --hook-type pre-commit
```

### Uninstall Hook

```bash
python3 <skill-path>/scripts/install_hook.py uninstall --hook-type pre-commit
```

### List Installed Hooks

```bash
ls -la .git/hooks/
```

### Hook Location

Hooks are installed to `.git/hooks/pre-commit` or `.git/hooks/pre-push`.

The hooks automatically find the `.ai-reviewer` directory by searching upward from the current directory.

## Running Reviews Manually

### Review Staged Changes

```bash
python3 <skill-path>/scripts/run_review.py --project-root .
```

### Test Rule Matching

```bash
python3 <skill-path>/scripts/load_rules.py .ai-reviewer/rules
```

Lists all rule metadata without running full review.

## Troubleshooting

### Review Not Running

**Check hook installation:**
```bash
ls -la .git/hooks/pre-commit
```

**Check hook is executable:**
```bash
chmod +x .git/hooks/pre-commit
```

**Check .ai-reviewer directory exists:**
```bash
ls -la .ai-reviewer/
```

### API Errors

**Missing API key:**
```bash
export ANTHROPIC_API_KEY=sk-ant-api03-...
```

Or set in `config.yaml`.

**Quota exceeded:** Use `ai_backend: claude-cli` instead.

### Rules Not Matching

**Test metadata loading:**
```bash
python3 <skill-path>/scripts/load_rules.py .ai-reviewer/rules
```

**Check keywords and patterns:**
- Keywords are case-insensitive
- File patterns use glob syntax (e.g., `*.py`, `src/**/*.js`)
- Empty arrays skip that check

### Large Diffs Skipped

If diff exceeds `max_diff_size`, review is skipped. Increase limit:

```yaml
max_diff_size: 50000
```

### Silent Failures

Enable debug logging:

```yaml
log_level: debug
log_file: .ai-reviewer/review.log
```

Check the log file for detailed error messages.

## Progressive Disclosure Design

This skill uses a two-stage loading pattern for token efficiency:

### Stage 1: Metadata Loading

Loads only frontmatter from all rules:
- `id`, `keywords`, `file_patterns`, `priority`, `description`
- Fast operation, minimal token usage
- Stored in `load_rules.py` as `RuleMetadata`

### Stage 2: Rule Matching

Matches rules against diff using only metadata:
- Keyword matching against diff content
- File pattern matching against changed files
- Returns only potentially applicable rules

### Stage 3: Full Rule Loading

Loads complete rule details only for matched rules:
- Specification, checklist, examples
- Passed to AI for detailed review
- Minimizes tokens sent to AI

**Benefits:**
- Scales to hundreds of rules
- Fast initial filtering
- AI receives only relevant context
- Efficient token usage

## Resources

### scripts/

- **install_hook.py**: Install/uninstall git hooks
  ```bash
  python3 scripts/install_hook.py install --hook-type pre-commit
  ```

- **run_review.py**: Main review workflow
  ```bash
  python3 scripts/run_review.py --project-root .
  ```

- **load_rules.py**: Progressive rule loading and matching
  ```python
  from load_rules import RuleLoader, RuleMetadata, FullRule
  ```

### references/

- **rule_format.md**: Complete rule file specification
  - Frontmatter fields
  - Body sections
  - Matching logic
  - Best practices

- **config_format.md**: Complete configuration reference
  - All config fields
  - Review modes
  - AI backends
  - Environment variables

### assets/

- **config.yaml**: Configuration file template
- **rules/**: Example rules
  - `error-handling.md`: Proper exception handling
  - `naming-convention.md`: PEP 8 naming conventions
- **hooks/**: Git hook templates
  - `pre-commit.template`
  - `pre-push.template`

## Best Practices

1. **Start Small**: Begin with 2-3 core rules, expand gradually
2. **Specific Keywords**: Choose unique keywords that indicate the rule's concern
3. **Real Examples**: Use examples from your actual codebase
4. **Block Mode**: Use `review_mode: block` for strict enforcement
5. **Team Adoption**: Discuss rules with team, get consensus
6. **Rule Priority**: Mark critical rules as `priority: high`
7. **Regular Updates**: Review and update rules as codebase evolves
8. **Token Limits**: Monitor AI usage, adjust `max_tokens` if needed

## Advanced Usage

### Custom Rule Categories

Organize rules by category using ID prefixes:
```yaml
id: security-001
id: style-001
id: performance-001
```

### Rule-Specific Prompts

Add custom AI instructions in specification:
```markdown
## Specification

When reviewing this rule, pay special attention to edge cases involving...
```

### Multi-Language Projects

Use file patterns to target specific languages:
```yaml
file_patterns: ["*.py"]  # Python only
file_patterns: ["*.js", "*.ts"]  # JavaScript/TypeScript
file_patterns: ["*"]  # All files
```

### CI/CD Integration

Add to CI pipeline:
```yaml
- name: AI Code Review
  run: python3 scripts/run_review.py --project-root .
```

## Limitations

- Requires Python 3.7+
- Git hooks run in project root context
- Large diffs (>10k chars) are skipped by default
- Claude API has rate limits (use CLI for unlimited reviews)
- Rules use keyword/pattern matching (not AST-based)
