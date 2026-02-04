---
name: asciinema-analyzer
description: Semantic analysis of asciinema recordings. TRIGGERS - analyze cast, keyword extraction, find patterns in recordings.
allowed-tools: Read, Bash, Grep, Glob, AskUserQuestion
---

# asciinema-analyzer

Semantic analysis of converted .txt recordings for Claude Code consumption. Uses tiered analysis: ripgrep (primary, 50-200ms) -> YAKE (secondary, 1-5s) -> TF-IDF (optional).

> **Platform**: macOS, Linux (requires ripgrep, optional YAKE)

## When to Use This Skill

Use this skill when:

- Searching for keywords or patterns in converted recordings
- Extracting topics or themes from session transcripts
- Finding specific commands or errors in session history
- Auto-discovering unexpected terms in recordings
- Analyzing session content for documentation or review

---

## Analysis Tiers

| Tier | Tool    | Speed (4MB) | When to Use                    |
| ---- | ------- | ----------- | ------------------------------ |
| 1    | ripgrep | 50-200ms    | Always start here (curated)    |
| 2    | YAKE    | 1-5s        | Auto-discover unexpected terms |
| 3    | TF-IDF  | 5-30s       | Topic modeling (optional)      |

**Decision**: Start with Tier 1 (ripgrep + curated keywords). Only use Tier 2 (YAKE) when auto-discovery is explicitly requested.

---

## Requirements

| Component   | Required | Installation           | Notes                   |
| ----------- | -------- | ---------------------- | ----------------------- |
| **ripgrep** | Yes      | `brew install ripgrep` | Primary search tool     |
| **YAKE**    | Optional | `uv run --with yake`   | For auto-discovery tier |

---

## Workflow Phases (ALL MANDATORY)

**IMPORTANT**: All phases are MANDATORY. Do NOT skip any phase. AskUserQuestion MUST be used at each decision point.

### Phase 0: Preflight Check

**Purpose**: Verify input file exists and check for .txt (converted) format.

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF'
INPUT_FILE="${1:-}"

if [[ -z "$INPUT_FILE" ]]; then
  echo "NO_FILE_PROVIDED"
elif [[ ! -f "$INPUT_FILE" ]]; then
  echo "FILE_NOT_FOUND: $INPUT_FILE"
elif [[ "$INPUT_FILE" == *.cast ]]; then
  echo "WRONG_FORMAT: Convert to .txt first with /asciinema-tools:convert"
elif [[ "$INPUT_FILE" == *.txt ]]; then
  SIZE=$(ls -lh "$INPUT_FILE" | awk '{print $5}')
  LINES=$(wc -l < "$INPUT_FILE" | tr -d ' ')
  echo "READY: $INPUT_FILE ($SIZE, $LINES lines)"
else
  echo "UNKNOWN_FORMAT: Expected .txt file"
fi
PREFLIGHT_EOF
```

If no .txt file found, suggest running `/asciinema-tools:convert` first.

---

### Phase 1: File Selection (MANDATORY)

**Purpose**: Discover .txt files and let user select which to analyze.

#### Step 1.1: Discover .txt Files

```bash
/usr/bin/env bash << 'DISCOVER_TXT_EOF'
# Find .txt files that look like converted recordings
for file in $(fd -e txt . --max-depth 3 2>/dev/null | head -10); do
  SIZE=$(ls -lh "$file" 2>/dev/null | awk '{print $5}')
  LINES=$(wc -l < "$file" 2>/dev/null | tr -d ' ')
  BASENAME=$(basename "$file")
  echo "FILE:$file|SIZE:$SIZE|LINES:$LINES|NAME:$BASENAME"
done
DISCOVER_TXT_EOF
```

#### Step 1.2: Present File Selection (MANDATORY AskUserQuestion)

```
Question: "Which file would you like to analyze?"
Header: "File"
Options:
  - Label: "{filename}.txt ({size})"
    Description: "{line_count} lines"
  - Label: "{filename2}.txt ({size2})"
    Description: "{line_count2} lines"
  - Label: "Enter path"
    Description: "Provide a custom path to a .txt file"
  - Label: "Convert first"
    Description: "Run /asciinema-tools:convert before analysis"
```

---

### Phase 2: Analysis Type (MANDATORY)

**Purpose**: Let user choose analysis depth.

```
Question: "What type of analysis do you need?"
Header: "Type"
Options:
  - Label: "Curated keywords (Recommended)"
    Description: "Fast search (50-200ms) with domain-specific keyword sets"
  - Label: "Auto-discover keywords"
    Description: "YAKE unsupervised extraction (1-5s) - finds unexpected patterns"
  - Label: "Full analysis"
    Description: "Both curated + auto-discovery for comprehensive results"
  - Label: "Density analysis"
    Description: "Find high-concentration sections (peak activity windows)"
```

---

### Phase 3: Domain Selection (MANDATORY)

**Purpose**: Let user select which keyword domains to search.

```
Question: "Which domain keywords to search?"
Header: "Domain"
multiSelect: true
Options:
  - Label: "Trading/Quantitative"
    Description: "sharpe, sortino, calmar, backtest, drawdown, pnl, cagr, alpha, beta"
  - Label: "ML/AI"
    Description: "epoch, loss, accuracy, sota, training, model, validation, inference"
  - Label: "Development"
    Description: "iteration, refactor, fix, test, deploy, build, commit, merge"
  - Label: "Claude Code"
    Description: "Skill, TodoWrite, Read, Edit, Bash, Grep, iteration complete"
```

See [Domain Keywords Reference](./references/domain-keywords.md) for complete keyword lists.

---

### Phase 4: Execute Curated Analysis

**Purpose**: Run Grep searches for selected domain keywords.

#### Step 4.1: Trading Domain

```bash
/usr/bin/env bash << 'TRADING_EOF'
INPUT_FILE="${1:?}"
echo "=== Trading/Quantitative Keywords ==="

KEYWORDS="sharpe sortino calmar backtest drawdown pnl cagr alpha beta roi volatility"
for kw in $KEYWORDS; do
  COUNT=$(rg -c -i "$kw" "$INPUT_FILE" 2>/dev/null || echo "0")
  if [[ "$COUNT" -gt 0 ]]; then
    echo "  $kw: $COUNT"
  fi
done
TRADING_EOF
```

#### Step 4.2: ML/AI Domain

```bash
/usr/bin/env bash << 'ML_EOF'
INPUT_FILE="${1:?}"
echo "=== ML/AI Keywords ==="

KEYWORDS="epoch loss accuracy sota training model validation inference tensor gradient"
for kw in $KEYWORDS; do
  COUNT=$(rg -c -i "$kw" "$INPUT_FILE" 2>/dev/null || echo "0")
  if [[ "$COUNT" -gt 0 ]]; then
    echo "  $kw: $COUNT"
  fi
done
ML_EOF
```

#### Step 4.3: Development Domain

```bash
/usr/bin/env bash << 'DEV_EOF'
INPUT_FILE="${1:?}"
echo "=== Development Keywords ==="

KEYWORDS="iteration refactor fix test deploy build commit merge debug error"
for kw in $KEYWORDS; do
  COUNT=$(rg -c -i "$kw" "$INPUT_FILE" 2>/dev/null || echo "0")
  if [[ "$COUNT" -gt 0 ]]; then
    echo "  $kw: $COUNT"
  fi
done
DEV_EOF
```

#### Step 4.4: Claude Code Domain

```bash
/usr/bin/env bash << 'CLAUDE_EOF'
INPUT_FILE="${1:?}"
echo "=== Claude Code Keywords ==="

KEYWORDS="Skill TodoWrite Read Edit Bash Grep Write"
for kw in $KEYWORDS; do
  COUNT=$(rg -c "$kw" "$INPUT_FILE" 2>/dev/null || echo "0")
  if [[ "$COUNT" -gt 0 ]]; then
    echo "  $kw: $COUNT"
  fi
done

# Special patterns
ITERATION=$(rg -c "iteration complete" "$INPUT_FILE" 2>/dev/null || echo "0")
echo "  'iteration complete': $ITERATION"
CLAUDE_EOF
```

---

### Phase 5: YAKE Auto-Discovery (if selected)

**Purpose**: Run unsupervised keyword extraction.

```bash
/usr/bin/env bash << 'YAKE_EOF'
INPUT_FILE="${1:?}"
echo "=== Auto-discovered Keywords (YAKE) ==="

uv run --with yake python3 -c "
import yake

kw = yake.KeywordExtractor(
    lan='en',
    n=2,           # bi-grams
    dedupLim=0.9,  # dedup threshold
    top=20         # top keywords
)

with open('$INPUT_FILE') as f:
    text = f.read()

keywords = kw.extract_keywords(text)
for score, keyword in keywords:
    print(f'{score:.4f}  {keyword}')
"
YAKE_EOF
```

---

### Phase 6: Density Analysis (if selected)

**Purpose**: Find sections with highest keyword concentration.

```bash
/usr/bin/env bash << 'DENSITY_EOF'
INPUT_FILE="${1:?}"
KEYWORD="${2:-sharpe}"
WINDOW_SIZE=100  # lines

echo "=== Density Analysis: '$KEYWORD' ==="
echo "Window size: $WINDOW_SIZE lines"
echo ""

TOTAL_LINES=$(wc -l < "$INPUT_FILE" | tr -d ' ')
TOTAL_MATCHES=$(rg -c -i "$KEYWORD" "$INPUT_FILE" 2>/dev/null || echo "0")

echo "Total matches: $TOTAL_MATCHES in $TOTAL_LINES lines"
echo "Overall density: $(echo "scale=4; $TOTAL_MATCHES / $TOTAL_LINES * 1000" | bc) per 1000 lines"
echo ""

# Find peak windows
echo "Top 5 densest windows:"
awk -v ws="$WINDOW_SIZE" -v kw="$KEYWORD" '
BEGIN { IGNORECASE=1 }
{
  lines[NR] = $0
  if (tolower($0) ~ tolower(kw)) matches[NR] = 1
}
END {
  for (start = 1; start <= NR - ws; start += ws/2) {
    count = 0
    for (i = start; i < start + ws && i <= NR; i++) {
      if (matches[i]) count++
    }
    if (count > 0) {
      printf "Lines %d-%d: %d matches (%.1f per 100)\n", start, start+ws-1, count, count*100/ws
    }
  }
}
' "$INPUT_FILE" | sort -t: -k2 -rn | head -5
DENSITY_EOF
```

---

### Phase 7: Report Format (MANDATORY)

**Purpose**: Let user choose output format.

```
Question: "How should results be presented?"
Header: "Output"
Options:
  - Label: "Summary table (Recommended)"
    Description: "Keyword counts + top 5 peak sections"
  - Label: "Detailed report"
    Description: "Full analysis with timestamps and surrounding context"
  - Label: "JSON export"
    Description: "Machine-readable output for further processing"
  - Label: "Markdown report"
    Description: "Save formatted report to file"
```

---

### Phase 8: Follow-up Actions (MANDATORY)

**Purpose**: Guide user to next action.

```
Question: "Analysis complete. What's next?"
Header: "Next"
Options:
  - Label: "Jump to peak section"
    Description: "Read the highest-density section in the file"
  - Label: "Search for specific keyword"
    Description: "Grep for a custom term with context"
  - Label: "Cross-reference with .cast"
    Description: "Map findings back to original timestamps"
  - Label: "Done"
    Description: "Exit - no further action needed"
```

---

## TodoWrite Task Template

```
1. [Preflight] Check input file exists and is .txt format
2. [Preflight] Suggest /convert if .cast file provided
3. [Discovery] Find .txt files with line counts
4. [Selection] AskUserQuestion: file to analyze
5. [Type] AskUserQuestion: analysis type (curated/auto/full/density)
6. [Domain] AskUserQuestion: keyword domains (multi-select)
7. [Curated] Run Grep searches for selected domains
8. [Auto] Run YAKE if auto-discovery selected
9. [Density] Calculate density windows if requested
10. [Format] AskUserQuestion: report format
11. [Next] AskUserQuestion: follow-up actions
```

---

## Post-Change Checklist

After modifying this skill:

1. [ ] All bash blocks use heredoc wrapper
2. [ ] Curated keywords match references/domain-keywords.md
3. [ ] Analysis tiers match references/analysis-tiers.md
4. [ ] YAKE invocation uses `uv run --with yake`
5. [ ] All AskUserQuestion phases are present
6. [ ] TodoWrite template matches actual workflow

---

## Reference Documentation

- [Domain Keywords Reference](./references/domain-keywords.md)
- [Analysis Tiers Reference](./references/analysis-tiers.md)
- [ripgrep Manual](https://github.com/BurntSushi/ripgrep)
- [YAKE Documentation](https://github.com/LIAAD/yake)

---

## Troubleshooting

| Issue                       | Cause                       | Solution                                          |
| --------------------------- | --------------------------- | ------------------------------------------------- |
| "WRONG_FORMAT" error        | .cast file provided         | Run /asciinema-tools:convert first to create .txt |
| ripgrep not found           | Not installed               | `brew install ripgrep`                            |
| YAKE import error           | Package not installed       | `uv run --with yake` handles this automatically   |
| No keywords found           | Wrong domain selected       | Try different domain or auto-discovery mode       |
| Density analysis empty      | Keyword not in file         | Use curated search first to find valid keywords   |
| File too large for YAKE     | Memory constraints          | Use Tier 1 (ripgrep) only for large files         |
| Zero matches in all domains | File is binary or corrupted | Verify file is plain text with `file` command     |
| fd command not found        | Not installed               | `brew install fd` or use `find` alternative       |
