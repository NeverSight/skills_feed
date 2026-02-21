#!/usr/bin/env python3
"""
Scan description_*.txt files for translation issues:
- description_cn.txt: EN is English but CN starts with same English (incomplete translation)
- description_tw/ar/de/es/fr/it/ja/ko/ru: target file identical to EN (first 55 chars)

Usage:
  python scan_description_translations.py           # summary counts
  python scan_description_translations.py --list 5   # show first 5 paths per lang
  python scan_description_translations.py --list 0   # show all paths (long)
"""

import argparse
from pathlib import Path

BASE = Path(__file__).parent.parent / "data" / "skills-md"
LANGS_OTHER = ["tw", "ar", "de", "es", "fr", "it", "ja", "ko", "ru"]


def scan_cn_identical() -> list[str]:
    """CN bad: en is English, cn starts with same 55 chars."""
    import re
    bad = []
    for en in BASE.rglob("description_en.txt"):
        cn = en.parent / "description_cn.txt"
        if not cn.exists():
            continue
        try:
            en_t = en.read_text(encoding="utf-8").strip().replace("\n", " ")[:55]
            cn_t = cn.read_text(encoding="utf-8").strip().replace("\n", " ")[:55]
        except Exception:
            continue
        if not en_t.strip() or not cn_t.strip():
            continue
        if en_t.strip() != cn_t.strip():
            continue
        # en could be Chinese too - only flag if en looks English
        if not re.match(r"^[A-Za-z][a-zA-Z0-9\s\.,\'\-\":;\(\)]{30,}", en_t):
            continue
        bad.append(str(en.parent))
    return bad


def scan_lang_identical(lang: str) -> list[str]:
    """Target file exists and first 55 chars equal en."""
    fname = f"description_{lang}.txt"
    bad = []
    for xx in BASE.rglob(fname):
        en = xx.parent / "description_en.txt"
        if not en.exists():
            continue
        try:
            en_t = en.read_text(encoding="utf-8").strip().replace("\n", " ")[:55]
            xx_t = xx.read_text(encoding="utf-8").strip().replace("\n", " ")[:55]
        except Exception:
            continue
        if en_t.strip() and xx_t.strip() and en_t.strip() == xx_t.strip():
            bad.append(str(xx.parent))
    return bad


def main():
    ap = argparse.ArgumentParser(description="Scan description translations for issues")
    ap.add_argument("--list", type=int, default=0, metavar="N", help="Show first N paths per lang (0 = none)")
    args = ap.parse_args()

    print("Scanning description_*.txt translation issues...\n")
    report = []

    # CN: incomplete (en=English, cn=same)
    cn_bad = scan_cn_identical()
    report.append(("zh-CN (cn)", len(cn_bad), cn_bad))
    print(f"  zh-CN (description_cn.txt): {len(cn_bad)} with EN/CN identical start (should be 0 after fix)")

    for lang in LANGS_OTHER:
        bad = scan_lang_identical(lang)
        report.append((lang, len(bad), bad))
        print(f"  {lang} (description_{lang}.txt): {len(bad)} identical to en")

    total_bad = sum(r[1] for r in report)
    print(f"\nTotal files to fix (identical/untranslated): {total_bad}")

    if args.list and total_bad > 0:
        print("\n--- Sample paths (--list) ---")
        for lang_name, count, paths in report:
            if count == 0:
                continue
            show = paths[: args.list] if args.list > 0 else paths[:5]
            print(f"\n  {lang_name}:")
            for p in show:
                print(f"    {p}")
            if count > len(show):
                print(f"    ... and {count - len(show)} more")

    print("\nTo fix: run for each target, e.g.")
    print("  python translate_descriptions.py --target zh-TW --fix-identical [--dry-run] [--limit N]")
    print("  python translate_descriptions.py --target ar --fix-identical")
    print("  ... (de, es, fr, it, ja, ko, ru)")


if __name__ == "__main__":
    main()
