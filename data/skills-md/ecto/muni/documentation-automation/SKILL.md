---
name: documentation-automation
description: Automatically maintains project documentation including CHANGELOG.md, README files, inline code documentation, and cross-references. Use proactively after implementing features, fixing bugs, making API changes, or completing significant work. Updates CHANGELOG.md with conventional commit format, adds README sections for new features, generates inline documentation for new functions/structs/components, and ensures documentation cross-references are up-to-date. Covers Rust doc comments, TypeScript JSDoc, conventional commits (feat/fix/docs/refactor/test/chore), and multi-level README organization.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Documentation Automation Skill

This skill proactively maintains project documentation as you work, ensuring that changes are properly documented across CHANGELOG.md, README files, and inline code comments.

## When This Skill Is Used

**Automatically trigger this skill** (proactively offer to use it) after:
- ✅ Implementing a new feature
- ✅ Fixing a bug
- ✅ Making breaking changes
- ✅ Adding new API endpoints or functions
- ✅ Refactoring significant code
- ✅ Completing a user story or task
- ✅ Before creating a git commit for significant work

**Do NOT trigger for**:
- Minor typo fixes (unless in documentation itself)
- Work in progress (not yet complete)
- Trivial code cleanup with no functional impact

## Documentation Strategy

### 1. CHANGELOG.md (Primary)

**Location**: Root `/Users/cam/Developer/muni/CHANGELOG.md`

**Format**: Conventional Commits with semantic versioning

**Entry Structure**:
```markdown
## [Unreleased]

### Added
- New feature description with reference to files changed (e.g., bvr/firmware/crates/control/src/lib.rs:150-180)
- Another feature with link to relevant documentation

### Changed
- Modified behavior with migration notes if breaking
- Updated API with before/after examples

### Fixed
- Bug fix description with issue reference if applicable (#123)

### Deprecated
- Feature scheduled for removal with timeline

### Removed
- Removed feature with migration path

### Security
- Security fix (never include vulnerability details)
```

**Conventional Commit Prefixes**:
- `feat`: New feature (user-facing)
- `fix`: Bug fix
- `docs`: Documentation only
- `refactor`: Code restructuring (no behavior change)
- `perf`: Performance improvement
- `test`: Add/update tests
- `chore`: Tooling, dependencies, build config
- `style`: Code style (formatting, no logic change)
- `ci`: CI/CD changes
- `build`: Build system changes

**Key Points**:
- [ ] Entries go under `## [Unreleased]` until versioned
- [ ] Use present tense ("Add feature", not "Added feature")
- [ ] Include file paths for easy navigation
- [ ] Group related changes together
- [ ] Reference issue numbers with `#123`
- [ ] Breaking changes get `### Changed` with migration notes

**Example Entry**:
```markdown
## [Unreleased]

### Added
- Safety watchdog with 500ms timeout in `bvr/firmware/crates/control/src/lib.rs` to automatically transition to Idle mode when commands stop arriving
- E-stop state machine transitions in `bvr/firmware/crates/state/src/lib.rs` requiring explicit release before resuming operation
- LED feedback for rover modes: green pulse (teleop), cyan pulse (autonomous), red flash (e-stop)

### Fixed
- CAN bus frame parsing now includes bounds checking in `bvr/firmware/crates/can/src/vesc.rs:167-191` to prevent panics on malformed frames (#42)
```

**See**: [changelog-format.md](changelog-format.md) for complete formatting guide.

### 2. README Files (Feature-Specific)

**Strategy**: Update appropriate README based on scope of change.

**README Hierarchy**:
```
/README.md                          # Project overview, quick start
/bvr/README.md                      # BVR rover-specific
/bvr/firmware/README.md             # Firmware development guide
/bvr/cad/README.md                  # CAD system usage
/depot/README.md                    # Depot services overview
/depot/console/README.md            # Console frontend development
/mcu/README.md                      # MCU firmware guide
```

**What to Update**:
- **Features List**: Add new capabilities to feature lists
- **Getting Started**: Update installation/setup steps if changed
- **API Documentation**: Document new endpoints, functions, or interfaces
- **Configuration**: Add new config options with examples
- **Examples**: Add usage examples for new features
- **Troubleshooting**: Add known issues and solutions

**README Update Rules**:
- [ ] Keep consistent tone and formatting with existing README
- [ ] Add to existing sections (don't create duplicates)
- [ ] Include code examples for complex features
- [ ] Link to detailed documentation files if lengthy
- [ ] Update table of contents if present

**Example README Addition**:
```markdown
### Safety Features

#### Watchdog Timer
The control system includes a command watchdog that monitors teleop connection health. If no commands are received for 500ms, the rover automatically transitions to Idle mode and stops all motors.

Configuration in `bvr/firmware/config/bvr.toml`:
```toml
[control]
command_timeout_ms = 500
```

See `bvr/firmware/crates/control/src/lib.rs` for implementation details.
```

### 3. Inline Documentation

**Rust Documentation Comments**:

**Module-level** (`//!` at top of `lib.rs`):
```rust
//! State machine and mode management for bvr.
//!
//! This module implements the rover's operational modes (Disabled, Idle, Teleop,
//! Autonomous, EStop, Fault) with safety-critical transition logic. The state
//! machine ensures that e-stop requires explicit release and that invalid
//! transitions are rejected.
//!
//! # Examples
//!
//! ```
//! let mut sm = StateMachine::new();
//! sm.handle(Event::Enable);
//! assert_eq!(sm.mode(), Mode::Idle);
//! ```
//!
//! # Safety
//!
//! E-stop transitions are one-way and require explicit `EStopRelease` event.
//! Always check `is_driving()` before sending motor commands.
```

**Function-level** (`///`):
```rust
/// Handles a state machine event and transitions to a new mode if valid.
///
/// # Arguments
///
/// * `event` - The event to process (Enable, Disable, EStop, etc.)
///
/// # Examples
///
/// ```
/// let mut sm = StateMachine::new();
/// sm.handle(Event::Enable);
/// assert_eq!(sm.mode(), Mode::Idle);
/// ```
///
/// # Safety
///
/// E-stop events are accepted from any mode but require explicit release.
pub fn handle(&mut self, event: Event) {
    // ...
}
```

**Struct/Enum-level**:
```rust
/// Represents the rover's current operational mode.
///
/// The mode determines which operations are permitted. Use `is_driving()`
/// to check if motor commands should be sent, and `is_safe()` to check
/// if configuration changes are allowed.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Mode {
    /// Motors disabled, awaiting initialization
    Disabled,
    /// Ready state, motors enabled but stationary
    Idle,
    /// Under human control via teleop
    Teleop,
    /// Autonomous navigation active
    Autonomous,
    /// Emergency stop, requires explicit release
    EStop,
    /// Error state, requires fault clear
    Fault,
}
```

**TypeScript/React Documentation** (JSDoc):

**Function/Component**:
```typescript
/**
 * Manages WebSocket connection to rover for real-time teleoperation.
 *
 * Handles binary protocol encoding/decoding, automatic reconnection with
 * exponential backoff, and connection state management.
 *
 * @param address - WebSocket address (e.g., "ws://rover:4850")
 * @returns Connection state and send function
 *
 * @example
 * ```typescript
 * const { connected, send } = useRoverConnection();
 * if (connected) {
 *   send(encodeTwist({ linear: 1.0, angular: 0.0, boost: false }));
 * }
 * ```
 */
export function useRoverConnection(address: string) {
  // ...
}
```

**Interface**:
```typescript
/**
 * Telemetry data received from rover at 20 Hz.
 *
 * Contains current operational mode, pose, velocity, power status,
 * and temperature readings for all motors and controllers.
 */
export interface Telemetry {
  /** Current operational mode (Idle, Teleop, etc.) */
  mode: Mode;
  /** Position and heading in world frame */
  pose: Pose;
  /** Current velocity command */
  velocity: Twist;
  /** Battery voltage and current */
  power: PowerStatus;
  /** Motor and controller temperatures (°C) */
  temperatures: TempStatus;
}
```

**When to Add Inline Documentation**:
- [ ] All public functions/methods (Rust `pub fn`, TypeScript `export`)
- [ ] All public structs/enums/interfaces
- [ ] All public modules (Rust `lib.rs`)
- [ ] Complex algorithms requiring explanation
- [ ] Safety-critical functions (always document safety invariants)
- [ ] Functions with non-obvious behavior

**When NOT to Add**:
- Private implementation details (unless complex)
- Self-explanatory getters/setters
- Trivial functions (<5 lines, obvious purpose)

### 4. Cross-References and Links

**Update cross-references** when:
- Moving functions between files
- Renaming modules or functions
- Adding new related documentation
- Splitting files

**Files with Cross-References**:
- `/Users/cam/Developer/muni/CLAUDE.md` - Project overview (central reference)
- `README.md` files - Link to detailed docs
- Skill supporting docs - Reference CLAUDE.md and other skills

**Cross-Reference Patterns**:
```markdown
<!-- Markdown links -->
See [firmware architecture](bvr/firmware/README.md) for details.
Refer to [safety checklist](.claude/skills/firmware-review/safety-checklist.md).

<!-- File path references -->
Implementation: `bvr/firmware/crates/state/src/lib.rs:50-120`

<!-- Code references with line numbers -->
The watchdog is implemented in bvr/firmware/crates/control/src/lib.rs:162-193
```

### 5. Detection Logic

**Automatically detect what needs documentation**:

**Check for new public APIs**:
```bash
# Rust: Find pub fn without ///
grep -rn "pub fn" --include="*.rs" | grep -v "///"

# Rust: Find pub struct without ///
grep -rn "pub struct" --include="*.rs" | grep -v "///"

# TypeScript: Find export function without /**
grep -rn "export function" --include="*.ts" --include="*.tsx" | grep -v "/\*\*"
```

**Check for missing CHANGELOG entries**:
```bash
# Recent commits not in CHANGELOG
git log --since="1 week ago" --pretty=format:"%s" | grep -v "docs:" | grep -v "chore:"
```

**Check for outdated documentation**:
- Files modified recently but README not updated (check git timestamps)
- New features implemented but no example code
- Breaking changes without migration notes

## Documentation Workflow

### Step 1: Analyze Changes

After completing work, identify:
1. **What changed**: Files modified, functions added/changed
2. **User impact**: Is this user-facing? Breaking change?
3. **Scope**: Which subsystem (firmware, console, MCU, CAD)?

Use git diff to see changes:
```bash
git diff --name-only
git diff --stat
```

### Step 2: Update CHANGELOG.md

Add entry under `## [Unreleased]`:
1. Determine category (Added, Changed, Fixed, etc.)
2. Write clear, present-tense description
3. Include file paths for navigation
4. Reference issues if applicable
5. Add breaking change notes if needed

### Step 3: Update Relevant README

Based on scope, update appropriate README:
- Root README: High-level project features
- Subsystem README: Implementation details
- Component README: Usage examples

### Step 4: Add/Update Inline Documentation

For new or significantly changed code:
1. Add module-level docs (`//!` or top-level comment)
2. Document all public APIs
3. Include examples for complex functions
4. Document safety invariants

### Step 5: Update Cross-References

If files moved or restructured:
1. Update links in CLAUDE.md
2. Update relative paths in READMEs
3. Fix broken skill references

### Step 6: Verify

- [ ] CHANGELOG entry is clear and complete
- [ ] README accurately reflects new features
- [ ] All public APIs are documented
- [ ] Examples compile/work
- [ ] Cross-references resolve
- [ ] Formatting is consistent

## Special Cases

### Breaking Changes

**CHANGELOG**:
```markdown
### Changed
- **BREAKING**: Renamed `set_mode()` to `handle_event()` in `state` crate for clarity

  Migration:
  ```rust
  // Before
  sm.set_mode(Mode::Teleop);

  // After
  sm.handle(Event::Enable);
  ```
```

**README**:
Add migration guide section if significant.

### Security Fixes

**CHANGELOG** (never include vulnerability details):
```markdown
### Security
- Fixed input validation issue in teleop command handler
```

**No public details** until after coordinated disclosure.

### Deprecations

**CHANGELOG**:
```markdown
### Deprecated
- `old_function()` is deprecated and will be removed in v2.0. Use `new_function()` instead.
```

**Inline Documentation**:
```rust
/// Legacy function for backward compatibility.
///
/// # Deprecated
/// This function is deprecated since v1.5 and will be removed in v2.0.
/// Use [`new_function`] instead.
#[deprecated(since = "1.5.0", note = "use `new_function` instead")]
pub fn old_function() {
    // ...
}
```

## Examples

### Example 1: New Feature (Safety Watchdog)

**CHANGELOG Addition**:
```markdown
### Added
- Safety watchdog in `bvr/firmware/crates/control/src/lib.rs` monitors command reception and automatically transitions to Idle mode after 500ms timeout, preventing runaway rovers if connection is lost
```

**README Update** (`bvr/firmware/README.md`):
```markdown
## Safety Features

### Command Watchdog

The control loop includes a command watchdog that monitors teleop connection health:
- Timeout: 500ms (configurable)
- Action: Automatic transition to Idle mode
- Reset: Fed on every valid command reception

**Configuration**:
```toml
[control]
command_timeout_ms = 500
```

**Implementation**: `crates/control/src/lib.rs:162-193`
```

**Inline Documentation**:
```rust
/// Command watchdog for safety monitoring.
///
/// Tracks the time since the last valid command was received. If the timeout
/// duration elapses without receiving commands, `is_timed_out()` returns true,
/// indicating that the rover should transition to a safe state.
///
/// # Examples
///
/// ```
/// let mut watchdog = Watchdog::new(Duration::from_millis(500));
/// assert!(watchdog.is_timed_out());  // Initially timed out
///
/// watchdog.feed();  // Reset timer
/// assert!(!watchdog.is_timed_out());
/// ```
///
/// # Safety
///
/// The watchdog timeout should be tuned to balance responsiveness with network
/// jitter. Too short causes false positives; too long delays safety response.
pub struct Watchdog {
    timeout: Duration,
    last_command: Option<Instant>,
}
```

### Example 2: Bug Fix (CAN Frame Parsing)

**CHANGELOG Addition**:
```markdown
### Fixed
- CAN bus VESC status frame parsing now validates buffer length before accessing bytes in `bvr/firmware/crates/can/src/vesc.rs:167-191`, preventing panics on malformed frames (#42)
```

**No README change** (implementation detail, not user-facing).

**Inline Documentation** (if not already present):
```rust
/// Parses VESC STATUS1 frame containing ERPM, current, and duty cycle.
///
/// # Arguments
///
/// * `data` - CAN frame payload (must be exactly 8 bytes)
///
/// # Returns
///
/// `Ok(())` if parsing succeeds, `Err(CanError::InvalidFrame)` if data is
/// too short or malformed.
///
/// # Safety
///
/// This function performs bounds checking before indexing into `data` to
/// prevent panics on malformed frames.
fn parse_status1(&mut self, data: &[u8]) -> Result<(), CanError> {
    if data.len() < 8 {
        warn!("STATUS1 frame too short: {} bytes", data.len());
        return Err(CanError::InvalidFrame);
    }
    // ... safe indexing
}
```

## Best Practices

### Writing Good CHANGELOG Entries

✅ **Good**:
- "Add rate limiting to prevent sudden acceleration in `control` crate with configurable max accel/decel values"
- "Fix WebSocket reconnection logic to use exponential backoff up to 30s max delay"
- "Update VESC CAN protocol to use big-endian byte order per spec"

❌ **Bad**:
- "Fix bug" (what bug?)
- "Update code" (what changed?)
- "Improve performance" (how? where? by how much?)

### Writing Good Inline Documentation

✅ **Good**:
- Includes purpose, parameters, return values, examples, safety notes
- Clear, concise language
- Links to related functions/types
- Documents edge cases and error conditions

❌ **Bad**:
- Repeats function name ("This function does X" for `fn do_x()`)
- No examples for complex APIs
- Missing safety documentation for unsafe code
- Outdated information after refactoring

### Maintaining README Consistency

- Match existing heading structure
- Use same formatting (code blocks, lists, etc.)
- Follow project tone (technical vs. beginner-friendly)
- Update table of contents if adding sections
- Place new sections logically (not just at end)

## References and Additional Resources

For more detailed information, see:
- [changelog-format.md](changelog-format.md) - Complete CHANGELOG formatting guide
- [documentation-patterns.md](documentation-patterns.md) - Language-specific doc patterns
- [CLAUDE.md](/Users/cam/Developer/muni/CLAUDE.md) - Project conventions
- [Keep a Changelog](https://keepachangelog.com/) - CHANGELOG format standard
- [Conventional Commits](https://www.conventionalcommits.org/) - Commit message format

## Quick Commands

```bash
# Check for undocumented pub functions (Rust)
grep -rn "pub fn" bvr/firmware/crates --include="*.rs" | grep -v "///"

# Check for undocumented exports (TypeScript)
grep -rn "export function" depot/console/src --include="*.ts" --include="*.tsx" | grep -v "/\*\*"

# View recent commits for CHANGELOG
git log --since="1 week ago" --pretty=format:"%h %s"

# Check modified files
git diff --name-only HEAD~5..HEAD
```
