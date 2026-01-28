---
name: plugin-packaging
description: Create branded PKG installers for plugin distribution. Use when user requests to package a plugin, create installer, share plugin with others, or mentions distributing/sending plugin to someone. Invoked by /package command or natural language like 'create installer for TapeAge' or 'package GainKnob'.
---

# plugin-packaging Skill

**Purpose:** Create professional PKG installers for sharing plugins with others.

## Overview

Generates macOS PKG installers with branded UI, automated plugin installation, and Gatekeeper bypass instructions.

## Workflow

<critical_sequence enforcement="strict" blocking="true">

**Track your progress:**

```
Plugin Packaging Progress:
- [ ] 1. Prerequisites verified (plugin installed, binaries exist)
- [ ] 2. Metadata extracted (contracts read, version/description/parameters)
- [ ] 3. Branding files created (Welcome, ReadMe, Conclusion)
- [ ] 4. Base package built (pkgbuild complete)
- [ ] 5. Branded installer created (productbuild complete)
- [ ] 6. Distribution package output (dist/ created, committed, PLUGINS.md updated)
```

---

### 1. Verify Prerequisites

Check plugin is ready for packaging:
- Read PLUGINS.md, verify status is 📦 Installed
- Verify VST3 exists: `~/Library/Audio/Plug-Ins/VST3/[ProductName].vst3`
- Verify AU exists: `~/Library/Audio/Plug-Ins/Components/[ProductName].component`

**Blocking:** If not installed, guide user to run `/install-plugin [PluginName]` first.

**Preconditions verified in this step:**
- Plugin status is 📦 Installed
- VST3 and AU binaries exist in system folders

### 2. Extract Plugin Metadata

**Read multiple files in parallel** using multiple Read tool calls:
- PLUGINS.md entry for plugin (version, description, parameter list, use cases)
- `plugins/[PluginName]/CMakeLists.txt` (for PRODUCT_NAME extraction)
- `plugins/[PluginName]/.ideas/parameter-spec.md` (detailed parameter descriptions)
- `plugins/[PluginName]/.ideas/creative-brief.md` (features, use cases, design rationale)

Extract PRODUCT_NAME using grep + sed (see Section 1.2 in references/pkg-creation.md).

**Template variables to extract:**
- {{PLUGIN_NAME}}, {{VERSION}}, {{DESCRIPTION}}
- {{PRODUCT_NAME}}, {{PARAM_COUNT}}, {{PARAMETERS}}
- {{FEATURES}}, {{QUICK_START_PRESETS}}

### 3. Create Branding Files

Generate Welcome.txt, ReadMe.txt, and Conclusion.txt by reading templates from `assets/` and replacing {{VARIABLE}} placeholders with metadata from contracts (.ideas/parameter-spec.md and creative-brief.md provide richer content than PLUGINS.md).

See Section 3 in references/pkg-creation.md for complete bash implementation.

### 4. Build Base Package

Create foundational PKG with installation logic:

**4a. Create temp directory structure** (see Section 4a in references/pkg-creation.md)

**4b. Copy binaries to payload** (see Section 4a in references/pkg-creation.md)

**Validation:** Verify binaries copied successfully. ONLY proceed to 4c when both files are present.

**4c. Create postinstall script** (see Section 4b in references/pkg-creation.md for complete script)

**4d. Run pkgbuild** (see Section 4c in references/pkg-creation.md for complete command)

**Validation:** Verify base PKG created. ONLY proceed to step 5 when PKG file exists.

### 5. Build Branded Installer

Wrap base package with branding:

**5a. Create Distribution.xml** (see Section 5a in references/pkg-creation.md for complete XML structure)

**5b. Run productbuild** (see Section 5b in references/pkg-creation.md for complete command)

**Validation:** Verify branded PKG created. ONLY proceed to step 6 when branded PKG exists.

### 6. Output Distribution Package

Finalize and present to user:

**6a. Create dist directory** (see Section 6a in references/pkg-creation.md)

**6b. Copy installer** (see Section 6b in references/pkg-creation.md)

**6c. Generate install-readme.txt** (see Section 6c in references/pkg-creation.md for complete template)

**6d. Commit distribution package:**
```bash
git add plugins/[PluginName]/dist/
git commit -m "feat([PluginName]): create v[X.Y.Z] distribution package"
```

**6e. Update PLUGINS.md** with packaging metadata:
```markdown
**Last Packaged:** YYYY-MM-DD
**Distribution:** plugins/[PluginName]/dist/[PluginName]-by-TACHES.pkg (X.X MB)
```

**6f. Display summary:**
```
✓ [PluginName] packaged successfully

Created: plugins/[PluginName]/dist/[PluginName]-by-TACHES.pkg (X.X MB)

Distribution package includes:
- [PluginName]-by-TACHES.pkg (branded installer)
- install-readme.txt (installation guide)

Send both files to your friend.
```

</critical_sequence>

---

## Integration Points

**Invoked by:**
- `/package [PluginName]` command
- Natural language: "Create installer for TapeAge", "Package GainKnob"

**Invokes:**
- None (terminal skill - does not invoke other skills)

**Reads:**
- `PLUGINS.md` → Plugin metadata
- `plugins/[PluginName]/CMakeLists.txt` → PRODUCT_NAME extraction
- `~/Library/Audio/Plug-Ins/VST3/[Product].vst3` → Source binary
- `~/Library/Audio/Plug-Ins/Components/[Product].component` → Source binary

**Creates:**
- `plugins/[PluginName]/dist/[PluginName]-by-TACHES.pkg` → Branded installer
- `plugins/[PluginName]/dist/install-readme.txt` → Installation guide

**Updates:**
- `PLUGINS.md` → Add **Last Packaged:** timestamp and **Distribution:** package path/size
- Git repository → Commit dist/ folder with distribution package

---

## Decision Menu

<decision_gate type="checkpoint" enforcement="strict">

After successful packaging, present this menu and WAIT for user response:

```
✓ [PluginName] packaged successfully

Created: plugins/[PluginName]/dist/[PluginName]-by-TACHES.pkg (X.X MB)

What's next?
1. Test installer (recommended) → Verify PKG works correctly
2. Package another plugin → /package [OtherPlugin]
3. View installation guide → Show install-readme.txt contents
4. Share distribution files → Instructions for sending to friend
5. Other

Choose (1-5): _
```

**Option handlers:**
1. **Test installer** → Provide testing checklist (see Testing Checklist in references/pkg-creation.md Section 6)
2. **Package another** → Prompt for plugin name, re-invoke skill
3. **View guide** → Display install-readme.txt with `cat` command
4. **Share instructions** → Explain what files to send, how to compress if needed
5. **Other** → Open-ended response

</decision_gate>

---

## Error Handling

For error scenarios and troubleshooting, see references/pkg-creation.md Section 6 (Error Scenarios).

---

## Success Criteria

Packaging succeeds when:
- ✅ Base PKG created with postinstall script
- ✅ Branded PKG created with Welcome/ReadMe/Conclusion screens
- ✅ Installer file copied to `plugins/[PluginName]/dist/`
- ✅ Installation guide generated
- ✅ File sizes reported (PKG should be 3-5 MB typically)
- ✅ User knows what files to share

**NOT required for success:**
- Actually testing installer (recommended but not blocking)
- Signing/notarization (future enhancement)
- Multi-format packages (DMG, ZIP - future modes)

---

## Notes for Claude

**When executing this skill:**

1. Extract PRODUCT_NAME carefully (may contain spaces, use quotes)
2. Populate branding templates with actual plugin metadata (not placeholders)
3. Postinstall script must handle user detection (can't assume /Users/[name])
4. Clean up temp files after success (`rm -rf /tmp/[PluginName]-installer`)
5. Report file size to user (helpful for sharing over email/Dropbox)

**Branding consistency:**
- Always use "TÂCHES" in title, welcome, conclusion
- Format: "[PluginName] by TÂCHES"
- Include Gatekeeper steps in ReadMe (critical for unsigned plugins)
