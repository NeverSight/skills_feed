---
name: lib-skill-creator-skill
description: "Guides users through the process of creating library skills, adding references to existing skills, or updating individual reference files"
---

# Source Code Into Skill

## Overview

This skill transforms specified source code into AI-coding-friendly guiding skills through natural collaborative conversations. It supports three operation modes:

1. **Create new skill** - Generate a complete new skill from source code
2. **Add references** - Add new API documentation to an existing skill
3. **Update reference** - Modify/update an existing API documentation file

**Why generate skills for libraries?**

When AI coding tools work on projects that depend on a library, they often need to understand the library's APIs and classes to complete user requests effectively. By generating a skill from the library's source code:

- AI tools can understand the purpose and logic of each API without reading the original source code
- Developers can share library knowledge with AI tools in a standardized format
- The generated skill serves as comprehensive, searchable documentation optimized for AI consumption

This approach ensures that the generated skills accurately reflect the codebase structure and provide clear, actionable guidance for AI coding tools.

## Select Operation Mode

**What would you like to do?**
- [ ] **Create new skill** - Generate a complete new skill from source code
- [ ] **Add references** - Add new API documentation to an existing skill
- [ ] **Update reference** - Modify/update an existing API documentation file

---

## Create New Skill Mode

### Understand the Repository

Analyze the source code to identify all publicly exposed APIs, objects, classes, interfaces, enums, services, and other constructs. Summarize your findings and present them to the user for confirmation.

Ask the user these questions:

**Is this summary correct?**
- [ ] Confirm - The summary is accurate, proceed to next step
- [ ] Revise - Need to add/remove/modify APIs
- [ ] Add context - Provide additional notes

**If "Revise" or "Add context" selected, ask:**
- Which APIs need to be added, removed, or modified?
- Any additional context or notes to include?

Once confirmed, proceed to determine the partitioning strategy.

### Determine the Partitioning Strategy

Ask the user to choose how to organize the generated documentation files based on the project structure. Present the following options:

- **By namespace** - Group APIs by their namespace/package structure
- **By folder** - Group APIs by their folder location in the source tree
- **By file** - Create one documentation file per source file

**Confirm with the user:**
- Which partitioning strategy works best for this project?
- Any specific folder/naming conventions to follow?

This ensures the generated documentation structure matches the logical organization of the codebase.

### Document and Generate API Files

Based on the confirmed list of APIs, document each API through collaborative dialogue and write the content to a file immediately after confirmation.

**For each API, confirm and document the following:**

1. **API Declaration** - The exact function/class/interface signature as it appears in the source code
2. **Description** - A clear explanation of what the API does and its purpose
3. **Usage Scenarios** - When and why a user would use this API, including common use cases
4. **Example Code** - Practical code snippets demonstrating how to use the API correctly

**Workflow for each API:**
1. Present the current documentation draft to the user
2. Ask for confirmation on each element (declaration, description, scenarios, examples)
3. Incorporate user feedback iteratively and present the revised content
4. Repeat the feedback loop until the user confirms the documentation is correct
5. Once confirmed, write the validated content to:
   ```
   /<skill-name>/references/<folder>/<api>.md
   ```
6. Proceed to the next API and repeat

**File path structure:**
- `<skill-name>` - The name of the skill being created
- `<folder>` - The folder determined by the partitioning strategy
- `<api>` - The name of the API being documented

Each `.md` file should contain the confirmed documentation for a single API, formatted clearly for AI coding tools to reference.

### Update Main Skill Documentation

After all public API documentation files have been generated, update the main skill documentation (`<skill-name>/SKILL.md`) to include references to all documented APIs.

**Generate or update the SKILL.md to:**
- **Include required metadata at the top of the file:**
  ```
  ---
  name: <skill-name>
  description: "<brief description of the library and its purpose>"
  ---
  ```
- Add a section listing all available APIs organized by the chosen partitioning strategy
- Provide brief descriptions or links to each API's detailed documentation
- Ensure the table of contents (if present) reflects all newly added API documentation

This step ensures users can easily discover and navigate all available API documentation from the main skill file.

---

## Add References Mode

### Identify Existing Skill

**What is the path to the existing skill?**
- [ ] Provide skill path (e.g., `/my-library-skill`)

Once the skill path is provided, proceed to load the existing structure.

### Load Existing Structure

Read the existing skill's structure to understand:
- Current partitioning strategy (by namespace, folder, or file)
- Existing reference files and their organization
- Current SKILL.md content

Present the findings to the user:

**Existing skill structure detected:**
- Partitioning strategy: [detected strategy]
- Existing references: [list of existing API files]
- Reference folders: [list of folders]

**Is this analysis correct?**
- [ ] Confirm - Proceed to next step
- [ ] Revise - Correct the analysis

### Analyze Source Code

Analyze the source code to identify all publicly exposed APIs, objects, classes, interfaces, enums, services, and other constructs.

**Important:** If the user provided a different source code path than the existing skill was based on, note any differences in the codebase.

### Determine New APIs to Document

Compare the analyzed APIs with the existing reference files to identify which APIs are new or need to be added.

Present the findings:

**Found [X] new APIs to add:**
- [List of new APIs]

**Existing APIs that will remain unchanged:**
- [List of existing APIs]

**Is this list correct?**
- [ ] Confirm - These are the APIs to add
- [ ] Revise - Need to modify the list
- [ ] Add context - Provide additional notes

### Confirm Partitioning Strategy

Based on the existing skill structure, present the current partitioning strategy and ask the user to confirm or change it.

**Existing partitioning strategy: [current strategy]**

**How would you like to proceed?**
- [ ] **Keep current strategy** - Use the existing partitioning approach (recommended)
- [ ] **Change strategy** - Select a different partitioning approach

**If "Change strategy" is selected, ask:**
- Which partitioning strategy would you like to use?
  - [ ] By namespace
  - [ ] By folder
  - [ ] By file
- Should existing documentation be migrated to the new structure?
  - [ ] Yes - Reorganize all existing files (may require significant file moves)
  - [ ] No - Only apply new strategy to new references

**If migration is selected, also ask:**
- This will move/rename existing reference files. Proceed?
- [ ] Yes - Migrate existing files
- [ ] No - Cancel and reconsider strategy

Once the partitioning strategy is confirmed, proceed to generate API files.

### Generate New API Files

For each new API identified, document it through collaborative dialogue and write the content to a file immediately after confirmation.

**For each API, confirm and document the following:**

1. **API Declaration** - The exact function/class/interface signature as it appears in the source code
2. **Description** - A clear explanation of what the API does and its purpose
3. **Usage Scenarios** - When and why a user would use this API, including common use cases
4. **Example Code** - Practical code snippets demonstrating how to use the API correctly

**Workflow for each API:**
1. Present the current documentation draft to the user
2. Ask for confirmation on each element (declaration, description, scenarios, examples)
3. Incorporate user feedback iteratively and present the revised content
4. Repeat the feedback loop until the user confirms the documentation is correct
5. Once confirmed, write the validated content to:
   ```
   /<skill-name>/references/<folder>/<api>.md
   ```
6. Proceed to the next API and repeat

**File path structure:**
- `<skill-name>` - The name of the existing skill
- `<folder>` - The folder determined by the partitioning strategy (existing or new)
- `<api>` - The name of the API being documented

**Important:** Use the confirmed partitioning strategy (existing or new) to determine the `<folder>` path for each new API file.

Each `.md` file should contain the confirmed documentation for a single API, formatted clearly for AI coding tools to reference.

### Update Main Skill Documentation

After all new API documentation files have been generated, update the main skill documentation (`<skill-name>/SKILL.md`) to include references to both existing and newly documented APIs.

**Update the SKILL.md to:**
- Keep existing metadata and structure
- Add the new APIs to the appropriate sections based on the partitioning strategy
- Ensure all APIs (existing and new) are properly listed
- Update the table of contents if present

This step ensures the main skill file remains comprehensive and up-to-date.

---

## Update Reference Mode

### Identify Target Reference

**What is the path to the reference file you want to update?**
- [ ] Provide file path (e.g., `/my-library-skill/references/utils/logger.md`)

**Alternative: Browse available references**
- [ ] List all skills
- [ ] List references in a specific skill

If the user chooses to browse, present the available options and help them navigate to the target file.

### Load Current Content

Read the existing reference file and present its current content to the user.

**Current content of [file path]:**
```
[Display the current file content]
```

**What would you like to update?**
- [ ] **API Declaration** - Modify the signature
- [ ] **Description** - Update the explanation
- [ ] **Usage Scenarios** - Revise use cases
- [ ] **Example Code** - Update or add examples
- [ ] **All sections** - Comprehensive update

### Collaborative Update

Based on the user's selection, work through the chosen sections collaboratively.

**For each selected section:**
1. Present the current content
2. Ask what changes are needed
3. Incorporate user feedback
4. Present the revised content
5. Repeat until the user confirms

**Example dialogue flow:**

*For API Declaration:*
- Current declaration: `[current signature]`
- What changes are needed?
- [User provides feedback]
- Revised declaration: `[proposed signature]`
- Is this correct?
  - [ ] Confirm
  - [ ] Revise

*For Description:*
- Current description: `[current description]`
- What changes are needed?
- [User provides feedback]
- Revised description: `[proposed description]`
- Is this correct?
  - [ ] Confirm
  - [ ] Revise

Repeat this process for all selected sections.

### Write Updated File

Once all changes have been confirmed, write the updated content to the file.

**Confirm final update:**
- [ ] **Write changes** - Save the updated content to the file
- [ ] **Review again** - Show the complete updated content one more time
- [ ] **Cancel** - Discard changes and keep original

If "Review again" is selected, display the complete updated content and ask for final confirmation.

If "Write changes" is confirmed, update the file and inform the user of the successful update.

---

## Key Constraints

- **Prefer multiple choice** - Structure questions as single-select options whenever possible
- **Recommend with rationale** - When presenting options, lead with the recommended approach followed by brief explanations
- **Preserve existing work** - In Add References and Update Reference modes, be careful not to accidentally overwrite or modify existing documentation unless explicitly requested
- **Clear file paths** - Always clearly communicate the file paths being read from or written to
- **Confirm destructive operations** - Before any operation that could overwrite or delete existing content, always ask for explicit confirmation
