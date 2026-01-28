---
name: skill-seekers
description: Generate LLM skills from documentation, codebases, and GitHub repositories
category: skill-management
tags: [skill-generation, codebase-analysis, documentation, automation]
---

# Skill Seekers

## Prerequisites

```bash
pip install skill-seekers
# Or: uv pip install skill-seekers
```

## Commands

| Source | Command |
|--------|---------|
| Local code | `skill-seekers-codebase --directory ./path` |
| Docs URL | `skill-seekers scrape --url https://...` |
| GitHub | `skill-seekers github --repo owner/repo` |
| PDF | `skill-seekers pdf --file doc.pdf` |

## Quick Start

```bash
# Analyze local codebase
skill-seekers-codebase --directory /path/to/project --output output/my-skill/

# Package for Claude
yes | skill-seekers package output/my-skill/ --no-open
```

## Options

| Flag | Description |
|------|-------------|
| `--depth surface/deep/full` | Analysis depth |
| `--skip-patterns` | Skip pattern detection |
| `--skip-test-examples` | Skip test extraction |
| `--ai-mode none/api/local` | AI enhancement |

---

# Skill_Seekers Codebase

## Description

Local codebase analysis and documentation generated from code analysis.

**Path:** `/home/lyh/Documents/Skill_Seekers`
**Files Analyzed:** 140
**Languages:** Python
**Analysis Depth:** deep

## When to Use This Skill

Use this skill when you need to:
- Understand the codebase architecture and design patterns
- Find implementation examples and usage patterns
- Review API documentation extracted from code
- Check configuration patterns and best practices
- Explore test examples and real-world usage
- Navigate the codebase structure efficiently

## ⚡ Quick Reference

### Codebase Statistics

**Languages:**
- **Python**: 140 files (100.0%)

**Analysis Performed:**
- ✅ API Reference (C2.5)
- ✅ Dependency Graph (C2.6)
- ✅ Design Patterns (C3.1)
- ✅ Test Examples (C3.2)
- ✅ Configuration Patterns (C3.4)
- ✅ Architectural Analysis (C3.7)

### 🎨 Design Patterns Detected

*From C3.1 codebase analysis (confidence > 0.7)*

- **Factory**: 44 instances
- **Strategy**: 28 instances
- **Observer**: 8 instances
- **Builder**: 6 instances
- **Command**: 3 instances

*Total: 90 high-confidence patterns*

*See `references/patterns/` for complete pattern analysis*

## 📝 Code Examples

*High-quality examples extracted from test files (C3.2)*

**Workflow: test full join multigraph** (complexity: 1.00)

```python
G = nx.MultiGraph()
G.add_node(0)
G.add_edge(1, 2)
H = nx.MultiGraph()
H.add_edge(3, 4)
U = nx.full_join(G, H)
assert set(U) == set(G) | set(H)
assert len(U) == len(G) + len(H)
assert len(U.edges()) == len(G.edges()) + len(H.edges()) + len(G) * len(H)
U = nx.full_join(G, H, rename=('g', 'h'))
assert set(U) == {'g0', 'g1', 'g2', 'h3', 'h4'}
assert len(U) == len(G) + len(H)
assert len(U.edges()) == len(G.edges()) + len(H.edges()) + len(G) * len(H)
G = nx.MultiDiGraph()
G.add_node(0)
G.add_edge(1, 2)
H = nx.MultiDiGraph()
H.add_edge(3, 4)
U = nx.full_join(G, H)
assert set(U) == set(G) | set(H)
assert len(U) == len(G) + len(H)
assert len(U.edges()) == len(G.edges()) + len(H.edges()) + len(G) * len(H) * 2
U = nx.full_join(G, H, rename=('g', 'h'))
assert set(U) == {'g0', 'g1', 'g2', 'h3', 'h4'}
assert len(U) == len(G) + len(H)
assert len(U.edges()) == len(G.edges()) + len(H.edges()) + len(G) * len(H) * 2
```

**Instantiate DataFrame: See gh-7407** (complexity: 1.00)

```python
df = pd.DataFrame([[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0]], index=[1010001, 2, 1, 1010002], columns=[1010001, 2, 1, 1010002])
```

**test edge removal** (complexity: 1.00)

```python
embedding_expected.set_data({1: [2, 7], 2: [1, 3, 4, 5], 3: [2, 4], 4: [3, 6, 2], 5: [7, 2], 6: [4, 7], 7: [6, 1, 5]})
assert nx.utils.graphs_equal(embedding, embedding_expected)
```

**Instantiate Graph: test graph1** (complexity: 1.00)

```python
G = nx.Graph([(3, 10), (2, 13), (1, 13), (7, 11), (0, 8), (8, 13), (0, 2), (0, 7), (0, 10), (1, 7)])
```

**Instantiate Graph: test graph2** (complexity: 1.00)

```python
G = nx.Graph([(1, 2), (4, 13), (0, 13), (4, 5), (7, 10), (1, 7), (0, 3), (2, 6), (5, 6), (7, 13), (4, 8), (0, 8), (0, 9), (2, 13), (6, 7), (3, 6), (2, 8)])
```

**Configuration example: test davis birank** (complexity: 1.00)

```python
answer = {'Laura Mandeville': 0.07, 'Olivia Carleton': 0.04, 'Frances Anderson': 0.05, 'Pearl Oglethorpe': 0.04, 'Katherina Rogers': 0.06, 'Flora Price': 0.04, 'Dorothy Murchison': 0.04, 'Helen Lloyd': 0.06, 'Theresa Anderson': 0.07, 'Eleanor Nye': 0.05, 'Evelyn Jefferson': 0.07, 'Sylvia Avondale': 0.07, 'Charlotte McDowd': 0.05, 'Verne Sanderson': 0.05, 'Myra Liddel': 0.05, 'Brenda Rogers': 0.07, 'Ruth DeSand': 0.05, 'Nora Fayette': 0.07, 'E8': 0.11, 'E7': 0.09, 'E10': 0.07, 'E9': 0.1, 'E13': 0.05, 'E3': 0.07, 'E12': 0.07, 'E11': 0.06, 'E2': 0.05, 'E5': 0.08, 'E6': 0.08, 'E14': 0.05, 'E4': 0.06, 'E1': 0.05}
```

**Configuration example: test davis birank with personalization** (complexity: 1.00)

```python
answer = {'Laura Mandeville': 0.29, 'Olivia Carleton': 0.02, 'Frances Anderson': 0.06, 'Pearl Oglethorpe': 0.04, 'Katherina Rogers': 0.04, 'Flora Price': 0.02, 'Dorothy Murchison': 0.03, 'Helen Lloyd': 0.04, 'Theresa Anderson': 0.08, 'Eleanor Nye': 0.05, 'Evelyn Jefferson': 0.09, 'Sylvia Avondale': 0.05, 'Charlotte McDowd': 0.06, 'Verne Sanderson': 0.04, 'Myra Liddel': 0.03, 'Brenda Rogers': 0.08, 'Ruth DeSand': 0.05, 'Nora Fayette': 0.05, 'E8': 0.11, 'E7': 0.1, 'E10': 0.04, 'E9': 0.07, 'E13': 0.03, 'E3': 0.11, 'E12': 0.04, 'E11': 0.03, 'E2': 0.1, 'E5': 0.11, 'E6': 0.1, 'E14': 0.03, 'E4': 0.06, 'E1': 0.1}
```

**test junction tree directed confounders** (complexity: 1.00)

```python
J.add_edges_from([(('C', 'E'), ('C',)), (('C',), ('A', 'B', 'C')), (('A', 'B', 'C'), ('C',)), (('C',), ('C', 'D'))])
assert nx.is_isomorphic(G, J)
```

**test junction tree directed cascade** (complexity: 1.00)

```python
J.add_edges_from([(('A', 'B'), ('B',)), (('B',), ('B', 'C')), (('B', 'C'), ('C',)), (('C',), ('C', 'D'))])
assert nx.is_isomorphic(G, J)
```

**test junction tree undirected** (complexity: 1.00)

```python
J.add_edges_from([(('A', 'D'), ('A',)), (('A',), ('A', 'C')), (('A', 'C'), ('C',)), (('C',), ('B', 'C')), (('B', 'C'), ('C',)), (('C',), ('C', 'E'))])
assert nx.is_isomorphic(G, J)
```

*See `references/test_examples/` for all extracted examples*

## ⚙️ Configuration Patterns

*From C3.4 configuration analysis*

**Configuration Files Analyzed:** 23
**Total Settings:** 165
**Patterns Detected:** 0

**Configuration Types:**
- unknown: 23 files

*See `references/config_patterns/` for detailed configuration analysis*

## 📚 Available References

This skill includes detailed reference documentation:

- **API Reference**: `references/api_reference/` - Complete API documentation
- **Dependencies**: `references/dependencies/` - Dependency graph and analysis
- **Patterns**: `references/patterns/` - Detected design patterns
- **Examples**: `references/test_examples/` - Usage examples from tests
- **Configuration**: `references/config_patterns/` - Configuration patterns

---

**Generated by Skill Seeker** | Codebase Analyzer with C3.x Analysis
