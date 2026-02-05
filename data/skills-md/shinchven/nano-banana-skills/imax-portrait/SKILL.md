---
name: imax-portrait
description: Expands and recomposes images into an IMAX 70mm portrait style (1.43:1 aspect ratio) with high-fidelity Christopher Nolan-esque aesthetics.
version: 1.0.0
---

# IMAX Portrait

## Capability
Expands an input image to a 1.43:1 aspect ratio, perfectly centering the subject with ample headroom and padding, and applies IMAX 70mm aesthetics (bokeh, grain, shallow depth of field).

## Triggers
- "Make this an IMAX portrait"
- "Expand to IMAX 70mm"
- "Recompose in 1.43:1"
- "Christopher Nolan style portrait"

## Instructions
1.  **Analyze Input**: Identify the main character content and lighting direction in the input image.
2.  **Apply Logic**: Use the following JSON logic to guide the image generation process:

```json
{
  "task": "imax-portrait",
  "parameters": {
    "aspect_ratio": "1.43:1",
    "allowed_aspect_ratios": [
      "1.43:1",
      "1.90:1"
    ],
    "output_format": "png",
    "guidance_scale": 7.5
  },
  "input": {
    "image_data": "<USER_UPLOADED_IMAGE_BASE64>",
    "expansion_direction": "all"
  },
  "prompt_construction": {
    "positive_prompt": "IMAX 70mm portrait photography. 1.43:1 aspect ratio. Christopher Nolan style. 80mm lens, f/1.4 aperture. Shallow depth of field. The subject is perfectly centered within the new, taller frame. Ample headroom is added above the subject, ensuring no part of the head is cut off. There is comfortable padding space around the entire character, creating a balanced composition. High fidelity texture.",
    "negative_prompt": "distorted, stretched, low resolution, cropped head, cramped framing, subject too close to edge"
  },
  "agent_instructions": {
    "step_1": "Identify the main character subject and the existing lighting direction within the input image.",
    "step_2": "Create a new, larger canvas at exactly the 1.43:1 aspect ratio.",
    "step_3": "Re-compose the shot by centering the identified subject within this new canvas, ensuring ample breathing room is added above the head and around the sides.",
    "step_4": "Fill the newly created surrounding areas with seamless bokeh and 70mm film grain consistent with the original image's environment."
  }
}
```

3.  **Generate**: Call the image generation/expansion tool.
    -   **Prompt**: Use the `positive_prompt` and `negative_prompt` from the JSON.
    -   **Process**: Ensure the subject is centered and the aspect ratio is 1.43:1.

## Tools / Commands
- Image generation/editing tool: Capable of outpainting/expansion and style transfer.

## Examples
User: "Turn this photo into an IMAX portrait."
Action:
1. Agent reads the input image.
2. Agent applies the `imax-portrait` logic.
3. Agent generates a new image with 1.43:1 aspect ratio, centered subject, and IMAX styling.
