#!/usr/bin/env python3
"""
Batch translate description_en.txt to description_cn.txt (using free Google Translate)

Usage:
    # Translate all missing Chinese descriptions
    python translate_descriptions.py
    
    # Only translate first 100 files (for testing)
    python translate_descriptions.py --limit 100
    
    # Start translation from file 200 (resume from checkpoint)
    python translate_descriptions.py --skip 200
    
    # Test mode
    python translate_descriptions.py --dry-run

    # Translate to Traditional Chinese (writes description_tw.txt by default)
    python translate_descriptions.py --target zh-TW

    # Translate to another language (writes description_<lang>.txt by default)
    python translate_descriptions.py --target ja
"""

import sys
import time
import argparse
from pathlib import Path
import os

# Base directory
BASE_DIR = Path(__file__).parent.parent / "data" / "skills-md"

_translator_cache: dict[tuple[str, str], object] = {}


def output_filename_for_target(target: str) -> str:
    """
    Decide output filename for a target language.

    Backward compatibility:
      - zh-CN -> description_cn.txt  (website expects this today)
      - zh-TW -> description_tw.txt
      - others -> description_<lang>.txt (sanitized)
    """
    t = (target or "").strip()
    t_norm = t.lower().replace("_", "-")
    if t_norm in {"zh-cn", "zh-hans", "zh-hans-cn"}:
        return "description_cn.txt"
    if t_norm in {"zh-tw", "zh-hant", "zh-hant-tw"}:
        return "description_tw.txt"
    safe = "".join(c if c.isalnum() or c in {"-", "_"} else "_" for c in t_norm).strip("_")
    safe = safe.replace("-", "_")
    return f"description_{safe or 'translated'}.txt"


def find_all_en_files() -> list[Path]:
    """Find all English description files that need translation.

    If the target translation file already exists (even if empty), we treat it as
    "already handled" to avoid overwriting manual edits.
    """
    en_files = []
    for en_file in BASE_DIR.rglob("description_en.txt"):
        out_file = en_file.parent / output_filename_for_target("zh-CN")
        # Only process files that don't have the default translation yet
        if not out_file.exists():
            en_files.append(en_file)
    return sorted(en_files)


def translate_with_google(text: str, source_lang: str, target_lang: str) -> str:
    """Translate using Google Translate (free)"""
    try:
        from deep_translator import GoogleTranslator
    except ImportError:
        print("Please install deep-translator: pip install deep-translator")
        sys.exit(1)
    
    key = (source_lang, target_lang)
    translator = _translator_cache.get(key)
    if translator is None:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        _translator_cache[key] = translator

    def _reset_translator() -> None:
        # In practice, Google Translate can temporarily block or return None.
        # Recreating the translator instance sometimes helps.
        _translator_cache.pop(key, None)
        _translator_cache[key] = GoogleTranslator(source=source_lang, target=target_lang)

    # Add retry logic
    for attempt in range(3):
        try:
            result = translator.translate(text)  # type: ignore[attr-defined]
            # deep-translator can occasionally return None on transient failures.
            if result is None:
                _reset_translator()
                raise RuntimeError("GoogleTranslator returned None")
            return str(result)
        except Exception as e:
            if attempt < 2:
                _reset_translator()
                # Exponential-ish backoff. Allow overriding via env for local runs.
                base = float(os.getenv("TRANSLATE_RETRY_SLEEP_SECONDS", "3"))
                time.sleep(base * (attempt + 1))
            else:
                last_error = e

    # Fallback: MyMemory (often works when Google blocks).
    try:
        from deep_translator import MyMemoryTranslator

        def _mm_lang(code: str) -> str:
            c = (code or "").strip().lower().replace("_", "-")
            if c in {"en", "en-us", "en-gb"}:
                return "english"
            if c in {"zh-cn", "zh-hans", "zh-hans-cn"}:
                return "chinese simplified"
            if c in {"zh-tw", "zh-hant", "zh-hant-tw"}:
                return "chinese traditional"
            if c == "es":
                return "spanish"
            if c == "fr":
                return "french"
            if c == "de":
                return "german"
            if c == "ja":
                return "japanese"
            if c == "ko":
                return "korean"
            return code

        mm = MyMemoryTranslator(source=_mm_lang(source_lang), target=_mm_lang(target_lang))
        res = mm.translate(text)
        if res is None:
            raise RuntimeError("MyMemoryTranslator returned None")
        return str(res)
    except Exception as e:
        # Re-raise the last Google error if available; otherwise raise MyMemory error.
        try:
            raise last_error  # type: ignore[misc]
        except Exception:
            raise e


# ============= Main translation logic =============

def translate_file(
    en_file: Path,
    *,
    dry_run: bool = False,
    force: bool = False,
    source_lang: str = "en",
    target_lang: str = "zh-CN",
) -> tuple[Path, bool, str]:
    """Translate a single file.

    Safety: if the output translation file already exists, we skip unless --force is provided.
    This prevents overwriting manually authored translations (or translations generated earlier).
    """
    try:
        out_name = output_filename_for_target(target_lang)
        out_file = en_file.parent / out_name
        if out_file.exists() and not force:
            return en_file, True, f"Skipped ({out_name} already exists)"

        # Read English content
        en_text = en_file.read_text(encoding="utf-8").strip()
        
        if not en_text:
            return en_file, False, "Empty file"
        
        # If the "English" file is actually Chinese and target is Chinese, copy directly.
        if target_lang.lower().startswith("zh"):
            chinese_chars = sum(1 for c in en_text if "\u4e00" <= c <= "\u9fff")
            if len(en_text) > 0 and chinese_chars / len(en_text) > 0.3:
                out_text = en_text
            else:
                out_text = translate_with_google(en_text, source_lang=source_lang, target_lang=target_lang)
        else:
            out_text = translate_with_google(en_text, source_lang=source_lang, target_lang=target_lang)
        if out_text is None:
            raise RuntimeError("Translation output is None")
        out_text = str(out_text)
        
        # Write translated file
        if not dry_run:
            out_file.write_text(out_text + "\n", encoding="utf-8")
        
        return en_file, True, out_text[:50] + "..." if len(out_text) > 50 else out_text
        
    except Exception as e:
        return en_file, False, str(e)


def main():
    parser = argparse.ArgumentParser(description="Batch translate description_en.txt to description_cn.txt (Google Translate)")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of files to translate (0 for all)")
    parser.add_argument("--skip", type=int, default=0, help="Skip first N files")
    parser.add_argument("--dry-run", action="store_true", help="Only show files to be translated, don't actually translate")
    parser.add_argument("--force", action="store_true", help="Force re-translate existing files")
    parser.add_argument("--source", type=str, default="en", help="Source language (default: en)")
    parser.add_argument("--target", type=str, default="zh-CN", help="Target language (default: zh-CN). Example: zh-TW, ja, ko")
    parser.add_argument("--sleep", type=float, default=float(os.getenv("TRANSLATE_SLEEP_SECONDS", "0.3")), help="Sleep seconds between files (default: 0.3, overridable via TRANSLATE_SLEEP_SECONDS)")
    
    args = parser.parse_args()
    
    # Find all files that need translation
    print("Scanning files...")
    
    if args.force:
        en_files = list(BASE_DIR.rglob("description_en.txt"))
    else:
        # In non-force mode, only translate missing files for the selected target.
        en_files = []
        out_name = output_filename_for_target(args.target)
        for en_file in BASE_DIR.rglob("description_en.txt"):
            out_file = en_file.parent / out_name
            if not out_file.exists():
                en_files.append(en_file)
    
    en_files = sorted(en_files)
    
    # Apply skip and limit
    if args.skip > 0:
        en_files = en_files[args.skip:]
    if args.limit > 0:
        en_files = en_files[:args.limit]
    
    total = len(en_files)
    print(f"Found {total} files to translate")
    
    if total == 0:
        print("No files need translation")
        return
    
    if args.dry_run:
        print("\n[DRY RUN] The following files will be translated:")
        for f in en_files[:20]:
            print(f"  - {f.relative_to(BASE_DIR)}")
        if total > 20:
            print(f"  ... and {total - 20} more files")
        return
    
    # Start translation
    out_name = output_filename_for_target(args.target)
    print(f"\nStarting translation (using Google Translate)...")
    print(f"Source: {args.source}  Target: {args.target}  Output: {out_name}")
    print("-" * 60)
    
    completed = 0
    failed = 0
    start_time = time.time()
    
    for en_file in en_files:
        en_file, success, message = translate_file(
            en_file,
            dry_run=args.dry_run,
            force=args.force,
            source_lang=args.source,
            target_lang=args.target,
        )
        completed += 1
        
        if success:
            print(f"[{completed}/{total}] ✓ {en_file.parent.name}: {message}")
        else:
            failed += 1
            print(f"[{completed}/{total}] ✗ {en_file.parent.name}: {message}")
        
        # Show progress
        if completed % 100 == 0:
            elapsed = time.time() - start_time
            rate = completed / elapsed
            remaining = (total - completed) / rate if rate > 0 else 0
            print(f"\n--- Progress: {completed}/{total} ({completed/total*100:.1f}%), "
                  f"Rate: {rate:.1f}/sec, Estimated remaining: {remaining/60:.1f} min ---\n")
        
        # Add delay to avoid rate limiting
        time.sleep(max(0.0, float(args.sleep)))
    
    # Final statistics
    elapsed = time.time() - start_time
    print("\n" + "=" * 60)
    print(f"Translation completed!")
    print(f"  Success: {completed - failed}")
    print(f"  Failed: {failed}")
    print(f"  Time: {elapsed/60:.1f} min")
    print(f"  Rate: {completed/elapsed:.1f} files/sec")


if __name__ == "__main__":
    main()
