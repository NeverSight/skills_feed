---
name: review-skill
description: "Review new skills for claude-skills-library standards. Use when adding new skills to verify they meet quality and structure requirements."
---

# Skill Review Checklist

Review new skills before adding to the library.

## File Structure Check

| Required | File | Purpose |
|----------|------|---------|
| ✅ | `skill.md` | Main skill file (lowercase!) |
| ⚠️ | `SETUP.md` | Setup guide (if skill needs API/config) |
| ⚠️ | `scripts/` | Helper scripts (if needed) |
| ⚠️ | `.env.example` | Example env file (never actual credentials!) |

## skill.md Requirements

### Frontmatter (YAML header)

```yaml
---
name: skill-name           # Required: kebab-case
description: "..."         # Required: trigger phrases
setup: "./SETUP.md"        # If SETUP.md exists
enhancedBy:                # Optional: complementary skills
  - other-skill: "Benefit description. Without it: fallback behavior"
usedBy:                    # Optional: for helper skills
  - parent-skill
---
```

### Content Guidelines

- **Concise** - Under 100 lines ideal, max 150
- **Workflow focused** - How to use, not how to set up
- **Examples** - Quick command examples
- **No setup instructions** - Those go in SETUP.md

## SETUP.md Requirements (if needed)

- Step-by-step setup guide
- API/account creation instructions
- Credential configuration (.env)
- Test commands to verify setup
- Troubleshooting table

## Docs Site Sync

After adding a skill, update `docs/index.html`:

1. Add skill card in `skills-grid` section
2. If skill has `enhancedBy`, add the combo badge:
```html
<div class="skill-combo" style="...">
  <span style="color: var(--green-primary);">🔗 עובד טוב יותר עם:</span>
  <span style="color: var(--text-secondary);">skill-a, skill-b</span>
</div>
```
3. Create `docs/skills/[skill-name].html` guide page
4. Create `docs/downloads/[skill-name].zip` for download

## Review Checklist

Before approving a new skill:

- [ ] `skill.md` exists (lowercase)
- [ ] Frontmatter has `name` and `description`
- [ ] `setup: "./SETUP.md"` if SETUP.md exists
- [ ] Content is under 150 lines
- [ ] No credentials or API keys in any file
- [ ] `.gitignore` includes `.env` and sensitive files
- [ ] If scripts exist, they have `--dry-run` option
- [ ] Docs site updated with skill card
- [ ] Download ZIP created

## Quality Standards

### Good Descriptions (trigger phrases)

```yaml
# Good - tells Claude when to use
description: "Send WhatsApp messages. Use when user says 'send message', 'whatsapp', 'הודעה'."

# Bad - too vague
description: "WhatsApp integration"
```

### Good enhancedBy Format

```yaml
# Good - explains benefit and fallback
enhancedBy:
  - get-contact: "Auto-lookup contact by name. Without it: ask user for phone directly"

# Bad - no context
enhancedBy:
  - get-contact
```

## Command

Run review on a skill folder:

```bash
# Check structure
ls -la skills/[skill-name]/

# Check frontmatter
head -20 skills/[skill-name]/skill.md

# Check line count
wc -l skills/[skill-name]/skill.md
```
