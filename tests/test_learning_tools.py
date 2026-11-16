"""Synthetic fixtures only: these tests do not assess or approve the real user."""

from copy import deepcopy
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def module(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


notes = module("learning_notes", ".agents/skills/obsidian-notes/scripts/notes.py")
gate = module("learning_gate", ".agents/skills/learning-mentor/scripts/check_handoff.py")


class LearningToolsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="learning-tools-test-")
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name).resolve()
        self.workspace = base / "learning"
        self.project = base / "source"
        self.workspace.mkdir()
        self.project.mkdir()
        (self.project / "Service.java").write_text("class Service { void createCompany() {} }\n")
        (self.project / "design.md").write_text("# Design\nKeep company and account separate.\n")
        (self.workspace / "projects.json").write_text(json.dumps({"schema_version": 1, "projects": {"source": {"name": "Source", "root": "../source"}}, "timezone": "Asia/Seoul"}))
        self.payload = {
            "kind": "project", "project_id": "source", "slug": "company", "title": "회사 생성", "summary": "회사 생성 학습",
            "why": "업무 책임을 이해하기 위해", "business_rules": ["회사와 계정을 구분한다"],
            "flow": "Controller → Service", "design_reasoning": "design.md 기준의 분리",
            "questions": ["계정은 언제 생성하는가?"],
            "sources": [{"role": "code", "path": "Service.java", "symbol": "createCompany", "purpose": "업무 진입점"},
                        {"role": "design", "path": "design.md", "purpose": "분리의 근거"}],
        }
        scope = {"project_id": "source", "project_root": str(self.project.resolve()), "goal": "합성 테스트 범위", "allowed_paths": ["Service.java"], "exclusions": ["실제 제품 작업"]}
        digest = gate.scope_digest(scope)
        self.record = {
            "schema_version": 2, "task_id": "synthetic-only", "scope": scope,
            "sources": [{"path": "Service.java", "sha256": hashlib.sha256((self.project / "Service.java").read_bytes()).hexdigest()}],
            "assessments": {dimension: {"status": "passed", "question": "합성 질문", "answer": "합성 답변",
                            "evidence": "unit-test fixture only", "reason": "기록 형식 테스트용"} for dimension in gate.DIMENSIONS},
            "passed_at": "2026-11-16T10:00:00+09:00", "assessed_scope_sha256": digest,
            "approval": {"status": "approved", "message": "합성 테스트의 승인 문구", "evidence": "fixture only",
                         "at": "2026-11-16T10:01:00+09:00", "scope_sha256": digest},
        }

    def test_unanswered_is_blocked(self):
        self.record["assessments"]["technical"].update(status="pending", answer="")
        self.assertFalse(gate.evaluate(self.record, self.project)["eligible"])

    def test_pass_label_without_answer_evidence_is_blocked(self):
        self.record["assessments"]["code"]["evidence"] = ""
        self.assertFalse(gate.evaluate(self.record, self.project)["eligible"])

    def test_passed_but_unapproved_is_blocked(self):
        self.record["approval"]["status"] = "pending"
        self.assertFalse(gate.evaluate(self.record, self.project)["eligible"])

    def test_premature_approval_is_blocked(self):
        self.record["approval"]["at"] = "2026-11-16T09:59:00+09:00"
        self.assertFalse(gate.evaluate(self.record, self.project)["eligible"])

    def test_changed_scope_is_blocked(self):
        self.record["scope"]["allowed_paths"].append("OtherService.java")
        self.assertFalse(gate.evaluate(self.record, self.project)["eligible"])

    def test_changed_source_is_blocked(self):
        (self.project / "Service.java").write_text("class Service { void changed() {} }\n")
        self.assertFalse(gate.evaluate(self.record, self.project)["eligible"])

    def test_complete_record_is_eligible_and_read_only(self):
        before = {p.name: p.read_bytes() for p in self.project.iterdir()}
        original_record = deepcopy(self.record)
        self.assertTrue(gate.evaluate(self.record, self.project)["eligible"])
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.project.iterdir()})
        self.assertEqual(original_record, self.record)

    def test_note_update_preserves_manual_text_and_metadata(self):
        first = notes.upsert(self.workspace, self.payload)
        target = Path(first["path"])
        target.write_text(target.read_text().replace("learning_status: learning", "learning_status: learning\nmy_property: keep") + "\n나만의 필기: 반드시 유지\n")
        self.payload["summary"] = "갱신한 설명"
        notes.upsert(self.workspace, self.payload)
        content = target.read_text()
        self.assertIn("나만의 필기: 반드시 유지", content)
        self.assertIn("my_property: keep", content)
        self.assertIn("갱신한 설명", content)
        self.assertEqual(1, content.count(notes.START))
        self.assertEqual("unchanged", notes.upsert(self.workspace, self.payload)["action"])
        self.assertFalse(notes.check(self.workspace)["errors"])

    def test_unmanaged_note_is_not_overwritten(self):
        target = self.workspace / "notes/projects/source/company.md"
        target.parent.mkdir(parents=True)
        target.write_text("기존 사용자 문서")
        with self.assertRaises(ValueError):
            notes.upsert(self.workspace, self.payload)
        self.assertEqual("기존 사용자 문서", target.read_text())

    def test_path_escape_and_symlink_cannot_write_source(self):
        invalid = deepcopy(self.payload)
        invalid["slug"] = "../../source/design"
        with self.assertRaises(ValueError):
            notes.upsert(self.workspace, invalid)
        vault = self.workspace / "notes"
        vault.mkdir()
        (vault / "projects").mkdir()
        (vault / "projects/source").symlink_to(self.project, target_is_directory=True)
        with self.assertRaises(ValueError):
            notes.upsert(self.workspace, self.payload)
        self.assertFalse((self.project / "company.md").exists())

    def test_missing_symbol_does_not_create_note(self):
        self.payload["sources"][0]["symbol"] = "doesNotExist"
        with self.assertRaises(ValueError):
            notes.upsert(self.workspace, self.payload)
        self.assertFalse((self.workspace / "notes/projects/source/company.md").exists())

    def test_source_reference_cannot_escape_project(self):
        self.payload["sources"][0]["path"] = "../learning/projects.json"
        with self.assertRaises(ValueError):
            notes.upsert(self.workspace, self.payload)

    def test_note_detects_stale_source(self):
        notes.upsert(self.workspace, self.payload)
        (self.project / "Service.java").write_text("class Service { void changed() {} }\n")
        self.assertTrue(notes.check(self.workspace)["errors"])

    def test_input_cannot_claim_understanding_passed(self):
        self.payload["learning_status"] = "passed"
        with self.assertRaises(ValueError):
            notes.upsert(self.workspace, self.payload)

    def test_two_projects_with_same_name_and_note_slug_stay_separate(self):
        first = Path(notes.upsert(self.workspace, self.payload)["path"])
        other = self.workspace.parent / "other/source"
        shutil.copytree(self.project, other)
        other_id = notes.projects.register(self.workspace, other)
        self.assertNotEqual("source", other_id)
        other_payload = deepcopy(self.payload)
        other_payload.update(project_id=other_id, summary="다른 프로젝트의 설명")
        second = Path(notes.upsert(self.workspace, other_payload)["path"])
        self.assertNotEqual(first, second)
        self.assertNotIn("다른 프로젝트의 설명", first.read_text())
        self.assertEqual(other_id, notes.projects.register(self.workspace, other))
        self.assertFalse(notes.check(self.workspace)["errors"])

    def test_concept_note_needs_no_project_or_fake_code(self):
        concept = deepcopy(self.payload)
        concept.update(kind="concept", project_id=None, sources=[])
        result = notes.upsert(self.workspace, concept)
        self.assertEqual(self.workspace / "notes/concepts/company.md", Path(result["path"]))
        self.assertNotIn("learning:source", Path(result["path"]).read_text())
        self.assertFalse(notes.check(self.workspace)["errors"])
        concept["project_id"] = "source"
        with self.assertRaises(ValueError):
            notes.upsert(self.workspace, concept)

    def test_python_project_without_adr_is_supported(self):
        (self.project / "main.py").write_text("def create_company():\n    return 1\n")
        self.payload["sources"] = [{"path": "main.py", "role": "code", "symbol": "create_company", "purpose": "처리 흐름"}]
        self.payload["design_reasoning"] = "설계 문서 없음. 아래 분리 이유는 멘토의 해석이다."
        notes.upsert(self.workspace, self.payload)
        self.assertFalse(notes.check(self.workspace)["errors"])

    def test_record_and_note_cannot_silently_retarget_another_checkout(self):
        notes.upsert(self.workspace, self.payload)
        other = self.workspace.parent / "copy"
        shutil.copytree(self.project, other)
        self.assertFalse(gate.evaluate(self.record, other)["eligible"])
        config_path = self.workspace / "projects.json"
        config = json.loads(config_path.read_text())
        config["projects"]["source"]["root"] = "../copy"
        config_path.write_text(json.dumps(config))
        self.assertTrue(notes.check(self.workspace)["errors"])
        self.record["scope"].update(project_id="copy", project_root=str(other))
        self.assertFalse(gate.evaluate(self.record, other)["eligible"])

    def test_launcher_uses_explicit_skills_and_keeps_source_outside_writable_root(self):
        shutil.copy(ROOT / "learn", self.workspace / "learn")
        shutil.copytree(ROOT / "scripts", self.workspace / "scripts")
        binary = self.workspace.parent / "bin"
        binary.mkdir()
        fake = binary / "codex"
        fake.write_text("#!/usr/bin/env python3\nimport json, sys\nprint(json.dumps(sys.argv[1:]))\n")
        fake.chmod(0o755)
        env = {**os.environ, "PATH": str(binary) + os.pathsep + os.environ["PATH"]}
        source = self.workspace.parent / "a project with spaces"
        source.mkdir()
        topic = '트랜잭션 $literal `whoami` ; $(touch unexpected-file)'
        original = (self.workspace / "projects.json").read_bytes()
        command = [sys.executable, str(self.workspace / "learn"), "--project", str(source), topic]
        preview = subprocess.run(command + ["--dry-run"], env=env, cwd=source, capture_output=True, text=True, check=True)
        self.assertEqual(original, (self.workspace / "projects.json").read_bytes())
        argv = json.loads(preview.stdout)["argv"][1:]
        launched = subprocess.run(command, env=env, cwd=source, capture_output=True, text=True, check=True)
        self.assertEqual(argv, json.loads(launched.stdout))
        self.assertEqual(["--cd", str(self.workspace), "--sandbox", "workspace-write"], argv[:4])
        self.assertNotIn("--add-dir", argv)
        self.assertIn("$learning-mentor", argv[-1])
        self.assertIn("$obsidian-notes", argv[-1])
        self.assertEqual(topic, json.loads(argv[-1].splitlines()[-1])["topic"])
        self.assertEqual([], list(source.iterdir()))

    def test_launcher_selects_current_project_and_concept_mode(self):
        shutil.copy(ROOT / "learn", self.workspace / "learn")
        shutil.copytree(ROOT / "scripts", self.workspace / "scripts")
        binary = self.workspace.parent / "bin"
        binary.mkdir()
        fake = binary / "codex"
        fake.write_text("#!/bin/sh\nexit 99\n")
        fake.chmod(0o755)
        env = {**os.environ, "PATH": str(binary) + os.pathsep + os.environ["PATH"]}
        launch = [sys.executable, str(self.workspace / "learn"), "--dry-run"]
        result = subprocess.run(launch, cwd=self.project, env=env, capture_output=True, text=True, check=True)
        self.assertEqual(str(self.project), json.loads(result.stdout)["context"]["source_root"])
        result = subprocess.run(launch + ["--concept", "트랜잭션"], cwd=self.workspace, env=env, capture_output=True, text=True, check=True)
        self.assertEqual("concept", json.loads(result.stdout)["context"]["mode"])
        self.assertNotIn("project_id", json.loads(result.stdout)["context"])


if __name__ == "__main__":
    unittest.main()
