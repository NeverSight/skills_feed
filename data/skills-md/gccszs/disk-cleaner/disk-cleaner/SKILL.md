---
name: disk-cleaner
description: "High-performance cross-platform disk space monitoring, analysis, and cleaning toolkit with v2.0 optimization enhancements. Use when Claude needs to: (1) Analyze disk space usage and identify large files/directories consuming space, (2) Clean temporary files, caches, logs, and other junk files safely, (3) Monitor disk usage with configurable warning/critical thresholds, (4) Generate detailed reports on disk health and cleanup recommendations. Features advanced optimization: 3-5x faster scanning with os.scandir(), concurrent multi-threaded I/O, intelligent sampling for large directories, memory-adaptive processing, and cross-platform compatibility (Windows/macOS/Linux). Specializes in Windows C drive cleanup while maintaining full compatibility with Unix systems. Provides interactive CLI, automated scripts, detailed reporting modes, and comprehensive test coverage (244 tests). All operations prioritize safety with built-in protection for system files."
---

# Disk Cleaner Skill v2.0

High-performance cross-platform disk management toolkit with advanced optimization features for monitoring, analyzing, and cleaning disk space safely.

## 🚀 What's New in v2.0

### Performance Enhancements
- **3-5x faster scanning** with os.scandir() optimization
- **Concurrent multi-threaded scanning** for I/O-bound operations
- **Intelligent sampling** with QuickProfiler (estimates in 0.5-1s instead of full scan)
- **Memory-adaptive processing** with automatic memory monitoring
- **Optimized duplicate detection** with parallel hashing and caching

### Reliability Improvements
- **244 comprehensive tests** across all platforms
- **Cross-platform compatibility** verified on Windows, macOS, Linux
- **Python 3.8-3.12 support** with full test coverage
- **Robust error handling** for permission issues and edge cases
- **Graceful degradation** when scanning protected directories

## Quick Start

### Analyze Disk Space

```bash
# Analyze current drive (C:\ on Windows, / on Unix)
python scripts/analyze_disk.py

# Analyze specific path
python scripts/analyze_disk.py --path "D:\Projects"

# Get top 50 largest items
python scripts/analyze_disk.py --top 50

# Output as JSON
python scripts/analyze_disk.py --json

# Save report
python scripts/analyze_disk.py --output disk_report.json
```

### Clean Junk Files

```bash
# Dry run (default - safe simulation)
python scripts/clean_disk.py --dry-run

# Actually clean files (use --force)
python scripts/clean_disk.py --force

# Clean specific category
python scripts/clean_disk.py --temp       # Clean temp files only
python scripts/clean_disk.py --cache      # Clean cache only
python scripts/clean_disk.py --logs       # Clean logs only
python scripts/clean_disk.py --recycle    # Clean recycle bin only
python scripts/clean_disk.py --downloads 90  # Clean downloads older than 90 days
```

### Monitor Disk Usage

```bash
# Check current status
python scripts/monitor_disk.py

# Continuous monitoring (every 60 seconds)
python scripts/monitor_disk.py --watch

# Custom thresholds
python scripts/monitor_disk.py --warning 70 --critical 85

# Alert mode (CI/CD friendly)
python scripts/monitor_disk.py --alerts-only

# Custom monitoring interval
python scripts/monitor_disk.py --watch --interval 300
```

## Performance Features

### High-Speed Scanning
The scanner uses advanced optimizations for rapid directory traversal:

- **os.scandir() optimization**: 3-5x faster than Path.glob/iterdir()
- **Bounded queue processing**: Efficient concurrent scanning
- **Adaptive worker threads**: CPU count × 4 for I/O-bound operations
- **Smart path exclusion**: Skip system directories automatically

### Intelligent Sampling (QuickProfiler)
For large directories, use sampling to get instant estimates:

```python
from diskcleaner.optimization.scan import QuickProfiler

profiler = QuickProfiler(sample_time=1.0)  # 1 second sampling
profile = profiler.profile(path)  # Returns: estimated file count, size, depth, time

# Example output for 442K files:
# - Estimated: 450,000 files (within 2%)
# - Estimated scan time: 14 seconds
# - Actual scan time: 14 seconds
```

### Memory Management
Automatic memory monitoring prevents system overload:

```python
from diskcleaner.optimization.memory import MemoryMonitor

monitor = MemoryMonitor(threshold_mb=1000)
if monitor.should_pause():
    # Reduce concurrency
    workers = monitor.get_optimal_workers(current_workers)
```

## Script Reference

### analyze_disk.py

Main disk analysis tool that identifies space consumption patterns.

**Key capabilities:**
- High-speed scanning with os.scandir() (3-5x faster)
- Scan large directories (100K+ files) in seconds
- Cross-platform path exclusion (Windows/macOS/Linux)
- Detailed statistics and reports

**Common use cases:**
```
"Analyze my C drive and show what's taking up space"
"What are the largest directories in my home folder?"
"Show me temp files taking up space"
"Scan this 400GB directory quickly"
```

### clean_disk.py

Safe junk file removal with multiple safety mechanisms.

**Safety features:**
- Protected paths (never deletes system directories)
- Protected extensions (never deletes executables)
- Dry-run mode by default
- Detailed logging of all operations
- Handles empty categories gracefully

**Categories cleaned:**
- **temp**: Temporary files (%TEMP%, /tmp, etc.)
- **cache**: Application and browser caches
- **logs**: Log files (older than 30 days default)
- **recycle**: Recycle bin / trash
- **downloads**: Old download files (configurable age)

**Important:** Always run with `--dry-run` first to preview changes.

### monitor_disk.py

Continuous or one-shot disk usage monitoring.

**Features:**
- Multi-drive monitoring (all mount points)
- Configurable warning/critical thresholds
- Continuous monitoring mode with alerts
- JSON output for automation
- Non-zero exit codes for CI/CD integration

**Exit codes:**
- 0: All drives OK
- 1: Warning threshold exceeded
- 2: Critical threshold exceeded

## Platform-Specific Information

See [temp_locations.md](references/temp_locations.md) for:
- Complete list of temporary file locations by platform
- Browser cache locations
- Development tool caches
- Safety guidelines for each platform

**Platform-specific optimizations:**
- **Windows**: Excludes C:\Windows, C:\Program Files, etc.
- **macOS**: Excludes /System, /Library, /private/var/vm (VM swap)
- **Linux**: Excludes /proc, /sys, /dev, /run

**When to read this file:**
- User asks about specific platform cleanup locations
- Need to understand what gets cleaned on each OS
- Customizing cleanup for specific applications

## Safety Rules

The scripts implement multiple safety layers:

1. **Protected Paths**: System directories never touched
2. **Protected Extensions**: Executables and system files protected
3. **Dry Run Default**: Must use `--force` for actual deletion
4. **Age Filters**: Logs cleaned only after 30+ days
5. **Error Handling**: Permission errors don't stop execution
6. **Graceful Degradation**: Handles edge cases (empty categories, missing paths)

**Protected extensions:**
```
.exe, .dll, .sys, .drv, .bat, .cmd, .ps1, .sh, .bash, .zsh,
.app, .dmg, .pkg, .deb, .rpm, .msi, .iso, .vhd, .vhdx
```

## Typical Workflows

### Workflow 1: Investigate and Clean

When user says "My C drive is full":

1. Analyze current state: `python scripts/analyze_disk.py`
2. Preview cleanup: `python scripts/clean_disk.py --dry-run`
3. Review report, confirm with user
4. Execute cleanup: `python scripts/clean_disk.py --force`
5. Verify results: `python scripts/analyze_disk.py`

### Workflow 2: Continuous Monitoring

For proactive disk management:

1. Start monitor: `python scripts/monitor_disk.py --watch --interval 300`
2. Set appropriate thresholds: `--warning 70 --critical 85`
3. Monitor alerts and take action when needed

### Workflow 3: Large-Scale Analysis (NEW)

For analyzing large directories (100K+ files):

```bash
# Use intelligent sampling for quick estimates
python scripts/analyze_disk.py --path "D:\Large\Project" --sample

# Full scan if needed
python scripts/analyze_disk.py --path "D:\Large\Project" --full

# Performance: Can scan 442K files in ~14 seconds
```

### Workflow 4: One-Time Deep Clean

For thorough cleanup:

```bash
# Preview all cleaning
python scripts/clean_disk.py --dry-run

# If satisfied, execute
python scripts/clean_disk.py --force

# Analyze results
python scripts/analyze_disk.py
```

## Output Formats

### Interactive Mode (Default)
Human-readable console output with:
- Visual progress bars
- Emoji indicators for status
- Formatted tables

### JSON Mode
Machine-readable output for:
- Automation pipelines
- Log aggregation
- Further processing

Use `--json` flag with any script.

### Report Files
Save detailed reports with `--output report.json` for:
- Historical tracking
- Comparison over time
- Audit trails

## Advanced Usage

### Python API

For integration with other tools:

```python
from diskcleaner.core import DirectoryScanner, SmartCleanupEngine

# Scan directory
scanner = DirectoryScanner("/path/to/scan")
files = scanner.scan()

# Analyze and get recommendations
engine = SmartCleanupEngine("/path/to/scan")
report = engine.analyze()

# Clean with safety checks
results = engine.clean(
    categories=["temp", "cache", "logs"],
    dry_run=True  # Set False to actually delete
)
```

### Performance Optimization

For maximum performance on large directories:

```python
from diskcleaner.optimization.scan import ConcurrentScanner, QuickProfiler

# Quick profiling first
profiler = QuickProfiler(sample_time=1.0)
profile = profiler.profile(large_path)

print(f"Estimated: {profile.file_count:,} files")
print(f"Estimated time: {profile.estimated_time:.1f}s")

# Full concurrent scan if needed
if profile.file_count < 100000:
    scanner = ConcurrentScanner()
    result = scanner.scan(large_path)
```

## Testing

Comprehensive test suite ensures reliability:

- **244 tests** covering all functionality
- **Cross-platform**: Windows, macOS, Linux
- **All Python versions**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Performance benchmarks**: Validate optimization improvements
- **Integration tests**: End-to-end workflows

Run tests:
```bash
# Run all tests
pytest tests/

# Run specific test category
pytest tests/test_optimization.py
pytest tests/benchmarks/

# With coverage
pytest tests/ --cov=diskcleaner --cov-report=html
```

## Troubleshooting

### Permission Errors
The scanner handles permission errors gracefully. Protected directories are automatically skipped on each platform:
- **Windows**: C:\Windows, C:\Program Files
- **macOS**: /System, /Library, /private/var/vm
- **Linux**: /proc, /sys, /dev

### Performance Issues
If scanning seems slow:
1. Check if path is network drive (slower than local)
2. Verify anti-virus isn't scanning every file access
3. Use `--sample` flag for quick estimates on large directories

### Empty Results
If no files found:
1. Check path exists and is accessible
2. Verify files aren't all protected (system directories)
3. Run with higher verbosity to see what's being scanned

## Contributing

To modify or extend the toolkit:

1. **Optimization modules**: `diskcleaner/optimization/`
   - `scan.py`: ConcurrentScanner, QuickProfiler
   - `hash.py`: AdaptiveHasher, DuplicateFinder
   - `delete.py`: BatchDeleter, AsyncDeleter
   - `memory.py`: MemoryMonitor
   - `profiler.py`: PerformanceProfiler

2. **Core modules**: `diskcleaner/core/`
   - `scanner.py`: DirectoryScanner with os.scandir()
   - `smart_cleanup.py`: SmartCleanupEngine
   - Other core components

3. **Platform-specific**: `diskcleaner/platforms/`
   - Windows, macOS, Linux implementations

4. **Tests**: `tests/`
   - Unit tests for all components
   - Performance benchmarks
   - Cross-platform tests

5. **Scripts**: `scripts/`
   - User-facing CLI tools

Always run tests after changes:
```bash
pytest tests/ -v
pre-commit run --all-files
```

## License

MIT License - See LICENSE file for details.
