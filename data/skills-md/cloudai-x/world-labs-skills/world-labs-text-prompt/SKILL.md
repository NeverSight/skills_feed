---
name: world-labs-text-prompt
description: Text-to-world generation best practices, prompt structure, style descriptors
allowed-tools:
  - Bash
  - WebFetch
---

# World Labs Text Prompting

Text prompts are the simplest way to generate 3D worlds. Describe a location in natural language, and the model creates an immersive environment.

## Quick Reference

- **Max length**: 2,000 characters
- **Cost**: 1,580 credits (plus) / 230 credits (mini)
- **Generation time**: ~5 min (plus) / ~30-45 sec (mini)

## Official Example

From World Labs documentation:

```
A warm, rustic cabin living room with a glowing stone fireplace, cozy leather sofa, wooden beams, and large windows overlooking a snowy forest.
```

## Prompt Structure

Effective prompts describe a **location** with:

```
[Setting/Location] + [Materials/Textures] + [Lighting/Atmosphere] + [Environmental Context]
```

### Components

1. **Setting**: The primary location type (cabin, temple, alley, forest)
2. **Materials**: Specific textures (rustic wood, polished marble, weathered stone)
3. **Lighting**: Light sources and quality (glowing, warm, flickering, dusk)
4. **Context**: Surrounding environment (overlooking forest, narrow corridor)

## Style Descriptors

### Lighting Keywords

| Keyword         | Effect                       |
| --------------- | ---------------------------- |
| `glowing`       | Soft emissive light sources  |
| `warm`          | Cozy, orange-tinted lighting |
| `flickering`    | Dynamic light suggestion     |
| `dusk` / `dawn` | Transitional daylight        |
| `neon-lit`      | Vibrant artificial lighting  |
| `candlelit`     | Intimate, warm glow          |
| `moonlit`       | Cool, ethereal nighttime     |

### Atmosphere Keywords

| Keyword           | Effect                    |
| ----------------- | ------------------------- |
| `cozy`            | Intimate, inviting feel   |
| `atmospheric`     | Mood-heavy, immersive     |
| `misty` / `foggy` | Depth, mystery            |
| `dusty`           | Age, particles            |
| `puddles`         | Wet surfaces, reflections |
| `snowy`           | Winter atmosphere         |

### Material Keywords

| Keyword     | Effect                     |
| ----------- | -------------------------- |
| `rustic`    | Natural, aged wood         |
| `polished`  | Reflective, clean surfaces |
| `weathered` | Worn, aged textures        |
| `mossy`     | Organic growth             |
| `metallic`  | Industrial surfaces        |
| `leather`   | Furniture textures         |

### Style Keywords

| Keyword     | Effect                  |
| ----------- | ----------------------- |
| `sci-fi`    | Futuristic elements     |
| `fantasy`   | Magical, otherworldly   |
| `modern`    | Contemporary design     |
| `vintage`   | Period aesthetics       |
| `immersive` | Full environmental feel |

## Best Practices

### DO

✅ **Focus on location**: "A cabin living room" not "a picture of a cabin"
✅ **Be specific about materials**: "glowing stone fireplace" not just "fireplace"
✅ **Include spatial context**: "large windows overlooking a snowy forest"
✅ **Add atmosphere**: "warm, cozy, flickering light"
✅ **Use concrete details**: "wooden beams, leather sofa"

### DON'T

❌ **Describe people or animals** as main subjects
❌ **Use vague adjectives**: "nice", "beautiful", "amazing"
❌ **Request camera angles**: handled in Studio, not generation
❌ **Contradict styles**: "futuristic medieval" confuses the model
❌ **Exceed 2,000 characters**: prompts are truncated

## Example Prompts

### Cyberpunk Alley

```
A cozy sci-fi alley at dusk, flickering neon signs, puddles reflecting colorful lights, narrow corridor between tall buildings, steam rising from vents, cables overhead
```

### Hidden Temple

```
A mossy ancient temple hidden in a jungle, neon lanterns casting warm pools of light, stone pillars covered in vines, shallow reflecting pool in the center, mysterious and serene atmosphere
```

### Cozy Interior

```
A warm coffee shop interior on a rainy day, exposed brick walls, wooden tables, rain-streaked windows overlooking a city street, Edison bulbs casting warm light, bookshelves along one wall, leather seating
```

### Natural Landscape

```
A dramatic coastal cliff at golden hour, crashing waves against ancient rock formations, wild grass swaying in the wind, salt spray catching sunlight, moody clouds on the horizon
```

## API Usage

```json
{
  "model": "Marble 0.1-plus",
  "world_prompt": {
    "type": "text",
    "text_prompt": "A warm, rustic cabin living room with a glowing stone fireplace, cozy leather sofa, wooden beams, and large windows overlooking a snowy forest.",
    "disable_recaption": false
  }
}
```

### Parameters

| Parameter           | Type    | Description                                                                |
| ------------------- | ------- | -------------------------------------------------------------------------- |
| `text_prompt`       | string  | Your location description (max 2,000 chars)                                |
| `disable_recaption` | boolean | If `true`, uses your prompt exactly; if `false`, model may enhance/clarify |

## Iteration Tips

1. **Start with mini**: Use `Marble 0.1-mini` for quick iterations (230 credits, ~30 sec)
2. **Refine prompts**: Adjust based on results
3. **Final generation**: Use `Marble 0.1-plus` for production quality (1,580 credits, ~5 min)

## Combining with Images

Text prompts can accompany image inputs to guide interpretation:

```json
{
  "model": "Marble 0.1-plus",
  "world_prompt": {
    "type": "image",
    "image_prompt": {
      "source": "media_asset",
      "media_asset_id": "your-media-asset-id"
    },
    "text_prompt": "Transform into a mystical nighttime scene with aurora borealis"
  }
}
```

When combined with images:

- Text guides the model's interpretation of ambiguous areas
- Can shift lighting, atmosphere, or style
- If omitted, model auto-generates a caption

## Related Skills

- `world-labs-api` - API integration details
- `world-labs-image-prompt` - Single image input
- `world-labs-studio` - Camera animation and recording
