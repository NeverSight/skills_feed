---
name: eae-performance-analyzer
description: >
  Prevents event storms in EcoStruxure Automation Expert applications through
  static analysis of event propagation, CPU load estimation, queue depth
  prediction, and anti-pattern detection. Analyzes IEC 61499 artifacts to
  identify cascading events before deployment.
license: MIT
compatibility: Designed for EcoStruxure Automation Expert 25.0+, Python 3.8+, PowerShell (Windows)
metadata:
  version: "1.0.0"
  model: claude-opus-4-5-20251101
  domain: industrial-automation
  standard: IEC-61499
  eae_version: "25.0+"
  timelessness_score: 9/10
  user-invocable: true
  platform: EcoStruxure Automation Expert
---
# EAE Performance Analyzer - Event Storm Prevention

Prevents catastrophic event storms in EcoStruxure Automation Expert applications through comprehensive static analysis. Identifies cascading event patterns, predicts queue overflow, estimates CPU load, and detects anti-patterns before deployment.

**Critical Problem**: Event storms cause Error Halt states, event loss, I/O glitches, and cross-communication failures in production EAE systems. Current detection is reactive (runtime monitoring) rather than proactive (design validation).

**Solution**: Multi-dimensional static analysis at design time calculates event multiplication factors, predicts queue depths, estimates CPU utilization, and flags explosive patterns with actionable recommendations.

---

## Quick Start

**Analyze entire application**:
```bash
Analyze my EAE application for event storm risks
```

**Analyze specific resource**:
```bash
Check Resource1 in my EAE application for performance issues
```

**Generate visual event flow diagram**:
```bash
Analyze my EAE application and show me the event flow visualization
```

---

## Triggers

This skill activates on:

- "Analyze my EAE application for event storms"
- "Check for performance issues in my EAE project"
- "Detect event cascade problems in EcoStruxure Automation Expert"
- "Validate event flow before deployment"
- "Predict event storm risks"

---

## Quick Reference

| Analysis Dimension | Metric | Safe Threshold | Warning Threshold | Critical Threshold |
|--------------------|--------|----------------|-------------------|-------------------|
| **Event Multiplication** | Single event → N events | <10x | 10-20x | >20x |
| **Queue Depth** | Peak events in queue | <100 | 100-500 | >500 |
| **CPU Load** | Resource utilization % | <70% | 70-90% | >90% |
| **Anti-Patterns** | Detected issues | 0 | Minor patterns | Severe patterns |

| Risk Level | Deployment Recommendation | Typical Action |
|------------|--------------------------|----------------|
| **SAFE** | Deploy with confidence | No action needed |
| **CAUTION** | Review before deployment | Optional optimization |
| **WARNING** | Deploy with monitoring | Address high-priority issues |
| **CRITICAL** | Do not deploy | Fix severe issues first |

---

## How It Works

### 4-Dimensional Analysis

The skill performs parallel analysis across 4 independent dimensions:

```
Parse EAE Application (.fbt, .cfg, .xml)
    │
    ├─→ [Event Flow Analysis] → Multiplication factors, cascade paths
    ├─→ [CPU Load Estimation] → Algorithm complexity, execution time
    ├─→ [Queue Depth Prediction] → External/internal queue modeling
    └─→ [Pattern Detection] → Known storm anti-patterns
    │
    ▼
Synthesis → Integrated risk assessment + recommendations
    │
    ▼
Reports (JSON, Markdown, Graphviz) + Deployment decision
```

### Event Multiplication Factor (Primary Metric)

The **event multiplication factor** quantifies how many downstream events result from a single event source:

- **1.0x**: No multiplication (1 event → 1 event) - Ideal
- **5.0x**: Low multiplication (1 event → 5 events) - Safe
- **15.0x**: Moderate multiplication - Monitor
- **30.0x**: High multiplication - Warning
- **50.0x+**: Explosive multiplication - Critical storm risk

**Example**: An I/O change event triggers 3 FBs, each generating 2 output events that trigger 4 more FBs → 1 event becomes 26+ events (26x multiplication).

---

## Commands

### Basic Analysis

```bash
# Analyze entire application
Analyze c:/Projects/MyEAEApp for event storm risks

# Analyze with custom output location
Analyze c:/Projects/MyEAEApp and save report to c:/Reports/performance.md
```

### Resource-Specific Analysis

```bash
# Analyze single resource (faster iteration)
Analyze Resource_PLC1 in c:/Projects/MyEAEApp

# Compare multiple resources
Analyze c:/Projects/MyEAEApp and compare performance across resources
```

### Advanced Options

```bash
# Include event flow visualization
Analyze c:/Projects/MyEAEApp with event flow diagram

# Specify target platform for calibrated thresholds
Analyze c:/Projects/MyEAEApp for soft-dpac platform

# Custom load scenario
Analyze c:/Projects/MyEAEApp under worst-case load scenario
```

---

## Scripts

This skill includes 4 autonomous Python scripts for fully agentic operation:

### 1. `analyze_event_flow.py` - Event Cascade Analysis

**Purpose**: Traces event propagation through FBNetworks, calculates multiplication factors, identifies explosive patterns.

**Usage**:
```bash
python scripts/analyze_event_flow.py --app-dir c:/Projects/MyEAEApp --output results.json
python scripts/analyze_event_flow.py --app-dir c:/Projects/MyEAEApp --visualize --output flow.dot
python scripts/analyze_event_flow.py --app-dir c:/Projects/MyEAEApp --resource Resource1
```

**Exit Codes**:
- `0`: No issues (multiplication <10x)
- `10`: Moderate risk (10-20x multiplication)
- `11`: High risk (>20x multiplication)
- `1`: Error (parsing failure, invalid files)

**Output**: JSON with multiplication factors, cascade paths, explosive patterns, resource breakdown

---

### 2. `estimate_cpu_load.py` - CPU Utilization Analysis

**Purpose**: Analyzes ST algorithm complexity, estimates execution time, aggregates resource CPU load.

**Usage**:
```bash
python scripts/estimate_cpu_load.py --app-dir c:/Projects/MyEAEApp --output cpu_load.json
python scripts/estimate_cpu_load.py --app-dir c:/Projects/MyEAEApp --platform hard-dpac-m262
python scripts/estimate_cpu_load.py --app-dir c:/Projects/MyEAEApp --resource Resource1
```

**Exit Codes**:
- `0`: Low load (<70%)
- `10`: Moderate load (70-90%)
- `11`: High load (>90%)
- `1`: Error (parsing failure)

**Output**: JSON with per-FB execution estimates, per-resource CPU load percentages, bottleneck identification

**Note**: Execution time estimates are approximate (±50% margin) due to platform variance and compiler optimizations.

---

### 3. `predict_queue_depth.py` - Queue Overflow Prediction

**Purpose**: Models event queue behavior, predicts peak depths under various load scenarios.

**Usage**:
```bash
python scripts/predict_queue_depth.py --app-dir c:/Projects/MyEAEApp --event-flow-results results.json
python scripts/predict_queue_depth.py --app-dir c:/Projects/MyEAEApp --event-flow-results results.json --scenario worst-case
python scripts/predict_queue_depth.py --app-dir c:/Projects/MyEAEApp --event-flow-results results.json --resource Resource1
```

**Exit Codes**:
- `0`: Safe (<100 events)
- `10`: Moderate (100-500 events)
- `11`: Overflow risk (>500 events)
- `1`: Error (missing dependencies)

**Output**: JSON with queue depth predictions (normal/burst/worst-case), event source contributions, overflow warnings

**Requires**: Output from `analyze_event_flow.py` (JSON file path via `--event-flow-results`)

---

### 4. `detect_storm_patterns.py` - Anti-Pattern Detection

**Purpose**: Rule-based detection of known event storm anti-patterns from SE Application Design Guidelines.

**Usage**:
```bash
python scripts/detect_storm_patterns.py --app-dir c:/Projects/MyEAEApp --output patterns.json
```

**Exit Codes**:
- `0`: No anti-patterns
- `10`: Minor anti-patterns (INFO/WARNING)
- `11`: Severe anti-patterns (CRITICAL)
- `1`: Error (parsing failure)

**Output**: JSON with detected patterns, severity levels, source locations, pattern-specific recommendations

**Detected Anti-Patterns**:
- **TIGHT_EVENT_LOOP** (CRITICAL): Event loops back to source within 2 hops
- **UNCONTROLLED_IO_MULTIPLICATION** (WARNING): Single I/O event triggers >30 events
- **CASCADING_TIMERS** (WARNING): Multiple fast timers on same resource
- **HMI_BURST_AMPLIFICATION** (INFO): HMI events trigger >10 downstream events
- **CROSS_RESOURCE_AMPLIFICATION** (WARNING): Cross-resource events trigger >15 events

---

## Validation

### Pre-Analysis Validation

Before analysis begins:
- ✅ Verify EAE application directory exists and contains .fbt/.cfg/.xml files
- ✅ Parse all XML files for well-formedness
- ✅ Resolve all FB references (check for missing library FBs)
- ✅ Validate resource mappings (FBs assigned to valid resources)

### Analysis Validation

During analysis:
- ✅ Event multiplication factor ≥0 (sanity check)
- ✅ Queue depth predictions ≥0 (sanity check)
- ✅ CPU load estimates 0-100% (sanity check)
- ✅ All cascade paths terminate (no infinite loops in graph traversal)

### Post-Analysis Validation

After synthesis:
- ✅ Every WARNING/CRITICAL issue has at least one recommendation
- ✅ Overall risk assessment matches worst individual dimension
- ✅ Deployment recommendation justified by specific metrics
- ✅ All requested output formats generated successfully

---

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| **Runtime-only monitoring** | Too late - storms discovered in production cause downtime | Static analysis at design time |
| **Single-metric focus** (CPU only) | Event storms are multi-dimensional | 4-dimensional analysis (events, CPU, queues, patterns) |
| **Blocking deployment without override** | Tool has false positives, engineer judgment paramount | Recommend but allow override with confirmation |
| **Perfect accuracy claims** | Algorithm timing is approximate due to platform variance | Communicate uncertainty (±50% margin) |
| **Ignoring resource boundaries** | Distributed apps have different characteristics | Per-resource analysis + cross-resource modeling |
| **Raw metrics without fixes** | Engineers need "how to fix" not just "what's wrong" | Every issue includes actionable recommendation |
| **Slow, complex analysis** | Won't be used in iterative workflow | Fast (<2 min), minimal setup |

---

## Verification Criteria

After running analysis, verify:

- [ ] Analysis completed in <2 minutes for large applications (1000+ FBs)
- [ ] All 4 scripts returned exit codes 0, 10, or 11 (not 1=error)
- [ ] JSON reports parse successfully and contain expected fields
- [ ] Multiplication factors are numeric and ≥0
- [ ] Queue depth predictions are numeric and ≥0
- [ ] CPU load estimates are 0-100%
- [ ] Every WARNING/CRITICAL issue has recommendation
- [ ] Overall risk level matches worst individual dimension
- [ ] Deployment recommendation is one of: SAFE TO DEPLOY, DEPLOY WITH CAUTION, DO NOT DEPLOY
- [ ] If event flow visualization requested, .dot file generated

---

## Integration with EAE Skills

| Skill | Integration Point | How Performance Analyzer Helps |
|-------|------------------|-------------------------------|
| **eae-basic-fb** | After Basic FB creation | Analyzes event generation patterns, warns if high multiplication potential |
| **eae-composite-fb** | After Composite FB creation | Checks FBNetwork complexity, identifies cascade risks |
| **eae-cat** | After CAT creation | Validates cross-communication patterns, HMI event loads |
| **eae-adapter** | After adapter creation | Analyzes bidirectional event flow impact |
| **eae-skill-router** | Orchestration | Automatically suggests performance analysis after artifact creation |

---

<details>
<summary><strong>Deep Dive: Event Multiplication Analysis</strong></summary>

## Event Multiplication Mechanics

### IEC 61499 Execution Model

EAE follows the IEC 61499 event-driven execution model with dual queues per resource:

1. **External Queue**: Events from outside the resource (I/O, HMI, cross-communication) - FIFO
2. **Internal Queue**: Events generated by FBs within the resource

**Critical Processing Order**:
1. Pop event from external queue
2. Execute target FB
3. FB generates output events → pushed to internal queue
4. **Process ALL internal events until queue empty** (cascade completes)
5. Return to step 1 (next external event)

**Storm Trigger**: If step 4 generates more events than step 1 consumes, queues grow unbounded.

### Multiplication Factor Calculation

For each event source `S`:

```
Multiplication Factor = Total Events Generated / 1 Event from S

Example:
  I/O Change Event "DI_Start"
    → Triggers ControllerFB (generates 2 events)
      → Each triggers 2 ProcessFBs (4 events total)
        → Each triggers LoggerFB (4 events total)

  Total: 1 + 2 + 4 + 4 = 11 events
  Multiplication Factor: 11 / 1 = 11.0x
```

### Event Sources Modeled

| Source Type | Frequency | Characteristics |
|-------------|-----------|-----------------|
| **I/O Changes** | Bus cycle dependent (10-100ms) | State-driven, bursty |
| **HMI Interactions** | Operator-driven (1-10 Hz) | Unpredictable, can burst |
| **Timers (E_CYCLE)** | Fixed (1ms - 1s) | Constant, predictable |
| **Cross-Communication** | Application-driven | Network latency (10-100ms) |
| **Internal Logic** | Event-driven cascade | Multiplication dependent |

### Cascade Path Tracing

The script uses **Breadth-First Search (BFS)** to enumerate all paths from event source to leaf FBs:

```
Source: INIT event on MainFB
  Path 1: MainFB → ProcessFB1 → LoggerFB (3 hops, 3 events)
  Path 2: MainFB → ProcessFB2 → AlarmFB (3 hops, 3 events)
  Path 3: MainFB → ProcessFB2 → TrendFB (3 hops, 3 events)

  Multiplication: 9 events / 1 source = 9.0x
```

Paths are color-coded in visualizations:
- Green: <10x (safe)
- Yellow: 10-20x (caution)
- Red: 20-50x (warning)
- Dark Red: >50x (critical)

</details>

<details>
<summary><strong>Deep Dive: CPU Load Estimation</strong></summary>

## Algorithm Complexity Analysis

### ST Code Metrics

The script analyzes Structured Text (ST) algorithms using simplified metrics:

| Metric | Description | Weight |
|--------|-------------|--------|
| **Cyclomatic Complexity** | Branches (IF/CASE) + Loops (FOR/WHILE) + 1 | High impact |
| **Operation Count** | Arithmetic, logic, function calls | Medium impact |
| **Data Access** | Variable reads/writes, array indexing | Low impact |

**Formula**:
```
Execution Time ≈ (Complexity × 10μs) + (Operations × 1μs) + (DataAccess × 0.5μs)
```

**Platform Factors**:
- Soft dPAC (Windows): 1.0x baseline
- Soft dPAC (Linux): 0.9x (slightly faster)
- Hard dPAC M251: 1.5x (slower embedded CPU)
- Hard dPAC M262: 1.2x (faster embedded CPU)

### Limitations

**IMPORTANT**: Execution time estimates are **heuristic-based** and vary ±50% due to:

- Compiler optimizations (loop unrolling, inlining)
- Cache effects (data locality, cache hits/misses)
- Operating system scheduling (preemption, interrupts)
- Instruction-level parallelism (CPU pipelining)
- Platform-specific instruction sets (SSE, AVX on x86)

**Treat estimates as order-of-magnitude indicators**: 50μs vs 500μs vs 5ms, not precise timings.

### Resource CPU Load Aggregation

For each resource:

```
CPU Load % = (Σ FB Execution Times × Event Frequency) / Available CPU Time × 100

Example Resource1:
  FB1: 100μs × 10 Hz (I/O events) = 1000μs/s = 0.1% load
  FB2: 500μs × 100 Hz (timer events) = 50000μs/s = 5.0% load
  FB3: 200μs × 5 Hz (HMI events) = 1000μs/s = 0.1% load

  Total: 5.2% load
  Headroom: 94.8%
```

**Thresholds**:
- <70%: SAFE (ample headroom)
- 70-90%: CAUTION (monitor under load)
- 90-95%: WARNING (minimal headroom)
- >95%: CRITICAL (insufficient headroom for bursts)

</details>

<details>
<summary><strong>Deep Dive: Queue Depth Prediction</strong></summary>

## Queue Behavior Modeling

### Dual Queue System

Each EAE resource maintains two event queues:

```
External Queue (from outside resource)
  ← I/O events
  ← HMI events
  ← Cross-communication events
  ← Timer events (E_CYCLE)

Internal Queue (from FBs in resource)
  ← FB output events
  ← Algorithm-generated events
  ← Cascaded events
```

**Processing**: External queue feeds internal queue, internal queue processes until empty before next external event.

### Load Scenarios

| Scenario | Description | Event Rates |
|----------|-------------|-------------|
| **Normal** | Average operating conditions | 1× baseline rates |
| **Burst** | Operator interaction spike | 2× baseline rates, 5s duration |
| **Worst-Case** | All sources simultaneous + timers aligned | 5× baseline rates, all timers fire together |

### Prediction Formula

```
Peak Queue Depth = (Event Generation Rate × Burst Duration) - (Processing Rate × Burst Duration)

If Peak Depth > Threshold:
  Overflow Risk = HIGH
```

**Example**:
```
Normal:
  Generation: 100 events/s
  Processing: 200 events/s
  Queue Depth: 0 (steady state)

Burst:
  Generation: 200 events/s (2× normal)
  Processing: 200 events/s
  Queue Depth: 0 (just keeping up)

Worst-Case:
  Generation: 500 events/s (5× normal, all aligned)
  Processing: 200 events/s
  Queue Depth: (500 - 200) × 5s = 1500 events (OVERFLOW)
```

### Event Source Contributions

The report breaks down which sources contribute most to queue load:

```json
{
  "event_sources_contribution": {
    "IO_CHANGE": "35%",
    "HMI_INTERACTION": "25%",
    "TIMERS": "20%",
    "CROSS_COMMUNICATION": "15%",
    "INTERNAL_LOGIC": "5%"
  }
}
```

This identifies where to focus optimization efforts (e.g., "Reduce timer frequency" vs "Consolidate HMI events").

</details>

<details>
<summary><strong>Deep Dive: Anti-Pattern Detection</strong></summary>

## Known Storm Patterns

Based on SE Application Design Guidelines (EIO0000004686.06):

### 1. TIGHT_EVENT_LOOP (CRITICAL)

**Description**: FB event output connects back to its own input within 2 hops, creating unstoppable cascade.

**Detection**: Graph cycle detection with depth limit 2.

**Example**:
```
ControllerFB.Output_Event
  → ProcessFB.Input_Event
    → ProcessFB.Output_Event
      → ControllerFB.Input_Event  ← LOOP DETECTED
```

**Risk**: Infinite event generation until Error Halt.

**Recommendation**: Break loop with state guard (flag variable) or timer-based debouncing.

---

### 2. UNCONTROLLED_IO_MULTIPLICATION (WARNING)

**Description**: Single I/O change triggers >30 downstream events (common with broadcast patterns).

**Detection**: Event cascade tracing from I/O sources, count total events.

**Example**:
```
DI_Emergency_Stop changes
  → Triggers SafetyControllerFB (5 events)
    → Each triggers AlarmFB + LoggerFB + HMIFB (3 × 5 = 15 events)
      → Each triggers NotificationFB (15 events)

  Total: 1 + 5 + 15 + 15 = 36 events (>30 threshold)
```

**Risk**: I/O events are frequent (10-100ms cycle) - high multiplication causes saturation.

**Recommendation**: Consolidate responses using adapter pattern or EventChainHead FB (SE.AppSequence library).

---

### 3. CASCADING_TIMERS (WARNING)

**Description**: Multiple fast timers (E_CYCLE <50ms) on same resource sum to high frequency baseline load.

**Detection**: Sum all timer frequencies per resource, flag if >100Hz aggregate.

**Example**:
```
Resource1:
  Timer1: E_CYCLE at 20ms (50 Hz)
  Timer2: E_CYCLE at 30ms (33 Hz)
  Timer3: E_CYCLE at 40ms (25 Hz)

  Total: 50 + 33 + 25 = 108 Hz (>100 Hz threshold)
```

**Risk**: Constant event load leaves no headroom for I/O or HMI events.

**Recommendation**: Reduce timer frequencies, consolidate timers, or distribute across resources.

---

### 4. HMI_BURST_AMPLIFICATION (INFO)

**Description**: HMI operator actions trigger >10 downstream events (normal but can spike under rapid interaction).

**Detection**: Trace HMI event sources (IThis interface events), count cascade.

**Example**:
```
HMI Setpoint Change
  → ControllerFB validates (2 events)
    → ProcessFB updates (3 events)
      → TrendFB logs (3 events)
        → AlarmFB checks limits (2 events)

  Total: 1 + 2 + 3 + 3 + 2 = 11 events (>10 threshold)
```

**Risk**: Rapid operator interactions (button mashing) create bursts.

**Recommendation**: Add debouncing (e.g., 100ms delay) or rate limiting on HMI inputs.

---

### 5. CROSS_RESOURCE_AMPLIFICATION (WARNING)

**Description**: Event crossing resource boundary (via OPC-UA/networking) triggers >15 events on target resource.

**Detection**: Identify cross-resource connections, trace cascade on target resource.

**Example**:
```
Resource1.OutputEvent
  → [Network: 10-100ms latency]
    → Resource2.InputEvent
      → Triggers 18 events on Resource2 (>15 threshold)
```

**Risk**: Network latency + event multiplication can cause target resource saturation.

**Recommendation**: Reduce cross-resource event frequency, consolidate with adapters, or use EventChainHead.

</details>

<details>
<summary><strong>Deep Dive: Actionable Recommendations</strong></summary>

## Recommendation Patterns

For each identified issue, the skill provides specific, implementable fixes:

### Event Consolidation Pattern

**Problem**: High event multiplication (20-50x)

**Recommendation**:
```
Use EventChainHead (SE.AppSequence library) to consolidate cascading events:

1. Create EventChainHead FB instance
2. Connect all event sources to EventChainHead.Input[]
3. EventChainHead outputs single CONSOLIDATED event
4. Connect CONSOLIDATED to downstream FBs

Reduction: 50x → 5x (10:1 improvement)
```

**Before**:
```
Event → FB1 → FB2 → FB3 → FB4 → FB5 (5 events)
     ↘ FB6 → FB7 → FB8 → FB9 → FB10 (5 events)
     ↘ ... (repeat 5× = 50 events total)
```

**After**:
```
Event → EventChainHead → CONSOLIDATED → (all FBs receive 1 event)
```

---

### Adapter Encapsulation Pattern

**Problem**: Uncontrolled I/O multiplication (>30 events)

**Recommendation**:
```
Encapsulate related I/O responses in Composite FB with adapter interface:

1. Create Composite FB "SafetyResponseController"
2. Add adapter input (Socket) for I/O event
3. Implement response logic inside Composite (hidden complexity)
4. Export single adapter output (Plug) with consolidated result
5. Connect I/O to adapter Socket

Reduction: 36 events → 3 events (adapter input + internal + adapter output)
```

**Benefit**: I/O sees simple 1:1 connection, complexity hidden inside Composite.

---

### Timer Frequency Reduction Pattern

**Problem**: Cascading timers (>100Hz aggregate)

**Recommendation**:
```
Reduce non-critical timer frequencies:

Identify timers by criticality:
- Safety/control loops: Keep fast (10-50ms)
- Trending/logging: Slow to 100-500ms
- Heartbeats: Slow to 1000ms

Example:
  TrendFB timer: 20ms → 200ms (50 Hz → 5 Hz)
  Savings: 45 Hz per resource
```

**Impact**: 108 Hz → 63 Hz (below 100 Hz threshold)

---

### Resource Distribution Pattern

**Problem**: Single resource overloaded (CPU >90% or queue >500)

**Recommendation**:
```
Distribute FBs across multiple resources:

1. Identify high-load FBs (top 20% by CPU)
2. Move to dedicated resource (Resource2)
3. Use adapters for cross-resource communication
4. Update resource mappings in .cfg

Example:
  Resource1: 95% load → 65% load (30% moved)
  Resource2: 0% load → 30% load (receives moved FBs)
```

**Consideration**: Cross-resource events have 10-100ms latency - ensure control loops stay on same resource.

---

### Loop Breaking Pattern

**Problem**: Tight event loop (CRITICAL)

**Recommendation**:
```
Break loop with state guard:

1. Add BOOL internal variable "m_EventProcessed"
2. In algorithm that generates loop event:

   IF NOT m_EventProcessed THEN
     m_EventProcessed := TRUE;
     // Generate output event
   END_IF

3. Reset flag on different event path

Alternative: Use timer-based debouncing (100ms minimum between events)
```

**Result**: Loop executes once per trigger instead of infinitely.

</details>

---

## Extension Points

Future enhancements planned:

1. **Simulation-Based Analysis** (Year 2)
   - Execute application with synthetic event sources
   - Measure actual queue depths and CPU load
   - Complement static analysis with dynamic verification

2. **Historical Trend Analysis** (Year 1)
   - Track performance metrics over application versions
   - Identify regressions (e.g., "v2.1 added 15x multiplication")
   - CI/CD integration for automated tracking

3. **Platform-Specific Calibration** (Year 1)
   - Empirical calibration of CPU thresholds per platform
   - Database of platform profiles (Soft dPAC, M251, M262)
   - Improved execution time accuracy

4. **Auto-Refactoring Suggestions** (Year 2+)
   - Generate actual code changes (insert EventChainHead, create adapters)
   - One-click fixes for common patterns
   - Requires deep code generation capability

5. **Multi-Application Analysis** (Year 2+)
   - Analyze multiple applications sharing same dPAC
   - Aggregate load across multi-tenant scenarios
   - Total system capacity planning

---

## References

- [SE Application Design Guidelines (EIO0000004686.06)](../../EAE_ADG/) - Official SE documentation on event storms and performance
- [EAE Concepts Primer](../eae-skill-router/references/EAE_CONCEPTS_PRIMER.md) - IEC 61499 fundamentals
- [Event Storm Patterns](references/event-storm-patterns.md) - Detailed anti-pattern catalog
- [Performance Thresholds](references/performance-thresholds.md) - Threshold calibration rationale
- [Script Implementation Details](references/script-implementation.md) - Algorithm details for scripts

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| eae-basic-fb | Analyzed by this skill (event generation patterns) |
| eae-composite-fb | Analyzed by this skill (network complexity) |
| eae-cat | Analyzed by this skill (cross-communication patterns) |
| eae-adapter | Analyzed by this skill (bidirectional event flow) |
| eae-skill-router | Orchestrates this skill after artifact creation |

---

## Changelog

### v1.0.0 (2026-01-20)
- Initial release
- 4-dimensional analysis (event flow, CPU load, queue depth, anti-patterns)
- 4 autonomous Python scripts with full agentic capabilities
- Multi-format reporting (JSON, Markdown, Graphviz)
- Integration with existing EAE skill ecosystem
- Timelessness score: 9/10 (based on IEC 61499 fundamentals)
