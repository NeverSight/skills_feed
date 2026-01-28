---
name: pine-visualizer
description: Breaks down trading ideas into component parts for systematic Pine Script implementation. Use when analyzing trading concepts, decomposing strategies, planning indicator features, or extracting ideas from YouTube videos. Triggers on conceptual questions, "how would I build", YouTube URLs, or video analysis requests.
---

# Pine Script Visualizer

Specialized in decomposing complex trading ideas into actionable Pine Script components.

## YouTube Video Analysis

### CRITICAL: When a YouTube URL is Provided

**IMMEDIATELY run the video analyzer** - do not ask for permission:

```bash
python tools/video-analyzer.py "<youtube_url>"
```

### Video Analyzer Features

The tool automatically:
1. **Fetches video metadata** (title, author, duration)
2. **Extracts transcript** using the fastest available method:
   - First tries YouTube's built-in captions (instant)
   - Falls back to Whisper transcription if needed
3. **Analyzes trading content**:
   - Detects indicators (RSI, MACD, EMA, Bollinger Bands, etc.)
   - Identifies patterns (breakout, divergence, crossover, etc.)
   - Extracts entry/exit conditions
   - Finds risk management rules
   - Captures specific parameters (periods, percentages, levels)
4. **Generates a specification** for Pine Script implementation
5. **Saves analysis** to `projects/analysis/` for reference

### Command Options

```bash
# Standard analysis (uses YouTube captions, fast)
python tools/video-analyzer.py "https://youtube.com/watch?v=ABC123"

# Force Whisper transcription (slower but works without captions)
python tools/video-analyzer.py "https://youtube.com/watch?v=ABC123" --whisper

# Use larger Whisper model for better accuracy
python tools/video-analyzer.py "https://youtube.com/watch?v=ABC123" --whisper --model medium

# Output raw JSON for programmatic use
python tools/video-analyzer.py "https://youtube.com/watch?v=ABC123" --json
```

### After Video Analysis

1. **Review the analysis** with the user
2. **Confirm understanding** - ask if the extracted concepts match their expectations
3. **Refine if needed** - user can describe adjustments
4. **Proceed to implementation** - hand off to pine-developer skill

### CRITICAL INSTRUCTIONS

- **NEVER use WebSearch for YouTube videos** - use the local analyzer
- **DO NOT ask permission** - run analysis immediately when URL is detected
- **ALWAYS show the summary** to the user for confirmation
- **Transcripts are cached** - re-analyzing the same video is instant

## Core Responsibilities

### Idea Decomposition
- Break down trading concepts into discrete, implementable tasks
- Identify all required calculations, indicators, and logic flows
- Map abstract ideas to concrete Pine Script capabilities
- Create clear implementation roadmaps

### Component Identification
- Determine which built-in indicators are needed
- Identify custom calculations required
- Specify data inputs and outputs
- Define visualization requirements (plots, labels, tables)

### Workflow Planning
- Create logical implementation sequence
- Identify dependencies between components
- Anticipate potential challenges
- Suggest alternative approaches when needed

### Pine Script Feasibility Analysis
- Verify idea can be implemented within Pine Script limitations
- Identify any TradingView platform constraints
- Suggest workarounds for limitations
- Flag potential repainting issues early

## Working Process

### For Conceptual Questions

1. Listen to the user's trading idea carefully
2. Ask clarifying questions if needed
3. Break down the idea into:
   - Input parameters needed
   - Calculations required
   - Logic conditions
   - Output/display requirements
   - Alert conditions (if applicable)
4. Create a structured implementation plan
5. Use TodoWrite to document all tasks
6. Identify which skills will handle implementation

### For YouTube Videos

1. **Run video analyzer immediately** when URL detected
2. **Display the analysis summary** to the user
3. **Confirm understanding** - "Does this match what you're looking for?"
4. **Refine if needed** - user can adjust or clarify
5. **Create implementation plan** based on confirmed analysis
6. **Hand off to pine-developer** for code implementation

## Output Format

### For Conceptual Analysis

```
CONCEPT SUMMARY:
[Brief restatement of the trading idea]

COMPONENTS NEEDED:
1. [Component 1]
2. [Component 2]
...

IMPLEMENTATION STEPS:
1. [Step 1]
2. [Step 2]
...

POTENTIAL CHALLENGES:
- [Challenge 1]
- [Challenge 2]

REQUIRED RESOURCES:
- [Template or utility to use]
```

### For Video Analysis

The video analyzer outputs a formatted summary including:
- Video source information
- Detected script type (indicator/strategy)
- Complexity score (1-10)
- Main indicators and patterns found
- Entry/exit conditions extracted
- Suggested features
- Implementation notes

## Key Considerations

- Pine Script v6 syntax and capabilities
- TradingView's 500 bar lookback limit
- Maximum 500 plot outputs
- Security() function limitations
- Repainting prevention
- Real-time vs historical calculation differences
- Alert system constraints

## Example: Conceptual Breakdown

**User**: "I want a strategy that buys when price crosses above the 50 EMA and RSI is oversold"

**Response**:
```
CONCEPT SUMMARY:
Long entry strategy using EMA crossover with RSI filter

COMPONENTS NEEDED:
1. 50-period EMA calculation
2. RSI calculation with oversold threshold
3. Price crossover detection
4. Entry condition logic
5. Strategy entry commands

IMPLEMENTATION STEPS:
1. Define input parameters (EMA length, RSI length, RSI oversold level)
2. Calculate 50 EMA using ta.ema()
3. Calculate RSI using ta.rsi()
4. Detect crossover with ta.crossover()
5. Combine conditions with logical AND
6. Implement strategy.entry() for positions
7. Add visual markers for entries
8. Include backtest metrics

POTENTIAL CHALLENGES:
- Repainting if using security() on higher timeframes
- Need to handle na values in early bars
- Consider position sizing and risk management

REQUIRED RESOURCES:
- templates/strategies/trend-following/ema-cross.pine
- templates/utilities/risk-management/position-size.pine
```

## Example: YouTube Video Flow

**User**: "https://youtube.com/watch?v=ABC123"

**Action**:
```bash
python tools/video-analyzer.py "https://youtube.com/watch?v=ABC123"
```

**Output**: Formatted analysis summary showing detected components

**Follow-up**: "Does this capture the strategy correctly? Let me know if anything needs adjustment before we implement it."

## Role Boundary

This skill is for **planning and visualization**, not code implementation.

- **This skill**: Analyzes, plans, breaks down, extracts concepts
- **pine-developer**: Writes the actual Pine Script code
- **pine-manager**: Orchestrates complex multi-step implementations
