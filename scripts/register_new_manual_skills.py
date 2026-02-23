"""
Register newly added manual skills with skills.sh via `npx skills add`.

Usage:
    python scripts/register_new_manual_skills.py [--prev-json PATH]

By default, compares data/manual_skills.json against HEAD~1 to detect new entries.
Pass --prev-json to supply the previous version explicitly.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def load_skills(path: str) -> dict[str, dict]:
    """Return {source/skillId: skill_entry} from a manual_skills.json file."""
    try:
        with open(path) as f:
            data = json.load(f)
        return {f"{s['source']}/{s['skillId']}": s for s in data.get("skills", [])}
    except Exception as e:
        print(f"Warning: could not load {path}: {e}", file=sys.stderr)
        return {}


def get_prev_skills_from_git() -> dict[str, dict]:
    """Read the previous commit's manual_skills.json via git show HEAD~1."""
    result = subprocess.run(
        ["git", "show", "HEAD~1:data/manual_skills.json"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("Could not read HEAD~1 (first commit or shallow clone) — treating all skills as new")
        return {}
    try:
        data = json.loads(result.stdout)
        return {f"{s['source']}/{s['skillId']}": s for s in data.get("skills", [])}
    except Exception as e:
        print(f"Warning: could not parse HEAD~1 manual_skills.json: {e}", file=sys.stderr)
        return {}


def register_skill(skill_path: str) -> bool:
    print(f"  npx skills add {skill_path}")
    result = subprocess.run(
        ["npx", "--yes", "skills", "add", skill_path],
        capture_output=True,
        text=True,
    )
    output = result.stdout.strip() or result.stderr.strip()
    if result.returncode == 0:
        print(f"  ✓ {skill_path}")
        if output:
            print(f"    {output}")
        return True
    else:
        print(f"  ✗ {skill_path}: {output}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Register new manual skills with skills.sh")
    parser.add_argument(
        "--prev-json",
        default=None,
        help="Path to the previous manual_skills.json for comparison (default: use HEAD~1 from git)",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent
    current_path = repo_root / "data" / "manual_skills.json"

    current = load_skills(str(current_path))
    prev = load_skills(args.prev_json) if args.prev_json else get_prev_skills_from_git()

    new_skills = sorted(set(current.keys()) - set(prev.keys()))

    if not new_skills:
        print("No new manual skills to register")
        return

    print(f"Registering {len(new_skills)} new skill(s) with skills.sh...")
    failed = []
    for skill_path in new_skills:
        if not register_skill(skill_path):
            failed.append(skill_path)

    if failed:
        print(f"\n{len(failed)} skill(s) failed to register:", file=sys.stderr)
        for s in failed:
            print(f"  - {s}", file=sys.stderr)
        # Non-fatal: don't block the rest of the workflow
        sys.exit(0)


if __name__ == "__main__":
    main()
