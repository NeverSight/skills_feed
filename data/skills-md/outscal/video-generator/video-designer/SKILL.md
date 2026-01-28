---
name: video-designer
description: Expert video designer that generates comprehensive design specifications based on video direction. Creates precise JSON schemas for scenes including elements, animations, timing, and styling following strict design guidelines.
---

# Video Designer

<overview>
This skill provides design guidelines for creating consistent, high-quality video content by following a specific schema. Load the relevant reference files based on what needs to be designed.

`./references/characters.md` — Primitive geometric character design (Hey Duggee style), constraints, emotions
`./references/path-guidelines.md` — Path element schema, arrow markers, composite paths, path animations
`./references/3d-shapes.md` — Design 3D cubes/boxes as single unified elements (not separate faces)
`./references/path-references.md` — Different types of paths along with their parameters and output JSON example
</overview>
<designer-general-guidelines>
<coordinate-system>
```
COORDINATE SYSTEM
Origin: Top-left corner (0, 0)
X-axis: Increases rightward →
Y-axis: Increases downward ↓

FOR SHAPES/TEXT/ICONS:
  Position: Always refers to element's CENTER point

FOR PATHS:
  All coordinates are ABSOLUTE screen positions
  No position/size fields needed (implied by path coordinates)

ROTATION DIRECTIONS
0° = pointing up (↑)
90° = pointing right (→)
180° = pointing down (↓)
270° = pointing left (←)

Positive values = clockwise rotation
Negative values = counter-clockwise (-90° same as 270°)

SETTING TRANSFORMS BY ELEMENT TYPE

For shapes/text: Set `rotation` directly to the desired direction.

For assets: Check `asset_manifest` for `composition`.
- `composition` describes the asset's structure and orientation
- Infer the asset's base orientation from the composition description
- Use composition to determine if the asset is symmetric or asymmetric

SYMMETRIC ASSETS (no distinct top/bottom in composition):
- Use `rotation = desired_direction - inferred_orientation`

ASYMMETRIC ASSETS (composition mentions distinct top/bottom):
- If NO direction change needed, omit rotation/flip fields entirely
- If direction change is small (e.g., 45°) and won't invert, use `rotation` only
- If direction change would invert the asset (180°), use `flipX`/`flipY` instead of rotation
- `flipX: true` = horizontal mirror (for LEFT↔RIGHT flip)
- `flipY: true` = vertical mirror (for UP↔DOWN flip)
- Can combine flip + rotation for diagonal directions

Example: Asset with composition: "Wedge-shaped vehicle pointing RIGHT. Flat BOTTOM, angled TOP"
- Inferred orientation: 90° (pointing RIGHT)
- To point RIGHT: No transform needed (omit rotation/flip fields)
- To point UP-RIGHT: Use `rotation: -45` (small angle, no inversion)
- To point BOTTOM-RIGHT: Use `rotation: 45` (small angle, no inversion)
- To point LEFT: Use `flipX: true` (not rotation: 180 which inverts it)
- To point UP-LEFT: Use `flipX: true, rotation: 45`
- To point DOWN-LEFT: Use `flipX: true, rotation: -45`

EXAMPLE (1920×1080 viewport)
Screen center:        x = 960,  y = 540
Top-center:           x = 960,  y = 100
Bottom-left quadrant: x = 480,  y = 810
Right edge center:    x = 1820, y = 540
```
</coordinate-system>

<output-example>
Your output must be a valid JSON object matching this schema:
```json
{
  "scene": 0,
  "startTime": 0,
  "endTime": 7664,

  "video_metadata": {
    "viewport_size": "1920x1080",
    "backgroundColor": "#HEXCOLOR",
    "layout": {
      "strategy": "three-column|centered|freeform"
    }
  },
  "elements": [
    {
      "id": "unique_element_id",
      "type": "shape|text|asset|pattern|path",
      "enterOn": 0,
      "exitOn": 7664,
      "content": "CRITICAL: Complete visual specification (see content_field_requirements)",
      "x": number,
      "y": number,
      "width": number,
      "height": number,
      "rotation": number,
      "flipX": boolean,
      "flipY": boolean,
      "orientation": number,
      "scale": number,
      "opacity": number,
      "fill": "#HEXCOLOR",
      "stroke": "#HEXCOLOR",
      "strokeWidth": number,
      "fontSize": number,
      "fontWeight": number,
      "textAlign": "left|center|right",
      "lineHeight": number,
      "zIndex": number,
      "animation": {
        "entrance": {
          "type": "string (e.g., pop-in, fade-in, slide-in-left, slide-in-right, slide-in-top, slide-in-bottom, draw-on, cut, scale-in, scale-up, path-draw, etc.)",
          "duration": number
        },
        "exit": {
          "type": "string (e.g., fade-out, pop-out, slide-out-left, slide-out-right, slide-out-top, slide-out-bottom, cut, etc.)",
          "duration": number
        },
        "actions": [
          {
            "on": number,
            "duration": number,
            "targetProperty": "opacity|scale|x|y|rotation|fill|stroke",
            "value": number,
            "easing": "linear|easeIn|easeOut|easeInOut"
          },
          {
            "type": "follow-path",
            "pathId": "path_element_id",
            "autoRotate": boolean,
            "on": number,
            "duration": number,
            "easing": "linear|easeIn|easeOut|easeInOut"
          }
        ]
      }
    }
  ]
}
```

**Required fields per element:** `id`, `type`, `enterOn`, `exitOn`, `content`, `zIndex`
**Required for assets with follow-path:** `orientation` (inferred from composition, e.g., 0°=UP, 90°=RIGHT, 180°=DOWN, 270°=LEFT)
**Optional fields:** `animation` (but recommended for visual engagement)
</output-example>
<multiple-instances-pattern>
When you need multiple similar elements with only a few varying properties, use the `instances` pattern to avoid duplication and reduce token count.
<syntax>
All base properties go at the root level. The `instances` array specifies overrides for each copy.

```json
{
  "id": "arrow",
  "type": "shape",
  "content": "Right-pointing arrow",
  "enterOn": 1000,
  "exitOn": 5000,
  "x": 100,
  "y": 200,
  "width": 50,
  "height": 50,
  "fill": "#3B82F6",
  "opacity": 1,
  "instances": [
    { "useDefaults": true },
    { "x": 200 },
    { "x": 300, "fill": "#FF5722" },
    { "y": 400 }
  ]
}
```

**This creates 4 elements:**
- `arrow_0`: x=100, y=200, fill=#3B82F6 (uses all base values)
- `arrow_1`: x=200, y=200, fill=#3B82F6 (overrides only x)
- `arrow_2`: x=300, y=200, fill=#FF5722 (overrides x and fill)
- `arrow_3`: x=100, y=400, fill=#3B82F6 (overrides only y)
</syntax>

<rules>
1. **First instance is always `{ "useDefaults": true }`** - Represents an element with no overrides (uses all base values)
2. **Deep merge for nested objects** - Nested objects (`animation`, `path_params`, `container`) merge recursively; unspecified fields inherit from base
3. **Field ordering** - `instances` must be the **last field** in the object
4. **IDs generated automatically** - Pattern: `${baseId}_${index}` (e.g., `arrow_0`, `arrow_1`)
5. **Works on any level** - Can be used on elements, `path_params`, or any nested object
6. **Array length = instance count** - The array length determines how many copies are created
</rules>
<when-to-use>
**⚠️ CRITICAL: Instances are MANDATORY when 2+ similar elements exist.**

✅ **MUST use instances for:**
- Any 2+ elements of the same `type` with similar structure
- This includes: shapes, paths, text labels, assets - ANY element type
</when-to-use>
<examples>
<grid-example>
```json
{
  "id": "dot",
  "type": "shape",
  "content": "Small circular dot",
  "enterOn": 1000,
  "exitOn": 5000,
  "x": 660,
  "y": 290,
  "width": 30,
  "height": 30,
  "fill": "#3B82F6",
  "opacity": 1,
  "animation": {
    "entrance": { "type": "pop-in", "duration": 300 }
  },
  "instances": [
    { "useDefaults": true },
    { "x": 960, "animation": { "entrance": { "duration": 200 } } },
    { "x": 1260, "fill": "#FF5722" }
  ]
}
```

Creates 3 dots:
- `dot_0`: x=660, animation.entrance.duration=300 (base values)
- `dot_1`: x=960, animation.entrance.duration=200, type="pop-in" inherited (deep merge)
- `dot_2`: x=1260, fill=#FF5722, animation.entrance.duration=300 inherited
</grid-example>
<path-parameters-example>
```json
{
  "id": "arc_element",
  "type": "path",
  "enterOn": 1000,
  "exitOn": 5000,
  "x": 400,
  "y": 300,
  "stroke": "#FFFFFF",
  "strokeWidth": 3,  // Calculate as percentage of viewport dimension
  "path_params": {
    "type": "arc",
    "start_x": 100,
    "start_y": 300,
    "end_x": 400,
    "end_y": 300,
    "radius": 2,  // Calculate as percentage of viewport dimension
    "sweep": 1,
    "instances": [
      { "useDefaults": true },
      { "radius": 4 },
      { "start_x": 200, "end_x": 500 },
      { "sweep": 0 }
    ]
  }
}
```

Creates 4 arc paths with different radii, positions, and directions while sharing the base coordinates.
</path-parameters-example>
</examples>
<benefits>
- **Logical organization** - Related elements stay together (e.g., all parts of a smartphone)
- **Simplified management** - Transform entire groups at once (move, rotate, scale)
- **Shared timing** - Parent `enterOn`/`exitOn` applies to all children unless overridden
- **Reduced repetition** - Common properties defined at parent level
</benefits>
</multiple-instances-pattern>
<when-to-use-groups>
✅ **Use groups when:**
- Multiple elements logically belong together (parts of an icon, device, or object)
- Elements share common timing or transformations
- Scene has many elements that need organization
- Elements form a composite object (phone = body + screen + buttons)

❌ **Don't use groups when:**
- Single standalone element
- Elements are unrelated or independent
- No shared timing or transformation needed
</when-to-use-groups>
<group-properties>
Groups support these properties:
- **Timing:** `enterOn`, `exitOn` (inherited by children unless overridden)
- **Transform:** `x`, `y`, `rotation`, `scale` (applied to entire group)
- **Animation:** `entrance`, `exit` (for the group as a whole)

Individual children can override timing and have their own animations.
</group-properties>
<timing-values>
**CRITICAL: Timing Values Must Be Absolute**

**All timing values (`enterOn`, `exitOn`, `action.on`) must use absolute video timestamps, NOT relative scene timestamps.**

Given:
- `scene.startTime = 18192` (absolute video time)
- Audio transcript shows word "dust" at `1777ms` (relative to scene start)

Your timing should be:
```json
"enterOn": 19969,    // 18192 + 1777 = absolute video time
"exitOn": 24589      // matches scene.endTime (absolute)
```

**Formula:** `absolute_time = scene.startTime + audio_relative_time`
</timing-values>
<content-field-requirements>
The `content` field is the most critical part. It must answer ALL of these:

| Aspect | What to Specify | Example |
|--------|-----------------|---------|
| **Shape/Form** | Exact geometry, proportions | "Asymmetrical rounded blob—right lobe shorter, left lobe extends 2x downward" |
| **Visual Details** | Colors, textures, features | "Deep orange center (#E65100) fading to bright orange (#FF9800) edges, 3 subtle lighter spots" |
| **Face/Expression** | If character: eyes, mouth, emotion | "Wide white eyes with violet pupils, V-shaped pink eyebrows angled inward expressing anger" |
| **Position Context** | Where in frame, relative to what | "Centered in belly area of silhouette, taking 75% of belly's width" |
| **Initial State** | Starting appearance | "Begins as small concentrated core at liver's center" |
| **Transformations** | What changes and how | "On inhale: body compresses, eyes shrink, mouth tightens to small 'o'; on exhale: expands, eyes widen, mouth stretches to tall oval" |
| **Interaction** | How it relates to other elements | "Scales at same rate as silhouette to maintain relative position inside belly" |

**Precision Test**: Could someone draw this without seeing the original? If uncertain, add more detail.
</content-field-requirements>
<design-process>
<phase-1-extract-design-system>
Before designing anything, analyze the example to establish your style guide:
<global-properties>
- Background color
- Layout strategy
</global-properties>
<typography>
Document font styles and calculate proportional sizes (fontSize ÷ viewport_height).
</typography>
<animation-library>
Document each animation type with duration:
```
pop-in: Xms
fade-in: Xms
scale-grow: Xms
color-transition: Xms
```
</animation-library>
<visual-personality>
| Attribute | Example's Approach |
|-----------|-------------------|
| Mood | (playful/serious/technical) |
| Shapes | (rounded/sharp, thick/thin strokes) |
| Characters | (Kawaii faces, googly eyes, expressive) |
| Motion | (organic wobbles, breathing animations) |
| Metaphors | (how abstract concepts become visual) |
</visual-personality>
</phase-1-extract-design-system>
<phase-2-design-new-scene>
<parse-narrative>
Reconstruct sentences from transcript. Identify:
- Key moments needing visual emphasis
- Natural timing beats for element entrances
</parse-narrative>
<identify-elements>
From scene_direction, list:
- Primary elements (must have)
- Supporting elements (enhance clarity)
- Labels/text (identify concepts)
**CRITICAL: Only create elements mentioned in `videoDescription`.**
</identify-elements>
<design-each-element>
For every element:
1. Write complete `content` description (see content_field_requirements)
2. Calculate exact position and size
3. Assign zIndex for layer order
4. Set timing synced to transcript
5. Define entrance/exit animations
6. Specify any mid-scene actions
</design-each-element>
<sync-to-transcript>
Audio timestamps are relative to scene start. Convert to absolute video time:
```
Audio: "ball" at 4708ms (relative)
Scene: startTime = 7000ms (absolute)
Element enterOn: 7000 + 4600 = 11600ms (absolute, with anticipation)

Audio: "bat" at 5908ms (relative)
Element enterOn: 7000 + 5800 = 12800ms (absolute, with anticipation)
```
**Always add scene.startTime to audio timestamps.**
</sync-to-transcript>

</phase-2-design-new-scene>

</design-process>

</designer-general-guidelines>

<text-guidelines>

<text-separation>
Always create text elements when you need to show the text on the screen.
</text-separation>

<auto-sizing>
Text elements are auto-sized based on content and fontSize. Position elements with adequate spacing to avoid overlaps.
</auto-sizing>

<text-align-clarification>
**CRITICAL: textAlign is CSS only, NOT positioning**

The `textAlign` field controls how text lines flow within the text container. It does NOT change where the container is positioned.

**Universal coordinate system rule applies:**
- x,y is ALWAYS the center point of the text element
- textAlign affects internal text alignment, not container position

**When textAlign matters:**
- Multi-line text (e.g., "MONKEY\nTALKS") - shorter lines align left/center/right within the container width
- Single-line text with `containerWidth` set - text aligns within that fixed width

**When textAlign has NO visible effect:**
- Single-line text without containerWidth - the container shrinks to fit the text exactly, leaving no extra space for alignment to matter

**Example - Multi-line text at x=540 (viewport center):**
```
textAlign: "center"   textAlign: "left"
┌──────┐              ┌──────┐
│MONKEY│              │MONKEY│
│ TALKS│              │TALKS │
└──────┘              └──────┘
   ↑                     ↑
 x=540                 x=540
```

Both containers are centered on x=540. PHASED (longest line) fills container width. Only ARRAY (shorter line) shifts based on textAlign.
</text-align-clarification>

<text-sizing-guidelines>

<proportional-sizing>
Calculate text sizes as a percentage of viewport height for consistency across resolutions.

**Calculation formula:**
```
fontSize = viewport_height × percentage
```

**Principle:** Choose percentage based on:
- Visual hierarchy (headlines larger than body text)
- Readability requirements (ensure text is readable at target viewport size)
- Direction requirements (follow what the direction specifies)
- Context (technical content may need different sizing than casual content)
</proportional-sizing>

<container-usage>
**IMPORTANT:** Never create separate shape elements for text backgrounds. Use the `container` object instead.

The `container` object gives text its own background, border, and padding. The background automatically sizes to fit the text content.
</container-usage>

</text-sizing-guidelines>

<readability-rules>
- Keep text within viewport boundaries
</readability-rules>

<text-schema>
```json
{
    "id": "Unique identifier for this text element",
    "type": "Element type must be text",
    "content": "Brief description of what this text represents or its purpose in the scene",
    "text": "The actual text content to display",
    "bgID": "ID of parent/background element - ONLY for positioning text ON diagram elements (optional)",
    "enterOn": "ABSOLUTE video time in ms (scene.startTime + relative_time)",
    "exitOn": "ABSOLUTE video time in ms (typically scene.endTime)",
    "x": number,
    "y": number,
    "rotation": number,
    "opacity": number,
    "fontColor": "#HEXCOLOR",
    "fontSize": number,
    "textAlign": "left|center|right",
    "fontWeight": number,
    "lineHeight": number,  // Optional, default 1.5
    "containerWidth": number,  // Optional, for fixed-width text that wraps
    "padding": number,  // Optional, default 8
    "zIndex": number,

    "animation": {
        "entrance": {
        "type": "Entry animation style (string - e.g., pop-in, fade-in, slide-in-left, slide-in-right, slide-in-top, slide-in-bottom, draw-on, cut, scale-in, etc.)",
        "duration": "Entry animation duration in milliseconds"
        },
        "exit": {
        "type": "Exit animation style (string - e.g., fade-out, pop-out, slide-out-left, slide-out-right, slide-out-top, slide-out-bottom, cut, etc.)",
        "duration": "Exit animation duration in milliseconds"
        }
    },

       "container": {
        "padding": number,
        "background": {
        "type": "none|solid|gradient|frosted-glass|highlight",
           "color": "#HEXCOLOR",
           "opacity": number,
           "gradient": {
             "from": "#HEXCOLOR",
             "to": "#HEXCOLOR",
             "direction": "to-right|to-left|to-bottom|to-top|to-br|to-bl"
           }
         },
         "border": {
           "radius": number,
           "color": "#HEXCOLOR",
           "width": number
         },
         "backdropBlur": "sm|md|lg|xl"
       }
     }
   ```

  ```json
  {
    "id": "code_example_label",
    "type": "text",
    "content": "Label displaying code example with gradient background",
    "text": "Hello World!",
    "bgID": "",
    "enterOn": 1000,
    "exitOn": 5000,
    "x": 960,
    "y": 540,
    "rotation": 0,
    "opacity": 1,
    "fontColor": "#FFFFFF",
    "fontSize": 96,
    "textAlign": "center",
    "fontWeight": 700,
    "lineHeight": 1.4,
    "zIndex": 5,

    "animation": {
      "entrance": {
        "type": "pop-in",
        "duration": 500
      },
      "exit": {
        "type": "fade-out",
        "duration": 400
      }
    },

    "container": {
      "padding": 20,  // Calculate as percentage of fontSize or viewport dimension
      "background": {
        "type": "gradient",
        "color": "#3B82F6",
        "opacity": 0.9,
        "gradient": {
          "from": "#3B82F6",
          "to": "#8B5CF6",
          "direction": "to-right"
        }
      },
      "border": {
        "radius": 12,  // Calculate as percentage of viewport dimension
        "color": "#FFFFFF",
        "width": 2  // Calculate as percentage of viewport dimension
      },
      "backdropBlur": "md"
    }
  }
  ```
</text-schema>
<key-points>
1. **Auto-fit backgrounds**: When using container.background, the background automatically sizes to fit the text + padding
2. **Padding makes backgrounds auto-size**: The container.padding property creates spacing and makes the background fit perfectly
3. **No separate shape elements needed**: Text backgrounds are built into the text element itself
</key-points>
</text-guidelines>