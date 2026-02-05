---
name: Team Group Photo
description: This skill should be used when the user asks to "create team photo", "generate group portrait", "make team banner", "pixel art team image", "group shot with multiple people", or needs a composite pixel art image featuring multiple team members arranged together.
---

# Team Group Photo

Generate pixel art team group portraits featuring multiple characters arranged in a composition, each maintaining likeness to their individual reference photos.

## Key Insight: Transfer, Don't Describe

**DO NOT describe faces in your prompt.** The more you describe facial features, the more the model will GENERATE new faces instead of TRANSFERRING likeness from the input images.

Instead:
- Provide all reference images as `--input` flags
- Use a simple prompt that instructs TRANSFER of likeness
- Include the background image as another input

## Usage

Use the generate-image skill script directly:

```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/generate-image && bun run scripts/generate.ts \
  "Pixel art team group portrait. Arrange left to right: [Name1], [Name2], [Name3], [etc], [Mascot]. Transfer exact likeness from each input reference. Use the background image exactly. Uniform pixel art style. No text. No border." \
  --input /path/to/person1.png \
  --input /path/to/person2.png \
  --input /path/to/person3.png \
  --input /path/to/mascot.jpg \
  --input /path/to/background.png \
  --aspect 21:9 \
  --size 2K \
  --output /path/to/output.png
```

## Example: B Open Team (Light Mode)

```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/generate-image && bun run scripts/generate.ts \
  "Pixel art team group portrait. Arrange left to right: Kurt, Luke, David, Jason, Dan, Root mascot. Transfer exact likeness from each input reference. Use the watercolor sky background exactly. Uniform pixel art style. No text. No border." \
  --input /path/to/team/kurt.png \
  --input /path/to/team/luke.png \
  --input /path/to/team/david.jpg \
  --input /path/to/team/jason.png \
  --input /path/to/team/dan.png \
  --input /path/to/team/root.jpg \
  --input /path/to/bg-light.png \
  --aspect 21:9 \
  --size 2K \
  --output /path/to/team-group-light.png
```

## Example: B Open Team (Dark Mode)

```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/generate-image && bun run scripts/generate.ts \
  "Pixel art team group portrait. Arrange left to right: Kurt, Luke, David, Jason, Dan, Root mascot. Transfer exact likeness from each input reference. Use the night mountain scene background exactly. Uniform pixel art style. No text. No border." \
  --input /path/to/team/kurt.png \
  --input /path/to/team/luke.png \
  --input /path/to/team/david.jpg \
  --input /path/to/team/jason.png \
  --input /path/to/team/dan.png \
  --input /path/to/team/root.jpg \
  --input /path/to/bg-dark.png \
  --aspect 21:9 \
  --size 2K \
  --output /path/to/team-group-dark.png
```

## What NOT to Do

**BAD - Describing faces causes model to generate instead of transfer:**

```
## CHARACTER LINEUP (Left to Right)

1. **KURT** (leftmost, front)
   - Bald head
   - Brown/auburn full beard
   - Dark navy suit jacket with tie
   - Friendly smile

2. **LUKE** (slightly behind Kurt)
   - Dark curly/wavy hair
   - Dark beard and goatee
   - Pink button-up shirt
```

This approach tells the model WHAT to generate, causing it to create generic faces matching the description rather than transferring likeness from the actual input photos.

**GOOD - Simple transfer instruction:**

```
"Transfer exact likeness from each input reference"
```

Let the input images speak for themselves. The model will extract the likeness directly from the photos.

## Light vs Dark Variants

For theme-aware websites, generate both variants:

1. **Light mode**: Use bright/day background image as input
2. **Dark mode**: Use dark/night background image as input

Same character references, different background input.

## Options Reference

- `--input <path>` - Reference image (up to 14 total: 5 humans, 6 objects)
- `--aspect <ratio>` - 1:1, 16:9, 9:16, 4:3, 3:4, 21:9
- `--size <1K|2K|4K>` - Image resolution
- `--output <path>` - Output file path

## Troubleshooting

### Faces don't match references
- Remove ALL facial descriptions from your prompt
- Ensure each reference image is included as `--input`
- Use simpler prompt focused on "transfer" language

### Background doesn't match reference
- Include background image as an `--input`
- Say "Use the background image exactly" in prompt
- Don't describe the background, just reference it

### Mascot rendered incorrectly
- Include mascot reference as `--input`
- Name the mascot in the arrangement list
- If still wrong, add brief note: "Root is a yellow frog with banana on head"

### Style inconsistent across characters
- Add "Uniform pixel art style" to prompt
- Use same reference style for all character inputs
- Generate at 2K for better detail consistency
