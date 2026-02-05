---
name: cli-design-guidelines
description: Design and UX guidance for command-line tools and scripts, based on the Command Line Interface Guidelines (clig.dev) and the Chinese translation at clig.onev.dev.
---

# CLI Design Guidelines

Use this skill when designing, reviewing, or refactoring command-line tools or scripts. Emphasize human-first UX, composability, clear help/output/error behaviors, and predictable flags/subcommands.

## Source & Attribution

Based on the Command Line Interface Guidelines (clig.dev) and the Chinese translation at clig.onev.dev. Licensed under CC BY-SA 4.0. Include attribution when copying or adapting text.

## When to Use

- Designing a new CLI or script interface
- Adding flags, subcommands, config, or env support
- Improving help, output, and error messages
- Making tools more composable in shell pipelines
- Reducing ambiguity and surprises in CLI UX

## Design Philosophy (Condensed)

- Human-first: optimize for humans, not just programmatic callers.
- Composable: small tools with clear interfaces; respect stdin/stdout/stderr.
- Consistent: reuse familiar conventions to reduce cognitive load.
- Say just enough: balance silence vs noisy output.
- Discoverable: help and examples make features easy to find.
- Conversational: guide the user through retries and multi-step flows.
- Robust: handle errors gracefully and look reliable.
- Empathy + chaos: expect misuse and messy real-world environments.

## Practical Guidelines

### Help & Docs

- Always support `-h` and `--help`; keep help scannable.
- Provide usage, options, examples, and key subcommands.
- Avoid raw escape garbage in non-TTY output.

### Output

- Prefer short success output over silence for humans.
- Provide `-q/--quiet` to suppress non-essential output.
- If state changes, explain what changed and how to inspect it.
- Suggest next commands in multi-step workflows.
- For long work, show progress; keep logs usable if errors occur.

### Errors

- Rewrite errors for humans; include an actionable hint.
- Keep signal high; group repetitive errors.
- Use non-zero exit codes on failure; stderr for errors.

### Args & Flags

- Prefer flags over positional args for clarity and future-proofing.
- Provide long-form flags; short only for common ones.
- Use standard flag names when possible (`--help`, `--json`, `--dry-run`, `--quiet`).
- Avoid ambiguous ordering; allow flags before/after subcommands if possible.
- Don’t force interactive input; always allow flags/args and support `--no-input`.

### Interactivity

- Only prompt when stdin is a TTY; otherwise error with guidance.
- Provide explicit opt-out (`--no-input`) and safe defaults.
- For dangerous actions, confirm appropriately and support `--force`/`--confirm`.

### Subcommands

- Use subcommands to reduce complexity; keep flags consistent.
- Prefer `noun verb` naming; avoid confusing near-duplicates.

### Robustness

- Validate inputs early; fail before side effects.
- Show feedback quickly; add progress for slow ops.
- Be explicit when crossing boundaries (network/filesystem).
- Add timeouts and recoverability for transient failures.

## CLI Review Checklist

- Help: readable, complete, examples included, `-h/--help` supported
- Output: concise by default, `--quiet` optional, progress for long tasks
- Errors: actionable hints, stderr, non-zero exit codes
- Flags: standard names, long + short where appropriate, predictable ordering
- Interactivity: TTY-only prompts, `--no-input`, safe confirmations
- Subcommands: consistent naming and flag behavior
- Composability: stdout machine-friendly; stderr for logs

## Examples (Templates)

### Help (human-scannable)
```
usage: mytool <command> [options]

commands:
  init      bootstrap workspace
  sync      fetch and apply updates

options:
  -h, --help        show help
  -q, --quiet       suppress non-essential output
  --json            machine-readable output

examples:
  mytool init --config ./tool.yaml
  mytool sync --dry-run
```

### Error (actionable)
```
error: cannot write to config.yml
hint: run `chmod +w config.yml` or pass --config <path>
```

### Progress
```
fetching updates... 42% (12/28)
```

## Reference Links

- clig.onev.dev (Chinese translation)
- clig.dev (original)
- CC BY-SA 4.0 license
