#!/usr/bin/env python3
"""
Scan for description_en.txt files whose content is NOT English (e.g. already Chinese),
then fix them by translating the content TO English and overwriting description_en.txt.

After that, translate_descriptions.py (or CI) can translate from the corrected English
to zh-CN, zh-TW, etc. This script only fixes the source en file.

Usage:
  # List all description_en.txt that are non-English (with preview)
  python fix_non_english_descriptions.py --list

  # List first 20 only
  python fix_non_english_descriptions.py --list 20

  # Fix: translate each to English and overwrite description_en.txt (requires NEVERSIGHT_API_KEY)
  python fix_non_english_descriptions.py --fix

  # Fix with dry-run (no writes)
  python fix_non_english_descriptions.py --fix --dry-run

  # Limit number of files to fix
  python fix_non_english_descriptions.py --fix --limit 100
"""

import argparse
import os
import sys
import time
from pathlib import Path

# Reuse logic from translate_descriptions (same BASE_DIR and detection)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from translate_descriptions import BASE_DIR, is_english_text, translate_with_llm


def find_non_english_en_files() -> list[tuple[Path, str]]:
    """Return [(en_file_path, content), ...] for each description_en.txt that is not primarily English."""
    out: list[tuple[Path, str]] = []
    for en_file in sorted(BASE_DIR.rglob("description_en.txt")):
        try:
            text = en_file.read_text(encoding="utf-8").strip()
        except Exception:
            continue
        if not text:
            continue
        if not is_english_text(text):
            out.append((en_file, text))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Scan/fix description_en.txt files that are actually in a non-English language"
    )
    ap.add_argument(
        "--list",
        nargs="?",
        const=0,
        type=int,
        default=None,
        metavar="N",
        help="List non-English en files; N = max to show (0 = all). No --list = no listing.",
    )
    ap.add_argument(
        "--fix",
        action="store_true",
        help="Translate each to English and overwrite description_en.txt. Requires NEVERSIGHT_API_KEY.",
    )
    ap.add_argument("--limit", type=int, default=0, help="Max files to fix (0 = all)")
    ap.add_argument("--dry-run", action="store_true", help="With --fix: do not write files")
    args = ap.parse_args()

    pairs = find_non_english_en_files()
    total = len(pairs)

    if args.list is not None:
        print(f"Found {total} description_en.txt file(s) with non-English content.\n")
        if total > 0:
            cap = args.list if args.list > 0 else total
            for i, (en_file, text) in enumerate(pairs[:cap]):
                rel = en_file.relative_to(BASE_DIR)
                preview = text.replace("\n", " ")[:70] + ("..." if len(text) > 70 else "")
                print(f"  {rel}")
                print(f"    {preview}\n")
            if total > cap:
                print(f"  ... and {total - cap} more (use --list 0 to show all)")
        print("\nTo fix (overwrite description_en.txt with English): python fix_non_english_descriptions.py --fix [--limit N]")
        if not args.fix:
            return

    if args.fix:
        if args.limit > 0:
            pairs = pairs[: args.limit]
        total = len(pairs)
        if total == 0:
            print("No non-English description_en.txt files to fix.")
            return
        if not os.getenv("NEVERSIGHT_API_KEY", "").strip():
            print("Error: NEVERSIGHT_API_KEY is not set. Required for --fix.", file=sys.stderr)
            sys.exit(1)
        print(f"Fixing {total} file(s): translate to English and overwrite description_en.txt (dry_run={args.dry_run})\n")
        ok = 0
        err = 0
        for i, (en_file, text) in enumerate(pairs):
            rel = en_file.relative_to(BASE_DIR)
            try:
                translated = translate_with_llm(text, "en")
                if not args.dry_run:
                    en_file.write_text(translated + "\n", encoding="utf-8")
                ok += 1
                print(f"[{i+1}/{total}] {rel}: OK")
            except Exception as e:
                err += 1
                print(f"[{i+1}/{total}] {rel}: FAIL {e}", file=sys.stderr)
            time.sleep(0.5)
        print(f"\nDone. OK={ok} Failed={err}")
        return

    # No --list and no --fix
    print(f"Found {len(pairs)} description_en.txt file(s) with non-English content.")
    print("Use --list to list them, or --fix to translate to English and overwrite description_en.txt.")


if __name__ == "__main__":
    main()
