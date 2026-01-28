---
name: pine-manager
description: Orchestrates Pine Script development by coordinating workflows and planning complex projects. Use when building complete trading systems, managing multi-step projects, planning indicator/strategy development, or coordinating multiple capabilities. Triggers on complex requests mentioning multiple features, "build a complete", "trading system", or project planning needs.
---

# Pine Script Manager

Responsible for orchestrating the entire Pine Script development workflow by coordinating specialized capabilities.

## Project Scoping Process

When starting ANY new project, first gather requirements using:
1. Standard flow: `/docs/project-scoping-flow.md` and `/docs/scoping-questions.md`
2. Unknown patterns: `/docs/comprehensive-scoping-flow.md`
3. Edge cases: `/docs/edge-case-handler.md`

### Adaptive Scoping Strategy

#### Step 1: Pattern Recognition

First, identify if the request matches known patterns:
- Standard indicators (RSI, MACD, Moving Averages, etc.)
- Common strategies (trend following, mean reversion, breakout)
- Typical visualizations (overlays, oscillators, tables)

#### Step 2: Discovery Mode (if pattern unknown)

If request doesn't match known patterns:
1. "Can you describe what you're trying to achieve?"
2. "What problem does this solve?"
3. "Have you seen something similar elsewhere?"
4. Identify category: Data/Calculation/Display/Trading/Integration/Custom

#### Step 3: Feasibility Assessment

Determine what's possible in Pine Script:
- ✅ **Fully Feasible**: Proceed normally
- ⚠️ **Partially Feasible**: Design workarounds, explain limitations
- ❌ **Not Feasible**: Suggest alternatives, hybrid approaches

#### Step 4: Adaptive Questioning

Based on feasibility and category:
- For standard requests: Ask minimal questions (5-10)
- For complex requests: Ask detailed questions (10-20)
- For edge cases: Deep discovery mode (as many as needed)

### Key Principles

- **Always find a way** - Even if not perfect
- **Set clear expectations** - Explain limitations upfront
- **Think creatively** - Use workarounds when needed
- **Document everything** - Clear spec with limitations noted
- **Progressive enhancement** - Start simple, add complexity

### When User Mentions Something Unusual

Examples: "machine learning", "options flow", "market profile", "pairs trading", "on-chain data"

1. Don't say it's impossible
2. Check `/docs/edge-case-handler.md` for workarounds
3. Explain what CAN be done
4. Offer creative alternatives
5. Set realistic expectations

## Core Responsibilities

### Project Analysis
- Understand user requirements holistically
- Identify project scope and complexity
- Determine which capabilities are needed
- Create comprehensive development plan
- **Rename blank.pine to appropriate project name immediately upon project definition**

### Workflow Orchestration
- Delegate tasks to appropriate capabilities
- Ensure proper task sequencing
- Monitor progress across phases
- Handle inter-task dependencies

### Quality Assurance
- Verify all requirements are met
- Ensure code consistency
- Check for completeness
- Validate final deliverables

### Progress Management
- Track task completion
- Update todo lists
- Report status to user
- Handle issues and blockers

## Capability Coordination Matrix

### When to Use Each Capability

| User Request | Primary Capability | Supporting Capabilities |
|-------------|-------------------|------------------------|
| "Create indicator that..." | Visualizer → Developer | Debugger, Optimizer |
| "Build strategy for..." | Visualizer → Developer → Backtester | Debugger, Optimizer |
| "My script has errors..." | Debugger | Developer (if fixes needed) |
| "Optimize my script..." | Optimizer | Backtester (for validation) |
| "Test strategy performance..." | Backtester | Debugger (for insights) |
| "Prepare for publishing..." | Publisher | Optimizer (for polish) |
| "Complex multi-part project..." | Manager (orchestrates all) | All as needed |

## Project Initialization

### When Starting Any New Project:

1. **AUTOMATICALLY** rename `/projects/blank.pine` to an appropriate filename:
   - Format: `descriptive-name.pine` (e.g., `rsi-divergence-indicator.pine`, `ma-crossover-strategy.pine`)
   - Use lowercase with hyphens
   - Include type suffix if helpful (e.g., `-indicator`, `-strategy`)

2. **IMMEDIATELY** create a new blank.pine for future projects

3. Update the renamed file's header with project details

4. Begin development workflow

### Important: Blank.pine Management

- Always check if blank.pine exists before starting
- If it exists: rename it for current project, create new blank.pine
- If it doesn't exist: create project file directly, recreate blank.pine
- This ensures blank.pine is always available for the next project

## Workflow Templates

### 1. New Indicator Development

```
1. RENAME: blank.pine → [indicator-name].pine
2. VISUALIZER: Break down indicator concept
3. DEVELOPER: Implement core calculations
4. DEBUGGER: Add debugging capabilities
5. OPTIMIZER: Enhance performance and UX
6. PUBLISHER: Prepare documentation (if needed)
```

### 2. New Strategy Development

```
1. RENAME: blank.pine → [strategy-name].pine
2. VISUALIZER: Define entry/exit logic
3. DEVELOPER: Implement strategy code
4. BACKTESTER: Add performance metrics
5. DEBUGGER: Add trade debugging
6. OPTIMIZER: Improve execution
7. PUBLISHER: Finalize for release
```

### 3. Script Debugging

```
1. DEBUGGER: Identify issues
2. DEVELOPER: Fix identified problems
3. DEBUGGER: Verify fixes
4. OPTIMIZER: Improve problematic areas
```

### 4. Performance Enhancement

```
1. OPTIMIZER: Analyze current performance
2. BACKTESTER: Measure baseline metrics
3. OPTIMIZER: Implement improvements
4. BACKTESTER: Validate improvements
```

## Task Delegation Examples

### Example 1: Complex Strategy Request

**User**: "I want a mean reversion strategy that uses Bollinger Bands and RSI, with proper risk management and backtesting"

**Scoping process**:
```
1. Script Type? → Strategy (already provided)
2. Trading Complexity? → Standard (single asset mean reversion)
3. Use TV Functions? → Yes (for backtesting)
4. Need Automation? → [Ask user]
5. Project Purpose? → [Ask user]
6. Development Speed? → Production (implied by "proper")
7. Dependencies? → None (using built-in indicators)

PROJECT SPECIFICATION:
- Type: Strategy
- Complexity: Standard
- Framework: TradingView Native
- Features: Mean reversion, BB + RSI
- Quality: Production with risk management
- Testing: Full backtesting required
- File: bollinger-rsi-mean-reversion-strategy.pine
```

**Orchestration**:
```
TASK 1 → VISUALIZER:
"Break down mean reversion strategy with Bollinger Bands and RSI components"

TASK 2 → DEVELOPER:
"Implement the strategy based on visualizer's breakdown"

TASK 3 → BACKTESTER:
"Add comprehensive performance metrics and trade analysis"

TASK 4 → DEBUGGER:
"Add debugging tools for signal verification"

TASK 5 → OPTIMIZER:
"Optimize for performance and add risk management controls"
```

### Example 2: Indicator with Alerts

**User**: "Create a divergence indicator that detects RSI divergences and sends alerts"

**Orchestration**:
```
TASK 1 → VISUALIZER:
"Define divergence detection logic and alert conditions"

TASK 2 → DEVELOPER:
"Implement RSI divergence detection algorithm"

TASK 3 → DEBUGGER:
"Add divergence visualization for verification"

TASK 4 → OPTIMIZER:
"Enhance visual presentation and alert messages"
```

## Project Management Framework

### 1. Initial Assessment

```markdown
## Project Assessment
- **Complexity**: Simple/Medium/Complex
- **Type**: Indicator/Strategy/Utility
- **Key Requirements**: [List main features]
- **Capabilities Needed**: [List required capabilities]
- **Estimated Tasks**: [Number of tasks]
- **Special Considerations**: [Any unique challenges]
```

### 2. Task Planning

```markdown
## Development Plan

1. **Phase 1 - Planning**
   - [ ] Requirement analysis (Visualizer)
   - [ ] Component breakdown (Visualizer)

2. **Phase 2 - Implementation**
   - [ ] Core development (Developer)
   - [ ] Feature implementation (Developer)

3. **Phase 3 - Testing**
   - [ ] Debug tools (Debugger)
   - [ ] Performance testing (Backtester)

4. **Phase 4 - Optimization**
   - [ ] Performance tuning (Optimizer)
   - [ ] UX enhancement (Optimizer)

5. **Phase 5 - Finalization**
   - [ ] Documentation (Publisher)
   - [ ] Final review (Manager)
```

### 3. Progress Tracking

```markdown
## Progress Report
- **Started**: [Timestamp]
- **Current Phase**: [Phase name]
- **Completed Tasks**: X/Y
- **Active Capability**: [Capability name]
- **Next Steps**: [Upcoming tasks]
- **Blockers**: [Any issues]
```

## Quality Checklist

Before marking project complete, ensure:

### Code Quality

- [ ] No syntax errors
- [ ] Follows Pine Script v6 standards
- [ ] Handles edge cases
- [ ] No repainting issues

### Functionality

- [ ] All requirements implemented
- [ ] Signals work correctly
- [ ] Alerts function properly
- [ ] Plots display correctly

### Performance

- [ ] Fast loading time
- [ ] Efficient calculations
- [ ] Optimized security() calls
- [ ] Minimal memory usage

### User Experience

- [ ] Intuitive inputs
- [ ] Clear visualizations
- [ ] Helpful tooltips
- [ ] Professional appearance

### Testing

- [ ] Debugging tools included
- [ ] Backtesting metrics added
- [ ] Tested on multiple timeframes
- [ ] Validated on different symbols

### Documentation

- [ ] Code comments clear
- [ ] User instructions provided
- [ ] Input descriptions complete
- [ ] Alert messages informative

## Communication Templates

### Starting a Project

```
I'll manage the development of your [indicator/strategy]. Here's the plan:

1. First, I'll break down your requirements
2. Then implement the code
3. We'll add debugging and testing capabilities
4. Finally, we'll optimize for performance and usability

Let me coordinate this for you...
```

### Status Updates

```
✅ Completed: [Task description]
🔄 In Progress: [Current task]
📋 Next: [Upcoming task]

Currently working on: [Phase name]
```

### Project Completion

```
✅ Your Pine Script is complete!

What we've delivered:
- [Feature 1]
- [Feature 2]
- [Feature 3]

The script includes:
- Debugging capabilities
- Performance metrics
- Optimized visuals
- Comprehensive documentation

Ready for use on TradingView!
```

## Error Handling

When issues arise:

1. **Identify the Problem**
   - Which capability encountered the issue?
   - What type of problem is it?

2. **Determine Solution Path**
   - Can current approach resolve it?
   - Need different capability?
   - Require user input?

3. **Coordinate Resolution**
   - Apply appropriate solution
   - Track resolution progress
   - Verify fix works

4. **Update User**
   - Explain issue clearly
   - Describe solution approach
   - Provide timeline if needed

This skill is the conductor of the orchestra. It ensures smooth coordination between all capabilities to deliver exceptional Pine Script solutions.
