---
name: photo-clipper
description: Crop photos intelligently based on natural language prompts using GPT-5 vision analysis. Use when the user asks to crop or trim a photo, remove parts of an image, focus on a specific subject, improve composition, or remove distractions from edges.
---

# Photo Clipper

## When to Use

Use this skill when the user asks to:
- Crop or trim a photo
- Remove parts of an image (e.g., "remove 20% from top")
- Focus on a specific subject or area
- Improve composition (e.g., "apply rule of thirds")
- Remove distractions from edges
- Adjust framing or aspect ratio

## Instructions

This skill uses GPT-5 vision API to analyze photos and suggest intelligent cropping. Always:

1. **Validate input** - Ensure photo exists and is JPG/PNG format
2. **Call GPT-5** - Get clipping suggestions based on user's natural language prompt
3. **Validate safety** - Ensure clipping doesn't remove more than 50% per dimension
4. **Apply clipping** - Crop the photo and save to new file (never overwrite original)
5. **Report results** - Show what was removed and GPT-5's reasoning

### Usage

```python
from photo_clipper import main

result = main(
    photo_path="photo.jpg",
    prompt="Remove 20% from top to reduce empty sky"
)
# Returns: "photo-clipped.jpg"
```

### Command Line

```bash
python photo_clipper.py <photo_path> "<prompt>" [output_path]
```

### Examples

**Remove empty sky:**
```
Remove 30% from top to reduce empty sky
```

**Focus on subject:**
```
Crop to focus on the person's face in the center
```

**Remove distractions:**
```
Remove the partial tree on the left edge
```

**Improve composition:**
```
Apply rule of thirds to balance the composition
```

**Trim specific amount:**
```
Remove 10% from all edges for a cleaner frame
```

## Output

- Returns path to clipped photo
- Never overwrites original
- Format: `{original_name}-clipped.{ext}`
- Displays GPT-5's confidence score and reasoning

## Error Handling

- Falls back to safe defaults (no clipping) if GPT-5 unavailable
- Validates parameters (max 50% removal per dimension)
- Clear error messages for missing files or invalid formats

## Requirements

- OPENROUTER_API_KEY environment variable must be set
- Photo must be JPG or PNG format
- Photo under 50MB recommended

## Technical Implementation

See `references/implementation.md` for:
- GPT-5 vision API integration
- Cropping algorithm details
- Error handling strategy
- Performance optimization

## Examples

See `examples/common-use-cases.md` for:
- Remove empty sky
- Focus on subject
- Remove distractions
- Improve composition
- Error handling scenarios
