---
name: pymol
description: Control PyMOL molecular visualization through Claude Code. Use when asked to "visualize protein", "render structure", "show cartoon", "color by chain", "ray trace", "set up pymol", "install pymol", or work with molecular graphics. Handles setup, visualization commands, and publication-quality figure generation.
---

# PyMOL: Molecular Visualization via claudemol

## Summary

This skill enables Claude Code to control PyMOL molecular visualization software through the claudemol socket interface. It supports:

- **Setup**: Cross-platform installation of claudemol and PyMOL
- **Visualization**: Rendering proteins, small molecules, and complexes
- **Publication figures**: Ray-traced high-resolution images
- **Interactive control**: Send PyMOL commands programmatically

## Applicable Scenarios

| Task Category | Examples |
|---------------|----------|
| Setup | Install PyMOL, configure claudemol, verify connection |
| Structure Loading | Load PDB files, fetch from RCSB, open local structures |
| Representations | Cartoon, surface, sticks, spheres, ribbons, lines |
| Coloring | Color by chain, spectrum, B-factor, custom colors |
| Selections | Select residues, chains, ligands, binding sites |
| Camera | Orient view, zoom, rotate, save viewpoints |
| Ray Tracing | High-quality renders, publication figures |
| Export | Save images (PNG), sessions (PSE), movies |

## Setup Instructions

### Quick Setup (All Platforms)

Run the automated setup script:

```bash
python /path/to/skills/pymol/scripts/setup_pymol.py
```

### Manual Setup

#### 1. Install claudemol

```bash
pip install claudemol
```

#### 2. Install PyMOL

**macOS (Recommended):**
```bash
brew install pymol
```

**Windows/Linux (Headless):**
```bash
pip install pymol-open-source
```

**Windows (Licensed PyMOL):**
Connect to existing PyMOL installation - see `references/troubleshooting.md`

#### 3. Configure PyMOL

```bash
claudemol setup
```

This adds the socket plugin to PyMOL's startup.

#### 4. Launch and Verify

1. Start PyMOL normally
2. Check that port 9880 is listening:
   ```bash
   lsof -i :9880  # macOS/Linux
   netstat -an | findstr 9880  # Windows
   ```

## Socket Communication

claudemol communicates with PyMOL via a TCP socket on port 9880.

### Basic Pattern

```python
import socket
import json

def send_pymol_command(code: str, host: str = 'localhost', port: int = 9880) -> dict:
    """Send a command to PyMOL via claudemol socket."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(30)
    try:
        sock.connect((host, port))
        message = json.dumps({"code": code})
        sock.sendall(message.encode('utf-8'))
        response = sock.recv(65536)
        return json.loads(response.decode('utf-8'))
    finally:
        sock.close()
```

### Multi-Command Example

```python
commands = """
cmd.load('1ubq.pdb')
cmd.show('cartoon')
cmd.color('cyan', 'all')
cmd.orient()
"""
result = send_pymol_command(commands)
```

## Quick Reference

### Loading Structures

```python
# From local file
cmd.load('/path/to/structure.pdb')
cmd.load('/path/to/structure.cif')

# From RCSB PDB
cmd.fetch('1ubq')
cmd.fetch('6lu7', type='cif')
```

### Representations

```python
# Show representations
cmd.show('cartoon', 'all')
cmd.show('surface', 'chain A')
cmd.show('sticks', 'resn LIG')
cmd.show('spheres', 'name CA')

# Hide representations
cmd.hide('lines', 'all')
cmd.hide('everything', 'solvent')
```

### Coloring

```python
# Color by chain (automatic colors)
cmd.util.cbc()

# Spectrum coloring (rainbow N to C)
cmd.spectrum('count', 'rainbow', 'all')

# Specific colors
cmd.color('red', 'chain A')
cmd.color('blue', 'resn LIG')
cmd.color('green', 'resi 50-100')

# B-factor coloring
cmd.spectrum('b', 'blue_white_red', 'all')
```

### Selections

```python
# Create named selections
cmd.select('binding_site', 'byres resn LIG around 5')
cmd.select('active_site', 'resi 145+41+166 and chain A')
cmd.select('interface', 'chain A within 4 of chain B')

# Selection algebra
cmd.select('no_water', 'all and not solvent')
```

### View and Camera

```python
# Orient and zoom
cmd.orient()
cmd.zoom('all')
cmd.zoom('chain A', buffer=5)
cmd.center('resn LIG')

# Set specific view
cmd.set_view([...])  # 18-element matrix

# Store and recall views
cmd.view('view1', 'store')
cmd.view('view1', 'recall')
```

### Ray Tracing and Export

```python
# Basic ray trace
cmd.ray(1920, 1080)
cmd.png('/path/to/output.png')

# Publication quality
cmd.set('ray_trace_mode', 1)
cmd.set('ray_shadows', 'on')
cmd.set('antialias', 2)
cmd.ray(2400, 2400)
cmd.png('/path/to/figure.png', dpi=300)
```

## Visualization Workflows

See `references/visualization.md` for complete workflows:

- Basic protein visualization
- Cartoon with chain coloring
- Surface with transparency
- Ligand binding site
- Domain highlighting
- Publication-quality figures

## Command Reference

See `references/commands.md` for complete command documentation:

- All `cmd.*` functions
- Selection syntax
- Setting parameters
- Color palettes

## Troubleshooting

See `references/troubleshooting.md` for platform-specific issues:

- macOS GLUT errors
- Windows headless mode
- Connection refused errors
- Display problems

## Common Issues

| Issue | Resolution |
|-------|------------|
| Connection refused | Ensure PyMOL is running with claudemol plugin loaded |
| Port 9880 in use | Kill other processes or change port |
| No GUI (Windows pip) | Use headless mode or licensed PyMOL |
| GLUT missing (macOS) | Install via Homebrew instead of pip |
| Slow ray tracing | Reduce resolution or simplify scene |

## External Resources

- PyMOL Documentation: https://pymol.org/dokuwiki/
- PyMOL Wiki: https://pymolwiki.org/
- claudemol GitHub: https://github.com/colorifix/claudemol
- Open-Source PyMOL: https://github.com/schrodinger/pymol-open-source
