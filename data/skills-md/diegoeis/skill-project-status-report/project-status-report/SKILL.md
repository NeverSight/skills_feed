---
name: project-status-report
description: Create and update structured project status reports from meetings, messages, documents, or notes. Use when users need to extract status updates into markdown reports with summary, problems, risks, and actions sections, consolidate multiple team reports, update existing reports maintaining reverse chronological order, save/modify reports in Obsidian vault, or mention terms like "status report", "project update", "sync", "war room", "team report", or "weekly update".
allowed-tools: conversation_search, google_drive_search, google_drive_fetch
metadata:
  author: Diego Eis
  version: "1.0.0"
---

# Project Status Report

## Overview

Extract project status information from various sources (meetings, messages, emails, documents) and generate structured status reports following standardized markdown templates.

**Report files:**
- Single team latest day report of all its projects (will be used to create other compiled files)
- Single team compiled report with all its projects and reports informations in date sections
- Consolidated document grouping multiple team reports
- Consolidated project list

## Core Rules and Principles

- **Never invent information** - Only use explicitly stated data
- **Never infer critical data** - Dates, deadlines, metrics must be explicit
- **Ask when unclear** - Request clarification for missing critical info
- **Flexible input** - Accept any format (text, markdown, Google Docs, transcriptions)
- **Contextual intelligence** - Infer team/project names from context when reasonable
- **Automatic language detection** - Match user's language for all output and template content. The final content of the templates, need to be the same users language or the language users set.
- **Historical context awareness** - Use previous reports for consistency, never for inventing data
- **Update capability** - Update existing reports maintaining exact structure
- **Fill yaml correctly** - Final output files need to have the yaml filled correctly. Use the existing notes to learn and reference patterns. Don't create others properties, use only the defined in templates
- **RAG status**: If the user defined the RAG status is the true. If user don't give this information, assume the status based on the latest informations

## Instructions

- **General:**
    - Use the informations, transcripts and documents given by the user to create the reports
    - Learn with notes to understand relations between reports and notes
    - If you will update an existing file, read and understand the file before you update with new informations
    - Find product/project/initiative in existing notes and update the right block
    - Follow template instructions completely
    - If unsure where to insert information, ask to user. 
    - Final output files need to have the yaml filled correctly
    - For projects/topics with resolved and done status, move the the right section indicated in templates
    - Be prepared to update the notes in the right topic section, when the user give updated informations about one individual topic

- **File naming pattern**
    - By default, follow the kabeb-case to create the final files.
    - Multiple teams: `all-teams-status-report-{YYYY-MM-DD}.md`
    - Single team day report: `{team_name}-status-report-{YYYY-MM-DD}.md`
    - Single Compiled Team: `{team_name}-compiled-status-report-{YYYY-MM-DD}.md`
    - Ask for team name if unknown
    - If you will save the file to Obsidian Vault, use Title Case com espaços, where the name of the file is the Title of the File.

- **Single team report:**
    - Usually is used to get latest status report of projects until that day.
    - Is used for structure informations and status report of one single team and your projects. 
    - Use `templates/template-single-team-status.md`
    - Group multiple projects under SINGLE team header
    - Before create the file, ask user confirmation a list of projects and iniatives the final report will have. User can ask to merge some topics or rename

- **Compiled Team report (well structured and formatted group of many single team report files):**
    - Used to group in one file all single team report of one specific team and your projects status reports of multiple days
    - To create or update this report, use the single team reports already created before by the user and the informations given by the user
    - When the user asks for a latest updated report of all projects of one specific team
        - Use the given informations or if the obsidian is used, look for the historical related notes and new related notes to update this report
        - Look for files that have the same name and content patterns created by this skill or for partterns users already asked in the past
    - Output file need to follow the instructions and structure of the template `templates/template-single-team-compiled-status.md`
    - Maintaining structure of the single team report notes, but following the structure and organization of the given template
    - Don't change informations or dates when group those notes
    - Ask for clarification if individual notes don't exist
    - Group multiple projects under SINGLE team header

- **Multiple Teams Reports (multiple teams, with multiple projects, multiple days):**
    - Used to group in one file all single report of all teams with many projects status reports of multiple teams
    - Output file need to follow the instructions and structure of the template `templates/template-multiple-teams-compiled-status.md`
    - Maintaining structure of single team report notes, but following the structure and organization of the given template
    - Don't change informations or dates when group those notes
    - Ask for clarification if individual notes don't exist
    
- **Giving updated list of projects**
    - If users wants an updated list of projects in the notes, use the `templates/template-projects-list.md` file to give the answer.

### Critical Structure Rule

**CORRECT - Single team header with all projects:**
```markdown
## Team Name

### First Project
#### DD-MM-YYYY
{content}

#### DD-MM-YYYY
{content}

#### DD-MM-YYYY
{content}

### Second Project
#### DD-MM-YYYY
{content}

#### DD-MM-YYYY
{content}
```

In the project section, dates sections should be organized from newest to oldest.

**WRONG - Repeated team headers:**
```markdown
## Team Name
### First Project
...

## Team Name
### Second Project
...
```

Team name (`## Team Name`) must appear ONCE with all projects nested under it.

### What to Avoid

- Don't update wrong dates or wrong projects
- Don't create extra blocks (Meeting Notes, Learnings, etc.) - follow templates exactly
- Don't assume - ask for clarification when in doubt

## When the user have Obsidian
Check if the user use Obsidian. If yes, check if you have access to use skills or available MCP to manipulate notes in Obsidian Vault.

- If user wants to save the files in Obsidian vault, ask for the vault path
- if user want to update or modify an existent note in Obsidian vault, ask for the file path in the vault
- Look in the vault to 

## Processing Workflow

### 1. Receive and Analyze
- Detect user's language
- Check for historical context (previous reports)
- Accept input in any format
- Scan for: team names, projects, status, problems, risks, actions, dates

### 2. Extract Information
For each project:
- Team name (explicit or contextual)
- Project/initiative name
- Summary content
- On track items (positive progress)
- Problems (current blockers)
- Risks & concerns (potential issues)
- Actions (specific next steps)

### 3. Handle Missing Information
**When to ask:**
- Critical info missing (team name can't be inferred)
- Contradictory information exists
- Info too vague to populate sections

**When NOT to ask:**
- Minor details missing but core clear
- Only 1-2 sections sparse (mark empty)
- Team/project names reasonably inferable

### 4. Generate Output
- Single markdown file with all projects (default)
- Follow template structure
- Use current date following the right format indicated by templates
- Match user's language
- Insert new updates BEFORE old content (reverse chronological)

## Critical Rules

### NEVER:
❌ Invent dates, deadlines, or timelines
❌ Create action items that weren't stated
❌ Infer problems/risks from neutral statements
❌ Add team members/stakeholders not mentioned
❌ Make up metrics or quantitative data
❌ Fabricate technical details
❌ Assume project status without indication

### ALWAYS:
✅ Use only explicitly stated information
✅ Mark sections empty if no relevant info
✅ Preserve original terminology
✅ Use exact dates when mentioned
✅ Quote specific problems/risks as stated
✅ List only explicitly discussed actions
✅ Ask for clarification when needed
✅ Check if updating existing report
✅ Preserve exact structure when updating
✅ Group projects under SINGLE team header
✅ Insert new content BEFORE old (reverse chronological)

## Quality Checklist

Before delivering:
- [ ] All dates from source or current date following the right format indicated by templates
- [ ] No invented action items or problems
- [ ] Team/project names accurate or marked uncertain
- [ ] All sections present (even if empty)
- [ ] Summary factual without speculation
- [ ] Format matches template exactly
- [ ] Content verifiable from sources
- [ ] No hallucinated details
- [ ] If updating: exact structure preserved
- [ ] Historical context only for terminology, not data invention
- [ ] Each team header appears only ONCE
- [ ] New content inserted BEFORE old content
- [ ] Done/Resolved topics inserted in the right section

## Output Formats

**Default:** 
- Markdown (.md)
- Language following the existing files languages or other language only when the user asks

## Detailed Reference

For section guidelines, historical context usage, edge cases, and detailed examples, see: `references/detailed-guide.md`
