"""Shared project registry for the independent learning workspace (stdlib only)."""

import hashlib
import json
import os
from pathlib import Path
import re
import tempfile


def valid_id(value):
    return isinstance(value, str) and value != "concepts" and bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value))


def load(workspace):
    workspace = Path(workspace).resolve()
    config = json.loads((workspace / "projects.json").read_text(encoding="utf-8"))
    if config.get("schema_version") != 1 or not isinstance(config.get("projects"), dict):
        raise ValueError("invalid projects.json")
    return config


def source_root(workspace, value):
    workspace = Path(workspace).resolve()
    root = (workspace / value).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("source project must be a directory")
    if root.is_relative_to(workspace) or workspace.is_relative_to(root):
        raise ValueError("source project and learning workspace must be separate")
    return root


def resolve(workspace, project_id):
    config = load(workspace)
    if not valid_id(project_id) or project_id not in config["projects"]:
        raise ValueError(f"unknown project_id: {project_id!r}; launch learn from that project first")
    return source_root(workspace, config["projects"][project_id]["root"])


def register(workspace, root, *, save=True):
    """Register only the explicitly selected path; never silently retarget an id."""
    workspace = Path(workspace).resolve()
    root = source_root(workspace, root)
    config = load(workspace)
    entries = config["projects"]
    for project_id, entry in entries.items():
        if (workspace / entry["root"]).resolve() == root:
            if not valid_id(project_id):
                raise ValueError("invalid registered project id")
            return project_id
    base = re.sub(r"[^a-z0-9]+", "-", root.name.lower()).strip("-") or "project"
    if base == "concepts":
        base = "project-concepts"
    project_id = base
    if project_id in entries:
        project_id += "-" + hashlib.sha256(str(root).encode()).hexdigest()[:10]
    if project_id in entries:
        raise ValueError("project id collision; assign a distinct id in projects.json")
    entries[project_id] = {"name": root.name, "root": os.path.relpath(root, workspace)}
    if save:
        target = workspace / "projects.json"
        if target.is_symlink():
            raise ValueError("projects.json must not be a symlink")
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=workspace, delete=False) as temp:
            json.dump(config, temp, ensure_ascii=False, indent=2)
            temp.write("\n")
            temporary = temp.name
        try:
            os.replace(temporary, target)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
    return project_id
