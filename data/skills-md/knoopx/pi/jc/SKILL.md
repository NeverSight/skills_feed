---
name: jc
description: Converts CLI output to JSON for structured processing and analysis. Use when parsing ps, dig, netstat, ls, or other command output into machine-readable format for piping to jq or scripts.
---

# jc

JSONifies the output of CLI tools and file-types for easier parsing.

## Basic Usage

```bash
command | jc --parser          # Pipe output
jc command                    # Magic syntax
jc --help                     # List all parsers
jc --help --parser            # Parser docs
```

## Examples

```bash
dig example.com | jc --dig | jq '.answer[].data'
ps aux | jc --ps
ifconfig | jc --ifconfig
```

## Parsers

| Category | Parsers                                                  |
| -------- | -------------------------------------------------------- |
| System   | `ps`, `top`, `free`, `df`, `du`, `ls`, `stat`, `uptime`  |
| Network  | `dig`, `ping`, `traceroute`, `netstat`, `ss`, `ifconfig` |
| Files    | `ls`, `find`, `stat`, `file`, `mount`, `fstab`           |
| Packages | `dpkg -l`, `rpm -qi`, `pacman`, `brew`                   |
| Logs     | `syslog`, `clf` (Common Log Format)                      |
| Dev      | `git log`, `docker ps`, `kubectl`                        |

## Options

| Flag | Description                 |
| ---- | --------------------------- |
| `-p` | Pretty format JSON          |
| `-r` | Raw output (less processed) |
| `-u` | Unbuffered output           |
| `-q` | Quiet (suppress warnings)   |
| `-d` | Debug mode                  |
| `-y` | YAML output                 |
| `-M` | Add metadata                |
| `-s` | Slurp multi-line input      |

## Slicing

Skip lines: `START:STOP` syntax

```bash
cat file.txt | jc 1:-1 --parser  # Skip first/last lines
```

## Slurp Mode

For multi-line parsers: `--slurp` outputs array

```bash
cat ips.txt | jc --slurp --ip-address
```

## Python Library

```python
import jc

# Parse command output
data = jc.parse('dig', output_string)

# Or parse directly
data = jc.parsers.dig.parse(output_string)
```

## Tips

- Magic syntax: `jc command` auto-detects parser
- Use `jq` for processing: `jc cmd | jq '.field'`
- `--slurp` for multiple items per file
- Streaming parsers for large outputs
- Python lib returns dict/list, not JSON

## Related Skills

- **nu-shell**: Alternative structured data processing
- **toon**: Compact JSON representation
