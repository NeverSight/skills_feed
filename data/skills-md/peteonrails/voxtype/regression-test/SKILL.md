---
name: regression-test
description: Run regression tests for voxtype releases. Use before major releases to verify core functionality, CLI commands, and configuration handling.
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# Regression Test

Comprehensive testing checklist for voxtype releases.

**Note:** For detailed manual smoke tests (recording cycles, GPU isolation, output drivers, etc.), see [docs/SMOKE_TESTS.md](docs/SMOKE_TESTS.md). Run those tests for thorough pre-release validation.

## Quick Smoke Test

```bash
# Build and basic checks
cargo build --release
./target/release/voxtype --version
./target/release/voxtype --help
./target/release/voxtype setup --help
```

## Unit Tests

```bash
cargo test
```

Key test modules:
- `text::` - Spoken punctuation and replacements
- `cli::` - Command-line argument parsing
- `state::` - State machine transitions

## CLI Command Tests

### Setup Commands

```bash
# List available models
./target/release/voxtype setup --list-models

# Show current configuration
./target/release/voxtype setup --show-config

# Check GPU detection (if available)
./target/release/voxtype setup gpu --status
```

### Status Commands

```bash
# Check daemon status (will fail if not running, that's ok)
timeout 2 ./target/release/voxtype status || echo "Daemon not running (expected)"

# JSON output format
timeout 2 ./target/release/voxtype status --format json || echo "Daemon not running (expected)"
```

### Transcription Test

```bash
# Test with a sample audio file (if available)
./target/release/voxtype transcribe test.wav
```

## Configuration Tests

### Default Config Loading

```bash
# Should not error with missing config
rm -f ~/.config/voxtype/config.toml
./target/release/voxtype --help

# Should load config without errors
mkdir -p ~/.config/voxtype
cp config/default.toml ~/.config/voxtype/config.toml
./target/release/voxtype setup --show-config
```

### Config Backwards Compatibility

Test that old config files still work:

```bash
# Create minimal old-style config
cat > /tmp/test-config.toml << 'EOF'
[hotkey]
key = "SCROLLLOCK"

[whisper]
model = "base.en"
EOF

# Should not error
./target/release/voxtype --config /tmp/test-config.toml --help
```

## Binary Variant Tests

For each binary variant, verify:

```bash
VERSION=0.4.14

# AVX2
releases/${VERSION}/voxtype-${VERSION}-linux-x86_64-avx2 --version
releases/${VERSION}/voxtype-${VERSION}-linux-x86_64-avx2 --help

# AVX-512
releases/${VERSION}/voxtype-${VERSION}-linux-x86_64-avx512 --version
releases/${VERSION}/voxtype-${VERSION}-linux-x86_64-avx512 --help

# Vulkan
releases/${VERSION}/voxtype-${VERSION}-linux-x86_64-vulkan --version
releases/${VERSION}/voxtype-${VERSION}-linux-x86_64-vulkan --help
```

## Integration Tests

### Daemon Lifecycle

```bash
# Start daemon
./target/release/voxtype &
DAEMON_PID=$!
sleep 2

# Check it's running
./target/release/voxtype status

# Stop daemon
kill $DAEMON_PID
```

### Signal Handling

```bash
./target/release/voxtype &
DAEMON_PID=$!
sleep 1

# SIGUSR1 should start recording (will fail without audio, ok)
kill -USR1 $DAEMON_PID

# SIGTERM should graceful shutdown
kill -TERM $DAEMON_PID
```

## Package Tests

### Debian Package

```bash
# Validate structure
dpkg-deb --info releases/${VERSION}/voxtype_${VERSION}-1_amd64.deb

# List contents
dpkg-deb --contents releases/${VERSION}/voxtype_${VERSION}-1_amd64.deb

# Check for required files
dpkg-deb --contents releases/${VERSION}/voxtype_${VERSION}-1_amd64.deb | grep -E 'voxtype-avx2|voxtype-avx512|config.toml|voxtype.service'
```

### RPM Package

```bash
rpm -qp --info releases/${VERSION}/voxtype-${VERSION}-1.x86_64.rpm
rpm -qp --list releases/${VERSION}/voxtype-${VERSION}-1.x86_64.rpm
```

## Checklist for Major Releases

- [ ] `cargo test` passes
- [ ] `cargo clippy` has no warnings
- [ ] All binary variants build successfully
- [ ] Binary instruction validation passes (no AVX-512 in AVX2/Vulkan)
- [ ] Version numbers match across all binaries
- [ ] CLI --help output is correct
- [ ] Default config loads without errors
- [ ] Old configs still work (backwards compatibility)
- [ ] Packages install correctly on target distros
- [ ] Daemon starts and stops cleanly
- [ ] Recording/transcription works end-to-end (manual test)

## Known Test Limitations

- Audio capture requires real audio hardware (can't fully test in CI)
- evdev hotkey detection requires `/dev/input` access
- Transcription requires downloaded Whisper model
- GPU acceleration requires Vulkan-capable hardware
