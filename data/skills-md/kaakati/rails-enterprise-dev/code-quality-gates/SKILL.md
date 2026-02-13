---
name: code-quality-gates
description: "Expert quality gate decisions for iOS/tvOS: which gates matter for your project size, threshold calibration that catches bugs without blocking velocity, SwiftLint rule selection, and CI integration patterns. Use when setting up linting, configuring CI pipelines, or calibrating coverage thresholds. Trigger keywords: SwiftLint, SwiftFormat, coverage, CI, quality gate, lint, static analysis, pre-commit, threshold, warning"
version: "3.0.0"
---

# Code Quality Gates — Expert Decisions

Expert decision frameworks for quality gate choices. Claude knows linting tools — this skill provides judgment calls for threshold calibration and rule selection.

---

## Decision Trees

### Which Quality Gates for Your Project

```
Project stage?
├─ Greenfield (new project)
│  └─ Enable ALL gates from day 1
│     • SwiftLint (strict)
│     • SwiftFormat
│     • SWIFT_TREAT_WARNINGS_AS_ERRORS = YES
│     • Coverage > 80%
│
├─ Brownfield (legacy, no gates)
│  └─ Adopt incrementally:
│     1. SwiftLint with --baseline (ignore existing)
│     2. Format new files only
│     3. Gradually increase thresholds
│
└─ Existing project with some gates
   └─ Team size?
      ├─ Solo/Small (1-3) → Lint + Format sufficient
      └─ Medium+ (4+) → Full pipeline
         • Add coverage gates
         • Add static analysis
         • Add security scanning
```

### Coverage Threshold Selection

```
What type of code?
├─ Domain/Business Logic
│  └─ 90%+ coverage required
│     • Business rules must be tested
│     • Silent bugs are expensive
│
├─ Data Layer (Repositories, Mappers)
│  └─ 85% coverage
│     • Test mapping edge cases
│     • Test error handling
│
├─ Presentation (ViewModels)
│  └─ 70-80% coverage
│     • Test state transitions
│     • Skip trivial bindings
│
└─ Views (SwiftUI)
   └─ Don't measure coverage
      • Snapshot tests or manual QA
      • Unit testing views has poor ROI
```

### SwiftLint Rule Strategy

```
Starting fresh?
├─ YES → Enable opt_in_rules aggressively
│  └─ Easier to disable than enable later
│
└─ NO → Adopting on existing codebase
   └─ Use baseline approach:
      1. Run: swiftlint lint --reporter json > baseline.json
      2. Configure: baseline_path: baseline.json
      3. New violations fail, existing ignored
      4. Chip away at baseline over time
```

---

## NEVER Do

### Threshold Anti-Patterns

**NEVER** set coverage to 100%:
```yaml
# ❌ Blocks legitimate PRs, encourages gaming
MIN_COVERAGE: 100

# ✅ Realistic threshold with room for edge cases
MIN_COVERAGE: 80
```

**NEVER** use zero-tolerance for warnings initially on legacy code:
```bash
# ❌ 500 warnings = blocked pipeline forever
SWIFT_TREAT_WARNINGS_AS_ERRORS = YES  # On day 1 of legacy project

# ✅ Incremental adoption
# 1. First: just report warnings
SWIFT_TREAT_WARNINGS_AS_ERRORS = NO

# 2. Then: require no NEW warnings
swiftlint lint --baseline existing-violations.json

# 3. Finally: zero tolerance (after cleanup)
SWIFT_TREAT_WARNINGS_AS_ERRORS = YES
```

**NEVER** skip gates on "urgent" PRs:
```yaml
# ❌ Creates precedent, gates become meaningless
if: github.event.pull_request.labels.contains('urgent')
  run: echo "Skipping quality gates"

# ✅ Gates are non-negotiable
# If code can't pass gates, it shouldn't ship
```

### SwiftLint Anti-Patterns

**NEVER** disable rules project-wide without documenting why:
```yaml
# ❌ Mystery disabled rules
disabled_rules:
  - force_unwrapping
  - force_cast
  - line_length

# ✅ Document the reasoning
disabled_rules:
  # line_length: Configured separately with custom thresholds
  # force_unwrapping: Using force_unwrapping opt-in rule instead (stricter)
```

**NEVER** use inline disables without explanation:
```swift
// ❌ No context
// swiftlint:disable force_unwrapping
let value = optionalValue!
// swiftlint:enable force_unwrapping

// ✅ Explain why exception is valid
// swiftlint:disable force_unwrapping
// Reason: fatalError path for corrupted bundle resources that should crash
let value = optionalValue!
// swiftlint:enable force_unwrapping
```

**NEVER** silence all warnings in a file:
```swift
// ❌ Nuclear option hides real issues
// swiftlint:disable all

// ✅ Disable specific rules for specific lines
// swiftlint:disable:next identifier_name
let x = calculateX()  // Math convention
```

### CI Anti-Patterns

**NEVER** run expensive gates first:
```yaml
# ❌ Slow feedback — tests run even if lint fails
jobs:
  test:  # 10 minutes
    ...
  lint:  # 30 seconds
    ...

# ✅ Fast feedback — fail fast on cheap checks
jobs:
  lint:
    runs-on: macos-14
    steps: [swiftlint, swiftformat]

  build:
    needs: lint  # Only if lint passes
    ...

  test:
    needs: build  # Only if build passes
    ...
```

**NEVER** run quality gates only on PR:
```yaml
# ❌ Main branch can have violations
on:
  pull_request:
    branches: [main]

# ✅ Protect main branch too
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
```

---

## Essential Configurations

### Minimal SwiftLint (Start Here)

```yaml
# .swiftlint.yml — Essential rules only

excluded:
  - Pods
  - .build
  - DerivedData

# Most impactful opt-in rules
opt_in_rules:
  - force_unwrapping          # Catches crashes
  - implicitly_unwrapped_optional
  - empty_count               # Performance
  - first_where               # Performance
  - contains_over_first_not_nil
  - fatal_error_message       # Debugging

# Sensible limits
line_length:
  warning: 120
  error: 200
  ignores_urls: true
  ignores_function_declarations: true

function_body_length:
  warning: 50
  error: 80

cyclomatic_complexity:
  warning: 10
  error: 15

type_body_length:
  warning: 300
  error: 400

file_length:
  warning: 500
  error: 800
```

### Minimal SwiftFormat

```ini
# .swiftformat — Essentials only

--swiftversion 5.9
--exclude Pods,.build,DerivedData

--indent 4
--maxwidth 120
--wraparguments before-first
--wrapparameters before-first

# Non-controversial rules
--enable sortedImports
--enable trailingCommas
--enable redundantSelf
--enable redundantReturn
--enable blankLinesAtEndOfScope

# Disable controversial rules
--disable acronyms
--disable wrapMultilineStatementBraces
```

### Xcode Build Settings (Quality Enforced)

```ini
# QualityGates.xcconfig

// Fail on warnings
SWIFT_TREAT_WARNINGS_AS_ERRORS = YES
GCC_TREAT_WARNINGS_AS_ERRORS = YES

// Strict concurrency (Swift 6 prep)
SWIFT_STRICT_CONCURRENCY = complete

// Static analyzer
RUN_CLANG_STATIC_ANALYZER = YES
CLANG_STATIC_ANALYZER_MODE = deep
```

---

## CI Patterns

### GitHub Actions (Minimal Effective)

```yaml
name: Quality Gates

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  # Fast gates first
  lint:
    runs-on: macos-14
    steps:
      - uses: actions/checkout@v4
      - run: brew install swiftlint swiftformat
      - run: swiftlint lint --strict --reporter github-actions-logging
      - run: swiftformat . --lint

  # Build only if lint passes
  build:
    needs: lint
    runs-on: macos-14
    steps:
      - uses: actions/checkout@v4
      - name: Build with strict warnings
        run: |
          xcodebuild build \
            -scheme App \
            -destination 'platform=iOS Simulator,name=iPhone 15' \
            SWIFT_TREAT_WARNINGS_AS_ERRORS=YES

  # Test only if build passes
  test:
    needs: build
    runs-on: macos-14
    steps:
      - uses: actions/checkout@v4
      - name: Test with coverage
        run: |
          xcodebuild test \
            -scheme App \
            -destination 'platform=iOS Simulator,name=iPhone 15' \
            -enableCodeCoverage YES \
            -resultBundlePath TestResults.xcresult

      - name: Check coverage threshold
        run: |
          COVERAGE=$(xcrun xccov view --report --json TestResults.xcresult | \
            jq '.targets[] | select(.name | contains("App")) | .lineCoverage * 100')
          echo "Coverage: ${COVERAGE}%"
          if (( $(echo "$COVERAGE < 80" | bc -l) )); then
            echo "❌ Coverage below 80%"
            exit 1
          fi
```

### Pre-commit Hook (Local Enforcement)

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running pre-commit quality gates..."

# SwiftLint (fast)
if ! swiftlint lint --strict --quiet 2>/dev/null; then
    echo "❌ SwiftLint failed"
    exit 1
fi

# SwiftFormat check (fast)
if ! swiftformat . --lint 2>/dev/null; then
    echo "❌ Code formatting issues. Run: swiftformat ."
    exit 1
fi

echo "✅ Pre-commit checks passed"
```

---

## Threshold Calibration

### Finding the Right Coverage Threshold

```
Step 1: Measure current coverage
$ xcodebuild test -enableCodeCoverage YES ...
$ xcrun xccov view --report TestResults.xcresult

Step 2: Set threshold slightly below current
Current: 73% → Set threshold: 70%
Prevents regression without blocking

Step 3: Ratchet up over time
Week 1: 70%
Week 4: 75%
Week 8: 80%
Stop at: 80-85% (diminishing returns above)
```

### SwiftLint Warning Budget

```yaml
# Start permissive, tighten over time
# Week 1
MAX_WARNINGS: 100

# Week 4
MAX_WARNINGS: 50

# Week 8
MAX_WARNINGS: 20

# Target (after cleanup sprint)
MAX_WARNINGS: 0
```

---

## Quick Reference

### Gate Priority Order

| Priority | Gate | Time | ROI |
|----------|------|------|-----|
| 1 | SwiftLint | ~30s | High — catches bugs |
| 2 | SwiftFormat | ~15s | Medium — consistency |
| 3 | Build (0 warnings) | ~2-5m | High — compiler catches issues |
| 4 | Unit Tests | ~5-15m | High — catches regressions |
| 5 | Coverage Check | ~1m | Medium — enforces testing |
| 6 | Static Analysis | ~5-10m | Medium — deep issues |

### Red Flags

| Smell | Problem | Fix |
|-------|---------|-----|
| Gates disabled for "urgent" PR | Culture problem | Gates are non-negotiable |
| 100% coverage requirement | Gaming metrics | 80-85% is optimal |
| All SwiftLint rules enabled | Too noisy | Curate impactful rules |
| Pre-commit takes > 30s | Devs skip it | Only fast checks locally |
| Different rules in CI vs local | Surprises | Same config everywhere |

### SwiftLint Rules Worth Enabling

| Rule | Why |
|------|-----|
| `force_unwrapping` | Prevents crashes |
| `implicitly_unwrapped_optional` | Prevents crashes |
| `empty_count` | Performance (O(1) vs O(n)) |
| `first_where` | Performance |
| `fatal_error_message` | Better crash logs |
| `unowned_variable_capture` | Prevents crashes |
| `unused_closure_parameter` | Code hygiene |

### SwiftLint Rules to Avoid

| Rule | Why Avoid |
|------|-----------|
| `explicit_type_interface` | Swift has inference for a reason |
| `file_types_order` | Team preference varies |
| `prefixed_toplevel_constant` | Outdated convention |
| `extension_access_modifier` | Rarely adds value |
