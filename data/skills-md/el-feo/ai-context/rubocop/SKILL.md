---
name: rubocop
description: >-
  Ruby static code analyzer and formatter for enforcing style guidelines, detecting bugs,
  and improving code quality. Supports Rails, RSpec, and Performance extensions with safe
  autocorrection capabilities.
---

# RuboCop Code Analysis & Formatting

RuboCop is Ruby's premier static code analyzer (linter) and formatter, based on the community-driven Ruby Style Guide. This skill enables comprehensive code analysis, automatic formatting, and enforcement of coding standards across Ruby projects including Rails applications.

## When to Use This Skill

Claude automatically uses this skill when users:

- Ask to "check", "lint", "analyze", or "review" Ruby code
- Request code formatting or style improvements
- Want to enforce coding standards or style guidelines
- Need to detect potential bugs or code smells
- Ask about RuboCop configuration or setup
- Request Rails, RSpec, or performance-specific analysis
- Want to run autocorrections on Ruby code

## Core Capabilities

**Code Analysis & Linting**
- Detects style violations, bugs, and code smells across all cop departments
- Supports Rails, RSpec, Performance, and custom cop extensions
- Provides detailed offense reports with line numbers and descriptions

**Automatic Code Correction**
- Safe autocorrection (`-a`) for guaranteed-safe fixes
- Unsafe autocorrection (`-A`) for broader but riskier corrections
- Layout-only fixes (`-x`) for formatting without logic changes

**Configuration & Customization**
- Flexible `.rubocop.yml` configuration
- Per-project and per-directory configuration inheritance
- Selective cop enabling/disabling and severity adjustment
- Custom cop development support

**Extension Integration**
- **rubocop-rails**: Rails best practices and conventions
- **rubocop-rspec**: RSpec-specific analysis
- **rubocop-performance**: Performance optimization checks

## Quick Analysis Workflow

### Run Basic Analysis

```bash
# Analyze current directory
rubocop

# Analyze specific files/directories
rubocop app spec lib/important_file.rb

# Show only correctable offenses
rubocop --display-only-correctable
```

### Apply Corrections

```bash
# Safe autocorrection only (recommended)
rubocop -a

# All corrections including unsafe
rubocop -A

# Layout/formatting corrections only
rubocop -x

# Autocorrect specific cops
rubocop -a --only Style/StringLiterals,Layout/TrailingWhitespace
```

### Targeted Analysis

```bash
# Run only specific cops
rubocop --only Style/StringLiterals,Naming/MethodName

# Run all cops except specified
rubocop --except Metrics/MethodLength

# Run only lint cops
rubocop --lint

# Check only Rails-specific issues
rubocop --only Rails
```

## Configuration Essentials

### Basic .rubocop.yml Setup

```yaml
# Enable extensions
plugins:
  - rubocop-rails
  - rubocop-rspec
  - rubocop-performance

AllCops:
  TargetRubyVersion: 3.2
  NewCops: enable  # Auto-enable new cops
  Exclude:
    - 'db/schema.rb'
    - 'vendor/**/*'
    - 'node_modules/**/*'

# Adjust specific cops
Style/StringLiterals:
  EnforcedStyle: double_quotes

Metrics/MethodLength:
  Max: 15
  Exclude:
    - 'spec/**/*'
```

### Common Configuration Patterns

**Inherit from shared config:**
```yaml
inherit_from:
  - .rubocop_todo.yml
  - config/rubocop_defaults.yml
```

**Rails-specific settings:**
```yaml
Rails:
  Enabled: true

Rails/ApplicationRecord:
  Enabled: true
  Exclude:
    - 'db/migrate/**'
```

**RSpec configuration:**
```yaml
RSpec/ExampleLength:
  Max: 10

RSpec/MultipleExpectations:
  Max: 3
```

## Analysis Interpretation

### Understanding Offense Output

```
app/models/user.rb:15:3: C: Style/StringLiterals: Prefer single-quoted strings...
  name = "John Doe"
         ^^^^^^^^^^
```

**Format breakdown:**
- `app/models/user.rb:15:3` - File path, line number, column number
- `C:` - Severity (C=Convention, W=Warning, E=Error, F=Fatal)
- `Style/StringLiterals` - Cop department and name
- Message explains the issue and often suggests fixes

### Severity Levels

- **Convention (C)**: Style/formatting issues
- **Warning (W)**: Potential problems that should be reviewed
- **Error (E)**: Definite problems that need fixing
- **Fatal (F)**: Syntax errors preventing analysis

## Common Workflows

### Initial Project Setup

```bash
# Generate initial configuration
rubocop --init

# Generate .rubocop_todo.yml for existing violations
rubocop --auto-gen-config

# Use todo file to gradually fix issues
# .rubocop.yml:
inherit_from: .rubocop_todo.yml
```

### Pre-commit Integration

```bash
# Check staged files only
git diff --name-only --cached | grep '\.rb$' | xargs rubocop

# With autocorrection
git diff --name-only --cached | grep '\.rb$' | xargs rubocop -a
```

### CI/CD Integration

```bash
# Exit with error code if offenses found
rubocop --format progress --fail-level warning

# Generate formatted reports
rubocop --format json --out rubocop-report.json
rubocop --format html --out rubocop-report.html
```

### Parallel Execution

```bash
# Use all available CPUs (enabled by default)
rubocop --parallel

# Limit CPU usage
PARALLEL_PROCESSOR_COUNT=2 rubocop
```

## Extension-Specific Features

### Rails Analysis

Detects Rails-specific issues:
- ActiveRecord best practices
- Controller and routing conventions
- Migration safety checks
- SQL injection risks

### RSpec Analysis

Enforces RSpec best practices:
- Example organization and naming
- Let vs instance variable usage
- Expectation patterns
- Test file structure

### Performance Analysis

Identifies performance optimizations:
- Inefficient collection methods
- String concatenation issues
- Unnecessary array allocations
- Regex compilation optimizations

## Troubleshooting

**"Unknown cop" errors:**
- Ensure required gems are installed (`rubocop-rails`, `rubocop-rspec`, etc.)
- Add to `.rubocop.yml`: `plugins: [rubocop-rails]`

**Autocorrection not working:**
- Some cops don't support autocorrection
- Use `-A` for unsafe corrections
- Check cop is enabled in configuration

**Performance issues:**
- Use `--parallel` for faster execution
- Add `UseCache: true` under `AllCops` in config
- Exclude large generated files

## Additional Resources

- [Configuration Guide](references/configuration_guide.md) - Comprehensive configuration reference
- [Cop Reference](references/cop_reference.md) - All cop departments and their responsibilities
- [Extensions Guide](references/extensions_guide.md) - Rails, RSpec, Performance extension details
- [Autocorrect Guide](references/autocorrect_guide.md) - Safe vs unsafe corrections explained
- [Custom Cops Guide](references/custom_cops_guide.md) - Creating custom cops for your project
