---
name: system-setup
description: Validates and configures all dependencies required for the Plugin Freedom System. This is a STANDALONE skill that runs BEFORE plugin workflows begin. It checks for Python, build tools, CMake, JUCE, and pluginval, optionally installing missing dependencies with user approval. Configuration is saved to .claude/system-config.json for use by other skills. Use when user mentions setup, installation, dependencies, missing tools, or when SessionStart hook detects configuration issues.
allowed-tools:
  - Bash # For dependency checks and installation
  - Read # For checking existing config
  - Write # For creating system-config.json
  - Edit # For updating config
preconditions:
  - None - this is the entry point for new users
---

# system-setup Skill

**Purpose:** Validate and configure all dependencies required for JUCE plugin development in the Plugin Freedom System.

## Overview

This skill ensures new users can get started without friction by:
- Detecting the current platform (macOS, Linux, Windows)
- Checking for required dependencies (Python, build tools, CMake, JUCE, pluginval)
- Offering automated installation where possible
- Guiding manual installation when automation isn't available
- Validating that all tools are functional
- Saving validated configuration for build scripts

**Target platform:** macOS (extensible to Windows/Linux later)

**User experience:** Interactive, with clear choices between automated and guided setup

<test_mode_protocol>
IF --test=SCENARIO argument provided:
  MUST pass --test=$SCENARIO to ALL system-check.sh invocations
  MUST display test mode banner at start:
    [TEST MODE: $SCENARIO]
    Using mock data - no actual system changes will be made
  MUST NOT make actual system changes
  MUST use mock data from test scenarios
</test_mode_protocol>

<precondition_gate>
None required - this is the entry point skill
Can be invoked anytime, creates system-config.json
No dependencies on PLUGINS.md or .continue-here.md
</precondition_gate>

<delegation_rules>
  <rule>This skill is STANDALONE - it does NOT delegate to other skills or subagents</rule>
  <rule>All validation logic is handled by system-check.sh bash script</rule>
  <rule>This skill is invoked BEFORE plugin workflows begin</rule>
  <rule>DO NOT invoke plugin-workflow, plugin-planning, or any other plugin skills from here</rule>
</delegation_rules>

<cross_references>
  <file>references/platform-requirements.md</file>
  <file>references/juce-setup-guide.md</file>
  <script>assets/system-check.sh</script>
</cross_references>

---

## Required Dependencies

For detailed dependency requirements and installation instructions, see [references/platform-requirements.md](references/platform-requirements.md).

**Summary**: Python 3.8+, Build Tools (Xcode Command Line Tools/GCC/MSVC), CMake 3.15+, JUCE 8.0.0+, pluginval (optional)

---

## Skill Entry Point

When invoked via `/setup` command:

**Check for existing configuration first:**

1. Check if `.claude/system-config.json` exists and is recent (validated within last 30 days)
2. If valid config exists, offer quick menu:
   ```
   System Setup - Plugin Freedom System

   Existing configuration found (validated 5 days ago)

   What would you like to do?
   1. Re-validate all dependencies (full check)
   2. View current configuration
   3. Reconfigure specific dependency
   4. Exit

   Choose (1-4): _
   ```
3. Handle choice:
   - Choice 1: Proceed to full validation flow below (skip MODE selection, use "check-only" mode)
   - Choice 2: Display `.claude/system-config.json` contents and exit
   - Choice 3: Ask which dependency to reconfigure, then run validation for that dependency only
   - Choice 4: Exit
4. Only load full references if user chooses option 1 (full re-validation)

**If no valid config exists, proceed with full setup:**

**Check for test mode:**
- TEST_MODE is set if user provided `--test=SCENARIO` argument to `/setup` command
- Store in variable: `TEST_MODE=SCENARIO` (or empty if not in test mode)
- This variable persists throughout the entire setup session
- Pass test mode to all system-check.sh invocations via `--test=$SCENARIO`
- Show test mode banner if active:
  ```
  [TEST MODE: $SCENARIO]
  Using mock data - no actual system changes will be made
  ```

1. **Welcome message:**
   ```
   System Setup - Plugin Freedom System

   This will validate and configure all dependencies needed for JUCE plugin development.

   How would you like to proceed?
   1. Automated setup (install missing dependencies automatically)
   2. Guided setup (step-by-step instructions for manual installation)
   3. Check only (detect what's installed, no changes)
   4. Exit

   Choose (1-4): _
   ```

2. **Store user choice in MODE variable and proceed to platform detection**

   ```bash
   # Store user's mode choice (persists throughout entire setup)
   MODE="automated"  # or "guided" or "check-only"
   ```

   This MODE variable determines behavior for ALL dependency validations (Python, Build Tools, CMake, JUCE, pluginval).

## Mode Definitions

| Mode | Behavior | Installation | User Actions |
|------|----------|--------------|--------------|
| **automated** | Attempt automated installation with confirmation | Offers automatic install → falls back to manual if fails | Confirms installations, completes any GUI steps |
| **guided** | Show manual instructions only | NEVER automated - always manual instructions | Completes all installations manually, confirms when done |
| **check-only** | Report status without changes | NEVER offers installation | None - just review report |

**Mode persistence**: User's initial mode choice applies to ALL 5 dependency validations. Mode does NOT change mid-session.

---

## Setup Progress Checklist

Copy this checklist at skill start to track your progress:

```text
Setup Progress:
- [ ] Platform detected and confirmed
- [ ] Python 3.8+ installed and verified
- [ ] Build tools installed and verified (Xcode Command Line Tools / GCC / MSVC)
- [ ] CMake 3.15+ installed and verified
- [ ] JUCE 8.0.0+ installed and verified
- [ ] pluginval installed and verified (optional)
- [ ] Configuration saved to .claude/system-config.json
- [ ] Setup complete
```

Mark each item as you complete it.

---

## State Management

Two variables persist throughout the entire setup session:

### MODE Variable

**Initialized**: At skill entry when user selects from menu (lines 85-99)
**Values**: `"automated"`, `"guided"`, `"check-only"`
**Scope**: Used for ALL dependency validations (Python, Build Tools, CMake, JUCE, pluginval)
**Persistence**: Does NOT change mid-session - user's initial choice applies to all 5 dependencies

**Example**:
```bash
# User selects option 1 at entry menu
MODE="automated"

# This MODE value is used for Python validation
# Then Build Tools validation
# Then CMake validation
# Then JUCE validation
# Then pluginval validation
# MODE never changes during session
```

### TEST_MODE Variable

**Initialized**: At skill entry if user provided `--test=SCENARIO` argument to `/setup` command
**Values**: Scenario name (e.g., `"missing-cmake"`, `"old-python"`) or empty if not in test mode
**Scope**: Appended to ALL system-check.sh invocations throughout session
**Persistence**: Does NOT change mid-session

**Example**:
```bash
# User invoked: /setup --test=missing-cmake
TEST_MODE="missing-cmake"

# All system-check.sh calls include test mode:
bash system-check.sh --check-python --test=missing-cmake
bash system-check.sh --check-xcode --test=missing-cmake
# etc.
```

---

<critical_sequence name="dependency-validation" enforcement="strict">
**These dependencies MUST be validated in order. Each dependency may block on user input.**

<execution_rules>
- Execute dependencies sequentially (1 → 2 → 3 → 4 → 5)
- Each dependency must complete or be explicitly skipped before proceeding
- Mode choice (automated/guided/check-only) persists across all dependencies unless changed
- Failed automated installs fall back to guided mode
- User can abort at any decision gate
- If TEST_MODE is set, append --test=$TEST_MODE to all system-check.sh invocations
</execution_rules>

## Platform Detection

**Step 1: Detect platform**

```bash
# Run system check script (append --test=$SCENARIO if in test mode)
bash .claude/skills/system-setup/assets/system-check.sh --detect-platform ${TEST_MODE:+--test=$TEST_MODE}
```

**Note:** If TEST_MODE is set, append `--test=$TEST_MODE` to ALL system-check.sh invocations throughout this skill.

The script returns JSON:
```json
{
  "platform": "darwin",
  "platform_version": "14.0",
  "arch": "arm64"
}
```

**Step 2: Confirm with user**

```
Detected platform: macOS 14.0 (arm64)

Is this correct?
1. Yes, continue
2. No, let me specify

Choose (1-2): _
```

---

## Dependency Validation Workflow

For each dependency (in order):

1. **Check if already installed and functional**
2. **If found:**
   - Display version and path
   - Validate it meets minimum requirements
   - Save to config
   - Continue to next dependency
3. **If not found:**
   - **Automated mode:** Offer to install automatically
   - **Guided mode:** Show manual installation instructions
   - **Check-only mode:** Report as missing, continue

## Dependency Validation

For detailed validation workflow, error handling, and dependency-specific variations, see:
- **Validation pattern**: [references/validation-workflow.md](references/validation-workflow.md)
- **Error recovery**: [references/error-recovery.md](references/error-recovery.md)

**High-level validation process**:

1. **Platform Detection** - Detect macOS/Linux/Windows, confirm with user
2. **Python 3.8+** - Required for build scripts
3. **Build Tools** - Xcode Command Line Tools (macOS), GCC/Clang (Linux), Visual Studio (Windows)
4. **CMake 3.15+** - Build system for JUCE projects
5. **JUCE 8.0.0+** - Audio plugin framework
6. **pluginval** - Plugin validation tool (optional)

For each dependency:
- Run detection via `system-check.sh`
- If found and version OK → save to config, continue
- If not found → offer installation based on MODE (automated/guided/check-only)
- After installation → verify and save to config

See [validation-workflow.md](references/validation-workflow.md) for complete algorithm and dependency-specific handling.


---


---

## Configuration Persistence

After all dependencies are validated, create `.claude/system-config.json`:

```bash
# Generate config file
cat > .claude/system-config.json <<EOF
{
  "platform": "darwin",
  "platform_version": "14.0",
  "arch": "arm64",
  "python_path": "/usr/local/bin/python3",
  "python_version": "3.11.5",
  "xcode_path": "/Library/Developer/CommandLineTools",
  "cmake_path": "/usr/local/bin/cmake",
  "cmake_version": "3.27.4",
  "juce_path": "/Users/lex/JUCE",
  "juce_version": "8.0.3",
  "pluginval_path": "/usr/local/bin/pluginval",
  "pluginval_version": "1.0.3",
  "validated_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
```

**Add to .gitignore if not already present:**
```bash
grep -q "system-config.json" .gitignore || echo ".claude/system-config.json" >> .gitignore
```

---

## System Report

After configuration is saved, display comprehensive summary:

```
✓ System Setup Complete

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Platform: macOS 14.0 (arm64)

Dependencies validated:
✓ Python 3.11.5 (/usr/local/bin/python3)
✓ Xcode Command Line Tools 15.0
✓ CMake 3.27.4 (/usr/local/bin/cmake)
✓ JUCE 8.0.3 (/Users/lex/JUCE)
✓ pluginval 1.0.3 (/usr/local/bin/pluginval)

Configuration saved to:
.claude/system-config.json

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What's next?
1. Create your first plugin (/dream)
2. View available commands (type /? or press Tab)
3. Read the documentation (@README.md)
4. Run system check again (/setup)
5. Exit

Choose (1-5): _
```

**Handle user choice:**
- Choice 1: Use Skill tool to invoke plugin-ideation: `Skill("plugin-ideation")`
- Choice 2: Show command list via `ls .claude/commands/`
- Choice 3: Display README.md
- Choice 4: Re-run system-setup skill
- Choice 5: Exit with message

<state_management>
This skill is STANDALONE and does NOT:
- Update PLUGINS.md
- Create .continue-here.md
- Invoke other workflow skills (plugin-workflow, plugin-planning, etc.)
- Create or modify plugin directories

This skill ONLY:
- Creates/updates .claude/system-config.json
- Validates system dependencies
- Adds system-config.json to .gitignore
- Exits when validation complete

After setup completes successfully:
1. Configuration stored in .claude/system-config.json only
2. NO state file updates needed
3. NO plugin workflow initiated
4. User chooses next action from final menu
</state_management>

---

## Error Handling

For detailed error recovery procedures and failure scenarios, see [references/error-recovery.md](references/error-recovery.md).

**General principle**: All errors offer recovery paths - automated installation failures fall back to guided mode, permission errors offer sudo or user-directory alternatives, and missing critical dependencies trigger warning menus.

---


## Integration Points

**Invoked by:**
- `/setup` command (primary entry point)
- New user onboarding
- When build scripts detect missing dependencies

**Reads:**
- `.claude/system-config.json` (if exists, to show current config)
- `references/platform-requirements.md` (platform-specific installation guides)
- `references/juce-setup-guide.md` (detailed JUCE installation)

**Creates:**
- `.claude/system-config.json` (validated dependency paths)

**Uses:**
- `assets/system-check.sh` (bash validation script)

**May invoke:**
- `plugin-ideation` skill (if user chooses to create plugin after setup)

---

## Success Criteria

Setup is successful when:

- All required dependencies are detected or installed
- All versions meet minimum requirements
- All tools are validated as functional (not just present)
- Configuration is saved to `.claude/system-config.json`
- User receives clear system report
- Decision menus presented at appropriate points
- Errors are handled gracefully with fallback options

---

## Implementation Notes

For detailed execution notes, critical requirements, and anti-patterns, see [references/execution-notes.md](references/execution-notes.md).

**Key reminders**:
- Check before installing (never install if already present and correct version)
- Respect MODE throughout entire session
- Use absolute paths in config
- Wait for user confirmation at all decision gates
- Append test mode to all system-check.sh calls if TEST_MODE set
