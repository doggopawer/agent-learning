#!/usr/bin/env python3
"""Link the explicit-only learning skills into the user's Codex skill directory."""

import argparse
import json
from pathlib import Path

NAMES = ("learning-mentor", "obsidian-notes")
WORKSPACE = Path(__file__).resolve().parents[1]


def install(workspace, skills_dir):
    workspace, skills_dir = Path(workspace).resolve(), Path(skills_dir).expanduser()
    links = [(skills_dir / name, workspace / ".agents/skills" / name) for name in NAMES]
    for destination, target in links:
        if not (target / "SKILL.md").is_file():
            raise ValueError(f"missing skill: {target}")
        if destination.exists() or destination.is_symlink():
            if not destination.is_symlink() or destination.resolve() != target:
                raise ValueError(f"existing skill preserved; choose another location or inspect it: {destination}")
    skills_dir.mkdir(parents=True, exist_ok=True)
    for destination, target in links:
        if not destination.is_symlink():
            destination.symlink_to(target, target_is_directory=True)
    return {"skills_dir": str(skills_dir), "skills": list(NAMES), "invocation": "$learning-mentor"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path, default=Path.home() / ".agents/skills")
    args = parser.parse_args()
    try:
        print(json.dumps(install(WORKSPACE, args.skills_dir), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError) as exc:
        parser.exit(2, f"install_skills: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
