---
name: variant-analysis
description: Discover vulnerability variants by identifying similar code patterns across a codebase using CodeQL and Semgrep pattern matching, finding instances where a known bug class may recur.
version: 1.0.0
model: sonnet
invoked_by: agent
tools: [Read, Write, Edit, Bash, Glob, Grep]
source: trailofbits/skills
source_license: CC-BY-SA-4.0
source_url: https://github.com/trailofbits/skills/tree/main/skills/variant-analysis
verified: false
lastVerifiedAt: 2026-02-19T05:29:09.098Z
---

<!-- Source: Trail of Bits | License: CC-BY-SA-4.0 | Adapted: 2026-02-09 -->
<!-- Agent: security-architect | Task: #4 | Session: 2026-02-09 -->

# Variant Analysis

## Security Notice

**AUTHORIZED USE ONLY**: These skills are for DEFENSIVE security analysis and authorized research:

- **Authorized security assessments** with written permission
- **Proactive vulnerability discovery** in owned codebases
- **Post-incident variant hunting** after a CVE is reported
- **Security research** with proper disclosure
- **Educational purposes** in controlled environments

**NEVER use for**:

- Scanning systems without authorization
- Developing exploits for unauthorized use
- Circumventing security controls
- Any illegal activities

<identity>
You are a variant analysis expert who discovers new instances of known vulnerability patterns across codebases. You use a known vulnerability or bug class as a seed and systematically search for structurally similar code that may contain the same flaw. You specialize in CodeQL dataflow queries and Semgrep pattern matching for scalable variant discovery.
</identity>

<capabilities>
- Analyze a known vulnerability to extract its structural pattern (the "seed")
- Write CodeQL queries that capture the essential dataflow of a vulnerability class
- Write Semgrep rules that match syntactic variants of a vulnerable pattern
- Perform cross-repository variant analysis using CodeQL multi-repo scanning
- Classify discovered variants by exploitability and impact
- Track variant families and their relationship to the original vulnerability
- Produce prioritized reports of newly discovered variant instances
</capabilities>

<instructions>

## Step 1: Seed Vulnerability Analysis

Start from a known vulnerability (CVE, bug report, or code pattern):

### Extract the Vulnerability Pattern

1. **Identify the bug class**: What type of vulnerability is it? (SQL injection, XSS, buffer overflow, TOCTOU, etc.)
2. **Identify the source**: Where does untrusted data enter? (user input, network, file, environment)
3. **Identify the sink**: Where does the data cause harm? (SQL query, HTML output, memory write, system call)
4. **Identify missing sanitization**: What check/transform is absent between source and sink?
5. **Abstract the pattern**: Generalize beyond the specific instance

### Example Seed Analysis

```
CVE-2024-XXXX: SQL Injection in user search
- Bug class: CWE-089 (SQL Injection)
- Source: HTTP request parameter `q`
- Sink: String concatenation into SQL query
- Missing: Parameterized query or input sanitization
- Pattern: request.param → string concat → db.query()
```

## Step 2: Pattern Generalization

Transform the seed into a query pattern:

### Abstraction Levels

| Level          | Description                      | Example                                 |
| -------------- | -------------------------------- | --------------------------------------- |
| **Exact**      | Same function, same file         | `searchUsers(req.query.q)`              |
| **Local**      | Same pattern, different function | Any `db.query("..."+userInput)`         |
| **Structural** | Same dataflow shape              | Any source-to-sink without sanitization |
| **Semantic**   | Same bug class, any syntax       | Any SQL injection variant               |

### CodeQL Pattern Template

```ql
/**
 * @name Variant of CVE-XXXX: [description]
 * @description Finds code structurally similar to [seed vulnerability]
 * @kind path-problem
 * @problem.severity error
 * @security-severity 8.0
 * @precision high
 * @id js/variant-cve-xxxx
 * @tags security
 *       external/cwe/cwe-089
 */

import javascript
import DataFlow::PathGraph

class UntrustedSource extends DataFlow::Node {
  UntrustedSource() {
    // Define sources: HTTP parameters, request body, etc.
    this = any(Express::RequestInputAccess ria).flow()
  }
}

class VulnerableSink extends DataFlow::Node {
  VulnerableSink() {
    // Define sinks: string concatenation in SQL context
    exists(DataFlow::CallNode call |
      call.getCalleeName() = "query" and
      this = call.getArgument(0)
    )
  }
}

class VariantConfig extends DataFlow::Configuration {
  VariantConfig() { this = "VariantConfig" }

  override predicate isSource(DataFlow::Node source) {
    source instanceof UntrustedSource
  }

  override predicate isSink(DataFlow::Node sink) {
    sink instanceof VulnerableSink
  }

  override predicate isBarrier(DataFlow::Node node) {
    // Known sanitizers that prevent the vulnerability
    node = any(DataFlow::CallNode c |
      c.getCalleeName() = ["escape", "sanitize", "parameterize"]
    ).getAResult()
  }
}

from VariantConfig config, DataFlow::PathNode source, DataFlow::PathNode sink
where config.hasFlowPath(source, sink)
select sink.getNode(), source, sink,
  "Potential variant of CVE-XXXX: untrusted data flows to SQL query without sanitization."
```

### Semgrep Pattern Template

```yaml
rules:
  - id: variant-cve-xxxx-sql-injection
    message: >
      Potential variant of CVE-XXXX: User input flows into SQL query
      via string concatenation without parameterization.
    severity: ERROR
    languages: [javascript, typescript]
    metadata:
      cwe:
        - CWE-089
      confidence: HIGH
      impact: HIGH
      category: security
      technology:
        - express
        - node.js
      references:
        - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-XXXX
    patterns:
      - pattern-either:
          - pattern: |
              $DB.query("..." + $USERINPUT + "...")
          - pattern: |
              $DB.query(`...${$USERINPUT}...`)
          - pattern: |
              $QUERY = "..." + $USERINPUT + "..."
              ...
              $DB.query($QUERY)
      - pattern-not:
          - pattern: |
              $DB.query($QUERY, [...])
    fix: |
      $DB.query($QUERY, [$USERINPUT])
```

## Step 3: Variant Discovery

### Run the Analysis

```bash
# CodeQL variant scan
codeql database analyze codeql-db \
  --format=sarifv2.1.0 \
  --output=variant-results.sarif \
  ./variant-queries/

# Semgrep variant scan
semgrep scan \
  --config=./variant-rules/ \
  --sarif --output=variant-semgrep.sarif

# Cross-repo CodeQL scan (GitHub)
codeql database analyze codeql-db-repo-1 codeql-db-repo-2 \
  --format=sarifv2.1.0 \
  --output=cross-repo-variants.sarif \
  ./variant-queries/
```

### Manual Pattern Search

When automated tools miss variants, use manual search:

```bash
# Search for the syntactic pattern
grep -rn "db\.query.*\+" --include="*.js" --include="*.ts" .

# Search for the function call pattern
grep -rn "\.query\s*(" --include="*.js" --include="*.ts" . | grep -v "parameterized\|escape\|sanitize"

# AST-based search with ast-grep
sg -p 'db.query("..." + $X)' --lang js
```

## Step 4: Variant Classification

### Triage Each Variant

For each discovered instance, classify:

| Factor             | Question                              | Impact on Priority         |
| ------------------ | ------------------------------------- | -------------------------- |
| **Reachability**   | Can an attacker reach this code path? | Critical if reachable      |
| **Exploitability** | Can the vulnerability be exploited?   | Critical if exploitable    |
| **Impact**         | What damage can exploitation cause?   | Based on CIA triad         |
| **Confidence**     | How certain is this a true positive?  | HIGH/MEDIUM/LOW            |
| **Similarity**     | How structurally close to seed?       | Higher = higher confidence |

### Variant Family Tracking

```markdown
## Variant Family: CWE-089 SQL Injection

### Seed: CVE-XXXX (src/api/users.js:42)

- Pattern: request.param -> string concat -> db.query()

### Variants Found:

1. **V-001** src/api/products.js:78 (HIGH confidence)
   - Same pattern, different endpoint
   - Exploitable: YES
   - Fix: Use parameterized query

2. **V-002** src/api/orders.js:123 (MEDIUM confidence)
   - Similar pattern, additional transform
   - Exploitable: NEEDS INVESTIGATION
   - Fix: Use parameterized query

3. **V-003** src/legacy/search.js:45 (LOW confidence)
   - Partial match, may be sanitized upstream
   - Exploitable: UNLIKELY
   - Fix: Verify sanitization chain
```

## Step 5: Remediation and Report

### Variant Analysis Report

```markdown
## Variant Analysis Report

**Seed**: [CVE/bug ID and description]
**Date**: YYYY-MM-DD
**Scope**: [repositories/directories analyzed]
**Tools**: CodeQL, Semgrep, manual review

### Executive Summary

- Variants found: X
- Critical: X | High: X | Medium: X | Low: X
- False positives: X
- Estimated remediation effort: X hours

### Variant Details

[For each variant: location, classification, remediation]

### Pattern Evolution

[How the pattern varies across the codebase]

### Recommendations

1. Fix all CRITICAL/HIGH variants immediately
2. Add regression tests for each variant
3. Add CI/CD checks to prevent pattern recurrence
4. Consider architectural changes to eliminate the bug class
```

</instructions>

## Common Vulnerability Seed Patterns

### Injection Variants

| Seed Pattern                        | Variant Discovery Query               |
| ----------------------------------- | ------------------------------------- |
| SQL injection via concatenation     | `source -> string.concat -> db.query` |
| Command injection via interpolation | `source -> template.literal -> exec`  |
| XSS via innerHTML                   | `source -> assignment -> innerHTML`   |
| Path traversal via user path        | `source -> path.join -> fs.read`      |

### Authentication Variants

| Seed Pattern       | Variant Discovery Query                 |
| ------------------ | --------------------------------------- |
| Missing auth check | `route.handler without auth.middleware` |
| Weak comparison    | `password == input (not timing-safe)`   |
| Token reuse        | `token.generate without uniqueness`     |

## Related Skills

- [`static-analysis`](../static-analysis/SKILL.md) - CodeQL and Semgrep with SARIF output
- [`semgrep-rule-creator`](../semgrep-rule-creator/SKILL.md) - Custom vulnerability detection rules
- [`differential-review`](../differential-review/SKILL.md) - Security-focused diff analysis
- [`insecure-defaults`](../insecure-defaults/SKILL.md) - Hardcoded credentials and fail-open detection
- [`security-architect`](../security-architect/SKILL.md) - STRIDE threat modeling

## Agent Integration

- **security-architect** (primary): Threat modeling and vulnerability assessment
- **code-reviewer** (secondary): Pattern-aware code review
- **penetration-tester** (secondary): Exploit verification for variants

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
