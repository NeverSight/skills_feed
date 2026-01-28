---
name: perf
description: Performance profiling and optimization. Use for benchmarking code, analyzing performance, running Lighthouse audits, and finding hotspots.
---

# Performance Profiler

Profile, benchmark, and optimize code performance.

## Prerequisites

```bash
# Node.js for profiling
node --version

# Lighthouse for web perf
npm install -g lighthouse

# Gemini for analysis
pip install google-generativeai
export GEMINI_API_KEY=your_api_key
```

## Benchmarking

### Quick Benchmark

```bash
# Time a Node.js script
time node script.js

# With memory
/usr/bin/time -l node script.js  # macOS
/usr/bin/time -v node script.js  # Linux
```

### Node.js Performance Hooks

```javascript
// benchmark.js
const { performance, PerformanceObserver } = require('perf_hooks');

const obs = new PerformanceObserver((list) => {
  console.log(list.getEntries()[0].duration);
});
obs.observe({ entryTypes: ['measure'] });

performance.mark('start');
// Code to benchmark
yourFunction();
performance.mark('end');
performance.measure('duration', 'start', 'end');
```

### Console Timing

```javascript
console.time('operation');
// Code to time
console.timeEnd('operation');  // Prints: operation: 123.456ms
```

## Node.js Profiling

### V8 Profiler

```bash
# Generate profile
node --prof script.js

# Process the log
node --prof-process isolate-*.log > profile.txt
```

### Inspect Mode

```bash
# Start with inspector
node --inspect script.js

# Break on start
node --inspect-brk script.js

# Open Chrome DevTools
open chrome://inspect
```

### Memory Profiling

```bash
# Heap snapshot
node --heapsnapshot-signal=SIGUSR2 script.js
# Then: kill -USR2 <pid>

# Expose GC for testing
node --expose-gc script.js
```

## Lighthouse Audits

### Basic Audit

```bash
# Full audit
lighthouse https://example.com

# Output to JSON
lighthouse https://example.com --output=json --output-path=report.json

# Output to HTML
lighthouse https://example.com --output=html --output-path=report.html

# Specific categories
lighthouse https://example.com --only-categories=performance

# Mobile vs Desktop
lighthouse https://example.com --preset=desktop
lighthouse https://example.com --preset=mobile  # default
```

### Performance Only

```bash
lighthouse https://example.com \
  --only-categories=performance \
  --output=json \
  --output-path=perf-report.json
```

### Chrome Flags

```bash
# Headless
lighthouse https://example.com --chrome-flags="--headless"

# Custom viewport
lighthouse https://example.com --chrome-flags="--window-size=1920,1080"
```

## AI Performance Analysis

### Analyze Code for Performance

```bash
CODE=$(cat slow-function.ts)

gemini -m pro -o text -e "" "Analyze this code for performance issues:

$CODE

Identify:
1. Time complexity issues
2. Memory leaks or bloat
3. Unnecessary operations
4. Opportunities for optimization
5. Caching opportunities

Provide specific recommendations with code examples."
```

### Analyze Profile Output

```bash
PROFILE=$(cat profile.txt)

gemini -m pro -o text -e "" "Analyze this Node.js profile:

$PROFILE

Identify:
1. Hot functions (most time spent)
2. Potential bottlenecks
3. Optimization opportunities
4. Priority of fixes"
```

## Finding Hotspots

### CPU Hotspots

```bash
# Record CPU profile
node --cpu-prof script.js

# Analyze generated .cpuprofile
# Open in Chrome DevTools or use:
npx speedscope *.cpuprofile
```

### Memory Hotspots

```bash
# Find large objects
node --heapsnapshot-signal=SIGUSR2 app.js

# Use clinic.js
npx clinic doctor -- node script.js
npx clinic flame -- node script.js
npx clinic bubbleprof -- node script.js
```

### Bundle Analysis

```bash
# Webpack
npx webpack-bundle-analyzer stats.json

# Vite
npx vite build --report

# Generic
du -sh dist/*
ls -lhS dist/*.js
```

## Common Patterns

### Anti-Patterns to Check

```bash
gemini -m pro -o text -e "" "Check this code for common performance anti-patterns:

$(cat src/*.ts)

Look for:
- Synchronous I/O in hot paths
- Repeated DOM queries
- Unnecessary re-renders
- N+1 query patterns
- Memory leaks in closures
- Blocking the event loop"
```

### Optimization Checklist

```bash
gemini -m pro -o text -e "" "Create a performance optimization checklist for:

Application type: [web app / API / CLI]
Stack: [your stack]
Current issues: [symptoms]

Include priority order and estimated impact."
```

## Comparison Benchmarks

### Before/After

```bash
#!/bin/bash
# benchmark-compare.sh

echo "=== Before optimization ==="
git checkout main
npm install
time npm run benchmark

echo "=== After optimization ==="
git checkout optimization-branch
npm install
time npm run benchmark
```

### A/B Script

```bash
#!/bin/bash
# Run same benchmark multiple times
for i in {1..10}; do
  echo "Run $i:"
  node benchmark.js
done | tee results.txt

# Calculate average
grep "time:" results.txt | awk '{sum+=$2; n++} END {print "Average:", sum/n}'
```

## Best Practices

1. **Measure first** - Don't optimize without data
2. **Profile production** - Dev performance differs
3. **Automate benchmarks** - Track over time
4. **Focus on hot paths** - 80/20 rule
5. **Test on target devices** - Especially mobile
6. **Monitor after deploy** - Verify improvements
7. **Document baselines** - Know what "good" looks like
