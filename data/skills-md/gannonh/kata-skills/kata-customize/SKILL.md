---
name: kata-customize
description: Manage template overrides for customizing Kata output formats. List available templates, copy defaults for local editing, edit overrides, validate template schemas. Triggers include "customize template", "override template", "edit template", "template overrides", "list templates", "show templates", "template customization", "manage templates", "what templates can I customize", "template schema", "custonmize Kata", "custom config".
metadata:
  version: "1.9.0"
---

<objective>
Manage template overrides for customizing Kata output formats.

Templates control the structure of planning artifacts (plans, summaries, UAT sessions, verification reports, changelogs). Override a template to change how Kata generates these files for your project.

Operations: list, copy, edit, validate.
</objective>

<context>
$ARGUMENTS
</context>

<process>

## 1. Validate Environment

```bash
ls .planning/ 2>/dev/null
```

**If not found:** Error — run `/kata-new-project` first.

## 2. Determine Operation

Parse `$ARGUMENTS` for the operation:

- If contains "list" or "show" or no arguments → **list** operation
- If contains "copy" → **copy** operation (extract template name from remaining args)
- If contains "edit" or "modify" or "change" → **edit** operation (extract template name)
- If contains "validate" or "check" or "drift" → **validate** operation

If unclear, present AskUserQuestion:

```
What would you like to do?

1. **List templates** — See all customizable templates and their override status
2. **Copy a template** — Copy a default template for local customization
3. **Edit a template** — Modify an existing template override
4. **Validate overrides** — Check all overrides for missing required fields
```

## 3. List Operation

Run the discovery script:

```bash
bash ./scripts/list-templates.sh
```

Parse the JSON output. Display:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Kata > CUSTOMIZABLE TEMPLATES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Template | Used By | Controls | Status |
| --- | --- | --- | --- |
| summary-template.md | kata-execute-phase | Phase completion docs | {override / default} |
| plan-template.md | kata-plan-phase | Phase plan structure | {override / default} |
| UAT-template.md | kata-verify-work | UAT session format | {override / default} |
| verification-report.md | kata-verify-work | Verification report format | {override / default} |
| changelog-entry.md | kata-complete-milestone | Changelog entry format | {override / default} |

Override location: `.planning/templates/`

To customize a template:
  `/kata-customize copy summary-template.md`
```

After displaying the list, stop. Do not proceed to another operation.

## 4. Copy Operation

Requires a template name argument. If not provided, run list operation first, then ask user to select.

**Step 4a: Resolve the default template path**

```bash
RESOLVE_SCRIPT="../kata-execute-phase/scripts/resolve-template.sh"
DEFAULT_PATH=$(bash "$RESOLVE_SCRIPT" "$TEMPLATE_NAME" 2>&1)
```

If the resolve script exits non-zero, the template name is invalid. Display the error and stop.

**Step 4b: Check for existing override**

```bash
[ -f ".planning/templates/$TEMPLATE_NAME" ] && echo "EXISTS" || echo "NEW"
```

If EXISTS, ask user via AskUserQuestion:

```
An override for `{TEMPLATE_NAME}` already exists at `.planning/templates/{TEMPLATE_NAME}`.

1. **Overwrite** — Replace with default (your customizations will be lost)
2. **Cancel** — Keep current override
```

If user selects Cancel, stop.

**Step 4c: Copy the default**

```bash
mkdir -p .planning/templates
cp "$DEFAULT_PATH" ".planning/templates/$TEMPLATE_NAME"
```

**Step 4d: Confirm**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Kata > TEMPLATE COPIED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Copied default to: `.planning/templates/{TEMPLATE_NAME}`

Edit the file to customize, then validate:
  `/kata-customize validate`
```

## 5. Edit Operation

Requires a template name argument. If not provided, run list operation to show overrides, then ask which to edit.

**Step 5a: Check override exists**

```bash
[ -f ".planning/templates/$TEMPLATE_NAME" ] && echo "EXISTS" || echo "MISSING"
```

If MISSING, ask user via AskUserQuestion:

```
No override exists for `{TEMPLATE_NAME}`.

1. **Copy and edit** — Copy the default first, then edit
2. **Cancel** — Do nothing
```

If user selects "Copy and edit", run step 4c first.

**Step 5b: Read current content**

Read `.planning/templates/{TEMPLATE_NAME}` and display the current content to the user.

**Step 5c: Accept modifications**

Ask the user what they want to change. Two paths:

- If user describes specific changes ("change heading X to Y", "add field Z"), apply the edits to the file using Edit tool and write the updated content.
- If user says they will edit externally ("let me edit it", "I'll do it in my editor"), acknowledge and offer to validate when they return.

**Step 5d: Validate after edit**

After writing changes (or when user returns from external editing), run single-template validation:

```bash
bash ../kata-doctor/scripts/check-template-drift.sh
```

If drift warnings mention the edited template, display them. If clean, display:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Kata > TEMPLATE VALID
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

`{TEMPLATE_NAME}` has all required fields. Override is active.
```

## 6. Validate Operation

Run validation on all overrides:

```bash
DRIFT_OUTPUT=$(bash ../kata-doctor/scripts/check-template-drift.sh 2>/dev/null)
```

If `DRIFT_OUTPUT` is empty and `.planning/templates/` exists with .md files:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Kata > ALL TEMPLATES VALID
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

All template overrides pass schema validation.
```

If `DRIFT_OUTPUT` is empty and no overrides exist:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Kata > NO OVERRIDES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

No template overrides found at `.planning/templates/`.

To create an override:
  `/kata-customize copy summary-template.md`
```

If `DRIFT_OUTPUT` has content (warnings):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Kata > TEMPLATE DRIFT DETECTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{DRIFT_OUTPUT}

To fix, edit the override or reset to default:
  `/kata-customize edit {template-name}`
  `/kata-customize copy {template-name}` (resets to default)
```

</process>

<success_criteria>

- [ ] Templates listed with descriptions and override status
- [ ] Default copied to .planning/templates/ with overwrite protection
- [ ] Edit operation reads current content and applies user changes
- [ ] Validation runs after edit and reports missing fields
- [ ] All operations use existing infrastructure (resolve-template.sh, check-template-drift.sh)
- [ ] Skill responds to natural language triggers
      </success_criteria>
