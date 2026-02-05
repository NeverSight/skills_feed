#!/usr/bin/env python3
"""
Sync derived index JSON files locally.

Regenerates:
  - data/skills_index.json
  - data/skills_first_seen.json
  - data/skills_search_index.json
  - data/skills_category_index.json

By default this does NOT re-crawl skills.sh; it rebuilds indexes from the
existing data/skills.json + data/manual_skills.json.

Usage:
  python scripts/sync_indexes.py
  python scripts/sync_indexes.py --full-crawl
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"


def run(cmd: list[str], *, env: dict[str, str] | None = None) -> None:
    print(f"$ {' '.join(cmd)}", flush=True)
    subprocess.run(cmd, cwd=str(REPO_ROOT), env=env, check=True)


def _has_nonempty_lists(skills_json: Path) -> bool:
    try:
        data = json.loads(skills_json.read_text(encoding="utf-8"))
        for key in ("allTime", "trending", "hot"):
            v = data.get(key)
            if not isinstance(v, list) or len(v) == 0:
                return False
        return True
    except Exception:
        return False


def main() -> None:
    ap = argparse.ArgumentParser(description="Sync derived index JSON files locally.")
    ap.add_argument(
        "--full-crawl",
        action="store_true",
        help="Run the full crawler first (updates data/skills.json), then rebuild indexes.",
    )
    ap.add_argument(
        "--skip-search",
        action="store_true",
        help="Skip rebuilding data/skills_search_index.json",
    )
    ap.add_argument(
        "--skip-category",
        action="store_true",
        help="Skip rebuilding data/skills_category_index.json",
    )
    args = ap.parse_args()

    skills_json = DATA_DIR / "skills.json"
    if args.full_crawl:
        runner = "bun" if shutil.which("bun") else "npm"
        if runner == "bun":
            run(["bun", "run", "crawl"])
        else:
            run(["npm", "run", "-s", "crawl"])
    else:
        if not skills_json.exists():
            raise SystemExit(f"Missing {skills_json}. Run with --full-crawl.")
        if not _has_nonempty_lists(skills_json) and os.getenv("ALLOW_EMPTY_CRAWL") != "1":
            raise SystemExit(
                f"{skills_json} looks empty/invalid. Refusing to sync indexes.\n"
                f"Run with --full-crawl, or set ALLOW_EMPTY_CRAWL=1 to override."
            )

        runner = "bun" if shutil.which("bun") else "npm"
        if runner == "bun":
            run(["bun", "run", "crawl", "--", "--sync-index-only"])
        else:
            run(["npm", "run", "-s", "crawl", "--", "--sync-index-only"])

    if not args.skip_search:
        run([sys.executable, "scripts/build_skill_search_index.py"])
    if not args.skip_category:
        run([sys.executable, "scripts/build_skill_category_index.py"])

    # Print summary counts.
    idx = json.loads((DATA_DIR / "skills_index.json").read_text(encoding="utf-8"))
    search = json.loads((DATA_DIR / "skills_search_index.json").read_text(encoding="utf-8"))
    cat = json.loads((DATA_DIR / "skills_category_index.json").read_text(encoding="utf-8"))
    print(
        "Done.",
        f"skills_index.count={idx.get('count')}",
        f"skills_search_index.count={search.get('count')}",
        f"skills_category_index.skills={len((cat.get('skillToCategory') or {}))}",
        sep="\n",
    )


if __name__ == "__main__":
    main()

