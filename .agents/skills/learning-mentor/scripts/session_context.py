#!/usr/bin/env python3
"""Select the current project and keep learning records in the shared workspace."""

import argparse
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
WORKSPACE = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(WORKSPACE / "scripts"))
import projects


def select(workspace, cwd, *, source=None, concept=False, preview=False):
    workspace = Path(workspace).resolve()
    result = {"workspace": str(workspace), "vault": str(workspace / "notes")}
    if concept:
        return {**result, "mode": "concept", "project_id": None}
    root = Path(source if source is not None else cwd).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError("source project must be a directory")
    if source is None:
        git = subprocess.run(["git", "-C", str(root), "rev-parse", "--show-toplevel"], capture_output=True, text=True)
        if git.returncode == 0:
            root = Path(git.stdout.strip()).resolve()
    if root.is_relative_to(workspace) or workspace.is_relative_to(root):
        return {**result, "mode": "needs-project", "question": "어느 프로젝트의 무엇을 공부하고 싶으세요?"}
    project_id = projects.register(workspace, root, save=not preview)
    return {**result, "mode": "project", "project_id": project_id, "source_root": str(root)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group()
    choice.add_argument("--source", type=Path, help="explicit project path; defaults to the caller's project")
    choice.add_argument("--concept", action="store_true")
    parser.add_argument("--preview", action="store_true", help="do not update the project registry")
    args = parser.parse_args()
    try:
        result = select(WORKSPACE, Path.cwd(), source=args.source, concept=args.concept, preview=args.preview)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f"session_context: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
