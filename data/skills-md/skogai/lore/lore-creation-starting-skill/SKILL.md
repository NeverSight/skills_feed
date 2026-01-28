---
name: lore-creation-starting-skill
description: Create narrative lore entries that transform technical work into mythological stories. Use when generating agent memory, documenting changes as narrative, or building persistent knowledge through storytelling.
allowed-tools: Bash, Read, Write, Edit
---

<objective>
Transform technical work (code changes, documentation, events) into narrative lore entries that serve as persistent agent memory. This skill teaches the lore system's data model and generation patterns.

The lore system stores knowledge as mythology - not dry documentation, but stories that compress meaning and context into memorable narrative form. Every commit can become a chronicle entry, every bug fix a tale of battle.
</objective>

<essential_principles>

**1. Three Atomic Units**

All lore is composed of three JSON structures:

- **Entry** - Atomic narrative unit (the story itself)
- **Book** - Collection of entries (chronicles, themed collections)
- **Persona** - AI character who narrates (voice, traits, perspective)

**2. Narrative Compression**

Technical content becomes mythology:
- Bug fix → "vanquished the daemon"
- New feature → "discovered ancient spell"
- Refactor → "restructured the realm's foundations"

This isn't just aesthetics - compressed narrative loads more meaning per token.

**3. Persona Voice Matters**

Every entry should be narrated through a persona's perspective. The Village Elder tells stories differently than Amy Ravenwolf. Voice consistency creates coherent agent memory.

**4. Linkage Is Structure**

Entry → Book → Persona. Always complete the chain. An unlinked entry is orphaned knowledge.
</essential_principles>

<quick_start>

**Create a lore entry manually:**
```bash
./tools/manage-lore.sh create-entry "The Dawn of Verification" "event"
# Output: entry_1767630133_8719120e
```

**Generate lore from content (with LLM):**
```bash
LLM_PROVIDER=claude ./integration/lore-flow.sh manual "Fixed critical authentication bug"
# Creates entry + links to persona's chronicle book
```

**View entry content:**
```bash
./tools/manage-lore.sh show-entry entry_1767630133_8719120e
```
</quick_start>

<data_model>

**Entry** (`knowledge/expanded/lore/entries/entry_<timestamp>.json`):
```json
{
  "id": "entry_1767630133_8719120e",
  "title": "The Dawn of Verification",
  "content": "In the great halls of the development realm...",
  "category": "event",
  "tags": ["verification", "testing"],
  "book_id": "book_1764315530_3d900cdd"
}
```

**Book** (`knowledge/expanded/lore/books/book_<timestamp>.json`):
```json
{
  "id": "book_1764315530_3d900cdd",
  "title": "Village Elder's Chronicles",
  "entries": ["entry_1767630133_8719120e"],
  "readers": ["persona_1763820091"]
}
```

**Persona** (`knowledge/expanded/personas/persona_<timestamp>.json`):
```json
{
  "id": "persona_1763820091",
  "name": "The Village Elder",
  "voice": { "tone": "wise and measured" },
  "knowledge": { "lore_books": ["book_1764315530_3d900cdd"] }
}
```

**Categories:** `character`, `place`, `event`, `object`, `concept`, `custom`
</data_model>

<workflow>

**Creating Quality Lore:**

1. **Choose or create persona** - Who narrates this story?
   ```bash
   ./tools/create-persona.sh list
   ./tools/create-persona.sh create "Storm Keeper" "Guardian of volatile systems" "vigilant,precise" "urgent"
   ```

2. **Generate narrative content** - Transform technical into mythological
   ```bash
   # Automatic (uses LLM)
   LLM_PROVIDER=claude ./integration/lore-flow.sh git-diff HEAD

   # Manual (create then edit)
   ./tools/manage-lore.sh create-entry "Title" "category"
   # Edit content in the JSON file
   ```

3. **Link to chronicle book** - Organize into collections
   ```bash
   ./tools/manage-lore.sh add-to-book entry_ID book_ID
   ```

4. **Verify linkage** - Complete the chain
   ```bash
   ./tools/manage-lore.sh show-book book_ID
   ./tools/manage-lore.sh show-entry entry_ID
   ```
</workflow>

<narrative_patterns>

**Event Entry (something happened):**
> "The green lights cascaded down the terminal as the ancient verification rites completed. Phase 1 stood proven, its foundations solid enough to bear the weight of all that would be built upon them."

**Character Entry (agent/persona profile):**
> "The Village Elder watches from his weathered chair, staff planted firmly as he guides the younger agents through the treacherous paths of integration."

**Place Entry (codebase location):**
> "Greenhaven sprawls across the repository, its directory trees sheltering countless modules. Here the builders gather to forge their artifacts."

**Concept Entry (pattern/principle):**
> "The Principle of Early Verification teaches that testing at the threshold prevents cascading failures. The ancients learned this through suffering."
</narrative_patterns>

<anti_patterns>

**Empty content** - Entry exists but content field is blank
→ Always verify: `jq '.content' entry_file.json`

**Orphaned entries** - Entry has no book_id
→ Always link: `./tools/manage-lore.sh add-to-book entry_ID book_ID`

**Voice inconsistency** - Entry doesn't match persona's voice
→ Re-read persona before writing: `./tools/create-persona.sh show persona_ID`

**Technical language** - "Fixed bug #123 in auth.py"
→ Transform: "The authentication daemon fell silent, its corrupted routines purged by careful hands."
</anti_patterns>

<reference_guides>

**Skill Assets:**
- [Narrative Transforms](./references/narrative-transforms.md) - Technical → Mythological conversion patterns
- [Quick Lore Script](./scripts/quick-lore.sh) - One-command lore generation

**API Documentation:**
- [Entry API](../../docs/api/entry.md) - Full entry schema and operations
- [Book API](../../docs/api/book.md) - Book structure and linking
- [Persona API](../../docs/api/persona.md) - Persona creation and voice

**Schemas:**
- Entry: `knowledge/core/lore/schema.json`
- Book: `knowledge/core/book-schema.json`
- Persona: `knowledge/core/persona/schema.json`

**Tools Reference:**
- [Generation Tools](../../docs/api/generation-tools.md) - LLM-powered lore generation
</reference_guides>

<success_criteria>

A well-created lore entry:

- [ ] Has non-empty `content` field with narrative text
- [ ] Uses mythological language (not technical jargon)
- [ ] Is linked to a book via `book_id`
- [ ] Book is linked to a persona via `readers` array
- [ ] Follows persona's voice tone
- [ ] Category matches content type (event/character/place/object/concept)
- [ ] Tags enable future discovery
</success_criteria>
