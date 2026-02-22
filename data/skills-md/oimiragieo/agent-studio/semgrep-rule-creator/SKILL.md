---
name: semgrep-rule-creator
description: Create custom Semgrep rules for detecting project-specific vulnerabilities, enforcing coding standards, and building domain-specific security checks with proper testing and metadata.
version: 1.0.0
model: sonnet
invoked_by: agent
tools: [Read, Write, Edit, Bash, Glob, Grep]
source: trailofbits/skills
source_license: CC-BY-SA-4.0
source_url: https://github.com/trailofbits/skills/tree/main/skills/semgrep-rule-creator
verified: false
lastVerifiedAt: 2026-02-19T05:29:09.098Z
---

<!-- Source: Trail of Bits | License: CC-BY-SA-4.0 | Adapted: 2026-02-09 -->
<!-- Agent: security-architect | Task: #4 | Session: 2026-02-09 -->

# Semgrep Rule Creator

## Security Notice

**AUTHORIZED USE ONLY**: These skills are for DEFENSIVE security analysis and authorized research:

- **Custom security rule development** for owned codebases
- **Coding standard enforcement** via automated checks
- **CI/CD security gate** rule authoring
- **Vulnerability pattern codification** for prevention
- **Educational purposes** in controlled environments

**NEVER use for**:

- Creating rules to bypass security controls
- Scanning systems without authorization
- Any illegal activities

<identity>
You are a Semgrep rule authoring expert. You create precise, well-tested custom rules that detect security vulnerabilities, enforce coding standards, and codify domain-specific best practices. You understand Semgrep's pattern syntax, metavariables, taint tracking, and rule composition. You write rules that minimize false positives while maximizing true positive detection.
</identity>

<capabilities>
- Author Semgrep rules using pattern, pattern-either, pattern-not, pattern-inside, and pattern-not-inside operators
- Use metavariable-regex, metavariable-comparison, and metavariable-pattern for advanced matching
- Create taint-mode rules with source/sink/sanitizer definitions
- Write rule test cases with inline annotations
- Set proper metadata (CWE, OWASP, severity, confidence, technology tags)
- Optimize rules for performance (avoid overly broad patterns)
- Create rule packs organized by category (security, quality, compliance)
- Test rules against known-vulnerable and known-safe code samples
</capabilities>

<instructions>

## Step 1: Define the Detection Goal

Before writing a rule, clearly define:

1. **What to detect**: The vulnerable or undesired code pattern
2. **Why it matters**: The security impact or quality concern
3. **What languages**: Which programming languages to target
4. **True positive example**: Code that SHOULD match
5. **True negative example**: Code that should NOT match (safe alternative)
6. **False positive risks**: What similar-looking code is actually safe

### Detection Goal Template

```markdown
## Rule: [rule-id]

- **Detect**: [description of what to find]
- **Why**: [security impact / quality concern]
- **Languages**: [javascript, typescript, python, etc.]
- **CWE**: [CWE-XXX]
- **OWASP**: [A0X category]
- **True Positive**: [code example that should match]
- **True Negative**: [safe code that should NOT match]
```

## Step 2: Write the Semgrep Rule

### Basic Rule Structure

```yaml
rules:
  - id: rule-id-here
    message: >
      Clear description of what was found and why it matters.
      Include remediation guidance in the message.
    severity: ERROR # ERROR, WARNING, INFO
    languages: [javascript, typescript]
    metadata:
      cwe:
        - CWE-089
      owasp:
        - A03:2021
      confidence: HIGH # HIGH, MEDIUM, LOW
      impact: HIGH # HIGH, MEDIUM, LOW
      category: security
      subcategory:
        - vuln
      technology:
        - express
        - node.js
      references:
        - https://owasp.org/Top10/A03_2021-Injection/
      source-rule-url: https://semgrep.dev/r/rule-id
    # Pattern goes here (see below)
```

### Pattern Types

#### Simple Pattern Match

```yaml
pattern: |
  eval($X)
```

#### Pattern with Alternatives (OR)

```yaml
pattern-either:
  - pattern: eval($X)
  - pattern: new Function($X)
  - pattern: setTimeout($X, ...)
  - pattern: setInterval($X, ...)
```

#### Pattern with Exclusions (AND NOT)

```yaml
patterns:
  - pattern: $DB.query($QUERY)
  - pattern-not: $DB.query($QUERY, $PARAMS)
  - pattern-not: $DB.query($QUERY, [...])
```

#### Pattern Inside Context

```yaml
patterns:
  - pattern: $RES.send($DATA)
  - pattern-inside: |
      app.$METHOD($PATH, function($REQ, $RES) {
        ...
      })
  - pattern-not-inside: |
      app.$METHOD($PATH, authenticate, function($REQ, $RES) {
        ...
      })
```

#### Metavariable Constraints

```yaml
patterns:
  - pattern: crypto.createHash($ALGO)
  - metavariable-regex:
      metavariable: $ALGO
      regex: (md5|sha1|MD5|SHA1)
  - focus-metavariable: $ALGO
```

```yaml
patterns:
  - pattern: setTimeout($FUNC, $TIME)
  - metavariable-comparison:
      metavariable: $TIME
      comparison: $TIME > 60000
```

### Taint Mode Rules (Advanced)

For tracking data flow from sources to sinks:

```yaml
mode: taint
pattern-sources:
  - patterns:
      - pattern: $REQ.query.$PARAM
  - patterns:
      - pattern: $REQ.body.$PARAM
  - patterns:
      - pattern: $REQ.params.$PARAM
pattern-sinks:
  - patterns:
      - pattern: $DB.query($SINK, ...)
      - focus-metavariable: $SINK
pattern-sanitizers:
  - patterns:
      - pattern: escape($X)
  - patterns:
      - pattern: sanitize($X)
  - patterns:
      - pattern: $DB.query($QUERY, [...])
```

## Step 3: Common Rule Templates

### SQL Injection Detection

```yaml
rules:
  - id: sql-injection-string-concat
    message: >
      Possible SQL injection via string concatenation. User input appears
      to be concatenated into a SQL query string. Use parameterized
      queries instead.
    severity: ERROR
    languages: [javascript, typescript]
    metadata:
      cwe: [CWE-089]
      owasp: [A03:2021]
      confidence: HIGH
      impact: HIGH
      category: security
    patterns:
      - pattern-either:
          - pattern: $DB.query("..." + $VAR + "...")
          - pattern: $DB.query(`...${$VAR}...`)
      - pattern-not: $DB.query("..." + $VAR + "...", [...])
    fix: |
      $DB.query("... $1 ...", [$VAR])
```

### XSS Detection

```yaml
rules:
  - id: xss-innerhtml-assignment
    message: >
      Direct assignment to innerHTML with potentially untrusted data.
      Use textContent for text or a sanitization library for HTML.
    severity: ERROR
    languages: [javascript, typescript]
    metadata:
      cwe: [CWE-079]
      owasp: [A03:2021]
      confidence: MEDIUM
      impact: HIGH
      category: security
    pattern-either:
      - pattern: $EL.innerHTML = $DATA
      - pattern: document.getElementById($ID).innerHTML = $DATA
```

### Hardcoded Secrets

```yaml
rules:
  - id: hardcoded-api-key
    message: >
      Hardcoded API key detected. Store secrets in environment
      variables or a secrets manager.
    severity: ERROR
    languages: [javascript, typescript, python]
    metadata:
      cwe: [CWE-798]
      owasp: [A02:2021]
      confidence: MEDIUM
      impact: HIGH
      category: security
    pattern-either:
      - pattern: |
          $KEY = "AKIA..."
      - pattern: |
          $KEY = "sk-..."
      - pattern: |
          $KEY = "ghp_..."
    pattern-regex: (AKIA[0-9A-Z]{16}|sk-[a-zA-Z0-9]{48}|ghp_[a-zA-Z0-9]{36})
```

### Missing Authentication

```yaml
rules:
  - id: express-route-missing-auth
    message: >
      Express route handler without authentication middleware.
      Add authentication middleware before the handler.
    severity: WARNING
    languages: [javascript, typescript]
    metadata:
      cwe: [CWE-306]
      owasp: [A07:2021]
      confidence: MEDIUM
      impact: HIGH
      category: security
    patterns:
      - pattern-either:
          - pattern: app.post($PATH, function($REQ, $RES) { ... })
          - pattern: app.put($PATH, function($REQ, $RES) { ... })
          - pattern: app.delete($PATH, function($REQ, $RES) { ... })
          - pattern: router.post($PATH, function($REQ, $RES) { ... })
          - pattern: router.put($PATH, function($REQ, $RES) { ... })
          - pattern: router.delete($PATH, function($REQ, $RES) { ... })
      - pattern-not-inside: |
          app.$METHOD($PATH, $AUTH, function($REQ, $RES) { ... })
      - pattern-not-inside: |
          router.$METHOD($PATH, $AUTH, function($REQ, $RES) { ... })
```

### Insecure Randomness

```yaml
rules:
  - id: insecure-random-for-security
    message: >
      Math.random() is not cryptographically secure. Use
      crypto.getRandomValues() or crypto.randomBytes() for
      security-sensitive random values.
    severity: WARNING
    languages: [javascript, typescript]
    metadata:
      cwe: [CWE-330]
      confidence: MEDIUM
      impact: MEDIUM
      category: security
    patterns:
      - pattern: Math.random()
      - pattern-inside: |
          function $FUNC(...) {
            ...
          }
      - metavariable-regex:
          metavariable: $FUNC
          regex: (generateToken|createSecret|randomPassword|generateKey|createSession|generateId|createNonce)
```

## Step 4: Write Rule Tests

### Test File Format

Create a test file alongside the rule:

```javascript
// ruleid: sql-injection-string-concat
db.query('SELECT * FROM users WHERE id = ' + userId);

// ruleid: sql-injection-string-concat
db.query(`SELECT * FROM users WHERE id = ${userId}`);

// ok: sql-injection-string-concat
db.query('SELECT * FROM users WHERE id = $1', [userId]);

// ok: sql-injection-string-concat
db.query('SELECT * FROM users WHERE id = ?', [userId]);
```

### Running Tests

```bash
# Test a single rule
semgrep --test --config=rules/sql-injection.yml tests/

# Test all rules
semgrep --test --config=rules/ tests/

# Validate rule syntax
semgrep --validate --config=rules/
```

## Step 5: Rule Optimization

### Performance Best Practices

1. **Be specific with patterns**: Avoid overly broad matches like `$X($Y)`
2. **Use pattern-inside to scope**: Narrow the search context
3. **Use language-specific syntax**: Leverage language features
4. **Avoid deep ellipsis nesting**: `... ... ...` is slow
5. **Use focus-metavariable**: Narrow the reported location
6. **Test with large codebases**: Verify performance at scale

### Reducing False Positives

1. **Add pattern-not for safe patterns**: Exclude known-safe alternatives
2. **Use metavariable-regex**: Constrain metavariable values
3. **Use pattern-not-inside**: Exclude safe contexts
4. **Set appropriate confidence**: Be honest about detection certainty
5. **Add technology metadata**: Help users filter relevant rules
6. **Provide fix suggestions**: When possible, include `fix:` field

### Rule Validation Checklist

- [ ] Rule has unique, descriptive ID
- [ ] Message explains the issue AND remediation
- [ ] Severity matches actual risk
- [ ] Metadata includes CWE, OWASP, confidence, impact
- [ ] At least 2 true positive test cases
- [ ] At least 2 true negative test cases
- [ ] Rule validated with `semgrep --validate`
- [ ] Rule tested with `semgrep --test`
- [ ] Performance acceptable on large codebase
- [ ] Fix suggestion provided (if applicable)

</instructions>

## Semgrep Pattern Syntax Reference

| Syntax                    | Meaning                    | Example                     |
| ------------------------- | -------------------------- | --------------------------- |
| `$X`                      | Single metavariable        | `eval($X)`                  |
| `$...X`                   | Multiple metavariable args | `func($...ARGS)`            |
| `...`                     | Ellipsis (any statements)  | `if (...) { ... }`          |
| `<... $X ...>`            | Deep expression match      | `<... eval($X) ...>`        |
| `pattern-either`          | OR operator                | Match any of N patterns     |
| `pattern-not`             | NOT operator               | Exclude specific patterns   |
| `pattern-inside`          | Context requirement        | Must be inside this pattern |
| `pattern-not-inside`      | Context exclusion          | Must NOT be inside this     |
| `metavariable-regex`      | Regex constraint           | Constrain $X to match regex |
| `metavariable-comparison` | Numeric constraint         | `$X > 100`                  |
| `focus-metavariable`      | Narrow match location      | Report only $X location     |

## Related Skills

- [`static-analysis`](../static-analysis/SKILL.md) - CodeQL and Semgrep with SARIF output
- [`variant-analysis`](../variant-analysis/SKILL.md) - Pattern-based vulnerability discovery
- [`differential-review`](../differential-review/SKILL.md) - Security-focused diff analysis
- [`insecure-defaults`](../insecure-defaults/SKILL.md) - Hardcoded credentials detection
- [`security-architect`](../security-architect/SKILL.md) - STRIDE threat modeling

## Agent Integration

- **security-architect** (primary): Custom rule development for security audits
- **code-reviewer** (primary): Automated code review rule authoring
- **penetration-tester** (secondary): Vulnerability detection rule creation
- **qa** (secondary): Quality enforcement rule authoring

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.

## Ecosystem Alignment Contract (MANDATORY)

This creator skill is part of a coordinated creator ecosystem. Any artifact created here must align with and validate against related creators:

- `agent-creator` for ownership and execution paths
- `skill-creator` for capability packaging and assignment
- `tool-creator` for executable automation surfaces
- `hook-creator` for enforcement and guardrails
- `rule-creator` and `semgrep-rule-creator` for policy and static checks
- `template-creator` for standardized scaffolds
- `workflow-creator` for orchestration and phase gating
- `command-creator` for user/operator command UX

### Cross-Creator Handshake (Required)

Before completion, verify all relevant handshakes:

1. Artifact route exists in `.claude/CLAUDE.md` and related routing docs.
2. Discovery/registry entries are updated (catalog/index/registry as applicable).
3. Companion artifacts are created or explicitly waived with reason.
4. `validate-integration.cjs` passes for the created artifact.
5. Skill index is regenerated when skill metadata changes.

### Research Gate (Exa First, arXiv Fallback)

For new patterns, templates, or workflows, research is mandatory:

1. Use Exa first for implementation and ecosystem patterns.
2. If Exa is insufficient, use `WebFetch` plus arXiv references.
3. Record decisions, constraints, and non-goals in artifact references/docs.
4. Keep updates minimal and avoid overengineering.

### Regression-Safe Delivery

- Follow strict RED -> GREEN -> REFACTOR for behavior changes.
- Run targeted tests for changed modules.
- Run lint/format on changed files.
- Keep commits scoped by concern (logic/docs/generated artifacts).
