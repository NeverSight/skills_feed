---
name: graph-easy
description: Create ASCII diagrams for markdown using graph-easy. TRIGGERS - ASCII diagram, graph-easy, architecture diagram, markdown diagram.
---

# Graph-Easy Diagram Skill

Create ASCII architecture diagrams for any GitHub Flavored Markdown file using graph-easy. Pure text output with automatic layout - no image rendering required.

## When to Use This Skill

- Adding diagrams to README files
- Design specification documentation
- Any GFM markdown file needing architecture visualization
- Creating flowcharts, pipelines, or system diagrams
- User mentions "diagram", "ASCII diagram", "graph-easy", or "architecture chart"

**NOT for ADRs** - Use `adr-graph-easy-architect` for Architecture Decision Records (includes ADR-specific patterns like 2-diagram requirement and before/after templates).

## Preflight Check

Run these checks in order. Each layer depends on the previous.

### Layer 1: Package Manager

```bash
/usr/bin/env bash << 'SETUP_EOF'
# Detect OS and set package manager
case "$(uname -s)" in
  Darwin) PM="brew" ;;
  Linux)  PM="apt" ;;
  *)      echo "ERROR: Unsupported OS (require macOS or Linux)"; exit 1 ;;
esac
command -v $PM &>/dev/null || { echo "ERROR: $PM not installed"; exit 1; }
echo "✓ Package manager: $PM"
SETUP_EOF
```

### Layer 2: Perl + cpanminus (mise-first approach)

```bash
# Prefer mise for unified tool management
if command -v mise &>/dev/null; then
  # Install Perl via mise
  mise which perl &>/dev/null || mise install perl
  # Install cpanminus under mise perl
  mise exec perl -- cpanm --version &>/dev/null 2>&1 || {
    echo "Installing cpanminus under mise perl..."
    mise exec perl -- curl -L https://cpanmin.us | mise exec perl -- perl - App::cpanminus
  }
  echo "✓ cpanminus installed (via mise perl)"
else
  # Fallback: Install cpanminus via system package manager
  command -v cpanm &>/dev/null || {
    echo "Installing cpanminus via $PM..."
    case "$PM" in
      brew) brew install cpanminus ;;
      apt)  sudo apt install -y cpanminus ;;
    esac
  }
  echo "✓ cpanminus installed"
fi
```

### Layer 3: Graph::Easy Perl module

```bash
# Check if Graph::Easy is installed (mise-first)
if command -v mise &>/dev/null; then
  mise exec perl -- perl -MGraph::Easy -e1 2>/dev/null || {
    echo "Installing Graph::Easy via mise perl cpanm..."
    mise exec perl -- cpanm Graph::Easy
  }
  echo "✓ Graph::Easy installed (via mise perl)"
else
  perl -MGraph::Easy -e1 2>/dev/null || {
    echo "Installing Graph::Easy via cpanm..."
    cpanm Graph::Easy
  }
  echo "✓ Graph::Easy installed"
fi
```

### Layer 4: Verify graph-easy is in PATH

```bash
# Verify graph-easy is accessible and functional
command -v graph-easy &>/dev/null || {
  echo "ERROR: graph-easy not found in PATH"
  exit 1
}
# Test actual functionality (--version hangs waiting for stdin AND exits with code 2)
echo "[Test] -> [OK]" | graph-easy &>/dev/null && echo "✓ graph-easy ready"
```

### All-in-One Preflight Script

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF'
# Copy-paste this entire block to ensure graph-easy is ready (macOS + Linux)
# Prefers mise for unified cross-platform tool management

# Check for mise first (recommended)
if command -v mise &>/dev/null; then
  echo "Using mise for Perl management..."
  mise which perl &>/dev/null || mise install perl
  mise exec perl -- cpanm --version &>/dev/null 2>&1 || \
    mise exec perl -- curl -L https://cpanmin.us | mise exec perl -- perl - App::cpanminus
  mise exec perl -- perl -MGraph::Easy -e1 2>/dev/null || mise exec perl -- cpanm Graph::Easy
else
  # Fallback: system package manager
  echo "💡 Tip: Install mise for unified tool management: curl https://mise.run | sh"
  case "$(uname -s)" in
    Darwin) PM="brew" ;;
    Linux)  PM="apt" ;;
    *)      echo "ERROR: Unsupported OS"; exit 1 ;;
  esac
  command -v $PM &>/dev/null || { echo "ERROR: $PM not installed"; exit 1; }
  command -v cpanm &>/dev/null || { [ "$PM" = "apt" ] && sudo apt install -y cpanminus || brew install cpanminus; }
  perl -MGraph::Easy -e1 2>/dev/null || cpanm Graph::Easy
fi

# Verify graph-easy is in PATH and functional
command -v graph-easy &>/dev/null || {
  echo "ERROR: graph-easy not in PATH after installation"
  exit 1
}
# Test actual functionality (--version hangs waiting for stdin AND exits with code 2)
echo "[Test] -> [OK]" | graph-easy &>/dev/null && echo "✓ graph-easy ready"
PREFLIGHT_EOF
```

---

## Part 1: DSL Syntax

### Basic Elements

```
# Nodes (square brackets)
[Node Name]

# Edges (arrows)
[A] -> [B]

# Labeled edges
[A] -- label --> [B]

# Bidirectional
[A] <-> [B]

# Chain
[A] -> [B] -> [C]
```

### Groups (Containers)

```
# Named group with dashed border
( Group Name:
  [Node A]
  [Node B]
)

# Nested connections
( Frontend:
  [React App]
  [API Client]
)
( Backend:
  [API Server]
  [Database]
)
[API Client] -> [API Server]
```

### Node Labels

```
# Custom label (different from ID)
[db] { label: "PostgreSQL Database"; }

# ASCII markers for visual distinction INSIDE boxes
# (emojis break box alignment - use ASCII markers instead)
[deleted] { label: "[x] Old Component"; }
[added] { label: "[+] New Component"; }
[warning] { label: "[!] Deprecated"; }
[success] { label: "[OK] Passed"; }
```

**Character rules for nodes:**

- Graphical emojis (rocket, bulb, checkmark) - NEVER (double-width breaks box alignment)
- Unicode symbols (check, cross, arrow) - OK (single-width, safe)
- ASCII markers ([x] [+] [!] :) ) - ALWAYS safe (monospace)

Use `graph { label: "..."; }` for graphical emojis in title/legend.

**Example: Emoji breaks alignment (DON'T DO THIS)**

```
# BAD - emoji inside node
[rocket] { label: "Launch"; }
```

Renders broken:

```
+----------------+
| Launch         |   <-- box edge misaligned due to double-width emoji
+----------------+
```

**Example: ASCII marker preserves alignment (DO THIS)**

```
# GOOD - ASCII marker inside node
[rocket] { label: "[>] Launch"; }
```

Renders correctly:

```
+--------------+
| [>] Launch   |
+--------------+
```

### Flow Direction (MANDATORY: Always specify)

```
# MANDATORY: Always specify flow direction explicitly
graph { flow: south; }   # Top-to-bottom (architecture, decisions)
graph { flow: east; }    # Left-to-right (pipelines, sequences)
```

Never rely on default flow - explicit is clearer.

### Graph Title and Legend (Outside Boxes - Emojis Safe Here)

Emojis break alignment INSIDE boxes but are SAFE in graph titles/legends.

**Emoji Selection Guide** - Choose emoji that matches diagram purpose:

| Diagram Type             | Emoji  | Example Title           |
| ------------------------ | ------ | ----------------------- |
| Migration/Change         | swap   | `"Database Migration"`  |
| Deployment/Release       | rocket | `"Deployment Pipeline"` |
| Data Flow                | chart  | `"Data Ingestion Flow"` |
| Security/Auth            | lock   | `"Authentication Flow"` |
| Error/Failure            | warn   | `"Error Handling"`      |
| Decision/Branch          | split  | `"Routing Decision"`    |
| Architecture             | build  | `"System Architecture"` |
| Network/API              | globe  | `"API Integration"`     |
| Storage/Database         | disk   | `"Storage Layer"`       |
| Monitoring/Observability | signal | `"Monitoring Stack"`    |

```
# Title with semantic emoji
graph { label: "Deployment Pipeline"; flow: east; }

# Title with legend (multiline using \n)
graph { label: "Hook Flow\n----------\nAllow  Deny  Warn"; flow: south; }
```

### Node Styling (Best Practices)

```
# Rounded corners for start/end nodes
[ Start ] { shape: rounded; }
[ End ] { shape: rounded; }

# Double border for emphasis
[ Critical Step ] { border: double; }

# Bold border for important nodes
[ Key Decision ] { border: bold; }

# Dotted border for optional/skippable
[ Optional ] { border: dotted; }

# Multiline labels with \n
[ Hook Input\n(stdin JSON) ]
```

**Rendered examples:**

```
+----------+              +---------+
| Rounded  |              | Default |
+----------+              +---------+

+==========+              +=========+
| Double   |              |  Bold   |
+==========+              +=========+
```

> **Note:** Dotted borders (`{ border: dotted; }`) use special characters that render inconsistently on GitHub. Use sparingly.

### Edge Styles

```
[ A ] -> [ B ]      # Solid arrow (default)
[ A ] ..> [ B ]     # Dotted arrow
[ A ] ==> [ B ]     # Bold/double arrow
[ A ] - -> [ B ]    # Dashed arrow
[ A ] -- label --> [ B ]  # Labeled edge
```

---

## Part 2: Common Diagram Patterns

### Pipeline (Left-to-Right)

```
graph { flow: east; }
[Input] -> [Process] -> [Output]
```

### Multi-Component System

```
graph { flow: south; }
[API Gateway] -> [Service A]
[API Gateway] -> [Service B]
[Service A] -> [Database]
[Service B] -> [Database]
```

### Decision with Options

```
graph { flow: south; }
[Decision] -> [Option A]
[Decision] -> [Option B]
[Decision] -> [Option C]
```

### Grouped Components

```
( Frontend:
  [React App]
  [Vue App]
)
( Backend:
  [API Server]
  [Worker]
)
[React App] -> [API Server]
[Vue App] -> [API Server]
[API Server] -> [Worker]
```

### Bidirectional Flow

```
[Client] <-> [Server]
[Server] -> [Database]
```

### Layered Architecture

```
graph { flow: south; }
( Presentation:
  [UI Components]
)
( Business:
  [Services]
)
( Data:
  [Repository]
  [Database]
)
[UI Components] -> [Services]
[Services] -> [Repository]
[Repository] -> [Database]
```

---

## Part 3: Rendering

### Command (Platform-Aware)

```bash
# For GitHub markdown (RECOMMENDED) - renders as solid lines
graph-easy --as=ascii << 'EOF'
graph { flow: south; }
[A] -> [B] -> [C]
EOF

# For terminal/local viewing - prettier Unicode lines
graph-easy --as=boxart << 'EOF'
graph { flow: south; }
[A] -> [B] -> [C]
EOF
```

### Output Modes

| Mode     | Command       | When to Use                                                     |
| -------- | ------------- | --------------------------------------------------------------- |
| `ascii`  | `--as=ascii`  | **GitHub markdown** - `+--+` renders as solid lines everywhere  |
| `boxart` | `--as=boxart` | **Terminal only** - `┌──┐` looks nice locally, dotted on GitHub |

**Why ASCII for GitHub?** GitHub's markdown preview renders Unicode box-drawing characters (`┌─┐│└─┘`) as **dotted lines**, breaking the visual appearance. Pure ASCII (`+---+`, `|`) renders correctly as solid lines on all platforms.

### Validation Workflow

```bash
# 1. Write DSL to heredoc
# 2. Render with ascii (for GitHub) or boxart (for terminal)
graph-easy --as=ascii << 'EOF'
[Your] -> [Diagram] -> [Here]
EOF

# 3. Review output
# 4. Iterate if needed
# 5. Copy final output to markdown
# 6. Validate alignment (RECOMMENDED)
```

### Post-Generation Alignment Validation (Recommended)

After embedding diagram in markdown, validate alignment to catch rendering issues.

**Use the doc-tools plugin skill:**

```
Skill: doc-tools:ascii-diagram-validator
```

Or invoke directly: `Skill(doc-tools:ascii-diagram-validator)` with the target file path.

**Why validate?**

- Catches copy-paste alignment drift
- Detects font rendering issues
- Ensures vertical columns align properly
- Graph-easy output is machine-aligned, but manual edits can break it

**When to skip**: If diagram was just generated by graph-easy and not manually edited, validation is optional (output is inherently aligned).

---

## Part 4: Embedding in Markdown

### Markdown Format (MANDATORY: Always Include Source)

**CRITICAL**: Every rendered diagram MUST be followed by a collapsible `<details>` block containing the graph-easy source code. This is non-negotiable for:

- **Reproducibility**: Future maintainers can regenerate the diagram
- **Editability**: Source can be modified and re-rendered
- **Auditability**: Changes to diagrams are trackable in git diffs

````markdown
## Architecture

```
+----------+     +----------+     +----------+
|  Input   | --> | Process  | --> |  Output  |
+----------+     +----------+     +----------+
```

<details>
<summary>graph-easy source</summary>

```
graph { flow: east; }
[Input] -> [Process] -> [Output]
```

</details>
````

**The `<details>` block is MANDATORY** - never embed a diagram without its source.

### GFM Collapsible Section Syntax

GitHub Flavored Markdown supports HTML `<details>` and `<summary>` tags for collapsible sections. Key syntax rules:

**Structure:**

```html
<details>
  <summary>Click to expand</summary>

  <!-- BLANK LINE REQUIRED HERE -->
  Content goes here (Markdown supported)
  <!-- BLANK LINE REQUIRED HERE -->
</details>
```

**Critical rules:**

1. **Blank lines required** - Must have empty line after `<summary>` and before `</details>` for Markdown to render
2. **No indentation** - `<details>` and `<summary>` must be at column 0 (no leading spaces)
3. **Summary is clickable label** - Text in `<summary>` appears as the collapsed header
4. **Markdown inside works** - Code blocks, headers, lists all render correctly inside

**Optional: Default expanded:**

```html
<details open>
  <summary>Expanded by default</summary>

  Content visible on page load
</details>
```

**Common mistake (Markdown won't render):**

```html
<details>
  <summary>Broken</summary>
  No blank line - this won't render as Markdown!
</details>
```

**References:**

- [GitHub Docs: Collapsed sections](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections)

### Regeneration

If the markdown changes, regenerate by running the source through graph-easy again:

```bash
# Extract source from <details> block, pipe through graph-easy
graph-easy --as=boxart << 'EOF'
# paste source here
EOF
```

---

## Reference: Monospace-Safe Symbols

**Avoid emojis** - they have variable width and break box alignment on GitHub.

### Status Markers

| Meaning            | Marker |
| ------------------ | ------ |
| Added/New          | `[+]`  |
| Removed/Deleted    | `[x]`  |
| Changed/Updated    | `[*]`  |
| Warning/Deprecated | `[!]`  |
| Deferred/Pending   | `[~]`  |
| Current/Active     | `[>]`  |
| Optional           | `[?]`  |
| Locked/Fixed       | `[=]`  |

### Box Drawing (U+2500-257F)

```
- | + + + + + + + + +   (light)
= | + + + + + + + + +   (double)
```

### Arrows & Pointers

```
-> <- up down            (arrows)
v ^                      (logic - graph-easy uses these)
< > ^ v                  (ASCII arrows)
```

### Shapes & Bullets

```
* o O                    (bullets)
[ ] #                    (squares)
< > <>                   (diamonds)
```

---

## Graph Label (MANDATORY: EVERY diagram MUST have emoji + title)

**WARNING**: This is the most commonly forgotten requirement. Diagrams without labels are invalid.

### Correct Example

```
graph { label: "🚀 Deployment Pipeline"; flow: east; }
[Build] -> [Test] -> [Deploy]
```

### Anti-Pattern (INVALID - DO NOT DO THIS)

```
graph { flow: east; }
[Build] -> [Test] -> [Deploy]
```

**Why this is wrong**: Missing `label:` with emoji. Every diagram needs context at a glance.

---

## Mandatory Checklist (Before Rendering)

### Graph-Level (MUST have)

- [ ] **`graph { label: "🚀 Title"; }`** - semantic emoji + title (MOST FORGOTTEN - check first!)
- [ ] `graph { flow: south; }` or `graph { flow: east; }` - explicit direction
- [ ] Command uses `--as=ascii` for GitHub markdown (or `--as=boxart` for terminal only)

### Embedding (MUST have - non-negotiable)

- [ ] **`<details>` block with source** - EVERY diagram MUST have collapsible source code block
- [ ] Format: rendered diagram in code block, followed immediately by `<details><summary>graph-easy source</summary>` with source in code block
- [ ] Never commit a diagram without its reproducible source

### Post-Embedding Validation (Recommended)

- [ ] Run `ascii-diagram-validator` on the file after embedding diagram
- [ ] Especially important if diagram was manually edited after generation
- [ ] Catches alignment drift from copy-paste or font rendering issues

### Node Styling (Visual hierarchy)

- [ ] Start/end nodes: `{ shape: rounded; }` - entry/exit points
- [ ] Critical/important nodes: `{ border: double; }` or `{ border: bold; }`
- [ ] Optional/skippable nodes: `{ border: dotted; }`
- [ ] Default nodes: no styling (standard border)
- [ ] Long labels use `\n` for multiline - max ~15 chars per line

### Edge Styling (Semantic meaning)

- [ ] Main/happy path: `->` solid arrow
- [ ] Conditional/alternate: `..>` dotted arrow
- [ ] Emphasized/critical: `==>` bold arrow
- [ ] Edge labels are SHORT (1-3 words): `-- YES -->`, `-- error -->`

### Character Safety (Alignment)

- [ ] NO graphical emojis inside nodes (break alignment)
- [ ] Unicode symbols OK inside nodes (single-width)
- [ ] ASCII markers ALWAYS safe ([x] [+] [!] [OK])
- [ ] Graphical emojis ONLY in `graph { label: "..."; }` title

### Structure (Organization)

- [ ] Groups `( Name: ... )` used for logical clustering when 4+ related nodes
- [ ] Node IDs short, labels descriptive: `[db] { label: "PostgreSQL"; }`
- [ ] No more than 7-10 nodes per diagram (split if larger)

## Success Criteria

### Correctness

1. **Parses without error** - graph-easy accepts the DSL
2. **Renders cleanly** - no misaligned boxes or broken lines
3. **Matches content** - all key elements from description represented
4. **Source preserved (MANDATORY)** - EVERY diagram MUST have `<details>` block with graph-easy DSL source immediately after the rendered output

### Aesthetics

1. **Platform-appropriate output** - `--as=ascii` for GitHub (solid lines), `--as=boxart` for terminal only
2. **Readable labels** - multiline with `\n`, no truncation
3. **Clear flow** - direction matches natural reading (top-down or left-right)
4. **Consistent styling** - same border style = same semantic meaning throughout

### Comprehensiveness

1. **Edge semantics** - solid=normal, dotted=conditional, bold=critical
2. **Logical grouping** - related nodes in `( Group: ... )` containers

## Troubleshooting

| Issue               | Cause                    | Solution                                      |
| ------------------- | ------------------------ | --------------------------------------------- |
| `command not found` | graph-easy not installed | Run preflight check                           |
| Dotted lines on GH  | Used `--as=boxart`       | Use `--as=ascii` for GitHub markdown          |
| Box border broken   | Graphical emoji in node  | Remove emojis, use ASCII markers [x][+]       |
| Nodes overlap       | Too complex              | Split into multiple diagrams (max 7-10 nodes) |
| Edge labels cut off | Label too long           | Shorten to 1-3 words                          |
| No title showing    | Wrong syntax             | Use `graph { label: "Title"; flow: south; }`  |
| Weird layout        | No flow direction        | Add `graph { flow: south; }` or `flow: east`  |
| Parse error         | Special chars in node    | Escape or simplify node names                 |

## Resources

- [Graph::Easy on CPAN](https://metacpan.org/dist/Graph-Easy)
- [Graph::Easy Manual](http://bloodgate.com/perl/graph/manual/)
- [Graph::Easy GitHub](https://github.com/ironcamel/Graph-Easy)
