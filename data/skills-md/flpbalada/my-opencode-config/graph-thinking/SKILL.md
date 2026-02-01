---
name: graph-thinking
description:
  Apply graph-based thinking to visualize complex relationships and solve
  problems non-linearly. Use when mapping dependencies, analyzing systems,
  exploring interconnected concepts, or designing architectures.
---

# Graph Thinking - Non-Linear Problem Solving

Mental model for visualizing complex relationships and connections between
ideas, concepts, or data points. Evolved from Graph-of-Thought (GoT) reasoning
that mirrors human cognition.

## When to Use This Skill

- Mapping feature dependencies in product development
- Analyzing stakeholder relationships
- Understanding system architectures
- Exploring interconnected concepts
- Designing recommendation systems or knowledge graphs
- Identifying opportunity areas through network analysis

## Core Concepts

### Graph Elements

| Element        | Description                                |
| -------------- | ------------------------------------------ |
| **Nodes**      | Individual elements or concepts            |
| **Edges**      | Relationships or connections between nodes |
| **Clusters**   | Groups of highly connected nodes           |
| **Pathways**   | Routes through the network                 |
| **Centrality** | Measures identifying most important nodes  |
| **Topology**   | Structural arrangement of connections      |

### Graph-of-Thought (GoT) Reasoning

```
Traditional (Chain-of-Thought):
A → B → C → D → Conclusion

Graph-of-Thought:
    ┌─── B ───┐
    │         │
A ──┼─── C ───┼──→ Synthesis → Conclusion
    │         │
    └─── D ───┘
         ↑
    Feedback Loop
```

GoT enables:

- Combining arbitrary thoughts into synergistic outcomes
- Distilling networks of thoughts for clarity
- Enhancing ideas using feedback loops
- Non-linear exploration of solution spaces

## Fundamental Principles

### First Principles Thinking

Break down complex problems into fundamental truths:

```
Surface Level:
"We need more marketing"
    ↓
Why?
    ↓
"Not enough customers"
    ↓
Why?
    ↓
Root Truth:
"Value proposition unclear to target audience"
```

### Second-Order Thinking

Demand deeper analysis by asking "And then what?":

```
Decision: Reduce prices by 20%

First-order:  More sales
Second-order: Lower margins → Less R&D budget
Third-order:  Competitors catch up → Price war
Fourth-order: Race to bottom → Industry commoditization
```

### Non-Linear Processing

Unlike sequential thinking:

| Sequential              | Graph-Based                               |
| ----------------------- | ----------------------------------------- |
| One path at a time      | Multiple paths simultaneously             |
| Linear information flow | Multi-directional exploration             |
| Fixed order             | Iterative refinement through loops        |
| Single conclusion       | Synthesized insights from multiple angles |

## Analysis Framework

### Double Diamond Model

Apply divergent and convergent thinking cycles:

```
    DISCOVER          DEFINE          DEVELOP          DELIVER
   (Diverge)        (Converge)       (Diverge)       (Converge)
       /\              \/              /\              \/
      /  \            /  \            /  \            /  \
     /    \          /    \          /    \          /    \
    /      \        /      \        /      \        /      \
   /        \      /        \      /        \      /        \

   Explore         Focus on         Generate         Focus on
   problem         specific         diverse          optimal
   space           challenges       solutions        implementation
```

### Step 1: Map the Nodes

Identify all relevant elements:

```
Product Launch Analysis:

Nodes:
├── Stakeholders
│   ├── Customers
│   ├── Engineering
│   ├── Marketing
│   └── Leadership
├── Features
│   ├── Core functionality
│   ├── Nice-to-haves
│   └── Technical debt
├── Constraints
│   ├── Timeline
│   ├── Budget
│   └── Resources
└── Dependencies
    ├── External APIs
    ├── Infrastructure
    └── Regulatory
```

### Step 2: Define Relationships (Edges)

Document connections between nodes:

```
Edge Types:
├── Dependency:    A requires B
├── Influence:     A affects B
├── Correlation:   A and B move together
├── Conflict:      A competes with B
└── Synergy:       A enhances B
```

### Step 3: Identify Clusters and Patterns

Find highly connected groups:

```
High Centrality (Critical Nodes):
├── Authentication service → 12 dependencies
├── Database layer → 8 dependencies
└── API gateway → 6 dependencies

Clusters:
├── User-facing features (tightly coupled)
├── Backend services (loosely coupled)
└── Third-party integrations (isolated)
```

### Step 4: Analyze Pathways

Trace routes through the network:

```
User Journey Graph:

Landing Page
    ↓
[Sign Up] ←→ [Social Login]
    ↓
Onboarding
    ↓           ↓
Quick Start   Full Setup
    ↓           ↓
    └─────┬─────┘
          ↓
    First Value
          ↓
    ↙    ↓    ↘
Churn  Retain  Upgrade
```

## Output Template

After completing analysis, document as:

```markdown
## Graph Thinking Analysis

**Subject:** [What you're analyzing]

**Analysis Date:** [Date]

### Node Map

| Category | Nodes   | Centrality     |
| -------- | ------- | -------------- |
| [Cat 1]  | [Nodes] | [High/Med/Low] |
| [Cat 2]  | [Nodes] | [High/Med/Low] |

### Relationship Matrix

| From | To  | Relationship | Strength |
| ---- | --- | ------------ | -------- |
| [A]  | [B] | [Type]       | [1-5]    |

### Key Insights

1. **Clusters identified:** [Description]
2. **Critical paths:** [Description]
3. **Bottlenecks:** [Description]
4. **Opportunities:** [Description]

### Recommendations

| Priority | Action   | Rationale |
| -------- | -------- | --------- |
| High     | [Action] | [Why]     |
| Medium   | [Action] | [Why]     |
```

## Application Examples

### Feature Dependency Mapping

```
Feature: Real-time Collaboration

Dependencies:
├── WebSocket infrastructure
│   ├── Connection management
│   └── Message queuing
├── Conflict resolution
│   ├── Operational transforms
│   └── CRDT implementation
├── Presence indicators
│   └── User state sync
└── Permissions
    ├── Document access
    └── Cursor visibility
```

### Stakeholder Analysis

```
                    HIGH INFLUENCE
                          │
    Keep Satisfied        │        Manage Closely
    ┌─────────────────────┼─────────────────────┐
    │                     │                     │
    │   Executives        │    Product Owner    │
    │   Compliance        │    Key Customers    │
    │                     │                     │
LOW ──────────────────────┼────────────────────── HIGH
INTEREST                  │                      INTEREST
    │                     │                     │
    │   General Users     │    Power Users      │
    │   IT Support        │    Dev Team         │
    │                     │                     │
    └─────────────────────┼─────────────────────┘
    Monitor               │        Keep Informed
                          │
                   LOW INFLUENCE
```

### System Architecture Analysis

```
Microservice Graph:

API Gateway [Centrality: 0.95]
    │
    ├── Auth Service [0.82]
    │   └── User DB
    │
    ├── Product Service [0.71]
    │   ├── Catalog DB
    │   └── Search Index
    │
    ├── Order Service [0.68]
    │   ├── Order DB
    │   └── Payment Gateway (external)
    │
    └── Notification Service [0.45]
        └── Email Provider (external)

Critical Path: Gateway → Auth → Product → Order
Bottleneck: Auth Service (single point of failure)
```

## Best Practices

### Do

- **Visualize relationships** - Draw the graph, don't just describe it
- **Iterate continuously** - Graphs evolve as understanding deepens
- **Measure centrality** - Identify the most critical nodes
- **Look for clusters** - Natural groupings reveal system structure
- **Trace pathways** - Understand how information/value flows

### Avoid

- **Over-connecting** - Not everything relates to everything
- **Ignoring edge types** - Different relationships have different meanings
- **Static thinking** - Graphs change over time
- **Missing feedback loops** - Circular dependencies are significant
- **Forgetting weights** - Some relationships are stronger than others

## Integration with Other Methods

| Method              | Combined Use                                   |
| ------------------- | ---------------------------------------------- |
| **Five Whys**       | Trace causal chains through the graph          |
| **Business Canvas** | Map relationships between canvas elements      |
| **Jobs-to-be-Done** | Connect user needs to feature nodes            |
| **Hypothesis Tree** | Structure experiments as branching graphs      |
| **Stakeholder Map** | Visualize influence and interest relationships |

## Tools

### Visualization

- **Mermaid** - Code-based diagrams in markdown
- **Graphviz** - Programmatic graph generation
- **Excalidraw** - Hand-drawn style diagrams
- **Miro/FigJam** - Collaborative whiteboarding

### Analysis

- **Gephi** - Network analysis and visualization
- **Neo4j** - Graph database for complex queries
- **NetworkX** - Python library for graph algorithms

## Resources

- [Graph of Thoughts: ArXiv Paper](https://arxiv.org/abs/2308.09687)
- [Neo4j Graph Database Use Cases](https://neo4j.com/use-cases/)
- [Network Science by Albert-László Barabási](http://networksciencebook.com/)
