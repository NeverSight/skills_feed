---
name: add-verb
description: Add synonyms to verb word lists. Use when adding verbs/synonyms for MUD actions like look, touch, attack, use, take, open, close, or drop.
---

# Adding Verbs to Word Lists

Verb word lists map player input to entity handlers (`OnLook`, `OnTouch`, etc.).

## Adding a Verb

Run the script from the project root:

```bash
./scripts/add_verb.py --action ACTION --verb VERB
```

**Valid actions**: Auto-discovered from `data/verbs/on_*.txt` files. Run `./scripts/add_verb.py --help` to see current options.

**Example**: `./scripts/add_verb.py --action on_attack --verb pummel`

## Rules

1. **No duplicates**: A verb can only exist in ONE file across all word lists
2. **Lowercase**: All verbs are stored lowercase
3. **Auto-sorted**: Files are automatically kept alphabetically sorted (Python default sort)
4. **One per line**: Each verb on its own line
5. **Multi-word verbs**: Supported (e.g., "log in", "log out")

## Files

Word lists are in `data/verbs/`:
- `on_look.txt` - examine, inspect, look, peer, etc.
- `on_touch.txt` - feel, poke, prod, touch, etc.
- `on_attack.txt` - attack, hit, smash, strike, etc.
- `on_use.txt` - activate, operate, use, etc.
- `on_take.txt` - grab, pick, take, etc.
- `on_open.txt` - open, login, access, boot, etc.
- `on_close.txt` - close, logout, disconnect, etc.
- `on_drop.txt` - drop, etc.

## Validation

Run `just verbs` to check for duplicates across all files.
