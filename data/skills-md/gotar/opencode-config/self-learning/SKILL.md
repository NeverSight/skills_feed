---
name: self-learning
description: Self-learning capability for agents. Captures execution traces, extracts insights, and adapts agent behavior. Use after completing complex tasks, when agents encounter recurring issues, or to optimize workflows over time. Critical for multi-agent systems like orchestrator, worker, and reviewer.
---

# Self Learning

## Overview

Enables agents to learn from their execution history by capturing traces, extracting actionable insights, and adapting behavior. Transforms raw execution patterns into reusable knowledge structures that improve future performance.

## When to Use This Skill

**Trigger this skill when:**
- An agent completes a complex task and should capture learnings
- Recurring patterns of failures or inefficiencies are detected
- An agent discovers a better approach that should be retained
- Multiple agents coordinate on a task and need shared learning
- Performance metrics show degradation or opportunity for improvement

**Automatic Invocation:**
Integrate into agents at critical points:
- **Orchestrator**: After merging worker results, capture coordination patterns
- **Worker**: After completing task (post-review), capture execution insights
- **Reviewer**: After detecting recurring issues, capture quality patterns
- **Task Manager**: After task completion, capture decomposition insights

## Core Capabilities

### 1. Trace Collection

Captures structured execution traces containing:

```markdown
# Execution Trace Structure
- Task Description
- Approach Used
- Tools Invoked (with tool calls)
- Context Loaded
- Results Achieved
- Failures/Errors Encountered
- Time Metrics (optional)
- Success/Failure Status
```

**Collection Strategy:**
- Manual capture: Agents document their execution after completion
- Automatic hooks: Trace capture integrated into agent workflows
- Context: Store traces in `.tmp/learning/traces/{timestamp}_{agent}_{task}.md`

**Example Trace:**
```markdown
# Trace: worker_implementation_20250108_1120
Agent: worker
Task: Implement user authentication feature
Status: Success

## Approach
1. Analyzed existing auth patterns in codebase
2. Implemented JWT token validation
3. Added tests for edge cases

## Tools Invoked
- Read: agent/openagent.md, code/auth.ts
- Write: code/auth.ts, tests/auth.test.ts
- lsp_diagnostics: code/auth.ts

## Results
- Auth implemented successfully
- All tests passing
- Zero diagnostics errors

## Failures Encountered
- Initial JWT secret configuration missing
- Fixed by reading config patterns from code/config.ts
```

### 2. Insight Extraction

Transforms traces into structured insights using pattern recognition:

**Insight Categories:**

| Category | Description | Example |
|----------|-------------|---------|
| **Success Patterns** | Approaches that consistently work | "Loading context.md before task start reduces errors by 40%" |
| **Failure Patterns** | Recurring causes of failures | " Skipping lsp_diagnostics leads to type errors in production" |
| **Efficiency Patterns** | Ways to complete tasks faster | "Reading multiple files in parallel reduces context load time" |
| **Coordination Patterns** | Best practices for multi-agent work | "Orchestrator spawning 2 workers instead of 3 reduces merge conflicts" |
| **Knowledge Gaps** | Information that should have been available | "Project lacks centralized error handling documentation" |

**Extraction Process:**
1. Analyze traces for recurring patterns
2. Identify successful vs unsuccessful approaches
3. Extract high-impact insights (prioritize by frequency and impact)
4. Structure insights as actionable recommendations
5. Store in `.tmp/learning/insights/{category}.md`

**Example Insights:**
```markdown
# Insights: Success Patterns

## Context Loading
**Finding**: Loading context.md before task start significantly reduces errors
**Evidence**: 10/10 successful tasks loaded context.md first
**Action**: Mandate context loading in all agent workflows
**Impact**: High (prevents 60% of failures)

## Parallel Execution
**Finding**: Spawning 2 workers in parallel reduces total time by 35%
**Evidence**: Compared to 3 workers (merge conflicts) and 1 worker (sequential)
**Action**: Default to 2 workers in orchestrator for most tasks
**Impact**: Medium (performance optimization)

# Insights: Failure Patterns

## Skipping Validation
**Finding**: 8/10 failures skipped lsp_diagnostics before completion
**Evidence**: Type errors detected post-merge
**Action**: Require lsp_diagnostics before task completion
**Impact**: High (prevents integration failures)
```

### 3. Adaptation

Applies insights to improve agent behavior:

**Adaptation Levels:**

1. **Immediate (Session-Local)**: Apply insights within current session
   - Example: "Switching to 2 workers based on merge conflict pattern"
   - Storage: `.tmp/learning/adaptations/session_{id}.md`

2. **Persistent (Agent-Specific)**: Update agent instructions for future sessions
   - Example: "Added mandatory lsp_diagnostics check to worker.md"
   - Storage: Update agent `.md` files directly

3. **System-Wide (All Agents)**: Modify agent orchestration patterns
   - Example: "Updated orchestrator.md to default to 2 workers"
   - Storage: Update core agent files

**Adaptation Rules:**
- Start with session-local adaptations (low risk)
- Promote to persistent only after 3+ confirming instances
- Require manual approval for system-wide changes
- Always preserve original behavior in comments

**Example Adaptation:**
```markdown
# Adaptation: Worker Validation Rule
Applied: Session
Date: 2025-01-08
Insight: "Skipping lsp_diagnostics leads to type errors in production"
Based on: 8/10 failures analyzed

Change:
- Added mandatory lsp_diagnostics check before swarm_worker_complete
- Updated worker.md to require validation in workflow

Result:
- Zero type errors in subsequent 5 tasks
- Minimal overhead (2-3 sec per task)
```

### 4. Knowledge Base

Builds a persistent knowledge base from insights:

**Structure:**
```
learning/
├── traces/           # Raw execution traces
├── insights/         # Extracted insights by category
├── adaptations/      # Applied adaptations by level
├── knowledge-base.md # Consolidated actionable knowledge
└── metrics/          # Performance metrics over time
```

**Knowledge Base Format:**
```markdown
# Self-Improving Agent Knowledge Base

Last Updated: 2025-01-08

## Agent Behavior Guidelines

### Context Management
- ALWAYS load context.md before starting tasks
- Read multiple files in parallel when possible
- Prune context aggressively (>50% reduction ideal)

### Validation
- Run lsp_diagnostics before completing any task
- Request review on all complex changes (>3 files)
- Verify with build/test commands when available

### Coordination
- Default to 2 parallel workers (3 causes merge conflicts)
- Wait for worker confirmation before spawning new workers
- Merge results sequentially, not all at once

### Common Pitfalls
Don't:
- Skip type checks to "save time"
- Assume patterns work without validation
- Batch-complete todos (mark individually)

Do:
- Extract key findings before pruning context
- Verify work after delegation
- Learn from failures, not just successes
```

## Workflow Decision Tree

```
Start Learning Process
├─ Is this task complete?
│  ├─ Yes → Capture trace
│  │      ├─ Manual documentation
│  │      └─ Automatic hooks (if integrated)
│  │
│  └─ No → Continue task
│
├─ Should we extract insights?
│  ├─ Yes (5+ traces available or pattern detected)
│  │      └─ Analyze traces
│  │             ├─ Identify patterns
│  │             ├─ Extract insights
│  │             └─ Prioritize by impact
│  │
│  └─ No (insufficient data) → Continue
│
└─ Should we adapt behavior?
   ├─ Yes (high-confidence insight available)
   │      └─ Determine adaptation level
   │             ├─ Session-local → Apply immediately
   │             ├─ Agent-specific → Update agent file
   │             └─ System-wide → Document and seek approval
   │
   └─ No (low confidence or risky) → Document and wait
```

## Integration Examples

### Integrating into Orchestrator

**Add to orchestrator.md:**

```markdown
## Post-Merge Learning

After merging worker results, capture coordination patterns:

1. Document:
   - Number of workers spawned
   - Merge conflicts encountered
   - Total execution time
   - Worker success/failure rates

2. If pattern detected (e.g., recurring conflicts):
   - Extract insight
   - Apply session-local adaptation
   - Example: "Reducing to 2 workers next phase"

3. After swarm completion:
   - Consolidate all traces
   - Extract insights for future swarms
   - Update orchestrator.md if pattern persists (>3 instances)
```

### Integrating into Worker

**Add to worker.md:**

```markdown
## Pre-Completion Learning

Before calling swarm_worker_complete:

1. REQUIRED: Run lsp_diagnostics
2. Capture execution trace:
   - Approach used
   - Tools invoked
   - Failures encountered
   - Success criteria met
3. Store trace: `.tmp/learning/traces/worker_{timestamp}.md`

## Post-Review Learning

After reviewer approval:

1. If reviewer identified issues:
   - Document failure pattern
   - Extract insight (e.g., "Always validate with reviewer before complex refactors")
   - Update worker.md if pattern recurs
```

### Integrating into Reviewer

**Add to reviewer.md:**

```markdown
## Pattern Detection

During review, watch for recurring issues:

1. Track issues by category:
   - Type safety violations
   - Missing validation
   - Inconsistent patterns
   - Performance issues

2. If same issue appears 3+ times:
   - Extract insight
   - Suggest agent adaptation
   - Update knowledge-base.md

3. Provide pattern-aware feedback:
   "Note: This is the 4th occurrence of X. Recommend adding Y to worker.md"
```

## Scripts

The following scripts support automated learning:

### analyze_traces.py

```python
"""
Analyze collected traces to extract patterns and insights.

Usage: python scripts/analyze_traces.py --traces .tmp/learning/traces/

Output: .tmp/learning/insights/
"""

import argparse
import json
from pathlib import Path
from collections import Counter
import re

def load_trace(trace_path):
    """Load and parse a trace file."""
    with open(trace_path) as f:
        content = f.read()
    # Extract structured data from trace
    return {
        'agent': extract_field(content, 'Agent'),
        'status': extract_field(content, 'Status'),
        'tools': extract_tools(content),
        'failures': extract_failures(content),
    }

def extract_field(content, field):
    """Extract a field from trace content."""
    pattern = f"{field}:\\s*(.+?)(?:\\n|$)"
    match = re.search(pattern, content)
    return match.group(1).strip() if match else None

def extract_tools(content):
    """Extract tools used from trace."""
    tools = re.findall(r'- ([\w_]+):', content)
    return Counter(tools)

def extract_failures(content):
    """Extract failure patterns from trace."""
    failures = re.findall(r'(?:Error|Failure):\\s*(.+)', content)
    return failures

def identify_patterns(traces):
    """Identify patterns across traces."""
    # Success patterns
    success_traces = [t for t in traces if t['status'] == 'Success']
    success_tools = Counter()
    for t in success_traces:
        success_tools.update(t['tools'])

    # Failure patterns
    failure_traces = [t for t in traces if t['status'] == 'Failure']
    failure_patterns = Counter()
    for t in failure_traces:
        failure_patterns.update(t['failures'])

    return {
        'success_tools': success_tools,
        'failure_patterns': failure_patterns,
        'success_rate': len(success_traces) / len(traces) if traces else 0,
    }

def generate_insights(patterns):
    """Generate actionable insights from patterns."""
    insights = []

    # Success pattern: Tools consistently used in successful traces
    for tool, count in patterns['success_tools'].most_common(5):
        insight = {
            'category': 'Success Patterns',
            'finding': f"Tool '{tool}' appears in {count} successful traces",
            'action': f"Consider making '{tool}' mandatory for relevant tasks",
            'impact': 'High' if count > 5 else 'Medium',
        }
        insights.append(insight)

    # Failure pattern: Recurring issues
    for pattern, count in patterns['failure_patterns'].most_common(5):
        insight = {
            'category': 'Failure Patterns',
            'finding': f"Failure pattern '{pattern}' occurs {count} times",
            'action': f"Add validation to prevent: {pattern}",
            'impact': 'High' if count > 3 else 'Medium',
        }
        insights.append(insight)

    return insights

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--traces', required=True, help='Path to traces directory')
    parser.add_argument('--output', default='.tmp/learning/insights', help='Output directory')
    args = parser.parse_args()

    # Load all traces
    trace_dir = Path(args.traces)
    traces = [load_trace(f) for f in trace_dir.glob('*.md')]

    # Identify patterns
    patterns = identify_patterns(traces)

    # Generate insights
    insights = generate_insights(patterns)

    # Save insights
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    for insight in insights:
        category = insight['category'].replace(' ', '_').lower()
        output_file = output_dir / f"{category}.md"

        with open(output_file, 'a') as f:
            f.write(f"## Insight: {insight['finding']}\n")
            f.write(f"**Category**: {insight['category']}\n")
            f.write(f"**Action**: {insight['action']}\n")
            f.write(f"**Impact**: {insight['impact']}\n\n")

    print(f"Generated {len(insights)} insights in {output_dir}")

if __name__ == '__main__':
    main()
```

### apply_adaptation.py

```python
"""
Apply an adaptation to agent behavior.

Usage: python scripts/apply_adaptation.py --agent worker --adaptation "Always run lsp_diagnostics"

Supports levels: session, agent, system
"""

import argparse
from pathlib import Path
from datetime import datetime

def apply_session_adaptation(agent, adaptation):
    """Apply session-local adaptation."""
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    adaptation_file = Path(f".tmp/learning/adaptations/session_{session_id}.md")

    with open(adaptation_file, 'w') as f:
        f.write(f"# Session Adaptation: {agent}\n")
        f.write(f"Applied: {datetime.now()}\n\n")
        f.write(f"**Adaptation**: {adaptation}\n")
        f.write(f"**Level**: Session-local\n")
        f.write(f"**Impact**: Applied to current session only\n")

    print(f"Session adaptation saved to {adaptation_file}")

def apply_agent_adaptation(agent, adaptation, agent_file):
    """Apply agent-specific adaptation."""
    agent_path = Path(agent_file)

    with open(agent_path, 'r') as f:
        content = f.read()

    # Find "## Workflow" or similar section
    if "## Workflow" in content:
        insertion_point = content.find("## Workflow")
        adapted_content = (
            content[:insertion_point] +
            f"## Learning Rule (Self-Improving)\n{adaptation}\n\n" +
            content[insertion_point:]
        )
    else:
        adapted_content = content + f"\n\n## Learning Rule (Self-Improving)\n{adaptation}\n"

    with open(agent_path, 'w') as f:
        f.write(adapted_content)

    print(f"Agent adaptation applied to {agent_path}")

def apply_system_adaptation(adaptation):
    """Apply system-wide adaptation (requires approval)."""
    print(f"SYSTEM-WIDE ADAPTATION REQUESTED:")
    print(f"  Adaptation: {adaptation}")
    print(f"\nThis requires manual approval.")
    print("Document in .tmp/learning/adaptations/system_pending.md")
    print("Then update relevant agent files after review.")

    pending_file = Path(".tmp/learning/adaptations/system_pending.md")
    pending_file.parent.mkdir(parents=True, exist_ok=True)

    with open(pending_file, 'a') as f:
        f.write(f"# System-Wide Adaptation (Pending Approval)\n")
        f.write(f"Requested: {datetime.now()}\n")
        f.write(f"**Adaptation**: {adaptation}\n")
        f.write(f"**Status**: Pending manual review\n\n")

    print(f"Adaptation documented in {pending_file}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--agent', required=True, help='Agent name (e.g., worker, orchestrator)')
    parser.add_argument('--adaptation', required=True, help='Adaptation description')
    parser.add_argument('--level', default='session', choices=['session', 'agent', 'system'], help='Adaptation level')
    parser.add_argument('--agent-file', help='Path to agent .md file (required for agent level)')
    args = parser.parse_args()

    if args.level == 'session':
        apply_session_adaptation(args.agent, args.adaptation)
    elif args.level == 'agent':
        if not args.agent_file:
            raise ValueError("--agent-file required for agent-level adaptations")
        apply_agent_adaptation(args.agent, args.adaptation, args.agent_file)
    elif args.level == 'system':
        apply_system_adaptation(args.adaptation)

if __name__ == '__main__':
    main()
```

## Safety Guidelines

**Critical Constraints:**

1. **Never adapt without evidence**
   - Require minimum 3-5 traces before extracting patterns
   - Validate insights across multiple sessions
   - Seek confirmation before major changes

2. **Start local, scale slowly**
   - Always apply session-local adaptations first
   - Promote to agent-specific only after validation
   - System-wide changes require manual approval

3. **Preserve original behavior**
   - Document what changed and why
   - Keep comments showing original patterns
   - Enable rollback if adaptation causes issues

4. **Don't override user intent**
   - Learning should optimize, not override
   - Adaptations must respect explicit instructions
   - Conflicts: user instructions > learned patterns

5. **Monitor for negative feedback**
   - Track adaptation effectiveness
   - Revert if success rate decreases
   - Learn from adaptation failures too

## Usage Example

**Scenario:** Orchestrator agent completes a complex swarm task with merge conflicts

**Execution:**

1. **Capture trace:**
```markdown
# Trace: orchestrator_swarm_20250108_1120
Agent: orchestrator
Task: Multi-feature implementation
Workers: 3
Merge Conflicts: 5 (high)
Total Time: 45min
Status: Success (with issues)
```

2. **Extract insight:**
```markdown
## Insight: Worker Count Optimization
**Finding**: 3 workers cause 5 merge conflicts
**Evidence**: Compared to previous 2-worker tasks (0-1 conflicts)
**Action**: Reduce to 2 workers for similar tasks
**Impact**: High (prevents merge conflicts, faster completion)
```

3. **Apply adaptation (session-local):**
```bash
python scripts/apply_adaptation.py \
  --agent orchestrator \
  --adaptation "Default to 2 workers instead of 3 for tasks with <5 subtasks" \
  --level session
```

4. **Result:**
   - Next swarm phase uses 2 workers
   - Merge conflicts reduced to 1
   - Total time reduced to 32min
   - Pattern validated

5. **Promote to persistent (after 3+ successful validations):**
```bash
python scripts/apply_adaptation.py \
  --agent orchestrator \
  --adaptation "Default to 2 workers instead of 3 for tasks with <5 subtasks" \
  --level agent \
  --agent-file /path/to/orchestrator.md
```

**Outcome:** Orchestrator permanently optimized based on learned experience.

## Metrics Tracking

Track learning effectiveness over time:

```markdown
# Learning Metrics

## Adaptation Success Rate
- Total adaptations applied: 15
- Successful improvements: 12 (80%)
- Neutral/no effect: 2 (13%)
- Negative (reverted): 1 (7%)

## Agent Performance (Before/After)
- Orchestrator: 45min → 32min (29% improvement)
- Worker: 3.2 failures/10 tasks → 1.1 failures/10 tasks (66% reduction)
- Reviewer: 2.1 issues/review → 1.4 issues/review (33% reduction)

## Knowledge Base Growth
- Traces collected: 127
- Insights extracted: 34
- Patterns validated: 12
```

---

**Key Principle:** This skill transforms execution history into actionable knowledge, enabling agents to systematically improve without human intervention. Start small, validate thoroughly, scale cautiously.
