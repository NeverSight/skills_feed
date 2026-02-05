---
name: character-reference-sheet
description: Generates a 1:1 split-screen (front/back) character reference sheet, mirroring facial, physical, and costume details from an uploaded image.
version: 1.0.0
---

# Character Reference Sheet

## Capability
Analyzes an attached character image to perform deep feature extraction (facial physiognomy, physical attributes, costume details) and generates a split-screen image containing two full-body views (Front and Back) on a simple color background, maintaining the exact visual style of the source.

## Triggers
- "Create a character reference sheet."
- "Generate a front and back view of this character."
- "Make a split-screen character sheet."
- "Analyze this character and create a reference image."

## Instructions
1.  **Research Character (Visual & Web Search)**:
    - **Visual Analysis**: detailed feature extraction (physiognomy, attributes, costume).
    - **Web Search**: If the character appears to be from a franchise or has a name, use `search_web` to find setting/lore details to inform dynamic poses.

2.  **Construct the Image Generation Prompt**:
    - **Layout & Views**:
        - **Default (Split Screen)**: "Split-screen, Left: Front view, Right: Back view."
        - **2x2 Layout**: "Four-panel grid. Top-Left: Front view. Top-Right: Back view. Bottom-Left & Bottom-Right: Dynamic action poses [based on character setting]."
        - **3x3 Layout**: "Nine-panel grid. Center: Front view. Top-Center: Back view. Remaining panels: Varied dynamic poses and close-ups [based on character setting]."
        - **Mandatory**: Front and Back views are *always* required.
    - **Background**: "...on a simple color background."
    - **Details**: "Exact mirror of facial features, physical attributes, and costume details from the source."
    - **Visual Constraints**: "Style Fidelity: Retain the exact visual style, rendering technique, and lighting quality of the source image."

3.  **Generate the Image**:
    - Use the image generation tool with the constructed prompt and the user's reference image.

## Tools / Commands
- `search_web`: To research character background/setting.
- Image generation tool: To generate the reference sheet.

## Examples
User: "Create a reference sheet for this character." (User attaches `[image]`)
Action:
1.  **Research**: Analyze `[image]`. (Optional) Web search if character is recognized.
2.  **Prompt**: "A split-screen character reference sheet... Left: Front, Right: Back..."
3.  **Generate**: Call tool.

User: "Make a 3x3 reference sheet for 'Cloud Strife'." (User attaches `[image]`)
Action:
1.  **Research**: Recognize "Cloud Strife". Search web -> "FF7, Buster Sword, Soldier pose".
2.  **Prompt**: "Nine-panel grid character sheet for Cloud Strife. Center: Front static. Top-Center: Back static. Surrounding panels: Dynamic sword swings, limit break poses. High fidelity to source."
3.  **Generate**: Call tool.
