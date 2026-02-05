---
name: dag-ooda-problem-solving
description: Uses NetworkX DAGs and OODA loops to derive the best course of action for fixing or solving new problems. Use when the user faces a new bug, feature, or decision and wants a structured plan, dependency-ordered tasks, or a repeatable problem-solving workflow.
---

# DAG + OODA Problem-Solving

Combines **OODA** (Observe, Orient, Decide, Act) with **DAGs** (Directed Acyclic Graphs) so the agent can model a problem as a dependency graph and choose an optimal execution order.

## Quick Start

1. **Observe**: List all known tasks, fixes, or sub-problems (these become **nodes**).
2. **Orient**: Identify dependencies (A must be done before B) and build a **DAG** with NetworkX.
3. **Decide**: Run a topological sort for a valid order; optionally weight nodes to pick the best first action or critical path.
4. **Act**: Execute in chosen order; after each step, re-Observe and update the DAG if the situation changed.

**Always try to run** the NetworkX helper script (`scripts/ooda_dag.py`) with the DAG’s nodes and edges so order, sources, longest path, and recommended first action are computed and reproducible.

## OODA Loop (Boyd)

- **Observe**: Gather data—symptoms, logs, constraints, requirements.
- **Orient**: Filter and interpret; this is the decisive phase. Form a mental model (here: the DAG).
- **Decide**: Choose a course of action (here: next node or sequence from the DAG).
- **Act**: Execute; then loop back to Observe.

Never skip Orient: a good DAG prevents wasted effort and wrong order.

## DAG Model

- **Nodes**: Discrete tasks, fixes, hypotheses, or sub-problems.
- **Edges**: Dependencies. Edge `A → B` means "A must be done before B."
- **Acyclic**: No cycles. If you find a cycle, break it by merging nodes or redefining dependencies.
- **Topological order**: Any linear order that respects edges; use it as execution order.
- **Sources**: Nodes with no incoming edges (in-degree 0); candidate first actions.
- **Sinks**: Nodes with no outgoing edges (out-degree 0); terminal outcomes or final deliverables.
- **Layers** (optional): Topological generations—layer 0 = sources, then nodes whose predecessors are done; nodes in the same layer can run in parallel.
- **Critical path** (optional): Longest path in the DAG; identifies bottlenecks and highest-impact sequence.

## AND-OR Trees (optional)

The DAG can represent **AND-OR** semantics so some nodes are satisfied when **any** predecessor is done (OR) instead of **all** (AND).

- **AND node** (default): Node is **ready** when **all** predecessors are done. Same as standard DAG dependency.
- **OR node**: Node is **ready** when **at least one** predecessor is done. Use for alternative ways to achieve the same goal (e.g. "fix by patching config OR by upgrading dependency").

**When to use OR**: When multiple paths lead to the same outcome and completing one path is enough—e.g. "unblock deploy" can be done by "fix auth" OR "bypass auth in dev." Use AND (default) when the node truly requires every predecessor.

**In JSON**: Add optional `node_types` keyed by node id: `"and"` or `"or"`. Omitted nodes default to `"and"`.

**Helper script** (when using AND/OR):
- Outputs **NODE_TYPES** (each node and its type).
- **READY_INITIAL**: Nodes ready with no nodes done (same as sources when all nodes are AND).
- When optional `"done": ["id1", "id2"]` is in the JSON:
  - **READY_NOW**: Nodes that are ready *now* under AND/OR rules (excluding already-done nodes). Re-run after each Act with updated `done` to get the next candidate set.
  - **RECOMMENDED_NEXT**: Best node from READY_NOW by impact/effort score (same as RECOMMENDED_FIRST logic applied to ready set).
  - **GOAL_REACHED**: `yes` if all sinks are *satisfied* (in done or reachable under AND/OR from done); `no` otherwise. With OR sinks, the goal can be reached without executing every node.

**Example** (OR node `deploy` is ready when either `fix-auth` or `add-retry` is done):

```json
{"nodes": ["fix-auth", "add-retry", "deploy"], "edges": [["fix-auth", "deploy"], ["add-retry", "deploy"]], "node_types": {"deploy": "or"}}
```

## Combined Workflow

Copy this checklist and track progress:

```
Task Progress:
- [ ] Observe: List nodes (tasks/fixes/sub-problems)
- [ ] Orient: Add edges (dependencies), build DAG, validate acyclic
- [ ] Decide: Topological sort; optionally score nodes (impact/effort) and pick first action
- [ ] Act: Execute next step; re-Observe and update DAG if needed
```

**Observe**  
Enumerate everything that might need to be done. One node per atomic task or fix. Name nodes clearly (e.g. "fix auth token expiry", "add retry for API call").

**Orient**  
For each pair (A, B): if A must complete before B, add edge A → B. Build the graph in NetworkX. Run `nx.is_directed_acyclic_graph(G)`; if False, remove or rewire edges until acyclic.

**Decide**  
- **Default**: Use `list(nx.topological_sort(G))` as the execution order.  
- **Best first action**: If you need a single “next step,” pick a node with no incoming edges (sources). If multiple sources, rank by impact/effort and choose one.  
- **Critical path**: Use `nx.dag_longest_path(G)` (or weight edges and use longest path) to find the highest-impact chain; prioritize nodes on that path when deciding order.

**Act**  
Execute the chosen node (fix, task, or experiment). After each step, re-Observe (new logs, new symptoms, new requirements) and update the DAG—add/remove nodes or edges—then re-Orient and Decide again.

## NetworkX Powers

When using this skill, the agent can rely on NetworkX to:

| Power | API / approach | Use when |
|-------|----------------|----------|
| **Build DAG** | `nx.DiGraph()`, `add_nodes_from()`, `add_edges_from()` | Modeling tasks and dependencies. |
| **Validate acyclic** | `nx.is_directed_acyclic_graph(G)` | Before any sort or path; break cycles if False. |
| **Execution order** | `list(nx.topological_sort(G))` | Decide the order to execute nodes. |
| **First actions** | `[n for n in G.nodes() if G.in_degree(n) == 0]` | Pick candidate “next step” (sources). |
| **Sinks** | `[n for n in G.nodes() if G.out_degree(n) == 0]` | Identify terminal outcomes or final deliverables. |
| **Layers** | `nx.topological_generations(G)` | Group nodes by wave; same-layer nodes can run in parallel. |
| **Critical path** | `nx.dag_longest_path(G)` or with `weight="weight"` | Find longest chain; prioritize those nodes. |
| **In-degree / out-degree** | `G.in_degree(n)`, `G.out_degree(n)` | Inspect prerequisites or dependents. |
| **Predecessors / successors** | `G.predecessors(n)`, `G.successors(n)` | Immediate prerequisites or dependents (one hop). |
| **Reachability** | `nx.has_path(G, u, v)` | Whether u must complete before v (u reaches v). |
| **Ancestors / descendants** | `nx.ancestors(G, n)`, `nx.descendants(G, n)` | See full upstream/downstream for a node. |
| **Subgraph** | `G.subgraph(nodes)` or `nx.subgraph_view()` | Restrict to a subset of nodes. |
| **Weighted DAG** | Set edge or node `weight`; use in `dag_longest_path(G, weight="weight")` | Prioritize by cost or impact along paths. |

**Always try to run the helper script** (`scripts/ooda_dag.py`) so the DAG yields reproducible order, sources, longest path, and recommended first action with impact/effort scoring—even for small graphs.

## NetworkX Snippets

**Create DAG and validate:**

```python
import networkx as nx

G = nx.DiGraph()
# Nodes: task IDs or labels
G.add_nodes_from(["fix-auth", "add-retry", "update-docs", "deploy"])
# Edges: from prerequisite to dependent
G.add_edges_from([
    ("fix-auth", "deploy"),
    ("add-retry", "deploy"),
    ("deploy", "update-docs"),
])
assert nx.is_directed_acyclic_graph(G), "Break cycles before proceeding"
```

**Topological order (execution sequence):**

```python
order = list(nx.topological_sort(G))
# e.g. ["fix-auth", "add-retry", "deploy", "update-docs"]
```

**Sources (nodes with no prerequisites—candidate “first actions”):**

```python
sources = [n for n in G.nodes() if G.in_degree(n) == 0]
```

**Sinks (nodes with no dependents—terminal outcomes):**

```python
sinks = [n for n in G.nodes() if G.out_degree(n) == 0]
```

**Layers (topological generations—for parallel execution):**

```python
# Nodes in the same layer have no dependency on each other; can run in parallel
for layer_idx, layer in enumerate(nx.topological_generations(G)):
    print(f"Layer {layer_idx}: {layer}")
```

**Immediate predecessors or successors (one hop):**

```python
preds = list(G.predecessors(n))   # nodes that must complete before n
succs = list(G.successors(n))    # nodes that depend on n
```

**Reachability (does u block v?):**

```python
nx.has_path(G, u, v)  # True if u must complete before v
```

**Critical path (longest path; unweighted = most steps):**

```python
# Requires networkx >= 2.6
path = nx.dag_longest_path(G)
# Or with weights: nx.dag_longest_path(G, weight="weight")
```

**Weighted nodes (impact/effort) to pick best source:**

Score only source nodes (in_degree 0). Use the standard scoring below; choose the source with highest score as the first action.

## Standard Weights (Knowledge-Based)

Use these scales so prioritization is consistent and interpretable.

**Impact** (1–5): How much doing this node advances the goal.

| Label        | Value | When to use |
|-------------|-------|-------------|
| Blocker / critical | 5 | Must fix or nothing else matters; blocks others. |
| High        | 4 | Core fix or major feature; unblocks or enables a lot. |
| Medium      | 3 | Meaningful improvement; default when unsure. |
| Low         | 2 | Nice-to-have; small win. |
| Nice-to-have | 1 | Optional; minimal effect. |

**Effort** (1–5): Cost to complete (time, complexity, risk).

| Label   | Value | When to use |
|--------|-------|-------------|
| Trivial | 1 | Minutes; no real risk. |
| Small   | 2 | Short task; well-understood. |
| Medium  | 3 | Default when unsure. |
| Large   | 4 | Significant time or complexity. |
| Huge    | 5 | Multi-day or high uncertainty. |

**Priority score** (for choosing among source nodes):

- `score = impact / effort` (prefer: high impact, low effort first).
- If effort is 0, treat as 1 to avoid division by zero.
- **Standard knowledge**: Fix blockers first (impact 5); then high impact / low effort; then fill by dependency order. Among sources with equal score, prefer one on the critical path or break ties arbitrarily.

**Optional in JSON**: `weights` object keyed by node id: `{"node_id": {"impact": 4, "effort": 2}}`. Omitted nodes default to impact 3, effort 3.

## Running Code

**Always try to run Python via the terminal** (prefer the helper script) so DAG results—order, sources, critical path—are real and reproducible.

**Use `uv`** so `networkx` is available without a pre-existing project or venv:

- **Inline one-off**: `uv run --with networkx python -c "import networkx as nx; G = nx.DiGraph(); G.add_edges_from([('a','b'),('b','c')]); print(list(nx.topological_sort(G)))"`
- **Helper script** (recommended for multi-step DAGs): run the skill’s script with JSON input.

**Helper script** `scripts/ooda_dag.py` (relative to this skill’s root):

- **Input**: JSON with `nodes` and `edges`; optional `weights` keyed by node id (see Standard Weights); optional `node_types` keyed by node id (`"and"` or `"or"`, see AND-OR Trees); optional `done` (list of node ids already completed, for AND/OR ready set).
  - Example: `{"nodes": ["fix-auth", "add-retry", "deploy"], "edges": [["fix-auth", "deploy"], ["add-retry", "deploy"]], "weights": {"fix-auth": {"impact": 5, "effort": 2}}, "node_types": {"deploy": "or"}}`
- **Run**: From the skill root (the `dag-ooda-problem-solving` folder containing this SKILL.md—e.g. `~/.cursor/skills/dag-ooda-problem-solving` or `.cursor/skills/dag-ooda-problem-solving`):
  `uv run --with networkx python scripts/ooda_dag.py`  
  then paste JSON and Ctrl-D; or pass a file:  
  `uv run --with networkx python scripts/ooda_dag.py /path/to/dag.json`
- **Output**: `TOPOLOGICAL_ORDER`, then `SOURCES`, then `SINKS`, then `NODE_TYPES`, then `READY_INITIAL`, then when `done` is provided: `READY_NOW`, `RECOMMENDED_NEXT`, `GOAL_REACHED` (yes/no), then `LAYERS`, then `LONGEST_PATH`, then `SOURCE_SCORES`, then `RECOMMENDED_FIRST`. Exit code 1 if the graph has a cycle.

When to run code: after **Orient** (graph built) to validate acyclic and get order/sources/path; or in **Decide** to pick the next action from sources/longest path. **Always try to run the helper script** (`scripts/ooda_dag.py`) rather than one-off snippets; fall back to inline `uv run` only if the script cannot be run.

## Output Format

When proposing a course of action:

1. **Observe**: Short list of nodes (what you’re considering).
2. **Orient**: DAG summary—number of nodes/edges and “acyclic: yes/no.”
3. **Decide**: Ordered list (topological order) and the recommended **next action** (one node, with brief rationale).
4. **Act**: Concrete steps for that next action (code changes, commands, or checks).

Keep the DAG in code or in a short table (e.g. “A → B”) so the user can see dependencies at a glance.

## Anti-Patterns

- **Don’t skip Orient**: Building the DAG is what makes the order reliable.
- **Don’t ignore cycles**: If the graph has a cycle, topological sort is undefined; always validate and break cycles first.
- **Don’t over-granulate**: Nodes should be actionable units; too many tiny nodes make the DAG noisy.
- **Don’t freeze the DAG**: After each Act, re-Observe and update the graph when the problem or context changes.
