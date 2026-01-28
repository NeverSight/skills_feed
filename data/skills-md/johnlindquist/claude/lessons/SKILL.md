---
name: lessons
description: Capture and review lessons learned from coding sessions. Use to record insights, read past lessons, and improve over time.
---

# Lessons Learned

Capture insights and learn from past experiences.

## Capture Patterns

### Quick Lesson Capture

When you learn something valuable during a session:

```bash
# Write to lessons file
cat >> ~/.claude/lessons.md << 'EOF'

## [Date] - [Topic]

**Context:** What were you doing?
**Lesson:** What did you learn?
**Application:** When to apply this?

EOF
```

### Structured Lesson

```markdown
## 2024-01-15 - TypeScript Generic Constraints

**Context:**
Building a type-safe form library, struggled with generic types.

**Problem:**
Generic function wasn't narrowing types correctly.

**Solution:**
Use `extends` constraints to narrow:
```typescript
function getValue<T extends { value: unknown }>(obj: T): T['value'] {
  return obj.value;
}
```

**Lesson:**
TypeScript generics need explicit constraints for type narrowing.

**Tags:** #typescript #generics #types
```

## Lesson Categories

### Bug Lessons

```markdown
## Bug: [Brief description]

**Symptom:** What happened
**Root Cause:** Why it happened
**Fix:** How to fix
**Prevention:** How to avoid in future
**Time Cost:** How long to debug (motivation to remember!)
```

### Pattern Lessons

```markdown
## Pattern: [Name]

**When to use:** Situations where this applies
**How to implement:** Basic structure
**Gotchas:** Common mistakes
**Example:** Working code
```

### Tool Lessons

```markdown
## Tool: [Name]

**What it does:** Brief description
**Key commands:** Most useful commands
**Gotchas:** Things that trip people up
**Alternatives:** Other options
```

## Review Practices

### Daily Review

```bash
# Review recent lessons
tail -100 ~/.claude/lessons.md

# Search for topic
grep -A 10 "typescript" ~/.claude/lessons.md
```

### Weekly Audit

```bash
gemini -m pro -o text -e "" "Review these lessons from the past week:

$(tail -500 ~/.claude/lessons.md)

1. What patterns emerge?
2. What mistakes keep recurring?
3. What should be turned into automation?
4. What needs deeper study?"
```

### Before Starting Work

```bash
# Get relevant lessons
TOPIC="authentication"
grep -B 2 -A 10 -i "$TOPIC" ~/.claude/lessons.md
```

## Automation from Lessons

When a lesson appears multiple times, automate it:

### Create Git Hook

```bash
# Lesson: Always run tests before commit
# → Create pre-commit hook

cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
npm test || exit 1
EOF
chmod +x .git/hooks/pre-commit
```

### Create Snippet

```bash
# Lesson: This pattern is useful
# → Save as snippet

cat > ~/.claude/snippets/async-error-handling.ts << 'EOF'
async function safeAsync<T>(promise: Promise<T>): Promise<[T, null] | [null, Error]> {
  try {
    const result = await promise;
    return [result, null];
  } catch (error) {
    return [null, error as Error];
  }
}
EOF
```

### Create Checklist

```bash
# Lesson: Keep forgetting these steps
# → Create checklist

cat > ~/.claude/checklists/pr-review.md << 'EOF'
# PR Review Checklist
- [ ] Tests pass
- [ ] No console.logs
- [ ] Types are explicit
- [ ] Error handling present
- [ ] Documentation updated
EOF
```

## AI-Assisted Learning

### Extract Lessons from Session

```bash
gemini -m pro -o text -e "" "Extract lessons learned from this coding session:

[Paste conversation or summary]

For each lesson:
1. What was learned
2. When it applies
3. How to remember it"
```

### Connect Lessons

```bash
gemini -m pro -o text -e "" "Find connections between these lessons:

$(cat ~/.claude/lessons.md)

1. What themes emerge?
2. What knowledge gaps exist?
3. What should be studied next?"
```

### Generate Quiz

```bash
gemini -m pro -o text -e "" "Create a quiz from these lessons:

$(tail -1000 ~/.claude/lessons.md)

Generate 5 questions that test understanding of key concepts."
```

## Storage Options

### File-based

```bash
# Single file
~/.claude/lessons.md

# By date
~/.claude/lessons/2024-01.md

# By topic
~/.claude/lessons/typescript.md
~/.claude/lessons/git.md
```

### Memory Integration

```bash
# Save to basic-memory
basic-memory tool write-note \
  --title "Lesson: TypeScript Generics" \
  --folder "lessons" \
  --content "$(cat lesson.md)" \
  --tags "lesson,typescript"
```

## Best Practices

1. **Capture immediately** - Don't wait, you'll forget
2. **Be specific** - Include code examples
3. **Note the cost** - Time spent motivates remembering
4. **Review regularly** - Lessons fade without review
5. **Automate repeated** - Turn lessons into tools
6. **Tag consistently** - Makes searching easier
7. **Connect to context** - When does this apply?
