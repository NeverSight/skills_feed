---
name: entity-descriptions
description: >-
  Style conventions for writing entity DescriptionShort templates in mansion.rec.
  Use when adding or editing entities in data/worlds/mansion.rec to ensure
  consistent prose flow in /look output. Covers capitalization rules and
  punctuation for top-level entities vs container contents.
---

# Entity Descriptions

Style guide for `DescriptionShort` templates in `data/worlds/mansion.rec`.

## Style Rules

**Top-level entities** (no `Container` field):
- Full sentences: capital letter + period
- Example: `A {{ name }} sits in the middle of the room.`

**Container contents** (has `Container` field):
- Capitalized fragments, no period (appear as bullet items)
- Example: `A teal {{ name }} with yellow roses in it`

## Examples

### Top-level (full sentences)

```rec
Id: gallery_map
DescriptionShort: A rough {{ name }} hangs on the wall.

Id: lounge_chairs
DescriptionShort: Several {{ name }} are scattered around the room.

Id: library_couches
DescriptionShort: A pair of {{ name }} surround a coffee table in the center.
```

### Container contents (capitalized fragments)

```rec
Id: foyer_flower_vase
Container: foyer_table
DescriptionShort: A teal {{ name }} with yellow roses in it

Id: foyer_plaque
Container: foyer_table
DescriptionShort: An {{ name }}
```

### Containers with contents template

```rec
Id: foyer_table
DescriptionShort: A {{ name }} sits in the middle of the room{% if contents %}. On it:{{ contents }}{% endif %}
```

## Rendered Output

Room descriptions render as:

```
You are standing in a grand entryway...

A *Wooden Table* sits in the middle of the room. On it:
- A teal *Flower Vase* with yellow roses in it
- An *Inscribed Plaque*
```

## Validation

After editing, run:

```bash
just entities
```
