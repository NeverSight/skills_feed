---
name: graphviz-diagrams
description: Create complex graph visualizations using Graphviz DOT language, with both source code and pre-rendered images.
---


# Graphviz Diagrams Skill

## Purpose
Create complex graph visualizations using Graphviz DOT language, with both source code and pre-rendered images.

## When to Use
- Complex dependency graphs
- Call graphs and code flow
- Network topologies
- Hierarchical structures
- State machines with complex transitions
- Any graph needing precise layout control

## Output Format

Every Graphviz diagram should include:
1. **Inline DOT source** - For reference and future editing
2. **Pre-rendered image** - For viewing in any markdown renderer

### Document Structure
~~~markdown
## Diagram: [Name]

### Source
```dot
digraph G {
    A -> B
}
```

### Rendered
![Diagram Name](./attachments/diagram-name.png)
~~~

## Rendering Workflow

### Step 1: Write DOT Source
```python
dot_source = """
digraph G {
    rankdir=LR;
    A -> B -> C;
}
"""
```

### Step 2: Render to Image
```python
import subprocess
from pathlib import Path

def render_graphviz(
    dot_source: str,
    output_path: Path,
    format: str = "png",
    engine: str = "dot"
) -> Path:
    """
    Render DOT source to image file.

    Args:
        dot_source: DOT language source code
        output_path: Output file path (without extension)
        format: Output format (png, svg, pdf)
        engine: Layout engine (dot, neato, fdp, circo, twopi, sfdp)

    Returns:
        Path to rendered image
    """
    output_file = output_path.with_suffix(f".{format}")

    result = subprocess.run(
        [engine, f"-T{format}", "-o", str(output_file)],
        input=dot_source,
        text=True,
        capture_output=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"Graphviz error: {result.stderr}")

    return output_file
```

### Step 3: Embed in Markdown
```python
def create_diagram_markdown(
    name: str,
    dot_source: str,
    image_path: str
) -> str:
    """Create markdown with both source and rendered image."""
    return f"""## Diagram: {name}

### Source
```dot
{dot_source}
```

### Rendered
![{name}]({image_path})
"""
```

## DOT Language Reference

### Basic Graph Types

#### Directed Graph (digraph)
```dot
digraph G {
    A -> B;
    B -> C;
    A -> C;
}
```

#### Undirected Graph (graph)
```dot
graph G {
    A -- B;
    B -- C;
    A -- C;
}
```

### Graph Attributes

```dot
digraph G {
    // Graph attributes
    rankdir=LR;           // Direction: TB, BT, LR, RL
    splines=ortho;        // Edge style: line, polyline, curved, ortho, spline
    nodesep=0.5;          // Space between nodes
    ranksep=1.0;          // Space between ranks
    bgcolor="white";      // Background color
    fontname="Helvetica"; // Font for labels

    // Nodes and edges
    A -> B;
}
```

### Node Attributes

```dot
digraph G {
    // Node defaults
    node [shape=box, style=filled, fillcolor=lightblue];

    // Individual node styling
    A [label="Start", shape=ellipse, fillcolor=green];
    B [label="Process
Data", shape=box];
    C [label="Decision", shape=diamond, fillcolor=yellow];
    D [label="End", shape=ellipse, fillcolor=red];

    A -> B -> C;
    C -> D;
}
```

#### Common Node Shapes
| Shape | Use Case |
|-------|----------|
| `box` | Process, action |
| `ellipse` | Start/end, terminal |
| `diamond` | Decision |
| `circle` | State |
| `record` | Structured data |
| `Mrecord` | Rounded record |
| `cylinder` | Database |
| `folder` | Directory/collection |
| `component` | Component |
| `note` | Annotation |

### Edge Attributes

```dot
digraph G {
    // Edge defaults
    edge [color=gray, fontsize=10];

    A -> B [label="step 1", color=blue, penwidth=2];
    B -> C [label="step 2", style=dashed];
    C -> D [label="step 3", arrowhead=empty];
    D -> A [label="loop", style=dotted, constraint=false];
}
```

#### Arrow Styles
| Arrowhead | Description |
|-----------|-------------|
| `normal` | Filled triangle (default) |
| `empty` | Open triangle |
| `dot` | Filled circle |
| `odot` | Open circle |
| `diamond` | Filled diamond |
| `none` | No arrowhead |
| `vee` | V-shape |
| `box` | Filled square |

### Subgraphs and Clusters

```dot
digraph G {
    // Cluster (named subgraph with cluster_ prefix)
    subgraph cluster_frontend {
        label="Frontend";
        style=filled;
        fillcolor=lightgray;

        UI -> Components -> State;
    }

    subgraph cluster_backend {
        label="Backend";
        style=filled;
        fillcolor=lightyellow;

        API -> Service -> Database;
    }

    // Cross-cluster edges
    State -> API [label="HTTP"];
}
```

### Records (Structured Nodes)

```dot
digraph G {
    node [shape=record];

    user [label="User|{id: int|name: string|email: string}"];
    order [label="Order|{id: int|user_id: int|total: decimal}"];

    user -> order [label="1:N"];
}
```

### HTML Labels

```dot
digraph G {
    node [shape=none];

    table [label=<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
            <TR><TD BGCOLOR="lightblue"><B>User</B></TD></TR>
            <TR><TD ALIGN="LEFT">id: int</TD></TR>
            <TR><TD ALIGN="LEFT">name: string</TD></TR>
            <TR><TD ALIGN="LEFT">email: string</TD></TR>
        </TABLE>
    >];
}
```

## Layout Engines

| Engine | Best For | Description |
|--------|----------|-------------|
| `dot` | Hierarchies | Directed graphs, trees, DAGs |
| `neato` | Networks | Undirected graphs, spring model |
| `fdp` | Large networks | Force-directed, scalable |
| `sfdp` | Very large | Multiscale force-directed |
| `circo` | Circular | Circular layouts |
| `twopi` | Radial | Radial layouts from root |

### Usage
```bash
# Different engines produce different layouts
dot -Tpng graph.dot -o graph-hierarchical.png
neato -Tpng graph.dot -o graph-spring.png
circo -Tpng graph.dot -o graph-circular.png
```

## Common Patterns

### Dependency Graph
```dot
digraph Dependencies {
    rankdir=BT;
    node [shape=box, style=filled, fillcolor=lightblue];

    // Packages
    app [label="app"];
    api [label="api"];
    core [label="core"];
    utils [label="utils"];
    db [label="database"];

    // Dependencies (arrows point to dependency)
    app -> api;
    app -> core;
    api -> core;
    api -> db;
    core -> utils;
    db -> utils;
}
```

### State Machine
```dot
digraph StateMachine {
    rankdir=LR;
    node [shape=circle];

    // Start state
    start [shape=point, width=0.2];

    // States
    idle [label="Idle"];
    loading [label="Loading"];
    success [label="Success", shape=doublecircle];
    error [label="Error"];

    // Transitions
    start -> idle;
    idle -> loading [label="fetch()"];
    loading -> success [label="200 OK"];
    loading -> error [label="error"];
    error -> idle [label="retry()"];
    success -> idle [label="reset()"];
}
```

### Call Graph
```dot
digraph CallGraph {
    rankdir=TB;
    node [shape=box, fontname="Courier"];

    main [style=filled, fillcolor=lightgreen];
    main -> init;
    main -> process;
    main -> cleanup;

    init -> loadConfig;
    init -> connectDB;

    process -> validateInput;
    process -> transform;
    process -> save;

    transform -> normalize;
    transform -> enrich;

    save -> connectDB [style=dashed, label="reuse"];
}
```

### Network Topology
```dot
graph Network {
    layout=neato;
    overlap=false;
    node [shape=box];

    // Nodes
    internet [shape=cloud, label="Internet"];
    firewall [shape=box3d, label="Firewall"];
    lb [label="Load
Balancer"];
    web1 [label="Web 1"];
    web2 [label="Web 2"];
    app1 [label="App 1"];
    app2 [label="App 2"];
    db [shape=cylinder, label="Database"];

    // Connections
    internet -- firewall;
    firewall -- lb;
    lb -- web1;
    lb -- web2;
    web1 -- app1;
    web1 -- app2;
    web2 -- app1;
    web2 -- app2;
    app1 -- db;
    app2 -- db;
}
```

### Entity Relationship
```dot
digraph ERD {
    rankdir=LR;
    node [shape=record, fontname="Helvetica"];
    edge [arrowhead=none];

    user [label="<pk> User|id: PK\lname: string\lemail: string\l"];
    order [label="<pk> Order|id: PK\luser_id: FK\ltotal: decimal\l"];
    item [label="<pk> OrderItem|id: PK\lorder_id: FK\lproduct_id: FK\l"];
    product [label="<pk> Product|id: PK\lname: string\lprice: decimal\l"];

    user:pk -> order:pk [label="1:N", arrowhead=crow];
    order:pk -> item:pk [label="1:N", arrowhead=crow];
    product:pk -> item:pk [label="1:N", arrowhead=crow];
}
```

### Flowchart
```dot
digraph Flowchart {
    rankdir=TB;
    node [fontname="Helvetica"];

    start [shape=ellipse, label="Start", style=filled, fillcolor=lightgreen];
    input [shape=parallelogram, label="Get Input"];
    validate [shape=diamond, label="Valid?"];
    process [shape=box, label="Process Data"];
    error [shape=box, label="Show Error", style=filled, fillcolor=lightyellow];
    output [shape=parallelogram, label="Output Result"];
    end [shape=ellipse, label="End", style=filled, fillcolor=lightcoral];

    start -> input;
    input -> validate;
    validate -> process [label="Yes"];
    validate -> error [label="No"];
    error -> input;
    process -> output;
    output -> end;
}
```

## Integration with Publishers

### Obsidian Integration
```python
def publish_graphviz_to_obsidian(
    vault_path: str,
    folder: str,
    filename: str,
    diagram_name: str,
    dot_source: str
):
    """Publish Graphviz diagram to Obsidian with source and image."""
    from pathlib import Path

    vault = Path(vault_path)
    target_dir = vault / folder
    attachments_dir = vault / "attachments"

    target_dir.mkdir(parents=True, exist_ok=True)
    attachments_dir.mkdir(parents=True, exist_ok=True)

    # Render image
    image_name = f"{filename}-diagram.png"
    image_path = attachments_dir / image_name
    render_graphviz(dot_source, image_path.with_suffix(""), "png")

    # Create markdown with both source and image
    content = f"""# {diagram_name}

## Source

```dot
{dot_source}
```

## Rendered

![[{image_name}]]
"""

    note_path = target_dir / f"{filename}.md"
    note_path.write_text(content)
```

### Joplin Integration
```python
def publish_graphviz_to_joplin(
    notebook: str,
    title: str,
    diagram_name: str,
    dot_source: str
):
    """Publish Graphviz diagram to Joplin with source and image."""
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Render image
        image_path = tmpdir / "diagram.png"
        render_graphviz(dot_source, image_path.with_suffix(""), "png")

        # Create markdown
        content = f"""# {diagram_name}

## Source

```dot
{dot_source}
```

## Rendered

![{diagram_name}](./diagram.png)
"""

        md_path = tmpdir / f"{title}.md"
        md_path.write_text(content)

        # Import to Joplin (imports markdown and referenced images)
        subprocess.run([
            "joplin", "import", str(tmpdir),
            "--notebook", notebook
        ], check=True)
```

## Graphviz vs Mermaid

| Feature | Graphviz | Mermaid |
|---------|----------|---------|
| **Layout control** | Precise, many engines | Automatic only |
| **Complexity** | Handles very large graphs | Better for simpler diagrams |
| **Rendering** | External tool required | Browser-native |
| **Styling** | Extensive options | Limited but sufficient |
| **Learning curve** | Steeper | Easier |
| **Use case** | Complex dependencies, call graphs | Quick diagrams, sequences |

**Use Graphviz when:**
- You need precise layout control
- Graph is large or complex
- You need specific node arrangements
- Creating dependency or call graphs

**Use Mermaid when:**
- Quick inline diagrams
- Sequence diagrams
- Simple flowcharts
- Native browser rendering preferred

## Prerequisites

### Install Graphviz
```bash
# macOS
brew install graphviz

# Ubuntu/Debian
sudo apt-get install graphviz

# Windows (chocolatey)
choco install graphviz

# Verify installation
dot -V
```

## Checklist

Before creating Graphviz diagrams:
- [ ] Graphviz installed (`dot -V`)
- [ ] Output directory writable
- [ ] DOT syntax validated
- [ ] Appropriate layout engine selected
- [ ] Both source and image included in output
- [ ] Image path correct for target (Obsidian/Joplin)
