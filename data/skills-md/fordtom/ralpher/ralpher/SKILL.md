---
name: ralpher
description: Generate Ralph loop scaffolding for autonomous codex workflows. Use when user asks to set up a ralph loop, scaffold ralph, or configure autonomous development.
allowed-tools: Read, create_file, edit_file
---

# Ralph Loop Setup

Generate scaffolding for running codex in an autonomous while loop.

## Usage

When asked to set up a ralph loop, create the following 4 files. Replace `[SPEC_FILES]` with the spec filenames provided by user. Configure MAX_ITERATIONS as requested.

### ralph.sh

```bash
#!/bin/bash
set -e

MAX_ITERATIONS=${1:-50}
STATUS_FILE="status.md"

for ((i = 1; i <= MAX_ITERATIONS; i++)); do
    echo "=== Iteration $i/$MAX_ITERATIONS ==="

    codex exec "$(cat prompt.md)" --model gpt-5.2-codex --full-auto --config model_reasoning_effort="xhigh"

    if [[ -f "summary.md" ]]; then
        echo "--- Summary: $(cat summary.md)"
    fi

    STATUS=$(head -1 "$STATUS_FILE" | grep -oE '(Done|Blocked|In Progress)')

    if [[ "$STATUS" == "Done" ]]; then
        echo "✅ Complete after $i iterations"
        exit 0
    elif [[ "$STATUS" == "Blocked" ]]; then
        echo "🚫 Blocked after $i iterations - manual intervention needed"
        exit 1
    fi

    echo "Status: $STATUS - continuing..."
done

echo "⚠️ Max iterations ($MAX_ITERATIONS) reached"
exit 1
```

Make executable with `chmod +x ralph.sh`.

### prompt.md

```markdown
Study [SPEC_FILES]
Study status.md for previous work and memory

Pick the most important incomplete task and work on it. Run the full quality gate (typecheck, lint, tests, format). If you learn something important for future work, add it to status.md. Commit when done.

Once finished, overwrite summary.md with a one-line summary.

If all tasks complete, set Status to 'Done'. If stuck on something impossible, set Status to 'Blocked'.

IMPORTANT:

- Follow any/all guidelines in AGENTS.md/CLAUDE.md
- author property-based tests or unit tests, whichever is better suited
```

### status.md

```markdown
Status: In Progress

## Memory
```

### summary.md

Create empty.
