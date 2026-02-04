---
name: asciinema-cast-format
description: Asciinema v3 .cast file format reference. TRIGGERS - cast format, asciicast spec, event codes, parse cast file.
allowed-tools: Read, Bash
---

# asciinema-cast-format

Reference documentation for the asciinema v3 .cast file format (asciicast v2 specification).

> **Platform**: All platforms (documentation only)

## When to Use This Skill

Use this skill when:

- Parsing or inspecting .cast file structure
- Understanding NDJSON header and event formats
- Building tools that read or write .cast files
- Debugging recording issues or format errors
- Learning the asciicast v2 specification

---

## Format Overview

Asciinema v3 uses NDJSON (Newline Delimited JSON) format:

- Line 1: Header object with recording metadata
- Lines 2+: Event arrays with timestamp, type, and data

---

## Header Specification

The first line is a JSON object with these fields:

| Field       | Type   | Required | Description                                 |
| ----------- | ------ | -------- | ------------------------------------------- |
| `version`   | int    | Yes      | Format version (always 2 for v3 recordings) |
| `width`     | int    | Yes      | Terminal width in columns                   |
| `height`    | int    | Yes      | Terminal height in rows                     |
| `timestamp` | int    | No       | Unix timestamp of recording start           |
| `duration`  | float  | No       | Total duration in seconds                   |
| `title`     | string | No       | Recording title                             |
| `env`       | object | No       | Environment variables (SHELL, TERM)         |
| `theme`     | object | No       | Terminal color theme                        |

### Example Header

```json
{
  "version": 2,
  "width": 120,
  "height": 40,
  "timestamp": 1703462400,
  "duration": 3600.5,
  "title": "Claude Code Session",
  "env": { "SHELL": "/bin/zsh", "TERM": "xterm-256color" }
}
```

---

## Event Codes

Each event after the header is a 3-element array:

```json
[timestamp, event_type, data]
```

| Code | Name   | Description                 | Data Format          |
| ---- | ------ | --------------------------- | -------------------- |
| `o`  | Output | Terminal output (stdout)    | String               |
| `i`  | Input  | Terminal input (stdin)      | String               |
| `m`  | Marker | Named marker for navigation | String (marker name) |
| `r`  | Resize | Terminal resize event       | `"WIDTHxHEIGHT"`     |
| `x`  | Exit   | Extension for custom data   | Varies               |

### Event Examples

```json
[0.5, "o", "$ ls -la\r\n"]
[1.2, "o", "total 48\r\n"]
[1.3, "o", "drwxr-xr-x  12 user  staff  384 Dec 24 10:00 .\r\n"]
[5.0, "m", "file-listing-complete"]
[10.5, "r", "80x24"]
```

---

## Timestamp Behavior

- Timestamps are **relative to recording start** (first event is 0.0)
- Measured in seconds with millisecond precision
- Used for playback timing and navigation

### Calculating Absolute Time

```bash
/usr/bin/env bash << 'CALC_TIME_EOF'
HEADER_TIMESTAMP=$(head -1 recording.cast | jq -r '.timestamp')
EVENT_OFFSET=1234.5  # From event array

ABSOLUTE=$(echo "$HEADER_TIMESTAMP + $EVENT_OFFSET" | bc)
date -r "$ABSOLUTE"  # macOS
# date -d "@$ABSOLUTE"  # Linux
CALC_TIME_EOF
```

---

## Parsing Examples

### Extract Header with jq

```bash
/usr/bin/env bash << 'HEADER_EOF'
head -1 recording.cast | jq '.'
HEADER_EOF
```

### Get Recording Duration

```bash
/usr/bin/env bash << 'DURATION_EOF'
head -1 recording.cast | jq -r '.duration // "unknown"'
DURATION_EOF
```

### Count Events by Type

```bash
/usr/bin/env bash << 'COUNT_EOF'
tail -n +2 recording.cast | jq -r '.[1]' | sort | uniq -c
COUNT_EOF
```

### Extract All Output Events

```bash
/usr/bin/env bash << 'OUTPUT_EOF'
tail -n +2 recording.cast | jq -r 'select(.[1] == "o") | .[2]'
OUTPUT_EOF
```

### Find Markers

```bash
/usr/bin/env bash << 'MARKERS_EOF'
tail -n +2 recording.cast | jq -r 'select(.[1] == "m") | "\(.[0])s: \(.[2])"'
MARKERS_EOF
```

### Get Event at Specific Time

```bash
/usr/bin/env bash << 'TIME_EOF'
TARGET_TIME=60  # seconds
tail -n +2 recording.cast | jq -r "select(.[0] >= $TARGET_TIME and .[0] < $((TARGET_TIME + 1))) | .[2]"
TIME_EOF
```

---

## Large File Considerations

For recordings >100MB:

| File Size | Line Count | Approach                              |
| --------- | ---------- | ------------------------------------- |
| <100MB    | <1M        | jq streaming works fine               |
| 100-500MB | 1-5M       | Use `--stream` flag, consider ripgrep |
| 500MB+    | 5M+        | Convert to .txt first with asciinema  |

### Memory-Efficient Streaming

```bash
/usr/bin/env bash << 'STREAM_EOF'
# Stream process large files
jq --stream -n 'fromstream(1|truncate_stream(inputs))' recording.cast | head -1000
STREAM_EOF
```

### Use asciinema convert

For very large files, convert to plain text first:

```bash
asciinema convert -f txt recording.cast recording.txt
```

This strips ANSI codes and produces clean text (typically 950:1 compression).

---

## TodoWrite Task Template

```
1. [Reference] Identify .cast file to analyze
2. [Header] Extract and display header metadata
3. [Events] Count events by type (o, i, m, r)
4. [Analysis] Extract relevant event data based on user need
5. [Navigation] Find markers or specific timestamps if needed
```

---

## Post-Change Checklist

After modifying this skill:

1. [ ] Event code table matches asciinema v2 specification
2. [ ] Parsing examples use heredoc wrapper for bash compatibility
3. [ ] Large file guidance reflects actual performance characteristics
4. [ ] All jq commands tested with sample .cast files

---

## Reference Documentation

- [asciinema asciicast v2 Format](https://docs.asciinema.org/manual/asciicast/v2/)
- [asciinema CLI Usage](https://docs.asciinema.org/manual/cli/)
- [jq Manual](https://jqlang.github.io/jq/manual/)

---

## Troubleshooting

| Issue                   | Cause                        | Solution                                           |
| ----------------------- | ---------------------------- | -------------------------------------------------- |
| jq parse error          | Invalid NDJSON in .cast file | Check each line is valid JSON with `jq -c .`       |
| Header missing duration | Recording in progress        | Duration added when recording ends                 |
| Unknown event type      | Custom extension event       | Check for `x` type events (extension data)         |
| Timestamp out of order  | Corrupted file               | Events should be monotonically increasing          |
| Large file jq timeout   | File too big for in-memory   | Use `--stream` flag or convert to .txt first       |
| Markers not found       | No markers in recording      | Markers are optional; not all recordings have them |
| Wrong version number    | Older cast format            | This skill covers v2 format (asciinema v3+)        |
| Empty output from tail  | File has only header         | Recording may be empty or single-line              |
