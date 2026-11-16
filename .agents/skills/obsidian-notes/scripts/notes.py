#!/usr/bin/env python3
"""Create managed learning notes; read project evidence without modifying it."""

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import sys
from zoneinfo import ZoneInfo

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
import projects

START = "<!-- learning:auto:start -->"
END = "<!-- learning:auto:end -->"
SOURCE = re.compile(r"^<!-- learning:source (.+) -->$", re.MULTILINE)
CONTEXT = re.compile(r"^<!-- learning:context (.+) -->$", re.MULTILINE)


def context(workspace, project_id=None):
    workspace = Path(workspace).resolve()
    config = projects.load(workspace)
    project = projects.resolve(workspace, project_id) if project_id is not None else None
    vault = workspace / "notes"
    if not vault.resolve().is_relative_to(workspace):
        raise ValueError("notes must remain inside the learning workspace")
    if project and (vault.resolve().is_relative_to(project) or project.is_relative_to(vault.resolve())):
        raise ValueError("source project and notes must be separate")
    return workspace, config, project, vault


def source_file(project, relative):
    if not isinstance(relative, str) or not relative or any(c in relative for c in "\n\r<>|\\"):
        raise ValueError("invalid source path")
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts or any(p.startswith(".") for p in path.parts):
        raise ValueError("source must be a non-hidden project-relative file")
    resolved = (project / path).resolve(strict=True)
    if not resolved.is_relative_to(project) or not resolved.is_file():
        raise ValueError("source escaped the project or is not a file")
    if resolved.suffix.lower() in {".pem", ".key", ".p12", ".pfx", ".class", ".jar"}:
        raise ValueError("unsupported source file")
    if resolved.stat().st_size > 2_000_000:
        raise ValueError("source is too large for a learning reference")
    return resolved


def text_field(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be nonempty text")
    if "<!-- learning:" in value:
        raise ValueError("reserved learning marker in input")
    return value.strip()


def lines_field(value, label):
    if not isinstance(value, list) or not value:
        raise ValueError(f"{label} must be a nonempty list")
    return [text_field(item, label) for item in value]


def evidence(project, entry):
    if not isinstance(entry, dict):
        raise ValueError("source entry must be an object")
    path = source_file(project, entry.get("path"))
    raw = path.read_bytes()
    content = raw.decode("utf-8")
    symbol = entry.get("symbol", "")
    if not isinstance(symbol, str) or "\n" in symbol:
        raise ValueError("invalid symbol")
    if symbol and symbol not in content:
        raise ValueError(f"symbol not found: {symbol} in {entry['path']}")
    line = content[:content.index(symbol)].count("\n") + 1 if symbol else None
    return {
        "path": entry["path"], "symbol": symbol, "line": line,
        "role": entry.get("role"),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "purpose": text_field(entry.get("purpose"), "source purpose"),
        "uri": path.as_uri(),
    }


def render(payload, project, config):
    required = {"kind", "project_id", "slug", "title", "summary", "why", "business_rules", "flow", "design_reasoning", "questions", "sources"}
    if not isinstance(payload, dict) or set(payload) != required:
        raise ValueError("note input must contain exactly the documented fields")
    slug = payload["slug"]
    if not isinstance(slug, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise ValueError("invalid note slug")
    strings = {k: text_field(payload[k], k) for k in ("title", "summary", "why", "flow", "design_reasoning")}
    business = lines_field(payload["business_rules"], "business_rules")
    questions = lines_field(payload["questions"], "questions")
    if not isinstance(payload["sources"], list):
        raise ValueError("sources must be a list")
    kind = payload["kind"]
    if kind == "project" and project is not None:
        sources = [evidence(project, source) for source in payload["sources"]]
        if not sources or not any(s["role"] == "code" for s in sources):
            raise ValueError("project notes require at least one actual code reference with role: code")
        if any(s["role"] not in {"code", "design", "business"} for s in sources):
            raise ValueError("source role must be code, design or business")
        result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=project, capture_output=True, text=True)
        head = result.stdout.strip() if result.returncode == 0 else "not-a-git-repository"
    elif kind == "concept" and payload["project_id"] is None and not payload["sources"]:
        sources, head = [], None
    else:
        raise ValueError("use project + project_id + sources, or concept + null project_id + empty sources")
    date = datetime.now(ZoneInfo(config.get("timezone", "Asia/Seoul"))).date().isoformat()
    metadata = {"kind": kind, "project_id": payload["project_id"]}
    parts = [START, "<!-- learning:context " + json.dumps(metadata, ensure_ascii=False) + " -->",
             f"확인일: {date} · 이번 학습의 제품 실행 검증: 미실행"]
    if head is not None:
        parts.append(f"\n프로젝트: `{payload['project_id']}` · 코드 읽기 확인 · Git HEAD: `{head}`. 개별 해시는 커밋되지 않은 파일 내용도 포함한다.")
    else:
        parts.append("\n공통 개념 학습: 특정 프로젝트의 코드·비즈니스 이해를 검증한 기록이 아니다.")
    for heading, body in [("한 문장으로", strings["summary"]), ("왜 필요한가", strings["why"]), ("비즈니스 규칙", "\n".join("- " + s for s in business)), ("실제 처리 흐름", strings["flow"]), ("설계 근거와 해석", strings["design_reasoning"])]:
        parts.append(f"\n## {heading}\n\n{body}")
    if sources:
        parts.append("\n## 실제 코드와 설계 근거\n\n외부 파일 링크는 원본 파일을 여는 용도다. 경로·심볼은 원본 저장소 기준이고, 행은 심볼의 첫 출현 위치를 찾는 힌트다.")
    for item in sources:
        hint = f" · `{item['symbol']}` · {item['line']}행 부근" if item["symbol"] else ""
        parts.append(f"\n- [{item['path']}]({item['uri']}){hint}\n  - 근거: {item['purpose']}\n  - SHA-256: `{item['sha256']}`")
        stored = {k: item[k] for k in ("path", "symbol", "sha256")}
        stored.update(project_id=payload["project_id"], project_root=str(project))
        parts.append("<!-- learning:source " + json.dumps(stored, ensure_ascii=False) + " -->")
    parts.append("\n## 문서를 덮고 답하기\n\n" + "\n".join(f"{i}. {q}" for i, q in enumerate(questions, 1)))
    parts.append(END)
    return slug, strings["title"], date, "\n".join(parts)


def upsert(workspace, payload):
    if not isinstance(payload, dict):
        raise ValueError("note input must be an object")
    _, config, project, vault = context(workspace, payload.get("project_id"))
    slug, title, date, block = render(payload, project, config)
    kind = payload["kind"]
    directory = vault / "concepts" if kind == "concept" else vault / "projects" / payload["project_id"]
    destination = directory / f"{slug}.md"
    if destination.is_symlink() or not destination.resolve().is_relative_to(vault.resolve()):
        raise ValueError("unsafe note destination")
    if destination.exists():
        old = destination.read_text()
        if old.count(START) != 1 or old.count(END) != 1 or old.index(START) >= old.index(END):
            raise ValueError("existing note has no unique managed region; merge manually")
        new = old[:old.index(START)] + block + old[old.index(END) + len(END):]
        if new == old:
            return {"path": str(destination), "action": "unchanged"}
        action = "updated"
    else:
        quoted = json.dumps(title, ensure_ascii=False)
        project_field = json.dumps(payload["project_id"], ensure_ascii=False)
        index = "../index.md" if kind == "concept" else "../../index.md"
        new = f'---\ntitle: {quoted}\ntype: {kind}\nproject_id: {project_field}\nlearning_status: learning\nexperiment_status: not-run\ncreated: "{date}"\ntags: [learning]\n---\n\n# {title}\n\n[학습 목차]({index})\n\n{block}\n\n## 내 설명과 질문\n\n아직 답변하지 않음. 이 영역은 자동 갱신 시 보존된다.\n'
        action = "created"
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=destination.parent, delete=False) as temp:
        temp.write(new)
        temporary = temp.name
    try:
        os.replace(temporary, destination)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return {"path": str(destination), "action": action}


def check(workspace):
    _, _, project, vault = context(workspace)
    errors, count = [], 0
    for note in sorted(vault.rglob("*.md")):
        if note.is_symlink() or not note.resolve().is_relative_to(vault.resolve()):
            errors.append(f"unsafe note path: {note.name}")
            continue
        content = note.read_text()
        if START not in content and END not in content:
            continue
        count += 1
        if content.count(START) != 1 or content.count(END) != 1 or content.index(START) >= content.index(END):
            errors.append(f"{note.name}: invalid managed region")
            continue
        block = content[content.index(START):content.index(END)]
        refs = SOURCE.findall(block)
        try:
            contexts = CONTEXT.findall(block)
            if len(contexts) != 1:
                raise ValueError("missing or ambiguous learning context")
            metadata = json.loads(contexts[0])
            if metadata["kind"] == "project":
                project = projects.resolve(workspace, metadata["project_id"])
                expected = vault / "projects" / metadata["project_id"]
                if not refs or note.parent != expected:
                    raise ValueError("project note needs evidence and its own project directory")
            elif metadata["kind"] == "concept" and metadata["project_id"] is None and not refs and note.parent == vault / "concepts":
                project = None
            else:
                raise ValueError("invalid concept context")
        except (ValueError, OSError, KeyError, TypeError) as exc:
            errors.append(f"{note.name}: {exc}")
            continue
        for encoded in refs:
            try:
                ref = json.loads(encoded)
                if ref.get("project_id") != metadata["project_id"] or ref.get("project_root") != str(project):
                    raise ValueError("source project identity changed")
                raw = source_file(project, ref["path"]).read_bytes()
                if hashlib.sha256(raw).hexdigest() != ref["sha256"]:
                    errors.append(f"{note.name}: changed source {ref['path']}")
                if ref.get("symbol") and ref["symbol"] not in raw.decode("utf-8"):
                    errors.append(f"{note.name}: missing symbol {ref['symbol']}")
            except (ValueError, OSError, KeyError, TypeError) as exc:
                errors.append(f"{note.name}: {exc}")
    return {"checked_notes": count, "errors": errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["upsert", "check"])
    parser.add_argument("--input", type=Path)
    parser.add_argument("--workspace", type=Path, default=Path(__file__).resolve().parents[4])
    args = parser.parse_args()
    try:
        if args.command == "upsert":
            if args.input is None:
                parser.error("upsert requires --input")
            result = upsert(args.workspace, json.loads(args.input.read_text()))
        else:
            result = check(args.workspace)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result.get("errors") else 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
