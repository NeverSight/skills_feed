---
name: langfuse-prompt-upsert
description: Create or update Langfuse prompt with development label. Use when creating new prompts, updating existing prompts, or improving prompt content.
license: MIT
compatibility: Node.js 18+ (native fetch required)
metadata:
  author: neuradex
  category: observability
allowed-tools:
  - Bash(npx tsx *scripts/langfuse-prompt-upsert.ts*)
  - Bash(npx tsx *scripts/langfuse-prompt-view.ts*)
  - Read
  - Write
  - AskUserQuestion
---

# Langfuse Prompt Upsert

Create or update a Langfuse prompt and attach the `development` label.
- If the prompt does not exist: creates a new one (v1)
- If the prompt exists: creates a new version

## Setup

Set the following environment variables before use:

| Variable | Required | Description |
|----------|----------|-------------|
| `LANGFUSE_PUBLIC_KEY` | Yes | Langfuse public key |
| `LANGFUSE_SECRET_KEY` | Yes | Langfuse secret key |
| `LANGFUSE_HOST` or `LANGFUSE_BASE_URL` | No | Langfuse host URL (default: `https://us.cloud.langfuse.com`) |

## When to Use

- Creating a new prompt
- Improving/updating an existing prompt
- Changing prompt content

## Steps

### 1. Check Current Prompt (for updates)

```bash
npx tsx scripts/langfuse-prompt-view.ts <prompt-name> --label=development
```

### 2. Prepare New Prompt Content

Use AskUserQuestion to confirm or propose new prompt content.

### 3. Create/Update Prompt

**Method A: Pipe directly (recommended)**

```bash
cat << 'EOF' | npx tsx scripts/langfuse-prompt-upsert.ts <prompt-name>
Prompt content goes here...
EOF
```

**Method B: Via file**

```bash
# Save to /tmp/new-prompt.txt using the Write tool, then:
npx tsx scripts/langfuse-prompt-upsert.ts <prompt-name> /tmp/new-prompt.txt
```

### 4. Verify Result

```bash
npx tsx scripts/langfuse-prompt-view.ts <prompt-name> --label=development
```

## Template Variables

Use `$variableName` format for dynamic values in prompts:

| Variable | Purpose |
|----------|---------|
| `$title` | Title |
| `$content` | Main content |
| `$searchResult` | Search results |
| `$conversation` | Conversation history |
| `$userQuestion` | User's question |

Variables are replaced in code with `.replace('$title', value)`.

## Notes

- This skill only attaches the `development` label
- Attaching the `production` label should be done manually in the Langfuse UI
- The existing `development` label is automatically moved to the new version
