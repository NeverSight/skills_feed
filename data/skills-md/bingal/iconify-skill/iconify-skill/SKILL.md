---
name: iconify-skill
description: Search Iconify collections and generate SVG icons with size/color customization; use for requests about finding icon IDs, suggesting icons by intent, retrieving SVG markup, or working offline with a bundled icon index.
---

# Iconify Skill

Use the CLI in `scripts/iconify_cli.py` to search, suggest, and fetch SVG icons.

## Quickstart

1. Ensure Python 3 is available.
2. Run `doctor` to validate the environment.
3. If the offline index is missing, build it.

```bash
python3 $SKILL_DIR/scripts/iconify_cli.py doctor
```

```bash
python3 $SKILL_DIR/scripts/iconify_cli.py build-index
```

## Command Interface

```bash
python3 $SKILL_DIR/scripts/iconify_cli.py <command> [arguments]
```

## Common Commands

- `list-collections` - List icon sets
- `search <query>` - Search icons (offline)
- `get <prefix:name>` - Get SVG (requires network)
- `suggest "<intent>"` - Suggest icons for intent
- `attribution` - Show license info
- `doctor` - System health check

## Usage Examples

```bash
# Search icons (offline)
python3 $SKILL_DIR/scripts/iconify_cli.py search "close button" --limit 5

# Get SVG with custom styling
python3 $SKILL_DIR/scripts/iconify_cli.py get mdi:home --size 24 --color "#3B82F6"

# Suggest icons for a feature
python3 $SKILL_DIR/scripts/iconify_cli.py suggest "user profile page"

# Filter by collection
python3 $SKILL_DIR/scripts/iconify_cli.py search "home" --prefixes lucide,heroicons
```

## Offline + Data Notes

- `search` works offline using the bundled SQLite index in `data/`.
- `get` needs network access (Iconify API).
- Use `doctor` to confirm cache/index availability.
- Use `build-index` to regenerate the search index if needed.

## Bundled Collections (32K icons)

mdi, ph, tabler, simple-icons, lucide, bi, heroicons, feather, radix-icons

## Output Format

### Exit Codes
- `0` - Success
- `1` - No icons found / invalid arguments
- `2` - Network error (get command)
- `3` - Database error (offline mode)

### SVG Output
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
  <path fill="#3B82F6" d="..."/>
</svg>
<!-- Icon: mdi:check -->
<!-- License: MIT -->
```

## References

- Read `references/REFERENCE.md` for architecture details, CLI behavior, cache paths, and error handling.
- Read `references/LICENSES_AND_ATTRIBUTION.md` when you need license requirements.
