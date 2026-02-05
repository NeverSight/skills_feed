---
name: photo-restoration
description: Restores vintage and blurry photos to high-definition 8k images while preserving identity.
version: 1.0.0
---

# Photo Restoration

## Capability
Transform blurry, vintage, or low-quality images into crystal-clear, 8k resolution modern photographs while preserving the original identity, pose, and composition.

## Triggers
- "Restore this photo."
- "Fix this blurry image."
- "Make this vintage photo look modern."
- "Upscale and sharpen this picture."

## Instructions
1.  **Analyze the User's Image**:
    - Note the subject's identity, pose, and composition.
    - Identify areas needing restoration: blur, grain, focus, lighting.

2.  **Construct the Image Generation Prompt**:
    - **Core Command**: "High-fidelity restoration of this vintage photograph. Transform this blurry image into a crystal-clear, 8k resolution modern photograph."
    - **Enhancements**: "Sharpen all details, remove film grain, and correct focus. Enhance facial features to be lifelike and highly detailed, ensuring realistic skin texture and eye clarity. Fix lighting to be balanced and natural."
    - **Preservation**: "Upscale to high definition while preserving the original identity, pose, and composition."
    - **Style**: "Professional portrait photography, shot on a 85mm lens, f/1.8, photorealistic, cinematic lighting."
    - **Constraint**: "While largely improving the quality of the photo, the restored image should remain identical to the original."

3.  **Generate the Image**:
    - Use the image generation tool.
    - Pass the constructed prompt.
    - Pass the user's uploaded image path in the reference image parameter to use as a reference/control.

## Tools / Commands
- Image generation tool: To generate the restored image based on the input.

## Examples
User: "Restore this old photo." (User attaches `[image]`)
Action:
1. Construct prompt using the standard restoration template.
2. Call the image generation tool with the constructed prompt and image paths.
