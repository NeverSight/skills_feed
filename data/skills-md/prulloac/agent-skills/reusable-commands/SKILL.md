---
name: reusable-commands
description: Create reusable commands for OpenCode or GitHub Copilot. Use this skill when a user wants to automate a repetitive prompt or task by creating a custom slash command.
---

# Reusable Commands Skill

This skill helps you create custom, reusable commands and prompts for either OpenCode or GitHub Copilot.

## References

- [OpenCode Commands Documentation](references/opencode-commands.md)
- [GitHub Copilot Prompt Files Documentation](references/copilot-prompt-files.md)
- [Templates](assets/) - Example templates for creating commands

## Workflow

1.  **Identify Target Agent:** Determine if the command is intended for OpenCode or GitHub Copilot.
    -   If the user mentions `/` commands in the TUI, it's likely OpenCode.
    -   If the user mentions `.prompt.md` files or VS Code Copilot Chat, it's Copilot.
    -   **If ambiguous, ask the user: "Is this reusable command intended for OpenCode or GitHub Copilot?"**

2.  **Gather Command Details:**
    -   **Command Name:** What will the user type to trigger it (e.g., `review`, `test`)?
    -   **Description:** A short summary of what it does.
    -   **Prompt Body:** The actual instructions for the AI. This can and should be an improved version of the user's original prompt, optimized for reuse.
    -   **Optional Parameters:** Specific agent, model, or tools.

3.  **Apply Correct Format:**
    -   **OpenCode:** Use `.opencode/commands/<name>.md`. Supports `$ARGUMENTS`, `!command` (shell), and `@filename`.
    -   **Copilot:** Use `.github/prompts/<name>.prompt.md`. Supports `${selection}`, `${file}`, and `[label](path)`.

4.  **Create the File:**
    -   **OpenCode:** Create `.opencode/commands/<name>.md`.
    -   **Copilot:** Create `.github/prompts/<name>.prompt.md`.

## Format Details

### OpenCode Commands (`.md`)
Frontmatter: `description` (required), `agent`, `model`, `subtask`.
Syntax:
- `$ARGUMENTS`: Full input.
- `!command`: Shell command output.
- `@filename`: File content.

See [references/opencode-commands.md](references/opencode-commands.md) for detailed documentation.

### Copilot Prompt Files (`.prompt.md`)
Frontmatter: `description` (required), `argument-hint`, `agent`, `model`, `tools`.
Syntax:
- `${selection}`: Editor selection.
- `[label](path)`: Specific file content.

See [references/copilot-prompt-files.md](references/copilot-prompt-files.md) for detailed documentation.

## Examples

### Creating an OpenCode "review" command
"Create an opencode command called 'review' that reviews the staged changes."
-> Create `.opencode/commands/review.md`:
```markdown
---
description: Review staged changes
agent: plan
---
Review the current staged changes:
!`git diff --cached`
```

### Creating a Copilot "doc" command
"Create a copilot prompt to document the selected function."
-> Create `.github/prompts/doc.prompt.md`:
```markdown
---
description: Generate documentation for the selection
argument-hint: Specify the style (e.g., JSDoc, Google)
---
Generate ${input:style} documentation for this code:
${selection}
```

## Verification

After creating the command file:
1.  **Check File Path:** Verify the file exists at the correct location (`.opencode/commands/` or `.github/prompts/`).
2.  **Verify Content:** Ensure the YAML frontmatter is properly formatted and the prompt body is present.
3.  **Test Command (Optional):** If possible, run the command (e.g., `/name` in TUI) to ensure it triggers correctly.
