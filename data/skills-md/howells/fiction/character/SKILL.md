---
name: character
description: Create or develop a character document.
argument-hint: "[name]"
context: fork
agent: fiction:character-developer
---

Develop a character using the character-developer agent.

## What This Does

1. Spawns the character-developer agent
2. Guides you through character questions
3. Produces a character document with:
   - Want vs. Need
   - The Lie, Ghost, and Flaw
   - Arc trajectory
   - Relationships
   - Voice samples
   - Key scenes

## Usage

```
/character                 # Develop a new character
/character Sacha           # Develop specific character
/character revise Jennifer # Revise existing character doc
```

If arguments provided: $ARGUMENTS

## Output

Produces/updates character doc in `characters/[name].md`
