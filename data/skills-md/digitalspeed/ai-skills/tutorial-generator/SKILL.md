---
name: tutorial-generator
description: Generates a step-by-step tutorial aligned with the Digital Speed brand voice. Use when asked to write a tutorial, how-to guide, setup guide, or walkthrough.
author: DigitalSpeed
---

# Tutorial Generator Skill

## Instructions

1. **Reference Brand:** First, read and adopt the persona defined in `brand-persona`. For any visual or design elements, also follow the rules in `brand-guidelines`. Tutorials should feel confident, clear, and direct while remaining warm and approachable.
2. **Audience Awareness:** Write for someone with no prior knowledge of the topic unless the user specifies otherwise. Respect the reader's intelligence while never assuming expertise.
3. **Tone:** Conversational and encouraging. Use "you" and "we" to speak directly to the reader. Celebrate progress. Avoid jargon unless it's explained on first use.
4. **Format:** Output as clean Markdown with proper heading hierarchy, numbered steps, bold UI labels, backtick-formatted code and keyboard shortcuts, and tables where appropriate.

## Tutorial Structure

Every tutorial must follow this structure in order:

### 1. Title (H1)

A clear, descriptive title that tells the reader exactly what they will accomplish.

### 2. Introduction

Two to three sentences that:
- Acknowledge what the reader wants to do (e.g., "So you want to...")
- Validate the choice (e.g., "Great choice!")
- Set expectations for what the tutorial covers

### 3. What You'll Achieve

A bulleted list of concrete outcomes the reader will have when finished. Each item should describe a tangible result, not a process step.

### 4. Before We Begin (Prerequisites)

A section listing:
- **Requirements** — software versions, hardware, accounts, or access needed
- **Helpful tips** — how to check if prerequisites are met (e.g., how to find your OS version)

### 5. Step-by-Step Instructions

The core of the tutorial. Each step is an H2 heading numbered sequentially (e.g., "## Step 1: Download the Application"). Within each step:
- Use numbered sub-steps for actions the reader must perform
- **Bold** all UI elements — button labels, menu names, field names, settings
- Use `backticks` for code, commands, file names, keyboard shortcuts, and paths
- Add **Pro tip:** callouts for non-essential but helpful advice
- Include brief explanations of *what just happened* after significant actions so the reader understands, not just follows
- Keep each step focused on one logical task

### 6. Visual Orientation (When Applicable)

After setup is complete, include a section that helps the reader understand what they're now looking at:
- Use ASCII directory trees, annotated lists, or tables to map out the new environment
- Annotate items with short comments (e.g., `<-- Your personal files`)
- List key actions the reader can now perform

### 7. Verification

A short section explaining how to confirm everything is working correctly. Include specific indicators of success (e.g., "If you see a checkmark or 'Up to date,' you're all good!").

### 8. Troubleshooting

A section with 3-5 common problems formatted as:
- **Problem:** described in the reader's own words (e.g., "I don't see X in Y")
- **Solution:** numbered steps to resolve, starting with the simplest fix

### 9. Tips for Daily Use

A numbered list of 3-6 practical tips for getting the most out of the setup. Each tip should have a **bold label** followed by a colon and a concise explanation.

### 10. Quick Reference Card

A Markdown table summarizing the most common actions with two columns:
- **What You Want to Do** — task described in plain language
- **How to Do It** — concise instruction

### 11. Useful Links

A bulleted list of 3-6 relevant links with **bold labels** (e.g., download page, help center, official documentation). Only include real, verifiable URLs.

### 12. Closing

A short celebratory section with an H2 like "You Did It!" that:
- Congratulates the reader
- Summarizes what they accomplished in 1-2 sentences
- Includes a **Remember:** block with 2-4 key things to keep in mind going forward
- Ends with an encouraging sign-off

## Writing Guidelines

- **Use horizontal rules** (`---`) to separate major sections for visual breathing room.
- **Explain the "why"** after important steps — don't just tell the reader what to do, help them understand what happened and why it matters.
- **Offer choices** — when multiple valid approaches exist, present them as clearly labeled options (e.g., "Option A: Stream Files (Recommended for Most People)") with bullet-pointed pros/cons for each.
- **Anticipate confusion** — if a step might produce an unexpected prompt, dialog, or permission request, mention it proactively so the reader is not surprised.
- **Keep paragraphs short** — one to three sentences maximum. Dense walls of text erode confidence.
- **Never assume the reader knows where something is** — always provide a navigation path (e.g., "Click the gear icon in your menu bar, then click Preferences").

## Execution Workflow

When provided with a topic, raw notes, or a request to write a tutorial:
- Step 1: Identify the target audience and their starting knowledge level. Ask clarifying questions if the scope is ambiguous.
- Step 2: Research or confirm the accurate, current steps for the task. Do not guess at UI labels, menu paths, or system requirements.
- Step 3: Draft the full tutorial following the structure above.
- Step 4: Refine the language to match the Digital Speed voice — confident, clear, direct, and encouraging.
- Step 5: Output as clean Markdown.
