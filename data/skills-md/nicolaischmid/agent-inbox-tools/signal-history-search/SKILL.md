---
name: signal-history-search
description: Search Signal Desktop message history on macOS with sub-second query times. Queries the encrypted SQLite database directly without export overhead.
license: MIT
metadata:
  author: Nicolai Schmid
  version: 1.0.0
  requires:
    - macOS
    - Signal Desktop (logged in)
    - nix-shell
scripts:
  search: ./scripts/signal-search
---

# Signal History Search

Direct SQL search against Signal Desktop's encrypted database. Queries complete in under 1 second against live data.

## When to use

- You need to quote or summarize prior Signal conversations.
- You already have Signal Desktop installed on macOS.
- You want fast, instant search without export delays.

## How it works

1. Retrieves the encryption key from macOS Keychain (`Signal Safe Storage`)
2. Decrypts the key using PBKDF2 (same as Signal Desktop)
3. Opens the SQLite database directly with SQLCipher
4. Runs SQL queries against `messages` and `conversations` tables
5. No files are written; searches happen in memory

First run caches the Python environment path (~5-10s setup), subsequent runs are sub-second.

## Usage

```bash
# List all available chats
signal-search list

# Dump all messages from a specific day
signal-search dump --date "2026-01-25"

# Dump a specific day's chat with one person
signal-search dump --date "2026-01-25" --chat "Dariush"

# Search within a specific chat
signal-search search --query "istanbul" --chat "Monika"

# Search with context (messages before/after matches)
signal-search search --query "flight" --chat "Monika" --context 3

# Regex search across all chats
signal-search search --query "invoice.*\d{4}"

# Literal string search (not regex)
signal-search search --query "100$" --literal

# Case-sensitive search
signal-search search --query "API" --case-sensitive

# Limit number of results
signal-search search --query "meeting" --max-count 10
```

### Commands

| Command | Description |
| ------- | ----------- |
| `list` | List all available chats (name and type) |
| `dump` | Dump all messages from a specific day |
| `search` | Search messages |

### Dump Flags

| Flag | Short | Description |
| ---- | ----- | ----------- |
| `--date <YYYY-MM-DD>` | `-d` | Date to dump (required) |
| `--chat <name>` | `-c` | Filter to chats containing this string |

### Search Flags

| Flag | Short | Description |
| ---- | ----- | ----------- |
| `--query <pattern>` | `-q` | Search pattern (regex by default) |
| `--chat <name>` | `-c` | Filter to chats containing this string |
| `--context <n>` | `-C` | Show N messages before and after matches |
| `--max-count <n>` | `-m` | Stop after N matches |
| `--case-sensitive` | `-s` | Case-sensitive search (default: smart-case) |
| `--literal` | `-F` | Treat query as literal string, not regex |

## Output Format

```
> [2026-01-15 12:01:11] Monika Schmid | Monika Schmid: Habe Fluge gebucht!
  [2026-01-15 12:40:53] Monika Schmid | Me: Schon!
```

- Lines starting with `>` are matches
- Format: `[timestamp] Chat Name | Sender: Message`
- Context lines (if requested) don't have the `>` prefix

## Performance

| Operation | Time |
| --------- | ---- |
| First run (env setup) | ~5-10s |
| Subsequent searches | <0.5s |
| Full chat search (1000s of messages) | <1s |

## Security considerations

- The database key is retrieved from macOS Keychain using `security find-generic-password`
- No data is written to disk; all searches happen in memory
- The cached Python path is stored in `~/.cache/signal-search/`
- Searches happen locally; nothing leaves your machine

## Legacy: Export-based search

The old export-based script (`signal-history-search`) is still available but deprecated. It uses `sigexport` to create a temporary export, then searches with `ripgrep`. This is slower (~15-30s) but may be useful if the direct DB access fails.

```bash
# Old method (slower, requires full export)
signal-history-search search --chat "Name" --query "pattern"
```

## Troubleshooting

- **"Failed to get keychain password"**: Ensure Signal Desktop has been opened at least once and you've granted keychain access
- **"Signal Desktop not found"**: Check that `~/Library/Application Support/Signal` exists
- **First run slow**: This is normal; nix-shell is setting up the Python environment with SQLCipher bindings
- **"nix-shell: command not found"**: Install Nix package manager
