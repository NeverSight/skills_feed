---
name: opengrep
description: >-
  Run Opengrep for pattern-based code search and security scanning.
  Use when grep is insufficient for finding code patterns that require
  structural understanding (function calls, data flow, nested structures).
  Also use for security vulnerability detection with custom YAML rules.
---

# Opengrep Static Analysis

Opengrep is a community-maintained, open-source static analysis tool forked from Semgrep. It uses the same rule syntax and CLI interface, making existing Semgrep rules and knowledge transferable.

## Two Use Cases

### 1. Semantic Code Search (grep alternative)

When exploring a codebase, grep finds text patterns but misses structural patterns. Opengrep understands code structure:

| Task                                 | Grep                        | Opengrep                     |
|--------------------------------------|-----------------------------|------------------------------|
| Find text "execute"                  | Fast, works                 | Overkill                     |
| Find `cursor.execute(...)` calls     | May match comments, strings | Matches only actual calls    |
| Find functions that call `os.system` | Difficult                   | `pattern-inside` + `pattern` |
| Find unparameterized SQL queries     | Nearly impossible           | Taint mode                   |

**Use Opengrep when:**
- You need to find function/method calls with specific arguments
- Grep returns too many false positives (matches in comments, strings, similar names)
- You need to find patterns inside specific contexts (inside loops, inside try blocks)
- The pattern has structural meaning, not just text

**Stick with grep when:**
- Simple text search
- Speed is critical
- The pattern is a literal string or simple regex

### 2. Security Scanning

Run rulesets to detect vulnerabilities and insecure patterns.

## Installation

### Linux / macOS

```bash
curl -fsSL https://raw.githubusercontent.com/opengrep/opengrep/main/install.sh | bash
```

### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/opengrep/opengrep/main/install.ps1 | iex
```

### Manual Install

Download binaries from the [releases page](https://github.com/opengrep/opengrep/releases).

### Verify

```bash
opengrep --version
```

Self-contained binaries are available for macOS, Linux, and Windows. No Python required.

Run `opengrep scan --help` to discover all available options and flags.

## Code Search Patterns

### Quick One-Liners

```bash
# Find all calls to a function
opengrep scan -e 'dangerous_function(...)' -l python .

# Find method calls on specific objects
opengrep scan -e '$OBJ.execute(...)' -l python .

# Find assignments to a variable name
opengrep scan -e '$VAR = os.environ.get(...)' -l python .

# Find function definitions
opengrep scan -e 'def $FUNC(...): ...' -l python .
```

### Performance Note

Opengrep parses the entire file into an AST. For a quick text search, grep is 10-100x faster. Use Opengrep when the structural match is worth the overhead.

## Security Scanning

### Quick Scan

```bash
# Scan with a ruleset
opengrep scan --config p/security-audit .

# Multiple rulesets
opengrep scan --config p/security-audit --config p/owasp-top-ten .

# Scan specific paths
opengrep scan --config p/python src/
```

### Output Formats

```bash
# SARIF for tooling
opengrep scan --config p/default --sarif -o results.sarif .

# JSON for automation
opengrep scan --config p/default --json -o results.json .

# Show data flow traces
opengrep scan --dataflow-traces -f rule.yaml .

# Include enclosing context (function/class) in JSON output (experimental)
opengrep scan --output-enclosing-context --json -f rule.yaml . --experimental
```

### Filtering

```bash
# By severity
opengrep scan --config p/default --severity ERROR .

# By path
opengrep scan --config p/default --include='src/**' --exclude='**/test/**' .

# Apply exclusions to explicitly passed file targets (not just directory scan roots)
opengrep scan --force-exclude --exclude='**/vendor/**' -f rule.yaml vendor/lib.py
```

### Intrafile Cross-Function Tainting

Opengrep supports tracking taint across functions within a file:

```bash
opengrep scan --taint-intrafile -f taint-rule.yaml .
```

This enables higher-order function support and is similar to Semgrep Pro's `--pro-intrafile`.

## Writing Custom Rules

### Basic Rule Structure

```yaml
rules:
  - id: hardcoded-secret
    languages: [python]
    message: "Hardcoded secret detected in $VAR"
    severity: ERROR
    patterns:
      - pattern: $VAR = "$VALUE"
      - metavariable-regex:
          metavariable: $VALUE
          regex: ^sk_live_
```

### Rule ID Uniqueness

**Important**: Rule IDs must be unique across all rules in a configuration. If multiple rules share the same ID, only one will be used due to deduplication during rule loading.

This is particularly important when writing rules for multiple languages. You cannot reuse the same rule ID even if the rules target different languages:

```yaml
# WRONG - both rules have id: taint, only one will be active
rules:
  - id: taint
    languages: [python]
    pattern: dangerous_call(...)
    # ...

  - id: taint
    languages: [rust]
    pattern: unsafe_fn(...)
    # ...
```

```yaml
# CORRECT - unique IDs for each rule
rules:
  - id: taint-python-dangerous-call
    languages: [python]
    pattern: dangerous_call(...)
    # ...

  - id: taint-rust-unsafe-fn
    languages: [rust]
    pattern: unsafe_fn(...)
    # ...
```

Use descriptive IDs that include the language or context to avoid collisions.

### Pattern Syntax

| Syntax         | Meaning                                       |
|----------------|-----------------------------------------------|
| `...`          | Match zero or more arguments/statements       |
| `$VAR`         | Metavariable (captures any expression)        |
| `$...ARGS`     | Ellipsis metavariable (captures zero or more) |
| `<... $X ...>` | Deep expression match (nested)                |

### Pattern Operators

| Operator                  | Purpose                         |
|---------------------------|---------------------------------|
| `pattern`                 | Match exact pattern             |
| `patterns`                | All must match (AND)            |
| `pattern-either`          | Any can match (OR)              |
| `pattern-not`             | Exclude matches                 |
| `pattern-inside`          | Must be inside context          |
| `pattern-not-inside`      | Must not be inside context      |
| `pattern-regex`           | Regex matching                  |
| `metavariable-regex`      | Filter captured values by regex |
| `metavariable-comparison` | Compare captured values         |

### Combining Patterns

```yaml
rules:
  - id: dangerous-deserialization
    languages: [python]
    message: "Unsafe pickle load on potentially untrusted data"
    severity: ERROR
    patterns:
      - pattern-either:
          - pattern: pickle.load(...)
          - pattern: pickle.loads(...)
      - pattern-not-inside: |
          def $FUNC(...):
            ...
```

### Taint Mode

For tracking data flow from sources to sinks:

```yaml
rules:
  - id: sql-injection
    languages: [python]
    message: "User input flows to SQL query without parameterization"
    severity: ERROR
    mode: taint
    pattern-sources:
      - pattern: request.args.get(...)
      - pattern: request.form[...]
    pattern-sinks:
      - pattern: cursor.execute($QUERY, ...)
        focus-metavariable: $QUERY
    pattern-sanitizers:
      - pattern: int(...)
      - pattern: escape(...)
```

**Key taint concepts:**
- **Sources**: Where untrusted data enters
- **Sinks**: Where data becomes dangerous
- **Sanitizers**: What makes data safe

### YAML Pitfalls

Patterns are YAML string values. Any pattern containing `: ` (colon-space) will be misinterpreted as a YAML mapping and cause a validation error. Always quote such patterns:

```yaml
# BROKEN -- YAML parser sees "shell: true" as a nested mapping
- pattern: spawn($CMD, { ..., shell: true, ... })

# CORRECT -- quoted string, parsed as a single pattern value
- pattern: "spawn($CMD, { ..., shell: true, ... })"
```

Common triggers: `shell: true`, `mode: 0o777`, `redirect: "follow"`, `error: $ERR`. When in doubt, quote the pattern.

For patterns containing both double quotes and colons, use escaped inner quotes:

```yaml
- pattern: "fetch($URL, { ..., redirect: \"follow\", ... })"
```

### Scanning Non-Code Files (generic language)

For XML configs, YAML pipelines, Dockerfiles, and other non-code files, structural patterns may not work. Use `languages: [generic]` with `pattern-regex`:

```yaml
rules:
  - id: cleartext-traffic
    patterns:
      - pattern-regex: 'cleartextTrafficPermitted\s*=\s*"true"'
    languages: [generic]
    severity: WARNING
    paths:
      include:
        - "app/src/"
```

The `paths` key restricts which files a rule applies to:

```yaml
paths:
  include:
    - ".github/workflows/"    # Only scan GHA workflow files
  exclude:
    - "test/"                 # Skip test directories
```

**Note**: `languages: [dockerfile]` exists but `pattern-not-inside` does not work reliably across multiple Dockerfile directives. Prefer `generic` + regex for Dockerfile security checks that span multiple lines.

### metavariable-pattern

Use `metavariable-pattern` to constrain what a metavariable can match. It must be a list item inside `patterns:`, alongside the pattern that captures the metavariable:

```yaml
rules:
  - id: dynamic-property-assignment
    patterns:
      - pattern: $OBJ[$KEY] = $VALUE
      - metavariable-pattern:
          metavariable: $KEY
          patterns:
            - pattern-not: "..."    # Exclude literal string keys
    languages: [typescript, javascript]
    severity: WARNING
```

This is distinct from `metavariable-regex` which filters by regex rather than by pattern.

### Pattern Parsing Limitations

Some language constructs cannot be matched as standalone fragments:

- **`catch` blocks**: `catch ($ERR) { ... }` alone is invalid. You must include the `try`: `try { ... } catch ($ERR) { ... }`. Even then, complex ellipsis inside the catch body may fail to parse for TypeScript.
- **Workaround**: Match the dangerous expression directly instead of wrapping in try/catch context.

### Rule Options (Opengrep-specific)

```yaml
rules:
  - id: expensive-rule
    options:
      timeout: 10              # Per-rule timeout (requires --allow-rule-timeout-control)
      dynamic_timeout: true    # Scale timeout with file size
      max_match_per_file: 100  # Limit matches per file
    # ... rest of rule
```

Use `--allow-rule-timeout-control` to enable per-rule timeouts.

## Testing Rules

### Test File Annotations

Place `# ruleid:` on the line immediately before the expected finding (for taint rules, before the sink):

```python
# test_rule.py

def vulnerable():
    user_id = request.args.get("id")
    # ruleid: sql-injection
    cursor.execute("SELECT * FROM users WHERE id = " + user_id)

def safe():
    user_id = int(request.args.get("id"))
    # ok: sql-injection
    cursor.execute("SELECT * FROM users WHERE id = " + user_id)
```

### Running Tests

```bash
# Test a rule (supports multiple target files)
opengrep test --config rule.yaml test_file.py test_file2.py

# Validate rule syntax (positional argument, not --config)
opengrep validate rule.yaml

# Debug taint flow
opengrep scan --dataflow-traces -f rule.yaml test_file.py
```

## Configuration

### .semgrepignore

Opengrep uses `.semgrepignore` for compatibility. Custom filename via `--semgrepignore-filename`:

```
# Ignore directories
vendor/
node_modules/
**/testdata/

# Ignore patterns
*.min.js
*.generated.go
```

### Inline Suppressions

Default annotations: `nosemgrep`, `nosem`, `noopengrep` (all work):

```python
password = get_from_vault()  # nosemgrep: hardcoded-password
password = get_from_vault()  # nosem: hardcoded-password
password = get_from_vault()  # noopengrep: hardcoded-password
```

Extend with additional patterns using `--opengrep-ignore-pattern`:

```bash
# Add nosec as an additional suppression annotation
opengrep scan --opengrep-ignore-pattern='nosec' -f rule.yaml .
```

## Rule Metadata

```yaml
rules:
  - id: command-injection
    metadata:
      category: security
      subcategory:
        - vuln              # vuln = confirmed vulnerability, audit = needs review
      cwe:
        - "CWE-78: Improper Neutralization of Special Elements used in an OS Command"
      owasp:
        - "A03:2021 - Injection"
      confidence: HIGH      # HIGH, MEDIUM, or LOW
      references:
        - https://owasp.org/Top10/A03_2021-Injection/
    # ... rest of rule
```

The `category`/`subcategory`/`confidence` fields are used by tooling to classify and filter findings. Use `subcategory: [vuln]` for high-confidence vulnerabilities and `subcategory: [audit]` for patterns that need manual review.

Use `--inline-metavariables` to include metavariable values in metadata output.

## Common Rulesets

| Ruleset                                  | Focus                        |
|------------------------------------------|------------------------------|
| `p/security-audit`                       | Comprehensive security rules |
| `p/owasp-top-ten`                        | OWASP Top 10 vulnerabilities |
| `p/cwe-top-25`                           | CWE Top 25 vulnerabilities   |
| `p/python` / `p/javascript` / `p/golang` | Language-specific            |

Note: Ruleset availability may differ from Semgrep registry.

## Differences from Semgrep

Opengrep is forked from Semgrep 1.100.0. Key differences:

- **Semgrep Pro features, open**: Intrafile cross-function tainting (`--taint-intrafile`), higher-order function support, and inter-method taint flow -- all available without a commercial license
- **Additional languages**: Visual Basic (not available in Semgrep CE or Pro), Apex, Elixir (not in Semgrep CE), improved Clojure with taint support
- **Windows**: Native support
- **Per-rule timeouts**: `timeout` and `dynamic_timeout` rule options
- **Match limits**: `max_match_per_file` rule option and `--max-match-per-file` CLI flag
- **Context output**: `--output-enclosing-context` shows function/class context
- **Custom ignore patterns**: `--opengrep-ignore-pattern` extends default suppressions

For full changelog, see: https://github.com/opengrep/opengrep/blob/main/OPENGREP.md

Existing Semgrep rules and documentation generally apply.

## Resources

- Opengrep: https://github.com/opengrep/opengrep
- Semgrep rule syntax (compatible): https://semgrep.dev/docs/writing-rules/rule-syntax
