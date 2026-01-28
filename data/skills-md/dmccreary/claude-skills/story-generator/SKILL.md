---
name: story-generator
description: This skill generates graphic novel narratives about physicists and scientists for intelligent textbooks. It creates compelling, historically-accurate stories with image prompts designed for high school students. Use this skill when the user wants to add a new scientist story to the Physics History Graphic Novels section of an MkDocs Material textbook, or when creating educational graphic novel content about historical scientists.
---

# Story Generator

This skill generates complete graphic novel narratives about physicists and scientists for intelligent textbooks built with MkDocs Material.

## When to Use This Skill

Use this skill when:

- The user requests a new graphic novel story about a scientist or physicist
- Adding a story to a Physics History Graphic Novels section
- Creating educational narrative content with image prompts for AI image generation
- The user mentions "story", "graphic novel", or "narrative" about a historical scientist

## Story Structure

Each story follows a consistent structure designed to engage high school students:

### Required Components

1. **YAML Frontmatter** - Title, description, social media image paths
2. **Cover Image** - With detailed generation prompt in `<details>` block
3. **Narrative Prompt** - Background context for generating the story
4. **Prologue** - Hook introducing the scientist's significance
5. **Chapters (12-14)** - Each with narrative text, image placeholder, and image prompt
6. **Epilogue** - Lessons table summarizing what made the scientist successful
7. **Call to Action** - Inspiring message connecting to readers
8. **Quotes** - 2-3 memorable quotes from the scientist
9. **References** - Academic sources (can use placeholders initially)

### Image Prompt Requirements

Every image prompt must specify:

- Wide-landscape **16:9 format**
- Period-appropriate art style (e.g., "Victorian", "Art Nouveau", "Renaissance")
- Specific scene details and characters
- Color palette guidance
- Emotional tone and mood

## Workflow

### Step 1: Gather Information

Before writing, identify:

- The scientist's name and birth/death years
- Key discoveries or contributions
- Central theme (e.g., "overcoming doubters", "persistence through failure")
- Historical period and appropriate art style
- 3-5 key life events that form the narrative arc

### Step 2: Create Story Directory

```bash
mkdir -p docs/stories/<scientist-name>
```

Use lowercase with hyphens for directory names (e.g., `nikola-tesla`, `marie-curie`).

### Step 3: Write the Story

Create `docs/stories/<scientist-name>/index.md` with the following structure:

```markdown
---
title: <Catchy Title> - <Scientist Name>'s <Theme>
description: A graphic-novel story of how <brief description>...
image: /stories/<scientist-name>/cover.png
og:image: /stories/<scientist-name>/cover.png
twitter:image: /stories/<scientist-name>/cover.png
social:
   cards: false
---

# <Catchy Title>: <Subtitle>

![Cover image](./cover.png)
<details>
<summary>Cover Image Prompt</summary>
[Detailed cover image generation prompt - 16:9 format, period style, composition details]
</details>

<details>
    <summary>Narrative Prompt</summary>
[Background context and style guide for the entire story]
</details>

### Prologue – <Hook Title>

[Opening narrative establishing the scientist's importance]

![](./image-01.png)
<details><summary>Image Prompt</summary>
[Detailed image prompt for prologue scene]
</details>

## Chapter 1 – <Chapter Title>

[Chapter narrative...]

![](./image-02.png)
<details><summary>Image Prompt</summary>
[Image prompt...]
</details>

[Continue for 12-14 chapters...]

### Epilogue – What Made <Scientist> Different?

[Summary of lessons learned]

| Challenge | How <Scientist> Responded | Lesson for Today |
|-----------|---------------------------|------------------|
| ... | ... | ... |

### Call to Action

[Inspiring message connecting to readers]

---

*"Quote from scientist"*
—<Scientist Name>

---

## References

1. [Title](PLACEHOLDER) - Description
[Continue with 4-6 references]
```

**Important:** Always use `.png` extension for image references (not `.jpg`).

### Step 4: Add to Navigation

Edit `mkdocs.yml` to add the story in **chronological order by birth year**:

```yaml
- Stories:
    - Overview: stories/index.md
    - <Scientist Name> - <Title>: stories/<scientist-name>/index.md
```

Reference chronological order:
- Archimedes (287 BC)
- Galileo (1564)
- Newton (1643)
- Faraday (1791)
- Tesla (1856)
- Marie Curie (1867)
- Rutherford (1871)
- Lise Meitner (1878)
- Einstein (1879)
- Chien-Shiung Wu (1912)
- Vera Rubin (1928)

### Step 5: Add Grid Card to Stories Index

Edit `docs/stories/index.md` to add a card using MkDocs Material grid format:

```markdown
- **[<Story Title>](<scientist-name>/index.md)**

    ![<Scientist Name>](./<scientist-name>/cover.png)
    <2-4 sentence compelling description emphasizing the story's theme>
```

## Writing Guidelines

### Target Audience

- High school students (grades 9-12)
- Age 14-18
- Introductory physics background
- Reading level: accessible but not dumbed down

### Narrative Style

- Use active voice and vivid descriptions
- Include dialogue when historically appropriate
- Balance drama with educational accuracy
- Emphasize the human story behind discoveries
- Show struggles, failures, and persistence
- Connect historical events to modern technology

### Theme Development

Choose a central theme that resonates with teenagers:

- Overcoming doubters and skeptics
- Persistence through failure
- Self-education and curiosity
- Fighting against discrimination
- Seeing what others couldn't see
- Staying humble despite success

### Historical Accuracy

- Research key dates, events, and relationships
- Use historically accurate details in image prompts
- Note any creative liberties in the narrative prompt
- Include verifiable quotes when possible

## Art Style Reference by Era

| Era | Suggested Art Style |
|-----|---------------------|
| Ancient (before 500 AD) | Classical Mediterranean, mosaic-inspired |
| Renaissance (1400-1600) | Italian Renaissance, warm lighting |
| Enlightenment (1600-1800) | Baroque, Dutch Golden Age |
| Victorian (1800-1900) | Pre-Raphaelite, industrial |
| Gilded Age (1870-1900) | Art Nouveau, American industrial |
| Early Modern (1900-1950) | Art Deco, Modernist |
| Mid-Century (1950-1980) | Atomic Age, clean lines |
| Contemporary | Photorealistic with period elements |

## Checklist

After completing a story, verify:

- [ ] Story directory created: `docs/stories/<name>/`
- [ ] `index.md` has full narrative and all image prompts
- [ ] All image references use `.png` extension
- [ ] YAML frontmatter has title, description, and image paths
- [ ] Added to `mkdocs.yml` navigation in chronological order
- [ ] Grid card added to `docs/stories/index.md`
- [ ] 12-14 chapters with consistent structure
- [ ] Epilogue includes lessons table
- [ ] References section present (placeholders OK initially)
- [ ] Image prompts specify 16:9 format and period style
