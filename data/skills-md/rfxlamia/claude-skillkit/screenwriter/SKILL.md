---
name: screenwriter
description: >
  Transform creative ideas into professional, production-ready screenplays optimized for AI video generation pipelines. Converts raw concepts into structured scene-by-scene narratives with rich visual descriptions, proper screenplay formatting, and XML-tagged output for seamless integration with image/video generation tools (imagine, arch-v).
  
  USE WHEN: Converting story ideas into screenplay format, preparing content for AI video pipelines, structuring narratives for 5-10 minute short films, generating visual-rich scene descriptions for image generation.
  
  WORKFLOW: Raw idea → Scene breakdown → Visual enhancement → Professional formatting → XML-tagged markdown output
  
  OUTPUT: Markdown document with XML-wrapped scenes, rich visual descriptions, proper screenplay elements (sluglines, action, dialogue), and metadata for pipeline processing.
---

# Screenwriter Skill

## Overview

This skill transforms creative concepts into professional screenplay documents optimized for AI-powered video production pipelines. It bridges the gap between raw story ideas and production-ready scripts by generating structured, visual-rich narratives in industry-standard screenplay format.

**Pipeline Position:** `diverse-content-gen` → **screenwriter** → `imagine` → `arch-v`

**Key Capabilities:**
- Convert raw ideas into structured scene-by-scene narratives
- Generate rich visual descriptions optimized for image generation
- Apply professional screenplay formatting (sluglines, action lines, dialogue)
- Output XML-tagged markdown for easy parsing
- Optimize pacing for 5-10 minute short films (8-15 scenes typical)

---

## Core Workflow

### 1. Analyze Input Concept
- Extract key story beats from raw ideas
- Identify characters, locations, emotional arc
- Determine story structure (beginning, middle, end)

### 2. Generate Scene Breakdown
- Convert story beats into discrete scenes
- Establish scene count (aim for 8-15 scenes for 5-10 min films)
- Define scene purpose and emotional progression

### 3. Write Professional Screenplay
- Apply industry-standard formatting
- Write visual-rich action lines
- Include dialogue when narratively essential
- Maintain consistent character descriptions

### 4. Output XML-Tagged Markdown
- Wrap each scene in XML tags with metadata
- Include scene numbers, locations, key visuals
- Format for easy pipeline parsing

---

## Screenplay Format Standards

### Scene Structure (Master Scene Heading)

**Slugline Format:**
```
INT/EXT. LOCATION - TIME
```

**Components:**
- **INT/EXT:** Interior or Exterior
- **LOCATION:** Specific place (be descriptive but concise)
- **TIME:** DAY, NIGHT, DAWN, DUSK, CONTINUOUS

**Examples:**
```
EXT. WASTELAND - DAWN
INT. ABANDONED SUBWAY STATION - NIGHT
EXT. ROOFTOP GARDEN - GOLDEN HOUR
```

**Guidelines:**
- Always use ALL CAPS for sluglines
- Use hyphens to separate elements
- Be specific with locations (aids visual generation)
- Time should suggest lighting/mood

### Action Lines (Visual Description)

**Purpose:** Describe what the audience sees on screen. This is CRITICAL for image generation.

**Visual-Rich Writing Principles:**
1. **Show, Don't Tell:** Write what's visible, not internal thoughts
2. **Sensory Details:** Include lighting, atmosphere, textures, colors
3. **Present Tense:** Always write in present tense
4. **Active Voice:** Use strong, active verbs
5. **Specific Props:** Name objects that matter visually
6. **Atmosphere:** Set mood through environmental details

**Example - Weak:**
```
A robot walks through the city. It's sad.
```

**Example - Strong:**
```
A BOXY ROBOT (Unit-7, weathered chrome with a single blue optical sensor) rolls through fog-shrouded streets. Neon signs flicker overhead, casting pink and cyan reflections on wet pavement. The robot's movements are slow, deliberate—almost hesitant.
```

**Visual Enhancement Checklist:**
- [ ] Lighting described (natural/artificial, quality, color)
- [ ] Atmosphere/mood established (fog, rain, dust, clarity)
- [ ] Character appearance detailed (first appearance only)
- [ ] Props/objects specified (important visual elements)
- [ ] Composition suggested (without technical camera direction)
- [ ] Colors/textures mentioned when relevant

### Character Introduction

**First Appearance - Detailed:**
```
SARAH (28, sharp eyes, wearing a weathered leather jacket over faded jeans) enters the frame. Her dark hair is pulled back, revealing a small scar above her left eyebrow.
```

**Subsequent Appearances - Brief:**
```
Sarah checks her watch.
```

**Guidelines:**
- Character names in ALL CAPS on first appearance only
- Include: age (if relevant), key physical traits, wardrobe
- Focus on visual identifiers for consistent image generation
- Avoid excessive detail—just enough for visual consistency

### Dialogue (Use Sparingly)

**Format:**
```
CHARACTER NAME
(parenthetical - optional)
Dialogue goes here.
```

**Guidelines for Short Films:**
- Use dialogue ONLY when essential to story
- Favor visual storytelling over talking
- Keep lines concise (max 3-4 lines per block)
- Parentheticals only for critical tone/action
- Character names centered, ALL CAPS

**Example:**
```
UNIT-7 (robotic voice, soft)
Organic life form detected.
Probability of survival: low.
```

### Transitions (Minimal Use)

**Common Transitions:**
- `FADE IN:` - Opening of screenplay only
- `CUT TO:` - Scene change (usually implied, use for emphasis)
- `SMASH CUT TO:` - Abrupt, jarring transition
- `DISSOLVE TO:` - Passage of time
- `FADE OUT.` - End of screenplay

**Modern Best Practice:** Most transitions are IMPLIED. Use sparingly, only for specific narrative effect.

---

## XML Output Format

### Scene Tag Structure

Each scene wrapped in XML with metadata for pipeline processing:

```xml
<scene number="1" duration="30-45s">
  <slugline>EXT. WASTELAND - DAWN</slugline>
  <location>Wasteland</location>
  <time>Dawn</time>
  <characters>Unit-7</characters>
  <mood>desolate, lonely</mood>
  <key_visuals>
    <visual>post-apocalyptic wasteland with ruined skyscrapers</visual>
    <visual>boxy robot with single blue optical sensor</visual>
    <visual>dust and smog atmosphere, weak pale sun</visual>
  </key_visuals>
  <action>
Gray dust covers everything. Skeletal remains of skyscrapers pierce the horizon. The sun, pale and weak, struggles through thick smog.

A ROBOT (Unit-7, boxy frame with single blue optical sensor) rolls across cracked asphalt. Its treads leave marks in the dust—the only sign of life.

The robot stops at a pile of rubble, extending a mechanical arm to sort through debris. Methodical. Purposeful. Lonely.
  </action>
</scene>
```

### Metadata Fields

- `number`: Scene sequence number (1, 2, 3...)
- `duration`: Estimated screen time (for 5-10 min total)
- `slugline`: Master scene heading
- `location`: Extracted location name
- `time`: Time of day
- `characters`: Comma-separated character list
- `mood`: Emotional tone/atmosphere
- `key_visuals`: Array of specific visual elements for image generation
- `action`: The full action/description text
- `dialogue` (optional): Character dialogue if present

---

## Short Film Structure (5-10 Minutes)

### Scene Count Guidelines
- **5 minutes:** 6-10 scenes
- **7 minutes:** 10-12 scenes
- **10 minutes:** 12-15 scenes

**Average:** ~30-60 seconds per scene

### Three-Act Structure (Compressed)

**Act 1 - Setup (20-25%):** 2-3 scenes
- Establish world, character, situation
- Inciting incident

**Act 2 - Confrontation (50-60%):** 4-8 scenes
- Development, obstacles, rising tension
- Midpoint twist or escalation

**Act 3 - Resolution (20-25%):** 2-3 scenes
- Climax and resolution
- Emotional payoff

### Pacing Tips
- **Open strong:** Hook audience in first 10-15 seconds
- **Visual variety:** Alternate between wide/close, action/stillness
- **Emotional beats:** Each scene should shift emotional state
- **Build tension:** Escalate stakes scene-by-scene
- **Satisfying end:** Clear resolution, even if bittersweet

---

## Best Practices

### For Pipeline Integration
- **Consistent naming:** Use same character names throughout
- **Rich visuals:** Every scene needs 3-5 key_visuals for image generation
- **Parseable format:** Maintain strict XML structure
- **Duration estimates:** Help pipeline plan total video length

### For Quality Output
- **Visual storytelling:** Show emotions through actions, not dialogue
- **Specific details:** "weathered chrome" beats "old metal"
- **Atmospheric writing:** Set mood through environment
- **Lean prose:** Each word should serve the image

### Common Pitfalls to Avoid
- ❌ **Vague descriptions:** "A person walks" → ✅ "A weathered woman in her 50s trudges through snow"
- ❌ **Telling emotions:** "She feels sad" → ✅ "Tears streak her dusty cheeks"
- ❌ **Camera directions:** "CLOSE UP ON" → ✅ "The crack in the glass spreads"
- ❌ **Over-dialogue:** Short films need visual storytelling
- ❌ **Inconsistent character names:** Stick to ONE name per character

---

## Additional Resources

### Pipeline Integration Guide
For detailed guidance on metadata standards, visual optimization, and integration with imagine/arch-v:
- [references/pipeline-integration.md](references/pipeline-integration.md)

### Advanced Techniques
For sophisticated screenwriting techniques, camera movement hints, and pacing optimization:
- [references/advanced-techniques.md](references/advanced-techniques.md)
