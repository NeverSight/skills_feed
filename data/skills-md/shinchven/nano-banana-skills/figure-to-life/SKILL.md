---
name: figure-to-life
description: Converts figure photos to photorealistic human cosplayer images using a strict JSON-based reasoning mandate.
version: 1.0.0
---

# Figure to Life

## Capability
Converts figure (toy/statue) photos into photorealistic "human cosplayer" images. It strictly enforces character lore, ethnicity preferences (Russian/Western or Japanese/Korean/Asian), and realistic biological details, while replacing plastic textures with high-fidelity materials and placing the subject in a cinematic environment.

## Triggers
- "figure to life"
- "make this figure real"
- "statue to person"
- "convert figure to cosplayer"

## Instructions
1.  **Analyze the Input**: Identify the character, their origin, and the visual attributes of the figure.
2.  **Execute Conversion Logic**: Apply the following JSON-based reasoning to construct the generation prompt.

    ```json
    {
      "task": "figure_to_photorealism_conversion",
      "reasoning_mandate": {
        "step_1": "Analyze input image to positively identify the fictional character.",
        "step_2": "Determine character origin. Apply Ethnicity Preference: Use 'Russian' features for Western-coded characters; use 'Japanese' or 'Korean' features for Asian-coded characters.",
        "step_3": "Retrieve canonical traits (Eye/Hair/Skin) and generate human cosplayer, strictly overriding toy plastic/paint inaccuracies.",
        "step_4": "Synthesize a background environment consistent with the character's narrative origin."
      },
      "subject": {
        "entity": "human_cosplayer",
        "visual_attributes": {
          "appearance": "pretty",
          "makeup": "delicate_and_professional",
          "skin_texture": "hyper_realistic_pores_and_imperfections",
          "biological_accuracy": {
            "ethnicity_preference": {
              "western_archetype": "Russian_Slavic_features",
              "asian_archetype": "Japanese_or_Korean_features",
              "logic": "Apply_preference_based_on_character_origin"
            },
            "gender": "STRICT_MATCH_CHARACTER_LORE",
            "body_type": "STRICT_MATCH_CHARACTER_LORE_PROPORTIONS",
            "eye_color": "STRICT_MATCH_CHARACTER_LORE",
            "hair_color": "STRICT_MATCH_CHARACTER_LORE",
            "skin_tone": "STRICT_MATCH_CHARACTER_LORE"
          },
          "pose": "exact_match_input_figure_pose"
        },
        "costume": {
          "fidelity": "high_quality_fabric_replica",
          "material_translation": "plastic_to_latex_or_fabric_or_leather",
          "match_reference": true
        }
      },
      "environment": {
        "instruction": "replace_toy_stand_with_lore_setting",
        "setting": "cinematic_world_appropriate_for_character",
        "lighting": {
          "style": "cinematic_portrait",
          "quality": "soft_volumetric_lighting"
        }
      },
      "camera_optics": {
        "type": "DSLR_photography",
        "lens": "85mm_portrait",
        "depth_of_field": "shallow_bokeh_background"
      },
      "references": {
        "input_source": "user_uploaded_figure_photo",
        "influence_strength": "pose_and_structure_only",
        "ignore_attributes": ["plastic_texture", "toy_joints", "paint_inaccuracies"]
      }
    }
    ```

3.  **Generate Image**: Use the image generation tool with the constructed prompt and the uploaded image as a reference (controlling pose/structure only).

## Tools / Commands
- Image generation tool: To generate the result.

## Examples
User: "Make this Miku figure real." (User attaches `[image]`)
Action:
1. Identify Hatsune Miku (Asian-coded).
2. Apply logic: Use Japanese/Korean features.
3. Construct prompt reflecting "Hyper-realistic Japanese cosplayer, Miku costume, high-quality fabric, stage lighting, soft bokeh".
4. Generate image.
