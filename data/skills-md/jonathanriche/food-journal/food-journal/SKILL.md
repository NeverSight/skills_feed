---
name: food-journal
description: CLI to log meals, track macros, and query daily totals.
license: Not specified
---

# Skill: food-journal CLI

This skill describes how an agent should use the `food-journal` CLI to record and query meals.

## Quick Start

Assumes `food-journal` is installed and in PATH.

```bash
food-journal <command>
```

## Logging meals

Add a meal entry with macros:

```bash
food-journal add "Greek Yogurt" 120 20 8 0 0 breakfast "Plain, 170g"
```

Add a meal entry using Open Food Facts cache (per-100g macros scaled by portion size):

```bash
food-journal search mayonnaise
food-journal add "50g mayonnaise" --from-db 5000157076410
```

Optional images list (store as a single string; comma-separated works well):

```bash
food-journal add "Salad" 320 8 24 18 6 lunch "With vinaigrette" --images "salad.jpg,plate.png"
```

Edit an entry by id (use `recent` to find ids):

```bash
food-journal edit 12 "Updated Salad" 350 9 26 20 6 lunch "Extra dressing" --images "salad2.jpg"
```

Upgrade to the latest release:

```bash
food-journal upgrade
```

## Checking totals

Show everything for today:

```bash
food-journal today
```

Show totals so far today (current time cutoff):

```bash
food-journal today --so-far
```

Show totals for a specific date up to a time:

```bash
food-journal show 2026-02-03 --until 14:30
```

## Searching and cleanup

- Search Open Food Facts (cached locally):
  ```bash
  food-journal search chicken
  ```
- List recent entries:
  ```bash
  food-journal recent 10
  ```
- Delete an entry by id:
  ```bash
  food-journal delete 42
  ```

## Data storage

Entries are stored at:

```
~/.local/share/food-journal/food_journal.db
```
