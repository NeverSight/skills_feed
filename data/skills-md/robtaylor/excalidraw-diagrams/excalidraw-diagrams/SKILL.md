---
name: excalidraw-diagrams
description: Creates Excalidraw diagrams programmatically. Use when the user wants flowcharts, architecture diagrams, system designs, or any visual diagram instead of ASCII art. Outputs .excalidraw files that can be opened directly in Excalidraw or VS Code with the Excalidraw extension.
---

# Excalidraw Diagram Generator

This skill generates Excalidraw diagrams programmatically using Python. Instead of creating ASCII diagrams, use this to produce professional-looking, editable diagrams.

**Output format**: `.excalidraw` JSON files that can be:
- Opened at https://excalidraw.com (drag & drop the file)
- Edited in VS Code with the Excalidraw extension
- Embedded in documentation
- **Exported to SVG/PNG** for embedding in Google Docs, presentations, etc.

## Quick Start

### Method 1: Direct Python Script (Recommended)

Write a Python script using the generator library and run it:

```python
#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/excalidraw-diagrams/scripts"))
from excalidraw_generator import Diagram, Flowchart, ArchitectureDiagram

# Create your diagram
d = Diagram()
box1 = d.box(100, 100, "Step 1", color="blue")
box2 = d.box(300, 100, "Step 2", color="green")
d.arrow_between(box1, box2, "next")
d.save("my_diagram.excalidraw")
```

Run with:
```bash
python3 /path/to/your_script.py
```

### Method 2: Inline Python Execution

```bash
python3 -c "
import sys, os
sys.path.insert(0, os.path.expanduser('~/.claude/skills/excalidraw-diagrams/scripts'))
from excalidraw_generator import Diagram

d = Diagram()
a = d.box(100, 100, 'Hello', color='blue')
b = d.box(300, 100, 'World', color='green')
d.arrow_between(a, b)
d.save('hello.excalidraw')
print('Created: hello.excalidraw')
"
```

---

## API Reference

### Diagram Class

The base class for all diagrams.

```python
from excalidraw_generator import Diagram

d = Diagram(background="#ffffff")  # white background
```

#### Methods

**`box(x, y, label, width=150, height=60, color="blue", shape="rectangle", font_size=18)`**

Create a labeled shape. Returns an `Element` for connecting.

- `x, y`: Position (top-left corner)
- `label`: Text to display
- `color`: "blue", "green", "red", "yellow", "orange", "violet", "cyan", "teal", "gray", "black"
- `shape`: "rectangle", "ellipse", "diamond"

```python
box1 = d.box(100, 100, "Process A", color="blue")
box2 = d.box(100, 200, "Decision?", color="yellow", shape="diamond")
```

**`text_box(x, y, content, font_size=20, color="black")`**

Create standalone text.

```python
d.text_box(100, 50, "System Architecture", font_size=28, color="black")
```

**`arrow_between(source, target, label=None, color="black", from_side="auto", to_side="auto")`**

Draw an arrow between two elements.

- `from_side`, `to_side`: "auto", "left", "right", "top", "bottom"

```python
d.arrow_between(box1, box2, "sends data")
d.arrow_between(box1, box3, from_side="bottom", to_side="top")
```

**`line_between(source, target, color="black")`**

Draw a line (no arrowhead) between elements.

**`save(path)`**

Save the diagram. Extension `.excalidraw` added if not present.

```python
d.save("output/my_diagram")  # Creates output/my_diagram.excalidraw
```

---

## Configuration & Styling

The diagram generator supports extensive customization through configuration classes.

### DiagramStyle - Global Appearance

Control the overall look of all elements in the diagram:

```python
from excalidraw_generator import Diagram, DiagramStyle

# Create a clean, professional diagram
d = Diagram(diagram_style=DiagramStyle(
    roughness=0,           # 0=clean, 1=hand-drawn, 2=rough sketch
    stroke_style="solid",  # "solid", "dashed", "dotted"
    stroke_width=2,        # Line thickness (1-4)
    color_scheme="corporate"  # Named color scheme
))
```

**Roughness levels:**
- `0` - Architect: Clean, precise lines
- `1` - Artist: Normal hand-drawn look (default)
- `2` - Cartoonist: Rough, sketchy appearance

### Color Schemes

Use semantic colors from predefined schemes:

```python
# Available schemes: "default", "monochrome", "corporate", "vibrant", "earth"
d = Diagram(diagram_style=DiagramStyle(color_scheme="vibrant"))

# Get colors by role
primary = d.scheme_color("primary")     # Main components
secondary = d.scheme_color("secondary") # Supporting elements
accent = d.scheme_color("accent")       # Highlights
warning = d.scheme_color("warning")     # Caution states
danger = d.scheme_color("danger")       # Error states
neutral = d.scheme_color("neutral")     # Backgrounds, users
```

**Scheme color mappings:**
| Scheme | Primary | Secondary | Accent | Warning | Danger |
|--------|---------|-----------|--------|---------|--------|
| default | blue | green | violet | yellow | red |
| monochrome | black | gray | gray | gray | black |
| corporate | blue | teal | violet | orange | red |
| vibrant | violet | cyan | orange | yellow | red |
| earth | teal | green | orange | yellow | red |

### FlowchartStyle - Flowchart Customization

Customize flowchart node colors and routing behavior:

```python
from excalidraw_generator import Flowchart, FlowchartStyle

fc = Flowchart(flowchart_style=FlowchartStyle(
    start_color="cyan",      # Start node color
    end_color="red",         # End node color
    process_color="blue",    # Process node color
    decision_color="orange", # Decision diamond color
))
```

### ArchitectureStyle - Architecture Diagram Customization

```python
from excalidraw_generator import ArchitectureDiagram, ArchitectureStyle

arch = ArchitectureDiagram(architecture_style=ArchitectureStyle(
    component_color="blue",
    database_color="green",
    service_color="violet",
    user_color="gray",
))
```

### BoxStyle - Text Box Sizing

Control automatic text box sizing:

```python
from excalidraw_generator import Diagram, BoxStyle

d = Diagram(box_style=BoxStyle(
    h_padding=40,      # Horizontal padding (total)
    v_padding=24,      # Vertical padding (total)
    min_width=80,      # Minimum box width
    min_height=40,     # Minimum box height
    font_size=18,      # Default font size
    font_family="hand" # "hand", "normal", "code"
))
```

---

### Flowchart Class

Specialized for flowcharts with automatic positioning.

```python
from excalidraw_generator import Flowchart

fc = Flowchart(direction="vertical", spacing=80)

fc.start("Begin")
fc.process("p1", "Process Data")
fc.decision("d1", "Valid?")
fc.process("p2", "Save")
fc.end("Done")

fc.connect("__start__", "p1")
fc.connect("p1", "d1")
fc.connect("d1", "p2", label="Yes")
fc.connect("d1", "__end__", label="No")

fc.save("flowchart.excalidraw")
```

#### Methods

- `start(label="Start")` - Green ellipse
- `end(label="End")` - Red ellipse
- `process(node_id, label, color="blue")` - Blue rectangle
- `decision(node_id, label, color="yellow")` - Yellow diamond
- `node(node_id, label, shape, color, width, height)` - Generic node
- `connect(from_id, to_id, label=None)` - Arrow between nodes
- `position_at(x, y)` - Set position for next node

---

### AutoLayoutFlowchart Class

For complex flowcharts with automatic hierarchical layout. Requires `grandalf` package.

```python
from excalidraw_generator import AutoLayoutFlowchart, DiagramStyle, FlowchartStyle, LayoutConfig

fc = AutoLayoutFlowchart(
    diagram_style=DiagramStyle(roughness=0),  # Clean lines
    flowchart_style=FlowchartStyle(decision_color="orange"),
    layout_config=LayoutConfig(
        vertical_spacing=100,
        horizontal_spacing=80,
    )
)

# Add nodes with semantic types
fc.add_node("start", "Start", shape="ellipse", color="green", node_type="terminal")
fc.add_node("process1", "Validate Input", node_type="process")
fc.add_node("check", "Is Valid?", shape="diamond", color="yellow", node_type="decision")
fc.add_node("success", "Process Data", node_type="process")
fc.add_node("error", "Show Error", color="red", node_type="process")
fc.add_node("end", "End", shape="ellipse", color="red", node_type="terminal")

# Add edges (arrows)
fc.add_edge("start", "process1")
fc.add_edge("process1", "check")
fc.add_edge("check", "success", label="Yes")
fc.add_edge("check", "error", label="No")
fc.add_edge("success", "end")
fc.add_edge("error", "process1", label="Retry")  # Back-edge auto-routes through whitespace

# Compute layout and render
result = fc.compute_layout(
    two_column=True,           # Split tall diagrams into columns
    target_aspect_ratio=0.8,   # Target width/height ratio
)

fc.save("auto_flowchart.excalidraw")
```

**Node types for routing:**
- `terminal` - Start/end nodes
- `process` - Standard processing steps
- `decision` - Decision diamonds (arrows exit from sides)

#### Methods

- `add_node(node_id, label, shape, color, width, height, node_type)` - Add a node
- `add_edge(from_id, to_id, label, color)` - Add an edge
- `compute_layout(start_x, start_y, max_width, max_height, routing, two_column, target_aspect_ratio, column_gap)` - Auto-position nodes

---

### ArchitectureDiagram Class

For system architecture diagrams.

```python
from excalidraw_generator import ArchitectureDiagram

arch = ArchitectureDiagram()

# Add components at specific positions
arch.user("user", "User", x=100, y=200)
arch.component("frontend", "React App", x=250, y=200, color="blue")
arch.service("api", "API Gateway", x=450, y=200, color="violet")
arch.database("db", "PostgreSQL", x=650, y=200, color="green")

# Connect them
arch.connect("user", "frontend", "HTTPS")
arch.connect("frontend", "api", "REST")
arch.connect("api", "db", "SQL")

arch.save("architecture.excalidraw")
```

#### Methods

- `component(id, label, x, y, width=150, height=80, color="blue")`
- `database(id, label, x, y, color="green")` - Ellipse shape
- `service(id, label, x, y, color="violet")`
- `user(id, label="User", x=100, y=100)` - Gray ellipse
- `connect(from_id, to_id, label=None, bidirectional=False)`

---

## Color Reference

Available colors (stroke color, with matching light background):

| Color | Stroke Hex | Use For |
|-------|-----------|---------|
| `blue` | #1971c2 | Primary components |
| `green` | #2f9e44 | Success, databases |
| `red` | #e03131 | Errors, end states |
| `yellow` | #f08c00 | Warnings, decisions |
| `orange` | #e8590c | Highlights |
| `violet` | #6741d9 | Services |
| `cyan` | #0c8599 | Network |
| `teal` | #099268 | Secondary |
| `gray` | #868e96 | Users, actors |
| `black` | #1e1e1e | Text, arrows |

---

## Complete Examples

### Example 1: Simple Flow

```python
import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/excalidraw-diagrams/scripts"))
from excalidraw_generator import Diagram

d = Diagram()

# Title
d.text_box(200, 30, "Data Processing Pipeline", font_size=24)

# Boxes
input_box = d.box(100, 100, "Input", color="gray")
process = d.box(300, 100, "Process", color="blue")
output = d.box(500, 100, "Output", color="green")

# Arrows
d.arrow_between(input_box, process, "raw data")
d.arrow_between(process, output, "results")

d.save("pipeline.excalidraw")
```

### Example 2: Decision Flowchart

```python
import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/excalidraw-diagrams/scripts"))
from excalidraw_generator import Flowchart

fc = Flowchart(direction="vertical", spacing=100)

fc.start("User Request")
fc.process("auth", "Authenticate")
fc.decision("valid", "Valid Token?")

# Branch for Yes
fc.position_at(300, 340)
fc.process("proc", "Process Request")
fc.process("resp", "Return Response")

# Branch for No
fc.position_at(100, 340)
fc.process("err", "Return 401")

fc.connect("__start__", "auth")
fc.connect("auth", "valid")
fc.connect("valid", "proc", "Yes")
fc.connect("valid", "err", "No")
fc.connect("proc", "resp")

fc.save("auth_flow.excalidraw")
```

### Example 3: Microservices Architecture

```python
import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/excalidraw-diagrams/scripts"))
from excalidraw_generator import ArchitectureDiagram

arch = ArchitectureDiagram()

# Client layer
arch.user("client", "Client", x=400, y=50)

# Gateway
arch.service("gateway", "API Gateway", x=350, y=180, color="violet")

# Services row
arch.service("auth", "Auth Service", x=100, y=350, color="blue")
arch.service("users", "User Service", x=300, y=350, color="blue")
arch.service("orders", "Order Service", x=500, y=350, color="blue")
arch.service("notify", "Notification", x=700, y=350, color="cyan")

# Databases
arch.database("authdb", "Auth DB", x=100, y=500, color="green")
arch.database("userdb", "User DB", x=300, y=500, color="green")
arch.database("orderdb", "Order DB", x=500, y=500, color="green")

# Message queue
arch.component("queue", "Message Queue", x=600, y=450, color="orange")

# Connections
arch.connect("client", "gateway", "HTTPS")
arch.connect("gateway", "auth", "gRPC")
arch.connect("gateway", "users", "gRPC")
arch.connect("gateway", "orders", "gRPC")
arch.connect("auth", "authdb", "SQL")
arch.connect("users", "userdb", "SQL")
arch.connect("orders", "orderdb", "SQL")
arch.connect("orders", "queue", "publish")
arch.connect("queue", "notify", "subscribe")

arch.save("microservices.excalidraw")
```

---

## Viewing the Output

After generating a `.excalidraw` file:

1. **Excalidraw.com**: Go to https://excalidraw.com and drag the file onto the canvas
2. **VS Code**: Install the "Excalidraw" extension, then open the file
3. **CLI**: Use `open filename.excalidraw` on macOS to open with default app

---

## Exporting to PNG

To embed diagrams in Google Docs, presentations, or other documents, export them to PNG using Playwright.

### Using the Export Script

```bash
# First time setup: install dependencies
cd ~/.claude/skills/excalidraw-diagrams/scripts
npm install
npx playwright install chromium

# Export to PNG
node ~/.claude/skills/excalidraw-diagrams/scripts/export_playwright.js diagram.excalidraw output.png
```

### How It Works

The Playwright export script:
1. Opens excalidraw.com in a headless Chromium browser
2. Loads your diagram via drag-and-drop simulation
3. Fits the view to content (Shift+1)
4. Screenshots the canvas at 1920x1200 resolution

### Requirements

- **Node.js**: Version 18 or later
- **Playwright**: Installed via `npm install` in the scripts directory
- **Chromium**: Installed via `npx playwright install chromium`

---

## Tips

1. **Positioning**: Use a grid system. Start shapes at multiples of 50 or 100 for alignment.

2. **Spacing**: Leave 50-100px between elements for clean arrows.

3. **Labels**: Keep labels short (2-3 words). Use text boxes for longer descriptions.

4. **Colors**: Use consistent colors for similar components (all databases green, all services blue).

5. **Layout patterns**:
   - **Horizontal flow**: x increases, y constant
   - **Vertical flow**: y increases, x constant
   - **Grid**: Combine both for complex diagrams

6. **After generation**: Open in Excalidraw to fine-tune positions and add hand-drawn elements.

---

## Google Drive Integration

Save diagrams directly to Google Drive for cloud storage and human editing via Excalidraw web.

### Quick Upload

```python
import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/excalidraw-diagrams/scripts"))
from excalidraw_generator import Diagram

d = Diagram()
d.box(100, 100, "Cloud Diagram", color="blue")

# Save directly to Google Drive
result = d.save_to_drive("my_diagram.excalidraw", share_public=True)

print(f"View in Drive: {result['file']['web_view_link']}")
print(f"Edit in Excalidraw: {result['edit_url']}")
```

### save_to_drive() Method

**`save_to_drive(name=None, folder_id=None, share_public=False, local_path=None)`**

Save diagram directly to Google Drive.

- `name`: Filename in Drive (default: "diagram.excalidraw")
- `folder_id`: Drive folder ID to upload to (default: root)
- `share_public`: If True, make file publicly accessible
- `local_path`: Also save locally to this path (optional)

Returns a dict with:
- `file.id`: Google Drive file ID
- `file.web_view_link`: Link to view in Drive
- `edit_url`: Link to open in Excalidraw.com
- `share`: Sharing info (if share_public=True)

### Using drive_helper Directly

For more control, use the drive_helper module:

```python
import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/excalidraw-diagrams/scripts"))
from excalidraw_generator import Diagram
from drive_helper import upload_to_drive, share_file, search_excalidraw_files

# Create and save locally first
d = Diagram()
d.box(100, 100, "Hello")
d.save("hello.excalidraw")

# Upload to specific folder
result = upload_to_drive("hello.excalidraw", folder_id="YOUR_FOLDER_ID")

# Share with specific user
share_file(result["file"]["id"], email="user@example.com", role="writer")

# Find all excalidraw files in Drive
files = search_excalidraw_files()
```

### DriveUploader Class

For batch uploads or folder organization:

```python
from drive_helper import DriveUploader

uploader = DriveUploader(folder_id="YOUR_FOLDER_ID")

result = uploader.upload(
    "diagram.excalidraw",
    name="My Diagram",
    share_public=True
)
```

### Human Editing Workflow

After saving to Drive, users can edit diagrams in two ways:

1. **Excalidraw.com** (via edit_url):
   - Open `edit_url` in browser
   - Excalidraw loads the file from Drive
   - Edit and save changes

2. **gdrive.excalidraw.com**:
   - Go to https://gdrive.excalidraw.com
   - Connect Google Drive
   - Open and edit files directly

### Round-Trip Workflow

Create with Claude → Human edits → Claude updates:

```python
from drive_helper import download_from_drive, update_in_drive

# Download human-edited version
download_from_drive(file_id, "updated_diagram.excalidraw")

# Make programmatic changes
d = Diagram()
# ... load and modify ...
d.save("updated_diagram.excalidraw")

# Upload changes back
update_in_drive(file_id, "updated_diagram.excalidraw")
```

### Complete Workflow: Diagram to Google Doc

Create a diagram, export to PNG, and embed in a Google Doc:

```python
import sys, os, subprocess, json
sys.path.insert(0, os.path.expanduser("~/.claude/skills/excalidraw-diagrams/scripts"))
from excalidraw_generator import ArchitectureDiagram

# 1. Create the diagram
arch = ArchitectureDiagram()
arch.user("user", "User", x=50, y=150)
arch.component("frontend", "Frontend", x=200, y=130, color="blue")
arch.service("api", "API Gateway", x=400, y=130, color="violet")
arch.database("db", "Database", x=600, y=150, color="green")
arch.connect("user", "frontend", "HTTPS")
arch.connect("frontend", "api", "REST")
arch.connect("api", "db", "SQL")

# 2. Save locally and to Drive
arch.save("/tmp/architecture.excalidraw")
drive_result = arch.save_to_drive("architecture.excalidraw", share_public=True)
file_id = drive_result["file"]["id"]
edit_url = drive_result["edit_url"]

# 3. Export to PNG using Playwright
subprocess.run([
    "node", os.path.expanduser("~/.claude/skills/excalidraw-diagrams/scripts/export_playwright.js"),
    "/tmp/architecture.excalidraw", "/tmp/architecture.png"
])

# 4. Upload PNG to Drive and share
drive_script = os.path.expanduser("~/.claude/skills/google-docs/scripts/drive_manager.rb")
png_result = subprocess.run(
    ["ruby", drive_script, "upload", "--file", "/tmp/architecture.png"],
    capture_output=True, text=True
)
png_data = json.loads(png_result.stdout)
png_id = png_data["file"]["id"]

# Share the PNG publicly
subprocess.run(["ruby", drive_script, "share", "--file-id", png_id, "--type", "anyone", "--role", "reader"])
png_url = f"https://drive.google.com/uc?id={png_id}&export=download"

# 5. Create Google Doc with embedded image
docs_script = os.path.expanduser("~/.claude/skills/google-docs/scripts/docs_manager.rb")

# Create document
doc_input = json.dumps({"title": "Architecture Overview", "content": "System Architecture\\n\\n"})
doc_result = subprocess.run(
    ["ruby", docs_script, "create"],
    input=doc_input, capture_output=True, text=True
)
doc_data = json.loads(doc_result.stdout)
doc_id = doc_data["document_id"]

# Insert image (Note: SVG not supported - must use PNG)
# Width 468pt fits standard Google Doc margins; height auto-scales
img_input = json.dumps({
    "document_id": doc_id,
    "image_url": png_url,
    "index": 25,
    "width": 468  # Page width in points (fits default margins)
})
subprocess.run(["ruby", docs_script, "insert-image"], input=img_input, capture_output=True, text=True)

# Append edit link
link_input = json.dumps({"document_id": doc_id, "text": f"\\n\\nEdit diagram: {edit_url}"})
subprocess.run(["ruby", docs_script, "append"], input=link_input, capture_output=True, text=True)

print(f"Document: https://docs.google.com/document/d/{doc_id}/edit")
print(f"Edit diagram: {edit_url}")
```

**Important**: Google Docs does not support SVG images. Always export to PNG for embedding.

### Prerequisites

- Google Docs skill must be installed (provides OAuth and drive_manager.rb)
- First run will prompt for Google authorization if not already done
