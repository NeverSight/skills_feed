---
name: process-meeting-transcript
description: Process raw meeting transcripts from Granola or other sources into structured notes with frontmatter, action items, summary, and formatted transcript. Use this skill when the user asks to process a meeting transcript or provides a raw transcript that needs formatting.
---

# Process Meeting Transcript

## Overview

Process raw meeting transcripts into well-structured Obsidian notes with YAML frontmatter, extracted action items, meeting summary, and properly formatted transcript sections.

## When to Use This Skill

Use this skill when:
- User provides a raw meeting transcript (typically from Granola)
- User asks to "process a meeting transcript" or "format meeting notes"
- User points to a file containing an unprocessed transcript
- User pastes transcript content directly into the conversation

## Workflow

### Step 1: Read the Transcript

If the transcript is in a file, read the entire contents. If the user pasted the transcript directly, use that content.

### Step 2: Extract Action Items

Carefully review the entire transcript to identify all action items, tasks, and commitments. Look for:
- Explicit commitments: "I'll do X", "Alex will review Y"
- Assigned tasks: "Nathan and Damian should schedule..."
- Follow-up items: "We need to...", "Let's make sure to..."
- Decisions requiring action: "We should deploy X before Y"

Format action items as:
- Bulleted list under `# Action Items` heading
- Use **bold** for person names when specific people are assigned
- Include context for what needs to be done and why
- Order by priority/importance when evident from discussion

Example format:
```markdown
# Action Items

- **Alice & Bob**: Review the new feature implementation next week and provide feedback
- **Charlie & Dana**: Schedule a knowledge transfer session on the payment service architecture
- **Eve**: Discuss deployment timeline with the infrastructure team
```

### Step 3: Create Meeting Summary

Write a comprehensive but concise summary that captures:
- Main topics discussed
- Key decisions made
- Technical architecture or approach agreed upon
- Timeline and next steps
- Important context or constraints

Structure the summary with:
- Opening paragraph: High-level overview of what was discussed and main outcome
- Subsections (using `##` or `###` headings) for major topics
- Use bold for important terms, decisions, or concepts
- Include enough detail that someone who wasn't in the meeting can understand what happened

Keep summaries factual and focused on outcomes, decisions, and technical details.

### Step 4: Format the Transcript

Place the raw transcript under a `# Transcript` heading. Preserve the original formatting but ensure it's readable. If the transcript includes metadata (meeting title, date, participants) at the top, keep that information.

### Step 5: Add Frontmatter

Use the `add-frontmatter` slash command to generate appropriate YAML frontmatter for the note. The frontmatter should include:
- `title`: Meeting title or topic
- `date`: Meeting date (YYYY-MM-DD format)
- `type`: Set to "meeting"
- `attendees`: Array of participant names
- `project`: Related project if applicable
- `tags`: Relevant tags (meeting, project tags, topic tags)
- `status`: Set to "complete"
- `key_topics`: Array of main discussion topics
- `action_items`: Array of action items (duplicate from Action Items section for searchability)
- `decisions`: Array of key decisions made
- `related_links`: Any links mentioned (Notion docs, Linear issues, etc.)

Invoke the add-frontmatter command by providing it with context about the meeting.

### Step 6: Assemble the Final Note

Combine all sections in this order:
1. YAML frontmatter (from add-frontmatter command)
2. Links section (if any Notion/Linear/GitHub links were mentioned)
3. `# Action Items` section
4. `# Summary` section
5. `# Transcript` section

## Output Format

The final note should follow this structure:

```markdown
---
title: Meeting Title
date: YYYY-MM-DD
type: meeting
attendees: ['Person 1', 'Person 2', ...]
project: Project Name
tags: [meeting, relevant, tags]
status: complete
key_topics:
  - Topic 1
  - Topic 2
action_items:
  - 'Action item 1'
  - 'Action item 2'
decisions:
  - Decision 1
  - Decision 2
related_links:
  - 'Link description: URL'
---

**Agenda** https://link-to-agenda-if-available

# Action Items

- **Person**: Action item description
- **Person**: Another action item

# Summary

Opening paragraph with high-level overview.

## Key Decisions/Topics

Details about decisions and topics discussed...

# Transcript

[Raw transcript content]
```

## Tips for Quality Output

1. **Be thorough with action items**: Don't miss commitments buried in discussion
2. **Capture decisions**: Explicit decisions are critical for reference
3. **Include technical details**: Preserve architecture discussions, API names, service names
4. **Maintain context**: Someone reading later should understand what was decided and why
5. **Preserve links**: Notion docs, Linear issues, GitHub PRs mentioned in meetings are important
6. **Use consistent formatting**: Follow the example structure for all transcripts
