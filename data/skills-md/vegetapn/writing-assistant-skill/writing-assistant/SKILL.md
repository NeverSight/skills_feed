---
name: writing-assistant
description: Comprehensive writing workflow from ideation to publication. Guides users through creating polished articles by collecting ideas, asking clarifying questions, researching content, polishing drafts, adding images, and publishing to platforms like WeChat or X. Use when users want to write articles, blog posts, or long-form content, especially when starting from a topic idea, rough materials, or initial draft. Also use when users mention writing, publishing, or content creation workflows.
---

# Writing Assistant

A complete end-to-end writing workflow that transforms ideas, materials, or rough drafts into polished, illustrated articles ready for publication.

## Overview

This skill orchestrates a multi-step writing process:
1. Collect initial content (topic, materials, or draft)
2. Clarify and enrich through interactive questioning
3. Generate or refine the initial draft
4. Polish the content using content-research-writer
5. Add appropriate illustrations using baoyu-xhs-images
6. Combine content and images into final article
7. Optionally publish to WeChat or X platforms

## Workflow

### Step 1: Choose Starting Mode

Ask the user to select one of three modes:

**Mode 1: Topic-Based**
- User provides a topic or theme they want to write about
- Most suitable when starting from scratch with just an idea

**Mode 2: Materials-Based**
- User provides loosely organized materials, notes, or reference content
- Can include rough notes, copied references, or miscellaneous content
- Ask for file paths if materials are in files

**Mode 3: Draft-Based**
- User provides an unpolished initial draft
- Suitable when the user has already written a rough version
- Ask for file path if draft is in a file

### Step 2: Collect and Clarify (Modes 1 & 2 Only)

For Modes 1 and 2, use an interactive questioning approach:

1. **Analyze the provided content first**:
   - Read and understand what the user has already provided
   - Identify what's clear vs. what needs clarification
   - Note gaps, ambiguities, or areas that need expansion

2. **Ask tailored, content-specific questions**:
   - Formulate questions based on the specific topic and materials provided
   - Focus on filling identified gaps and resolving ambiguities
   - Ask about aspects that are unclear or need deeper exploration
   - Adapt questions to the user's context and writing goals

3. **Collect user responses** systematically

4. **Supplement with research** if context is insufficient:
   - Use WebSearch for relevant information
   - Use WebFetch if user provides URLs
   - Gather supporting materials from the internet

5. **Organize into initial draft** based on:
   - User's answers to questions
   - Researched supplementary materials
   - Logical article structure

6. **Proceed to Step 4** after creating the initial draft

**Question Strategy:**
- Ask 2-4 questions at a time (avoid overwhelming the user)
- Tailor each question to the specific content provided - no fixed templates
- Common areas to explore (adjust based on actual needs):
  - What's the main message or takeaway?
  - Who is the target audience?
  - What's the desired tone (professional, casual, technical, etc.)?
  - Are there specific points that need more detail?
  - What context or background should readers have?
  - Are there particular examples or stories to include?
- Let the content guide the questions - if something is already clear, don't ask about it

### Step 3: Process Draft (Mode 3 Only)

For Mode 3, skip directly to Step 4 with the user's provided draft.

### Step 4: Polish the Draft

Use the **@content-research-writer** skill to refine and polish the draft:

```
Invoke: content-research-writer skill
Input: The initial or user-provided draft
Output: {filename}-polished.md
```

The polished version will have:
- Improved structure and flow
- Better hooks and engagement
- Citations and research integration
- Professional writing quality

### Step 5: Generate Illustrations

Use the **@baoyu-xhs-images** skill to create appropriate images:

```
Invoke: baoyu-xhs-images skill
Input: {filename}-polished.md content
Output: Generated images
```

**Image Guidelines:**
- Images should be appropriately spaced (not too dense, usually 3~5 images)
- Select key points that benefit from visual illustration
- Maintain balance between text and visuals

### Step 6: Create Final Article

Combine the polished content with generated images:

1. Take the {filename}-polished.md content
2. Insert images at appropriate positions
3. Ensure proper formatting and layout
4. Create final output: {filename}-final.md

**Layout Considerations:**
- Place images near relevant text sections
- Maintain readable flow
- Use consistent formatting
- Ensure images enhance rather than disrupt reading

### Step 7: Next Steps

After creating the final article, summarize the work completed and ask the user about publication:

**Do not write a summary document**. Instead, provide a brief verbal summary and ask:
- "Would you like to publish this article?"
- "Which platform would you prefer: WeChat Official Account (微信公众号) or X (Twitter)?"
- "Or would you like to make any revisions first?"

### Step 8: Publish (Optional)

If the user wants to publish, invoke the appropriate skill:

**For WeChat Official Account:**
```
Invoke: baoyu-post-to-wechat skill
Input: {filename}-final.md and images
```

**For X (Twitter):**
```
Invoke: baoyu-post-to-x or x-article-publisher skill
Input: {filename}-final.md and images
```

Follow the publishing skill's workflow for platform-specific requirements.

## Best Practices

1. **Be Patient with Questions**: Take time in Step 2 to thoroughly understand the user's vision
2. **Research Thoughtfully**: Supplement user input with credible sources when gaps exist
3. **Preserve User Voice**: While polishing, maintain the user's intended tone and style
4. **Image Selection**: Be selective with images - quality and relevance over quantity
5. **Review Before Publishing**: Confirm the user is satisfied with the final article before publishing

## File Naming Convention

Use consistent naming throughout the workflow:
- Initial draft: `{topic-or-title}.md`
- Polished version: `{topic-or-title}-polished.md`
- Final version: `{topic-or-title}-final.md`
