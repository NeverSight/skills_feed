---
name: fanfuaji
description: Use when user requests Chinese terminology conversion, checking, or ensuring terminology - "使用繁體中文", "使用台灣用語", "轉換成台灣用語", "確保都是台灣用語", "統一台灣用語", "改成台灣用語", "用台灣的說法", "簡體轉繁體", "繁體轉簡體", "全部改成繁體", "轉成台灣繁體", check/ensure Taiwan/Hong Kong/China terminology, simplified/traditional conversion, or phonetic transcription (Pinyin/Bopomofo)
license: MIT
metadata:
  author: shihyuho
  version: "1.0.0"
---

# Fanfuaji - Chinese Terminology Converter

Convert Chinese text between simplified/traditional, regional variants (China/Taiwan/Hong Kong), and phonetic forms (Pinyin/Bopomofo).

**Includes `scripts/fanfuaji.py` - zero-dependency Python wrapper with multi-encoding support.**

## When to Use

- User requests Traditional Chinese, Taiwan/Hong Kong/China terminology
- Simplified ↔ Traditional conversion
- Pinyin or Bopomofo transcription
- Custom replacement rules or term protection needed

## Converter Selection (REQUIRED)

**If user does NOT specify conversion target, MUST ask using `question` tool.**

**Available converters (priority order):**

| Name | API Value | Description |
|------|-----------|-------------|
| 台灣化 | `Taiwan` | Traditional + Taiwan terminology |
| 繁體化 | `Traditional` | Traditional characters only |
| 注音化 | `Bopomofo` | Bopomofo (Zhuyin) phonetic |
| 中国化 | `China` | Simplified + China terminology |
| 香港化 | `Hongkong` | Traditional + Hong Kong terminology |
| 简体化 | `Simplified` | Simplified characters only |
| 拼音化 | `Pinyin` | Pinyin romanization |
| 火星化 | `Mars` | Internet slang variant |
| 維基繁體化 | `WikiTraditional` | Wikipedia Traditional |
| 维基简体化 | `WikiSimplified` | Wikipedia Simplified |

**Ambiguity examples:**
- ❌ "轉換成繁體" → Ask: Traditional, Taiwan, or Hongkong?
- ✅ "使用台灣用語" → Clear: use `Taiwan`

## Output Handling (REQUIRED)

**Recommendation**: Use absolute paths for input/output files to avoid directory context issues.

### 1. Output Destination (if unclear, MUST ask)

**If user does NOT specify output destination, ask using `question` tool:**

**When input is from file (`--file input.txt`):**
```
How would you like to receive the result?
- Display in chat (stdout)
- Overwrite original file (input.txt)
- Save to new file (specify filename)
```

**When input is text (no `--file`):**
```
How would you like to receive the result?
- Display in chat (stdout)
- Save to file (specify filename)
```

### 2. File Overwrite Check

**Rule**: When output will write to a file AND file exists, MUST ask using `question` tool.

**File will be written when:**

| Command Pattern | Target File | Check Needed? |
|----------------|-------------|---------------|
| `"text" --output file.txt` | file.txt | ✅ If exists |
| `--file input.txt` (no --output) | input.txt (overwrite) | ✅ Always |
| `--file input.txt --output out.txt` | out.txt | ✅ If exists |
| `"text"` (stdout) | - | ❌ No |

**Question template:**
```
File "filename" already exists. What would you like to do?
- Overwrite existing file
- Save to new file (filename_YYYY-MM-DD.txt)
- Cancel operation
```

## Basic Usage

```bash
# Text conversion
python scripts/fanfuaji.py "软件开发" --converter Taiwan
# → 軟體開發

# File conversion
python scripts/fanfuaji.py --file input.txt --converter Taiwan --output output.txt

# Different encodings (Big5, GBK, GB2312, Shift_JIS)
python scripts/fanfuaji.py --file big5_file.txt --encoding big5 --converter Taiwan

# Term protection
python scripts/fanfuaji.py "软件" --converter Taiwan --protect "软件"

# Post-conversion replacement
python scripts/fanfuaji.py "哦" --converter Taiwan --post-replace "哦=喔,啰=囉"
```

## Python Library Usage

```python
import sys
sys.path.insert(0, 'scripts')
from fanfuaji import convert_text, Converter

result = convert_text("软件开发", Converter.TAIWAN)
print(result)  # 軟體開發
```

## Encoding Support

**Default:** UTF-8

**Supported:** big5, gbk, gb2312, and all Python codecs

**Output:** Always UTF-8

```bash
# Auto-detect and handle legacy encodings
python scripts/fanfuaji.py --file legacy.txt --encoding big5 --converter Taiwan
```

## Script Features

- ✅ Zero dependencies (stdlib only)
- ✅ Multi-encoding support (UTF-8, Big5, GBK, etc.)
- ✅ File and text input
- ✅ Error handling (encoding, network, API)
- ✅ Term protection & custom replacements

## Notes

- Free tier available (no API key needed)
- Commercial use requires API key
- Output destination and file overwrite checks REQUIRED (see Output Handling)
- Converter selection confirmation REQUIRED if ambiguous

## Resources

- [Fanhuaji API](https://zhconvert.org)
- [API Docs](https://docs.zhconvert.org)
- [Script](scripts/fanfuaji.py)
