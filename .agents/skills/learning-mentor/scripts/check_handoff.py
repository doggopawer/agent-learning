#!/usr/bin/env python3
"""Check recorded handoff prerequisites. Never grant authority or implement code."""

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
import projects

DIMENSIONS = ("technical", "business", "code")


def scope_digest(scope):
    return hashlib.sha256(json.dumps(scope, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def timestamp(value):
    if not isinstance(value, str):
        raise ValueError("missing timestamp")
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError("timestamp needs a timezone")
    return parsed


def relative_file(project, value, must_exist=True):
    if not nonempty(value):
        raise ValueError("invalid relative path")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or any(p.startswith(".") for p in path.parts):
        raise ValueError("path must stay in the source project")
    resolved = (project / path).resolve(strict=must_exist)
    if not resolved.is_relative_to(project):
        raise ValueError("path escaped source project")
    return resolved


def evaluate(record, project):
    project = Path(project).resolve()
    reasons = []
    if not isinstance(record, dict):
        return {"eligible": False, "reasons": ["record must be an object"]}
    if record.get("schema_version") != 2 or not nonempty(record.get("task_id")):
        reasons.append("invalid record version or task id")
    scope = record.get("scope")
    digest = scope_digest(scope)
    if not isinstance(scope, dict) or not nonempty(scope.get("goal")) or not isinstance(scope.get("allowed_paths"), list) or not scope.get("allowed_paths") or not isinstance(scope.get("exclusions"), list):
        reasons.append("concrete implementation scope is missing")
    else:
        if not projects.valid_id(scope.get("project_id")) or scope.get("project_root") != str(project):
            reasons.append("scope does not identify the current source project")
        for path in scope["allowed_paths"]:
            try:
                relative_file(project, path, must_exist=False)
            except (OSError, ValueError) as exc:
                reasons.append(str(exc))
    assessments = record.get("assessments")
    if not isinstance(assessments, dict):
        assessments = {}
    for dimension in DIMENSIONS:
        item = assessments.get(dimension)
        if not isinstance(item, dict) or item.get("status") != "passed":
            reasons.append(f"{dimension}: not passed")
        elif not all(nonempty(item.get(key)) for key in ("question", "answer", "evidence", "reason")):
            reasons.append(f"{dimension}: missing answer or assessment evidence")
    if record.get("assessed_scope_sha256") != digest:
        reasons.append("scope is unassessed or changed")
    try:
        passed_at = timestamp(record.get("passed_at"))
    except ValueError:
        passed_at = None
        reasons.append("valid assessment completion time is missing")
    approval = record.get("approval")
    if not isinstance(approval, dict):
        approval = {}
    if approval.get("status") != "approved" or not all(nonempty(approval.get(key)) for key in ("message", "evidence")):
        reasons.append("explicit user approval and its conversation evidence are missing")
    if approval.get("scope_sha256") != digest:
        reasons.append("approval does not cover the current scope")
    try:
        approved_at = timestamp(approval.get("at"))
        if passed_at is None or approved_at <= passed_at:
            reasons.append("approval must follow the completed assessment")
    except ValueError:
        reasons.append("valid approval time is missing")
    sources = record.get("sources")
    if not isinstance(sources, list) or not sources:
        reasons.append("source fingerprints are missing")
    else:
        for entry in sources:
            try:
                if not isinstance(entry, dict):
                    raise ValueError("invalid source entry")
                path = relative_file(project, entry.get("path"))
                if hashlib.sha256(path.read_bytes()).hexdigest() != entry.get("sha256"):
                    reasons.append(f"source changed: {entry.get('path')}")
            except (OSError, ValueError) as exc:
                reasons.append(f"source unavailable: {exc}")
    return {"eligible": not reasons, "current_scope_sha256": digest, "reasons": reasons,
            "limit": "Checks record consistency only; mentor must verify actual answers and approval against the conversation. No product files are changed."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    parser.add_argument("--workspace", type=Path, default=Path(__file__).resolve().parents[4])
    args = parser.parse_args()
    try:
        record = json.loads(args.record.read_text())
        project = projects.resolve(args.workspace, record["scope"]["project_id"])
        result = evaluate(record, project)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        result = {"eligible": False, "reasons": [str(exc)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["eligible"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
