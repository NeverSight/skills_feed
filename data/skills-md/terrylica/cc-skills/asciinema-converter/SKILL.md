---
name: asciinema-converter
description: Convert .cast recordings to .txt for analysis. TRIGGERS - convert cast, cast to txt, strip ANSI, batch convert.
allowed-tools: Read, Bash, Glob, Write, AskUserQuestion
---

# asciinema-converter

Convert asciinema .cast recordings to clean .txt files for Claude Code analysis. Achieves 950:1 compression (3.8GB -> 4MB) by stripping ANSI codes and JSON structure.

> **Platform**: macOS, Linux (requires asciinema CLI v2.4+)

## When to Use This Skill

Use this skill when:

- Converting .cast recordings to searchable .txt format
- Preparing recordings for Claude Code Read/Grep tools
- Batch converting multiple recordings
- Reducing storage size of session archives
- Extracting clean text from ANSI-coded terminal output

---

## Why Convert?

| Format | Size (22h session) | Claude Code Compatible | Searchable |
| ------ | ------------------ | ---------------------- | ---------- |
| .cast  | 3.8GB              | No (NDJSON + ANSI)     | Via jq     |
| .txt   | ~4MB               | Yes (clean text)       | Grep/Read  |

**Key benefit**: Claude Code's Read and Grep tools work directly on .txt output.

---

## Requirements

| Component     | Required | Installation             | Notes                 |
| ------------- | -------- | ------------------------ | --------------------- |
| **asciinema** | Yes      | `brew install asciinema` | v2.4+ for convert cmd |

---

## Workflow Phases (ALL MANDATORY)

**IMPORTANT**: All phases are MANDATORY. Do NOT skip any phase. AskUserQuestion MUST be used at each decision point.

### Phase 0: Preflight Check

**Purpose**: Verify asciinema is installed and supports convert command.

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF'
if command -v asciinema &>/dev/null; then
  VERSION=$(asciinema --version | head -1)
  echo "asciinema: $VERSION"

  # Check if convert command exists (v2.4+)
  if asciinema convert --help &>/dev/null 2>&1; then
    echo "convert: available"
  else
    echo "convert: MISSING (update asciinema to v2.4+)"
  fi
else
  echo "asciinema: MISSING"
fi
PREFLIGHT_EOF
```

If asciinema is NOT installed or convert is missing, use AskUserQuestion:

```
Question: "asciinema CLI issue detected. How would you like to proceed?"
Header: "Setup"
Options:
  - Label: "Install/upgrade asciinema (Recommended)"
    Description: "Run: brew install asciinema (or upgrade if outdated)"
  - Label: "Show manual instructions"
    Description: "Display installation commands for all platforms"
  - Label: "Cancel"
    Description: "Exit without converting"
```

---

### Phase 1: File Discovery & Selection (MANDATORY)

**Purpose**: Discover .cast files and let user select which to convert.

#### Step 1.1: Discover .cast Files

```bash
/usr/bin/env bash << 'DISCOVER_EOF'
# Search for .cast files with metadata
for file in $(fd -e cast . --max-depth 5 2>/dev/null | head -10); do
  SIZE=$(ls -lh "$file" 2>/dev/null | awk '{print $5}')
  LINES=$(wc -l < "$file" 2>/dev/null | tr -d ' ')
  DURATION=$(head -1 "$file" 2>/dev/null | jq -r '.duration // "unknown"' 2>/dev/null)
  BASENAME=$(basename "$file")
  echo "FILE:$file|SIZE:$SIZE|LINES:$LINES|DURATION:$DURATION|NAME:$BASENAME"
done
DISCOVER_EOF
```

#### Step 1.2: Present File Selection (MANDATORY AskUserQuestion)

Use discovery results to populate options:

```
Question: "Which recording would you like to convert?"
Header: "Recording"
Options:
  - Label: "{filename} ({size})"
    Description: "{line_count} events, {duration}s duration"
  - Label: "{filename2} ({size2})"
    Description: "{line_count2} events, {duration2}s duration"
  - Label: "Browse for file"
    Description: "Search in a different directory"
  - Label: "Enter path"
    Description: "Provide a custom path to a .cast file"
```

---

### Phase 2: Output Options (MANDATORY)

**Purpose**: Let user configure conversion behavior.

```
Question: "Select conversion options:"
Header: "Options"
multiSelect: true
Options:
  - Label: "Plain text output (Recommended)"
    Description: "Convert to .txt with all ANSI codes stripped"
  - Label: "Create timestamp index"
    Description: "Generate [HH:MM:SS] indexed version for navigation"
  - Label: "Split by idle time"
    Description: "Create separate chunks at 30s+ pauses"
  - Label: "Preserve terminal dimensions"
    Description: "Add header with original terminal size"
```

---

### Phase 3: Output Location (MANDATORY)

**Purpose**: Let user choose where to save the output.

```
Question: "Where should the output be saved?"
Header: "Output"
Options:
  - Label: "Same directory as source (Recommended)"
    Description: "Save {filename}.txt next to {filename}.cast"
  - Label: "Workspace tmp/"
    Description: "Save to ${PWD}/tmp/"
  - Label: "Custom path"
    Description: "Specify a custom output location"
```

---

### Phase 4: Execute Conversion

**Purpose**: Run the conversion and report results.

#### Step 4.1: Run asciinema convert

```bash
/usr/bin/env bash << 'CONVERT_EOF'
INPUT_FILE="${1:?Input file required}"
OUTPUT_FILE="${2:?Output file required}"

echo "Converting: $INPUT_FILE"
echo "Output:     $OUTPUT_FILE"
echo ""

# Run conversion
asciinema convert -f txt "$INPUT_FILE" "$OUTPUT_FILE"

if [[ $? -eq 0 && -f "$OUTPUT_FILE" ]]; then
  echo "Conversion successful"
else
  echo "ERROR: Conversion failed"
  exit 1
fi
CONVERT_EOF
```

#### Step 4.2: Report Compression

```bash
/usr/bin/env bash << 'REPORT_EOF'
INPUT_FILE="${1:?}"
OUTPUT_FILE="${2:?}"

# Get file sizes (macOS compatible)
INPUT_SIZE=$(stat -f%z "$INPUT_FILE" 2>/dev/null || stat -c%s "$INPUT_FILE" 2>/dev/null)
OUTPUT_SIZE=$(stat -f%z "$OUTPUT_FILE" 2>/dev/null || stat -c%s "$OUTPUT_FILE" 2>/dev/null)

# Calculate ratio
if [[ $OUTPUT_SIZE -gt 0 ]]; then
  RATIO=$((INPUT_SIZE / OUTPUT_SIZE))
else
  RATIO=0
fi

# Human-readable sizes
INPUT_HR=$(numfmt --to=iec "$INPUT_SIZE" 2>/dev/null || echo "$INPUT_SIZE bytes")
OUTPUT_HR=$(numfmt --to=iec "$OUTPUT_SIZE" 2>/dev/null || echo "$OUTPUT_SIZE bytes")

echo ""
echo "=== Conversion Complete ==="
echo "Input:       $INPUT_HR"
echo "Output:      $OUTPUT_HR"
echo "Compression: ${RATIO}:1"
echo "Output path: $OUTPUT_FILE"
REPORT_EOF
```

---

### Phase 5: Create Timestamp Index (if selected)

**Purpose**: Generate indexed version for navigation.

```bash
/usr/bin/env bash << 'INDEX_EOF'
INPUT_CAST="${1:?}"
OUTPUT_INDEX="${2:?}"

echo "Creating timestamp index..."

# Process .cast file to indexed format
(
  echo "# Recording Index"
  echo "# Format: [HH:MM:SS] content"
  echo "#"

  cumtime=0
  tail -n +2 "$INPUT_CAST" | while IFS= read -r line; do
    # Extract timestamp and content
    ts=$(echo "$line" | jq -r '.[0]' 2>/dev/null)
    type=$(echo "$line" | jq -r '.[1]' 2>/dev/null)
    content=$(echo "$line" | jq -r '.[2]' 2>/dev/null)

    if [[ "$type" == "o" && -n "$content" ]]; then
      # Format timestamp as HH:MM:SS
      hours=$((${ts%.*} / 3600))
      mins=$(((${ts%.*} % 3600) / 60))
      secs=$((${ts%.*} % 60))
      timestamp=$(printf "%02d:%02d:%02d" "$hours" "$mins" "$secs")

      # Clean and output (strip ANSI, limit length)
      clean=$(echo "$content" | sed 's/\x1b\[[0-9;]*[a-zA-Z]//g' | tr -d '\r' | head -c 200)
      [[ -n "$clean" ]] && echo "[$timestamp] $clean"
    fi
  done
) > "$OUTPUT_INDEX"

echo "Index created: $OUTPUT_INDEX"
wc -l "$OUTPUT_INDEX"
INDEX_EOF
```

---

### Phase 6: Next Steps (MANDATORY)

**Purpose**: Guide user to next action.

```
Question: "Conversion complete. What's next?"
Header: "Next"
Options:
  - Label: "Analyze with /asciinema-tools:analyze"
    Description: "Run keyword extraction on the converted file"
  - Label: "Open in editor"
    Description: "View the converted text file"
  - Label: "Done"
    Description: "Exit - no further action needed"
```

---

## Batch Mode (Phases 7-9)

Batch mode converts all .cast files in a directory with organized output. Activated via `--batch` flag.

**Use case**: Convert 1000+ iTerm2 auto-logged recordings efficiently.

### Phase 7: Batch Source Selection

**Purpose**: Select source directory for batch conversion.

**Trigger**: `--batch` flag without `--source` argument.

```
Question: "Select source directory for batch conversion:"
Header: "Source"
Options:
  - Label: "~/asciinemalogs (iTerm2 default)" (Recommended)
    Description: "Auto-logged iTerm2 recordings"
  - Label: "~/Downloads"
    Description: "Recent downloads containing .cast files"
  - Label: "Current directory"
    Description: "Convert .cast files in current working directory"
  - Label: "Custom path"
    Description: "Specify a custom source directory"
```

**Skip condition**: If `--source` argument provided, skip this phase.

---

### Phase 8: Batch Output Organization

**Purpose**: Configure output directory structure.

**Trigger**: `--batch` flag without `--output-dir` argument.

```
Question: "Where should converted files be saved?"
Header: "Output"
Options:
  - Label: "~/Downloads/cast-txt/ (Recommended)"
    Description: "Organized output directory, easy to find"
  - Label: "Same as source"
    Description: "Save .txt files next to .cast files"
  - Label: "Custom directory"
    Description: "Specify a custom output location"
```

**Skip condition**: If `--output-dir` argument provided, skip this phase.

---

### Phase 9: Execute Batch Conversion

**Purpose**: Convert all files with progress reporting.

```bash
/usr/bin/env bash << 'BATCH_EOF'
SOURCE_DIR="${1:?Source directory required}"
OUTPUT_DIR="${2:?Output directory required}"
SKIP_EXISTING="${3:-true}"

mkdir -p "$OUTPUT_DIR"

echo "=== Batch Conversion ==="
echo "Source:        $SOURCE_DIR"
echo "Output:        $OUTPUT_DIR"
echo "Skip existing: $SKIP_EXISTING"
echo ""

total=0
converted=0
skipped=0
failed=0
total_input_size=0
total_output_size=0

# Count files first
total=$(find "$SOURCE_DIR" -maxdepth 1 -name "*.cast" -type f 2>/dev/null | wc -l | tr -d ' ')
echo "Found $total .cast files"
echo ""

for cast_file in "$SOURCE_DIR"/*.cast; do
  [[ -f "$cast_file" ]] || continue

  basename=$(basename "$cast_file" .cast)
  txt_file="$OUTPUT_DIR/${basename}.txt"

  # Skip if already converted (and skip mode enabled)
  if [[ "$SKIP_EXISTING" == "true" && -f "$txt_file" ]]; then
    echo "SKIP: $basename (already exists)"
    ((skipped++))
    continue
  fi

  # Get input size
  input_size=$(stat -f%z "$cast_file" 2>/dev/null || stat -c%s "$cast_file" 2>/dev/null)

  # Convert
  if asciinema convert -f txt "$cast_file" "$txt_file" 2>/dev/null; then
    output_size=$(stat -f%z "$txt_file" 2>/dev/null || stat -c%s "$txt_file" 2>/dev/null)
    if [[ $output_size -gt 0 ]]; then
      ratio=$((input_size / output_size))
    else
      ratio=0
    fi
    echo "OK:   $basename (${ratio}:1 compression)"
    ((converted++))
    total_input_size=$((total_input_size + input_size))
    total_output_size=$((total_output_size + output_size))
  else
    echo "FAIL: $basename"
    ((failed++))
  fi
done

echo ""
echo "=== Batch Complete ==="
echo "Converted: $converted"
echo "Skipped:   $skipped"
echo "Failed:    $failed"

if [[ $total_output_size -gt 0 ]]; then
  overall_ratio=$((total_input_size / total_output_size))
  echo "Overall compression: ${overall_ratio}:1"
fi
echo "Output directory: $OUTPUT_DIR"
BATCH_EOF
```

---

### Phase 10: Batch Next Steps

**Purpose**: Guide user after batch conversion.

```
Question: "Batch conversion complete. What's next?"
Header: "Next"
Options:
  - Label: "Batch analyze with /asciinema-tools:analyze --batch"
    Description: "Run keyword extraction on all converted files"
  - Label: "Open output directory"
    Description: "View converted files in Finder"
  - Label: "Done"
    Description: "Exit - no further action needed"
```

---

## iTerm2 Filename Format

iTerm2 auto-logged files follow this format:

```
{creationTimeString}.{profileName}.{termid}.{iterm2.pid}.{autoLogId}.cast
```

**Example**: `20260118_232025.Claude Code.w0t1p1.70C05103-2F29-4B42-8067-BE475DB6126A.68721.4013739999.cast`

| Component          | Description                    | Example                              |
| ------------------ | ------------------------------ | ------------------------------------ |
| creationTimeString | YYYYMMDD_HHMMSS                | 20260118_232025                      |
| profileName        | iTerm2 profile (may have dots) | Claude Code                          |
| termid             | Window/tab/pane identifier     | w0t1p1                               |
| iterm2.pid         | iTerm2 process UUID            | 70C05103-2F29-4B42-8067-BE475DB6126A |
| autoLogId          | Session auto-log identifier    | 68721.4013739999                     |

---

## TodoWrite Task Template

### Single File Mode

```
1. [Preflight] Check asciinema CLI and convert command
2. [Preflight] Offer installation if missing
3. [Discovery] Find .cast files with metadata
4. [Selection] AskUserQuestion: file to convert
5. [Options] AskUserQuestion: conversion options (multi-select)
6. [Location] AskUserQuestion: output location
7. [Convert] Run asciinema convert -f txt
8. [Report] Display compression ratio and output path
9. [Index] Create timestamp index if requested
10. [Next] AskUserQuestion: next steps
```

### Batch Mode (--batch flag)

```
1. [Preflight] Check asciinema CLI and convert command
2. [Preflight] Offer installation if missing
3. [Source] AskUserQuestion: source directory (skip if --source)
4. [Output] AskUserQuestion: output directory (skip if --output-dir)
5. [Batch] Execute batch conversion with progress
6. [Report] Display aggregate compression stats
7. [Next] AskUserQuestion: batch next steps
```

---

## Post-Change Checklist

After modifying this skill:

### Single File Mode

1. [ ] Preflight check detects asciinema version correctly
2. [ ] Discovery uses heredoc wrapper for bash compatibility
3. [ ] Compression calculation handles macOS stat syntax
4. [ ] All AskUserQuestion phases are present
5. [ ] TodoWrite template matches actual workflow

### Batch Mode

1. [ ] `--batch` flag triggers batch workflow (phases 7-10)
2. [ ] `--source` skips Phase 7 (source selection)
3. [ ] `--output-dir` skips Phase 8 (output organization)
4. [ ] `--skip-existing` prevents re-conversion of existing files
5. [ ] Aggregate compression ratio calculated correctly
6. [ ] iTerm2 filename format documented

---

## CLI Quick Reference

```bash
# Basic conversion
asciinema convert -f txt recording.cast recording.txt

# Check asciinema version
asciinema --version

# Verify convert command exists
asciinema convert --help
```

---

## Reference Documentation

### Internal References

- [Anti-Patterns](./references/anti-patterns.md) - Common mistakes to avoid
- [Batch Processing](./references/batch-processing.md) - Patterns for bulk conversion
- [Integration Guide](./references/integration-guide.md) - Chaining with analyze/summarize

### External References

- [asciinema convert command](https://docs.asciinema.org/manual/cli/)
- [asciinema-cast-format skill](../asciinema-cast-format/SKILL.md)

---

## Troubleshooting

| Issue                       | Cause                     | Solution                                       |
| --------------------------- | ------------------------- | ---------------------------------------------- |
| convert command not found   | asciinema too old         | Upgrade: `brew upgrade asciinema` (need v2.4+) |
| asciinema not installed     | Missing CLI               | `brew install asciinema`                       |
| Empty output file           | Corrupted .cast input     | Verify .cast file has valid NDJSON structure   |
| Conversion failed           | Invalid cast format       | Check header line is valid JSON with `jq`      |
| numfmt not found            | macOS missing coreutils   | Use raw byte count or `brew install coreutils` |
| stat syntax error           | Linux vs macOS difference | Script handles both; check stat version        |
| Batch skipping all files    | All .txt already exist    | Use `--skip-existing=false` to reconvert       |
| Permission denied on output | Directory not writable    | Check output directory permissions             |
