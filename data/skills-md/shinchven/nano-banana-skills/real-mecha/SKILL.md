---
name: real-mecha
description: Converts 2D/anime mecha art into photorealistic 3D/real-world visualizations with high-fidelity material textures.
version: 1.0.0
---

# Real Mecha

## Capability
Transforms an uploaded anime, art, or 2D rendering of a mecha/robot into a completely photorealistic photograph. It converts both the mechanical unit and the background into a cohesive real-world scene, replacing drawn textures with realistic hard-surface materials while maintaining the exact silhouette, pose, and loadout.

## Triggers
- "Make this mecha look real."
- "Convert this robot drawing to a photo."
- "Real life version of this mecha."
- "Photorealistic mecha."

## Instructions
1.  **Analyze the Input Image**:
    - Identify the mecha's overall design, chassis shape, weapon loadout, and specific pose/posture.
    - Identify the background elements (buildings, terrain, sky, debris).
    - Note the lighting direction and camera angle.

2.  **Construct the Image Generation Prompt**:
    - **Subject**: "A photorealistic photograph of a mechanical unit..."
    - **Structure**: "...retaining the exact chassis design, silhouette, posture, and weapon loadout."
    - **Materials**: "Replace drawn textures with realistic hard-surface materials: painted automotive metal, weathered steel, brushed aluminum, carbon fiber, and reinforced glass."
    - **Details**: "Functioning machine details: grease in joints, heat discoloration on exhausts. **Brand new condition**, surface is clean, NO dirt, NO dust, NO rust."
    - **Sensors**: "Optical sensors as functional hardware: lenses, reflective glass, glowing LED arrays (no cartoon eyes)."
    - **Environment**: "Photorealistic 3D environment: [describe background], with realistic textures, volumetric lighting, atmospheric haze, and physically accurate shadows."
    - **Photography**: "Match exact angle, framing, and dramatic lighting direction."

3.  **Generate the Image**:
    - Use the image generation tool.
    - Pass the constructed prompt.
    - Pass the user's uploaded image path as the reference image to strictly control structure/pose.

## Tools / Commands
- Image generation tool: To generate the photorealistic image.

## Examples
User: "Make this Gundam drawing realistic." (User attaches `[image]`)
Action:
1. Analyze: Gundam-style mecha, white/blue/red scheme, beam rifle, space colony background.
2. Prompt: "A photorealistic photograph of a massive mecha unit in a space colony. Hard-surface automotive metal and brushed aluminum plating. Carbon fiber internal frame. Functional glass camera lenses for eyes. Heat discoloration on thrusters. Brand new condition, clean surfaces, grease in joints. Background of cylindrical colony habitat with atmospheric haze and volumetric lighting. Exact angle and pose match."
3. Call generation tool with prompt and image.
