---
name: anime-to-life
description: Transforms anime, art, or 3D rendering images into photorealistic cosplay-style photographs using a specific JSON-based prompt structure.
version: 1.0.0
---

# Anime to Life

## Capability
Transforms an uploaded anime, art, or 3D rendering image into a photorealistic photograph. It generates a real person (cosplayer) matching the character's features, pose, and background details in a realistic style.

## Triggers
- User uploads an anime, art, or 3D image and asks to "bring it to life", "make it real", "realistic version", or "generate a photo of this".

## Instructions
1.  **Analyze Input**: Analyze the input image features.
2.  **Identify Character**:
    - Use `search_web` to fully identify the character.
    - Retrieve: Name, source material, canonical ethnicity, and detailed appearance traits (hair, eyes, clothing, accessories).
3.  **Execute Logic**: Apply the retrieved data to the following **Core Prompt Logic**:

```json
{
  "name": "anime_to_life",
  "task": "User uploads an anime or art or 3D rendering image, the AI will completely generate a photorealistic photograph featuring the same character in the same background. Character and environment both transformed to photorealistic style yet retaining original features.",
  "pre_processing": {
    "step_1": "Analyze input image features",
    "step_2": "Use SEARCH to fully identify the character: retrieve name, source material, canonical ethnicity, and detailed appearance traits (hair, eyes, clothing, accessories)",
    "step_3": "Apply retrieved data to the subject parameters below"
  },
  "subject": "Real person cosplayer (Russian or Japanese ethnicity based on character identity), pretty appearance with delicate and refined idol-style makeup, anime-inspired facial features, identical physique, eye color, clothing, hair and props to the original character",
  "action": "Exact match of original pose, position, and facial expression",
  "environment": "The original background shall be rendered in a realistic style matching the source image",
  "lighting": "Photorealistic lighting matching the source image's mood and direction",
  "camera": "Identical framing and camera angle to the uploaded image, photorealistic lens characteristics",
  "style": "Photorealistic photography, high fidelity, 8k, realistic skin texture, authentic fabric details, cosplay photography style",
  "negative_constraint": "The generated image must NOT look like art, anime, CGI, 3D rendering, drawing, or painting. It must be a photorealistic photograph.",
  "final_step": "GENERATE the image"
}
```

4.  **Generate**: Use the image generation tool.
    - **Prompt**: Construct a comprehensive prompt based on the JSON logic above, incorporating the identified character details and constraints.
    - **Reference Images**: Include the user's original uploaded image path to ensure the pose and composition are matched.

## Tools / Commands
- `search_web`: specific inputs: `query="character name appearance details"`
- Image generation tool: specific inputs: `Prompt="..."`, `Reference Images=["..."]`

## Examples
User: [Uploads image of detailed anime girl] "Bring this to life."
Action:
1. Agent searches to identify the character (e.g., "Asuka Langley Soryu").
2. Agent follows the JSON logic to construct the prompt parameters.
3. Agent calls the image generation tool with the constructed prompt and image paths.
