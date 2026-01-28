---
name: pokemon-data-fetcher
description: Fetches Pokemon data from the PokeAPI (pokeapi.co) and organizes it by generation. Use this skill when you need to retrieve Pokemon information, list Pokemon by generation, or collect Pokemon data in JSON format.
license: MIT
compatibility: Python 3.6+, no external dependencies required (uses standard library only)
metadata:
  author: kehwar
  version: "1.0"
  category: api-integration
---

# Pokemon Data Fetcher

## Overview

This skill provides a Python script to fetch Pokemon data from the [PokeAPI](https://pokeapi.co/docs/v2) and organize it into JSON files. The script retrieves all Pokemon names, sorts them by generation, and saves the results in a structured format.

## Quick Start

Fetch all Pokemon data organized by generation:

```bash
cd pokemon-data-fetcher/scripts
python3 fetch_pokemon.py
```

This will create JSON files in the current directory containing Pokemon data organized by generation.

## Features

### 1. Fetch All Pokemon

The script fetches all Pokemon from the PokeAPI and organizes them by their generation:

- Generation I (Kanto region)
- Generation II (Johto region)
- Generation III (Hoenn region)
- Generation IV (Sinnoh region)
- Generation V (Unova region)
- Generation VI (Kalos region)
- Generation VII (Alola region)
- Generation VIII (Galar region)
- Generation IX (Paldea region)

### 2. Sort by Generation

Pokemon are automatically sorted alphabetically within each generation for easy reference.

### 3. JSON Output

Results are saved in JSON format for easy parsing and integration with other tools:

- `pokemon_by_generation.json` - All Pokemon organized by generation
- Clean, readable JSON formatting

## Installation

1. Ensure Python 3.6+ is installed
2. No external dependencies required - uses Python standard library only

The script uses built-in modules: `urllib`, `json`, `sys`, `time`

## Usage

### Basic Usage

Navigate to the scripts directory and run:

```bash
cd pokemon-data-fetcher/scripts
python3 fetch_pokemon.py
```

### Script Output

The script will:
1. Connect to PokeAPI
2. Fetch all Pokemon species
3. Organize them by generation
4. Sort alphabetically within each generation
5. Save to `pokemon_by_generation.json`

### Output Format

```json
{
  "generation-i": [
    "bulbasaur",
    "charmander",
    "squirtle",
    ...
  ],
  "generation-ii": [
    "chikorita",
    "cyndaquil",
    "totodile",
    ...
  ],
  ...
}
```

## Examples

### Example 1: Fetch Pokemon Data

```bash
cd pokemon-data-fetcher/scripts
python3 fetch_pokemon.py
```

**Output:**
```
Fetching Pokemon data from PokeAPI...
Fetched 1025 Pokemon species
Organizing by generation...
Results saved to pokemon_by_generation.json
```

### Example 2: Use the Data

```python
import json

# Load the generated data
with open('pokemon_by_generation.json', 'r') as f:
    data = json.load(f)

# Get all Generation I Pokemon
gen1_pokemon = data['generation-i']
print(f"Generation I has {len(gen1_pokemon)} Pokemon")
print(f"First Pokemon: {gen1_pokemon[0]}")
```

## Script Details

### fetch_pokemon.py

The main script that handles all Pokemon data fetching:

**Functions:**
- `fetch_all_pokemon()` - Retrieves all Pokemon species from the API
- `organize_by_generation()` - Groups Pokemon by their generation
- `save_to_json()` - Writes results to a JSON file

**API Endpoints Used:**
- `https://pokeapi.co/api/v2/pokemon-species/?limit=10000` - Get all Pokemon species
- `https://pokeapi.co/api/v2/generation/{id}` - Get generation details

## Troubleshooting

### Issue: Connection Error

**Symptoms:** Script fails with connection error

**Solution:** Check your internet connection and verify PokeAPI is accessible:
```bash
curl https://pokeapi.co/api/v2/pokemon-species/1
```

**Prevention:** The script includes retry logic for temporary network issues

### Issue: Missing Dependencies

**Symptoms:** Script runs successfully without additional installation

**Note:** This script uses only Python standard library modules (`urllib.request`, `json`, `sys`, `time`), so no external dependencies need to be installed.

### Issue: Permission Denied

**Symptoms:** Cannot write output file

**Solution:** Ensure you have write permissions in the current directory:
```bash
chmod +w .
```

## Best Practices

- Run the script periodically to get updated Pokemon data
- Store the JSON output in version control to track changes
- Use the data as a reference for Pokemon-related applications
- Consider caching the results to avoid repeated API calls

## API Information

This skill uses the [PokeAPI](https://pokeapi.co/docs/v2), a free and open Pokemon API that provides comprehensive Pokemon data.

**API Features:**
- No authentication required
- Rate limiting: Fair use policy (no strict limits for reasonable use)
- Data includes: Pokemon species, abilities, types, moves, and more
- Well-documented and actively maintained

**API Limits:**
- Please be respectful of the free service
- Implement caching when making frequent requests
- The script is designed to minimize API calls

## Reference

- **PokeAPI Documentation**: https://pokeapi.co/docs/v2
- **PokeAPI GitHub**: https://github.com/PokeAPI/pokeapi
- **Pokemon Generations**: https://bulbapedia.bulbagarden.net/wiki/Generation

## See Also

- For detailed Pokemon data analysis, extend the script with additional API endpoints
- Consider using the data for Pokemon team builders, Pokedex apps, or educational tools
