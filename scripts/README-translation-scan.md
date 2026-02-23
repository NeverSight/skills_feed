# Description Translation Scan and Fix

## Scanning

Check whether any `description_*.txt` files have “identical to English” (untranslated) issues:

```bash
python scripts/scan_description_translations.py           # count only
python scripts/scan_description_translations.py --list 5   # list top 5 paths per language
```

- **zh-CN**: If `description_en.txt` is in English and `description_cn.txt` starts the same as en → treated as untranslated (should be 0).
- **tw / ar / de / es / fr / it / ja / ko / ru**: If the first 55 characters of the corresponding `description_XX.txt` match `description_en.txt` exactly → treated as an untranslated copy.

## Fixing “identical to en” entries

Only re-translate files whose current content matches the start of en; do not overwrite correctly translated ones:

```bash
# Run per language (add --dry-run to see which files would be changed)
python scripts/translate_descriptions.py --target zh-TW --fix-identical
python scripts/translate_descriptions.py --target ar --fix-identical
python scripts/translate_descriptions.py --target de --fix-identical
python scripts/translate_descriptions.py --target es --fix-identical
python scripts/translate_descriptions.py --target fr --fix-identical
python scripts/translate_descriptions.py --target it --fix-identical
python scripts/translate_descriptions.py --target ja --fix-identical
python scripts/translate_descriptions.py --target ko --fix-identical
python scripts/translate_descriptions.py --target ru --fix-identical
```

After fixing, run `scan_description_translations.py` again to confirm each language’s “identical” count drops to 0.

## Batch fix (optional)

```bash
for lang in zh-TW ar de es fr it ja ko ru; do
  python scripts/translate_descriptions.py --target "$lang" --fix-identical
done
```

Note: Each language may have hundreds to thousands of files; a full run can take a long time. Consider running in CI or in the background.
