---
name: networkx
description: Use when "NetworkX", "graph analysis", "network analysis", "graph algorithms", "shortest path", "centrality", "PageRank", "community detection", "social network", "knowledge graph"
version: 1.0.0
---

# NetworkX Graph Analysis

Python library for creating, analyzing, and visualizing networks and graphs.

## When to Use

- Social network analysis
- Knowledge graphs and ontologies
- Shortest path problems
- Community detection
- Citation/reference networks
- Biological networks (protein interactions)

---

## Graph Types

| Type | Edges | Multiple Edges |
|------|-------|----------------|
| `Graph` | Undirected | No |
| `DiGraph` | Directed | No |
| `MultiGraph` | Undirected | Yes |
| `MultiDiGraph` | Directed | Yes |

---

## Key Algorithms

### Centrality Measures

| Measure | What It Finds | Use Case |
|---------|---------------|----------|
| **Degree** | Most connections | Popular nodes |
| **Betweenness** | Bridge nodes | Information flow |
| **Closeness** | Fastest reach | Efficient spreaders |
| **PageRank** | Importance | Web pages, citations |
| **Eigenvector** | Influential connections | Who knows important people |

### Path Algorithms

| Algorithm | Purpose |
|-----------|---------|
| **Shortest path** | Minimum hops |
| **Weighted shortest** | Minimum cost |
| **All pairs shortest** | Full distance matrix |
| **Dijkstra** | Efficient weighted paths |

### Community Detection

| Method | Approach |
|--------|----------|
| **Louvain** | Modularity optimization |
| **Greedy modularity** | Hierarchical merging |
| **Label propagation** | Fast, scalable |

---

## Graph Generators

| Generator | Model |
|-----------|-------|
| **Erdős-Rényi** | Random edges |
| **Barabási-Albert** | Preferential attachment (scale-free) |
| **Watts-Strogatz** | Small-world |
| **Complete** | All connected |

---

## Layout Algorithms

| Layout | Best For |
|--------|----------|
| **Spring** | General purpose |
| **Circular** | Regular structure |
| **Kamada-Kawai** | Aesthetics |
| **Spectral** | Clustered graphs |

---

## I/O Formats

| Format | Preserves Attributes | Human Readable |
|--------|---------------------|----------------|
| **GraphML** | Yes | Yes (XML) |
| **Edge list** | No | Yes |
| **JSON** | Yes | Yes |
| **Pandas** | Yes | Via DataFrame |

---

## Performance Considerations

| Scale | Approach |
|-------|----------|
| < 10K nodes | Any algorithm |
| 10K - 100K | Use approximate algorithms |
| > 100K | Consider graph-tool or igraph |

**Key concept**: NetworkX is pure Python - great for prototyping, may need alternatives for production scale.

---

## Best Practices

- Set random seeds for reproducibility
- Choose correct graph type upfront
- Use pandas integration for data exchange
- Consider memory for large graphs

## Resources

- NetworkX docs: <https://networkx.org/documentation/latest/>
- Tutorial: <https://networkx.org/documentation/latest/tutorial.html>
