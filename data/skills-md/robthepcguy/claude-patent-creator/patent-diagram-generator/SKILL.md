---
name: patent-diagram-generator
description: Create patent-style technical diagrams including flowcharts, block diagrams, and system architectures using Graphviz with reference numbering
tools: Bash, Read, Write
model: sonnet
---

# Patent Diagram Generator Skill

Create patent-style technical diagrams including flowcharts, block diagrams, and system architectures using Graphviz.

## When to Use

Invoke this skill when users ask to:
- Create flowcharts for method claims
- Generate block diagrams for system claims
- Draw system architecture diagrams
- Create technical illustrations for patents
- Add reference numbers to diagrams
- Generate patent figures

## What This Skill Does

1. **Flowchart Generation**:
   - Method step flowcharts
   - Decision trees
   - Process flows with branches
   - Patent-style step numbering

2. **Block Diagram Creation**:
   - System component diagrams
   - Hardware architecture diagrams
   - Software module diagrams
   - Component interconnections

3. **Custom Diagram Rendering**:
   - Render Graphviz DOT code
   - Support multiple formats (SVG, PNG, PDF)
   - Multiple layout engines (dot, neato, fdp, circo, twopi)

4. **Patent-Style Formatting**:
   - Add reference numbers (10, 20, 30, etc.)
   - Use clear labels and connections
   - Professional formatting for USPTO filing

## Required Dependencies

This skill requires Graphviz to be installed:

**Windows**:
```bash
choco install graphviz
```

**Linux**:
```bash
sudo apt install graphviz
```

**Mac**:
```bash
brew install graphviz
```

**Python Package**:
```bash
pip install graphviz
```

## How to Use

When this skill is invoked:

1. **Load diagram generator**:
   ```python
   import sys
   sys.path.insert(0, os.path.join(os.environ.get('CLAUDE_PLUGIN_ROOT', '.'), 'python'))
   from python.diagram_generator import PatentDiagramGenerator

   generator = PatentDiagramGenerator()
   ```

2. **Create flowchart** from steps:
   ```python
   steps = [
       {"id": "start", "label": "Start", "shape": "ellipse", "next": ["step1"]},
       {"id": "step1", "label": "Initialize System", "shape": "box", "next": ["decision"]},
       {"id": "decision", "label": "Is Valid?", "shape": "diamond", "next": ["step2", "error"]},
       {"id": "step2", "label": "Process Data", "shape": "box", "next": ["end"]},
       {"id": "error", "label": "Handle Error", "shape": "box", "next": ["end"]},
       {"id": "end", "label": "End", "shape": "ellipse", "next": []}
   ]

   diagram_path = generator.create_flowchart(
       steps=steps,
       filename="method_flowchart",
       output_format="svg"
   )
   ```

3. **Create block diagram**:
   ```python
   blocks = [
       {"id": "input", "label": "Input\\nSensor", "type": "input"},
       {"id": "cpu", "label": "Central\\nProcessor", "type": "process"},
       {"id": "memory", "label": "Memory\\nStorage", "type": "storage"},
       {"id": "output", "label": "Output\\nDisplay", "type": "output"}
   ]

   connections = [
       ["input", "cpu", "raw data"],
       ["cpu", "memory", "store"],
       ["memory", "cpu", "retrieve"],
       ["cpu", "output", "processed data"]
   ]

   diagram_path = generator.create_block_diagram(
       blocks=blocks,
       connections=connections,
       filename="system_diagram",
       output_format="svg"
   )
   ```

4. **Render custom DOT code**:
   ```python
   dot_code = """
   digraph PatentSystem {
       rankdir=LR;
       node [shape=box, style=rounded];

       Input [label="User Input\\n(10)"];
       Processor [label="Processing Unit\\n(20)"];
       Output [label="Display\\n(30)"];

       Input -> Processor [label="data"];
       Processor -> Output [label="result"];
   }
   """

   diagram_path = generator.render_dot_diagram(
       dot_code=dot_code,
       filename="custom_diagram",
       output_format="svg",
       engine="dot"
   )
   ```

5. **Add reference numbers**:
   ```python
   # After creating a diagram, add patent-style reference numbers
   reference_map = {
       "Input Sensor": 10,
       "Central Processor": 20,
       "Memory Storage": 30,
       "Output Display": 40
   }

   annotated_path = generator.add_reference_numbers(
       svg_path=diagram_path,
       reference_map=reference_map
   )
   ```

## Diagram Templates

Get common templates:
```python
templates = generator.get_diagram_templates()

# Available templates:
# - simple_flowchart: Basic process flow
# - system_block: System architecture
# - method_steps: Sequential method
# - component_hierarchy: Hierarchical structure
```

## Shape Types

### Flowchart Shapes
- `ellipse`: Start/End points
- `box`: Process steps
- `diamond`: Decision points
- `parallelogram`: Input/Output operations
- `cylinder`: Database/Storage

### Block Diagram Types
- `input`: Input devices/sensors
- `output`: Output devices/displays
- `process`: Processing units
- `storage`: Memory/storage
- `decision`: Control logic
- `default`: General components

## Layout Engines

- `dot`: Hierarchical (top-down/left-right)
- `neato`: Spring model layout
- `fdp`: Force-directed layout
- `circo`: Circular layout
- `twopi`: Radial layout

## Output Formats

- `svg`: Scalable Vector Graphics (best for editing)
- `png`: Raster image (good for viewing)
- `pdf`: Portable Document Format (USPTO compatible)

## Patent-Style Reference Numbers

Convention:
- Main components: 10, 20, 30, 40, ...
- Sub-components: 12, 14, 16 (under 10)
- Elements: 22, 24, 26 (under 20)

Example labeling:
```
"Input Sensor (10)"
"  - Detector Element (12)"
"  - Signal Processor (14)"
"Central Unit (20)"
"  - CPU Core (22)"
"  - Cache (24)"
```

## Presentation Format

When creating diagrams:

1. **Describe what will be generated**:
   "Creating a flowchart for the authentication method with 5 steps..."

2. **Generate the diagram**:
   Run Python code to create SVG/PNG/PDF

3. **Show file location**:
   "Diagram created: ${CLAUDE_PLUGIN_ROOT}/python\diagrams\method_flowchart.svg"

4. **List reference numbers** (if added):
   ```
   Reference Numbers:
   - Input Module (10)
   - Processing Unit (20)
   - Output Interface (30)
   ```

## Common Use Cases

1. **Method Claims** → Flowcharts
   - Show sequential steps
   - Include decision branches
   - Number steps (S1, S2, S3...)

2. **System Claims** → Block Diagrams
   - Show components and connections
   - Use reference numbers
   - Indicate data flow directions

3. **Architecture Diagrams** → Custom DOT
   - Complex system layouts
   - Multiple interconnections
   - Hierarchical structures

## Error Handling

If Graphviz is not installed:
1. Check installation: `dot -V`
2. Install for your OS (see above)
3. Verify Python package: `pip show graphviz`
4. Test generation: `python scripts/test_diagrams.py`

## Tools Available

- **Bash**: To run Python diagram generation
- **Write**: To save DOT code or diagrams
- **Read**: To load existing diagrams or templates
