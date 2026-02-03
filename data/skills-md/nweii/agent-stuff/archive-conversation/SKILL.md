---
name: archive-conversation
description: "Create analytical archival summaries of AI conversations, capturing intellectual journeys, key insights, and technical logs. Use when archiving, saving, or documenting a chat session."
argument-hint: "[save-location]"
metadata:
  author: nweii
  version: "1.1.0"
---

# AI Conversation Archival Summary

Create an archival summary of an AI conversation that captures its intellectual journey, key insights, or technical work session logs. Document either how thinking evolved throughout the discussion or the specific actions and technical decisions made during a work session.

## Deep Analysis Requirements

Conduct a thorough analysis of the entire conversation:

1. Read through completely first, identifying all conceptual threads, task sequences, and transitions
2. Note patterns in questioning, resistance points, breakthrough moments, or technical hurdles
3. Identify the conversation's nature (technical work session, creative exploration, strategic planning, philosophical inquiry, etc.)
4. Understand what made this particular exchange worth preserving (insight-driven vs. action-documentation)
5. Determine what structure would best capture its unique value (narrative vs. log-formatted)

**Look deeply for:**

- The real question beneath the initial question
- How the problem space was redefined or the technical path was forged
- Moments where assumptions were challenged or implementation details were decided
- Conceptual frameworks or technical patterns that emerged organically
- The emotional/intellectual journey or the step-by-step progress of a work session
- Valuable tangents or "failed" approaches that taught something or informed the final code
- Connections made between seemingly unrelated ideas or system components
- What remained intentionally unresolved or deferred to later tasks

## Creating Descriptive Structure

Instead of using generic headings like "Initial Question" or "Key Findings," create headings that describe the actual content of each section. The heading should give readers immediate context about what happened in that part of the conversation.

**Examples of descriptive headings:**

- "Starting from hourly vs. project pricing questions"
- "Why the recursive function kept hitting memory limits"
- "Exploring whether this needs to be real-time"
- "The confusion about state management"
- "Deciding between complexity and maintainability"

Use sentence-case for headings, not title case. Avoid marketing-speak, dramatic phrasing, or trying to be clever.

## Flexible Documentation Approaches

Let the conversation's natural flow determine your structure:

**For Problem-Solving Sessions:**
Open with what broke/what problem triggered the conversation → Document failed approaches if instructive → Describe the working solution → Note implementation details or next steps

**For Creative Explorations:**
Start with the initial vision or desire → Show how ideas evolved or branched → Capture key decisions and why they were made → Preserve unexplored directions worth revisiting

**For Learning Journeys:**
Begin with what the user didn't understand → Track how understanding built piece by piece → Highlight breakthrough moments → List remaining questions

**For Work Sessions & Implementation Logs:**
Define the session's objective → Document specific actions taken and files modified → Capture technical hurdles and how they were resolved → Summarize the current state of the work and remaining tasks

**For Strategic Thinking:**
Frame the decision that needed making → Explore options considered and their trade-offs → Document the framework or criteria that emerged → Capture action items or next considerations

## Excerpt Guidelines

Include conversation excerpts that show thinking in action:

> [User's first name, if known]: "[moment of recognition or confusion]"
> AI: "[response that shifted understanding or articulated key insight]"

Choose excerpts that reveal intellectual movement - the moments where thinking actually changed, not just where information was exchanged. Be generous in your excerpt lengths.

## File Output Requirements

### Naming Convention

- **Format**: `{{Type}} - {{topic}} YYYY-MM.md`
- Use `Thinking` for insight-heavy journeys or `Log` for action-leaning work sessions
- Example: `Thinking - Portfolio strategy 2025-08.md`
- Example: `Log - Refactoring auth middleware 2025-01.md`

### Save Location Logic

1. **If save-location argument provided**: Use that path directly
2. **Context-aware detection**: Analyze the existing folder structure to find the most relevant folder for the note being archived (e.g., matching "Working" or "Journaling" folders to the conversation type).
3. **If no context**: Ask the user to confirm where to save
4. **Fallback**: If vault access unavailable (mobile/restricted), output as markdown code block for manual saving

### Metadata

- Add appropriate tags (e.g., `#thinking`, `#log`, `#journal`, `#learning`, `#ai-chat`) based on the user's system
- Use third person or neutral documentation style, not first person (except when quoting)

## Remember

- You're documenting intellectual exploration OR technical execution/work sessions
- Perform deep analysis to identify all important threads, transitions, and task sequences
- Use headings that describe what actually happened or what was achieved in that section
- Keep language natural and straightforward - no marketing-speak or forced drama
- Capture why this journey or work session matters, and what was actually produced or decided
- Include the messy, human elements - confusion, recognition, technical frustrations, breakthroughs
- Preserve what would be valuable to revisit months or years later
- When using specific examples repeatedly, vary phrasing or generalize after first mention
