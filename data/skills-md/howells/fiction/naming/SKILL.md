---
name: naming
description: Generate and validate book title options. Produces candidates using proven naming strategies and checks availability against existing books.
---

Generate title options for your book using the naming agent.

## What This Does

1. Reads your project materials (README, themes, characters, world)
2. Extracts potential naming seeds (objects, places, themes, contradictions)
3. Generates 8-12 title candidates using proven strategies
4. **Searches to verify titles aren't already taken**
5. Rates availability and genre fit
6. Provides ranked recommendations

## Usage

```
/fiction:naming                    # Generate titles for current project
/fiction:naming /path/to/project   # Generate for specific project
```

## Output

For each recommended title:
- **Strategy used** — Object, place, character, theme, etc.
- **Why it works** — What makes this title effective
- **Availability** — Clear, Caution, or Taken
- **Genre signal** — What readers will expect

## Availability Checking

The agent searches for each candidate:
- Exact title matches on Goodreads, Amazon
- Similar titles from well-known books
- Potential confusion with existing works

**Note:** Book titles can't be copyrighted, but sharing a title with a famous book hurts discoverability.

## Title Strategies

The agent generates candidates using:
- **The Object** — Significant item (*The Kite Runner*)
- **The Place** — Key location (*Wuthering Heights*)
- **The Character** — Protagonist name (*Jane Eyre*)
- **The Theme** — Abstract made concrete (*Atonement*)
- **[Noun] of [Noun]** — Classic scope (*House of Leaves*)
- **The [Person] + [Location]** — Thriller staple (*The Girl on the Train*)
- **The Contradiction** — Tension in words (*Brave New World*)
- **The Cultural Echo** — References readers know (*East of Eden*)

## When to Use

- Project is ready for a final title
- Current title feels weak or generic
- Preparing to publish or pitch
- Series planning (title patterns that extend)
- Want to validate an existing title choice

## After Naming

1. Test favorites with target readers
2. Check domain/social availability if relevant
3. Coordinate with `/fiction:cover` — title and cover should work together
