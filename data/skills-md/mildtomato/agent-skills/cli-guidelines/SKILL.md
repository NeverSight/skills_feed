---
name: cli-guidelines
description: Design and build well-crafted command-line interfaces following modern best practices. This skill should be used when creating CLI tools, adding commands/subcommands, implementing help text, handling errors, parsing arguments/flags, or improving CLI UX. Triggers on tasks involving command-line tools, terminal interfaces, argument parsing, error handling, or CLI design.
license: MIT
metadata:
  author: CLI Guidelines
  version: '1.0.0'
---

# CLI Design Guidelines

Comprehensive guide to designing command-line interfaces following modern best practices. Based on the [Command Line Interface Guidelines](https://clig.dev/). Prioritized by impact to guide CLI development and code review.

## When to Apply

Reference these guidelines when:

- Creating new CLI tools or adding commands/subcommands
- Implementing help text and error handling
- Parsing arguments and flags
- Designing interactive prompts
- Setting up configuration systems
- Improving CLI UX and output formatting
- Reviewing CLI code for best practices
- Refactoring existing command-line tools

## Rule Categories by Priority

| Priority | Category              | Impact      | Prefix         |
| -------- | --------------------- | ----------- | -------------- |
| 1        | The Basics            | CRITICAL    | `basics-`      |
| 2        | AI Agent Integration  | CRITICAL    | `agents-`      |
| 3        | Help & Documentation  | CRITICAL    | `help-`        |
| 4        | Output Formatting     | HIGH        | `output-`      |
| 5        | Error Handling        | HIGH        | `errors-`      |
| 6        | Arguments & Flags     | HIGH        | `args-`        |
| 7        | Interactivity         | HIGH        | `interactive-` |
| 8        | Signals & Control     | HIGH        | `signals-`     |
| 9        | Robustness            | MEDIUM-HIGH | `robustness-`  |
| 10       | Subcommands           | MEDIUM-HIGH | `subcommands-` |
| 11       | Configuration         | MEDIUM      | `config-`      |
| 12       | Future-proofing       | MEDIUM      | `future-`      |
| 13       | Naming & Distribution | LOW-MEDIUM  | `naming-`      |
| 14       | Documentation         | MEDIUM      | `help-`        |
| 15       | Analytics             | MEDIUM      | `analytics-`   |

## Quick Reference

### 1. The Basics (CRITICAL)

- `basics-use-parsing-library` - Use argument parsing library (don't roll your own)
- `basics-exit-codes` - Return 0 on success, non-zero on failure
- `basics-stdout-stderr` - Send output to stdout, messages/errors to stderr
- `basics-help-flags` - Support `-h` and `--help` flags
- `basics-full-flags` - Have full-length versions of all flags

### 2. AI Agent Integration (CRITICAL)

- `agents-json-required` - Always support --json for agent consumption
- `agents-structured-errors` - Provide structured error information
- `agents-exit-codes-documented` - Document all exit codes
- `agents-no-prompts-default` - Avoid interactive prompts, use flags
- `agents-yes-flag` - Provide --yes flag to skip confirmations
- `agents-progress-to-stderr` - Send progress to stderr, data to stdout
- `agents-deterministic-output` - Ensure deterministic, versioned output
- `agents-dry-run` - Provide --dry-run for safety
- `agents-help-machine-readable` - Make help text machine-readable

### 3. Help & Documentation (CRITICAL)

- `help-concise-default` - Display concise help when run with no args
- `help-lead-examples` - Lead with examples in help text
- `help-suggest-corrections` - Suggest corrections for typos

### 4. Output Formatting (HIGH)

- `output-tty-detection` - Check if TTY before using colors/animations
- `output-json-flag` - Support `--json` for machine-readable output
- `output-plain-flag` - Support `--plain` for script-friendly output
- `output-state-changes` - Tell the user when you change state
- `output-pager` - Use a pager for long output

### 5. Error Handling (HIGH)

- `errors-rewrite-for-humans` - Catch errors and rewrite for humans
- `errors-signal-to-noise` - Maintain signal-to-noise ratio in error output
- `errors-important-info-end` - Put important info at end of output
- `errors-exit-code-mapping` - Map exit codes to failure modes

### 6. Arguments & Flags (HIGH)

- `args-prefer-flags` - Prefer flags over positional arguments
- `args-standard-names` - Use standard flag names (`-f/--force`, `-n/--dry-run`)
- `args-no-secrets-flags` - Don't read secrets from flags (use files or stdin)
- `args-stdin-stdout` - Accept `-` to read from stdin / write to stdout
- `args-order-independent` - Make flags order-independent

### 7. Interactivity (HIGH)

- `interactive-tty-check` - Only prompt if stdin is a TTY
- `interactive-no-input-flag` - Support `--no-input` to disable prompts
- `interactive-password-no-echo` - Don't echo passwords as user types

### 8. Signals & Control (HIGH)

- `signals-exit-on-ctrl-c` - Exit immediately on Ctrl-C
- `signals-crash-only-design` - Design for crash-only operation

### 9. Robustness (MEDIUM-HIGH)

- `robustness-100ms-response` - Print something within 100ms
- `robustness-progress-indicators` - Show progress for long operations
- `robustness-validate-early` - Validate input early, fail fast
- `robustness-idempotent` - Make operations idempotent/recoverable
- `robustness-network-timeouts` - Set timeouts on network operations

### 10. Subcommands (MEDIUM-HIGH)

- `subcommands-consistency` - Be consistent across subcommands (same flags, output)
- `subcommands-consistent-verbs` - Use consistent verbs (create/get/update/delete)
- `subcommands-no-abbreviations` - Don't allow arbitrary abbreviations
- `subcommands-no-catch-all` - Don't have catch-all subcommands

### 11. Configuration (MEDIUM)

- `config-precedence` - Follow precedence: Flags > Env vars > Project > User > System
- `config-xdg-spec` - Follow XDG Base Directory spec for config locations

### 12. Future-proofing (MEDIUM)

- `future-additive-changes` - Keep changes additive (add flags, don't change behavior)

### 13. Naming & Distribution (LOW-MEDIUM)

- `naming-simple-memorable` - Use simple, memorable, lowercase command names
- `naming-distribute-single-binary` - Distribute as single binary when possible

### 14. Help & Documentation (MEDIUM)

- `help-web-documentation` - Provide web-based documentation

### 15. Analytics (MEDIUM)

- `analytics-no-phone-home` - Don't phone home without consent

## Philosophy

These are the fundamental principles of good CLI design:

1. **Human-first design** - Design for humans, optimize for machines second
2. **Simple parts that work together** - Composable via stdin/stdout/stderr, exit codes, JSON
3. **Consistency across programs** - Follow existing patterns users already know
4. **Saying (just) enough** - Not too much output, not too little
5. **Ease of discovery** - Help users learn through suggestions, examples, clear errors
6. **Conversation as the norm** - CLI interaction is iterative—guide the user through it
7. **Robustness** - Handle failures gracefully, be responsive, feel solid
8. **Empathy** - Be on the user's side, help them succeed
9. **Chaos** - Know when to break the rules—do so with intention

## Structure

This skill contains:

- **`rules/`** - Focused, actionable rules
  - Each rule has frontmatter (title, impact, tags)
  - Includes incorrect/correct code examples
  - TypeScript/JavaScript examples with modern libraries
- **`references/`** - Comprehensive topic guides (for deeper context)
  - Background documentation and detailed explanations
  - Loaded by agents only when deeper understanding is needed
- **`AGENTS.md`** - Complete compiled guide (auto-generated from rules)
  - All rules in one document
  - Full table of contents
  - Searchable reference

## How to Use

Read individual rule files for specific guidance:

```
rules/basics-use-parsing-library.md
rules/agents-json-required.md
rules/output-tty-detection.md
```

Each rule file contains:

- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and implementation details

For deeper background, see reference files:

```
references/philosophy.md
references/basics.md
```

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`

## Common Argument Parsing Libraries

| Language       | Libraries              |
| -------------- | ---------------------- |
| Node           | oclif, commander       |
| Go             | Cobra, urfave/cli      |
| Python         | Click, Typer, argparse |
| Rust           | clap                   |
| Ruby           | TTY                    |
| Java           | picocli                |
| Swift          | swift-argument-parser  |
| Multi-platform | docopt                 |

## Further Reading

- [Command Line Interface Guidelines](https://clig.dev/)
- [The Unix Programming Environment](https://en.wikipedia.org/wiki/The_Unix_Programming_Environment)
- [POSIX Utility Conventions](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html)
- [12 Factor CLI Apps](https://medium.com/@jdxcode/12-factor-cli-apps-dd3c227a0e46)
