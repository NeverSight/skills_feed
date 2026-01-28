---
name: baoyu-danger-x-to-markdown
description: Converts X (Twitter) tweets and articles to markdown with YAML front matter. Uses reverse-engineered API requiring user consent. Use when user mentions "X to markdown", "tweet to markdown", "save tweet", or provides x.com/twitter.com URLs for conversion.
---

# X to Markdown

Converts X content to markdown:
- Tweets/threads → Markdown with YAML front matter
- X Articles → Full content extraction

## Script Directory

Scripts located in `scripts/` subdirectory.

**Path Resolution**:
1. `SKILL_DIR` = this SKILL.md's directory
2. Script path = `${SKILL_DIR}/scripts/main.ts`

## Consent Requirement

**Before any conversion**, check and obtain consent.

### Consent Flow

**Step 1**: Check consent file

```bash
# macOS
cat ~/Library/Application\ Support/baoyu-skills/x-to-markdown/consent.json

# Linux
cat ~/.local/share/baoyu-skills/x-to-markdown/consent.json
```

**Step 2**: If `accepted: true` and `disclaimerVersion: "1.0"` → print warning and proceed:
```
Warning: Using reverse-engineered X API. Accepted on: <acceptedAt>
```

**Step 3**: If missing or version mismatch → display disclaimer:
```
DISCLAIMER

This tool uses a reverse-engineered X API, NOT official.

Risks:
- May break if X changes API
- No guarantees or support
- Possible account restrictions
- Use at your own risk

Accept terms and continue?
```

Use `AskUserQuestion` with options: "Yes, I accept" | "No, I decline"

**Step 4**: On accept → create consent file:
```json
{
  "version": 1,
  "accepted": true,
  "acceptedAt": "<ISO timestamp>",
  "disclaimerVersion": "1.0"
}
```

**Step 5**: On decline → output "User declined. Exiting." and stop.

## Preferences (EXTEND.md)

Use Bash to check EXTEND.md existence (priority order):

```bash
# Check project-level first
test -f .baoyu-skills/baoyu-danger-x-to-markdown/EXTEND.md && echo "project"

# Then user-level (cross-platform: $HOME works on macOS/Linux/WSL)
test -f "$HOME/.baoyu-skills/baoyu-danger-x-to-markdown/EXTEND.md" && echo "user"
```

┌────────────────────────────────────────────────────────────┬───────────────────┐
│                            Path                            │     Location      │
├────────────────────────────────────────────────────────────┼───────────────────┤
│ .baoyu-skills/baoyu-danger-x-to-markdown/EXTEND.md         │ Project directory │
├────────────────────────────────────────────────────────────┼───────────────────┤
│ $HOME/.baoyu-skills/baoyu-danger-x-to-markdown/EXTEND.md   │ User home         │
└────────────────────────────────────────────────────────────┴───────────────────┘

┌───────────┬───────────────────────────────────────────────────────────────────────────┐
│  Result   │                                  Action                                   │
├───────────┼───────────────────────────────────────────────────────────────────────────┤
│ Found     │ Read, parse, apply settings                                               │
├───────────┼───────────────────────────────────────────────────────────────────────────┤
│ Not found │ Use defaults                                                              │
└───────────┴───────────────────────────────────────────────────────────────────────────┘

**EXTEND.md Supports**: Default output directory | Output format preferences

## Usage

```bash
npx -y bun ${SKILL_DIR}/scripts/main.ts <url>
npx -y bun ${SKILL_DIR}/scripts/main.ts <url> -o output.md
npx -y bun ${SKILL_DIR}/scripts/main.ts <url> --json
```

## Options

| Option | Description |
|--------|-------------|
| `<url>` | Tweet or article URL |
| `-o <path>` | Output path |
| `--json` | JSON output |
| `--login` | Refresh cookies only |

## Supported URLs

- `https://x.com/<user>/status/<id>`
- `https://twitter.com/<user>/status/<id>`
- `https://x.com/i/article/<id>`

## Output

```markdown
---
url: https://x.com/user/status/123
author: "Name (@user)"
tweet_count: 3
---

Content...
```

**File structure**: `x-to-markdown/{username}/{tweet-id}.md`

## Authentication

1. **Environment variables** (preferred): `X_AUTH_TOKEN`, `X_CT0`
2. **Chrome login** (fallback): Auto-opens Chrome, caches cookies locally

## Extension Support

Custom configurations via EXTEND.md. See **Preferences** section for paths and supported options.
