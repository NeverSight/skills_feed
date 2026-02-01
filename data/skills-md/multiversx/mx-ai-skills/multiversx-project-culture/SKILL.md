---
name: multiversx-project-culture
description: Assess codebase quality and maturity based on documentation, testing practices, and code hygiene indicators. Use when evaluating project reliability, estimating audit effort, or onboarding to new codebases.
---

# Project Culture & Code Maturity Assessment

Evaluate the quality and reliability of a MultiversX codebase based on documentation presence, testing culture, code hygiene, and development practices. This assessment helps calibrate audit depth and identify areas of concern.

## When to Use

- Starting engagement with a new project
- Estimating audit scope and effort
- Evaluating investment or integration risk
- Providing feedback on development practices
- Prioritizing review focus areas

## 1. Documentation Quality

### Documentation Presence Checklist

| Item | Location | Status |
|------|----------|--------|
| README.md | Project root | [ ] Present [ ] Useful |
| Build instructions | README or BUILDING.md | [ ] Present [ ] Tested |
| API documentation | docs/ or inline | [ ] Present [ ] Complete |
| Architecture overview | docs/ or specs/ | [ ] Present |
| Deployment guide | README or DEPLOY.md | [ ] Present |

### MultiversX-Specific Documentation

| Item | Purpose | Status |
|------|---------|--------|
| `mxpy.json` | Standard build configuration | [ ] Present |
| `sc-config.toml` | Contract configuration | [ ] Present |
| `multiversx.yaml` | Additional config | [ ] Optional |
| `snippets.sh` | Interaction scripts | [ ] Helpful |
| `interaction/` | Deployment/call scripts | [ ] Very helpful |

### Specification Documents

| Document | Quality Indicator |
|----------|-------------------|
| Whitepaper | Formal specification of behavior |
| `specs/` directory | Detailed technical specs |
| MIP compliance docs | Standard adherence documentation |
| Security considerations | Threat model awareness |

### Documentation Quality Scoring

```
HIGH QUALITY:
- README explains purpose, build, test, deploy
- Architecture diagrams present
- API fully documented with examples
- Security model documented

MEDIUM QUALITY:
- README with basic instructions
- Some inline documentation
- Partial API coverage

LOW QUALITY:
- Minimal or no README
- No inline comments
- No architectural documentation
```

## 2. Testing Culture Assessment

### Test Presence

```bash
# Check for Rust unit tests
grep -r "#\[test\]" src/

# Check for Mandos/scenario tests
ls -la scenarios/

# Check for integration tests
ls -la tests/
```

### Mandos Scenario Coverage

| Coverage Level | Indicators |
|----------------|------------|
| **Excellent** | Every endpoint has scenario, edge cases tested, failure paths covered |
| **Good** | All endpoints have basic scenarios, some edge cases |
| **Minimal** | Only `deploy.scen.json` or few scenarios |
| **None** | No `scenarios/` directory |

### Test Quality Indicators

```rust
// HIGH QUALITY: Tests cover edge cases
#[test]
fn test_deposit_zero_amount() { }  // Boundary
#[test]
fn test_deposit_max_amount() { }   // Boundary
#[test]
fn test_deposit_wrong_token() { }  // Error case
#[test]
fn test_deposit_unauthorized() { } // Access control

// LOW QUALITY: Only happy path
#[test]
fn test_deposit() { }  // Basic only
```

### Continuous Integration

| CI Feature | Status |
|------------|--------|
| Automated builds | [ ] Present |
| Test execution | [ ] Present |
| Coverage reporting | [ ] Present |
| Lint/format checks | [ ] Present |
| Security scanning | [ ] Present |

### Simulation Testing

Look for:
- `mx-chain-simulator-go` usage
- Docker-based test environments
- Integration test scripts

## 3. Code Hygiene Assessment

### Linter Compliance

```bash
# Run Clippy
cargo clippy -- -W clippy::all

# Check formatting
cargo fmt --check
```

| Clippy Status | Interpretation |
|---------------|----------------|
| 0 warnings | Excellent hygiene |
| < 10 warnings | Good, minor issues |
| 10-50 warnings | Needs attention |
| > 50 warnings | Poor hygiene |

### Magic Numbers

```bash
# Find raw numeric literals
grep -rn "[^a-zA-Z_][0-9]\{2,\}[^a-zA-Z0-9_]" src/
```

**Bad:**
```rust
let seconds = 86400;  // What is this?
let fee = amount * 3 / 100;  // Magic 3%
```

**Good:**
```rust
const SECONDS_PER_DAY: u64 = 86400;
const FEE_PERCENT: u64 = 3;
const FEE_DENOMINATOR: u64 = 100;

let seconds = SECONDS_PER_DAY;
let fee = amount * FEE_PERCENT / FEE_DENOMINATOR;
```

### Error Handling

```bash
# Count unwrap usage
grep -c "\.unwrap()" src/*.rs

# Count expect usage
grep -c "\.expect(" src/*.rs

# Count proper error handling
grep -c "sc_panic!\|require!" src/*.rs
```

| Pattern | Quality Indicator |
|---------|-------------------|
| Mostly `require!` with messages | Good |
| Mixed `require!` and `unwrap()` | Needs review |
| Mostly `unwrap()` | Poor |

### Code Comments

| Aspect | Good Practice |
|--------|---------------|
| Complex logic | Has explanatory comments |
| Public APIs | Has doc comments |
| Assumptions | Documented inline |
| TODOs | Tracked, not ignored |

```rust
// GOOD: Complex logic explained
/// Calculates rewards using compound interest formula.
/// Formula: P * (1 + r/n)^(nt) where:
/// - P: principal
/// - r: annual rate (in basis points)
/// - n: compounding frequency
/// - t: time in years
fn calculate_rewards(&self, principal: BigUint, time: u64) -> BigUint {
    // ...
}

// BAD: No explanation for complex logic
fn calc(&self, p: BigUint, t: u64) -> BigUint {
    // Dense, unexplained calculation
}
```

## 4. Dependency Management

### Cargo.lock Presence

```bash
ls -la Cargo.lock
```

| Status | Interpretation |
|--------|----------------|
| Committed | Reproducible builds |
| Not committed | Version drift risk |

### Version Pinning

```toml
# GOOD: Specific versions
[dependencies.multiversx-sc]
version = "0.54.0"

# BAD: Wildcard versions
[dependencies.multiversx-sc]
version = "*"

# ACCEPTABLE: Caret (minor updates)
[dependencies.multiversx-sc]
version = "^0.54"
```

### Dependency Audit

```bash
# Check for known vulnerabilities
cargo audit
```

## 5. Maturity Scoring Matrix

### Score Calculation

| Category | Weight | High (3) | Medium (2) | Low (1) |
|----------|--------|----------|------------|---------|
| Documentation | 20% | Complete | Partial | Minimal |
| Testing | 30% | Full coverage | Basic coverage | Minimal |
| Code hygiene | 20% | Clean Clippy | Few warnings | Many issues |
| Dependencies | 15% | Pinned, audited | Pinned | Wildcards |
| CI/CD | 15% | Full pipeline | Basic | None |

### Interpretation

| Score | Maturity | Audit Focus |
|-------|----------|-------------|
| 2.5-3.0 | High | Business logic, edge cases |
| 1.5-2.4 | Medium | Broad review, verify basics |
| 1.0-1.4 | Low | Everything, assume issues exist |

## 6. Red Flags

### Immediate Concerns

| Red Flag | Risk |
|----------|------|
| No tests at all | Logic likely untested |
| Wildcard dependencies | Supply chain vulnerability |
| `unsafe` blocks without justification | Memory safety issues |
| Excessive `unwrap()` | Panic vulnerabilities |
| No README | Maintenance abandoned? |
| Outdated framework version | Known vulnerabilities |

### Yellow Flags

| Yellow Flag | Concern |
|-------------|---------|
| Few scenario tests | Limited coverage |
| Some Clippy warnings | Technical debt |
| Incomplete documentation | Knowledge silos |
| No CI/CD | Regression risk |

## 7. Assessment Report Template

```markdown
# Project Maturity Assessment

**Project**: [Name]
**Version**: [Version]
**Date**: [Date]
**Assessor**: [Name]

## Summary Score: [X/3.0] - [HIGH/MEDIUM/LOW] Maturity

## Documentation (Score: X/3)
- README: [Present/Missing]
- Build instructions: [Tested/Untested/Missing]
- Architecture docs: [Complete/Partial/Missing]
- API docs: [Complete/Partial/Missing]

## Testing (Score: X/3)
- Unit tests: [X tests found]
- Scenario tests: [X scenarios covering Y endpoints]
- Coverage estimate: [X%]
- Edge case coverage: [Good/Partial/Minimal]

## Code Hygiene (Score: X/3)
- Clippy warnings: [X warnings]
- Formatting: [Consistent/Inconsistent]
- Magic numbers: [X instances]
- Error handling: [Good/Needs work]

## Dependencies (Score: X/3)
- Cargo.lock: [Committed/Missing]
- Version pinning: [All/Some/None]
- Known vulnerabilities: [None/X found]

## CI/CD (Score: X/3)
- Build automation: [Yes/No]
- Test automation: [Yes/No]
- Security scanning: [Yes/No]

## Recommendations
1. [Highest priority improvement]
2. [Second priority]
3. [Third priority]

## Audit Focus Areas
Based on this assessment, the audit should prioritize:
1. [Area based on weaknesses]
2. [Area based on risk]
```

## 8. Improvement Recommendations by Level

### For Low Maturity Projects
1. Add basic README with build instructions
2. Create scenario tests for all endpoints
3. Fix all Clippy warnings
4. Pin dependency versions
5. Set up basic CI

### For Medium Maturity Projects
1. Expand test coverage to edge cases
2. Add architecture documentation
3. Document security considerations
4. Add coverage reporting
5. Implement security scanning

### For High Maturity Projects
1. Formal verification consideration
2. Fuzzing and property testing
3. External security audit
4. Bug bounty program
5. Incident response documentation
