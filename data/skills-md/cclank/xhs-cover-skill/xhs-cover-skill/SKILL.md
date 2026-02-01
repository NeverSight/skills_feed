---
name: xhs-cover-skill
description: Generates image generation prompts for Xiaohongshu covers based on user content. It polishes the content to fit Xiaohongshu style + applies a visual style template to produce a JSON output for image generation.
---

# Xiaohongshu Cover Generator (xhs-cover-skill)

This skill helps you turn raw content into a high-quality image generation prompt suitable for a Xiaohongshu cover.

## Workflow

1.  **Analyze Content**: Read the user's provided content.
2.  **Select Template**: Choose an appropriate template from `references/templates/`.
    *   Default: `references/templates/style_infographic_cartoon.md` (unless user specifies otherwise).
3.  **Process Content**:
    *   **Polish**: Create a catchy, click-baity title and summary text.
    *   **Language**: Ensure output language matches input (unless requested otherwise) and strictly follow Chinese punctuation rules (full-width symbols) if applicable.
    *   **Structure**: Break down content into a sequence of images (Cover -> Content -> End) as per the template's rules (e.g., 2-10 slides).
4.  **Generate JSON**: Output the final result in the strict JSON format below.

## Output Format

The output must be a single JSON object.

```json
{
  "title": "The Main Title 🌟",
  "content_polished": "The polished caption text for the post...",
  "tags": ["#Tag1", "#Tag2"],
  "image_prompts": [
    {
      "index": 1,
      "type": "Cover | Content | End",
      "text_overlays": {
        "title": "Text on image",
        "subtitle": "Subtitle on image",
        "notes": "Any extra text"
      },
      "prompt": "Full English image generation prompt...",
      "negative_prompt": "..."
    }
  ]
}
```

## Example Interaction (Infographic Style)

**User:** "Explain how to make perfect scrambled eggs."

**Model:**
```json
{
  "title": "🍳 Perfect Eggs Every Time! Secret Revealed! 😋",
  "content_polished": "Stop making rubbery eggs! 🛑 These simple tips will change your breakfast game forever. Creamy, fluffy, and delicious! #BreakfastHacks #ScrambledEggs #Foodie",
  "tags": ["#CookingTips", "#Breakfast"],
  "image_prompts": [
    {
      "index": 1,
      "type": "Cover",
      "text_overlays": {
        "title": "PERFECT SCRAMBLED EGGS",
        "subtitle": "Creamy & Fluffy!"
      },
      "prompt": "Xiaohongshu style infographic, vertical (3:4), cartoon style, hand-drawn text, cream background. Illustration of a plate of fluffy yellow scrambled eggs with steam rising. Cute chef character giving a thumbs up. Title 'PERFECT SCRAMBLED EGGS' in bold playful font at top. Watermark '岚叔' at bottom right.",
      "negative_prompt": "photorealistic, dark, messy"
    },
    {
      "index": 2,
      "type": "Content",
      "text_overlays": {
        "title": "Step 1: Low Heat",
        "subtitle": "Don't rush it!"
      },
      "prompt": "Xiaohongshu style infographic, vertical (3:4), cartoon style. Illustration of a frying pan on a stove with a small flame. Text 'Step 1: Low Heat'. Cute egg character sweating. Pastel colors.",
      "negative_prompt": "photorealistic"
    }
  ]
}
```

## Resources

*   `references/templates/`: Contains the style templates (e.g., `style_infographic_cartoon.md`, `style_infographic_pro.md`).
*   `references/xiaohongshu_style_guide.md`: Tips for Xiaohongshu stylization.
