---
name: generate-image
description: Generate an image for a worldbuilding entity using OpenAI's gpt-image-1.5 model. Reads the filled prompt from the entity file, generates the image, downloads it locally, and updates the entity to reference it.
argument-hint: "[entity path or name]"
---

# Generate Image

Generate an image for: $ARGUMENTS

## Instructions

You are generating an AI image for an existing worldbuilding entity.

### Step 1: Locate the Entity

Find the entity file based on the user's input:

1. **If given a full path:** Use that path directly
2. **If given just a name:** Search in `Worlds/` for matching entity files
3. **If ambiguous:** Ask the user to clarify which entity they mean

Read the entity file to extract the image prompt.

### Step 2: Extract the Image Prompt

Look in the `## Image Prompts` section of the entity file.

Entity templates have different prompt subsections. Common patterns:
- **Characters:** `### Portrait (Bust)` and `### Full Body`
- **Settlements:** `### Exterior View` and `### Interior View`
- **Items:** `### Display View` and `### In Use`
- **Creatures:** `### Natural Habitat` and `### Combat Pose`
- **Geography:** `### Landscape View` and `### Aerial View`

Find the **Prompt:** field under one of these subsections. This is the filled prompt to use.

**Prompt Selection Priority:**
1. If user specifies which prompt (e.g., "portrait", "full body", "exterior"), use that one
2. If the entity has a Portrait/Bust prompt filled, prefer that
3. Otherwise use the first filled prompt found

If no prompts are filled (only templates exist), inform the user that the entity needs its image prompts filled first.

### Step 3: Prepare for Generation

**Determine the filename:**
- Use the entity name as the base filename
- Add `.png` extension
- Save in the same directory as the entity file

Example: `Worlds/Eldoria/Characters/Aldric the Bold.md` -> `Worlds/Eldoria/Characters/Aldric the Bold.png`

**Image Parameters for gpt-image-1.5:**
- **Size:** `1024x1024` (square, best for portraits and general use)
  - Or `1024x1536` (portrait orientation) for full-body characters
  - Or `1536x1024` (landscape) for geography/settlements
- **Quality:** `high` (best detail for fantasy art)
- **Format:** `png` (best quality, supports transparency)


### Step 5: Update the Entity File

After successfully generating and saving the image:

1. **Add `image:` field to frontmatter** (if not present):
   ```yaml
   image: "[[Entity Name.png]]"
   ```

2. **Insert image embed after frontmatter:**
   Add `![[Entity Name.png]]` on a new line immediately after the closing `---` of the frontmatter, before the `# Title`.

**Example result:**
```markdown
---
tags: [character, protagonist]
name: "Aldric the Bold"
image: "[[Aldric the Bold.png]]"
status: complete
---
![[Aldric the Bold.png]]

# Aldric the Bold
...
```

### Step 6: Confirm Success

Report to the user:
1. Path where the image was saved
2. Which prompt was used (e.g., "Portrait" or "Full Body")
3. Confirmation that the entity file was updated
4. Suggest opening the file in Obsidian to see the embedded image

### Optional: Generate Prompt from Entity

If the image prompt section is empty but the user wants an image, offer to generate a prompt based on the entity's content:

1. Read the entity's description, appearance, and other sections
2. Craft an appropriate prompt following the template format
3. Fill in the prompt section
4. Then proceed with image generation

### Image Type Selection

Ask the user which image type they want if the entity has multiple prompt options:

**For Characters:**
- Portrait (bust, chest-up) - good for character sheets, NPC cards
- Full Body - good for reference sheets, action poses

**For Settlements:**
- Exterior View - the building/settlement from outside
- Interior View - inside a key room or area

**For Geography:**
- Landscape View - ground-level scenic view
- Aerial View - bird's eye or map-like perspective

**For Items:**
- Display View - clean showcase of the item
- In Use - the item being wielded/used


**Size Options:**
| Orientation | Size | Use For |
|-------------|------|---------|
| Square | 1:1 | Portraits, items, icons |
| Portrait | 2:3 | Full-body characters |
| Landscape | 3:2 | Geography, settlements, battles |
