---
name: gemini-image
description: Analyze images using Gemini's vision capabilities. Use for image analysis, text extraction from screenshots, and visual content understanding.
---

# Gemini Image Analysis

Analyze images using Gemini Pro's vision capabilities.

## Prerequisites

```bash
pip install google-generativeai
export GEMINI_API_KEY=your_api_key
```

## CLI Reference

### Basic Image Analysis

```bash
# Analyze an image
gemini -m pro -f /path/to/image.png "Describe this image in detail"

# With specific question
gemini -m pro -f screenshot.png "What error message is shown?"

# Multiple images
gemini -m pro -f image1.png -f image2.png "Compare these two images"
```

## Analysis Operations

### General Description

```bash
gemini -m pro -f image.png "Describe this image comprehensively:
1. Main subject/content
2. Colors and composition
3. Text visible (if any)
4. Context and purpose
5. Notable details"
```

### Extract Text (OCR)

```bash
gemini -m pro -f screenshot.png "Extract all text from this image.
Format as plain text, preserving layout where possible.
Include any text in buttons, labels, or UI elements."
```

### Code from Screenshot

```bash
gemini -m pro -f code-screenshot.png "Extract the code from this screenshot.
Provide as properly formatted code with correct indentation.
Note any parts that are unclear or partially visible."
```

### UI Analysis

```bash
gemini -m pro -f ui-screenshot.png "Analyze this UI:
1. What application/website is this?
2. What page/screen is shown?
3. Main UI elements and their purpose
4. User flow/actions available
5. Any UX issues or suggestions"
```

### Error Analysis

```bash
gemini -m pro -f error-screenshot.png "Analyze this error:
1. What error is shown?
2. What is the likely cause?
3. How to fix it?
4. Any related information visible?"
```

### Diagram Understanding

```bash
gemini -m pro -f diagram.png "Explain this diagram:
1. What type of diagram is this?
2. Main components and their relationships
3. Data/process flow
4. Key takeaways"
```

## Specific Use Cases

### Debug Screenshot

```bash
gemini -m pro -f debug-screen.png "I'm debugging an issue. From this screenshot:
1. What is the current state?
2. What errors or warnings are visible?
3. What should I look at?
4. Suggested next steps"
```

### Compare Before/After

```bash
gemini -m pro -f before.png -f after.png "Compare these before and after images:
1. What changed?
2. Is this an improvement?
3. Any issues in the 'after' version?
4. Anything missing?"
```

### Design Feedback

```bash
gemini -m pro -f design.png "Provide design feedback:
1. Visual hierarchy
2. Color usage
3. Typography
4. Spacing and alignment
5. Accessibility concerns
6. Suggestions for improvement"
```

### Data Extraction

```bash
gemini -m pro -f chart.png "Extract data from this chart:
1. Chart type
2. Data series and values
3. Axes labels and ranges
4. Key trends or insights
5. Output as structured data if possible"
```

### Form Analysis

```bash
gemini -m pro -f form.png "Analyze this form:
1. Form purpose
2. Fields and their types
3. Required vs optional
4. Validation rules visible
5. UX suggestions"
```

## Workflow Patterns

### Screenshot to Issue

```bash
# Capture screenshot (macOS)
screencapture -i /tmp/bug.png

# Analyze and format as issue
gemini -m pro -f /tmp/bug.png "Create a bug report from this screenshot:

## Summary
[One-line description]

## Steps to Reproduce
[Inferred from screenshot]

## Expected Behavior
[What should happen]

## Actual Behavior
[What the screenshot shows]

## Environment
[Any visible system info]"
```

### UI to Code

```bash
gemini -m pro -f ui-design.png "Generate React component code that recreates this UI:
- Use Tailwind CSS for styling
- Make it responsive
- Include proper TypeScript types
- Add appropriate accessibility attributes"
```

### Documentation

```bash
gemini -m pro -f app-screen.png "Write user documentation for this screen:
- What this screen is for
- How to use each feature
- Common tasks
- Tips and notes"
```

## Image Types Supported

- PNG, JPEG, GIF, WebP
- Screenshots
- Photos
- Diagrams and charts
- UI mockups
- Code snippets
- Documents

## Best Practices

1. **Use clear images** - Higher quality = better analysis
2. **Crop to relevant area** - Remove unnecessary context
3. **Ask specific questions** - Vague prompts get vague answers
4. **Provide context** - Tell Gemini what you're looking for
5. **Verify extracted text** - OCR isn't perfect
6. **Multiple angles** - Use multiple images for complex subjects
