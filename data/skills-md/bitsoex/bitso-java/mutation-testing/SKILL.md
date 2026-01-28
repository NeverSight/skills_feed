---
name: mutation-testing
description: >
  Use PIT (Pitest) mutation testing to identify weak tests and improve test quality
  in Java projects. Finds tests that pass but don't actually verify behavior correctly.
  Use when improving test suite quality beyond line coverage metrics.
compatibility: Java projects using Gradle 8.x+ with JUnit 5 or Spock
metadata:
  version: "1.0.0"
  technology: java
  category: testing
  tags:
    - java
    - gradle
    - testing
    - mutation-testing
    - pitest
    - quality
---

# Mutation Testing

Use PIT mutation testing to identify tests that pass but don't verify behavior correctly.

## When to use this skill

- Improving test quality beyond line coverage metrics
- Finding weak test assertions that don't catch bugs
- Validating critical business logic has strong tests
- Setting up mutation testing in CI pipelines
- Analyzing which tests need strengthening

## Skill Contents

### Sections

- [When to use this skill](#when-to-use-this-skill) (L25-L32)
- [Quick Start](#quick-start) (L54-L90)
- [Key Concepts](#key-concepts) (L91-L116)
- [References](#references) (L117-L125)
- [Related Rules](#related-rules) (L126-L130)
- [Related Skills](#related-skills) (L131-L136)

### Available Resources

**📚 references/** - Detailed documentation
- [configuration](references/configuration.md)
- [improving tests](references/improving-tests.md)
- [intensity levels](references/intensity-levels.md)
- [troubleshooting](references/troubleshooting.md)

---

## Quick Start

### 1. Check readiness

```bash
bash java/scripts/check-pitest-readiness.sh
```

### 2. Apply PIT configuration

Copy `java/templates/pitest.gradle` to `gradle/pitest.gradle` and apply in `build.gradle`.

### 3. Run mutation testing

```bash
# QUICK level - fast feedback
./gradlew pitest -Ppitest.mutators=DEFAULTS

# STANDARD level - recommended
./gradlew pitest -Ppitest.mutators=STRONGER

# COMPREHENSIVE level - thorough
./gradlew pitest -Ppitest.mutators=ALL
```

### 4. Analyze results

```bash
open build/reports/pitest/index.html
```

Focus on **SURVIVED** mutants - these indicate weak tests.

### 5. Improve tests

Add specific assertions that kill the surviving mutants.

## Key Concepts

### Mutation Score vs Line Coverage

- **Line coverage**: Does your test execute the code?
- **Mutation score**: Does your test actually verify the code works correctly?

High line coverage with low mutation score = tests run code but don't verify results.

### Intensity Levels

| Level | Mutators | Use Case | Time |
|-------|----------|----------|------|
| QUICK | DEFAULTS (~11) | Initial analysis, CI | 1x |
| STANDARD | STRONGER (~14) | Regular improvement | 1.5x |
| COMPREHENSIVE | ALL (~30+) | Critical logic | 3-5x |

### Mutation Statuses

| Status | Meaning | Action |
|--------|---------|--------|
| Killed | Test detected mutation | Good |
| Survived | Test missed mutation | Improve test |
| No Coverage | No test covers code | Write test |
| Timed Out | Infinite loop | Usually OK |

## References

| Reference | Description |
|-----------|-------------|
| [references/intensity-levels.md](references/intensity-levels.md) | Detailed mutator descriptions |
| [references/improving-tests.md](references/improving-tests.md) | Patterns for killing mutants |
| [references/configuration.md](references/configuration.md) | PIT configuration options |
| [references/troubleshooting.md](references/troubleshooting.md) | Common issues and solutions |

## Related Rules

- `.cursor/rules/java-testing-guidelines.mdc` - Spock/JUnit patterns
- `.cursor/rules/java-jacoco-coverage.mdc` - Line coverage configuration

## Related Skills

| Skill | Purpose |
|-------|---------|
| [java-testing](../java-testing/SKILL.md) | Test configuration |
| [java-coverage](../java-coverage/SKILL.md) | JaCoCo coverage |
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → java/skills/mutation-testing/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

