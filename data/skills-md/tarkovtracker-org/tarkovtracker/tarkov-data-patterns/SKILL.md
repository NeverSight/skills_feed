---
name: tarkov-data-patterns
description: Use this skill when querying Tarkov game data via MCP tools. Provides optimal query patterns, data relationships, and best practices for the tarkov-dev and eft-wiki MCP servers.
---

# Tarkov Data Query Patterns

## CRITICAL: No Speculation or Editorializing

**NEVER speculate, guess, infer, or make value judgments about game items/mechanics.**

Forbidden patterns:
- ❌ "The two halves can likely be combined..."
- ❌ "This item is probably used for..."
- ❌ "These appear to be joke/troll items"
- ❌ "This is a way to throw away money"
- ❌ "Verdict: [any editorial conclusion]"
- ❌ Any value judgment about items being "useless", "worthless", "bad", etc.

Required patterns:
- ✅ Only state facts directly from the API response
- ✅ If data is missing: "The API doesn't show uses for this item. Data may be incomplete."
- ✅ If no crafts/tasks found: "No crafts or tasks found in the API data. Check in-game or wiki for current uses."
- ✅ Acknowledge data limitations: "This information may not reflect recent game updates."

**Remember: Missing data ≠ feature doesn't exist. The API may be incomplete.**

## Data Sources

| Source | Best For | Tools |
|--------|----------|-------|
| **tarkov.dev** | Stats, numbers, structured data | search_items, get_item, get_tasks, get_boss, get_ammo |
| **eft-wiki** | Lore, tactics, guides, narrative | search_wiki, get_wiki_page, get_wiki_section |

## Response Modes

All tools accept `mode` parameter:

- **concise** (default): Paginated, essential fields, bounded output
- **full**: All data, all fields, complete details

Use `concise` for:
- Discord bots, public interfaces
- Initial searches before drilling down
- Lists and overviews

Use `full` for:
- Development and research
- Single-item deep dives
- When user explicitly wants everything

## Common Patterns

### Finding Items
```
search_items(query="bitcoin")           # Find by name
get_item(id="physical-bitcoin")         # Get full details
get_items_by_category(category="keys")  # Browse category
```

### Task Research
```
get_tasks(trader="Prapor")              # All tasks from trader
get_tasks(map="Customs")                # Tasks on specific map
get_task(id="Delivery from the Past")   # Single task details
```

### Ammo Comparison
```
get_ammo(caliber="7.62x39mm")           # All ammo for caliber
# Then compare penetration vs damage trade-offs
```

### Boss Intel
```
get_boss(name="Killa")                  # Stats, health, gear
get_wiki_section("Killa", "Tactics")    # Fight strategies
```

### Pagination
```
get_items_by_category(category="weapon", limit=10, offset=0)   # First 10
get_items_by_category(category="weapon", limit=10, offset=10)  # Next 10
```

## Data Relationships

```
Items ←→ Tasks (required for / rewarded by)
Items ←→ Hideout (crafts, upgrades)
Items ←→ Barters (trade requirements)
Tasks ←→ Traders (quest givers)
Tasks ←→ Maps (where objectives are)
Bosses ←→ Maps (spawn locations)
```

## Query Optimization

1. **Start narrow**: Use specific IDs/names before broad searches
2. **Use filters**: trader, map, caliber reduce result sets
3. **Paginate early**: Use limit/offset in concise mode
4. **Cache results**: Don't re-query same data in one session

## Error Handling

- Item not found → Try search_items with partial name
- Boss not found → API returns list of valid boss names
- Wiki section missing → Response includes available sections

## Caliber Formats

Common caliber strings for `get_ammo`:
- `5.45x39mm`, `5.56x45mm`, `7.62x39mm`, `7.62x51mm`
- `9x19mm`, `9x18mm`, `9x21mm`
- `12.7x55mm`, `.338 Lapua Magnum`, `.300 Blackout`

## Category Names

Common categories for `get_items_by_category`:
- Weapons: `assault-rifle`, `smg`, `pistol`, `shotgun`, `sniper-rifle`
- Gear: `armor`, `helmet`, `rig`, `backpack`
- Items: `keys`, `medical`, `provisions`, `barter`
