---
name: project-teacher
description: Generates a detailed project explanation and retrospective (FOR_USER.md) to help the user learn from the project. Use this skill when the user asks to explain the project, asks "what did we just build?", or invokes the skill to generate a learning resource after a coding session.
metadata:
    author: nweii
    version: "1.0.0"
    inspo: https://x.com/zarazhangrui/status/2015057205800980731
---

# Project Teacher

Generate a detailed explanation of the current project or task, focusing on the "why" and "how" to help the user learn.

## Usage

When triggered, generate a markdown file containing the learning resource.

### 1. Check for Existing Documents (Synchronization)

Before generating a new file, search the output directory (default: `learning/`) for existing documents related to the current project.

*   **If a match is found**: Ask the user: _"I found an existing learning doc '[Filename]'. Do you want to **update** it or create a **new** snapshot?"_
*   **If User chooses Update**:
    1.  **Rename**: Updates the suffix date to **today's date** (e.g., `API_Layout - 2024-03-25.md`) to reflect freshness.
    2.  **Metadata**: Update the `last` and `commit` fields in the frontmatter.
    3.  **Content**: Rewrite sections that are outdated, but **preserve** valuable historical context if it still applies.
    4.  **Log**: Add a line to a `## Version history` section at the bottom (create one if missing).
*   **If User chooses New / No match found**: Create a new file.

### 2. Output Location

1.  **Check for user preference**: If the user specified a location (e.g., "save to my vault"), use that.
    *   **Obsidian / External Vaults**: If saving to an external Obsidian vault, first check its root or `.cursor/` / `.claude/` folders for applicable context files. These files often contain specific instructions for how to save and format notes in that system. **Delegate to those instructions** if they exist.
2.  **Default Location**: If no location is specified, use a directory named `learning/` in the project root.
    *   Create the `learning/` directory if it doesn't exist.
    *   **CRITICAL**: Check if `learning/` is in `.gitignore`. If not, add it to `.gitignore` to ensure these personal documents are not committed to shared repositories.
3.  **File Naming**: Name the file `[Descriptive title] - [YYYY-MM-DD].md`.
    *   **Structure**: `[Topic or Component] - [Date].md`. The leading part should be semantic and descriptive of *what* is being explained.
    *   **Examples**:
        *   `Authentication system walkthrough - 2024-03-25.md`
        *   `Recipe parser logic - 2024-03-25.md`
        *   `Project Teacher overview - 2024-03-25.md`

### 3. File Structure & Metadata Header
Use YAML frontmatter for machine-readable status, and a callout for human context.

```markdown
---
last: [YYYY-MM-DD]
commit: [Current Git Commit Hash or "N/A"]
tags: [project-teacher, learning, ...]
---

# [Descriptive title in sentence case]

> [!NOTE]
> **Context**: [Brief description, e.g., "Updated after migration to v2"]
> _This document reflects the system state at the time of the last update._

## Code index
*   [MainController.ts](path/to/MainController.ts) - Handles the core logic for...
*   [UserAuth.ts](path/to/UserAuth.ts) - Manages session state.
*   [api/endpoints/](path/to/api/endpoints/) - API route definitions.

## 1. Project overview
[Explain the whole project in plain language as an expert tutor. What did we just build?]

## 2. Architecture and logic
[Use ASCII diagrams or Mermaid charts here to visualize how data flows or how components interact.]

## 3. Key technical decisions
[Explain "why" technical decisions were made.]

### Trade-offs and alternatives
[Explicitly mention what alternatives were considered and why they were rejected. e.g., "Considered using Redux, but opted for React Context because..."]

---
## Version history
*   **[YYYY-MM-DD]**: [Brief note on what changed, e.g. "Initial creation"]
*   **[YYYY-MM-DD]**: [e.g. "Updated diagram to reflect new caching layer"]

## Reflection questions
*   [Question 1 asking about a specific architectural choice]
*   [Question 2 asking about a potential edge case]
*   [Question 3 challenging the user to explain a complex part of the code]
```

### 4. Writing Style & Visuals

*   **Heuristics for Headings**:
    *   **Sentence Case**: Always use sentence case for headings (e.g., "Architecture and logic" NOT "Architecture And Logic").
    *   **Descriptive**: Make headings descriptive of the actual content. Instead of generic "Challenges", use "Handling concurrent requests".
*   **Be Visual**: Use **ASCII diagrams** (using code blocks) or **Mermaid charts** to explain complex logic, data flows, or state changes. A visual representation of _how_ it works is often more valuable than text.
*   **Code Index**: Always include a "Code index" or "Quick links" section at the top. This allows the user to jump directly to the relevant files in their IDE.
*   **Trade-offs**: ALWAYS include a section on trade-offs. This is critical for deep learning.
*   **Reflection**: End with questions that challenge the user's understanding, but **do not provide the answers**.
*   **Be Flexible**: Do not force the explanation into a rigid template if it doesn't fit. Adapt the headers to tell the most effective learning story.
*   **Expert Tutor Persona**: Write as if you are explaining this to a smart colleague who wants to understand the *reasoning*, not just the lines of code.
