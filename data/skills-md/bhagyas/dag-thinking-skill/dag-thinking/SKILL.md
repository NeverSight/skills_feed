---
name: dag-thinking
description: Solve problems by modeling them as a directed acyclic graph (DAG). Use when tasks have dependencies, prerequisites, ordering constraints, pipelines, workflows, causal graphs, or when you need to detect cycles, find a topological order, identify critical paths, or simplify dependency structure.
---

# DAG Thinking (Directed Acyclic Graph)

Use a **directed acyclic graph (DAG)** as the core representation for any problem that involves *dependencies*.
Reference: https://grokipedia.com/page/Directed_acyclic_graph

## 0) Decide if DAG framing fits
Use this when you can phrase the problem as:
- “X must happen **before** Y”
- “Y depends on X”
- “If X changes, downstream things affected are …”

If there are **feedback loops** that matter, you may have cycles; handle them explicitly (see Cycle handling).

## 1) Build the graph
### 1A) Define nodes
Pick a consistent unit:
- tasks, steps, tickets, files, components, decisions, assumptions, people, etc.

### 1B) Define edges
Use one direction consistently:
- **X → Y** means “X is a prerequisite of Y” (Y depends on X)

### 1C) Capture metadata
For each node, store:
- owner, status, estimate/cost, risk, notes

## 2) Validate the DAG
### 2A) Detect cycles (must do)
If cycles exist, you don’t have a DAG yet.

Cycle handling (pick one):
- **Break the cycle** by clarifying dependency direction (often one edge is “nice-to-have”, not required)
- **Collapse** a strongly-connected set into a single “super-node” (treat as one unit)
- **Time-slice**: convert feedback into iterative stages (v1 → v2)

## 3) Compute order (topological sorting)
Produce a valid execution order:
- pick any node with no remaining prerequisites (in-degree 0)
- execute/remove it
- repeat

If multiple nodes are available, choose by:
- shortest-first (unblock quickly)
- highest impact
- critical path urgency (see below)

## 4) Reduce graph complexity (optional but powerful)
### 4A) Transitive reduction mindset
If A→B and B→C exist, then A→C is often redundant. Prefer the **minimal** edge set that preserves reachability.

Practical heuristic:
- keep the edge only if removing it would change what’s reachable

### 4B) Cluster by layers
Group nodes by “distance from sources” to create phases:
- Phase 0: sources
- Phase 1: depends only on Phase 0
- …

## 5) Find the critical path (for planning)
If nodes have durations/estimates:
- compute the longest path from sources to sinks
- that path dictates the minimum completion time

Output:
- critical path nodes
- slack nodes (can be delayed without affecting finish)

## 6) Answer typical questions with DAG outputs
- **What do we do next?** → topological frontier (available nodes)
- **What blocks this task?** → ancestors of node
- **What breaks if we change X?** → descendants of node
- **How do we simplify?** → transitive reduction / merge nodes
- **Where are we stuck?** → cycle detection, no available nodes

## 7) Output format (default)
When you apply this skill, produce:
1) **Nodes** (with 1-line descriptions)
2) **Edges** (X → Y)
3) **Cycle check** result
4) **Proposed order** (phases or linear list)
5) (Optional) **Critical path** + slack
6) **Next actions**

## Quick prompts to ask the user (only if needed)
- “What counts as ‘done’ for each node?”
- “Is X truly required for Y, or just preferred?”
- “Do any dependencies create a loop?”
- “Do you care about fastest completion, lowest risk, or minimal context switching?”
