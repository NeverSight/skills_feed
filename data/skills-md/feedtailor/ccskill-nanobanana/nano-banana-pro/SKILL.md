---
name: nano-banana-pro
description: |
  Skill for image generation.
  Uses Google Nano Banana Pro (Gemini 3 Pro Image) API to generate high-quality images.
  Supports logos, infographics, illustrations, photorealistic images, and more.
---

# Nano Banana Pro Image Generation Skill

## Overview

This skill uses the Google Nano Banana Pro API to generate images.
Use this skill when users need image generation.

## Prerequisites

- Set the environment variable `CCSKILL_NANOBANANA_DIR` to the path of this skill's repository
  ```bash
  export CCSKILL_NANOBANANA_DIR="$HOME/projects/ccskill-nanobanana"
  ```
- The environment variable `GEMINI_API_KEY` must be set (or specified in `$CCSKILL_NANOBANANA_DIR/.env`)

## Usage

Generate images with the following command:

```bash
$CCSKILL_NANOBANANA_DIR/venv/bin/python $CCSKILL_NANOBANANA_DIR/generate_image.py "prompt"
```

### Options

- `--resolution`: Resolution (1K, 2K, 4K) Default: 2K
- `--aspect`: Aspect ratio (1:1, 16:9, 9:16, 4:3, etc.) Default: 16:9
- `--output`: Output directory Default: ./generated_images
- `--reference`: Reference image path (multiple allowed, up to 14)

### Examples

Basic image generation:
```bash
$CCSKILL_NANOBANANA_DIR/venv/bin/python $CCSKILL_NANOBANANA_DIR/generate_image.py "a cat playing piano in watercolor style"
```

High-resolution wide image:
```bash
$CCSKILL_NANOBANANA_DIR/venv/bin/python $CCSKILL_NANOBANANA_DIR/generate_image.py "sunset coastline" --resolution 4K --aspect 16:9
```

Output to specific directory:
```bash
$CCSKILL_NANOBANANA_DIR/venv/bin/python $CCSKILL_NANOBANANA_DIR/generate_image.py "logo design" --output ./assets/images
```

### Reference Image Editing

Edit or modify existing images by providing reference images:

```bash
# Change background
$CCSKILL_NANOBANANA_DIR/venv/bin/python $CCSKILL_NANOBANANA_DIR/generate_image.py "change background to sunset" --reference ./original.png

# Use multiple reference images (pose, style, etc.)
$CCSKILL_NANOBANANA_DIR/venv/bin/python $CCSKILL_NANOBANANA_DIR/generate_image.py "draw this person in this pose" --reference ./person.png --reference ./pose.png
```

Reference image use cases:
- Partial image editing (background change, color adjustment, etc.)
- Style transfer (apply style from another image)
- Character consistency (same person in different scenes)
- Image compositing

## Prompting Guide

### Quick Reference

> Source: [7 tips to get the most out of Nano Banana Pro](https://blog.google/products/gemini/prompting-tips-nano-banana-pro/) - Google Official Blog

Include these elements in your prompts for better results:

- **Subject**: Who/what is in the image? Be specific. (e.g., "a stoic robot barista with glowing blue eyes", "a fluffy calico cat wearing a tiny wizard hat")
- **Composition**: How is the shot framed? (e.g., extreme close-up, wide shot, low-angle shot, portrait)
- **Action**: What's happening? (e.g., brewing coffee, casting a spell, mid-run through a meadow)
- **Location**: Where does the scene take place? (e.g., a futuristic cafe on Mars, a cluttered alchemist's study, a sunlit meadow at golden hour)
- **Style**: What's the overall aesthetic? (e.g., 3D animation, film noir, watercolor, photorealistic, 1990s product photography)
- **Editing Instructions**: When editing existing images, be direct and specific. (e.g., "change the man's tie to green", "remove the car from the background")

For professional results, include more specific instructions:

- **Composition & Aspect Ratio**: Define the canvas (e.g., "9:16 vertical poster", "cinematic 21:9 wide shot")
- **Camera & Lighting**: Direct the shot like a cinematographer (e.g., "low-angle shot with shallow depth of field (f/1.8)", "golden hour backlight casting long shadows")
- **Text Integration**: Clearly specify text appearance and placement (e.g., "place the headline 'URBAN EXPLORER' at the top in bold, white, sans-serif font")

### Comprehensive Guide

> Source: Guillaume Vernade, Gemini Developer Advocate, Google DeepMind
> - [X/Twitter Thread](https://x.com/GoogleAIStudio/status/1994480371061469306)

#### The Golden Rules of Prompting

Nano-Banana Pro is a "Thinking" model. It doesn't just match keywords; it understands intent, physics, and composition. To get the best results, stop using "tag soups" (e.g., dog, park, 4k, realistic) and start acting like a Creative Director.

**1. Edit, Don't Re-roll**

The model is exceptionally good at understanding conversational edits. If an image is 80% correct, do not generate a new one from scratch. Instead, simply ask for the specific change you need.

Example: "That's great, but change the lighting to sunset and make the text neon blue."

**2. Use Natural Language & Full Sentences**

Talk to the model as if you were briefing a human artist. Use proper grammar and descriptive adjectives.

- Bad: "Cool car, neon, city, night, 8k."
- Good: "A cinematic wide shot of a futuristic sports car speeding through a rainy Tokyo street at night. The neon signs reflect off the wet pavement and the car's metallic chassis."

**3. Be Specific and Descriptive**

Vague prompts yield generic results. Define the subject, the setting, the lighting, and the mood.

- Subject: Instead of "a woman," say "a sophisticated elderly woman wearing a vintage chanel-style suit."
- Materiality: Describe textures. "Matte finish," "brushed steel," "soft velvet," "crumpled paper."

**4. Provide Context (The "Why" or "For whom")**

Because the model "thinks," giving it context helps it make logical artistic decisions.

Example: "Create an image of a sandwich for a Brazilian high-end gourmet cookbook." (The model will infer professional plating, shallow depth of field, and perfect lighting).

#### Text Rendering, Infographics & Visual Synthesis

Nano-Banana Pro has SOTA capabilities for rendering legible, stylized text and synthesizing complex information into visual formats.

**Best Practices:**
- Compression: Ask the model to "compress" dense text or PDFs into visual aids.
- Style: Specify if you want a "polished editorial," a "technical diagram," or a "hand-drawn whiteboard" look.
- Quotes: Clearly specify the text you want in quotes.

**Example Prompts:**

Earnings Report Infographic (Data Ingestion):
```
[Input PDF of Google's latest earnings report]
"Generate a clean, modern infographic summarizing the key financial highlights from this earnings report. Include charts for 'Revenue Growth' and 'Net Income', and highlight the CEO's key quote in a stylized pull-quote box."
```

Retro Infographic:
```
"Make a retro, 1950s-style infographic about the history of the American diner. Include distinct sections for 'The Food,' 'The Jukebox,' and 'The Decor.' Ensure all text is legible and stylized to match the period."
```

Technical Diagram:
```
"Create an orthographic blueprint that describes this building in plan, elevation, and section. Label the 'North Elevation' and 'Main Entrance' clearly in technical architectural font. Format 16:9."
```

Whiteboard Summary (Educational):
```
"Summarize the concept of 'Transformer Neural Network Architecture' as a hand-drawn whiteboard diagram suitable for a university lecture. Use different colored markers for the Encoder and Decoder blocks, and include legible labels for 'Self-Attention' and 'Feed Forward'."
```

#### Character Consistency & Viral Thumbnails

Nano-Banana Pro supports up to 14 reference images (6 with high fidelity). This allows for "Identity Locking"—placing a specific person or character into new scenarios without facial distortion.

**Best Practices:**
- Identity Locking: Explicitly state: "Keep the person's facial features exactly the same as Image 1."
- Expression/Action: Describe the change in emotion or pose while maintaining the identity.
- Viral Composition: Combine subjects with bold graphics and text in a single pass.

**Example Prompts:**

The "Viral Thumbnail" (Identity + Text + Graphics):
```
"Design a viral video thumbnail using the person from Image 1. Face Consistency: Keep the person's facial features exactly the same as Image 1, but change their expression to look excited and surprised. Action: Pose the person on the left side, pointing their finger towards the right side of the frame. Subject: On the right side, place a high-quality image of a delicious avocado toast. Graphics: Add a bold yellow arrow connecting the person's finger to the toast. Text: Overlay massive, pop-style text in the middle: '3 mins!' Use a thick white outline and drop shadow. Background: A blurred, bright kitchen background. High saturation and contrast."
```

The "Fluffy Friends" Scenario (Group Consistency):
```
[Input 3 images of different plush creatures]
"Create a funny 10-part story with these 3 fluffy friends going on a tropical vacation. The story is thrilling throughout with emotional highs and lows and ends in a happy moment. Keep the attire and identity consistent for all 3 characters, but their expressions and angles should vary throughout all 10 images. Make sure to only have one of each character in each image."
```

Brand Asset Generation:
```
[Input 1 image of a product]
"Create 9 stunning fashion shots as if they're from an award-winning fashion editorial. Use this reference as the brand style but add nuance and variety to the range so they convey a professional design touch. Please generate nine images, one at a time."
```

#### Advanced Editing, Restoration & Colorization

The model excels at complex edits via conversational prompting. This includes "In-painting" (removing/adding objects), "Restoration" (fixing old photos), "Colorization" (Manga/B&W photos), and "Style Swapping."

**Best Practices:**
- Semantic Instructions: You do not need to manually mask; simply tell the model what to change naturally.
- Physics Understanding: You can ask for complex changes like "fill this glass with liquid" to test physics generation.

**Example Prompts:**

Object Removal & In-painting:
```
"Remove the tourists from the background of this photo and fill the space with logical textures (cobblestones and storefronts) that match the surrounding environment."
```

Manga/Comic Colorization:
```
[Input black and white manga panel]
"Colorize this manga panel. Use a vibrant anime style palette. Ensure the lighting effects on the energy beams are glowing neon blue and the character's outfit is consistent with their official colors."
```

Localization (Text Translation + Cultural Adaptation):
```
[Input image of a London bus stop ad]
"Take this concept and localize it to a Tokyo setting, including translating the tagline into Japanese. Change the background to a bustling Shibuya street at night."
```

Lighting/Seasonal Control:
```
[Input image of a house in summer]
"Turn this scene into winter time. Keep the house architecture exactly the same, but add snow to the roof and yard, and change the lighting to a cold, overcast afternoon."
```

#### Dimensional Translation (2D to 3D)

A powerful new capability is translating 2D schematics into 3D visualizations, or vice versa. This is ideal for interior designers, architects, and meme creators.

**Example Prompts:**

2D Floor Plan to 3D Interior Design Board:
```
"Based on the uploaded 2D floor plan, generate a professional interior design presentation board in a single image. Layout: A collage with one large main image at the top (wide-angle perspective of the living area), and three smaller images below (Master Bedroom, Home Office, and a 3D top-down floor plan). Style: Apply a Modern Minimalist style with warm oak wood flooring and off-white walls across ALL images. Quality: Photorealistic rendering, soft natural lighting."
```

2D to 3D Meme Conversion:
```
"Turn the 'This is Fine' dog meme into a photorealistic 3D render. Keep the composition identical but make the dog look like a plush toy and the fire look like realistic flames."
```

#### One-Shot Storyboarding & Concept Art

You can generate sequential art or storyboards without a grid, ensuring a cohesive narrative flow in a single session. This is also popular for "Movie Concept Art" (e.g., fake leaks of upcoming films).

**Example Prompt:**
```
"Create an addictively intriguing 9-part story with 9 images featuring a woman and man in an award-winning luxury luggage commercial. The story should have emotional highs and lows, ending on an elegant shot of the woman with the logo. The identity of the woman and man and their attire must stay consistent throughout but they can and should be seen from different angles and distances. Please generate images one at a time. Make sure every image is in a 16:9 landscape format."
```

#### Structural Control & Layout Guidance

Input images aren't limited to character references or subjects to edit. You can use them to strictly control the composition and layout of the final output. This is a game-changer for designers who need to turn a napkin sketch, a wireframe, or a specific grid layout into a polished asset.

**Best Practices:**
- Drafts & Sketches: Upload a hand-drawn sketch to define exactly where the text and object should sit.
- Wireframes: Use screenshots of existing layouts or wireframes to generate high-fidelity UI mockups.
- Grids: Use grid images to force the model to generate assets for tile-based games or LED displays.

**Example Prompts:**

Sketch to Final Ad:
```
"Create a ad for a [product] following this sketch."
```

UI Mockup from Wireframe:
```
"Create a mock-up for a [product] following these guidelines."
```

Pixel Art & LED Displays:
```
"Generate a pixel art sprite of a unicorn that fits perfectly into this 64x64 grid image. Use high contrast colors."
(Tip: Developers can then programmatically extract the center color of each cell to drive a connected 64x64 LED matrix display).
```

Sprites:
```
"Sprite sheet of a woman doing a backflip on a drone, 3x3 grid, sequence, frame by frame animation, square aspect ratio. Follow the structure of the attached reference image exactly."
(Tip: You can then extract each cell and make a gif)
```

### Current Limitations

- Small text, fine details, and accurate spelling may not be perfect
- Always verify factual accuracy of diagrams and infographics
- Multilingual text generation may have grammatical errors or lack cultural nuance
- Advanced edits like compositing or lighting changes may produce unnatural artifacts

## Output

- Images are saved to the specified directory (default: `./generated_images`)
- Filename format is timestamp (e.g., `20251130_153045.png`, `20251130_153045.jpg`)
- File extension is automatically determined based on the API response format (PNG/JPEG/WebP)

## Notes

- The environment variable `GEMINI_API_KEY` must be set
- Nano Banana Pro is a paid API, so charges will apply
- Generated images include SynthID watermark
