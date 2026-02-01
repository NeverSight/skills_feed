---
name: image-generation
description: Generate images using AI models (Gemini 2.5 Flash Image, Gemini 3 Pro Image Preview, or Imagen). Use when the user asks to generate, create, or draw an image.
---

# Image Generation

This skill enables generating images using Google's Gemini API (specifically the "Nano Banana" models) or OpenRouter.

## Models

### Google Gemini API
- **Nano Banana** (`gemini-2.5-flash-image`): Designed for speed and efficiency. Default model.
- **Nano Banana Pro** (`gemini-3-pro-image-preview`): Built on Gemini 3, this is the most advanced image model. Key capabilities:
  - State-of-the-art text rendering in multiple languages
  - Real-world knowledge and deep reasoning for precise, detailed results
  - Advanced controls: up to 14 input images for composition
  - Studio-quality editing: lighting, camera settings, color grading
  - High-fidelity resolutions: 1K, 2K, and 4K
  - Brand consistency and character resemblance across edits

## Prerequisites

You need an API key to use this skill. The recommended way is to create a `.env` file in this skill's directory (`<your-skill-directory>/image-generation/`), but placing it in the workspace root is also supported.

1.  Create a `.env` file in the skill directory:
    ```bash
    touch <your-skill-directory>/image-generation/.env
    ```
2.  Add your API key(s) to the `.env` file:
    ```env
    GEMINI_API_KEY=AIzaSy...
    # OR
    OPENROUTER_API_KEY=sk-or-v1-...
    ```

## Usage

To generate an image, run the script located in this skill's directory.

### Command

```bash
<your-skill-directory>/image-generation/scripts/generate_image.ts "Your prompt here"
```

### Options

- `--output`, `-o`: Specify output filename (default: `image_TIMESTAMP.png`)
- `--provider`: Force `openrouter` or `gemini`. If not specified, auto-detects based on available API keys:
  - If only `OPENROUTER_API_KEY` is set: uses OpenRouter
  - If only `GEMINI_API_KEY` is set: uses Gemini
  - If both keys are set: defaults to Gemini
- `--model`: Specify a custom model ID (default: `google/gemini-3-pro-image-preview` for OpenRouter, `gemini-2.5-flash-image` for Gemini)
- `--aspect-ratio`: Aspect ratio (e.g., `1:1`, `16:9`, `4:3`, `3:4`, `5:4`, `9:16`). Default: `1:1`.
- `--image-size`: Resolution (`1K`, `2K`, `4K`). Only supported by `gemini-3-pro-image-preview`.
- `--input-images`: Paths to input images for editing or composition (supported by Gemini).
- `--api-key`: Pass API key directly if not in env vars

**Important:** Do NOT specify `--provider` or `--model` unless explicitly requested by the user. The script auto-detects the provider based on available API keys and uses sensible defaults for the model.
**Important:** Before specifying an output path with `--output`, ALWAYS check if a file already exists at that path. NEVER overwrite an existing image unless the user explicitly requests it. When in doubt, let the script generate a timestamped filename automatically.

## Examples

**Example 1: Basic Generation**

User: "Generate an image of a futuristic city."

Action:
```bash
<your-skill-directory>/image-generation/scripts/generate_image.ts "A futuristic city with flying cars and neon lights"
```

**Example 2: High Quality with 4K Resolution**

User: "Create a detailed 4K infographic about photosynthesis"

Action:
```bash
<your-skill-directory>/image-generation/scripts/generate_image.ts "A vibrant infographic that explains photosynthesis" --model gemini-3-pro-image-preview --aspect-ratio 16:9 --image-size 4K
```

**Example 3: Specific Aspect Ratio**

User: "Draw a portrait of a cat in 3:4 ratio"

Action:
```bash
<your-skill-directory>/image-generation/scripts/generate_image.ts "A portrait of a fluffy cat" --aspect-ratio 3:4
```

**Example 4: Image Editing (Add/Remove Elements)**

User: "Add a wizard hat to this cat image"

Action:
```bash
<your-skill-directory>/image-generation/scripts/generate_image.ts "Add a small knitted wizard hat on the cat's head. Make it look natural." --input-images cat.png
```

**Example 5: Style Transfer**

User: "Make this city photo look like a Van Gogh painting"

Action:
```bash
<your-skill-directory>/image-generation/scripts/generate_image.ts "Transform this photograph into the artistic style of Vincent van Gogh's Starry Night. Preserve the composition but render with swirling brushstrokes and deep blues." --input-images city.png
```

**Example 6: Combining Multiple Images**

User: "Put this dress on this model"

Action:
```bash
<your-skill-directory>/image-generation/scripts/generate_image.ts "Create a professional fashion photo. The woman from the second image is wearing the dress from the first image." --input-images dress.png model.png
```

## Image Editing Guide

Image editing (text-and-image-to-image) allows you to provide images alongside text prompts to add, remove, or modify elements, change style, or compose new scenes.

### Input Image Limits
- **`gemini-2.5-flash-image`**: Works best with up to 3 input images.
- **`gemini-3-pro-image-preview`**: Supports up to 5 images with high fidelity, and up to 14 images total.

### Editing Templates

#### 1. Adding and Removing Elements
Provide an image and describe your change. The model matches the original style, lighting, and perspective.

**Template:**
> Using the provided image of [subject], please [add/remove/modify] [element] to/from the scene. Ensure the change [description of how it should integrate].

#### 2. Inpainting (Semantic Masking)
Conversationally define a "mask" to edit a specific part while leaving the rest untouched.

**Template:**
> Using the provided image, change only the [specific element] to [new description]. Keep everything else exactly the same, preserving the original style, lighting, and composition.

#### 3. Style Transfer
Recreate an image's content in a different artistic style.

**Template:**
> Transform the provided photograph of [subject] into the artistic style of [artist/style]. Preserve the original composition but render with [stylistic elements].

#### 4. Advanced Composition (Multiple Images)
Combine elements from multiple images into a new scene.

**Template:**
> Create a new image by combining the elements from the provided images. Take the [element from image 1] and place it with/on the [element from image 2]. The final image should be [description].

#### 5. High-Fidelity Detail Preservation
To ensure critical details (face, logo) are preserved, describe them explicitly.

**Template:**
> Using the provided images, place [element from image 2] onto [element from image 1]. Ensure that the features of [element] remain completely unchanged. The added element should [integration description].

#### 6. Sketch to Finished Image
Turn rough sketches into polished renders.

**Template:**
> Turn this rough [medium] sketch of a [subject] into a [style description] photo. Keep the [specific features] from the sketch but add [new details].

#### 7. Character Consistency (360 View)
Generate different angles of a character by iteratively prompting.

**Template:**
> A studio portrait of this [person/character] against [background], [pose/angle description].

## Prompting Guide

Mastering image generation starts with one fundamental principle: **Describe the scene, don't just list keywords.** A narrative, descriptive paragraph will almost always produce a better, more coherent image than a list of disconnected words.

**Important:** Before crafting a prompt, first check `image-generation/assets/` for existing curated prompt templates that match the user's request. Use or adapt these templates when available.

### Establishing the Vision: Core Prompt Elements

To achieve the best results and have nuanced creative control, structure your prompts with these elements:

| Element | Description | Example |
|---------|-------------|---------|
| **Subject** | Who or what is in the image? Be specific. | "A stoic robot barista with glowing blue optics" or "A fluffy calico cat wearing a tiny wizard hat" |
| **Composition** | How is the shot framed? | "Extreme close-up", "wide shot", "low angle shot", "portrait" |
| **Action** | What is happening? | "Brewing a cup of coffee", "casting a magical spell", "mid-stride running through a field" |
| **Location** | Where does the scene take place? | "A futuristic cafe on Mars", "a cluttered alchemist's library", "a sun-drenched meadow at golden hour" |
| **Style** | What is the overall aesthetic? | "3D animation", "film noir", "watercolor painting", "photorealistic", "1990s product photography" |
| **Editing Instructions** | For modifying existing images, be direct and specific. | "Change the man's tie to green", "remove the car in the background" |

### Refining the Details: Advanced Controls

While simple prompts work, achieving professional results requires more specific instructions:

- **Composition and aspect ratio:** Define the canvas. (e.g., "A 9:16 vertical poster," "A cinematic 21:9 wide shot.")
- **Camera and lighting details:** Direct the shot like a cinematographer. (e.g., "A low-angle shot with a shallow depth of field (f/1.8)," "Golden hour backlighting creating long shadows," "Cinematic color grading with muted teal tones.")
- **Specific text integration:** Clearly state what text should appear and how. (e.g., "The headline 'URBAN EXPLORER' rendered in bold, white, sans-serif font at the top.")
- **Factual constraints (for diagrams):** Specify accuracy needs and ensure inputs are factual. (e.g., "A scientifically accurate cross-section diagram," "Ensure historical accuracy for the Victorian era.")
- **Reference inputs:** When using uploaded images, clearly define each role. (e.g., "Use Image A for the character's pose, Image B for the art style, and Image C for the background environment.")

### 1. Photorealistic scenes
For realistic images, use photography terms. Mention camera angles, lens types, lighting, and fine details.

**Template:**
> A photorealistic [shot type] of [subject], [action or expression], set in [environment]. The scene is illuminated by [lighting description], creating a [mood] atmosphere. Captured with a [camera/lens details], emphasizing [key textures and details].

### 2. Stylized illustrations & stickers
To create stickers, icons, or assets, be explicit about the style and request a transparent background (if needed).

**Template:**
> A [style] sticker of a [subject], featuring [key characteristics] and a [color palette]. The design should have [line style] and [shading style]. The background must be transparent.

### 3. Accurate text in images
Gemini excels at rendering text in multiple languages. Be clear about the text, the font style (descriptively), and the overall design. Use **Gemini 3 Pro Image Preview** for professional asset production.

**Template:**
> Create a [image type] for [brand/concept] with the text "[text to render]" in a [font style]. The design should be [style description], with a [color scheme].

**Example (wordplay):**
> Create an image showing the phrase "How much wood would a woodchuck chuck if a woodchuck could chuck wood" made out of wood chucked by a woodchuck.

### 4. Product mockups & commercial photography
Perfect for creating clean, professional product shots for ecommerce, advertising, or branding.

**Template:**
> A high-resolution, studio-lit product photograph of a [product description] on a [background surface/description]. The lighting is a [lighting setup] to [lighting purpose]. The camera angle is a [angle type] to showcase [specific feature]. Ultra-realistic, with sharp focus on [key detail].

### 5. Minimalist & negative space design
Excellent for creating backgrounds for websites, presentations, or marketing materials where text will be overlaid.

**Template:**
> A minimalist composition featuring a single [subject] positioned in the [bottom-right/top-left/etc.] of the frame. The background is a vast, empty [color] canvas, creating significant negative space. Soft, subtle lighting.

### 6. Sequential art (Comic panel / Storyboard)
Builds on character consistency and scene description to create panels for visual storytelling.

**Template:**
> Make a 3 panel comic in a [style]. Put the character in a [type of scene].

**Example:**
> Create a storyboard for this scene (with input image)

### 7. Translation and Localization
Generate localized text, or translate text inside images for international markets.

**Template:**
> Translate all the [source language] text on [object description] into [target language], while keeping everything else the same.

**Example:**
> Translate all the English text on the three yellow and blue cans into Korean, while keeping everything else the same.

### 8. Infographics and Diagrams
Create data-driven visuals with real-world knowledge. Always verify factual accuracy of generated diagrams.

**Template:**
> Create an infographic that shows [topic/process]. Include [specific elements]. Use a [style] design with [color scheme].

**Example:**
> Create an infographic that shows how to make elaichi chai.

### 9. Studio-Quality Lighting and Camera Control
Directly influence lighting and camera settings for professional results.

**Template:**
> [Scene description]. Use [lighting type] lighting. Camera settings: [angle], [focus], [color grading].

**Examples:**
> Turn this scene into nighttime (with input image)
> Focus on the flowers (with input image)

### 10. Brand Identity Systems
Render and apply designs with consistent brand styling. Create logo variations and mockups.

**Template (Logo):**
> Create a smooth logo in a [style] based on [concept]. The letters should be [letter style description]. Use [color palette].

**Template (Identity System):**
> Now create identity system one by one, use [number] high quality mockups with variety of relevant products, ads, billboards, bus stop, etc. Generate one at a time, 16:9 each.

### 11. Image Blending and Character Consistency
Combine multiple images while maintaining character resemblance. Supports 6-14 input images depending on surface.

**Template:**
> Combine these images into one appropriately arranged [style] image in [aspect ratio] format. [Specific instructions for each element].

**Example:**
> Combine these images into one appropriately arranged cinematic image in 16:9 format and change the dress on the mannequin to the dress in the image.

## Best Practices

- **Be Hyper-Specific:** Instead of "fantasy armor," describe: "ornate elven plate armor, etched with silver leaf patterns, with a high collar and pauldrons shaped like falcon wings."
- **Provide Context and Intent:** Explain the purpose. "Create a logo for a high-end, minimalist skincare brand" yields better results than just "Create a logo."
- **Iterate and Refine:** Use follow-up prompts like "That's great, but make the lighting warmer" or "Keep everything the same, but change the expression."
- **Use Step-by-Step Instructions:** For complex scenes, break into steps. "First, create a background of a misty forest. Then, add a stone altar. Finally, place a glowing sword on the altar."
- **Use Semantic Negative Prompts:** Instead of "no cars," describe positively: "an empty, deserted street with no signs of traffic."
- **Control the Camera:** Use photography terms like `wide-angle shot`, `macro shot`, `low-angle perspective`, `85mm portrait lens`, `shallow depth of field (f/1.8)`.
- **Image Order Matters:** When using input images with text, the text prompt typically comes after the images.
- **Leverage Real-World Knowledge:** Nano Banana Pro uses Gemini 3's reasoning capabilities—ask for historically accurate, scientifically precise, or culturally specific content.
- **Experiment with Aspect Ratios:** Different ratios suit different purposes. Generate crisp visuals at 1K, 2K, or 4K across 9:16 (vertical poster), 16:9 (cinematic), 1:1 (social), etc.
- **Define Reference Image Roles:** When using multiple images, explicitly state each image's purpose (e.g., "Image A for pose, Image B for style, Image C for background").

## Limitations

### General Limits
- **Languages:** Best performance in EN, ar-EG, de-DE, es-MX, fr-FR, hi-IN, id-ID, it-IT, ja-JP, ko-KR, pt-BR, ru-RU, ua-UA, vi-VN, zh-CN.
- **No Audio/Video Input:** Image generation does not support audio or video inputs.
- **Image Count:** May not always follow the exact number of requested output images.
- **Input Images:** `gemini-2.5-flash-image` works best with up to 3 images; `gemini-3-pro-image-preview` supports 5 high-fidelity images (up to 14 total).
- **Watermarks:** All generated images include a SynthID watermark.

### Known Quality Limitations
These are areas where the model may produce imperfect results:

- **Visual and text fidelity:** Rendering small text, fine details, and producing accurate spellings may not work perfectly. For best results, generate text first, then ask for an image containing that text.
- **Data and factual accuracy:** Always verify the factual accuracy of data-driven visuals like diagrams and infographics.
- **Translation and localization:** Multilingual text generation may make grammar mistakes or miss specific cultural nuances.
- **Complex edits and image blending:** Advanced editing tasks like blending or lighting changes can sometimes produce unnatural artifacts.
- **Character features:** While usually reliable, character consistency across edits may vary.

## Troubleshooting

- **No API key found**: Ensure you have a `.env` file in your workspace root or skill directory with `GEMINI_API_KEY`.
- **Model errors**: Ensure you are using the correct model ID (`gemini-2.5-flash-image` or `gemini-3-pro-image-preview`).
- **Resolution errors**: `1K`, `2K`, `4K` must be uppercase. Only supported on Gemini 3 Pro.
