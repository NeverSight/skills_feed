---
name: "ARB Translation Updater"
description: "Batch update ARB translation files across all languages when new translation keys are added to English and Chinese files; use when adding new i18n strings to the Flutter app."
---

# ARB Translation Updater

## Purpose

This skill helps batch update all language ARB (Application Resource Bundle) files when new translation entries are added to the base languages (English and Chinese). It automates the process of translating and distributing new entries across 60+ language files.

## Use Cases

- Add new translation keys to all language files
- Keep all ARB files synchronized with English (en) and Chinese (zh) base files
- Batch translate new UI strings for the Flutter app
- Maintain consistency across all localization files

## **CRITICAL RULES** ⚠️

### Rule 1: New Strings MUST Be Added at the END of ARB Files

**ALWAYS add new translation entries at the very end of each ARB file, just before the closing `}`.**

- ✅ CORRECT: Add entries after the last existing entry in the file
- ❌ WRONG: Insert entries in the middle of the file
- This applies to BOTH manual additions (to `intl_en.arb` and `intl_zh.arb`) AND automated additions via the update script

**Example:**
```json
{
  "existingKey1": "...",
  "@existingKey1": {},
  "existingKey2": "...",
  "@existingKey2": {},
  // Add new entries HERE ↓
  "newKey": "...",
  "@newKey": {}
}
```

### Rule 2: All Metadata Descriptions MUST Be in English

**ALL ARB files (including non-English languages) must have metadata descriptions written in English.**

- ✅ CORRECT: `"@perfectDatabaseChallengeHint": {"description": "Hint to enable perfect database for greater challenge", ...}`
- ❌ WRONG: `"@perfectDatabaseChallengeHint": {"description": "启用完美数据库以获得更大挑战的提示", ...}` (in `intl_zh.arb`)

This applies to:
- The `description` field in `@key` metadata
- Placeholder descriptions within metadata
- ALL language files: `intl_en.arb`, `intl_zh.arb`, `intl_ja.arb`, etc.

**Rationale:** Flutter's ARB format specification requires metadata to be in English for tooling compatibility and consistency across all locales.

### Rule 3: ALWAYS Check for Existing Entries Before Adding

**Before adding new translations, ALWAYS check if the key already exists in the ARB files.**

**Check before adding:**
```bash
# Check if key exists in a specific file
grep -c "keyName" intl_en.arb

# Check all files
for file in intl_*.arb; do
  count=$(grep -c "keyName" "$file")
  echo "$file: $count occurrences"
done
```

**Decision matrix:**
- **If count = 0 (no occurrences)**: ✅ Add the new entry
- **If count = 2 (one complete entry: key + metadata)**: ⚠️ Entry already complete, DO NOT add again
- **If count = 1 or count > 2**: ❌ Incomplete or duplicate entry - fix before proceeding

**If duplicates exist:**
1. Remove ALL occurrences of the duplicate key
2. Re-add only ONE complete entry (key + metadata) at the END of the file
3. Validate JSON format after fixing

**Prevention:**
- Always use version control to check what was actually added
- Don't assume keys need to be added just because the task mentions them
- Verify the current state of ARB files before running update scripts

### Rule 4: MUST Use 4-Space Indentation

**ALL ARB files MUST use 4-space indentation, NOT 2-space or tabs.**

**Indentation levels:**
- Top-level keys: 4 spaces
- Metadata object first level: 8 spaces (4+4)
- Placeholders object: 8 spaces
- Placeholder keys: 12 spaces (4+4+4)
- Placeholder properties: 16 spaces (4+4+4+4)

**Example with correct 4-space indentation:**
```json
{
    "myKey": "My value",
    "@myKey": {
        "description": "My description",
        "placeholders": {
            "param": {
                "description": "Parameter description",
                "type": "String"
            }
        }
    }
}
```

**❌ WRONG (2-space indentation):**
```json
{
  "myKey": "My value",
  "@myKey": {
    "description": "My description",
    "placeholders": {
      "param": {
        "description": "Parameter description",
        "type": "String"
      }
    }
  }
}
```

**Important:**
- When creating `new-items.txt`, use 4-space indentation
- The `update_arb_files.sh` script will copy indentation exactly as written
- Always verify indentation after running the update script

## Workflow Overview

```
1. Use git to identify new entries in intl_en.arb (and intl_zh.arb if available)
2. Generate translations for all 59 other languages
3. Create new-items.txt with all translations
4. Run update_arb_files.sh to apply changes
5. Validate JSON format of updated files
```

## Step-by-Step Process

### Step 1: Identify New Entries Using Git

**Use git to see what was recently added** (most reliable method):

```bash
cd src/ui/flutter_app/lib/l10n

# Check recent changes to English ARB file
git log -p --follow -1 intl_en.arb

# Or see diff from last commit
git diff HEAD~1 intl_en.arb

# See what was added (lines starting with +)
git diff HEAD~1 intl_en.arb | grep "^+"

# Check if Chinese file also has new entries
git diff HEAD~1 intl_zh.arb

# If no recent changes in git, check uncommitted changes
git diff intl_en.arb
git diff intl_zh.arb
```

**Extract the new keys:**
- Look for newly added key-value pairs
- Note both the key and its metadata (lines starting with `@`)
- Each translation typically has 2 lines: `"key": "value"` and `"@key": {}`
- **IMPORTANT**: All metadata objects must be empty `{}` - NO `description` field in any language file (including English and Chinese)

**Priority:**
1. If both `intl_en.arb` and `intl_zh.arb` have new entries → use both as translation reference
2. If only `intl_en.arb` has new entries → translate from English only
3. Chinese translation is optional; English is the primary source

### Step 2: Determine Which Languages Need Updates

Check if the new keys exist in other language files:

```bash
# Check if a specific key exists in all files
grep -l "newKeyName" intl_*.arb

# Count how many files already have the key
grep -l "newKeyName" intl_*.arb | wc -l

# Find which files are missing the key
for file in intl_*.arb; do
  if ! grep -q "newKeyName" "$file"; then
    echo "Missing in: $file"
  fi
done
```

### Step 3: Generate Translations for All Languages

Create translations for all required languages. Each ARB file needs:
- Translation appropriate to the language
- NOT just English text copied across
- Context-aware for the Mill game domain

**Supported Languages (59+ total excluding en and zh):**
- European: de, de_ch, fr, es, it, pt, ru, pl, nl, sv, da, fi, nb, cs, sk, hu, ro, bg, hr, sr, sl, el, et, lv, lt, is, be, uk, mk, bs, sq, ca
- Asian: ja, ko, zh_Hant, hi, bn, ta, te, kn, gu, th, vi, id, ms, km, my, si, bo
- Middle Eastern: ar, fa, he, ur, hy, az, uz, tr
- African: am, sw, zu, af

### Step 4: Create new-items.txt

The `update_arb_files.sh` script reads from `new-items.txt` with this format:

```txt
// intl_<locale>.arb
  "keyName": "Translated text",
  "@keyName": {},
  "keyNameDetail": "Detailed translated text",
  "@keyNameDetail": {}

// intl_<another_locale>.arb
  "keyName": "其他语言的翻译",
  "@keyName": {},
  ...
```

**Format Rules:**
- Comment line: `// intl_<locale>.arb` (indicates which file to update)
- Entries: JSON key-value pairs with proper indentation (4 spaces)
- Blank line between different locale sections
- No trailing comma on last entry in each section
- **Do NOT include intl_en.arb or intl_zh.arb** in new-items.txt (these are already updated)
- **CRITICAL**: All `@key` metadata must be empty objects `{}` - NEVER include `description` or any other fields

**Example new-items.txt:**

```txt
// intl_ja.arb
    "stopPlacing": "配置を停止",
    "@stopPlacing": {},
    "stopPlacing_Detail": "ボード上に空きスペースが2つだけ残ったときに配置フェーズが終了します。",
    "@stopPlacing_Detail": {}

// intl_fr.arb
    "stopPlacing": "Arrêter le placement",
    "@stopPlacing": {},
    "stopPlacing_Detail": "La phase de placement se termine lorsque le plateau n'a plus que 2 espaces vides.",
    "@stopPlacing_Detail": {}

// intl_de.arb
    "stopPlacing": "Setzen beenden",
    "@stopPlacing": {},
    "stopPlacing_Detail": "Die Setzphase endet, wenn das Brett nur noch 2 freie Felder hat.",
    "@stopPlacing_Detail": {}
```

### Step 5: Run Update Script

Execute the update script to apply all translations:

```bash
cd src/ui/flutter_app/lib/l10n

# Run the update script
./update_arb_files.sh

# The script will:
# - Read new-items.txt
# - Parse each locale section
# - Append entries to corresponding .arb files
# - Maintain proper JSON formatting
```

### Step 6: Validate Results

Verify that all files were updated correctly:

```bash
# Check how many files contain the new key
grep -l "stopPlacing" intl_*.arb | wc -l
# Should return 63 (all language files including en and zh)

# Count total arb files
ls -1 intl_*.arb | wc -l
# Should return 63

# Validate JSON format of all files
for file in intl_*.arb; do
  if ! python3 -m json.tool "$file" > /dev/null 2>&1; then
    echo "❌ JSON Error in $file"
  fi
done
echo "✅ JSON validation complete"

# Spot check a few languages
tail -6 intl_ja.arb   # Japanese
tail -6 intl_fr.arb   # French
tail -6 intl_ru.arb   # Russian
tail -6 intl_ar.arb   # Arabic
```

## Available Scripts

### update_arb_files.sh

**Location:** `src/ui/flutter_app/lib/l10n/update_arb_files.sh`

**What it does:**
- Reads `new-items.txt` from the same directory
- Parses locale-specific sections (marked with `// intl_<locale>.arb`)
- Appends new entries to corresponding ARB files
- Maintains proper JSON structure (removes trailing commas, adds closing braces)

**How it works:**
1. Detects comment lines with ARB filenames
2. Accumulates translation entries for each locale
3. Removes last `}` from target file
4. Appends new entries
5. Adds closing `}` back

### Other Helper Scripts

```bash
# append.sh - Appends content from append.txt to specified ARB file
./append.sh <arb_file>

# append-items.sh - Calls append.sh for all ARB files
./append-items.sh

# replace-locale.sh - Replace locale identifiers
./replace-locale.sh
```

## Translation Quality Guidelines

### Context Matters

When translating Mill game terms, consider:
- **Placing phase** - Initial piece placement on board
- **Moving phase** - Moving pieces already on board
- **Flying** - Special move when player has few pieces left
- **Mill** - Three pieces in a row
- **Pieces** - Game tokens (not chess pieces)

### Translation Source Priority

1. **Primary source**: English (`intl_en.arb`)
2. **Secondary reference**: Chinese (`intl_zh.arb`) - if available and recently updated
3. **Existing translations**: Check similar keys in the same file for consistency

### Language-Specific Considerations

**Right-to-Left Languages (ar, he, fa, ur):**
- Ensure proper RTL text direction
- Numbers and punctuation may need special handling

**Asian Languages (zh, ja, ko, th, vi):**
- May not need plural forms
- Consider formal vs informal register

**European Languages:**
- Watch for gender agreement (de, fr, es, it)
- Plural forms vary by language

## Common Issues & Solutions

### Issue: Not sure what was added recently

**Solution:**
```bash
# Use git to see the actual changes
git log -p --since="1 week ago" -- intl_en.arb

# Compare with current HEAD
git diff HEAD intl_en.arb

# See only added lines
git diff HEAD intl_en.arb | grep "^+[^+]"
```

### Issue: Chinese file doesn't have the new keys

**Solution:**
- This is normal and expected
- Translate from English only
- Chinese translations can be added separately later

### Issue: Script doesn't update files

**Solution:**
- Check `new-items.txt` exists in l10n directory
- Verify file format (comment lines start with `//`)
- Ensure proper indentation (2 spaces)
- Make sure you're NOT including intl_en.arb or intl_zh.arb in new-items.txt

### Issue: JSON validation fails

**Cause:** Trailing comma or malformed JSON

**Solution:**
```bash
# Find the problematic file
for file in intl_*.arb; do
  python3 -m json.tool "$file" > /dev/null 2>&1 || echo "Error: $file"
done

# Manually fix JSON or re-run script
```

### Issue: Some languages missing translations

**Check:**
```bash
# Verify all locales are in new-items.txt
grep "^//" new-items.txt | wc -l
# Should be around 59-61 (excluding en and zh base files)

# List which files are included
grep "^//" new-items.txt
```

### Issue: Translations are just English text

**Problem:** Not properly translated, just English copied

**Solution:** Regenerate translations ensuring each language gets proper localization

### Issue: Metadata contains description field

**Problem:** ARB files have `"@key": {"description": "..."}` instead of `"@key": {}`

**Solution:**
```python
# Fix all ARB files to have empty metadata objects
import json

for locale in ['en', 'zh', 'ja', 'fr', ...]:  # all locales
    file_path = f'intl_{locale}.arb'
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Remove description from all @ keys
    for key in list(data.keys()):
        if key.startswith('@'):
            data[key] = {}

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.write('\n')
```

**Important:**
- ALL language files (including `intl_en.arb` and `intl_zh.arb`) must have empty metadata objects `{}`
- NEVER add `description` or any other fields to metadata
- This applies to both base language files and all translations

## Best Practices

1. **Use git to identify changes**
   - `git diff` is more reliable than `tail`
   - Shows exactly what was added/modified
   - Avoids guessing from file endings

2. **English is the primary source**
   - Always check `intl_en.arb` for new entries
   - Chinese (`intl_zh.arb`) is optional reference
   - Don't wait for Chinese translations

3. **Use consistent terminology**
   - Refer to existing translations for game terms
   - Maintain consistent voice and style
   - Check similar keys in same file

4. **Test after updating**
   - Run Flutter app with different locales
   - Verify text displays correctly
   - Check for UI overflow issues

5. **Version control**
   - Commit base language changes separately first
   - Commit batch translations in one commit
   - Use clear commit messages: `i18n: Add translations for [feature]`

6. **Quality over speed**
   - Use professional translation services or AI for accuracy
   - Review machine translations for context
   - Consider cultural appropriateness

## File Locations

```
src/ui/flutter_app/lib/l10n/
├── intl_en.arb          # English (primary base)
├── intl_zh.arb          # Chinese Simplified (optional reference)
├── intl_zh_Hant.arb     # Chinese Traditional
├── intl_*.arb           # 60 other language files
├── new-items.txt        # Temporary: new translations to add
├── update_arb_files.sh  # Main update script
├── append.sh            # Helper script
├── append-items.sh      # Helper script
└── replace-locale.sh    # Helper script
```

## Verification Checklist

After running the update process:

- [ ] Used git to identify what was actually added
- [ ] All required ARB files contain the new keys
- [ ] All JSON files validate successfully
- [ ] Translations are in correct languages (not English placeholders)
- [ ] Spot-checked 5+ languages for quality
- [ ] No trailing commas or syntax errors
- [ ] Flutter app builds without i18n errors
- [ ] UI displays correctly in different locales

## Example: Complete Workflow

```bash
# 1. Navigate to l10n directory
cd src/ui/flutter_app/lib/l10n

# 2. Use git to identify what's new
git diff HEAD~1 intl_en.arb
# OR if uncommitted:
git diff intl_en.arb

# Output shows:
# +"newFeature": "Stop placing when empty",
# +"@newFeature": {},
# +"newFeature_Detail": "Detailed explanation...",
# +"@newFeature_Detail": {}

# 3. Check if Chinese also has these (optional)
git diff HEAD~1 intl_zh.arb
# If not found, proceed with English only

# 4. Extract the new keys
# newFeature
# newFeature_Detail

# 5. Generate translations for all languages
# (Use AI or translation service to create new-items.txt)
# Remember: do NOT include intl_en.arb or intl_zh.arb

# 6. Verify new-items.txt format
head -30 new-items.txt
# Should start with: // intl_af.arb or similar (NOT intl_en.arb)

# 7. Run update script
./update_arb_files.sh

# 8. Validate results
grep -l "newFeature" intl_*.arb | wc -l
# Output: 63 ✓ (all files including en and zh)

# 9. Validate JSON
for file in intl_*.arb; do
  python3 -m json.tool "$file" > /dev/null 2>&1 || echo "Error: $file"
done
echo "✅ All files valid"

# 10. Spot check translations
tail -8 intl_ja.arb
tail -8 intl_de.arb
tail -8 intl_ar.arb

# 11. Verify with git
git diff intl_ja.arb
git diff intl_de.arb

# 12. Clean up
rm new-items.txt  # Optional: keep for reference

# 13. Commit changes
# Navigate to project root directory
git add src/ui/flutter_app/lib/l10n/intl_*.arb
git commit -m "i18n: Add translations for new feature across all languages"
```

## Advanced: Automated Translation Generation

When using AI to generate all translations:

**Important:** Translate from English, optionally reference Chinese

```markdown
# Prompt template for AI translation:

Translate the following Mill game UI strings from English to all these languages:
[List of target languages]

English source:
"newFeature": "Stop placing when only two empty squares remain"
"newFeature_Detail": "When enabled, the placing phase ends and moving phase begins when the board has only 2 empty spaces left, regardless of pieces in hand. This rule only applies to 12-piece games."

Optional Chinese reference (if available):
"newFeature": "棋盘只剩两个空位时停止放子"
"newFeature_Detail": "启用后，当棋盘只剩2个空位时，无论手中是否还有棋子，放子阶段都会结束并进入走子阶段。此规则仅适用于12子棋。"

Context:
- This is for a Mill board game app (Nine Men's Morris)
- "newFeature" is a short settings label
- "newFeature_Detail" is a detailed description shown in settings

Please provide natural, fluent translations for each language.
Format as new-items.txt (do NOT include English or Chinese).
```

Then format the response into new-items.txt format.

## Quick Reference Commands

```bash
# See what was added to English ARB
git diff HEAD~1 intl_en.arb | grep "^+"

# Check if all files have a key
grep -l "keyName" intl_*.arb | wc -l

# Validate all JSON files
for f in intl_*.arb; do python3 -m json.tool "$f" >/dev/null 2>&1 || echo "Bad: $f"; done

# Count languages in new-items.txt
grep "^//" new-items.txt | wc -l

# Update all ARB files
./update_arb_files.sh

# View recent ARB commits
git log --oneline --follow -10 intl_en.arb
```

## Reference Resources

- **ARB Format Spec**: https://github.com/google/app-resource-bundle
- **Flutter i18n Guide**: https://docs.flutter.dev/development/accessibility-and-localization/internationalization
- **Mill Game Terminology**: Refer to existing translations in intl_en.arb
- **Update Script**: `src/ui/flutter_app/lib/l10n/update_arb_files.sh`
- **Git Workflow**: Use `git diff` to identify new entries reliably
