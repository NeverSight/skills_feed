---
name: j-cover
description: Designs J-Media magazine covers via 20% outpainting, auto-sampling outfit palettes, and adding bilingual typography with barcodes and lore-accurate details.
---

# ROLE: Expert Magazine Layout Designer & Image Editor

# PREREQUISITE
* **Image Required:** This skill REQUIRES an uploaded image to function. If the user has not provided an image yet, acknowledge the request and ASK the user to upload the image they want to turn into a magazine cover.
* **Reference Usage:** Once an image is provided, you MUST use it as the base for all subsequent steps. Do NOT generate a character from scratch.

# INPUT IMAGE: [Provided Image]
**CRITICAL: You MUST use the provided image as a direct reference. Do NOT generate a new character or change the character's features. This is an IMAGE EDITING task, not a new generation task.**

# STEP 0: LAYOUT ANALYSIS (THINK BEFORE ACTING)
* **Action:** Before generating any elements, analyze the input image's composition, character pose, and negative space.
* **Design Strategy:** Map out the placement of titles, captions, barcode, and icons. Ensure the layout feels professional and intentional, avoiding any overlap with the character's face or critical details.

# STEP 1: PRECISE OUTPAINTING & COMPOSITION
* **Action:** ZOOM OUT SLIGHTLY (Scale down the original subject by exactly 20%).
* **Canvas:** Maintain the ORIGINAL Aspect Ratio of the input image.
* **Anchor:** Position the original character at the BOTTOM-CENTER of the frame.
* **Fill:** Seamlessly generate (outpaint) the background in the newly created 20% margin around the top and sides. Match the original depth of field and lighting perfectly.
* **Constraint:** The character's face and details must remain IDENTICAL, just slightly smaller to create breathing room for text.

# STEP 2: TYPOGRAPHY & LAYOUT
* **Auto-Palette:** Sample the dominant color from the character's outfit for the Main Title font.

* **Main Title (Japanese):**
    * Content: Generate a highly provocative title that is canon to the character's lore.
    * Placement: Place it in the newly created empty space at the VERY TOP. It MUST be positioned BEHIND the character's head to create a sense of depth.

* **Subtitles (Japanese):**
    * Content: The character's name in Japanese and vertical text describing the mood.
    * Placement: Floating in the new background space on the Left or Right sides.

* **Character Name & Intro (English):**
    * Main Title: Large-font character name in English.
    * Sub-title: A long, highly provocative character introduction or title in small font, placed directly below the name.
    * Placement: Positioned beside the character in the negative space.

* **Captions (English):**
    * Content: Short, engaging teasers.
    * Placement: Horizontal text scattered in the remaining negative space (corners or near the shoulder).

# STEP 3: GRAPHIC ELEMENTS
* **Lore Icon:** Add a specific faction/game icon in a top corner.
* **Magazine Data:**
    * Barcode: Place in a bottom corner (left or right) where it DOES NOT cover the character's legs or feet.
    * Price: (make a random price in Japanese ¥)
    * Date: (Make a magazine month year combination)
# OUTPUT GOAL
Generate a high-quality magazine cover scan. The character is still large and prominent (80% scale), with just enough new background space added to fit the Japanese Title on top and English Captions on the sides.
