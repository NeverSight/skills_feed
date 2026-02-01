---
name: multiversx-semgrep-creator
description: Write custom Semgrep rules to automatically detect MultiversX-specific security patterns and best practice violations. Use when creating automated code scanning, enforcing coding standards, or scaling security reviews.
---

# Semgrep Rule Creator for MultiversX

Create custom Semgrep rules to automatically detect MultiversX-specific security patterns, coding violations, and best practice issues. This skill enables scalable security scanning across codebases.

## When to Use

- Setting up automated security scanning for CI/CD
- Enforcing MultiversX coding standards across teams
- Scaling security reviews with automated pattern detection
- Creating custom rules after finding manual vulnerabilities
- Building organizational security rule libraries

## 1. Semgrep Basics for Rust

### Rule Structure
```yaml
rules:
  - id: rule-identifier
    languages: [rust]
    message: "Description of the issue and why it matters"
    severity: ERROR  # ERROR, WARNING, INFO
    patterns:
      - pattern: <code pattern to match>
    metadata:
      category: security
      technology:
        - multiversx
```

### Pattern Syntax

| Syntax | Meaning | Example |
|--------|---------|---------|
| `$VAR` | Any expression | `$X + $Y` matches `a + b` |
| `...` | Zero or more statements | `{ ... }` matches any block |
| `$...VAR` | Zero or more arguments | `func($...ARGS)` |
| `<... $X ...>` | Contains expression | `<... panic!(...) ...>` |

## 2. Common MultiversX Patterns

### Unsafe Arithmetic Detection

```yaml
rules:
  - id: mvx-unsafe-addition
    languages: [rust]
    message: "Potential arithmetic overflow. Use BigUint or checked arithmetic for financial calculations."
    severity: ERROR
    patterns:
      - pattern: $X + $Y
      - pattern-not: $X.checked_add($Y)
      - pattern-not: BigUint::from($X) + BigUint::from($Y)
    paths:
      include:
        - "*/src/*.rs"
    metadata:
      category: security
      subcategory: arithmetic
      cwe: "CWE-190: Integer Overflow"

  - id: mvx-unsafe-multiplication
    languages: [rust]
    message: "Potential multiplication overflow. Use BigUint or checked_mul."
    severity: ERROR
    patterns:
      - pattern: $X * $Y
      - pattern-not: $X.checked_mul($Y)
      - pattern-not: BigUint::from($X) * BigUint::from($Y)
```

### Floating Point Detection

```yaml
rules:
  - id: mvx-float-forbidden
    languages: [rust]
    message: "Floating point arithmetic is non-deterministic and forbidden in smart contracts."
    severity: ERROR
    pattern-either:
      - pattern: "let $X: f32 = ..."
      - pattern: "let $X: f64 = ..."
      - pattern: "$X as f32"
      - pattern: "$X as f64"
    metadata:
      category: security
      subcategory: determinism
```

### Payable Endpoint Without Value Check

```yaml
rules:
  - id: mvx-payable-no-check
    languages: [rust]
    message: "Payable endpoint does not check payment value. Verify token ID and amount."
    severity: WARNING
    patterns:
      - pattern: |
          #[payable("*")]
          #[endpoint]
          fn $FUNC(&self, $...PARAMS) {
              $...BODY
          }
      - pattern-not: |
          #[payable("*")]
          #[endpoint]
          fn $FUNC(&self, $...PARAMS) {
              <... self.call_value() ...>
          }
    metadata:
      category: security
      subcategory: input-validation
```

### Unsafe Unwrap Usage

```yaml
rules:
  - id: mvx-unsafe-unwrap
    languages: [rust]
    message: "unwrap() can panic. Use unwrap_or_else with sc_panic! or proper error handling."
    severity: ERROR
    patterns:
      - pattern: $EXPR.unwrap()
      - pattern-not-inside: |
          #[test]
          fn $FUNC() { ... }
    fix: "$EXPR.unwrap_or_else(|| sc_panic!(\"Error message\"))"
    metadata:
      category: security
      subcategory: error-handling
```

### Missing Owner Check

```yaml
rules:
  - id: mvx-sensitive-no-owner-check
    languages: [rust]
    message: "Sensitive operation without owner check. Add #[only_owner] or explicit verification."
    severity: ERROR
    patterns:
      - pattern: |
          #[endpoint]
          fn $FUNC(&self, $...PARAMS) {
              <... self.$MAPPER().set(...) ...>
          }
      - pattern-not: |
          #[only_owner]
          #[endpoint]
          fn $FUNC(&self, $...PARAMS) { ... }
      - pattern-not: |
          #[endpoint]
          fn $FUNC(&self, $...PARAMS) {
              <... self.blockchain().get_owner_address() ...>
          }
      - metavariable-regex:
          metavariable: $MAPPER
          regex: "(admin|owner|config|fee|rate)"
```

## 3. Advanced Patterns

### Callback Without Error Handling

```yaml
rules:
  - id: mvx-callback-no-error-handling
    languages: [rust]
    message: "Callback does not handle error case. Async call failures will silently proceed."
    severity: ERROR
    patterns:
      - pattern: |
          #[callback]
          fn $FUNC(&self, $...PARAMS) {
              $...BODY
          }
      - pattern-not: |
          #[callback]
          fn $FUNC(&self, #[call_result] $RESULT: ManagedAsyncCallResult<$TYPE>) {
              ...
          }
```

### Unbounded Iteration

```yaml
rules:
  - id: mvx-unbounded-iteration
    languages: [rust]
    message: "Iterating over storage mapper without bounds. Can cause DoS via gas exhaustion."
    severity: ERROR
    pattern-either:
      - pattern: self.$MAPPER().iter()
      - pattern: |
          for $ITEM in self.$MAPPER().iter() {
              ...
          }
    metadata:
      category: security
      subcategory: dos
      cwe: "CWE-400: Uncontrolled Resource Consumption"
```

### Storage Key Collision Risk

```yaml
rules:
  - id: mvx-storage-key-short
    languages: [rust]
    message: "Storage key is very short, increasing collision risk. Use descriptive keys."
    severity: WARNING
    patterns:
      - pattern: '#[storage_mapper("$KEY")]'
      - metavariable-regex:
          metavariable: $KEY
          regex: "^.{1,3}$"
```

### Reentrancy Pattern Detection

```yaml
rules:
  - id: mvx-reentrancy-risk
    languages: [rust]
    message: "External call before state update. Follow Checks-Effects-Interactions pattern."
    severity: ERROR
    patterns:
      - pattern: |
          fn $FUNC(&self, $...PARAMS) {
              ...
              self.send().$SEND_METHOD(...);
              ...
              self.$STORAGE().set(...);
              ...
          }
      - pattern: |
          fn $FUNC(&self, $...PARAMS) {
              ...
              self.tx().to(...).transfer();
              ...
              self.$STORAGE().set(...);
              ...
          }
```

## 4. Creating Rules from Findings

### Workflow

1. **Find a bug manually** during audit
2. **Abstract the pattern** - what makes this a bug?
3. **Write a Semgrep rule** to catch similar issues
4. **Test on the codebase** - find all variants
5. **Refine to reduce false positives**

### Example: From Bug to Rule

**Bug Found:**
```rust
#[endpoint]
fn withdraw(&self, amount: BigUint) {
    let caller = self.blockchain().get_caller();
    self.send().direct_egld(&caller, &amount);  // Sends before balance check!
    self.balances(&caller).update(|b| *b -= &amount);  // Can underflow
}
```

**Pattern Abstracted:**
- Send/transfer before state update
- No balance validation before deduction

**Rule Created:**
```yaml
rules:
  - id: mvx-withdraw-pattern-unsafe
    languages: [rust]
    message: "Withdrawal sends funds before updating balance. Risk of reentrancy and underflow."
    severity: ERROR
    patterns:
      - pattern: |
          fn $FUNC(&self, $...PARAMS) {
              ...
              self.send().$METHOD(...);
              ...
              self.$BALANCE(...).update(|$B| *$B -= ...);
              ...
          }
      - pattern: |
          fn $FUNC(&self, $...PARAMS) {
              ...
              self.tx().to(...).transfer();
              ...
              self.$BALANCE(...).update(|$B| *$B -= ...);
              ...
          }
```

## 5. Running Semgrep

### Command Line Usage
```bash
# Run single rule
semgrep --config rules/mvx-unsafe-arithmetic.yaml src/

# Run all rules in directory
semgrep --config rules/ src/

# Output JSON for processing
semgrep --config rules/ --json -o results.json src/

# Ignore test files
semgrep --config rules/ --exclude="*_test.rs" --exclude="tests/" src/
```

### CI/CD Integration
```yaml
# GitHub Actions example
- name: Run Semgrep
  uses: returntocorp/semgrep-action@v1
  with:
    config: >-
      rules/mvx-security.yaml
      rules/mvx-best-practices.yaml
```

## 6. Rule Library Organization

```
semgrep-rules/
├── security/
│   ├── mvx-arithmetic.yaml      # Overflow/underflow
│   ├── mvx-access-control.yaml  # Auth issues
│   ├── mvx-reentrancy.yaml      # CEI violations
│   └── mvx-input-validation.yaml
├── best-practices/
│   ├── mvx-storage.yaml         # Storage patterns
│   ├── mvx-gas.yaml             # Gas optimization
│   └── mvx-error-handling.yaml
└── style/
    ├── mvx-naming.yaml          # Naming conventions
    └── mvx-documentation.yaml   # Doc requirements
```

## 7. Testing Rules

### Test File Format
```yaml
# test/mvx-unsafe-unwrap.test.yaml
rules:
  - id: mvx-unsafe-unwrap
    # ... rule definition ...

# Test cases
test_cases:
  - name: "Should match unwrap"
    code: |
      fn test() {
          let x = some_option.unwrap();
      }
    should_match: true

  - name: "Should not match unwrap_or_else"
    code: |
      fn test() {
          let x = some_option.unwrap_or_else(|| sc_panic!("Error"));
      }
    should_match: false
```

### Running Tests
```bash
semgrep --test rules/
```

## 8. Best Practices for Rule Writing

1. **Start specific, then generalize**: Begin with exact pattern, relax constraints carefully
2. **Include fix suggestions**: Use `fix:` field when automated fixes are safe
3. **Document the "why"**: Message should explain impact, not just what's detected
4. **Include CWE references**: Link to standard vulnerability classifications
5. **Test with real codebases**: Validate against actual MultiversX projects
6. **Version your rules**: Rules evolve as framework APIs change
7. **Categorize by severity**: ERROR for security, WARNING for best practices
